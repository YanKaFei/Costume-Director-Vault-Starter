# 下一步计划（NEXT-PLAN）— P3.1 复验后

- 基准：2026-11-04 02:50；快照 328 卡（内容 154 + 来源 174）、41 例验收、quality_eval OVERALL FAIL（仅 query relevance）
- 当前验收：**PASS 17 / WARN 5 / FAIL 1 / HUMAN_UAT_PENDING 4**；**D2/D4 已关闭**
- 原则：先关 R7（唯一发布门槛阻断），再清 WARN 与覆盖扩展；所有修复须配回归用例并由 verifier 复验。

## 1. P4-a（发布门槛，必须关闭）

| # | 任务 | 对应 | 验收阈值 | 建议 owner |
|---|---|---|---|---|
| 1 | **提升 query relevance**：P09「蕾丝 晚装」、P10「丝绸 和服」跨文化多词精度；P14 noir 排除 example 卡；卡片 aliases/tags 增补（服饰术语同义词、跨文化标签）；query 权重/去重策略调整 | **R7（FAIL）** | verifier 独立 relevant@5 **≥4.0** 且 engineer `quality_eval` OVERALL PASS；precision ≥90%；0-hit 仅限已知未覆盖主题 | engineer + architect（标签） |
| 2 | 职业同义词与医疗内层：扩充 occupation hint 词表（巡警/女警/护士长/外科医生/厨师长/急诊医师等）；医生 A 套禁止韩服等非医疗 one_piece，除非无医疗基底时明确 warning | R1（WARN） | 合成职业案例（巡警/医生/护士长等）A 套使用匹配卡或无他职业顶替；T32 内层合理 | engineer |
| 3 | example 卡从 query 结果中排除或降权至 top5 之外 | R2（WARN） | P14/P25 等 filtered 查询 top5 无 example；T41 保持 PASS | engineer |
| 4 | 和服重复卡数据层处理：合并或 canonical 标注（GAR-0001/GAR-0065），保留查询去重 | R2/R3 | 数据字典/索引标注 canonical，query 不重复；validate 不变 | architect |
| 5 | **SOURCES.csv 同步机制**：发布清单/检查脚本固定执行 `build_sources.py --write` + `--check`，并在 acceptance SUMMARY 增记 CSV 行数 | R6/D1 复发 | 每次卡片/来源修改后 `--check` 必过；QA 复验无漂移 | engineer（流程） |
| 6 | 噪声 warning 措辞（no upper_body/lower_body 在 one_piece/set 场景） | R4 | 文案改为「由 one_piece/set 覆盖」，不误导 | engineer |
| 7 | 自评与独立评分口径并表：quality_eval 与 verifier rubric 同时输出 | R5 | release 报告同时列两套指标并注明差异 | engineer + lead |

## 2. P4-b（覆盖扩展，非阻断）

| # | 任务 | 验收 |
|---|---|---|
| 8 | pattern 族系 1/11 → ≥6/11；material 4/8 → 7/8；garment_part 6/16 → ≥10/16；lower_body/inner_layer 增补 | P3-COVERAGE 缺口逐项核销；每类 ≥1 verified 来源 |
| 9 | 接入 19 张 Getty AAT 与其余未引用来源（114/174 → ≥150/174） | 来源引用率 ≥85%；AAT 术语用于定义类卡片 |
| 10 | 15 案例中 9 例切题 0–1 的分支：明制/宫廷、未来基底、身份弧线 wardrobe-stage 化、跨文化仪式礼服 | rubric 切题均值 ≥1.6/2；无「切题 0 + 无 warning」案例 |
| 11 | 补现代职业基底卡（PPE/工牌/防滑鞋/雨衣/头盔/配送箱/义体外骨骼） | 相关 warning 降为低频，A 套切题改善 |

## 3. 人工 UAT（发布前必须完成，不得由 agent 代签）

| # | 项 | 状态 | 完成标准 |
|---|---|---|---|
| H1 | Obsidian GUI 打开/渲染/wikilink 跳转 | HUMAN_UAT_PENDING | 截图 + 抽 10 条链接点击通过 |
| H2 | 逐图版权授权核验 | HUMAN_UAT_PENDING | 每张外链图记录许可结论；无授权仅 link_only（当前 0 下载/0 内嵌） |
| H3 | 15 案例语义评分签核 | HUMAN_UAT_PENDING | lead 对 `P3-QA §5` 评分签字或调整 |
| H4 | 62 张 draft 卡人工复核 | HUMAN_UAT_PENDING | `review_status` 更新，draft=0 |

## 4. 发布清单（Definition of Done）

- [ ] **R7 关闭**：verifier relevant@5 ≥4.0；`quality_eval` OVERALL PASS（当前 FAIL 3.92 < 4.0）
- [ ] D2/D4 保持关闭（回归用例 T31–T41 通过；F1/F2/F3 回归保持 PASS）
- [ ] R1/R2/R6 关闭；R3/R4/R5 处理或书面接受
- [ ] `validate.py` exit 0；`build_sources --check` exit 0（CSV 174 行一致）；`run_acceptance` ≥41/41 PASS
- [ ] 15 案例 rubric：PASS ≥12/15、无切题 0 分且无 warning 的案例
- [ ] HUMAN_UAT_PENDING 四项完成并留档
- [ ] 报表与最终 commit 一致：`P3-QA/P3-DEFECTS/P3-COVERAGE/CHANGELOG-P3/NEXT-PLAN/STATUS/QA/COVERAGE/SOURCES.csv`

## 5. 建议节奏

1. 第 1 批：R7 query relevance（query 权重 + aliases/tags + example 排除）→ 复评 ≥4.0；verifier 复验。
2. 第 2 批：R1 职业同义词/医疗内层 + R2/R3 + R4/R5/R6；重跑 41+ 例。
3. 第 3 批：覆盖扩展（pattern/material/structure/来源接入）。
4. 收尾：HUMAN_UAT_PENDING 四项 + 发布清单签字。
