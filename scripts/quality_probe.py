#!/usr/bin/env python3
"""quality_probe.py - reproducible P2.5 probes for query.py / recommend.py quality.

This is an AUDIT helper, not an acceptance gate: exit code 0 only means the
probes ran, not that quality is good.  Read the printed table / JSON to judge.

What it does
------------
1. Runs the 25 query.py probes used in reports/P2.5-AUDIT.md and prints hit
   counts + IDs (flags 0-hit probes).
2. Runs recommend.py on every 11-验收/P2.5-案例/inputs/C*.json and on the 10
   T-scenario inputs, printing exit codes, look counts and warning counts.
3. Re-runs the P2.5 crash probe: historical requests for 1940s/1950s/1960s/
   1970s often return exit 1 (KeyError: 'evidence'); the probe records this.

Usage:
    python3 scripts/quality_probe.py              # human readable
    python3 scripts/quality_probe.py --json       # machine readable

No network access is performed (URL audit lives in the QA report).
"""

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

QUERY_PROBES = [
    ("P01", ["旗袍"]), ("P02", ["和服"]), ("P03", ["风衣"]), ("P04", ["蕾丝"]),
    ("P05", ["朋克"]), ("P06", ["徽章"]), ("P07", ["1930s", "上海"]),
    ("P08", ["立领", "盘扣"]), ("P09", ["蕾丝", "晚装"]), ("P10", ["丝绸", "和服"]),
    ("P11", ["--phrase", "stand-up collar"]),
    ("P12", ["--phrase", "right side fastening"]),
    ("P13", ["--type", "garment", "--category", "footwear"]),
    ("P14", ["--style-tag", "noir"]),
    ("P15", ["--period", "1930s", "--region", "shanghai"]),
    ("P16", ["--type", "source", "--evidence", "verified"]),
    ("P17", ["--type", "look"]), ("P18", ["--category", "accessory"]),
    ("P19", ["--type", "garment", "--category", "outerwear"]),
    ("P20", ["spacesuit"]), ("P21", ["Mughal"]), ("P22", ["mourning", "jewelry"]),
    ("P23", ["--match", "any", "旗袍", "太空服"]),
    ("P24", ["--type", "pattern"]), ("P25", ["雨", "夜", "调查"]),
]

# historical-mode crash probe inputs (period -> expected crash)
CRASH_PERIODS = ["1940s", "1950s", "1960s", "1970s"]
CRASH_TEMPLATE = {
    "character": {"name": "Sid", "occupation": "punk musician",
                  "economic_status": "low", "arc": "gig"},
    "scene": {"scene_id": "S7", "time": "night", "weather": "dry",
              "action": "stage performance", "location": "london club"},
    "period": "1970s", "region": "london", "season": "autumn",
    "art_direction": "realist period drama", "lighting": "cool",
    "camera": "medium shot", "budget": "medium", "fidelity_mode": "historical",
    "tool": "midjourney",
    "state": {"wetness": "dry", "damage": "none", "dirt": "none"},
}


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def query_probes():
    rows = []
    for pid, args in QUERY_PROBES:
        proc = run([PY, "scripts/query.py"] + args + ["--limit", "5", "--json"])
        try:
            hits = json.loads(proc.stdout)
        except Exception:
            hits = []
        rows.append({
            "probe": pid,
            "args": args,
            "exit": proc.returncode,
            "hits": len(hits),
            "ids": [h.get("id") for h in hits],
        })
    return rows


def recommend_probes():
    rows = []
    patterns = ["11-验收/测试输入/T*.json", "11-验收/P2.5-案例/inputs/C*.json"]
    files = []
    for pattern in patterns:
        files.extend(sorted(glob.glob(os.path.join(ROOT, pattern))))
    for path in files:
        proc = run([PY, "scripts/recommend.py", path, "--json"])
        rec = None
        try:
            rec = json.loads(proc.stdout)
        except Exception:
            pass
        rows.append({
            "input": os.path.basename(path),
            "exit": proc.returncode,
            "looks": len((rec or {}).get("looks") or []),
            "warnings": len((rec or {}).get("warnings") or []),
            "error": (proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""),
        })
    # crash probe
    tmpdir = tempfile.mkdtemp(prefix="p25probe_")
    for period in CRASH_PERIODS:
        payload = json.loads(json.dumps(CRASH_TEMPLATE))
        payload["period"] = period
        path = os.path.join(tmpdir, "hist_%s.json" % period)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)
        proc = run([PY, "scripts/recommend.py", path, "--json"])
        rows.append({
            "input": "historical_%s_test.json" % period,
            "exit": proc.returncode,
            "looks": None,
            "warnings": None,
            "error": (proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""),
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description="P2.5 quality probes (not an acceptance gate).")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    queries = query_probes()
    recs = recommend_probes()
    if args.json:
        print(json.dumps({"query_probes": queries, "recommend_probes": recs},
                         ensure_ascii=False, indent=2))
        return 0
    print("== query.py probes (limit 5) ==")
    for row in queries:
        flag = " <-- 0 HIT" if row["hits"] == 0 else ""
        print("%s exit=%s hits=%d ids=%s%s" % (
            row["probe"], row["exit"], row["hits"], ",".join(row["ids"]), flag))
    zero = [r["probe"] for r in queries if r["hits"] == 0]
    print("0-hit probes: %d/%d %s" % (len(zero), len(queries), zero))
    print("\n== recommend.py probes ==")
    for row in recs:
        print("%-42s exit=%s looks=%s warnings=%s %s" % (
            row["input"], row["exit"], row["looks"], row["warnings"], row["error"]))
    crashes = [r for r in recs if r["exit"] not in (0, 3)]
    print("\nunexpected exits (%d): %s" % (
        len(crashes), [(r["input"], r["exit"]) for r in crashes]))
    print("NOTE: exit 0 = ran; quality must be judged from the printed cases and report.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
