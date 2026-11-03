# 下一步计划（NEXT-PLAN）— P3.3 最终复验后

- 基准：2026-11-04 03:24；343 卡（内容 158 + 来源 185）、45 例验收；git HEAD `fcebf79`
- 验收：**PASS 24 / WARN 4 / FAIL 0 / HUMAN_UAT_PENDING 4（32 项）**
- 发布门槛：**技术/数据/质量门 PASS**（R7 已关闭：relevant@5 4.16、0 命中 0%；R1–R5 关闭；45/45、validate、build 全 PASS）；发布仍需完成 HUMAN_UAT_PENDING 4 项

## 1. 发布前必须完成（HUMAN_UAT_PENDING，4 项）

| # | 项 | 完成标准 |
|---|---|---|
| H1 | Obsidian GUI 打开/渲染/wikilink 跳转 | 截图 + 抽 10 条链接点击通过 |
| H2 | 逐图版权授权核验 | 每张外链图记录许可结论；无授权仅 link_only（当前 0 下载/0 内嵌） |
| H3 | 15 案例语义评分签核 | lead 对 `P3-QA §5`（7 PASS/8 WARN）签字或调整 |
| H4 | 62 张 draft 卡人工复核 | `review_status` 更新，draft=0 |

## 2. 发布清单（技术项已全部满足）

- [x] validate exit 0（343/343，17/17，0 错误 0 警告）
- [x] build_sources --check exit 0（185/185；R5 门禁实测有效）
- [x] run_acceptance exit 0（45/45）
- [x] quality_eval OVERALL PASS（relevant@5 4.16、precision 0.945、0-hit 0、CSV gate PASS）
- [x] D2/D4/R1/R2/R3/R4/M1–M7/F1–F3 关闭
- [ ] HUMAN_UAT_PENDING 四项完成并留档
- [ ] 最终 commit 与 reports 一致（P3-QA/P3-DEFECTS/P3-COVERAGE/CHANGELOG-P3/NEXT-PLAN/STATUS/QA/COVERAGE/SOURCES.csv）

## 3. 非阻断改进（P4，可选）

| # | 任务 | 验收 |
|---|---|---|
| 1 | W1 案例覆盖：明/清服装、未来基底、身份弧线 wardrobe-stage、跨文化仪式礼服 | rubric 切题均值 ≥1.6/2；C01/C03/C05/N4 至少一例升 PASS |
| 2 | W2 明末清初跨文化近似：补明/清卡或提高 region 硬约束 | C01 A 套不再出现非东亚传统服 |
| 3 | W3 filtered 查询结果数：为 style-tag/noir、pattern、雨夜等补条目 | 相关查询返回 ≥5 条 |
| 4 | W4 证据覆盖：为 example/设计推断件补来源或标注 | evidence_coverage ≥0.97 |
| 5 | 覆盖扩展：pattern 1/11→≥6/11、material 4/8→7/8、garment_part 6/16→≥10/16；接入 19 张 AAT | 缺口核销 + 来源引用率 ≥85% |
| 6 | 每次来源卡修改后执行 `build_sources --write/--check`（R5 门禁已在 quality_eval 中自动化） | 漂移必被拦截 |

## 4. 建议顺序

1. lead 签核 H3/H4（draft 复核可并行）→ 完成 H1/H2 → 发布。
2. P4 按 W1–W4 + 覆盖扩展排期；每次改动后重跑 45 例 + quality_eval（OVERALL PASS 才可合并）。
