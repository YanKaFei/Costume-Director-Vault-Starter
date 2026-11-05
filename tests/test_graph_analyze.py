#!/usr/bin/env python3
"""P5-F graph resolution tests: EXAMPLE IDs, code examples, real orphans."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/graph_analyze.py"


def make_vault(card_body="", nav_body="", extra=""):
    tmp = Path(tempfile.mkdtemp())
    for d in ("00-系统", "01-服装单品", "04-来源", "09-造型组合"):
        (tmp / d).mkdir(parents=True, exist_ok=True)
    (tmp / "01-服装单品/GAR-EXAMPLE-001-white-shirt.md").write_text(
        "---\nid: GAR-EXAMPLE-001\ntype: garment\nevidence_status: example\n"
        "source_ids: [SRC-0001]\n---\n# example\n" + card_body,
        encoding="utf-8")
    (tmp / "04-来源/SRC-0001-test.md").write_text(
        "---\nid: SRC-0001\ntype: source\nevidence_status: verified\n---\n# source\n",
        encoding="utf-8")
    (tmp / "00-系统/关系类型.md").write_text(
        "---\nid: REL-TYPES\ntype: navigation\n---\n# schema\n" + nav_body,
        encoding="utf-8")
    if extra:
        (tmp / extra).write_text(
            "---\nid: LOOK-EXAMPLE-001\ntype: look\nevidence_status: example\n"
            "look_items: [GAR-EXAMPLE-001]\n---\n# look\n", encoding="utf-8")
    return tmp


def run_graph(root):
    out = root / "graph.json"
    proc = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root),
                           "--json", str(out)], capture_output=True, text=True)
    return proc, json.loads(out.read_text(encoding="utf-8")) if out.exists() else None


class GraphAnalyzeTests(unittest.TestCase):
    def test_example_id_resolves(self):
        root = make_vault(extra="09-造型组合/LOOK-EXAMPLE-001.md")
        proc, graph = run_graph(root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(graph["typed_unresolved"], 0)
        self.assertGreaterEqual(graph["typed_edges"], 2)

    def test_inline_and_fenced_code_ignored(self):
        nav = "Inline `[[target]]` example.\n\n```\n[[fake-link]]\n```\n"
        root = make_vault(nav_body=nav)
        proc, graph = run_graph(root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(graph["unresolved_wikilinks"], {})

    def test_real_unresolved_still_reported(self):
        root = make_vault(card_body="\nSee [[GAR-9999-missing]].\n")
        proc, graph = run_graph(root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("GAR-9999-missing", graph["unresolved_wikilinks"])

    def test_production_graph_is_clean(self):
        out = ROOT / "11-验收/P5F/test-graph.json"
        proc = subprocess.run([sys.executable, str(SCRIPT), "--json", str(out)],
                              cwd=str(ROOT), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        graph = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(graph["typed_unresolved"], 0)
        self.assertEqual(graph["unresolved_wikilinks"], {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
