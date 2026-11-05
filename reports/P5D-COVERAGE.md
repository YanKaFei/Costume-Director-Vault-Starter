# P5-D 前后覆盖矩阵（P5D-COVERAGE）

- 日期：2026-11-05（Asia/Shanghai）；执行：narrator（P5-D 独立复核）
- 快照：
  - **Before**：`5ae2c52`（P5-C 已提交）— **458 卡 = 224 内容 + 234 来源**，**265** 条卡片 relations
  - **After**：当前 P5-D 工作区 — 同样 **458 卡 = 224 内容 + 234 来源**，**314** 条卡片 relations（**+49**：30 条 design backfill + 19 条 book claim）
  - 相同分母：两期均为 224 内容卡（本任务只比较同一批卡，不因新增卡改分母）
- 数据文件：`11-验收/P5D/coverage-before-after.csv`（136 行 = 17 个 type/category 组 × 8 维；其中 51 行为 N/A）
- 性质：**只读复核**；未改卡片/脚本；**不提升 draft/verified**；未新增卡；GUI NOT_RUN（未开 Obsidian）。
- 校验（当前树）：`validate.py` PASS 458/458；`relation_consistency.py` 0 errors / 314 relations；`validate_outfits.py --all` 12 pass / 23 legacy / 0 fail。

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 关系数量 | 265 → **314（+49）**：19 条 book claim + 30 条 design（6 appears_in_look / 7 in_style / 6 look_scene / 4 may_have_part / 7 uses_material） |
| 覆盖矩阵 | **几乎不变**：garment material 37/92 → 39/92；garment claim 86/92 → 87/92；component/style/outfit/narrative 维持；关系数增加但**卡级维度覆盖没有同等增长** |
| P5-D 回填 | **30 条 design 关系已写入卡**；**239 条仍在 REVIEW-QUEUE**（未写卡）；另有 19 条 book claim 来自书籍证据协调 |
| 来源可见率（单列） | source_ids 对 460→479；正文可见 **352→371（76.5%→77.5%）**；唯一被引/可见来源 167→172；零可见卡 **39→39（不变，均为 draft/GAR-0045）** |
| Outfit 叙事 | LOOK→narrative **25/35（71.4%）**，与 P5-C 持平；P5-B 基线为 13/23（56.5%） |
| draft/verified | 未改变任何 draft/verified；全库 draft 仍为 79（38 基线 draft + 新增 LOOK/STY 等） |

**核心判断**：P5-D 把关系图从 265 增到 314，但**新增的 30 条 design 关系多数是 LOOK/SCN→target**，不落入 Garment→Component/Material/Style/Outfit 的卡级覆盖；19 条 book claim 只有 1 条使 garment→claim 新覆盖。因此“关系数增加 ≠ 覆盖矩阵提升”；真正的覆盖缺口仍在结构（component）、材料、风格、Outfit→narrative 的细分。

## 1. 口径与矩阵

- **Formal（正式）**：卡片 frontmatter `relations`、结构化字段（`source_ids`/`look_items`/`look_scene`/`key_garments`）、正文可见 `[[ID]]` 的并集。
- **Review（待审核）**：`11-验收/P5D/REVIEW-QUEUE.csv` 的 239 条 medium 设计/共现候选；**未写入卡片**，不计入正式覆盖。
- **N/A**：按类型设计不要求该关系（如 material→component；look→outfit 不作为 LOOK 的“被穿”方向；CSV 中 51 行 N/A）。
- **Source visibility**：**单独计算**（frontmatter `source_ids` 对 vs 正文 `[[SRC-…]]` 命中），不与关系覆盖相加。
- 维度：
  - Garment→Component（STR）、Material（MAT/PAT）、Silhouette（字段）、Style（STY/风格标签）、Footwear-Accessory（鞋/头饰/配饰/携带物）、Outfit（被 LOOK 引用）；
  - Outfit（LOOK）→Narrative（`narrative_meaning`）；
  - Claim→Source（内容→SRC）。
- 完整 136 行矩阵：`11-验收/P5D/coverage-before-after.csv`；每行含 `before_applicable/formal/review/uncovered`、`after_*`、`applicability` 与 note。

## 2. 矩阵摘要（同分母；After 为当前树）

| 维度（type） | Before 正式 | After 正式 | After review | 变化 |
|---|---:|---:|---:|---:|
| garment→component | 16/92（17.4%） | **16/92（17.4%）** | 0 | 持平 |
| garment→material | 37/92（40.2%） | **39/92（42.4%）** | 19 | +2（设计回填/Token 关系） |
| garment→silhouette | 92/92（100%） | 92/92（100%） | 0 | 持平（字段层） |
| garment→style | 2/92（2.2%） | **2/92（2.2%）** | 0 | 持平 |
| garment→footwear-accessory | 63/92（68.5%） | 63/92（68.5%） | 0 | 持平 |
| garment→outfit | 55/92（59.8%） | **55/92（59.8%）** | 0 | 持平 |
| look→narrative | 25/35（71.4%） | **25/35（71.4%）** | 0 | 持平 |
| garment→claim/source | 86/92（93.5%） | **87/92（94.6%）** | 0 | +1 |
| garment_part→material | 7/35（20.0%） | **7/35（20.0%）** | 3 | 持平 |
| garment_part→style | 0/35 | 0/35 | 0 | 无 |
| material/pattern→style | 0/16; 0/3 | 0/16; 0/3 | 0 | 无 |

- 聚合（全部类型 applicable）：component 16/92、material 44/127→46/127、style 62/208、accessory 63/92、outfit 55/92、narrative 25/35、claim 216/224→217/224。
- **Review 列**：矩阵可映射的 review 只有 material 22 条（其余 queue 行 subject 是 LOOK/SCN，不对应 Garment→维度；见 §4）。
- **N/A 数**：51 行；例如 material/pattern/scene 的 component 不适用，style 的 outfit 不适用——不是 0% 失败。

## 3. 关系增量拆分（265→314）

| 来源 | 数量 | 类型 | 是否落卡 |
|---|---:|---|---|
| design backfill（engineer） | **30** | appears_in_look 6 / in_style 7 / look_scene 6 / may_have_part 4 / uses_material 7 | 是（30 条写入 relations；见 §4 语义问题） |
| book claim（书籍证据协调） | **19** | claim_supported_by | 是（19 条写入） |
| 仍待审核 | **239** | appears_in_look 122 / uses_material 77 / in_style 39 / look_scene 22 / may_have_part 9 | 否（REVIEW-QUEUE） |

- 关系数 +49（+18.5%），但卡级维度 formal 覆盖仅 material +2、claim +1；**design 增量主要是 LOOK/SCN→target 的设计边**，不改变 Garment→Component/Style/Outfit 的卡级覆盖。
- 这**不是**失败：关系密度与覆盖矩阵是两套指标；但发布/宣称“覆盖提升”时不能用关系数代替矩阵。

## 4. 来源可见率（独立口径）

| 指标 | Before（5ae2c52） | After（当前） | 变化 |
|---|---:|---:|---:|
| content 卡 | 224 | 224 | 0 |
| frontmatter source_ids 对 | 460 | **479** | +19 |
| 正文可见 SRC 对（`[[SRC-…]]` 且属 source_ids） | 352（76.5%） | **371（77.5%）** | +19 |
| 唯一被引来源 | 167 | **172** | +5 |
| 唯一可见来源 | 167（100%） | **172（100%）** | +5 |
| 零可见 SRC 卡 | 39 | **39** | 0（38 draft + GAR-0045） |

- 19 条新增 book source_ids 同时带可见 `[[SRC-…]]`（book claim 关系），所以可见率不降；39 张零可见卡保持 draft 基线，未提升。
- 这组数字与 P5-C 报告的 460/352 一致；与 P5B 的 299/193 不可直接比较（分母不同）。

## 5. 仍缺的真正知识（只建议，不扩卡）

1. **结构（component）**：Garment→component 仅 16/92（17.4%）；outerwear/footwear/headwear 的 component 为 0；结构卡→材质仅 7/35、→风格 0/35。需要 **部件-服装/材料连接的方法**（不是硬连），优先 be-spoke 结构卡（里布/衬/袖窿/裤裆/开衩等）与现有 garment 的正文映射。
2. **材料**：garment→material 39/92（42.4%）；设计/Token 回填 19 条 review 尚未进卡；`style/material→style` 为 0，材料卡无法表达风格关联。
3. **风格**：garment→style 2/92（2.2%）；风格仍主要靠自由 tag，不是可检索关系；5 张新 STY 仅覆盖 P5-C 主题。
4. **Outfit 叙事**：25/35（71.4%），10 套 LOOK 仍无 `narrative_meaning`；新 LOOK（P5-C）叙事很好，但旧 LOOK 缺口仍在；Outfit→Narrative 不是靠 backfill 可自动补的，需人工内容。
5. **配饰/鞋履**：63/92（68.5%）；缺“配饰与服装的时代/角色兼容”关系；独立专题（拜占庭/莫卧儿/日本/奥斯曼/非西方）仍无区域 MOC/专题入口。
6. **来源**：39 张零可见卡（draft；不可自动提升）；239 条 queue；9 本书源已由 19 条 book claim 接入但仍为 book_fact，不得当 standalone verified。
7. **6 flags**（PRD-0004/0006/0007/0008/0011 key_garments）仍 review_queue；38 基线 draft 未变；这些是人工/owner 决策，不是覆盖率能解决的。

## 6. 结论与边界

- **Before/After 同分母矩阵**：关系 265→314，但 formal 维度仅 material +2、claim +1；其余持平。P5-D 的 30 条 design 回填增加了图谱边（尤其 LOOK/SCN 层），但**没有实质改善 garment 结构/风格覆盖**；19 条 book claim 增加了来源密度，1 条使 claim 覆盖新增。
- 未提升 draft/verified；未新增卡；未改脚本；未把 design/medium 当事实。GUI NOT_RUN。
- 建议以 `11-验收/P5D/coverage-before-after.csv` 作为后续 P5-E 的基线；不要用 314 关系数替代矩阵宣称覆盖提升。


---

## 9. 最终口径复核（task-86，2026-11-05 10:47）

- MISLINK 修复后最终 **308 relations**（不是本报告正文采样时的 314）：5 条 subject-type 错误 design 关系已移除 + GAR-0033 book claim（WEAK）移除；GAR-0079→SRC-0069 降 medium/interpretive。
- 最终覆盖（独立复算，同口径）：garment→material **39/92（42.4%）**、garment→claim **87/92（94.6%）**；component 16/92（17.4%）、style 2–3/92、outfit 55/92（59.8%）、narrative 25/35（71.4%）——与 §2 After 一致，不因移除 5 条 design 而下降（均非 garment 维度）。
- 来源可见（单列）：source_ids 对 **478**、可见 **370（77.4%）**；可见来源 **172/172**；零可见卡 39（38 draft + GAR-0045）。本报告正文的 479/371 含随后移除的 GAR-0033 book source；最终以 478/370 为准。
- 书籍：应用记录 18 卡/19 组，最终有效 **17 卡/18 book claims**（GAR-0033 移除）。
- 59 isolates（isolates.csv 更新后）；另有 3 个未分类 uncited 来源（SRC-0163/0157/0175）。


## 10. 最终口径（MISLINK 清理后）

- 最终 relations = **308**（正文 §1–§9 的 314 为清理前）；design pilot 30 条中 **25 条有效**（5 条主语错误已移除）；book claims 19 组中 **18 保留**（GAR-0033 WEAK 移除）。
- 最终 high 262 / medium 46；覆盖矩阵以 308 口径为准（material 39/92、claim 87/92、component 16/92、style 2–3%、outfit 55/92、narrative 25/35）。
- 来源可见 370/478（77.4%），可见来源 172/172；零可见卡 39（38 draft + GAR-0045）。
