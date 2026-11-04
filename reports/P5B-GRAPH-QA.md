# P5-B 图谱与关系 QA（P5B-GRAPH-QA）

- 生成：2026-11-05 01:36（Asia/Shanghai）；verifier / task-68（P5-B 最终独立验收）
- 快照：HEAD `afcd9ec`（P5-A commit）+ P5-B 工作区修正（48 项未提交）；**400 卡（189 内容 + 211 来源）**；`validate PASS 400/400`、`build_sources PASS`
- 性质：只读验收；未改卡片/脚本；证据 `/tmp/p5b_sample.json`、`/tmp/p5b_graph.json`、`11-验收/P5B/*`、`reports/P5B-*`

## 1. 关系抽样准确率（≥40，实际 48）

独立分层抽样 **48 条关系**，覆盖 7 个域；逐条核对 subject/target 存在、结构化依据、正文可见链接、证据/置信与年代/地域兼容性：

| 域 | 样本 | PASS | 检查要点 |
|---|---:|---:|---|
| 历史/地域（PRD key_garments） | 8 | 8 | PRD/目标的 periods 区间归一后重叠；regions 兼容（宽标签/世纪级）；flag review 对单独标注 |
| 结构（garment→STR 可见） | 6 | 6 | STR 卡真实存在；正文 `[[STR-…]]` 可见 |
| 面料（uses_material + garment→MAT 可见） | 6 | 6 | MAT 卡存在；formal uses_material 规则/置信符合 v2（最高 medium）；可见链接 |
| 鞋履配饰（LOOK look_items 中 footwear/accessory/headwear/carried_prop） | 6 | 6 | 目标在 `look_items` 且真实存在；正文可见 |
| 风格（in_style） | 6 | 6 | `style_tags` 精确 STY；target 真实；正文可见 |
| 完整造型（LOOK look_items） | 6 | 6 | 目标在 `look_items`；正文可见 |
| 来源（claim_supported_by） | 10 | 10 | target 在 `source_ids`；来源卡存在；正文 `[[SRC-…]]` 可见；evidence=verified/confidence=high |
| **合计** | **48** | **48** | **准确率 100.0%（目标 ≥95%）** |

- 逐条明细：`/tmp/p5b_sample.json`（含 data_ok/visible_ok/pass/note）。
- 方法边界：历史/地域用区间归一（decade/世纪/era→区间，`contemporary` 宽标签单列），不做关键词/颜色推断；可见性检查按文件名 stem 解析。
- 未把候选 CSV（RELATION-CANDIDATES/REVIEW-QUEUE）算入 accuracy；仅检查真实卡片/来源。

## 2. MISLINK（4 条）与 WEAK（8 条）关闭/隔离

### 2.1 4 MISLINK

| ID | 内容 | 处置 | 独立核验 |
|---|---|---|---|
| MISLINK-01 | PRD-0007 (1950s) key_garments 含 GAR-0006 (1960s+) | **closed：移除** | PRD-0007 key_garments 现为 `[GAR-0014, GAR-0023]`（无 GAR-0006） |
| MISLINK-02 | PRD-0010 (拜占庭) key_garments 含 MAT-0003 (16–19c 欧洲) | **closed：替换 MAT-0011（拜占庭 samite）** | PRD-0010 key_garments 现为 `[GAR-0009, MAT-0011]` |
| MISLINK-03 | 候选 GAR-0002→MAT-0013 uses_material（物性卡 token 误命中） | **rejected（候选，未入正式 relations）** | GAR-0002 正式 relations 仅 `SRC-0103` claim；无 MAT-0013 |
| MISLINK-04 | 候选 GAR-0013→STR-0001 may_have_part（共现语义不通） | **rejected（候选，未入正式 relations）** | GAR-0013 正式 relations 仅 SRC-0114 claim；无 STR-0001 |

→ **4/4 关闭或隔离；无 MISLINK 残留进入正式关系。**

### 2.2 8 WEAK

| ID | 处置 | 独立核验 |
|---|---|---|
| WEAK-07 GAR-0033→SRC-0155（1930s 来源支撑 1940s） | **closed：移除 relation**（source_ids 保留背景，SRC-0204 保留为 1940s 证据） | GAR-0033 relations 现有 SRC-0204（high/verified），无 SRC-0155 relation |
| WEAK-12 GAR-0045→SRC-0405（2014 实例） | **review_queue：降 interpretive/medium** | GAR-0045 relation 现 evidence=interpretive、confidence=medium |
| WEAK-11 GAR-0020→MAT-0001（token 越级） | **review_queue：降 medium，规则 R-MAT-TOKEN** | 现 confidence=medium；uses_material 上限 medium |
| SCAN-MAT-02 PRD-0002→MAT-0001 | **review_queue：降 medium** | 现 confidence=medium |
| WEAK-05/06 GAR-0002/0003→STR-0001 may_have_part | **keep_review（候选，不升 has_part）** | 正式 relations 无 may_have_part；仅在候选/审核队列 |
| WEAK-08 GAR-0002→GAR-0024 ensemble_with | **keep_review_design（候选）** | 未进入正式 relations |
| WEAK-09 LOOK-0001→STY-0010 in_style | **keep_review_design（设计标签）** | 未进入正式 relations |
| WEAK-10 LOOK-EXAMPLE-001 appears_in_look | **rejected/excluded（example/low 不迁移）** | 未进入正式 relations |

→ **8/8 处置合理；低置信/设计推断不进入正式关系或降级 review。**

### 2.3 高风险年代/地域

- 6 对明确冲突：**5 移除 + 1 替换**（PRD-0007→GAR-0006、PRD-0010→MAT-0003→MAT-0011、PRD-0003→GAR-0012、PRD-0005→GAR-0007、PRD-0006→GAR-0017、PRD-0006→GAR-0011）。
- 6 对 flag review（未删除，**review_queue**）：PRD-0004→GAR-0007、PRD-0007→GAR-0023、PRD-0006→GAR-0022、PRD-0008→GAR-0014、PRD-0008→MAT-0004、PRD-0011→GAR-0033。
- **是否从正式推荐排除**：`scripts/recommend.py`/`scripts/outfit.py` **不读取 key_garments/context_includes**（grep 确认），因此 flag 对不进入推荐主路径；但它们在卡片 frontmatter/查询语义中仍存在 → **记录为 WARN（需人工核），不是完全删除**。

## 3. YAML ↔ 正文一致性 / MOC / 重复

| 检查 | 结果 |
|---|---|
| 正式 relations 总数 | **201**（claim 191、in_style 8、uses_material 2） |
| relation target 在正文有可见 wikilink | **200/201（99.5%）**；唯一例外 GAR-0045→SRC-0405（WEAK-12，已降 interpretive/medium review，策略性不渲染为强证据） → 记录 WARN，不是隐藏事实 |
| 重复 relation 条目 | **0** |
| 双向同类型重复事实（A→B 与 B→A 同 type） | **0** |
| 低置信进强证据 | 3 条 medium（WEAK-11/12、SCAN-MAT-02）均为 **review_queue**，无 high 级误升；formal 198 high/verified + 3 medium |
| MOC 仅导航 | 9 页 MOC 无 frontmatter、无 `relations` 字段，仅 wikilink；graph_analyze 把 MOC 计入导航边（494）**不计入 content+source 语义分量** |

## 4. Agent E2E（五项标准，官方/overlay 分开）

对 `11-验收/P5B/agent-e2e/` 事件独立解析（非仅采信脚本输出），逐项判定 skill 调用 / 工具执行 / 结果产生 / turn_end.completed / 完整输出：

| 运行 | 用例 | skill | tools | result | turn_end | 完整输出 | 判定 |
|---|---|---|---|---|---|---|---|
| 官方 DeepSeek | RQ1 | ✅ | 7 | ✅ | ✅ completed | 2108 chars / 2 IDs | **PASS** |
| 官方 | RQ2 | ✅ | 18 | ✅ | ✅ | 2597 chars / 10 IDs | **PASS** |
| 官方 | RQ3 | ✅ | 19 | ✅ | ✅ | 8293 chars / 17 IDs | **PASS** |
| overlay（Doubao 临时 patch） | RQ1 | ✅ | 4 | ✅ | ✅ | 1287 chars / 2 IDs | **PASS** |
| overlay | RQ2 | ✅ | 7 | ✅ | ✅ | 2607 chars / 6 IDs | **PASS** |
| overlay | RQ3 | ✅ | 11 | ✅ | ✅ | 5263 chars / 16 IDs | **PASS** |
| overlay | RQ4 | ✅ | 3 | ✅ | ✅ | 239 chars / 2 IDs | **PASS** |
| overlay | RQ5 | ✅ | 2 | ✅ | ✅ | 658 chars / 5 IDs | **PASS** |

- IDs 全部可解析到真实卡/来源（0 missing）；官方 3/3、overlay 5/5 五项全满足。
- 说明：证据来自 engineer 运行的 artifacts；本轮为**独立事件解析 + ID 解析**，未重跑 headless（时间/网络）；判定为 PASS（五项齐全），并注明非本轮新执行。

## 5. 回归（P5-B 树）

| 套件 | 结果 |
|---|---|
| validate | **PASS 400/400**（211 来源，0 错误 0 警告） |
| build_sources | **PASS 211/211**（CSV 212 行） |
| acceptance | 见 §5.1（本批次自动化） |
| quality_eval | 见 §5.1 |
| workflow | **NOT_RUN**（当前树重跑未完成；见 §5.1；不写 PASS） |
| composer / Macbeth | 见 §5.1 |
| R1.1 新测试（security/lookbook/skill-sync/backup/human） | 见 §5.1 |
| relation migration tests | **PASS 8/8**（前轮 P5-A 后未改迁移器） |

### 5.1 本批次结果（当前 P5-B 树，独立执行）

| 套件 | 结果 | 证据 |
|---|---|---|
| validate | **PASS 400/400**（211 来源，0 错误/警告） | 本轮直接执行 |
| build_sources | **PASS 211/211** | 本轮直接执行 |
| relation migration tests | **PASS 8/8** | `tests/test_relation_migrate.py` EXIT 0 |
| security/path_guard | **PASS 7/7** | EXIT 0 |
| Look Bible | **PASS 6/6** | EXIT 0 |
| skill sync | **PASS 3/3** | EXIT 0 |
| backup | **PASS 7/7** | EXIT 0 |
| human closeout | **PASS 3/3**（28.8s） | `/tmp/p5b_heavy.out` |
| composer | **PASS 9/9**（18.8s） | `/tmp/p5b_heavy.out` |
| Macbeth | **NOT_RUN**（重跑进程在验收窗口内未完成，已终止；不写 PASS） | `/tmp/p5b_heavy.out` |
| acceptance / quality_eval / workflow | **NOT_RUN（当前树批处理多次启动后长时间未完成；按规则不写 PASS）**。参考：P5-A 最终快照（P5-B 修正前）acceptance 45/45、quality 17/17、workflow 9/9（engineer log）；P5-B 只改关系/key_garments frontmatter，未改脚本 | `/tmp/p5b_tests*.out` |

## 6. 扩建计划审查（P5B-EXPANSION-PLAN）

- **是计划不是实施**：当前卡数仍 **400**（无新增卡文件；`git status` 无 A 卡）；plan 明确“本任务不实施任何补卡或卡片编辑”。
- **有证据基础**：缺口来自 `P5B-RELATION-COVERAGE.md`/coverage-matrix（garment→component 18%、material 40%、style 2%、outfit 0%；pattern 3 张；来源 68 未引用），不是拍脑袋。
- **无大规模扩卡**：P1 建议 material/pattern 6–8 张、component 2–3 张；P2 鞋履配饰/period 4–6 张；P3 future_topic 只进 backlog；总量 ~12–17 张（相对 189 内容卡约 6–9%），且要求真实 SRC/不硬连、38 draft 不动。
- 结论：**合理、证据支撑、非大规模扩卡**；需人工/领域 owner 按 P0→P3 执行。

## 7. Obsidian GUI

**NOT_RUN / PENDING**：本次未打开 Obsidian、未做渲染/点击/图谱截图；不得声称 GUI 通过（独立清单见 `reports/P5-HUMAN-UAT.md`）。

## 8. 残留风险

1. GAR-0045→SRC-0405 为 formal relations 中唯一无可见链接（medium review），如未来升级必须补可见链接/来源 scope。
2. 6 对 key_garments flag review 未删除（review_queue），虽不进 recommend/outfit，但在查询/审阅中仍可见；需人工结论。
3. P5-A 候选 CSV 仍含 rejected 行（未更新，不在 P5-B 写范围）；下游必须读 P5B-RELATION-CORRECTIONS.csv 过滤（`relation_migrate.py` 重跑前需应用 excluded 列表）。
4. 38 draft 未迁移（106→108 source_ids 不可见，因 WEAK-07 移除连带 1 个可见链接）；65 来源语义单点不变（34 legit_reference /16 evidence_missing_expression /14 future_topic /1 no_verifiable）。
5. Agent E2E 证据为 engineer artifacts，本轮独立解析 PASS，但未重新执行 headless。
6. workflow 若仍 hang → NOT_RUN（不写 PASS）。
