# 覆盖情况（COVERAGE）— P3.2 终态

- 更新时间：2026-11-04 03:14；快照 **328 卡**（内容 154 + 来源 174）；**45 例验收**；git HEAD `281e3b1`
- 完整报告：[P3-COVERAGE.md](P3-COVERAGE.md)；本页为摘要

## 1. 总量

| 指标 | P2.5 | P3 | **P3.1** | **P3.2（终态）** | 目标 | 结论 |
|---|---|---|---|---|---|---|
| 总卡 | 235 | 328 | 328 | **328** | P3 ≥250 | **PASS** |
| 内容卡 | 93 | 154 | 154 | **154** | — | — |
| 来源卡 | 142 | 174 | 174 | **174** | — | — |
| 验收用例 | 18 | 30 | 41 | **45** | ≥15 | **PASS 45/45** |
| verified | 218 | 282 | 282 | **282** | — | — |
| draft | 37 | 62 | 62 | **62** | 0（人工复核后） | HUMAN_UAT_PENDING |

## 2. 类型分布（不变）

garment 71、garment_part 11、material 8、pattern 3、style 11、period_region 11、look 23、scene 16、source 174。

## 3. 关键事实

- carried_prop 3；职业服/雨具/跨文化传统服已补；**pattern 1/11 族、material 4/8 族、garment_part 6/16 族仍为最大缺口**；lower_body 4、inner_layer 2 偏薄。
- 来源 174：被引用 114、未引用 60（含 19 张 AAT）；平均 1.22 来源/verified 内容卡；3 组重复 URL canonical；`SOURCES.csv` 174 行（P3.2 已同步）。
- 测试 45：新增 T31–T45（职业匹配含同义词、雨具、室内派克、context、查询排序/去重/example 排除）。
- Look 23（全部 ≥3 具体 ID）、scene 16；身份弧线/连续性由 warning 声明未建模。
