# QA 独立验收报告 — Costume Director Knowledge System

- 验收人：`verifier`（task-6 首验 + task-7 修复后复验；独立于构建者，不修改卡片、他人工件、`00-系统/`）
- 本轮复验时间：2026-11-04 01:46–01:52（Asia/Shanghai）
- 环境：macOS，Python 3.9.6，PyYAML 6.0.3；网络可用（抽查 URL 全部 HTTP 200）；无 Obsidian GUI
- **最终快照**：235 张卡（内容卡 93 + 来源卡 142）；最新卡片写入 `04-来源/SRC-0157`/`06-时代地域/PRD-0007` @ 01:46:43，`GAR-0034`/`STR-0004`/`STR-0008`/`MAT-0010` @ 01:47:05，`00-系统/卡片模板.md` @ 01:47:15；验收 SUMMARY @ 01:49:29（本 worker 独立重跑）；复验期间无卡片再变更
- 修复轮次：researcher 归一化 49 张来源卡 `source_kind`；engineer 修复 `query.py` 多词检索并为验收加入 `query_hits ≥1` 断言后重跑；architect 修 GAR-0034 从属断言、3 处 YAML 数字加引号、同步卡片模板 v1.1；narrator 将 `PRD-0007` 改用 `SRC-0115` 并给 `SRC-0157` 标重复

## 0. 结论摘要

| # | 验收项 | 结论 | 依据 |
|---|---|---|---|
| 1 | YAML frontmatter（解析 + 扁平） | **PASS** | 235/235 可解析、235/235 无嵌套 |
| 2 | 必填字段（数据字典 v1.1 分型规则） | **PASS** | 235/235（内容卡 §3.1+§3.2，来源卡 §3.1+§4.9） |
| 3 | 枚举值 | **PASS** | **235/235**（修复前 49 张 `source_kind` 越界，已归一化） |
| 4 | 字段类型（list[string]/string） | **PASS** | **235/235**（修复前 3 处数字未加引号，已加引号） |
| 5 | ID 唯一 / 格式 / 文件名 | **PASS** | 0 重复、235/235 前缀与 type 匹配、235/235 文件名以 id 开头 |
| 6 | wikilink 可达 | **PASS** | 609/609 双链目标存在，0 坏链 |
| 7 | source_ids 可解析 | **PASS** | 内容卡 125 条引用全部解析到 `04-来源/` 卡 |
| 8 | verified ⇒ 有来源 | **PASS** | 218/218 张 verified 卡（76 内容 + 142 来源）满足 v1.1 证据规则 |
| 9 | 无本地内嵌图片 | **PASS** | Vault 内 0 个图片文件、0 条本地图片引用 |
| 10 | 正文小节（内容卡 8 节 / 来源卡 §4.9） | **PASS** | 235/235 |
| 11 | `reports/SOURCES.csv` 与来源卡一致 | **PASS** | 重建后 142/142 行一致；3 组重复 URL 已标 canonical（见 §2.3） |
| 12 | 证据独立抽查（curl） | **PASS** | 14 张卡 / 19 个卡-来源对：**19/19 PASS**（GAR-0034 原 PARTIAL 已修复关闭） |
| 13 | P2 检索/推荐/18 例验收复跑 | **PASS** | `run_acceptance.py` exit 0，PASS 18/18，FAIL 0/18，21.56s；query 命中总数 53、逐例最小 1 |
| 14 | 输出无编造 ID / 来源 | **PASS** | 36 个 raw JSON + 18 个结果 MD 中 0 个未知卡 ID、0 个坏 SRC、0 个 URL 不匹配 |
| 15 | `query.py` 检索接口 | **PASS** | 多词/引号/`--phrase` 均已修复并可复现（见 §4.3） |
| 16 | Obsidian 本地打开与跳转 | **NOT_TESTED** | 环境无 Obsidian GUI，无法实测 |
| 17 | 逐图版权授权核验 | **NOT_TESTED** | 仅验证「不内嵌图片」，未逐张核对图片授权 |

**最终：`python3 scripts/validate.py` exit 0，17/17 检查项 PASS，0 错误级失败、0 警告。**

## 1. `scripts/validate.py` — 全库结构校验（修复后）

### 1.1 命令与实际退出码

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
python3 scripts/validate.py          # exit 0（0 错误级失败、0 警告）
python3 scripts/validate.py --json   # exit 0（同上，JSON 摘要）
```

实现要点：仅用标准库 + PyYAML；离线运行，不访问网络；按数据字典 v1.1 分型规则校验；错误级失败时退出码非 0，警告级（tags 规范、字段类型）只记录。

### 1.2 逐项结果（最终快照 235 卡 / 142 来源卡）

| 检查项 | 结果 | 通过/总数 |
|---|---|---|
| 1. frontmatter 可解析为 YAML dict | PASS | 235/235 |
| 2. frontmatter 扁平（无嵌套） | PASS | 235/235 |
| 3. 必填字段（§3.1 通用 + §3.2 内容类型 / §4.9 来源卡） | PASS | 235/235 |
| 4. 枚举值合法（type/category/evidence/review/license/source_kind/属性枚举） | **PASS** | **235/235** |
| 5. id 格式且前缀与 type 匹配 | PASS | 235/235 |
| 6. id 全局唯一 | PASS | 235/235 |
| 7. 文件名以 `id-` 开头 | PASS | 235/235 |
| 8. `[[wikilink]]` 目标存在 | PASS | 235/235（609 条链接） |
| 9. source_ids 均解析到 `04-来源/` | PASS | 235/235（125 条引用） |
| 10. verified ⇒ 证据可解析 | PASS | 218/218 |
| 11. `date_accessed` 为 YYYY-MM-DD | PASS | 142/142 |
| 12. 正文小节（内容卡 8 节 / 来源卡 §4.9） | PASS | 235/235 |
| 13. verified 卡 `## 来源链接` 提及全部 source_ids | PASS | 76/76 |
| 14. 无本地内嵌图片 | PASS | 235/235 |
| 15. 来源卡 url 为 http(s)、§4.9 字段非空且记录 HTTP | PASS | 142/142 |
| 16. tags 小写/下划线（警告级） | PASS | 235/235 |
| 17. 字段类型 list[string]/string（警告级） | **PASS** | **235/235** |

跳过的非卡片 `.md`（无 frontmatter）：`04-来源/README.md`、`04-来源/验证记录.md`（按设计，不计失败）。
汇总：**错误级失败 0；警告 0；RESULT: PASS**。

### 1.3 修复验证：`source_kind` 归一化（原 49 项错误 → 0）

researcher 已把 `SRC-0001..0060` 中的 49 张越界值归一化；现全库 `source_kind` 分布（全部在字典 v1.1 §4.9 枚举内）：

| source_kind | 卡数 |
|---|---|
| academic_reference | 78 |
| museum_collection | 24 |
| vocabulary | 19 |
| other | 8 |
| industry_framework | 5 |
| image_repository | 5 |
| dataset | 2 |
| reference_work | 1 |
| **合计** | **142** |

### 1.4 修复验证：YAML 数字加引号与模板同步

- `STR-0004` `construction_era: ['1824-1836','1862','1890-1896','1960-1980']`、`STR-0008` `construction_era: ['1856','1860s']`、`MAT-0010` `periods: ['1856','1870s','late_19th_century']` —— 已加引号，第 17 项警告清零。
- `00-系统/卡片模板.md` @ 01:47:15 已按字典 v1.1 改写来源卡部分（明确豁免 `category/.../source_ids` 与 8 节，给出研究型/内容型正文），与字典 §3.1/§4.9/§9 一致。
- `00-系统/数据字典.md` 仍为 v1.1（01:38:14）；`00-系统/来源规范.md` 仍为启动模板（2026-11-03），未记录 SRC-0200..0299 段位（见 §6）。

## 2. `scripts/build_sources.py` — SOURCES.csv 生成与对账（修复后）

### 2.1 命令、退出码与结论

```bash
python3 scripts/build_sources.py --check   # 修复期间研究员已重生成 60 行 CSV → exit 1（缺 82 行）
python3 scripts/build_sources.py --write   # 从 142 张来源卡重建 → exit 0
python3 scripts/build_sources.py --check   # 重建后 → exit 0
```

| 阶段 | 来源卡 | CSV 行数 | 表头契约 | 覆盖差异 | 字段差异 | 重复 SRC ID | 重复 URL | 退出码 |
|---|---|---|---|---|---|---|---|---|
| 修复期（researcher 重生成） | 142 | 60 | 通过 | 缺 82 行 | 0 | 0 | 3 组 | 1 |
| 本轮重建后 | 142 | 142 | 通过 | 0 | 0 | 0 | 3 组（已标 canonical） | 0 |

- **表头**：`source_id,title,publisher,url,accessed_at,source_kind,rights_statement,note`（**8 列**，与 `00-系统/来源规范.md` §6 一致；任务简报「7 列」与规范冲突，按规范执行）。
- `title` 对 82 张无 `title` 字段的来源卡回退到 `name_zh`（v1.1 中 `title` 可选）。
- 本轮为 `build_sources.py` 增加 canonical 识别：从来源卡 `note` 中解析 `canonical ... SRC-xxxx` 并在重复 URL 清单中显示。

### 2.2 来源卡与引用覆盖（修复后）

- 来源卡 142 张；内容卡共引用 125 次、**82 张被引用**、**60 张未被任何内容卡引用**（42.3%）。
- 未被引用者包含**全部 19 张 Getty AAT 来源卡**（`SRC-0004/0005/0006/0007/0008/0009/0010/0011/0012/0013/0014/0051..0058`）与多数 FIT 个案/Met 对象卡；researcher 来源包仍未被内容卡证据链充分吸收。
- `SRC-0157` 因 `PRD-0007` 改用 canonical `SRC-0115`，由上一轮的「1 次引用」变为未引用。
- 平均每张 verified 内容卡引用 1.32 个来源（76 张）。

### 2.3 重复 URL 对账（3 组，均已标 canonical）

| 归一化 URL | 重复来源卡 | 引用计数 | canonical | 处理状态 |
|---|---|---|---|---|
| `fashionhistory.fitnyc.edu/1950-1959` | `SRC-0115`、`SRC-0157` | 2 / 0 | **SRC-0115** | narrator 已将 `PRD-0007` 改用 `SRC-0115`；`SRC-0157` note 标注「canonical 为 SRC-0115，保留作重复交叉引用」 |
| `fashionhistory.fitnyc.edu/late-byzantine-silk-damask-dress` | `SRC-0022`、`SRC-0163` | 1 / 0 | **SRC-0022** | `SRC-0163` note 标注 canonical=SRC-0022（重复交叉引用） |
| `www.screenireland.ie/.../Booklet_5_-_Costume_Department_2024.pdf` | `SRC-0036`、`SRC-0175` | 2 / 0 | **SRC-0036** | `SRC-0175` note 标注 canonical=SRC-0036（重复交叉引用） |

- 3 组重复均为「同一页面登记两张卡」，已通过 canonical 标注去重语义；是否物理删除重复卡由 lead 决定（本轮不动卡片）。
- **重复 SRC ID：0**；SRC 编号缺口：`SRC-0164` 缺失；`SRC-0061..0099`、`SRC-0176..0199` 为段位预留。连续段：0001..0060(60)、0100..0163(64)、0165..0175(11)、0200..0206(7)。
- `04-来源/SRC-0204-V&A-1930年代男式西装.md` 已改名 `SRC-0204-V&A-1940年代男式西装.md`（对象实为 1940–49），git 仍为「旧名 deleted + 新名 untracked」，待 lead 版本收口。

## 3. 证据独立抽查（curl 实测 + 原文比对）

### 3.1 方法

- 抽查 14 张卡（12 张内容卡 + 2 张来源卡），覆盖：单品（含要求的 GAR-0031 旗袍 / GAR-0032 长衫 / GAR-0033 西装）、Met 馆藏、Getty AAT、年代卡、Look 卡、场景卡。
- 命令：`curl -sS -m 10 -L -o <tmp> -w '%{http_code} %{size_download} %{content_type}' <url>`；HTML 去标签、JSON 直读；Screen Ireland PDF 用 macOS PDFKit 提取文本。
- 首轮实测 21 个 URL 全部 HTTP 200；修复轮对关键修复对象复测 4 个 URL（V&A O235319、FIT 1950-1959、Screen Ireland PDF、Getty AAT 300046159）**全部 200**。
- 逐条原文引用、结论与命令见 `reports/EVIDENCE-SPOTCHECK.csv`（19 个卡-来源对，现 **19/19 PASS**）。

### 3.2 结果（修复后）

| 卡片 | 来源 | HTTP | 结论 | 页面支撑要点（原文摘要） |
|---|---|---|---|---|
| GAR-0031 旗袍 | SRC-0200 V&A O1151302 | 200 | PASS | 「Full length garment. Right side fastening with ten loop and knot buttons (four at the neck). High stiff stand-up collar. Short sleeves … Slit at sides. Cream silk twill lining with applied lace. White synthetic cut velvet on a crepe ground … burn-out (devoré)」；「Coming into vogue as the new Chinese republic was founded in 1911 … retained the basic form of the dress of the 'Banner people', the Manchus」 |
| GAR-0031 旗袍 | SRC-0201 V&A O107537 | 200 | PASS | 「small stand-up collar and long and tight sleeves … slits at both sides about 30cm long … lined throughout with cream fur」；「hidden zip in the side seam … two loop and knot buttons」 |
| GAR-0032 长衫 | SRC-0202 V&A O80590 | 200 | PASS | 「right side fastening with five loop and knot buttons, a small stand-up collar, long and tight sleeves, straight cuffs, and slits at both sides … hidden pocket on the inner flap. The robe is unlined」；「Across the shoulder width: 149cm」「Overall length … 133cm」；「made of luo … cherished by scholars and urban elites」 |
| GAR-0033 西装 | SRC-0204 V&A O110441 | 200 | PASS | 「jacket and trousers in brown herringbone tweed lined with sateen … 1940-1949」；「lounge suit with its generous cut and wide trousers was the most popular form of daywear … waistcoats were often omitted due to rationing」 |
| GAR-0033 西装 | SRC-0155 FIT 1930s | 200 | PASS | 「suits were still worn for formal occasions and work, casual wear such as knitted sweaters and soft-collared shirts became increasingly popular during the day」 |
| GAR-0034 针织背心 | SRC-0203 V&A O235319 | 200 | PASS（本轮复测 200） | 「Man's woollen jersey knit vest, made by Meridian, England, 1930s」；「Waist … 76cm … Chest … 78cm … Nape hem length: 70cm」 |
| GAR-0034 针织背心 | SRC-0155 FIT 1930s | 200 | **PASS（已修复）** | 原 PARTIAL：卡片曾称 FIT 支撑「传统 waistcoat/vest 在 1930s 减少」，页面无此表述。architect 已删去该从属断言，`source_ids` 改为 `[SRC-0203]`，并在 `## 来源链接` 明示「上海/民国搭配与‘休闲层取代正装马甲’叙事均为 interpretive」→ 本轮复核通过 |
| GAR-0035 女式皮鞋 | SRC-0205 V&A O350849 | 200 | PASS | 「black lace overlay shoes, flat pumps, with pink and green small sequins, by Benefit, Great Britain, 1930s」；页面确未载鞋跟高度 |
| GAR-0035 女式皮鞋 | SRC-0206 V&A O350850 | 200 | PASS | 「evening shoes, red and silver floral brocade, with silver buckle front detail, by Debonair, Great Britain, 1930s」 |
| GAR-0001 和服 | SRC-0100 Met API 125953 | 200 | PASS | JSON：`Kimono / 19th century / silk / Japan / 170.5 × 122.2 cm / Main dress-Womenswear / C.I.53.22.10 / isPublicDomain: true` |
| STR-0001 美第奇领 | SRC-0101 FIT | 200 | PASS | 「large, decorative frame around the sides and back of a woman's head … worn with a gown with a décolleté neckline … Supported by wire or heavy starch … late sixteenth and early seventeenth century … Marie de' Medici introducing the Medici collar」 |
| MAT-0002 尚蒂伊蕾丝 | SRC-0141 FIT | 200 | PASS | 「a French style that flourished in the mid-eighteenth century … usually made in black silk thread」；「Half stitch pattern areas. Thick gimp outline … two styles of hexagonal ground」 |
| PRD-0004 1920s | SRC-0154 FIT | 200 | PASS | 「tubular 'la garçonne' look … flapper … dropped waist and creeping hemlines … sportswear worn as daywear … cut their hair into a bob … beadwork, sequins, and embroidery … democratization of fashion」 |
| STY-0005 黑色电影 | SRC-0156 FIT 1940s | 200 | PASS | 「clothing styles were dictated by rationing and Utility clothing … padded shoulders, a nipped-in waist … suits were quite boxy」；卡片显式声明 noir 类型定义无逐条可核验来源、相关断言标 interpretive |
| SCN-0003 1977 银禧河船 | SRC-0165 FIT 1977 | 200 | PASS | 「hired a boat to travel down the River Thames … boarded by the police. McLaren was arrested」；「the summer of 1977 became known as 'the Summer of Hate'」 |
| LOOK-0006 朋克青年 | SRC-0159 FIT 1970s | 200 | PASS | 「shop Seditionaries … tight black pants, leather jackets and Doctor Marten boots … slashed and ripped, embellished with safety pins, zips and studs」 |
| LOOK-0006 朋克青年 | SRC-0173 Met API 185220 | 200 | PASS | JSON：`"God Save the Queen" T-shirt / 1977 / cotton / British / isPublicDomain: false` |
| SRC-0100（来源卡自身） | Met API 125953 | 200 | PASS | 对象与来源卡描述一致 |
| SRC-0004（Getty AAT 来源卡） | AAT 300046159 | 200 | PASS | 「Main garments for women, children, or infants consisting of a bodice and skirt made in one or more pieces.」；该来源卡仍未被任何内容卡引用（§2.2） |

### 3.3 抽查结论

- 14 张抽查卡、19 个卡-来源对：**19/19 PASS**；此前唯一的 GAR-0034 PARTIAL 因 architect 修复而关闭。
- 未发现伪造馆藏编号、伪造 URL、来源与断言无关；V&A/Met/FIT 页面与卡片核心断言逐条对应。
- Screen Ireland PDF（`SRC-0036/0175`）经 PDFKit 提取文本核对 `continuity records`、`schedule, continuity information and costume breakdown`、`old/warm/wet weather`、`story days` 等条目成立；PDF 版面/图表未逐页审阅。

## 4. P2 决策闭环复跑（修复后）

### 4.1 实际命令与退出码

| 命令 | 退出码 | 关键输出 |
|---|---|---|
| `python3 scripts/query.py "旗袍" --limit 3` | 0 | 3 命中：GAR-0031、GAR-0032、LOOK-0009 |
| `python3 scripts/query.py "立领 shirt" --json` | 0 | **7 命中**（修复前 0；docstring 示例现可用） |
| `python3 scripts/query.py --type garment --category footwear --json` | 0 | 4 命中：GAR-0022/0023/0024/0035；JSON 契约键完整 |
| `python3 scripts/query.py "1930s 上海" --type garment --json` | 0 | **5 命中**（修复前 0；现按空白拆分为 AND 词） |
| `python3 scripts/query.py --phrase "1930s 上海" --json` | 0 | 1 命中（`--phrase` 精确短语） |
| `python3 scripts/recommend.py T01/T03/T05 --json` | 0 | historical 3 套 / continuity 1 Look×3 场 / fictional 3 套；0 未知 ID |
| `python3 scripts/run_acceptance.py` | **0** | **PASS 18/18，FAIL 0/18**，real 21.56s；query 命中总数 53、逐例最小 1 |

### 4.2 SUMMARY.md 与实际输出一致性

- 本 worker 独立重跑 `run_acceptance.py`（exit 0，21.56s），重写 SUMMARY 与 `raw/`；与 engineer 末次（01:48:29）逐行 diff **仅运行时间不同**（18/18 PASS、query hits 53、逐例命中完全一致）。
- SUMMARY 实际值：测试数 18（≥15）、PASS 18/18、FAIL 0/18、卡片总数 235、来源卡 142、`query.py 命中总数 53`、`每个场景 query 步骤均返回 ≥1 命中：是`。
- 逐例结果 MD：18 个 `**VERDICT: PASS**`、18 个「退出码：0」、**18 个 `query_hits | PASS`**（新断言）；`raw/` 36 个 JSON（18×2）。
- 36 个 query raw JSON 命中数 `[5,2,1,6,2,1,4,4,4,1,4,5,2,1,5,2,1,3]`，最小值 1、合计 53，与 SUMMARY 一致。
- 时间戳：SUMMARY 01:49:29 > 最新卡片 01:47:05、模板 01:47:15 → **不陈旧**。
- 可重复性：`recommend.py` 对同一输入连续两次运行逐字节一致（确定性）。

### 4.3 修复验证：`query.py` 多词检索

| 场景 | 修复前 | 修复后 |
|---|---|---|
| `query.py "1930s 上海" --type garment` | 0 命中 | **5 命中**（GAR-0035/0034/0031/0032/0033） |
| `query.py "立领 shirt"`（docstring 示例） | 0 命中 | **7 命中** |
| `query.py --phrase "1930s 上海"` | 无该选项 | 1 命中（精确短语） |
| 18 例验收 query 步骤 | 18/18 均 0 命中、仅校验退出码 | **逐例 ≥1 命中**，`query_hits` 检查项 18/18 PASS |

- 实现与文档一致：positional terms 按空白拆分为 AND 词，`--phrase` 保留整段精确匹配；`run_acceptance.py` 新增 `query_hits` 检查（query exit 0 且 hits ≥1）。
- 首验发现的「引号多词恒 0 命中、验收 query 证据为空」问题**已关闭**。

### 4.4 编造 ID / 来源扫描

- 扫描全部 36 个 raw JSON 与 18 个结果 MD：**0 个未知内容 ID、0 个坏 SRC 引用**；recommend 输出 `sources[].url` 与来源卡 URL **0 不匹配**；`missing_urls` 均为空。
- recommend 结构：standard/inspired/historical 用例均 3 套 Look（含 items、prompt_image、prompt_video、risks），continuity 用例按设计为 1 Look × 多场次（T03 3 场、T17 4 场）；T03/T17 `continuity_pass=PASS`、`same_item_ids=True`、`locks_in_every_prompt=True`。
- query JSON 契约：18 例均非空且字段完整（`id,path,name_zh,name_en,type,evidence_status,source_ids,snippet,score`）。

## 5. 与 TASK-001 §8 自动验收条件逐条对照（修复后）

| §8 条件 | 结论 | 说明 |
|---|---|---|
| Obsidian 本地打开、笔记显示、`[[wikilinks]]` 可跳转 | **NOT_TESTED** | 无 Obsidian GUI；结构层面 609/609 链接目标存在 |
| 0 个 YAML 解析错误 | **PASS** | 235/235 |
| 0 个重复 ID | **PASS** | 0 |
| 0 个坏内部链接 | **PASS** | 609/609 可达；无人工例外 |
| verified 卡片均有真实来源 ID、无虚构链接/未确认图像授权 | **PASS（链接）/ NOT_TESTED（逐图授权）** | 218/218 verified 有来源；21 URL 实测 200；0 内嵌图片；未逐张核验图片许可 |
| ≥15 个剧情测试，记录真实输入/输出/理由/失败案例 | **PASS（18 例）** | 18 例真实子进程执行，PASS 18/18；query 逐例 ≥1 命中；无 FAIL 案例 |
| 至少 1 个完整多场次连续性案例，同一 Look 固定属性不自相矛盾 | **PASS** | T03（3 场）、T17（4 场）连续性检查全 PASS |
| 形成 STATUS/COVERAGE/QA/SOURCES.csv 并区分 PASS/PARTIAL/BLOCKED/NOT_TESTED | **PASS** | 本报告、COVERAGE、STATUS、SOURCES.csv（142 行） |
| 总结新增笔记数/来源数/脚本用法/未完成项/下一步 | **PASS** | 见 `reports/STATUS.md`、`reports/COVERAGE.md` |

## 6. 本轮已关闭问题（修复验证）

1. **49 张来源卡 `source_kind` 越界** → researcher 已归一化；validate 第 4 项 235/235 PASS。
2. **`query.py` 引号多词恒 0 命中 + 验收 query 证据为空** → engineer 已修 split/`--phrase`，并新增 `query_hits ≥1` 断言；18/18 PASS、命中总数 53。
3. **GAR-0034 一条从属断言扩写** → architect 已删去 FIT 从属断言、`source_ids` 改为 `[SRC-0203]`、叙事改标 interpretive；抽查关闭 PARTIAL。
4. **3 处列表数字未加引号** → architect 已加引号；validate 第 17 项 235/235 PASS。
5. **卡片模板未同步字典 v1.1** → architect 已同步（01:47:15）；来源卡字段/正文规则与字典一致。
6. **`SRC-0157` 重复未标注** → narrator 已标 canonical=SRC-0115，`PRD-0007` 改用 `SRC-0115`；`SRC-0163`/`SRC-0175` 亦标 canonical。
7. **任务简报「7 列表头」与规范冲突** → 按项目规范 8 列执行并在本报告记录。

## 7. 仍存在的缺口 / 未解决项（如实记录）

1. **60/142 来源卡未被任何内容卡引用**（42.3%），含全部 19 张 Getty AAT 卡；researcher 来源包与内容卡证据链仍未打通（§2.2）。
2. **P3 250+ 未达**：总卡 235（差 15）；按内容卡口径 93（差 157）。
3. **分类缺口**：`carried_prop` 0 张；结构 16 族系中 10 族为 0；材质 8 族仅 4 族、纹样 11 族仅 1 族（详见 COVERAGE §3）。
4. **Look「完整拆解」口径未定**：严格五槽 0/10、四槽 5/10；「至少 6 套完整拆解」需 lead 裁定口径（COVERAGE §3.F）。
5. **37 张卡 `review_status: draft`**（全部 PRD/STY/LOOK/SCN 与 example 卡），未经人工复核。
6. **3 组重复 URL**仍保留为交叉引用（已标 canonical）；是否物理合并由 lead 决定。
7. **`00-系统/来源规范.md` 仍为启动模板**（2026-11-03），未记录 SRC-0200..0299 段位扩展。
8. **`SRC-0204` 来源卡改名未提交**：git 为「旧名 deleted + 新名 untracked」，由 lead 版本收口。

## 8. NOT_TESTED 清单

- **Obsidian 本地打开/跳转：NOT_TESTED**（无 GUI；仅结构层验证 YAML/Markdown/wikilink）。
- **逐图版权授权：NOT_TESTED**（只验证 0 本地图片、0 内嵌；未逐张核对许可）。
- 史学方法学/叙事正确性未审（只验证「来源页是否支撑卡片断言」）。
- 推荐评分权重合理性未做调参评估（仅验证可运行、结构完整、ID 真实、退出码 0）。

## 9. 复现命令清单

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
python3 scripts/validate.py                       # exit 0：17/17 PASS，0 错误 0 警告
python3 scripts/validate.py --json > /tmp/validate.json
python3 scripts/build_sources.py --check          # exit 0：142/142 一致，3 组重复 URL（canonical 已标注）
python3 scripts/build_sources.py --write          # 从 142 张来源卡重建 reports/SOURCES.csv
python3 scripts/query.py "旗袍" --limit 3
python3 scripts/query.py "1930s 上海" --type garment --json       # 5 命中
python3 scripts/query.py "立领 shirt" --json                      # 7 命中
python3 scripts/query.py --phrase "1930s 上海" --json             # 1 命中
python3 scripts/recommend.py 11-验收/测试输入/T01-1930s上海知识分子-历史准确.json --json
python3 scripts/recommend.py 11-验收/测试输入/T03-现代雨夜调查者-多场次连续性.json --json
python3 scripts/run_acceptance.py                 # exit 0，PASS 18/18，query 命中总数 53
# 证据抽查（修复轮复测 4 URL 全 200；完整 19 对见 reports/EVIDENCE-SPOTCHECK.csv）
curl -sS -m 10 -L -o /tmp/ev.html -w '%{http_code}\n' https://collections.vam.ac.uk/item/O235319/
```

## 10. 版本

- v1.0（2026-11-04，verifier/task-6）：首次独立验收；对齐数据字典 v1.1；validate/build_sources、SOURCES.csv 重建、14 卡证据抽查、18 例验收复跑；报 49 枚举错误 + 3 警告 + query 缺陷。
- v1.1（2026-11-04，verifier/task-7）：修复后复验；**validate exit 0（17/17 PASS，0 错误 0 警告）**；query 多词缺陷与 GAR-0034 断言关闭；重建 SOURCES.csv（142 行，3 组重复 URL 标 canonical）；独立复跑 18/18 PASS（query 命中合计 53、逐例 ≥1）；剩余缺口见 §7。
