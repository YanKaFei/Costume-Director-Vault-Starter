#!/usr/bin/env python3
"""R1.1 C/D tests: hard constraints, creative override, A/B/C gaming, held-out."""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CD = ROOT / "11-验收/R1.1/CD"
FIX = ROOT / "11-验收/P4-COMPOSER/fixtures"
sys.path.insert(0, str(ROOT / "scripts"))
import abc_eval  # noqa: E402
import costume_lib as lib  # noqa: E402
import outfit  # noqa: E402

CROSS = {
    "character": {"name": "Macbeth", "occupation": "thane", "economic_status": "high"},
    "period": "11th century Scotland", "region": "scotland", "season": "winter",
    "scene": "heath", "time": "night", "weather": "storm, cold", "action": "battle",
    "art_direction": "stark medieval tragedy", "lighting": "torchlight",
    "camera": "medium shot", "budget": "medium", "fidelity_mode": "historical",
    "tool": "generic",
}


def run(args):
    return subprocess.run([sys.executable] + args, cwd=str(ROOT),
                          capture_output=True, text=True)


def load_cards():
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(c["meta"], "id"): c for c in cards}
    sources = {lib.get_str(c["meta"], "id"): c for c in cards
               if lib.norm_text(c["meta"].get("type")) == "source"}
    return by_id, sources


class R11CDTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.by_id, cls.sources = load_cards()
        CD.mkdir(parents=True, exist_ok=True)
        cls.cross_path = CD / "_cross_era.json"
        cls.cross_path.write_text(json.dumps(CROSS, ensure_ascii=False), encoding="utf-8")

    def test_normal_composer_hard_constraints(self):
        proc = run(["scripts/outfit.py", "--input", str(FIX / "macbeth.json"), "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr[-500:])
        payload = json.loads(proc.stdout)
        # Inspired Macbeth is an analogue look: every item must be declared;
        # it may not be status=ok/hard_constraints_passed when mismatches exist.
        self.assertEqual(payload["status"], "declared_mismatch")
        self.assertFalse(payload["checks"]["hard_constraints_passed"])
        self.assertEqual(len(payload["looks"]), 3)
        self.assertTrue(payload["declared_mismatches"])
        for look in payload["looks"]:
            for item in look["items"]:
                self.assertTrue(any(entry["id"] == item["id"] and
                                    entry["slot"] == item["slot"]
                                    for entry in payload["item_compatibility"]))

    def test_cross_era_mismatch_blocks(self):
        proc = run(["scripts/outfit.py", "--input", str(self.cross_path), "--json"])
        self.assertIn(proc.returncode, (0, 3))
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertEqual(payload["looks"], [])
        self.assertTrue(payload["constraint_violations"])
        self.assertFalse(payload["checks"]["hard_constraints_passed"])

    def test_creative_override_is_explicit(self):
        data = copy.deepcopy(CROSS)
        data["creative_override"] = {
            "intent": "stylized stage Macbeth",
            "conflicts": ["11th c Scotland has no exact garment cards",
                          "inspired analogue wardrobe"],
            "historical_accuracy": False,
        }
        path = CD / "_cross_override.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        proc = run(["scripts/outfit.py", "--input", str(path), "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "override")
        self.assertFalse(payload["historical_accuracy"])
        self.assertTrue(payload["constraint_violations"])
        self.assertEqual(payload["creative_override"]["historical_accuracy"], False)
        self.assertEqual(len(payload["creative_override"]["conflicts"]), 2)

    def test_override_cannot_claim_historical_accuracy(self):
        data = copy.deepcopy(CROSS)
        data["creative_override"] = {
            "intent": "stylized stage Macbeth",
            "conflicts": ["no exact cards"],
            "historical_accuracy": True,
        }
        path = CD / "_cross_bad_override.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        proc = run(["scripts/outfit.py", "--input", str(path), "--json"])
        self.assertIn(proc.returncode, (0, 3))
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertFalse(payload["historical_accuracy"])

    def test_one_item_swap_is_not_meaningful(self):
        proc = run(["scripts/outfit.py", "--input", str(FIX / "macbeth.json"), "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        # Build a synthetic B that is A plus one item-only change, preserving
        # the same palette/material/silhouette language.
        manipulated = copy.deepcopy(payload)
        looks = manipulated["looks"]
        a = looks[0]
        b = copy.deepcopy(a)
        other = looks[2]["items"]
        a_by_slot = {item["slot"]: item["id"] for item in a["items"]}
        replacement = next(item for item in other
                           if item["id"] != a_by_slot.get(item["slot"]))
        target_slot = replacement["slot"]
        b["items"] = [copy.deepcopy(item) for item in a["items"]]
        for index, item in enumerate(b["items"]):
            if item["slot"] == target_slot:
                b["items"][index] = copy.deepcopy(replacement)
                break
        b["palette"] = copy.deepcopy(a["palette"])
        b["materials"] = copy.deepcopy(a["materials"])
        b["silhouette"] = copy.deepcopy(a["silhouette"])
        manipulated["looks"] = [a, b, looks[2]]
        checks = abc_eval.evaluate(manipulated, self.by_id, self.sources)
        self.assertTrue(checks["one_item_swap_gaming"])
        self.assertFalse(checks["all_pairs_meaningful"])
        self.assertFalse(checks["pass"])

    def test_heldout_evaluation(self):
        heldout = CD / "heldout"
        self.assertTrue(heldout.exists())
        proc = run(["scripts/abc_eval.py", "--heldout", str(heldout), "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr[-500:])
        rows = json.loads(proc.stdout)
        self.assertGreaterEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(row["pass"], row.get("case"))
            self.assertTrue(row["all_pairs_meaningful"], row.get("case"))
            self.assertFalse(row["one_item_swap_gaming"], row.get("case"))
            self.assertTrue(row["all_items_real"], row.get("case"))

    def test_source_validity_and_narrative(self):
        proc = run(["scripts/outfit.py", "--input", str(FIX / "T31.json"), "--json"])
        self.assertEqual(proc.returncode, 0)
        payload = json.loads(proc.stdout)
        checks = abc_eval.evaluate(payload, self.by_id, self.sources)
        self.assertTrue(checks["all_items_real"])
        self.assertFalse(checks["missing_source_ids"])
        self.assertTrue(checks["narrative_present"])
        self.assertTrue(checks["pass"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
