#!/usr/bin/env python3
"""R1.2-A portable Obsidian config installer.

Default is dry-run. Only explicit --apply writes .obsidian/{app,graph}.json.
- app: preserve every user key; add only missing recommended userIgnoreFilters.
- graph: preserve every existing user key; fill only missing recommended keys.
- never touches themes/plugins/hotkeys/workspace/appearance.
- --apply backs up the whole .obsidian directory first.
- --restore BACKUP restores app.json/graph.json from a backup and leaves other files.
- idempotent, auditable JSON/diff; no credentials/absolute paths in templates.

Usage:
  python3 scripts/obsidian_config.py --dry-run
  python3 scripts/obsidian_config.py --diff
  python3 scripts/obsidian_config.py --apply
  python3 scripts/obsidian_config.py --restore /tmp/obsidian-config-backup-...
  python3 scripts/obsidian_config.py --scope-report
"""
import argparse
import collections
import difflib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "config/obsidian"
DEFAULT_IGNORES = ["11-验收/", "reports/", "projects/", "docs/", "tests/",
                   "skills/", ".dsh/", "TASKS/", "TASKS.md", "AGENTS.md",
                   "visuals/", "images/", "assets/", "templates/",
                   "00-系统/视觉规范.md", "00-系统/数据字典-v1.5-扩展.md"]
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
CODE = re.compile(r"`[^`\n]*`")
FENCE = re.compile(r"(?ms)^```.*?^```")


def load_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default if default is not None else {}


def template(name):
    return load_json(TPL / name, {})


def merge_app(current, recommended):
    merged = dict(current or {})
    user = list(merged.get("userIgnoreFilters") or [])
    for item in recommended.get("userIgnoreFilters") or []:
        if item not in user:
            user.append(item)
    merged["userIgnoreFilters"] = user
    return merged


def merge_graph(current, recommended):
    merged = dict(current or {})
    for key, value in recommended.items():
        if key not in merged:
            merged[key] = value
    return merged


def diff_text(name, before, after):
    a = json.dumps(before, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    b = json.dumps(after, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    return "\n".join(difflib.unified_diff(a, b, fromfile=name + " (current)",
                                          tofile=name + " (recommended-merged)",
                                          lineterm=""))


def backup_obsidian(obsidian):
    dest = Path("/tmp") / ("obsidian-config-backup-" + time.strftime("%Y%m%d-%H%M%S-") + str(time.time_ns() % 1000000))
    shutil.copytree(obsidian, dest)
    return dest


def restore(backup, obsidian):
    backup = Path(backup)
    for name in ("app.json", "graph.json"):
        src = backup / name if (backup / name).exists() else backup / ".obsidian" / name
        if src.exists():
            obsidian.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, obsidian / name)
    return 0


def scope_stats(root=ROOT, ignores=None):
    """Obsidian-scope stats: file nodes after userIgnoreFilters; links resolved by
    path/stem/frontmatter id; code examples ignored."""
    ignores = ignores or DEFAULT_IGNORES
    files = []
    for path in sorted(Path(root).rglob("*.md")):
        rel = str(path.relative_to(root)).replace(os.sep, "/")
        if any(rel == i or rel.startswith(i) for i in ignores):
            continue
        if rel.startswith(".obsidian/"):
            continue
        files.append((rel, path))
    by_path, by_stem, by_id = {}, {}, {}
    nodes = {}
    for rel, path in files:
        key = rel[:-3]
        nodes[key] = path
        by_path[key] = key
        by_stem.setdefault(path.stem, key)
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        fm = m.group(1) if m else ""
        for line in fm.splitlines():
            if line.startswith("id:"):
                cid = line.split(":", 1)[1].strip().strip("'\"")
                by_id.setdefault(cid, key)
                break
    edges = {k: set() for k in nodes}
    unresolved = collections.Counter()
    code = re.compile(r"`[^`\n]*`")
    fence = re.compile(r"(?ms)^```.*?^```")
    for rel, path in files:
        key = rel[:-3]
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        body = m.group(2) if m else text
        for raw in WIKILINK.findall(code.sub("", fence.sub("", body))):
            target = raw.split("|")[0].split("#")[0].strip().replace("\\", "/")
            if target.endswith(".md"):
                target = target[:-3]
            dst = (by_path.get(target) or by_path.get(target.split("/")[-1]) or
                   by_stem.get(target) or by_stem.get(target.split("/")[-1]) or
                   by_id.get(target))
            if not dst:
                for token in re.findall(
                        r"(?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-[A-Za-z0-9-]+", target):
                    if token in by_id:
                        dst = by_id[token]
                        break
            if dst and dst != key and dst in edges:
                edges[key].add(dst)
                edges[dst].add(key)
            elif not dst:
                unresolved[target] += 1
    zero = [key for key, links in edges.items() if not links]
    seen, components = set(), 0
    for key in edges:
        if key in seen:
            continue
        components += 1
        stack = [key]
        seen.add(key)
        while stack:
            cur = stack.pop()
            for nxt in edges[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return {"nodes": len(nodes), "zero_degree": len(zero),
            "components": components, "unresolved_wikilinks": len(unresolved),
            "unresolved_samples": unresolved.most_common(10),
            "edges_directed": sum(len(v) for v in edges.values()) // 2}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=str(ROOT))
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--restore", metavar="BACKUP")
    parser.add_argument("--scope-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.vault).resolve()
    if args.scope_report:
        data = scope_stats(root)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    obsidian = root / ".obsidian"
    if args.restore:
        return restore(args.restore, obsidian)
    app_path = obsidian / "app.json"
    graph_path = obsidian / "graph.json"
    current_app = load_json(app_path, {})
    current_graph = load_json(graph_path, {})
    new_app = merge_app(current_app, template("app.recommended.json"))
    new_graph = merge_graph(current_graph, template("graph.recommended.json"))
    diff = []
    if new_app != current_app:
        diff.append(diff_text("app.json", current_app, new_app))
    if new_graph != current_graph:
        diff.append(diff_text("graph.json", current_graph, new_graph))
    if args.diff:
        print("\n".join(diff) if diff else "no differences")
    backup = None
    if args.apply and (new_app != current_app or new_graph != current_graph):
        if not args.no_backup:
            backup = str(backup_obsidian(obsidian))
        obsidian.mkdir(parents=True, exist_ok=True)
        if new_app != current_app:
            app_path.write_text(json.dumps(new_app, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
        if new_graph != current_graph:
            graph_path.write_text(json.dumps(new_graph, ensure_ascii=False, indent=2) + "\n",
                                  encoding="utf-8")
    report = {"mode": "apply" if args.apply else "dry-run",
              "vault": str(root), "app_changed": new_app != current_app,
              "graph_changed": new_graph != current_graph,
              "user_ignore_filters": new_app.get("userIgnoreFilters") or [],
              "changed": bool(new_app != current_app or new_graph != current_graph),
              "backup": backup,
              "untouched": ["appearance.json", "core-plugins.json",
                            "community-plugins.json", "hotkeys.json",
                            "workspace.json", "themes/", "plugins/"]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
