#!/usr/bin/env python3
"""P4-3 Outfit Composer regression tests (>=8 scenarios).

Run:
    python3 11-验收/P4-COMPOSER/test_outfit.py

Saves each composer output under 11-验收/P4-COMPOSER/runs/ and writes
SUMMARY.md + comparison.json.  Checks real IDs/SRC, full slots, A/B/C
structural differences (>=2 items), palette/material/silhouette metrics,
English prompts, continuity states, evidence gaps, and a legacy-vs-new
comparison against scripts/recommend.py.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
RUNS = HERE / "runs"
WORKFLOW = ROOT / "scripts/outfit.py"
RECOMMEND = ROOT / "scripts/recommend.py"
sys.path.insert(0, str(ROOT / "scripts"))
import costume_lib as lib  # noqa: E402

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
SCENARIOS = {
    "macbeth": ("macbeth.json", 0, 3),
    "lady_macbeth": ("lady_macbeth.json", 0, 3),
    "cross_cultural_ghana": ("T36.json", 0, 3),
    "rain_continuity": ("rain_continuity.json", 0, 3),
    "low_budget": ("low_budget.json", 0, 3),
    "closeup": ("closeup.json", 0, 3),
    "action_dance": ("T04.json", 0, 3),
    "occupation_nurse": ("T31.json", 0, 3),
    "conflict_reject": ("conflict.json", None, None),
}


def run(cmd):
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return proc


def load_cards():
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    sources = {lib.get_str(card["meta"], "id"): card for card in cards
               if lib.norm_text(card["meta"].get("type")) == "source"}
    return by_id, sources


def composer(name, meta):
    fixture = FIX / meta
    out = RUNS / (name + ".json")
    proc = run([sys.executable, str(WORKFLOW), "--input", str(fixture), "--json",
                "--out", str(out)])
    data = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
    return proc, data, out


def fail(name, reasons):
    return {"case": name, "pass": False, "reasons": reasons}


def main():
    RUNS.mkdir(parents=True, exist_ok=True)
    by_id, sources = load_cards()
    results = []
    outputs = {}
    for name, (meta, expected_exit, expected_looks) in SCENARIOS.items():
        proc, data, out = composer(name, meta)
        outputs[name] = data
        reasons = []
        if data is None:
            reasons.append("no JSON output")
        else:
            if proc.returncode not in ((expected_exit,) if expected_exit is not None
                                       else (0, 3)):
                reasons.append("exit %s (expected %s)" % (proc.returncode, expected_exit))
            looks = data.get("looks") or []
            if expected_looks is not None and len(looks) != expected_looks:
                reasons.append("looks=%d expected %d" % (len(looks), expected_looks))
            if name != "conflict_reject":
                if not data.get("checks", {}).get("abc_pairwise_ge_2"):
                    reasons.append("A/B/C pairwise item difference <2")
                if len(looks) >= 3:
                    for i in range(3):
                        for j in range(i + 1, 3):
                            a = {item["id"] for item in looks[i]["items"]}
                            b = {item["id"] for item in looks[j]["items"]}
                            if len(a.symmetric_difference(b)) < 2:
                                reasons.append("look diff <2 between %s/%s" % (
                                    looks[i]["look_ref"], looks[j]["look_ref"]))
            else:
                if not any(any(word in warning for word in
                               ("conflict", "historical", "gap", "unknown", "evidence"))
                           for warning in data.get("warnings") or []):
                    reasons.append("conflict case did not report a conflict/gap")
            for look in looks:
                for item in look.get("items", []):
                    if item["id"] not in by_id:
                        reasons.append("fabricated ID %s" % item["id"])
                    if item.get("evidence_status") == "example":
                        reasons.append("example card in composed look %s" % item["id"])
                    for sid in item.get("source_ids") or []:
                        if sid not in sources:
                            reasons.append("unknown SRC %s" % sid)
                for sid in look.get("missing_source_ids") or []:
                    if sid:
                        reasons.append("missing source %s" % sid)
                if not look.get("prompt_image") or not look.get("prompt_video"):
                    reasons.append("missing English prompt")
                if CJK.search(look.get("prompt_image", "")) or CJK.search(look.get("prompt_video", "")):
                    reasons.append("non-English prompt")
                if not look.get("prompt_negative"):
                    reasons.append("missing negative constraints")
                palette = look.get("palette") or {}
                if not palette.get("colors") or not (0 <= palette.get("harmony", -1) <= 1):
                    reasons.append("invalid palette metrics")
                materials = look.get("materials") or {}
                if not (0 <= materials.get("harmony", -1) <= 1):
                    reasons.append("invalid material metrics")
                if (look.get("silhouette") or {}).get("shape") not in ("A", "H", "X", "Y", "O", "I"):
                    reasons.append("invalid silhouette")
                if not look.get("source_ids"):
                    reasons.append("look has no SRC provenance")
            checks = data.get("checks") or {}
            for key in ("ids_all_exist", "source_ids_resolve", "real_ids_only"):
                if not checks.get(key):
                    reasons.append("check failed: %s" % key)
            if name != "conflict_reject":
                if not data.get("completeness", {}).get("all_have_torso"):
                    reasons.append("missing torso coverage")
                if not data.get("completeness", {}).get("all_have_footwear"):
                    reasons.append("missing footwear")
                # accessory/carried may be unavailable; require either slot or warning
                for slot in ("accessory", "carried_prop"):
                    covered = data["completeness"].get("all_have_" + slot)
                    if not covered and not any(slot in warning for warning in data.get("warnings", [])):
                        reasons.append("missing %s without warning" % slot)
            if name == "rain_continuity":
                states = data.get("continuity", {}).get("states") or []
                if [s.get("wetness") for s in states] != ["wet", "dry"]:
                    reasons.append("rain continuity state chain is not wet->dry")
            if name == "low_budget":
                if not any("unknown" in state.get("wetness", "unknown")
                           for state in data.get("continuity", {}).get("states", [])):
                    reasons.append("unspecified continuity state should stay unknown")
        results.append({"case": name, "pass": not reasons, "reasons": reasons,
                        "output": str(out.relative_to(ROOT))})
    # Old-vs-new comparison on three representative fixtures.
    comparison = {}
    for name in ("macbeth", "cross_cultural_ghana", "occupation_nurse"):
        fixture = FIX / SCENARIOS[name][0]
        old_path = RUNS / (name + "-legacy-recommend.json")
        proc = run([sys.executable, str(RECOMMEND), str(fixture),
                    "--json", "--out", str(old_path)])
        old = json.loads(old_path.read_text(encoding="utf-8")) if old_path.exists() else {}
        new = outputs[name]
        if not new:
            continue
        old_looks = old.get("looks") or []
        new_looks = new.get("looks") or []
        old_count = len(old_looks[0].get("items") or []) if old_looks else 0
        new_count = len(new_looks[0].get("items") or []) if new_looks else 0
        old_diff = 0
        if len(old_looks) >= 3:
            old_diff = min(len({item["id"] for item in old_looks[i]["items"]} ^
                               {item["id"] for item in old_looks[j]["items"]})
                           for i, j in ((0, 1), (0, 2), (1, 2)))
        new_diff = min((len({item["id"] for item in new_looks[i]["items"]} ^
                             {item["id"] for item in new_looks[j]["items"]})
                        for i, j in ((0, 1), (0, 2), (1, 2))), default=0)
        comparison[name] = {
            "legacy_slots": old_count,
            "composer_slots": new_count,
            "slot_gain": new_count - old_count,
            "legacy_min_pair_diff": old_diff,
            "composer_min_pair_diff": new_diff,
            "legacy_three_looks": old.get("checks", {}).get("three_looks"),
            "composer_three_looks": new.get("checks", {}).get("three_looks"),
        }
        if new_count < old_count:
            results.append({"case": "comparison_" + name, "pass": False,
                            "reasons": ["composer has fewer slots than legacy"]})
    clean = [r for r in results if r["pass"]]
    lines = ["# P4-3 Outfit Composer — regression tests", "",
             "- Command: `python3 11-验收/P4-COMPOSER/test_outfit.py`",
             "- Real KB IDs/SRC only; no card/script changes.", ""]
    lines.append("| Case | Result | Reasons |")
    lines.append("| --- | --- | --- |")
    for result in results:
        lines.append("| %s | %s | %s |" % (
            result["case"], "PASS" if result["pass"] else "FAIL",
            "; ".join(result["reasons"]) or "-"))
    lines.append("")
    lines.append("- PASS: %d / %d" % (len(clean), len(results)))
    lines.append("- FAIL: %d / %d" % (len(results) - len(clean), len(results)))
    (HERE / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / "comparison.json").write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
    print("\n".join(lines))
    bad = [result for result in results if not result["pass"]]
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
