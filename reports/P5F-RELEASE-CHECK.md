# P5-F 知识库健康检查（P5F-RELEASE-CHECK）

- 生成：2026-11-05 11:55（Asia/Shanghai）；verifier / task-95（只读；未改卡片/脚本）
- 快照：**HEAD `4128266`**（P5-E 已提交）；工作区仅 21 个未跟踪 sandbox；**458 卡 = 224 内容 + 234 来源；334 relations**
- 基础校验：`validate` **458/458 PASS**、`build_sources` **PASS 234**、`relation_consistency` **0 errors / 334**

## 0. 健康结论（摘要）

| 维度 | 结果 | 判定 |
|---|---|---|
| schema/字段完整性 | validate 458/458 PASS；ID/文件名一致 | **PASS** |
| type/category 语义 | 3 张 MAT 前缀卡 type=pattern；92/234 来源缺 category 字段 | **WARN（P3）** |
| 重复/同义词 | 0 重复 ID；3 对重复来源 URL；2 组跨类型重名；6 组别名冲突 | **WARN（P2/P3）** |
| source_ids 引用 | 478 对，0 缺失；172/234 被引；370/478 可见（77.4%） | **PASS（有缺口）** |
| MOC 导航 | 9 页、无 frontmatter、**544 链接全解析；覆盖 224/224 内容 + 234/234 来源**（lead 已补 35 内容/23 来源） | **PASS** |
| wikilink/backlinks | 真实 unresolved **0**（graph 1 为 code 示例，task-93 修）；回链非对称 981/1663（设计如此） | **PASS** |
| 专业 vs 导航 | 458 语义卡 vs 26 导航 + 5 研究；MOC 仅导航；11 个导航文档零链接 | **WARN（P3）** |
| 适用性覆盖 | present **474/775（61.2%）**；APPLICABLE 380 / REVIEW 94 / INSUFFICIENT 301 / N/A 1017 | **数据真实，不追求全连通** |
| 遗留 | 59 isolates / 62 uncited / 38 draft / 6 flags；quality NOT_RUN；GUI NOT_RUN | 见 §8 |

## 1. 分类 / type / category 一致性

- 类型：source 234、garment 92、garment_part 35、look 35、material 16、style 16、scene 16、period_region 11、pattern 3（合计 458）。
- ID 前缀 vs type：**3 处不一致**——`MAT-0005`（肯特布）、`MAT-0006`（阿丁克拉纹样）、`MAT-0007`（泥染布纹样）为 `type=pattern`（纹样卡），却使用 MAT 前缀（应为 PAT 语义）。**不改 ID**（会破坏现有链接）；建议在数据字典登记“MAT 前缀纹样卡例外”或未来做一次 canonical 迁移（WARN/P3）。
- 文件名 vs ID：**0 处不一致**（458/458 文件名以 ID 开头）。
- category：内容卡分类齐全；**来源卡 142 有 `category=source`、92 张缺 `category`**（来源卡主要用 `source_kind`）；validate 通过，属字段使用不统一（P3，报告口径即可，不必批量补）。
- evidence/review：verified 393 / interpretive 61 / example 4；reviewed 378 / draft 79 / needs_review 1。

## 2. 重复 / 同义词

| 项 | 结果 |
|---|---|
| 重复 ID | **0** |
| 重复 name_zh/name_en | 2 组跨类型：`gloves`（GAR-0083 vs SRC-0052）、`leather`（MAT-0017 vs SRC-0549）——内容/来源同名，非重复卡 |
| 别名冲突（同 alias 多个卡） | **6 组**：腰带（GAR-0066/GAR-0080）、着物（GAR-0065/GAR-0001）、tunic（GAR-0075/GAR-0061）、长袍（GAR-0032/GAR-0004）、gigot（STR-0029/STR-0004）、seam allowance（STR-0021/STR-0025）→ 浏览/改写时需消歧（P3） |
| 重复来源 URL | **3 对**：SRC-0036 ↔ SRC-0175（Screen Ireland 手册）、SRC-0163 ↔ SRC-0022（FIT Byzantine silk）、SRC-0115 ↔ SRC-0157（FIT 1950-1959）→ 是 3 个 uncited 未分类来源的来源；建议合并/标 canonical（P2） |
| 重复内容卡 | 未发现（同一概念多卡属细分，如 MAT-0012/0013 物性 vs MAT-0015.. 材料） |

## 3. source_ids / 引用健康

- source_ids 对 **478**；**0 目标缺失**；被引来源 **172/234**；未引用 **62**（59 isolates + 3 个重复来源 SRC-0163/0157/0175）。
- 正文可见对 **370/478（77.4%）**；可见来源 **172/172（100%）**；**零可见 SRC 卡 39** = 38 draft（LOOK22/SCN15/STY1）+ GAR-0045（medium review）。
- 有 source_ids 无任何可见来源的卡：**40**（含 GAR-0033 部分可见）；这是“draft/待审未渲染来源链接”的已知状态，不是数据错误。
- 来源卡 234 在语义图零可见为 0（内容/来源链接），但 **MOC 只链到 211/234**（23 张新来源未进 MOC）；语义接入以 source_ids/可见对（370）衡量，导航可达 ≠ 语义覆盖。

## 4. MOC 导航（已补齐，PASS）

- **9 个 MOC 页**（`00-系统/MOC/`）：README + 时代地域/服装单品/材质纹样/来源证据/结构细节/造型组合/鞋履配饰/风格体系。
- **均无 frontmatter（navigation-only）**；总链接 **482**，全部解析（0 未解析）；来源证据页链 211 来源。
- **覆盖（lead 已补齐）**：**内容 224/224、来源 234/234**；新增 35 内容（LOOK-0024..0035、STY-0011..0015、GAR-0088..0091、STR-0027..0035、MAT-0015..0019）与 23 来源（SRC-0530..0552）均已入 MOC；**544 链接、0 未解析**；9 页仍无 frontmatter（navigation-only）。
- 结论：**P2 MOC 缺口已关闭**；UAT 第 2 项预期改为 PASS。原有 482→544 链接（+62，导航新增，不计语义）。
- 另有 11 个导航文档零链接：Outfit模型、来源规范、数据字典 v1.2/1.3/1.4、4 个提示词模板、根 README、AGENTS；根 README 零链接不利入口（P3）。

## 5. Wikilink / Backlinks

- 可见边 **2158**（语义 1663 + 导航 495）；内容零链接 **0/224**；来源零可见 **0/234（MOC 导航）**。
- **真实 unresolved wikilink = 0**（剔除 fenced/inline code 后）；graph 工具报 1 为 `00-系统/关系类型.md` 行内 code 示例，**非真实链接**（task-93 修复中）。
- **真实 typed unresolved = 0**（脚本按 fm.id 校验）；graph 工具报 5 为 `GAR-EXAMPLE-001` 被 ID 正则漏识别（文件存在、ID 合法；task-93 修复中）。
- 回链：卡片可见对 1663，互链 682，非对称 981（内容→来源 370、来源→内容 186、来源→来源 16、内容→内容 1071）。**非对称是引用模型设计**（来源卡主动列实例），不是坏链；不追求 100% 互链。
- 未见重复/坏链；`source_ids` 全解析。

## 6. 专业关系 vs 导航

- 语义卡：**458**（内容 224 + 来源 234）；导航 **26**（MOC 9 + 系统/模板等 17）+ 研究 **5**（含书籍研究 2? graph 口径 5）。
- 可见边：语义 **1663**、导航 **495**；MOC 只做导航、不承载专业事实（无 frontmatter/relations）。
- 语义分量 60（最大 399，单点 59 全为来源）；**不以全图连通率为目标**：导航可达（234 来源经 MOC）≠ 语义接入（370/478 可见对）。
- 专业关系：334（claim 256 / uses_material 34 / in_style 14 / style_interpretation 12 / may_have_part 6 / look_scene 6 / appears_in_look 6）；high 262 / medium 72；无自动 high。

## 7. 适用性覆盖（E1 口径；E3 后复算）

| 维度 | present / 适用 | 状态（APPLICABLE / REVIEW / INSUFFICIENT） |
|---|---:|---|
| garment→component | **16/92（17.4%）** | 0 / 16 / 76 |
| garment→material | **53/92（57.6%）** | 9 / 44 / 39 |
| garment→silhouette（字段） | **74/92（80.4%）** | 74 / 0 / 18 |
| garment→style | **3/92（3.3%）** | 0 / 3 / 89 |
| garment→footwear-accessory | **31/56（55.4%）** | 0 / 31 / 25 |
| garment→outfit | **55/92（59.8%）** | 55 / 0 / 37 |
| LOOK→narrative | **25/35（71.4%）** | 25 / 0 / 10 |
| claim→source | **217/224（96.9%）** | 217 / 0 / 7 |
| **合计（8 维）** | **474/775（61.2%）** | **380 / 94 / 301**（N/A 1017） |

- 说明：E1 eligibility.csv 为 E3 前 308 relations 快照；上表按 E3 新增 26 条 medium 关系更新（present +14 卡、REVIEW +14）复算；`garment_part→material` 另列 **10/35（28.6%）**。
- 来源可见率单列：**370/478（77.4%）**，不与覆盖混算。
- 结论：真实缺口是“有来源但未建/待审关系”，不是分母被非适用卡稀释；不以卡数或全连通率为目标。

## 8. 遗留与风险

| 项 | 状态 |
|---|---|
| 59 isolates / 62 uncited | 59 file + 3 重复来源未分类；不强连 |
| 38 基线 draft（全库 79） | 未提升；零可见 SRC 39 |
| 6 key_garments flags | 仍 review_queue，人工 |
| MOC 覆盖 | **已补齐 224/234（P2 关闭）** |
| 重复来源 URL / 别名冲突 | 3 对 / 6 组（P2/P3） |
| graph 工具误报 | 1 code + 5 EXAMPLE → task-93 修复中 |
| quality_eval | **NOT_RUN**（超时；需稳定环境重跑） |
| GUI/UAT | **NOT_RUN/PENDING**（无截图/签字） |

**总体判定：结构健康、数据完整性 PASS；MOC 覆盖已补齐（P2 关闭）；剩 3 对重复来源 URL 为发布前 P2；不追求全连通率/卡数。**


---

## 9. MOC 更新复核（task-96，2026-11-05 12:02）

- 触发：lead 补齐 P5-C 新卡导航（GAR-0088..91、STR-0027..35、MAT-0015..19、STY-0011..15、LOOK-0024..35、SRC-0530..552）。
- 独立复算：MOC 9 页；**链接 544、unresolved 0**；**内容 224/224、来源 234/234**；无 frontmatter（navigation-only）；validate 仍 **458/458 PASS**、build 234、consistency 0/334。
- 结论：**原 P2-1（MOC 缺 35 内容/23 来源）CLOSED**；P5F-OBSIDIAN-UAT 第 2 项预期改为 **PASS**（仍需人工执行/截图/签字）。
- 仍开放：重复来源 URL 3 对（P2）、别名消歧（P3）、3 张 MAT 前缀 pattern 卡（P3）、92 来源 category 字段（P3）、11 导航零链接（P3）。
