#!/usr/bin/env python3
"""Path safety gate for Agent file access (SEC-A05).

Policy:
- allow paths inside the Vault except explicitly private/sensitive areas;
- deny private/, .ssh/, credentials/secrets, key files, Vault-external paths,
  traversal, and symlinks that resolve outside allowed roots;
- every check/read appends a JSONL audit record.

CLI:
  python3 scripts/path_guard.py check PATH [--audit FILE] [--json]
  python3 scripts/path_guard.py read PATH [--audit FILE] [--max-bytes N]
Exit codes: 0 allowed/success, 3 denied.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "11-验收/R1.1/security/path-guard-audit.jsonl"
DENY_PARTS = {"private", ".ssh", "credentials", ".aws", ".gnupg", "secrets"}
DENY_NAMES = {".env", "id_rsa", "id_dsa", "id_ed25519", "credentials.yaml",
              "credentials.yml", ".credentials.yaml", ".netrc", "known_hosts"}
SENSITIVE_SUFFIXES = (".pem", ".key", ".p12", ".pfx")


def _audit(path, action, allowed, reason, audit=None):
    target = Path(audit) if audit else DEFAULT_AUDIT
    target.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "action": action,
              "path": str(path), "allowed": bool(allowed), "reason": reason}
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def check_path(path, root=ROOT, audit=None, action="check"):
    """Return (allowed, realpath, reason). Never reads content."""
    raw = Path(str(path)).expanduser()
    # Reject traversal text and home shorthand explicitly.
    if ".." in Path(str(path)).parts:
        _audit(raw, action, False, "path traversal", audit)
        return False, None, "path traversal"
    if str(path).startswith("~"):
        _audit(raw, action, False, "home-relative path", audit)
        return False, None, "home-relative path"
    candidate = raw if raw.is_absolute() else (Path(root) / raw)
    try:
        real = candidate.resolve(strict=False)
        root_real = Path(root).resolve()
    except OSError as exc:
        _audit(candidate, action, False, "resolve error: %s" % exc, audit)
        return False, None, "resolve error"
    try:
        real.relative_to(root_real)
    except ValueError:
        _audit(raw, action, False, "outside vault", audit)
        return False, None, "outside vault"
    for part in real.parts:
        if part in DENY_PARTS:
            _audit(raw, action, False, "private/sensitive directory", audit)
            return False, None, "private/sensitive directory"
    if real.name in DENY_NAMES or real.name.startswith(".env"):
        _audit(raw, action, False, "sensitive filename %s" % real.name, audit)
        return False, None, "sensitive filename"
    if real.suffix.lower() in SENSITIVE_SUFFIXES:
        _audit(raw, action, False, "sensitive key file", audit)
        return False, None, "sensitive key file"
    # Symlink escape: any symlink component must resolve inside the allowed root.
    current = raw if raw.is_absolute() else (Path(root) / raw)
    while True:
        if current.exists() and current.is_symlink():
            try:
                current.resolve(strict=False).relative_to(root_real)
            except ValueError:
                _audit(raw, action, False, "symlink escapes root", audit)
                return False, None, "symlink escapes root"
        if str(current) in ("/", str(root_real)) or current == current.parent:
            break
        current = current.parent
    _audit(raw, action, True, "allowed", audit)
    return True, str(real), "allowed"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Path safety gate")
    parser.add_argument("command", choices=["check", "read", "resolve"])
    parser.add_argument("path")
    parser.add_argument("--audit", help="JSONL audit log path")
    parser.add_argument("--max-bytes", type=int, default=200000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    allowed, real, reason = check_path(args.path, audit=args.audit,
                                       action=args.command)
    result = {"command": args.command, "path": args.path,
              "realpath": real, "allowed": allowed, "reason": reason}
    if args.command == "check":
        print(json.dumps(result, ensure_ascii=False) if args.json else
              ("ALLOW %s" % real if allowed else "DENY %s" % reason))
        return 0 if allowed else 3
    if not allowed:
        print(json.dumps(result, ensure_ascii=False) if args.json else
              ("DENY %s" % reason), file=sys.stderr)
        return 3
    try:
        data = Path(real).read_bytes()[:args.max_bytes]
        text = data.decode("utf-8", errors="replace")
    except OSError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 3
    if args.json:
        result["content"] = text
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
