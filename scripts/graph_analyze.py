#!/usr/bin/env python3
"""graph_analyze.py - P5-A read-only link/graph diagnosis for the Costume Director Vault.

Scope (per task-59): scan Markdown under content/source/navigation dirs only:
  00-系统/ 01-服装单品/ 02-结构细节/ 03-材质纹样/ 04-来源/ 05-风格体系/
  06-时代地域/ 07-剧情场景/ 09-造型组合/ 10-提示词模板/ + root README.md/AGENTS.md
Excluded: .git, projects/, 11-验收/, reports/, tests/, docs/, .dsh/, skills/, .obsidian,
          sandbox-* copies (regenerable), __pycache__.

It distinguishes:
  * visible Obsidian wikilinks ([[...]] in body)  -> "visible" edges
  * machine/typed frontmatter relations (source_ids, look_items, look_scene,
    key_garments, superseded_by, canonical_id)    -> "typed" edges
  * navigation documents vs content/source cards

Outputs:
  --csv PATH   node baseline CSV (default reports/P5-GRAPH-BASELINE.csv)
  --json PATH  optional machine-readable summary
  stdout       human summary

Never writes cards; only CSV/JSON paths given.
"""

import argparse
import collections
import glob
import json
import os
import re
import sys

try:
    import yaml
except Exception as exc:  # pragma: no cover
    print("PyYAML required: %s" % exc, file=sys.stderr)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCAN_DIRS = [
    "00-系统",
    "01-服装单品",
    "02-结构细节",
    "03-材质纹样",
    "04-来源",
    "05-风格体系",
    "06-时代地域",
    "07-剧情场景",
    "09-造型组合",
    "10-提示词模板",
]
ROOT_FILES = ["README.md", "AGENTS.md"]
EXCLUDE_DIR_NAMES = {".git", "projects", "11-验收", "reports", "tests", "docs", ".dsh",
                     "skills", ".obsidian", "__pycache__"}
CONTENT_TYPES = {"garment", "garment_part", "material", "pattern", "style",
                 "period_region", "scene", "look"}
ID_RE = re.compile(r"^((?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-[A-Z0-9][A-Z0-9-]*)$", re.I)
CODE_SPAN = re.compile(r"`[^`\n]*`")
FENCED = re.compile(r"(?ms)^```.*?^```")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
ID_IN_TEXT = re.compile(r"\b(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4}\b", re.I)


def iter_markdown():
    seen = set()
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames
                           if x not in EXCLUDE_DIR_NAMES and not x.startswith("sandbox-")]
            for name in sorted(filenames):
                if not name.endswith(".md"):
                    continue
                p = os.path.join(dirpath, name)
                if p in seen:
                    continue
                seen.add(p)
                yield p
    for name in ROOT_FILES:
        p = os.path.join(ROOT, name)
        if os.path.isfile(p) and p not in seen:
            seen.add(p)
            yield p


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, text
    try:
        fm = yaml.safe_load(parts[1])
    except Exception:
        return None, parts[2]
    return (fm if isinstance(fm, dict) else None), parts[2]


def role_of(path, fm):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    t = (fm or {}).get("type")
    if t == "source":
        return "source"
    if t in CONTENT_TYPES:
        return "content"
    if rel.startswith("06-时代地域/书籍研究/"):
        return "research"
    if rel.startswith(("00-系统/", "10-提示词模板/", "04-来源/")) or rel in ("README.md", "AGENTS.md"):
        return "navigation"
    return "unknown"


def node_key(path, fm):
    if fm and fm.get("id"):
        return str(fm["id"])
    return os.path.splitext(os.path.basename(path))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="", help="vault root to scan (default: script's project root)")
    ap.add_argument("--csv", default="", help="CSV output path (default: <root>/reports/P5-GRAPH-BASELINE.csv)")
    ap.add_argument("--json", default="")
    args = ap.parse_args()
    global ROOT
    if args.root:
        ROOT = os.path.abspath(args.root)
    if not args.csv:
        args.csv = os.path.join(ROOT, "reports", "P5-GRAPH-BASELINE.csv")

    nodes = {}
    order = []
    used_keys = set()
    for path in iter_markdown():
        text = open(path, encoding="utf-8", errors="replace").read()
        fm, body = parse_frontmatter(text)
        key = node_key(path, fm)
        rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        if key in used_keys:
            base = os.path.splitext(rel)[0]
            key = base
            i = 2
            while key in used_keys:
                key = "%s_%d" % (base, i)
                i += 1
        used_keys.add(key)
        links = []
        visible_body = CODE_SPAN.sub("", FENCED.sub("", body))
        for raw in WIKILINK_RE.findall(visible_body):
            target = raw.split("|")[0].split("#")[0].strip()
            if target:
                links.append(target)
        nodes[key] = {
            "id": key,
            "path": rel,
            "role": role_of(path, fm),
            "type": (fm or {}).get("type") or ("navigation" if role_of(path, fm) == "navigation" else "none"),
            "fm": fm or {},
            "body": body,
            "link_targets_raw": links,
            "link_occurrences": len(links),
        }
        order.append(key)

    # ---- resolution index ----
    by_stem = {}
    by_lower = {}
    by_id = {}
    for key, n in nodes.items():
        stem = os.path.splitext(os.path.basename(n["path"]))[0]
        by_stem.setdefault(stem, key)
        by_lower.setdefault(stem.lower(), key)
        # Index by actual frontmatter id, including EXAMPLE/letter-suffixed IDs.
        node_id = str((n.get("fm") or {}).get("id") or "")
        if node_id:
            by_id[node_id.upper()] = key
        m = ID_RE.match(key)
        if m:
            by_id[key.upper()] = key
    # include nav doc stems pointing to a node with same stem

    def resolve_target(target):
        t = target.strip().strip("[]").replace("\\", "/")
        if t.endswith(".md"):
            t = t[:-3]
        if t in by_stem:
            return by_stem[t]
        if t.lower() in by_lower:
            return by_lower[t.lower()]
        m = ID_RE.match(t.split("/")[-1])
        if m:
            key = by_id.get(t.split("/")[-1].upper())
            if key:
                return key
        # try ID prefix inside text
        found = ID_IN_TEXT.findall(t)
        if found:
            # last ID-looking token
            ids = re.findall(r"((?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4})", t, re.I)
            if ids and ids[-1].upper() in by_id:
                return by_id[ids[-1].upper()]
        return None

    visible_out = collections.defaultdict(set)   # key -> set(target keys)
    visible_out_occ = collections.Counter()
    visible_in = collections.defaultdict(set)
    unresolved_links = collections.Counter()
    nav_edges = 0
    semantic_edges = 0
    edge_kind_visible = collections.Counter()

    for key in order:
        n = nodes[key]
        for target in n["link_targets_raw"]:
            dst = resolve_target(target)
            if dst is None or dst == key:
                if dst is None:
                    unresolved_links[target] += 1
                continue
            if dst in visible_out[key]:
                continue
            visible_out[key].add(dst)
            visible_out_occ[key] += 1
            visible_in[dst].add(key)
            if n["role"] == "navigation" or n["role"] == "research":
                nav_edges += 1
                edge_kind_visible["navigation"] += 1
            else:
                semantic_edges += 1
                edge_kind_visible["semantic"] += 1

    # ---- typed (machine) relations ----
    typed_out = collections.defaultdict(dict)  # src -> {dst: kinds set}
    typed_in = collections.defaultdict(dict)
    typed_pairs = []  # (src,dst,kind)
    typed_unresolved = []

    def add_typed(src, dst, kind):
        if src == dst or dst is None:
            return
        typed_out[src].setdefault(dst, set()).add(kind)
        typed_in[dst].setdefault(src, set()).add(kind)
        typed_pairs.append((src, dst, kind))

    for key in order:
        n = nodes[key]
        fm = n["fm"]
        if not fm:
            continue
        for sid in fm.get("source_ids") or []:
            dst = by_id.get(str(sid).upper())
            if dst is None:
                typed_unresolved.append((key, "source_ids", str(sid)))
                continue
            add_typed(key, dst, "source_ids")
        if n["type"] == "look":
            for cid in fm.get("look_items") or []:
                dst = by_id.get(str(cid).upper())
                if dst is None:
                    typed_unresolved.append((key, "look_items", str(cid)))
                else:
                    add_typed(key, dst, "look_items")
            for scn in fm.get("look_scene") or []:
                dst = by_id.get(str(scn).upper())
                if dst is None:
                    typed_unresolved.append((key, "look_scene", str(scn)))
                else:
                    add_typed(key, dst, "look_scene")
        if n["type"] == "period_region":
            for cid in fm.get("key_garments") or []:
                dst = by_id.get(str(cid).upper())
                if dst is None:
                    typed_unresolved.append((key, "key_garments", str(cid)))
                else:
                    add_typed(key, dst, "key_garments")
        for field in ("superseded_by", "canonical_id"):
            val = fm.get(field)
            if val:
                dst = by_id.get(str(val).upper())
                if dst is None:
                    typed_unresolved.append((key, field, str(val)))
                else:
                    add_typed(key, dst, field)

    # ---- degrees / metrics ----
    def deg_in(key):
        return len(visible_in[key]), len(typed_in[key])

    def deg_out(key):
        return len(visible_out[key]), len(typed_out[key])

    semantic_component = {}
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    semantic_nodes = [k for k in order if nodes[k]["role"] in ("content", "source")]
    for k in semantic_nodes:
        parent[k] = k
    semantic_edge_pairs = set()
    for k in semantic_nodes:
        for dst in visible_out.get(k, set()):
            if dst in parent:
                semantic_edge_pairs.add((k, dst))
        for dst in typed_out.get(k, {}):
            if dst in parent:
                semantic_edge_pairs.add((k, dst))
    for a, b in semantic_edge_pairs:
        union(a, b)

    comp_members = collections.defaultdict(list)
    for k in semantic_nodes:
        comp_members[find(k)].append(k)
    comps = sorted(comp_members.values(), key=len, reverse=True)
    comp_id = {}
    for i, members in enumerate(comps, 1):
        for m in members:
            comp_id[m] = i

    # ---- source isolation causes ----
    def source_reason(key):
        n = nodes[key]
        vin, tin = deg_in(key)
        vout, tout = deg_out(key)
        incoming_content_visible = sum(1 for s in visible_in[key]
                                       if nodes[s]["role"] == "content")
        incoming_content_typed = sum(1 for s in typed_in[key]
                                     if nodes[s]["role"] == "content")
        incoming_nav_visible = sum(1 for s in visible_in[key]
                                   if nodes[s]["role"] in ("navigation", "research"))
        incoming_look_visible = sum(1 for s in visible_in[key]
                                    if nodes[s]["type"] == "look")
        if vin == 0 and tin == 0:
            kind = (n["fm"].get("source_kind") or "").lower()
            sid_num = key.upper()
            if re.match(r"^SRC-00[6][0-9]$", sid_num) or sid_num in {
                    "SRC-0061", "SRC-0062", "SRC-0063", "SRC-0064", "SRC-0065",
                    "SRC-0066", "SRC-0067", "SRC-0068", "SRC-0069"}:
                return "book_source_no_card_integration", False
            if kind in ("academic_reference", "reference_work", "vocabulary"):
                return "background_or_dictionary_uncited", False
            if vout > 0:
                return "outbound_only_no_incoming", False
            return "isolated_source", True
        if incoming_content_typed > 0 and incoming_content_visible == 0 and vin == 0:
            return "source_ids_only_no_visible_link", False
        if incoming_content_visible > 0:
            return "linked_visible_from_content", False
        if incoming_content_typed > 0 and incoming_content_visible == 0:
            return "source_ids_only_mixed", False
        if incoming_nav_visible > 0 and incoming_content_visible == 0 and incoming_content_typed == 0:
            return "navigation_only", False
        if incoming_look_visible > 0 and incoming_content_typed == 0:
            return "look_card_only", False
        return "linked_other", False

    # ---- typed-without-visible-link analysis ----
    typed_no_visible = []
    by_kind_no_visible = collections.Counter()
    for src, dst, kind in typed_pairs:
        if dst not in visible_out.get(src, set()):
            typed_no_visible.append((src, dst, kind))
            by_kind_no_visible[kind] += 1

    # source_ids pairs
    source_ids_pairs = [(s, d) for s, d, k in typed_pairs if k == "source_ids"]
    source_ids_no_visible = [(s, d) for s, d in source_ids_pairs
                             if d not in visible_out.get(s, set())]
    cards_with_source_ids = {s for s, d in source_ids_pairs}
    cards_with_source_ids_no_visible = {s for s, d in source_ids_no_visible}
    sources_cited_typed = {d for s, d in source_ids_pairs}
    sources_cited_visible = {d for s, d in source_ids_pairs if d in visible_out.get(s, set())}

    # ---- component stats ----
    def comp_types(members):
        return dict(collections.Counter(nodes[m]["role"] for m in members))

    comp_rows = []
    for i, members in enumerate(comps, 1):
        types_ = comp_types(members)
        visible_links_inside = sum(1 for a, b in semantic_edge_pairs
                                   if comp_id.get(a) == i)
        comp_rows.append({"component": i, "size": len(members), "roles": types_,
                          "visible_edges_inside": visible_links_inside})
    largest = comp_rows[0] if comp_rows else {"size": 0}
    independent_topic = [
        c for c in comp_rows[1:]
        if c["roles"].get("content", 0) >= 1 and c["roles"].get("source", 0) >= 1
        and c["visible_edges_inside"] >= 2
    ]

    # ---- zero-link / degree stats by role ----
    role_stats = {}
    for role in ("content", "source", "navigation", "research", "unknown"):
        keys = [k for k in order if nodes[k]["role"] == role]
        if not keys:
            continue
        role_stats[role] = {
            "nodes": len(keys),
            "zero_visible": sum(1 for k in keys if deg_in(k)[0] + deg_out(k)[0] == 0),
            "zero_total": sum(1 for k in keys if deg_in(k)[0] + deg_out(k)[0]
                              + deg_in(k)[1] + deg_out(k)[1] == 0),
            "only_in_visible": sum(1 for k in keys if deg_in(k)[0] > 0 and deg_out(k)[0] == 0),
            "only_out_visible": sum(1 for k in keys if deg_out(k)[0] > 0 and deg_in(k)[0] == 0),
            "bidirectional_visible": sum(1 for k in keys if deg_in(k)[0] > 0 and deg_out(k)[0] > 0),
            "with_source_ids": sum(1 for k in keys if nodes[k]["fm"].get("source_ids")),
            "source_ids_no_visible": sum(
                1 for k in keys
                if nodes[k]["fm"].get("source_ids")
                and any(d not in visible_out.get(k, set())
                        for d in [x for x in typed_out.get(k, {})]
                        if nodes[d]["role"] == "source")),
        }

    # ---- rows ----
    rows = []
    for key in order:
        n = nodes[key]
        vin, tin = deg_in(key)
        vout, tout = deg_out(key)
        fm = n["fm"]
        if n["role"] == "source":
            reason, isolated = source_reason(key)
        elif n["role"] == "content":
            if comp_id.get(key, -1) and len(comps[comp_id[key] - 1]) == 1:
                reason = "isolated_content"
            elif vout == 0 and vin == 0:
                reason = "content_zero_visible"
            elif tout == 0 and tin == 0:
                reason = "visible_only_content"
            else:
                reason = "linked_content"
        elif n["role"] in ("navigation", "research"):
            reason = "navigation_doc" if vout or vin else "navigation_unlinked"
        else:
            reason = "unclassified"
        rows.append({
            "id": key,
            "type": n["type"],
            "role": n["role"],
            "path": n["path"],
            "in": vin,
            "out": vout,
            "source_ids": len(fm.get("source_ids") or []),
            "wikilinks": n["link_occurrences"],
            "component": comp_id.get(key, 0),
            "component_size": len(comps[comp_id[key] - 1]) if key in comp_id else 0,
            "in_typed": tin,
            "out_typed": tout,
            "zero_visible": int(vin + vout == 0),
            "zero_total": int(vin + vout + tin + tout == 0),
            "reason": reason,
        })

    # ---- top isolates ----
    def isolate_sort(r):
        priority = {"content": 0, "source": 1, "unknown": 2, "navigation": 3, "research": 4}
        return (r["zero_total"] == 0, priority.get(r["role"], 9), -r["source_ids"], r["id"])
    top_isolates = [r for r in rows if r["zero_total"]] [:30]
    top_isolates.sort(key=isolate_sort)

    typed_by_kind = collections.Counter(k for _s, _d, k in typed_pairs)
    singleton_comps = [c for c in comps if len(c) == 1]
    singleton_kinds = collections.Counter(
        (nodes[c[0]]["fm"].get("source_kind") or "none") for c in singleton_comps)
    isolation_groups = {}
    for r in rows:
        if r["role"] != "source":
            continue
        if r["reason"] in ("source_ids_only_no_visible_link", "source_ids_only_mixed"):
            continue
        sid = r["id"]
        bucket = "SRC-0%sxx" % (sid.split("-")[1][:1]) if sid.startswith("SRC-0") else "other"
        isolation_groups.setdefault(r["reason"], collections.Counter())[bucket] += 1
    visible_by_role_pair = collections.Counter()
    for src in order:
        for dst in visible_out.get(src, set()):
            visible_by_role_pair[(nodes[src]["role"], nodes[dst]["role"])] += 1

    summary = {
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": ROOT,
        "scanned_files": len(order),
        "nodes_by_role": dict(collections.Counter(nodes[k]["role"] for k in order)),
        "nodes_by_type": dict(collections.Counter(nodes[k]["type"] for k in order)),
        "wikilink_occurrences": sum(nodes[k]["link_occurrences"] for k in order),
        "resolved_visible_edges": sum(len(v) for v in visible_out.values()),
        "nav_visible_edges": nav_edges,
        "semantic_visible_edges": semantic_edges,
        "unresolved_wikilinks": dict(unresolved_links.most_common(20)),
        "typed_edges": len(typed_pairs),
        "typed_unresolved": len(typed_unresolved),
        "typed_without_visible": len(typed_no_visible),
        "typed_without_visible_by_kind": dict(by_kind_no_visible),
        "typed_by_kind": dict(typed_by_kind),
        "visible_by_role_pair": {"%s->%s" % k: v for k, v in visible_by_role_pair.items()},
        "source_ids_pairs": len(source_ids_pairs),
        "source_ids_without_visible": len(source_ids_no_visible),
        "cards_with_source_ids": len(cards_with_source_ids),
        "cards_with_source_ids_without_any_visible_source": len(cards_with_source_ids_no_visible),
        "sources_cited_typed": len(sources_cited_typed),
        "sources_cited_visible": len(sources_cited_visible),
        "role_stats": role_stats,
        "semantic_nodes": len(semantic_nodes),
        "components": len(comps),
        "largest_component": {"size": largest.get("size"), "roles": largest.get("roles")},
        "component_rows_top": comp_rows[:8],
        "singleton_components": len(singleton_comps),
        "singleton_component_source_kinds": dict(singleton_kinds),
        "isolation_groups_by_src_bucket": {k: dict(v) for k, v in isolation_groups.items()},
        "component_size_histogram": dict(collections.Counter(len(c) for c in comps)),
        "components_with_content_and_source": sum(
            1 for c in comp_rows if c["roles"].get("content", 0) >= 1 and c["roles"].get("source", 0) >= 1),
        "independent_topic_components": independent_topic[:20],
        "source_reasons": dict(collections.Counter(r["reason"] for r in rows if r["role"] == "source")),
        "top_isolates": top_isolates[:20],
    }

    os.makedirs(os.path.dirname(args.csv) or ".", exist_ok=True)
    with open(args.csv, "w", encoding="utf-8", newline="") as fh:
        writer = __import__("csv").DictWriter(
            fh, fieldnames=["id", "type", "role", "path", "in", "out", "source_ids",
                            "wikilinks", "component", "component_size", "in_typed",
                            "out_typed", "zero_visible", "zero_total", "reason"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, ensure_ascii=False, indent=1)

    print(json.dumps({k: summary[k] for k in (
        "scanned_files", "nodes_by_role", "nodes_by_type", "wikilink_occurrences",
        "resolved_visible_edges", "nav_visible_edges", "semantic_visible_edges",
        "unresolved_wikilinks", "typed_edges", "typed_without_visible",
        "typed_without_visible_by_kind", "source_ids_pairs",
        "source_ids_without_visible", "cards_with_source_ids",
        "cards_with_source_ids_without_any_visible_source",
        "sources_cited_typed", "sources_cited_visible", "role_stats",
        "semantic_nodes", "components", "largest_component",
        "component_size_histogram", "components_with_content_and_source",
        "source_reasons")}, ensure_ascii=False, indent=1))
    print("\nCSV:", args.csv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
