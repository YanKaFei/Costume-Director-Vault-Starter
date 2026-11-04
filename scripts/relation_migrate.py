#!/usr/bin/env python3
"""P5-A relation migration: source_ids -> exact 04-来源 wikilinks + typed relations.

Rules
-----
- Resolve source_ids only by exact `SRC-xxxx` -> `04-来源/SRC-xxxx-*.md`. No URL
  fuzzy matching, no title guessing.
- Preserve YAML `source_ids` and all original facts. Only append frontmatter
  `relations:` (high confidence) and body source links; never delete cards.
- Relation schema (assumption documented in reports/P5-RELATION-MIGRATION.md):
    relations:
      - target: "SRC-0453"
        relation_type: source
        evidence: verified
        confidence: high
        note: "optional cross-ref"
- High-confidence only in body/YAML; medium/low/unresolved go to
  `11-验收/P5/REVIEW-QUEUE.csv` and are not linked.
- Canonical duplicate map: SRC-0022<-0163, SRC-0036<-0175, SRC-0115<-0157.
  Duplicate IDs remain in source_ids; migration links the canonical source and
  records the duplicate as a cross-ref.
- Idempotent, backup/rollback, pilot before full migration.

Usage:
  python3 scripts/relation_migrate.py --dry-run --pilot 30
  python3 scripts/relation_migrate.py --apply --pilot 30
  python3 scripts/relation_migrate.py --apply --full
  python3 scripts/relation_migrate.py --rollback 11-验收/P5/rollback-.../manifest.json
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
P5 = ROOT / "11-验收/P5"
SOURCE_DIR = ROOT / "04-来源"
SRC_RE = re.compile(r"^SRC-(\d{3,4})$")
ALLOWED_TYPES = {"appears_in_look", "uses_material", "may_have_part",
                 "ensemble_with", "context_includes", "in_style",
                 "look_appears_in_scene", "claim_supported_by"}
TYPE_MAP = {
    "garment_part": "garment_part", "material": "material",
    "style": "style", "period_region": "period_region", "look": "look",
    "scene": "scene", "source": "source", "pattern": "material",
}
# category fallbacks for content cards whose type is `garment`
CATEGORY_MAP = {"footwear": "footwear", "accessory": "accessory",
                "carried_prop": "accessory", "outerwear": "garment_part",
                "upper_body": "garment_part", "lower_body": "garment_part",
                "one_piece": "garment_part", "set": "garment_part"}
DUPLICATE_CANONICAL = {"SRC-0163": "SRC-0022", "SRC-0175": "SRC-0036",
                       "SRC-0157": "SRC-0115"}
AUDIT_PATH = P5 / "source-audit.csv"


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not match:
        return None, None, text
    return match.group(1), match.group(2), text[match.end():]


def load_cards(root=ROOT):
    cards = []
    for path in sorted(Path(root).glob("0[1-9]-*/**/*.md")):
        text = path.read_text(encoding="utf-8")
        fm, body, rest = split_frontmatter(text)
        if fm is None:
            continue
        try:
            meta = yaml.safe_load(fm) or {}
        except yaml.YAMLError:
            continue
        cards.append({"path": path, "text": text, "fm": fm, "meta": meta,
                      "body": body})
    return cards


def load_sources(root=ROOT):
    mapping = {}
    for path in sorted((Path(root) / "04-来源").glob("SRC-*.md")):
        cid = path.name.split("-", 2)[:2]
        cid = "-".join(cid[:2])
        if cid in mapping:
            continue
        text = path.read_text(encoding="utf-8")
        fm, _, _ = split_frontmatter(text)
        try:
            meta = yaml.safe_load(fm) or {} if fm else {}
        except yaml.YAMLError:
            meta = {}
        mapping[cid] = {"path": path, "stem": path.stem, "meta": meta,
                        "name_zh": meta.get("name_zh") or path.stem}
    return mapping


def load_audit_classes(root=ROOT):
    path = Path(root) / "11-验收/P5/source-audit.csv"
    classes = {}
    if not path.exists():
        return classes
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            cid = row.get("source_id") or row.get("id")
            if cid:
                classes[cid] = row
    return classes


def resolve_target(target, cards_by_id, sources):
    if target in sources:
        return "source", sources[target]
    card = cards_by_id.get(target)
    if card:
        return "card", card
    return None, None


def relation_type_for(card):
    meta = card["meta"]
    typ = str(meta.get("type") or "")
    if typ in ALLOWED_TYPES:
        return typ
    category = str(meta.get("category") or "")
    return CATEGORY_MAP.get(category, "garment_part")


def extract_related_ids(body):
    ids = []
    for match in re.finditer(r"\[\[([A-Z]{2,4}-\d{3,4})(?:-[^\]|]+)?(?:\|[^\]]+)?\]\]", body):
        cid = match.group(1)
        if cid not in ids:
            ids.append(cid)
    return ids


def plan_card(card, sources, cards_by_id, audit_classes, is_pilot=True):
    """Return plan dict for one content card."""
    meta = card["meta"]
    cid = str(meta.get("id") or card["path"].stem.split("-")[0])
    source_ids = [str(v) for v in (meta.get("source_ids") or []) if v]
    relations = []
    queue = []
    body_additions = []
    duplicates = []
    def has_relation(relation):
        token_target = "target=%s" % relation["target"]
        token_type = "type=%s" % relation["relation_type"]
        return token_target in card["text"] and token_type in card["text"]

    for sid in source_ids:
        target = DUPLICATE_CANONICAL.get(sid, sid)
        if sid in DUPLICATE_CANONICAL:
            duplicates.append({"duplicate": sid, "canonical": target})
        source = sources.get(target)
        if not source:
            queue.append({"card_id": cid, "card_path": str(card["path"].relative_to(ROOT)),
                          "target": sid, "relation_type": "source",
                          "evidence": "unknown", "confidence": "low",
                          "reason": "source_id not found in 04-来源"})
            continue
        evidence = str(source["meta"].get("evidence_status") or "unknown")
        content_evidence = str(meta.get("evidence_status") or "unknown")
        confidence = "high" if (evidence == "verified" and
                                content_evidence == "verified") else "medium"
        relation = {"target": target, "relation_type": "claim_supported_by",
                    "direction": "outgoing", "evidence": evidence,
                    "confidence": confidence,
                    "source_ids": [target], "rule": "R-SOURCE-IDS"}
        if target != sid:
            relation["note"] = "canonical cross-ref; card source_ids retains %s" % sid
        if confidence == "high":
            if not has_relation(relation):
                relations.append(relation)
            link = "[[%s]]" % source["stem"]
            if link not in card["body"] and link not in body_additions:
                body_additions.append("- [[%s]] — cited source (exact source_ids; no URL guessing)" % source["stem"])
        else:
            queue.append({"card_id": cid, "card_path": str(card["path"].relative_to(ROOT)),
                          "target": target, "relation_type": "claim_supported_by",
                          "evidence": evidence, "confidence": confidence,
                          "reason": "content or source evidence is not verified"})
    # Explicit related-card wikilinks already present in the body are citations.
    for target in extract_related_ids(card["body"]):
        kind, resolved = resolve_target(target, cards_by_id, sources)
        if not resolved:
            queue.append({"card_id": cid, "card_path": str(card["path"].relative_to(ROOT)),
                          "target": target, "relation_type": "unknown",
                          "evidence": "unknown", "confidence": "low",
                          "reason": "related-card target not found"})
            continue
        if kind == "source":
            continue  # source_ids/source links handled above
        target_meta = resolved["meta"]
        target_type = str(target_meta.get("type") or "")
        target_evidence = str(target_meta.get("evidence_status") or "unknown")
        content_evidence = str(meta.get("evidence_status") or "unknown")
        if target_type == "style" and target in (meta.get("style_tags") or []):
            relation_type = "in_style"
            rule = "R-STYLE-TAGS"
            confidence = "high" if (target_evidence == "verified" and
                                    content_evidence == "verified" and
                                    bool(meta.get("source_ids"))) else "medium"
        elif target_type == "material":
            relation_type = "uses_material"
            rule = "R-MATERIAL-FIELD"
            material_names = [str(v).lower() for v in (meta.get("materials") or [])]
            target_names = [str(target_meta.get("name_zh") or "").lower(),
                            str(target_meta.get("name_en") or "").lower()]
            explicit = any(name and name in material_names for name in target_names)
            confidence = "high" if (explicit and target_evidence == "verified" and
                                    content_evidence == "verified" and
                                    bool(meta.get("source_ids"))) else "medium"
        else:
            # Architect contract: may_have_part / ensemble_with cap at medium
            # without human review; do not write them into body/YAML.
            relation_type = relation_type_for(resolved)
            rule = "R-REVIEW-RELATED"
            confidence = "medium"
        relation = {"target": target, "relation_type": relation_type,
                    "direction": ("incoming" if relation_type == "context_includes"
                                 else "outgoing"),
                    "evidence": target_evidence,
                    "confidence": confidence,
                    "source_ids": [str(v) for v in (target_meta.get("source_ids") or [])],
                    "rule": rule}
        if confidence == "high" and relation_type in ALLOWED_TYPES:
            if not any(r["target"] == target for r in relations) and not has_relation(relation):
                relations.append(relation)
        else:
            queue.append({"card_id": cid, "card_path": str(card["path"].relative_to(ROOT)),
                          "target": target, "relation_type": relation_type,
                          "evidence": target_evidence, "confidence": confidence,
                          "reason": "relation caps at medium or evidence not verified"})
    # Source card topics/independent vocabulary whitelist: no forced source link.
    changed = bool(body_additions or relations)
    return {"card_id": cid, "path": card["path"], "source_ids": source_ids,
            "relations": relations, "queue": queue, "duplicates": duplicates,
            "body_additions": body_additions, "changed": changed,
            "original_sha256": sha256(card["text"]),
            "original_text": card["text"]}


def add_section_links(body, additions):
    if not additions:
        return body
    marker = "## 来源链接"
    if marker in body:
        return body.rstrip() + "\n" + "\n".join(additions) + "\n"
    marker2 = "## 相关卡片"
    block = "\n" + marker + "\n" + "\n".join(additions) + "\n\n"
    if marker2 in body:
        return body.replace(marker2, block + marker2, 1)
    return body.rstrip() + "\n\n" + marker + "\n" + "\n".join(additions) + "\n"


def append_yaml_relations(fm, relations):
    if not relations:
        return fm
    # Deterministic YAML block appended at the end of frontmatter; original
    # fields are preserved verbatim.
    lines = ["relations:"]
    for relation in relations:
        parts = ["target=%s" % relation["target"],
                 "type=%s" % relation["relation_type"],
                 "direction=%s" % relation.get("direction", "outgoing"),
                 "evidence=%s" % relation["evidence"],
                 "confidence=%s" % relation["confidence"],
                 "source_ids=%s" % ",".join(relation.get("source_ids") or []),
                 "rule=%s" % relation.get("rule", "R-MIGRATE")]
        if relation.get("note"):
            parts.append("note=%s" % relation["note"])
        lines.append("  - %r" % "; ".join(parts))
    return fm.rstrip() + "\n" + "\n".join(lines) + "\n"


def apply_plan(plan):
    path = plan["path"]
    fm, body, _ = split_frontmatter(plan["original_text"])
    if fm is None:
        return False
    new_body = add_section_links(body, plan["body_additions"])
    new_fm = append_yaml_relations(fm, plan["relations"]).rstrip("\n")
    text = "---\n" + new_fm + "\n---\n" + new_body
    if text == plan["original_text"]:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def select_pilot(plans, count=30):
    preferred = []
    seen_types = set()
    for plan in plans:
        if not plan["changed"]:
            continue
        types = tuple(sorted({r["relation_type"] for r in plan["relations"]})) or ("none",)
        if types not in seen_types:
            seen_types.add(types)
            preferred.append(plan)
    for plan in plans:
        if len(preferred) >= count:
            break
        if plan["changed"] and plan not in preferred:
            preferred.append(plan)
    return preferred[:count]


def run_backup(dest):
    cmd = [sys.executable, "scripts/backup_restore.py", "backup",
           "--dest", str(dest), "--json"]
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def audit_queue_rows(root=ROOT):
    """Queue researcher source-audit candidates; never auto-link uncited cards."""
    path = Path(root) / "11-验收/P5/source-audit.csv"
    rows = []
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as handle:
        for audit in csv.DictReader(handle):
            if audit.get("migration_class") != "action_should_connect":
                continue
            text = audit.get("evidence_relation_candidates") or ""
            match = re.search(r"\b(GAR|STR|MAT|STY|PRD|LOOK|SCN)-\d{3,4}\b", text)
            if not match:
                continue
            rows.append({"card_id": match.group(0), "card_path": "",
                         "target": audit.get("source_id"),
                         "relation_type": "claim_supported_by",
                         "evidence": audit.get("relation_verdict") or "unknown",
                         "confidence": ("low" if audit.get("confidence") == "low"
                                        else "medium"),
                         "reason": "source-audit action_should_connect; candidate only, "
                                   "no card link until curated: " + text[:160]})
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--pilot", type=int, default=0)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--rollback", help="manifest.json to rollback")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)
    root = Path(args.root)
    P5.mkdir(parents=True, exist_ok=True)
    if args.rollback:
        manifest = json.loads(Path(args.rollback).read_text(encoding="utf-8"))
        for entry in manifest.get("files", []):
            original = Path(manifest["rollback_dir"]) / (entry["card_id"] + ".md")
            target = root / entry["path"]
            if original.exists():
                shutil.copy2(original, target)
        print("rolled back %d files" % len(manifest.get("files", [])))
        return 0
    cards = load_cards(root)
    sources = load_sources(root)
    cards_by_id = {str(c["meta"].get("id")): c for c in cards if c["meta"].get("id")}
    audit_classes = load_audit_classes(root)
    plans = []
    for card in cards:
        if str(card["meta"].get("type") or "") == "source":
            continue
        plans.append(plan_card(card, sources, cards_by_id, audit_classes))
    changed = [plan for plan in plans if plan["changed"]]
    queue = [row for plan in plans for row in plan["queue"]]
    seen_queue = {(row["card_id"], row["target"], row["relation_type"]) for row in queue}
    for row in audit_queue_rows(root):
        key = (row["card_id"], row["target"], row["relation_type"])
        if key not in seen_queue:
            queue.append(row)
            seen_queue.add(key)
    if args.pilot:
        selected = select_pilot(changed, args.pilot)
    elif args.full:
        selected = changed
    else:
        selected = changed
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    rollback_dir = P5 / ("rollback-" + timestamp)
    manifest = {"created": timestamp, "root": str(root),
                "backup_dir": str(rollback_dir), "rollback_dir": str(rollback_dir),
                "files": []}
    # queue first (even dry run) so reviewers see medium/low.
    queue_path = P5 / "REVIEW-QUEUE.csv"
    with queue_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["card_id", "card_path", "target",
                                                   "relation_type", "evidence",
                                                   "confidence", "reason"])
        writer.writeheader()
        writer.writerows(queue)
    if args.apply and selected:
        if not args.no_backup:
            backup_dest = Path("/tmp") / ("p5-backup-" + timestamp)
            proc = run_backup(backup_dest)
            if proc.returncode != 0:
                print("ERROR: backup failed: %s" % proc.stderr[-500:], file=sys.stderr)
                return 2
            verify = subprocess.run([sys.executable, "scripts/backup_restore.py",
                                     "verify", str(backup_dest), "--json"],
                                    cwd=str(ROOT), capture_output=True, text=True)
            if verify.returncode != 0:
                print("ERROR: backup verify failed", file=sys.stderr)
                return 2
            manifest["backup"] = str(backup_dest)
        rollback_dir.mkdir(parents=True, exist_ok=True)
        for plan in selected:
            (rollback_dir / (plan["card_id"] + ".md")).write_text(
                plan["original_text"], encoding="utf-8")
            manifest["files"].append({"card_id": plan["card_id"],
                                      "path": str(plan["path"].relative_to(root)),
                                      "original_sha256": plan["original_sha256"]})
            if not args.dry_run:
                apply_plan(plan)
        (P5 / "last-rollback-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # second pass idempotence check (in memory)
    plans_after = []
    if args.apply and not args.dry_run:
        cards2 = load_cards(root)
        cards_by_id2 = {str(c["meta"].get("id")): c for c in cards2 if c["meta"].get("id")}
        for card in cards2:
            if str(card["meta"].get("type") or "") == "source":
                continue
            plans_after.append(plan_card(card, sources, cards_by_id2, audit_classes))
        non_idempotent = [p["card_id"] for p in plans_after if p["changed"]]
    else:
        non_idempotent = []
    report = {
        "mode": "apply" if args.apply else "dry-run",
        "content_cards": len(plans),
        "changed_cards": len(changed),
        "selected": len(selected),
        "relations_high": sum(len(p["relations"]) for p in selected),
        "source_links": sum(len(p["body_additions"]) for p in selected),
        "duplicates": sum(len(p["duplicates"]) for p in selected),
        "queue": len(queue),
        "pilot": args.pilot,
        "full": args.full,
        "non_idempotent": non_idempotent,
        "backup": manifest.get("backup"),
        "rollback_dir": str(rollback_dir) if selected else None,
        "selected_cards": [p["card_id"] for p in selected],
        "queue_path": str(queue_path),
    }
    (P5 / "migration-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not non_idempotent else 1


if __name__ == "__main__":
    sys.exit(main())
