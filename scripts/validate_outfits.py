#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate Outfit knowledge objects (P5-C / task-70).

Backward compatible: LOOK cards without v1.4 fields are reported as `legacy`
(accepted, warnings only). New Outfit objects must declare evidence_type,
complete slots and pass scripts/outfit.py hard constraints. Historical
evidence_type fails if hard constraints fail.

Examples:
  python3 scripts/validate_outfits.py --vault . --all --json
  python3 scripts/validate_outfits.py --vault . --look LOOK-0001
  python3 scripts/validate_outfits.py --vault . --input /tmp/outfit.json --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = str(ROOT / "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import costume_lib as lib  # noqa: E402
import outfit  # noqa: E402
import recommend  # noqa: E402

SLOTS = set(outfit.SLOTS)
REQUIRED_CHECKS = {"period", "region", "identity", "weather", "action", "compatibility", "approved_anchors"}
EVIDENCE_TYPES = {"historical_evidence", "sourced_style_observation", "creative_inference"}
NEW_KEYS = {"outfit_slots", "evidence_type", "historical_evidence", "style_observation",
            "creative_inference", "constraints_checked", "period_tiers", "region_tiers",
            "approved_anchors", "context", "character_function", "continuity_state",
            "outfit_silhouette"}
SRC_RE = re.compile(r"SRC-\d{4}")


def load_vault(vault):
    cards, errors = lib.load_cards(root=str(vault))
    if errors:
        for err in errors:
            sys.stderr.write("WARN card parse: %s (%s)\n" % (err.get("path"), err.get("error")))
    sources = lib.load_sources(cards=cards)
    by_id = {lib.get_str(c["meta"], "id"): c for c in cards}
    return cards, sources, by_id, errors


def parse_pairs(value, field):
    """Parse list strings 'slot=value' or dict into {slot: value}."""
    if not value:
        return {}
    if isinstance(value, dict):
        return {str(k): str(v) for k, v in value.items()}
    out = {}
    for item in value if isinstance(value, list) else [value]:
        text = str(item)
        if "=" not in text:
            raise ValueError("%s item must be 'slot=value': %s" % (field, text))
        key, val = text.split("=", 1)
        out[key.strip()] = val.strip()
    return out


def card_items(meta):
    return [str(x) for x in (meta.get("look_items") or []) if str(x)]


def derive_slots(meta, by_id):
    slots = {}
    for cid in card_items(meta):
        card = by_id.get(cid)
        if not card or card["meta"].get("type") != "garment":
            continue
        slot = recommend.classify_slot(card)
        if slot and slot in SLOTS and slot not in slots:
            slots[slot] = cid
    return slots


def parse_outfit(card, by_id):
    """Return (id, meta, slots, is_new)."""
    meta = card["meta"]
    oid = lib.get_str(meta, "id")
    explicit = {}
    if meta.get("outfit_slots"):
        explicit = parse_pairs(meta.get("outfit_slots"), "outfit_slots")
    slots = explicit or derive_slots(meta, by_id)
    is_new = any(k in meta for k in NEW_KEYS)
    return oid, meta, slots, is_new


def tiers_from_cards(slots, by_id, field):
    out = {}
    for slot, cid in slots.items():
        card = by_id.get(cid)
        if not card:
            out[slot] = "unknown"
            continue
        ev = lib.get_str(card["meta"], "evidence_status")
        out[slot] = {"verified": "era", "interpretive": "approximate",
                     "example": "none"}.get(ev, "unknown")
    return out


def validate_one(oid, meta, slots, is_new, cards, sources, by_id, synthetic=False):
    errors, warnings = [], []
    et = lib.get_str(meta, "evidence_type")
    if not et:
        if is_new:
            errors.append("new Outfit object requires evidence_type")
        else:
            warnings.append("legacy LOOK: no evidence_type (accepted; cannot be used as historical evidence)")
    elif et not in EVIDENCE_TYPES:
        errors.append("invalid evidence_type: %s" % et)

    if not slots:
        if is_new:
            errors.append("outfit_slots/look_items produced no garment slots")
        else:
            warnings.append("legacy LOOK: no derivable garment slots")
    for slot in slots:
        if slot not in SLOTS:
            (errors if is_new else warnings).append("invalid slot: %s" % slot)
    ids = list(slots.values())
    if len(ids) != len(set(ids)):
        (errors if is_new else warnings).append("duplicate item IDs across slots: %s" % ids)
    for cid in ids:
        card = by_id.get(cid)
        if not card:
            (errors if is_new else warnings).append("slot card not found: %s" % cid)
        elif card["meta"].get("type") != "garment":
            (errors if is_new else warnings).append("slot item is not a garment card: %s (%s)" % (cid, card["meta"].get("type")))
        elif lib.get_str(card["meta"], "evidence_status") == "example":
            if et == "historical_evidence":
                errors.append("historical_evidence contains example card: %s" % cid)
            else:
                warnings.append("example card in outfit: %s" % cid)
    torso = ("one_piece" in slots or "set" in slots or
             ("upper_body" in slots and "lower_body" in slots))
    if is_new and not torso:
        errors.append("incomplete outfit: need one_piece/set or upper_body+lower_body")
    if is_new and "footwear" not in slots:
        errors.append("incomplete outfit: missing footwear")
    if "one_piece" in slots and ({"upper_body", "lower_body"} & set(slots)):
        (errors if is_new else warnings).append("torso conflict: one_piece with upper/lower")
    if "set" in slots and ({"upper_body", "lower_body", "one_piece"} & set(slots)):
        (errors if is_new else warnings).append("torso conflict: set with another torso layer")

    checks = []
    if meta.get("constraints_checked"):
        checks = [str(x).strip() for x in meta.get("constraints_checked")]
    if et == "historical_evidence" and is_new:
        if not checks:
            errors.append("historical_evidence requires constraints_checked")
        else:
            missing = REQUIRED_CHECKS - set(checks)
            if missing:
                errors.append("constraints_checked missing: %s" % sorted(missing))
        hist = [str(x) for x in (meta.get("historical_evidence") or [])]
        if not hist:
            errors.append("historical_evidence requires historical_evidence list")
        srcs = []
        for x in hist:
            srcs.extend(SRC_RE.findall(x))
        if not any(s in sources for s in srcs):
            errors.append("historical_evidence has no resolvable SRC id")
        for s in srcs:
            if s not in sources:
                errors.append("historical_evidence references unknown source: %s" % s)
    if et == "sourced_style_observation" and is_new:
        if not meta.get("style_observation"):
            errors.append("sourced_style_observation requires style_observation")
    if et == "creative_inference" and is_new:
        if not meta.get("creative_inference"):
            errors.append("creative_inference requires creative_inference note")

    anchors = [str(x) for x in (meta.get("approved_anchors") or [])]
    for cid in anchors:
        if cid not in ids:
            errors.append("approved anchor missing from outfit slots: %s" % cid)

    # build payload expected by scripts/outfit.py
    items = []
    for slot, cid in slots.items():
        card = by_id.get(cid)
        if not card:
            continue
        items.append({
            "slot": slot, "id": cid,
            "name_zh": lib.get_str(card["meta"], "name_zh"),
            "name_en": lib.get_str(card["meta"], "name_en"),
            "colors": list(card["meta"].get("colors") or []),
            "materials": list(card["meta"].get("materials") or []),
            "evidence_status": lib.get_str(card["meta"], "evidence_status"),
            "source_ids": list(card["meta"].get("source_ids") or []),
        })
    ptiers = parse_pairs(meta.get("period_tiers"), "period_tiers") if meta.get("period_tiers") else tiers_from_cards(slots, by_id, "period_tiers")
    rtiers = parse_pairs(meta.get("region_tiers"), "region_tiers") if meta.get("region_tiers") else tiers_from_cards(slots, by_id, "region_tiers")
    look = {"look_ref": oid, "items": items, "slot_ids": slots,
            "period_tiers": ptiers, "region_tiers": rtiers}
    payload = {"looks": [look], "occupation_anchor": None}
    periods = list(meta.get("periods") or [])
    regions = list(meta.get("regions") or [])
    ctx = " ".join(str(x) for x in (meta.get("context") or [])) if isinstance(meta.get("context"), list) else str(meta.get("context") or "")
    inp = {
        "fidelity_mode": {"historical_evidence": "historical",
                          "sourced_style_observation": "inspired",
                          "creative_inference": "fictional"}.get(et, "inspired"),
        "period": periods[0] if periods else "unknown",
        "region": regions[0] if regions else "unknown",
        "weather": str(meta.get("weather") or "dry"),
        "action": str(meta.get("action") or "standing"),
        "scene": ctx or "unspecified",
        "location": str(meta.get("location") or ""),
        "approved_anchors": anchors,
    }
    # optional explicit weather/action for synthetic inputs and tests
    if meta.get("weather"):
        inp["weather"] = str(meta.get("weather"))
    if meta.get("action"):
        inp["action"] = str(meta.get("action"))
    if meta.get("location"):
        inp["location"] = str(meta.get("location"))
    try:
        violations = outfit.validate_hard_constraints(payload, inp, cards)
    except Exception as exc:  # hard-constraint engine failure is a validator error
        errors.append("outfit.validate_hard_constraints failed: %s" % exc)
        violations = []
    if violations:
        if et == "historical_evidence":
            errors.extend("hard constraint: %s (%s)" % (v.get("code"), v.get("message")) for v in violations)
        else:
            warnings.extend("hard constraint (non-historical): %s" % v.get("code") for v in violations)
    status = "fail" if errors else ("legacy" if not is_new else "pass")
    if not errors and not is_new and warnings:
        status = "legacy_warn"
    return {
        "id": oid, "status": status, "legacy": not is_new,
        "evidence_type": et or None,
        "slots": slots,
        "errors": errors,
        "warnings": warnings,
        "hard_constraints": {
            "passed": not violations,
            "violations": violations,
            "item_compatibility": payload.get("item_compatibility", []),
            "declared_mismatches": payload.get("declared_mismatches", []),
        },
        "constraints_checked": checks,
        "period_tiers": ptiers, "region_tiers": rtiers,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(prog="validate_outfits.py",
                                 description="Validate Outfit knowledge objects against Outfit model + outfit.py hard constraints")
    ap.add_argument("--vault", default=str(ROOT))
    ap.add_argument("--look", action="append", default=[], help="LOOK id(s); repeatable")
    ap.add_argument("--all", action="store_true", help="validate all LOOK cards")
    ap.add_argument("--input", default=None, help="synthetic outfit JSON (object or list/outfits)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    vault = Path(args.vault).resolve()
    cards, sources, by_id, load_errors = load_vault(vault)
    results = []
    if args.input:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        outfits = data.get("outfits") if isinstance(data, dict) and "outfits" in data else [data]
        for obj in outfits:
            meta = dict(obj)
            oid = str(meta.get("id") or meta.get("look_id") or "INPUT")
            slots = parse_pairs(meta.get("outfit_slots"), "outfit_slots") if meta.get("outfit_slots") else derive_slots(meta, by_id)
            results.append(validate_one(oid, meta, slots, True, cards, sources, by_id, synthetic=True))
    else:
        look_ids = [lib.get_str(c["meta"], "id") for c in cards if c["meta"].get("type") == "look"]
        selected = look_ids if (args.all or not args.look) else [x for x in look_ids if x in set(args.look)]
        missing = set(args.look) - set(look_ids)
        for m in sorted(missing):
            results.append({"id": m, "status": "fail", "errors": ["LOOK id not found"], "warnings": []})
        for c in cards:
            if c["meta"].get("type") != "look":
                continue
            oid, meta, slots, is_new = parse_outfit(c, by_id)
            if oid in selected:
                results.append(validate_one(oid, meta, slots, is_new, cards, sources, by_id))
    summary = {
        "vault": str(vault),
        "looks": len(results),
        "passed": sum(1 for r in results if r.get("status") == "pass"),
        "failed": sum(1 for r in results if r.get("status") == "fail"),
        "legacy": sum(1 for r in results if r.get("legacy")),
        "errors": load_errors,
    }
    out = {"summary": summary, "results": results}
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    if args.json or args.out:
        print(text)
    else:
        for r in results:
            print("%-8s %-14s %s" % (r["id"], r["status"], "; ".join(r.get("errors") or r.get("warnings") or [])))
        print("summary: %d looks, pass %d, fail %d, legacy %d" % (
            summary["looks"], summary["passed"], summary["failed"], summary["legacy"]))
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
