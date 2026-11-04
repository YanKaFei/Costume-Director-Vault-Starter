#!/usr/bin/env python3
"""P5-B relation query filters: card YAML + structured candidate index."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def query(*args):
    proc = subprocess.run([sys.executable, "scripts/query.py", *[str(a) for a in args], "--json"], cwd=str(ROOT), capture_output=True, text=True)
    return proc, json.loads(proc.stdout) if proc.stdout.strip() else []


class RelationQueryTests(unittest.TestCase):
    def test_claim_supported_by_source(self):
        proc, rows = query("--relation-type", "claim_supported_by",
                           "--related-to", "SRC-0109", "--confidence", "high",
                           "--evidence", "verified")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(rows)
        self.assertEqual(rows[0]["id"], "GAR-0008")
        relation = rows[0]["relations"][0]
        self.assertEqual(relation["target"], "SRC-0109")
        self.assertTrue(relation["target_path"].startswith("04-来源/"))

    def test_part_and_accessory(self):
        for rtype in ("may_have_part", "ensemble_with"):
            proc, rows = query("--relation-type", rtype, "--confidence", "medium")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(rows, rtype)
            for row in rows:
                for relation in row["relations"]:
                    self.assertTrue(relation["target_path"])

    def test_material_period_outfit(self):
        for rtype in ("uses_material", "context_includes", "appears_in_look"):
            proc, rows = query("--relation-type", rtype, "--limit", 5)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(rows, rtype)
            for row in rows:
                self.assertTrue(row["relations"], rtype)

    def test_related_to_garment(self):
        proc, rows = query("--relation-type", "appears_in_look",
                           "--related-to", "GAR-0002")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(rows)
        for row in rows:
            self.assertTrue(any(r["target"] == "GAR-0002" for r in row["relations"]))

    def test_no_wikilink_only_inference(self):
        # A card with no typed relation must not be returned by a relation filter.
        proc, rows = query("--relation-type", "claim_supported_by", "--id", "GAR-0043",
                           "--relations-from", "cards")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertFalse(rows)


if __name__ == "__main__":
    unittest.main(verbosity=2)
