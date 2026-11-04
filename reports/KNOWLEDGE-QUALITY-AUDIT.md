# R1 审计三：知识质量、来源定位与许可状态（KNOWLEDGE-QUALITY-AUDIT）

- 生成：2026-11-04 17:30（Asia/Shanghai）；worker：researcher（task-48，R1 审计三）
- 快照：**399 卡 = 内容 188 + 来源 211**；v1.2 可选字段 42 个；git HEAD `56f4225`（审计期间只读，未改卡片）
- 范围：`01-服装单品`、`02-结构细节`、`03-材质纹样`、`04-来源`、`05-风格体系`、`06-时代地域`、`07-剧情场景`、`09-造型组合`，以及 `reports/DRAFT-REVIEW.csv`、`11-验收/` 输出、`06-时代地域/书籍研究/`（P4 书籍结论）。
- 只读声明：本审计**不修改任何卡片**；新增的只有 `scripts/audit_knowledge.py` 与本报告。
- 工具：`scripts/audit_knowledge.py`（Python 标准库；8 个检查域；`--json` 输出机读结果；不写 Vault）。

## 0. 结论摘要

| # | 检查域 | 结果 | 计数 | 最严重 |
|---|---|---|---|---|
| 1 | 同名/重复/冲突卡片 | **FAIL（1 对真重复，2 对范围重叠，6 个别名冲突）** | 重复 ID 0；同名 0；别名冲突 6；近重复 5 | P1 |
| 2 | 书籍引用定位（≥8 抽检） | **PASS** | 31/31 条可回原文（27 自动 + 4 人工）；页码 UNCONFIRMED 100% | — |
| 3 | 年代/地域/文化错配 | **PASS（定向抽检）/ WARN（字段粒度）** | 定向 7 组 0 违规；字段粒度 30 条（多为对比/否定语境与宏观区域） | P2 |
| 4 | v1.2 属性 / wikilink / source_ids | **PASS** | 42 字段 0 违规；链接 399/399；source_ids 100% 可解析；verified 无来源 0 | — |
| 5 | 事实/证据/推断三分 | **WARN** | 卡片 0 实质违规；45 份测试输出中 41 份缺显式「假设/unknown」标记；P4 JSON 14/14 合规 | P1 |
| 6 | 62 张 draft 与 DRAFT-REVIEW | **PASS（可追溯）；H4 待人工** | 62/62 有记录；0 缺失；0 漂移；仍 draft 62；reviewed 0 | P1（流程） |
| 7 | 许可错标 / 0 图片策略 | **WARN** | 3 张来源卡许可字段粒度歧义；内嵌图片 **0**，本地图片文件 **0** | P1 |
| 8 | 三项独立状态字段提案 | 已提出并试评 | data_status：内容 188/188 stated；content_verified：141/43/4；license_verified：208 verified / 3 partial / 188 n/a | — |

- **P0：0**
- **P1：4**（KQ-01 手袋重复卡；KQ-05 许可字段粒度；KQ-06 输出缺「假设」标记；KQ-13 H4 人工签核未完成）
- **P2：5**；**P3：4**；**PASS/CLOSED：8**

## 1. 审计方法与复现

```bash
python3 scripts/audit_knowledge.py                  # 人读摘要
python3 scripts/audit_knowledge.py --json > /tmp/audit.json   # 机读结果（不写 Vault）
python3 scripts/audit_knowledge.py --section locators # 单域：书籍定位
```

- 卡片解析：扁平 YAML 子集解析器（不依赖 PyYAML），按 `01-09` 目录递归加载；重复 ID、同名、别名、近重复（token Jaccard）、已知重复 URL 组。
- 书籍定位：从 `06-时代地域/书籍研究/书籍研究-历史服饰术语与结构.md` 解析 31 条结论，用 PG 全文重建 body/chapter/paragraph，要求「行号在正文内 + 段号一致 + 章/词条一致 + 关键词/引文命中」；文本缓存必须含 PG START/END 标记（防止截断下载造成假失败）。
- 许可：对来源卡的 `license_status` 与 `rights_statement` 做启发式冲突检查；0-图片策略扫描 `![...](...)` 与 Vault 内图片文件。
- 说明：正则启发式可能误报；下文每条给出证据与人工复核结论。

## 2. 发现（按严重度）

### KQ-01（P1，OPEN）真实重复卡：GAR-0048「手提包」 vs GAR-0087「手袋结构」

- 证据：两卡 `type=garment`、`category=carried_prop`、`subcategory=bag`、`periods=[1930s]`、`source_ids=[SRC-0408]` 完全相同；`name_en` 分别为 handbag / handbag construction；别名同为 handbag/purse/手袋，GAR-0087 额外含「手提包」。两卡均 `evidence_status=verified`、`review_status=reviewed`。
- 影响：检索/推荐同一物件会命中两张卡，计数虚增；「结构」卡实际未按 `garment_part`（结构）建卡，与 v1.2「结构卡用 STR/部件字段」的设计不一致。
- 复现：`grep -rl '^id: GAR-0048$' 01-服装单品` 与 `GAR-0087`；或 `python3 scripts/audit_knowledge.py --section dups`（near_dups 显示同名率 0.71）。
- 修复建议：保留 GAR-0048 作物件卡；把 GAR-0087 改为结构卡（`type: garment_part`，`category: construction`，正文拆解提手/袋身/闭合），或合并入 GAR-0048 并在索引注销一 ID。
- 验收：`audit_knowledge.py` 不再报该近重复；`query.py 手袋` 只返回 1 张物件卡 + 1 张结构卡且二者互链；`validate.py` PASS。

### KQ-02（P2，OPEN）范围重叠：GAR-0061「科普特束腰长袍」 vs GAR-0075「束腰长袍 tunic」

- 证据：同 `category/subcategory=one_piece/tunic`；periods 部分重叠（late_antiquity / early_middle_ages）；来源不同（SRC-0421 vs SRC-0480+0481）；别名同时含 tunic/束腰长袍。
- 影响：「tunic」通用卡与具体馆藏卡并存，推荐时可能双计；词汇检索无区分。
- 修复：GAR-0075 改名「束腰长袍（通称）/ tunic (generic)」并在正文写明与 GAR-0061 的分工；两卡互加「相关卡片」并说明一个是通称、一个是科普特实例。
- 验收：alias 冲突消失（或保留但加 scope note）；两卡互链；查询 tunic 返回 2 卡且首段说明区别。

### KQ-03（P2，OPEN）别名冲突 6 组（除 KQ-01/02 外 4 组）

| alias | 卡片 | 判定 | 建议 |
|---|---|---|---|
| `着物` / `kimono` | GAR-0001 和服 / GAR-0065 出口和服 | **可区分但需限定**：命名与来源不同（19c 和服 vs 1910s-30s 出口和服），语义时段重叠 | GAR-0065 别名改为 `export kimono`、`輸出着物`；正文加与 GAR-0001 的区分 |
| `handbag` / `purse` / `手袋` / `手提包` | GAR-0048 / GAR-0087 | **真重复** | 见 KQ-01 |
| `长袍` | GAR-0004 卡夫坦 / GAR-0032 长衫 | 不同物件、通用别名过宽 | 分别改为 `caftan/kaftan`、`changshan`，移除泛用「长袍」或加限定 |
| `tunic` | GAR-0061 / GAR-0075 | 范围重叠 | 见 KQ-02 |
| `腰带` | GAR-0066 和服腰带 obi / GAR-0080 腰带 belt | 不同层级（obi vs belt），可区分 | GAR-0066 保留 `obi/和服带`，移除泛用「腰带」；两卡互链 |
| `seam allowance` | STR-0021 接缝与省道 / STR-0025 松量与版型 | **别名错配**：`seam allowance` 属接缝/缝份，不属松量 | 从 STR-0025 移除 `seam allowance`，改 `wearing ease/ease allowance` |

- 验收：同 type 内 alias 唯一（或冲突 alias 均带 scope 限定）；`audit_knowledge.py --section dups` alias_collisions 降为 0/带说明白名单。

### KQ-04（P2，OPEN）来源重复 URL 3 组（登记层重复，卡内已有 canonical 说明）

- 证据：`build_sources.py` WARN：
  - `fashionhistory.fitnyc.edu/1950-1959` → SRC-0115 / SRC-0157；
  - `.../late-byzantine-silk-damask-dress` → SRC-0022 / SRC-0163；
  - `.../Booklet_5_-_Costume_Department_2024.pdf` → SRC-0036 / SRC-0175。
  后两组在重复卡正文有「canonical 以 SRC-00xx 登记，本卡保留作重复交叉引用」说明；SRC-0157 亦有 canonical 说明。
- 影响：`reports/SOURCES.csv` 保留两行同 URL，外部发布/统计会重复计数；build_sources 只是 WARN 不阻断。
- 修复（不改卡前提下）：在 `SOURCES.csv` 生成时排除 `duplicate_of` 标记卡（需在卡片/生成器加一个可选 `duplicate_of` 字段，属 v1.2 之后的小扩展）；或 QA 手工维护 canonical 白名单。
- 验收：`build_sources.py` 0 duplicate-URL WARN；`SOURCES.csv` 唯一 URL；被排除卡仍可在 04-来源/ 被 wikilink 引用。

### KQ-05（P1，OPEN）许可字段粒度歧义 3 张来源卡（非「错标」，是单字段无法同时表达内容与图像权利）

- 证据：
  - SRC-0001 / SRC-0002：`license_status=cc_by`（Fashionpedia 注释/本体 CC BY 4.0，已核验），但 `rights_statement` 同时声明「数据集内图像版权归原始图库，不得复制」；
  - SRC-0417：`license_status=link_only`，`rights_statement` 写「文字 CC BY-NC-SA 4.0，图片除外；仅链接引用与转述」。
- 影响：单字段读者会误读：cc_by 卡看似整体可复用（图像不可），link_only 卡看似无开放许可（文字实为 CC BY-NC-SA）。对外许可声明有风险。
- 修复建议：把 `license_status` 拆为 `content_license_status`（文字/数据）与 `image_license_status`（图像，默认 link_only），或在 rights_statement 使用固定句式：「内容许可 X；图像许可 Y；本项目仅链接」。NC 许可需新增枚举或 `other_permission` + note。
- 验收：无「同一字段两种权利」歧义；抽查 20 张来源卡，内容/图像许可各自可读；`audit_knowledge.py --section license` 冲突项为 0（或全部带说明白名单）。

### KQ-06（P1，CLOSED-R1.1）推荐/测试输出缺少显式「已知 vs 假设」分离

> **R1.1 状态更新（2026-11-05，task-56）**：KQ-06 已修复。实际修复点在 **`scripts/run_acceptance.py` 的结果生成器**（`render_result()` 新增「已知输入 / 假设 / unknown / 风险 / 证据」五节，并把 reasons 归到「证据」）——不只 recommend/workflow；已用生成器全量重建 45 份 `T*.md`（未手改）。复跑：45/45 文件含五节、PASS 45/45；`audit_knowledge.py --section sep` 的 `missing assumption` 由 41 降为 **0**。证据见 `reports/R1.1-KNOWLEDGE-REPO.md` §1。状态：**CLOSED（R1.1）**。

- 证据：45 份 `11-验收/测试结果/T*.md` 中 **41 份**没有「假设/unknown/假定」标记（有「实际输入」「风险与证据」「来源链接」）；`11-验收/P4-MACBETH/outputs/*.json` 14/14 含 `input`/`evidence{source_ids}`/`risks`/`warnings`，分离良好。
- 影响：TASK-001 §7 要求「角色与剧情理解（区分已知/假设）」；当前 md 输出把输入当已知，未显式列出 assumed/unknown，人工复核与跨场次复用可能把假设当事实。
- 修复建议：`scripts/recommend.py`/`workflow.py` 的 md 输出模板增加「已知条件 / 假设与 unknown / 证据与推断」三段；JSON 已有字段可直接渲染。
- 验收：45/45 T*.md 含上述三段（或至少 `假设`+`unknown` 标记）；P2/P4 回归不降级；抽检 3 例人工确认分离语义正确。

### KQ-07（P2，OPEN）P4-MACBETH 的 period/region 粒度不足（非错标，但导致 era-level 推荐）

- 证据：`11-验收/P4-MACBETH/outputs/complex_historical.json` 输入 `period=medieval, region=europe`；输出 warnings 明示「no reliable period/region context card…」「period evidence is approximate/none for GAR-0003, GAR-0028, GAR-0033（requested medieval）；treat these as era-level hypotheses」，并提示 `items without source_ids: GAR-0079`。
- 影响：麦克白 11 世纪苏格兰语境无专门 PRD 卡，推荐只能到「medieval/europe」层级；好在编排器已诚实标注，不构成错标。
- 修复：新增/扩充 11 世纪苏格兰（或 medieval Scotland）语境卡，或在输入 schema 用 `period=11th_century, region=scotland`；让 composer 的 period_evidence 从 none/unknown 提升。
- 验收：Macbeth 三例 warnings 减少；period_evidence 至少 one_piece/footwear 为 `era` 以上；11/11 测试仍 PASS。

### KQ-08（P2，WARN）年代/地域字段粒度与检出一致性（30 条启发式，需人工分级）

- 证据：`audit_knowledge.py --section periods` 报 30 条：region_dominant_other 6、region_words_absent 9、body_decades_not_in_periods 15。人工抽读后：
  - 15 条 decade 差异**多为对比/否定语境**（不适用条件里的「1830s 后的大袖」「1950s New Look」），非错标；
  - 9 条 region 差异多为**宏观区域**（`east_asia`/`europe`）与正文具体国家（China）不匹配，字段可接受但粗；
  - 6 条 dominant_other 中，GAR-0076/78/79/80 的「scotland」来自 `SRC-0482/0483/0486/0487/0488` 的正文出处描述，非卡片地域错标。
- 影响：真实错配率低，但**用宏观区域替代证据地域**会让「年代/地域」检索不精确（如 zipper 卡 regions=europe/north_america 却只引中国旗袍）。
- 修复：对 9 条 region 差异逐条在正文加「证据地域」说明或把 `regions` 扩为 `[europe, east_asia, china]`；对 15 条 decade 差异在正文标明是反例/对比（不改字段）。
- 验收：`audit --section periods` 剩余项均带「反例/对比」或「宏观区域」人工白名单；抽检 10 条 region 与正文一致。

### KQ-09（P3，WARN）5 张 interpretive 卡无 `source_ids`（允许，但不可追溯）

- 证据：GAR-0041 医生白袍、GAR-0042 警察制服、GAR-0043 厨师服、GAR-0044 医疗工作鞋、GAR-0079 基尔特长袍：`evidence_status=interpretive`，`source_ids=[]`。
- 影响：符合证据规则（interpretive 不需来源），但 `content_verified` 只能记 design_inference；若被推荐引用，来源链断。
- 修复：能补来源则补（V&A/Met 职业服、kirtle 研究）；不能补则在正文明确「无外部来源，设计推断」并加 `design_inference` 标签。
- 验收：5 卡正文含显式推断声明；推荐输出对无来源卡给出 warning（composer 已有 `items without source_ids` 机制，抽查 1 例）。

### KQ-10（P3，WARN）别名/近重复启发式的假阳性（无需修复，记录以免误报）

- 证据：`near_dups` 5 组均为**不同物件**：SRC-0012 shoes vs SRC-0055 boots（AAT 不同词条）；SRC-0023/0024/0025/0029/0030 为不同 Met 藏品（年代/材质不同）。
- 判定：不构成重复；建议 QA 把「同 category 不同年代/不同馆藏号」加入白名单，避免下一轮重复排查。
- 验收：审计报告注明白名单；后续 rerun 计数解释一致。

### KQ-11（PASS，CLOSED）书籍引用定位 31/31 可回原文

- 证据：`06-时代地域/书籍研究/书籍研究-历史服饰术语与结构.md` 31 条结论全部回到 PG 全文：
  - 27 条自动校验 PASS（行号/段号/章或词典词条一致 + 关键词或引文命中）；
  - 4 条无 ASCII 检索词（C18 PG46949:2651、C19 PG46949:5699、C24 PG34903:1402、C28 PG56978:1190），人工回读原文逐条核对一致，例如 C18 原文 `A broad-leafed Flemish beaver hat, with a rich hatband and plume of feathers…`、C24 原文 `Before the 16th century… applied ornamental bands at the neck, waist, and borders of skirt and cloak`；
  - 页码：31/31 标 `UNCONFIRMED`（纯文本无页码）；无编造页码。
- 影响：P4 书籍结论可复核；≥8 抽检要求超额完成（31）。
- 复现：`python3 scripts/audit_knowledge.py --section locators`（首次运行会下载/校验 PG 文本；截断文件会被 START/END 标记拒绝）。
- 状态：CLOSED（无需修复）。

### KQ-12（PASS，CLOSED）v1.2 可选字段 / wikilink / source_ids 完整性

- 证据：
  - 42 个可选字段，**0** 个非法值/类型/适用类型错误；`fit_class` 与 `fit` 冲突 0；
  - 21 张卡使用可选字段（P4-2 新卡中 21/30 使用，可选性允许其余未用）；
  - `[[wikilink]]` 399/399 可解析（validate.py 与审计一致）；
  - `source_ids` 100% 解析；`verified` 内容卡无来源 = 0；`type=source` 卡 url/publisher/date/rights/source_kind/note 全非空。
- 状态：CLOSED。

### KQ-13（P1 流程，OPEN）62 张 draft 可追溯，但人工签核未完成（H4）

> **R1.1 状态更新（2026-11-05，task-56）**：已生成 `reports/DRAFT-SIGNOFF-R1.1.md`（62 行逐卡清单 + 45/17 分组 + 人工签字栏；未改任何卡状态、无自动提升）。KQ-13 的人类签核（H4）仍未完成，状态保持 **OPEN（等待人工）**。


- 证据：`reports/DRAFT-REVIEW.csv` 62 行 = GAR-EXAMPLE-001、23 LOOK、11 PRD、16 SCN、11 STY；当前 62 卡**全部仍 draft**（reviewed 0），无缺失、无漂移；
  - 结论分布：REVIEWED-CANDIDATE 45 / STAY_DRAFT 17；
  - 签核要求：38「人工签核」+ 20「人工重配来源/重写断言后复评」+ 4「确认 example 身份」；
  - `evidence_status_change` 62/62 为「无（禁止自动提升）」——未发生自动提升。
- 影响：62 卡仍不能计为 reviewed；若发布门禁把 reviewed 当条件，需保留 H4 为阻断（STATUS.md 已列 H4）。
- 修复：按 DRAFT-REVIEW 人工走签核；对 20 张「需重配来源/重写断言」优先处理；签核后同步 CSV 与卡 `review_status`。
- 验收：reviewed 数量 > 0 且与 CSV 一致；`audit_knowledge.py --section drafts` drift=0/missing=0；发布门禁显式记录 H4 状态。

### KQ-14（PASS，CLOSED）0-图片政策

- 证据：全 Vault 扫描 `![...](...)` = **0**；本地图片文件（png/jpg/jpeg/webp/gif/svg/bmp/tif）= **0**；来源卡均含 `rights_statement` 且图片策略为链接引用。
- 状态：CLOSED（与 `docs`/NEXT-PLAN 的 0 图片策略一致）。

### KQ-15（P3，WARN）审计工具与下载健壮性（已修复，记录方法）

- 证据：首轮 PG 文本下载出现截断（76299 只拿到 482,944/861,084 bytes），若直接使用会产生 31 条假定位失败；脚本已改为要求 START+END 标记且优先复用完整缓存（`/tmp/p4books`），之后 31/31 正常。
- 影响：任何依赖 PG 全文的审计必须校验完整性，否则会把网络问题误报为知识错误。
- 状态：CLOSED（脚本内置校验；复跑一致）。

## 3. P0 / P1 汇总（给 lead 的决策清单）

| 级别 | 数量 | 条目 |
|---|---|---|
| **P0** | **0** | — |
| **P1** | 4 | KQ-01 真重复卡（手袋）；KQ-05 许可字段粒度；KQ-06 输出缺「假设」标记；KQ-13 H4 人工签核未完成（流程） |
| P2 | 5 | KQ-02 tunic 范围重叠；KQ-03 别名冲突；KQ-04 来源重复 URL；KQ-07 Macbeth 语境粒度；KQ-08 年代/地域字段粒度 |
| P3 | 4 | KQ-09 无来源 interpretive 卡；KQ-10 启发式假阳性；KQ-15 工具健壮性；KQ-12 备注（21/30 v1.2 使用率） |
| PASS/CLOSED | 8 | KQ-11 书籍定位、KQ-12 v1.2/链接/来源、KQ-14 0 图片、其余摘要项 |

**发布判断**：知识质量无 P0；4 项 P1 中 KQ-01/05/06 可在一轮内修复，KQ-13 属人工流程。公开/发布前建议先关闭 KQ-01/KQ-05/KQ-06，并保留 H4 为显式阻断。

## 4. 三项独立状态字段提案（只建议，不改 schema）

现状问题：`evidence_status` 同时承担「卡片断言是否有证据」「来源是否真实」「许可是否清楚」三种语义；`review_status` 又混合「人工复核」与「草稿状态」。因此建议**分离**为三个独立字段（v1.3 可选字段，向后兼容；不改变 v1.1/v1.2 必填与枚举）：

| 字段 | 取值 | 判定依据 | 用途 |
|---|---|---|---|
| `data_status` | `complete` / `partial` / `missing` / `conflict` | 结构化字段完整度（periods/regions/category/材料/别名）+ 是否与其他卡冲突（KQ-01/02/03） | 数据可用性；影响检索/推荐前过滤 |
| `content_verified` | `verified` / `interpretive` / `example` / `unverified` | 断言是否有可解析来源；来源是否支撑断言（书籍定位、交叉验证）；无来源 interpretive 记 `interpretive` 而非 `unverified` | 事实强度；决定提示词/报告措辞 |
| `license_verified` | `verified` / `partial` / `not_applicable` / `unknown` | 内容许可与图像许可是否分别核验（KQ-05）；`partial`=内容许可清楚但图像未核验或反之 | 公开/商用发布门禁；与 0-图片策略联动 |

**试评结果（本审计脚本按现有字段推导，非最终人工判定）**：

- `data_status`：内容卡 188/188 具备 ≥3 个描述维度（`complete`）；来源卡 211/211 元数据完整（`complete`）；KQ-01/02/03 冲突项标 `conflict` 候选 3 张（GAR-0048/0087/0075，或合并后 1 张）。
- `content_verified`：内容卡 **verified 141 / interpretive 43 / example 4**；其中 5 张 interpretive 无来源（KQ-09）→ 建议记 `interpretive`（不升级、不阻断）。来源卡 211 为 `not_applicable`（来源记录自身不做内容断言，或记 `verified` 表示卡存在性已核验，两者二选一需 schema 明确）。
- `license_verified`：来源卡 **verified 208 / partial 3（KQ-05）/ not_applicable 188（内容卡）**；内容卡不直接主张第三方许可。
- 迁移建议：先以**旁路报告**（`reports/CARD-STATUS.csv` 或 validator 扩展）计算三字段，不改卡片；确认稳定后再作为 v1.3 可选字段写入 frontmatter，并在 `00-系统/数据字典.md` 登记枚举；旧卡默认 `data_status=complete`、`content_verified=evidence_status`、`license_verified=not_applicable`（来源卡除外）。
- 验收：三字段在 399 卡上可计算且与 validator 不冲突；抽查 20 卡人工判定一致率 ≥95%；发布门禁能分别引用三者（例如：public-ready 需 `content_verified!=unverified` 且 `license_verified=verified/not_applicable`）。

## 5. 已通过项（不再重复排查）

- 重复 ID：0（399/399 唯一）；文件名与 ID 前缀一致；YAML 扁平可解析（与 `validate.py` 17/17 PASS 一致）。
- 来源真实性：`build_sources.py` PASS（CSV 与 211 来源卡一致，0 缺失/0 多余/0 字段差异）；3 组重复 URL 已记录（KQ-04）。
- 书籍来源：9/9 PD 文本 HTTP 200；31/31 定位；页码 UNCONFIRMED；P4 索引与来源卡一致。
- 0-图片策略：0 内嵌 / 0 文件（KQ-14）。

## 6. 限制与后续

- 启发式检出（KQ-03/08/10）含假阳性；本报告已逐条人工抽读分级，P0/P1 均为人工确认。
- `license_status` 的「正确性」依赖来源页（部分来源仅能链接、无法逐页复核图像）；KQ-05 只解决**字段表达**问题，不等于已完成逐图授权核验（H2 仍开放）。
- 62 draft 的人工签核（H4）不在本审计范围，仅提供可追溯证据；不可由脚本代签。
- 建议下一轮：先修 KQ-01/05/06（一轮内可关闭），再对 KQ-02/03/04/08 做卡片级最小改动；KQ-07 需新语境卡（可与 P4-2 结构扩展同批）。

## 7. 复现命令

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter

# 全量审计（人读）
python3 scripts/audit_knowledge.py

# 机读结果（写到 /tmp，不污染 Vault）
python3 scripts/audit_knowledge.py --json > /tmp/audit.json

# 单域复跑
python3 scripts/audit_knowledge.py --section dups
python3 scripts/audit_knowledge.py --section locators
python3 scripts/audit_knowledge.py --section periods
python3 scripts/audit_knowledge.py --section v12
python3 scripts/audit_knowledge.py --section sep
python3 scripts/audit_knowledge.py --section drafts
python3 scripts/audit_knowledge.py --section license
python3 scripts/audit_knowledge.py --section proposal

# 交叉复核（项目既有）
python3 scripts/validate.py
python3 scripts/build_sources.py
```
