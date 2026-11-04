# R1.1-CREATIVE — 验证证据索引

- 报告：`reports/R1.1-CREATIVE.md`
- 被测代码版本：R1.1 落盘版（`scripts/outfit.py`、`scripts/abc_eval.py`、`scripts/lookbook.py`，2026-11-05 00:28–00:30）
- 本目录只存验证输入/输出/日志，不改卡片或脚本。

## 1. 目录

| 路径 | 内容 |
|---|---|
| `inputs/` | 跨时代、override、approved_anchors、historical 变体输入 |
| `outputs/` | 上述输入的 outfit 输出；`briefs/` 为 5 组独立 brief 输入+abc 结果 |
| `logs/` | 官方测试/abc_eval/heldout/P4-MACBETH 回归日志 |
| `lookbook-root/` | Look Bible 实测项目（demo / selfapprove），含 human/agent 签名样本 |

## 2. 关键证据

| 检查 | 命令/文件 | 结果 |
|---|---|---|
| 严格 11th c 跨时代阻断 | `outfit.py --input inputs/cross_era_macbeth.json` | exit 3, status=blocked, looks=[] |
| 合法 override | `outfit.py --input inputs/cross_override.json` | exit 0, status=override, historical_accuracy=false |
| 非法 override（historical_accuracy=true） | `outfit.py --input inputs/cross_bad_override.json` | exit 3, blocked |
| 普通 inspired 错配 | `outfit.py --input 11-验收/P4-MACBETH/inputs/macbeth_rise.json` | exit 0, status=ok（FAIL 证据：未逐项声明 GAR-0048/0079） |
| A/B/C 同视觉单件替换 | `logs/one_item_swap_evidence.json` same_vis | pass=false, gaming=true |
| A/B/C 单件+silhouette 变化 | 同上 diff_vis + `logs/abc_macbeth_rise.json` | pass=true, meaningful=true（FAIL 证据） |
| 固定 held-out | `scripts/abc_eval.py --heldout 11-验收/R1.1/CD/heldout --json` | exit 0, 5/5 pass |
| 独立 5 组 brief | `outputs/briefs/*.abc.json` | 4 pass / 1 blocked（nurse） |
| Look Bible 保护 | `lookbook-root/projects/demo/look-bible/look-bible.json` | hard anchor 拒绝覆盖；soft patch v7 diff=1 |
| 自批拦截 | `lookbook-root/agent-signature.json` / `agent-human-role.json` | exit 1，状态仍 Proposed |
| R1.1 C/D 测试 | `logs/test_r1_1_cd.log` | 7/7 PASS |
| Lookbook 测试 | `logs/test_lookbook.log` | 6/6 PASS |
| Composer 回归 | `logs/test_outfit.log` | 9/9 PASS |
| P4-MACBETH 回归 | `logs/test_macbeth_p4.log` | 9/15 PASS, 6 FAIL（回归 OPEN） |

## 3. 复现注意

- 官方测试会重写生成工件：`11-验收/P4-MACBETH/outputs/`、`11-验收/P4-COMPOSER/runs/`、`11-验收/P3.5/workflow-runs/`。这是测试输出，不是本任务编辑卡片/脚本。
- Look Bible 实测 `--root` 指向本目录，不写公共 `projects/`。
- `abc_eval.automated_score` 不是导演评分；`not_for_director_review=true`。
