# 04-来源 — 来源包说明（Source Pack）

> 访问与验证日期：2026-11-04。本目录 SRC-0001..SRC-0060 由 researcher（task-2）建立；SRC-0100+ 由其他 worker（页面级来源卡）建立，两套编号互不冲突。

## 1. 目的与范围

- 为 P1 卡片作者提供**真实、可再次核验**的来源：术语与本体（Fashionpedia、Getty AAT）、服装史（FIT Fashion History Timeline）、博物馆实物（Met Collection API、Cleveland Museum of Art API）、服装设计实践与连续性（Costume Designers Guild、Screen Ireland）、时代/地域语境（V&A）与研究社群入口。
- 每个来源卡都记录：真实 URL、发布者、访问日期、来源类型、权利声明、许可状态、可见证据、使用限制，以及**逐条 curl 验证结果**（HTTP 状态 + 命中内容）。
- 本来源包**不下载、不嵌入任何图片**；只保存页面 URL 与元数据。

## 2. 数量与分布

- 来源卡总数：**60**（SRC-0001 – SRC-0060），全部 `evidence_status: verified`。
- 验证方式：对每个 URL 执行 `curl -sS -m 10 -L -o /tmp/src.html -w '%{http_code}' <url>`，要求 **HTTP 200**；再从响应中确认页面标题/记录标题与关键词命中（PDF 用 zlib 解压文本流核验，JSON 直接比对字段）。
- 失败链接：**0**（未通过的 URL 未写入任何来源卡；详见 `验证记录.md`）。

| source_kind | 数量 |
| --- | --- |
| academic_reference | 9 |
| dataset | 2 |
| image_repository | 5 |
| industry_framework | 4 |
| museum_collection | 12 |
| other | 8 |
| reference_work | 1 |
| vocabulary | 19 |

## 3. 来源 → 卡片主题映射

### 术语、本体与许可证据

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0001 | Fashionpedia | 单品类别、部件、属性标签；提示词与检索字段设计 |
| SRC-0002 | Fashionpedia | 部件与属性字段设计、检索标签体系 |
| SRC-0003 | Fashionpedia | 来源许可台账、CC BY 署名要求 |
| SRC-0004 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 连身类单品、术语对照、定义引用 |
| SRC-0005 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 外层单品、外衣术语、防水/御寒属性 |
| SRC-0006 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 上装单品、内衣/外衣功能、衬衫结构 |
| SRC-0007 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 下装单品、分叉下装、裤型术语 |
| SRC-0008 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 内层/束身衣、塑形结构、内衣术语 |
| SRC-0009 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 连身/传统服、日式服装、腰带（obi）结构 |
| SRC-0010 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 中层/马甲、男装三件套、上装术语 |
| SRC-0011 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 帽/头饰、配饰、头饰术语 |
| SRC-0012 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 足部单品、鞋靴术语、配饰 |
| SRC-0013 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 材质属性、丝绸、面料术语 |
| SRC-0014 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 材质/工艺、蕾丝、装饰工艺术语 |
| SRC-0051 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 下装单品、半身裙、裙摆结构 |
| SRC-0052 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 手部配饰、礼仪手套、配饰术语 |
| SRC-0053 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 围巾/披巾、颈部配饰、多功能服饰 |
| SRC-0054 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 手袋/钱包、携带物、配饰术语 |
| SRC-0055 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 足部单品、靴、鞋履术语 |
| SRC-0056 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 头饰/头巾、南亚与中东语境、配饰术语 |
| SRC-0057 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 面纱/头纱、头饰配饰、宗教与文化语境 |
| SRC-0058 | Art & Architecture Thesaurus Full Record Display (Getty Research) | 结构细节、袖型、可拆卸部件 |

### 服装史与个案分析（FIT Fashion History Timeline）

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0015 | Fashion History Timeline / A hub for fashion research | 年代/地域索引、术语入口、研究方法 |
| SRC-0016 | Dictionary / Fashion History Timeline | 术语对照、非西方服饰词、词典索引 |
| SRC-0017 | How to Research Fashion / Fashion History Timeline | 研究方法、证据流程、年代定位 |
| SRC-0018 | 1869 – Red Silk Dress / Fashion History Timeline | 19 世纪女装、bustle 结构、蕾丝/流苏装饰 |
| SRC-0019 | 1883 – Charles Frederick Worth, red silk satin and velvet dinner dress / Fashion History Timeline | 19 世纪晚装、Worth、bustle、领型与饰边 |
| SRC-0020 | 1855 – English Blue and White Print Day Dress / Fashion History Timeline | 19 世纪中女装、crinoline、印花面料、袖型 |
| SRC-0021 | Inès Gâches-Sarraute and the Straight-Front Corset / Fashion History Timeline | 束身衣史、内衣结构、1900 年代轮廓 |
| SRC-0022 | 15th century – Late Byzantine Silk Damask Dress and Taffeta Tunic / Fashion History Timeline | 拜占庭服饰、考古实物、丝织品、束腰衣 |

### 博物馆实物记录（Met Collection API / Cleveland API）

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0023 | Dress | 19 世纪中女装、博物馆实物、年代/材质证据 |
| SRC-0024 | Dress | 19 世纪末女装、棉质日装、博物馆实物 |
| SRC-0025 | Dress | 19 世纪末女装、丝质礼服、博物馆实物 |
| SRC-0026 | Corset | 束身衣、内衣结构、19 世纪末材质 |
| SRC-0027 | Wedding corset | 束身衣、婚礼服饰、博物馆实物（受限许可） |
| SRC-0028 | Kimono | 日式服装、和服、20 世纪初跨文化服饰 |
| SRC-0029 | Waistcoat | 17 世纪男装、马甲、亚麻/丝/金属材质 |
| SRC-0030 | Waistcoat | 18 世纪男装、马甲、丝/棉材质 |
| SRC-0031 | Gym suit | 运动服/专门类型、19 世纪末女装、活动性 |
| SRC-0032 | Athletic ensemble | 运动服/套装、多件式服装、19 世纪末材质 |
| SRC-0050 | Belt for a Lady's Dress | 中世纪配饰、腰带工艺、金属/珐琅材质 |

### 服装设计职业实践与剧组连续性（CDG / Screen Ireland）

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0033 | What Is Costume Design? - Costume Designers Guild, I.A.T.S.E. Local 892 | 服装设计职业定义、剧组协作、案例索引 |
| SRC-0034 | Design Details - Costume Designers Guild, I.A.T.S.E. Local 892 | 制帽/钉珠工艺、尺码与剪裁、行业实践 |
| SRC-0035 | Competency Framework - Crew / Screen Ireland | 服装部门分工、剧本拆解与连续性、行业框架 |
| SRC-0036 | Booklet 5 - Costume Department 2024 (PDF) | 服装部门角色、剧本拆解、continuity、面料动态、时期内衣 |

### 时代、地域与专题语境（V&A 博客）

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0037 | Trench coats: from real mud to Nostalgia of Mud • V&A Blog | 外层单品、防水结构、gabardine、风衣 |
| SRC-0038 | Undressed Archives • V&A Blog | 内衣史、1750 年至今、功能×时尚 |
| SRC-0039 | From Feathers to Fascinators: Part Three • V&A Blog | 制帽/羽毛工艺、礼帽、配饰 |
| SRC-0040 | Guest Post: A Warrior's Magic Shirt • V&A Blog | 南亚/中东服饰、护身衣、博物馆修复、宗教语境 |
| SRC-0041 | Guest Post: Stitch Narratives - Continuance and Evolution of Running Stitch Embroidery • V&A Blog | 刺绣工艺、南亚纺织、走针/kantha、纹样 |
| SRC-0059 | A very brief history of staying dry • V&A Blog | 防雨外层、伞/雨具、20 世纪初视觉文化 |
| SRC-0060 | Location Scout Part II: Resist block printing • V&A Blog | 纹样/印花工艺、防染与蓝染、南亚纺织 |

### 研究社群与馆藏入口（学会 / 博物馆）

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0042 | Home / Costume Society of America | 研究社群、期刊与学术资源、方法学背景 |
| SRC-0043 | The Costume Society | 研究社群、期刊、服装复原与工艺奖项 |
| SRC-0044 | Museum / The Museum at FIT | 博物馆收藏、美国时装、展陈资源 |

### 图像与许可参照（Wikimedia Commons，仅链接）

| 来源 ID | 来源（页面标题） | 可支撑的卡片主题 |
| --- | --- | --- |
| SRC-0045 | File:Wedding dress MET 69.2.26 front CP4.jpg - Wikimedia Commons | 19 世纪婚礼服视觉参照、CC0 图像来源 |
| SRC-0046 | File:Petersons walking dress 1870.jpg - Wikimedia Commons | 1870 年代女装、时尚插图、视觉参照 |
| SRC-0047 | File:Print, Plate No. 153 in Fashion Review in the Family Gazette (Revue de la Mode, Gazette de la Famille), 1874 (CH 18530117).jpg - Wikimedia Commons | 1870 年代女装、bustle、时尚版画、配饰细节 |
| SRC-0048 | File:Corset - Royal Worcester Corset Company, ca. 1890.jpg - Wikimedia Commons | 束身衣、内衣材质、1890 年代视觉参照 |
| SRC-0049 | File:Khalili Collection of Kimono KX158.jpg - Wikimedia Commons | 和服/kosode、日式纹样、视觉参照 |

### 按卡片类别的检索建议

| 卡片类别 | 优先引用来源 |
| --- | --- |
| 单品定义/类别边界（GAR） | SRC-0004..0014 与 SRC-0051..0058（AAT：dresses/coats/shirts/trousers/corsets/kimonos/waistcoats/hats/shoes/skirts/gloves/scarves/purses/boots/turbans/veils/sleeves）、SRC-0001..0003（Fashionpedia 本体）、SRC-0016（FIT 词典） |
| 结构细节（STR） | SRC-0008（corset 结构）、SRC-0010（waistcoat 层次）、SRC-0005（coat 前开/袖）、SRC-0058（sleeves 可拆卸袖史）、SRC-0018..0021（FIT 个案的领型、袖型、bustle、裙撑） |
| 材质/纹样（MAT） | SRC-0013（silk 物性）、SRC-0014（lace 工艺）、SRC-0020（印花+丝毛）、SRC-0041（kantha 走针）、SRC-0022（丝 damask/taffeta）、SRC-0060（防染/蓝染/木版印花） |
| 风格（STY） | SRC-0037（风衣/gabardine 的实用与怀旧）、SRC-0059（防雨与伞的视觉文化）、SRC-0032（运动套装）、SRC-0038（内衣的实用×感官）、SRC-0033（行业定义） |
| 时代/地域（PRD） | SRC-0015（FIT 时间线索引）、SRC-0018..0022（1860s/1880s/1850s/1900s/拜占庭）、SRC-0023..0032、SRC-0050（Met/CMA 实物）、SRC-0040（南亚/中东） |
| Look 与连续性（LOOK/SCN） | SRC-0035、SRC-0036（剧组角色、script breakdown、continuity、面料动态）、SRC-0034（制帽/钉珠工艺） |
| 图像许可与引用 | SRC-0045（CC0）、SRC-0046/0047（公有领域）、SRC-0048/0049（CC BY-SA 4.0）、SRC-0003（Fashionpedia CC BY 4.0）、SRC-0004..0014（AAT ODC-BY） |

## 4. 图像与许可政策（强制）

1. **不下载、不嵌入**：本目录的所有卡只存来源 URL 与文字元数据；Vault 内不出现来源图片文件。
2. **版权不明 => `link_only`**：FIT、CDG、Screen Ireland、V&A、CSA、The Costume Society、The Museum at FIT 的页面均只允许链接引用，`license_status: link_only`（AAT 因 ODC-BY 记 `other_permission`，并在 `rights_statement` 中写明需署名）。
3. **CC0/开放数据必须有显式证据**：只有页面/元数据明确写明的才标 `cc0` / `cc_by`：
   - Fashionpedia 本体：`data_license.html` 明文 CC BY 4.0 → `cc_by`；
   - Met 对象记录：仅当 API 字段 `isPublicDomain: true` → `cc0`（记录与公有领域图像按 Met Open Access 政策提供），`isPublicDomain: false` 的对象（SRC-0027、SRC-0028）→ `link_only`；
   - Cleveland API：`share_license_status: CC0` → `cc0`；
   - Wikimedia Commons：按 Commons API `LicenseShortName` 逐文件判定——`CC0` → `cc0`；`Public domain`（著作权已届满）→ `not_applicable` 并在 note 写明；`CC BY-SA 4.0` → `other_permission`。
4. **署名**：复用 AAT（ODC-BY）、Fashionpedia（CC BY 4.0）、Commons CC BY-SA 文件的内容时，必须保留发布者与许可；`license_status` 只是粗粒度枚举，具体条件以各卡 `rights_statement` 与原始页面为准。
5. **禁止**把 Pinterest、无来源营销图、自动生成页面当作权威来源；本包未收录此类来源。

## 5. 验证方法与网络限制

- 每条命令：`curl -sS -m 10 -L -o /tmp/src.html -w '%{http_code}' "<url>"`；记录 HTTP 状态、响应大小、页面标题与关键词命中；完整表格见 `验证记录.md`。
- 已知网络限制（本次会话实测，2026-11-04）：`www.metmuseum.org` 返回 HTTP 429（Vercel 校验），因此 Met 卡以 `collectionapi.metmuseum.org` 的 API URL 作为验证链接，官方对象页链接写在 note/正文中；Met `v1/search` 已于 2026-10-01 停用，改用 `v1.1/search`。`europeana.eu`、`id.loc.gov`、`archive.org`、`risdmuseum.org`、`api.artic.edu`、`si.edu` 在本网络下返回 403/000，均未采用。
- PDF 来源（SRC-0036）用 Python `zlib` 解压 PDF 文本流并检索关键词，确认内容含 "Costume Department Roles" 等文本。

## 6. 如何引用

- 卡片 frontmatter 的 `source_ids` 填本目录的 `SRC-XXXX`；正文用纯文本或（目标卡存在时的）wikilink 指向来源卡。
- `verified` 历史/工艺事实必须至少挂 1 个本包来源 ID；若只能在 `interpretive` 层面使用，须明确标注。
- 每个来源卡的 `note` 与 `reports/SOURCES.csv` 的 `note` 列一一对应；CSV 与卡片由同一数据源生成，不得手改其中一方。

## 7. 与 SRC-0100+ 的关系

- 本包（SRC-0001..0050）偏「机构级/术语级/实物级」来源；SRC-0100+ 为其他 worker 的页面级来源卡（如 FIT 词条页、Met 单件和服、FIT 年代页等）。
- 若同一 URL 在两处出现，以内容证据更具体者为准，并在两卡 note 中注明互见；本包不修改 0100+ 的卡片。
