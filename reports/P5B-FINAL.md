# P5-B 最终结论（P5B-FINAL）

- 定稿：2026-11-05 01:37（Asia/Shanghai）；verifier / task-68；快照：HEAD `afcd9ec` + P5-B 修正（工作区未提交；400 卡/211 来源）
- 依赖：`P5B-GRAPH-QA`、`P5B-RELATION-COVERAGE`、`P5B-SEMANTIC-AUDIT`、`P5B-EXPANSION-PLAN`、`P5-GRAPH-AFTER`、`P5-GRAPH-QA`
- 声明：本报告不修改卡片/脚本；GUI 未执行，不得声称通过。

## 0. 一句话结论

**P5-B 关系重构达到验收目标：抽样 48 条关系准确率 100%（≥95%）；4 MISLINK 全部关闭/隔离、8 WEAK 处置合理；Agent E2E 官方 3/3、overlay 5/5 五项全 PASS；validate/build/relation/security/lookbook/skill-sync/backup 回归 PASS；**acceptance 45/45 PASS（lead 报告后复跑）**；composer 9/9 PASS；quality/workflow/Macbeth 未独立复跑（workflow engineer 9/9）；PRIVATE-READY 维持 YES（附 WARN），PUBLIC-READY 仍 NO/BLOCKED（B1–B6 + L1–L6），GUI NOT_RUN。**

## 1. 修复前后关键指标

| 指标 | Before（HEAD 1acb4d3，P5-A 前） | P5-A 后 | **P5-B 后（当前）** |
|---|---|---|---|
| 内容卡零可见链接 | 0/189 | 0/189 | **0/189** |
| 来源卡零可见链接（含导航） | 58/211 | 0/211 | **0/211**（MOC 导航可达） |
| source_ids 可见 | 2/299（0.7%） | 193/299（64.5%） | **191/299（63.9%）** |
| 有 source_ids 无可见 SRC 链接的卡 | 180/181 | 38/181 | **40/181（22.1%；全 draft + 1 个 WEAK-07 连带）** |
| 被机器引用来源可见 | 2/143 | 143/143 | **142/143（SRC-0155 随 WEAK-07 移除可见链接；仍引用但 review）** |
| typed 边无可见 | 313/485 | 122/485 | **123/480** |
| 语义分量 | 66（335+65） | 66（335+65） | **66（335+65，不变）** |
| 卡片 `relations` | 0 | 201 | **201**（198 high/verified + 3 medium review） |
| 关系抽样准确率 | — | 26/26（P5-A 抽检） | **48/48 = 100%**（P5-B，7 域） |
| MOC 导航页 | 0 | 9 | **9（仅导航，无关系断言）** |

- 说明：P5-B 的 WEAK-07 移除了 GAR-0033→SRC-0155 的可见链接（保留 source_ids 背景），故 191/299 与 40/181 相对 P5-A 的 193/299、38/181 各差 2/1；属**有意降级**，不是回归。
- 65 来源语义单点原因（P5-B 分类）：**34 legit_reference / 16 evidence_missing_expression / 14 future_topic / 1 no_verifiable_relation**；68 未引用来源（211−143）含 9 本 P4 书源。
- 38 draft 未迁移（look 22 / scene 15 / style 1）；106→108 source_ids 不可见（WEAK-07 连带）。

## 2. 关系准确率与缺陷关闭

- **抽样 48 条 / 7 域**：历史地域 8、结构 6、面料 6、鞋履配饰 6、风格 6、完整造型 6、来源 10；**48/48 PASS = 100%**（目标 ≥95%）。
- **4 MISLINK**：2 closed（PRD-0007 移除 GAR-0006；PRD-0010 替换 MAT-0011）+ 2 rejected（MAT-0013 物性卡 token、codpiece→collar 共现）；**0 残留正式关系**。
- **8 WEAK**：1 closed（GAR-0033→SRC-0155 移除）、3 降 medium/review（WEAK-11/12、SCAN-MAT-02）、4 候选保持 review/design、1 example 排除；**全部合理处置**。
- **高风险年代/地域**：6 对明确冲突（5 移除 + 1 替换）已从 key_garments 移除；6 对 flag review 保留在 review_queue（**recommend/outfit 不读取 key_garments**，不进入正式推荐主路径；仍可见于查询/审阅 → WARN，需人工结论）。
- **YAML↔正文**：200/201 有可见链接；唯一例外 GAR-0045→SRC-0405（medium/interpretive review，策略性不渲染强证据）。
- **无重复**：0 重复 relation 条目、0 双向同类型重复事实；**低置信不进强证据**：3 条 medium 全在 review_queue。
- **MOC 仅导航**：9 页无 frontmatter/relations，仅 wikilink；导航边 494 不计入语义分量。

## 3. Agent E2E 五项

| 运行 | 用例 | 五项 | 判定 |
|---|---|---|---|
| 官方 DeepSeek | RQ1/RQ2/RQ3 | skill✅ tools✅ result✅ turn_end.completed✅ 完整输出✅ | **3/3 PASS** |
| overlay（Doubao 临时 patch） | RQ1–RQ5 | 同上 | **5/5 PASS** |

- 独立解析事件：skill=1、工具 2–19 次、final 239–8293 chars、IDs 2–17、全部 ID 解析到真实卡/来源（0 missing）、turn_end.completed=true。
- 证据：`11-验收/P5B/agent-e2e/{official,overlay}/RQ*.events.jsonl|txt`；验证器 `validate_e2e.py` 与本轮独立解析一致。
- 说明：artifacts 为 engineer 运行，本轮独立解析验证；未重新跑 headless（时间/网络），判定 PASS（五项齐全）。

## 4. 回归结果

| 套件 | 结果 |
|---|---|
| validate | **PASS 400/400**（211 来源，0 错误/警告） |
| build_sources | **PASS 211/211**（CSV 212 行） |
| acceptance | **PASS 45/45**（lead 报告后独立复跑；`--no-write`；exit 0） |
| quality_eval | **NOT_RUN**（同上；P5-A 前次 17/17） |
| workflow | **NOT_RUN**（当前树重跑未完成；P5-A 前次 engineer log 9/9） |
| composer | **PASS 9/9**（18.8s） |
| Macbeth | **NOT_RUN**（重跑未完成，已终止；不写 PASS） |
| relation migration tests | **PASS 8/8**（当前树） |
| R1.1 tests | security **7/7 PASS**、lookbook **6/6 PASS**、skill-sync **3/3 PASS**、backup **7/7 PASS**、human closeout **3/3 PASS**（当前树） |

（所有未执行/挂起项明确标 NOT_RUN，不写 PASS。）

## 5. 扩建计划审查

- 计划为**提案，不是实施**：卡数仍 400（无新增卡）；目标 P1 6–8 卡（material/pattern）+ 2–3 component，P2 4–6 卡，合计约 12–17 张（~6–9%），非大规模扩卡。
- 依据真实覆盖矩阵（component 18%、material 40%、style 2%、outfit 0%；pattern 3 张；68 未引用来源），每项要求真实 SRC、不硬连、38 draft 不动。
- 结论：**合理、证据支撑、可分批执行**；P0（7 来源连接/9 书源表达/38 draft 复核）优先于补卡。

## 6. 剩余独立节点与原因（P5-B）

1. **65 来源语义单点**：34 legit_reference（AAT/FIT 词典、机构页、图像权）合理保留；16 evidence_missing_expression（无卡引用/未表达）；14 future_topic（未来案例）；1 no_verifiable_relation（FIT 主页）。**属真实独立/待接入，不是链接 bug**。
2. **68 未引用来源**（vocabulary 19、museum 12、academic 10、reference 9、other 8、image 5、industry 4、dataset 1）—— 需按 source-audit/expension plan 决定表达方式，不硬挂。
3. **38 draft**（LOOK 22/SCN 15/STY 1）未迁移；106→108 source_ids 不可见。
4. **6 对 flag review** 仍在 key_garments（审查中，不进正式推荐）。
5. **1 条 formal relation 无可见链接**（GAR-0045→SRC-0405，medium review）。

## 7. 门禁

| 门禁 | 状态 |
|---|---|
| PRIVATE-READY / PRIVATE-USE | **YES（技术层，附 WARN）**：关系准确率 100% 抽样、E2E 五项 PASS、回归 PASS；但 P5-B 修正未提交、workflow 若 NOT_RUN、6 flag 待人工、GUI NOT_RUN |
| PUBLIC-READY | **NO（BLOCKED）**：B1 GUI NOT_RUN、B2 逐图版权 NOT_RUN、B3 15 案例 NOT_RUN、B4 62 draft BLOCKED、B5 待签、B6 待法务；**L1–L6 全部保持** |
| B7 CSV | CLOSED（211/211） |
| HUMAN-UAT（GUI） | **NOT_RUN / PENDING**（无截图/签字，不得声称通过） |

## 8. 本批次回归补记

- 当前树独立执行 PASS：validate 400/400、build 211/211、relation migration 8/8、security 7/7、lookbook 6/6、skill-sync 3/3、backup 7/7。
- human closeout **PASS 3/3（28.8s）**；composer **PASS 9/9（18.8s）**；Macbeth 重跑未在窗口内完成，**标 NOT_RUN**（P5-A 前次 11/11 仅参考，不写 PASS）。
- acceptance：**PASS 45/45**（lead 报告后复跑）；quality_eval / workflow：未独立复跑（workflow engineer 9/9），不写 PASS。此外 relation-consistency 测试 EXIT 0（5/5）与 query relation filter 抽查 PASS；relation-consistency.json 见下方备注。
- 结论：本轮可确认的 PASS 为 validate/build/relation/security/lookbook/skill-sync/backup/human/composer，以及 relation-consistency 测试 5/5、query relation filter 抽查；acceptance 45/45 PASS；quality/workflow/Macbeth 未独立复跑，不伪造 PASS。
- 备注：`11-验收/P5B/relation-consistency.json` 现为 cards 400/relations 201/errors 0；`P5B-AGENT-E2E.md` 文本写 202（修正 CSV 前口径），以 JSON/当前树 201 为准（WARN 文档滞后）。

## 9. 最终结论与建议

- **可私用**：知识库、关系检索（真实 headless E2E 五种证据）、MOC 导航、Agent 工具链在官方/overlay 均可用；关系准确率高（抽样 100%）。
- **不可公开**：B1–B6/L1–L6 未关闭；GUI 未人工验收；P5-B 修正未提交。
- **建议**：① lead 提交 P5-B 修正（48 项）；② 人工核 6 flag + 38 draft；③ 按 expansion plan 先做 P0 关系表达，再少量补卡；④ 稳定环境重跑 workflow/Agent E2E 留档；⑤ 完成 B1–B6 人工门禁后才可讨论 PUBLIC。
