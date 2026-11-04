# -*- coding: utf-8 -*-
"""Tests for scripts/validate_outfits.py (P5-C / task-70)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_outfits.py"
CHECKS = ["period", "region", "identity", "weather", "action", "compatibility", "approved_anchors"]


def base_outfit(**overrides):
    data = {
        "id": "TEST-OUTFIT",
        "periods": ["11th_century"],
        "regions": ["scotland"],
        "weather": "dry",
        "action": "standing",
        "outfit_slots": ["one_piece=GAR-0075", "outerwear=GAR-0076", "footwear=GAR-0081"],
        "evidence_type": "historical_evidence",
        "historical_evidence": ["GAR-0075:SRC-0480", "SRC-0481"],
        "constraints_checked": CHECKS,
        "period_tiers": ["one_piece=era", "outerwear=era", "footwear=era"],
        "region_tiers": ["one_piece=none", "outerwear=era", "footwear=era"],
    }
    data.update(overrides)
    return data


class ValidateOutfitsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_input(self, obj, expected=0):
        path = self.root / "outfit.json"
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(SCRIPT), "--vault", str(ROOT),
                               "--input", str(path), "--json"],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(proc.returncode, expected, msg=proc.stderr + proc.stdout)
        return json.loads(proc.stdout)

    def test_valid_historical_outfit(self):
        data = self.run_input(base_outfit())
        result = data["results"][0]
        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["hard_constraints"]["passed"])

    def test_missing_footwear_fails(self):
        data = self.run_input(base_outfit(outfit_slots=["one_piece=GAR-0075", "outerwear=GAR-0076"]), expected=1)
        self.assertTrue(any("footwear" in e for e in data["results"][0]["errors"]))

    def test_historical_without_evidence_fails(self):
        data = self.run_input(base_outfit(historical_evidence=[]), expected=1)
        self.assertTrue(any("historical_evidence" in e for e in data["results"][0]["errors"]))

    def test_new_outfit_without_evidence_type_fails(self):
        obj = base_outfit()
        del obj["evidence_type"]
        data = self.run_input(obj, expected=1)
        self.assertTrue(any("evidence_type" in e for e in data["results"][0]["errors"]))

    def test_approved_anchor_missing_fails(self):
        data = self.run_input(base_outfit(evidence_type="creative_inference",
                                          creative_inference=["design test"],
                                          approved_anchors=["GAR-0084"]), expected=1)
        self.assertTrue(any("approved anchor" in e for e in data["results"][0]["errors"]))

    def test_hard_constraint_rain_fails_historical(self):
        data = self.run_input(base_outfit(outfit_slots=["one_piece=GAR-0075", "footwear=GAR-0081"],
                                          weather="heavy rain", location="outdoor street"),
                              expected=1)
        result = data["results"][0]
        self.assertTrue(any("rain_without_rainwear" in e for e in result["errors"]))
        self.assertFalse(result["hard_constraints"]["passed"])

    def test_sourced_style_requires_observation(self):
        obj = base_outfit(evidence_type="sourced_style_observation")
        obj.pop("historical_evidence")
        data = self.run_input(obj, expected=1)
        self.assertTrue(any("style_observation" in e for e in data["results"][0]["errors"]))

    def test_creative_inference_passes_with_note(self):
        data = self.run_input(base_outfit(evidence_type="creative_inference",
                                          creative_inference=["cross-era design test"]))
        self.assertEqual(data["results"][0]["status"], "pass")

    def test_legacy_look_accepted(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "--vault", str(ROOT),
                               "--look", "LOOK-0001", "--json"],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["results"][0]["status"], "legacy_warn")
        self.assertTrue(data["results"][0]["legacy"])

    def test_all_legacy_looks_do_not_fail(self):
        data = subprocess.run([sys.executable, str(SCRIPT), "--vault", str(ROOT),
                               "--all", "--json"], cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(data.returncode, 0, msg=data.stderr)
        parsed = json.loads(data.stdout)
        self.assertEqual(parsed["summary"]["failed"], 0)
        self.assertEqual(parsed["summary"]["looks"], 35)


if __name__ == "__main__":
    unittest.main()
