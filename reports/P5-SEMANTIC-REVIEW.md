# P5-A 语义关系与 MOC 独立复核

- 日期：2026-11-05（Asia/Shanghai）；复核者：narrator（独立于 P5-A worker 自评）
- 性质：**静态语义/导航审查**。只写 `reports/P5-SEMANTIC-REVIEW.md` 与 `11-验收/P5/SEMANTIC-SPOTCHECK.csv`；未修改卡片/脚本/MOC。
- **Obsidian GUI：NOT_RUN**。本环境未打开 Obsidian、未做点击/渲染/图谱/搜索；本文所有结论均来自文件静态读取与 `scripts/validate.py` 的链接校验。**不得把本报告当作 GUI UAT 通过。**
- 基线：HEAD `1acb4d3` + P5 工作区；400 卡（189 内容 + 211 来源）；`validate.py` PASS 400/400、0 errors；P5 产物：`00-系统/MOC/` 9 页、`11-验收/P5/RELATION-CANDIDATES.csv` 677 行、`11-验收/P5/source-audit.csv`、`REVIEW-QUEUE.csv`。
- 抽检样本：`11-验收/P5/pilot-report.json` 的 **30 张 pilot 内容卡**（GAR-0002…GAR-0076）及其已迁移 `relations`；另从候选 CSV 抽 **10 条**设计/语境/材料关系做反例审查。逐行结果见 `11-验收/P5/SEMANTIC-SPOTCHECK.csv`（40 行）。

## 0. 结论摘要

| 项 | 结果 | 说明 |
|---|---|---|
| 30 张 pilot 卡（主 relation） | **28 PASS / 2 WEAK** = **93.3%** | 主要是 `claim_supported_by` high/verified，目标真实、类型匹配；2 条因证据范围/置信越级降为 WEAK |
| 40 条关系逐行抽检 | **28 PASS / 8 WEAK / 4 MISLINK** = **70.0% pass** | 候选层的 `may_have_part`/`ensemble_with`/`context_includes`/`uses_material` 是主要问题来源 |
| 误连/弱连候选 | **12 条**（4 mislink + 8 weak） | 见 §3；满足“至少 5 条”要求 |
| MOC 9 页 | **9/9 存在、跨页链接完整、0 broken** | README + 8 内容页；导航可用但**发现路径/密度/独立专题**有 WARN |
| 独立专题（拜占庭/莫卧儿/日本/奥斯曼/非西方） | **未被类型化关系强行连通** | 但卡片 `## 相关卡片` 有泛化跨文化比较；MOC 无区域专题入口，属“欠导航”而非“强连通” |
| GUI | **NOT_RUN** | 静态审查，不声称 Obsidian 渲染/点击通过 |

**总体判断**：**已迁移的 `claim_supported_by` 关系语义质量高（pilot 93.3%）**；但候选层（677 行）不能整体视为可用关系——`may_have_part`/`ensemble_with` 只是 LOOK 共现，`context_includes` 存在真实错配，`uses_material` 存在把“物性卡”当材料卡的误连。MOC 可作为静态目录使用，但入口和密度需要改进。

---

## 1. 方法与证据

1. 读取 30 张 pilot 卡 frontmatter `relations`，逐条核对 subject/object 类型、证据、置信、`source_ids`、目标卡语义，并与来源卡标题/正文范围对照。
2. 从 `RELATION-CANDIDATES.csv` 选取 `context_includes`/`may_have_part`/`ensemble_with`/`uses_material`/`in_style`/`appears_in_look` 中涉及 pilot 卡或高风险配对的 10 条，做反例审查。
3. 读取 `00-系统/MOC/` 9 个文件：标题、分组、行数、`[[...]]` 链接数/重复、跨 MOC 链接、卡片→MOC 反向链接。
4. 用卡片 `periods`/`regions`/`key_garments` 对照 `context_includes` 目标，人工判断年代/地域是否成立。
5. 静态链接完整性以 `python3 scripts/validate.py` 为准（PASS 400/400；MOC 页 `[[...]]` 无 broken）。
6. 未执行 GUI；未用截图/按钮/Properties/图谱；不把脚本 PASS 当语义 PASS。

---

## 2. Pilot 30 张卡抽检结果

- 30/30 卡均有至少 1 条新 `relations`（共 34 条 relation 行；多数为 1 条，GAR-0072/0077/0033/0076 各 2 条）。
- 34 条中 32 条是 `claim_supported_by`（high/verified），1 条 `uses_material`（GAR-0020 → MAT-0001），1 条 `claim_supported_by` 的第二来源（GAR-0033 → SRC-0155，WEAK）。
- 30 张卡主 relation 判定：**28 PASS / 2 WEAK**（93.3%）。
  - PASS 例：GAR-0002 达布里特 → SRC-0103 FIT doublet；GAR-0008 马甲 → SRC-0109 FIT vest/waistcoat；GAR-0072 帕贾马裤 → SRC-0453/0454 V&A paijama；GAR-0077 紧身长袜 → SRC-0484/0485 V&A；GAR-0001 和服 → SRC-0100 Met 江户和服；GAR-0065 出口和服 → SRC-0426 V&A 1910–30 出口和服。
  - WEAK 1：**GAR-0020 假衬衣 → MAT-0001 平纹细布（uses_material, high/verified）**——schema `00-系统/关系类型.md` §2 明确 `uses_material` **最高 medium**；卡内却写 `confidence=high`、`rule=R-MATERIAL-FIELD`（v1 规则表无此规则），属于**置信/规则越级**。关系方向可解释（假衬衣常用 muslin），但不能以 high 迁移。
  - WEAK 2：**GAR-0045 风衣 → SRC-0405（V&A 2014 Burberry Prorsum 蕾丝风衣）**——该来源可支撑“现代 designer trench 实例”，但 GAR-0045 是通用风衣卡，来源不足以单独支撑其通用历史/结构断言；应标 instance/range 或补 19–20 世纪来源。
- 其余 28 张卡的 claim 关系目标与卡片主题一致，且 source_ids 可解析；未发现“事实关系冒充史实”越级（除上述 2 条）。

> 逐行结果（card_id/relation/judgement/reason/recommendation）见 `11-验收/P5/SEMANTIC-SPOTCHECK.csv` 前 30 行。

---

## 3. 误连/弱连候选（12 条）

| # | card_id | relation | 判定 | 证据/原因 | 建议 |
|---|---|---|---|---|---|
| 1 | PRD-0007 | `context_includes: PRD-0007 → GAR-0006`（high/verified） | **MISLINK** | PRD-0007 = 1950 年代美英语境；GAR-0006 达希基套衫 periods = 1960s/70s/contemporary；高置信关系存在明确年代错配 | PRD-0007.key_garments 移除 GAR-0006，或改挂 PRD-0008（1960s）；重生成 |
| 2 | PRD-0010 | `context_includes: PRD-0010 → MAT-0003`（high/verified） | **MISLINK** | PRD-0010 = 拜占庭帝国晚期；MAT-0003 是 16–19 世纪欧洲 passementerie/编带类材料；同库已有 MAT-0011 拜占庭 samite | key_garments 改指 MAT-0011（或删除）；MAT-0003 进 review |
| 3 | GAR-0002 | `uses_material: GAR-0002 → MAT-0013`（medium/verified） | **MISLINK** | MAT-0013 是“克重与垂坠”物性卡（type=material 但语义是 material_property）；token `linen` 命中 fiber_content 不等于“使用该材料” | 规则排除属性卡；不要迁移；如需 linen 关系指向真实亚麻材料卡 |
| 4 | GAR-0013 | `may_have_part: GAR-0013 → STR-0001`（medium/interpretive） | **MISLINK** | GAR-0013 是遮阴袋/codpiece；STR-0001 是美第奇领/Medici collar；二者仅在 LOOK-0003 共现，codpiece 不存在“有领子”的结构关系 | 删除该候选；改成 LOOK-0003 的两个独立 `appears_in_look` |
| 5 | GAR-0002 | `may_have_part: GAR-0002 → STR-0001`（medium/interpretive） | WEAK | 达布里特与美第奇领同现；领子可与 doublet 搭配，但共现不是结构字段证据 | 留 review；人工确认部件后再 `has_part` |
| 6 | GAR-0003 | `may_have_part: GAR-0003 → STR-0001`（medium/interpretive） | WEAK | 杰金与美第奇领同现；同样只是搭配候选 | 留 review；与 #5 合并结构审核 |
| 7 | GAR-0033 | `claim_supported_by: GAR-0033 → SRC-0155`（high/verified） | WEAK | GAR-0033 西式休闲西装 periods=1940s；SRC-0155 是 1930–1939 FIT 概览，不能覆盖 1940s 具体断言（卡内另有 SRC-0204 1940s 实例） | 以 SRC-0204 为主证据；SRC-0155 降背景或删除 |
| 8 | GAR-0002 | `ensemble_with: GAR-0002 → GAR-0024`（medium/interpretive） | WEAK | 达布里特与穆勒鞋仅在 LOOK-0003 同现；16 世纪男装 + 16–18 世纪 mule 是策展搭配，不是历史搭配 | 保留设计候选；迁移时写“design ensemble in LOOK-0003” |
| 9 | LOOK-0001 | `in_style: LOOK-0001 → STY-0010`（medium/interpretive） | WEAK | style_tags 精确含 STY-0010（时代剧历史考据），但 LOOK-0001 是 1770s 洛可可沙龙；属于设计风格标签，不是事实层关系 | 保留 medium/design；MOC/正文标“设计风格标签” |
| 10 | LOOK-EXAMPLE-001 | `appears_in_look: LOOK-EXAMPLE-001 → GAR-0014`（low/example） | WEAK | 目标含 example 卡；example LOOK 可演示模板，但不能进入迁移/生产关系 | 过滤 example/low 行；不迁移 |
| 11 | GAR-0020 | `uses_material: GAR-0020 → MAT-0001`（high/verified） | WEAK | `uses_material` 最高 medium；卡内 high + 旧 rule R-MATERIAL-FIELD；token 关联不足以 high | 降 medium/review；补 canonical material 关系 |
| 12 | GAR-0045 | `claim_supported_by: GAR-0045 → SRC-0405`（high/verified） | WEAK | SRC-0405 是 2014 Burberry 蕾丝风衣实例，支撑现代实例而非通用风衣历史/结构 | 保留为 instance；补 19–20 世纪来源或标 gap |

- 合计：**4 MISLINK + 8 WEAK**；其中 §3 #1–#4 为明确误连，其余为证据/置信/设计层级上的弱连。
- 这说明：**claim 层是事实关系（可用），候选的设计/语境/材料层是 hypothesis（须审核）**；`may_have_part`/`ensemble_with` 绝不能直接升格为 `has_part`/历史搭配。

---

## 4. 事实关系 vs 创作推断的分层检查

| 关系类型 | 本次抽检表现 | 判断 |
|---|---|---|
| `claim_supported_by`（high/verified） | pilot 32/34 条目标/主题匹配；2 条 WEAK（GAR-0033 的 1930s 来源、GAR-0045 的现代实例） | **事实层基本可信**；仍要检查来源覆盖范围（instance vs general） |
| `context_includes`（high/verified） | 45 条高置信；抽检发现 PRD-0007→GAR-0006、PRD-0010→MAT-0003 两条年代/文化错配 | **语境级，不等于逐单品史实**；语义审查必须逐对做 |
| `appears_in_look`/`look_appears_in_scene`（medium/interpretive） | LOOK 显式字段；关系本身正确，但组合是策展/设计 | **设计层**；不得当历史套装 |
| `ensemble_with`/`may_have_part`（medium/interpretive） | 共现候选；抽检 4/10 反例；类型上不可能 high | **只能是候选**；迁移前需人工/结构证据 |
| `uses_material`（medium/verified） | token 映射；MAT-0013 物性卡被误当材料 | **材料族候选**；需 canonical material ID；排除属性卡 |
| `in_style`（medium/interpretive） | style_tags 精确；设计语言 | **风格标签**，不是史实风格证据 |

> 与 `00-系统/关系类型.md` 的一致性：来源/语境/风格 high 的语义边界写在文档中；本次问题主要是**执行层越级**（GAR-0020 high uses_material）与**上游 key_garments 错配**（PRD-0007/0010），不是 schema 没写清楚。

---

## 5. MOC 9 页静态审查

### 5.1 逐页结果

| MOC | 行数（条目） | `[[...]]` 链接 | 分组 | 静态判定 |
|---|---:|---:|---|---|
| `README.md` | 32 | 18（8 个重复为入口+路径） | 总览 + 5 条浏览路径 + 维护规则 | **PASS**（hub 清晰；重复链接是导航复用） |
| `服装单品.md` | 151（88 卡） | 95 | category 11 组 | **PASS（密度高但可扫）**；含 GAR-0087（已迁移 redirect），与鞋履配饰页重复列出 |
| `结构细节.md` | 96（26 卡） | 29 | part_family 13 组 | **PASS** |
| `材质纹样.md` | 34（14 卡） | 16 | material/pattern | **PASS** |
| `鞋履配饰.md` | 62（32 卡） | 35 | footwear/headwear/accessory/carried_prop | **PASS** |
| `时代地域.md` | 89（11 PRD） | 17 | period 14 组（多时段重复） | **WARN**：PRD-0002 出现 3 次、PRD-0011 出现 2 次（多 period 归组导致），无 region 分组，易被误读为重复卡 |
| `风格体系.md` | 51（11 卡） | 13 | category 7 组 | **PASS** |
| `造型组合.md` | 62（23 LOOK + 16 SCN） | 41 | LOOK/SCN | **PASS**（LOOK/SCN 分开，好） |
| `来源证据.md` | 261（211 SRC） | 218 | source_kind 9 组 | **WARN（过密）**：单页 211 行/218 链接；未标 deprecated/duplicate 来源；被引次数无上下文 |

- 跨 MOC 链接：README 覆盖 8 页；内容页互相链接（服装→结构/材质/鞋履；时代→风格/来源；造型→风格/单品）；**跨页导航存在**。
- 链接完整性：`validate.py` PASS 400/400；MOC 页 `[[...]]` 无 broken（静态）。

### 5.2 MOC 问题（按严重度）

1. **MOC 入口不可从主索引到达**：`00-系统/索引.md` 的“目录地图”未列 `MOC/` 或 `关系类型`；MOC 只能通过文件树/README 打开。同时**卡片→MOC 反向链接为 0**（扫 01–09 的 cards，0 个 `[[服装单品]]`/`[[结构细节]]` 等链接）——用户从任何单品卡无法跳回 MOC。**建议**：在索引首屏加入 MOC 入口；在每张卡末尾（或 `## 相关卡片` 后）加“MOC：[[服装单品]]”等导航（纯导航，不是关系断言）。
2. **来源证据页过密且不分层**：211 来源一页列完，仅按 `source_kind` 分组；`SRC-0157/0163/0175` 是 `blacklist_duplicate` 却与正常卡同样展示；无“已引用/未引用/待补引用”筛选或标记。**建议**：拆成 `来源证据-已引用` / `来源证据-背景/独立`，或在行内加 `migration_class`/deprecated 标记；保留 211 可检索但默认先展 143 connected。
3. **服装单品页与鞋履配饰页重复列出 GAR-0087**：`服装单品` category=bag_redirect、`鞋履配饰` carried_prop 也列出，且都标“已迁移”；卡本身是 redirect/deprecated。**建议**：只在鞋履配饰页保留 redirect 行，或从计数中排除 deprecated。
4. **时代地域页多 period 重复**：PRD-0002 出现在 1790s/1800s/1810s 三组、PRD-0011 出现在 1930s/republican_era 两组；不是错误，但读者会以为重复卡。**建议**：行内注明“multi-period: 1790s–1810s”，或按 region 分组再列 period。
5. **独立专题无入口**：拜占庭/莫卧儿/日本/奥斯曼/非西方只在综合品类表里以单行出现（如 GAR-0071 莫卧儿 jama、MAT-0011 拜占庭 samite、PRD-0010 拜占庭、PRD-0009 奥斯曼）；没有“区域/专题 MOC”。**建议**：新增 `区域专题.md`，按 region 列卡，页面顶部明确“并列展示 ≠ 文化同源/可互换”。

---

## 6. 独立专题（拜占庭/莫卧儿/日本/奥斯曼/非西方）

**结论：未被“类型化关系”强行连通；但卡片导航层有泛化比较，MOC 层欠导航。**

1. **类型化关系**：`claim_supported_by` 只指向各自来源（GAR-0009 拜占庭 dalmatic→SRC-0110 FIT；GAR-0071/0072 莫卧儿/南亚→SRC-0450–0454 V&A；GAR-0001/0065 日本→SRC-0100/0426；GAR-0009/PRD-0010 拜占庭；GAR-0004 伊斯兰/奥斯曼语境等），**没有**把日本卡连到中国卡、把莫卧儿卡连到欧洲卡的事实关系。
2. **独立专题的“弱/强连”问题**只在：
   - `context_includes` **PRD-0007→GAR-0006**（1950s vs 1960s+）、**PRD-0010→MAT-0003**（拜占庭 vs 16–19c passementerie）——是**上游 key_garments 错配**，不是专题互连；
   - 卡片 `## 相关卡片` 的泛化跨文化链接：GAR-0001 和服→STR-0003 拉夫领/MAT-0005 肯特布/GAR-0029 托加袍/GAR-0015 法式长袍；GAR-0004 卡夫坦→GAR-0005 布布/GAR-0029 托加/MAT-0005 肯特/GAR-0001 和服；GAR-0072 帕贾马→GAR-0059 1970s 牛仔背带裤/GAR-0010 灯笼裤。这些**不是 typed relation**，但作为“相关卡片”容易被误读为等价/同源。
   - **建议**：把卡片 `相关卡片` 分成「同文化/同结构」与「跨文化比较（analogy）」两栏；跨文化比较要写一句边界（“仅比较轮廓/层搭，不是同源或可互换”），或从卡片正文移到 MOC 的区域专题，避免在单卡层制造伪关系。
3. **MOC**：`服装单品` 按 category 分组，把日本和服、西非 boubou、莫卧儿 jama、欧洲 robe 混在同一“robe/one_piece”列表；这是**并列展示，不是连接**，但会让用户以为它们可直接比较。新增按 region 的专题页可解决“欠导航”，同时不添加事实关系。

---

## 7. 建议优先级

| 优先级 | 动作 | 对应问题 |
|---|---|---|
| P0 | 修复 `context_includes` 两处明确错配（PRD-0007→GAR-0006、PRD-0010→MAT-0003），重生成候选 | §3 #1/#2 |
| P0 | `uses_material` 规则排除“物性卡”（MAT-0013）并把 GAR-0020 high 降 medium | §3 #3/#11 |
| P1 | `may_have_part` 移除 codpiece→collar 类误连；其余共现候选保留 review，禁止迁移为 has_part | §3 #4–#6 |
| P1 | GAR-0033 的 SRC-0155、GAR-0045 的 SRC-0405 标 instance/背景或补来源 | §3 #7/#12 |
| P1 | MOC 入口：索引首屏 + 卡片→MOC 导航；来源证据页加 deprecated/connected 标记 | §5.2 #1/#2 |
| P2 | 新增区域/专题 MOC；卡片相关链接区分同文化/跨文化比较 | §6 |
| P2 | 时代地域/鞋履配饰页去重/redirect 标注 | §5.2 #3/#4 |

---

## 8. 限制（必须保留）

- **GUI NOT_RUN**：未打开 Obsidian，未验证渲染、wikilink 点击、Properties、搜索、图谱、图片外链；本报告不构成 GUI UAT 通过。
- 抽检为**静态人工判断**，不是全量 677 条关系的语义审计；40 条样本偏向 pilot 卡与高风险类型，不能外推为“全部关系 70% 正确”。
- 未修改卡片/脚本/MOC；`RELATION-CANDIDATES.csv`/`pilot-report.json` 的生成逻辑未复核；只审查产物语义。
- 未做导演评分；关系/风格判定是知识层判断，不是创作评分。
- MOC 链接完整性依赖 `validate.py`（静态）；Obsidian 实际渲染/别名解析未测。
