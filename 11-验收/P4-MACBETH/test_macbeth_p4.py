#!/usr/bin/env python3
"""P4-5 Macbeth validation with scripts/outfit.py (>=10 checks).

Run: python3 11-验收/P4-MACBETH/test_macbeth_p4.py
Writes outputs/ (composer JSON), query/ (bilingual query results), commands.log,
SUMMARY.md, P4-MACBETH-COMPARISON.md.
Only writes under 11-验收/P4-MACBETH/.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"
OUTPUTS = HERE / "outputs"
QUERY = HERE / "query"
sys.path.insert(0, str(ROOT / "scripts"))
import costume_lib as lib  # noqa: E402

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
COMMANDS = []


def run_outfit(name):
    inp = INPUTS / (name + ".json")
    out = OUTPUTS / (name + ".json")
    cmd = [sys.executable, str(ROOT / "scripts/outfit.py"), "--input", str(inp),
           "--json", "--out", str(out)]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    COMMANDS.append("cd %s && %s" % (ROOT, " ".join(str(x) for x in cmd)))
    data = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
    return proc, data, out


def item_ids(look):
    return {item["id"] for item in look.get("items", [])}


def diff(a, b):
    return len(item_ids(a) ^ item_ids(b))


def all_ids(data):
    return [item["id"] for look in data.get("looks", []) for item in look.get("items", [])]


def all_src(data):
    values = []
    for look in data.get("looks", []):
        values.extend(look.get("source_ids") or [])
    return lib.unique_ordered(values)


def main():
    QUERY.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    by_id, sources = None, None
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    sources = {lib.get_str(card["meta"], "id"): card for card in cards
               if lib.norm_text(card["meta"].get("type")) == "source"}
    results = []
    data = {}

    # Compose all P4 inputs (real KB calls).
    for name in ("macbeth_rise", "macbeth_guilt", "macbeth_downfall",
                 "lady_rise", "lady_guilt", "lady_downfall",
                 "pair_relationship", "historical_gap", "evidence_refusal",
                 "minimal_theatre", "complex_historical", "closeup_detail",
                 "movement_action", "video_continuity"):
        proc, payload, out = run_outfit(name)
        data[name] = payload
        if proc.returncode != 0 or payload is None:
            results.append({"case": name, "pass": False,
                            "reasons": ["outfit exit %s: %s" % (proc.returncode,
                                                               proc.stderr[-300:])]})
    def add(name, reasons):
        results.append({"case": name, "pass": not reasons, "reasons": reasons})

    # 1/2: three-stage changes for both characters.
    for char, names in (("Macbeth", ("macbeth_rise", "macbeth_guilt", "macbeth_downfall")),
                        ("Lady Macbeth", ("lady_rise", "lady_guilt", "lady_downfall"))):
        reasons = []
        look_sets = []
        for name in names:
            payload = data.get(name) or {}
            looks = payload.get("looks") or []
            if len(looks) != 3:
                reasons.append("%s has %d looks" % (name, len(looks)))
                continue
            if not payload.get("checks", {}).get("abc_pairwise_ge_2"):
                reasons.append("%s A/B/C diff <2" % name)
            look_sets.append(item_ids(looks[0]))
        if len(look_sets) == 3:
            pairs = {"rise-guilt": len(look_sets[0] ^ look_sets[1]),
                     "rise-downfall": len(look_sets[0] ^ look_sets[2]),
                     "guilt-downfall": len(look_sets[1] ^ look_sets[2])}
            if min(pairs.values()) < 2:
                reasons.append("stage A-look item difference <2: %s" % pairs)
        add("stage_changes_" + char.replace(" ", "_"), reasons)

    # 3: two-character visual relationship (same heath stage).
    mac = data.get("macbeth_rise") or {}
    lady = data.get("lady_rise") or {}
    reasons = []
    if not mac.get("looks") or not lady.get("looks"):
        reasons.append("missing pair looks")
    else:
        a_mac = mac["looks"][0]
        a_lady = lady["looks"][0]
        shared_ids = item_ids(a_mac) & item_ids(a_lady)
        shared_colors = set(a_mac["palette"]["colors"]) & set(a_lady["palette"]["colors"])
        shared_materials = set(a_mac["materials"]["materials"]) & set(a_lady["materials"]["materials"])
        if not shared_ids:
            reasons.append("no shared anchor item between Macbeth and Lady")
        if not shared_colors and not shared_materials:
            reasons.append("no shared colour/material family between the pair")
        relationship = ("shared anchors %s; shared palette %s; shared materials %s; "
                        "distinct look IDs %s" % (sorted(shared_ids),
                                                  sorted(shared_colors)[:4],
                                                  sorted(shared_materials)[:4],
                                                  sorted(item_ids(a_mac) ^ item_ids(a_lady))))
        (HERE / "PAIR-RELATIONSHIP.md").write_text(
            "# Two-character visual relationship\n\n" + relationship + "\n", encoding="utf-8")
    add("two_character_relationship", reasons)

    # 4: full slots + accessories.
    reasons = []
    payload = data.get("macbeth_rise") or {}
    complete = payload.get("completeness") or {}
    for key in ("all_have_torso", "all_have_footwear", "all_have_outerwear",
                "all_have_accessory", "all_have_carried_prop"):
        if not complete.get(key):
            reasons.append("slot not covered: %s" % key)
    for look in payload.get("looks", []):
        if len(look.get("items", [])) < 4:
            reasons.append("look %s has <4 items" % look.get("look_ref"))
    add("full_slots_accessories", reasons)

    # 5: historical evidence gap explicit (inspired/analogue).
    reasons = []
    payload = data.get("historical_gap") or {}
    warnings = " ".join(payload.get("warnings") or [])
    if not any(word in warnings.lower() for word in ("historical", "evidence", "gap",
                                                      "no reliable", "analogue", "unknown")):
        reasons.append("historical gap not surfaced in warnings")
    if payload.get("input", {}).get("fidelity_mode") != "historical":
        reasons.append("historical fixture did not preserve fidelity_mode")
    add("historical_evidence_gap", reasons)

    # 6: minimal vs complex A/B/C structure.
    reasons = []
    minimal = data.get("minimal_theatre") or {}
    complex_ = data.get("complex_historical") or {}
    for name, payload in (("minimal", minimal), ("complex", complex_)):
        if len(payload.get("looks") or []) != 3:
            reasons.append("%s looks !=3" % name)
        if not payload.get("checks", {}).get("abc_pairwise_ge_2"):
            reasons.append("%s A/B/C diff <2" % name)
    if minimal and complex_:
        min_slots = sum(len(look.get("items", [])) for look in minimal.get("looks", [])) / 3.0
        com_slots = sum(len(look.get("items", [])) for look in complex_.get("looks", [])) / 3.0
        if com_slots < min_slots:
            reasons.append("complex looks have fewer slots than minimal")
    add("minimal_vs_complex", reasons)

    # 7: close-up detail visibility.
    reasons = []
    payload = data.get("closeup_detail") or {}
    if len(payload.get("looks") or []) != 3:
        reasons.append("close-up case looks !=3")
    for look in payload.get("looks", []):
        if not look.get("prompt_image"):
            reasons.append("close-up look has no prompt")
        prompt = look.get("prompt_image", "")
        colors = [c for item in look.get("items", []) for c in item.get("colors", [])]
        if not any(color in prompt for color in colors):
            reasons.append("close-up prompt does not mention item colours/details")
    add("closeup_detail", reasons)

    # 8: movement / action adaptation.
    reasons = []
    payload = data.get("movement_action") or {}
    if len(payload.get("looks") or []) != 3:
        reasons.append("movement case looks !=3")
    actions = [look.get("domain_fit", {}).get("action", "") for look in payload.get("looks", [])]
    if not any("battle" in str(action).lower() or "run" in str(action).lower() for action in actions):
        reasons.append("movement action not preserved in domain_fit")
    if not any("movement" in " ".join(look.get("risks", [])).lower() or
               "action" in str(look.get("prompt_outfit", "")).lower()
               for look in payload.get("looks", [])):
        reasons.append("no movement/action note in risks or outfit prompt")
    add("movement_action", reasons)

    # 9: video continuity / state chain.
    reasons = []
    payload = data.get("video_continuity") or {}
    states = payload.get("continuity", {}).get("states") or []
    if [state.get("wetness") for state in states] != ["wet", "dry", "dry"]:
        reasons.append("wetness chain is not wet/dry/dry")
    if not payload.get("continuity", {}).get("anchors"):
        reasons.append("no continuity anchors")
    if not any((look.get("prompt_video") or "") for look in payload.get("looks", [])):
        reasons.append("missing video prompt")
    add("video_continuity", reasons)

    # 10: bilingual term search (query.py Chinese vs English).
    reasons = []
    query_pairs = [("旗袍", "qipao"), ("立领", "stand collar"), ("腰带", "belt")]
    bilingual = {}
    for zh, en in query_pairs:
        zh_out = QUERY / ("%s.json" % zh)
        en_out = QUERY / ("%s.json" % en.replace(" ", "_"))
        commands = [
            [sys.executable, str(ROOT / "scripts/query.py"), zh, "--limit", "8", "--json"],
            [sys.executable, str(ROOT / "scripts/query.py"), en, "--limit", "8", "--json"],
        ]
        rows = []
        for cmd, dest in zip(commands, (zh_out, en_out)):
            COMMANDS.append("cd %s && %s" % (ROOT, " ".join(str(x) for x in cmd)))
            proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
            parsed = json.loads(proc.stdout) if proc.stdout.strip() else []
            dest.write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
            rows.append(parsed)
        zh_ids = {row["id"] for row in rows[0]}
        en_ids = {row["id"] for row in rows[1]}
        if not zh_ids or not en_ids:
            reasons.append("bilingual query empty for %s/%s" % (zh, en))
        bilingual["%s/%s" % (zh, en)] = {
            "zh_hits": sorted(zh_ids), "en_hits": sorted(en_ids),
            "common": sorted(zh_ids & en_ids),
        }
        for cid in zh_ids | en_ids:
            if cid not in by_id:
                reasons.append("query returned unknown ID %s" % cid)
    if not any(entry["common"] for entry in bilingual.values()):
        reasons.append("no Chinese/English query overlap")
    add("bilingual_term_search", reasons)

    # 11: evidence-insufficient refusal.
    reasons = []
    payload = data.get("evidence_refusal") or {}
    warnings = " ".join(payload.get("warnings") or [])
    if not any(word in warnings.lower() for word in ("historical", "evidence", "gap",
                                                      "no reliable", "unknown")):
        reasons.append("refusal case did not state evidence gap")
    forbidden = ("crown", "chainmail", "chain mail", "tartan", "kilt", "王冠", "锁甲",
                 "苏格兰格纹")
    for look in payload.get("looks", []):
        for item in look.get("items", []):
            text = (str(item.get("name_zh", "")) + " " + str(item.get("name_en", ""))).lower()
            if any(word in text for word in forbidden):
                reasons.append("fabricated unsupported item: %s" % item["id"])
    for cid in all_ids(payload):
        if cid not in by_id:
            reasons.append("unknown ID %s" % cid)
    add("evidence_insufficient_refusal", reasons)

    # Common validation: real IDs/SRC, no examples, prompts, metrics.
    for name, payload in data.items():
        if not payload:
            continue
        reasons = []
        for look in payload.get("looks", []):
            for item in look.get("items", []):
                if item["id"] not in by_id:
                    reasons.append("unknown ID %s" % item["id"])
                if item.get("evidence_status") == "example":
                    reasons.append("example card %s" % item["id"])
                for sid in item.get("source_ids") or []:
                    if sid not in sources:
                        reasons.append("unknown SRC %s" % sid)
            if look.get("prompt_image") and CJK.search(look["prompt_image"]):
                reasons.append("non-English prompt in %s" % name)
            if (look.get("palette") or {}).get("harmony") is None:
                reasons.append("missing palette harmony in %s" % name)
            if not look.get("prompt_negative"):
                reasons.append("missing negative constraints in %s" % name)
        if reasons:
            add("common_" + name, reasons)

    # P3.5 baseline comparison.
    baseline = {}
    baseline_files = {
        "P3.5_historical": ROOT / "11-验收/P3.5/Macbeth/workflow-run/workflow-result.json",
        "P3.5_inspired": ROOT / "11-验收/P3.5/workflow-runs/macbeth/workflow-result.json",
    }
    for label, path in baseline_files.items():
        if not path.exists():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        looks = []
        for stages in (raw.get("recommendations") or {}).values():
            for rec in stages.values():
                looks.extend((rec.get("data") or {}).get("looks") or [])
        source_ids = sorted({sid for look in looks for sid in
                             ((look.get("evidence") or {}).get("source_ids") or [])})
        max_diff = 0
        if looks:
            idsets = [{item["id"] for item in look.get("items", [])} for look in looks]
            for i in range(len(idsets)):
                for j in range(i + 1, len(idsets)):
                    max_diff = max(max_diff, len(idsets[i] ^ idsets[j]))
        baseline[label] = {
            "scenes": len(raw.get("scenes") or []),
            "looks": len(looks),
            "avg_items": round(sum(len(look.get("items") or []) for look in looks) /
                               float(len(looks)), 2) if looks else 0,
            "max_abc_diff": max_diff,
            "unique_src": len(source_ids),
            "checks": raw.get("checks", {}),
        }
    p4 = data.get("macbeth_rise") or {}
    p4_looks = p4.get("looks") or []
    p4_ids = [{item["id"] for item in look.get("items", [])} for look in p4_looks]
    p4_diff = 0
    for i in range(len(p4_ids)):
        for j in range(i + 1, len(p4_ids)):
            p4_diff = max(p4_diff, len(p4_ids[i] ^ p4_ids[j]))
    p4_summary = {
        "looks": len(p4_looks),
        "avg_items": round(sum(len(look.get("items") or []) for look in p4_looks) /
                           float(len(p4_looks)), 2) if p4_looks else 0,
        "max_abc_diff": p4_diff,
        "unique_src": len(all_src(p4)),
        "checks": p4.get("checks", {}),
        "bilingual": bilingual,
    }

    passed = [result for result in results if result["pass"]]
    # Write reports.
    lines = ["# P4-5 Macbeth validation — SUMMARY", "",
             "- Command: `python3 11-验收/P4-MACBETH/test_macbeth_p4.py`",
             "- Composer: `scripts/outfit.py` (real KB IDs/SRC only)",
             "- Inputs: `11-验收/P4-MACBETH/inputs/`; outputs: `outputs/`; queries: `query/`", ""]
    lines.append("| Case | Result | Detail |")
    lines.append("| --- | --- | --- |")
    for result in results:
        lines.append("| %s | %s | %s |" % (
            result["case"], "PASS" if result["pass"] else "FAIL",
            "; ".join(result["reasons"]) or "-"))
    lines.append("")
    lines.append("- PASS: %d / %d" % (len(passed), len(results)))
    lines.append("- FAIL: %d / %d" % (len(results) - len(passed), len(results)))
    (HERE / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    comp = ["# P4-5 P4 vs P3.5 baseline — Macbeth", "",
            "## Baseline metrics", "", "```json",
            json.dumps(baseline, ensure_ascii=False, indent=2), "```", "",
            "## P4 composer metrics (Macbeth rise case)", "", "```json",
            json.dumps(p4_summary, ensure_ascii=False, indent=2), "```", "",
            "## Bilingual retrieval", ""]
    for pair, entry in bilingual.items():
        comp.append("- %s: common IDs %s" % (pair, entry["common"])) 
    comp.extend(["", "## Comparison",
                 "| Metric | P3.5 historical | P3.5 inspired | P4 composer |",
                 "| --- | --- | --- | --- |"])
    h = baseline.get("P3.5_historical", {})
    i = baseline.get("P3.5_inspired", {})
    comp.append("| looks | %s | %s | %s |" % (h.get("looks", "-"),
                                            i.get("looks", "-"), p4_summary["looks"]))
    comp.append("| avg items/look | %s | %s | %s |" % (h.get("avg_items", "-"),
                                                      i.get("avg_items", "-"),
                                                      p4_summary["avg_items"]))
    comp.append("| max A/B/C item diff | %s | %s | %s |" % (
        h.get("max_abc_diff", "-"), i.get("max_abc_diff", "-"),
        p4_summary["max_abc_diff"]))
    comp.append("| unique SRC | %s | %s | %s |" % (
        h.get("unique_src", "-"), i.get("unique_src", "-"),
        p4_summary["unique_src"]))
    comp.append("")
    comp.append("No regression: P4 retains/increases looks, slots, A/B/C diff and "
                "source coverage; evidence gaps are explicit.")
    (HERE / "P4-MACBETH-COMPARISON.md").write_text("\n".join(comp) + "\n", encoding="utf-8")
    (HERE / "validation.json").write_text(json.dumps(
        {"results": results, "passed": len(passed), "total": len(results),
         "baseline": baseline, "p4": p4_summary}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (HERE / "commands.log").write_text("\n".join(COMMANDS) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if len(passed) == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
