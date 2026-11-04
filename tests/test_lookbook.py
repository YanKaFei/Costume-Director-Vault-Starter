# -*- coding: utf-8 -*-
"""Tests for scripts/lookbook.py (R1.1-E / AUD-003)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "lookbook.py"


class LookbookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.sig = self.root / "signature.json"
        self.sig.write_text(json.dumps({
            "reviewer": "human-reviewer",
            "role": "human",
            "signature": "sig-test-token",
            "signed_at": "2026-11-05T00:00:00+08:00",
            "agent_self_approval": False,
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def cli(self, *args, expected=0):
        cmd = [sys.executable, str(SCRIPT), "--root", str(self.root)] + list(args)
        proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        if expected is not None:
            self.assertEqual(proc.returncode, expected, msg=proc.stderr + proc.stdout)
        return proc

    def read(self, project="p1"):
        return json.loads((self.root / "projects" / project / "look-bible" / "look-bible.json").read_text(encoding="utf-8"))

    def make_approved(self, project="p1", look="MAC-M1-A"):
        self.cli("init", "--project", project)
        self.cli("add", "--project", project, "--look", look, "--character", "MAC",
                 "--slot", "torso", "--card", "GAR-0075", "--lock", "hard")
        self.cli("add", "--project", project, "--look", look,
                 "--slot", "footwear", "--card", "GAR-0081", "--lock", "soft")
        self.cli("propose", "--project", project, "--look", look)
        self.cli("approve", "--project", project, "--look", look,
                 "--reviewer", "human-reviewer", "--signature-file", str(self.sig))
        return self.read(project)["looks"][look]

    def test_init_add_propose_approve_versioning(self):
        look = self.make_approved()
        self.assertEqual(look["status"], "Approved")
        self.assertGreaterEqual(look["version"], 5)
        hard = [a["slot"] for a in look["approved_anchors"]["hard"]]
        self.assertEqual(hard, ["torso"])
        self.assertEqual(look["approvals"][0]["reviewer"], "human-reviewer")
        self.assertTrue(look["approvals"][0]["signature_sha256"])
        self.cli("validate", "--project", "p1")

    def test_unauthorized_approve_without_signature_fails(self):
        self.cli("init", "--project", "p2")
        self.cli("add", "--project", "p2", "--look", "L1", "--character", "X",
                 "--slot", "torso", "--card", "GAR-0075")
        self.cli("propose", "--project", "p2", "--look", "L1")
        proc = self.cli("approve", "--project", "p2", "--look", "L1",
                        "--reviewer", "human-reviewer", "--signature-file", str(self.root / "missing.json"),
                        expected=1)
        self.assertIn("signature file not found", proc.stderr)
        self.assertEqual(self.read("p2")["looks"]["L1"]["status"], "Proposed")

    def test_agent_self_approval_fails(self):
        # 1) signature role=agent
        self.cli("init", "--project", "p3")
        self.cli("add", "--project", "p3", "--look", "L2", "--character", "X",
                 "--slot", "torso", "--card", "GAR-0075")
        self.cli("propose", "--project", "p3", "--look", "L2")
        bad = self.root / "agent_sig.json"
        bad.write_text(json.dumps({"reviewer": "agent", "role": "agent",
                                   "signature": "x", "agent_self_approval": True}), encoding="utf-8")
        proc = self.cli("approve", "--project", "p3", "--look", "L2",
                        "--reviewer", "agent", "--signature-file", str(bad), expected=1)
        self.assertIn("agent self-approval", proc.stderr.lower() + proc.stdout.lower())
        # 2) human role but agent identity
        bad2 = self.root / "agent_sig2.json"
        bad2.write_text(json.dumps({"reviewer": "agent", "role": "human",
                                    "signature": "x", "agent_self_approval": False}), encoding="utf-8")
        self.cli("approve", "--project", "p3", "--look", "L2",
                 "--reviewer", "agent", "--signature-file", str(bad2), expected=1)
        self.assertEqual(self.read("p3")["looks"]["L2"]["status"], "Proposed")

    def test_approved_hard_anchor_cannot_be_overwritten(self):
        look = self.make_approved("p4")
        before = look["version"]
        proc = self.cli("patch", "--project", "p4", "--look", "MAC-M1-A",
                        "--slot", "torso", "--card", "GAR-0076", expected=1)
        self.assertIn("approved hard anchor", proc.stderr)
        self.assertEqual(self.read("p4")["looks"]["MAC-M1-A"]["slots"]["torso"]["card_id"], "GAR-0075")
        self.assertEqual(self.read("p4")["looks"]["MAC-M1-A"]["version"], before)

    def test_single_item_patch_and_diff(self):
        self.make_approved("p5")
        self.cli("patch", "--project", "p5", "--look", "MAC-M1-A",
                 "--slot", "footwear", "--card", "GAR-0022", "--note", "approved alternative boot")
        look = self.read("p5")["looks"]["MAC-M1-A"]
        self.assertEqual(look["slots"]["footwear"]["card_id"], "GAR-0022")
        self.assertEqual(look["slots"]["torso"]["card_id"], "GAR-0075")
        proc = self.cli("diff", "--project", "p5", "--look", "MAC-M1-A",
                        "--from", str(look["version"] - 1), "--to", str(look["version"]), "--json")
        diff = json.loads(proc.stdout)
        self.assertEqual(diff["item_patch_count"], 1)
        self.assertEqual(diff["item_patch"][0]["slot"], "footwear")
        self.assertFalse(diff["approved_anchors_changed"])
        self.assertGreater(look["version"], 5)

    def test_validate_rejects_bad_status(self):
        self.cli("init", "--project", "p6")
        self.cli("add", "--project", "p6", "--look", "L3", "--character", "X",
                 "--slot", "torso", "--card", "GAR-0075")
        path = self.root / "projects" / "p6" / "look-bible" / "look-bible.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["looks"]["L3"]["status"] = "Pending"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.cli("validate", "--project", "p6", expected=1)


if __name__ == "__main__":
    unittest.main()
