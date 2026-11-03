#!/usr/bin/env python3
"""quality_eval.py - independent relevance / recommendation-quality evaluation.

The acceptance runner checks contract-level criteria.  This script measures the
semantic quality that `exit 0` alone cannot prove:

  * query relevance@5 and precision on 25 fixed probes
  * recommendation: crash rate, example-card-in-A, A/B/C difference,
    warning coverage, evidence coverage, context-ref cleanliness,
    narrative presence, prompt contamination, no-fabrication
  * before/after comparison against the P2.5 audit baseline

Outputs (written next to the acceptance results):
  11-验收/质量评估/current.json
  11-验收/质量评估/baseline.json
  11-验收/质量评估/SUMMARY.md

Usage:
  python3 scripts/quality_eval.py            # evaluate + write
  python3 scripts/quality_eval.py --no-write # print summary only
Exit code 0 when all quality thresholds pass, 1 otherwise.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import costume_lib as lib

ROOT = lib.vault_root()
INPUT_DIR = ROOT / "11-验收/测试输入"
OUT_DIR = ROOT / "11-验收/质量评估"

# P2.5 audit baseline (reports/P2.5-AUDIT.md, 235-card snapshot)
BASELINE = {
    "snapshot_cards": 235,
    "query_relevant_at_5": 3.0,
    "query_precision": 0.862,
    "query_zero_hit_rate": 0.16,
    "recommend_crash_rate": 1.0,
    "example_in_a_rate": 13.0 / 18.0,
    "warning_coverage_rate": 0.0,
    "abc_all_pairwise_distinct_rate": 0.0,
    "b_c_shared_one_item_rate": 10.0 / 16.0,
    "a_c_shared_two_or_more_rate": 13.0 / 16.0,
    "budget_c_cheaper_rate": 0.5,
    "prompt_contamination_rate": 0.11,
    "context_ref_mismatch_rate": 0.7,
}

# 25 query probes: expected IDs and keyword/type relevance rules.
PROBES = [
    {"id": "P01", "query": ["旗袍"], "expected_ids": {"GAR-0031", "LOOK-0009",
                                                      "SRC-0200", "SRC-0201"},
     "keywords": ["旗袍", "qipao", "cheongsam"]},
    {"id": "P02", "query": ["和服"], "expected_ids": {"GAR-0001"},
     "keywords": ["和服", "kimono"]},
    {"id": "P03", "query": ["风衣"], "expected_ids": {"GAR-0045",
                                                      "LOOK-0012", "LOOK-0014"},
     "keywords": ["风衣", "trench", "raincoat"]},
    {"id": "P04", "query": ["蕾丝"], "expected_ids": {"MAT-0002", "STR-0001"},
     "keywords": ["lace", "蕾丝"]},
    {"id": "P05", "query": ["朋克"], "expected_ids": {"LOOK-0006", "STY-0007",
                                                      "SCN-0003"},
     "keywords": ["朋克", "punk"]},
    {"id": "P06", "query": ["徽章"], "expected_ids": {"GAR-0050", "GAR-0051",
                                                      "GAR-0042"},
     "keywords": ["徽章", "badge", "pin", "button"]},
    {"id": "P07", "query": ["1930s 上海"], "expected_ids": {
        "GAR-0031", "LOOK-0008", "LOOK-0009", "LOOK-0012", "LOOK-0015",
        "PRD-0011", "SCN-0004"},
     "keywords": ["1930s", "上海", "shanghai", "qipao", "旗袍"]},
    {"id": "P08", "query": ["立领", "盘扣"], "expected_ids": {
        "STR-0011", "GAR-0031", "GAR-0032", "LOOK-0008", "LOOK-0009",
        "LOOK-0012", "LOOK-0019"},
     "keywords": ["立领", "盘扣", "stand collar", "frog"]},
    {"id": "P09", "query": ["蕾丝", "晚装"], "expected_ids": {"MAT-0002",
                                                              "GAR-0054", "GAR-0031",
                                                              "GAR-0015", "GAR-0007"},
     "keywords": ["lace", "蕾丝", "evening", "晚装", "gown", "cocktail"]},
    {"id": "P10", "query": ["丝绸", "和服"], "expected_ids": {"GAR-0001",
                                                              "GAR-0063", "GAR-0064",
                                                              "LOOK-0020"},
     "keywords": ["和服", "kimono", "silk", "sari", "hanbok", "纱丽", "韩服"]},
    {"id": "P11", "query": ["--phrase", "stand-up collar"],
     "expected_ids": {"GAR-0031", "GAR-0032"}, "keywords": ["stand"]},
    {"id": "P12", "query": ["--phrase", "right side fastening"],
     "expected_ids": {"GAR-0031", "GAR-0032", "STR-0011"},
     "keywords": ["fastening", "qipao"]},
    {"id": "P13", "query": ["--type", "garment", "--category", "footwear"],
     "expected_ids": {"GAR-0022", "GAR-0023", "GAR-0024", "GAR-0035",
                      "GAR-0044", "GAR-0058", "GAR-0060"},
     "keywords": ["鞋", "靴", "shoe", "boot", "footwear"], "type": "garment"},
    {"id": "P14", "query": ["--style-tag", "noir"],
     "expected_ids": {"LOOK-0007", "LOOK-0021", "STY-0005", "SCN-0001"},
     "keywords": ["noir", "黑色"]},
    {"id": "P15", "query": ["--period", "1930s", "--region", "shanghai"],
     "expected_ids": {"GAR-0031", "LOOK-0008", "LOOK-0009", "PRD-0011",
                      "SCN-0004"}, "keywords": ["1930s", "上海"]},
    {"id": "P16", "query": ["--type", "source", "--evidence", "verified"],
     "expected_ids": set(), "keywords": [], "any_type": "source"},
    {"id": "P17", "query": ["--type", "look"], "expected_ids": set(),
     "keywords": [], "any_type": "look"},
    {"id": "P18", "query": ["--category", "accessory"],
     "expected_ids": {"GAR-0021", "GAR-0028", "GAR-0050", "GAR-0051",
                      "GAR-0066", "GAR-0067"},
     "keywords": ["accessory", "配饰", "徽章", "belt", "scarf", "gloves"]},
    {"id": "P19", "query": ["--type", "garment", "--category", "outerwear"],
     "expected_ids": {"GAR-0016", "GAR-0017", "GAR-0018", "GAR-0019",
                      "GAR-0033", "GAR-0037", "GAR-0040", "GAR-0041",
                      "GAR-0045", "GAR-0046", "GAR-0057"},
     "keywords": ["coat", "jacket", "外", "风衣", "雨衣", "parka", "banyan",
                  "suit"], "type": "garment"},
    {"id": "P20", "query": ["spacesuit"], "expected_ids": set(),
     "keywords": ["spacesuit", "太空服", "space"]},
    {"id": "P21", "query": ["Mughal"], "expected_ids": set(),
     "keywords": ["mughal", "莫卧儿"]},
    {"id": "P22", "query": ["mourning jewelry"], "expected_ids": set(),
     "keywords": ["mourning", "丧", "哀悼"]},
    {"id": "P23", "query": ["--match", "any", "旗袍", "太空服"],
     "expected_ids": {"GAR-0031", "LOOK-0009", "LOOK-0011", "LOOK-0019",
                      "SCN-0006"},
     "keywords": ["旗袍", "qipao", "spacesuit"]},
    {"id": "P24", "query": ["--type", "pattern"], "expected_ids": set(),
     "keywords": [], "any_type": "pattern"},
    {"id": "P25", "query": ["雨", "夜", "调查"], "expected_ids": {
        "LOOK-0007", "LOOK-0021", "STY-0005", "SCN-0001", "GAR-0046",
        "GAR-0045"},
     "keywords": ["雨", "night", "rain", "investig", "调查"]},
]


def check_sources_csv():
    """R5 gate: reports/SOURCES.csv must be in sync with 04-来源 cards."""
    proc = subprocess.run([sys.executable, "scripts/build_sources.py", "--check"],
                          cwd=str(ROOT), capture_output=True, text=True)
    tail = [line for line in (proc.stdout or "").strip().splitlines()
            if line.startswith("RESULT:") or line.startswith("[FAIL]")]
    return proc.returncode, " | ".join(tail[-2:]) or (proc.stderr or "").strip()[:300]


def run_query(args):
    proc = subprocess.run([sys.executable, "scripts/query.py"] + args,
                          cwd=str(ROOT), capture_output=True, text=True)
    try:
        return proc.returncode, json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.returncode, []


def is_relevant(row, probe):
    rid = row.get("id", "")
    if probe.get("any_type"):
        return row.get("type") == probe["any_type"]
    if rid in probe.get("expected_ids", set()):
        return True
    hay = (str(row.get("name_zh", "")) + " " + str(row.get("name_en", ""))).lower()
    if any(keyword.lower() in hay for keyword in probe.get("keywords", [])):
        return True
    if probe.get("type") and row.get("type") != probe["type"]:
        return False
    if probe.get("keywords") and any(keyword.lower() in hay for keyword in
                                     probe["keywords"]):
        return True
    return False


def evaluate_queries():
    probes = []
    total_relevant = 0
    total_returned = 0
    zero_hit = 0
    example_in_top2 = 0
    for probe in PROBES:
        args = list(probe["query"]) + ["--limit", "5", "--json"]
        rc, rows = run_query(args)
        rows = rows if isinstance(rows, list) else []
        relevant = [row for row in rows if is_relevant(row, probe)]
        total_relevant += len(relevant)
        total_returned += len(rows)
        if not rows:
            zero_hit += 1
        if any(row.get("id", "").endswith("EXAMPLE-001") for row in rows[:2]):
            example_in_top2 += 1
        probes.append({
            "id": probe["id"],
            "query": probe["query"],
            "exit": rc,
            "hits": len(rows),
            "relevant": len(relevant),
            "ids": [row.get("id") for row in rows],
            "relevant_ids": [row.get("id") for row in relevant],
        })
    n = len(PROBES)
    return {
        "probes": probes,
        "relevant_at_5": round(total_relevant / float(n), 3),
        "precision": round(total_relevant / float(total_returned), 3)
        if total_returned else 0.0,
        "zero_hit_rate": round(zero_hit / float(n), 3),
        "example_in_top2_rate": round(example_in_top2 / float(n), 3),
        "total_relevant": total_relevant,
        "total_returned": total_returned,
    }


def run_recommend(path, meta):
    if meta.get("brief"):
        args = [sys.executable, "scripts/recommend.py", "--brief",
                meta["brief"], "--json"]
    else:
        args = [sys.executable, "scripts/recommend.py", str(path), "--json"]
    proc = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        data = None
    return proc.returncode, data, proc.stderr


def evaluate_recommendations(all_ids, source_ids):
    results = []
    cases = sorted(INPUT_DIR.glob("T*.json"))
    for path in cases:
        raw = json.loads(path.read_text(encoding="utf-8"))
        meta = raw.get("_test", {})
        rc, data, stderr = run_recommend(path, meta)
        metrics = {
            "id": meta.get("id"),
            "exit": rc,
            "json_ok": isinstance(data, dict),
            "crashed": rc not in (0, 3),
            "looks": 0,
            "example_in_a": False,
            "abc_distinct": False,
            "differences": {},
            "warnings": [],
            "expected_warnings": [],
            "warning_coverage": None,
            "evidence_coverage": 0.0,
            "context_clean": True,
            "narrative": False,
            "prompt_contamination": [],
            "no_fabrication": True,
            "budget_mode": None,
            "budget_cheaper_or_explained": False,
            "occupation_category": None,
            "occupation_forbidden": [],
            "rainwear_false_claim": False,
            "arctic_indoor": False,
            "context_mismatch": False,
        }
        if not isinstance(data, dict):
            results.append(metrics)
            continue
        looks = data.get("looks", [])
        metrics["looks"] = len(looks)
        inp = data.get("input", {})
        expected = [c.split(":", 1)[1] for c in meta.get("criteria", [])
                    if isinstance(c, str) and c.startswith("warning_code:")]
        got_codes = [entry.get("code") for entry in data.get("warnings_detail", [])]
        metrics["warnings"] = got_codes
        metrics["expected_warnings"] = expected
        if expected:
            present = sum(1 for code in expected if code in got_codes)
            metrics["warning_coverage"] = present / float(len(expected))
        checks_local = data.get("checks", {})
        metrics["occupation_category"] = checks_local.get("occupation_category")
        metrics["occupation_forbidden"] = checks_local.get(
            "occupation_forbidden_selected") or []
        inp = data.get("input", {})
        weather = lib.norm_text(str(inp.get("weather", "")))
        scene_text = lib.norm_text(" ".join(str(inp.get(key, "")) for key in
                                            ("scene", "location", "weather")))
        indoor = any(marker in scene_text for marker in
                     ("indoor", "interior", "室内", "office", "corridor", "room",
                      "kitchen", "hospital", "ward", "studio", "lobby", "hall",
                      "basement", "apartment", "shelter", "病房", "办公室", "走廊"))
        rain_only = any(word in weather for word in
                        ("rain", "rainy", "storm", "drizzle", "monsoon", "雨"))
        for look in looks:
            outer = next((item for item in look.get("items", [])
                          if item.get("slot") == "outerwear"), None)
            if indoor and outer:
                outer_text = lib.norm_text(str(outer.get("name_en", "")) + " " +
                                           str(outer.get("name_zh", "")) + " " +
                                           " ".join(outer.get("materials", [])))
                if any(word in outer_text for word in
                       ("arctic", "anorak", "parka", "fur", "seal", "极地",
                        "兽皮", "派克")):
                    metrics["arctic_indoor"] = True
            if rain_only and not indoor and outer:
                outer_text = lib.norm_text(str(outer.get("name_en", "")) + " " +
                                           str(outer.get("name_zh", "")) + " " +
                                           " ".join(outer.get("tags", [])))
                if not any(word in outer_text for word in
                           ("rain", "trench", "raincoat", "waterproof", "雨衣",
                            "风衣")):
                    metrics["rainwear_false_claim"] = True
        for entry in data.get("warnings_detail", []):
            if entry.get("code") == "rainwear_gap" and "rainwear cards are missing" in entry.get("message", ""):
                metrics["rainwear_false_claim"] = True
        if looks:
            a = looks[0]
            metrics["example_in_a"] = any(
                item.get("evidence_status") == "example"
                for item in a.get("items", []))
            diffs = a.get("differences") or {}
            metrics["differences"] = diffs
            metrics["abc_distinct"] = bool(diffs) and all(
                (diffs.get(key) or 0) >= 2 for key in ("a_b", "a_c", "b_c"))
            items = [item for look in looks for item in look.get("items", [])]
            covered = [item for item in items if item.get("source_ids")]
            metrics["evidence_coverage"] = (
                len(covered) / float(len(items)) if items else 0.0)
            metrics["narrative"] = all(bool(look.get("narrative_meaning"))
                                       for look in looks)
            refs = data.get("context_refs", [])
            metrics["context_clean"] = all(
                ref.get("period_tier") != "none" and
                not (ref.get("type") == "period_region" and
                     ref.get("region_tier") in ("none", None))
                for ref in refs)
            weather = lib.norm_text(str(inp.get("weather", "")))
            scene_text = lib.norm_text(" ".join(str(inp.get(key, "")) for key in
                                                ("scene", "location", "weather")))
            indoor = any(marker in scene_text for marker in
                         ("indoor", "interior", "室内", "office", "corridor",
                          "room", "kitchen", "hospital", "ward", "studio", "lobby",
                          "hall", "basement", "apartment", "shelter", "病房",
                          "办公室", "走廊"))
            snow_ok = (not indoor) and any(word in weather for word in
                                           ("snow", "snowy", "雪"))
            for look in looks:
                selected = lib.norm_text(" ".join(
                    str(item.get("name_en", "")) + " " + str(item.get("name_zh", ""))
                    for item in look.get("items", [])))
                for field in ("prompt_image", "prompt_video"):
                    prompt = str(look.get(field, ""))
                    if "worn in snow" in prompt and not snow_ok:
                        metrics["prompt_contamination"].append(
                            "%s:%s:worn in snow" % (look.get("look_ref"), field))
                    if indoor and ("arctic anorak" in prompt.lower() or
                                   "parka" in prompt.lower()):
                        metrics["prompt_contamination"].append(
                            "%s:%s:arctic parka in indoor scene" % (
                                look.get("look_ref"), field))
                    if "white t-shirt and leather jacket" in prompt and not (
                            "t-shirt" in selected or "leather jacket" in selected):
                        metrics["prompt_contamination"].append(
                            "%s:%s:non-selected garment" % (look.get("look_ref"), field))
            mode = a.get("budget_mode")
            metrics["budget_mode"] = mode
            a_cost = a.get("cost_total") or 0
            c_cost = (looks[2].get("cost_total") or 0) if len(looks) > 2 else None
            metrics["budget_c_cheaper_or_explained"] = (
                mode == "equivalent_cost" and bool(a.get("budget_explanation"))
            ) or (c_cost is not None and a_cost > 0 and c_cost <= a_cost * 0.9 + 1e-9)
            ids = [item.get("id") for item in items]
            metrics["no_fabrication"] = all(
                cid in all_ids for cid in ids) and not data.get("missing_urls")
            for item in items:
                for sid in item.get("source_ids", []):
                    if sid not in source_ids:
                        metrics["no_fabrication"] = False
            if "continuity" in data:
                scenes = data["continuity"].get("scenes", [])
                top_video = a.get("prompt_video", "")
                for scene in scenes:
                    action = scene.get("action") or ""
                    weather = scene.get("weather") or ""
                    if action and action in top_video:
                        metrics["prompt_contamination"].append(
                            "%s:top prompt contains scene action" % scene.get("scene_id"))
                    if weather and weather in top_video:
                        metrics["prompt_contamination"].append(
                            "%s:top prompt contains scene weather" % scene.get("scene_id"))
        results.append(metrics)
    return results


def rate(values):
    values = [value for value in values if value is not None]
    return round(sum(values) / float(len(values)), 3) if values else None


def build_summary(query_metrics, rec_metrics, thresholds, csv_check=None):
    n = len(rec_metrics)
    crash_rate = sum(1 for m in rec_metrics if m["crashed"]) / float(n) if n else 0
    example_a_rate = sum(1 for m in rec_metrics if m["example_in_a"]) / float(n) if n else 0
    abc_rate = sum(1 for m in rec_metrics if m["abc_distinct"]) / float(n) if n else 0
    warning_values = [m["warning_coverage"] for m in rec_metrics
                      if m["warning_coverage"] is not None]
    warning_coverage = rate(warning_values)
    evidence = rate([m["evidence_coverage"] for m in rec_metrics])
    context_clean_rate = rate([1.0 if m["context_clean"] else 0.0 for m in rec_metrics])
    narrative_rate = rate([1.0 if m["narrative"] else 0.0 for m in rec_metrics])
    contamination = sum(len(m["prompt_contamination"]) for m in rec_metrics)
    fabrication = sum(1 for m in rec_metrics if not m["no_fabrication"])
    budget = rate([1.0 if m["budget_c_cheaper_or_explained"] else 0.0
                   for m in rec_metrics])
    occ_forbidden = sum(len(m["occupation_forbidden"]) for m in rec_metrics)
    occupation_mismatch_cases = sum(1 for m in rec_metrics
                                    if m["occupation_forbidden"])
    rainwear_false = sum(1 for m in rec_metrics if m["rainwear_false_claim"])
    arctic_indoor = sum(1 for m in rec_metrics if m["arctic_indoor"])
    context_mismatch = sum(1 for m in rec_metrics if not m["context_clean"])
    csv_ok, csv_detail = csv_check if csv_check else (0, "not checked")
    current = {
        "snapshot_cards": None,
        "query_relevant_at_5": query_metrics["relevant_at_5"],
        "query_precision": query_metrics["precision"],
        "query_zero_hit_rate": query_metrics["zero_hit_rate"],
        "recommend_crash_rate": crash_rate,
        "example_in_a_rate": example_a_rate,
        "warning_coverage_rate": warning_coverage,
        "abc_all_pairwise_distinct_rate": abc_rate,
        "budget_c_cheaper_or_explained_rate": budget,
        "evidence_coverage": evidence,
        "context_ref_clean_rate": context_clean_rate,
        "narrative_presence_rate": narrative_rate,
        "prompt_contamination_count": contamination,
        "fabrication_violations": fabrication,
        "occupation_mismatch_cases": occupation_mismatch_cases,
        "occupation_forbidden_items": occ_forbidden,
        "rainwear_false_claim_cases": rainwear_false,
        "arctic_indoor_cases": arctic_indoor,
        "context_mismatch_cases": context_mismatch,
        "sources_csv_sync": 1.0 if csv_ok == 0 else 0.0,
    }
    comparisons = [
        ("query relevant@5 (0-5)", BASELINE["query_relevant_at_5"],
         current["query_relevant_at_5"]),
        ("query precision", BASELINE["query_precision"],
         current["query_precision"]),
        ("query zero-hit rate", BASELINE["query_zero_hit_rate"],
         current["query_zero_hit_rate"]),
        ("recommend crash rate", BASELINE["recommend_crash_rate"],
         current["recommend_crash_rate"]),
        ("example card in A rate", BASELINE["example_in_a_rate"],
         current["example_in_a_rate"]),
        ("warning coverage", BASELINE["warning_coverage_rate"],
         current["warning_coverage_rate"]),
        ("A/B/C all-pairwise distinct rate", BASELINE["abc_all_pairwise_distinct_rate"],
         current["abc_all_pairwise_distinct_rate"]),
        ("prompt contamination count", BASELINE["prompt_contamination_rate"],
         current["prompt_contamination_count"]),
        ("occupation mismatch cases (P3-QA D2)", 9, occupation_mismatch_cases),
        ("false rainwear-missing claims (P3-QA D4)", 2, rainwear_false),
        ("arctic outerwear indoors (P3-QA M6)", 2, arctic_indoor),
        ("context mismatch cases (P3-QA M4)", 1, context_mismatch),
        ("SOURCES.csv sync gate (R5)", "not gated", "PASS" if csv_ok == 0 else "FAIL"),
    ]
    lines = []
    lines.append("# P3 质量评估 SUMMARY")
    lines.append("")
    lines.append("- 评估脚本：`scripts/quality_eval.py`（独立子进程）")
    lines.append("- 输入：25 个 query 探针 + %d 个推荐用例（11-验收/测试输入）" % n)
    lines.append("")
    lines.append("## 指标前后对比（P2.5 审计 → 当前）")
    lines.append("")
    lines.append("| 指标 | P2.5 基线 | 当前 |")
    lines.append("| --- | --- | --- |")
    for label, before, after in comparisons:
        lines.append("| %s | %s | %s |" % (label, before, after))
    lines.append("")
    lines.append("## 当前推荐质量")
    lines.append("")
    lines.append("- SOURCES.csv 同步（R5 质量门）：%s（`build_sources.py --check` exit=%s；%s）" % (
        "PASS" if csv_ok == 0 else "FAIL", csv_ok, csv_detail))
    lines.append("- 用例数：%d；崩溃：%d；证据覆盖率：%s；警告覆盖率：%s；A/B/C 全差异率：%s；narrative 覆盖率：%s；context 引用清洁率：%s；预算替代满足率：%s；prompt 串文数：%d；编造违规：%d；职业错配：%d；虚假 rainwear 声明：%d；室内极地派克：%d；context 错配：%d" % (
        n, sum(1 for m in rec_metrics if m["crashed"]), evidence,
        warning_coverage, abc_rate, narrative_rate, context_clean_rate, budget,
        contamination, fabrication, occupation_mismatch_cases, rainwear_false,
        arctic_indoor, context_mismatch))
    lines.append("")
    lines.append("## 逐用例（推荐）")
    lines.append("")
    lines.append("| 用例 | exit | looks | example in A | A/B/C diffs | budget | warnings |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for m in rec_metrics:
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            m["id"], m["exit"], m["looks"], m["example_in_a"],
            m["differences"], m["budget_mode"],
            ",".join(m["warnings"][:6])))
    lines.append("")
    lines.append("## 阈值与结论")
    lines.append("")
    passed = True
    for key, threshold in thresholds.items():
        value = current.get(key)
        ok = (value <= threshold) if key in ("query_zero_hit_rate",
                                             "recommend_crash_rate",
                                             "example_in_a_rate",
                                             "prompt_contamination_count",
                                             "fabrication_violations") else (
            value >= threshold)
        passed = passed and ok
        lines.append("- %s：当前=%s，阈值=%s → %s" % (
            key, value, threshold, "PASS" if ok else "FAIL"))
    lines.append("")
    lines.append("**OVERALL: %s**" % ("PASS" if passed else "FAIL"))
    return current, "\n".join(lines), passed


def main(argv=None):
    parser = argparse.ArgumentParser(description="Independent quality evaluation.")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    all_ids = set()
    source_ids = set()
    cards, _errors = lib.load_cards()
    for card in cards:
        cid = lib.get_str(card["meta"], "id")
        all_ids.add(cid)
        if lib.norm_text(card["meta"].get("type")) == "source":
            source_ids.add(cid)
    query_metrics = evaluate_queries()
    rec_metrics = evaluate_recommendations(all_ids, source_ids)
    thresholds = {
        "query_relevant_at_5": 4.0,
        "query_precision": 0.8,
        "query_zero_hit_rate": 0.2,
        "recommend_crash_rate": 0.0,
        "example_in_a_rate": 0.0,
        "warning_coverage_rate": 0.8,
        "abc_all_pairwise_distinct_rate": 0.8,
        "evidence_coverage": 0.65,
        "context_ref_clean_rate": 1.0,
        "narrative_presence_rate": 1.0,
        "prompt_contamination_count": 0,
        "fabrication_violations": 0,
        "occupation_mismatch_cases": 0,
        "rainwear_false_claim_cases": 0,
        "arctic_indoor_cases": 0,
        "context_mismatch_cases": 0,
        "sources_csv_sync": 1.0,
    }
    csv_check = check_sources_csv()
    current, summary, passed = build_summary(query_metrics, rec_metrics,
                                             thresholds, csv_check=csv_check)
    current["snapshot_cards"] = len(cards)
    baseline = dict(BASELINE)
    baseline["snapshot_cards"] = 235
    if not args.no_write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "current.json").write_text(
            json.dumps({"summary": current, "queries": query_metrics,
                        "recommendations": rec_metrics}, ensure_ascii=False,
                       indent=2) + "\n", encoding="utf-8")
        (OUT_DIR / "baseline.json").write_text(
            json.dumps(baseline, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")
        (OUT_DIR / "SUMMARY.md").write_text(summary + "\n", encoding="utf-8")
        print("wrote", OUT_DIR / "SUMMARY.md")
    else:
        print(summary)
    print("QUALITY:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
