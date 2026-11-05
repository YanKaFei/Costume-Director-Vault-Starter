# P5-E E1 关系适用性审计与适用性分母覆盖率

- 任务：task-88（P5-E E1）；日期 2026-11-05（Asia/Shanghai）
- 快照：当前工作区 **458 卡 = 224 内容 + 234 来源**；308 条 cards relations
- 输入：224 内容卡、308 relations、source_ids、structured fields、正文 `[[...]]`、P5-D 覆盖基线
- 输出：`11-验收/P5E/eligibility.csv`（**1792 行 = 224 卡 × 8 关系维度**）+ 本报告
- 性质：**只读审计**；未改任何卡片/事实/关系/状态；未通过不真实链接提高指标
- 校验：`validate.py` PASS 458/458（0 errors/0 warnings）；`relation_consistency.py` cards=458 relations=308 **errors=0**

## 0. 结论摘要

| 项 | 数值 |
|---|---:|
| 总审计单元 | **1792**（224 卡 × 8 维） |
| APPLICABLE | **380** |
| INSUFFICIENT_EVIDENCE | **315** |
| REVIEW_REQUIRED | **80** |
| NOT_APPLICABLE | **1017** |
| 适用（非 N/A）单元 | **775** |
| 有可靠来源但缺关系（fix 行） | **291**（其中 177 有可执行方向；114 需人工目标） |
| 其中带真实候选目标（材料卡） | **38** 行（候选 MAT 卡见表；不是已建关系） |

**核心结论**：把分母改为“适用性分母”后，**只有 garment→footwear/accessory 明显变化**（legacy 31/92=33.7% → eligibility 31/56=55.4%，因为 36 张配饰/鞋履/头饰/携带物卡作为 target class 被排除）；component/material/style/outfit/narrative/claim 的适用分母与 legacy 基本相同（92/92/92/92/35/224）。因此覆盖缺口不是“分母被非适用卡稀释”，而是**真实关系/证据缺失**：component 17.4%、style 3.3%、footwear 55.4%、material 42.4%、outfit 59.8%、narrative 71.4%、claim 96.9%。

## 1. 方法/状态定义

- 8 个维度：Garment→Component（STR）、Garment→Material（MAT/PAT）、Garment→Silhouette（字段）、Garment→Style（STY）、Garment→Footwear/Accessory（配饰/鞋/头饰/携带物）、Garment→Outfit（被 LOOK 引用）、Outfit（LOOK）→Narrative（`narrative_meaning`）、Claim→Source（内容→SRC）。
- **Applicability**：前 6 维仅 `type=garment`；Outfit→Narrative 仅 `type=look`；Claim→Source 对所有内容卡。Garment→Footwear/Accessory 对 category ∈ {accessory,footwear,headwear,carried_prop} 的**主体卡** N/A（它们是该关系的 target class，不是 subject）；其余 garment 适用。
- **状态**：
  - `APPLICABLE`：适用且存在可用的结构化/类型化证据（formal relation 非 low、字段或结构化 membership）；
  - `REVIEW_REQUIRED`：适用且有 formal relation 但为 medium/design-only，或仅有正文 visible link、无类型化关系；需人工 review；
  - `INSUFFICIENT_EVIDENCE`：适用但无 formal relation/结构化字段/可见目标链接；
  - `NOT_APPLICABLE`：type/方向/目标类别不适用。
- **Formal 口径**：relations + structured fields（`silhouette`/`look_items`/`narrative_meaning`/`source_ids`）+ 正文可见 `[[target]]` 的并集；**仅 visible link 而无 typed relation 不升为 APPLICABLE**（标 REVIEW_REQUIRED）。
- `existing_fields` 记录实际字段/关系/链接；`source_ids` 列全部真实来源；fix 候选不是已建关系，禁止强连。

## 2. 各关系适用性/证据状态（CSV 聚合）

| relation | subject cards | N/A | applicable | APPLICABLE | REVIEW_REQUIRED | INSUFFICIENT | 关系存在（present） |
|---|---:|---:|---:|---:|---:|---:|---:|
| Garment→Component | 92 | 132* | 92 | 0 | 16 | 76 | 16 |
| Garment→Material | 92 | 132* | 92 | 9 | 30 | 53 | 39 |
| Garment→Silhouette | 92 | 132* | 92 | 74 | 0 | 18 | 74 |
| Garment→Style | 92 | 132* | 92 | 0 | 3 | 89 | 3 |
| Garment→Footwear/Accessory | 92 | 168* | 56 | 0 | 31 | 25 | 31 |
| Garment→Outfit | 92 | 132* | 92 | 55 | 0 | 37 | 55 |
| Outfit→Narrative | 35 | 189* | 35 | 25 | 0 | 10 | 25 |
| Claim→Source | 224 | 0 | 224 | 217 | 0 | 7 | 217 |
| **合计** | — | **1017** | **775** | **380** | **80** | **315** | **460** |

\* N/A 包含：非 subject 类型（material/pattern/look/scene/style/period_region 等）的 garment 维度 N/A；look 以外的 narrative N/A；以及 accessory/footwear/headwear/carried_prop 主体卡在 Garment→Footwear/Accessory 的 N/A。各行 subject cards 的总行数按 8 维展开，所以 N/A 是跨类型行数，不是“卡片缺失”。

- Garment→Component：16 条均为**正文可见链接**（formal relation 0）→ REVIEW_REQUIRED；`APPLICABLE` 0。不是“16 个强关系”。
- Garment→Material：9 条 formal high/可用；30 条 medium/可见链接 review；53 条不足。
- Garment→Silhouette：74 条字段已填且非 unknown；18 条 `silhouette=unknown` 不足。
- Garment→Style：仅 3 条可见 STY 链接 review，0 条强；89 条不足。
- Garment→Footwear/Accessory：31 条可见链接 review；25 条不足；因 36 张配饰/鞋履/头饰/携带物主体卡被标 N/A，applicable 仅 56。
- Outfit→Narrative：25/35 有 `narrative_meaning`；10 条缺。
- Claim→Source：217/224 有 source_ids；7 条无来源（GAR-0041..0044、GAR/LOOK/STY-EXAMPLE-001）。

## 3. 覆盖率：legacy 分母 vs 适用性分母

- `legacy coverage = relation_present / subject_cards`（沿用旧的全部 subject 分母；不含 N/A 区分）
- `eligibility coverage = relation_present / applicable`（排除 N/A；按本审计）
- `strong coverage = APPLICABLE / applicable`（仅强/可用，不含 review）

| relation | legacy | eligibility | strong | 说明 |
|---|---:|---:|---:|---|
| Garment→Component | 17.4% | 17.4% | 0.0% | 分母相同；16 条仅 visible link，均 review |
| Garment→Material | 42.4% | 42.4% | 9.8% | 39 存在，9 条 strong；30 条 review |
| Garment→Silhouette | 80.4% | 80.4% | 80.4% | 18 unknown 未计 |
| Garment→Style | 3.3% | 3.3% | 0.0% | 3 条仅 link review；0 strong |
| Garment→Footwear/Accessory | **33.7%** | **55.4%** | 0.0% | **仅此项因 N/A 分母明显变化**（31/56 vs 31/92） |
| Garment→Outfit | 59.8% | 59.8% | 59.8% | 结构化 look_items membership |
| Outfit→Narrative | 71.4% | 71.4% | 71.4% | 25/35 |
| Claim→Source | 96.9% | 96.9% | 96.9% | 217/224 |

**解读**：
1. 适用性分母并未大幅“美化”整体覆盖；除 footwear/accessory（因 target class 排除）外，其他维度分母与旧口径几乎相同。
2. Component/style/material 的缺口是**真实关系缺失/弱关系**，不是分母问题；不能用改分母宣称提升。
3. `strong coverage` 与 `eligibility coverage` 必须分开报告：前者仅 380/775 适用单元；后者含 review/visible link，不应当强证据。

## 4. 有可靠来源但缺关系的定向修复清单

**291 行**（`status=INSUFFICIENT_EVIDENCE` 且 `source_ids` 全部为真实 verified 来源）；按关系：
component 71 / material 49 / silhouette 18 / style 85 / footwear-accessory 24 / outfit 35 / narrative 9。
- `fix_candidate=yes`：177 行（有明确方向/可继续人工建关系；不自动建）；
- `fix_candidate=review`：114 行（需人工目标判断，尤其 silhouette unknown、style 自由 tag、component 无结构目标）。

真实候选目标仅在材料维度给出 **38 行**（真实 MAT 卡，候选非已建关系；排除 MAT-0012/0013 物性卡与 dye 卡）：
| card | source_ids | 候选 MAT（不强制） |
|---|---|---|
| GAR-0008 | SRC-0109;SRC-0066 | MAT-0001 / MAT-0002 / MAT-0003 / MAT-0011 / MAT-0014 / MAT-0015 / MAT-0018 |
| GAR-0011 | SRC-0112;SRC-0066 | MAT-0015 |
| GAR-0014 | SRC-0115 | MAT-0001 / MAT-0003 |
| GAR-0022 | SRC-0123 | MAT-0017 / MAT-0019 |
| GAR-0036 | SRC-0400 | MAT-0004 |
| GAR-0075 | SRC-0480;SRC-0481 | MAT-0001 / MAT-0003 / MAT-0015 / MAT-0016 |

其他维度示例（无真实目标卡时留 human，不硬连）：
- component：GAR-0004（SRC-0105）、GAR-0005（SRC-0106）、GAR-0006（SRC-0107）— 无 STR 关系/链接；需人工确认实际部件。
- style：GAR-0001（SRC-0100；`style_tags=japanese_traditional`）、GAR-0002（SRC-0103；renaissance/elizabethan）— 自由 tag 不等于 STY 关系，需人工映射。
- silhouette：GAR-0047/0048/0049（SRC-0407/0408/0409）— `silhouette=unknown`，需结构/图像证据，不能猜。
- footwear-accessory：GAR-0001/0002/0003（SRC-0100/0103/0104）— 无配饰关系/链接，需人工搭配证据。
- outfit：GAR-0001/0006/0008（SRC-0100/0107/0109）— 未被任何 LOOK `look_items` 引用；无法为覆盖率强塞 LOOK。
- narrative：LOOK-0001/0002/0003（SRC-0150/0152;SRC-0169/0101;SRC-0103）— `narrative_meaning` 缺失，需人工叙事内容。
- claim→source 7 条不足：GAR-0041/0042/0043/0044（interpretive，无 source）、GAR/LOOK/STY-EXAMPLE-001（example，无 source）；不应为指标补假来源。

**约束**：这些是候选/人工方向，不是已建关系；不得把候选 MAT/STR/LOOK 直接写成事实，不得为覆盖率制造链接。

## 5. 审计使用的字段/来源

- CSV `existing_fields` 列出实际 `relations=N; body_links=N`、`materials=[...]`、`silhouette=...`、`style_tags=[...]`、`look_items_membership=...`、`narrative_meaning=present/missing`、`source_ids`。
- CSV `source_ids` 全部为卡片真实 source_ids；fix 行要求全部 source 卡 `verified`（无编造来源）。
- N/A 不是失败：按关系类型设计，如 material/pattern→component、look→narrative 以外的类型、配饰类卡作为 garment→footwear/accessory 的 target 而非 subject。

## 6. 结论与边界

1. **覆盖缺口是真实的**：component 17.4%、style 3.3%、material 42.4%、outfit 59.8%、narrative 71.4%（strong 口径）；改动分母只在 footwear/accessory 上产生明显变化（33.7%→55.4%）。
2. **Review/visible link 不等同强关系**：component 16 条、style 3 条、footwear 31 条都只是 visible link/review，不计入 APPLICABLE。
3. 修复清单 291 行，材料 38 行给出真实 MAT 候选；其余留人工，不硬连。
4. 未改卡片/来源/脚本/关系；`validate.py` PASS 458/458，`relation_consistency` 0 errors/308 relations；本报告不声称 GUI/渲染/历史事实验收。
