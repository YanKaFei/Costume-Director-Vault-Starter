#!/usr/bin/env python3
"""R1.3B prompt QA tests: text/status/homogeneity checks, no image claims."""
import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "11-验收/R1.3B"
sys.path.insert(0, str(ROOT / "scripts"))
import prompt_qa as qa  # noqa: E402


class PromptQATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = subprocess.run([sys.executable, "scripts/prompt_qa.py"], cwd=str(ROOT),
                           capture_output=True, text=True)
        cls.returncode = p.returncode
        cls.summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
        cls.rows = list(csv.DictReader((OUT / "PROMPT-QA.csv").open(encoding="utf-8")))

    def test_all_new_prompts_sampled(self):
        self.assertEqual(self.returncode, 0)
        self.assertGreaterEqual(self.summary["prompts"], 40)
        self.assertGreaterEqual(self.summary["cards"], 20)
        self.assertEqual(len(self.rows), self.summary["prompts"])

    def test_statuses(self):
        self.assertEqual(self.summary["statuses"]["DOMAIN_REVIEWED"], "NOT_RUN")
        self.assertEqual(self.summary["statuses"]["IMAGE_TESTED"], "NOT_RUN")
        self.assertEqual(self.summary["statuses"]["HUMAN_VISUAL_APPROVED"], "NOT_RUN")
        self.assertFalse(self.summary["image_generation"])
        for row in self.rows:
            self.assertEqual(row["domain_reviewed"], "NOT_RUN")
            self.assertEqual(row["image_tested"], "NOT_RUN")
            self.assertEqual(row["human_visual_approved"], "NOT_RUN")

    def test_invalid_cases_reported(self):
        bad = [r for r in self.rows if r["text_status"] == "TEXT_INVALID"]
        self.assertEqual(len(bad), self.summary["text_invalid"])
        # Current cards must not assert material without evidence; historically
        # two such cases existed and were fixed by their card owners.
        self.assertEqual(bad, [])
        self.assertEqual(self.summary["text_invalid"], 0)

    def test_homogeneity_reported(self):
        self.assertGreater(self.summary["homogeneity_pairs"], 0)
        self.assertGreater(self.summary["template_scaffold_pairs"], 0)
        self.assertIn("Jaccard", self.summary["homogeneity_threshold"])
        md = (OUT / "PROMPT-QA.md").read_text(encoding="utf-8")
        self.assertIn("Cross-card homogeneity", md)

    def test_material_unknown_not_guessed(self):
        card = {"id": "X", "meta": {"type": "garment", "materials": [], "prompt_en": ""},
                "body": ""}
        block = {"kind": "image", "prompt": "SUBJECT: full-body X. MATERIAL (FACT): silk."}
        result = qa.check_prompt(card, block)
        self.assertIn("prompt asserts material while card has no materials field", result["errors"])

    def test_baseline_179_block_audit(self):
        p = subprocess.run([sys.executable, "scripts/prompt_qa.py", "--baseline-179",
                            "--out-csv", str(OUT / "BLOCK-AUDIT-179.csv"),
                            "--out-md", str(OUT / "BLOCK-AUDIT-179.md")],
                           cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        rows = list(csv.DictReader((OUT / "BLOCK-AUDIT-179.csv").open(encoding="utf-8")))
        self.assertEqual(len(rows), 179)
        self.assertTrue(all(r["status"] == "TEXT_VALID" for r in rows))
        columns = {"card_id", "prompt_id", "type", "subtype", "location", "hash",
                   "status", "evidence"}
        self.assertTrue(columns.issubset(set(rows[0].keys())))
        self.assertEqual(len({r["prompt_id"] for r in rows}), 179)
        subtypes = {}
        types = {}
        for r in rows:
            subtypes[r["subtype"]] = subtypes.get(r["subtype"], 0) + 1
            types[r["type"]] = types.get(r["type"], 0) + 1
        self.assertEqual(subtypes, {"base": 112, "detail": 26, "applied": 26,
                                    "product": 5, "worn": 5, "side_back": 5})
        self.assertEqual(types, {"image": 110, "video": 69})

    def test_clean_text(self):
        card = {"id": "GAR-0015", "meta": {"name_en": "robe", "type": "garment",
                 "materials": ["silk"], "prompt_en": "robe"},
                "body": ""}
        block = {"kind": "image", "prompt": "SUBJECT: full-body robe GAR-0015. "
                 "MATERIAL: silk. CAMERA: 50mm full-body."}
        result = qa.check_prompt(card, block)
        self.assertFalse(result["errors"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
