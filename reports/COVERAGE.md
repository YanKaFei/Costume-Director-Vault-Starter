# 覆盖情况（COVERAGE）— P3.1 终态

- 更新时间：2026-11-04 02:51；快照 **328 卡**（内容 154 + 来源 174）；**41 例验收**；git HEAD `0345f05` + P3.1 工作区修改
- 完整报告：[P3-COVERAGE.md](P3-COVERAGE.md)；本页为摘要

## 1. 总量

| 指标 | P2.5 | P3 | **P3.1（终态）** | 目标 | 结论 |
|---|---|---|---|---|---|
| 总卡 | 235 | 328 | **328** | P3 ≥250 | **PASS** |
| 内容卡 | 93 | 154 | **154** | — | — |
| 来源卡 | 142 | 174 | **174** | — | — |
| 验收用例 | 18 | 30 | **41** | ≥15 | **PASS 41/41** |
| verified | 218 | 282 | **282** | — | — |
| draft | 37 | 62 | **62** | 0（人工复核后） | HUMAN_UAT_PENDING |

## 2. 类型分布（不变）

garment 71、garment_part 11、material 8、pattern 3、style 11、period_region 11、look 23、scene 16、source 174。

## 3. 关键覆盖事实

- **carried_prop 0→3**（雨伞/手提包/手杖）；职业服（护士/医生/警察/厨师/消防/军装）、雨具（风衣/雨衣）、跨文化传统服（和服/韩服/纱丽/agbada/gele/科普特/文艺复兴）已补。
- **最大缺口**：pattern 1/11 族、material 4/8 族（leather/fur/metal/finish 缺）、garment_part 6/16 族；lower_body 4、inner_layer 2 偏薄；period_region/style 各 11 未再扩充。
- **来源**：174 张；被引用 114；未引用 60（含全部 19 张 AAT）；平均 1.22 来源/verified 内容卡；3 组重复 URL 已标 canonical；`SOURCES.csv` 174 行（P3.1 QA 重建）。
- **测试**：30→41；新增 T31–T41 覆盖职业匹配/雨具/室内派克/context/查询排序与去重（全部 PASS）。
- **Look/Scene**：look 23（全部 ≥3 具体 ID）、scene 16；身份弧线/连续性由 warning 声明未建模。
