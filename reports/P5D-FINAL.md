# P5-D 最终验收结论（P5D-FINAL）

- 定稿：2026-11-05 10:47（Asia/Shanghai）；verifier / task-86；快照：HEAD `3c9d216`（P5-D commit；458 卡）；**458 卡 = 224 内容 + 234 来源**
- 依赖：`P5D-BASELINE`、`P5D-RELATION-BACKFILL`、`P5D-RELATION-QA`、`P5D-COVERAGE`、`P5D-SEMANTIC`、`P5D-BOOK-EVIDENCE`、`P5D-AGENT-REGRESSION`
- 声明：未改卡片/脚本；GUI 未执行，不得声称通过。

## 0. 结论摘要

**P5-D 关系治理/回填/书籍证据通过最终验收（PASS，附 WARN）：**
- **关系**：265 → **308**（+43；30 design 写入中 **25 有效**，6 MISLINK 已关闭：5 移除 + 1 降级；19 book claim 中 **18 保留**，GAR-0033 WEAK 移除）；`relation_consistency` **0 errors / 308 relations**；subject-type 校验已加入脚本（`invalid_subject_type`）。
- **抽样**：独立抽 **60 条**当前关系（32 design + 18 book claim + 10 high claim）严格核对（target/结构化/可见/subject/schema/证据/置信），**60/60 = 100%**（≥95% PASS）。
- **覆盖**：garment→material **37→39/92（42.4%）**、garment→claim **86→87/92（94.6%）**；component/style/outfit/narrative 持平（component 17.4%、style 2–3%、outfit 59.8%、narrative 71.4%）；来源可见 **352/460→370/478（77.4%）**，可见来源 167→172。
- **书籍**：5 本 connected（SRC-0061/0062/0064/0066/0069），4 本背景（0063/0065/0067/0068）；**有效 17 卡/18 book claims**；0 evidence_status 变更；页码 UNCONFIRMED。
- **回归**：acceptance 45/45、quality PASS、composer 9/9、workflow 9/9、Macbeth **11/11**、relation_trace 6/6、security/lookbook/skill-sync/backup/human、validate 458、build 234、validate_outfits 35（12+23 legacy）——以 engineer P5-D logs 为主，另本轮独立 validate/build/consistency/relation_trace/validate_outfits/security/lookbook/skill-sync/backup PASS；quality/Macbeth/human 独立复跑未在窗口完成 → **独立 NOT_RUN**（不写独立 PASS）。
- **E2E**：official RQ4–6 **3/3**、overlay RQ4/7/8 **3/3**，五项全满足。
- **门禁**：PRIVATE-READY/PRIVATE-USE = **YES（附 WARN：6 flags 人工、38 draft、59 isolates、页码 UNCONFIRMED）**；PUBLIC-READY = **NO（B1–B6 + L1–L6）**；**GUI = NOT_RUN/PENDING**。

## 1. 回填数量与质量（问题 1）

| 项 | 数值 |
|---|---|
| 起始 | 265 relations（P5-C 提交） |
| design pilot | 30 条写入；**25 条语义有效**；5 条 MISLINK（SCN→STY 1、LOOK→STR may_have_part 4）**已移除** |
| book claims | 19 条应用；**18 条保留**；GAR-0033→SRC-0066（1940s 卡引 1908 词典，WEAK）**已移除** |
| MISLINK 关闭 | **6/6**：5 移除 + **GAR-0079→SRC-0069 降为 interpretive/medium**（原 high 越级） |
| 最终 relations | **308**（claim 256 / uses_material 14 / in_style 14 / style_interpretation 12 / look_scene 6 / appears_in_look 6）；evidence 269 verified + 39 interpretive；confidence 262 high + 46 medium |
| consistency | **0 errors**；scripts 已含 `invalid_subject_type`（本次 0 命中） |
| 未写卡 | **239 条候选**仍在 `11-验收/P5D/REVIEW-QUEUE.csv`（未自动提升） |
| 自动提升 | **0**（draft/verified 未变；38 基线 draft 保持） |

## 2. 覆盖率变化（问题 2；同口径，Final=308）

| 指标 | Before（265） | After（308） | 说明 |
|---|---:|---:|---|
| garment→material | 37/92（40.2%） | **39/92（42.4%）** | +2（design/token 回填） |
| garment→claim/source | 86/92（93.5%） | **87/92（94.6%）** | +1（book claim） |
| garment→component | 16/92（17.4%） | **16/92（17.4%）** | 持平（缺口） |
| garment→style | 2–3/92（2–3%） | **2–3/92** | 持平（缺口） |
| garment→outfit | 55/92（59.8%） | **55/92（59.8%）** | 持平 |
| LOOK→narrative | 25/35（71.4%） | **25/35（71.4%）** | 持平（P5-B 56.5%） |
| 全部 relations | 265 | **308** | +43 |
| 来源可见（单列） | 352/460（76.5%） | **370/478（77.4%）** | 可见来源 167→172；零可见卡 39（38 draft + GAR-0045） |

- **不混算**：design/review（239 未写卡）不计入正式覆盖；high 262 / medium 46 分开；来源可见率单独统计。
- 结论：**关系数增加不等于卡级覆盖提升**；结构（component 17.4%）、风格（2–3%）、Outfit 细分仍是主要缺口。

## 3. 旧卡 Agent 可用性（问题 3）

- `relation_trace` / query 可检索新增 design 关系（design-only，factual=false；Agent 过滤规则已写入 `00-系统/关系类型.md` v3）。
- 6 MISLINK 中 5 条主语类型错误（此前 relation_trace 会展示）已删除；1 条 book claim 已降级 → **Agent 不再得到越级/错误主语路径**。
- E2E 官方 RQ4–6、overlay RQ4/7/8 各 3/3，五项（skill/工具/结果/turn_end.completed/完整输出）全 PASS；IDs 0 missing。
- 限制：`11-验收/P5D/REVIEW-QUEUE.csv` 239 条候选未写卡，Agent 不可见（预期，避免弱连）；`relation_trace` 不把 wikilink 当事实关系；`disturbed` 样例见 P5D-AGENT-REGRESSION。

## 4. 书籍级证据（问题 4）

| 项 | 结果 |
|---|---|
| connected（5 本） | SRC-0061（PG21534 Textiles and Clothing）、SRC-0062、SRC-0064、SRC-0066（PG76299 Men's Wear）、SRC-0069 |
| 背景（4 本） | SRC-0063、SRC-0065、SRC-0067、SRC-0068（未接卡） |
| 应用记录 | 18 卡 / 19 组（`11-验收/P5D/book-source-application.csv`）；**有效 17 卡 / 18 book claims**（GAR-0033 移除） |
| 定位 | book_fact 章/段/行；page **UNCONFIRMED** |
| evidence_status | **未改**（GAR-0079 仍 interpretive；不因书源升级） |
| 风险 | 书=公版文本+现代转录；页码未核；V&A/AAT 许可边界保持；无图片 |

> 不一致：P5D-BOOK-EVIDENCE §9 记「18 卡/19 组」，移除 GAR-0033 后实际 **17 卡/18 claims**；报告需按最终口径引用。

## 5. 仍缺知识（问题 5）

- **结构**：component 16/92（17.4%），领型/袖型/门襟等大量 garment 无 STR 关系；silhouette 仅字段层（无目标卡）。
- **风格**：garment→style 2–3/92；style→garment 太弱；5 本风格卡未充分回连。
- **材质**：39/92（42.4%），且 token 级 medium 需正文 marker；STR-0029→MAT-0001 仍 review。
- **Outfit/叙事**：LOOK→narrative 25/35（71.4%）；连续状态/场景→outfit 未系统化。
- **书籍**：4 本背景书未接卡；book_fact 页码 UNCONFIRMED；6 组部分支撑候选未应用。
- **其他**：38 基线 draft、59 isolates（+3 未分类 uncited：SRC-0163/0157/0175）、6 key_garments flags、239 候选队列。

## 6. 回归与 E2E（证据）

| 套件 | 结果 |
|---|---|
| validate 458 / build 234 / consistency 0 | **本轮独立 PASS** |
| acceptance | **PASS 45/45**（P5-D log） |
| quality_eval | **PASS**（engineer log `QUALITY=PASS`）；本轮独立复跑 96.6s 未完成被终止（EXIT -15）→ **独立 NOT_RUN**，不写独立 PASS |
| composer | **PASS 9/9**（log） |
| workflow | **PASS 9/9**（log OK） |
| Macbeth | **PASS 11/11**（engineer log `MACBETH=0`）；本轮独立复跑未启动（随 quality 终止，0.0s）→ **独立 NOT_RUN** |
| relation_trace / security / lookbook / skill-sync / backup | **PASS**（本轮独立）；human closeout **engineer log PASS**（独立复跑在第三测中断 → 独立 NOT_RUN） |
| validate_outfits | **35 looks / 12 pass / 23 legacy / 0 fail**（engineer log）；本轮独立测试 **EXIT 0** |
| E2E official / overlay | **3/3 / 3/3**，五项全 true（P5D/e2e/validation-summary.json） |
| GUI | **NOT_RUN**（无 Obsidian 截图/签字） |

## 7. 最终版本回复（六个问题）

1. **回填数量/质量**：265→308；30 design 中 25 有效、5 MISLINK 移除；19 book claim 中 18 保留（GAR-0033 WEAK 移除）；6 MISLINK 全关闭（5 删 + GAR-0079 降级）；239 候选未写卡；0 自动提升；抽样 60/60=100%。
2. **覆盖率变化**：material 37→39/92、claim 86→87/92；component/style/outfit/narrative 持平；来源可见 352/460→370/478（77.4%）；关系数 +43 但卡级覆盖主要缺口未变。
3. **旧卡 Agent 可用性**：relation_trace/query 可用；错误主语 5 条已删，book 越级 1 条已降；E2E 3/3+3/3 五项；239 候选不可见（有意）；仍受 draft/低置信过滤限制。
4. **书籍级证据**：5 本 connected + 4 背景；应用记录 18 卡/19 组，**有效 17 卡/18 claims**（GAR-0033 WEAK 移除）；book_fact 章/段/行、page UNCONFIRMED；未改 evidence_status。
5. **仍缺知识**：component 17.4%、style 2–3%、material 42.4%、outfit/narrative 71.4%；silhouette 无卡；4 背景书、6 部分支撑候选、239 队列、38 draft、59 isolates、6 flags。
6. **未关闭门禁**：PRIVATE **YES（WARN：6 flags 人工、38 draft、59 isolates、页码 UNCONFIRMED）**；PUBLIC **NO（B1–B6 + L1–L6）**；GUI **NOT_RUN**。

## 8. 门禁与建议

- **PRIVATE-READY / PRIVATE-USE = YES**（技术/数据层；附 WARN）
- **PUBLIC-READY = NO（BLOCKED）**
- **GUI / HUMAN UAT = NOT_RUN/PENDING**
- 建议：提交 P5-D（148 项）；更新 P5D-BOOK 应用记录为 17/18；更新 isolates 文件（62 uncited/3 未分类）；处理 6 flags/38 draft；补 quality/Macbeth 独立留档（本轮已跑，见日志）；清理 STR-0029/GAR-0088 两条 material WARN。
