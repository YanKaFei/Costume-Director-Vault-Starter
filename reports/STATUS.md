# 运行状态（STATUS）— Costume Director Knowledge System（P3 终态）

- 更新时间：2026-11-04 02:44（Asia/Shanghai）；P3 独立 QA 后
- 快照：**328 张卡**（内容 154 + 来源 174）；git HEAD `0345f05`（P3 commit，工作区 clean）
- 总体：**P0/P1/P2/P3 数据与流程完成；P3 质量验收 = PASS 12 / WARN 7 / FAIL 2 / HUMAN_UAT_PENDING 4**
- 详细报告：[P3-QA.md](P3-QA.md) · [P3-COVERAGE.md](P3-COVERAGE.md) · [P3-DEFECTS.md](P3-DEFECTS.md) · [CHANGELOG-P3.md](CHANGELOG-P3.md) · [NEXT-PLAN.md](NEXT-PLAN.md)

## 1. 阶段状态

| 阶段 | 状态 | 证据 |
|---|---|---|
| P0 架构 | DONE | 数据字典 v1.1、模板、索引、来源规范 |
| P1 种子库 | DONE | 32 内容卡阶段 → P3 终态 154 |
| P2 决策闭环 | DONE | query/recommend/3 模板/18 例测试 |
| P2.5 质量审计 | DONE（有条件） | PASS 6/WARN 9/FAIL 3/H_U_P 4；见 `P2.5-ACCEPTANCE.md` |
| P3 扩充与修复 | **DONE（数据/流程）** | 328 卡（≥250）；30/30 验收；F1/F2/F3 回归 FIXED |
| P3 质量验收 | **FAIL 2（S1/S2 未关闭）** | D2 职业服万能填充、D4 虚假 rainwear 声明 |
| P4 / 发布 | START PENDING | 见 `NEXT-PLAN.md` |

## 2. 当前可用

- **知识库**：328 卡，`00-系统/索引.md` 导航；结构校验 `validate.py` exit 0（17/17 PASS，0 错误 0 警告）；609+ 链接可达、0 内嵌图片。
- **来源**：174 张来源卡，`reports/SOURCES.csv` 174 行 + 表头（QA 重建），`build_sources --check` exit 0；32 个新增来源 URL 32/32 HTTP 200。
- **检索/推荐**：`query.py`（多词/`--phrase`/过滤）与 `recommend.py`（3 套 Look + 评分 + prompt + warnings + 连续性）；30/30 验收 PASS；query 命中 124。
- **提示词模板**：角色/静态生图/视频 3 模板；`skills/costume-director/SKILL.md` 已更新。
- **验收材料**：30 例（T01–T30）输入/结果/raw/SUMMARY；15 个语义案例（C01–C10 + N1–N5 由 verifier 复核）。

## 3. 已知问题（S1/S2 未关闭）

1. **D2（S2）职业服万能填充**：当代/职业请求 A 套普遍为警察制服+医生白袍+医疗工作鞋；warning 自称「无职业卡」但 护士制服/医生白袍/厨师服/护士 LOOK 均在库——**推荐切题错误 + 自相矛盾**。
2. **D4（S1）虚假 warning**：「rainwear cards are missing」但 风衣/雨衣卡存在（GAR-0045/0046）。
3. **M4/M6/M7（S2）**：C01 context 仍引用 1770s/维多利亚；GAR-0019 仍作室内/雨景外层；T13 prompt 仍含「worn in snow」。
4. **M1/M2/M8 部分**：GAR-0010 扩写、SRC-0046/47 许可、query example 排序与和服重复卡。
5. **D1（S3）**：`SOURCES.csv` 曾是旧版（142 行）；QA 已重建，需纳入发布步骤防复发。
6. 数据缺口：pattern 1/11 族、material 4/8 族、structure 6/16 族；60/174 来源未引用（含 19 张 AAT）。
7. 62 张 `review_status: draft`。

## 4. HUMAN_UAT_PENDING（不得写成 PASS）

- H1 Obsidian GUI 打开/渲染/wikilink 跳转
- H2 逐图版权授权核验
- H3 15 案例语义评分人工签核
- H4 62 张 draft 卡人工复核

## 5. 下一步（详见 NEXT-PLAN.md）

1. 修 D4 → D2（职业匹配表）→ M4/M6/M7 → M1/M2/D3/D5/D6；每个缺陷配回归用例，verifier 复验。
2. 覆盖扩展：pattern/material/structure 族系、lower_body/inner_layer、接入 AAT 与未引用来源。
3. 完成 HUMAN_UAT_PENDING 四项；更新发布清单。
4. 发布前重跑：`validate.py`、`build_sources.py --check`、`run_acceptance.py`，并要求 query/15 案例质量阈值达标。
