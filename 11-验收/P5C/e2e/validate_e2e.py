#!/usr/bin/env python3
"""Validate P5-C Agent E2E: five criteria, no intermediate PASS."""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
ID_RE = re.compile(r"\b(?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4}\b")


def load(path):
    rows = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def validate(rows):
    calls = [r for r in rows if r.get("type") == "tool_call"]
    results = [r for r in rows if r.get("type") == "tool_result"]
    skill = [r for r in calls if r.get("tool") == "skill"]
    bash = [r for r in calls if r.get("tool") == "bash"]
    trace = []
    for call in bash:
        cmd = json.dumps(call.get("input", {}), ensure_ascii=False)
        if "relation_trace.py" in cmd:
            trace.append(call)
    completed = [r for r in results if r.get("status") in ("completed", "success")]
    finals = [r.get("text", "") for r in rows if r.get("type") == "final"]
    final = finals[-1] if finals else ""
    ends = [r for r in rows if r.get("type") == "status" and r.get("phase") == "turn_end"]
    turn_end = bool(ends and (ends[-1].get("reason") or {}).get("kind") == "completed")
    ids = sorted(set(ID_RE.findall(final)))
    criteria = {
        "skill_call": bool(skill),
        "tools_executed": bool(trace and completed),
        "result_success": bool(completed),
        "turn_end_completed": turn_end,
        "complete_user_output": bool(len(final.strip()) >= 120 and len(ids) >= 2),
    }
    return {"criteria": criteria, "ids": ids, "final_chars": len(final),
            "skill_calls": len(skill), "trace_tool_calls": len(trace),
            "completed_tool_results": len(completed),
            "final_preview": final[:500], "pass": all(criteria.values())}


def main():
    summary = {"official": {}, "overlay": {}}
    case_sets = {"official": ("RQ1", "RQ2", "RQ3"),
                 "overlay": ("RQ2", "RQ3", "RQ4")}
    for mode in ("official", "overlay"):
        for case in case_sets[mode]:
            result = validate(load(BASE / mode / (case + ".events.jsonl")))
            (BASE / mode / (case + ".validation.json")).write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
            summary[mode][case] = result
    (BASE / "validation-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({m: {k: v["pass"] for k, v in cases.items()}
                      for m, cases in summary.items()}, ensure_ascii=False, indent=2))
    return 0 if all(v["pass"] for cases in summary.values() for v in cases.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
