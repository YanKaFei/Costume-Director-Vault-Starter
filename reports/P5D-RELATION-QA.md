# P5-D 关系质量治理（task-82）

- 日期：2026-11-05（Asia/Shanghai）
- 快照：**458 卡 = 224 内容 + 234 来源**；**265 条 cards relations**（claim_supported_by 238 / style_interpretation 12 / in_style 8 / uses_material 7）
- 校验：`validate.py` **PASS 458/458，0 errors/0 warnings**；`relation_consistency.py` **cards=458 relations=265 errors=0 moc_skipped=9**
- 性质：**只读治理**；未改任何卡片事实/状态/关系；只写 `reports/P5D-RELATION-QA.md`、`11-验收/P5D/review-queue.csv`、`11-验收/P5D/semantic-spotcheck.csv`，并更新 `00-系统/关系类型.md` 一条 visibility 规则
- 注：同目录已有 engineer 的 `REVIEW-QUEUE.csv`（大写）/backfill artifacts；本任务按任务书面路径写小写 `review-queue.csv` 与 `semantic-spotcheck.csv`，未覆盖 engineer 文件。

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| STR-0029→MAT-0001 medium WARN | **保留 review，不升级/不自动删除**；source SRC-0533 支持 muslin 实例，但 part→material 仅 token/实例关联且正文无可见 MAT marker；需卡片 owner 补 marker 或移除 |
| 6 组 key_garments flags | 6/6 给出人工建议（5 建议移除、1 条件保留/补证）；**未自动确认/未改卡** |
| 38 张基线 draft | 38/38 仍 draft；**仅生成审核队列/candidate-only**，未提升 reviewed/verified，未批量补关系 |
| 64 个有效语义单点 | 64/64 保留原因复核；**不为降低单点数强连**；`isolates.csv` 仍 65（SRC-0013 已被 MAT-0018 引用→有效 64，文件未更新） |
| 已存在关系 vs 可见 Wikilink | 全量 **262/265 visible**；3 条 medium 无可见 marker（STR-0029→MAT-0001、GAR-0088→MAT-0017、GAR-0045→SRC-0405）；抽样 **41 条**（13 PASS / 25 DESIGN_ONLY / 3 WARN） |
| 人工审核队列 | **111 行**：3 WARN + 6 key_garments flags + 38 draft + 64 isolate；P1 9 行（WARN+flags），P2 102 行 |

## 1. STR-0029→MAT-0001（medium WARN）

- 当前 formal relation：`target=MAT-0001; type=uses_material; direction=outgoing; evidence=verified; confidence=medium; source_ids=SRC-0533; rule=R-MAT-TOKEN`。
- 证据：SRC-0533 V&A O353415 原文 “white muslin dress … long puffed and pleated sleeves”；MAT-0001 是 muslin/平纹细布，token 可解释。
- 问题：STR-0029 是**结构卡（泡泡袖）**，`uses_material` 来自“该实例裙为 muslin”，是实例/材料族关联，不是“泡泡袖结构必然使用 muslin”；且正文没有 `[[MAT-0001]]` 可见 marker（relation_consistency 允许 medium design 关系，故 0 errors 但按 P5-C WARN 口径未达可见性）。
- **决策：保留 review，不升级、不自动移除**（移除需卡片 owner；本任务不改卡）。
  - 不计入强证据/覆盖；Agent 不得用该关系作材料事实；
  - 卡片 owner 二选一：正文补 `[[MAT-0001]]` 可见 marker（保持 medium review），或移除该 relation；随后重跑 relation_consistency。
- 队列：`Q-0001`（P1，blocks_historical_use=yes）。

## 2. 6 组 key_garments flags（人工建议，**不自动确认**）

| flag | PRD / 目标 | 现状/证据 | 建议（人工） |
|---|---|---|---|
| FLAG-KG-04 | PRD-0004 1920s → GAR-0007 | GAR-0007 periods=1890s/Edwardian/early20c；仅边界相邻 | **建议从 key_garments 移除**；若保留需 owner 补 1920s 来源 |
| FLAG-KG-06B | PRD-0006 1940s → GAR-0022 | Wellington 19c/contemporary；1940s 无重叠 | **建议移除**，或 owner 替换为有来源的 1940s 鞋 |
| FLAG-KG-07 | PRD-0007 1950s → GAR-0023 | moccasin 19c/contemporary；region indigenous_america 与美英不直接兼容 | **建议移除**；除非 owner 补跨文化/年代证据 |
| FLAG-KG-08 | PRD-0008 1960s → GAR-0014 | 牛仔裤 1950s/contemporary，无 1960s 字段 | **条件保留**：reviewer 认可“1960s 延续”才保留；否则移除/owner 补 period 来源 |
| FLAG-KG-08B | PRD-0008 1960s → MAT-0004 | Lurex 1940s/1970s/contemporary，无 1960s 精确重叠 | **建议移除**，或 owner 补 period 来源后再保留 |
| FLAG-KG-11 | PRD-0011 1930s 上海 → GAR-0033 | GAR-0033 periods=1940s；PRD 1930s | **建议移除**；除非 owner 补 1930s Shanghai 证据 |

- 6 行均在 `review-queue.csv`（category=KEY_GARMENTS_FLAG，priority=P1，blocks_historical_use=yes）；**未改任何 key_garments/卡片**。补证/替换不得为覆盖率硬连。

## 3. 38 张基线 draft（只做 candidate-only）

- 口径：`review_status=draft` + 有 `source_ids` + 正文无可见 `[[SRC-…]]`；当前命中 **38** 张（STY 1 / SCN 15 / LOOK 22）。
- 全库 draft 实际 **79**（P5-C 新增 12 LOOK +5 STY 等未计入本 38 基线）；本任务只审核 38 基线，不把新增 draft 一并提升/补关系。
- 决策：全部保持 `draft`；只在审核队列生成“candidate relation/可见来源确认”建议；**不写 verified/reviewed、不批量补关系**。队列 38 行（category=DRAFT_BASELINE，P2）。

## 4. 64 个有效语义单点（不强制连接）

- `11-验收/P5B/isolates.csv` 仍 65 行；**SRC-0013 已被 MAT-0018 引用** → 有效 **64**（文件未更新，属 P5-C 残留）。
- 有效 64 行分类：legit_reference **33** / evidence_missing_expression **16** / future_topic **14** / no_verifiable_relation **1**；原因计数：isolated_source 28 / background_or_dictionary_uncited 26 / navigation_only 9 / book_source_no_card_integration 1。SRC-0013 原为 legit_reference，已由 MAT-0018 引用。
- 决策：64/64 保留原因复核；**不为降低单点数强连**。legit_reference/independent → 保留；future_topic → backlog；evidence_missing_expression → 人工确认后再补表达；无依据不造关系。队列 64 行（ISOLATE，P2）。

## 5. 类型化关系 vs 可见 Wikilink（抽样 41，全量 262/265）

- 全量：265 relations 中 **262 visible**、3 条 medium 无可见 marker（见 §1 与 `Q-0002/Q-0003`）。
- 抽样 41 条：**13 PASS（claim high + visible）/ 25 DESIGN_ONLY / 3 WARN**；`semantic-spotcheck.csv` 每行含 card/relation/target/evidence/confidence/visible/is_strong_evidence/judgement/action。
- 强证据口径：仅 `claim_supported_by` + high + visible 计 `is_strong_evidence=yes`；`style_interpretation`/`uses_material`/`in_style` 即使 high/medium 也只作设计/材料候选，**low/medium 一律不进强证据**。
- `style_interpretation` 12 条全部 design-only/medium、有可见 LOOK 链接；未当史实。
- 3 条 WARN：STR-0029→MAT-0001、GAR-0088→MAT-0017、GAR-0045→SRC-0405；均进队列，不自动改卡。

## 6. 人工审核队列

`11-验收/P5D/review-queue.csv`：111 行，字段 `queue_id,category,item_id,item_type,issue,evidence,current_state,recommendation,required_human_action,priority,blocks_historical_use`。

| category | 行数 | 说明 |
|---|---:|---|
| WARN_RELATION | 3 | STR-0029 / GAR-0088 / GAR-0045 medium 无可见 marker |
| KEY_GARMENTS_FLAG | 6 | 6 flags 人工结论建议，不自动确认 |
| DRAFT_BASELINE | 38 | 38 基线 draft，candidate-only，不提升 |
| ISOLATE | 64 | 有效单点，保留独立/backlog，不强连 |
| **合计** | **111** | P1 9 / P2 102；WARN/flag 标 blocks_historical_use=yes |

## 7. 规则更新（`00-系统/关系类型.md` v3.1）

- 新增 visibility 规则：medium 的 `uses_material`/`may_have_part`/`ensemble_with`/`style_interpretation` 必须有正文可见 `[[target]]` 或 review marker；无 marker → `review_queue`，**不计强证据/覆盖**（STR-0029 即例）。
- high factual 关系（claim/context）仍必须 visible；design-only 关系不得因“有来源”升格为事实。
- 兼容：v2/v3 八类/九类关系与旧卡均不需迁移；未改卡片。

## 8. 残余风险

1. STR-0029、GAR-0088、GAR-0045 的 medium 无可见 marker 仍在 formal relations；需卡片 owner 行动后重跑。
2. `11-验收/P5B/isolates.csv` 仍 65（有效 64），文件未更新；`11-验收/P5/source-audit.csv` 仍 211 白名单，未含 SRC-0530..0552；需 owner 重建。
3. 6 flags 未自动确认；任何移除/替换需人工证据，不得为覆盖率强连。
4. 38 基线 draft 之外仍有新增 draft（全库 79）；本任务未审新增 draft，未提升任何状态。
5. GUI/workflow 未运行；本任务只做静态关系/链接审查。


---

## 6. MISLINK 关闭复核（task-86 最终验收）

| # | MISLINK（P5D-SEMANTIC 发现） | 最终状态（独立核验） |
|---|---|---|
| 1 | SCN-0001 → STY-0005（in_style，scene 主语非法） | **已移除**（当前无该关系） |
| 2 | LOOK-0019 → STR-0011（may_have_part，LOOK 主语非法） | **已移除** |
| 3 | LOOK-0003 → STR-0001（may_have_part） | **已移除** |
| 4 | LOOK-0017 → STR-0010（may_have_part） | **已移除** |
| 5 | LOOK-0008 → STR-0011（may_have_part） | **已移除** |
| 6 | GAR-0079 → SRC-0069（interpretive 却 high，越级） | **已降级**：当前 evidence=interpretive、confidence=medium |
| WEAK | GAR-0033 → SRC-0066（1940s 卡引 1908 词典） | **已移除**（source_ids 不含 SRC-0066，仅 SRC-0204/0155） |

- subject-type 校验：`scripts/relation_consistency.py` 已含 `invalid_subject_type`（in_style 允许 garment/part/look/period_region；may_have_part/ensemble_with 仅 garment；appears_in_look/look_appears_in_scene 仅 look）；当前 **0 errors / 308 relations**。
- GAR-0079 保持 review（medium/interpretive），不计入 high 262；book 应用记录需从 18 卡/19 组更新为 **17 卡/18 claims**。
