#!/usr/bin/env python3
"""Validate P3.6 Agent-native end-to-end runs under 11-验收/P3.6/e2e/T01..T10.

Checks per case:
  - events.jsonl exists and is valid JSONL;
  - a real skill tool call to costume-director occurred;
  - at least one real python3 scripts/(query|recommend|workflow).py bash call occurred;
  - final answer text exists and the turn completed (not quota/error);
  - all GAR/STR/MAT/STY/PRD/LOOK/SCN/SRC IDs in the answer exist in the vault;
  - all SRC IDs resolve to source cards;
  - case-specific honesty/continuity/prompt requirements;
  - T07 additionally validates the same-session follow-up events file.

Writes validation.json in each case directory and SUMMARY.md at the e2e root.
Exit 0 iff every case passes.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E2E = ROOT / "11-验收/P3.6/e2e"
sys.path.insert(0, str(ROOT / "scripts"))
import costume_lib as lib  # noqa: E402

ID_RE = re.compile(r"\b(?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4}\b")
CASE_TITLES = {
    "T01": "Macbeth Lady - three-stage contemporary theatre A/B/C",
    "T02": "Macbeth - three-stage A/B/C",
    "T03": "1930s Shanghai rainy-night journalist + continuity",
    "T04": "ER nurse night shift",
    "T05": "space-station mechanic",
    "T06": "Ghana-UK wedding groom",
    "T07": "same-session modification",
    "T08": "insufficient historical evidence",
    "T09": "historical+cyberpunk conflict request",
    "T10": "multi-scene continuity + image/video prompts",
}


def load_cards():
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    sources = {lib.get_str(card["meta"], "id"): card for card in cards
               if lib.norm_text(card["meta"].get("type")) == "source"}
    return by_id, sources


def read_events(path):
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            events.append({"type": "invalid-json", "raw": line[:200]})
    return events


def tool_calls(events):
    return [event for event in events if event.get("type") == "tool_call"]


def final_text(events):
    finals = [event.get("text", "") for event in events
              if event.get("type") == "final"]
    return finals[-1].strip() if finals else ""


def turn_completed(events):
    ends = [event for event in events if event.get("type") == "status" and
            event.get("phase") == "turn_end"]
    if not ends:
        return False
    reason = ends[-1].get("reason", {})
    return reason.get("kind") == "completed"


def command_texts(events):
    texts = []
    for call in tool_calls(events):
        data = call.get("input") or {}
        if isinstance(data, dict):
            for key in ("command", "cmd"):
                if isinstance(data.get(key), str):
                    texts.append(data[key])
    return texts


def skill_called(events):
    for call in tool_calls(events):
        if call.get("tool") == "skill":
            name = (call.get("input") or {}).get("name", "")
            if "costume-director" in name:
                return True
    return False


def script_calls(events):
    calls = []
    for text in command_texts(events):
        for script in ("query.py", "recommend.py", "workflow.py"):
            if script in text:
                calls.append(script)
    return sorted(set(calls))


def check_case(case, by_id, sources):
    directory = E2E / case
    events = read_events(directory / "events.jsonl")
    answer = ""
    answer_path = directory / "answer.md"
    if answer_path.exists():
        answer = answer_path.read_text(encoding="utf-8")
    if not answer:
        answer = final_text(events)
    checks = {}
    reasons = []
    checks["events_file"] = bool(events)
    if not events:
        reasons.append("missing/empty events.jsonl")
    checks["skill_called"] = skill_called(events)
    if not checks["skill_called"]:
        reasons.append("no costume-director skill call in events")
    scripts = script_calls(events)
    checks["script_calls"] = scripts
    if not scripts:
        reasons.append("no query/recommend/workflow script call in events")
    checks["answer_present"] = bool(answer.strip())
    if not answer.strip():
        reasons.append("empty final answer")
    checks["turn_completed"] = turn_completed(events)
    if not checks["turn_completed"]:
        reasons.append("turn did not complete cleanly (quota/error)")
    ids = sorted(set(ID_RE.findall(answer)))
    missing_ids = [cid for cid in ids if cid not in by_id and cid not in sources]
    checks["ids"] = ids
    checks["missing_ids"] = missing_ids
    if missing_ids:
        reasons.append("answer cites unknown/fabricated IDs: %s" % ", ".join(missing_ids))
    src_ids = [cid for cid in ids if cid.startswith("SRC-")]
    missing_src = [sid for sid in src_ids if sid not in sources]
    checks["src_resolvable"] = bool(src_ids) and not missing_src
    if not src_ids:
        reasons.append("answer cites no SRC-* provenance")
    if missing_src:
        reasons.append("unresolvable SRC IDs: %s" % ", ".join(missing_src))
    checks["source_ids"] = src_ids
    lowered = answer.lower()
    if case in ("T08", "T09"):
        honest_words = ("缺口", "不足", "没有", "unknown", "证据", "冲突", "拒绝",
                        "不能", "警告", "风险")
        checks["honesty"] = any(word in lowered for word in honest_words)
        if not checks["honesty"]:
            reasons.append("case requires an explicit gap/conflict/refusal statement")
    if case == "T10":
        checks["continuity"] = any(word in lowered for word in
                                   ("连续", "continuity", "状态", "anchor", "锚点"))
        checks["prompts"] = ("prompt" in lowered or "生图" in answer or
                             "image" in lowered)
        if not checks["continuity"]:
            reasons.append("T10 answer lacks continuity statement")
        if not checks["prompts"]:
            reasons.append("T10 answer lacks image/video prompt")
    if case == "T07":
        follow_events = read_events(directory / "events-followup.jsonl")
        checks["followup_events"] = bool(follow_events)
        checks["followup_skill"] = skill_called(follow_events)
        checks["followup_scripts"] = script_calls(follow_events)
        checks["same_session"] = False
        session_ids = [event.get("sessionId") for event in events
                       if event.get("type") == "session"]
        follow_ids = [event.get("sessionId") for event in follow_events
                      if event.get("type") == "session"]
        if session_ids and follow_ids and session_ids[0] == follow_ids[0]:
            checks["same_session"] = True
        if not checks["followup_events"]:
            reasons.append("T07 missing same-session follow-up events")
        if not checks["same_session"]:
            reasons.append("T07 follow-up did not reuse the same session id")
    checks["pass"] = not reasons
    return {"case": case, "title": CASE_TITLES[case], "checks": checks,
            "reasons": reasons, "answer_chars": len(answer)}


def main():
    by_id, sources = load_cards()
    results = [check_case(case, by_id, sources) for case in sorted(CASE_TITLES)]
    for result in results:
        path = E2E / result["case"] / "validation.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    passed = [result for result in results if result["checks"]["pass"]]
    lines = ["# P3.6 Agent-native E2E — 10 real headless runs", "",
             "- Command: real `dsh --profile headless --json` sessions in the Vault",
             "- Checker: `scripts/check_skill_e2e.py`", ""]
    lines.append("| Case | Scenario | Skill | Scripts | IDs/SRC | Answer | PASS/FAIL |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for result in results:
        checks = result["checks"]
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            result["case"], result["title"],
            "yes" if checks.get("skill_called") else "no",
            ", ".join(checks.get("script_calls") or []) or "none",
            "yes" if checks.get("src_resolvable") and not checks.get("missing_ids") else "no",
            "yes" if checks.get("answer_present") else "no",
            "PASS" if checks.get("pass") else "FAIL"))
        if result["reasons"]:
            lines.append("|  | _%s_ |  |  |  |  |  |" % "; ".join(result["reasons"]))
    lines.append("")
    lines.append("- PASS: %d / %d" % (len(passed), len(results)))
    lines.append("- FAIL: %d / %d" % (len(results) - len(passed), len(results)))
    (E2E / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS %d/%d" % (len(passed), len(results)))
    for result in results:
        print("%s %s %s" % (result["case"], "PASS" if result["checks"]["pass"] else "FAIL",
                            "; ".join(result["reasons"])))
    return 0 if len(passed) == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
