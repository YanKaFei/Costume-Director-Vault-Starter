# P5-E 图谱对比（P5-A 前 → 当前）（P5E-GRAPH-COMPARISON）

- 生成：2026-11-05 11:40（Asia/Shanghai）；verifier / task-92（P5-E 最终验收，只读）
- 快照：**HEAD `0e8d37d` + P5-E 工作区**（458 卡 = 224 内容 + 234 来源；**334 relations**；validate 458 PASS；consistency 0 errors）
- 工具：`scripts/graph_analyze.py --root .`（当前 489 节点；`/tmp/p5e_graph2.json`），P5-A 前/后数据取 `reports/P5-GRAPH-DIAGNOSIS.md` / `P5-GRAPH-AFTER.md`
- 口径：**可见 Wikilink** 与 **YAML/结构化 typed** 分列；MOC/导航可达 ≠ 语义连通；**graph 工具的 typed_edges 不含卡片 `relations` 字段**（只计 source_ids/look_items/look_scene/key_garments/superseded/canonical），卡片 relations 另行统计。

## 1. 总表

| 指标 | P5-A 之前（1acb4d3，400 卡） | P5-A 之后（400 卡 +MOC） | **当前（P5-E 后，458 卡）** | 变化（前→当前） |
|---|---:|---:|---:|---:|
| 扫描节点 | **416**（content 189 / source 211 / nav 14 / research 2） | 426（nav 24） | **489**（content 224 / source 234 / nav 26 / research 5） | **+73** |
| Wikilink 出现次数 | 1271 | 1944 | **2353** | +1082 |
| 去重可见边 | **1114**（语义 1090 + 导航 24） | 1775（语义 1281 + 导航 494） | **2158**（语义 1663 + 导航 495） | **+1044** |
| 内容卡零可见链接 | **0/189** | 0/189 | **0/224** | 0（保持） |
| 来源卡零可见链接 | **58/211** | 0/211（MOC 导航） | **0/234**（MOC 导航） | **−58** |
| source_ids 机器对 | **299** | 299 | **478** | +179 |
| source_ids 有可见链接 | **2/299（0.7%）** | 193/299（64.5%） | **370/478（77.4%）** | **+368 对** |
| 被引用来源 / 其中可见 | **143 / 2** | 143 / 143 | **172 / 172** | +29 / +170 |
| typed 边（结构化字段） | **485** | 485 | **737** | +252 |
| typed 无可见 | **313（64.5%）** | 122（25.2%） | **123**（source_ids 108 + key_garments 15） | −190 |
| 卡片 `relations`（工具外） | — | — | **334**（high 262 / medium 72） | 308→334（P5-E +26） |
| 语义分量数 | **66** | 66 | **60** | **−6** |
| 最大分量 | **335**（189 content + 146 source） | 335 | **399**（224 content + 175 source） | **+64** |
| 单点分量 | **65**（全 source） | 65 | **59**（全 source） | **−6** |
| 9 本书源 | 仅研究文档，未接卡 | 同 | **5 connected / 4 背景**（SRC-0061/62/64/66/69） | 接入 5 本 |

## 2. 来源接入（单列，不与关系覆盖混算）

| 指标 | P5-A 前 | 当前 |
|---|---:|---:|
| source_ids 对 / 正文可见 | 299 / 2（0.7%） | **478 / 370（77.4%）** |
| 被引用来源 / 可见 | 143 / 2 | **172 / 172（100%）** |
| 零可见 SRC 卡 | 180/181（99.4%） | **39**（38 draft + GAR-0045 medium review） |
| 有≥1 不可见 source 的卡 | — | 40（含 GAR-0033 部分可见） |
| 来源隔离原因 | 58 零可见（56 零总度） | **59 singletons**（graph） + 172 linked visible / 62 navigation-only |
| MOC/导航来源可见 | 无 | **234/234 经 MOC**（仅导航，不计语义） |

## 3. 单点 / 孤立

- P5-A 前：65 个单点（28 isolated + 27 background + 9 nav-only 书源 + 1 book）；source_kind：vocabulary 19 / museum 12 / reference 9 / academic 8 / other 8 / image 5 / industry 3 / dataset 1。
- 当前：**59 singletons**（source kinds：vocabulary 18 / museum 12 / other 8 / academic 8 / image 5 / reference 4 / industry 3 / dataset 1）；`isolates.csv` 59 行；另有 3 个 uncited 未分类（SRC-0163/0157/0175）→ uncited 62。
- 来源原因：linked_visible_from_content **172**、navigation_only **62**（MOC）。
- P5-E 的 26 条新关系（20 uses_material + 6 may_have_part）**未新增 high**，不改变 semantic component 数（仍在已有主分量内）。

## 4. 未解决项（图工具）

- `typed_unresolved` **5**、`unresolved_wikilink` **1**（P5-E 前后均存在；未定位具体 ID）→ 需在 E5 对比前解释或归零，否则污染“typed 全解析”结论。
- `typed_edges` 不含卡片 `relations`：**737 结构化 vs 334 卡片 relations**，报告须分列，不可相加。
- 来源“零可见 0”来自 MOC 导航；语义接入仍以 **370/478（77.4%）** 衡量。

## 5. 结论

- 相比 P5-A 前：内容零链接保持 0；来源零可见 **58→0（导航）**；source_ids 可见 **2→370**；typed 无可见 **313→123**；分量 **66→60**、最大分量 **335→399**、单点 **65→59**；9 本书源由 0 接入 → 5 connected。
- 当前图谱的主要改进来自 P5-A 的 MOC/来源链接 + P5-C/P5-D 的卡片与书源接入；P5-E 只新增 26 条 medium design 关系，**不改变分量结构**。
- 依然存在：59 个来源单点、62 uncited（3 个未分类）、39 零可见 SRC 卡（38 draft + GAR-0045）、5 typed_unresolved +1 unresolved wikilink、4 本背景书未接卡。
