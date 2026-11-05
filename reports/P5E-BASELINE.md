# P5-E 启动核对与图谱基线（P5E-BASELINE）

- 生成：2026-11-05 11:02（Asia/Shanghai）；verifier / task-87（P5-E 启动核对，只读）
- 快照：**HEAD `0e8d37d`**（P5-D 已提交：3c9d216 + 0e8d37d）
- 工作区（定稿时 26 项）：21 个 sandbox 未跟踪、P5-E 队友产物（`11-验收/P5E/`、`scripts/candidate_review.py`、`tests/test_candidate_review.py`）、本报告，以及 **1 个被安全测试重写的审计文件** `11-验收/R1.1/security/path-guard-audit.jsonl`；**无卡片/脚本事实改动**
- 规模：**458 卡 = 224 内容 + 234 来源**；`validate PASS 458/458`、`build_sources PASS 234`、`relation_consistency` **0 errors / 308 relations**
- 图工具：`scripts/graph_analyze.py --root .`（只读；当前 489 节点快照，`/tmp/p5e_graph.json`）
- 性质：只写本报告；未改卡片/脚本。

## 1. HEAD / 工作区 / 数据完整性（PASS）

| 项 | 值 |
|---|---|
| HEAD | **`0e8d37d`**（P5-D sync；父 3c9d216） |
| 工作区 | 定稿时 26 项：21 sandbox + P5-E 产物 + 本报告 + 1 个审计 JSONL 重写；**无卡片改动** → P5-D 已提交，基线稳定 |
| 卡片 | **458 = 224 内容 + 234 来源**（garment 92 / part 35 / look 35 / material 16 / style 16 / scene 16 / PRD 11 / pattern 3） |
| relations | **308**：claim 256 / uses_material 14 / in_style 14 / style_interpretation 12 / look_scene 6 / appears_in_look 6；high 262 / medium 46 |
| validate / build / consistency | **458/458 PASS / 234 PASS / 0 errors** |
| 未解决（图工具） | typed_unresolved **5**、unresolved_wikilink **1**（见 §6，E5 需核查） |

## 2. P5-A–D 报告要点（供 P5-E 继承）

| 阶段 | 关键交付/指标 | 关键限制 |
|---|---|---|
| **P5-A**（1acb4d3） | 图谱诊断：416 节点；内容零链接 0/189；来源零可见 58/211；source_ids 299→可见 2；typed 485→无可见 313；分量 66（335+65）；MOC 9 页；来源可见迁移 | 来源可见仍低；书源未接卡；导航/研究分层 |
| **P5-B**（f500289） | 201 relations；8 WEAK 处置；`source_ids` 可见 191/299（63.9%）；零可见卡 38 draft + GAR-0045；65 单点；组件 66 | 1 条 formal 无可见（GAR-0045 review）；6 flags 人工 |
| **P5-C**（5ae2c52） | +35 内容卡/+23 来源（458）；265 relations；12 Outfit 12/12；来源可见 352/460（76.5%）；E2E 3/3+3/3 | 71 consistency 临时错误→修复；6 MISLINK 待 P5-D |
| **P5-D**（0e8d37d） | 308 relations；25 design 有效、6 MISLINK 关闭（5 删 1 降）、18 book claims；抽样 60/60；来源可见 370/478（77.4%）；59 isolates；5 本 connected 书 | 239/244 队列口径、17/18 卡书账目、GUI NOT_RUN |

## 3. P5-E 前基线（当前，E5 对比起点）

### 3.1 覆盖率（卡级，P5-D 口径）

| 维度 | 当前 | 说明 |
|---|---:|---|
| garment→component | **16/92（17.4%）** | 最大结构缺口 |
| garment→material | **39/92（42.4%）** | token/design 回填后 |
| garment→style | **2/92（2.2%）** | STY 精确关系；风格卡未充分回连 |
| garment→footwear-accessory | **63/92（68.5%）** | P5-D 矩阵口径 |
| garment→outfit | **55/92（59.8%）** | 12 LOOK 已接卡 |
| LOOK→narrative | **25/35（71.4%）** | P5-B 56.5% |
| garment→claim/source | **87/92（94.6%）** | P5-D +1 |
| 全部 relations | **308** | high 262 / medium 46 |
| design/review 未写卡 | **239（任务口径；实际文件 244 行，见 §6）** | 不进正式覆盖 |

### 3.2 来源可见率（单独口径，不混算）

| 指标 | 当前 |
|---|---|
| source_ids 机器对 | **478** |
| 正文可见 SRC 对 | **370（77.4%）** |
| 被引用/可见来源 | **172 / 172（100%）** |
| 零可见 SRC 卡 | **39**（38 draft + GAR-0045 medium review） |
| 图工具 source_ids 无可见 | 108（=478−370）；卡片有≥1不可见=40 |
| MOC/导航可见来源 | 全部 234（仅导航，不计语义） |

### 3.3 单点 / draft / flags / 队列

| 项 | 当前 |
|---|---|
| **59 isolates** | `11-验收/P5C/isolates.csv` **59 行**；图工具 singleton components **59**；另有 3 个 uncited 未分类来源（SRC-0163/0157/0175）→ uncited 总数 62 |
| **38 draft（基线）** | 38 张基线 draft 保持（零可见 SRC：look22/scene15/style1）；全库 draft **79**（含新 LOOK/STY） |
| **6 flags** | PRD-0004→GAR-0007；PRD-0006→GAR-0022；PRD-0007→GAR-0023；PRD-0008→GAR-0014、MAT-0004；PRD-0011→GAR-0033；仍 review_queue，**未自动确认** |
| 审核队列 | `11-验收/P5D/REVIEW-QUEUE.csv` 实际 **244 行**（appears_in_look 116 / uses_material 70 / in_style 33 / look_scene 16 / may_have_part 9；全部 medium） |
| 书源 | 5 本 connected（SRC-0061/0062/0064/0066/0069）；4 背景（0063/0065/0067/0068）；有效 **17 卡/18 claims** |
| E2E | official RQ4–6 3/3、overlay RQ4/7/8 3/3（五项全 true） |
| GUI | **NOT_RUN**（无 Obsidian 截图/签字） |
| quality_eval / Macbeth | **P5-D 提交版证据**：quality **PASS**、Macbeth **11/11**（`11-验收/P5D/regress-quality.log`、`regress-macbeth.log`）；**P5-E 本轮日志为空/未跑**（quality/composer/acceptance log 0 字节，Macbeth 无日志）→ 新窗口 **NOT_RUN**，不写 PASS |
| 239 候选审查 | `11-验收/P5E/summary.json`：239 reviewed；tier = source_verifiable 39 / needs_human 163 / reject_or_rework 37；auto_promotions 0 / card_writes 0 |

## 4. P5-A 之前图谱基线（E5 对比锚点）

来源：`reports/P5-GRAPH-DIAGNOSIS.md`（HEAD `1acb4d3` 干净快照，400 卡；P5-A 迁移**前**）。

| 指标 | P5-A 之前（1acb4d3） | P5-A 之后（P5-GRAPH-AFTER） | 当前（458 卡） |
|---|---:|---:|---:|
| 扫描节点 | **416**（content 189/source 211/nav 14/research 2） | 426（nav 24） | **489**（content 224/source 234/nav 26/research 5） |
| Wikilink 出现次数 | **1271** | 1944 | **2327** |
| 去重可见边 | **1114**（语义 1090 + 导航 24） | 1775（语义 1281 + 导航 494） | **2138**（语义 1643 + 导航 495） |
| 内容卡零可见链接 | **0/189** | 0/189 | **0/224** |
| 来源卡零可见链接 | **58/211** | 0/211（MOC 导航） | **0/234**（MOC 导航） |
| source_ids 机器对 | **299** | 299 | **478** |
| source_ids 有可见链接 | **2/299（0.7%）** | 193/299（64.5%） | **370/478（77.4%）** |
| 被引用来源 | **143** | 143 | **172** |
| 其中可见 | **2** | 143 | **172** |
| typed 边 | **485** | 485 | **737** |
| typed 无可见 | **313（64.5%）** | 122（25.2%） | **123**（source_ids 108 + key_garments 15） |
| 语义分量数 | **66** | 66 | **60** |
| 最大分量 | **335**（189 content + 146 source） | 335 | **399**（224 content + 175 source） |
| 单点分量 | **65**（全 source） | 65 | **59**（全 source） |
| 书源（9 本） | 仅研究文档，未接卡 | 同 | **5 本 connected / 4 背景** |

P5-A 之前的关键病灶（E5 应继续对比）：
- 内容卡零链接 0，但 **来源 58/211 零可见**；source_ids 297/299 不可见；
- 内容→source 可见仅 **2 对**；source→content 出链 186；
- 65 个来源单点（28 isolated + 27 background + 9 nav-only 书源 + 1 book）；
- 9 本书源只在 research 文档可见、未进入卡片图；
- 导航层 9/14 零可见。

## 5. 当前图（458 卡）补充指标（E5 起点）

- 图工具：**489 扫描文件 / 224 content + 234 source + 26 nav + 5 research**；components **60**；largest **399**（224 content+175 source）；singletons **59**；source reasons：linked_visible 172 / navigation_only 62。
- 内容→source 可见 370；source→content 186；source→source 16；content→content 1071。
- **注意**：来源卡「零可见 0」是 MOC/导航链接的功劳；**语义接入**仍以 source_ids/可见对衡量（370/478，77.4%），不可把导航可达当语义连通。
- 图工具报告 **typed_unresolved 5**、**unresolved_wikilink 1**（具体 ID 未在图 JSON 展开；E5 应核查并归零或解释）。

## 6. 不一致清单（E5 必须知道）

1. **队列口径 239 vs 244 vs 269**：P5-D 任务/报告写 239，P5D-BACKFILL 写 269，当前 `REVIEW-QUEUE.csv` 实际 **244 行**（全 medium）；239 未与文件对齐。
2. **P5D-COVERAGE 314 vs 最终 308**：314 为 MISLINK 清理前；最终 308（5 design 移除 + GAR-0033 移除；GAR-0079 降级）。
3. **书源账目 18 卡/19 组 vs 有效 17 卡/18 claims**：应用记录 CSV 仍 19 行/18 卡（含 GAR-0033），GAR-0033 WEAK 已移除。
4. **来源可见 479/371 vs 478/370**：后者为最终（GAR-0033 book source 移除后）；E5 以 **478/370（77.4%）** 为基线。
5. **59 isolates vs 62 uncited**：59 为 isolates.csv/图 singleton；另有 3 个 uncited 未分类 SRC-0163/0157/0175。
6. **图工具 5 typed_unresolved + 1 unresolved wikilink**：当前未在报告中定位；E5 应先解释/修复，避免污染 E5 图对比。
6b. **P5-E 团队日志不完整**：validate/build/consistency PASS；acceptance/composer/quality log 0 字节、Macbeth 无日志、test-candidate-review log 空 → 不可作为回归 PASS 证据，E5 需重跑并留档。
6c. **队列两个数**：`summary.json` 候选 239（E1/E4 审查口径）vs `REVIEW-QUEUE.csv` 244 行（写入卡/清理后文件）；239 是“候选审查数”，244 是“当前文件行数”，引用需带口径。
7. **P5-D 报告/STATUS 仍写「P5-D 未提交」**：实际 HEAD `0e8d37d` 已提交 P5-D（3c9d216+0e8d37d）；旧 WARN 需更新。
8. **quality/Macbeth/human 独立复跑**：P5-D 仅有 engineer logs PASS；本轮独立窗口未完成（NOT_RUN）——E5 若要“独立”证据需重跑并在报告中区分。
9. **P5-C/P5-D 报告关系数**：P5C 写 265、P5D 写 308；当前一致 308；引用时带阶段。

## 7. 结论

- 基线稳定：HEAD 0e8d37d、458 卡、308 relations、0 consistency errors、validate/build PASS。
- P5-E 起点：**coverage 见 §3.1、source visible 370/478（77.4%）、244 队列（任务口径 239）、59 isolates、38 基线 draft、6 flags**；P5-A 前图谱锚点见 §4（416 节点/485 typed/313 不可见/66 分量/65 单点）。
- E5 对比时须区分：**语义可见 vs MOC 导航可见**、**formal vs review 队列**、**high vs medium**、**P5-A 前 vs 当前分母**。
