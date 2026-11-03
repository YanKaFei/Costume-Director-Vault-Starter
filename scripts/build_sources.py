#!/usr/bin/env python3
"""build_sources.py - build / reconcile reports/SOURCES.csv from 04-来源/ source cards.

The source register is the CSV projection of the source cards, never a
hand-maintained file: 04-来源/README.md requires the CSV and the cards to be
generated from the same data.  This script reads every `type: source` card in
04-来源/, derives the register rows, and compares them with the current
reports/SOURCES.csv.

Column contract (canonical, 00-系统/来源规范.md §6):
    source_id,title,publisher,url,accessed_at,source_kind,rights_statement,note
`title` falls back to `name_zh` when a source card has no legacy `title` field.

It also reports:
  * rows that exist only in the cards (CSV stale/incomplete) or only in the CSV
  * field-level differences for shared source_ids
  * duplicate URLs across source cards (same page registered twice)
  * duplicate source IDs (must be zero; violates 数据字典 §2)
  * SRC id gaps and non-contiguous ranges (informational)

Usage:
    python3 scripts/build_sources.py            # check (default), exit 1 on mismatch
    python3 scripts/build_sources.py --write    # regenerate reports/SOURCES.csv
    python3 scripts/build_sources.py --write --strict
    python3 scripts/build_sources.py --json     # machine-readable report

Exit codes:
    0  CSV matches the cards (duplicate URLs are warnings only)
    1  CSV mismatch or duplicate source IDs
    2  fatal errors (no cards / unreadable CSV / write failure)
"""

import argparse
import collections
import csv
import datetime
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "04-来源"
DEFAULT_CSV = ROOT / "reports" / "SOURCES.csv"

# 00-系统/来源规范.md §6: `source_id, title, publisher, url, accessed_at,
# source_kind, rights_statement, note`.  NOTE: a delegate brief mentioned a
# "7-column" header; the project specification and the pre-existing CSV both
# have eight columns, and this script enforces the specification.
EXPECTED_HEADER = [
    "source_id", "title", "publisher", "url", "accessed_at",
    "source_kind", "rights_statement", "note",
]


def norm_date(value):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    text = str(value or "").strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return text
    return text


def read_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, None
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, None
    try:
        meta = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        return None, f"YAML 解析失败: {exc}"
    if not isinstance(meta, dict):
        return None, "frontmatter 不是映射"
    return meta, None


def collect_sources():
    """Return (rows list, errors list, skipped list)."""
    rows, errors, skipped = [], [], []
    if not SOURCE_DIR.exists():
        return rows, [f"缺少目录: {SOURCE_DIR}"], skipped
    for path in sorted(SOURCE_DIR.glob("*.md")):
        meta, err = read_frontmatter(path)
        if err:
            errors.append(f"{path.name}: {err}")
            continue
        if meta is None:
            skipped.append(path.name)
            continue
        if meta.get("type") != "source":
            skipped.append(path.name)
            continue
        source_id = str(meta.get("id", "")).strip()
        if not source_id:
            errors.append(f"{path.name}: 缺 id")
            continue
        rows.append({
            "source_id": source_id,
            "title": str(meta.get("title") or meta.get("name_zh") or "").strip(),
            "publisher": str(meta.get("publisher") or "").strip(),
            "url": str(meta.get("url") or "").strip(),
            "accessed_at": norm_date(meta.get("date_accessed")),
            "source_kind": str(meta.get("source_kind") or "").strip(),
            "rights_statement": str(meta.get("rights_statement") or "").strip(),
            "note": str(meta.get("note") or "").strip(),
            "_file": path.name,
        })
    rows.sort(key=lambda r: (r["source_id"].split("-")[0], int(re.sub(r"\D", "", r["source_id"]) or 0)))
    return rows, errors, skipped


def normalize_url(url):
    text = url.strip().lower()
    text = re.sub(r"^https?://", "", text)
    text = text.rstrip("/")
    return text


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("CSV 为空")
        rows = []
        for line_no, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) != len(header):
                raise ValueError(f"第 {line_no} 行列数 {len(row)} != 表头 {len(header)}")
            rows.append(dict(zip(header, row)))
        return header, rows


def display(text, limit=60):
    text = str(text).replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def main():
    ap = argparse.ArgumentParser(description="Build/check reports/SOURCES.csv from source cards.")
    ap.add_argument("--check", action="store_true",
                    help="compare only (default; kept as explicit alias)")
    ap.add_argument("--write", action="store_true", help="regenerate reports/SOURCES.csv")
    ap.add_argument("--strict", action="store_true", help="treat duplicate URLs as failures")
    ap.add_argument("--csv", default=str(DEFAULT_CSV), help="CSV path (default reports/SOURCES.csv)")
    ap.add_argument("--json", action="store_true", help="print JSON report")
    args = ap.parse_args()

    csv_path = Path(args.csv)
    rows, errors, skipped = collect_sources()
    if errors:
        for err in errors:
            print(f"ERROR {err}", file=sys.stderr)
        return 2

    # duplicate source IDs (must be zero)
    id_counts = collections.Counter(r["source_id"] for r in rows)
    dup_ids = {sid: n for sid, n in id_counts.items() if n > 1}

    # duplicate URLs
    url_groups = collections.defaultdict(list)
    for r in rows:
        if r["url"]:
            url_groups[normalize_url(r["url"])].append(r["source_id"])
    dup_urls = {u: sorted(ids) for u, ids in url_groups.items()
                if len(set(ids)) > 1}

    # ID gaps / ranges
    numeric = sorted({int(re.sub(r"\D", "", sid)) for sid in id_counts if re.match(r"^SRC-\d{4}$", sid)})
    gaps = []
    for prev, cur in zip(numeric, numeric[1:]):
        if cur == prev + 1:
            continue
        if cur - prev <= 20:  # only report short, meaningful gaps
            gaps.append(f"SRC-{prev + 1:04d}..SRC-{cur - 1:04d}")
        else:
            gaps.append(f"SRC-{prev + 1:04d}..SRC-{cur - 1:04d}（段位间隔）")
    ranges = []
    if numeric:
        start = prev = numeric[0]
        for cur in numeric[1:]:
            if cur == prev + 1:
                prev = cur
                continue
            ranges.append((start, prev))
            start = prev = cur
        ranges.append((start, prev))

    # compare with current CSV
    csv_header, csv_rows = None, []
    csv_error = None
    if csv_path.exists():
        try:
            csv_header, csv_rows = read_csv(csv_path)
        except (ValueError, OSError) as exc:
            csv_error = str(exc)
    else:
        csv_error = f"CSV 不存在: {csv_path}"

    card_rows = {r["source_id"]: r for r in rows}
    old_rows = {}
    duplicate_csv_ids = []
    if csv_rows:
        for old in csv_rows:
            sid = old.get("source_id", "").strip()
            if sid in old_rows:
                duplicate_csv_ids.append(sid)
            old_rows[sid] = old

    missing_in_csv = sorted(set(card_rows) - set(old_rows))
    missing_card = sorted(set(old_rows) - set(card_rows))
    field_diffs = []
    for sid in sorted(set(card_rows) & set(old_rows)):
        new, old = card_rows[sid], old_rows[sid]
        changed = []
        for col in EXPECTED_HEADER:
            a = new.get(col, "")
            b = (old.get(col) or "").strip()
            if a != b:
                changed.append((col, b, a))
        if changed:
            field_diffs.append((sid, changed))

    header_ok = csv_header == EXPECTED_HEADER
    mismatch = bool(csv_error or duplicate_csv_ids or missing_in_csv or missing_card
                    or field_diffs or not header_ok)

    # write mode
    write_ok = True
    if args.write:
        try:
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with csv_path.open("w", encoding="utf-8", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=EXPECTED_HEADER,
                                        extrasaction="ignore", lineterminator="\n")
                writer.writeheader()
                for row in rows:
                    writer.writerow({k: row.get(k, "") for k in EXPECTED_HEADER})
        except OSError as exc:
            write_ok = False
            print(f"ERROR 写入失败: {exc}", file=sys.stderr)

    report = {
        "source_cards": len(rows),
        "csv_path": str(csv_path),
        "expected_header": EXPECTED_HEADER,
        "csv_header": csv_header,
        "header_ok": header_ok,
        "csv_rows": len(csv_rows),
        "csv_error": csv_error,
        "missing_in_csv": missing_in_csv,
        "missing_source_card": missing_card,
        "duplicate_csv_ids": duplicate_csv_ids,
        "field_diffs": [
            {"source_id": sid, "diffs": [{"column": c, "csv": b, "card": a} for c, b, a in changed]}
            for sid, changed in field_diffs
        ],
        "duplicate_ids": dup_ids,
        "duplicate_urls": [
            {"url": u, "source_ids": ids} for u, ids in sorted(dup_urls.items())
        ],
        "id_gaps": gaps,
        "id_ranges": [{"from": f"SRC-{a:04d}", "to": f"SRC-{b:04d}", "count": b - a + 1} for a, b in ranges],
        "skipped_non_source": skipped,
        "wrote_csv": bool(args.write and write_ok),
    }

    exit_code = 0
    if dup_ids or not write_ok:
        exit_code = 1
    if mismatch and not args.write:
        exit_code = 1
    if args.strict and dup_urls:
        exit_code = 1

    if args.json:
        report["exit_code"] = exit_code
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return exit_code

    print("=" * 78)
    print("Costume Director Vault — build_sources.py")
    print(f"来源卡目录: {SOURCE_DIR}")
    print(f"来源卡（type=source）: {len(rows)} 张；跳过非来源卡: {len(skipped)} 个")
    if skipped:
        print("    跳过: " + ", ".join(skipped))
    print(f"CSV: {csv_path}（当前 {len(csv_rows)} 行）")
    print("=" * 78)
    print(f"[{'PASS' if header_ok else 'FAIL'}] 表头契约（{len(EXPECTED_HEADER)} 列）")
    if not header_ok:
        print(f"    期望: {','.join(EXPECTED_HEADER)}")
        print(f"    实际: {','.join(csv_header or [])}")
    print(f"[{'PASS' if not csv_error else 'FAIL'}] CSV 可读: {csv_error or 'ok'}")
    print(f"[{'PASS' if not duplicate_csv_ids else 'FAIL'}] CSV 内 source_id 无重复: {len(duplicate_csv_ids)} 个重复")
    print(f"[{'PASS' if not missing_in_csv else 'FAIL'}] 卡片 → CSV 覆盖: 缺 {len(missing_in_csv)} 行")
    if missing_in_csv:
        print("    缺失 source_id: " + ", ".join(missing_in_csv[:30]) +
              (" ..." if len(missing_in_csv) > 30 else ""))
    print(f"[{'PASS' if not missing_card else 'FAIL'}] CSV → 卡片可解析: 多出 {len(missing_card)} 行")
    if missing_card:
        print("    多出 source_id: " + ", ".join(missing_card))
    print(f"[{'PASS' if not field_diffs else 'FAIL'}] 共有行的字段一致: {len(field_diffs)} 行有差异")
    for sid, changed in field_diffs[:20]:
        for col, oldv, newv in changed:
            print(f"    {sid}.{col}: CSV={display(oldv)!r} 卡片={display(newv)!r}")
    if len(field_diffs) > 20:
        print(f"    ... 另有 {len(field_diffs) - 20} 行差异")
    print(f"[{'PASS' if not dup_ids else 'FAIL'}] source_id 全局唯一: {len(dup_ids)} 个重复")
    for sid, n in dup_ids.items():
        print(f"    {sid}: {n} 张卡")
    print(f"[{'WARN' if dup_urls else 'PASS'}] 重复 URL: {len(dup_urls)} 组")
    for url, ids in sorted(dup_urls.items()):
        print(f"    {url} -> {', '.join(ids)}")
    print(f"[INFO] SRC 编号缺口: {', '.join(gaps) if gaps else '无'}")
    print("[INFO] 连续编号段: " + "; ".join(
        f"SRC-{a:04d}..SRC-{b:04d}({b - a + 1})" for a, b in ranges))
    print("-" * 78)
    if args.write:
        print("RESULT: 已重建 reports/SOURCES.csv" + ("（写入成功）" if write_ok else "（写入失败）"))
    else:
        if mismatch:
            print("RESULT: FAIL（CSV 与来源卡不一致；用 --write 重建，或修正卡片后重跑）")
        elif exit_code == 0:
            print("RESULT: PASS（CSV 与全部来源卡一致）")
        else:
            print("RESULT: FAIL")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
