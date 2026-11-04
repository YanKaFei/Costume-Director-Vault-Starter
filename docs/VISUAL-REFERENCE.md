# 视觉参考索引使用指南（Met CC0 原型）

- 状态：**PROTOTYPE（P4-4）**；28 条 Met 对象，逐件 `isPublicDomain=true`，只存链接、不下载、不内嵌图片。
- 主索引：`11-验收/P4-VISUAL/visual-index.csv`；核验记录：`11-验收/P4-VISUAL/verification-log.csv`；说明：`11-验收/P4-VISUAL/README.md`。
- 本文件面向导演/服装设计/美术/摄影：**怎么用**、**怎么引用**、**什么不能做**。

## 1. 这是什么

一个可检索的博物馆视觉参考索引：每条记录 = 一件 Met 藏品的对象 ID、年代、文化、类别、metadata 级结构信息、检索关键词、CC0 状态、官方图像链接、对象页链接，以及可回链的知识库卡 ID（GAR/STR/PRD/STY 等）。

它解决的是“设计讨论时找可信、可许可、可溯源参考”的问题，**不是**图库下载站，也不是对“某件衣服长什么样”的完整结构档案（因为原型不下载图片，结构字段只来自 API 元数据）。

## 2. 快速使用

1. 用表格软件/`grep` 打开 `visual-index.csv`，按 `keywords_zh`/`keywords_en`、`date`、`culture`、`classification` 过滤。
2. 找到候选后，先打开 `object_url` 人工核对图像与描述；`image_url` 仅用于浏览器查看或生成工具的**外部输入**（不要上传/再分发）。
3. 需要结构化设计语言时，用 `related_card` 跳到对应知识库卡（如 `GAR-0008` 马甲、`STR-0007` 臀垫、`STY-0001` 新古典主义）；卡内的 `prompt_en`/结构/适用条件比视觉索引更细。
4. 需要“证据三分”时，回到 `04-来源/` 的 SRC 卡（有 SRC 的 13 条）或 `EVIDENCE.md` 类文档；`source_id=MET-API` 的条目以 object_id 为锚，不伪造 SRC。

## 3. 代表性条目（10 条，全部已在 CSV 中）

| visual_id | Met objectID | 对象 | 年代/文化 | 适合参考的卡 | 用途示例 |
|---|---|---|---|---|---|
| VIS-0002 | 108233 | Mourning dress | ca. 1867 / American | `STY-0002` 维多利亚丧服 | 丧服场次的深色层搭与裙长 |
| VIS-0003 | 125953 | Kimono | 19th c. / Japan | `GAR-0001` 和服 | 和服廓形、腰带层次、面料纹样 |
| VIS-0004 | 157760 | Waistcoat | 1780–1800 / French | `GAR-0008` 马甲 | 18 世纪男装内层与门襟 |
| VIS-0005 | 157943 | Dress | ca. 1885 / American | `STR-0007` 臀垫 | 1880s 臀部体积与裙撑结构 |
| VIS-0006 | 158100 | Corset | ca. 1890 / French | `PRD-0003` 1890s 语境 | 直裁胸衣/塑形轮廓 |
| VIS-0008 | 159244 | Dress | ca. 1855 / American | `STR-0008` 笼式裙撑 | crinoline 时代的外轮廓 |
| VIS-0010 | 475116 | Tunic | 4th–7th c. / Coptic | `GAR-0061` 科普特束腰长袍 | 早期中世纪/晚期古代束腰长袍层搭 |
| VIS-0011 | 81132 | Waistcoat | 1615–20 / British | `GAR-0008` 马甲 | 17 世纪早期马甲与装饰 |
| VIS-0012 | 83189 | Dress | 1804–14 / French | `STY-0001` 新古典主义 | 高腰、轻薄棉质、柱状轮廓 |
| VIS-0023 | 156206 | Boots | 1780–95 / European | `GAR-0022` 威灵顿靴 | 18 世纪皮靴形制与靴筒 |

## 4. 许可与引用边界

**可以做**：

- 在浏览器打开 `object_url` 查看对象页与图像；
- 引用对象页 URL 与 Met 官方署名；
- 在注明“参考（reference）”的前提下，用 `related_card` 与 CSV 字段支持设计讨论；
- 把 `image_url` 作为外部工具输入（若该工具条款允许），但本 Vault 不存储、不再分发图片。

**不可以做**：

- ❌ 把 `image_url` 复制/下载进 Vault、附件、PPT 或生成式服务；
- ❌ 把 `image_url` 当作许可凭证；许可判断以 `object_url` 的 Met Open Access 说明与 `isPublicDomain` 为准；
- ❌ 批量抓取、镜像、热链或转售图像；
- ❌ 把 `source_id=MET-API` 写成 `SRC-xxxx`（尚未建卡）；
- ❌ 把 `structure_features` 当作完整结构档案（它只来自 API 元数据，未做图像鉴定）；
- ❌ 把本索引条目当作“某角色实际穿着过的服装”证据。

**建议引用格式**：

> The Metropolitan Museum of Art, *[Title]*, [Date], [Object ID]. https://www.metmuseum.org/art/collection/search/[objectID] (Met Open Access; isPublicDomain=true, accessed 2026-11-04)

## 5. 与知识库结合的工作流

1. **角色/场次约束** → 从 Look/Scene 卡确定年代、地域、阶层、动作与气候。
2. **找视觉参考** → CSV 按 `keywords_zh` 与 `date` 过滤，选 2–3 个候选，打开 `object_url` 人工核对。
3. **回到结构** → 用 `related_card` 跳到 GAR/STR/MAT/PRD/STY 卡，读取结构要点、适用/不适用条件、prompt 片段。
4. **写进分镜/置装单** → 引用 `visual_id` + `object_url` + 卡 ID；不复制图像。
5. **复核许可** → 记录 `public_domain_verified` 与访问日期；如需对外发布，另做独立权利审查。

## 6. 已知限制

- 仅 Met 一个馆；V&A/FIT 等尚未纳入（V&A 多为 link_only，需逐件核验）。
- 结构字段为 metadata-only；领型、袖型、版型等需要人工看图补充，标 `visual_reviewed` 后再用于强断言。
- `classification` 多为 Costume Institute 空值，用 `department / objectName` 派生，不是 Met 原始分类。
- 15/28 条暂无 `SRC-` 来源卡（`source_id=MET-API`），待来源组统一建卡后可升级。
- 图像 URL 可能限流/超时；verification-log 记录 2026-11-04 的实际状态，不保证长期可用。
- 跨馆/跨许可的统一索引尚未建立；不要把本原型作为法律意见。

## 7. 相关文件

- `11-验收/P4-VISUAL/README.md` — 方法、字段、核验结果与缺口
- `11-验收/P4-VISUAL/visual-index.csv` — 28 条主索引
- `11-验收/P4-VISUAL/verification-log.csv` — 逐条 HTTP/PD 状态
- `11-验收/P3.5/Macbeth/` — 18 套造型案例（视觉参考可服务于该类叙事设计）
