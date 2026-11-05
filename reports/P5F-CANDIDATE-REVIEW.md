# P5-F 39 条 source_verifiable 候选裁决

- 任务：task-94（P5-F 任务二）；日期 2026-11-05（Asia/Shanghai）
- 输入：`11-验收/P5E/candidate-review.csv` 中 `tier=source_verifiable` 的 **39** 条；全部 `uses_material`、evidence=interpretive、confidence=medium、`design_only=true`（P5-E 生成，未写卡）
- 输出：`11-验收/P5F/candidate-verdicts.csv`（39 行）+ 本报告
- 规则：`00-系统/关系类型.md` v3/v3.1（`uses_material` 设计关系最高 medium，property/pattern 不得为目标/主体；不得自动升 high/verified）；本任务 **0 卡写入、0 自动提升**。

## 0. 裁决分布

| verdict | 数量 | 含义/动作 |
|---|---:|---|
| **VERIFIED** | **18** | 端点均 verified、source_ids 均 verified、共享材料 token；**可作为 medium design-only 关系建议正式入库**（不是 high/verified；需另任务写卡+可见 marker） |
| **REVIEW_REQUIRED** | **15** | 语义/本体边界问题，保留人工审核；不得自动入库 |
| **REJECTED** | **6** | 本体规则明确不合法（自指/物性卡主体）；不得入库 |
| **INSUFFICIENT_EVIDENCE** | **0** | 本批无此类（source_verifiable 已筛过端点/来源） |
| **合计** | **39** | 可提出正式 medium 建议 **18**；review 15；reject 6 |

> **命名说明**：`VERIFIED` 仅表示“证据链/本体检查通过，可建议作为 **medium design-only** 关系入库”；**不等于** `evidence_status=verified`，也不等于 high/事实。任何 high/verified 提升需单独人工审批，本任务 0 提升。

## 1. VERIFIED 18（可建议正式 medium design 入库）

| target | cards |
|---|---|
| MAT-0016 亚麻织物（7） | GAR-0077, GAR-0078, GAR-0076, GAR-0061, GAR-0075, STR-0003, STR-0005 |
| MAT-0017 皮革（8） | GAR-0022, GAR-0023, GAR-0024, GAR-0058, GAR-0060, GAR-0081, GAR-0084, GAR-0080 |
| MAT-0019 现代合成/涂层（3） | GAR-0057, GAR-0022, GAR-0058 |

- 证据：subject/target 均 `verified`；`source_ids` 均解析到 verified 来源；subject `materials` 与 target `materials/fiber_content` 存在精确共享 token（linen/leather/rubber/vinyl）。
- 本体：target 为 material/leather/synthetic 实体卡，不是 MAT-0012/0013 物性卡，也不是 pattern；subject 为 garment/garment_part，不是 style/PRD；无自指。
- 动作：**建议另任务**以 `confidence=medium; evidence=interpretive; factual=false; design_only=true` 写入并补正文可见 `[[target]]`；**不得 high/verified**；写入前重跑 validate/build/relation_consistency。
- 注意：CSV 中 `source_audit_ok=false` 全部为真（P5-E 的 source-audit 白名单仍 211，未含新增来源；不是“来源不存在”）；source 卡均 verified；正式入库前仍应由 source owner 刷新 audit。

## 2. REVIEW_REQUIRED 15（保留审核，不自动入库）

| 原因组 | 数量 | 候选 |
|---|---:|---|
| target 为 trim/metal-fiber（MAT-0003 装饰绦带 / MAT-0004 卢勒克斯金属线）；token 可能只反映部件/纤维列表，不能直接等同物体材质 | 6 | GAR-0076→MAT-0003, GAR-0023→MAT-0003, GAR-0036→MAT-0004, GAR-0066→MAT-0003, GAR-0067→MAT-0003, STR-0006→MAT-0003 |
| subject 为 style/period_region；`uses_material` 会变成风格/语境的设计解释，不是物理“使用材料”事实 | 9 | STY-0001→MAT-0001, STY-0003→MAT-0003, STY-0007→MAT-0017, STY-0009→MAT-0019, STY-0009→MAT-0004, STY-0010→MAT-0016, PRD-0001→MAT-0016, PRD-0004→MAT-0003, PRD-0007→MAT-0004 |

- 动作：保留 `review_queue`，由人工/领域 owner 确认语义；即使确认，也只能 medium design，不能 high/事实。
- 不得为覆盖率/候选数强行改成 VERIFIED。

## 3. REJECTED 6（本体不合法）

| 候选 | 原因 |
|---|---|
| MAT-0003→MAT-0003 | 自指：material→itself 不是 uses_material 事实 |
| MAT-0004→MAT-0004 | 自指 |
| MAT-0008→MAT-0008 | 自指 |
| MAT-0009→MAT-0009 | 自指 |
| MAT-0010→MAT-0010 | 自指 |
| MAT-0013→MAT-0016 | subject 是物性卡（克重/垂坠），v2 规则排除其作为 uses_material 主体 |

- 动作：`do_not_propose`；不得改写为其他关系/目标来“救活”候选。

## 4. 与独立队列的关系

- 本任务只处理 P5-E 的 **39 条 source_verifiable**；**38 张 draft、6 个 key_garments flags、163 条 needs_human、37 条 reject_or_rework/其他队列保持独立**，未合并、未改状态、未提升。
- `11-验收/P5E/candidate-review.csv` 239 行其他 200 条不在本轮 verdict 内；仍由原队列处理。
- 本任务 **不写卡**；18 条 VERIFIED 只是**建议**，正式入库必须另立写卡任务并备份/回归。

## 5. 验证/边界

- 输入 39 条均可解析；CSV 39 行与输入 1:1；无重复 candidate-target。
- 未改卡片/来源/脚本；`validate.py` PASS 458/458；`relation_consistency.py` 308 relations/0 errors（本任务未触发写卡）。
- 主要残留：source-audit 白名单 211 未含 SRC-0530..0552；`source_audit_ok=false` 不能当正式审计通过；VERIFIED 18 仍为 design-only medium，不得宣传为已入库/已 high。
