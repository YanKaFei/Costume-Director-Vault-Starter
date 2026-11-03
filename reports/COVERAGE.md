# 覆盖情况（COVERAGE）— P3 终态

- 更新时间：2026-11-04 02:44；快照 **328 卡**（内容 154 + 来源 174），git HEAD `0345f05`
- 完整报告：[P3-COVERAGE.md](P3-COVERAGE.md)（类型/category/来源/覆盖矩阵/缺口）；本页为摘要

## 1. 总量与目标

| 指标 | P2.5 | P3 终态 | 目标 | 结论 |
|---|---|---|---|---|
| 总卡 | 235 | **328** | P3 ≥250 | **PASS** |
| 内容卡 | 93 | **154** | — | +61 |
| 来源卡 | 142 | **174** | — | +32 |
| verified | 218 | **282** | — | +64 |
| 30 例验收 | 18 | **30** | ≥15 | **PASS 30/30** |

## 2. 类型分布（P3）

garment **71**、garment_part 11、material **8**、pattern 3、style 11、period_region 11、look **23**、scene **16**、source **174**。

## 3. 分类覆盖（摘要）

- **A 单品**：10/10 category 均有卡；**carried_prop 0→3**（雨伞/手提包/手杖）；职业服/雨具/跨文化传统服新增。
- **B 结构**：11 张，覆盖 6/16 part_family；neckline/shoulder/pocket/waistline/pleats/vent/seam/length/layering/silhouette 仍为 0。
- **C 材质/纹样**：material 8（4/8 族：fiber/textile/dye/trim；leather/fur/metal/finish 缺）；pattern 3（仅 geometric，1/11 族）——**最大覆盖缺口**。
- **D 风格**：11 张、6/6 style_family；P3 未扩充。
- **E 时空剧情**：period_region 11；scene 16（新增急诊、空间站、加纳婚礼等）。
- **F Look/连续性**：look 23（全部 ≥3 具体 ID）；新增身份弧线/跨文化/太空站/1930s 上海雨夜/当代四场连续性；身份弧线未建模由 warning 声明。
- **来源**：174 张；被引用 114；60 张未引用（含全部 19 张 AAT）；平均 1.22 来源/verified 内容卡；3 组重复 URL 已标 canonical。
- **draft**：62 张待人工复核。

## 4. 缺口优先级

1. pattern 族系（1/11）、material 族系（4/8）、garment_part 族系（6/16）。
2. lower_body（4）/inner_layer（2）偏薄；period/style 未扩充。
3. 60 张来源未引用（AAT 优先接入）。
4. 62 张 draft 人工复核（HUMAN_UAT_PENDING H4）。
