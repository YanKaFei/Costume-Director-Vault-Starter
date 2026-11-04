#!/usr/bin/env python3
"""Validate P5-B Agent E2E evidence: all five criteria, no intermediate PASS."""
import json
import re
import sys
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
    tool_calls = [r for r in rows if r.get("type") == "tool_call"]
    tool_results = [r for r in rows if r.get("type") == "tool_result"]
    skill_calls = [r for r in tool_calls if r.get("tool") == "skill"]
    bash_calls = [r for r in tool_calls if r.get("tool") == "bash"]
    bash_query = []
    for call in bash_calls:
        cmd = json.dumps(call.get("input", {}), ensure_ascii=False)
        if "query.py" in cmd and "--relation-type" in cmd:
            bash_query.append(call)
    completed_results = [r for r in tool_results
                         if r.get("status") in ("completed", "success")]
    finals = [r.get("text", "") for r in rows if r.get("type") == "final"]
    final = finals[-1] if finals else ""
    turn_ends = [r for r in rows if r.get("type") == "status" and
                 r.get("phase") == "turn_end"]
    completed_turn = bool(turn_ends and
                          (turn_ends[-1].get("reason") or {}).get("kind") == "completed")
    ids = sorted(set(ID_RE.findall(final)))
    criteria = {
        "skill_call": bool(skill_calls),
        "tools_executed": bool(bash_query and completed_results),
        "result_success": bool(completed_results),
        "turn_end_completed": completed_turn,
        "complete_user_output": bool(len(final.strip()) >= 120 and
                                     len(ids) >= 2),
    }
    return {"criteria": criteria, "ids": ids, "final_chars": len(final),
            "skill_calls": len(skill_calls), "bash_calls": len(bash_calls),
            "query_tool_calls": len(bash_query),
            "completed_tool_results": len(completed_results),
            "final_preview": final[:500],
            "pass": all(criteria.values())}


def main():
    summary = {"official": {}, "overlay": {}}
    for mode in ("official", "overlay"):
        for case in ("RQ1", "RQ2", "RQ3"):
            events = BASE / mode / (case + ".events.jsonl")
            result = validate(load(events))
            (BASE / mode / (case + ".validation.json")).write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
            summary[mode][case] = {k: result[k] for k in
                                   ("pass", "criteria", "ids", "final_chars",
                                    "skill_calls", "query_tool_calls")}
    (BASE / "validation-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if all(v["pass"] for mode in summary.values()
                    for v in mode.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
