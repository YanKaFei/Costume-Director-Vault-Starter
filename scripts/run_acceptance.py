#!/usr/bin/env python3
"""run_acceptance.py - real end-to-end acceptance tests for the Costume Director P2 loop.

For every 11-验收/测试输入/T*.json file:
  1. run scripts/recommend.py <input> --json          (real subprocess, exit code recorded)
  2. run scripts/query.py <test query args> --json    (real subprocess, exit code recorded)
  3. evaluate the declared acceptance criteria against the actual output
  4. write 11-验收/测试结果/<test>.md with input, commands, retrieved IDs,
     A/B/C looks, scores, prompts, risks, PASS/FAIL and notes
  5. write 11-验收/测试结果/raw/<test>.json with the raw script output
Finally write 11-验收/测试结果/SUMMARY.md with verdict counts, failures and command
exit codes.

This runner never invents results: if a script fails or the knowledge base lacks
a slot, the corresponding criterion is FAIL/PARTIAL and the reason is recorded.

Usage:
    python3 scripts/run_acceptance.py                 # all tests
    python3 scripts/run_acceptance.py --only T03,T17  # subset
    python3 scripts/run_acceptance.py --no-write      # evaluate only (no result files)

Exit code: 0 when every test passes, 1 when at least one criterion fails.
"""

import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

import costume_lib as lib
import recommend as rec

RESULTS_DIR = "11-验收/测试结果"
INPUTS_DIR = "11-验收/测试输入"

HEEL_WORDS = ("heel", "stiletto", "高跟", "pump")
OPEN_WORDS = ("sandal", "flip", "slipper", "凉鞋", "拖鞋")


def run_command(args, cwd, timeout=240):
    started = time.time()
    try:
        proc = subprocess.run(args, cwd=str(cwd), capture_output=True,
                              text=True, timeout=timeout)
        return {
            "cmd": " ".join(args),
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration": round(time.time() - started, 2),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": " ".join(args),
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": "TIMEOUT after %ss" % timeout,
            "duration": round(time.time() - started, 2),
        }


def safe_json(text):
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def load_test_inputs(root):
    base = root / INPUTS_DIR
    items = []
    for path in sorted(base.glob("T*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print("ERROR: bad test input %s: %s" % (path, exc), file=sys.stderr)
            continue
        items.append({"path": path, "raw": raw, "meta": raw.get("_test", {})})
    return items


# ---------------------------------------------------------------------------
# criterion evaluation
# ---------------------------------------------------------------------------
def looks_of(data):
    return (data or {}).get("looks", []) or []


def items_for_slot(look, slot):
    return [item for item in look.get("items", []) if item.get("slot") == slot]


def all_items(data):
    out = []
    for look in looks_of(data):
        out.extend(look.get("items", []))
    return out


def item_card(card_index, item_id):
    return card_index.get(item_id)


def is_heel(item, card_index):
    card = item_card(card_index, item.get("id"))
    text = ""
    if card:
        text = (lib.norm_text(lib.get_str(card["meta"], "subcategory")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_en")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_zh")))
    else:
        text = lib.norm_text(item.get("name_en", "") + " " + item.get("name_zh", ""))
    return any(word in text for word in HEEL_WORDS)


def is_open_footwear(item, card_index):
    card = item_card(card_index, item.get("id"))
    if card:
        text = (lib.norm_text(lib.get_str(card["meta"], "subcategory")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_en")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_zh")))
    else:
        text = lib.norm_text(item.get("name_en", "") + " " + item.get("name_zh", ""))
    return any(word in text for word in OPEN_WORDS)


def criterion(name, record, card_index, source_ids):
    """Return (status, detail) where status is PASS/FAIL/PARTIAL/NOT_TESTED."""
    data = record["data"]
    rc = record["recommend"]["returncode"]
    meta = record["meta"]
    looks = looks_of(data)
    checks = (data or {}).get("checks", {})
    if rc != 0 or data is None:
        return "FAIL", "recommend.py exit=%s, no usable JSON output (stderr: %s)" % (
            rc, record["recommend"]["stderr"].strip()[:300] or "none")

    if name == "three_looks":
        ok = len(looks) == 3 and checks.get("three_looks") and checks.get("looks_distinct")
        return ("PASS" if ok else "FAIL",
                "looks=%d, distinct=%s, checks=%s" % (
                    len(looks), checks.get("looks_distinct"),
                    {k: checks.get(k) for k in ("three_looks", "looks_distinct")}))
    if name == "ids_exist":
        return ("PASS" if checks.get("ids_all_exist") else "FAIL",
                "all garment ids resolvable: %s" % checks.get("ids_all_exist"))
    if name == "fidelity_matches":
        expected = meta.get("expected_mode")
        got = (data or {}).get("fidelity_mode")
        ok = got == expected
        return ("PASS" if ok else "FAIL", "expected=%s got=%s" % (expected, got))
    if name == "historical_verified":
        evidence = [look.get("evidence", {}) for look in looks]
        verified_counts = [sum(1 for status in (ev.get("item_evidence") or {}).values()
                               if status == "verified") for ev in evidence]
        all_have = all(count > 0 for count in verified_counts) and bool(verified_counts)
        missing_urls = (data or {}).get("missing_urls", [])
        has_sources = any(ev.get("source_ids") for ev in evidence)
        ok = checks.get("history_evidence") and all_have and not missing_urls and has_sources
        return ("PASS" if ok else "FAIL",
                "history_evidence=%s verified/item=%s missing_source_ids=%s has_source_ids=%s" % (
                    checks.get("history_evidence"), verified_counts,
                    missing_urls, has_sources))
    if name == "query_hits":
        if record.get("query") is None:
            return "FAIL", "no query.py step configured for this scenario"
        hits = record.get("query_data")
        count = len(hits) if isinstance(hits, list) else 0
        ids = [row.get("id") for row in (hits or []) if isinstance(row, dict)]
        ok = record["query"]["returncode"] == 0 and count >= 1
        return ("PASS" if ok else "FAIL",
                "query.py exit=%s, hits=%d, ids=%s" % (
                    record["query"]["returncode"], count,
                    ", ".join(ids[:6]) + ("…" if len(ids) > 6 else "") if ids else "(none)"))
    if name == "structured_result":
        ids_ok = checks.get("ids_all_exist")
        warn_ok = bool((data or {}).get("warnings_detail")) or bool((data or {}).get("warnings"))
        ok = (rc == 0 and 1 <= len(looks) <= 3 and ids_ok and warn_ok
              and all(look.get("items") for look in looks))
        return ("PASS" if ok else "FAIL",
                "exit=%s looks=%d ids_exist=%s warnings=%s" % (
                    rc, len(looks), ids_ok, warn_ok))
    if name == "no_crash":
        ok = rc == 0
        return ("PASS" if ok else "FAIL",
                "recommend.py exit=%s (must be 0, no KeyError/uncaught exception)" % rc)
    if name == "warnings_present":
        codes = [entry.get("code") for entry in (data or {}).get("warnings_detail", [])]
        ok = bool(codes) or bool((data or {}).get("warnings"))
        return ("PASS" if ok else "FAIL",
                "wytyczne count=%d codes=%s" % (len(codes), codes[:12]))
    if name.startswith("warning_code:"):
        wanted = name.split(":", 1)[1]
        codes = [entry.get("code") for entry in (data or {}).get("warnings_detail", [])]
        ok = wanted in codes
        return ("PASS" if ok else "FAIL",
                "expected warning code %r; got %s" % (wanted, codes))
    if name.startswith("conflict_code:"):
        wanted = name.split(":", 1)[1]
        codes = [entry.get("code") for entry in (data or {}).get("conflicts", [])]
        ok = wanted in codes
        return ("PASS" if ok else "FAIL",
                "expected conflict %r; got %s" % (wanted, codes))
    if name == "conflicts_present":
        conflicts = (data or {}).get("conflicts", [])
        return ("PASS" if conflicts else "FAIL",
                "conflicts=%s" % [entry.get("code") for entry in conflicts])
    if name == "no_example_in_a":
        if not looks:
            return "FAIL", "no looks"
        a = looks[0]
        example_ids = [item["id"] for item in a.get("items", [])
                       if item.get("evidence_status") == "example"]
        ok = not example_ids and not a.get("contains_example")
        return ("PASS" if ok else "FAIL",
                "Look A example ids=%s contains_example=%s" % (
                    example_ids, a.get("contains_example")))
    if name == "abc_distinct":
        if len(looks) < 3:
            return "FAIL", "fewer than 3 looks"
        diffs = looks[0].get("differences") or {}
        ok = (checks.get("abc_distinct") and
              all((diffs.get(key) or 0) >= 2 for key in ("a_b", "a_c", "b_c")))
        return ("PASS" if ok else "FAIL",
                "checks.abc_distinct=%s differences=%s" % (
                    checks.get("abc_distinct"), diffs))
    if name == "narrative_present":
        missing = [look.get("look_ref") for look in looks
                   if not look.get("narrative_meaning")]
        return ("PASS" if looks and not missing else "FAIL",
                "missing narrative for %s" % (missing or "none"))
    if name == "context_refs_clean":
        refs = (data or {}).get("context_refs", [])
        bad = [ref for ref in refs
               if ref.get("period_tier") == "none"
               or (ref.get("type") == "period_region"
                   and ref.get("region_tier") in ("none", None))]
        example_refs = [ref["id"] for ref in refs if ref.get("id", "").endswith("EXAMPLE-001")]
        ok = not bad and not example_refs
        return ("PASS" if ok else "FAIL",
                "refs=%d bad=%s example_refs=%s" % (
                    len(refs), [r.get("id") for r in bad], example_refs))
    if name == "period_coverage":
        tiers = {}
        for look in looks:
            for slot, tier in (look.get("period_tiers") or {}).items():
                tiers[slot] = tier
        wanted = set(tiers.values()) & {"exact", "era", "approximate", "fictional"}
        ok = bool(wanted) and rc == 0
        return ("PASS" if ok else "FAIL",
                "period evidence tiers=%s" % tiers)
    if name == "region_evidence_new":
        region = (data or {}).get("input", {}).get("region", "")
        want = rec.labels([region])
        compatible = []
        for item in all_items(data):
            card = item_card(card_index, item.get("id"))
            if not card:
                continue
            region_labels = rec.card_region_labels(card)
            if region_labels and want and rec.region_compatible_labels(want, region_labels):
                compatible.append(item["id"])
        return ("PASS" if compatible else "FAIL",
                "region-compatible evidence for %r: %s" % (region, compatible))
    if name == "evidence_coverage":
        items = all_items(data)
        covered = [item["id"] for item in items if item.get("source_ids")]
        look_evidence = [bool((look.get("evidence") or {}).get("source_ids"))
                         for look in looks]
        ok_items = bool(items) and len(covered) >= max(1, int(len(items) * 0.5))
        ok_looks = bool(look_evidence) and all(look_evidence)
        ok = ok_items or ok_looks
        return ("PASS" if ok else "FAIL",
                "items with source_ids=%d/%d; looks with evidence=%d/%d" % (
                    len(covered), len(items), sum(look_evidence), len(look_evidence)))
    if name == "brief_parsed":
        parsed = (data or {}).get("brief_parse") or {}
        known = [key for key in ("period", "region", "occupation")
                 if parsed.get(key) not in (None, "unknown", "")]
        ok = bool(parsed) and bool(known) and parsed.get("brief")
        return ("PASS" if ok else "FAIL",
                "brief_parse fields=%s acknowledged_unknown=%s" % (
                    known, parsed.get("unknown_fields")))
    if name == "no_prompt_contamination":
        problems = []
        inp = (data or {}).get("input", {})
        weather = rec.lib.norm_text(str(inp.get("weather", "")) + " " +
                                    str(inp.get("season", "")))
        scene_text = rec.lib.norm_text(" ".join(str(inp.get(key, "")) for key in
                                                ("scene", "location", "weather")))
        indoor = any(marker in scene_text for marker in
                     ("indoor", "interior", "室内", "office", "corridor", "room",
                      "kitchen", "hospital", "ward", "studio", "lobby", "hall",
                      "basement", "apartment", "shelter", "病房", "办公室", "走廊"))
        snow_ok = (not indoor) and any(word in weather for word in
                                       ("snow", "snowy", "雪"))
        for look in looks:
            selected_names = " ".join(
                rec.lib.norm_text(item.get("name_en", "") + " " + item.get("name_zh", ""))
                for item in look.get("items", []))
            for field in ("prompt_image", "prompt_video"):
                prompt = look.get(field, "")
                if "worn in snow" in prompt and not snow_ok:
                    problems.append("%s %s: 'worn in snow' in non-snow/indoor scene" % (
                        look.get("look_ref"), field))
                if indoor and ("arctic anorak" in prompt.lower() or
                               "parka" in prompt.lower()):
                    problems.append("%s %s: arctic parka language in indoor scene" % (
                        look.get("look_ref"), field))
                if "white t-shirt and leather jacket" in prompt and not (
                        "t-shirt" in selected_names or "leather jacket" in selected_names):
                    problems.append("%s %s: non-selected garment phrase" % (
                        look.get("look_ref"), field))
        return ("PASS" if not problems else "FAIL",
                "; ".join(problems) or "no cross-scene/card-text contamination")
    if name == "per_scene_prompts":
        continuity = (data or {}).get("continuity") or {}
        scenes = continuity.get("scenes", [])
        if len(scenes) < 2:
            return "FAIL", "continuity scenes=%d" % len(scenes)
        problems = []
        top_video = looks[0].get("prompt_video", "") if looks else ""
        for scene in scenes:
            action = scene.get("action") or ""
            weather = scene.get("weather") or ""
            if action and action not in scene.get("prompt_video", ""):
                problems.append("%s missing action" % scene.get("scene_id"))
            if "wetness=%s" % scene.get("state", {}).get("wetness") not in scene.get(
                    "prompt_video", ""):
                problems.append("%s missing wetness token" % scene.get("scene_id"))
            if "continuity lock" not in scene.get("prompt_video", "").lower():
                problems.append("%s missing continuity lock" % scene.get("scene_id"))
            if action and action in top_video:
                problems.append("top-level prompt contains scene action %r" % action)
            if weather and weather in top_video:
                problems.append("top-level prompt contains scene weather %r" % weather)
        ok = not problems and continuity.get("prompt_mode") == "per_scene"
        return ("PASS" if ok else "FAIL",
                "; ".join(problems) or "per-scene prompts isolated (scenes=%d)" % len(scenes))
    if name == "occupation_match":
        checks_local = (data or {}).get("checks", {})
        forbidden = checks_local.get("occupation_forbidden_selected") or []
        ok = bool(checks_local.get("occupation_match")) and not forbidden
        return ("PASS" if ok else "FAIL",
                "category=%s match=%s forbidden=%s" % (
                    checks_local.get("occupation_category"),
                    checks_local.get("occupation_match"), forbidden))
    if name == "no_occupation_mismatch":
        checks_local = (data or {}).get("checks", {})
        forbidden = checks_local.get("occupation_forbidden_selected") or []
        return ("PASS" if not forbidden else "FAIL",
                "category=%s forbidden_selected=%s" % (
                    checks_local.get("occupation_category"), forbidden))
    if name == "no_cultural_mispick":
        checks_local = (data or {}).get("checks", {})
        category = checks_local.get("occupation_category")
        strict = {"doctor", "police", "nurse", "chef", "space",
                  "firefighter", "military"}
        if category not in strict:
            return "PASS", "non-occupational brief; cultural pieces may be valid"
        bad = []
        cultural_words = ("韩服", "纱丽", "和服", "旗袍", "汉服", "长衫",
                          "马褂", "云肩", "agbada", "buba", "kaftan", "kimono",
                          "sari", "hanbok", "qipao", "hanfu")
        for look in looks:
            for item in look.get("items", []):
                text = rec.lib.norm_text(str(item.get("name_zh", "")) + " " +
                                         str(item.get("name_en", "")))
                if any(word in text for word in cultural_words):
                    bad.append(item.get("id"))
        return ("PASS" if not bad else "FAIL",
                "cultural pieces in %s occupational look=%s" % (category, bad))
    if name == "occasion_match":
        checks_local = (data or {}).get("checks", {})
        ok = bool(checks_local.get("occasion_match"))
        return ("PASS" if ok else "FAIL",
                "occasion_match=%s" % checks_local.get("occasion_match"))
    if name == "rainwear_selected":
        checks_local = (data or {}).get("checks", {})
        value = checks_local.get("rainwear_selected")
        return ("PASS" if value is True else "FAIL",
                "checks.rainwear_selected=%s" % value)
    if name.startswith("warning_absent:"):
        wanted = name.split(":", 1)[1]
        codes = [entry.get("code") for entry in (data or {}).get("warnings_detail", [])]
        return ("PASS" if wanted not in codes else "FAIL",
                "warning %r present? %s (codes=%s)" % (
                    wanted, wanted in codes, codes))
    if name == "no_arctic_indoor":
        inp = (data or {}).get("input", {})
        scene_text = rec.lib.norm_text(" ".join(str(inp.get(key, "")) for key in
                                                ("scene", "location", "weather")))
        indoor = any(marker in scene_text for marker in
                     ("indoor", "interior", "室内", "office", "corridor", "room",
                      "kitchen", "hospital", "ward", "studio", "lobby", "hall",
                      "basement", "apartment", "shelter", "病房", "办公室", "走廊"))
        if not indoor:
            return "PASS", "not an indoor scene; arctic outdoor wear may be valid"
        bad = []
        for look in looks:
            for slot, item in ((i.get("slot"), i) for i in look.get("items", [])):
                if slot != "outerwear":
                    continue
                text = rec.lib.norm_text(str(item.get("name_en", "")) + " " +
                                         str(item.get("name_zh", "")) + " " +
                                         " ".join(item.get("materials", [])))
                if any(word in text for word in
                       ("arctic", "anorak", "parka", "fur", "seal", "极地",
                        "兽皮", "派克")):
                    bad.append(item.get("id"))
        return ("PASS" if not bad else "FAIL",
                "indoor arctic outerwear=%s" % bad)
    if name.startswith("query_top5_contains:"):
        wanted = name.split(":", 1)[1]
        rows = record.get("query_data") or []
        top = [row.get("id") for row in rows[:5] if isinstance(row, dict)]
        return ("PASS" if wanted in top else "FAIL",
                "query top5=%s (wanted %s)" % (top, wanted))
    if name == "query_no_example_top":
        rows = record.get("query_data") or []
        bad = [row.get("id") for row in rows[:5]
               if isinstance(row, dict) and row.get("evidence_status") == "example"]
        return ("PASS" if not bad else "FAIL",
                "example ids in query top5=%s" % bad)
    if name == "query_no_duplicate_names":
        rows = record.get("query_data") or []
        seen = {}
        dupes = []
        for row in rows[:5]:
            if not isinstance(row, dict):
                continue
            name = rec.lib.norm_text(str(row.get("name_zh", "")) or
                                     str(row.get("name_en", "")))
            if name and name in seen:
                dupes.append(name)
            seen[name] = row.get("id")
        return ("PASS" if not dupes else "FAIL",
                "duplicate names in query top5=%s" % dupes)
    if name == "region_evidence":
        region = (data or {}).get("input", {}).get("region", "")
        want = rec.reco_norm.region_profile(region)
        compatible = []
        for item in all_items(data):
            card = item_card(card_index, item.get("id"))
            if not card:
                continue
            have = rec.card_region_profile(card)
            if have["entities"] and want["entities"]:
                tier = rec.reco_norm.region_tier(want, have)
                if tier in ("exact", "regional", "approximate"):
                    compatible.append(item["id"])
        ok = bool(compatible)
        return ("PASS" if ok else "FAIL",
                "region-compatible evidence for %r: %s (items=%s)" % (
                    region, compatible,
                    [item.get("id") for item in all_items(data)]))
    if name == "rain_outerwear":
        ok = all(items_for_slot(look, "outerwear") for look in looks) and bool(looks)
        return ("PASS" if ok else "FAIL",
                "outerwear per look=%s" % [len(items_for_slot(look, "outerwear")) for look in looks])
    if name == "outerwear":
        ok = bool(looks) and bool(items_for_slot(looks[0], "outerwear"))
        return ("PASS" if ok else "FAIL",
                "A outerwear=%s" % [i["id"] for i in items_for_slot(looks[0], "outerwear")] if looks else [])
    if name in ("dance_safe", "safe_footwear"):
        footwear = [item for look in looks for item in items_for_slot(look, "footwear")]
        bad = [item["id"] for item in footwear
               if (is_heel(item, card_index) if name == "dance_safe"
                   else (is_heel(item, card_index) or is_open_footwear(item, card_index)))]
        ok = bool(footwear) and not bad
        return ("PASS" if ok else "FAIL",
                "footwear=%s unsafe=%s" % ([i["id"] for i in footwear], bad))
    if name == "budget_alternative":
        if len(looks) < 3:
            return "FAIL", "less than 3 looks, cannot compare budget alternative"
        a, c = looks[0], looks[2]
        a_cost = a.get("cost_total") or 0.0
        c_cost = c.get("cost_total") or 0.0
        distinct = (set(i["id"] for i in a.get("items", [])) !=
                    set(i["id"] for i in c.get("items", [])))
        mode = a.get("budget_mode")
        cheaper = a_cost > 0 and c_cost <= a_cost * 0.9 + 1e-9
        equivalent = mode == "equivalent_cost" and bool(a.get("budget_explanation"))
        ok = distinct and (cheaper or equivalent)
        return ("PASS" if ok else "FAIL",
                "A cost=%.3f C cost=%.3f (%.1f%%), mode=%s, cheaper=%s, "
                "equivalent_explained=%s, distinct=%s" % (
                    a_cost, c_cost,
                    ((c_cost - a_cost) / a_cost * 100.0) if a_cost else 0.0,
                    mode, cheaper, equivalent, distinct))
    if name == "wet_state_lock":
        lock = looks[0].get("continuity_lock", "") if looks else ""
        ok = "wetness=wet" in lock
        return ("PASS" if ok else "FAIL", "lock wetness=wet: %s" % ok)
    if name == "fictional_phrasing":
        ok = bool(looks) and all("not a historical reconstruction" in look.get("prompt_image", "")
                                 for look in looks)
        return ("PASS" if ok else "FAIL",
                "all prompts declare fictional: %s" % ok)
    if name == "no_fake_sources":
        missing = (data or {}).get("missing_urls", [])
        sources = (data or {}).get("sources", [])
        bad_urls = [entry for entry in sources
                    if not str(entry.get("url", "")).startswith("http")]
        unresolved = [sid for sid in
                      set(sid for look in looks
                          for sid in (look.get("evidence", {}) or {}).get("source_ids", []))
                      if sid not in source_ids]
        ok = not missing and not bad_urls and not unresolved
        return ("PASS" if ok else "FAIL",
                "missing_source_ids=%s bad_urls=%s unresolved_source_cards=%s" % (
                    missing, bad_urls, unresolved))
    if name == "prompts":
        problems = []
        for idx, look in enumerate(looks):
            image = look.get("prompt_image", "")
            video = look.get("prompt_video", "")
            if len(image) < 150:
                problems.append("look %d image prompt too short" % idx)
            if len(video) < 200:
                problems.append("look %d video prompt too short" % idx)
            if "continuity lock" not in video.lower():
                problems.append("look %d video prompt lacks continuity lock" % idx)
            if "negative constraints" not in video.lower():
                problems.append("look %d video prompt lacks negative constraints" % idx)
        return ("PASS" if not problems else "FAIL", "; ".join(problems) or "all prompts complete")
    if name == "continuity_pass":
        continuity = (data or {}).get("continuity") or {}
        scenes = continuity.get("scenes", [])
        verdict = continuity.get("verdict")
        ids = [tuple(scene.get("item_ids", [])) for scene in scenes]
        same_ids = bool(ids) and len(set(ids)) == 1
        locks = all("continuity lock" in scene.get("prompt_video", "").lower()
                    and "continuity lock" in scene.get("prompt_image", "").lower()
                    for scene in scenes)
        ok = verdict == "PASS" and len(scenes) >= 3 and same_ids and locks
        return ("PASS" if ok else "FAIL",
                "verdict=%s scenes=%d same_item_ids=%s locks_in_every_prompt=%s issues=%s" % (
                    verdict, len(scenes), same_ids, locks,
                    continuity.get("issues", [])))
    return "NOT_TESTED", "unknown criterion %r" % name


# ---------------------------------------------------------------------------
# pair checks
# ---------------------------------------------------------------------------
def pair_check(name, first, second):
    d1, d2 = first["data"] or {}, second["data"] or {}
    looks1, looks2 = looks_of(d1), looks_of(d2)
    if not looks1 or not looks2:
        return "FAIL", "one side produced no looks"

    def ids(look):
        return set(item["id"] for item in look.get("items", []))

    if name == "stylisation_pair":
        if d1.get("fidelity_mode") == "historical":
            hist_data, insp_data = d1, d2
        else:
            hist_data, insp_data = d2, d1
        hist_looks = looks_of(hist_data)
        insp_looks = looks_of(insp_data)
        ok = (hist_data.get("fidelity_mode") == "historical" and
              insp_data.get("fidelity_mode") == "inspired" and
              bool(hist_looks) and bool(insp_looks))
        p1 = bool(hist_looks) and "period-accurate" in hist_looks[0].get("prompt_image", "")
        p2 = bool(insp_looks) and "period-inspired" in insp_looks[0].get("prompt_image", "")
        ok = ok and p1 and p2
        return ("PASS" if ok else "FAIL",
                "modes=%s/%s historical phrase=%s inspired phrase=%s" % (
                    hist_data.get("fidelity_mode"), insp_data.get("fidelity_mode"),
                    p1, p2))
    if name == "lighting_pair":
        a1, a2 = looks1[0], looks2[0]
        overlap = len(ids(a1) & ids(a2))
        p1 = a1.get("prompt_image", "")
        p2 = a2.get("prompt_image", "")
        differs = p1 != p2
        ok = overlap >= 2 and differs
        return ("PASS" if ok else "FAIL",
                "A item overlap=%d, prompts differ=%s" % (overlap, differs))
    if name == "class_pair":
        def id_text(values):
            # Avoid "[[" sequences: Obsidian must never parse them as wikilinks.
            return ", ".join(sorted(values)) if values else "none"

        a_symmetric = ids(looks1[0]) ^ ids(looks2[0])
        total_symmetric = 0
        per_look = []
        for idx in range(min(len(looks1), len(looks2))):
            diff = ids(looks1[idx]) ^ ids(looks2[idx])
            per_look.append(id_text(diff))
            total_symmetric += len(diff)
        # Class differentiation can appear in the alternatives when the anchor
        # look is constrained by the same scene (e.g. same raincoat): accept
        # >=2 item changes anywhere, but report A equality explicitly.
        ok = len(a_symmetric) >= 2 or total_symmetric >= 2
        note = "" if a_symmetric else " (A is the same anchor look; class difference is in B/C)"
        return ("PASS" if ok else "FAIL",
                "A missing/extra ids: %s; per-look differences: %s%s" % (
                    id_text(a_symmetric), " | ".join(per_look), note))
    return "NOT_TESTED", "unknown pair check %r" % name


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def md_json_block(data):
    return "```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```"


def fmt_items(look):
    rows = []
    for item in look.get("items", []):
        rows.append("| %s | `%s` | %s / %s | %s | %s | %s |" % (
            item.get("slot"), item.get("id"), item.get("name_zh", "-"),
            item.get("name_en", "-"), ", ".join(item.get("colors", [])) or "-",
            ", ".join(item.get("materials", [])) or "-",
            item.get("evidence_status", "-")))
    return "\n".join(rows)



# ---------------------------------------------------------------------------
# known / assumptions / unknown (R1.1 KQ-06: explicit separation)
# ---------------------------------------------------------------------------
INPUT_FIELD_LABELS = [
    ("character.name", "角色名"),
    ("character.gender_presentation", "性别呈现"),
    ("character.age", "年龄"),
    ("character.occupation", "职业"),
    ("character.economic_status", "经济状态"),
    ("character.arc", "人物弧线"),
    ("period", "年代"),
    ("region", "地域"),
    ("season", "季节"),
    ("scene.scene_id", "场次"),
    ("scene.time", "时间"),
    ("scene.weather", "天气"),
    ("scene.action", "动作"),
    ("scene.location", "地点"),
    ("art_direction", "美术方向"),
    ("lighting", "摄影光线"),
    ("camera", "景别"),
    ("budget", "预算"),
    ("fidelity_mode", "严格度模式"),
    ("tool", "生成工具"),
    ("state.wetness", "湿度状态"),
    ("state.damage", "破损状态"),
    ("state.dirt", "污渍状态"),
]
UNKNOWN_VALUES = {"", "unknown", "none", "null", "n/a", "-", "未指定"}


def flatten_mapping(value, prefix=""):
    flat = {}
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).startswith("_"):
                continue
            flat.update(flatten_mapping(child, prefix + str(key) + "."))
    elif isinstance(value, list):
        flat[prefix[:-1]] = value
    else:
        flat[prefix[:-1]] = value
    return flat


def is_unknown(value):
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in UNKNOWN_VALUES
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def render_known_assumptions_unknown(lines, record):
    raw = record["raw"]
    data = record.get("data") or {}
    flat = flatten_mapping(raw)
    labels = dict(INPUT_FIELD_LABELS)

    lines.append("## 已知输入")
    lines.append("")
    lines.append("以下字段来自测试输入文件，是**已知条件**（不是模型推断）：")
    lines.append("")
    known_rows = 0
    for key, label in INPUT_FIELD_LABELS:
        value = flat.get(key)
        if is_unknown(value):
            continue
        known_rows += 1
        lines.append("- %s（`%s`）：%s" % (label, key, json.dumps(value, ensure_ascii=False)))
    if not known_rows:
        lines.append("- （输入中没有可用的已知字段）")
    lines.append("")

    lines.append("## 假设")
    lines.append("")
    assumptions = []
    if raw.get("character", {}).get("arc"):
        assumptions.append("人物弧线（%s）对服装的映射属于导演/设计解释，不是服饰史事实。" % raw["character"]["arc"])
    mode = str(raw.get("fidelity_mode") or "standard")
    if mode == "historical":
        assumptions.append("historical 模式：年代/文化可行性优先于视觉表现；证据不足时按脚本警告处理，不把推断写成史实。")
    elif mode == "inspired":
        assumptions.append("inspired 模式：允许对历史元素做艺术化重构；卡片中的 verified 事实只作为灵感锚点。")
    elif mode == "fictional":
        assumptions.append("fictional 模式：不主张历史准确性，只要求内部一致与可拍摄性。")
    if is_unknown(flat.get("budget")):
        assumptions.append("预算未在输入中给出：按库内默认成本策略处理，C 套仅作低预算替代提示。")
    warnings = data.get("warnings") or []
    for warning in warnings:
        text = str(warning)
        if "period evidence is approximate" in text or "period/region context card" in text:
            assumptions.append("年代/地域匹配为近似层级（脚本警告：%s）。" % text[:160])
    assumptions.append("输入未提供的属性保持 unknown，不向服装史或剧作事实补造；本文件的推荐是设计建议而非史料。")
    for item in assumptions:
        lines.append("- %s" % item)
    lines.append("")

    lines.append("## unknown")
    lines.append("")
    unknown_lines = []
    for key, label in INPUT_FIELD_LABELS:
        value = flat.get(key)
        if is_unknown(value):
            unknown_lines.append("- %s（`%s`）：未指定 / unknown，未向生成器发明取值。" % (label, key))
    for key, value in sorted(flat.items()):
        if key in labels or str(key).startswith(("state.", "scene.", "character.")):
            continue
        if is_unknown(value):
            unknown_lines.append("- `%s`：unknown" % key)
    missing = []
    for look in looks_of(data):
        if look.get("missing"):
            missing.append("%s 缺口槽位：%s" % (look.get("look_ref"), ", ".join(look["missing"])))
    if missing:
        unknown_lines.extend("- " + item for item in missing)
    for warning in warnings:
        text = str(warning)
        if "items without source_ids" in text:
            unknown_lines.append("- 无来源卡片的单品：%s" % text.split(":", 1)[-1].strip())
    if record.get("query") is not None and record.get("query_hits", 0) == 0:
        unknown_lines.append("- `query.py` 在本用例命中 0 张卡片：该查询方向的库内证据为 unknown。")
    if not unknown_lines:
        unknown_lines.append("- 本用例输入完整，无显式 unknown 字段。")
    lines.extend(unknown_lines)
    lines.append("")


def render_result(record, pair_results):
    raw = record["raw"]
    meta = record["meta"]
    data = record["data"]
    lines = []
    tid = meta.get("id") or record["path"].stem
    lines.append("# %s — %s" % (tid, meta.get("title", record["path"].stem)))
    lines.append("")
    lines.append("- 运行时间：%s" % record["timestamp"])
    lines.append("- 测试类型：%s" % ", ".join(meta.get("types", [])))
    lines.append("- 模式：%s" % meta.get("mode", "standard"))
    lines.append("- 输入文件：`%s`" % record["path"].relative_to(lib.vault_root()).as_posix())
    lines.append("- 运行命令：`%s`" % record["recommend"]["cmd"])
    lines.append("- 退出码：**%s**（耗时 %ss）" % (
        record["recommend"]["returncode"], record["recommend"]["duration"]))
    if record["recommend"]["stderr"].strip():
        lines.append("- stderr：`%s`" % record["recommend"]["stderr"].strip()[:500])
    lines.append("")
    lines.append("## 实际输入")
    lines.append("")
    clean = {key: value for key, value in raw.items() if key != "_test"}
    lines.append(md_json_block(clean))
    lines.append("")
    render_known_assumptions_unknown(lines, record)
    lines.append("## 检索执行记录")
    lines.append("")
    lines.append("| 命令 | 退出码 | 耗时 |")
    lines.append("| --- | --- | --- |")
    lines.append("| `%s` | %s | %ss |" % (
        record["recommend"]["cmd"], record["recommend"]["returncode"],
        record["recommend"]["duration"]))
    if record["query"]:
        lines.append("| `%s` | %s | %ss |" % (
            record["query"]["cmd"], record["query"]["returncode"],
            record["query"]["duration"]))
    lines.append("")
    query_ids = [row.get("id") for row in (record["query_data"] or [])
                 if isinstance(row, dict) and row.get("id")]
    lines.append("- `query.py` 命中数量：**%s**（验收要求 ≥1）" % record.get("query_hits", 0))
    lines.append("- `query.py` 命中卡片 ID：%s" % (", ".join(query_ids) if query_ids else "(none)"))
    retrieved = (data or {}).get("retrieved_ids", {})
    lines.append("- `recommend.py` 候选池：" + "; ".join(
        "%s=%s" % (slot, ", ".join(ids)) for slot, ids in sorted(retrieved.items()))
        if retrieved else "- `recommend.py` 候选池：(none)")
    selected = []
    for look in looks_of(data):
        selected.append("%s: %s" % (look.get("look_ref"),
                                    ", ".join(i["id"] for i in look.get("items", []))))
    lines.append("- 三套推荐选中：" + "; ".join(selected) if selected else "- 三套推荐选中：(none)")
    lines.append("")
    lines.append("## 候选造型 A/B/C")
    lines.append("")
    for look in looks_of(data):
        label = look.get("look_ref", "?")
        lines.append("### Look %s（score %.1f/100，cost %.3f，source_look=%s）" % (
            label, look.get("total", -1), look.get("cost", -1),
            look.get("source_look_id") or "assembled"))
        lines.append("")
        if look.get("missing"):
            lines.append("- **缺口**：%s" % ", ".join(look["missing"]))
        lines.append("| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        lines.append(fmt_items(look))
        if look.get("parts"):
            lines.append("")
            lines.append("- 结构卡：%s" % ", ".join(p["id"] for p in look["parts"]))
        if look.get("materials"):
            lines.append("- 材质卡：%s" % ", ".join(m["id"] for m in look["materials"]))
        lines.append("")
    lines.append("### 评分明细")
    lines.append("")
    labels = [("period", "年代/文化", 25), ("identity", "角色身份", 15),
              ("environment", "环境气候", 15), ("art", "美术方向", 15),
              ("movement", "动作可行", 10), ("arc", "剧情弧线", 10),
              ("camera", "摄影/一致性", 10)]
    lines.append("| 维度 | " + " | ".join(
        look.get("look_ref", "?") for look in looks_of(data)) + " |")
    lines.append("| --- | " + " | ".join("---" for _ in looks_of(data)) + " |")
    for key, label, _weight in labels:
        lines.append("| %s | %s |" % (label, " | ".join(
            str(look.get("scores", {}).get(key, "-")) for look in looks_of(data))))
    lines.append("| **总计** | %s |" % " | ".join(
        str(look.get("total", "-")) for look in looks_of(data)))
    lines.append("")
    if (data or {}).get("continuity"):
        continuity = data["continuity"]
        lines.append("## 多场次连续性")
        lines.append("")
        lines.append("- verdict：**%s**" % continuity.get("verdict"))
        if continuity.get("issues"):
            lines.append("- issues：%s" % "; ".join(continuity["issues"]))
        lines.append("")
        lines.append("| 场次 | wetness | damage | 锁定 ID |")
        lines.append("| --- | --- | --- | --- |")
        for scene in continuity.get("scenes", []):
            state = scene.get("state", {})
            lines.append("| %s | %s | %s | %s |" % (
                scene.get("scene_id"), state.get("wetness"), state.get("damage"),
                ", ".join(scene.get("item_ids", []))))
        lines.append("")
    lines.append("## 生图 / 视频 Prompt（实际输出）")
    lines.append("")
    for look in looks_of(data):
        lines.append("### Look %s" % look.get("look_ref", "?"))
        lines.append("")
        lines.append("**Image prompt (EN):**")
        lines.append("")
        lines.append("```")
        lines.append(look.get("prompt_image", ""))
        lines.append("```")
        lines.append("")
        lines.append("**Video prompt (EN):**")
        lines.append("")
        lines.append("```")
        lines.append(look.get("prompt_video", ""))
        lines.append("```")
        lines.append("")
    if (data or {}).get("continuity"):
        for scene in data["continuity"].get("scenes", []):
            lines.append("### 场景 %s — %s / %s" % (
                scene.get("scene_id"), scene.get("state", {}).get("wetness"),
                scene.get("state", {}).get("damage")))
            lines.append("")
            lines.append("**Image prompt:**")
            lines.append("")
            lines.append("```")
            lines.append(scene.get("prompt_image", ""))
            lines.append("```")
            lines.append("")
            lines.append("**Video prompt:**")
            lines.append("")
            lines.append("```")
            lines.append(scene.get("prompt_video", ""))
            lines.append("```")
            lines.append("")
    lines.append("## 风险")
    lines.append("")
    for look in looks_of(data):
        lines.append("### Look %s" % look.get("look_ref", "?"))
        lines.append("")
        for risk in look.get("risks", []):
            lines.append("- 风险：%s" % risk)
        if not look.get("risks"):
            lines.append("- 无单件/搭配级风险声明。")
        lines.append("")
    if data.get("warnings") or data.get("warnings_detail"):
        lines.append("### 脚本级风险与缺口")
        lines.append("")
        for detail in data.get("warnings_detail") or []:
            if isinstance(detail, dict):
                lines.append("- [%s/%s] %s" % (detail.get("code"), detail.get("severity"),
                                               detail.get("message")))
        for warning in data.get("warnings") or []:
            lines.append("- %s" % warning)
        lines.append("")
    else:
        lines.append("- 脚本无额外风险警告。")
        lines.append("")

    lines.append("## 证据")
    lines.append("")
    for look in looks_of(data):
        lines.append("### Look %s" % look.get("look_ref", "?"))
        lines.append("")
        for reason in look.get("reasons", []):
            lines.append("- 理由（解释性，不是史实）：%s" % reason)
        evidence = look.get("evidence", {})
        lines.append("- source_ids：%s" % (
            ", ".join(evidence.get("source_ids", [])) or "(none)"))
        for entry in evidence.get("source_urls", []):
            lines.append("- 来源链接：%s → %s" % (entry.get("source_id"), entry.get("url")))
        items = look.get("items", [])
        if items:
            lines.append("- 单件证据状态：" + "; ".join(
                "%s=%s" % (item.get("id"), item.get("evidence_status", "-")) for item in items))
        lines.append("")
    lines.append("## 验收判定")
    lines.append("")
    lines.append("| 检查项 | 结果 | 说明 |")
    lines.append("| --- | --- | --- |")
    for check in record["checks"]:
        lines.append("| %s | %s | %s |" % (check["name"], check["status"], check["detail"]))
    for name, status, detail in pair_results:
        lines.append("| %s（pair） | %s | %s |" % (name, status, detail))
    lines.append("")
    verdict = "PASS" if all(
        check["status"] == "PASS" for check in record["checks"]) and all(
        status == "PASS" for _name, status, _detail in pair_results) else "FAIL"
    lines.append("**VERDICT: %s**" % verdict)
    lines.append("")
    lines.append("## 备注")
    lines.append("")
    warnings = (data or {}).get("warnings", [])
    if warnings:
        for warning in warnings:
            lines.append("- 脚本警告：%s" % warning)
    else:
        lines.append("- 脚本无警告。")
    lines.append("- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。")
    lines.append("- 知识库为运行时刻快照；新增卡片后必须重跑本测试。")
    lines.append("")
    return "\n".join(lines), verdict


def render_summary(records, errors, vault_stats):
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = []
    lines.append("# P2 验收测试 SUMMARY")
    lines.append("")
    lines.append("- 运行时间：%s" % now)
    lines.append("- Python：%s" % sys.version.split()[0])
    lines.append("- 测试数：%d" % len(records))
    lines.append("- 结果目录：`11-验收/测试结果/`")
    lines.append("- 重跑命令：`python3 scripts/run_acceptance.py`")
    lines.append("")
    lines.append("## 知识库快照")
    lines.append("")
    lines.append("- 卡片总数：%d" % vault_stats["total"])
    for ctype, count in sorted(vault_stats["types"].items()):
        lines.append("  - `%s`: %d" % (ctype, count))
    lines.append("- 来源卡：%d" % vault_stats["sources"])
    if vault_stats["errors"]:
        lines.append("- YAML 解析问题（由检索脚本跳过）：")
        for err in vault_stats["errors"]:
            lines.append("  - `%s`: %s" % (err["path"], err["error"]))
    lines.append("")
    lines.append("## 逐例结果")
    lines.append("")
    lines.append("| 用例 | 标题 | 模式 | recommend exit | query exit | query hits | VERDICT | 失败项 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    pass_count = fail_count = 0
    for record in records:
        verdict = record["verdict"]
        if verdict == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        failed = [check["name"] for check in record["checks"]
                  if check["status"] != "PASS"]
        failed += [name for name, status, _detail in record["pair_results"]
                   if status != "PASS"]
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            record["meta"].get("id"), record["meta"].get("title", ""),
            record["meta"].get("mode", "standard"),
            record["recommend"]["returncode"],
            record["query"]["returncode"] if record["query"] else "-",
            record.get("query_hits", 0),
            verdict, ", ".join(failed) or "-"))
    lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append("- PASS：%d / %d" % (pass_count, len(records)))
    lines.append("- FAIL：%d / %d" % (fail_count, len(records)))
    hit_counts = [(record["meta"].get("id"), record.get("query_hits", 0))
                  for record in records if record.get("query") is not None]
    total_hits = sum(count for _tid, count in hit_counts)
    zero_hits = [tid for tid, count in hit_counts if count == 0]
    lines.append("- query.py 命中总数：%d（逐例：%s）" % (
        total_hits, ", ".join("%s=%d" % (tid, count) for tid, count in hit_counts)))
    lines.append("- 每个场景 query 步骤均返回 ≥1 命中：%s" % (
        "是" if hit_counts and not zero_hits else "否（%s）" % (", ".join(zero_hits) or "无 query 步骤")))
    lines.append("")
    lines.append("## 失败明细")
    lines.append("")
    if fail_count == 0:
        lines.append("- 无失败项。")
    else:
        for record in records:
            for check in record["checks"]:
                if check["status"] != "PASS":
                    lines.append("- %s `%s`：%s" % (
                        record["meta"].get("id"), check["name"], check["detail"]))
            for name, status, detail in record["pair_results"]:
                if status != "PASS":
                    lines.append("- %s pair `%s`：%s" % (
                        record["meta"].get("id"), name, detail))
    lines.append("")
    lines.append("## 知识库缺口汇总（来自脚本 warnings）")
    lines.append("")
    gap_counter = {}
    for record in records:
        for warning in (record["data"] or {}).get("warnings", []):
            gap_counter[warning] = gap_counter.get(warning, 0) + 1
    if not gap_counter:
        lines.append("- 无脚本警告。")
    else:
        for warning, count in sorted(gap_counter.items(), key=lambda kv: -kv[1]):
            lines.append("- ×%d %s" % (count, warning))
    lines.append("")
    lines.append("## 配对检查")
    lines.append("")
    pair_rows = []
    for record in records:
        for name, status, detail in record["pair_results"]:
            pair_rows.append("- %s → `%s`：%s（%s）" % (
                record["meta"].get("id"), name, status, detail))
    lines.extend(pair_rows or ["- 无配对检查。"])
    lines.append("")
    lines.append("## 说明与限制")
    lines.append("")
    lines.append("- 所有命令均为真实 `python3` 子进程，退出码与原始输出见各用例文件与 `raw/`。")
    lines.append("- 测试只验证 P2 决策闭环（检索/评分/提示词/连续性）；Obsidian GUI、图片授权与史学正确性需另行人工核验。")
    lines.append("- 若知识库新增卡片，必须重跑 `python3 scripts/run_acceptance.py` 更新本 SUMMARY。")
    lines.append("")
    return "\n".join(lines), pass_count, fail_count


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Run real P2 acceptance tests.")
    parser.add_argument("--only", help="comma separated test ids, e.g. T03,T17")
    parser.add_argument("--no-write", action="store_true", help="do not write result files")
    args = parser.parse_args(argv)

    root = lib.vault_root()
    cards, card_errors = lib.load_cards()
    card_index = {lib.get_str(card["meta"], "id"): card for card in cards}
    source_ids = set(card_index)
    vault_stats = {
        "total": len(cards),
        "types": {},
        "sources": sum(1 for card in cards
                       if lib.norm_text(card["meta"].get("type")) == "source"),
        "errors": card_errors,
    }
    for card in cards:
        ctype = lib.get_str(card["meta"], "type") or "unknown"
        vault_stats["types"][ctype] = vault_stats["types"].get(ctype, 0) + 1

    only = set(part.strip() for part in args.only.split(",")) if args.only else None
    test_items = [item for item in load_test_inputs(root)
                  if not only or item["meta"].get("id") in only]
    if not test_items:
        print("No matching tests found in %s" % (root / INPUTS_DIR), file=sys.stderr)
        return 2

    results_dir = root / RESULTS_DIR
    raw_dir = results_dir / "raw"
    if not args.no_write:
        results_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for item in test_items:
        path = item["path"]
        meta = item["meta"]
        tid = meta.get("id") or path.stem
        print("== %s %s" % (tid, meta.get("title", "")))
        if meta.get("brief"):
            recommend = run_command(
                [sys.executable, "scripts/recommend.py",
                 "--brief", str(meta["brief"]), "--json"], root)
        else:
            recommend = run_command(
                [sys.executable, "scripts/recommend.py", str(path), "--json"], root)
        print("   recommend.py exit=%s (%.2fs)" % (
            recommend["returncode"], recommend["duration"]))
        data = safe_json(recommend["stdout"])
        query = None
        query_data = None
        query_args = meta.get("query") or []
        if query_args:
            query = run_command([sys.executable, "scripts/query.py"] + query_args, root)
            print("   query.py exit=%s (%.2fs)" % (
                query["returncode"], query["duration"]))
            query_data = safe_json(query["stdout"])
        record = {
            "path": path,
            "raw": item["raw"],
            "meta": meta,
            "recommend": recommend,
            "query": query,
            "data": data,
            "query_data": query_data,
            "query_hits": len(query_data) if isinstance(query_data, list) else 0,
            "timestamp": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "checks": [],
            "pair_results": [],
        }
        criteria = list(meta.get("criteria", []))
        if query is not None and "query_hits" not in criteria:
            criteria.append("query_hits")
        for name in criteria:
            status, detail = criterion(name, record, card_index, source_ids)
            record["checks"].append({"name": name, "status": status, "detail": detail})
        records.append(record)
        if not args.no_write:
            raw_name = path.stem + ".json"
            (raw_dir / raw_name).write_text(
                recommend["stdout"] or json.dumps(
                    {"returncode": recommend["returncode"],
                     "stderr": recommend["stderr"]}, ensure_ascii=False, indent=2),
                encoding="utf-8")
            if query is not None:
                (raw_dir / (path.stem + ".query.json")).write_text(
                    query["stdout"] or "[]", encoding="utf-8")

    # pair checks are evaluated after both sides have run
    by_id = {record["meta"].get("id"): record for record in records}
    for record in records:
        pair_with = record["meta"].get("pair_with")
        if not pair_with or pair_with not in by_id:
            continue
        other = by_id[pair_with]
        pair_name = record["meta"].get("pair_check", "pair")
        status, detail = pair_check(pair_name, record, other)
        record["pair_results"].append((pair_name, status, detail))

    rendered = []
    for record in records:
        text, verdict = render_result(record, record["pair_results"])
        record["verdict"] = verdict
        rendered.append((record, text))
        if not args.no_write:
            out_path = results_dir / (record["path"].stem + ".md")
            out_path.write_text(text + "\n", encoding="utf-8")
            print("   wrote %s" % out_path.relative_to(root))

    summary_text, pass_count, fail_count = render_summary(records, card_errors, vault_stats)
    if not args.no_write:
        (results_dir / "SUMMARY.md").write_text(summary_text + "\n", encoding="utf-8")
        print("wrote", (results_dir / "SUMMARY.md").relative_to(root))
    else:
        print(summary_text)

    print("PASS %d / %d, FAIL %d / %d" % (pass_count, len(records),
                                           fail_count, len(records)))
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
