#!/usr/bin/env python3
"""run_acceptance.py - real end-to-end acceptance tests for the Costume Director P2 loop.

For every 11-验收/测试输入/T*.json file:
  1. run scripts/recommend.py <input> --json          (real subprocess, exit code recorded)
  2. run scripts/query.py <test query args> --json    (real subprocess, exit code recorded)
  3. evaluate the declared acceptance criteria against the actual output
  4. write 11-验收/测试结果/<test>.md with input, commands, retrieved IDs,
     A/B/C looks, scores, prompts, risks, PASS/FAIL and notes
  5. write 11-验收/测试结果/raw/<test>.json with the raw script output
Finally write 11-验收/测试结果/SUMMARY.md with verdict counts, failures and command
exit codes.

This runner never invents results: if a script fails or the knowledge base lacks
a slot, the corresponding criterion is FAIL/PARTIAL and the reason is recorded.

Usage:
    python3 scripts/run_acceptance.py                 # all tests
    python3 scripts/run_acceptance.py --only T03,T17  # subset
    python3 scripts/run_acceptance.py --no-write      # evaluate only (no result files)

Exit code: 0 when every test passes, 1 when at least one criterion fails.
"""

import argparse
import datetime
import json
import subprocess
import sys
import time
from pathlib import Path

import costume_lib as lib
import recommend as rec

RESULTS_DIR = "11-验收/测试结果"
INPUTS_DIR = "11-验收/测试输入"

HEEL_WORDS = ("heel", "stiletto", "高跟", "pump")
OPEN_WORDS = ("sandal", "flip", "slipper", "凉鞋", "拖鞋")


def run_command(args, cwd, timeout=240):
    started = time.time()
    try:
        proc = subprocess.run(args, cwd=str(cwd), capture_output=True,
                              text=True, timeout=timeout)
        return {
            "cmd": " ".join(args),
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "duration": round(time.time() - started, 2),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": " ".join(args),
            "returncode": 124,
            "stdout": exc.stdout or "",
            "stderr": "TIMEOUT after %ss" % timeout,
            "duration": round(time.time() - started, 2),
        }


def safe_json(text):
    text = (text or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def load_test_inputs(root):
    base = root / INPUTS_DIR
    items = []
    for path in sorted(base.glob("T*.json")):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print("ERROR: bad test input %s: %s" % (path, exc), file=sys.stderr)
            continue
        items.append({"path": path, "raw": raw, "meta": raw.get("_test", {})})
    return items


# ---------------------------------------------------------------------------
# criterion evaluation
# ---------------------------------------------------------------------------
def looks_of(data):
    return (data or {}).get("looks", []) or []


def items_for_slot(look, slot):
    return [item for item in look.get("items", []) if item.get("slot") == slot]


def all_items(data):
    out = []
    for look in looks_of(data):
        out.extend(look.get("items", []))
    return out


def item_card(card_index, item_id):
    return card_index.get(item_id)


def is_heel(item, card_index):
    card = item_card(card_index, item.get("id"))
    text = ""
    if card:
        text = (lib.norm_text(lib.get_str(card["meta"], "subcategory")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_en")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_zh")))
    else:
        text = lib.norm_text(item.get("name_en", "") + " " + item.get("name_zh", ""))
    return any(word in text for word in HEEL_WORDS)


def is_open_footwear(item, card_index):
    card = item_card(card_index, item.get("id"))
    if card:
        text = (lib.norm_text(lib.get_str(card["meta"], "subcategory")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_en")) + " " +
                lib.norm_text(lib.get_str(card["meta"], "name_zh")))
    else:
        text = lib.norm_text(item.get("name_en", "") + " " + item.get("name_zh", ""))
    return any(word in text for word in OPEN_WORDS)


def criterion(name, record, card_index, source_ids):
    """Return (status, detail) where status is PASS/FAIL/PARTIAL/NOT_TESTED."""
    data = record["data"]
    rc = record["recommend"]["returncode"]
    meta = record["meta"]
    looks = looks_of(data)
    checks = (data or {}).get("checks", {})
    if rc != 0 or data is None:
        return "FAIL", "recommend.py exit=%s, no usable JSON output (stderr: %s)" % (
            rc, record["recommend"]["stderr"].strip()[:300] or "none")

    if name == "three_looks":
        ok = len(looks) == 3 and checks.get("three_looks") and checks.get("looks_distinct")
        return ("PASS" if ok else "FAIL",
                "looks=%d, distinct=%s, checks=%s" % (
                    len(looks), checks.get("looks_distinct"),
                    {k: checks.get(k) for k in ("three_looks", "looks_distinct")}))
    if name == "ids_exist":
        return ("PASS" if checks.get("ids_all_exist") else "FAIL",
                "all garment ids resolvable: %s" % checks.get("ids_all_exist"))
    if name == "fidelity_matches":
        expected = meta.get("expected_mode")
        got = (data or {}).get("fidelity_mode")
        ok = got == expected
        return ("PASS" if ok else "FAIL", "expected=%s got=%s" % (expected, got))
    if name == "historical_verified":
        evidence = [look.get("evidence", {}) for look in looks]
        verified_counts = [sum(1 for status in (ev.get("item_evidence") or {}).values()
                               if status == "verified") for ev in evidence]
        all_have = all(count > 0 for count in verified_counts) and bool(verified_counts)
        missing_urls = (data or {}).get("missing_urls", [])
        has_sources = any(ev.get("source_ids") for ev in evidence)
        ok = checks.get("history_evidence") and all_have and not missing_urls and has_sources
        return ("PASS" if ok else "FAIL",
                "history_evidence=%s verified/item=%s missing_source_ids=%s has_source_ids=%s" % (
                    checks.get("history_evidence"), verified_counts,
                    missing_urls, has_sources))
    if name == "query_hits":
        if record.get("query") is None:
            return "FAIL", "no query.py step configured for this scenario"
        hits = record.get("query_data")
        count = len(hits) if isinstance(hits, list) else 0
        ids = [row.get("id") for row in (hits or []) if isinstance(row, dict)]
        ok = record["query"]["returncode"] == 0 and count >= 1
        return ("PASS" if ok else "FAIL",
                "query.py exit=%s, hits=%d, ids=%s" % (
                    record["query"]["returncode"], count,
                    ", ".join(ids[:6]) + ("…" if len(ids) > 6 else "") if ids else "(none)"))
    if name == "region_evidence":
        region = (data or {}).get("input", {}).get("region", "")
        want = rec.labels([region])
        compatible = []
        for item in all_items(data):
            card = item_card(card_index, item.get("id"))
            if not card:
                continue
            region_labels = rec.card_region_labels(card)
            if region_labels and want and rec.region_compatible_labels(want, region_labels):
                compatible.append(item["id"])
        ok = bool(compatible)
        return ("PASS" if ok else "FAIL",
                "region-compatible evidence for %r: %s (items=%s)" % (
                    region, compatible,
                    [item.get("id") for item in all_items(data)]))
    if name == "rain_outerwear":
        ok = all(items_for_slot(look, "outerwear") for look in looks) and bool(looks)
        return ("PASS" if ok else "FAIL",
                "outerwear per look=%s" % [len(items_for_slot(look, "outerwear")) for look in looks])
    if name == "outerwear":
        ok = bool(looks) and bool(items_for_slot(looks[0], "outerwear"))
        return ("PASS" if ok else "FAIL",
                "A outerwear=%s" % [i["id"] for i in items_for_slot(looks[0], "outerwear")] if looks else [])
    if name in ("dance_safe", "safe_footwear"):
        footwear = [item for look in looks for item in items_for_slot(look, "footwear")]
        bad = [item["id"] for item in footwear
               if (is_heel(item, card_index) if name == "dance_safe"
                   else (is_heel(item, card_index) or is_open_footwear(item, card_index)))]
        ok = bool(footwear) and not bad
        return ("PASS" if ok else "FAIL",
                "footwear=%s unsafe=%s" % ([i["id"] for i in footwear], bad))
    if name == "budget_alternative":
        if len(looks) < 3:
            return "FAIL", "less than 3 looks, cannot compare budget alternative"
        a, c = looks[0], looks[2]
        ok = c.get("cost", 9) <= a.get("cost", 0) + 0.02 and (
            set(i["id"] for i in a.get("items", [])) !=
            set(i["id"] for i in c.get("items", [])))
        return ("PASS" if ok else "FAIL",
                "A cost=%.3f C cost=%.3f, C distinct=%s" % (
                    a.get("cost", -1), c.get("cost", -1),
                    set(i["id"] for i in a.get("items", [])) !=
                    set(i["id"] for i in c.get("items", []))))
    if name == "wet_state_lock":
        lock = looks[0].get("continuity_lock", "") if looks else ""
        ok = "wetness=wet" in lock
        return ("PASS" if ok else "FAIL", "lock wetness=wet: %s" % ok)
    if name == "fictional_phrasing":
        ok = bool(looks) and all("not a historical reconstruction" in look.get("prompt_image", "")
                                 for look in looks)
        return ("PASS" if ok else "FAIL",
                "all prompts declare fictional: %s" % ok)
    if name == "no_fake_sources":
        missing = (data or {}).get("missing_urls", [])
        sources = (data or {}).get("sources", [])
        bad_urls = [entry for entry in sources
                    if not str(entry.get("url", "")).startswith("http")]
        unresolved = [sid for sid in
                      set(sid for look in looks
                          for sid in (look.get("evidence", {}) or {}).get("source_ids", []))
                      if sid not in source_ids]
        ok = not missing and not bad_urls and not unresolved
        return ("PASS" if ok else "FAIL",
                "missing_source_ids=%s bad_urls=%s unresolved_source_cards=%s" % (
                    missing, bad_urls, unresolved))
    if name == "prompts":
        problems = []
        for idx, look in enumerate(looks):
            image = look.get("prompt_image", "")
            video = look.get("prompt_video", "")
            if len(image) < 150:
                problems.append("look %d image prompt too short" % idx)
            if len(video) < 200:
                problems.append("look %d video prompt too short" % idx)
            if "continuity lock" not in video.lower():
                problems.append("look %d video prompt lacks continuity lock" % idx)
            if "negative constraints" not in video.lower():
                problems.append("look %d video prompt lacks negative constraints" % idx)
        return ("PASS" if not problems else "FAIL", "; ".join(problems) or "all prompts complete")
    if name == "continuity_pass":
        continuity = (data or {}).get("continuity") or {}
        scenes = continuity.get("scenes", [])
        verdict = continuity.get("verdict")
        ids = [tuple(scene.get("item_ids", [])) for scene in scenes]
        same_ids = bool(ids) and len(set(ids)) == 1
        locks = all("continuity lock" in scene.get("prompt_video", "").lower()
                    and "continuity lock" in scene.get("prompt_image", "").lower()
                    for scene in scenes)
        ok = verdict == "PASS" and len(scenes) >= 3 and same_ids and locks
        return ("PASS" if ok else "FAIL",
                "verdict=%s scenes=%d same_item_ids=%s locks_in_every_prompt=%s issues=%s" % (
                    verdict, len(scenes), same_ids, locks,
                    continuity.get("issues", [])))
    return "NOT_TESTED", "unknown criterion %r" % name


# ---------------------------------------------------------------------------
# pair checks
# ---------------------------------------------------------------------------
def pair_check(name, first, second):
    d1, d2 = first["data"] or {}, second["data"] or {}
    looks1, looks2 = looks_of(d1), looks_of(d2)
    if not looks1 or not looks2:
        return "FAIL", "one side produced no looks"

    def ids(look):
        return set(item["id"] for item in look.get("items", []))

    if name == "stylisation_pair":
        if d1.get("fidelity_mode") == "historical":
            hist_data, insp_data = d1, d2
        else:
            hist_data, insp_data = d2, d1
        hist_looks = looks_of(hist_data)
        insp_looks = looks_of(insp_data)
        ok = (hist_data.get("fidelity_mode") == "historical" and
              insp_data.get("fidelity_mode") == "inspired" and
              bool(hist_looks) and bool(insp_looks))
        p1 = bool(hist_looks) and "period-accurate" in hist_looks[0].get("prompt_image", "")
        p2 = bool(insp_looks) and "period-inspired" in insp_looks[0].get("prompt_image", "")
        ok = ok and p1 and p2
        return ("PASS" if ok else "FAIL",
                "modes=%s/%s historical phrase=%s inspired phrase=%s" % (
                    hist_data.get("fidelity_mode"), insp_data.get("fidelity_mode"),
                    p1, p2))
    if name == "lighting_pair":
        a1, a2 = looks1[0], looks2[0]
        overlap = len(ids(a1) & ids(a2))
        p1 = a1.get("prompt_image", "")
        p2 = a2.get("prompt_image", "")
        differs = p1 != p2
        ok = overlap >= 2 and differs
        return ("PASS" if ok else "FAIL",
                "A item overlap=%d, prompts differ=%s" % (overlap, differs))
    if name == "class_pair":
        def id_text(values):
            # Avoid "[[" sequences: Obsidian must never parse them as wikilinks.
            return ", ".join(sorted(values)) if values else "none"

        a_symmetric = ids(looks1[0]) ^ ids(looks2[0])
        total_symmetric = 0
        per_look = []
        for idx in range(min(len(looks1), len(looks2))):
            diff = ids(looks1[idx]) ^ ids(looks2[idx])
            per_look.append(id_text(diff))
            total_symmetric += len(diff)
        ok = len(a_symmetric) >= 2 or (len(a_symmetric) >= 1 and total_symmetric >= 4)
        return ("PASS" if ok else "FAIL",
                "A missing/extra ids: %s; per-look differences: %s" % (
                    id_text(a_symmetric), " | ".join(per_look)))
    return "NOT_TESTED", "unknown pair check %r" % name


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def md_json_block(data):
    return "```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```"


def fmt_items(look):
    rows = []
    for item in look.get("items", []):
        rows.append("| %s | `%s` | %s / %s | %s | %s | %s |" % (
            item.get("slot"), item.get("id"), item.get("name_zh", "-"),
            item.get("name_en", "-"), ", ".join(item.get("colors", [])) or "-",
            ", ".join(item.get("materials", [])) or "-",
            item.get("evidence_status", "-")))
    return "\n".join(rows)


def render_result(record, pair_results):
    raw = record["raw"]
    meta = record["meta"]
    data = record["data"]
    lines = []
    tid = meta.get("id") or record["path"].stem
    lines.append("# %s — %s" % (tid, meta.get("title", record["path"].stem)))
    lines.append("")
    lines.append("- 运行时间：%s" % record["timestamp"])
    lines.append("- 测试类型：%s" % ", ".join(meta.get("types", [])))
    lines.append("- 模式：%s" % meta.get("mode", "standard"))
    lines.append("- 输入文件：`%s`" % record["path"].relative_to(lib.vault_root()).as_posix())
    lines.append("- 运行命令：`%s`" % record["recommend"]["cmd"])
    lines.append("- 退出码：**%s**（耗时 %ss）" % (
        record["recommend"]["returncode"], record["recommend"]["duration"]))
    if record["recommend"]["stderr"].strip():
        lines.append("- stderr：`%s`" % record["recommend"]["stderr"].strip()[:500])
    lines.append("")
    lines.append("## 实际输入")
    lines.append("")
    clean = {key: value for key, value in raw.items() if key != "_test"}
    lines.append(md_json_block(clean))
    lines.append("")
    lines.append("## 检索执行记录")
    lines.append("")
    lines.append("| 命令 | 退出码 | 耗时 |")
    lines.append("| --- | --- | --- |")
    lines.append("| `%s` | %s | %ss |" % (
        record["recommend"]["cmd"], record["recommend"]["returncode"],
        record["recommend"]["duration"]))
    if record["query"]:
        lines.append("| `%s` | %s | %ss |" % (
            record["query"]["cmd"], record["query"]["returncode"],
            record["query"]["duration"]))
    lines.append("")
    query_ids = [row.get("id") for row in (record["query_data"] or [])
                 if isinstance(row, dict) and row.get("id")]
    lines.append("- `query.py` 命中数量：**%s**（验收要求 ≥1）" % record.get("query_hits", 0))
    lines.append("- `query.py` 命中卡片 ID：%s" % (", ".join(query_ids) if query_ids else "(none)"))
    retrieved = (data or {}).get("retrieved_ids", {})
    lines.append("- `recommend.py` 候选池：" + "; ".join(
        "%s=%s" % (slot, ", ".join(ids)) for slot, ids in sorted(retrieved.items()))
        if retrieved else "- `recommend.py` 候选池：(none)")
    selected = []
    for look in looks_of(data):
        selected.append("%s: %s" % (look.get("look_ref"),
                                    ", ".join(i["id"] for i in look.get("items", []))))
    lines.append("- 三套推荐选中：" + "; ".join(selected) if selected else "- 三套推荐选中：(none)")
    lines.append("")
    lines.append("## 候选造型 A/B/C")
    lines.append("")
    for look in looks_of(data):
        label = look.get("look_ref", "?")
        lines.append("### Look %s（score %.1f/100，cost %.3f，source_look=%s）" % (
            label, look.get("total", -1), look.get("cost", -1),
            look.get("source_look_id") or "assembled"))
        lines.append("")
        if look.get("missing"):
            lines.append("- **缺口**：%s" % ", ".join(look["missing"]))
        lines.append("| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        lines.append(fmt_items(look))
        if look.get("parts"):
            lines.append("")
            lines.append("- 结构卡：%s" % ", ".join(p["id"] for p in look["parts"]))
        if look.get("materials"):
            lines.append("- 材质卡：%s" % ", ".join(m["id"] for m in look["materials"]))
        lines.append("")
    lines.append("### 评分明细")
    lines.append("")
    labels = [("period", "年代/文化", 25), ("identity", "角色身份", 15),
              ("environment", "环境气候", 15), ("art", "美术方向", 15),
              ("movement", "动作可行", 10), ("arc", "剧情弧线", 10),
              ("camera", "摄影/一致性", 10)]
    lines.append("| 维度 | " + " | ".join(
        look.get("look_ref", "?") for look in looks_of(data)) + " |")
    lines.append("| --- | " + " | ".join("---" for _ in looks_of(data)) + " |")
    for key, label, _weight in labels:
        lines.append("| %s | %s |" % (label, " | ".join(
            str(look.get("scores", {}).get(key, "-")) for look in looks_of(data))))
    lines.append("| **总计** | %s |" % " | ".join(
        str(look.get("total", "-")) for look in looks_of(data)))
    lines.append("")
    if (data or {}).get("continuity"):
        continuity = data["continuity"]
        lines.append("## 多场次连续性")
        lines.append("")
        lines.append("- verdict：**%s**" % continuity.get("verdict"))
        if continuity.get("issues"):
            lines.append("- issues：%s" % "; ".join(continuity["issues"]))
        lines.append("")
        lines.append("| 场次 | wetness | damage | 锁定 ID |")
        lines.append("| --- | --- | --- | --- |")
        for scene in continuity.get("scenes", []):
            state = scene.get("state", {})
            lines.append("| %s | %s | %s | %s |" % (
                scene.get("scene_id"), state.get("wetness"), state.get("damage"),
                ", ".join(scene.get("item_ids", []))))
        lines.append("")
    lines.append("## 生图 / 视频 Prompt（实际输出）")
    lines.append("")
    for look in looks_of(data):
        lines.append("### Look %s" % look.get("look_ref", "?"))
        lines.append("")
        lines.append("**Image prompt (EN):**")
        lines.append("")
        lines.append("```")
        lines.append(look.get("prompt_image", ""))
        lines.append("```")
        lines.append("")
        lines.append("**Video prompt (EN):**")
        lines.append("")
        lines.append("```")
        lines.append(look.get("prompt_video", ""))
        lines.append("```")
        lines.append("")
    if (data or {}).get("continuity"):
        for scene in data["continuity"].get("scenes", []):
            lines.append("### 场景 %s — %s / %s" % (
                scene.get("scene_id"), scene.get("state", {}).get("wetness"),
                scene.get("state", {}).get("damage")))
            lines.append("")
            lines.append("**Image prompt:**")
            lines.append("")
            lines.append("```")
            lines.append(scene.get("prompt_image", ""))
            lines.append("```")
            lines.append("")
            lines.append("**Video prompt:**")
            lines.append("")
            lines.append("```")
            lines.append(scene.get("prompt_video", ""))
            lines.append("```")
            lines.append("")
    lines.append("## 风险与证据")
    lines.append("")
    for look in looks_of(data):
        lines.append("### Look %s" % look.get("look_ref", "?"))
        lines.append("")
        for reason in look.get("reasons", []):
            lines.append("- 理由：%s" % reason)
        for risk in look.get("risks", []):
            lines.append("- 风险：%s" % risk)
        evidence = look.get("evidence", {})
        lines.append("- source_ids：%s" % (
            ", ".join(evidence.get("source_ids", [])) or "(none)"))
        for entry in evidence.get("source_urls", []):
            lines.append("- 来源链接：%s → %s" % (entry.get("source_id"), entry.get("url")))
        lines.append("")
    lines.append("## 验收判定")
    lines.append("")
    lines.append("| 检查项 | 结果 | 说明 |")
    lines.append("| --- | --- | --- |")
    for check in record["checks"]:
        lines.append("| %s | %s | %s |" % (check["name"], check["status"], check["detail"]))
    for name, status, detail in pair_results:
        lines.append("| %s（pair） | %s | %s |" % (name, status, detail))
    lines.append("")
    verdict = "PASS" if all(
        check["status"] == "PASS" for check in record["checks"]) and all(
        status == "PASS" for _name, status, _detail in pair_results) else "FAIL"
    lines.append("**VERDICT: %s**" % verdict)
    lines.append("")
    lines.append("## 备注")
    lines.append("")
    warnings = (data or {}).get("warnings", [])
    if warnings:
        for warning in warnings:
            lines.append("- 脚本警告：%s" % warning)
    else:
        lines.append("- 脚本无警告。")
    lines.append("- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。")
    lines.append("- 知识库为运行时刻快照；新增卡片后必须重跑本测试。")
    lines.append("")
    return "\n".join(lines), verdict


def render_summary(records, errors, vault_stats):
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = []
    lines.append("# P2 验收测试 SUMMARY")
    lines.append("")
    lines.append("- 运行时间：%s" % now)
    lines.append("- Python：%s" % sys.version.split()[0])
    lines.append("- 测试数：%d" % len(records))
    lines.append("- 结果目录：`11-验收/测试结果/`")
    lines.append("- 重跑命令：`python3 scripts/run_acceptance.py`")
    lines.append("")
    lines.append("## 知识库快照")
    lines.append("")
    lines.append("- 卡片总数：%d" % vault_stats["total"])
    for ctype, count in sorted(vault_stats["types"].items()):
        lines.append("  - `%s`: %d" % (ctype, count))
    lines.append("- 来源卡：%d" % vault_stats["sources"])
    if vault_stats["errors"]:
        lines.append("- YAML 解析问题（由检索脚本跳过）：")
        for err in vault_stats["errors"]:
            lines.append("  - `%s`: %s" % (err["path"], err["error"]))
    lines.append("")
    lines.append("## 逐例结果")
    lines.append("")
    lines.append("| 用例 | 标题 | 模式 | recommend exit | query exit | query hits | VERDICT | 失败项 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    pass_count = fail_count = 0
    for record in records:
        verdict = record["verdict"]
        if verdict == "PASS":
            pass_count += 1
        else:
            fail_count += 1
        failed = [check["name"] for check in record["checks"]
                  if check["status"] != "PASS"]
        failed += [name for name, status, _detail in record["pair_results"]
                   if status != "PASS"]
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (
            record["meta"].get("id"), record["meta"].get("title", ""),
            record["meta"].get("mode", "standard"),
            record["recommend"]["returncode"],
            record["query"]["returncode"] if record["query"] else "-",
            record.get("query_hits", 0),
            verdict, ", ".join(failed) or "-"))
    lines.append("")
    lines.append("## 统计")
    lines.append("")
    lines.append("- PASS：%d / %d" % (pass_count, len(records)))
    lines.append("- FAIL：%d / %d" % (fail_count, len(records)))
    hit_counts = [(record["meta"].get("id"), record.get("query_hits", 0))
                  for record in records if record.get("query") is not None]
    total_hits = sum(count for _tid, count in hit_counts)
    zero_hits = [tid for tid, count in hit_counts if count == 0]
    lines.append("- query.py 命中总数：%d（逐例：%s）" % (
        total_hits, ", ".join("%s=%d" % (tid, count) for tid, count in hit_counts)))
    lines.append("- 每个场景 query 步骤均返回 ≥1 命中：%s" % (
        "是" if hit_counts and not zero_hits else "否（%s）" % (", ".join(zero_hits) or "无 query 步骤")))
    lines.append("")
    lines.append("## 失败明细")
    lines.append("")
    if fail_count == 0:
        lines.append("- 无失败项。")
    else:
        for record in records:
            for check in record["checks"]:
                if check["status"] != "PASS":
                    lines.append("- %s `%s`：%s" % (
                        record["meta"].get("id"), check["name"], check["detail"]))
            for name, status, detail in record["pair_results"]:
                if status != "PASS":
                    lines.append("- %s pair `%s`：%s" % (
                        record["meta"].get("id"), name, detail))
    lines.append("")
    lines.append("## 知识库缺口汇总（来自脚本 warnings）")
    lines.append("")
    gap_counter = {}
    for record in records:
        for warning in (record["data"] or {}).get("warnings", []):
            gap_counter[warning] = gap_counter.get(warning, 0) + 1
    if not gap_counter:
        lines.append("- 无脚本警告。")
    else:
        for warning, count in sorted(gap_counter.items(), key=lambda kv: -kv[1]):
            lines.append("- ×%d %s" % (count, warning))
    lines.append("")
    lines.append("## 配对检查")
    lines.append("")
    pair_rows = []
    for record in records:
        for name, status, detail in record["pair_results"]:
            pair_rows.append("- %s → `%s`：%s（%s）" % (
                record["meta"].get("id"), name, status, detail))
    lines.extend(pair_rows or ["- 无配对检查。"])
    lines.append("")
    lines.append("## 说明与限制")
    lines.append("")
    lines.append("- 所有命令均为真实 `python3` 子进程，退出码与原始输出见各用例文件与 `raw/`。")
    lines.append("- 测试只验证 P2 决策闭环（检索/评分/提示词/连续性）；Obsidian GUI、图片授权与史学正确性需另行人工核验。")
    lines.append("- 若知识库新增卡片，必须重跑 `python3 scripts/run_acceptance.py` 更新本 SUMMARY。")
    lines.append("")
    return "\n".join(lines), pass_count, fail_count


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Run real P2 acceptance tests.")
    parser.add_argument("--only", help="comma separated test ids, e.g. T03,T17")
    parser.add_argument("--no-write", action="store_true", help="do not write result files")
    args = parser.parse_args(argv)

    root = lib.vault_root()
    cards, card_errors = lib.load_cards()
    card_index = {lib.get_str(card["meta"], "id"): card for card in cards}
    source_ids = set(card_index)
    vault_stats = {
        "total": len(cards),
        "types": {},
        "sources": sum(1 for card in cards
                       if lib.norm_text(card["meta"].get("type")) == "source"),
        "errors": card_errors,
    }
    for card in cards:
        ctype = lib.get_str(card["meta"], "type") or "unknown"
        vault_stats["types"][ctype] = vault_stats["types"].get(ctype, 0) + 1

    only = set(part.strip() for part in args.only.split(",")) if args.only else None
    test_items = [item for item in load_test_inputs(root)
                  if not only or item["meta"].get("id") in only]
    if not test_items:
        print("No matching tests found in %s" % (root / INPUTS_DIR), file=sys.stderr)
        return 2

    results_dir = root / RESULTS_DIR
    raw_dir = results_dir / "raw"
    if not args.no_write:
        results_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for item in test_items:
        path = item["path"]
        meta = item["meta"]
        tid = meta.get("id") or path.stem
        print("== %s %s" % (tid, meta.get("title", "")))
        recommend = run_command(
            [sys.executable, "scripts/recommend.py", str(path), "--json"], root)
        print("   recommend.py exit=%s (%.2fs)" % (
            recommend["returncode"], recommend["duration"]))
        data = safe_json(recommend["stdout"])
        query = None
        query_data = None
        query_args = meta.get("query") or []
        if query_args:
            query = run_command([sys.executable, "scripts/query.py"] + query_args, root)
            print("   query.py exit=%s (%.2fs)" % (
                query["returncode"], query["duration"]))
            query_data = safe_json(query["stdout"])
        record = {
            "path": path,
            "raw": item["raw"],
            "meta": meta,
            "recommend": recommend,
            "query": query,
            "data": data,
            "query_data": query_data,
            "query_hits": len(query_data) if isinstance(query_data, list) else 0,
            "timestamp": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "checks": [],
            "pair_results": [],
        }
        criteria = list(meta.get("criteria", []))
        if query is not None and "query_hits" not in criteria:
            criteria.append("query_hits")
        for name in criteria:
            status, detail = criterion(name, record, card_index, source_ids)
            record["checks"].append({"name": name, "status": status, "detail": detail})
        records.append(record)
        if not args.no_write:
            raw_name = path.stem + ".json"
            (raw_dir / raw_name).write_text(
                recommend["stdout"] or json.dumps(
                    {"returncode": recommend["returncode"],
                     "stderr": recommend["stderr"]}, ensure_ascii=False, indent=2),
                encoding="utf-8")
            if query is not None:
                (raw_dir / (path.stem + ".query.json")).write_text(
                    query["stdout"] or "[]", encoding="utf-8")

    # pair checks are evaluated after both sides have run
    by_id = {record["meta"].get("id"): record for record in records}
    for record in records:
        pair_with = record["meta"].get("pair_with")
        if not pair_with or pair_with not in by_id:
            continue
        other = by_id[pair_with]
        pair_name = record["meta"].get("pair_check", "pair")
        status, detail = pair_check(pair_name, record, other)
        record["pair_results"].append((pair_name, status, detail))

    rendered = []
    for record in records:
        text, verdict = render_result(record, record["pair_results"])
        record["verdict"] = verdict
        rendered.append((record, text))
        if not args.no_write:
            out_path = results_dir / (record["path"].stem + ".md")
            out_path.write_text(text + "\n", encoding="utf-8")
            print("   wrote %s" % out_path.relative_to(root))

    summary_text, pass_count, fail_count = render_summary(records, card_errors, vault_stats)
    if not args.no_write:
        (results_dir / "SUMMARY.md").write_text(summary_text + "\n", encoding="utf-8")
        print("wrote", (results_dir / "SUMMARY.md").relative_to(root))
    else:
        print(summary_text)

    print("PASS %d / %d, FAIL %d / %d" % (pass_count, len(records),
                                           fail_count, len(records)))
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
