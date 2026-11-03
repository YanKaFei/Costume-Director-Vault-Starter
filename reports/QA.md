# QA 独立验收报告 — Costume Director Knowledge System

- 验收人：`verifier`（task-6，独立于构建者；不修改卡片、他人工件、`00-系统/`）
- 验收时间：2026-11-04 01:34–01:46（Asia/Shanghai）
- 环境：macOS，Python 3.9.6，PyYAML 6.0.3；网络可用（抽查 URL 全部 HTTP 200）；无 Obsidian GUI
- **最终快照**：235 张卡（内容卡 93 + 来源卡 142）；最新写入卡 `SCN-0004` @ 2026-11-04 01:37:20；数据字典 v1.1 @ 01:38:14；验收 SUMMARY 重跑 @ 01:38:16 → 快照不陈旧
- 本次新增：`scripts/validate.py`、`scripts/build_sources.py`、`reports/EVIDENCE-SPOTCHECK.csv`、本报告与 `reports/COVERAGE.md`、`reports/STATUS.md`；重建了 `reports/SOURCES.csv`

## 0. 结论摘要

| # | 验收项 | 结论 | 依据 |
|---|---|---|---|
| 1 | YAML frontmatter（解析 + 扁平） | **PASS** | 235/235 可解析、235/235 无嵌套 |
| 2 | 必填字段（数据字典 v1.1 分型规则） | **PASS** | 235/235（内容卡按 §3.1+§3.2，来源卡按 §3.1+§4.9） |
| 3 | 枚举值 | **PARTIAL** | 186/235；49 张 researcher 来源卡 `source_kind` 使用字典外扩展标签（见 §1.3） |
| 4 | ID 唯一 / 格式 / 文件名 | **PASS** | 0 重复、235/235 前缀与 type 匹配、235/235 文件名以 id 开头 |
| 5 | wikilink 可达 | **PASS** | 609/609 双链目标存在，0 坏链 |
| 6 | source_ids 可解析 | **PASS** | 内容卡 126 条引用全部解析到 `04-来源/` 卡 |
| 7 | verified ⇒ 有来源 | **PASS** | 218/218 张 verified 卡（76 内容 + 142 来源）满足 v1.1 证据规则 |
| 8 | 无本地内嵌图片 | **PASS** | Vault 内 0 个图片文件、0 条本地图片引用；图片一律只存 URL |
| 9 | 正文小节（内容卡 8 节 / 来源卡 §4.9） | **PASS** | 235/235 |
| 10 | `reports/SOURCES.csv` 与来源卡一致 | **PASS** | 重建后 142/142 行一致；3 组重复 URL（警告，见 §2.3） |
| 11 | 证据独立抽查（curl） | **PARTIAL** | 14 张卡 / 19 个卡-来源对：18 PASS、1 PARTIAL（GAR-0034 一条从属断言扩写） |
| 12 | P2 检索/推荐/18 例验收复跑 | **PASS** | `run_acceptance.py` exit 0，PASS 18/18，FAIL 0/18，23.16s |
| 13 | 输出无编造 ID / 来源 | **PASS** | 36 个 raw JSON + 18 个结果 MD 中 0 个未知卡 ID、0 个坏 SRC、0 个 URL 不匹配 |
| 14 | `query.py` 检索接口 | **PARTIAL** | 单词/字段过滤可用；**引号多词查询恒 0 命中**；18 例验收的 query 步骤全部 0 命中（见 §4.3） |
| 15 | Obsidian 本地打开与跳转 | **NOT_TESTED** | 环境无 Obsidian GUI，无法实测 |
| 16 | 逐图版权授权核验 | **NOT_TESTED** | 仅验证「不内嵌图片」；未逐张核对图片授权（不下载、不嵌入策略已由结构检查覆盖） |

## 1. `scripts/validate.py` — 全库结构校验

### 1.1 命令与实际退出码

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
python3 scripts/validate.py          # exit 1（49 个枚举错误级失败）
python3 scripts/validate.py --json   # exit 1（同上，JSON 摘要）
```

实现要点：仅用标准库 + PyYAML；离线运行，不访问网络；按数据字典 v1.1 分型规则校验；错误级失败时退出码非 0；警告级（tags 规范、字段类型、来源卡可选 `source_ids`）只记录、不影响退出码。

### 1.2 逐项结果（最终快照 235 卡 / 142 来源卡）

| 检查项 | 结果 | 通过/总数 |
|---|---|---|
| 1. frontmatter 可解析为 YAML dict | PASS | 235/235 |
| 2. frontmatter 扁平（无嵌套） | PASS | 235/235 |
| 3. 必填字段（§3.1 通用 + §3.2 内容类型 / §4.9 来源卡） | PASS | 235/235 |
| 4. 枚举值合法 | **FAIL** | 186/235 |
| 5. id 格式且前缀与 type 匹配 | PASS | 235/235 |
| 6. id 全局唯一 | PASS | 235/235 |
| 7. 文件名以 `id-` 开头 | PASS | 235/235 |
| 8. `[[wikilink]]` 目标存在 | PASS | 235/235（609 条链接） |
| 9. source_ids 均解析到 `04-来源/` | PASS | 235/235（126 条引用） |
| 10. verified ⇒ 证据可解析 | PASS | 218/218 |
| 11. `date_accessed` 为 YYYY-MM-DD | PASS | 142/142 |
| 12. 正文小节（内容卡 8 节 / 来源卡 §4.9） | PASS | 235/235 |
| 13. verified 卡 `## 来源链接` 提及全部 source_ids | PASS | 76/76 |
| 14. 无本地内嵌图片 | PASS | 235/235 |
| 15. 来源卡 url 为 http(s)、§4.9 字段非空且记录 HTTP | PASS | 142/142 |
| 16. tags 小写/下划线（警告级） | PASS | 235/235 |
| 17. 字段类型 list[string]/string（警告级） | WARN | 232/235 |

跳过的非卡片 `.md`（无 frontmatter）：`04-来源/README.md`、`04-来源/验证记录.md`（按设计，不计失败）。

汇总：**错误级失败 49 项（仅枚举）＋警告 3 项**；退出码 1（有错误级失败时的预期行为）。

### 1.3 唯一错误级问题：49 张来源卡的 `source_kind` 枚举越界

数据字典 v1.1 §4.9 仍只允许 `museum_collection / academic_reference / vocabulary / industry_framework / image_repository / dataset / reference_work / other` 8 个值；researcher 的 `SRC-0001..0060` 使用了 10 个扩展标签：

| 非法值 | 卡数 | 建议映射（供 researcher/architect 决定，未擅自改卡） |
|---|---|---|
| `controlled_vocabulary` | 19 | `vocabulary` |
| `museum_object_record` | 11 | `museum_collection` |
| `institutional_blog` | 6 | `other`（或字典新增该值） |
| `garment_analysis` | 4 | `reference_work` |
| `ontology_dataset` | 2 | `dataset` |
| `professional_guild` | 2 | `industry_framework` |
| `scholarly_society` | 2 | `other` |
| `license_document` | 1 | `other` |
| `thematic_essay` | 1 | `academic_reference` |
| `exhibition_page` | 1 | `other` |

影响：仅 `SRC-0001..0060`（60 张 researcher 来源卡）中的 49 张；82 张内容型来源卡与全部 93 张内容卡枚举合法。两条可选修复路径：(a) 字典 v1.2 扩充枚举；(b) 归一化这 49 张来源卡的 `source_kind`。**本轮只记录，不改卡。**

### 1.4 其它说明

- 校验脚本离线运行，无法验证「来源页 HTTP 200」；该点由来源卡 `note` 记录 + 本轮 curl 抽查（§3）覆盖。
- 数据字典 §11 要求字典变更同步 `00-系统/卡片模板.md`：模板 mtime 为 01:26:06，早于字典 v1.1（01:38:14），模板的来源卡部分仍是 v1.0 写法（要求 `category/subcategory/...` 与 8 节）。属文档不一致，记入 §6。`00-系统/` 不属本 worker 写权限。

## 2. `scripts/build_sources.py` — SOURCES.csv 生成与对账

### 2.1 命令、退出码与结论

```bash
python3 scripts/build_sources.py --check   # 重建前：exit 1（CSV 仅 60 行，缺 82 行）
python3 scripts/build_sources.py --write   # 重建：exit 0
python3 scripts/build_sources.py --check   # 重建后：exit 0
```

| 阶段 | 来源卡 | CSV 行数 | 表头契约 | 覆盖差异 | 字段差异 | 重复 SRC ID | 重复 URL | 退出码 |
|---|---|---|---|---|---|---|---|---|
| 重建前 | 142 | 60 | 通过 | 缺 82 行 | 0 | 0 | 3 组 | 1 |
| 重建后 | 142 | 142 | 通过 | 0 | 0 | 0 | 3 组（警告） | 0 |

- **表头**：`source_id,title,publisher,url,accessed_at,source_kind,rights_statement,note`（**8 列**）。
  - ⚠️ 任务简报提到「exact 7-column header」，但项目权威规范 `00-系统/来源规范.md` §6 与既有 60 行 CSV 均为 **8 列**（`note` 为第 8 列）。本实现按规范保持 8 列；若确需 7 列请明确删除哪一列，否则会破坏研究者的既有约定。
- `title` 对 82 张无 `title` 字段的来源卡回退到 `name_zh`（v1.1 中 `title` 为可选字段）。
- CSV 由 `04-来源/*.md` 单源生成，`04-来源/README.md` 要求「CSV 与卡片同源、不得手改一方」，重建后二者一致。

### 2.2 来源卡与引用覆盖

- 来源卡 142 张；内容卡共引用 126 次、**83 张被引用**、**59 张未被任何内容卡引用**（41.5%）。
- 被引用率为 0 的重点来源包括：**全部 19 张 Getty AAT 来源卡**（`SRC-0004/0005/0006/0007/0008/0009/0010/0011/0012/0013/0014/0051..0058`）、多数 FIT 个案卡与 Met 对象卡。researcher 的来源包（尤其 AAT 术语）已建成但未接入 verified 内容卡；内容卡引用集中在 `SRC-0100+`。这是「来源 ↔ 卡片」的证据链缺口，不是坏链（坏链为 0）。
- 平均每张 verified 内容卡挂 1.33 个来源。

### 2.3 重复 URL 对账（3 组，均为同页重复登记）

| 归一化 URL | 重复来源卡 | 引用计数 | 对账建议 |
|---|---|---|---|
| `fashionhistory.fitnyc.edu/1950-1959` | `SRC-0115`（architect）、`SRC-0157`（narrator） | 1 / 1 | 同页两个 ID 各被 1 张卡引用；二选一后需同步改 2 张卡，或保留但登记为「重复登记」 |
| `www.screenireland.ie/.../Booklet_5_-_Costume_Department_2024.pdf` | `SRC-0036`、`SRC-0175` | 2 / 0 | 建议以 `SRC-0036` 为准，`SRC-0175` 未引用可退休 |
| `fashionhistory.fitnyc.edu/late-byzantine-silk-damask-dress` | `SRC-0022`、`SRC-0163` | 1 / 0 | 建议以 `SRC-0022` 为准，`SRC-0163` 未引用可退休 |

- **重复 SRC ID：0**（全库唯一）。
- SRC 编号缺口（信息级）：`SRC-0164` 缺失；`SRC-0061..0099`、`SRC-0176..0199` 为段位预留空档。连续段：0001..0060(60)、0100..0163(64)、0165..0175(11)、0200..0206(7)。

### 2.4 来源卡文件改名（未提交，提示 lead）

`04-来源/SRC-0204-V&A-1930年代男式西装.md` 已改名为 `SRC-0204-V&A-1940年代男式西装.md`（对象实为 1940–49），git 状态为「旧名 deleted + 新名 untracked」。卡片存在、id/url 正确，非丢卡；由 lead 在版本收口时处理。

## 3. 证据独立抽查（curl 实测 + 原文比对）

### 3.1 方法

- 抽查 14 张卡（12 张内容卡 + 2 张来源卡），覆盖：单品（含要求的 GAR-0031 旗袍 / GAR-0032 长衫 / GAR-0033 西装）、Met 馆藏、Getty AAT、年代卡、Look 卡、场景卡。
- 逐条命令：`curl -sS -m 10 -L -o <tmp> -w '%{http_code} %{size_download} %{content_type}' <url>`，记录状态码与返回体；HTML 去标签、JSON 直读；Screen Ireland PDF 用 macOS PDFKit 提取文本。
- 共实测 21 个 URL（抽查表 19 对引用其中 17 个；另附 FIT 1950s、doublet、AAT coats 等辅助核对）：**21/21 HTTP 200**。
- 逐条原文引用、匹配结论与命令见 `reports/EVIDENCE-SPOTCHECK.csv`（19 个卡-来源对）。

### 3.2 结果

| 卡片 | 来源 | HTTP | 结论 | 页面支撑要点（原文摘要） |
|---|---|---|---|---|
| GAR-0031 旗袍 | SRC-0200 V&A O1151302 | 200 | PASS | 「Full length garment. Right side fastening with ten loop and knot buttons (four at the neck). High stiff stand-up collar. Short sleeves … Slit at sides. Cream silk twill lining with applied lace. White synthetic cut velvet on a crepe ground … burn-out (devoré)」；「Coming into vogue as the new Chinese republic was founded in 1911 … retained the basic form of the dress of the 'Banner people', the Manchus」 |
| GAR-0031 旗袍 | SRC-0201 V&A O107537 | 200 | PASS | 「small stand-up collar and long and tight sleeves … slits at both sides about 30cm long … lined throughout with cream fur」；「hidden zip in the side seam … two loop and knot buttons」 |
| GAR-0032 长衫 | SRC-0202 V&A O80590 | 200 | PASS | 「right side fastening with five loop and knot buttons, a small stand-up collar, long and tight sleeves, straight cuffs, and slits at both sides … hidden pocket on the inner flap. The robe is unlined」；「Across the shoulder width: 149cm」「Overall length … 133cm」；「made of luo … cherished by scholars and urban elites」 |
| GAR-0033 西装 | SRC-0204 V&A O110441 | 200 | PASS | 「jacket and trousers in brown herringbone tweed lined with sateen … 1940-1949」；「lounge suit with its generous cut and wide trousers was the most popular form of daywear … waistcoats were often omitted due to rationing」 |
| GAR-0033 西装 | SRC-0155 FIT 1930s | 200 | PASS | 「suits were still worn for formal occasions and work, casual wear such as knitted sweaters and soft-collared shirts became increasingly popular during the day」 |
| GAR-0034 针织背心 | SRC-0203 V&A O235319 | 200 | PASS | 「Man's woollen jersey knit vest, made by Meridian, England, 1930s」；「Waist … 76cm … Chest … 78cm … Nape hem length: 70cm」 |
| GAR-0034 针织背心 | SRC-0155 FIT 1930s | 200 | **PARTIAL** | 页面只有「sweaters or sweater vests were worn over collared cotton shirts」与正式场合「waistcoats and vests」清单；**未出现「传统 waistcoat/vest 在 1930 年代减少」**。卡片 `## 来源链接` 中该从属断言属扩写（主证据 V&A 成立，故卡片整体不判 FAIL） |
| GAR-0035 女式皮鞋 | SRC-0205 V&A O350849 | 200 | PASS | 「black lace overlay shoes, flat pumps, with pink and green small sequins, by Benefit, Great Britain, 1930s」；页面确未载鞋跟高度 |
| GAR-0035 女式皮鞋 | SRC-0206 V&A O350850 | 200 | PASS | 「evening shoes, red and silver floral brocade, with silver buckle front detail, by Debonair, Great Britain, 1930s」 |
| GAR-0001 和服 | SRC-0100 Met API 125953 | 200 | PASS | JSON：`Kimono / 19th century / silk / Japan / 170.5 × 122.2 cm / Main dress-Womenswear / C.I.53.22.10 / isPublicDomain: true` |
| STR-0001 美第奇领 | SRC-0101 FIT | 200 | PASS | 「large, decorative frame around the sides and back of a woman's head … worn with a gown with a décolleté neckline … Supported by wire or heavy starch … late sixteenth and early seventeenth century … Marie de' Medici introducing the Medici collar」 |
| MAT-0002 尚蒂伊蕾丝 | SRC-0141 FIT | 200 | PASS | 「a French style that flourished in the mid-eighteenth century … usually made in black silk thread」；「Half stitch pattern areas. Thick gimp outline … two styles of hexagonal ground」 |
| PRD-0004 1920s | SRC-0154 FIT | 200 | PASS | 「tubular 'la garçonne' look … flapper … dropped waist and creeping hemlines … sportswear worn as daywear … cut their hair into a bob … beadwork, sequins, and embroidery … democratization of fashion」 |
| STY-0005 黑色电影 | SRC-0156 FIT 1940s | 200 | PASS | 「clothing styles were dictated by rationing and Utility clothing … padded shoulders, a nipped-in waist … suits were quite boxy」；卡片显式声明 noir 类型定义无逐条可核验来源、相关断言标 interpretive，**证据范围标注正确** |
| SCN-0003 1977 银禧河船 | SRC-0165 FIT 1977 | 200 | PASS | 「hired a boat to travel down the River Thames … boarded by the police. McLaren was arrested」；「the summer of 1977 became known as 'the Summer of Hate'」 |
| LOOK-0006 朋克青年 | SRC-0159 FIT 1970s | 200 | PASS | 「shop Seditionaries … tight black pants, leather jackets and Doctor Marten boots … slashed and ripped, embellished with safety pins, zips and studs」 |
| LOOK-0006 朋克青年 | SRC-0173 Met API 185220 | 200 | PASS | JSON：`"God Save the Queen" T-shirt / 1977 / cotton / British / isPublicDomain: false` |
| SRC-0100（来源卡自身） | Met API 125953 | 200 | PASS | 对象与来源卡描述一致 |
| SRC-0004（Getty AAT 来源卡） | AAT 300046159 | 200 | PASS | 「Main garments for women, children, or infants consisting of a bodice and skirt made in one or more pieces.」；**但该来源卡未被任何内容卡引用**（见 §2.2） |

### 3.3 抽查结论

- 14 张抽查卡中 **13 张 PASS、1 张 PARTIAL**（GAR-0034 的 FIT 从属断言扩写）；**0 张 FAIL**。
- 未发现伪造馆藏编号、伪造 URL、来源与断言无关的情况；V&A/Met/FIT 页面内容与卡片核心断言逐条对应。
- 未能核验的边界：Screen Ireland PDF（`SRC-0036/0175`）为二进制 PDF，本轮用 PDFKit 提取文本核对「continuity records / story days / wet weather」等断言成立（「Knowledge of how to use schedule, continuity information and costume breakdown」「old/warm/wet weather」「Keeps and oversees all continuity records」）；但 PDF 的版面/图表本身未逐页审阅。

## 4. P2 决策闭环复跑

### 4.1 实际命令与退出码

| 命令 | 退出码 | 关键输出 |
|---|---|---|
| `python3 scripts/query.py "旗袍" --limit 3` | 0 | 3 命中：GAR-0031、GAR-0032、LOOK-0009 |
| `python3 scripts/query.py --type garment --category footwear --limit 5 --json` | 0 | 4 命中：GAR-0022/0023/0024/0035；JSON 键含 `id,path,name_zh,name_en,type,evidence_status,source_ids,snippet,score` |
| `python3 scripts/query.py "1930s 上海" --type garment --limit 6 --json` | 0 | **0 命中**（见 §4.3） |
| `python3 scripts/recommend.py 11-验收/测试输入/T01-… --json` | 0 | historical 模式，3 套 Look，A/B/C 均含单品/颜色/材质/prompt |
| `python3 scripts/recommend.py 11-验收/测试输入/T03-… --json` | 0 | continuity 模式，1 Look × 3 场次，状态（wetness/damage/dirt）锁定 |
| `python3 scripts/recommend.py 11-验收/测试输入/T05-… --json` | 0 | fictional 模式，3 套 Look，`missing_urls: []` |
| `python3 scripts/run_acceptance.py` | **0** | **PASS 18 / 18，FAIL 0 / 18**，real 23.16s（含 18×recommend + 18×query 子进程） |

### 4.2 SUMMARY.md 与实际输出一致性

- 本 worker 独立重跑 `run_acceptance.py`（exit 0），重写 `11-验收/测试结果/SUMMARY.md` 与 `raw/`。重跑前（engineer 末次 234 卡）与本轮（235 卡，`LOOK-0009` 于 01:37:20 写入）的 SUMMARY 逐行比对：差异仅为「运行时间、卡片总数 234→235、look 9→10」三处；**18 例 VERDICT、退出码、检查项全部不变**。`recommend.py` 对同一输入实测确定性输出（连续两次运行逐字节一致），raw 变化来自快照差异而非随机性。
- SUMMARY 实际值：测试数 18（≥15）、PASS 18/18、FAIL 0/18、recommend/query 退出码均 0、卡片总数 235、来源卡 142。
- 逐例结果文件 `T01..T18.md`：18 个 `**VERDICT: PASS**`、18 个「退出码：0」；`raw/` 36 个 JSON（18×2）。
- 时间戳新陈：SUMMARY 01:38:16 > 最新卡片 01:37:20 → **不陈旧**（若 SUMMARY 早于最新卡才应判 PARTIAL）。
- 可重复性补测：在写完本报告后，又以 `python3 scripts/run_acceptance.py --no-write`（不写任何文件）复跑一次，同样 **exit 0、PASS 18/18、FAIL 0/18**；确认快照稳定（01:38:20 之后无卡片写入）。
- 题外：`run_acceptance.py` 的 query 步骤只用退出码做判定，不校验命中数；见 §4.3。

### 4.3 发现：`query.py` 多词（引号）查询恒 0 命中

| 命令 | 命中 |
|---|---|
| `query.py 1930s --type garment` | 5 |
| `query.py 上海 --type garment` | 5 |
| `query.py "1930s 上海" --type garment` | **0** |
| `query.py 1930s 上海 --type garment`（不加引号） | 5 |
| `query.py "立领 shirt"`（脚本 docstring 自带示例） | **0** |

- 根因：`terms` 为 `nargs="*"`，引号包裹的多词被当作**单个含空格的 term** 做子串匹配，而空格串不会连续出现在字段文本中，导致 AND 判定失败；脚本 docstring 的示例写法因此不可用。
- 影响：① 文档示例误导；② 18 例验收的 query 子命令全部（18/18）以 `query.py 1930s 上海 --type garment --limit 6 --json` 形式调用 → 全部 0 命中，验收只记录退出码 0，检索「命中证据」实际为空（recommend.py 内部检索不受影响，T01 候选池仍真实命中 GAR-0031 等）。
- 记录为 **PARTIAL**；修复建议（由 engineer 决定）：`terms` 按空白 split（或 `--match any` 默认），并在验收中增加「query 命中数 ≥1」断言。

### 4.4 编造 ID / 来源扫描

- 扫描全部 36 个 raw JSON 与 18 个结果 MD，匹配 `GAR/STR/MAT/STY/PRD/LOOK/SCN/SRC-\d{4}`：**0 个未知内容 ID、0 个坏 SRC 引用**；recommend 输出的 `sources[].url` 与来源卡 URL **0 不匹配**；`missing_urls` 均为空。
- recommend 结构：standard/inspired/historical 用例均 3 套 Look（各含 items、prompt_image、prompt_video、risks），continuity 用例按设计为 1 Look × 多场次（T03 3 场、T17 4 场），与 §4.4「多场次连续性」要求一致。
- query JSON 契约：18 个 query raw 均为空数组（0 命中），但抽查单词查询时字段契约完整。

## 5. 与 TASK-001 §8 自动验收条件逐条对照

| §8 条件 | 结论 | 说明 |
|---|---|---|
| Obsidian 本地打开、笔记显示、`[[wikilinks]]` 可跳转 | **NOT_TESTED** | 无 Obsidian GUI；结构层面 609/609 链接目标存在 |
| 0 个 YAML 解析错误 | **PASS** | 235/235 |
| 0 个重复 ID | **PASS** | 0 |
| 0 个坏内部链接 | **PASS** | 609/609 可达；无人工例外 |
| verified 卡片均有真实来源 ID、无虚构链接/未确认图像授权 | **PASS（链接）/ NOT_TESTED（逐图授权）** | 218/218 verified 有来源；21 URL 实测 200；0 内嵌图片；未逐张核验图片许可 |
| ≥15 个剧情测试，记录真实输入/输出/理由/失败案例 | **PASS（18 例）** | 18 例真实子进程执行，PASS 18/18；query 命中为 0（§4.3），且无 FAIL 案例可记录 |
| 至少 1 个完整多场次连续性案例，同一 Look 固定属性不自相矛盾 | **PASS** | T03（3 场）、T17（4 场）：`continuity_pass=PASS`、`same_item_ids=True`、`locks_in_every_prompt=True` |
| 形成 STATUS/COVERAGE/QA/SOURCES.csv 并区分 PASS/PARTIAL/BLOCKED/NOT_TESTED | **PASS** | 本报告、COVERAGE、STATUS、SOURCES.csv（142 行） |
| 总结新增笔记数/来源数/脚本用法/未完成项/下一步 | **PASS** | 见 `reports/STATUS.md`、`reports/COVERAGE.md` |

## 6. 已知问题与不一致（只记录，不代改）

1. **49 张来源卡 `source_kind` 枚举越界**（§1.3）：需字典扩枚举或卡片归一化，二选一。
2. **`query.py` 引号多词恒 0 命中**（§4.3）：文档示例不可用、18 例 query 证据为空；engineer 修复后应重跑验收。
3. **59/142 来源卡未被任何内容卡引用**（§2.2），含全部 19 张 Getty AAT 卡；researcher 来源包与内容卡证据链未打通。
4. **3 组重复 URL**（§2.3）：其中 `SRC-0175`、`SRC-0163` 未被引用，可退休合并。
5. **GAR-0034 一条从属断言扩写**（§3.2）：`## 来源链接` 称 FIT 1930s 支撑「传统 waistcoat/vest 减少」，页面无此表述；建议删去该从属断言或改标 interpretive（本轮未改卡）。
6. **模板未同步字典 v1.1**：`00-系统/卡片模板.md`（01:26:06）早于字典 v1.1（01:38:14），来源卡部分仍是 v1.0 的强制字段/8 节写法，违反字典 §11「同步更新模板」；需 architect 处理。
7. **`00-系统/来源规范.md` 未更新**（仍为启动模板 2026-11-03）：其 §6 元数据 8 列与现状一致，但未记录 SRC 段位扩展（0200..0299）。
8. **任务简报「7 列表头」与项目规范「8 列」不一致**（§2.1）：本实现按项目规范 8 列；若确需 7 列需明确删列。
9. **Look 五要素完整度**：10 张 Look 卡均拆解为 ≥3 个具体 GAR/STR/MAT ID（无散文式 Look），但按「上装/下装或连身/外层/鞋/配饰」五槽严格计，**0/10 全五槽**（5/10 达四槽）；是否达标取决于「完整拆解」的严格程度，详见 `reports/COVERAGE.md`。
10. **37 张卡 `review_status: draft`**（全部 PRD/STY/LOOK/SCN 与 example 卡）：机器生成、未人工复核；不影响结构校验，但属人工验收缺口。
11. **SRC-0204 来源卡改名未提交**（§2.4）：旧文件名 deleted、新文件名 untracked，由 lead 版本收口。
12. **3 处列表值未加引号（数字类型）**：`STR-0004` `construction_era: [1862]`、`STR-0008` `construction_era: [1856]`、`MAT-0010` `periods: [1856]` 被 YAML 解析为 int，违反字典 §3「list[string]/字符串」；validate.py 第 17 项以警告级记录。

## 7. 限制与未测试项

- **Obsidian GUI：NOT_TESTED**（本环境无 GUI；仅确认 Markdown/YAML/wikilink 结构合规）。
- **图片版权逐图核验：NOT_TESTED**（策略层已保证 0 本地图片、0 内嵌；未下载/未嵌入，无法也无需逐图比对授权）。
- **史学方法学正确性**：本轮抽查只验证「页面内容是否支撑卡片断言」，不评估史料选择是否最优；推断性卡片（13 张 interpretive + 4 张 example）不在史实核验范围。
- **网络稳定性**：抽查时全部 200；Met 人类可读页此前有 429 限流记录（来源卡已注明以 API 为核验对象）。
- **推荐算法质量**：仅验证可运行、结构完整、ID 真实、退出码 0；未对评分权重合理性做调参评估。
- 本 worker 未运行 `git add/commit/checkout/push`；未修改任何卡片、`00-系统/`、`10-提示词模板/`、`11-验收/` 成品（仅重跑验收脚本导致其按设计重写自身产物）。

## 8. 复现命令清单

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
python3 scripts/validate.py                       # exit 1：49 个 source_kind 枚举错误
python3 scripts/validate.py --json > /tmp/validate.json
python3 scripts/build_sources.py --check          # exit 0（重建前为 exit 1，缺 82 行）
python3 scripts/build_sources.py --write          # 重建 reports/SOURCES.csv（142 行）
python3 scripts/query.py "旗袍" --limit 3
python3 scripts/query.py --type garment --category footwear --limit 5 --json
python3 scripts/recommend.py 11-验收/测试输入/T01-1930s上海知识分子-历史准确.json --json
python3 scripts/recommend.py 11-验收/测试输入/T03-现代雨夜调查者-多场次连续性.json --json
python3 scripts/recommend.py 11-验收/测试输入/T05-未来虚构城市-虚构模式.json --json
python3 scripts/run_acceptance.py                 # exit 0，PASS 18/18
# 证据抽查命令模板（19 对、21 URL，结果见 reports/EVIDENCE-SPOTCHECK.csv）
curl -sS -m 10 -L -o /tmp/ev.html -w '%{http_code}\n' https://collections.vam.ac.uk/item/O1151302/
```

## 9. 版本

- v1.0（2026-11-04，verifier/task-6）：首次独立验收；对齐数据字典 v1.1；含 validate/build_sources 脚本、SOURCES.csv 重建、14 卡证据抽查、18 例验收复跑。
