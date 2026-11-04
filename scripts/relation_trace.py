#!/usr/bin/env python3
"""P5-C relation-path retrieval + outfit lookup (read-only; no card writes).

Capabilities:
- depth-limited typed relation paths (<=3) over migrated card relations and
  structured P5 relation candidates; excludes low confidence; marks design/
  co-occurrence edges as non-factual; dedupes IDs; returns real IDs, SRC and
  evidence/confidence.
- character brief -> complete look (reuses LOOK cards, not a new composer).
- garment -> related outfits.
- rationale paths, conflicts, look prompts, Look Bible approved anchors.

Usage:
  python3 scripts/relation_trace.py --start GAR-0015 --max-depth 3 --json
  python3 scripts/relation_trace.py --character "1770s 法国沙龙女主人" --json
  python3 scripts/relation_trace.py --garment GAR-0015 --json
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
P5 = ROOT / "11-验收/P5"
REL_RE = re.compile(
    r"target=([^;]+); type=([^;]+); direction=([^;]+); evidence=([^;]+); "
    r"confidence=([^;]+); source_ids=([^;]*); rule=([^;']+)")
ALLOWED_TYPES = {"appears_in_look", "uses_material", "may_have_part",
                 "ensemble_with", "context_includes", "in_style",
                 "look_appears_in_scene", "claim_supported_by",
                 "style_interpretation"}
FACTUAL_TYPES = {"claim_supported_by", "context_includes", "in_style"}


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
        cards[cid] = {"id": cid, "path": str(path.relative_to(root)),
                      "meta": meta, "body": body or ""}
    sources = {}
    for path in sorted((Path(root) / "04-来源").glob("SRC-*.md")):
        sid = path.name.split("-", 2)[0] + "-" + path.name.split("-", 2)[1]
        sources[sid] = {"id": sid, "path": str(path.relative_to(root)),
                        "stem": path.stem, "name_zh": path.stem}
    return cards, sources


def load_corrections(root=ROOT):
    path = Path(root) / "reports/P5B-RELATION-CORRECTIONS.csv"
    rejected, downgraded = set(), {}
    if not path.exists():
        return rejected, downgraded
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            action = row.get("action")
            text = (row.get("old") or "") + " " + (row.get("new") or "")
            m = re.search(r"target=([^;]+)", text)
            target = m.group(1).strip() if m else ""
            ids = re.findall(r"\b(?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4}\b", text)
            if not target and ids:
                target = ids[-1]
            key = (row.get("card_id"), target, row.get("relation_type"))
            if action == "downgrade_relation":
                cm = re.search(r"confidence=(medium|low)", text)
                downgraded[key] = cm.group(1) if cm else "medium"
            elif action in ("reject_candidate", "remove_relation",
                            "exclude_from_migration"):
                rejected.add(key)
    return rejected, downgraded


def load_relations(root=ROOT):
    cards, sources = load_cards(root)
    rejected, downgraded = load_corrections(root)
    edges = {}
    for cid, card in cards.items():
        for raw in card["meta"].get("relations") or []:
            match = REL_RE.search(str(raw))
            if not match:
                continue
            target, rtype, direction, evidence, confidence, sids, rule = match.groups()
            if rtype not in ALLOWED_TYPES:
                continue
            key = (cid, target, rtype)
            if key in rejected:
                continue
            if key in downgraded:
                confidence = downgraded[key]
            edge = {"from": cid, "to": target, "type": rtype,
                    "direction": direction, "evidence": evidence,
                    "confidence": confidence,
                    "source_ids": [s for s in sids.split(",") if s],
                    "rule": rule, "origin": "card",
                    "factual": rtype in FACTUAL_TYPES and confidence == "high"}
            edges[(cid, target, rtype, confidence)] = edge
    candidates = P5 / "RELATION-CANDIDATES.csv"
    if candidates.exists():
        with candidates.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                key = (row.get("subject_id"), row.get("object_id"),
                       row.get("relation_type"))
                if row.get("relation_type") not in ALLOWED_TYPES:
                    continue
                if key in rejected:
                    continue
                confidence = row.get("confidence")
                if key in downgraded:
                    confidence = downgraded[key]
                if confidence == "low":
                    continue
                edge = {"from": row.get("subject_id"),
                        "to": row.get("object_id"),
                        "type": row.get("relation_type"),
                        "direction": "outgoing", "evidence": row.get("evidence"),
                        "confidence": confidence,
                        "source_ids": [s for s in (row.get("source_ids") or "").split(";") if s],
                        "rule": row.get("rule_id"), "origin": "candidate",
                        "factual": row.get("relation_type") in FACTUAL_TYPES and confidence == "high"}
                edges[key + (confidence,)] = edge
    return list(edges.values()), cards, sources


def relation_paths(start, edges, max_depth=3, factual_only=False, limit=12):
    adjacency = {}
    for edge in edges:
        if factual_only and not edge["factual"]:
            continue
        for a, b in ((edge["from"], edge["to"]), (edge["to"], edge["from"])):
            adjacency.setdefault(a, []).append((b, edge))
    paths = []
    def walk(node, path, visited, depth):
        if depth > 0 and len(path) <= max_depth:
            paths.append(list(path))
        if depth >= max_depth:
            return
        for nxt, edge in adjacency.get(node, []):
            if nxt in visited:
                continue
            walk(nxt, path + [{"id": nxt, "edge": edge}], visited | {nxt}, depth + 1)
    walk(start, [], {start}, 0)
    # Prefer type-diverse paths; dedupe by node sequence.
    seen = set()
    unique = []
    for path in paths:
        ids = tuple([start] + [step["id"] for step in path])
        if ids in seen:
            continue
        seen.add(ids)
        unique.append(path)
    def score(path):
        types = [step["edge"]["type"] for step in path]
        factual = sum(1 for step in path if step["edge"]["factual"])
        diversity = len(set(types))
        return (factual, diversity, -len(path))
    unique.sort(key=score, reverse=True)
    result = []
    for path in unique[:limit]:
        steps = []
        for step in path:
            edge = step["edge"]
            steps.append({"from": edge["from"], "to": edge["to"],
                          "target": step["id"], "relation_type": edge["type"],
                          "confidence": edge["confidence"],
                          "evidence": edge["evidence"],
                          "factual": edge["factual"],
                          "origin": edge["origin"],
                          "source_ids": edge["source_ids"]})
        result.append({"depth": len(steps), "path": steps})
    return result


def resolve_items(items, cards, sources):
    out = []
    for cid in items:
        card = cards.get(cid)
        source = sources.get(cid)
        out.append({"id": cid,
                    "path": card["path"] if card else source["path"] if source else None,
                    "name_zh": (card["meta"].get("name_zh") if card else
                                source["name_zh"] if source else None),
                    "evidence": (card["meta"].get("evidence_status") if card else
                                 "source" if source else "unknown")})
    return out


def load_approved_anchors(look_bible):
    if not look_bible:
        return {}
    path = Path(look_bible)
    if not path.exists():
        return {"error": "not found"}
    data = json.loads(path.read_text(encoding="utf-8"))
    anchors = data.get("approved_anchors") or {}
    if "looks" in data:
        merged = {}
        for look in data.get("looks") or []:
            merged.update(look.get("approved_anchors") or {})
        anchors = merged or anchors
    return anchors


def look_summary(card, cards, sources):
    meta = card["meta"]
    items = resolve_items(meta.get("look_items") or [], cards, sources)
    conflicts = []
    for key in ("不适用条件", "适用条件"):
        m = re.search(r"## %s\n(.*?)(?=\n## |\Z)" % key, card["body"], re.S)
        if m and key == "不适用条件":
            text = " ".join(m.group(1).split())
            if text:
                conflicts.append(text[:300])
    return {"look_id": card["id"], "path": card["path"],
            "name_zh": meta.get("name_zh"),
            "role": meta.get("look_role"),
            "items": items,
            "prompt_image": meta.get("prompt_en"),
            "prompt_negative": meta.get("negative_prompt_en"),
            "continuity_lock": meta.get("continuity_lock"),
            "conflicts": conflicts,
            "evidence": meta.get("evidence_status"),
            "source_ids": meta.get("source_ids") or []}


def character_looks(query, cards, sources, max_results=3):
    terms = [t for t in re.split(r"\s+", query.lower()) if t]
    found = []
    for cid, card in cards.items():
        if card["meta"].get("type") != "look":
            continue
        hay = " ".join(str(card["meta"].get(k) or "") for k in
                       ("look_role", "name_zh", "name_en", "subcategory")) + " " + card["body"]
        score = sum(1 for term in terms if term in hay.lower())
        if score:
            found.append((score, cid, card))
    found.sort(key=lambda x: (-x[0], x[1]))
    return [look_summary(card, cards, sources) for _, _, card in found[:max_results]]


def garment_looks(garment_id, cards, sources):
    rows = []
    for cid, card in cards.items():
        if card["meta"].get("type") != "look":
            continue
        if garment_id in (card["meta"].get("look_items") or []):
            rows.append(look_summary(card, cards, sources))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="start card ID for relation path trace")
    parser.add_argument("--character", help="character brief / role text")
    parser.add_argument("--garment", help="garment ID -> related outfits")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--factual-only", action="store_true")
    parser.add_argument("--look-bible", help="optional look-bible.json for approved anchors")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    edges, cards, sources = load_relations()
    output = {"limits": {"max_depth": min(args.max_depth, 3),
                         "low_confidence": "filtered",
                         "design_edges": "included and marked factual=false; "
                                         "use --factual-only to exclude",
                         "engine": "read-only; no card writes"}}
    if args.start:
        if args.start not in cards and args.start not in sources:
            print("ERROR: unknown start ID", file=sys.stderr)
            return 2
        paths = relation_paths(args.start, edges, max_depth=min(args.max_depth, 3),
                               factual_only=args.factual_only)
        output["start"] = args.start
        output["paths"] = paths
        seen_ids = []
        for path in paths:
            for step in path["path"]:
                if step["target"] not in seen_ids:
                    seen_ids.append(step["target"])
        output["related_ids"] = seen_ids
        output["related"] = [{"id": cid,
                              "path": cards[cid]["path"] if cid in cards else
                                      sources[cid]["path"] if cid in sources else None,
                              "name_zh": cards[cid]["meta"].get("name_zh") if cid in cards else
                                         sources[cid]["name_zh"] if cid in sources else None}
                             for cid in seen_ids]
    if args.character:
        output["character_looks"] = character_looks(args.character, cards, sources)
    if args.garment:
        output["garment_looks"] = garment_looks(args.garment, cards, sources)
    if args.look_bible:
        output["approved_anchors"] = load_approved_anchors(args.look_bible)
    text = json.dumps(output, ensure_ascii=False, indent=2)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
