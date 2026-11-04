#!/usr/bin/env python3
"""Validate R1 official vs overlay Skill E2E runs.

Writes validation-official.json, validation-overlay.json and SUMMARY.md.
Does not modify cards/scripts/skill/profile.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import costume_lib as lib  # noqa: E402

ID_RE = re.compile(r"\b(?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4}\b")
VIS_RE = re.compile(r"\bVIS-\d{4}\b")
CASES = {
    "C01": {
        "title": "PG76299 / English Costume book terms",
        "required": ["76299", "blazer", "waistcoat", "trousers"],
        "coverage": "books",
    },
    "C02": {
        "title": "v1.2 structures STR-0012/13/14",
        "required": ["STR-0012", "STR-0013", "STR-0014"],
        "coverage": "structures",
    },
    "C03": {
        "title": "accessories GAR-0083..0087",
        "required": ["GAR-0083", "GAR-0084", "GAR-0085", "GAR-0086", "GAR-0087"],
        "coverage": "accessories",
    },
    "C04": {
        "title": "outfit composer / full look",
        "required": ["outfit.py", "A", "B", "C"],
        "coverage": "outfit",
    },
    "C05": {
        "title": "bilingual term search",
        "required": ["旗袍", "qipao", "立领", "stand collar", "腰带", "belt"],
        "coverage": "bilingual",
    },
    "C06": {
        "title": "visual index reference",
        "required": ["VIS-0001", "VIS-0003", "VIS-0005", "PRD-0003", "GAR-0001", "STR-0007"],
        "coverage": "visual",
    },
}
SKILL_SCRIPTS = ("query.py", "recommend.py", "workflow.py", "outfit.py")


def read_events(path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            rows.append({"type": "invalid"})
    return rows


def final_text(events):
    finals = [event.get("text", "") for event in events
              if event.get("type") == "final"]
    return finals[-1].strip() if finals else ""


def turn_end(events):
    ends = [event for event in events if event.get("type") == "status" and
            event.get("phase") == "turn_end"]
    return ends[-1].get("reason", {}) if ends else {}


def validate(mode, by_id, sources, vis_ids):
    out = {}
    for case, spec in CASES.items():
        directory = HERE / mode / case
        events = read_events(directory / "events.jsonl")
        answer = ""
        if (directory / "answer.md").exists():
            answer = (directory / "answer.md").read_text(encoding="utf-8")
        if not answer:
            answer = final_text(events)
        checks = {}
        reasons = []
        checks["events"] = bool(events)
        skill = any(event.get("type") == "tool_call" and event.get("tool") == "skill"
                    and "costume-director" in str((event.get("input") or {}).get("name", ""))
                    for event in events)
        checks["skill_called"] = skill
        if not skill:
            reasons.append("no costume-director skill call")
        scripts = []
        for event in events:
            if event.get("type") != "tool_call" or event.get("tool") != "bash":
                continue
            command = (event.get("input") or {}).get("command", "")
            for script in SKILL_SCRIPTS:
                if script in command:
                    scripts.append(script)
        checks["scripts"] = sorted(set(scripts))
        if not scripts:
            reasons.append("no query/recommend/workflow/outfit script call")
        checks["answer"] = bool(answer)
        if not answer:
            reasons.append("empty final answer")
        reason = turn_end(events)
        checks["turn_end"] = reason.get("kind")
        checks["quota_blocked"] = bool(
            reason.get("kind") == "error" or "QUOTA" in json.dumps(reason)
            or "Insufficient Balance" in json.dumps(reason))
        if checks["turn_end"] != "completed":
            reasons.append("turn did not complete: %s" % reason)
        lowered = answer.lower()
        missing_required = [word for word in spec["required"] if word.lower() not in lowered]
        checks["required_terms_missing"] = missing_required
        if missing_required:
            reasons.append("missing required terms: %s" % ", ".join(missing_required))
        ids = sorted(set(ID_RE.findall(answer)))
        checks["ids"] = ids
        missing_ids = [cid for cid in ids if cid not in by_id and cid not in sources]
        checks["missing_ids"] = missing_ids
        if missing_ids:
            reasons.append("unknown/fabricated IDs: %s" % ", ".join(missing_ids))
        srcs = [cid for cid in ids if cid.startswith("SRC-")]
        checks["src_ids"] = srcs
        if not srcs:
            reasons.append("no SRC provenance cited")
        if [sid for sid in srcs if sid not in sources]:
            reasons.append("unresolvable SRC IDs")
        vis = sorted(set(VIS_RE.findall(answer)))
        checks["visual_ids"] = vis
        if case == "C06" and any(vid not in vis_ids for vid in vis):
            reasons.append("unknown VIS id")
        checks["pass"] = not reasons
        out[case] = {"title": spec["title"], "coverage": spec["coverage"],
                     "checks": checks, "reasons": reasons}
    return out


def main():
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(c["meta"], "id"): c for c in cards}
    sources = {lib.get_str(c["meta"], "id"): c for c in cards
               if lib.norm_text(c["meta"].get("type")) == "source"}
    vis_ids = set()
    vis_path = ROOT / "11-验收/P4-VISUAL/visual-index.csv"
    if vis_path.exists():
        import csv
        with vis_path.open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                vis_ids.add(row.get("visual_id"))
    official = validate("official", by_id, sources, vis_ids)
    overlay = validate("overlay", by_id, sources, vis_ids)
    (HERE / "validation-official.json").write_text(
        json.dumps(official, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "validation-overlay.json").write_text(
        json.dumps(overlay, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def column(results):
        return {case: ("PASS" if data["checks"]["pass"] else
                        ("BLOCKED" if data["checks"].get("quota_blocked") else "FAIL"))
                for case, data in results.items()}

    off_col = column(official)
    ov_col = column(overlay)
    lines = ["# R1 Skill E2E — official vs Doubao overlay", "",
             "- Official: `dsh --profile headless --json` (DeepSeek key, no overlay)",
             "- Overlay: same prompts + temporary `--patch /tmp/dsh-doubao.yml`",
             "- Skill: `.dsh/skills/costume-director/SKILL.md` (not modified)",
             "", "| Case | Coverage | Official | Overlay |", "| --- | --- | --- | --- |"]
    for case in CASES:
        lines.append("| %s | %s | %s | %s |" % (
            case, CASES[case]["coverage"], off_col[case], ov_col[case]))
    lines.append("")
    lines.append("- Official: %d PASS / %d BLOCKED / %d FAIL" % (
        sum(1 for v in off_col.values() if v == "PASS"),
        sum(1 for v in off_col.values() if v == "BLOCKED"),
        sum(1 for v in off_col.values() if v == "FAIL")))
    lines.append("- Overlay: %d PASS / %d BLOCKED / %d FAIL" % (
        sum(1 for v in ov_col.values() if v == "PASS"),
        sum(1 for v in ov_col.values() if v == "BLOCKED"),
        sum(1 for v in ov_col.values() if v == "FAIL")))
    lines.append("")
    lines.append("## Official mode details")
    for case, data in official.items():
        lines.append("- %s: %s%s" % (
            case, off_col[case],
            (" — " + "; ".join(data["reasons"])) if data["reasons"] else ""))
    lines.append("")
    lines.append("## Overlay mode details")
    for case, data in overlay.items():
        lines.append("- %s: %s%s" % (
            case, ov_col[case],
            (" — " + "; ".join(data["reasons"])) if data["reasons"] else ""))
    lines.append("")
    (HERE / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if all(v == "PASS" for v in list(off_col.values()) + list(ov_col.values())) else 1


if __name__ == "__main__":
    sys.exit(main())
