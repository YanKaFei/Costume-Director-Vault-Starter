# P3 覆盖报告（COVERAGE）

- 统计时间：2026-11-04 03:12（Asia/Shanghai，P3.2 最终复验后）
- 快照：**328 张卡**（内容 154 + 来源 174）；git HEAD `281e3b1`（P3.2）；**45 例验收**
- 口径：`01/02/03/04/05/06/07/09` 下带 frontmatter 的 `.md`；`00-系统/`、`10-提示词模板/`、`11-验收/`、`skills/` 不计入
- 数据来源：本人 frontmatter 全量统计 + `validate.py`（328/328 PASS）+ `build_sources.py`（174/174 一致）

## 1. 总量与阶段目标

| 指标 | P2.5 | **P3** | 目标 | 结论 |
|---|---|---|---|---|
| 总卡数 | 235 | **328** | P3 ≥250 | **PASS（+93）** |
| 内容卡 | 93 | **154** | — | +61 |
| 来源卡 | 142 | **174** | — | +32（SRC-0400..0431） |
| verified | 218 | **282** | — | +64 |
| interpretive | 13 | **42** | — | +29 |
| example | 4 | 4 | — | 0 变化 |
| `review_status: draft` | 37 | **62** | 0（人工复核后） | HUMAN_UAT_PENDING |

## 2. 类型分布（P3）

| type | P2.5 | **P3** | 变化 |
|---|---|---|---|
| garment | 36 | **71** | +35 |
| garment_part | 11 | 11 | 0 |
| material | 7 | **8** | +1 |
| pattern | 3 | 3 | 0 |
| style | 11 | 11 | 0 |
| period_region | 11 | 11 | 0 |
| look | 10 | **23** | +13 |
| scene | 4 | **16** | +12 |
| source | 142 | **174** | +32 |
| **合计** | 235 | **328** | +93 |

## 3. 单品按 category（garment 71）

| category | P2.5 | **P3** | 说明 |
|---|---|---|---|
| upper_body | 7 | 8 | 新增厨师服等 |
| lower_body | 4 | 4 | 未扩充 |
| one_piece | 6 | **20** | 护士/警察/Utility/鸡尾酒裙/科普特/文艺复兴/纱丽/韩服/和服/agbada 等 |
| outerwear | 5 | **11** | 风衣/雨衣/医生白袍/军装外套/消防防护外套/Courrèges 外套 |
| inner_layer | 2 | 2 | 未扩充 |
| footwear | 4 | **7** | 医疗工作鞋/1930s 男鞋/1970s 厚底鞋/牛津鞋 |
| headwear | 3 | **6** | 安全头盔等 |
| accessory | 2 | **6** | 制服徽章/朋克徽章/和服腰带等 |
| **carried_prop** | **0** | **3** | **缺口已补**：雨伞/手提包/手杖 |
| specialised | 3 | 4 | 和服/惠皮尔等 |

## 4. 其它维度

- **结构（11 张）**：仍覆盖 6/16 个 `part_family`（collar 3、support 3、sleeve 2、ornament/placket/closure 各 1）；neckline/shoulder/pocket/waistline/pleats/vent/seam/length/layering/silhouette 仍为 0。
- **材质（8 张）**：`fiber` 1、`textile` 2、`dye` 3、`trim` 2；`leather/fur/metal/finish` 仍为 0（4/8 族）。
- **纹样（3 张）**：仍仅 `geometric` 3（1/11 族：floral/animal/abstract/figurative/stripe/check/paisley/border/allover/placement 均缺）。
- **风格（11 张）/时代地域（11 张）**：P3 未扩充；6 个 style_family 仍全覆盖。
- **Look（23 张）**：全部 `look_items` ≥3 个具体 ID；新增跨文化（加纳婚礼、伦敦中国云肩、南亚纱丽）、身份弧线（LOOK-0017/0015）、太空站（LOOK-0011）、1930s 上海雨夜（LOOK-0012）、当代雨夜四场连续性（LOOK-0021）。
- **场景（16 张）**：新增加纳婚礼、急诊、太空等场景卡。

## 5. 来源包（174）

| 段位 | 数量 | 说明 |
|---|---|---|
| SRC-0001..0060 | 60 | researcher 来源包 |
| SRC-0100..0149 | 50 | P1 单品/结构/材质 |
| SRC-0150..0175（缺 0164） | 25 | P1 风格/时代/Look |
| SRC-0200..0206 | 7 | 1930s 上海 |
| **SRC-0400..0431** | **32** | **P3 新增**：V&A/Met 职业服、雨具、徽章、Utility、跨文化服饰等 |

- 被内容卡引用：**114/174**；未被引用 **60 张**（含全部 19 张 Getty AAT 及部分 P3 来源）。
- 平均每张 verified 内容卡引用 **1.22** 个来源（P2.5 1.32）。
- 重复 URL 3 组（canonical 已标注）：SRC-0115/SRC-0157、SRC-0022/SRC-0163、SRC-0036/SRC-0175。
- `reports/SOURCES.csv`：P3 提交时未同步（142 行）→ QA 已重建为 **174 行 + 表头**；`build_sources --check` PASS。
- 新增 32 个来源 URL 全部 HTTP 200 且页面内容与卡名吻合（见 P3-QA §3.3）。

## 6. 覆盖矩阵（TASK §2 A–F vs P3 实际）

| 维度 | 覆盖情况 | 结论 |
|---|---|---|
| A 物理单品 | 10/10 category 均有卡（carried_prop 3） | 达标（深度不均：lower_body 4、inner_layer 2 偏薄） |
| B 结构与形态 | 6/16 part_family | 缺口（10 族为 0） |
| C 属性/材质纹样 | material 4/8 族、pattern 1/11 族 | **明显缺口** |
| D 风格 | 6/6 style_family、11 张 | 达标（未扩充） |
| E 时空与剧情 | style/period 各 11；scene 16 | 达标（地域/年代未新增） |
| F Look 与连续性 | look 23（全部可拆解）、连续性与状态表 | 达标（叙事弧线仍由警告声明未建模） |
| P3 250+ 有效卡 | **328** | **PASS** |

## 6.1 P3.1 复验变化（2026-11-04 02:48）

- **卡片数量不变**：328（内容 154 + 来源 174）；P3.1 只修 M1/M2 与和服去重提示，未新增卡片。
- **测试 30 → 41**：新增 T31–T41 覆盖职业匹配（护士/医生/警察/厨师/太空/婚礼）、雨具选择、室内禁极地派克、context 清洁、query 排序/去重。
- **SOURCES.csv**：因 SRC-0046/47 许可修正再次漂移（2 行）→ QA 重建 174 行；来源总数与被引用数不变（174 / 114 / 未引用 60）。
- **缺口不变**：pattern 1/11 族、material 4/8 族、garment_part 6/16 族；62 张 draft；19 张 AAT 未接入仍为最大来源缺口。

## 7. 结论与剩余缺口（按价值）

1. **已达 P3 体量目标**（328 ≥ 250），carried_prop 与职业/雨具/跨文化分支得到实质补充。
2. **最大覆盖缺口**：pattern（1/11 族）、material（4/8 族）、garment_part（6/16 族）、lower_body/inner_layer 偏薄。
3. **来源利用**：60/174 来源未引用（AAT 19 张仍未接入），平均引用 1.22 偏低。
4. **人工复核**：62 张 draft（新增卡多为 draft），需人工复核后方可视为完成。
5. 报告一致性：SOURCES.csv 已由 QA 重建；后续每次扩卡必须重新生成 CSV（已列入 NEXT-PLAN）。


## 6.2 P3.2 最终复验（2026-11-04 03:12）

- 卡片/来源数量不变：**328 卡（内容 154 + 来源 174）**；P3.2 仅改 scripts/tests 与 query 策略，无新增卡片。
- **测试 41 → 45**：新增 T42 巡警、T43 医师、T44 宇航员、T45 民警同义词职业匹配（`occupation_match`/`no_occupation_mismatch`/`no_cultural_mispick`）。
- `SOURCES.csv`：P3.2 commit 已同步（`build_sources --check` PASS，174 行）；3 组重复 URL 仍为 canonical 交叉引用。
- 来源覆盖不变：174 张；被引用 114；未引用 60（含 19 张 AAT）；平均 1.22 来源/verified 内容卡。
- 缺口不变：pattern 1/11 族、material 4/8 族、garment_part 6/16 族；62 张 draft。
- 查询层新增：example 卡默认排除（`--include-example` 可恢复）、区域意图加权（和服/旗袍/纱丽/gele 等）——P14 已无 example、P02 无重复和服。
