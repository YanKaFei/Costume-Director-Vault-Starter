#!/usr/bin/env python3
"""R1.1-A: regression tests for scripts/backup_restore.py.

Run:  python3 tests/test_backup_restore.py
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "backup_restore.py"


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True, cwd=cwd or str(ROOT))


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class BackupRestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="r11-backup-test-"))
        root = self.tmp / "root"
        (root / "reports").mkdir(parents=True)
        (root / "11-验收/R1/security/cases/A01").mkdir(parents=True)
        (root / "11-验收/R1/security/sandbox-A01").mkdir(parents=True)
        (root / "projects/p1").mkdir(parents=True)
        (root / ".obsidian").mkdir(parents=True)
        (root / "reports" / "unreadable.txt").write_text("secret-unreadable\n", encoding="utf-8")
        (root / "reports" / "unreadable.txt").chmod(0)
        (root / "a.txt").write_text("alpha\n", encoding="utf-8")
        (root / "reports/r.md").write_text("# report\n", encoding="utf-8")
        (root / "11-验收/x.md").write_text("evidence\n", encoding="utf-8")
        (root / "11-验收/R1/security/cases/A01/events.jsonl").write_text(
            '{"type":"session"}\n', encoding="utf-8")
        (root / "11-验收/R1/security/sandbox-A01/copy.txt").write_text(
            "sandbox copy (regenerable)\n", encoding="utf-8")
        (root / "projects/p1/private.txt").write_text("PRIVATE\n", encoding="utf-8")
        (root / ".obsidian/app.json").write_text("{}\n", encoding="utf-8")
        self.root = root

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_backup_verify_restore_roundtrip(self):
        dest = self.tmp / "backup1"
        self.assertEqual(run("backup", "--root", str(self.root), "--dest", str(dest),
                             "--json").returncode, 0)
        manifest = json.loads((dest / "MANIFEST.json").read_text(encoding="utf-8"))
        paths = {e["path"] for e in manifest["files"]}
        for need in ("a.txt", "reports/r.md", "11-验收/x.md",
                     "11-验收/R1/security/cases/A01/events.jsonl"):
            self.assertIn(need, paths)
        for banned in ("projects/p1/private.txt", ".obsidian/app.json",
                       "11-验收/R1/security/sandbox-A01/copy.txt"):
            self.assertNotIn(banned, paths)
        self.assertEqual(run("verify", str(dest), "--json").returncode, 0)
        restored = self.tmp / "restored1"
        self.assertEqual(run("restore", str(dest), "--dest", str(restored),
                             "--json").returncode, 0)
        for entry in manifest["files"]:
            self.assertEqual(sha(restored / entry["path"]), entry["sha256"],
                             "restored hash mismatch: " + entry["path"])

    def test_tampered_backup_fails_verify_and_restore(self):
        dest = self.tmp / "backup2"
        self.assertEqual(run("backup", "--root", str(self.root), "--dest", str(dest)).returncode, 0)
        with open(dest / "tree" / "a.txt", "a", encoding="utf-8") as fh:
            fh.write("tampered\n")
        self.assertEqual(run("verify", str(dest)).returncode, 3)
        restored = self.tmp / "restored2"
        self.assertEqual(run("restore", str(dest), "--dest", str(restored)).returncode, 3)
        self.assertFalse((restored / "a.txt").exists())

    def test_unreadable_file_skipped_with_manifest_warning(self):
        dest = self.tmp / "backup-unreadable"
        r = run("backup", "--root", str(self.root), "--dest", str(dest), "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        manifest = json.loads((dest / "MANIFEST.json").read_text(encoding="utf-8"))
        paths = {e["path"] for e in manifest["files"]}
        self.assertNotIn("reports/unreadable.txt", paths)
        skipped = {row["path"] for row in manifest.get("skipped_unreadable", [])}
        self.assertIn("reports/unreadable.txt", skipped)
        self.assertTrue(manifest.get("warnings"), "expected a manifest warning for skipped file")
        self.assertEqual(run("verify", str(dest)).returncode, 0)
        restored = self.tmp / "restored-unreadable"
        self.assertEqual(run("restore", str(dest), "--dest", str(restored)).returncode, 0)

    def test_manifest_tamper_detected(self):
        dest = self.tmp / "backup3"
        self.assertEqual(run("backup", "--root", str(self.root), "--dest", str(dest)).returncode, 0)
        mp = dest / "MANIFEST.json"
        data = json.loads(mp.read_text(encoding="utf-8"))
        data["files"][0]["sha256"] = "0" * 64
        mp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        self.assertEqual(run("verify", str(dest)).returncode, 3)

    def test_dest_inside_root_rejected(self):
        r = run("backup", "--root", str(self.root),
                "--dest", str(self.root / "backup-inside"))
        self.assertEqual(r.returncode, 2)

    def test_restore_inside_root_rejected(self):
        dest = self.tmp / "backup4"
        self.assertEqual(run("backup", "--root", str(self.root), "--dest", str(dest)).returncode, 0)
        r = run("restore", str(dest), "--dest", str(self.root / "restore-inside"))
        self.assertEqual(r.returncode, 2)


class RealRepoBackupTests(unittest.TestCase):
    """Smoke test on the actual repository (exclusions + verify + restore)."""

    def test_real_repo_backup_excludes_private_and_machine_config(self):
        tmp = Path(tempfile.mkdtemp(prefix="r11-real-backup-"))
        try:
            dest = tmp / "backup"
            r = run("backup", "--root", str(ROOT), "--dest", str(dest), "--json")
            self.assertEqual(r.returncode, 0, r.stderr)
            manifest = json.loads((dest / "MANIFEST.json").read_text(encoding="utf-8"))
            paths = {e["path"] for e in manifest["files"]}
            self.assertGreater(manifest["count"], 1000, "expected a real backup with >1000 files")
            self.assertFalse(any(p.startswith("projects/") for p in paths))
            self.assertFalse(any(p.startswith(".obsidian/") for p in paths))
            self.assertFalse(any(p.startswith("11-验收/R1/security/sandbox-") for p in paths))
            self.assertFalse(any(p.startswith("11-验收/R1.1/security/sandbox-") for p in paths))
            self.assertIn("reports/P4-REPORT.md", paths)
            self.assertIn("11-验收/P4-MACBETH/HUMAN-CLOSEOUT.md", paths)
            self.assertEqual(run("verify", str(dest)).returncode, 0)
            restored = tmp / "restored"
            self.assertEqual(run("restore", str(dest), "--dest", str(restored)).returncode, 0)
            e = next(x for x in manifest["files"] if x["path"] == "reports/P4-REPORT.md")
            self.assertEqual(sha(restored / "reports/P4-REPORT.md"), e["sha256"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
