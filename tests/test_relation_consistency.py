#!/usr/bin/env python3
"""P5-B relation consistency tests: missing/orphan/duplicate/low-confidence/MOC."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import relation_consistency as rc  # noqa: E402


def card(meta_lines, body):
    return "---\n" + "\n".join(meta_lines) + "\n---\n" + body


SOURCE = card(["id: SRC-0001", "type: source", "evidence_status: verified",
               "name_zh: test source"], "")
BASE = ["id: GAR-0001", "type: garment", "evidence_status: verified",
        "source_ids: [SRC-0001]"]


class RelationConsistencyTests(unittest.TestCase):
    def make_root(self, body, relation, source=True):
        tmp = tempfile.mkdtemp()
        root = Path(tmp)
        (root / "01-服装单品").mkdir(parents=True)
        (root / "04-来源").mkdir(parents=True)
        (root / "00-系统/MOC").mkdir(parents=True)
        if source:
            (root / "04-来源/SRC-0001-test.md").write_text(SOURCE, encoding="utf-8")
        text = card(BASE + [relation], body)
        (root / "01-服装单品/GAR-0001.md").write_text(text, encoding="utf-8")
        (root / "00-系统/MOC/服装单品.md").write_text(
            card(["id: MOC-0001", "type: moc"], "- [[GAR-0001]]"), encoding="utf-8")
        return root

    def test_clean_relation(self):
        rel = "relations: [\"target=SRC-0001; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0001; rule=R-SOURCE-IDS\"]"
        root = self.make_root("## 来源链接\n- [[SRC-0001-test]]\n", rel)
        report = rc.check(root)
        self.assertEqual(report["error_count"], 0, report["errors"])
        self.assertTrue(report["moc_files_skipped"])

    def test_missing_visible_link(self):
        rel = "relations: [\"target=SRC-0001; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0001; rule=R-SOURCE-IDS\"]"
        report = rc.check(self.make_root("no link\n", rel))
        self.assertIn("missing_visible_wikilink",
                      [e["code"] for e in report["errors"]])

    def test_orphan_source_link(self):
        report = rc.check(self.make_root("## 来源链接\n- [[SRC-0001-test]] — cited source\n",
                                         "relations: []"))
        self.assertIn("orphan_cited_source_link",
                      [e["code"] for e in report["errors"]])

    def test_duplicate_relation(self):
        rel = "relations: [\"target=SRC-0001; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0001; rule=R-SOURCE-IDS\", \"target=SRC-0001; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0001; rule=R-SOURCE-IDS\"]"
        report = rc.check(self.make_root("## 来源链接\n- [[SRC-0001-test]]\n", rel))
        self.assertIn("duplicate_relation",
                      [e["code"] for e in report["errors"]])

    def test_low_confidence_in_body(self):
        rel = "relations: [\"target=SRC-0001; type=claim_supported_by; direction=outgoing; evidence=interpretive; confidence=medium; source_ids=SRC-0001; rule=R-SOURCE-IDS\"]"
        report = rc.check(self.make_root("## 来源链接\n- [[SRC-0001-test]]\n", rel))
        self.assertIn("low_confidence_in_body",
                      [e["code"] for e in report["errors"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
