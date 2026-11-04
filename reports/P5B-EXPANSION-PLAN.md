# P5-B 扩建计划（关系优先、少量补卡、不硬连）

- 日期：2026-11-05（Asia/Shanghai）；执行：narrator（P5-B）
- 依据：`reports/P5B-RELATION-COVERAGE.md`、`11-验收/P5B/coverage-matrix.csv`、`11-验收/P5B/isolates.csv`
- 原则：**先补真实关系表达，再补少量卡**；不要求全类型覆盖；不为连通率硬连；**38 张 draft 不改状态**；只提交清单与高价值建议，本任务不实施补卡。
- 当前基线：189 内容卡 / 211 来源卡 / `validate.py` PASS 400/400；MOC 9 页导航独立。

## 0. 优先级总览

| 优先级 | 动作 | 工作量 | 预期效果 |
|---|---|---|---|
| **P0** | 连接 7 个 should-connect 来源；9 本书源决定表达方式；38 draft 人工复核 | 0 新卡；审核/文档 | 来源可见性 106 对 → 0（若人工确认）；证据不丢 |
| **P1** | 少量补 material/pattern（各 3–4 张，选现有 garment 需求最高的） | 6–8 新卡 | garment→material 40%→≥60%；pattern 3→7 |
| **P1** | 少量补 component（2–3 张，仅补被现有 garment 高频引用但缺卡的） | 2–3 新卡 | garment→component 18%→≥35%；garment_part→material 8%→≥30% |
| **P2** | 鞋履/配饰少量补 2–3 张；period 语境 2–3 张 | 4–6 新卡 | 鞋履/配饰薄；Macbeth/历史案例有语境支撑 |
| **P2** | LOOK narrative 10 套补齐（人工内容，不新卡）；区域/专题 MOC | 文档 | LOOK→narrative 57%→≥80%；独立专题可导航 |
| **P3** | future_topic 14 个来源归档/未来补卡；不现在做 |  backlog | 避免为孤立来源硬凑卡 |

**非目标**：不追求“每个类型全 100%”；不把 `may_have_part`/`ensemble_with` 升格为事实；不为了 65 个单点全部建关系；不自动提升 38 draft。

---

## 1. P0：不新增卡，先补真实关系/可见性

### 1.1 连接 7 个 should-connect 来源（已有卡，人工复核后补 `source_ids`/可见链接）

| 来源 | 目标卡（真实 ID） | 关系/动作 | 依据 |
|---|---|---|---|
| SRC-0028 Met 和服 ca.1910 | GAR-0001 和服 | 补 source_ids/可见 SRC 链接（实例，注意 `isPublicDomain=false`） | `reports/P5-SOURCE-RELATIONS.md` §3 #6 |
| SRC-0029 Met 马甲 1615–20 | GAR-0008 马甲 | 补 source_ids（17 世纪实例） | 同上 #3 |
| SRC-0030 Met 马甲 1780–1800 | GAR-0008 马甲 | 补 source_ids（18 世纪实例） | 同上 #4 |
| SRC-0037 V&A 风衣博客 | GAR-0045 风衣 | 补 source_ids（gabardine/防雨历史语境） | 同上 #1 |
| SRC-0041 V&A kantha 刺绣 | GAR-0063 纱丽 | **不自动迁移**；先转 REVIEW-QUEUE，建议建“刺绣/工艺”关系或卡后再挂 | 同上 #7（low） |
| SRC-0050 Cleveland 腰带 c.1375–1400 | GAR-0080 腰带 | 补 source_ids（实例） | 同上 #2 |
| SRC-0059 V&A 保持干燥简史 | GAR-0047 雨伞 | 补 source_ids（历史语境） | 同上 #5 |

- 验收：6 条 high/medium 进对应卡 `source_ids` 且可见；SRC-0041 保持 review；`validate.py` PASS；不修改正文事实。

### 1.2 9 本 P4 书源（SRC-0061..0069）——先决定“表不表达”，不硬连

- 当前只在研究笔记以 wikilink 出现，不在任何内容卡 `source_ids`；分类为 `evidence_missing_expression`（见 `isolates.csv`）。
- 可表达的候选（需人工确认书内定位；页码 UNCONFIRMED，用章/段/行）：
  - SRC-0066《男士服饰词典》→ `GAR-0008 马甲` / `GAR-0002 达布里特` / `GAR-0016 班扬袍`（词条定位见 `11-验收/P4-BOOKS/TERMS-GLOSSARY.md`）；
  - SRC-0067《足部之书》→ `GAR-0022 威灵顿靴` / `GAR-0035 女式皮鞋` / `GAR-0010 灯笼裤`（鞋/裤语境）；
  - SRC-0068《法国时装史》→ `PRD-0001 1770s 英法` / `PRD-0002 1790–1810 英法`（标 book_fact）；
  - SRC-0063《英国服装》→ `PRD-0003 1890s 英美`（标 book_fact）；
  - SRC-0069《服装漫谈》→ `GAR-0002` / `GAR-0016`（可支撑的历史术语）；
  - SRC-0061/0062/0064/0065 与现有卡对应弱：保留为背景/书籍 MOC，不强行挂卡。
- 验收：每一条只在“书内结论可定位 + 内容卡有对应断言”时补；否则保留 independent；不把 book_fact 写成 verified。

### 1.3 38 张 draft（只复核，不迁移）

- 38 = look 22 / scene 15 / style 1（`source_ids` 有、可见 SRC 链接无；对应 106 对）。
- 步骤：人工逐卡确认 `source_ids` 是否真实支撑 → 补可见 `[[SRC-...]]`/关系候选 → `validate.py`；**不自动改 `review_status`**；未确认的保持 draft。
- 验收：106 对中可确认的补链接；不可确认的记 review 原因；draft 数量不减少（除非人工签核）。

---

## 2. P1：少量补卡（6–11 张，按现有 garment 需求选）

> 不一次性扩卡；以下只在“现有 garment 已引用/高需求”时立项。新卡仍需真实来源（V&A/Met/FIT/PD 书）与 SRC；不编造 ID。

### 2.1 material（建议 3–4 张）

| 候选主题 | 为什么优先 | 现有需求依据 | 来源策略 |
|---|---|---|---|
| leather（皮革） | 鞋履/外套/腰带核心；现有 garment 多写 leather 但无材料卡 | outerwear 12、footwear 9、accessory 11 的 material 覆盖低（matrix） | V&A/Met 实物或 SRC-0061..0069 书源（book_fact + 实物交叉） |
| fur/毛皮 | 历史/寒冷场景；outerwear 12 中无材料卡 | outerwear material 5/12 | V&A/Met 实物；不得支持现代皮草伦理争议外推 |
| knit/针织物 | 1930s–70s 针织背心/毛衣语境 | GAR-0034 等针织卡 | V&A/FIT；结构卡（针法）可后续 |
| waterproof/finish（防水/涂层） | 风衣/雨衣/雨伞语境 | GAR-0045/0046/0047 | V&A/技术史；标 finish 非 fiber |

### 2.2 pattern（建议 3–4 张）

stripes（条纹）、check/plaid（格纹/苏格兰格——**不用于 11 世纪 Macbeth**）、print（印花）、embroidery（刺绣/kantha）。依据：pattern 仅 3 张；material/pattern→style 0%；现有 LOOK/garment 的纹样描述只能在正文出现。

### 2.3 component（建议 2–3 张，从高频缺口选）

| 候选 | 现状证据 | 触发条件 |
|---|---|---|
| lining/interfacing/padding（里布/衬/填充） | garment_part 26 中无；outerwear/suit 需要 | 有 ≥3 张现有 garment 正文提到里布/衬 |
| pleats（褶裥） | 结构卡有褶但无独立细化 | 有 ≥2 张 LOOK/garment 需要 |
| pocket/slit（口袋/开衩） | 结构卡有袋结构 1 张，无开衩 | 动作/历史案例需要 |

- 不补“仅为连通”的空泛部件；每张必须有来源 + 明确被现有卡引用。

---

## 3. P2：鞋履/配饰、历史语境、LOOK 叙事与专题导航

1. **鞋履/配饰（2–3 张）**：1930s–40s 女鞋、战后通勤包袋、当代调查者配件；依据 matrix 鞋履 9/配饰 11/头饰 7 偏薄与 P3.5/P4 案例。
2. **period_region（2–3 张）**：11 世纪苏格兰（Macbeth）、中世纪盛期、18 世纪法国宫廷；只补有案例需求的语境，不做年代百科；必须真实来源 + 语境级声明。
3. **LOOK→narrative（10 套）**：不新建卡；对 10/23 缺 `narrative_meaning` 的 LOOK 补叙事字段（人工），目标 ≥80%；不改变设计内容。
4. **区域/专题 MOC**：新增 `00-系统/MOC/区域专题.md` 或等价的只读导航页，列出拜占庭（PRD-0010、GAR-0009、MAT-0011）、莫卧儿/南亚（GAR-0071/0072、SRC-0450..0454）、日本（GAR-0001/0065、SRC-0100/0426）、奥斯曼（PRD-0009、GAR-0004）、非西方（GAR-0005/0006、MAT-0005/0006、GAR-0031/0032）等；页首写明“并列展示，不代表同源/可互换”。**纯导航，不加关系断言。**

---

## 4. P3：future_topic 来源（不现在补卡）

来自 `isolates.csv` 的 14 个 `future_topic`：SRC-0018/19/20（FIT 19c 裙）、SRC-0023–0027（Met 裙/束胸）、SRC-0031/0032（体操/运动服）、SRC-0038（Undressed 内衣史）、SRC-0039（羽毛帽）、SRC-0040（武士衬衫）、SRC-0060（防染印花）。
- 处理：进入 backlog，按未来案例需求再建卡；不把它们硬挂到现有卡上。
- 34 个 `legit_reference`（AAT/FIT 词典、CDG/Screen Ireland、学会、图像权）：保留独立参考/背景，MOC 标注用途即可。
- 1 个 `no_verifiable_relation`（SRC-0044 Museum at FIT 主页）：只作导航/背景。

---

## 5. 验收标准（建议）

| 动作 | 验收 |
|---|---|
| P0 7 来源连接 | 6 条补入真实卡；SRC-0041 留 review；validate PASS；无正文事实改动 |
| P0 书源 | 每条要么有 book_fact + 定位 + 内容卡断言，要么明确 independent；0 硬连 |
| P0 draft | 38 draft 状态不变；106 对逐条有“可确认/不可确认”结论 |
| P1 material/pattern | 新增 6–8 卡均有真实 SRC；garment→material ≥60%、pattern ≥7 张；不新增无来源卡 |
| P1 component | 新增 2–3 卡；garment→component ≥35%；garment_part→material ≥30% |
| P2 叙事/MOC | LOOK→narrative ≥80%；区域专题页无 broken；独立专题不为连通强行加关系 |
| 通用 | `validate.py` PASS；不自动改 draft/review_status；所有新关系有 SRC/ID 可追溯 |

## 6. 风险与不做的事

- 不用“补卡”掩盖关系缺口：P0 已可修复大部分来源表达问题。
- 不为非西方/独立专题造“同源”关系；只做并列导航。
- 不把 `context_includes`/`may_have_part`/`ensemble_with` 写成事实；不把 book_fact 写成 verified。
- 不在本任务实施任何补卡或卡片编辑；本文件仅为计划。
