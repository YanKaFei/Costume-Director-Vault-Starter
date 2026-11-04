---
type: human_closeout
version: "1.0"
created_at: "2026-11-05T00:32:00+08:00"
restored_from_commit: "7f7a21b"
restored_by: "verifier (R1.1-A / task-52)"
restored_reason: "R1-F1：56f4225 的测试重跑覆盖并删除了 SUMMARY.md / P4-MACBETH-COMPARISON.md 中的人工 close-out 段"
reviewer: "PENDING_HUMAN_SIGN_OFF"
signature: "____________________"
status: "RESTORED_PENDING_HUMAN_SIGNATURE"
authoritative: true
scope: "P4-MACBETH 人工 close-out；生成的 SUMMARY.md / P4-MACBETH-COMPARISON.md 不是权威来源"
---

# P4-MACBETH 人工 close-out（受保护文件）

> **本文件是人工结论的唯一权威副本。** `SUMMARY.md` 与 `P4-MACBETH-COMPARISON.md` 由
> `test_macbeth_p4.py` 自动生成，重跑会覆盖其内容；人工结论（根因、修复、验收矩阵）以本文件为准。
> 版本：v1.0；恢复自 `7f7a21b`；恢复时间：2026-11-05T00:32+08:00；恢复人：verifier（R1.1-A/task-52）。
> 人工审核者：**PENDING_HUMAN_SIGN_OFF**（签名栏见文末）；状态：**RESTORED_PENDING_HUMAN_SIGNATURE**。

## movement_action root cause / fix（来自 7f7a21b SUMMARY.md）

- Root cause: the test joined `prompt_outfit` with `" ".join(...)` (iterating characters) and only inspected `risks`, so an existing `prompt_outfit`/`movement_note` was invisible to the assertion.
- Fix: (a) test now inspects `str(look["prompt_outfit"]).lower()` and `movement_note`; (b) composer now emits an explicit `movement_note` and includes the action adaptation in `prompt_outfit` for action-constrained briefs (`battle, running, riding, climbing stairs`).
- After fix: `movement_action` PASS; P4-5 11/11.

## Final regression matrix（来自 7f7a21b SUMMARY.md）

| Suite | Result |
| --- | --- |
| P4-5 Macbeth validation (`test_macbeth_p4.py`) | PASS 11/11 |
| P4-3 Outfit Composer (`P4-COMPOSER/test_outfit.py`) | PASS 9/9 |
| P3 acceptance (`run_acceptance.py --no-write`) | PASS 45/45 |
| P3.5 workflow (`tests/test_workflow.py`) | 9/9 PASS |

## movement_action close-out（来自 7f7a21b P4-MACBETH-COMPARISON.md）

- Original FAIL was a test assertion bug: it joined `prompt_outfit` character-by-character and only checked `risks`; composer output had `movement_note` / action adaptation.
- Fixed the assertion; composer also now emits `movement_note` and "movement/action adaptation" in `prompt_outfit` for action-constrained briefs.
- Final: movement_action PASS; P4-5 11/11; Composer 9/9; acceptance 45/45; workflow 9/9.

## P4-5 case result summary（来自 7f7a21b P4-MACBETH-COMPARISON.md）

| Case | Result |
| --- | --- |
| stage_changes_Macbeth | PASS (3 stages, all A-look pair diffs >=4 in run) |
| stage_changes_Lady_Macbeth | PASS (3 stages, all pair diffs >=6) |
| two_character_relationship | PASS |
| full_slots_accessories | PASS |
| historical_evidence_gap | PASS (explicit gap; 1 look) |
| minimal_vs_complex | PASS |
| closeup_detail | PASS |
| movement_action | PASS |
| video_continuity | PASS |
| bilingual_term_search | PASS (旗袍/qipao, 立领/stand collar, 腰带/belt) |
| evidence_insufficient_refusal | PASS |

## 保护约定（生成脚本不得覆盖本文件）

1. 本文件路径固定为 `11-验收/P4-MACBETH/HUMAN-CLOSEOUT.md`，由人工/恢复流程写入；自动测试只允许写 `SUMMARY.md`、`P4-MACBETH-COMPARISON.md`、`outputs/`、`validation.json` 等生成物。
2. `tests/test_human_closeout.py` 会在重跑 `test_macbeth_p4.py` 前后计算本文件 SHA-256，要求完全一致；不一致即失败（退出非 0）。
3. 修改本文件必须升 `version`、记录 `restored_by`/审核者/日期，并由人工签名；不得代填签名。

## 人工签名

| 角色 | 姓名 | 签名 | 日期 | 备注 |
| --- | --- | --- | --- | --- |
| 人工审核者（导演/制片/QA） |  |  |  |  |
| 复核（Lead） |  |  |  |  |

> 状态：RESTORED_PENDING_HUMAN_SIGNATURE；在人工签名前，本文件内容可追溯但不构成发布批准。
