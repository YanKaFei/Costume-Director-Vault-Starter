# P5-E E3 旧卡知识深化与定向关系补齐（P5E-KNOWLEDGE-EXPANSION）

- 日期：2026-11-05（Asia/Shanghai）；执行：narrator（P5-E E3）
- 输入：E1 `reports/P5E-RELATION-ELIGIBILITY.md` + `11-验收/P5E/eligibility.csv`（1792 行；291 reliable-source fix candidates、177 actionable）；E2 `reports/P5E-SOURCE-RESEARCH.md` + `11-验收/P5E/candidate-review.csv`（239 条候选，39 条 source_verifiable）
- 快照：Before P5-E `0e8d37d` — **458 卡 = 224 内容 + 234 来源**，**308 relations**；After 当前树 — **同样 458 卡**，**334 relations（+26）**
- 写入范围：01/02/03/05/09 的 28 张旧卡正文/relations；**未改 ID、既有事实、evidence_status、review_status**；**新增卡 0**；未改脚本/00-系统。
- 校验：`validate.py` **PASS 458/458，0 errors/0 warnings**；`relation_consistency.py` **cards=458 / relations=334 / errors=0**；新增关系 target 全部可见/可解析。
- 注：GUI NOT_RUN；本任务不提升 draft/verified。

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 试点旧卡 | **28 张**（20 张 material 深化 + 6 张 component 深化 + 2 张风格解释卡） |
| 新增 typed relations | **26 条**：`uses_material` 20（medium/interpretive，review）+ `may_have_part` 6（medium/interpretive，review） |
| 新增 visible links | 26 条 relation 的 target 均在正文有 `[[…]]`；材料卡另加 MAT 卡链接 |
| 新增卡 | **0**（无需新卡；E2 候选可落在既有卡） |
| 覆盖变化 | garment→material **39/92→53/92（42.4%→57.6%）**；garment_part→material **7/35→10/35（20%→28.6%）**；component/style/outfit/narrative/claim 持平；relations 308→334 |
| 来源可见率 | **478 对 / 370 可见（77.4%）**；本批未改 source_ids，可见率不变 |
| 证据等级 | 本批全部 medium/interpretive/review；**未新增 high**（无独立证据支持“材料/部件事实”）；无 keyword/相似度硬连 |

## 1. 选择与改动原则

- 从 E1 的 `fix_candidate=yes` / `APPLICABLE` / `INSUFFICIENT_EVIDENCE` 与 E2 的 `source_verifiable` 候选中选：
  - 20 张 garment/garment_part：`uses_material` 候选（真实 MAT target；materials token 明确）；
  - 6 张 garment：`may_have_part` 候选（正文已有 STR 链接；仅部件候选，不是 has_part）；
  - 2 张 style：只加“历史事实 vs 风格解释”说明，不伪造风格事实。
- 每张卡只加**已有字段/正文/来源可支撑**的内容：
  - 结构：部件卡的 `part_family` + 该 STR 卡来源；正文不声称实物必然包含；
  - 材料：卡内 `materials` token 与 MAT 卡材料族定义；不声称独立成分检测；
  - 风格：设计解释，明确不是史实；
  - 廓形：卡内 `silhouette` 字段记录，不做裁剪图推断。
- 不改既有段落/既有事实；只在 `## 结构要点` 追加 P5-E 注释与正文 Wikilink。

## 2. 逐卡改动（28 张）

| # | Card | type | 深化内容 | 新增 typed relation | source_ids |
|---|---|---|---|---|---|
| 1 | `GAR-0077` 紧身长袜 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0484,SRC-0485,SRC-0066 |
| 2 | `GAR-0078` 亚麻衬衣 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0486 |
| 3 | `GAR-0057` 1960 年代 Courrèges 外套 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0019`（medium/interpretive，review） | SRC-0417 |
| 4 | `GAR-0076` 斗篷与披风 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0482,SRC-0483 |
| 5 | `GAR-0022` 威灵顿靴 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0123 |
| 6 | `GAR-0023` 莫卡辛鞋 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0124 |
| 7 | `GAR-0024` 穆勒鞋 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0125 |
| 8 | `GAR-0058` 1970 年代厚底鞋 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0418 |
| 9 | `GAR-0060` 1930 年代男式皮鞋 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0420 |
| 10 | `GAR-0081` 皮靴 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0489 |
| 11 | `GAR-0084` 高跟鞋 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0524 |
| 12 | `GAR-0036` 护士制服 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0004`（medium/interpretive，review） | SRC-0400 |
| 13 | `GAR-0061` 科普特束腰长袍 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0421 |
| 14 | `GAR-0075` 束腰长袍 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0480,SRC-0481 |
| 15 | `GAR-0066` 和服腰带 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0003`（medium/interpretive，review） | SRC-0427 |
| 16 | `GAR-0067` 云肩 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0003`（medium/interpretive，review） | SRC-0428 |
| 17 | `GAR-0080` 腰带 | garment | 材料/工艺, 廓形 | uses_material → `MAT-0017`（medium/interpretive，review） | SRC-0487,SRC-0488 |
| 18 | `STR-0003` 拉夫领 | garment_part | 材料/工艺 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0133 |
| 19 | `STR-0005` 十六世纪羊腿袖 | garment_part | 材料/工艺 | uses_material → `MAT-0016`（medium/interpretive，review） | SRC-0135 |
| 20 | `STR-0006` 胸衣插片 | garment_part | 材料/工艺 | uses_material → `MAT-0003`（medium/interpretive，review） | SRC-0136,SRC-0064 |
| 21 | `GAR-0001` 和服 | garment | 结构/部件, 廓形 | may_have_part → `STR-0003`（medium/interpretive，review） | SRC-0133 |
| 22 | `GAR-0002` 达布里特 | garment | 结构/部件, 廓形 | may_have_part → `STR-0003`（medium/interpretive，review） | SRC-0133 |
| 23 | `GAR-0003` 杰金 | garment | 结构/部件, 廓形 | may_have_part → `STR-0006`（medium/interpretive，review） | SRC-0136 |
| 24 | `GAR-0008` 马甲 | garment | 结构/部件, 廓形 | may_have_part → `STR-0006`（medium/interpretive，review） | SRC-0136 |
| 25 | `GAR-0009` 达尔马提亚长袍 | garment | 结构/部件, 廓形 | may_have_part → `STR-0005`（medium/interpretive，review） | SRC-0135 |
| 26 | `GAR-0012` 衬裤 | garment | 结构/部件, 廓形 | may_have_part → `STR-0008`（medium/interpretive，review） | SRC-0138 |
| 27 | `STY-0001` 新古典主义着装风格 | style | 风格解释 | 无新增关系（仅正文解释） | — |
| 28 | `STY-0003` 爵士时代摩登风格 | style | 风格解释 | 无新增关系（仅正文解释） | — |

## 3. 覆盖变化（同分母 224 内容卡；Before `0e8d37d` / After 当前）

| 维度 | Before | After | 变化 |
|---|---:|---:|---:|
| garment→component | 16/92（17.4%） | **16/92（17.4%）** | 持平（6 条只把既有正文链接 formalize，未新增卡级覆盖） |
| garment→material | 39/92（42.4%） | **53/92（57.6%）** | **+14** |
| garment→style | 2/92（2.2%） | 2/92（2.2%） | 持平 |
| garment→footwear-accessory | 63/92（68.5%） | 63/92（68.5%） | 持平 |
| garment→outfit | 55/92（59.8%） | 55/92（59.8%） | 持平 |
| LOOK→narrative | 25/35（71.4%） | 25/35（71.4%） | 持平 |
| garment→claim/source | 87/92（94.6%） | 87/92（94.6%） | 持平 |
| garment_part→material | 7/35（20.0%） | **10/35（28.6%）** | **+3** |
| garment_part→style | 0/35 | 0/35 | 持平 |
| 全部 relations | **308** | **334** | **+26** |
| source_ids 可见率 | 478 / 370（77.4%） | 478 / 370（77.4%） | 持平（未改 source_ids） |

- **注意**：矩阵中的 material 覆盖包含本批 medium/review 关系；它们不是“材料事实”，是材料族候选；不能把覆盖数字当强证据。
- component 覆盖没有上升，因为 6 张卡此前已有正文 STR 链接（E1 标 REVIEW_REQUIRED/body-link-only）；本批只把“链接/候选”固化为 typed `may_have_part`（medium/review），不改 `has_part`。

## 4. 证据与诚实边界

| 改动类型 | 证据来源 | 等级 | 不得声称 |
|---|---|---|---|
| 20 条 `uses_material` | 卡内 `materials` token + 真实 MAT 卡材料族定义；target MAT 及其 SRC 能解析 | **medium/interpretive/review** | 该实物成分已独立检测/该服装一定由该材料制成 |
| 6 条 `may_have_part` | 正文已有 STR 链接 + 目标 STR 卡 `part_family`/来源 | **medium/interpretive/review** | `has_part`（永久结构关系）/该实物必然包含该部件 |
| 2 张风格解释 | 既有 STY 卡内容；风格=设计解释 | **design-only** | 风格标签是年代/地域史实 |
| 廓形 26 张 | 卡内 `silhouette` 字段 | 字段记录 | 裁剪图/实物测量 |

- 本批**没有新增 high**：E2 候选均为 medium/review 或 design-only；若强行 high 会违反“evidence+visible”与不伪造事实原则。既有 high claim/关系未改。
- 没有使用关键词/相似度生成历史事实；`uses_material` 只用 materials token 的唯一映射，`may_have_part` 只用正文已有链接。

## 5. 批次校验

- `python3 scripts/validate.py` → **PASS 458/458，0 errors，0 warnings**。
- `python3 scripts/relation_consistency.py` → **cards=458 / relations=334 / errors=0 / moc_skipped=9**。
- 26 条新增 relation：target 全部存在，正文可见链接全部存在；无 duplicate，无 keyword-only 高危点。
- 28 张卡 ID/evidence_status/review_status 与 Before 快照逐项比较 **0 变化**。
- 本批未新建卡；新增 relation 全为 medium/review；未提升 draft/verified。

## 6. 仍缺证据/下一步

1. **material canonical 化**：20 条 uses_material 是 token→MAT 族；需要 canonical material ID/映射后才能升级，不应直接 high。
2. **component 真实结构证据**：6 条 may_have_part 依赖正文链接；缺 `part_ids`/裁片字段，不能升 has_part。需要结构卡与服装卡之间的可核验结构证据（书/实物/版型）。
3. **style**：2 张旧 STY 仅补“设计解释”说明；garment→style 仍 2/92；需要来源支持的风格判断（不是自由 tag）。
4. **材料/工艺深度**：皮革/毛皮/针织/防水/纹样卡仍薄；本批只做既有材料的族级关系，不新增卡。
5. **Outfit/narrative**：本批未动 LOOK 叙事；25/35（71.4%）仍是缺口。
6. **独立专题/区域**：本次未动；仍缺区域 MOC/专题，不应硬连。
7. **来源**：39 张零可见 SRC 卡、59 isolates、38 baseline draft、6 flags 仍按原状态保留；未自动提升。

## 7. 结论

- 28 张旧卡完成有来源/有字段依据的深化：20 条材料候选、6 条部件候选、2 张风格解释；relation 308→334；garment material 42.4%→57.6%、garment_part material 20%→28.6%；component/style/outfit/narrative/claim 持平。
- 本批**没有用风格想象替代史实，没有伪造 high，没有新建卡**；所有新增关系为 medium/review，可见链接已同步。
- 仍缺的知识是**结构证据（component）、canonical 材料、来源支持的风格、Outfit narrative、区域专题**；下一步应扩来源/结构证据而不是继续堆 medium 边。
