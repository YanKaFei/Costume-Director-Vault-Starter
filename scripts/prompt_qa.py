#!/usr/bin/env python3
"""R1.3B Batch2 prompt QA.

Checks all card visual-prompt blocks (`## 生图提示词` / `## 视频提示词`) for:
term accuracy (name_en/part_family, no CJK/bad links/typos), structural location,
material evidence, view consistency, conflicting attributes, cross-card prompt
homogeneity, and semantic consistency with the card's prompt_en.

Statuses:
  TEXT_VALID               text checks run and no error
  DOMAIN_REVIEWED          NOT_RUN (requires human domain review)
  IMAGE_TESTED             NOT_RUN (no image generation/test available)
  HUMAN_VISUAL_APPROVED    NOT_RUN (requires human visual approval)

No card edits; QA output only. Unknown physical properties are never guessed: a
prompt that asserts material/structure while the card has no evidence is flagged.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "11-验收/R1.3B"
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
WIKI = re.compile(r"\[\[[^\]]*\]\]")
BLOCK = re.compile(r"## (生图提示词|视频提示词)\s*\n(.*?)(?=\n## |\Z)", re.S)
TEXT_BLOCK = re.compile(r"```(?:text)?\s*\n(.*?)```", re.S)
VIEW_WORDS = {"full-body": ["full-body", "full body"], "macro": ["macro", "extreme close"],
              "detail": ["detail", "close-up", "close up"], "flat": ["flat lay", "flat-lay"]}


def split_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else (None, None)


def load_cards():
    cards = []
    for path in sorted(ROOT.glob("0[1-9]-*/**/*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)
        if fm is None:
            continue
        try:
            meta = yaml.safe_load(fm) or {}
        except yaml.YAMLError:
            continue
        if meta.get("id"):
            cards.append({"id": str(meta["id"]), "path": path, "meta": meta,
                          "body": body or "", "text": text})
    return cards


def prompt_blocks(card):
    """Return every fenced prompt block, including ### detail/applied/product sub-blocks.

    Earlier versions joined all fenced blocks under a ## heading into one prompt,
    which under-counted structure/garment sub-prompts by 36 (143 vs 179).
    """
    blocks = []
    for match in BLOCK.finditer(card["body"]):
        kind = "image" if match.group(1) == "生图提示词" else "video"
        section = match.group(2)
        # Find each code fence and the nearest preceding ### subtype heading.
        for text_match in TEXT_BLOCK.finditer(section):
            prefix = section[:text_match.start()]
            subheads = re.findall(r"(?m)^###\s+(.+?)\s*$", prefix)
            subtype = subheads[-1].strip() if subheads else ""
            prompt = text_match.group(1).strip()
            if prompt:
                blocks.append({"kind": kind, "subtype": subtype,
                               "location": "## %s%s" % (
                                   match.group(1),
                                   (" / ### " + subtype) if subtype else ""),
                               "prompt": prompt})
    return blocks


def tokens(text):
    return set(re.findall(r"[a-z][a-z0-9_-]{2,}", text.lower()))


TEMPLATE_STOP = set("subject fact observation creative structure material color light "
                    "camera background style negative consistency full body adult figure "
                    "garment part card props object frame image shot prompt no not from "
                    "with and the for a of in on to is are as at or by be this that these "
                    "those preserve across frames soft directional neutral studio".split())


def content_tokens(text):
    return tokens(text) - TEMPLATE_STOP


def values(meta, key):
    v = meta.get(key) or []
    return [str(x).lower() for x in v] if isinstance(v, list) else [str(v).lower()]


def check_prompt(card, block):
    meta, prompt = card["meta"], block["prompt"]
    errors, warnings = [], []
    name_en = str(meta.get("name_en") or "")
    part_family = str(meta.get("part_family") or "")
    materials = values(meta, "materials")
    if CJK.search(prompt):
        errors.append("prompt_en contains CJK")
    if "[[" in prompt or "]]" in prompt:
        errors.append("prompt contains wikilink markup")
    for typo in ("silhhouette", "may_have_par"):
        if typo in prompt:
            errors.append("typo: %s" % typo)
    if name_en and name_en.lower() not in prompt.lower() and card["id"] not in prompt:
        warnings.append("card name/id not clearly named in prompt")
    if card["id"] not in prompt:
        warnings.append("card ID missing from prompt")
    prompt_tokens = tokens(prompt)
    material_line = ""
    for line in prompt.splitlines():
        if line.upper().startswith("MATERIAL"):
            material_line = line
            break
    if materials:
        if not any(m in material_line.lower() or m in prompt.lower()
                   for m in materials if m not in ("unknown", "")):
            warnings.append("materials not represented in prompt")
    else:
        material_hypothesis = ("INFERENCE" in material_line.upper() or
                               "HYPOTHESIS" in prompt.upper() or
                               "UNKNOWN" in prompt.upper() or
                               "NOT MATERIAL FACT" in prompt.upper())
        if (not material_hypothesis and
                re.search(r"(silk|wool|leather|cotton|linen|lace|satin|velvet|denim|nylon)",
                          prompt, re.I)):
            errors.append("prompt asserts material while card has no materials field")
    if card["meta"].get("type") in ("garment", "garment_part"):
        if "STRUCTURE" not in prompt.upper():
            warnings.append("missing STRUCTURE block")
        if part_family and part_family.lower() not in prompt.lower():
            warnings.append("part_family not represented")
    views = [name for name, words in VIEW_WORDS.items()
             if any(w in prompt.lower() for w in words)]
    if not views:
        warnings.append("no explicit view/camera framing (full-body/macro/detail/flat)")
    if len(set(views)) > 1:
        warnings.append("multiple view classes: " + ",".join(sorted(set(views))))
    # conflicting attributes (conservative phrase pairs)
    pairs = [("matte", "glossy"), ("fitted", "oversized"), ("front", "back"),
             ("long-sleeve", "sleeveless"), ("high-waist", "low-waist")]
    for a, b in pairs:
        if a in prompt.lower() and b in prompt.lower():
            warnings.append("potential conflicting attributes: %s vs %s" % (a, b))
    # semantic consistency with card prompt_en
    semantic = 0.0
    card_prompt = str(meta.get("prompt_en") or "")
    if card_prompt:
        semantic = round(SequenceMatcher(None, sorted(prompt_tokens),
                                          sorted(tokens(card_prompt))).ratio(), 3)
        if semantic < 0.10:
            warnings.append("low semantic overlap with card prompt_en (%.2f)" % semantic)
    return {"errors": errors, "warnings": warnings, "views": views,
            "semantic": semantic, "materials": materials,
            "part_family": part_family}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--out-csv", default=str(OUT / "PROMPT-QA.csv"))
    p.add_argument("--out-md", default=str(OUT / "PROMPT-QA.md"))
    p.add_argument("--json", action="store_true")
    p.add_argument("--baseline-179", action="store_true",
                   help="audit the 179-block Batch2 baseline; exclude the 13 "
                        "cards whose 26 base blocks were added in Batch3")
    args = p.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)
    cards = load_cards()
    batch3_cards = {f"STY-{i:04d}" for i in range(1, 12)} | {
        "LOOK-0004", "LOOK-0024", "STY-0024", "STY-0025"}
    if args.baseline_179:
        cards = [c for c in cards if c["id"] not in batch3_cards]
    rows = []
    prompt_map = {}
    pid = 0
    for card in cards:
        blocks = prompt_blocks(card)
        if not blocks:
            continue
        for block in blocks:
            pid += 1
            checks = check_prompt(card, block)
            text_valid = not checks["errors"]
            prompt_hash = hashlib.sha256(block["prompt"].encode("utf-8")).hexdigest()[:16]
            row = {"card_id": card["id"],
                   "prompt_id": "PID-%04d" % pid,
                   "type": block["kind"],
                   "subtype": block["subtype"] or "base",
                   "location": block["location"],
                   "hash": prompt_hash,
                   "status": "TEXT_VALID" if text_valid else "TEXT_INVALID",
                   "evidence": "FACT/OBSERVATION/INFERENCE/CREATIVE",
                   "path": str(card["path"].relative_to(ROOT)),
                   "prompt_kind": block["kind"], "chars": len(block["prompt"]),
                   "text_status": "TEXT_VALID" if text_valid else "TEXT_INVALID",
                   "domain_reviewed": "NOT_RUN", "image_tested": "NOT_RUN",
                   "human_visual_approved": "NOT_RUN",
                   "errors": "; ".join(checks["errors"]),
                   "warnings": "; ".join(checks["warnings"]),
                   "views": ",".join(checks["views"]),
                   "semantic": checks["semantic"]}
            rows.append(row)
            prompt_map.setdefault(block["kind"], []).append((card["id"], block["prompt"]))
    # cross-card homogeneity (same kind)
    homogeneity = []
    template_pairs = 0
    for kind, items in prompt_map.items():
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i][1], items[j][1]
                ta, tb = content_tokens(a), content_tokens(b)
                if ta and tb:
                    jaccard = len(ta & tb) / float(len(ta | tb))
                else:
                    jaccard = 0.0
                raw = SequenceMatcher(None, sorted(tokens(a)), sorted(tokens(b))).ratio()
                if raw >= 0.82:
                    template_pairs += 1
                if jaccard >= 0.80:
                    homogeneity.append({"prompt_kind": kind, "card_a": items[i][0],
                                        "card_b": items[j][0],
                                        "content_jaccard": round(jaccard, 3)})
    with Path(args.out_csv).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    errors = [r for r in rows if r["text_status"] == "TEXT_INVALID"]
    warnings = [r for r in rows if r["warnings"]]
    summary = {"prompts": len(rows), "cards": len({r["card_id"] for r in rows}),
               "text_valid": sum(1 for r in rows if r["text_status"] == "TEXT_VALID"),
               "text_invalid": len(errors), "warnings": len(warnings),
               "errors": sum(1 for r in rows for _ in (r["errors"].split(";") if r["errors"] else [])),
               "subtype_counts": {t: sum(1 for r in rows if r["subtype"] == t)
                                  for t in sorted({r["subtype"] for r in rows})},
               "type_counts": {t: sum(1 for r in rows if r["type"] == t)
                               for t in sorted({r["type"] for r in rows})},
               "homogeneity_pairs": len(homogeneity),
               "template_scaffold_pairs": template_pairs,
               "homogeneity_threshold": "content-token Jaccard >= 0.80 after removing template vocabulary",
               "homogeneity": homogeneity,
               "statuses": {"TEXT_VALID": sum(1 for r in rows if r["text_status"] == "TEXT_VALID"),
                            "DOMAIN_REVIEWED": "NOT_RUN",
                            "IMAGE_TESTED": "NOT_RUN",
                            "HUMAN_VISUAL_APPROVED": "NOT_RUN"},
               "unknown_policy": "unknown material/structure is not guessed; asserted material without card evidence = error",
               "image_generation": False}
    lines = ["# R1.3B Batch2 Prompt QA", "",
             "- Prompts: **%d** across **%d** cards" % (summary["prompts"], summary["cards"]),
             "- TEXT_VALID: **%d**; TEXT_INVALID: **%d**; warnings: **%d**" % (
                 summary["text_valid"], summary["text_invalid"], summary["warnings"]),
             "- DOMAIN_REVIEWED / IMAGE_TESTED / HUMAN_VISUAL_APPROVED: **NOT_RUN**",
             "- Image generation: **false**", "",
             "## Cross-card homogeneity",
             "",
             "- content-token Jaccard >= 0.80: **%d** pairs" % len(homogeneity),
             "- raw template-scaffold similarity >= 0.82: **%d** pairs" % template_pairs,
             ""]
    if homogeneity:
        for h in sorted(homogeneity, key=lambda x: -x["content_jaccard"])[:30]:
            lines.append("- %s: `%s` vs `%s` (content %.3f)" % (
                h["prompt_kind"], h["card_a"], h["card_b"], h["content_jaccard"]))
    else:
        lines.append("- none")
    lines += ["", "## Warnings", ""]
    for r in warnings[:80]:
        lines.append("- `%s` (%s): %s" % (r["card_id"], r["prompt_kind"], r["warnings"]))
    lines += ["", "## Limits", "- No domain review, image test, or human visual approval.",
              "- Prompt QA is text/evidence consistency, not visual rendering quality."]
    Path(args.out_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path(OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
