#!/usr/bin/env python3
"""P5-E candidate review tests: 239 queue, tiers, no auto promotion/writes."""
import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P5E = ROOT / "11-验收/P5E"
sys.path.insert(0, str(ROOT / "scripts"))
import candidate_review as cr  # noqa: E402


class CandidateReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run([sys.executable, "scripts/candidate_review.py", "--json"],
                                  cwd=str(ROOT), capture_output=True, text=True)
        cls.summary = json.loads(cls.proc.stdout)
        cls.rows = list(csv.DictReader((P5E / "candidate-review.csv").open(encoding="utf-8")))

    def test_239_queue(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stderr)
        self.assertEqual(self.summary["candidates"], 239)
        self.assertEqual(self.summary["reviewed"], 239)
        self.assertEqual(len(self.rows), 239)

    def test_no_promotion_or_card_writes(self):
        self.assertEqual(self.summary["auto_promotions"], 0)
        self.assertEqual(self.summary["card_writes"], 0)
        self.assertIn("NEVER auto-promote", self.summary["promotion_policy"])
        for row in self.rows:
            self.assertIn(row["tier"], ("source_verifiable", "needs_human",
                                        "reject_or_rework"))
            self.assertNotIn("high", row["recommendation"])
            self.assertEqual(row["auto_promotion"], "False")

    def test_tiers_and_design_flag(self):
        self.assertEqual(self.summary["design_only"], 239)
        self.assertGreater(self.summary["source_verifiable"], 0)
        self.assertGreater(self.summary["needs_human"], 0)
        self.assertGreater(self.summary["reject_or_rework"], 0)
        self.assertEqual(sum(self.summary["tiers"].values()), 239)

    def test_invalid_subject_rejected(self):
        rejects = [r for r in self.rows if r["tier"] == "reject_or_rework"]
        text = " ".join(r["reasons"] for r in rejects)
        self.assertIn("invalid subject type", text)
        self.assertIn("in_style", text)
        self.assertIn("may_have_part", text)

    def test_design_only_filter(self):
        before = (P5E / "candidate-review.csv").read_text(encoding="utf-8")
        proc = subprocess.run([sys.executable, "scripts/candidate_review.py",
                               "--design-only", "--json"],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["reviewed"], 239)
        self.assertEqual(before, (P5E / "candidate-review.csv").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
