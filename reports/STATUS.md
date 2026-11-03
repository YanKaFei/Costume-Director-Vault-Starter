# 运行状态（STATUS）— Costume Director Knowledge System（P3.1 复验后）

- 更新时间：2026-11-04 02:51（Asia/Shanghai）；P3.1 独立复验（task-17）后
- 快照：**328 张卡**（内容 154 + 来源 174）；**41 例验收**；git HEAD `0345f05` + P3.1 工作区修改（未提交）
- 总体：**数据/结构/诚实性 PASS；质量门槛 FAIL 1（query relevance 未达 4.0）**；D2/D4 已关闭
- 最终计数：**PASS 17 / WARN 5 / FAIL 1 / HUMAN_UAT_PENDING 4（27 项）**
- 详细：[P3-QA.md](P3-QA.md) · [P3-DEFECTS.md](P3-DEFECTS.md) · [P3-COVERAGE.md](P3-COVERAGE.md) · [CHANGELOG-P3.md](CHANGELOG-P3.md) · [NEXT-PLAN.md](NEXT-PLAN.md)

## 1. 阶段状态

| 阶段 | 状态 | 证据 |
|---|---|---|
| P0/P1/P2 | DONE | 字典/模板/索引、种子库、18 例闭环 |
| P2.5 | DONE（有条件） | PASS 6/WARN 9/FAIL 3/H_U_P 4 → P3 修复 |
| P3 | DONE（数据/流程） | 328 卡；30→41 例；D2/D4/M1/M2/M4/M6/M7 关闭 |
| P3.1 质量门槛 | **FAIL 1（query relevance）** | 独立 relevant@5 3.64、engineer 自评 3.92 均 <4.0；quality_eval OVERALL FAIL；其余 17 项 PASS |
| P4 | PENDING | 见 NEXT-PLAN |

## 2. 当前可用

- **知识库**：328 卡；`validate.py` exit 0（17/17 PASS，0 错误 0 警告）；609+ 链接可达；0 内嵌图片。
- **来源**：174 张来源卡；`SOURCES.csv` 174 行 + 表头（P3.1 再次由 QA 重建，`build_sources --check` PASS）；32 个新增来源 URL 32/32 HTTP 200。
- **检索/推荐**：`query.py`/`recommend.py`；**41/41 验收 PASS**（query 命中 178、逐例 ≥1）；职业匹配（护士/医生/警察/厨师/太空/婚礼）、雨具选择、室内禁极地派克、context 清洁、query 排序/去重均有回归用例并 PASS。
- **提示词模板 / skills**：3 模板 + SKILL.md 可用。

## 3. 已知问题（残余风险）

1. **R7（FAIL，唯一发布门槛阻断）**：query relevance@5 独立 3.64 / 自评 3.92 < 4.0；`quality_eval` OVERALL FAIL（其余 15 项 PASS，precision 自评 96.1%）。
2. R1（WARN）：职业同义词未全覆盖（合成「巡警」→旗袍+派克）；医生 A 套含韩服（内层不当）。
3. R2（WARN）：example 卡仍在 query top5 第 4/5；GAR-0001/GAR-0065 和服重复卡仅查询层去重。
4. R6（WARN）：SOURCES.csv 同步流程缺失（P3.1 再次漂移，QA 已重建）。
5. R3/R4/R5（轻）：数据层和服重复、噪声 warning 措辞、自评与独立评分口径差异。
6. 数据缺口：pattern 1/11 族、material 4/8 族、structure 6/16 族；60/174 来源未引用（AAT 19 张）；62 张 draft。

## 4. HUMAN_UAT_PENDING（不得写成 PASS）

- H1 Obsidian GUI 打开/渲染/wikilink 跳转
- H2 逐图版权授权核验
- H3 15 案例语义评分人工签核
- H4 62 张 draft 卡人工复核

## 5. 下一步（详见 NEXT-PLAN.md）

R7（query relevance + aliases/tags + example 排除）→ R1（职业同义词/医疗内层）→ R2/R3（example top5/和服数据层）→ R6（CSV 同步机制）→ 覆盖扩展 → HUMAN_UAT_PENDING 四项。发布前必须 `quality_eval` OVERALL PASS（relevant@5 ≥4.0）且 41+ 例全 PASS。
