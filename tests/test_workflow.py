#!/usr/bin/env python3
"""Regression tests for scripts/workflow.py (P3.5).

Run with:
    python3 tests/test_workflow.py

Fixtures: Macbeth public-domain excerpt, contemporary rain-night scene,
1930s Shanghai historical scene, sparse-unknown scene, and a no-character
exit-3 fixture.  Assertions cover real IDs/sources, A/B/C distinctness,
evidence completeness, unknown handling, continuity states, English prompts,
and CLI exit codes 0/2/3.
"""

import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import costume_lib as lib  # noqa: E402
import workflow  # noqa: E402

FIXTURE_DIR = ROOT / "tests/fixtures"
RUN_DIR = ROOT / "11-验收/P3.5/workflow-runs"
WORKFLOW = ROOT / "scripts/workflow.py"
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

USABLE = ["macbeth", "rain_night", "shanghai_1930s", "sparse_unknown"]


def run_workflow(name, meta=None, out=None, script=None):
    meta = meta if meta is not None else FIXTURE_DIR / (name + "_meta.json")
    script = script if script is not None else FIXTURE_DIR / (name + ".txt")
    out = out if out is not None else RUN_DIR / ("test-" + name)
    cmd = [sys.executable, str(WORKFLOW), "--script", str(script)]
    if meta is not None:
        cmd += ["--meta", str(meta)]
    cmd += ["--out", str(out)]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    result = None
    result_path = Path(out) / "workflow-result.json"
    if result_path.exists():
        result = json.loads(result_path.read_text(encoding="utf-8"))
    return proc, result, Path(out)


def card_indexes():
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    sources = {lib.get_str(card["meta"], "id"): card for card in cards
               if lib.norm_text(card["meta"].get("type")) == "source"}
    return by_id, sources


class WorkflowRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs = {}
        cls.by_id, cls.sources = card_indexes()
        for name in USABLE:
            proc, result, out = run_workflow(name)
            cls.runs[name] = {"proc": proc, "result": result, "out": out}

    # ------------------------------------------------------------------
    def test_exit_codes_0_2_3_and_outputs(self):
        for name in USABLE:
            run = self.runs[name]
            self.assertEqual(run["proc"].returncode, 0,
                             "%s stderr=%s" % (name, run["proc"].stderr[-500:]))
            self.assertIsNotNone(run["result"])
            for filename in ("character-dossier.md", "scene-costume-table.md",
                             "scene-costume-table.csv", "full-looks.md",
                             "prompts.md", "continuity-plan.md",
                             "fact-evidence-inference.md", "workflow-result.json"):
                self.assertTrue((run["out"] / filename).exists(),
                                "%s missing %s" % (name, filename))
        # exit 2: missing script
        proc, _, _ = run_workflow("macbeth", script=ROOT / "tests/fixtures/missing.txt",
                                  out=RUN_DIR / "test-invalid")
        self.assertEqual(proc.returncode, 2)
        # exit 2: malformed meta JSON
        bad_meta = ROOT / "tests/fixtures/_bad_meta.json"
        bad_meta.write_text("{not-json", encoding="utf-8")
        try:
            proc, _, _ = run_workflow("macbeth", meta=bad_meta,
                                      out=RUN_DIR / "test-invalid")
            self.assertEqual(proc.returncode, 2)
        finally:
            bad_meta.unlink(missing_ok=True)
        # exit 2: --out outside the vault is rejected before any write (D3)
        outside = Path("/tmp") / ("costume-workflow-outside-%d" % os.getpid())
        if outside.exists():
            import shutil
            shutil.rmtree(outside)
        try:
            proc, _, _ = run_workflow("macbeth", out=outside)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("inside the vault", proc.stderr)
            self.assertFalse(outside.exists(), "workflow wrote outside the vault")
        finally:
            if outside.exists():
                import shutil
                shutil.rmtree(outside)
        # exit 3: no characters anywhere
        proc, result, _ = run_workflow("no_characters",
                                       out=RUN_DIR / "test-no-characters")
        self.assertEqual(proc.returncode, 3)

    # ------------------------------------------------------------------
    def test_real_ids_and_sources(self):
        for name, run in self.runs.items():
            result = run["result"]
            for character, stages in result["recommendations"].items():
                for stage_id, rec in stages.items():
                    self.assertIn(rec["exit"], (0, 3))
                    data = rec.get("data")
                    self.assertIsInstance(data, dict)
                    self.assertGreaterEqual(len(data.get("looks") or []), 3,
                                            "%s/%s/%s looks" % (name, character, stage_id))
                    for look in data["looks"]:
                        self.assertIn(look["look_ref"], ("A", "B", "C"))
                        self.assertTrue(look.get("items"))
                        for item in look["items"]:
                            self.assertIn(item["id"], self.by_id,
                                          "fabricated card ID %s" % item["id"])
                            self.assertNotEqual(item.get("evidence_status"), "example",
                                                "example card used in workflow look")
                            for sid in item.get("source_ids") or []:
                                self.assertIn(sid, self.sources,
                                              "fabricated source ID %s" % sid)

    # ------------------------------------------------------------------
    def test_abc_distinct(self):
        for name, run in self.runs.items():
            result = run["result"]
            self.assertTrue(result["checks"]["abc_distinct"], name)
            for character, stages in result["recommendations"].items():
                for stage_id, rec in stages.items():
                    looks = rec["data"].get("looks") or []
                    if len(looks) < 3:
                        continue
                    sets = [set(item["id"] for item in look["items"])
                            for look in looks[:3]]
                    self.assertNotEqual(sets[0], sets[1])
                    self.assertNotEqual(sets[0], sets[2])
                    self.assertNotEqual(sets[1], sets[2])

    # ------------------------------------------------------------------
    def test_evidence_fields_complete(self):
        for name, run in self.runs.items():
            result = run["result"]
            self.assertTrue(result["checks"]["evidence_complete"], name)
            self.assertTrue(result["checks"]["source_ids_resolve"], name)
            for character, stages in result["recommendations"].items():
                for stage_id, rec in stages.items():
                    for look in rec["data"]["looks"]:
                        evidence = look.get("evidence")
                        self.assertIsInstance(evidence, dict)
                        for key in ("source_ids", "item_evidence", "source_urls"):
                            self.assertIn(key, evidence)
                        self.assertTrue(evidence["item_evidence"])
                        self.assertFalse(evidence.get("missing_urls"))
                        for sid in evidence["source_ids"]:
                            self.assertIn(sid, self.sources)
                        for entry in evidence.get("source_urls") or []:
                            self.assertTrue(str(entry.get("url", "")).startswith("http"))
            # historical fixture should return exact/verified evidence
            if name == "shanghai_1930s":
                tiers = [look.get("evidence_tier")
                         for stages in result["recommendations"].values()
                         for rec in stages.values()
                         for look in rec["data"]["looks"]]
                self.assertIn("exact", tiers)

    # ------------------------------------------------------------------
    def test_unknowns_not_invented(self):
        result = self.runs["sparse_unknown"]["result"]
        unknown_text = "\n".join(result["unknowns"])
        for field in ("period", "region", "budget", "art_direction"):
            self.assertIn(field, unknown_text)
        for character in result["characters"]:
            self.assertIn(character["occupation"], ("unknown", ""))
        self.assertTrue(any("unknown" in issue for issue in result["continuity"]["issues"]))
        self.assertIn("**Unknown / not provided:**",
                      (self.runs["sparse_unknown"]["out"] / "character-dossier.md")
                      .read_text(encoding="utf-8"))
        # unknown scene state is explicitly unknown in continuity output
        plan = result["continuity"]["plan"]
        for character_plan in plan.values():
            for state in character_plan["scene_states"]:
                self.assertEqual(set(state["state"].values()), {"unknown"})

    # ------------------------------------------------------------------
    def test_continuity_states(self):
        rain = self.runs["rain_night"]["result"]
        self.assertEqual(rain["scenes"][0]["state"]["wetness"], "wet")
        self.assertEqual(rain["scenes"][1]["state"]["wetness"], "dry")
        self.assertEqual(rain["scenes"][0]["state"]["damage"], "none")
        for character, plan in rain["continuity"]["plan"].items():
            self.assertTrue(plan["anchors"], "%s has no anchor items" % character)
            self.assertEqual([state["scene"] for state in plan["scene_states"]],
                             ["S1", "S2"])
        shanghai = self.runs["shanghai_1930s"]["result"]
        self.assertEqual(shanghai["scenes"][0]["state"]["wetness"], "wet")
        self.assertEqual(shanghai["scenes"][1]["state"]["wetness"], "dry")
        # no invented damage anywhere in explicitly dry/none states
        for name in ("rain_night", "shanghai_1930s"):
            for scene in self.runs[name]["result"]["scenes"]:
                self.assertIn(scene["state"]["damage"], ("none", "unknown", "present"))
                if scene["state"]["wetness"] == "dry":
                    self.assertNotEqual(scene["state"]["damage"], "present")

    # ------------------------------------------------------------------
    def test_english_prompts(self):
        for name, run in self.runs.items():
            for stages in run["result"]["recommendations"].values():
                for rec in stages.values():
                    for look in rec["data"]["looks"]:
                        for key in ("prompt_image_en", "prompt_video_en"):
                            prompt = look.get(key) or ""
                            self.assertTrue(prompt.strip(), "%s %s empty" % (name, key))
                            self.assertIsNone(CJK_RE.search(prompt),
                                              "%s %s contains CJK" % (name, key))
                            self.assertGreater(len(prompt.split()), 8)

    # ------------------------------------------------------------------
    def test_act_scene_stage_mapping(self):
        PROC, result, out = run_workflow(
            "macbeth_actscene", out=RUN_DIR / "test-macbeth-actscene")
        self.assertIn(PROC.returncode, (0, 3))
        self.assertEqual([scene["id"] for scene in result["scenes"]],
                         ["S1", "S2", "S3", "S4"])
        self.assertEqual([(scene["act_number"], scene["scene_number"])
                          for scene in result["scenes"]],
                         [(1, 3), (1, 5), (2, 2), (5, 1)])
        mapping = {stage["id"]: stage["scenes"] for stage in result["stage_list"]}
        self.assertEqual(mapping.get("M1"), ["S1"])
        self.assertEqual(mapping.get("M2"), ["S3"])
        self.assertEqual(mapping.get("L1"), ["S2"])
        self.assertEqual(mapping.get("L3"), ["S4"])
        self.assertNotIn("unassigned", mapping)
        self.assertEqual(result["stage_mapping"]["M1"]["refs"], ["1-3"])
        self.assertEqual(result["stage_mapping"]["M2"]["refs"], ["2-2"])
        # S-id compatibility + direct resolver forms
        parsed = workflow.split_scenes(
            (ROOT / "tests/fixtures/macbeth_actscene.txt").read_text(encoding="utf-8"))
        self.assertEqual(workflow.resolve_scene_ref("S1", parsed), "S1")
        self.assertEqual(workflow.resolve_scene_ref("1-3", parsed), "S1")
        self.assertEqual(workflow.resolve_scene_ref("2.2", parsed), "S3")
        self.assertEqual(workflow.resolve_scene_ref("Act 5 Scene 1", parsed), "S4")
        self.assertIsNone(workflow.resolve_scene_ref("9-9", parsed))

    def test_macbeth_public_domain_and_english_prompt(self):
        result = self.runs["macbeth"]["result"]
        self.assertIn("Macbeth", result["title"])
        self.assertGreaterEqual(len(result["scenes"]), 3)
        self.assertEqual([scene["id"] for scene in result["scenes"]],
                         ["S1", "S2", "S3"])
        stage_ids = [stage["id"] for stage in result["stage_list"]]
        self.assertNotEqual(stage_ids, ["unassigned"])
        self.assertTrue(any(stage["id"] != "unassigned" and stage["scenes"]
                            for stage in result["stage_list"]))
        names = [character["name"] for character in result["characters"]]
        self.assertIn("Macbeth", names)
        self.assertIn("Banquo", names)
        # every character has real looks for each stage where they appear
        for character in result["characters"]:
            if character["present_scenes"]:
                self.assertTrue(result["recommendations"][character["name"]])
        # ACT/SCENE headings keep scene boundaries; separate ACT lines do not
        # create empty fragment scenes or an all-unassigned stage.
        text = ("ACT I\nSCENE I. A desert place.\nFIRST WITCH: hail\n"
                "SCENE II. A heath near Forres.\nMACBETH: so foul and fair\n")
        parsed = workflow.split_scenes(text)
        self.assertEqual([scene["id"] for scene in parsed], ["S1", "S2"])
        self.assertTrue(all("ACT I" in scene["title"] for scene in parsed))
        self.assertFalse(any(not scene["body"].strip() for scene in parsed))
        # saved Macbeth run for the delivery exists
        self.assertTrue((RUN_DIR / "macbeth/workflow-result.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
