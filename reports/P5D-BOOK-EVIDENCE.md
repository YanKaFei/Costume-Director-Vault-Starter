# P5-D 九本公版书章节级证据与卡片引用（P5D-BOOK-EVIDENCE）

- 生成：2026-11-05（Asia/Shanghai）；worker：researcher（task-83，P5-D 书籍证据深化）
- 写权限：本报告 + `06-时代地域/书籍研究/`（+`04-来源/` 如需）。§1–§8 为评估（写卡前状态）；**§9 为 lead 批准后的实际应用记录**（18 卡/19 组，未改 evidence_status/事实）。
- 基线：HEAD `5ae2c52`，458 卡 = 224 内容 + 234 来源；9 本书来源卡 SRC-0061..0069 已存在（PD in USA）。
- 引用规则：一律 `book_fact`，格式 `book_fact: 《书名》PG<id>，章「X」，段 n，行 n（page UNCONFIRMED）`；**书内事实不得单独支撑 `verified`**，卡片已有独立来源的 verified 状态不因加书源改变。
- 关联：`06-时代地域/书籍研究/书籍章节级证据与卡片引用.md`（给 architect/lead 的逐卡清单）。

## 0. 总览

| 指标 | 结果 |
|---|---|
| 深化书籍 | **5 本**：高复用 PG21534、PG76299；中用 PG46949、PG48551、PG34903 |
| 建立 locator | **32 条**（21534 11 + 76299 13 + 46949 3 + 48551 2 + 34903 3） |
| 卡片级证据候选 | **25 组**（19 组直接支撑 + 6 组部分支撑），去重后 **24 张卡**（直接 18 + 部分 6） |
| 建议可加 `source_ids` 的卡 | **18 张卡 / 19 组证据**（book_fact，非 standalone verified；见 §2 表；MAT-0015 两组） |
| 未匹配/不建议加 | **5 组**（语义错配/仅背景；见 §4） |
| 许可 | 文本 PD US；PG License 约束再分发；无图版/无图像；译文/数据集口径见 §5 |
| 应用记录 | §1–§8 为评估；§9 经 lead 批准应用 18 卡/19 组 source_ids（0 evidence_status/事实变更） |

## 1. 五本书章节级定位（新增/复核）

### PG 21534《Textiles and Clothing》（SRC-0062，1907）
章节数 39；本次新增 11 条可引用定位（章/段/行，页码 UNCONFIRMED）：

| 主题 | 章 | 段 | 行 | 原文要点 |
|---|---|---|---|---|
| 羊毛纤维 | Wool | 3 | 737 | “Wool is the most important animal fiber… scale-like surface which gives it its felting and spinning…” |
| 亚麻纤维 | Flax | 2 | 860 | “Next to wool and cotton, flax… linen fiber consists of the bast cells…” |
| 蚕丝纤维 | Silk | 2 | 1018 | “The silk fiber is the most perfect… fine and continuous…” |
| 织物组织 | Weaves | 2 | 1332 | “The great variety of weaves… modifications of a few fundamental weaves…” |
| 门襟定义 | Plackets | 2 | 3169 | “A placket is an opening in a garment allowing it to be put on…” |
| 衣摆/折边 | Hems | 3 | 2953 | “A hem is a fold of goods twice folded to protect a raw edge…” |
| 纽扣/扣眼 | Fastenings | 2 | 3277 | “The standard fastenings are buttons and button holes, hooks and eyes…” |
| 七片裙/裁片 | Patterns | 7 | 4045 | “SEVEN-GORED SKIRT… a well-fitting skirt should hang even…” |
| 领/衬 | Collars | 2 | 4749 | “The shaped, standing collar… an interlining of canvas or crinoline is necessary.” |
| 抽褶 | Hand Sewing | 24 | 2648 | “Gathering, gauging, casing, etc., are used for drawing up the fullness…” |
| 抽褶做法 | Hand Sewing | 26 | 2654 | “For gathering, the cloth is held in the same manner as for running…” |

### PG 76299《A Dictionary of Men's Wear》（SRC-0066，1908）
词典体（无章节，词条=定位）；本次 13 个词条：Waistcoat 16668/段5147、Frock coat 6367/1945、Sack coat 12504/3864、Knickerbockers 8515/2604、Hose 7819/2377、Tweed 16062/4979、Flannel 5939/1803、Serge 13006/4020、Worsteds 17403/5352、Denim 4342/1339、Overalls 10546/3245、Cravat 3944/1206、Spats 14344/4439。

### PG 46949《Chats on Costume》（SRC-0069，1906）
- Tunic：II THE TUNIC，段 6，行 1374（“The earliest made-up garment… a simple bag…”）
- Kirtle or Petticoat：V THE KIRTLE OR PETTICOAT，段 11，行 2811（“The kirtle or petticoat is in reality a development of the tunic…”）
- Collars and Cuffs：VII COLLARS AND CUFFS，段 8，行 3598（“collar and cuff… linen, lace… separate from the rest of the costume…”）

### PG 48551《Costume: Fanciful, Historical and Theatrical》（SRC-0064，1906）
- 17 世纪初套装：CHAPTER VII，段 9，行 1821（“With the farthingale were worn long sleeves, lace coifs, and fluted basques, and stomachers…”）
- 裙撑谱系：CHAPTER XVII，段 24，行 5155（“The crinoline boasts as its great-great-grand-mother the farthingale…”）
- Fancy dress 概念：CHAPTER XV，段 16，行 4561（“not by the borrowing of clothes, but by making them, planning them, inventing them…”）

### PG 34903《Dress Design》（SRC-0061，1919/1920 reprint）
- 16 世纪前装饰：CHAPTER V，段 3，行 1402（“applied ornamental bands at the neck, waist, and borders of skirt and cloak…”）
- slashed/puffed：CHAPTER V，段 4，行 1419（“we enter what may be termed the slashed and puffed period…”）
- farthingale 支撑：CHAPTER V，段 63，行 1745（“full pleated skirt was supported on a farthingale or hoop…”）

## 2. 建议可新增书籍 `source_ids` 的现有卡（18 张 / 19 组，book_fact）

> 全部为“卡片断言 ↔ 书内原句”直接对应；只加 `source_ids` + 正文可见引用，不改正文事实、不改 evidence_status。

| # | 卡 | 书籍来源 | 定位（章/段/行） | 卡片断言 | 书内支撑句（摘录） | 置信 |
|---|---|---|---|---|---|---|
| 1 | MAT-0015 羊毛织物 | SRC-0062 PG21534 | Wool / 3 / 737 | 羊毛纤维/毡缩/手感 | “Wool… scale-like surface which gives it its felting and spinning…” | 高 |
| 2 | MAT-0015 羊毛织物 | SRC-0066 PG76299 | Tweed 16062/4979；Flannel 5939/1803；Serge 13006/4020；Worsteds 17403/5352 | 羊毛织物家族（tweed/flannel/serge/worsted） | 词条定义（twill/all-wool/soft open texture 等） | 高（仅词义，不证明具体卡断言全部） |
| 3 | MAT-0016 亚麻织物 | SRC-0062 | Flax / 2 / 860 | 亚麻纤维来源（flax bast cells） | “linen fiber consists of the bast cells…” | 高 |
| 4 | MAT-0018 丝绸 | SRC-0062 | Silk / 2 / 1018 | 蚕丝纤维连续/细长 | “The silk fiber… fine and continuous…” | 高 |
| 5 | MAT-0012 织物组织 | SRC-0062 | Weaves / 2 / 1332 | 三大基础组织是少数基本组织变体 | “modifications of a few fundamental weaves…” | 高 |
| 6 | STR-0017 门襟 | SRC-0062 | Plackets / 2 / 3169 | 门襟=便于穿着的开口 | “A placket is an opening in a garment allowing it to be put on…” | 高 |
| 7 | STR-0016 衣摆与开衩 | SRC-0062 | Hems / 3 / 2953 | 折边=双折保护毛边 | “A hem is a fold of goods twice folded to protect a raw edge…” | 高 |
| 8 | STR-0018 纽扣与扣眼 | SRC-0062 | Fastenings / 2 / 3277 | 纽扣/扣眼/钩眼/系带等标准闭合 | “standard fastenings are buttons and button holes, hooks and eyes…” | 高 |
| 9 | STR-0020 裁片与拼片 | SRC-0062 | Patterns / 7 / 4045 | gore/多片裙结构 | “SEVEN-GORED SKIRT… hang even…” | 中高（结构原则，非片数定义） |
| 10 | STR-0030 里布与衬 | SRC-0062 | Collars / 2 / 4749 | 领需 canvas/crinoline interlining | “an interlining of canvas or crinoline is necessary” | 中高（interlining 应用实例） |
| 11 | STR-0032 褶裥与抽褶 | SRC-0062 | Hand Sewing / 24 / 2648；26 / 2654 | 抽褶用于聚拢量 | “Gathering… drawing up the fullness…” | 中高（工艺操作，非历史） |
| 12 | GAR-0008 马甲 | SRC-0066 | Waistcoat / 5147 / 16668 | 无袖、及腰、前后片结构 | 词条原文（foreparts/backs 结构） | 高 |
| 13 | GAR-0017 夫罗克大衣 | SRC-0066 | Frock coat / 1945 / 6367 | 前片/侧体/后片/裙摆裁片 | 词条原文（forepart/sidebody/backpart/skirt） | 高 |
| 14 | GAR-0033 西式休闲西装 | SRC-0066 | Sack coat / 3864 / 12504 | 无裙摆短外套=lounge coat | “Also called lounge c.” | 中高（命名与结构，非 1940s 史） |
| 15 | GAR-0011 尼克裤 | SRC-0066 | Knickerbockers / 2604 / 8515 | 膝裤、宽松膝、束带 | 词条原文 | 高 |
| 16 | GAR-0077 紧身长袜 | SRC-0066 | Hose / 2377 / 7819 | hose=stockings，古义 tights | 词条原文 | 高 |
| 17 | GAR-0079 基尔特长袍 | SRC-0069 | Kirtle / 11 / 2811 | kirtle 由 tunic 发展（贴身 bodice+垂褶） | “kirtle or petticoat… closely fitting bodice, with long draperies…” | 中高（本卡现为 interpretive，加书源后仍不得升 verified） |
| 18 | STR-0010 剪口装饰 | SRC-0061 | CHAPTER V / 4 / 1419 | 16c slashed and puffed | “slashed and puffed period… sleeves of Henry VIII…” | 高 |
| 19 | STR-0006 胸衣插片 | SRC-0064 | CHAPTER VII / 9 / 1821 | 17c stomacher 与 farthingale 同穿 | “With the farthingale were worn… stomachers” | 中（存在/搭配，不含结构细节） |

## 3. 部分支撑（6 组，建议只作背景或需改写断言）

| 卡 | 书/定位 | 问题 | 建议 |
|---|---|---|---|
| GAR-0007 衬衫式女衫 | PG21534 Patterns / 56 / 4303 | 书只讲 shirtwaist 缝制（trace seams/grain），不含 1890s 成衣史/领型断言 | 只把“缝制/经向”作 book_fact；历史断言保留现有 FIT 来源 |
| STR-0012 翻领与驳领 | PG21534 Collars / 2 / 4749 | 书讲 standing collar，不是 turndown/lapel 分类 | 不加；或只作“领需衬”背景 |
| STR-0023 袖口 | PG46949 Collars & Cuffs / 8 / 3598 | 书讲可分离 collar/cuff 概念，不含 cuff 类型（turnback/french） | 可作 detachable cuff book_fact，类型断言另引 |
| STR-0008 笼式裙撑 | PG48551 CHAPTER XVII / 24 / 5155 | 书讲 farthingale→crinoline 谱系，不含 1850s 钢圈结构 | 只作谱系背景；1850s 事实保留现有来源 |
| STY-0010 时代剧历史考据 | PG48551 CHAPTER XV / 16 / 4561 | 书是 fancy dress 的“再创作”论，与方法论卡不同 | 仅作“历史 vs 化装”概念对照，不挂 source_ids |
| STR-0029 泡泡袖 | PG34903 CHAPTER V / 4 / 1419 | 书是 16c puffed 袖，卡是 1825 实例；年代错位 | 不加；改用 SRC-0533 |

## 4. 未匹配 / 不建议加（5 组）

| 卡 | 书/定位 | 原因 |
|---|---|---|
| GAR-0038 连体工作服 | PG76299 Overalls / 3245 / 10546 | 1908 “overalls”=loose over-trousers（罩裤），与卡“bib 连体工装”语义不同 → 语义错配，勿加 |
| GAR-0059 1970s 牛仔背带裤 | PG76299 Denim / 1339 / 4342 | 书只给 denim 织物定义，不含 1970s 时装史；可加仅限“denim 织物”断言，但卡无该断言 → 不加 |
| GAR-0002 达布里特 | PG46949 Doublet & Hose / 7-9 / 2351 | 书仅一句“tunic 让位于 doublet”，无结构/年代细节 → 不加 |
| GAR-0045 风衣 | PG76299 Gabardine / 2009 / 6710 | 1908 gabardine=俄国犹太人长袍，与卡 Burberry 织物义冲突（语义演变见 C08）→ 勿作支撑，只作语义史背景 |
| STR-0008 / GAR-0085 等 | PG46949 / 34903 的文学引文段 | 章节含文学引文与轶事，无结构断言 → 不加 |

## 5. 许可边界（文本/译文/图版/数据集）

| 对象 | 权利/许可 | 本库用法 |
|---|---|---|
| **书籍纯文本（9 本）** | Project Gutenberg 页头：**Public domain in the USA**；再分发其制备文本须遵守 **Project Gutenberg License**（保留许可/商标，不暗示背书） | 只取文本事实；`book_fact`；不复制整章/整书；不内嵌 |
| **现代译文** | PG76717 为 1882 英译（Frances Cashel Hoey & John Lillie），译本是历史公版（pre-1929）；**不使用任何现代译本/注疏** | 引用时标“1882 英译”+章/段/行；不信现代译注 |
| **图版/插图** | 纯文本 `.txt` 不含插图；PG 文本许可不覆盖插图；GITenberg 镜像可能含图，但**本库未下载/未使用** | 0 图片；若要引图须逐图另核权利（H2 仍开放） |
| **数据集/元数据** | PG ebook 书目元数据 + GITenberg repo README/license（PD/PG License）；`11-验收/P4-BOOKS/extracted/` 为本项目解析产物 | 仅本地分析；不再分发数据集；无 AI 训练授权声明 |
| **9 本中仅背景** | PG33020、PG56978、PG76717、PG49559 | 1947/1882/1902 旧著或行业史，只作时代/语境背景，不作新卡直接证据 |
| **0 图片策略** | 不变 | 0 下载、0 内嵌 |

## 6. 若协调后实际加入 `source_ids`（给 architect/lead 的操作清单）

1. 只在 §2 的 18 张卡（19 组证据）上加对应书源；每次只加“书内原句确实支持该断言”的那一条，不批量挂。
2. 卡片 `source_ids` 追加 `SRC-006x`；正文加可见引用（推荐 `[[SRC-0062-PG21534-textiles-and-clothing]]` wikilink 或明确“book_fact: … 章/段/行”），确保 source-audit/P5 可见率口径可计。
3. **不改 `evidence_status`**；书源只作 book_fact 补充。若卡片当前仅靠书源（如 GAR-0079 kirtle），仍保持 interpretive，除非另找独立来源。
4. 改后运行 `python3 scripts/validate.py`（source_ids 可解析）与 `python3 scripts/build_sources.py --check`；如新增 source 行需同步 `reports/SOURCES.csv`。
5. 保留 `page UNCONFIRMED` 字样，不要编造页码；引用须带 PG 编号 + 章/段/行。

## 7. 限制与未完成

- 仅深化 5 本；其余 4 本（33020/56978/76717/49559）按背景处理（理由见 §5）。
- 部分候选为“部分支撑”，未纳入可加清单；宁可少加，不为降低 isolate 数硬连。
- 未做全量 224 卡 × 5 书机器匹配；本报告 25 组候选为人工回读原文确认，其余未匹配项未逐一枚举。
- 书为 1847–1919 旧著，年代/文化判断需现代研究校正；book_fact 一律不升级 verified。

## 8. 复现

```bash
# locator 复核（PG 文本；页码不可得，只用章/段/行）
python3 scripts/books_extract.py --search "The kirtle or petticoat is in reality"
# 结构校验
python3 scripts/validate.py && python3 scripts/build_sources.py --check
```

## 9. 已应用（lead 批准，2026-11-05 10:27）

- **已应用 18 张卡 / 19 组证据**（§2 直接支撑全部落地）：`source_ids` 追加 SRC-0061..0069 对应书源；正文 `## 来源链接` 增加可见 `[[SRC-...]]` 链接 + `book_fact` 章/段/行说明；同步增加 `claim_supported_by` relations（evidence=verified；GAR-0079 因卡本身 interpretive 用 evidence=interpretive）。
- **未改** `evidence_status`、未改正文事实；**GAR-0079 仍为 interpretive**（书源不升级）。
- 备份：`11-验收/P5D/backup-20261105-102725/`（18 卡原文 + manifest.json）。
- 台账：`11-验收/P5D/book-source-application.csv`（19 行，old/new source_ids、locator、relation/visible link、evidence_status_after）。
- 校验：`validate.py` **PASS 458/458**；`build_sources.py` **PASS 234/234**；`relation_consistency.py` **relations=284, errors=0**。
- **未应用（按指示保留 candidate）**：§3 的 6 组部分支撑（GAR-0007/STR-0012/STR-0023/STR-0008/STY-0010/STR-0029）与 §4 的 5 组无匹配/语义错配（GAR-0038/GAR-0059/GAR-0002/GAR-0045/文学引文段）。若要再推进，需先改断言或另找独立来源。

---

## 10. isolates 口径更新（P5-D 应用后，2026-11-05 10:40）

- 应用 5 本已 connected 书籍后，`11-验收/P5C/isolates.csv` 从 **64 → 有效 59**：移除 SRC-0061/0062/0064/0066/0069；保留 4 本背景书（SRC-0063/0065/0067/0068）与其他 55 条，**分类不变**。
- 分布：legit_reference 33 / future_topic 14 / evidence_missing_expression 11 / no_verifiable_relation 1。
- 与 source-audit 一致：whitelist 234、connected **172**、needs-citation **4**；本轮无卡片改动。


## 11. 最终应用口径（MISLINK 清理后）

- 应用记录 18 卡 / 19 组；**最终有效 17 卡 / 18 book claims**（GAR-0033→SRC-0066 仅 1908 术语、不支持 1940s，已移除）。
- 5 本 connected（0061/0062/0064/0066/0069），4 本背景（0063/0065/0067/0068）；page UNCONFIRMED；未改 evidence_status。
