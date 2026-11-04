#!/usr/bin/env python3
"""P5-C source visible link fixer tests."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import link_p5c_sources as lp  # noqa: E402


class LinkP5CTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cards = lp.load_cards()
        cls.sources = lp.source_map()

    def test_target_set_is_35(self):
        targets = [cid for cid in lp.TARGETS if cid in self.cards]
        self.assertEqual(len(lp.TARGETS), 35)
        self.assertEqual(len(targets), 35)

    def test_exact_source_mapping_no_guess(self):
        for cid in lp.TARGETS:
            plan = lp.plan_card(self.cards[cid], self.sources)
            for item in plan["replaced"]:
                self.assertIn(item["source_id"], self.sources)
                self.assertEqual(self.sources[item["source_id"]], item["stem"])
            for sid in plan["missing"]:
                self.assertNotIn(sid, self.sources)

    def test_idempotent_after_apply(self):
        changed = 0
        for cid in lp.TARGETS:
            if lp.plan_card(self.cards[cid], self.sources)["changed"]:
                changed += 1
        self.assertEqual(changed, 0)

    def test_source_visible_rate(self):
        total = linked = 0
        for cid in lp.TARGETS:
            match = lp.SRC_SECTION.search(self.cards[cid]["text"])
            if not match:
                continue
            section = match.group(0)
            ids = list(dict.fromkeys(lp.SRC_ID.findall(section)))
            total += len(ids)
            linked += sum(1 for sid in ids
                          if any(sid in link for link in lp.WIKILINK.findall(section)))
        self.assertGreater(total, 0)
        self.assertEqual(linked, total)

    def test_dry_run_is_read_only(self):
        before = {cid: self.cards[cid]["text"] for cid in lp.TARGETS}
        proc = subprocess.run([sys.executable, "scripts/link_p5c_sources.py",
                               "--dry-run", "--json"], cwd=str(ROOT),
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["targets"], 35)
        after = lp.load_cards()
        for cid in lp.TARGETS:
            self.assertEqual(before[cid], after[cid]["text"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
