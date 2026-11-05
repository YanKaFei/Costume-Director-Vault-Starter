#!/usr/bin/env python3
"""R1.3-D visual prompt tests: typed modules, evidence tags, conflicts, no images."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/visual_prompt.py"
sys.path.insert(0, str(ROOT / "scripts"))
import visual_prompt as vp  # noqa: E402


def run(*args):
    p = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=str(ROOT),
                       capture_output=True, text=True)
    return p, json.loads(p.stdout) if p.stdout.strip() else {}


class VisualPromptTests(unittest.TestCase):
    def test_material_macro(self):
        p, d = run("--id", "MAT-0017", "--kind", "material_macro", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(d["kind"], "material_macro")
        self.assertFalse(d["image_generation"])
        self.assertIn("FACT", d["evidence_tags"])
        self.assertIn("OBSERVATION", d["evidence_tags"])
        self.assertTrue(d["modules"])
        self.assertIn("macro", d["modules"][0]["prompt_en"].lower())

    def test_component_detail(self):
        p, d = run("--id", "STR-0011", "--kind", "component_detail", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("structure_detail", [m["module"] for m in d["modules"]])
        self.assertTrue(d["modules"][0]["prompt_en"])

    def test_garment_flat(self):
        p, d = run("--id", "GAR-0015", "--kind", "garment_flat", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(d["card_path"].split("/")[0], "01-服装单品")
        self.assertTrue(d["modules"][0]["prompt_en"])

    def test_outfit_modules_and_continuity(self):
        p, d = run("--id", "LOOK-0001", "--kind", "outfit", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        names = [m["module"] for m in d["modules"]]
        self.assertIn("outfit_hero", names)
        self.assertIn("continuity", names)
        self.assertIn("CREATIVE", d["evidence_tags"])
        self.assertFalse(d["image_generation"])

    def test_style_module(self):
        p, d = run("--id", "STY-0010", "--kind", "style", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(d["modules"][0]["module"], "style_language")
        self.assertTrue(d["modules"][0]["prompt_zh"])

    def test_conflicts(self):
        p, d = run("--id", "GAR-0015", "--kind", "garment_flat",
                   "--period", "1930s", "--json")
        self.assertEqual(p.returncode, 0, p.stderr)
        codes = [c["code"] for c in d["conflicts"]]
        self.assertIn("period_conflict", codes)
        p2, d2 = run("--id", "GAR-0015", "--kind", "outfit", "--json")
        self.assertIn("kind_type_mismatch", [c["code"] for c in d2["conflicts"]])
        p3, d3 = run("--id", "GAR-EXAMPLE-001", "--kind", "garment_worn", "--json")
        self.assertIn("low_confidence", [c["code"] for c in d3["conflicts"]])

    def test_markdown_and_record(self):
        log = ROOT / "11-验收/R1.3/PROMPT-LOG.jsonl"
        before = log.read_text(encoding="utf-8").count("\n") if log.exists() else 0
        p = subprocess.run([sys.executable, str(SCRIPT), "--id", "MAT-0017",
                            "--kind", "material_macro", "--markdown", "--record"],
                           cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Image generation: **false**", p.stdout)
        self.assertIn("FACT", p.stdout)
        after = log.read_text(encoding="utf-8").count("\n")
        self.assertEqual(after, before + 1)
        entry = json.loads(log.read_text(encoding="utf-8").splitlines()[-1])
        self.assertFalse(entry["image_generation"])

    def test_all_kinds_clean_english(self):
        import re
        cases = [("MAT-0017", "material_macro"), ("STR-0011", "component_detail"),
                 ("GAR-0008", "garment_flat"), ("GAR-0008", "garment_worn"),
                 ("GAR-0028", "accessory"), ("STY-0010", "style"),
                 ("LOOK-0001", "outfit")]
        for cid, kind in cases:
            p, d = run("--id", cid, "--kind", kind, "--json")
            self.assertEqual(p.returncode, 0, (cid, kind, p.stderr))
            for module in d["modules"]:
                en = module["prompt_en"]
                self.assertFalse(re.search(r"[\u3400-\u9fff]", en), (cid, kind, en))
                self.assertNotIn("[[", en)
                self.assertNotIn("]]", en)
                self.assertNotIn("silhhouette", en)
                self.assertNotIn("may_have_par;", en)
                self.assertFalse(en.rstrip().endswith(("...", "…")), (cid, kind, en))
                # no obviously truncated final token
                self.assertTrue(en.split()[-1].strip(".,;:"), (cid, kind, en))
            for module in d["modules"]:
                self.assertNotIn("[[", module["prompt_zh"])
                self.assertNotIn("]]", module["prompt_zh"])

    def test_card_not_found(self):
        p, d = run("--id", "GAR-9999", "--kind", "garment_flat", "--json")
        self.assertEqual(p.returncode, 2)
        self.assertIn("error", d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
