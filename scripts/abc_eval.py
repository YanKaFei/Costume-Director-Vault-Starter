#!/usr/bin/env python3
"""Independent A/B/C quality evaluation for P4 outfit compositions (AUD-001).

Generation (outfit.py) and quality evaluation are separate: this script reads a
composer input or an existing outfit JSON and scores actual structural
differences, hard constraints, source validity, coordination, narrative fit and
repeat/one-item-swap gaming.  It is diagnostic, not a substitute for the human
director review.

Usage:
    python3 scripts/abc_eval.py --input input.json
    python3 scripts/abc_eval.py --outfit outfit.json
    python3 scripts/abc_eval.py --heldout DIR --json
"""
import argparse
import json
import sys
from pathlib import Path

import costume_lib as lib
import outfit
import recommend


def _items(look):
    return [item for item in (look.get("items") or []) if item]


def _ids(look):
    return {item["id"] for item in _items(look)}


def _slots(look):
    return {item.get("slot"): item["id"] for item in _items(look)}


def _palette(look):
    return set((look.get("palette") or {}).get("colors") or [])


def _materials(look):
    return set((look.get("materials") or {}).get("materials") or [])


def _silhouette(look):
    return (look.get("silhouette") or {}).get("shape")


def pair_metrics(left, right):
    lid, rid = _ids(left), _ids(right)
    lslot, rslot = _slots(left), _slots(right)
    item_diff = len(lid.symmetric_difference(rid))
    slot_diff = sum(1 for slot in set(lslot) | set(rslot)
                    if lslot.get(slot) != rslot.get(slot))
    palette_diff = len(_palette(left).symmetric_difference(_palette(right)))
    material_diff = len(_materials(left).symmetric_difference(_materials(right)))
    silhouette_diff = _silhouette(left) != _silhouette(right)
    narrative_diff = bool((left.get("narrative_meaning") or "").strip()) and         (left.get("narrative_meaning") != right.get("narrative_meaning"))
    # Independent conceptual axes.  A single item swap is one item-difference
    # axis only, regardless of a silhouette change; meaningful direction needs
    # >=2 actual item changes across >=2 slots plus at least a second axis.
    axes = []
    if item_diff >= 4:
        axes.append("items")
    if slot_diff >= 2:
        axes.append("slots")
    if silhouette_diff:
        axes.append("silhouette")
    if material_diff >= 2:
        axes.append("materials")
    if palette_diff >= 2:
        axes.append("palette")
    if narrative_diff:
        axes.append("narrative")
    meaningful = ("items" in axes and "slots" in axes and len(axes) >= 2)
    one_item_swap = (item_diff <= 2 or slot_diff < 2)
    return {
        "item_diff": item_diff,
        "slot_diff": slot_diff,
        "palette_diff": palette_diff,
        "material_diff": material_diff,
        "silhouette_diff": silhouette_diff,
        "narrative_diff": narrative_diff,
        "axes": axes,
        "silhouettes": [_silhouette(left), _silhouette(right)],
        "meaningful": bool(meaningful),
        "one_item_swap_gaming": bool(one_item_swap),
    }


def evaluate(payload, by_id, sources):
    looks = payload.get("looks") or []
    looks = [look for look in looks if _items(look)]
    status = payload.get("status", "ok")
    violations = payload.get("constraint_violations") or []
    source_ids = []
    missing_sources = []
    item_errors = []
    for look in looks:
        for item in _items(look):
            cid = item.get("id")
            if cid not in by_id:
                item_errors.append("unknown item ID %s" % cid)
            if item.get("evidence_status") == "example":
                item_errors.append("example card %s" % cid)
            for sid in item.get("source_ids") or []:
                source_ids.append(sid)
                if sid not in sources:
                    missing_sources.append(sid)
    pairs = {}
    if len(looks) >= 2:
        for i, j, label in ((0, 1, "a_b"), (0, 2, "a_c"), (1, 2, "b_c")):
            if j < len(looks):
                pairs[label] = pair_metrics(looks[i], looks[j])
    idsets = [ _ids(look) for look in looks ]
    duplicate = len({frozenset(ids) for ids in idsets}) < len(idsets) if idsets else False
    # Synonym/recolour-only detection: same item set, different order/names is
    # still not a costume-direction difference.
    synonym_only = False
    if len(idsets) >= 2:
        for i in range(len(idsets)):
            for j in range(i + 1, len(idsets)):
                if idsets[i] == idsets[j]:
                    synonym_only = True
    pair_values = [value for value in pairs.values()]
    meaningful_pairs = [value for value in pair_values if value["meaningful"]]
    gaming_pairs = [value for value in pair_values if value["one_item_swap_gaming"]]
    coord = [look.get("palette", {}).get("harmony", 0.0) for look in looks]
    mat_harmony = [look.get("materials", {}).get("harmony", 0.0) for look in looks]
    narrative = [bool(look.get("narrative_meaning")) for look in looks]
    constraints_ok = status == "ok" and not violations
    overridden = status == "override"
    checks = {
        "status": status,
        "three_looks": len(looks) == 3,
        "hard_constraints_passed": constraints_ok,
        "declared_mismatch": status == "declared_mismatch",
        "declared_mismatch_count": len(payload.get("declared_mismatches") or []),
        "override": overridden,
        "historical_accuracy": payload.get("historical_accuracy", False),
        "constraint_violations": len(violations),
        "all_items_real": not item_errors,
        "source_ids": sorted(set(source_ids)),
        "missing_source_ids": sorted(set(missing_sources)),
        "source_coverage": (len(set(source_ids)) - len(set(missing_sources))) /
                           float(len(set(source_ids))) if source_ids else 0.0,
        "all_pairs_meaningful": bool(pair_values) and all(v["meaningful"] for v in pair_values),
        "meaningful_pairs": len(meaningful_pairs),
        "gaming_pairs": len(gaming_pairs),
        "one_item_swap_gaming": any(v["one_item_swap_gaming"] for v in pair_values),
        "duplicate_looks": duplicate,
        "synonym_or_reorder_only": synonym_only,
        "palette_harmony": round(sum(coord) / float(len(coord)), 3) if coord else 0.0,
        "material_harmony": round(sum(mat_harmony) / float(len(mat_harmony)), 3) if mat_harmony else 0.0,
        "narrative_present": all(narrative) if narrative else False,
        "not_for_director_review": True,
    }
    # A high automated score cannot substitute for director review.
    checks["automated_score"] = round(
        100.0 * (
            0.25 * (1.0 if checks["all_pairs_meaningful"] else 0.0) +
            0.2 * (1.0 if checks["hard_constraints_passed"] or overridden else 0.0) +
            0.15 * checks["source_coverage"] +
            0.15 * checks["palette_harmony"] +
            0.1 * checks["material_harmony"] +
            0.1 * (1.0 if checks["narrative_present"] else 0.0) +
            0.05 * (0.0 if gaming_pairs else 1.0)
        ), 1)
    checks["automated_score_note"] = (
        "Heuristic diagnostic only. Not a director score, not a historical "
        "accuracy claim; human review remains required.")
    checks["pair_metrics"] = pairs
    checks["pass"] = (
        len(looks) == 3 and
        checks["all_items_real"] and
        not checks["missing_source_ids"] and
        checks["all_pairs_meaningful"] and
        not checks["one_item_swap_gaming"] and
        not checks["duplicate_looks"] and
        not checks["synonym_or_reorder_only"] and
        (checks["hard_constraints_passed"] or checks["override"] or
         checks["declared_mismatch"]) and
        (checks["historical_accuracy"] is False or not checks["override"])
    )
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser(description="Independent A/B/C outfit evaluator")
    parser.add_argument("--input", help="composer input JSON")
    parser.add_argument("--outfit", help="existing outfit JSON")
    parser.add_argument("--heldout", help="directory of held-out composer input JSON")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    sources = {lib.get_str(card["meta"], "id"): card for card in cards
               if lib.norm_text(card["meta"].get("type")) == "source"}
    outputs = []
    if args.heldout:
        for path in sorted(Path(args.heldout).glob("*.json")):
            raw = json.loads(path.read_text(encoding="utf-8"))
            inp = outfit.normalise_composer_input(raw)
            payload = outfit.composer_payload(inp, cards, sources)
            checks = evaluate(payload, by_id, sources)
            checks["case"] = path.stem
            outputs.append(checks)
    elif args.outfit:
        payload = json.loads(Path(args.outfit).read_text(encoding="utf-8"))
        outputs.append(evaluate(payload, by_id, sources))
    elif args.input:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        inp = outfit.normalise_composer_input(raw)
        payload = outfit.composer_payload(inp, cards, sources)
        outputs.append(evaluate(payload, by_id, sources))
        outputs[0]["composer_status"] = payload.get("status")
        outputs[0]["constraint_violations"] = payload.get("constraint_violations")
    else:
        print("ERROR: provide --input, --outfit or --heldout", file=sys.stderr)
        return 2
    text = json.dumps(outputs if args.heldout else outputs[0],
                      ensure_ascii=False, indent=2)
    print(text)
    return 0 if all(item.get("pass") for item in outputs) else 1


if __name__ == "__main__":
    sys.exit(main())
