#!/usr/bin/env python3
"""P5-E E4/E6 candidate risk review for the 239 relation queue.

Conservative triage only; NEVER promotes medium/review to high/verified and never
writes cards.  Checks real targets, endpoint evidence, source audit and subject-type
rules, then classifies each candidate:

  source_verifiable  - explicit structured relation, endpoints verified, source path
                       known; human may promote later (recommendation only)
  needs_human        - design/co-occurrence or interpretive evidence; requires review
  reject_or_rework   - missing target, invalid subject type, blacklisted duplicate,
                       or unsupported historical claim

Outputs JSON/CSV and a summary; design relations are marked design_only and can be
filtered by relation tools / --design-only.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
P5E = ROOT / "11-验收/P5E"
P5D = ROOT / "11-验收/P5D"
DEFAULT_QUEUE = P5D / "DESIGN-QUEUE-REMAINING.csv"
ALLOWED_TYPES = {"appears_in_look", "uses_material", "may_have_part",
                 "ensemble_with", "context_includes", "in_style",
                 "look_appears_in_scene", "claim_supported_by",
                 "style_interpretation"}
DESIGN_TYPES = {"uses_material", "may_have_part", "ensemble_with",
                "in_style", "appears_in_look", "look_appears_in_scene",
                "style_interpretation"}
SUBJECT_RULES = {
    "in_style": {"garment", "garment_part", "look", "period_region"},
    "may_have_part": {"garment"},
    "ensemble_with": {"garment"},
    "appears_in_look": {"look"},
    "look_appears_in_scene": {"look"},
    "context_includes": {"period_region"},
    "style_interpretation": {"look", "garment", "garment_part", "style"},
}
BLACKLIST = {"SRC-0157", "SRC-0163", "SRC-0175"}


def split_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    return (match.group(1), match.group(2)) if match else (None, None)


def load_cards(root=ROOT):
    cards, sources = {}, {}
    for path in sorted(Path(root).glob("0[1-9]-*/**/*.md")):
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        if fm is None:
            continue
        try:
            meta = yaml.safe_load(fm) or {}
        except yaml.YAMLError:
            continue
        cid = str(meta.get("id") or path.stem.split("-")[0])
        cards[cid] = {"id": cid, "path": str(path.relative_to(root)),
                      "meta": meta, "body": body or ""}
    for path in sorted((Path(root) / "04-来源").glob("SRC-*.md")):
        sid = "-".join(path.name.split("-", 2)[:2])
        sources[sid] = {"id": sid, "path": str(path.relative_to(root)),
                        "name_zh": path.stem}
    return cards, sources


def load_source_audit(root=ROOT):
    path = Path(root) / "11-验收/P5/source-audit.csv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return {row.get("source_id"): row for row in csv.DictReader(handle)}


def source_verified_ids(card):
    return [str(s) for s in (card["meta"].get("source_ids") or []) if s]


def review_row(row, cards, sources, audit):
    cid = row.get("card_id") or ""
    tid = row.get("target") or ""
    rtype = row.get("relation_type") or ""
    subject = cards.get(cid)
    target = cards.get(tid)
    target_source = sources.get(tid)
    reasons = []
    risks = []
    design_only = rtype in DESIGN_TYPES
    if not subject:
        reasons.append("missing subject card")
    if not target and not target_source:
        reasons.append("missing real target")
    subject_type = str(subject["meta"].get("type") or "") if subject else ""
    rules = SUBJECT_RULES.get(rtype)
    if rules and subject_type not in rules:
        reasons.append("invalid subject type %s for %s" % (subject_type, rtype))
        risks.append("historical_misleading")
    if tid in BLACKLIST:
        reasons.append("blacklisted duplicate source")
        risks.append("historical_misleading")
    if rtype not in ALLOWED_TYPES:
        reasons.append("unknown relation type")
    subject_verified = bool(subject and subject["meta"].get("evidence_status") == "verified")
    target_verified = bool((target and target["meta"].get("evidence_status") == "verified") or
                           (target_source and tid in sources))
    source_ids = source_verified_ids(subject) if subject else []
    sourced = bool(source_ids)
    audit_row = audit.get(tid) or audit.get(cid)
    audit_ok = bool(audit_row and str(audit_row.get("migration_class")) in
                    ("whitelist_connected", "whitelist_independent"))
    if rtype in ("claim_supported_by", "context_includes", "in_style"):
        if not (subject_verified and target_verified):
            reasons.append("historical/evidence endpoints not both verified")
            risks.append("historical_misleading")
        if not sourced:
            reasons.append("no subject source_ids")
    if rtype in ("uses_material", "may_have_part", "ensemble_with"):
        risks.append("material_structure_misleading")
        if not target_verified:
            reasons.append("material/structure target not verified")
    if design_only:
        risks.append("design_interpretation_not_fact")
    if reasons:
        tier = "reject_or_rework"
        recommendation = "do_not_migrate; rework/remove"
    elif (subject_verified and target_verified and (sourced or audit_ok) and
          not any(risk == "historical_misleading" for risk in risks)):
        # Source-checkable candidate; design_only rows stay design/review and are
        # never promoted to high/verified by this tool.
        tier = "source_verifiable"
        recommendation = ("source-checkable; human review only; "
                          + ("design_only/not historical fact" if design_only
                             else "no auto promotion"))
    else:
        tier = "needs_human"
        recommendation = "human semantic review; keep queued; design/review only"
    return {
        "card_id": cid, "target": tid, "relation_type": rtype,
        "evidence": row.get("evidence") or "unknown",
        "confidence": row.get("confidence") or "medium",
        "rule": row.get("rule") or "",
        "tier": tier, "recommendation": recommendation,
        "design_only": design_only, "auto_promotion": False,
        "subject_type": subject_type, "subject_path": subject["path"] if subject else None,
        "target_path": (target["path"] if target else
                        target_source["path"] if target_source else None),
        "subject_verified": subject_verified, "target_verified": target_verified,
        "source_ids": source_ids, "source_audit_ok": audit_ok,
        "risks": sorted(set(risks)), "reasons": reasons,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", default=str(DEFAULT_QUEUE))
    parser.add_argument("--out", default=str(P5E / "candidate-review.csv"))
    parser.add_argument("--json-out", default=str(P5E / "candidate-review.json"))
    parser.add_argument("--design-only", action="store_true",
                        help="only design/co-occurrence candidates")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    P5E.mkdir(parents=True, exist_ok=True)
    cards, sources = load_cards()
    audit = load_source_audit()
    rows = []
    with Path(args.queue).open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    reviewed = [review_row(row, cards, sources, audit) for row in rows]
    if args.design_only:
        reviewed = [row for row in reviewed if row["design_only"]]
    fieldnames = list(reviewed[0].keys()) if reviewed else []
    with Path(args.out).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviewed)
    summary = {
        "input": str(Path(args.queue)),
        "candidates": len(rows),
        "reviewed": len(reviewed),
        "tiers": {tier: sum(1 for r in reviewed if r["tier"] == tier)
                  for tier in ("source_verifiable", "needs_human",
                               "reject_or_rework")},
        "source_verifiable": sum(1 for r in reviewed if r["tier"] == "source_verifiable"),
        "needs_human": sum(1 for r in reviewed if r["tier"] == "needs_human"),
        "reject_or_rework": sum(1 for r in reviewed if r["tier"] == "reject_or_rework"),
        "design_only": sum(1 for r in reviewed if r["design_only"]),
        "auto_promotions": 0,
        "card_writes": 0,
        "promotion_policy": "NEVER auto-promote medium/review to high/verified",
    }
    Path(args.json_out).write_text(
        json.dumps({"summary": summary, "rows": reviewed}, ensure_ascii=False,
                   indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
