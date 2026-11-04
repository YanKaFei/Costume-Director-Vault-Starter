# P4 变更日志（CHANGELOG-P4）

- 阶段：P4（书籍 / 结构 v1.2 / 组合器 / 视觉 / Macbeth / 许可门禁）
- commit：`7f7a21b`（P4: source audit, books, structure v1.2, outfit composer, visual index, Macbeth validation）
- 快照：399 卡（内容 188 + 来源 211）；45 acceptance；9 composer；11 Macbeth；9 workflow

## 1. 数据字典与规范

| 文件 | 变更 |
|---|---|
| `00-系统/数据字典.md` | v1.1 → **v1.2**：新增「可选字段」说明与指向扩展文件；强调不修改必填/枚举/正文/证据规则，旧卡无需迁移 |
| `00-系统/数据字典-v1.2-扩展.md` | **新增**：42 个向后兼容可选字段（领型/袖型/肩线/腰线/衣摆/长度/版型/松量/裁片/接缝/闭合/门襟/织物组织/厚薄/垂坠/反光/鞋型/鞋跟/鞋面/鞋底/帽/首饰/腰带/手套/携带物等），含类型/适用 type/允许值/用途 |
| `00-系统/来源规范.md` | 补充 SRC 段位（SRC-0520..0524 等）与登记规则 |
| `00-系统/索引.md` | P4 新增卡片/研究笔记入口 |

## 2. 卡片

### 2.1 新增内容卡 22 张（全部 `verified`，含来源与证据边界）
- garment 5：GAR-0083 手套、GAR-0084 高跟鞋、GAR-0085 帽子结构、GAR-0086 胸针结构、GAR-0087 手袋结构；
- garment_part 14：STR-0012 翻领与驳领、STR-0013 装袖与插肩袖、STR-0014 肩线与肩垫、STR-0015 腰线、STR-0016 衣摆与开衩、STR-0017 门襟、STR-0018 纽扣与扣眼、STR-0019 拉链、STR-0020 裁片与拼片、STR-0021 接缝与省道、STR-0022 腰头、STR-0023 袖口、STR-0024 结构属性词表（Fashionpedia）、STR-0025 松量与版型；
- material 3：MAT-0012 织物组织、MAT-0013 克重与垂坠、MAT-0014 反光与金属线。

### 2.2 新增来源卡 14 张
- 9 本 PD 书：SRC-0061（34903 Dress Design）、SRC-0062（21534 Textiles and Clothing）、SRC-0063（33020 English Costume）、SRC-0064（48551 Costume Fanciful）、SRC-0065（49559 Jewellery and Fans）、SRC-0066（76299 Dictionary of Men's Wear）、SRC-0067（56978 Book of the Feet）、SRC-0068（76717 History of Fashion in France）、SRC-0069（46949 Chats on Costume）；
- FreeSewing 2：SRC-0520 缝份与折边加放、SRC-0521 袖山长度适配（MIT，license_status `other_permission` 文档许可映射）；
- V&A 3：SRC-0522 1660s 鹿皮手套、SRC-0523 1590–1670 海狸毡帽、SRC-0524 1770–89 黑缎高跟鞋（link_only）。

### 2.3 旧卡
- **0 修改**（git diff 01–09 无 M 条目）；validate 399/399 PASS。

## 3. 脚本与工具

| 文件 | 变更 |
|---|---|
| `scripts/books_extract.py` | **新增**（Python 标准库）：PG 文本下载/清洗、章节识别、段落编号、术语 hits、词典词条提取、定位输出（章/段/行） |
| `scripts/outfit.py` | **新增**：完整搭配（composer）层，复用 recommend/costume_lib/reco_norm；A/B/C、槽位、连续性 states、证据/SRC、冲突/缺口 warnings；不改旧 CLI |
| `scripts/validate.py` 等旧脚本 | **0 变更**（P4 不修改既有脚本） |

## 4. 文档与验收

| 文件/目录 | 内容 |
|---|---|
| `docs/OUTFIT-COMPOSER.md` | Composer 完整用法/输入/输出/退出码/测试 |
| `docs/VISUAL-REFERENCE.md` | CC0 视觉索引使用说明与许可边界（只存链接、不下载） |
| `11-验收/P4-BOOKS/` | 9 书解析 JSON、TERMS-HITS.md、TERMS-GLOSSARY.md（31 条结论）、README |
| `11-验收/P4-COMPOSER/` | fixtures 9 例、runs、test_outfit.py、SUMMARY/REPORT、回归日志 |
| `11-验收/P4-MACBETH/` | inputs/outputs/query、test_macbeth_p4.py、SUMMARY、P4-MACBETH-COMPARISON、PAIR-RELATIONSHIP |
| `11-验收/P4-VISUAL/` | visual-index.csv（28 条 CC0）、verification-log.csv、README |
| `reports/P4-SOURCE-AUDIT.md` / `P4-LICENSE-MATRIX.csv` | 20 源许可审计与矩阵（P4-0） |
| `reports/P4-BOOKS-INDEX.md` | 9 本书目索引与来源映射 |
| `reports/SOURCES.csv` | 197 → **211 行**数据（+14） |
| `11-验收/P3.5/workflow-runs/*` | 部分 fixture 产物随 workflow/测试重跑更新（非卡片） |

## 5. 回归与验收（P4 commit 后）

- validate 399/399 PASS；build_sources 211/211 PASS；acceptance 45/45；quality_eval 17/17 OVERALL PASS；workflow 9/9；composer 9/9；Macbeth 11/11（均由 verifier 独立复跑）。
- 旧检索指标：relevant@5 4.16 持平、0-hit 0 持平；precision 94.5%→92.9%（−1.6pp，仍 ≥0.8）→ 记录为 WARN，列入 NEXT-PLAN。
- 许可：P4 新增来源均有明确许可依据；受限来源（DeepFashion2/FashionStylist/polyvore/open-pose）未建卡。
