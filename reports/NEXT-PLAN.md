# 下一步计划（NEXT-PLAN）

- 基于：`reports/P3-QA.md`（PASS 12 / WARN 7 / FAIL 2 / HUMAN_UAT_PENDING 4）、`P3-DEFECTS.md`、`P3-COVERAGE.md`
- 原则：**先修 S1/S2 语义缺陷，再扩覆盖；所有修复须有回归用例并由 verifier 复验**；GUI/版权/签核/draft 复核未完成前不得宣布全量 PASS。

## 1. P3.1（阻断修复，最高优先）

| # | 任务 | 对应缺陷 | 验收阈值 | 建议 owner |
|---|---|---|---|---|
| 1 | 职业匹配表：occupation→garment/LOOK 映射（护士→GAR-0036/LOOK-0010、急诊→加 PPE；厨师→GAR-0043；警察→GAR-0042 仅警察场景；建筑师/教师等无卡时保持诚实「无职业卡」但不得用他职业制服） | **D2** | T04/T15/T18/T26/C02/N1 的 A 套不得出现无关职业制服；warning 不得声称「无职业卡」当对应卡存在；15 案例切题均值 ≥1.2/2 | engineer |
| 2 | 修虚假 warning「rainwear cards are missing」→ 改为「有雨具卡但年代/地域不匹配」；T01/T02 断言检查 | **D4** | 20 例抽查 warning 文本与库内卡一致；无虚假声明 | engineer |
| 3 | context 过滤：C01 等去掉 1770s/维多利亚等无关引用；只在 card/period 匹配时输出 | **M4** | C01 context 仅含 1644/Ming-Qing 相关引用 | engineer |
| 4 | prompt 串文：T13 室内场景剔除 anorak「worn in snow」；只取已选 items 的 prompt_en | **M7** | prompt contamination scan = 0（排除输入光照/雪景合理项） | engineer |
| 5 | GAR-0019 环境约束（室内/雨景禁用极地派克）或硬过滤；M6 | **M6** | T10/T13 不再把 anorak 用于室内/雨景 | engineer + architect |
| 6 | 修 M1（GAR-0010 从属断言）、M2（SRC-0046/0047 许可标签）；GAR-0001/GAR-0065 和服重复卡合并/canonical | **M1/M2/D3** | validate 0 错、卡片声明与页面一致、query P02 不返回重复语义卡 | architect / researcher |

## 2. P3.2（质量与覆盖）

| # | 任务 | 验收 |
|---|---|---|
| 7 | 环境/职业/文化约束字段化（indoor/outdoor/rain/snow/hospital/ceremonial），用于硬过滤与 warning | 20 例抽查无「室内穿极地派克/医院穿厨师服」 |
| 8 | query 排序：example 卡降权/排除；修正 1930s 上海 top5 缺 GAR-0031；跨文化多词查询（P09/P10）精度提升 | relevant@5 ≥4.0、precision ≥92% |
| 9 | 补 pattern 族系（1/11 → ≥6/11）、material 族系（4/8 → 7/8）、garment_part 族系（6/16 → ≥10/16）、lower_body/inner_layer | P3-COVERAGE 缺口表逐项核销 |
| 10 | 接入 19 张 Getty AAT 与其余未引用来源（114/174 → ≥150/174） | 来源引用率 ≥85% |
| 11 | 增加回归用例：职业匹配（急诊护士/建筑师/教师）、室内极地派克、rainwear 声明、context 清洁、prompt 串文、和服重复 | 每缺陷至少 1 个断言用例，verifier 复验通过 |

## 3. 人工 UAT（发布前必须完成，不得由 agent 代签）

| # | 项 | 状态 | 完成标准 |
|---|---|---|---|
| H1 | Obsidian GUI 打开/渲染/wikilink 跳转 | HUMAN_UAT_PENDING | 截图 + 抽 10 条链接点击通过 |
| H2 | 逐图版权授权核验 | HUMAN_UAT_PENDING | 每张外链图记录许可结论；无授权者仅 link_only（当前已 0 下载/0 内嵌） |
| H3 | 15 案例语义评分签核 | HUMAN_UAT_PENDING | lead 对 `P3-QA §3.2` 评分签字或调整 |
| H4 | 62 张 draft 卡人工复核 | HUMAN_UAT_PENDING | `review_status` 更新，draft=0 |

## 4. 发布清单（Definition of Done）

- [ ] S1/S2 缺陷全部关闭：D4、D2、M4、M6、M7（+ 回归用例通过，verifier 复验）
- [ ] M1/M2/D3/D5/D6 关闭
- [ ] `validate.py` exit 0；`build_sources --check` exit 0（CSV 与来源卡一致）；`run_acceptance` PASS 30+/30+
- [ ] query relevant@5 ≥4.0、precision ≥92%、0-hit 仅限已知未覆盖主题
- [ ] 15 案例 6 维 rubric：PASS ≥10/15、无切题 0 分案例（或明确标注「KB 无覆盖+诚实声明」）
- [ ] HUMAN_UAT_PENDING 四项完成并留档
- [ ] 报表更新：`STATUS/QA/COVERAGE/P3-QA/P3-DEFECTS/CHANGELOG/NEXT-PLAN` 与最终 git commit 一致

## 5. 建议节奏

1. 第 1 批（0.5 天）：D4 → D2 映射 → 回归用例；verifier 复验。
2. 第 2 批（0.5 天）：M4/M6/M7 + M1/M2/D3；validate/build 重跑。
3. 第 3 批（1 天）：覆盖扩展（pattern/material/structure）；query 排序与来源接入。
4. 收尾：HUMAN_UAT_PENDING 四项 + 发布清单签字。

> 说明：本计划不修改任何卡片/脚本；任务分配给对应 owner，verifier 负责独立复验与报表。
