# QA 报告（P3 终态索引）

- 更新时间：2026-11-04 02:44；快照 **328 卡**，git HEAD `0345f05`
- 本页为 P3 终态 QA 摘要；**详细独立验收见 [P3-QA.md](P3-QA.md)**，缺陷见 [P3-DEFECTS.md](P3-DEFECTS.md)，历史见 [P2.5-ACCEPTANCE.md](P2.5-ACCEPTANCE.md)

## 1. 机械验收（PASS）

| 项 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | 328/328；17/17 PASS；0 错误 0 警告 |
| 来源对账 | `python3 scripts/build_sources.py --check` | 0 | 174/174（QA 重建后；初始 142 行 FAIL → 已修复） |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | PASS 30/30；query 命中总 124、逐例 ≥1 |

## 2. 独立质量结论（P3-QA）

**PASS 12 / WARN 7 / FAIL 2 / HUMAN_UAT_PENDING 4**
- 回归：F1 崩溃、F2 假阴性、F3 静默 → **FIXED**；M3/M5 FIXED；M7/M8 PARTIAL；M1/M2/M4/M6 OPEN。
- query：relevant@5 **3.64/5**、precision **89.2%**、0 命中 12%（P2.5：3.0/86.2%/16%）。
- 15 案例 6 维 rubric：PASS 1 / WARN 14 / FAIL 0；切题均值 0.53/2、诚实/证据 2.0/2。
- 新来源：SRC-0400..0431 共 32 个 URL，32/32 HTTP 200 且内容吻合。
- **FAIL 2**：D2 职业服万能填充（S2）、D4 虚假「rainwear cards are missing」（S1）。

## 3. 结论

P3 数据与诚实性显著提升（崩溃/假阴性/静默缺陷已修复），但**语义质量仍未通过发布门槛**：职业匹配错误与虚假 warning 必须在 P3.1 修复并回归复验（NEXT-PLAN §1）。

## 4. HUMAN_UAT_PENDING（不得写成 PASS）

- H1 Obsidian GUI；H2 逐图版权授权；H3 15 案例语义评分签核；H4 62 张 draft 复核。
- 另：query 相关性无标注集、评分未做参数敏感性测试；未改任何卡片/脚本（只读审计）。
