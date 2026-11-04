#!/usr/bin/env python3
"""outfit.py - full-slot Outfit Composer on top of the existing recommend engine.

This is a thin P4 composition layer around scripts/recommend.py.  It does NOT
replace or modify the legacy recommend/query/workflow CLIs; it adds:

  - complete slot coverage (upper+lower or one-piece, outerwear, footwear,
    accessory, carried prop) with real card IDs and SRC provenance;
  - colour/material harmony and silhouette/proportion metrics;
  - period/region/culture + occupation/class/occasion + weather/action/
    lighting/camera fit notes;
  - A/B/C structural difference metrics (>=2 item difference where possible);
  - wetness/damage/dirt continuity states (explicit input only, never invented);
  - English image/video prompts + negative constraints;
  - explicit warnings/evidence gaps.

Usage:
    python3 scripts/outfit.py --input input.json [--json] [--out file]
    python3 scripts/outfit.py --brief "..." [--json]
Exit codes: 0 = at least one composed look; 2 = bad input; 3 = no candidates.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import costume_lib as lib
import recommend

CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")
SLOTS = ["inner_layer", "upper_body", "lower_body", "one_piece", "set",
         "outerwear", "footwear", "accessory", "carried_prop"]
SLOT_LABELS = {
    "inner_layer": "inner layer", "upper_body": "top", "lower_body": "bottom",
    "one_piece": "one-piece / dress", "set": "set", "outerwear": "outerwear",
    "footwear": "footwear", "accessory": "accessory",
    "carried_prop": "carried prop",
}
NEUTRALS = {"black", "white", "gray", "grey", "beige", "cream", "ivory", "tan",
            "brown", "charcoal", "silver", "gold", "taupe", "stone"}
WARM = {"red", "orange", "yellow", "pink", "burgundy", "maroon", "rust",
        "mustard", "coral", "peach", "rose", "crimson", "amber", "copper"}
COOL = {"blue", "navy", "indigo", "green", "teal", "purple", "violet",
        "turquoise", "emerald", "cyan", "lavender", "mint"}
MATERIAL_FAMILIES = {
    "wool": {"wool", "tweed", "cashmere", "flannel", "suiting"},
    "linen": {"linen", "hemp", "ramie"},
    "cotton": {"cotton", "denim", "canvas", "poplin", "muslin"},
    "silk": {"silk", "satin", "damask", "velvet", "crepe", "chiffon", "taffeta"},
    "leather": {"leather", "suede", "hide", "skin"},
    "metal": {"metal", "silver", "gold", "iron", "steel", "brass", "bronze"},
    "synthetic": {"polyester", "nylon", "acrylic", "spandex", "vinyl", "pvc",
                  "rayon", "viscose", "synthetic", "rubber"},
}
SILHOUETTE_HINTS = [
    ("A", ("a-line", "a line", "flared", "flare", "full skirt", "tent")),
    ("X", ("fitted waist", "cinched", "nipped", "hourglass", "peplum")),
    ("H", ("straight", "column", "boxy", "shift", "tunic")),
    ("Y", ("shoulder", "epaulette", "puffed shoulder", "strong shoulder",
           "wide shoulder", "cape")),
    ("O", ("oversized", "loose", "voluminous", "cocoon", "ball")),
]


def english_only(text):
    text = str(text or "")
    parts = re.split(r"(?<=[.;])\s+", text)
    kept = [part for part in parts if part.strip() and not CJK_RE.search(part)]
    cleaned = " ".join(kept).strip()
    if not cleaned:
        cleaned = CJK_RE.sub("", text)
    return re.sub(r"\s+", " ", cleaned).strip()


def item_colors(item):
    return [lib.norm_text(color) for color in (item.get("colors") or []) if color]


def color_family(color):
    color = lib.norm_text(color)
    if not color:
        return "unknown"
    for token in color.replace("_", " ").split():
        if token in NEUTRALS:
            return "neutral"
        if token in WARM:
            return "warm"
        if token in COOL:
            return "cool"
    return "neutral" if color in NEUTRALS else "other"


def item_materials(item):
    return [lib.norm_text(material) for material in (item.get("materials") or [])
            if material]


def material_family(material):
    material = lib.norm_text(material)
    for family, words in MATERIAL_FAMILIES.items():
        if any(word in material for word in words):
            return family
    return "other"


def all_items(look):
    return [item for item in (look.get("items") or {}).values() if item]


def color_profile(items):
    colors = []
    for item in items:
        colors.extend(item_colors(item))
    families = {}
    for color in colors:
        family = color_family(color)
        families[family] = families.get(family, 0) + 1
    total = float(len(colors)) or 1.0
    shares = {family: count / total for family, count in families.items()}
    distinct = len({color for color in colors if color})
    dominant_family = max(shares, key=shares.get) if shares else "unknown"
    dominant_share = shares.get(dominant_family, 0.0)
    # a harmony heuristic: 2-4 families, not one family overwhelming, and at
    # least 2 distinct colours.  It is deterministic, not a colour-science claim.
    if distinct <= 1:
        score = 0.25
    elif dominant_share >= 0.85:
        score = 0.45
    elif dominant_share >= 0.7:
        score = 0.7
    elif len({f for f in families if f not in ("unknown", "other")}) >= 2:
        score = 0.92
    else:
        score = 0.78
    return {
        "colors": sorted(set(colors)),
        "families": families,
        "dominant_family": dominant_family,
        "dominant_share": round(dominant_share, 3),
        "harmony": round(score, 3),
    }


def material_profile(items):
    materials = []
    for item in items:
        materials.extend(item_materials(item))
    families = {}
    for material in materials:
        family = material_family(material)
        families[family] = families.get(family, 0) + 1
    total = float(len(materials)) or 1.0
    distinct = len(families)
    if distinct <= 1:
        score = 0.4
    elif distinct == 2:
        score = 0.85
    else:
        score = 0.9
    # leather + wool, silk + metal, linen + cotton are common compatible pairs.
    compatible = 0
    for left, right in (("leather", "wool"), ("silk", "metal"),
                        ("linen", "cotton"), ("wool", "cotton"),
                        ("silk", "leather")):
        if left in families and right in families:
            compatible += 1
    score = min(1.0, score + 0.05 * compatible)
    return {
        "materials": sorted(set(materials)),
        "families": families,
        "distinct": distinct,
        "harmony": round(score, 3),
    }


def silhouette_profile(items):
    hay = []
    for item in items:
        meta = item.get("card", {}).get("meta", {})
        hay.extend([lib.norm_text(meta.get("silhouette")),
                    lib.norm_text(meta.get("name_zh")),
                    lib.norm_text(meta.get("name_en")),
                    lib.norm_text(meta.get("subcategory")),
                    " ".join(lib.norm_text(tag) for tag in meta.get("tags", []))])
        hay.append(lib.norm_text(item.get("name_zh")))
        hay.append(lib.norm_text(item.get("name_en")))
    text = " | ".join(value for value in hay if value)
    scores = {}
    for shape, words in SILHOUETTE_HINTS:
        scores[shape] = sum(1 for word in words if word in text)
    # I/straight is the fallback when cards do not document a silhouette.
    shape = max(scores, key=scores.get) if any(scores.values()) else "I"
    # proportion: defined waist, balanced top/bottom, or one-piece/outer layer.
    slots = {item.get("slot") for item in items}
    has_waist = any(word in text for word in
                    ("fitted waist", "cinched", "belt", "peplum", "waistline"))
    balanced = ("upper_body" in slots and "lower_body" in slots) or \
               ("one_piece" in slots) or ("set" in slots)
    layered = "outerwear" in slots
    proportion = 0.5
    if balanced:
        proportion += 0.2
    if has_waist:
        proportion += 0.15
    if layered:
        proportion += 0.08
    return {
        "shape": shape,
        "proportion": round(min(1.0, proportion), 3),
        "has_defined_waist": has_waist,
        "balanced_slots": balanced,
        "layered": layered,
    }


def difference_count(left, right):
    left_ids = {item["id"] for item in all_items(left)}
    right_ids = {item["id"] for item in all_items(right)}
    return len(left_ids.symmetric_difference(right_ids))


def look_ids(look):
    return [item["id"] for item in all_items(look)]


def domain_fit(result, look):
    inp = result["input"]
    checks = result["checks"]
    risks = " ".join(look.get("risks") or [])
    return {
        "period": inp.get("period"),
        "region": inp.get("region"),
        "culture": inp.get("culture"),
        "period_evidence": look.get("period_tiers", {}),
        "region_evidence": look.get("region_tiers", {}),
        "occupation": checks.get("occupation_category"),
        "occupation_match": checks.get("occupation_match"),
        "class": inp.get("economic_status") or inp.get("class"),
        "occasion": checks.get("occasion_match"),
        "weather": inp.get("weather"),
        "action": inp.get("action"),
        "lighting": inp.get("lighting"),
        "camera": inp.get("camera"),
        "weather_risk": "open footwear" in risks or "weather:" in risks,
        "movement_risk": "dance:" in risks,
        "budget": inp.get("budget"),
        "budget_mode": look.get("budget_mode"),
    }


def composer_look(look, result, cards, sources, ctx):
    items = look.get("items") or {}
    selected = all_items(look)
    palette = color_profile(selected)
    mats = material_profile(selected)
    sil = silhouette_profile(selected)
    source_ids = []
    for item in selected:
        source_ids.extend(item.get("source_ids") or [])
    evidence = look.get("evidence") or {}
    source_ids.extend(evidence.get("source_ids") or [])
    source_ids = lib.unique_ordered(source_ids)
    missing_src = [sid for sid in source_ids if sid not in sources]
    no_src = [item["id"] for item in selected if not item.get("source_ids")]
    item_evidence = {item["id"]: item.get("evidence_status") for item in selected}
    image_prompt = english_only(look.get("prompt_image", ""))
    video_prompt = english_only(look.get("prompt_video", ""))
    action = (result.get("input") or {}).get("action") or "unknown"
    movement_note = ("movement/action adaptation: %s; preserve range of motion, "
                     "layer stability and footwear traction in motion" % action)
    outfit_prompt = (
        "complete outfit: one coherent full-body look; %s; %s; silhouette %s; "
        "proportion %.2f; palette %s; materials %s; keep every card ID, colour, "
        "material and accessory position consistent across shots; "
        "negative constraints: no costume morphing, no extra layers, no colour shift, "
        "no invented accessories, no logo/text/watermark, no changing hairstyle"
        % (
            "; ".join("%s %s" % (SLOT_LABELS.get(item.get("slot"), item.get("slot")),
                                 item.get("id")) for item in selected),
            movement_note,
            sil["shape"], sil["proportion"], ", ".join(palette["colors"]),
            ", ".join(mats["materials"]),
        )
    )
    covered = []
    if "one_piece" in items or "set" in items or ("upper_body" in items and "lower_body" in items):
        covered.append("torso")
    if "outerwear" in items:
        covered.append("outerwear")
    if "footwear" in items:
        covered.append("footwear")
    if "accessory" in items:
        covered.append("accessory")
    if "carried_prop" in items:
        covered.append("carried_prop")
    return {
        "look_ref": look.get("look_ref"),
        "total": look.get("total"),
        "items": [
            {"slot": item.get("slot"), "id": item["id"],
             "name_zh": item.get("name_zh"), "name_en": item.get("name_en"),
             "colors": item.get("colors") or [],
             "materials": item.get("materials") or [],
             "evidence_status": item.get("evidence_status"),
             "source_ids": item.get("source_ids") or []}
            for item in selected
        ],
        "covered_slots": covered,
        "slot_count": len(selected),
        "slot_ids": {slot: item["id"] for slot, item in items.items() if item},
        "missing_slots": look.get("missing") or [],
        "palette": palette,
        "materials": mats,
        "silhouette": sil,
        "domain_fit": domain_fit(result, look),
        "source_ids": source_ids,
        "missing_source_ids": missing_src,
        "items_without_source": no_src,
        "item_evidence": item_evidence,
        "evidence_tier": look.get("evidence_tier"),
        "period_tiers": look.get("period_tiers") or {},
        "region_tiers": look.get("region_tiers") or {},
        "evidence": evidence,
        "narrative_meaning": look.get("narrative_meaning"),
        "reasons": look.get("reasons") or [],
        "risks": look.get("risks") or [],
        "budget_mode": look.get("budget_mode"),
        "prompt_image": image_prompt,
        "prompt_video": video_prompt,
        "prompt_outfit": english_only(outfit_prompt),
        "movement_note": movement_note if action not in ("", "unknown", None) else "",
        "prompt_negative": ("no costume morphing, no extra layers, no colour shift, "
                            "no invented accessories, no logo/text/watermark"),
    }


def occupation_anchor(ctx, cards):
    """Pick the strongest occupational garment anchor for strict professions."""
    occ = ctx.get("occupation_profile")
    if not occ or occ.get("category") not in recommend.OCCUPATIONAL_STRICT:
        return None
    card_by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    ranked = sorted((occ.get("affinity_ids") or {}).items(),
                    key=lambda pair: (-pair[1], pair[0]))
    for cid, affinity in ranked:
        if affinity < 0.8 or cid not in card_by_id:
            continue
        card = card_by_id[cid]
        if lib.norm_text(card["meta"].get("type")) != "garment":
            continue
        slot = recommend.classify_slot(card)
        if slot not in ("one_piece", "set", "upper_body", "outerwear"):
            continue
        return {"id": cid, "card": card, "slot": slot, "affinity": affinity}
    return None


def inject_occupation_anchor(looks, ctx, cards):
    """Ensure A/B/C alternatives do not lose the professional garment anchor."""
    anchor = occupation_anchor(ctx, cards)
    if not anchor:
        return None, []
    warnings = []
    for look in looks:
        items = look.get("items") or {}
        if any(item and item["id"] == anchor["id"] for item in items.values()):
            continue
        item = recommend.score_item(anchor["card"], anchor["slot"], ctx)
        # Replace a conflicting torso slot rather than stacking a second torso.
        if anchor["slot"] in ("one_piece", "set"):
            for slot in ("one_piece", "set", "upper_body", "lower_body"):
                items.pop(slot, None)
        elif anchor["slot"] == "upper_body":
            items.pop("one_piece", None)
            items.pop("set", None)
            items["upper_body"] = item
            continue
        items[anchor["slot"]] = item
        rebuilt = recommend.score_look(items, ctx, cards,
                                       source_look_id=look.get("source_look_id"),
                                       full=True)
        rebuilt["look_ref"] = look.get("look_ref")
        if look.get("curated_occupation_match"):
            rebuilt["curated_occupation_match"] = True
        look.clear()
        look.update(rebuilt)
        warnings.append("occupation anchor %s enforced in look %s" % (
            anchor["id"], look.get("look_ref")))
    return anchor, warnings


def candidate_context_compatible(candidate, selected, inp):
    """Do not add a culturally/period-specific accessory from another context.

    Legacy recommend intentionally allows cross-region borrowings with warnings;
    the composer's extra accessory/carried slot uses a stricter rule: when both
    the candidate and the already-selected items carry explicit region labels,
    require at least one shared region label.  This avoids e.g. adding a Japanese
    obi to a Shanghai qipao just to complete an accessory slot.
    """
    selected_regions = set()
    selected_periods = set()
    for item in selected:
        selected_regions |= set(lib.norm_text(region)
                                for region in recommend.card_region_labels(item["card"]))
        selected_periods |= set(lib.norm_text(period)
                                for period in recommend.card_period_labels(item["card"]))
    cand_regions = set(lib.norm_text(region)
                       for region in recommend.card_region_labels(candidate["card"]))
    cand_periods = set(lib.norm_text(period)
                       for period in recommend.card_period_labels(candidate["card"]))
    if selected_regions and cand_regions and not (selected_regions & cand_regions):
        return False
    if selected_periods and cand_periods:
        try:
            if not recommend.period_compatible_labels(cand_periods, selected_periods):
                return False
        except Exception:
            if not (selected_periods & cand_periods):
                return False
    return True


def fill_context_slots(looks, pools, ctx, cards, sources):
    """Add accessory/carried_prop from the existing pools when missing.

    Legacy recommend leaves these optional.  The composer explicitly completes
    them with real candidates; no card is invented and no old CLI is changed.
    """
    warnings = []
    for look in looks:
        changed = False
        items = look.get("items") or {}
        selected_ids = {item["id"] for item in items.values() if item}
        for slot in ("accessory", "carried_prop"):
            if items.get(slot):
                continue
            candidates = [item for item in pools.get(slot, [])
                          if item["id"] not in selected_ids
                          and item.get("evidence_status") != "example"
                          and candidate_context_compatible(
                              item, [item for item in items.values() if item],
                              ctx.get("input", {}))]
            if not candidates:
                warnings.append("no %s candidate in the vault for this brief" % slot)
                continue
            current_families = {color_family(color) for item in items.values()
                                if item for color in item_colors(item)}
            current_materials = {material_family(material) for item in items.values()
                                 if item for material in item_materials(item)}

            def key(candidate):
                families = {color_family(color) for color in item_colors(candidate)}
                mats = {material_family(material) for material in item_materials(candidate)}
                clash = 1 if families and families == current_families else 0
                return (-candidate["total"], clash, -len(families & current_families),
                        candidate["id"])

            chosen = min(candidates, key=key)
            items[slot] = chosen
            selected_ids.add(chosen["id"])
            changed = True
        if changed:
            rebuilt = recommend.score_look(items, ctx, cards,
                                           source_look_id=look.get("source_look_id"),
                                           full=True)
            rebuilt["look_ref"] = look.get("look_ref")
            if look.get("curated_occupation_match"):
                rebuilt["curated_occupation_match"] = True
            # Keep composer-selected look identity/selection metadata.
            rebuilt["selection_warning_codes"] = look.get("selection_warning_codes", [])
            look.clear()
            look.update(rebuilt)
    return warnings


def build_continuity(inp, looks):
    raw = inp.get("scenes") or inp.get("continuity_states") or inp.get("states")
    warnings = []
    if isinstance(raw, list) and raw:
        states = []
        for index, scene in enumerate(raw, 1):
            if not isinstance(scene, dict):
                continue
            state = scene.get("state") if isinstance(scene.get("state"), dict) else scene
            states.append({
                "scene": scene.get("scene_id") or scene.get("id") or "S%d" % index,
                "wetness": state.get("wetness", "unknown"),
                "damage": state.get("damage", "unknown"),
                "dirt": state.get("dirt", "unknown"),
                "source": "input",
            })
        if not states:
            warnings.append("continuity states were provided but no valid state could be read")
    else:
        state = inp.get("state") if isinstance(inp.get("state"), dict) else {}
        states = [{
            "scene": "single",
            "wetness": state.get("wetness", "unknown"),
            "damage": state.get("damage", "unknown"),
            "dirt": state.get("dirt", "unknown"),
            "source": "input" if state else "not specified",
        }]
        if not state:
            warnings.append("wetness/damage/dirt not specified; left unknown (not invented)")
    for entry in states:
        for key in ("wetness", "damage", "dirt"):
            if entry.get(key) in (None, ""):
                entry[key] = "unknown"
                warnings.append("%s.%s missing; left unknown" % (entry["scene"], key))
    anchor = []
    if looks:
        sets = [set(look_ids(look)) for look in looks]
        if sets:
            anchor = sorted(set.intersection(*sets)) if len(sets) > 1 else sorted(sets[0])
    return {
        "states": states,
        "anchors": anchor,
        "note": ("States are explicit input facts; unknown values are never replaced "
                 "with invented dry/clean/damage-free assumptions."),
        "warnings": warnings,
    }


def ensure_abc_difference(looks, pools, ctx, cards):
    """Guarantee A/B/C has >=2 changed items across >=2 slots.

    Swapping one shared accessory (or relying on a silhouette label) is not a
    meaningful costume direction.  This routine replaces up to two shared slots
    with real unused candidates and recomputes each look; it never invents IDs.
    """
    def ids(look):
        return {item["id"] for item in look.get("items", {}).values() if item}

    def diff(left, right):
        return len(ids(left).symmetric_difference(ids(right)))

    def slot_diff(left, right):
        left_slots = left.get("items") or {}
        right_slots = right.get("items") or {}
        return sum(1 for slot in set(left_slots) | set(right_slots)
                   if (left_slots.get(slot) or {}).get("id") !=
                   (right_slots.get(slot) or {}).get("id"))

    warnings = []
    for _ in range(4):
        changed = False
        for i, j in ((0, 1), (0, 2), (1, 2)):
            if j >= len(looks):
                continue
            left, target = looks[i], looks[j]
            if diff(left, target) >= 4 and slot_diff(left, target) >= 2:
                continue
            used = ids(left) | ids(target)
            replacements = []
            for slot, current in list((target.get("items") or {}).items()):
                if not current or current["id"] not in ids(left):
                    continue
                compatible = []
                fallback = []
                for candidate in pools.get(slot, []):
                    if candidate["id"] in used or candidate.get("evidence_status") == "example":
                        continue
                    if candidate_context_compatible(candidate, [v for v in target.get("items", {}).values() if v], ctx.get("input", {})):
                        compatible.append(candidate)
                    else:
                        fallback.append(candidate)
                choice = (compatible or fallback)
                if choice:
                    replacements.append((slot, choice[0]))
                if len(replacements) >= 2:
                    break
            if not replacements:
                continue
            for slot, candidate in replacements[:2]:
                target["items"][slot] = candidate
                used.add(candidate["id"])
            rebuilt = recommend.score_look(target["items"], ctx, cards,
                                           source_look_id=target.get("source_look_id"),
                                           full=True)
            rebuilt["look_ref"] = target.get("look_ref")
            if target.get("curated_occupation_match"):
                rebuilt["curated_occupation_match"] = True
            target.clear()
            target.update(rebuilt)
            warnings.append("A/B/C structural repair: %d shared slot(s) replaced in look %s" % (
                min(2, len(replacements)), target.get("look_ref")))
            changed = True
            break
        if not changed:
            break
    for i, j in ((0, 1), (0, 2), (1, 2)):
        if j < len(looks) and (diff(looks[i], looks[j]) < 4 or slot_diff(looks[i], looks[j]) < 2):
            warnings.append("A/B/C could not reach 2 items/2 slots in pair %d/%d (KB candidate gap)" % (i, j))
    return warnings


def _tiers_have_evidence(tiers):
    if not isinstance(tiers, dict) or not tiers:
        return False
    return any(str(tier).lower() not in ("none", "unknown", "")
               for tier in tiers.values())


def _valid_creative_override(value):
    if not isinstance(value, dict):
        return None, "creative_override must be an object"
    intent = str(value.get("intent") or "").strip()
    conflicts = value.get("conflicts")
    if not intent:
        return None, "creative_override.intent is required"
    if not isinstance(conflicts, list) or not conflicts:
        return None, "creative_override.conflicts must be a non-empty list"
    if value.get("historical_accuracy") is not False:
        return None, "creative_override.historical_accuracy must be false"
    return {"intent": intent, "conflicts": conflicts,
            "historical_accuracy": False}, None


def normalise_composer_input(raw):
    inp = recommend.normalise_input(raw)
    for key in ("creative_override", "approved_anchors"):
        if key in raw:
            inp[key] = raw[key]
    return inp


def item_compatibility(look, inp, cards):
    """Declare every item's era/region compatibility, even in inspired mode."""
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    period_wanted = recommend.labels([inp.get("period")])
    region_wanted = recommend.labels([inp.get("region")])
    entries = []
    for slot, cid in (look.get("slot_ids") or {}).items():
        card = by_id.get(cid)
        if not card:
            entries.append({"slot": slot, "id": cid, "status": "unknown_item",
                            "period_ok": False, "region_ok": False})
            continue
        p_labels = recommend.card_period_labels(card)
        r_labels = recommend.card_region_labels(card)
        p_ok = (not p_labels or not period_wanted or
                recommend.period_compatible_labels(period_wanted, p_labels))
        r_ok = (not r_labels or not region_wanted or
                recommend.region_compatible_labels(region_wanted, r_labels))
        tier = (look.get("period_tiers") or {}).get(slot)
        if tier == "none":
            p_ok = False
        status = "compatible"
        if p_labels and period_wanted and not p_ok:
            status = "period_mismatch"
        elif r_labels and region_wanted and not r_ok:
            status = "region_mismatch"
        elif not p_labels or not r_labels:
            status = "unknown"
        entries.append({"slot": slot, "id": cid, "status": status,
                        "period_ok": bool(p_ok), "region_ok": bool(r_ok),
                        "period_labels": sorted(p_labels),
                        "region_labels": sorted(r_labels),
                        "period_tier": tier})
    return entries


def validate_hard_constraints(payload, inp, cards):
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    violations = []
    looks = payload.get("looks") or []
    compatibility = []
    declared_mismatches = []
    for look in looks:
        entries = item_compatibility(look, inp, cards)
        compatibility.extend(entries)
        for entry in entries:
            if entry["status"] in ("period_mismatch", "region_mismatch"):
                declared_mismatches.append({"look": look.get("look_ref"), **entry})
    payload["item_compatibility"] = compatibility
    payload["declared_mismatches"] = declared_mismatches
    strict_occ = recommend.detect_occupation_profile(inp) or {}
    strict_category = strict_occ.get("category")
    approved = [str(value) for value in (inp.get("approved_anchors") or [])
                if str(value)]
    anchor = payload.get("occupation_anchor")
    action = lib.norm_text(inp.get("action"))
    weather = lib.norm_text(inp.get("weather"))
    indoor = recommend.is_indoor_context({"input": inp})
    rain = any(word in weather for word in ("rain", "雨", "wet")) and not indoor
    cold = any(word in weather for word in ("cold", "snow", "storm", "寒", "冬")) and not indoor
    battle = any(word in action for word in ("battle", "fight", "战斗", "打斗"))
    dance = any(word in action for word in ("dance", "舞"))
    if not looks:
        violations.append({"code": "no_looks", "message": "no composed look"})
    for look in looks:
        ref = look.get("look_ref")
        slot_ids = look.get("slot_ids") or {}
        all_ids = [item["id"] for item in look.get("items", [])]
        if len(all_ids) != len(set(all_ids)):
            violations.append({"code": "duplicate_item", "look": ref, "items": all_ids,
                               "message": "same item used in multiple slots"})
        if "one_piece" in slot_ids and ({"upper_body", "lower_body"} & set(slot_ids)):
            violations.append({"code": "torso_conflict", "look": ref,
                               "message": "one_piece combined with upper/lower"})
        if "set" in slot_ids and ({"upper_body", "lower_body", "one_piece"} & set(slot_ids)):
            violations.append({"code": "torso_conflict", "look": ref,
                               "message": "set combined with another torso layer"})
        if not ("one_piece" in slot_ids or "set" in slot_ids or
                ("upper_body" in slot_ids and "lower_body" in slot_ids)):
            violations.append({"code": "missing_torso", "look": ref,
                               "message": "no one_piece/set or top+bottom"})
        if "footwear" not in slot_ids:
            violations.append({"code": "missing_footwear", "look": ref,
                               "message": "no footwear"})
        for item in look.get("items", []):
            cid = item["id"]
            card = by_id.get(cid)
            if not card:
                violations.append({"code": "unknown_item", "look": ref, "items": [cid],
                                   "message": "card ID does not exist"})
            elif item.get("evidence_status") == "example":
                violations.append({"code": "example_item", "look": ref, "items": [cid],
                                   "message": "example card in production look"})
        if rain:
            outer = slot_ids.get("outerwear")
            outer_card = by_id.get(outer) if outer else None
            if not outer_card or not recommend.is_rainwear_card(outer_card):
                violations.append({"code": "rain_without_rainwear", "look": ref,
                                   "items": [outer] if outer else [],
                                   "message": "rain context without rainwear outer"})
        if cold and "outerwear" not in slot_ids:
            violations.append({"code": "cold_without_outer", "look": ref,
                               "message": "cold/storm context without outerwear"})
        footwear = slot_ids.get("footwear")
        shoe = by_id.get(footwear) if footwear else None
        if shoe and (battle or dance) and inp.get("fidelity_mode") == "historical":
            if recommend.is_heels(shoe) or recommend.is_open_footwear(shoe):
                violations.append({"code": "unsafe_action_footwear", "look": ref,
                                   "items": [footwear],
                                   "message": "heeled/open footwear in action context"})
        if strict_category in recommend.OCCUPATIONAL_STRICT:
            required = [anchor] if anchor else approved
            if required and not any(cid in all_ids for cid in required):
                violations.append({"code": "missing_approved_anchor", "look": ref,
                                   "items": required,
                                   "message": "strict profession/approved anchor missing"})
        for cid in approved:
            if cid not in all_ids:
                violations.append({"code": "missing_approved_anchor", "look": ref,
                                   "items": [cid],
                                   "message": "approved anchor %s missing" % cid})
        if inp.get("fidelity_mode") == "historical":
            if not _tiers_have_evidence(look.get("period_tiers")):
                violations.append({"code": "historical_period_unverified", "look": ref,
                                   "message": "no period evidence tier in historical mode"})
            if not _tiers_have_evidence(look.get("region_tiers")):
                violations.append({"code": "historical_region_unverified", "look": ref,
                                   "message": "no region evidence tier in historical mode"})
    return violations


def composer_payload(inp, cards, sources):
    result = recommend.make_result(inp, cards, sources)
    ctx = result.get("context") or {}
    ctx["sources"] = sources
    pools = recommend.build_pools(cards, ctx)
    anchor, anchor_warnings = inject_occupation_anchor(
        result.get("looks", []), ctx, cards)
    fill_warnings = fill_context_slots(result.get("looks", []), pools, ctx, cards, sources)
    abc_fix_warnings = ensure_abc_difference(result.get("looks", []), pools, ctx, cards)
    looks = result.get("looks", [])
    composer_looks = [composer_look(look, result, cards, sources, ctx) for look in looks]
    abc = {}
    if len(composer_looks) >= 2:
        for i, j, label in ((0, 1, "a_b"), (0, 2, "a_c"), (1, 2, "b_c")):
            if j < len(composer_looks):
                abc[label] = {
                    "item_diff": difference_count(looks[i], looks[j]),
                    "palette_diff": len(set(composer_looks[i]["palette"]["colors"]) ^
                                        set(composer_looks[j]["palette"]["colors"])),
                    "silhouette": [composer_looks[i]["silhouette"]["shape"],
                                   composer_looks[j]["silhouette"]["shape"]],
                }
    abc["all_pairwise_ge_2"] = (
        len(composer_looks) >= 3 and
        all(value["item_diff"] >= 2 for value in abc.values()
            if isinstance(value, dict) and "item_diff" in value))
    warnings = list(result.get("warnings") or [])
    warnings.extend(anchor_warnings)
    warnings.extend(fill_warnings)
    warnings.extend(abc_fix_warnings)
    for entry in abc.values():
        if isinstance(entry, dict) and entry.get("item_diff", 0) < 2:
            warnings.append("A/B/C structural difference below 2 items in one pair")
    completeness = {
        "all_have_torso": all(
            ("one_piece" in look["items"] or "set" in look["items"] or
             ("upper_body" in look["items"] and "lower_body" in look["items"]))
            for look in looks) if looks else False,
        "all_have_footwear": all("footwear" in look["items"] for look in looks) if looks else False,
        "all_have_outerwear": all("outerwear" in look["items"] for look in looks) if looks else False,
        "all_have_accessory": all("accessory" in look["items"] for look in looks) if looks else False,
        "all_have_carried_prop": all("carried_prop" in look["items"] for look in looks) if looks else False,
    }
    if looks and not completeness["all_have_torso"]:
        warnings.append("a composed look lacks torso coverage (one-piece or top+bottom)")
    if looks and not completeness["all_have_footwear"]:
        warnings.append("a composed look lacks footwear (knowledge-base gap)")
    if looks and not completeness["all_have_accessory"]:
        warnings.append("a composed look lacks accessory (knowledge-base gap)")
    if looks and not completeness["all_have_carried_prop"]:
        warnings.append("a composed look lacks carried prop (knowledge-base gap)")
    continuity = build_continuity(inp, looks)
    warnings.extend(continuity["warnings"])
    all_source_ids = []
    for look in composer_looks:
        all_source_ids.extend(look["source_ids"])
        if look["missing_source_ids"]:
            warnings.append("missing source cards: " + ", ".join(look["missing_source_ids"]))
        if look["items_without_source"]:
            warnings.append("items without source_ids: " + ", ".join(look["items_without_source"]))
        if look["evidence_tier"] in (None, "unknown"):
            warnings.append("look %s has no reliable evidence tier" % look["look_ref"])
    payload = {
        "composer": "P4-3 outfit-composer",
        "input": result.get("input"),
        "occupation_anchor": anchor["id"] if anchor else None,
        "looks": composer_looks,
        "abc_metrics": abc,
        "completeness": completeness,
        "continuity": continuity,
        "evidence": {
            "source_ids": lib.unique_ordered(all_source_ids),
            "missing_source_ids": [sid for sid in lib.unique_ordered(all_source_ids)
                                   if sid not in sources],
            "source_urls": [{"source_id": sid, "url": url}
                            for sid, url in lib.source_urls(
                                lib.unique_ordered(all_source_ids), sources)],
        },
        "warnings": lib.unique_ordered(warnings),
        "warnings_detail": result.get("warnings_detail") or [],
        "checks": {
            "exit_ok": bool(looks),
            "three_looks": len(looks) == 3,
            "abc_pairwise_ge_2": abc.get("all_pairwise_ge_2", False),
            "ids_all_exist": result.get("checks", {}).get("ids_all_exist"),
            "source_ids_resolve": not [sid for sid in lib.unique_ordered(all_source_ids)
                                       if sid not in sources],
            "real_ids_only": result.get("checks", {}).get("ids_all_exist"),
            "continuity_states_explicit": all(
                state["source"] == "input" for state in continuity["states"]),
        },
    }
    violations = validate_hard_constraints(payload, inp, cards)
    declared = payload.get("declared_mismatches") or []
    override, override_error = _valid_creative_override(inp.get("creative_override"))
    payload["constraint_violations"] = violations
    if violations:
        payload["checks"]["hard_constraints_passed"] = False
        if override is None:
            payload["status"] = "blocked"
            payload["blocked_looks"] = payload["looks"]
            payload["looks"] = []
            payload["warnings"].append("blocked by post-composition hard constraints")
            if override_error:
                payload["warnings"].append("creative_override invalid: " + override_error)
        else:
            payload["status"] = "override"
            payload["creative_override"] = override
            payload["historical_accuracy"] = False
            payload["warnings"].append("creative_override: design shown as override, not historical accuracy")
    elif declared:
        payload["checks"]["hard_constraints_passed"] = False
        if override is None:
            # Complete looks with only declared per-item mismatches are shown as
            # declared_mismatch (never as ok / historical accuracy); hard
            # violations/missing layers still take the blocked branch above.
            payload["status"] = "declared_mismatch"
            payload["warnings"].append(
                "design includes declared per-item era/region mismatches; "
                "not a historical-accuracy claim")
        else:
            payload["status"] = "override"
            payload["creative_override"] = override
            payload["historical_accuracy"] = False
            payload["warnings"].append("creative_override: design shown as override, not historical accuracy")
    else:
        payload["checks"]["hard_constraints_passed"] = True
        payload["status"] = "ok"
    payload["historical_accuracy"] = bool(
        inp.get("fidelity_mode") == "historical" and not violations and
        not declared and payload["status"] == "ok")
    return payload


def render_markdown(payload):
    lines = ["# Outfit Composer — %s" % (payload.get("input", {}).get("character", {}).get("name", "character")), "",
             "- Composer: %s" % payload["composer"],
             "- A/B/C pairwise ≥2 item diff: %s" % payload["checks"]["abc_pairwise_ge_2"]]
    for look in payload["looks"]:
        lines.extend(["", "## Look %s — score %s" % (look["look_ref"], look["total"]),
                      "", "| Slot | ID | Name | Colors | Materials | Evidence | Sources |",
                      "| --- | --- | --- | --- | --- | --- | --- |"])
        for item in look["items"]:
            lines.append("| %s | `%s` | %s | %s | %s | %s | %s |" % (
                SLOT_LABELS.get(item["slot"], item["slot"]), item["id"],
                item.get("name_zh") or item.get("name_en"),
                ", ".join(item["colors"]), ", ".join(item["materials"]),
                item["evidence_status"], ", ".join(item["source_ids"]) or "—"))
        lines.extend(["", "- Palette: %s (harmony %.2f, dominant %s %.0f%%)" % (
            ", ".join(look["palette"]["colors"]), look["palette"]["harmony"],
            look["palette"]["dominant_family"],
            look["palette"]["dominant_share"] * 100),
            "- Materials: %s (harmony %.2f)" % (
                ", ".join(look["materials"]["materials"]), look["materials"]["harmony"]),
            "- Silhouette: %s (proportion %.2f)" % (
                look["silhouette"]["shape"], look["silhouette"]["proportion"]),
            "- Prompt (image):", "```", look["prompt_image"], "```",
            "- Prompt (video):", "```", look["prompt_video"], "```"])
    lines.extend(["", "## A/B/C metrics", "", "```json",
                  json.dumps(payload["abc_metrics"], ensure_ascii=False, indent=2),
                  "```", "", "## Continuity", "", "```json",
                  json.dumps(payload["continuity"], ensure_ascii=False, indent=2),
                  "```", "", "## Warnings", ""])
    for warning in payload["warnings"]:
        lines.append("- %s" % warning)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="P4 full-slot outfit composer")
    parser.add_argument("--input", help="input JSON path")
    parser.add_argument("--brief", help="free-text character/scene brief")
    parser.add_argument("--brief-file", help="read brief from file")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--out", help="write output to file")
    parser.add_argument("--md", action="store_true", help="emit Markdown")
    args = parser.parse_args(argv)
    raw = {}
    if args.input:
        try:
            raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
        except FileNotFoundError:
            print("ERROR: input file not found: %s" % args.input, file=sys.stderr)
            return 2
        except json.JSONDecodeError as exc:
            print("ERROR: invalid JSON: %s" % exc, file=sys.stderr)
            return 2
        if not isinstance(raw, dict):
            print("ERROR: input JSON must be an object", file=sys.stderr)
            return 2
    brief = args.brief or ""
    if args.brief_file:
        try:
            brief = Path(args.brief_file).read_text(encoding="utf-8").strip()
        except OSError as exc:
            print("ERROR: cannot read brief file: %s" % exc, file=sys.stderr)
            return 2
    if brief:
        raw = dict(raw)
        raw.setdefault("brief", brief)
    if not raw:
        print("ERROR: provide --input or --brief/--brief-file", file=sys.stderr)
        return 2
    try:
        inp = normalise_composer_input(raw)
    except ValueError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    cards, errors = lib.load_cards()
    for error in errors:
        print("WARN card parse: %s: %s" % (error["path"], error["error"]), file=sys.stderr)
    sources = lib.load_sources(cards=cards)
    payload = composer_payload(inp, cards, sources)
    text = json.dumps(payload, ensure_ascii=False, indent=2) if args.json else render_markdown(payload)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print("wrote %s" % args.out)
    else:
        print(text)
    if payload.get("status") in ("blocked", "declared_mismatch"):
        print("BLOCKED: hard constraints or insufficient composition; see constraint_violations "
              "(status=blocked, no approved looks).", file=sys.stderr)
        return 0
    if not payload["looks"]:
        print("FAIL: no complete outfit candidates", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
