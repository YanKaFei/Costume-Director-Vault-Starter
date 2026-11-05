#!/usr/bin/env python3
"""Typed, evidence-labelled visual prompt builder (R1.3-D).

Reads one real card (YAML + body + source_ids + optional visual_assets),
emits modular JSON/Markdown prompts by kind:
  material_macro, component_detail, garment_flat, garment_worn,
  accessory, style, outfit.

Every module carries evidence tags:
  FACT        - explicit structured/verified card fields
  OBSERVATION - card body visual/lighting/movement description
  INFERENCE   - interpretive combination/design reading
  CREATIVE    - requested staging/art-direction choice

No image is generated. Output explicitly records `image_generation: false` and
`delivery: text prompt only`.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
KINDS = ["material_macro", "component_detail", "garment_flat", "garment_worn",
         "accessory", "style", "outfit"]
RECORD = ROOT / "11-验收/R1.3/PROMPT-LOG.jsonl"


def load_card(card_id):
    for path in sorted(ROOT.glob("0[1-9]-*/**/*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        if not m:
            continue
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        if str(meta.get("id")) == card_id:
            return {"id": card_id, "path": str(path.relative_to(ROOT)),
                    "meta": meta, "body": m.group(2)}
    return None


def section(body, title):
    m = re.search(r"## %s\n(.*?)(?=\n## |\Z)" % re.escape(title), body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def values(meta, key):
    v = meta.get(key) or []
    return [str(x) for x in v] if isinstance(v, list) else [str(v)]


def conflicts(card, kind, period=None, region=None):
    meta = card["meta"]
    out = []
    if not values(meta, "materials") and kind in ("material_macro", "garment_flat",
                                                  "garment_worn", "accessory", "outfit"):
        out.append({"code": "missing_material", "severity": "warning",
                    "detail": "no materials field on card"})
    if kind == "component_detail" and not section(card["body"], "结构要点"):
        out.append({"code": "missing_structure", "severity": "warning",
                    "detail": "card has no 结构要点 section"})
    if not values(meta, "source_ids"):
        out.append({"code": "missing_source", "severity": "warning",
                    "detail": "no source_ids; visual claims are not sourced"})
    if str(meta.get("evidence_status")) != "verified":
        out.append({"code": "low_confidence", "severity": "notice",
                    "detail": "evidence_status=%s; not verified" % meta.get("evidence_status")})
    if period and values(meta, "periods"):
        wanted = period.lower().replace(" ", "_")
        have = [p.lower().replace(" ", "_") for p in values(meta, "periods")]
        if not any(wanted == h or wanted in h or h in wanted for h in have):
            out.append({"code": "period_conflict", "severity": "error",
                        "detail": "requested %s vs card periods %s" % (period, have)})
    if region and values(meta, "regions"):
        wanted = region.lower().replace(" ", "_")
        have = [r.lower().replace(" ", "_") for r in values(meta, "regions")]
        if not any(wanted == h or wanted in h or h in wanted for h in have):
            out.append({"code": "region_conflict", "severity": "error",
                        "detail": "requested %s vs card regions %s" % (region, have)})
    if kind == "outfit" and str(meta.get("type")) != "look":
        out.append({"code": "kind_type_mismatch", "severity": "error",
                    "detail": "outfit kind expects a LOOK card"})
    if kind == "style" and str(meta.get("type")) not in ("style", "look"):
        out.append({"code": "kind_type_mismatch", "severity": "error",
                    "detail": "style kind expects STY/LOOK"})
    return out


def evidence_tags(card, kind):
    meta = card["meta"]
    tags = []
    if meta.get("evidence_status") == "verified" and meta.get("source_ids"):
        tags.append("FACT")
    if section(card["body"], "视觉辨识") or meta.get("lighting_notes") or meta.get("movement_notes"):
        tags.append("OBSERVATION")
    if meta.get("evidence_status") in ("interpretive", "example", "unverified") or meta.get("prompt_en"):
        tags.append("INFERENCE")
    tags.append("CREATIVE")
    return tags


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
WIKILINK_RE = re.compile(r"\[\[[^\]]*\]\]")
MARKDOWN_RE = re.compile(r"[*_#`>|]")


def safe_english(value, max_words=36):
    """Copy-ready English: no CJK, wikilinks, markdown or truncated mid-token."""
    text = str(value or "")
    text = WIKILINK_RE.sub(" ", text)
    text = MARKDOWN_RE.sub(" ", text)
    if CJK_RE.search(text):
        text = CJK_RE.sub(" ", text)
    words = text.split()
    words = [w.strip(".,;:()[]{}") for w in words if w.strip(".,;:()[]{}")]
    words = [w for w in words if w and not CJK_RE.search(w)]
    return " ".join(words[:max_words]).strip()


def safe_chinese(value):
    text = WIKILINK_RE.sub(" ", str(value or ""))
    text = MARKDOWN_RE.sub(" ", text)
    return " ".join(text.split()).strip()


def field_en(meta, key, max_words=18):
    vals = values(meta, key)
    return safe_english(", ".join(vals), max_words)


def modules(card, kind, lang):
    meta = card["meta"]
    typ = str(meta.get("type"))
    name_en = safe_english(meta.get("name_en") or card["id"], 12)
    if not name_en:
        name_en = card["id"]
    name_zh = safe_chinese(meta.get("name_zh") or name_en)
    category = safe_english(meta.get("category"), 4)
    subcategory = safe_english(meta.get("subcategory"), 4)
    silhouette = safe_english(meta.get("silhouette"), 4) or "unspecified"
    fit = safe_english(meta.get("fit"), 4) or "unspecified"
    colors = field_en(meta, "colors", 16) or "unspecified"
    materials = field_en(meta, "materials", 16) or "unspecified"
    periods = field_en(meta, "periods", 10)
    regions = field_en(meta, "regions", 10)
    source_prompt = safe_english(meta.get("prompt_en"), 60)
    negative = safe_english(meta.get("negative_prompt_en"), 32)
    lighting = safe_english(meta.get("lighting_notes"), 16)
    movement = safe_english(meta.get("movement_notes"), 16)
    base_fact = ("Card %s (%s): %s; category %s/%s; silhouette %s; fit %s; "
                 "materials %s; palette %s." % (
                     card["id"], typ, name_en, category or "unspecified",
                     subcategory or "unspecified", silhouette, fit, materials, colors))
    mods = []
    def add(name, en, zh, tags, source):
        en = safe_english(en, 72)
        if en:
            mods.append({"module": name, "prompt_en": en,
                         "prompt_zh": safe_chinese(zh),
                         "evidence": tags, "source": source})
    if kind == "material_macro":
        add("material_surface",
            "extreme macro of %s, %s; focus on fiber, weave, sheen and surface irregularity; "
            "neutral 5600K light, shallow depth of field, no logos" % (materials, name_en),
            "材质微距：%s，%s；聚焦纤维、织法、光泽与表面不均；中性 5600K 光、浅景深、无标识" % (materials, name_zh),
            ["FACT", "OBSERVATION"], "materials/colors + lighting_notes")
        if lighting:
            add("surface_observation", "lighting observation: " + lighting,
                "光照观察：" + safe_chinese(meta.get("lighting_notes")),
                ["OBSERVATION"], "lighting_notes")
    elif kind == "component_detail":
        add("structure_detail",
            "detail of %s on %s; construction seams, closures, edge finish and hardware; "
            "orthographic clarity, no stylisation" % (name_en, typ),
            "结构细节：%s；缝线、闭合、边缘处理与五金；正交清晰、不风格化" % name_zh,
            ["FACT", "OBSERVATION"], "card type + structured fields")
        if source_prompt:
            add("construction_note", "construction note from card prompt: " + source_prompt,
                "卡片结构提示：" + safe_chinese(meta.get("prompt_en")),
                ["INFERENCE"], "prompt_en")
    elif kind in ("garment_flat", "garment_worn"):
        pose = ("flat lay on neutral background, front and back, true scale, no model"
                if kind == "garment_flat" else
                "full-body neutral model, front side and back, natural stance, face out of frame, no identity")
        en = "%s, %s; silhouette %s; fit %s; category %s/%s; materials %s; palette %s" % (
            name_en, pose, silhouette, fit, category or "unspecified",
            subcategory or "unspecified", materials, colors)
        if source_prompt:
            en += "; reference prompt: " + source_prompt
        add(kind, en,
            "%s：%s；廓形 %s；合体度 %s；类别 %s/%s；材质 %s；色彩 %s%s" % (
                name_zh, pose, silhouette, fit, category or "未指定",
                subcategory or "未指定", materials, colors,
                ("；参考提示：" + safe_chinese(meta.get("prompt_en"))) if source_prompt else ""),
            ["FACT", "OBSERVATION", "INFERENCE"], "YAML + English prompt_en")
        if movement:
            add("movement_note", "movement observation: " + movement,
                "动作观察：" + safe_chinese(meta.get("movement_notes")),
                ["OBSERVATION"], "movement_notes")
    elif kind == "accessory":
        add("accessory_hero",
            "isolated hero product shot of %s; accessory scale; materials %s; palette %s; "
            "neutral background, true colour, no model" % (name_en, materials, colors),
            "配饰单品图：%s；配饰比例；材质 %s；色彩 %s；中性背景、真实色、无模特" % (
                name_zh, materials, colors),
            ["FACT", "OBSERVATION"], "YAML + card type")
    elif kind == "style":
        en = ("design language board for %s; palette %s; materials %s; period %s; "
              "region %s; no single historical fact claimed" % (
                  name_en, colors, materials, periods or "unspecified",
                  regions or "unspecified"))
        if source_prompt:
            en += "; reference design prompt: " + source_prompt
        add("style_language", en,
            "风格语言板：%s；色彩 %s；材质 %s；年代 %s；地域 %s；不声称单一史实%s" % (
                name_zh, colors, materials, periods or "未指定",
                regions or "未指定",
                ("；参考设计提示：" + safe_chinese(meta.get("prompt_en"))) if source_prompt else ""),
            ["OBSERVATION", "INFERENCE", "CREATIVE"], "style card fields")
    elif kind == "outfit":
        items = [str(x) for x in (meta.get("look_items") or [])]
        en = "complete outfit %s; items %s; palette %s" % (
            name_en, ", ".join(items), colors)
        if source_prompt:
            en += "; reference prompt: " + source_prompt
        add("outfit_hero", en,
            "完整造型：%s；单品 %s；色彩 %s%s" % (
                name_zh, ", ".join(items), colors,
                ("；参考提示：" + safe_chinese(meta.get("prompt_en"))) if source_prompt else ""),
            ["FACT", "OBSERVATION", "INFERENCE", "CREATIVE"], "LOOK look_items + prompt_en")
        continuity_en = safe_english(meta.get("continuity_lock"), 0)
        add("continuity",
            "continuity locks: " + (continuity_en or "recorded in card; preserve slot state"),
            "连续性锁定：%s" % (safe_chinese(meta.get("continuity_lock")) or "见卡片；保持槽位状态"),
            ["FACT"], "continuity_lock")
        if negative:
            add("negative", "negative: " + negative,
                "负向：" + safe_chinese(meta.get("negative_prompt_en")),
                ["CREATIVE"], "negative_prompt_en")
    return {"base_fact": base_fact if "FACT" in evidence_tags(card, kind) else None,
            "modules": mods,
            "observation": safe_english(meta.get("prompt_en"), 40) or "structured card metadata only",
            "inference": safe_english(meta.get("prompt_en"), 40) or "design reading from structured fields",
            "creative": "staging and art-direction choices; not a historical claim"}


def build(card_id, kind, lang="en", period=None, region=None):
    card = load_card(card_id)
    if card is None:
        return {"error": "card not found", "id": card_id}
    mods = modules(card, kind, lang)
    cf = conflicts(card, kind, period, region)
    result = {
        "card_id": card_id, "card_path": card["path"],
        "kind": kind, "lang": lang, "model_agnostic": True,
        "image_generation": False, "delivery": "text prompt only",
        "evidence_status": card["meta"].get("evidence_status"),
        "source_ids": values(card["meta"], "source_ids"),
        "evidence_tags": evidence_tags(card, kind),
        "modules": mods["modules"], "observation": mods["observation"],
        "inference": mods["inference"], "creative": mods["creative"],
        "conflicts": cf,
        "conflict_summary": {"errors": sum(1 for c in cf if c["severity"] == "error"),
                             "warnings": sum(1 for c in cf if c["severity"] == "warning"),
                             "notices": sum(1 for c in cf if c["severity"] == "notice")},
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    return result


def markdown(result):
    if "error" in result:
        return "# error\n\n" + result["error"]
    lines = ["# Visual prompt: %s (%s)" % (result["card_id"], result["kind"]),
             "", "- Card: `%s`" % result["card_path"],
             "- Evidence status: %s" % result["evidence_status"],
             "- Sources: %s" % ", ".join(result["source_ids"]),
             "- Evidence tags: %s" % ", ".join(result["evidence_tags"]),
             "- Image generation: **false** (text prompt only)", ""]
    for m in result["modules"]:
        lines += ["## %s" % m["module"], "*Evidence:* %s" % ", ".join(m["evidence"]),
                  "", "**EN**", m["prompt_en"], "", "**ZH**", m["prompt_zh"], ""]
    lines += ["## Conflicts", "```json", json.dumps(result["conflicts"], ensure_ascii=False, indent=2),
              "```", "", "## Facts / observation / inference",
              "- FACT: %s" % (result["modules"] and result["modules"][0]["prompt_en"] if
                               "FACT" in result["evidence_tags"] else "none"),
              "- OBSERVATION: %s" % (result["observation"] or "none"),
              "- INFERENCE: %s" % (result["inference"] or "none"),
              "- CREATIVE: %s" % result["creative"]]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True)
    p.add_argument("--kind", choices=KINDS, default="garment_worn")
    p.add_argument("--lang", choices=["en", "zh", "both"], default="en")
    p.add_argument("--model-agnostic", action="store_true", default=True)
    p.add_argument("--period", default="")
    p.add_argument("--region", default="")
    p.add_argument("--json", action="store_true")
    p.add_argument("--markdown", action="store_true")
    p.add_argument("--out", default="")
    p.add_argument("--record", action="store_true")
    args = p.parse_args(argv)
    result = build(args.id, args.kind, args.lang, args.period, args.region)
    text = json.dumps(result, ensure_ascii=False, indent=2) if args.json or not args.markdown else markdown(result)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    if args.record and "error" not in result:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        record = {"generated_at": result["generated_at"], "card_id": result["card_id"],
                  "kind": result["kind"], "lang": result["lang"],
                  "evidence_tags": result["evidence_tags"],
                  "conflicts": len(result["conflicts"]),
                  "image_generation": False, "delivery": result["delivery"]}
        with RECORD.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return 0 if "error" not in result else 2


if __name__ == "__main__":
    sys.exit(main())
