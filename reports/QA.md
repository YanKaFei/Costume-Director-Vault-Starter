# QA 报告（P3.1 复验索引）

- 更新时间：2026-11-04 02:51；快照 **328 卡 / 41 例验收**；git HEAD `0345f05` + P3.1 工作区修改
- 详细独立验收：[P3-QA.md](P3-QA.md)；缺陷：[P3-DEFECTS.md](P3-DEFECTS.md)；历史：[P2.5-ACCEPTANCE.md](P2.5-ACCEPTANCE.md)

## 1. 机械验收（PASS）

| 项 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | 328/328；17/17 PASS；0 错误 0 警告 |
| 来源对账 | `python3 scripts/build_sources.py --check` | 0（QA 重建后） | 174/174 一致；P3.1 后曾 2 行漂移（QA `--write` 修复） |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | **PASS 41/41**；query 命中 178、逐例 ≥1 |

## 2. 独立质量结论（P3.1）

**PASS 17 / WARN 5 / FAIL 1 / HUMAN_UAT_PENDING 4（27 项）**
- **D2/D4 已关闭**：职业匹配（护士 GAR-0036/白袍 GAR-0041/警察 GAR-0042/厨师 GAR-0043/太空 GAR-0038+0039/婚礼 GAR-0005+0070）与雨具选择/无虚假 rainwear warning 均验证通过；M1/M2/M4/M6/M7 同步关闭。
- **FAIL 1（R7）**：query relevance@5 独立 **3.64**、engineer 自评 **3.92**，均 <4.0 发布门槛；`quality_eval` **OVERALL FAIL（exit 1）**。其余指标：precision 独立 89.2%（自评 96.1%）、0 命中 12%、崩溃 0、example-in-A 0、warnings 100%、A/B/C 差异 0.976、证据覆盖 0.959。
- **15 案例 6 维 rubric**：PASS 6 / WARN 9 / FAIL 0（P3：1/14/0）；切题均值 1.27/2、诚实/证据 2.0/2。
- **WARN 5**：R1 职业同义词/医疗内层、R2 example top5/和服重复、R6 CSV 同步流程、R5 评分口径差、证据覆盖不均。

## 3. 结论

P3.1 修复确认：D2/D4 关闭、F1/F2/F3 保持修复、41/41 验收 PASS。但**未完全通过发布门槛**：query relevance 未达 4.0（唯一 FAIL），另有 5 项 WARN 与 4 项 HUMAN_UAT_PENDING。按 NEXT-PLAN 关闭 R7/R1/R2/R6 并完成 UAT 后方可发布。

## 4. HUMAN_UAT_PENDING（不得写成 PASS）

- H1 Obsidian GUI；H2 逐图版权；H3 15 案例语义评分签核；H4 62 张 draft 复核。
- 其它限制：query 相关性无标注集；评分未做参数敏感性测试；未改任何卡片/脚本（只读审计）。
