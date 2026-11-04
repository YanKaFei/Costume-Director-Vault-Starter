# P4 覆盖报告（COVERAGE）

- 生成：2026-11-04 16:26；verifier / task-45；快照 **399 卡**（内容 188 + 来源 211）；HEAD `7f7a21b`
- 口径：`01/02/03/04/05/06/07/09` 带 frontmatter 的 `.md`；`00-系统/`、`10-提示词模板/`、`11-验收/`、`docs/`、`skills/`、`.dsh/`、`projects/` 不计入

## 1. 总量

| 指标 | P3.6 | **P4** | 变化 |
|---|---|---|---|
| 总卡 | 363 | **399** | +36 |
| 内容卡 | 166 | **188** | +22 |
| 来源卡 | 197 | **211** | +14 |
| verified | 316（P3.6 时） | **352** | — |
| interpretive | 43 | **43** | — |
| example | 4 | 4 | — |
| `review_status: draft` | 62 | **62** | — |
| 验收用例 | 45 | **45** | — |
| composer 用例 | — | **9** | +9 |
| Macbeth P4 用例 | — | **11** | +11 |

## 2. 类型分布（P4）

| 类型 | 数量 | P4 变化 |
|---|---|---|
| garment | **88** | +13（P4 新增 5：GAR-0083..0087） |
| garment_part | **25** | +14（STR-0012..0025） |
| material | **11** | +3（MAT-0012..0014） |
| pattern | 3 | 0（仍是最大缺口） |
| style | 11 | 0 |
| period_region | 11 | 0 |
| look | 23 | 0 |
| scene | 16 | 0 |
| source | **211** | +14（SRC-0061..0069 九本 PD 书 + SRC-0520/0521 FreeSewing + SRC-0522..0524 V&A） |

## 3. P4 新增卡片覆盖

### 3.1 结构/配饰/材料（22 张，全部 `verified`）
- 配饰/结构类：GAR-0083 手套、GAR-0084 高跟鞋、GAR-0085 帽子结构、GAR-0086 胸针结构、GAR-0087 手袋结构；
- 部件类（STR-0012..0025）：翻领与驳领、装袖与插肩袖、肩线与肩垫、腰线、衣摆与开衩、门襟、纽扣与扣眼、拉链、裁片与拼片、接缝与省道、腰头、袖口、结构属性词表（Fashionpedia）、松量与版型；
- 材料类（MAT-0012..0014）：织物组织、克重与垂坠、反光与金属线。

### 3.2 v1.2 可选字段
- 文档：`00-系统/数据字典-v1.2-扩展.md`；**42 个可选字段**（向后兼容；不修改 v1.1）。
- 使用：22 张新卡覆盖 **36/42** 字段（翻领/袖型/肩线/腰线/衣摆/门襟/纽扣/拉链/裁片/接缝/腰头/袖口/松量/鞋型/鞋跟/帽/首饰/携带物/织物组织/厚薄/垂坠/反光等）。
- 旧卡：0 修改（git diff 01–09 无 M 条目），validate 399/399 PASS。

### 3.3 来源覆盖与许可
- 211 张来源卡；license 分布：`link_only 139 / other_permission 43 / cc0 17 / cc_by 3`（内容卡 `not_applicable 197`）。
- P4 新增来源：9 本 PD 书（Public Domain + PG License）、2 张 FreeSewing（MIT→other_permission）、3 张 V&A（link_only）。

## 4. 书籍/术语覆盖（P4-1）

| 指标 | 结果 |
|---|---|
| 解析书目 | **9/9**（5 GITenberg + 4 Gutenberg；均 PD in USA） |
| 章节识别 | 8/9 按章（49559 为文集无章节），共 **157 章** |
| 术语 hits | **12,640**（9 书合计，记录上限 2000/书） |
| 词典词条 | PG 76299：**5,391** 个男装词条头 |
| 研究结论 | **31 条**（verified 15 / partial 11 / candidate 5） |
| 页码 | 全部 UNCONFIRMED（纯文本无页码；章/段/行定位） |
| 现代版权文本 | 0（仅用 PG 公版文本） |

## 5. 视觉索引覆盖（P4-4）

- `visual-index.csv`：**28 条**，覆盖 4–7 世纪至 1890 年代多个品类（连衣裙/外套/马甲/胸衣/靴/鞋/扇/阳伞/和服/束腰长袍等）；
- `rights_status`：28/28 = CC0 / Met Open Access (`isPublicDomain=true`)；图像 URL 200（28/28）；
- 关联：`related_card` 27/28（1 条空白）；`source_id` 为 SRC 或 MET-API（原型，未建独立 SRC）；
- **0 下载/0 内嵌**：Vault 内图片文件 0。

## 6. 验收覆盖（P4-3 / P4-5）

- Composer 回归 **9 例**：macbeth、lady_macbeth、cross_cultural_ghana、rain_continuity、low_budget、closeup、action_dance、occupation_nurse、conflict_reject。
- Macbeth P4 **11 例**：阶段变化×2、双人关系、全槽/配饰、历史证据缺口、极简 vs 复杂、特写、动作、视频连续性、中英术语检索、证据不足拒绝。
- 覆盖缺口（不变）：pattern 3/11 族、material 11/8 族（仍缺 leather/fur/metal 细化）、garment_part 25/16 族（超额但偏结构词表）；62 draft；19 张 AAT 未接入。

## 7. 结论

- P4 新增 **36 张卡**（22 内容 + 14 来源），总量 **399**；旧卡 0 破坏、validate 399/399；未引入受限来源。
- 书籍/视觉/composer/Macbeth 四域交付均有独立验收证据；覆盖缺口主要集中在 pattern/material 颗粒度、draft 人工复核与 AAT 接入。
- 索引/结构字段覆盖显著提升（v1.2 42 可选字段，36 个已被新卡使用）。
