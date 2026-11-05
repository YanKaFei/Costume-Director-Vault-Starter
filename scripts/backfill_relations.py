#!/usr/bin/env python3
"""P5-D conservative relation backfill (old cards only; append-only).

Rules:
- in_style: exact STY-xxxx in style_tags -> STY card; high only if target visible
  in body; otherwise medium review queue.
- uses_material: unique token -> MAT entity card, excluding property MAT-0012/0013
  and pattern cards; medium/interpretive review queue.
- appears_in_look: LOOK.look_items -> item; medium/creative queue.
- ensemble_with: same LOOK garment + footwear/accessory; medium/design queue.
- may_have_part: same LOOK garment + garment_part co-occurrence; medium review.
- look_appears_in_scene: LOOK.look_scene -> SCN; high when both verified and LOOK
  has source_ids; visible link added; else queue.
- claim_supported_by: never duplicated.
- silhouette: N/A (no target card type).

Only appends relations/visible links; never changes facts/source_ids/evidence_status.
Backup, idempotent, rollback, relation_consistency/validate checks in report.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
P5D = ROOT / "11-验收/P5D"
REL_RE = re.compile(r"target=([^;]+); type=([^;]+); direction=([^;]+); evidence=([^;]+); confidence=([^;]+); source_ids=([^;]*); rule=([^;']+)")
DESIGN_TYPES = {"in_style", "uses_material", "appears_in_look", "ensemble_with",
                "may_have_part", "look_appears_in_scene"}
P5C_NEW = set(
    [f"LOOK-{n:04d}" for n in range(24, 36)] +
    [f"STY-{n:04d}" for n in range(11, 16)] +
    [f"GAR-{n:04d}" for n in range(88, 92)] +
    [f"STR-{n:04d}" for n in range(27, 36)] +
    [f"MAT-{n:04d}" for n in range(15, 20)])


def split_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    return (match.group(1), match.group(2)) if match else (None, None)


def load_cards(root=ROOT):
    cards = {}
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
        cards[cid] = {"id": cid, "path": path, "text": text, "fm": fm,
                      "body": body or "", "meta": meta}
    sources = {}
    for path in sorted((Path(root) / "04-来源").glob("SRC-*.md")):
        sid = "-".join(path.name.split("-", 2)[:2])
        sources.setdefault(sid, {"id": sid, "stem": path.stem,
                                 "path": path, "name_zh": path.stem})
    return cards, sources


def existing_keys(card):
    keys = set()
    for raw in card["meta"].get("relations") or []:
        m = REL_RE.search(str(raw))
        if m:
            keys.add((m.group(2), m.group(1)))
    return keys


def visible_target(body, target, stem=None):
    return ("[[%s" % target in body) or bool(stem and "[[%s" % stem in body)


def plan_card(card, cards, sources):
    cid = card["id"]
    meta = card["meta"]
    keys = existing_keys(card)
    high = []
    queue = []
    body_additions = []
    def add_relation(rtype, target, evidence, confidence, rule, extra=None):
        if (rtype, target) in keys:
            return False
        if rtype in DESIGN_TYPES and confidence == "high" and rtype not in ("look_appears_in_scene", "in_style"):
            return False
        relation = {"target": target, "relation_type": rtype,
                    "direction": "outgoing", "evidence": evidence,
                    "confidence": confidence,
                    "source_ids": [str(x) for x in (meta.get("source_ids") or [])],
                    "rule": rule, "factual": False}
        if extra:
            relation.update(extra)
        if confidence == "high":
            high.append(relation)
        else:
            queue.append({"card_id": cid, "target": target,
                          "relation_type": rtype, "evidence": evidence,
                          "confidence": confidence, "rule": rule,
                          "reason": "medium/low design relation -> review queue"})
        keys.add((rtype, target))
        return True

    # in_style: exact STY ID; high only when target already visible.
    for tag in meta.get("style_tags") or []:
        tag = str(tag)
        if not re.match(r"^STY-\d{4}$", tag) or tag == cid:
            continue
        target = cards.get(tag)
        if not target or target["meta"].get("type") != "style":
            continue
        visible = visible_target(card["body"], tag, target["path"].stem)
        subject_verified = meta.get("evidence_status") == "verified"
        target_verified = target["meta"].get("evidence_status") == "verified"
        high_ok = subject_verified and target_verified and bool(meta.get("source_ids"))
        added = add_relation("in_style", tag, "verified" if high_ok else "interpretive",
                             "high" if high_ok else "medium", "R-STY-EXACT")
        if high_ok and added and not visible:
            body_additions.append("- [[%s]] — exact style tag relation" % target["path"].stem)

    # uses_material: unique token -> MAT entity; exclude property/pattern cards.
    material_cards = [c for c in cards.values()
                      if c["meta"].get("type") == "material" and
                      c["id"] not in ("MAT-0012", "MAT-0013")]
    for token in meta.get("materials") or []:
        norm = str(token).strip().lower()
        matches = []
        for mat in material_cards:
            names = [str(mat["meta"].get("name_zh") or "").lower(),
                     str(mat["meta"].get("name_en") or "").lower()]
            mats = [str(x).lower() for x in (mat["meta"].get("materials") or [])]
            if norm in names or norm in mats:
                matches.append(mat)
        if len(matches) == 1:
            mat = matches[0]
            add_relation("uses_material", mat["id"], "interpretive", "medium",
                         "R-MAT-TOKEN")

    # LOOK-derived relations.
    if meta.get("type") == "look":
        items = [str(x) for x in (meta.get("look_items") or [])]
        by_type = {}
        for item in items:
            target = cards.get(item)
            if not target:
                continue
            typ = target["meta"].get("type")
            by_type.setdefault(typ, []).append(item)
        for item in items:
            target = cards.get(item)
            if target and target["meta"].get("type") in ("garment", "garment_part",
                                                         "material", "pattern"):
                add_relation("appears_in_look", item, "interpretive", "medium",
                             "R-LOOK-ITEMS")
        garments = by_type.get("garment", [])
        accessories = (by_type.get("footwear", []) + by_type.get("accessory", []) +
                       by_type.get("carried_prop", []))
        for garment in garments:
            for accessory in accessories:
                add_relation("ensemble_with", accessory, "interpretive", "medium",
                             "R-LOOK-ENSEMBLE")
            for part in by_type.get("garment_part", []):
                add_relation("may_have_part", part, "interpretive", "medium",
                             "R-LOOK-PART-COOCCUR")
        for scene in meta.get("look_scene") or []:
            scene = str(scene)
            target = cards.get(scene)
            if not target or target["meta"].get("type") != "scene":
                continue
            high_ok = (meta.get("evidence_status") == "verified" and
                       target["meta"].get("evidence_status") == "verified" and
                       bool(meta.get("source_ids")))
            add_relation("look_appears_in_scene", scene,
                         "verified" if high_ok else "interpretive",
                         "high" if high_ok else "medium", "R-LOOK-SCENE")
            if high_ok and not visible_target(card["body"], scene, target["path"].stem):
                body_additions.append("- [[%s]] — explicit look scene" % target["path"].stem)
    return {"card_id": cid, "path": card["path"], "high": high, "queue": queue,
            "body_additions": body_additions,
            "changed": bool(high or body_additions),
            "original_text": card["text"], "original_fm": card["fm"],
            "original_body": card["body"], "source_ids": meta.get("source_ids") or []}


def append_relations(fm, relations):
    if not relations:
        return fm
    lines = []
    for relation in relations:
        parts = ["target=%s" % relation["target"],
                 "type=%s" % relation["relation_type"],
                 "direction=%s" % relation.get("direction", "outgoing"),
                 "evidence=%s" % relation["evidence"],
                 "confidence=%s" % relation["confidence"],
                 "source_ids=%s" % ",".join(relation.get("source_ids") or []),
                 "rule=%s" % relation.get("rule", "R-BACKFILL")]
        if relation.get("design_only"):
            parts.extend(["review_status=review_queue", "factual=false",
                          "design_only=true"])
        lines.append("  - %r" % "; ".join(parts))
    match = re.search(r"(?ms)^relations:\s*\n(.*?)(?=^[A-Za-z_][^:\n]*:|\Z)", fm)
    if match:
        block = match.group(0).rstrip("\n")
        prefix = fm[:match.start()].rstrip("\n")
        suffix = fm[match.end():].strip("\n")
        existing = block.splitlines()[1:]
        for line in lines:
            if line not in existing:
                existing.append(line)
        merged = "relations:\n" + "\n".join(existing)
        return "\n".join(x for x in (prefix, merged, suffix) if x) + "\n"
    return fm.rstrip() + "\nrelations:\n" + "\n".join(lines) + "\n"


def append_body_links(body, additions):
    if not additions:
        return body
    marker = "## 相关卡片"
    if marker in body:
        return body.rstrip() + "\n" + "\n".join(additions) + "\n"
    return body.rstrip() + "\n\n## 相关卡片\n" + "\n".join(additions) + "\n"


def apply_plan(plan):
    new_fm = append_relations(plan["original_fm"], plan["high"]).rstrip("\n")
    new_body = append_body_links(plan["original_body"], plan["body_additions"])
    text = "---\n" + new_fm + "\n---\n" + new_body
    if text == plan["original_text"]:
        return False
    plan["path"].write_text(text, encoding="utf-8")
    return True


def choose_targets(cards, pilot):
    old = [cid for cid, card in cards.items()
           if card["meta"].get("type") != "source" and cid not in P5C_NEW]
    # Prioritise cards whose structure produces gaps, then fill by type diversity.
    changed = [p for p in (plan_card(cards[cid], cards, {}) for cid in old) if p["changed"]]
    chosen = changed[:pilot]
    for cid in old:
        if len(chosen) >= pilot:
            break
        if cards[cid] not in [cards[x["card_id"]] for x in chosen]:
            chosen.append(plan_card(cards[cid], cards, {}))
    return chosen[:pilot]


def run_backup(dest):
    return subprocess.run([sys.executable, "scripts/backup_restore.py", "backup",
                           "--dest", str(dest), "--json"], cwd=str(ROOT),
                          capture_output=True, text=True)


def run_design_pilot(root, count=30, backup=True):
    """Controlled exception: add medium design relations from REVIEW-QUEUE."""
    cards, sources = load_cards(root)
    queue_path = P5D / "REVIEW-QUEUE.csv"
    rows = []
    if queue_path.exists():
        with queue_path.open(encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    by_card = {}
    for row in rows:
        by_card.setdefault(row["card_id"], []).append(row)
    type_order = ["in_style", "uses_material", "appears_in_look", "ensemble_with",
                  "may_have_part", "look_appears_in_scene"]
    selected = []
    used_cards = set()
    while len(selected) < count:
        progress = False
        for rtype in type_order:
            for cid in sorted(by_card):
                if cid in used_cards:
                    continue
                matches = [r for r in by_card[cid] if r["relation_type"] == rtype]
                if matches:
                    selected.append((cid, matches[0]))
                    used_cards.add(cid)
                    progress = True
                    break
            if len(selected) >= count:
                break
        if not progress:
            break
    applied = []
    skipped = []
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = None
    if selected and backup:
        dest = Path("/tmp") / ("p5d-design-backup-" + timestamp)
        proc = run_backup(dest)
        if proc.returncode != 0:
            print("ERROR backup failed: %s" % proc.stderr[-500:], file=sys.stderr)
            return 2
        backup_path = str(dest)
    rollback_dir = P5D / ("design-rollback-" + timestamp)
    manifest = {"created": timestamp, "rollback_dir": str(rollback_dir), "files": []}
    for cid, row in selected:
        card = cards.get(cid)
        target = cards.get(row["target"])
        if not card or not target:
            skipped.append({"card_id": cid, "target": row["target"],
                            "reason": "missing card/target"})
            continue
        key = (row["relation_type"], row["target"])
        if key in existing_keys(card):
            skipped.append({"card_id": cid, "target": row["target"],
                            "reason": "existing relation"})
            continue
        stem = target["path"].stem
        relation = {"target": row["target"], "relation_type": row["relation_type"],
                    "direction": "outgoing", "evidence": "interpretive",
                    "confidence": "medium", "source_ids": [],
                    "rule": row.get("rule") or "R-DESIGN-REVIEW",
                    "design_only": True}
        new_fm = append_relations(card["fm"], [relation]).rstrip("\n")
        addition = "- [[%s]] — design relation (medium/review_queue; design_only=true; not a historical fact)" % stem
        new_body = append_body_links(card["body"], [addition])
        new_text = "---\n" + new_fm + "\n---\n" + new_body
        rollback_dir.mkdir(parents=True, exist_ok=True)
        (rollback_dir / (cid + ".md")).write_text(card["text"], encoding="utf-8")
        manifest["files"].append({"card_id": cid, "path": str(card["path"].relative_to(root))})
        card["path"].write_text(new_text, encoding="utf-8")
        applied.append({"card_id": cid, "target": row["target"],
                        "relation_type": row["relation_type"],
                        "path": str(card["path"].relative_to(root)),
                        "visible_marker": addition})
    if applied:
        (P5D / "design-rollback-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with (P5D / "DESIGN-PILOT.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["card_id", "target",
                                                       "relation_type", "path",
                                                       "visible_marker"])
            writer.writeheader()
            writer.writerows(applied)
        applied_keys = {(a["card_id"], a["target"], a["relation_type"]) for a in applied}
        remaining = [r for r in rows
                     if (r["card_id"], r["target"], r["relation_type"]) not in applied_keys]
        with (P5D / "DESIGN-QUEUE-REMAINING.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else [])
            writer.writeheader()
            writer.writerows(remaining)
        # Keep the live review queue aligned with what remains.
        with queue_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys() if rows else [])
            writer.writeheader()
            writer.writerows(remaining)
    report = {"mode": "design-pilot", "requested": count,
              "selected": len(selected), "applied": len(applied),
              "skipped": len(skipped), "design_relations": len(applied),
              "design_cards": len({a["card_id"] for a in applied}),
              "remaining_queue": len(rows) - len(applied),
              "types": {t: sum(1 for a in applied if a["relation_type"] == t)
                        for t in sorted({a["relation_type"] for a in applied})},
              "backup": backup_path,
              "rollback_dir": str(rollback_dir) if applied else None}
    (P5D / "design-pilot-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--pilot", type=int, default=0)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--backup", action="store_true")
    parser.add_argument("--rollback", help="manifest JSON")
    parser.add_argument("--design-pilot", type=int, default=0,
                        help="controlled medium design-relation pilot from REVIEW-QUEUE")
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root)
    P5D.mkdir(parents=True, exist_ok=True)
    if args.rollback:
        manifest = json.loads(Path(args.rollback).read_text(encoding="utf-8"))
        for entry in manifest.get("files", []):
            original = Path(manifest["rollback_dir"]) / (entry["card_id"] + ".md")
            if original.exists():
                (root / entry["path"]).write_text(original.read_text(encoding="utf-8"),
                                                  encoding="utf-8")
        print("rolled back %d files" % len(manifest.get("files", [])))
        return 0
    if args.design_pilot:
        return run_design_pilot(root, args.design_pilot, backup=not args.no_backup)
    cards, sources = load_cards(root)
    old = [cid for cid, card in cards.items()
           if card["meta"].get("type") != "source" and cid not in P5C_NEW]
    plans = [plan_card(cards[cid], cards, sources) for cid in old]
    changed = [p for p in plans if p["changed"]]
    if args.pilot:
        # deterministic representative subset: inspect 30 old cards even if no safe
        # high-confidence gap is found (queue may still be populated).
        type_order = ["look", "garment", "garment_part", "period_region",
                      "material", "style", "scene", "pattern"]
        buckets = {t: [] for t in type_order}
        for plan in plans:
            typ = cards[plan["card_id"]]["meta"].get("type")
            buckets.setdefault(typ, []).append(plan)
        ordered = []
        while len(ordered) < args.pilot and any(buckets.values()):
            for typ in type_order + sorted(set(buckets) - set(type_order)):
                if buckets.get(typ) and len(ordered) < args.pilot:
                    ordered.append(buckets[typ].pop(0))
        selected = ordered
    else:
        selected = changed if args.full else changed
    queue = [row for p in plans for row in p["queue"]]
    # queue even in dry-run
    qpath = P5D / "REVIEW-QUEUE.csv"
    with qpath.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["card_id", "target",
                                                   "relation_type", "evidence",
                                                   "confidence", "rule", "reason"])
        writer.writeheader()
        writer.writerows(queue)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    rollback_dir = P5D / ("rollback-" + timestamp)
    manifest = {"created": timestamp, "rollback_dir": str(rollback_dir), "files": []}
    backup = None
    to_apply = [p for p in selected if p["changed"]]
    if args.apply and to_apply:
        if args.backup:
            dest = Path("/tmp") / ("p5d-backup-" + timestamp)
            proc = run_backup(dest)
            if proc.returncode != 0:
                print("ERROR backup failed: %s" % proc.stderr[-500:], file=sys.stderr)
                return 2
            backup = str(dest)
        rollback_dir.mkdir(parents=True, exist_ok=True)
        for plan in to_apply:
            (rollback_dir / (plan["card_id"] + ".md")).write_text(plan["original_text"],
                                                                  encoding="utf-8")
            manifest["files"].append({"card_id": plan["card_id"],
                                      "path": str(plan["path"].relative_to(root))})
            if not args.dry_run:
                apply_plan(plan)
        (P5D / "last-rollback-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # idempotence in-memory
    plans_after = [plan_card(cards[cid], cards, sources) for cid in old]
    if args.apply and not args.dry_run:
        cards2, sources2 = load_cards(root)
        plans_after = [plan_card(cards2[cid], cards2, sources2) for cid in old
                       if cid in cards2]
    non_idempotent = [p["card_id"] for p in plans_after if p["changed"]]
    report = {"mode": "apply" if args.apply else "dry-run",
              "old_cards": len(old), "plans": len(plans),
              "changed_cards": len(changed), "selected": len(selected),
              "applied_cards": len(to_apply),
              "high_relations": sum(len(p["high"]) for p in selected),
              "visible_links": sum(len(p["body_additions"]) for p in selected),
              "queue": len(queue),
              "types": {t: sum(1 for p in selected for r in p["high"]
                               if r["relation_type"] == t)
                        for t in sorted({r["relation_type"] for p in selected for r in p["high"]})},
              "pilot": args.pilot, "full": args.full,
              "non_idempotent": non_idempotent, "backup": backup,
              "rollback_dir": str(rollback_dir) if to_apply else None,
              "selected_cards": [p["card_id"] for p in selected]}
    (P5D / "backfill-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else json.dumps(report, ensure_ascii=False))
    return 0 if not non_idempotent else 1


if __name__ == "__main__":
    sys.exit(main())
