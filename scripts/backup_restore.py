#!/usr/bin/env python3
"""backup_restore.py - verified local backup & restore for the Costume Director Vault.

Purpose
-------
R1.1-A data safety: produce a local, checksum-verified backup of the project,
restore it to a temporary directory, and verify byte-for-byte integrity.

Scope / exclusions
------------------
Included:
  * tracked files (when --root is a git repo: `git ls-files`), plus
  * untracked evidence under `reports/` and `11-验收/` (R1 audit evidence).
Excluded (never written to a backup, always):
  * `projects/`        - user-private material (must not leave the machine / must not enter public git)
  * `.obsidian/`       - local Obsidian GUI config (machine-specific)
  * `.git/`            - repository internals
  * `11-验收/R1/security/sandbox-*/` - regenerable sandbox copies of the whole vault
  * `__pycache__/`, `.DS_Store`, backup destination (if inside root)

Usage
-----
  python3 scripts/backup_restore.py backup --dest /tmp/r1.1-backup-XXXX [--root PATH] [--json]
  python3 scripts/backup_restore.py verify /tmp/r1.1-backup-XXXX [--json]
  python3 scripts/backup_restore.py restore /tmp/r1.1-backup-XXXX --dest /tmp/r1.1-restore-XXXX [--json]

Exit codes
----------
  0  success
  2  usage / IO error (bad path, dest inside root, missing backup, etc.)
  3  verification failure (missing file, hash mismatch, unexpected extra file)

The script never writes inside the source root and never touches git.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

EXCLUDED_DIR_NAMES = {".git", ".obsidian", "projects", "__pycache__", ".DS_Store"}
EXCLUDED_REL_PREFIXES = (
    "11-验收/R1/security/sandbox-",
    "11-验收/R1.1/security/sandbox-",
)
INCLUDE_UNTRACKED_PREFIXES = ("reports/", "11-验收/")
MANIFEST_NAME = "MANIFEST.json"
TREE_DIR = "tree"
CHUNK = 1 << 20


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def is_excluded(rel):
    parts = rel.split("/")
    if any(p in EXCLUDED_DIR_NAMES for p in parts):
        return True
    if rel == ".DS_Store" or rel.endswith("/.DS_Store"):
        return True
    if "/security/sandbox-" in rel:
        # any regenerable sandbox copy (R1/R1.1/security) is never backed up
        return True
    for pref in EXCLUDED_REL_PREFIXES:
        if rel.startswith(pref):
            return True
    return False


def git_tracked(root):
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace")
    except Exception:
        return set()
    return {p for p in out.split("\x00") if p}


def git_head(root):
    try:
        return subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, check=True, text=True,
        ).stdout.strip()
    except Exception:
        return None


def git_status_summary(root):
    """Return {'dirty': bool, 'modified': [paths], 'untracked': [paths]} (no writes)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return {"dirty": None, "modified": [], "untracked": []}
    modified, untracked = [], []
    for line in out.splitlines():
        if not line.strip():
            continue
        code, path = line[:2], line[3:].strip().strip('"')
        if code == "??":
            untracked.append(path)
        elif code.strip():
            modified.append(path)
    return {"dirty": bool(modified or untracked),
            "modified": modified[:500], "untracked": untracked[:500],
            "modified_count": len(modified), "untracked_count": len(untracked)}


def collect_files(root, dest, tracked_mode):
    """Return (files, skipped) where skipped lists unreadable candidates (with reason)."""
    root = Path(root).resolve()
    dest = Path(dest).resolve()
    tracked = git_tracked(root) if tracked_mode else set()
    files = []
    skipped = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames) if d not in EXCLUDED_DIR_NAMES]
        for name in sorted(filenames):
            p = Path(dirpath) / name
            try:
                rel = p.relative_to(root).as_posix()
            except ValueError:
                continue
            if is_excluded(rel):
                continue
            # never include the destination if it happens to nest under root
            try:
                p.resolve().relative_to(dest)
                continue
            except ValueError:
                pass
            if tracked_mode and rel not in tracked and not rel.startswith(INCLUDE_UNTRACKED_PREFIXES):
                continue
            if p.is_symlink():
                target = os.readlink(p)
                files.append((rel, "symlink", target, None))
            elif p.is_file():
                if not os.access(p, os.R_OK):
                    skipped.append({"path": rel, "reason": "unreadable (permission denied)"})
                    continue
                try:
                    size = p.stat().st_size
                except OSError as exc:
                    skipped.append({"path": rel, "reason": "stat failed: %s" % exc})
                    continue
                files.append((rel, "file", None, size))
    return files, skipped


def cmd_backup(args):
    root = Path(args.root).resolve()
    dest = Path(args.dest).resolve()
    if not root.is_dir():
        print(f"ERROR: root not a directory: {root}", file=sys.stderr)
        return 2
    try:
        dest.relative_to(root)
        print("ERROR: --dest must be OUTSIDE the source root (backup must not be committed)", file=sys.stderr)
        return 2
    except ValueError:
        pass
    if dest.exists() and any(dest.iterdir()):
        print(f"ERROR: destination is not empty: {dest}", file=sys.stderr)
        return 2
    tracked_mode = bool(git_tracked(root))
    files, skipped = collect_files(root, dest, tracked_mode)
    tree = dest / TREE_DIR
    entries = []
    for rel, kind, target, size in files:
        src = root / rel
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if kind == "symlink":
            if dst.exists() or dst.is_symlink():
                dst.unlink()
            os.symlink(target, dst)
            entries.append({"path": rel, "kind": "symlink", "target": target,
                            "sha256": None, "size": None, "mode": None})
        else:
            try:
                shutil.copy2(src, dst)
            except OSError as exc:
                skipped.append({"path": rel, "reason": "copy failed: %s" % exc})
                continue
            entries.append({"path": rel, "kind": "file", "target": None,
                            "sha256": sha256_file(dst), "size": dst.stat().st_size,
                            "mode": oct(dst.stat().st_mode & 0o777)})
    manifest = {
        "format": "r1.1-backup-v1",
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "root": str(root),
        "git_head": git_head(root) if tracked_mode else None,
        "tracked_mode": tracked_mode,
        "git_status": git_status_summary(root) if tracked_mode else None,
        "exclusions": {
            "dirs": sorted(EXCLUDED_DIR_NAMES),
            "rel_prefixes": list(EXCLUDED_REL_PREFIXES),
            "note": "projects/ (private) and .obsidian/ (machine config) are never backed up",
        },
        "count": len(entries),
        "total_bytes": sum(e["size"] or 0 for e in entries),
        "skipped_unreadable": skipped,
        "warnings": (["%d unreadable file(s) skipped" % len(skipped)] if skipped else []),
        "files": entries,
    }
    manifest_path = dest / MANIFEST_NAME
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    manifest_sha = sha256_file(manifest_path)
    with open(dest / "MANIFEST.sha256", "w", encoding="utf-8") as fh:
        fh.write(manifest_sha + "  " + MANIFEST_NAME + "\n")
    result = {
        "ok": True, "dest": str(dest), "count": len(entries),
        "total_bytes": manifest["total_bytes"], "manifest_sha256": manifest_sha,
        "git_head": manifest["git_head"], "tracked_mode": tracked_mode,
        "skipped_unreadable": len(skipped),
        "excluded": {"projects/": "private", ".obsidian/": "machine config",
                      "sandbox-*": "regenerable copies"},
    }
    if skipped:
        print("WARNING: %d unreadable file(s) skipped (see MANIFEST.json skipped_unreadable)" % len(skipped),
              file=sys.stderr)
    print(json.dumps(result, ensure_ascii=False, indent=1) if args.json else
          "backup OK: {count} files, {bytes} bytes -> {dest} (skipped {sk})".format(
              count=len(entries), bytes=manifest["total_bytes"], dest=dest, sk=len(skipped)))
    return 0


def load_manifest(backup):
    backup = Path(backup).resolve()
    mp = backup / MANIFEST_NAME
    if not mp.is_file():
        print(f"ERROR: manifest not found: {mp}", file=sys.stderr)
        return None, 2
    with open(mp, encoding="utf-8") as fh:
        manifest = json.load(fh)
    sha_file = backup / "MANIFEST.sha256"
    if sha_file.is_file():
        expected = sha_file.read_text(encoding="utf-8").split()[0]
        actual = sha256_file(mp)
        if expected != actual:
            print("ERROR: MANIFEST.json checksum mismatch", file=sys.stderr)
            return None, 3
    return manifest, None


def verify_tree(backup, manifest):
    tree = Path(backup).resolve() / TREE_DIR
    problems = []
    expected = {e["path"]: e for e in manifest["files"]}
    present = set()
    if tree.is_dir():
        for dirpath, _dirs, filenames in os.walk(tree):
            for name in filenames:
                p = Path(dirpath) / name
                present.add(p.relative_to(tree).as_posix())
    for rel, entry in expected.items():
        p = tree / rel
        if entry["kind"] == "symlink":
            if not p.is_symlink() or os.readlink(p) != entry["target"]:
                problems.append(f"symlink mismatch: {rel}")
            continue
        if not p.is_file():
            problems.append(f"missing: {rel}")
            continue
        if p.stat().st_size != entry["size"]:
            problems.append(f"size mismatch: {rel}")
            continue
        if sha256_file(p) != entry["sha256"]:
            problems.append(f"sha256 mismatch: {rel}")
    for extra in sorted(present - set(expected)):
        problems.append(f"unexpected extra file: {extra}")
    return problems


def cmd_verify(args):
    manifest, code = load_manifest(args.backup)
    if manifest is None:
        return code
    problems = verify_tree(args.backup, manifest)
    out = {"ok": not problems, "backup": str(Path(args.backup).resolve()),
           "count": manifest.get("count"), "problems": problems[:50],
           "problem_count": len(problems), "git_head": manifest.get("git_head")}
    print(json.dumps(out, ensure_ascii=False, indent=1) if args.json else
          ("verify OK: {count} files".format(count=manifest.get("count")) if not problems
           else "verify FAILED: {n} problem(s)\n  ".format(n=len(problems)) + "\n  ".join(problems[:20])))
    return 0 if not problems else 3


def cmd_restore(args):
    manifest, code = load_manifest(args.backup)
    if manifest is None:
        return code
    problems = verify_tree(args.backup, manifest)
    if problems:
        print("ERROR: backup verification failed; refusing to restore", file=sys.stderr)
        for p in problems[:10]:
            print("  " + p, file=sys.stderr)
        return 3
    dest = Path(args.dest).resolve()
    root = Path(manifest["root"]).resolve()
    try:
        dest.relative_to(root)
        print("ERROR: restore destination must be OUTSIDE the source root (use a temp dir)", file=sys.stderr)
        return 2
    except ValueError:
        pass
    if dest.exists() and any(dest.iterdir()):
        print(f"ERROR: restore destination not empty: {dest}", file=sys.stderr)
        return 2
    tree = Path(args.backup).resolve() / TREE_DIR
    restored = 0
    for entry in manifest["files"]:
        rel = entry["path"]
        src = tree / rel
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if entry["kind"] == "symlink":
            os.symlink(entry["target"], dst)
        else:
            shutil.copy2(src, dst)
        restored += 1
    # post-restore verification against manifest
    mismatches = []
    for entry in manifest["files"]:
        rel = entry["path"]
        dst = dest / rel
        if entry["kind"] == "symlink":
            if not dst.is_symlink() or os.readlink(dst) != entry["target"]:
                mismatches.append(f"symlink mismatch: {rel}")
        elif not dst.is_file() or sha256_file(dst) != entry["sha256"]:
            mismatches.append(f"sha256 mismatch: {rel}")
    out = {"ok": not mismatches, "restored": restored, "dest": str(dest),
           "count": manifest.get("count"), "mismatches": mismatches[:20]}
    print(json.dumps(out, ensure_ascii=False, indent=1) if args.json else
          ("restore OK: {restored} files -> {dest}".format(restored=restored, dest=dest)
           if not mismatches else "restore FAILED:\n  " + "\n  ".join(mismatches[:20])))
    return 0 if not mismatches else 3


def main(argv=None):
    parser = argparse.ArgumentParser(description="Verified local backup/restore (R1.1-A).")
    sub = parser.add_subparsers(dest="command", required=True)

    p_backup = sub.add_parser("backup", help="create a verified backup")
    p_backup.add_argument("--root", default=os.getcwd(), help="source root (default: cwd)")
    p_backup.add_argument("--dest", required=True, help="backup destination (must be outside root)")
    p_backup.add_argument("--json", action="store_true")
    p_backup.set_defaults(func=cmd_backup)

    p_verify = sub.add_parser("verify", help="verify an existing backup")
    p_verify.add_argument("backup")
    p_verify.add_argument("--json", action="store_true")
    p_verify.set_defaults(func=cmd_verify)

    p_restore = sub.add_parser("restore", help="restore a verified backup to a temp dir")
    p_restore.add_argument("backup")
    p_restore.add_argument("--dest", required=True)
    p_restore.add_argument("--json", action="store_true")
    p_restore.set_defaults(func=cmd_restore)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
