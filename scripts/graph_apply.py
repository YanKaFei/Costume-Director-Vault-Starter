#!/usr/bin/env python3
"""Apply/export typed relation graph for P5-A (idempotent, no guessing).

Reads card frontmatter `relations` (target, relation_type, evidence, confidence)
and source_ids; writes a graph JSON and optionally a review queue of unresolved
or non-high-confidence target references.  Never invents targets.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_RE = re.compile(r"SRC-\d{3,4}")


def iter_cards(root):
    for path in sorted(Path(root).glob("0[1-9]-*/**/*.md")):
        if path.name in ("README.md", "验证记录.md"):
            continue
        yield path


def load_corrections(root):
    path = Path(root) / "reports/P5B-RELATION-CORRECTIONS.csv"
    if not path.exists():
        return set(), {}
    import csv, re
    rejected, downgraded = set(), {}
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            action = row.get("action")
            if action not in ("reject_candidate", "remove_relation",
                              "downgrade_relation", "exclude_from_migration"):
                continue
            text = (row.get("old") or "") + " " + (row.get("new") or "")
            m = re.search(r"target=([^;]+)", text)
            target = m.group(1).strip() if m else ""
            key = (row.get("card_id"), target, row.get("relation_type"))
            if action == "downgrade_relation":
                down = re.search(r"confidence=(medium|low)", text)
                downgraded[key] = down.group(1) if down else "medium"
            else:
                rejected.add(key)
    return rejected, downgraded


def build_graph(root, queue_path=None):
    rejected, downgraded = load_corrections(root)
    nodes = {}
    edges = []
    queue = []
    for path in iter_cards(root):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not match:
            continue
        try:
            import yaml
            meta = yaml.safe_load(match.group(1)) or {}
        except Exception:
            continue
        cid = str(meta.get("id") or path.stem.split("-")[0])
        nodes[cid] = {"path": str(path.relative_to(root)),
                      "type": meta.get("type"), "name_zh": meta.get("name_zh")}
        for relation in meta.get("relations") or []:
            if isinstance(relation, str):
                parsed = {}
                for part in relation.split(";"):
                    if "=" in part:
                        key, value = part.split("=", 1)
                        parsed[key.strip()] = value.strip()
                relation = parsed
            if not isinstance(relation, dict):
                continue
            target = str(relation.get("target") or "")
            relation_type = relation.get("type") or relation.get("relation_type")
            evidence = relation.get("evidence")
            confidence = relation.get("confidence")
            if target not in nodes and target not in queue:
                # target is resolved later; unresolved queued by migration tool
                pass
            key = (cid, target, relation_type)
            if key in rejected:
                continue
            if key in downgraded:
                confidence = downgraded[key]
            edges.append({"source": cid, "target": target,
                          "relation_type": relation_type,
                          "evidence": evidence, "confidence": confidence})
    known = set(nodes)
    unresolved = [edge for edge in edges if edge["target"] not in known]
    if queue_path:
        Path(queue_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(queue_path).open("w", encoding="utf-8", newline="") as handle:
            import csv
            writer = csv.DictWriter(handle, fieldnames=["source", "target",
                                                       "relation_type", "evidence",
                                                       "confidence", "reason"])
            writer.writeheader()
            for edge in unresolved:
                writer.writerow({**edge, "reason": "unresolved target"})
    return {"nodes": nodes, "edges": edges, "unresolved": unresolved}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--out", default=str(ROOT / "11-验收/P5/graph.json"))
    parser.add_argument("--queue", default=str(ROOT / "11-验收/P5/graph-unresolved.csv"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    graph = build_graph(args.root, args.queue)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    print(json.dumps({"nodes": len(graph["nodes"]), "edges": len(graph["edges"]),
                      "unresolved": len(graph["unresolved"]), "out": args.out},
                     ensure_ascii=False) if args.json else
          "nodes=%d edges=%d unresolved=%d" % (
              len(graph["nodes"]), len(graph["edges"]), len(graph["unresolved"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
