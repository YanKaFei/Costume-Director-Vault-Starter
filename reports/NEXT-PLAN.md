# 下一步计划（NEXT-PLAN）— P3.2 最终复验后

- 基准：2026-11-04 03:12；328 卡、45 例验收；git HEAD `281e3b1`
- 验收：**PASS 19 / WARN 5 / FAIL 0 / HUMAN_UAT_PENDING 4（28 项）**；D2/D4/R1/R2（查询层）已关闭
- 发布门槛：**条件性通过**——R7 raw relevant@5=3.92（<4.0，差 0.08），剔除已确认真实缺卡探针后=4.26（≥4.0）

## 1. 发布决策（lead）

| 选项 | 说明 | 结果 |
|---|---|---|
| A. 接受已知缺口放行 | 将 P21 Mughal、P22 mourning jewelry 标记为「已知 KB 缺口」，门槛用调整后 relevant@5（4.26） | 可进入发布；发布说明需披露缺口与 HUMAN_UAT_PENDING |
| B. 继续提升后再发布 | 提升 P09（3/5）/P10（4/5）/P20（4/5）相关性，或补 Mughal/哀悼珠宝卡后 raw relevant@5 ≥4.0 | 需 1 轮微调 + verifier 复验 |

> verifier 建议：R7 属 0.08 的测量边界差异（自评 4.0 vs 独立 3.92，标注严格度不同），倾向 A + 明确披露；若对外承诺「relevant@5 ≥4.0」则必须选 B。

## 2. 发布前必须完成（HUMAN_UAT_PENDING，4 项）

| # | 项 | 完成标准 |
|---|---|---|
| H1 | Obsidian GUI 打开/渲染/wikilink 跳转 | 截图 + 抽 10 条链接点击通过 |
| H2 | 逐图版权授权核验 | 每张外链图记录许可结论；无授权仅 link_only（当前 0 下载/0 内嵌） |
| H3 | 15 案例语义评分签核 | lead 对 `P3-QA §5`（7 PASS/8 WARN）签字或调整 |
| H4 | 62 张 draft 卡人工复核 | `review_status` 更新，draft=0 |

## 3. 非阻断改进（WARN，可 P4）

| # | 任务 | 验收 |
|---|---|---|
| 1 | R8 单探针相关性：P09/P10/P20 的跨文化/跨时代部分相关结果 | 每个探针 relevant@5 ≥4 |
| 2 | R3 数据层和服重复：GAR-0001/GAR-0065 canonical 标注或合并 | 索引/字典标注 canonical；query 去重保持 |
| 3 | R4 噪声 warning：「no upper_body/lower_body candidates」改述 | 文案与 one_piece/set 实际情况一致 |
| 4 | R5 流程：`build_sources --write` + `--check` 纳入发布清单 | 每次来源卡修改后 check 必过 |
| 5 | 覆盖扩展（可选）：pattern 1/11→≥6/11、material 4/8→7/8、garment_part 6/16→≥10/16；接入 19 张 AAT | 缺口核销 + 来源引用率 ≥85% |

## 4. 最终发布清单

- [ ] lead 决定 A/B（R7 处理方式）并记录
- [ ] D2/D4/R1/R2/M1–M7 保持关闭（45/45 + T31–T45 回归 PASS）
- [ ] `validate.py` exit 0；`build_sources --check` exit 0；`run_acceptance.py` ≥45/45 PASS
- [ ] HUMAN_UAT_PENDING 四项完成并留档
- [ ] 报表与最终 commit 一致：P3-QA / P3-DEFECTS / P3-COVERAGE / CHANGELOG-P3 / NEXT-PLAN / STATUS / QA / COVERAGE / SOURCES.csv
