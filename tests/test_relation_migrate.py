#!/usr/bin/env python3
"""P5-A relation migration tests: exact resolution, no guessing, idempotence,
typed flat relations, queue confidence, preserved source_ids/facts."""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P5 = ROOT / "11-验收/P5"
sys.path.insert(0, str(ROOT / "scripts"))
import relation_migrate as R  # noqa: E402

SRC_LINK = re.compile(r"\[\[(SRC-\d{3,4})-[^\]]+\]\]")
REL_TOKEN = re.compile(r"^  - 'target=([^;]+); type=([^;]+); direction=([^;]+); "
                       r"evidence=([^;]+); confidence=([^;]+); source_ids=([^;]*); "
                       r"rule=([^;']+)'$", re.M)
ALLOWED = {"appears_in_look", "uses_material", "may_have_part", "ensemble_with",
           "context_includes", "in_style", "look_appears_in_scene",
           "claim_supported_by"}


class RelationMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = R.load_cards()
        cls.sources = R.load_sources()
        cls.content = [c for c in cls.cards
                       if str(c["meta"].get("type")) != "source"]
        cls.by_id = {str(c["meta"].get("id")): c for c in cls.content
                     if c["meta"].get("id")}

    def test_every_source_id_resolves_exactly(self):
        missing = []
        for card in self.content:
            for sid in card["meta"].get("source_ids") or []:
                if sid not in self.sources:
                    missing.append((card["meta"].get("id"), sid))
        self.assertFalse(missing, missing[:10])

    def test_source_links_only_cited(self):
        for card in self.content:
            ids = [str(v) for v in card["meta"].get("source_ids") or []]
            for match in re.finditer(r"- \[\[(SRC-\d{3,4})-[^\]]+\]\] — cited source", card["body"]):
                self.assertIn(match.group(1), ids,
                              "linked source not in source_ids: %s" % card["path"])

    def test_flat_typed_relations(self):
        count = 0
        for card in self.content:
            for match in REL_TOKEN.finditer(card["text"]):
                target, rtype, direction, evidence, confidence, source_ids, rule = match.groups()
                count += 1
                self.assertIn(rtype, ALLOWED)
                self.assertEqual(confidence, "high")
                self.assertIn(direction, ("outgoing", "incoming"))
                self.assertIn(target, self.sources) if target.startswith("SRC-") else self.assertIn(target, self.by_id)
                for sid in [s for s in source_ids.split(",") if s]:
                    self.assertIn(sid, self.sources)
        self.assertGreater(count, 0)

    def test_review_queue_not_high(self):
        path = P5 / "REVIEW-QUEUE.csv"
        self.assertTrue(path.exists())
        import csv
        with path.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertTrue(rows)
        self.assertTrue(all(row["confidence"] != "high" for row in rows))

    def test_idempotent_full_plan(self):
        proc = R.main(["--dry-run", "--full", "--no-backup"])
        self.assertEqual(proc, 0)
        report = json.loads((P5 / "migration-report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["changed_cards"], 0)
        self.assertEqual(report["non_idempotent"], [])

    def test_preserved_source_ids_and_original_body(self):
        # Rollback copies are the original cards captured before migration.
        originals = {}
        for directory in sorted(P5.glob("rollback-*")):
            for path in directory.glob("*.md"):
                originals[path.stem] = path.read_text(encoding="utf-8")
        self.assertTrue(originals)
        checked = 0
        for cid, original in originals.items():
            current = self.by_id.get(cid)
            if not current:
                continue
            checked += 1
            old_meta = R.split_frontmatter(original)[0]
            new_meta = R.split_frontmatter(current["text"])[0]
            import yaml
            old = yaml.safe_load(old_meta) or {}
            new = yaml.safe_load(new_meta) or {}
            self.assertEqual(old.get("source_ids") or [], new.get("source_ids") or [])
            # facts outside generated source-link/relations additions survive.
            old_body = R.split_frontmatter(original)[1]
            for marker in ("## 来源链接", "## 相关卡片"):
                if marker in old_body:
                    prefix = old_body.split(marker)[0]
                    self.assertTrue(current["body"].startswith(prefix.strip()),
                                    cid)
                    break
            else:
                self.assertTrue(current["body"].startswith(old_body.strip()), cid)
        self.assertGreater(checked, 20)

    def test_rollback_roundtrip(self):
        import tempfile, shutil
        source = next(c for c in self.content if c["meta"].get("id") == "GAR-0008")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "01-服装单品/上装/GAR-0008-马甲.md"
            target.parent.mkdir(parents=True)
            target.write_text("BROKEN", encoding="utf-8")
            rollback = root / "rollback"
            rollback.mkdir()
            (rollback / "GAR-0008.md").write_text(source["text"], encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({
                "rollback_dir": str(rollback),
                "files": [{"card_id": "GAR-0008",
                           "path": "01-服装单品/上装/GAR-0008-马甲.md"}],
            }), encoding="utf-8")
            self.assertEqual(R.main(["--rollback", str(manifest), "--root", tmp]), 0)
            self.assertEqual(target.read_text(encoding="utf-8"), source["text"])

    def test_graph_apply_builds_unresolved_queue(self):
        graph = __import__("graph_apply").build_graph(ROOT, P5 / "graph-unresolved.csv")
        self.assertIn("nodes", graph)
        self.assertIn("edges", graph)


if __name__ == "__main__":
    unittest.main(verbosity=2)
