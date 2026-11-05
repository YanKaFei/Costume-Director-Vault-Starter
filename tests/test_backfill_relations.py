#!/usr/bin/env python3
"""P5-D conservative backfill tests: exact rules, high/medium split, idempotence."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import backfill_relations as B  # noqa: E402


def card(meta, body=""):
    return "---\n" + "\n".join(meta) + "\n---\n" + body


class BackfillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for d in ("01-服装单品", "02-结构细节", "03-材质纹样/材料", "04-来源",
                  "05-风格体系", "06-时代地域", "07-剧情场景", "09-造型组合"):
            (self.tmp / d).mkdir(parents=True, exist_ok=True)
        (self.tmp / "04-来源/SRC-0001-test.md").write_text(
            card(["id: SRC-0001", "type: source", "evidence_status: verified"]),
            encoding="utf-8")
        (self.tmp / "05-风格体系/STY-0001-test.md").write_text(
            card(["id: STY-0001", "type: style", "evidence_status: verified",
                  "source_ids: [SRC-0001]"]), encoding="utf-8")
        (self.tmp / "07-剧情场景/SCN-0001-test.md").write_text(
            card(["id: SCN-0001", "type: scene", "evidence_status: verified",
                  "source_ids: [SRC-0001]"]), encoding="utf-8")
        (self.tmp / "03-材质纹样/材料/MAT-0001-silk.md").write_text(
            card(["id: MAT-0001", "type: material", "name_zh: silk",
                  "name_en: silk", "materials: [silk]",
                  "evidence_status: verified"]), encoding="utf-8")
        (self.tmp / "02-结构细节/STR-0001-part.md").write_text(
            card(["id: STR-0001", "type: garment_part",
                  "evidence_status: verified"]), encoding="utf-8")
        (self.tmp / "01-服装单品/GAR-0001.md").write_text(
            card(["id: GAR-0001", "type: garment", "evidence_status: verified",
                  "source_ids: [SRC-0001]", "style_tags: [STY-0001]",
                  "materials: [silk]"]), encoding="utf-8")
        (self.tmp / "09-造型组合/LOOK-0001.md").write_text(
            card(["id: LOOK-0001", "type: look", "evidence_status: verified",
                  "source_ids: [SRC-0001]", "look_items: [GAR-0001, STR-0001]",
                  "look_scene: [SCN-0001]"]), encoding="utf-8")

    def test_high_in_style_and_scene_added_visible(self):
        cards, sources = B.load_cards(self.tmp)
        for cid in ("GAR-0001", "LOOK-0001"):
            plan = B.plan_card(cards[cid], cards, sources)
            self.assertTrue(plan["changed"], cid)
            self.assertTrue(plan["high"], cid)
            self.assertTrue(plan["body_additions"], cid)
            B.apply_plan(plan)
            text = cards[cid]["path"].read_text(encoding="utf-8")
            self.assertIn("relations:", text)
            self.assertIn("confidence=high", text)
            self.assertFalse("`[[" in text)
        # idempotent after apply
        cards2, sources2 = B.load_cards(self.tmp)
        self.assertFalse(B.plan_card(cards2["GAR-0001"], cards2, sources2)["changed"])
        self.assertFalse(B.plan_card(cards2["LOOK-0001"], cards2, sources2)["changed"])

    def test_medium_rules_queue_not_body(self):
        cards, sources = B.load_cards(self.tmp)
        plan = B.plan_card(cards["LOOK-0001"], cards, sources)
        types = {q["relation_type"] for q in plan["queue"]}
        self.assertIn("appears_in_look", types)
        self.assertIn("may_have_part", types)
        for q in plan["queue"]:
            self.assertNotEqual(q["confidence"], "high")
        self.assertNotIn("uses_material", {r["relation_type"] for r in plan["high"]})
        self.assertNotIn("silhouette", {r["relation_type"] for r in plan["high"]})

    def test_facts_and_source_ids_preserved(self):
        cards, sources = B.load_cards(self.tmp)
        original = cards["GAR-0001"]["text"]
        plan = B.plan_card(cards["GAR-0001"], cards, sources)
        B.apply_plan(plan)
        new = cards["GAR-0001"]["path"].read_text(encoding="utf-8")
        self.assertIn("source_ids: [SRC-0001]", new)
        self.assertIn("#", new.split("---", 2)[2])  # body facts retained
        # no evidence_status mutation
        self.assertEqual(cards["GAR-0001"]["meta"].get("evidence_status"), "verified")

    def test_rollback_roundtrip(self):
        import json, shutil
        cards, sources = B.load_cards(self.tmp)
        plan = B.plan_card(cards["GAR-0001"], cards, sources)
        original = plan["original_text"]
        B.apply_plan(plan)
        rollback = self.tmp / "rollback"
        rollback.mkdir()
        (rollback / "GAR-0001.md").write_text(original, encoding="utf-8")
        manifest = self.tmp / "manifest.json"
        manifest.write_text(json.dumps({"rollback_dir": str(rollback), "files": [
            {"card_id": "GAR-0001", "path": "01-服装单品/GAR-0001.md"}]}), encoding="utf-8")
        self.assertEqual(B.main(["--rollback", str(manifest), "--root", str(self.tmp)]), 0)
        self.assertEqual(cards["GAR-0001"]["path"].read_text(encoding="utf-8"), original)

    def test_design_pilot_30_are_marked_and_visible(self):
        import csv, json, re
        report = json.loads((B.P5D / "design-pilot-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["design_cards"], 30)
        self.assertEqual(report["design_relations"], 30)
        rows = list(csv.DictReader((B.P5D / "DESIGN-PILOT.csv").open(encoding="utf-8")))
        self.assertEqual(len(rows), 30)
        cards, sources = B.load_cards()
        removed_invalid = {
            ("SCN-0001", "STY-0005"), ("LOOK-0019", "STR-0011"),
            ("LOOK-0003", "STR-0001"), ("LOOK-0017", "STR-0010"),
            ("LOOK-0008", "STR-0011"),
        }
        valid = 0
        for row in rows:
            card = cards[row["card_id"]]
            key = (row["card_id"], row["target"])
            if key in removed_invalid:
                # semantic P5-D review removed these; no visible design marker.
                self.assertNotIn("design relation (medium/review_queue", card["body"])
                continue
            self.assertIn("type=%s" % row["relation_type"], card["text"])
            self.assertIn("confidence=medium", card["text"])
            self.assertIn("review_status=review_queue", card["text"])
            self.assertIn("factual=false", card["text"])
            self.assertIn("design_only=true", card["text"])
            # visible, non-code markdown link
            self.assertIn("[[", card["body"])
            self.assertNotIn("`[[", card["body"])
            self.assertTrue(row["target"] in card["body"])
            valid += 1
        self.assertEqual(valid, 25)

    def test_pilot_30_actual(self):
        code = B.main(["--dry-run", "--pilot", "30", "--json"])
        self.assertEqual(code, 0)
        import json
        report = json.loads((B.P5D / "backfill-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["selected"], 30)
        self.assertEqual(report["non_idempotent"], [])
        self.assertGreater(report["queue"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
