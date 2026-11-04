# P5-C 启动核对与基线（P5C-BASELINE）

- 生成：2026-11-05 01:52（Asia/Shanghai）；verifier / task-69（P5-C 启动核对，只读）
- 快照：**HEAD `f500289`**（P5-B 全部已提交：6beaf1d + f500289）；工作区仅 21 个未跟踪 sandbox 副本（无卡片改动）
- 规模：**400 卡（189 内容 + 211 来源）**；`validate PASS 400/400`（0 错误/警告）、`build_sources PASS`（CSV 212 行）
- 性质：只写本报告；未改卡片/脚本。所有数字为独立统计（不直接采信 P5-B 报告）。

## 1. 201 条 relations 与证据状态

| 项 | 独立结果 |
|---|---|
| 正式 relations 总数 | **201**（142 张内容卡；189 内容卡覆盖 75.1%） |
| 类型 | claim_supported_by **191**、in_style **8**、uses_material **2** |
| evidence | **verified 200 / interpretive 1** |
| confidence | **high 198 / medium 3** |
| 3 条 medium（逐条） | GAR-0045→SRC-0405（interpretive/medium）、GAR-0020→MAT-0001（verified/medium）、PRD-0002→MAT-0001（verified/medium） |
| target 解析 | **0 missing**（全部指向真实内容卡/来源卡） |
| 关系内 source_ids 解析 | **0 missing**（source_ids 均存在） |
| target 正文可见链接 | **200/201**；唯一例外 GAR-0045→SRC-0405（medium review，策略性不渲染强证据） |
| 重复 relation 条目 | **0** |
| 双向同类型重复事实 | **0**（修正前统计时需注意方向口径；按 (subject,type,target) 检查） |

**口径提示（不一致点）**：`reports/P5B-AGENT-E2E.md` §1 写「**202 relations**」，但 `11-验收/P5B/relation-consistency.json` 与当前树均为 **201**（WEAK-07 移除 1 条后未更新文档）→ **文档滞后 1，非数据错误**。

## 2. 8 条 WEAK 最终分类（去重口径）

`reports/P5B-RELATION-CORRECTIONS.csv` 中 WEAK 行 **8 条（unique 8）**：

| 最终动作 | 数量 | ID |
|---|---:|---|
| 移除（remove_relation） | **1** | WEAK-07（GAR-0033→SRC-0155） |
| 降级（downgrade_relation） | **2** | WEAK-11（GAR-0020→MAT-0001）、WEAK-12（GAR-0045→SRC-0405） |
| review/design（不升格） | **4** | WEAK-05/06（may_have_part keep_review）、WEAK-08/09（keep_review_design） |
| 拒绝/排除（rejected） | **1** | WEAK-10（example/low 排除） |
| **合计** | **8** | — |

- 另有 **SCAN-MAT-02**（PRD-0002→MAT-0001）降 medium，但它属 SCAN 审计行、不属 8 WEAK；因此 **medium 共 3 条**（WEAK-11/12 + SCAN-MAT-02），与 §1 一致。
- 卡片落地核验：WEAK-07 relation 已移除（GAR-0033 现仅 SRC-0204 claim）；WEAK-11/12 为 medium；WEAK-05/06/08/09/10 均未进入正式 relations。

## 3. 独立口径：来源可见率 ≠ 关系覆盖率

### 3.1 来源可见率（source visibility）

| 指标 | 数值 |
|---|---|
| source_ids 机器引用对 | **299** |
| 正文可见 SRC 链接对 | **191/299（63.9%）** |
| 不可见引用对 | **108** |
| 被机器引用的唯一来源 | **143** |
| 正文可见的唯一来源 | **142/143**（唯一例外 SRC-0405，由 GAR-0045 medium review 使用） |
| 有 source_ids 的内容卡 | **181** |
| 零可见 SRC 链接的卡 | **39** = **38 draft**（LOOK 22 / SCN 15 / STY 1）+ **GAR-0045**（WEAK-12） |
| 部分可见（≥1 不可见）的卡 | **1**（GAR-0033：2 个 source_ids 中 1 个可见；WEAK-07 连带） |
| 有 ≥1 个不可见 source 的卡（graph 口径） | **40** = 39 零可见 + 1 部分可见（GAR-0033） |
| 未被任何内容引用的来源 | **68/211**（vocabulary 19、museum 12、academic 10、reference 9、other 8、image 5、industry 4、dataset 1；含 9 本 P4 书源） |
| MOC 可见来源（导航层） | **211/211**（9 页 MOC 链接全部来源，**仅导航，不计语义分量**） |

### 3.2 关系覆盖率（relation coverage，独立口径）

| 指标 | 数值 |
|---|---|
| 有 ≥1 条正式 relation 的内容卡 | **142/189（75.1%）** |
| 正式 relations 数 | 201（见 §1） |
| 结构化字段覆盖（不等于 relation 覆盖） | source_ids 181 卡；look_items 23 卡；look_scene 18 卡；key_garments 11 卡 |
| 无 formal relations 的内容卡 | 47（其中 42 张 draft 无 relations；其余为无关系设计的卡） |

> **不得混算**：191/299 是「source_ids 引用对的正文可见率」，不是「内容卡关系覆盖率」；75.1% 是「有 formal relations 的内容卡占比」，与来源可见率无分母关系。MOC 211 来源可达属导航层，不能计入语义连通或关系覆盖。

## 4. 6 组待人工复核 key_garments（不得自动确认）

| # | PRD 卡 | key_garments 中的待核目标 | 当前状态 |
|---|---|---|---|
| FLAG-KG-04 | PRD-0004（1920s US/W.Europe） | GAR-0007 | 在 key_garments；review_queue；未删/未确认 |
| FLAG-KG-07 | PRD-0007（1950s US/UK） | GAR-0023 | 同上 |
| FLAG-KG-06B | PRD-0006（1940s US/UK） | GAR-0022 | 同上 |
| FLAG-KG-08 | PRD-0008（1960s London/US） | GAR-0014 | 同上 |
| FLAG-KG-08B | PRD-0008（1960s） | MAT-0004 | 同上 |
| FLAG-KG-11 | PRD-0011（1930s 上海） | GAR-0033 | 同上（1930s vs 1940s 宽 era） |

- 独立核验：6 行均在 `P5B-RELATION-CORRECTIONS.csv`（action=flag_review、status=review_queue）；当前卡片 key_garments **仍包含**对应目标；**没有自动升级/删除/确认**。
- 说明：`recommend.py`/`outfit.py` 不读取 key_garments（grep 确认），因此这些 flag 不进入正式推荐主路径；但查询/审阅可见，需人工结论（P5-C 未处理）。

## 5. 65 个语义单点 / 38 张 draft（状态保持）

- **65 个语义单点**（`11-验收/P5B/isolates.csv`，65 行）：legit_reference **34**、evidence_missing_expression **16**、future_topic **14**、no_verifiable_relation **1**。
  - 按理由：isolated_source 28、background_or_dictionary_uncited 27、navigation_only 9（P4 书源）、book_source_no_card_integration 1。
- **38 张 draft**：= LOOK 22 + SCN 15 + STY 1（均有 source_ids 但无可见 SRC 链接的 draft）；当前 `review_status` 仍为 draft。
  - 全库 draft 总数 **62**（LOOK 23 / SCN 16 / STY 11 / PRD 11 / GAR 1）；P5-B commit 无 `review_status/evidence_status` 改动（diff 核验），**38 张状态保持**。
  - 106→108 source_ids 不可见：P5-A 后 106，P5-B WEAK-07 移除 1 条可见链接 + GAR-0045 降级 → 108（与 §3 一致）。

## 6. 补跑 quality_eval 与 P4-MACBETH（当前树）

- 运行方式：独立子进程 + 超时（quality 240s、Macbeth 360s）。
- **quality_eval：NOT_RUN**（当前树；进程运行 **97.0s** 后仍未产出结果/日志为空（0 bytes），因环境变慢于窗口内终止；exit -15；不写 PASS）。参考：P5-A 同结构树前次 quality_eval **17/17 PASS**（relevant@5 4.16、precision 0.929、0-hit 0；日志 `/tmp/r11f_qeval.txt` 等），P5-B commit 仅改 frontmatter 关系/key_garments，未改脚本。
- **P4-MACBETH：NOT_RUN**（quality 终止后子进程未启动/0.0s 即退出；无日志；不写 PASS）。参考：P5-A 同结构树前次 **11/11 PASS**（`/tmp/p5v4_macbeth.log`）。
- 证据：`/tmp/p5c_tests.out`（`quality EXIT -15 97.0s`、`macbeth EXIT -15 0.0s`）、`/tmp/p5c_quality.log` 与 `/tmp/p5c_macbeth.log` 均为 0 字节。
- 结论：本轮未能独立复跑这两套；按规则标 **NOT_RUN**，不伪造 PASS。

## 7. 不一致清单（需 P5-C 注意）

1. `reports/P5B-AGENT-E2E.md` 写 **202 relations**；当前/`relation-consistency.json` 为 **201**（WEAK-07 移除后文档未更新）→ 文档滞后，**WARN**。
2. 「38 张 draft」与「39 张零可见 SRC 卡」相差 1：38 draft + **GAR-0045**（WEAK-12 medium review）；`graph_analyze` 的「40/181」是「≥1 个不可见 source 的卡」= 39 零可见 + 1 部分（GAR-0033）。三种口径不同，**不是数据冲突**，P5-C 引用时须写明口径。
3. 来源可见率 191/299 与内容卡索引/语义连通不可混算；MOC 211 来源可达 **仅导航**，不计语义分量（语义分量仍 66 = 335 + 65 单点）。
4. 6 组 key_garments flag 仍待人工，不能自动视为已确认；expension/P5-C 若引用需标 review。
5. 8 WEAK 与 corrections CSV 39 行（含 SCAN/FLAG）范围不同：8 WEAK 是子集；勿把 39 行都当 WEAK。
6. `11-验收/P5B/relation-consistency.json` 与当前树一致（201/0 errors）；但 `P5B-AGENT-E2E.md`、`P5B-GRAPH-QA` 的 40/181 需按口径理解。

## 8. 结论

- **201 条 relations**：198 high/verified + 3 medium review；target/source_ids 全解析；200/201 正文可见（唯一例外 GAR-0045）。
- **8 WEAK**：移除 1 / 降级 2 / review 4 / 拒绝 1（unique 8）；SCAN-MAT-02 另计降级。
- **来源可见率**：191/299 对（63.9%），142/143 来源可见；**关系覆盖率**：142/189 卡（75.1%）——两者分开统计，不混算。
- **6 组 key_garments flag** 仍在 review_queue，未自动确认。
- **65 单点**（34/16/14/1）与 **38 draft** 状态保持（全库 draft 62；commit 无状态改动）。
- **quality_eval / Macbeth**：**NOT_RUN（当前树；quality 97s 内未产出、Macbeth 未启动，已终止；日志 0 字节）**；P5-A 前次分别为 17/17、11/11 PASS，仅参考不写 PASS。
