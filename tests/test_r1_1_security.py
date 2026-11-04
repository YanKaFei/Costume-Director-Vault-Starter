#!/usr/bin/env python3
"""R1.1 B tests: path_guard allow/deny/traversal/symlink/audit."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "11-验收/R1.1/security/path-guard-audit.jsonl"


class PathGuardTests(unittest.TestCase):
    def run_guard(self, *args):
        return subprocess.run([sys.executable, "scripts/path_guard.py", *args],
                              cwd=str(ROOT), capture_output=True, text=True)

    def test_allowed_vault_card(self):
        p = self.run_guard("check", "01-服装单品/下装/GAR-0072-帕贾马裤.md",
                           "--audit", str(AUDIT), "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(json.loads(p.stdout)["allowed"])

    def test_deny_private_ssh_credentials(self):
        for path in ("private/local-draft-play.txt", ".ssh/id_rsa",
                     "credentials.yaml", "assets/.env"):
            p = self.run_guard("check", path, "--audit", str(AUDIT), "--json")
            self.assertEqual(p.returncode, 3, path)
            self.assertFalse(json.loads(p.stdout)["allowed"], path)

    def test_deny_traversal_and_outside(self):
        for path in ("../../etc/passwd", "~/.ssh/id_rsa", "/tmp/outside.txt"):
            p = self.run_guard("check", path, "--audit", str(AUDIT), "--json")
            self.assertEqual(p.returncode, 3, path)
            self.assertFalse(json.loads(p.stdout)["allowed"], path)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            link = ROOT / "11-验收/R1.1/security/_escape_link"
            if link.exists() or link.is_symlink():
                link.unlink()
            os.symlink(tmp, link)
            try:
                p = self.run_guard("check", str(link / "secret.txt"),
                                   "--audit", str(AUDIT), "--json")
                self.assertEqual(p.returncode, 3)
                self.assertFalse(json.loads(p.stdout)["allowed"])
            finally:
                link.unlink(missing_ok=True)

    def test_read_denied_returns_no_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            secret = Path(tmp) / "secret.txt"
            secret.write_text("SHOULD-NOT-LEAK")
            p = self.run_guard("read", str(secret), "--audit", str(AUDIT))
            self.assertEqual(p.returncode, 3)
            self.assertNotIn("SHOULD-NOT-LEAK", p.stdout)

    def test_audit_jsonl(self):
        if AUDIT.exists():
            AUDIT.unlink()
        self.run_guard("check", "private/x", "--audit", str(AUDIT), "--json")
        self.assertTrue(AUDIT.exists())
        rows = [json.loads(line) for line in AUDIT.read_text().splitlines()]
        self.assertTrue(rows)
        self.assertFalse(rows[-1]["allowed"])
        self.assertEqual(rows[-1]["reason"], "private/sensitive directory")

    def test_read_allowed_card(self):
        p = self.run_guard("read", "01-服装单品/下装/GAR-0072-帕贾马裤.md",
                           "--audit", str(AUDIT), "--json")
        self.assertEqual(p.returncode, 0)
        data = json.loads(p.stdout)
        self.assertTrue(data["allowed"])
        self.assertIn("GAR-0072", data["content"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
