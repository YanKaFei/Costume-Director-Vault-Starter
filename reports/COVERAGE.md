# 覆盖情况（COVERAGE）— P3.3 终态

- 更新时间：2026-11-04 03:26；快照 **343 卡**（内容 158 + 来源 185）；**45 例验收**；git HEAD `fcebf79`
- 完整报告：[P3-COVERAGE.md](P3-COVERAGE.md)；本页为摘要

## 1. 总量

| 指标 | P2.5 | P3 | P3.1 | P3.2 | **P3.3（终态）** | 目标 | 结论 |
|---|---|---|---|---|---|---|---|
| 总卡 | 235 | 328 | 328 | 328 | **343** | P3 ≥250 | **PASS** |
| 内容卡 | 93 | 154 | 154 | 154 | **158** | — | — |
| 来源卡 | 142 | 174 | 174 | 174 | **185** | — | — |
| 验收用例 | 18 | 30 | 41 | 45 | **45** | ≥15 | **PASS 45/45** |
| verified | 218 | 282 | 282 | 282 | **297** | — | — |
| draft | 37 | 62 | 62 | 62 | **62** | 0（人工复核后） | HUMAN_UAT_PENDING |

## 2. 类型分布

garment **75**、garment_part 11、material 8、pattern 3、style 11、period_region 11、look 23、scene 16、source **185**。

## 3. 关键事实

- P3.3 新增：GAR-0071 莫卧儿 jama、GAR-0072 帕贾马裤、GAR-0073 维多利亚哀悼珠宝、GAR-0074 哀悼戒指与胸针；SRC-0450..0460 共 11 张 V&A 来源（11/11 HTTP 200）。
- carried_prop 3；职业服/雨具/跨文化传统服已补；**pattern 1/11 族、material 4/8 族、garment_part 6/16 族仍为最大缺口**；lower_body 5、inner_layer 2 偏薄。
- 来源 185：被引用 125、未引用 60（含 19 张 AAT）；`SOURCES.csv` 186 行（R5 质量门有效）。
- 测试 45：T31–T45 覆盖职业匹配（含同义词）、雨具、室内派克、context、查询排序/去重/example 排除。
- Look 23（全部 ≥3 具体 ID）、scene 16；身份弧线/连续性由 warning 声明未建模。


## 4. P3.6 更新（2026-11-04 15:56）

- 卡片/来源覆盖不变：**363 卡（内容 166 + 来源 197）**；`reports/SOURCES.csv` 198 行。
- 新增与验收相关资产（不计入卡片覆盖）：`.dsh/skills/costume-director/SKILL.md`、`docs/SKILL-USAGE.md`、`projects/` 用户隔离区、`11-验收/P3.6/`（smoke/e2e/导演材料）、`scripts/check_skill_e2e.py`。
- 验收用例保持 **45**；workflow tests **9**；e2e **10**（T01–T10，全部通过独立审计）。
- 覆盖缺口不变：pattern 1/11 族、material 4/8 族、garment_part 6/16 族；62 draft（45 REVIEWED-CANDIDATE / 17 STAY_DRAFT）。


## 5. P4 更新（2026-11-04 16:26）

- 卡片/来源：**399 卡（内容 188 + 来源 211）**；`SOURCES.csv` 212 行；P4 新增 22 内容卡 + 14 来源卡，旧卡 0 修改。
- 新卡：garment 5（手套/高跟鞋/帽/胸针/手袋结构）、garment_part 14（STR-0012..0025）、material 3（MAT-0012..0014）；v1.2 可选字段 42 个（新卡使用 36 个）。
- 书籍：9 本 PD 书、31 条结论（15 verified/11 partial/5 candidate）、157 章、12,640 hits、5,391 词典词条；页码 UNCONFIRMED。
- 视觉：28 条 CC0 索引（28/28 isPublicDomain、27 关联、0 下载/0 内嵌图片）。
- Composer/Macbeth：9 例 + 11 例验收；P4 相对 P3.5 的槽位/来源覆盖提升。
- 缺口不变：pattern 3/11 族、material 细化（leather/fur/metal/finish）不足、62 draft、AAT 19 张未接入。
