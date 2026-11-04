#!/usr/bin/env python3
"""P5-C relation path / character-outfit / approved-anchor tests."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import relation_trace as rt  # noqa: E402


def run(*args):
    proc = subprocess.run([sys.executable, "scripts/relation_trace.py", *args, "--json"],
                          cwd=str(ROOT), capture_output=True, text=True)
    return proc, json.loads(proc.stdout) if proc.stdout.strip() else {}


class RelationTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.edges, cls.cards, cls.sources = rt.load_relations()

    def test_depth_limit_and_real_targets(self):
        proc, data = run("--start", "GAR-0015", "--max-depth", "3")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(data["paths"])
        for path in data["paths"]:
            self.assertLessEqual(path["depth"], 3)
            for step in path["path"]:
                self.assertIn(step["target"], self.cards or self.sources)
                for sid in step["source_ids"]:
                    self.assertIn(sid, self.sources)
                self.assertNotEqual(step["confidence"], "low")
        # dedupe by full node sequence
        sequences = [tuple([data["start"]] + [s["target"] for s in p["path"]])
                     for p in data["paths"]]
        self.assertEqual(len(sequences), len(set(sequences)))

    def test_factual_only_excludes_design_edges(self):
        proc, data = run("--start", "GAR-0015", "--max-depth", "3", "--factual-only")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for path in data["paths"]:
            for step in path["path"]:
                self.assertTrue(step["factual"])
                self.assertNotIn(step["confidence"], ("low",))

    def test_character_to_complete_outfit(self):
        proc, data = run("--character", "沙龙女主人")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(data["character_looks"])
        look = data["character_looks"][0]
        self.assertEqual(look["look_id"], "LOOK-0001")
        self.assertGreaterEqual(len(look["items"]), 5)
        self.assertTrue(look["prompt_image"])
        self.assertTrue(look["prompt_negative"])
        self.assertTrue(look["conflicts"])
        self.assertTrue(all(item["path"] for item in look["items"]))

    def test_garment_to_related_outfit(self):
        proc, data = run("--garment", "GAR-0015")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(data["garment_looks"])
        self.assertIn("LOOK-0001", [x["look_id"] for x in data["garment_looks"]])
        self.assertTrue(data["garment_looks"][0]["prompt_image"])

    def test_approved_anchors_loader(self):
        anchors = rt.load_approved_anchors(
            ROOT / "projects/_template/look-bible/versions/SAMPLE-M1-A/v5.json")
        self.assertIn("hard", anchors)
        self.assertIn("soft", anchors)

    def test_depth_is_capped(self):
        proc, data = run("--start", "GAR-0015", "--max-depth", "99")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(data["limits"]["max_depth"], 3)
        self.assertTrue(all(p["depth"] <= 3 for p in data["paths"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
