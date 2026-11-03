# 覆盖情况（COVERAGE）— 实际数量 vs P0/P1/P2/P3 目标

- 统计时间：2026-11-04 01:44（Asia/Shanghai）
- 快照：**235 张卡**（内容卡 93 + 来源卡 142）；数据来源：`scripts/validate.py --json`、`scripts/build_sources.py --json` 与逐卡 frontmatter 统计
- 统计口径：`01/02/03/04/05/06/07/09` 八个知识目录下带 YAML frontmatter 的 `.md`；`00-系统/`、`10-提示词模板/`、`11-验收/`、`skills/` 不计入卡片数

## 1. 卡片总量与类型分布

| type | 数量 | verified | interpretive | example |
|---|---|---|---|---|
| garment（单品） | 36 | 35 | 0 | 1 |
| garment_part（结构细节） | 11 | 11 | 0 | 0 |
| material（材料） | 7 | 7 | 0 | 0 |
| pattern（纹样） | 3 | 3 | 0 | 0 |
| style（风格） | 11 | 9 | 1 | 1 |
| period_region（年代地域） | 11 | 11 | 0 | 0 |
| look（造型组合） | 10 | 0 | 9 | 1 |
| scene（剧情场景） | 4 | 0 | 3 | 1 |
| source（来源） | 142 | 142 | 0 | 0 |
| **合计** | **235** | **218** | **13** | **4** |

- `unverified`：0；`review_status: draft` 37 张（全部 PRD/STY/LOOK/SCN 与 example 卡），`reviewed` 198 张。
- `license_status`：`not_applicable` 95、`link_only` 82、`other_permission` 41、`cc0` 14、`cc_by` 3；`unknown` 0。
- 每张 verified 内容卡平均引用 1.33 个来源（共 76 张 verified 内容卡、126 条引用）。

## 2. 与 P0/P1/P2/P3 目标对照

| 阶段目标 | 目标值 | 实际 | 结论 | 备注 |
|---|---|---|---|---|
| P0 架构：字典/模板/索引/来源规范/来源登记/检索工具/最小测试/≥5 卡 | 全部 | 字典 v1.1、模板、索引、来源规范、来源登记 142、validate/query/recommend、18 例测试、235 卡 | **PASS** | 模板未同步 v1.1（见 QA §6.6） |
| P1 高质量卡总数 | ≥80 | 235（内容卡 93 + 来源 142） | **PASS** | 只计内容卡 93 亦 ≥80 |
| P1 单品 | ≥30 | **36**（35 正式 + 1 example） | **PASS** | +20% |
| P1 结构 | ≥10 | **11** | **PASS** | |
| P1 材质/纹样 | ≥10 | **10**（7 material + 3 pattern） | **PASS**（数量） | 族系覆盖窄，见 §3.C |
| P1 风格 | ≥10 | **10** 正式（9 verified + 1 interpretive）+ 1 example | **PASS** | 6 个 style_family 全覆盖 |
| P1 时代/地域 | ≥10 | **11** | **PASS** | 1930s 上海民国新增 |
| P1 Look/场景 | ≥10 | **14**（10 look + 4 scene） | **PASS**（数量） | 完整拆解口径见 §4 |
| P2 query/recommend/三模板/≥15 例测试 | 全部 | query.py + recommend.py + 3 模板（另 1 汇总页）+ **18 例** | **PASS** | 18/18 PASS，exit 0；query 多词 bug 见 QA §4.3 |
| P2 多场次连续性 | ≥1 | T03（3 场）、T17（4 场） | **PASS** | `same_item_ids=True`、`locks_in_every_prompt=True` |
| P2 skills 调用说明 | 1 | `skills/costume-director/SKILL.md`（13 KB） | **PASS** | |
| P3 有效卡片 250+ | ≥250 | **235 总卡**（内容卡 93） | **PARTIAL** | 按总卡数差 15；按“内容卡”口径差 157；来源卡 142 是否计入 250+ 需 lead 裁定 |
| P3 高价值薄弱分支扩充 | — | 部分 | **PARTIAL** | 见 §3 缺口 |

## 3. 分类维度 A–F 细分覆盖

### A. 物理单品（garment 36 张，10 个 category）

| category | 数量 | 备注 |
|---|---|---|
| upper_body 上装 | 7 | shirt/blouse/knitwear/vest 等 |
| lower_body 下装 | 4 | trousers/skirt 等 |
| one_piece 连身 | 6 | 含 `GAR-0031 旗袍`、`GAR-0032 长衫`、`GAR-0001 和服` |
| outerwear 外层 | 5 | suit_jacket/coat/parka/trench 等 |
| inner_layer 内层 | 2 | shift/petticoat 类 |
| footwear 足部 | 4 | 含 `GAR-0035 女式皮鞋` |
| headwear 头部 | 3 | hat/cap/fez 类 |
| accessory 配饰 | 2 | |
| specialised 专门类型 | 3 | 传统地域/戏曲制服类 |
| **carried_prop 携带物** | **0** | **缺口**：包袋/伞/手杖等 §2 A 明确列出的类别尚未建卡 |

### B. 结构与形态（11 张，16 个 part_family 中覆盖 6 类）

| part_family | 数量 |
|---|---|
| collar | 3 |
| support | 3 |
| sleeve | 2 |
| ornament | 1 |
| placket | 1 |
| closure | 1 |

**缺口（0 张）**：`neckline`、`shoulder`、`pocket`、`waistline`、`pleats`、`vent`、`seam`、`length`、`layering`、`silhouette`（10 个族系为空）。

### C. 材质/纹样（10 张）

- `material_family`：`dye` 3、`trim` 2、`fiber` 1、`textile` 1；**缺口**：`leather`、`fur`、`metal`、`finish` 为 0。
- `pattern_family`：仅 `geometric` 3；**缺口**：`floral`、`animal`、`abstract`、`figurative`、`stripe`、`check`、`paisley`、`border`、`allover`、`placement` 为 0。

### D. 风格（11 张，6 个 style_family 全覆盖）

| style_family | 数量 |
|---|---|
| historical_style | 3 |
| cinematic_genre | 4 |
| art_movement | 1 |
| occupational | 1 |
| subculture | 1 |
| fictional_world | 1 |

### E. 时代/地域（11 张 period_region 卡；全库 periods/regions 标签）

- 全库 `periods` 标签 55 个：19th_century 19、16th_century 12、contemporary 12、20th_century 12、18th_century 15、17th_century 10、1930s 10、1890s 7、republican_era 7 等；**1930s 上海/民国**由 `GAR-0031..0035`、`PRD-0011`、`LOOK-0008/0009`、`SCN-0004` 补入。
- 全库 `regions` 标签 41 个：欧洲/英美为主（europe 38、united_states 31、britain 24、france 14、england 7），东亚仅 japan 3、china 7、hong_kong 1；**南美、撒哈拉以南非洲（除 west_africa/senegal/mali/ghana）、南亚（1）、大洋洲为缺口**。
- 11 张 period_region 卡覆盖：1770s、1790–1810、1890s、1920s、1930s、1940s、1950s、1960s、奥斯曼晚期、拜占庭晚期、1930s 上海民国。

### F. Look 与连续性（10 look + 4 scene）

- 10 张 Look 全部由 ≥3 个具体 GAR/STR/MAT ID 组成（无散文式 Look）；1 张 example。
- 每张 Look 的五槽（上装 / 下装或连身 / 外层 / 鞋 / 配饰）严格覆盖如下：

| Look | 单品数 | 五槽满足（严格） | 说明 |
|---|---|---|---|
| LOOK-0001 洛可可沙龙女主人 | 6 | 4/5 | 连身 + 配件 + 鞋 + 材质；无外层 |
| LOOK-0002 摄政时期乡间日装 | 6 | 3/5 | 内层 + 外层 + 头饰 + 鞋 + 材质；无上装/下装类目 |
| LOOK-0003 十六世纪宫廷男装 | 5 | 3/5 | 上装 + 下装 + 鞋 + 结构；缺外层/配饰 |
| LOOK-0004 奥斯曼晚期官员 | 4 | 4/5 | 连身 + 头饰 + 鞋 + 材质 |
| LOOK-0005 1900 南方庄园女主人 | 7 | 4/5 | 上装 + 下装 + 内层 + 头饰 + 鞋 + 结构 + 材质；缺外层 |
| LOOK-0006 1977 伦敦朋克青年 | 5 | 4/5 | 上装 + 下装 + 外层 + 鞋 + 结构；缺配饰槽 |
| LOOK-0007 当代雨夜调查者连续性 | 4 | 4/5 | 上装 + 下装 + 外层 + 鞋；缺配饰槽 |
| LOOK-0008 1930s 上海长衫知识分子 | 3 | 2/5 | 连身 + 上装 + 结构；缺外层/鞋/配饰 |
| LOOK-0009 1930s 上海旗袍女性知识分子 | 3 | 3/5 | 连身 + 结构 + 鞋；缺外层/配饰 |
| LOOK-EXAMPLE-001 雨夜调查者（示例） | 3 | 3/5 | 上装 + 下装 + 鞋 |
| **合计** | — | **0/10 全五槽；5/10 达四槽** | 全部 ≥3 个具体 ID |

- 目标「至少 6 套完整拆解」的判定依赖口径：
  - 严格五槽全覆盖 → **0/10，未达标**；
  - 四槽以上 → 5/10，仍未达 6；
  - 若按「连身可替代上装+下装，外层/配饰按场景可选」的实际设计口径 → 10/10 均可拆解。
  建议 lead 明确验收口径；本轮不将其判为 PASS。
- 场景卡 4 张（SCN-0001..0004）；多场次连续性由 T03（3 场）/T17（4 场）验收用例覆盖并通过。
- 连续性字段：LOOK-0007 有 wetness/damage/dirt/accessories 状态表；T03/T17 每场次锁定同组 `item_ids`。

## 4. 来源包覆盖（142 张）

| 段位 | 数量 | 建立者/用途 |
|---|---|---|
| SRC-0001..0060 | 60 | researcher 来源包（含 19 张 Getty AAT、Met 对象、FIT 等） |
| SRC-0100..0149 | 50 | P1 单品/结构/材质自建 |
| SRC-0150..0175（缺 0164） | 25 | P1 风格/时代/Look 自建 |
| SRC-0200..0206 | 7 | 1930s 上海民国补卡（P3/P4 段位） |

- 被内容卡引用：**83 张 / 142（58.5%）**；**59 张未被引用（41.5%）**，其中包含**全部 19 张 Getty AAT 来源卡**与多数 FIT 个案/Met 对象卡（researcher 来源包未接入内容卡证据链）。
- 引用次数：126；平均每张 verified 内容卡 1.33 个来源。
- 重复 URL 3 组（3 组共 6 张卡去重后应为 139 个唯一页面）：`SRC-0115/SRC-0157`、`SRC-0036/SRC-0175`、`SRC-0022/SRC-0163`；后两组各有一张未被引用。
- `source_kind` 分布：`academic_reference` 72、`controlled_vocabulary` 19（非法值）、`museum_collection` 13、`museum_object_record` 11（非法值）、`institutional_blog` 6（非法值）、`image_repository` 5、`garment_analysis` 4（非法值）、其他 12。→ 49 张越界（见 QA §1.3）。
- SRC 编号缺口：`SRC-0164` 缺失（不连续）；`0061..0099`、`0176..0199` 为段位预留空档。

## 5. 测试与模板覆盖（P2）

| 项 | 状态 |
|---|---|
| `scripts/query.py` | 存在；单词/字段过滤可用；**引号多词恒 0 命中**（QA §4.3） |
| `scripts/recommend.py` | 存在；3 套 Look + 评分 + prompt + 风险 + 证据；historical/inspired/fictional 区分 |
| `scripts/validate.py` / `scripts/build_sources.py` | 本轮新增，见 QA §1–§2 |
| `10-提示词模板/` | `01-角色设计模板.md`、`02-静态生图提示词模板.md`、`03-视频提示词模板.md`（3 个必需）+ `人物与视频模板.md`（重复汇总页，建议合并或标注） |
| `11-验收/测试结果/` | 18 个用例 MD + 36 个 raw JSON + SUMMARY（18/18 PASS） |
| 测试类型覆盖 | 历史准确 T01、艺术化对照 T02/T16、现代现实主义 T15/T18、阶层变化 T10/T11、舞蹈动作 T04/T12、雨夜湿衣 T03/T09、冷暖光 T07/T08、多场次连续性 T03/T17、低预算 T06/T13、虚构 T05、冬季安全 T14、1920s 爵士 T12、年代剧复用 T13 —— TASK §5 P2 要求类型全部覆盖 |
| `skills/costume-director/SKILL.md` | 存在（13 KB，含脚本用法） |

## 6. 结论：达标与缺口

**达标**
- P0/P1/P2 的数量型目标全部达到；18 例测试 PASS；多场次连续性、证据抽查、SOURCES.csv 重建通过。
- 235 张卡中 218 张 verified、0 unverified；0 YAML 错误、0 重复 ID、0 坏链、0 内嵌图片。

**缺口（按价值排序）**
1. **P3 250+ 目标未达**：总卡 235（差 15）；若按内容卡口径 93（差 157）。
2. **来源 ↔ 内容卡证据链**：59/142 来源卡未被引用（含全部 AAT 卡），researcher 来源包与内容卡未打通。
3. **分类缺口**：`carried_prop` 0；结构 10 个族系为 0；材质/纹样族系窄（material 仅 4/8、pattern 仅 1/11）。
4. **Look 完整拆解**：严格五槽 0/10，四槽 5/10；「至少 6 套」需口径裁定。
5. **人工复核缺口**：37 张 `review_status: draft`（全部 PRD/STY/LOOK/SCN）。
6. **来源卡 schema 不一致**：49 张 `source_kind` 越界；3 处列表数字未加引号；模板未同步字典 v1.1。
7. **query.py 多词检索缺陷**：引号多词 0 命中，18 例验收的 query 证据为空。

## 7. 下一步建议（按优先级）

1. 修复 `query.py` 多词 split 并在验收中增加「query 命中 ≥1」断言后重跑 18 例。
2. 统一 `source_kind`（字典扩枚举或归一并回写 49 张卡）；同步更新 `00-系统/卡片模板.md` 到 v1.1。
3. 把 19 张 AAT 与高价值未被引用来源接入相应内容卡（或标注「保留备用」），提高来源利用率。
4. 补 `carried_prop`（包袋/伞/手杖）与结构族系（领口/肩线/口袋/腰线/褶裥/缝线/长度）卡片。
5. 明确 Look「完整拆解」验收口径，补齐缺失槽位或调整目标。
6. 人工复核 37 张 draft 卡后改 `review_status`。
