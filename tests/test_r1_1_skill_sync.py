#!/usr/bin/env python3
"""R1.1 F: canonical .dsh skill -> repo mirror sync test."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / ".dsh/skills/costume-director/SKILL.md"
MIRROR = ROOT / "skills/costume-director/SKILL.md"
sys.path.insert(0, str(ROOT / "scripts"))
import sync_skill  # noqa: E402


class SkillSyncTests(unittest.TestCase):
    def test_generated_matches_mirror(self):
        generated = sync_skill.generate()
        self.assertEqual(MIRROR.read_text(encoding="utf-8"), generated)
        self.assertTrue(MIRROR.read_text(encoding="utf-8").startswith("<!-- DO NOT EDIT:"))

    def test_required_sections(self):
        text = CANON.read_text(encoding="utf-8")
        for needle in ("scripts/outfit.py", "scripts/abc_eval.py",
                       "scripts/path_guard.py", "STR-0012", "PG76299",
                       "11-验收/P4-VISUAL/visual-index.csv",
                       "creative_override", "relationship"):
            self.assertIn(needle, text)
        # mirror contains the same body after the generated header
        self.assertIn("## 6b. P4 sources", MIRROR.read_text(encoding="utf-8"))

    def test_sync_check(self):
        proc = subprocess.run([sys.executable, "scripts/sync_skill.py", "--check", "--json"],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "match")


if __name__ == "__main__":
    unittest.main(verbosity=2)
