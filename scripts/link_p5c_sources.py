#!/usr/bin/env python3
"""P5-C source visible fix: exact SRC IDs in the 35 new cards' 来源链接 -> Obsidian links.

- Only the authorized P5-C cards (LOOK-0024..0035, STY-0011..0015,
  GAR-0088..0091, STR-0027..0035, MAT-0015..0019).
- Only exact SRC IDs already present in the `## 来源链接` section; map to the real
  `04-来源/SRC-xxxx-*.md` filename. No guessing, no new source IDs.
- Preserves YAML/source_ids/facts; converts the visible token to [[stem]].
- Backup before writes, idempotent, JSON report with before/after visibility.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [f"LOOK-{n:04d}" for n in range(24, 36)] + \
          [f"STY-{n:04d}" for n in range(11, 16)] + \
          [f"GAR-{n:04d}" for n in range(88, 92)] + \
          [f"STR-{n:04d}" for n in range(27, 36)] + \
          [f"MAT-{n:04d}" for n in range(15, 20)]
SRC_SECTION = re.compile(r"(?ms)^## 来源链接\s*\n(.*?)(?=^## |\Z)")
SRC_ID = re.compile(r"SRC-\d{3,4}")
WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
CODE_SPAN = re.compile(r"`[^`\n]*`")
FENCED = re.compile(r"(?ms)^```.*?^```")


def visible_text(text):
    """Remove fenced and inline code before checking Obsidian-visible links."""
    return CODE_SPAN.sub("", FENCED.sub("", text))


def visible_links(text):
    return WIKILINK.findall(visible_text(text))


def load_cards(root=ROOT):
    cards = {}
    for path in sorted(Path(root).glob("0[1-9]-*/**/*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        if not match:
            continue
        fm = match.group(1)
        cid_match = re.search(r"^id:\s*(\S+)", fm, re.M)
        if cid_match:
            cards[cid_match.group(1).strip()] = {"path": path, "text": text,
                                                 "meta": fm}
    return cards


def source_map(root=ROOT):
    mapping = {}
    for path in sorted((Path(root) / "04-来源").glob("SRC-*.md")):
        sid = "-".join(path.name.split("-", 2)[:2])
        mapping.setdefault(sid, path.stem)
    return mapping


def plan_card(card, sources):
    text = card["text"]
    match = SRC_SECTION.search(text)
    if not match:
        return {"changed": False, "before": 0, "after": 0,
                "replaced": [], "missing": [], "reason": "no 来源链接 section"}
    section = match.group(0)
    # Normalise code-wrapped links (invalid Obsidian wikilinks) to real links.
    normalized = re.sub(r"`(\[\[[^\]]+\]\])`", r"\1", section)
    visible_section = visible_text(normalized)
    linked = set()
    for link in WIKILINK.findall(visible_section):
        for sid in SRC_ID.findall(link):
            linked.add(sid)
    ids = []
    for sid in SRC_ID.findall(section):
        if sid not in ids:
            ids.append(sid)
    new_section = normalized
    replaced = []
    missing = []
    for sid in ids:
        if sid in linked:
            continue
        stem = sources.get(sid)
        if not stem:
            missing.append(sid)
            continue
        # Replace only the visible token occurrence, not source_ids/YAML.
        token = re.compile(r"(?<!\[\[)\b%s\b(?!-[^\]]*\]\])" % re.escape(sid))
        new_section, count = token.subn("[[%s]]" % stem, new_section, count=1)
        if count:
            replaced.append({"source_id": sid, "stem": stem})
    new_section = re.sub(r"`(\[\[[^\]]+\]\])`", r"\1", new_section)
    if new_section == section:
        return {"changed": False, "before": len(ids),
                "after": len([s for s in ids if s in linked]),
                "replaced": [], "missing": missing, "reason": "already linked"}
    new_text = text[:match.start()] + new_section + text[match.end():]
    return {"changed": True, "new_text": new_text,
            "before": len(ids), "after": len(ids), "replaced": replaced,
            "missing": missing}


def run_backup(dest):
    return subprocess.run([sys.executable, "scripts/backup_restore.py", "backup",
                           "--dest", str(dest), "--json"],
                          cwd=str(ROOT), capture_output=True, text=True)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root)
    cards = load_cards(root)
    sources = source_map(root)
    targets = [cid for cid in TARGETS if cid in cards]
    before_total = after_total = 0
    changed = []
    results = []
    for cid in targets:
        plan = plan_card(cards[cid], sources)
        before_total += plan["before"]
        after_total += plan["after"]
        item = {"card_id": cid, "path": str(cards[cid]["path"].relative_to(root)),
                "changed": plan["changed"], "before": plan["before"],
                "after": plan["after"], "replaced": plan["replaced"],
                "missing": plan["missing"]}
        results.append(item)
        if plan["changed"]:
            changed.append((cid, plan, item))
    backup = None
    if changed and not args.dry_run:
        dest = Path("/tmp") / ("p5c-link-backup-" + time.strftime("%Y%m%d-%H%M%S"))
        proc = run_backup(dest)
        if proc.returncode != 0:
            print("ERROR backup failed: %s" % proc.stderr[-500:], file=sys.stderr)
            return 2
        backup = str(dest)
        for cid, plan, item in changed:
            cards[cid]["path"].write_text(plan["new_text"], encoding="utf-8")
    report = {"mode": "dry-run" if args.dry_run else "apply",
              "targets": len(targets), "changed_cards": len(changed),
              "source_ids_before": before_total, "source_ids_after": after_total,
              "visible_rate_before": round(before_total and 0.0, 3),
              "visible_rate_after": round(after_total / before_total, 3) if before_total else 0.0,
              "cards": results, "backup": backup,
              "missing_sources": sorted({m for r in results for m in r["missing"]})}
    # rate before: count original linked IDs in section; plan before is section ID
    # count, not linked count, so recompute visible linked tokens before/after.
    def linked_count(cards_after):
        total = linked = 0
        for cid in targets:
            text = (cards[cid]["path"].read_text(encoding="utf-8")
                    if cards_after else cards[cid]["text"])
            match = SRC_SECTION.search(text)
            if not match:
                continue
            section = match.group(0)
            ids = list(dict.fromkeys(SRC_ID.findall(section)))
            total += len(ids)
            linked += sum(1 for sid in ids if any(sid in link for link in visible_links(section)))
        return total, linked
    if args.dry_run:
        total_before = linked_before = 0
        total_after = linked_after = 0
        for cid in targets:
            match = SRC_SECTION.search(cards[cid]["text"])
            if not match:
                continue
            section = match.group(0)
            ids = list(dict.fromkeys(SRC_ID.findall(section)))
            total_before += len(ids)
            linked_before += sum(1 for sid in ids if any(sid in link for link in visible_links(section)))
            plan = plan_card(cards[cid], sources)
            text2 = plan.get("new_text", cards[cid]["text"])
            match2 = SRC_SECTION.search(text2)
            if match2:
                sec2 = match2.group(0)
                ids2 = list(dict.fromkeys(SRC_ID.findall(sec2)))
                total_after += len(ids2)
                linked_after += sum(1 for sid in ids2 if any(sid in link for link in visible_links(sec2)))
    else:
        total_before = after_total  # not used; visible before recorded from results
        total_after, linked_after = linked_count(cards_after=True)
        total_before, linked_before = 0, 0
        for cid in targets:
            # original text unavailable after write; use plan result before as IDs
            pass
    report["source_visible_before"] = {"linked": linked_before if args.dry_run else None,
                                       "total": total_before if args.dry_run else before_total}
    report["source_visible_after"] = {"linked": linked_after,
                                      "total": total_after}
    if args.dry_run:
        report["visible_rate_before"] = round(linked_before / total_before, 3) if total_before else 0.0
        report["visible_rate_after"] = round(linked_after / total_after, 3) if total_after else 0.0
    else:
        report["visible_rate_before"] = None
        report["visible_rate_after"] = round(linked_after / total_after, 3) if total_after else 0.0
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
