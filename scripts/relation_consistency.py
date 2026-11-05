#!/usr/bin/env python3
"""P5-B relation consistency checker.

Checks card YAML `relations:` against visible wikilinks and real targets:
- every relation target resolves to a real content card or 04-来源 source;
- high-confidence relation has a visible wikilink in the card body;
- a visible cited-source link has a matching claim_supported_by relation;
- no duplicate relation or duplicate bidirectional fact;
- no medium/low confidence relation written into cards (queue only);
- MOC pages are navigation, not facts: skipped, never used as evidence.

Usage:
  python3 scripts/relation_consistency.py [--root PATH] [--json]
Exit 0 clean; 1 errors.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TYPES = {"appears_in_look", "uses_material", "may_have_part",
                 "ensemble_with", "context_includes", "in_style",
                 "look_appears_in_scene", "claim_supported_by",
                 "style_interpretation"}
# Explicit P5-D semantic corrections: medium claim retained after downgrade.
P5D_ALLOWED_MEDIUM = {("GAR-0079", "SRC-0069", "claim_supported_by")}
DESIGN_MEDIUM_TYPES = {"style_interpretation", "uses_material",
                       "may_have_part", "ensemble_with", "in_style",
                       "appears_in_look", "look_appears_in_scene"}
ALLOWED_EVIDENCE = {"verified", "interpretive", "example"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
REL_RE = re.compile(
    r"target=(?P<target>[^;]+); type=(?P<type>[^;]+); direction=(?P<direction>[^;]+); "
    r"evidence=(?P<evidence>[^;]+); confidence=(?P<confidence>[^;]+); "
    r"source_ids=(?P<source_ids>[^;]*); rule=(?P<rule>[^;']+)")


def split_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        return None, None
    return match.group(1), match.group(2)


def parse_relations(meta):
    result = []
    for raw in meta.get("relations") or []:
        if isinstance(raw, dict):
            # tolerate old nested form only for reporting; card migration uses flat
            result.append({k: str(v) for k, v in raw.items()})
            continue
        match = REL_RE.search(str(raw))
        if not match:
            result.append({"raw": str(raw), "parse_error": True})
            continue
        item = match.groupdict()
        item["source_ids"] = [s for s in item["source_ids"].split(",") if s]
        result.append(item)
    return result


CODE_SPAN = re.compile(r"`[^`\n]*`")
FENCED = re.compile(r"(?ms)^```.*?^```")


def obsidian_visible(body):
    """Ignore fenced/inline code; only real Obsidian-visible wikilinks count."""
    return FENCED.sub("", CODE_SPAN.sub("", body))


def visible_links(body):
    return re.findall(r"\[\[([^\]]+)\]\]", obsidian_visible(body))


CORRECTIONS = None


def load_corrections(root=ROOT):
    global CORRECTIONS
    if CORRECTIONS is not None:
        return CORRECTIONS
    path = Path(root) / "reports/P5B-RELATION-CORRECTIONS.csv"
    rows = []
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    CORRECTIONS = rows
    return rows


def corrected_downgrades(root=ROOT):
    out = set()
    for row in load_corrections(root):
        if row.get("action") != "downgrade_relation":
            continue
        text = (row.get("old") or "") + " " + (row.get("new") or "")
        target = ""
        match = re.search(r"target=([^;]+)", text)
        if match:
            target = match.group(1).strip()
        if target:
            out.add((row.get("card_id"), target, row.get("relation_type")))
    return out


def check(root=ROOT):
    root = Path(root)
    cards = {}
    errors = []
    warnings = []
    moc_files = []
    for path in sorted(root.glob("0[1-9]-*/**/*.md")):
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        if fm is None:
            continue
        try:
            meta = yaml.safe_load(fm) or {}
        except yaml.YAMLError:
            continue
        cid = str(meta.get("id") or path.stem.split("-")[0])
        cards[cid] = {"path": path, "meta": meta, "body": body,
                      "links": visible_links(body)}
    moc_dir = root / "00-系统/MOC"
    if moc_dir.exists():
        moc_files = [str(p.relative_to(root)) for p in moc_dir.rglob("*.md")]
    sources = {p.name.split("-", 2)[0] + "-" + p.name.split("-", 2)[1]:
               p for p in sorted((root / "04-来源").glob("SRC-*.md"))}
    relations = []
    allowed_downgrades = corrected_downgrades(root)
    for cid, card in cards.items():
        for relation in parse_relations(card["meta"]):
            if relation.get("parse_error"):
                errors.append({"code": "unparseable_relation", "card": cid,
                               "raw": relation.get("raw")})
                continue
            target = relation["target"]
            rtype = relation["type"]
            confidence = relation["confidence"]
            evidence = relation["evidence"]
            relation["subject"] = cid
            relation["card_path"] = str(card["path"].relative_to(root))
            relations.append(relation)
            if rtype not in ALLOWED_TYPES:
                errors.append({"code": "invalid_relation_type", "card": cid,
                               "target": target, "type": rtype})
            subject_type = str(card["meta"].get("type") or "")
            subject_rules = {
                # period_region style membership is historical context metadata,
                # not a scene misuse; scene subjects remain invalid.
                "in_style": {"garment", "garment_part", "look", "period_region"},
                "may_have_part": {"garment"},
                "ensemble_with": {"garment"},
                "appears_in_look": {"look"},
                "look_appears_in_scene": {"look"},
                "context_includes": {"period_region"},
                "style_interpretation": {"look", "garment", "garment_part", "style"},
            }
            allowed_subjects = subject_rules.get(rtype)
            if allowed_subjects and subject_type not in allowed_subjects:
                errors.append({"code": "invalid_subject_type", "card": cid,
                               "target": target, "type": rtype,
                               "subject_type": subject_type})
            if evidence not in ALLOWED_EVIDENCE:
                errors.append({"code": "invalid_evidence", "card": cid,
                               "target": target, "evidence": evidence})
            if confidence not in ALLOWED_CONFIDENCE:
                errors.append({"code": "invalid_confidence", "card": cid,
                               "target": target, "confidence": confidence})
            review_status = str(card["meta"].get("review_status") or "").strip()
            design_ok = (rtype in DESIGN_MEDIUM_TYPES and
                         confidence == "medium" and
                         evidence in ("interpretive", "verified") and
                         bool(review_status))
            if rtype == "style_interpretation" and confidence != "medium":
                errors.append({"code": "invalid_design_confidence", "card": cid,
                               "target": target, "confidence": confidence})
            if (confidence != "high" and not design_ok and
                    (cid, target, rtype) not in allowed_downgrades and
                    (cid, target, rtype) not in P5D_ALLOWED_MEDIUM):
                errors.append({"code": "low_confidence_in_body", "card": cid,
                               "target": target, "confidence": confidence})
            if target not in cards and target not in sources:
                errors.append({"code": "missing_target", "card": cid,
                               "target": target})
            if confidence == "high":
                target_stem = None
                if target in sources:
                    target_stem = sources[target].stem
                if not any(target in link or (target_stem and target_stem in link)
                           for link in card["links"]):
                    errors.append({"code": "missing_visible_wikilink", "card": cid,
                                   "target": target})
        # cited-source marker must have a matching claim_supported_by relation
        cited = re.findall(r"\[\[(SRC-\d{3,4})-[^\]]+\]\] — cited source",
                           obsidian_visible(card["body"]))
        for sid in cited:
            if not any(r["target"] == sid and r["type"] == "claim_supported_by"
                       and r["confidence"] == "high"
                       for r in parse_relations(card["meta"])):
                errors.append({"code": "orphan_cited_source_link", "card": cid,
                               "target": sid})
    # duplicate exact relation and bidirectional duplicate fact
    seen = {}
    pair_seen = {}
    for relation in relations:
        key = (relation["subject"], relation["target"], relation["type"])
        if key in seen:
            errors.append({"code": "duplicate_relation", "card": relation["subject"],
                           "target": relation["target"], "type": relation["type"]})
        seen[key] = True
        pair = tuple(sorted((relation["subject"], relation["target"]))) + (relation["type"],)
        if relation["direction"] in ("outgoing", "subject_to_object", "symmetric"):
            pair_seen.setdefault(pair, []).append(relation)
    for pair, items in pair_seen.items():
        if len(items) > 1 and len({i["subject"] for i in items}) > 1:
            errors.append({"code": "duplicate_bidirectional_fact",
                           "pair": list(pair)})
    return {"cards": len(cards), "relations": len(relations),
            "errors": errors, "warnings": warnings,
            "error_count": len(errors), "moc_files_skipped": moc_files,
            "correction_rows": len(load_corrections(root)),
            "corrected_downgrades": len(allowed_downgrades)}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", help="write JSON report to file")
    args = parser.parse_args(argv)
    report = check(args.root)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text if args.json else
          "cards=%d relations=%d errors=%d moc_skipped=%d" % (
              report["cards"], report["relations"], report["error_count"],
              len(report["moc_files_skipped"])))
    for error in report["errors"][:20]:
        print("ERROR %s" % json.dumps(error, ensure_ascii=False), file=sys.stderr)
    return 0 if report["error_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
