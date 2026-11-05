#!/usr/bin/env python3
"""R1.2-A Obsidian portable config tests (isolated vault copy)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/obsidian_config.py"
sys.path.insert(0, str(ROOT / "scripts"))
import obsidian_config as oc  # noqa: E402

KNOWLEDGE = ["00-系统", "01-服装单品", "02-结构细节", "03-材质纹样", "04-来源",
             "05-风格体系", "06-时代地域", "07-剧情场景", "09-造型组合",
             "10-提示词模板"]


def make_isolated_vault():
    tmp = Path(tempfile.mkdtemp(prefix="obsidian-r12-"))
    for name in KNOWLEDGE:
        shutil.copytree(ROOT / name, tmp / name)
    for name in ("README.md",):
        if (ROOT / name).exists():
            shutil.copy2(ROOT / name, tmp / name)
    shutil.copytree(ROOT / ".obsidian", tmp / ".obsidian")
    # User-owned settings/plugins/themes/hotkeys/workspace must survive.
    app_path = tmp / ".obsidian/app.json"
    app = json.loads(app_path.read_text(encoding="utf-8"))
    app["userIgnoreFilters"] = ["my-private/"]
    app["myCustomKey"] = "keep-me"
    app_path.write_text(json.dumps(app, ensure_ascii=False, indent=2), encoding="utf-8")
    graph_path = tmp / ".obsidian/graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["scale"] = 0.42
    graph["myGraphKey"] = {"keep": True}
    graph.pop("repelStrength", None)
    graph_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    (tmp / ".obsidian/hotkeys.json").write_text('{"custom": "keep"}', encoding="utf-8")
    (tmp / ".obsidian/workspace.json").write_text('{"custom": "workspace"}', encoding="utf-8")
    (tmp / ".obsidian/appearance.json").write_text('{"theme": "custom"}', encoding="utf-8")
    (tmp / ".obsidian/themes").mkdir()
    (tmp / ".obsidian/themes/custom.css").write_text("/* user theme */", encoding="utf-8")
    return tmp


def run(vault, *args):
    return subprocess.run([sys.executable, str(SCRIPT), "--vault", str(vault), *args],
                          cwd=str(ROOT), capture_output=True, text=True)


class ObsidianConfigTests(unittest.TestCase):
    def setUp(self):
        self.vault = make_isolated_vault()
        self.obsidian = self.vault / ".obsidian"

    def tearDown(self):
        shutil.rmtree(self.vault, ignore_errors=True)

    def test_scope_488_0_1(self):
        stats = oc.scope_stats(self.vault)
        self.assertEqual(stats["nodes"], 488)
        self.assertEqual(stats["zero_degree"], 0)
        self.assertEqual(stats["components"], 1)

    def test_dry_run_default_does_not_write(self):
        before = (self.obsidian / "app.json").read_bytes()
        proc = run(self.vault, "--diff")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(before, (self.obsidian / "app.json").read_bytes())

    def test_apply_preserves_user_keys_and_files(self):
        hotkeys = (self.obsidian / "hotkeys.json").read_bytes()
        workspace = (self.obsidian / "workspace.json").read_bytes()
        appearance = (self.obsidian / "appearance.json").read_bytes()
        proc = run(self.vault, "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        app = json.loads((self.obsidian / "app.json").read_text(encoding="utf-8"))
        graph = json.loads((self.obsidian / "graph.json").read_text(encoding="utf-8"))
        self.assertIn("my-private/", app["userIgnoreFilters"])
        self.assertEqual(app["myCustomKey"], "keep-me")
        self.assertEqual(graph["scale"], 0.42)
        self.assertEqual(graph["myGraphKey"], {"keep": True})
        self.assertEqual(hotkeys, (self.obsidian / "hotkeys.json").read_bytes())
        self.assertEqual(workspace, (self.obsidian / "workspace.json").read_bytes())
        self.assertEqual(appearance, (self.obsidian / "appearance.json").read_bytes())
        self.assertTrue((self.obsidian / "themes/custom.css").exists())
        # configured scope stays 488/0/1
        stats = oc.scope_stats(self.vault)
        self.assertEqual((stats["nodes"], stats["zero_degree"], stats["components"]),
                         (488, 0, 1))

    def test_idempotent_and_restore(self):
        proc = run(self.vault, "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        report = json.loads(proc.stdout)
        backup = report["backup"]
        self.assertTrue(backup)
        app_after = (self.obsidian / "app.json").read_bytes()
        graph_after = (self.obsidian / "graph.json").read_bytes()
        proc2 = run(self.vault, "--apply")
        self.assertEqual(proc2.returncode, 0, proc2.stderr)
        self.assertFalse(json.loads(proc2.stdout)["changed"])
        self.assertEqual(app_after, (self.obsidian / "app.json").read_bytes())
        self.assertEqual(graph_after, (self.obsidian / "graph.json").read_bytes())
        proc3 = run(self.vault, "--restore", backup)
        self.assertEqual(proc3.returncode, 0, proc3.stderr)
        restored_app = json.loads((self.obsidian / "app.json").read_text(encoding="utf-8"))
        self.assertIn("my-private/", restored_app["userIgnoreFilters"])
        self.assertEqual(restored_app["myCustomKey"], "keep-me")

    def test_templates_contain_no_absolute_paths_or_secrets(self):
        for name in ("app.recommended.json", "graph.recommended.json"):
            text = (ROOT / "config/obsidian" / name).read_text(encoding="utf-8")
            self.assertNotIn("/Users/", text)
            self.assertNotIn("api_key", text.lower())

    def test_scope_report_cli(self):
        proc = run(self.vault, "--scope-report", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["nodes"], 488)
        self.assertEqual(data["zero_degree"], 0)
        self.assertEqual(data["components"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
