# P5-C 公版书与来源再利用、新来源核验（P5C-SOURCE-REUSE）

- 生成：2026-11-05（Asia/Shanghai）；worker：researcher（task-73，P5-C 来源再利用）
- 写权限：`04-来源/`、`06-时代地域/书籍研究/`、本报告；**未改任何内容卡事实、未改脚本/00-系统**。
- 基线：HEAD `f500289`（400 卡 = 189 内容 + 211 来源）；执行后：来源卡 **234**（+23），内容卡 **206**（narrator/task-71 新增 17 张 LOOK/STY 并行落地；非本任务改动）。
- 关联文件：`06-时代地域/书籍研究/书籍来源复用指南.md`、`06-时代地域/书籍研究/来源复用-白名单增补-2026-11-05.md`、`04-来源/SRC-0530..0552-*.md`。

## 0. 总览

| 项 | 结果 |
|---|---|
| P4 九本书评估 | **9/9** 判定：高复用 2、中用 3、低/背景 4；**0 本作废** |
| 可复用结论 | P4-1 既有 31 条中 **15 条 verified**（书+独立来源）可作强引用；11 partial / 5 candidate 只能 book_fact 背景 |
| 新来源卡 | **23 张（SRC-0530..0552）**：V&A 对象 10 + Getty AAT 词条 13；**23/23 HTTP 200 + 内容命中** |
| 新卡 `source_ids` 核验 | 17 张新 LOOK/STY（narrator 并行）**0 source_ids** → 无“不支撑引用”；抽样 8 张 P4-2/P5 结构/材质卡 → **0 未支撑** |
| 许可限制 | Books: PD in USA + PG License + 无图像 + 页码 UNCONFIRMED；V&A: © link_only；AAT: ODC-BY |
| 0 图片策略 | 保持：0 下载、0 内嵌（全部新来源仅存链接） |

## 1. 九本公版书：可复用于新卡的具体证据

详见 `06-时代地域/书籍研究/书籍来源复用指南.md`（含每条的章/段/行定位）。摘要：

| 书 | 等级 | 可支撑的 P5-C 主题（book_fact） |
|---|---|---|
| **PG 21534 Textiles and Clothing**（SRC-0062） | **高** | 羊毛（Wool 733/1）、亚麻（Flax 858/1）、丝绸（Silk 1016/1）、织物组织（Weaves 1330/1）、手工缝（2541/1）、门襟（Plackets 3167/1）、领（Collars 4747/1）、七片裙（4045/7）、shirtwaist（4303/56） |
| **PG 76299 Dictionary of Men's Wear**（SRC-0066） | **高** | Worsted/Serge/Flannel/Tweed/Denim 词条（17403/5352、13006/4020、5939/1803、16062/4979、4342/1339）；Waistcoat、Frock/Sack coat、Trousers、Cravat、Hose、Knickerbockers、Spats 等定义 |
| PG 46949 Chats on Costume（SRC-0069） | 中 | collar/cuff 3598/8、doublet & hose 2351/7、kirtle 2811/11、crinoline 3223/2、hats 4097/9、shoes 5589/1、tunic 1374/6 |
| PG 48551 Costume Fanciful（SRC-0064） | 中 | farthingale 5155/24、stomacher/袖 1821/9、fancy dress 4561/16 |
| PG 34903 Dress Design（SRC-0061） | 中 | trimmings 1402/3、slashed/puffed 1419/4、farthingale 1746/63 |
| PG 33020 English Costume（SRC-0063） | 低（背景） | tunic→doublet 6143/7（已在 P4 C29 使用）；其余君主期叙事仅背景 |
| PG 56978 Book of the Feet（SRC-0067） | 低（背景） | 英国靴鞋史 622/1、外国靴鞋 1185/1、气候与鞋形 1190/3 |
| PG 76717 History of Fashion in France（SRC-0068） | 低（背景） | Gallic 1009/1、woad 1023/4 |
| PG 49559 Jewellery and Fans（SRC-0065） | 低（背景） | 珠宝材料 202/25、金/象牙/珐琅/珍珠 507/70 |

- **引用格式**：`book_fact: 《书名》PG<id>，章「X」，段 n，行 n（page UNCONFIRMED）`；只有同时挂独立 V&A/Met/FIT/AAT 来源并双向一致时才可 `verified`。
- **未强制引用**：现有内容卡大多已用页面级 SRC（FIT/V&A/Met）承载同类断言；再挂书源只为孤立数服务，本任务不采用。

## 2. 新来源卡 SRC-0530..0552（23 张，全部核验）

### 2.1 V&A 对象（10 张，museum_collection，link_only）

| SRC | 对象号 | 支撑主题 | 关键引文（馆方描述） |
|---|---|---|---|
| SRC-0530 | O72654 | 领口（square）、丝绸/乔其纱、1920s 晚装 | “Square-shape neckline and straight long bodice” |
| SRC-0531 | O85657 | 领口（round）、抽褶 | “a round and wide neckline … slightly gathered at the hips” |
| SRC-0532 | O102166 | 青果领、门襟贴边、袋盖口袋、袖口 | “shawl collar, front facings, pocket flaps and cuffs of scarlet satin” |
| SRC-0533 | O353415 | 泡泡袖、褶裥、抽褶、高腰线、后开合 | “long puffed and pleated sleeves, high waistline, back fastening … gathered at the waist” |
| SRC-0534 | O353447 | 羊毛织物、里布、贴边/衬 | “wool … faced with satin and lined with glazed cotton” |
| SRC-0535 | O355340 | 拖尾、方领、纽扣开合、钟形袖 | “rounded train … low square neckline … button fastening” |
| SRC-0536 | O68370 | 腰封/束腰带、1940s New Look | “The \'waspie\' was a belt-girdle designed to cinch the waist…” |
| SRC-0537 | O135197 | 乐福鞋、流苏饰 | “Black leather loafers … tassel and fringes” |
| SRC-0538 | O356431 | 晚装长手套 | “Fine white kid evening or opera length gloves designed to cover the entire arm” |
| SRC-0539 | O1242729 | 亚麻织物、青果领（现代实例） | “Jacket, of green linen … and shawl collar” |

### 2.2 Getty AAT 词条（13 张，vocabulary，ODC-BY）

| SRC | AAT 记录 | 首选词 | 用途 |
|---|---|---|---|
| SRC-0540 | 300227843 | interlining | 里布与衬 |
| SRC-0541 | 300053656 | quilting | 填充与绗缝 |
| SRC-0542 | 300227860 | padding (material) | 填充 |
| SRC-0543 | 300227874 | pleats | 褶裥 |
| SRC-0544 | 300231237 | gathering (textile process) | 抽褶 |
| SRC-0545 | 300210517 | pockets (costume components) | 口袋结构 |
| SRC-0546 | 300224243 | trains (costume components) | 拖尾 |
| SRC-0547 | 300243430 | wool (textile) | 羊毛织物 |
| SRC-0548 | 300014069 | linen (material) | 亚麻织物 |
| SRC-0549 | 300011845 | leather | 皮革 |
| SRC-0550 | 300014058 | synthetic fiber | 现代合成纤维 |
| SRC-0551 | 300046001 | necklaces | 项链 |
| SRC-0552 | 300045998 | earrings (jewelry) | 耳环 |

### 2.3 验证记录

- 每张 V&A 卡：`collections.vam.ac.uk/item/<Oxxxx>/` HTTP **200**，页面标题与卡片 `title` 一致；`api.vam.ac.uk/v2/museumobject/<Oxxxx>` HTTP **200**，`record.physicalDescription` 与卡内引文一致。
- 每张 AAT 卡：`vocab.getty.edu/aat/<id>.nt` HTTP **200**，`skos:prefLabel` 与卡片 `name_en` 一致；`vocab.getty.edu/page/aat/<id>` HTTP **200**，`Note:` 与卡内引文一致。
- 批检结果：**23/23 HTTP 200，0 失败**（2026-11-05）。
- 图片：0 下载、0 内嵌；V&A/AAT 图像均只保留对象页/记录页链接。

## 3. 新增内容卡的 source_ids 支撑核验

### 3.1 narrator 新增 17 张（LOOK-0024..0035、STY-0011..0015）
- 状态：全部 `evidence_status: interpretive`，**`source_ids` 为空**；正文含 **2–10 个 SRC 引用**（如 LOOK-0024 含 SRC-0423/0480/0481/0482/0483/0487 等）。
- 结论：**没有“source_ids 不支撑断言”的问题**（因为没有挂 source_ids）；但“可见证据”不足——如需要，可把正文实际使用的 SRC 补进 `source_ids`（保持 interpretive，不升级 verified）。本任务不强制、不改卡。
- 建议（给 narrator/architect）：这些 LOOK/STY 的引用是关系/设计参考，不是断言证据；若要提升可审计性，只补“实际使用”的 2–4 个 SRC，避免把正文所有链接都挂上。

### 3.2 P4-2/P5 结构/材质卡（23 张）抽样 8 张
- 抽样：GAR-0083 手套、GAR-0084 高跟鞋、GAR-0085 帽子结构、STR-0013 装袖/插肩、STR-0014 肩线/肩垫、STR-0019 拉链、STR-0026 手袋结构、MAT-0012 织物组织。
- 核验方法：读卡片 `支撑范围` + 来源卡正文的对应事实（不是只看 URL/关键词）：
  - STR-0013 ↔ SRC-0406：来源卡正文含 “raglan 肩、宽外扩袖…”；↔ SRC-0484：doublet 描述含两片弯袖装袖；**支撑**。
  - STR-0014 ↔ SRC-0412：来源卡正文含 “垫肩（padded shoulders）” 与 1942 Utility 语境；**支撑**。
  - STR-0019 ↔ SRC-0201：来源卡正文含 “侧缝暗藏按扣与隐形拉链”；**精确支撑**。
  - GAR-0085 ↔ SRC-0523：来源卡含帽冠/宽檐/尺寸/pack threads 等；**支撑**。
  - MAT-0012 ↔ SRC-0102/0423：muslin 平纹与 samite 组织描述；**支撑**（组织细分仍标 interpretive 的部分除外）。
  - STR-0026 ↔ SRC-0408：来源仅载刺绣帆布+羊毛十字绣与作者，未载提手/扣合；**卡内已把提手/扣合标 interpretive**，做法正确，无“不支撑却标 verified”。
- 结果：**抽样 0 条失败**；无需改 interpretive/补源。限制：仅抽样 8/23，未覆盖全部 P4-2 卡；建议 QA 下一轮做全量 source-claim 对照。

## 4. 白名单/黑名单更新

- 已写 `06-时代地域/书籍研究/来源复用-白名单增补-2026-11-05.md`：
  - 10 张 V&A 对象卡 = `action_should_connect`（目标为 task-72 计划新卡；被引用后转 `whitelist_connected`）；
  - 13 张 AAT 词条卡 = `whitelist_independent`（术语背景，按既有 AAT 政策）；
  - **黑名单无新增**；canonical 重复仍为 SRC-0157→0115、SRC-0163→0022、SRC-0175→0036。
- **待办（不在本任务写权限）**：`11-验收/P5/source-audit.csv` 仍为 211 行旧快照；`reports/SOURCES.csv` 仍为 211 登记行。**新卡落地后必须重跑** `python3 scripts/build_sources.py --write` 与 P5-A 审计（engineer/verifier），否则 `build_sources.py --check` 会报 23 行缺失。

## 5. 许可边界与失败项

- **书籍**：PD in USA；PG License 约束再分发制备文本；无插图；纯文本无可靠页码 → 页码统一 UNCONFIRMED；旧书（1847–1919）为二手综述，现代研究可纠正其年代/文化判断。非美国地区使用需查当地法。
- **V&A 对象**：文字与图像 © Victoria and Albert Museum；本库只链接、不复制图像；馆方描述是单件著录，不可外推为时代通例。
- **AAT**：ODC-BY 1.0，需署名 Getty Research Institute；定义不含具体历史/工艺细分。
- **失败项**：新来源 URL **0 失败**；书籍文本此前已验证 9/9 HTTP 200（PG 书目页偶发超时，但文本与 PD 声明可用，见 P4 报告）。
- **0 图片策略**：保持 0 下载 / 0 内嵌。

## 6. 仍需补的文献（新卡缺口）

1. A/H/Y/T/X 廓形分类：无权威词汇来源（Fashionpedia 不提供该分类）→ 建议 interpretive，或另找服装史/制版教材。
2. 鱼尾摆（fishtail）特殊剪裁：AAT trains 不含鱼尾剪裁 → 需专门裁剪书/馆藏结构分析。
3. 皮革植鞣 vs 铬鞣：AAT leather 无工艺细分 → 需工艺/技术史来源。
4. 现代合成纤维的具体聚合物（nylon/polyester）：AAT 仅泛称 synthetic fiber。
5. 纹样族（条纹/格纹/印花/提花/刺绣）：现有 pattern 卡仅 3 张，需专门图录/术语来源（AAT stripe/check 可先补）。
6. 11 世纪苏格兰/中世纪盛期语境、18 世纪法国宫廷：period_region 缺口（P5 覆盖矩阵已列）。
7. 书籍工艺细节：P4 书为综述，缺裁剪图/工艺步骤；衬/填充/口袋/褶裥仍建议补一手裁剪书或馆藏工艺记录。

## 7. 复现命令

```bash
# 新来源核验（逐卡）
for f in 04-来源/SRC-053*.md 04-来源/SRC-054*.md 04-来源/SRC-055*.md; do :; done
curl -sS -m 20 -L -o /tmp/p.html -w '%{http_code}' https://collections.vam.ac.uk/item/O72654/
curl -sS -m 20 -L -o /tmp/a.nt -w '%{http_code}' https://vocab.getty.edu/aat/300227843.nt
# 结构校验（当前 440 卡应 PASS）
python3 scripts/validate.py
# 登记重建（本任务写权限外，需 engineer/verifier 执行）
python3 scripts/build_sources.py --write
```
