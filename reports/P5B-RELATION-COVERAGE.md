# P5-B 关系覆盖矩阵与语义单点分类

- 日期：2026-11-05（Asia/Shanghai）；执行：narrator（P5-B 覆盖/独立节点）
- 性质：**静态数据审查**；只写 `reports/P5B-RELATION-COVERAGE.md`、`reports/P5B-EXPANSION-PLAN.md`、`11-验收/P5B/coverage-matrix.csv`、`11-验收/P5B/isolates.csv`；**未修改卡片/脚本/MOC；不提升 draft**。
- 数据快照：当前树 400 卡（**189 内容卡 + 211 来源卡**）+ 9 个 MOC 页 + 1 个关系类型页；`validate.py` **PASS 400/400**（静态链接校验）。
- **GUI NOT_RUN**：未打开 Obsidian，未做渲染/点击/搜索/图谱；本文及 CSV 只代表文件层静态关系。
- 覆盖口径：**existing relation coverage** = 卡片 `relations` + 结构化字段（`source_ids`/`look_items`/`look_scene`/`key_garments`）+ 正文可见 `[[ID]]` 链接的并集；**不把 `RELATION-CANDIDATES.csv` 的候选算入**（候选是假设层，算入会高估）。`—` 表示按类型设计不要求该关系，不是 0% 失败。

## 0. 结论摘要

| 项 | 结果 |
|---|---|
| 189 内容卡覆盖 | 按类别矩阵见 `11-验收/P5B/coverage-matrix.csv`（18 行；garment 10 类 + garment ALL + 其余 7 类型） |
| 最强覆盖 | garment 的 `silhouette/period/region` ≈ **99–100%**；claim→source（机器字段+链接）garment **93%** |
| 最弱覆盖（Top 5） | garment→**component 18%**、→**style 2%**、→**outfit 0%**、→**material 40%**；garment_part→**material 8%**；LOOK→**narrative 57%** |
| 65 个语义单点 | **34 legit_reference / 16 evidence_missing_expression / 14 future_topic / 1 no_verifiable_relation** |
| 38 张 draft | **未改状态、未迁移**；38 = look 22 / scene 15 / style 1（P5 迁移批次） |
| 来源/导航 | 211 来源：143 被引用、68 未引用；65 单点见 `isolates.csv`；导航 9 MOC + 1 关系页，**不计入**语义覆盖 |

## 1. 方法与类别分母

- 内容卡 189：garment **88**、garment_part **26**、look **23**、scene **16**、material **11**、period_region **11**、style **11**、pattern **3**。
- 覆盖维度按类型定义（不是所有类型都需要全部列）：
  - **garment**：component（→STR）、material（→MAT/PAT）、silhouette（`silhouette` 字段）、period/region（`periods`/`regions`）、accessory-footwear（→鞋履/头饰/配饰/携带物 GAR）、style（→STY 或 `style_tags` 含 STY）、outfit（→LOOK）、claim→source（→SRC）；narrative n/a。
  - **garment_part**：material、period、region、style、claim→source；component/outfit/narrative n/a（部件不是完整套装）。
  - **look**：narrative（`narrative_meaning` 非空）、style、period、region、claim→source；component/material/outfit n/a（套装本身）。
  - **material/pattern**：period、region、style、claim→source；component/outfit/narrative n/a。
  - **scene**：style、period、region、claim→source；component/outfit/narrative n/a。
  - **style**：period、region、claim→source；component/outfit/narrative n/a。
  - **period_region**：period、region、style、claim→source；component/outfit/narrative n/a。
- `claim_source` 包含机器 `source_ids`/关系与可见 SRC 链接；**visible-only 缺口**另见 §4（38 draft 有 106 对 source_ids 无可见 SRC 链接）。

## 2. 覆盖矩阵摘要

| 类型 | 卡数 | component | material | style | outfit | narrative | claim→source |
|---|---:|---|---|---|---|---|---|
| garment ALL | 88 | 16/88 (18%) | 35/88 (40%) | 2/88 (2%) | 0/88 (0%) | — | 82/88 (93%) |
| ├ one_piece | 23 | 6/23 (26%) | 14/23 (61%) | 0/23 (0%) | 0/23 (0%) | — | 21/23 (91%) |
| ├ outerwear | 12 | 0/12 (0%) | 5/12 (42%) | 0/12 (0%) | 0/12 (0%) | — | 11/12 (92%) |
| ├ accessory | 11 | 2/11 (18%) | 3/11 (27%) | 2/11 (18%) | 0/11 (0%) | — | 11/11 (100%) |
| ├ footwear | 9 | 0/9 (0%) | 1/9 (11%) | 0/9 (0%) | 0/9 (0%) | — | 8/9 (89%) |
| ├ upper_body | 8 | 3/8 (38%) | 3/8 (38%) | 0/8 (0%) | 0/8 (0%) | — | 6/8 (75%) |
| ├ headwear | 7 | 0/7 (0%) | 3/7 (43%) | 0/7 (0%) | 0/7 (0%) | — | 7/7 (100%) |
| ├ lower_body | 6 | 1/6 (17%) | 1/6 (17%) | 0/6 (0%) | 0/6 (0%) | — | 6/6 (100%) |
| ├ carried_prop | 5 | 2/5 (40%) | 0/5 (0%) | 0/5 (0%) | 0/5 (0%) | — | 5/5 (100%) |
| ├ specialised | 4 | 1/4 (25%) | 3/4 (75%) | 0/4 (0%) | 0/4 (0%) | — | 4/4 (100%) |
| └ inner_layer | 3 | 1/3 (33%) | 2/3 (67%) | 0/3 (0%) | 0/3 (0%) | — | 3/3 (100%) |
| garment_part | 26 | — | 2/26 (8%) | 0/26 (0%) | — | — | 26/26 (100%) |
| look | 23 | — | — | 22/23 (96%) | — | **13/23 (57%)** | 22/23 (96%) |
| material | 11 | — | — | 0/11 (0%) | — | — | 11/11 (100%) |
| pattern | 3 | — | — | 0/3 (0%) | — | — | 3/3 (100%) |
| period_region | 11 | — | — | 10/11 (91%) | — | — | 11/11 (100%) |
| scene | 16 | — | — | 16/16 (100%) | — | — | 16/16 (100%) |
| style | 11 | — | — | — | — | — | 10/11 (91%) |

完整 18 行矩阵（含 silhouette/period/region/accessory_footwear/source_ids_yaml 与 draft 计数）：`11-验收/P5B/coverage-matrix.csv`。

## 3. 缺口 Top（按高价值排序）

1. **garment→component 18%**：88 件中仅 16 件有结构部件关系（多数为正文 `相关卡片` 链到 STR）；outerwear/footwear/headwear 的 component 为 0%。结构层对服装的解释力不足。
2. **garment→style 2%、→outfit 0%**：仅 2/88 garment 有 STY 标签/链接；没有 garment→LOOK 关系（LOOK 的 `look_items` 是 LOOK→garment 单向，卡片侧无回链）。风格与造型使用面几乎空。
3. **garment→material 40%**：one_piece 61% 尚可，outerwear 42%、upper_body 38%、footwear 11%，与“材料是服装核心”不匹配。
4. **garment_part→material 8%（2/26）**：部件卡几乎不连材料/风格，部件无法回答“这个领/袖用什么面料/属于什么风格”。
5. **LOOK→narrative 57%（13/23）**：10 套 LOOK 无 `narrative_meaning`；LOOOK 的 claim→source 96% 但叙事字段缺口明显。
6. **document/notation**：material/pattern 风格关系 0%；pattern 仅 3 张；鞋履 9/配饰 11/头饰 7 偏薄（与 `P5-COVERAGE-GAPS` 一致）。
7. **来源可见性**：143/143 被引用来源已可见（P5-A 修复）；但 **38 张 draft 仍有 106 对 `source_ids` 无可见 SRC 链接**；68 来源未被任何内容卡引用（65 个语义单点的主要来源）。

## 4. 来源 / 导航（与内容矩阵分开）

| 指标 | 数值 | 说明 |
|---|---:|---|
| 来源卡 | 211 | `type=source` |
| 被内容卡引用 | 143 | 机器 `source_ids`，均已有可见链接（P5-A 后） |
| 未被引用 | 68 | vocabulary 19 / museum 12 / academic 10 / reference 9 / other 8 / image 5 / industry 4 / dataset 1（含 9 本 P4 书源） |
| 65 个语义单点来源 | 65 | 28 isolated + 27 background + 9 navigation-only + 1 book（旧图分类） |
| 导航 | 9 MOC + 1 关系类型页 | 只做导航，不计入 content+source 语义分量；静态 `[[...]]` 无 broken（validate PASS） |
| draft 可见性 | 38 draft = 106 source pairs 不可见 | look 22 / scene 15 / style 1；本任务不迁移、不改状态 |

## 5. 65 个语义单点分类

- 完整 65 行：`11-验收/P5B/isolates.csv`（`source_id,name_zh,source_kind,isolate_reason,classification,evidence,related_cards,recommendation`；全部为真实 SRC，related_cards 只填真实卡 ID）。
- 统计：

| 分类 | 数量 | 代表 | 处置 |
|---|---:|---|---|
| legit_reference | **34** | SRC-0004–0020 AAT/FIT 词典；SRC-0033–0035 CDG/Screen Ireland 实践；SRC-0042/0043 学会；SRC-0045–0049 Wikimedia 图像权 | 保留独立参考/背景；MOC 标注用途，不强制连接 |
| evidence_missing_expression | **16** | 7 个 should-connect（SRC-0028/0029/0030/0037/0041/0050/0059）+ 9 本 P4 书源 SRC-0061..0069 | 人工复核后补 source_ids/关系；书源用 book_fact + 章/行定位，不自动迁移 |
| future_topic | **14** | SRC-0018/19/20 FIT 服饰分析；SRC-0023–0027 Met 连衣裙/束身衣；SRC-0031/0032 体操/运动服；SRC-0038 Undressed；SRC-0039 羽毛帽；SRC-0040 武士衬衫；SRC-0060 防染印花 | 列入未来主题 backlog；先有案例需求再做卡，不硬连 |
| no_verifiable_relation | **1** | SRC-0044 The Museum at FIT 主页 | 仅作背景/导航，不建立内容关系 |

- 这 65 个都是**来源单点**，不是内容卡孤立；189 内容卡全部在语义主分量（P5-GRAPH-AFTER）。因此“单点”不应用“强制链接”消除。
- 7 个 should-connect 的现成目标（真实 ID）：
  `SRC-0028→GAR-0001`、`SRC-0029→GAR-0008`、`SRC-0030→GAR-0008`、`SRC-0037→GAR-0045`、`SRC-0041→GAR-0063`、`SRC-0050→GAR-0080`、`SRC-0059→GAR-0047`。

## 6. 38 张 draft（保持原状）

- 38 张 = **look 22 / scene 15 / style 1**（draft + `source_ids` + 无可见 SRC 链接；P5 迁移批次）：
  - LOOK：`LOOK-0001..0022` 中的 22 张（以实际 frontmatter 为准，含 LOOK-0011、LOOK-0013 等）；
  - SCN：SCN-0002..0016 中的 15 张；
  - STY：STY-0005。
- **本任务未改任何 draft 的 `review_status`/正文/`relations`**；不自动提升。
- 当前内容卡 draft 总数为 **62**（38 迁移批次 + 24 其他 draft：period_region 11、style 10、garment 1、look 1、scene 1 的合计，按实际字段）；扩建计划只处理 38 批次的“是否补可见关系”，其余 draft 保持独立审核。
- 若后续补关系：需人工复核 + `validate.py`；不在本任务实施。

## 7. 独立专题（拜占庭/莫卧儿/日本/奥斯曼/非西方）

- 覆盖矩阵没有“region/topic”维度；这些专题卡分散在 garment/material/period_region 行中，**没有类型化强制连通**（无日本↔中国、莫卧儿↔欧洲事实关系）。
- 但 65 个 future_topic 中多为非西方/历史专题素材（如 SRC-0018/19/20 欧洲 19c 裙、SRC-0023–0027 Met 裙/束胸、SRC-0038–0040 内衣/羽帽/武士衬衫；莫卧儿/日本卡已有 GAR-0071/0072、GAR-0001/0065）。
- 结论：**不应为了连通率把独立专题硬连**；应建“区域/专题 MOC”做并列导航（见扩建计划 P2），并等案例需求再补卡。

## 8. 结论

- 内容层“**元数据强、结构与使用关系弱**”：period/region/silhouette/claim 覆盖高，component/style/outfit/material 覆盖低；缺口集中在 garments 的结构与使用面，以及 LOOK 的叙事字段。
- 来源层：P5-A 已修复可见性主体（143/143 被引用来源可见）；剩余 65 个单点主要是**合理独立参考/未来主题/证据未表达**，不应以硬连解决。
- 下一步见 `reports/P5B-EXPANSION-PLAN.md`（P0 先补“已有卡之间的真实关系/可见性”，P1 才少量补卡）。
