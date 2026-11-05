# P5-D 启动核对与基线（P5D-BASELINE）

- 生成：2026-11-05 10:28（Asia/Shanghai）；verifier / task-80（P5-D 启动核对，只读）
- 快照：**HEAD `5ae2c52`**（"P5-C: update reports to committed snapshot"；P5-C 已提交：42327d0 + 5ae2c52）；工作区仅 **21 个未跟踪 sandbox 目录**（无卡片/脚本改动）
- 规模：**458 卡 = 224 内容 + 234 来源**；`validate PASS 458/458`（0 错误/警告）；`build_sources PASS`（CSV 234 行）；`relation_consistency` **cards 458 / relations 265 / errors 0 / moc_skipped 9**
- 性质：只写本报告；未改卡片/脚本。

## 1. 基线表

| 项 | 值 |
|---|---|
| HEAD | **`5ae2c52`**；父 `42327d0`（P5-C: outfit knowledge, structure/material expansion, relation fix and QA） |
| 提交链 | f500289（P5-B）→ 42327d0（P5-C）→ 5ae2c52（P5-C reports） |
| 工作区 | 21 项未跟踪（`11-验收/R1.1/security/sandbox-A01..A10 + template`）；无 M/A 卡片/脚本改动 |
| 卡片 | 458 = 224 内容（garment 92 / garment_part 35 / look 35 / material 16 / style 16 / scene 16 / period_region 11 / pattern 3）+ 234 来源 |
| validate | **458/458 PASS**（0 errors/0 warnings） |
| build_sources | **PASS**；CSV 234 行 |
| relation_consistency | **0 errors / 265 relations** |
| 正式 relations | **265**：claim_supported_by 238 / style_interpretation 12 / in_style 8 / uses_material 7；evidence 252 verified / 13 interpretive；confidence 245 high / 20 medium |
| 来源可见率（独立） | source_ids 对 **460**、可见 **352（76.5%）**；可见来源 **167/167**（100%）；零可见 SRC 卡 **39 = 38 draft + GAR-0045（medium review）** |
| E2E 证据 | official RQ1–3 **3/3**、overlay RQ2–4 **3/3**（P5-C e2e/validation-summary.json；五项全 true） |
| 遗留 | isolates.csv 仍 65（SRC-0013 已引用→有效 64）；source-audit 211（23 新源未纳入）；9 本书源 0 内容引用；6 flags 仍 review_queue；GUI NOT_RUN |

## 2. P5-C 关系抽样未通过 2 条（62/64，identify）

抽样口径：P5-C 新增 64 条 formal relations（claim 47 / uses_material 5 / style_interpretation 12），按 target+结构化+**正文可见**+schema+证据/置信 严格核对；通过 **62/64 = 96.9%**（≥95% 目标已达标，但仍有 2 条严格失败，需 P5-D 处理）。

| # | 关系 | 类型/证据/置信 | 失败原因 | 影响 | 建议处理 |
|---|---|---|---|---|---|
| 1 | **GAR-0088（晚装长手套）→ MAT-0017（皮革）** | uses_material / verified / medium；rule=R-MAT-TOKEN；source_ids=SRC-0538 | 正文**没有** `MAT-0017` 提及或 `[[MAT-0017-…]]` wikilink；materials token=`kid_leather` → MAT-0017 为 token 级映射，正文无可见/无 review marker | 图谱中「长手套↔皮革」材料关系不可见；Agent 按可见链接回答时可能漏掉该材料关联；**证据本身不假**（SRC-0538 描述白色小羊皮） | 在 GAR-0088「相关卡片/材质」加 `[[MAT-0017-皮革]]` 可见链接，或降为 review 并在正文标 medium；重跑 consistency/抽样 |
| 2 | **STR-0029（泡泡袖）→ MAT-0001（平纹细布）** | uses_material / verified / medium；rule=R-MAT-TOKEN；source_ids=SRC-0533 | 正文**没有** `MAT-0001` 提及或 `[[MAT-0001-…]]` wikilink；materials token=`muslin` → MAT-0001 为 token 级映射，正文无可见/无 review marker | 结构卡「泡泡袖↔细布」材料关系不可见；影响同 #1，属设计/材料层弱关系 | 同上：补可见 `[[MAT-0001-平纹细布]]` 或标 review；不虚构来源 |

- 共同原因：P5-C 修复把 **claim→SRC** 全部可见；但 **uses_material 的 token 级关系**（R-MAT-TOKEN）仍只有 YAML 关系、没有正文可见链接/marker。这两个不是「事实错误」，而是「可见性/表达不完整」。
- 量化影响：严格抽样 62/64；证据-only（忽略可见）64/64；`relation_consistency` 0 errors（schema 允许 medium design/material 关系无可见），因此不影响一致性门禁，但影响 Agent 可见材料关系与抽样满分。
- 修复优先级：**P2**（非 P1；不阻断 P5-C 已重分类 PASS 的结论；P5-D 回填/QA 阶段处理）。

## 3. 门禁快速复核

- **PRIVATE-READY / PRIVATE-USE = YES**（技术层；P5-C 已重分类 PASS）
- **PUBLIC-READY = NO（BLOCKED）**：B1 GUI NOT_EXECUTED、B2 逐图版权 NOT_EXECUTED、B3 15 案例 NOT_SCORED、B4 62 draft、B5、B6；L1–L6 保持
- **HUMAN-UAT（GUI）= NOT_RUN/PENDING**（无截图/签字，不得声称通过）
- R1.1/P5 快速复核（本轮独立）：
  - validate **458/458 PASS**、build **PASS**、relation_consistency **0 errors**
  - **PASS**：relation_trace 6/6、security 7/7、lookbook 6/6、skill-sync 3/3、backup 7/7
  - **FAIL**：**human closeout 测试 1/3 FAIL**——根因不是 hash 覆盖（保护两测通过），而是第三测「HEAD 快照重跑生成器」中 **P4-MACBETH 生成器 FAIL 10/11**（见 §4），导致测试判失败。
  - P5-C E2E 五项（official 3/3、overlay 3/3）证据仍在 `11-验收/P5C/e2e/validation-summary.json`
- 6 flags：PRD-0004/0006/0007/0008/0011 key_garments 未变，仍 review_queue（人工）
- 38 基线 draft：保持；全库 draft 79
- singles：isolates.csv 65（有效 **64**，SRC-0013 已引用）

## 4. quality_eval 与 P4-MACBETH（当前树）

- 运行方式：独立子进程 + 超时（quality 240s、Macbeth 300s）。
- **quality_eval：PASS（EXIT 0，109.8s）**：**OVERALL PASS / QUALITY PASS**；relevant@5 **4.16**、precision **0.92**（P5-B 0.929；仍 ≥0.8）、0-hit **0.0**；日志 `/tmp/p5d_quality.log`。
- **P4-MACBETH：FAIL 10/11**（两路独立证据：① human-closeout 测试的 pristine HEAD `5ae2c52` 重跑；② 本轮当前树独立运行 EXIT 1 / 36.9s，同一失败）：
  - 唯一失败：**`stage_changes_Lady_Macbeth`**：`stage A-look item difference <2: {'rise-guilt': 0, 'rise-downfall': 4, 'guilt-downfall': 4}`（rise 与 guilt 的 A-look 完全相同）。
  - **具体变化（对比 f500289 基线）**：
    - 基线 lady_rise A：`GAR-0079, GAR-0076, GAR-0081, GAR-0080, GAR-0082`；lady_guilt A：`GAR-0009, GAR-0076, GAR-0084, GAR-0028, GAR-0082`（差异 3 件）
    - 当前 lady_rise A：`GAR-0009, GAR-0076, GAR-0081, GAR-0080, GAR-0082`；lady_guilt A 同上 → rise==guilt（同 5 件）
    - 即 **lady_rise 的 one_piece 从 GAR-0079 变为 GAR-0009**，导致两阶段 A 套完全一致；P5-C 新增 35 卡后 composer 候选/评分变化所致（待 engineer 定位评分/tie-break；P5-D 应优先修复，不得靠放宽测试）。
  - 对比：P5-B/P5-C 前基线为 **11/11 PASS**；P5-C 新增 35 卡后出现回归（可能为 composer 候选池/槽位选择受新卡影响；需 P5-D 定位修复）。
  - 证据：`/tmp/p5d_human_detail.log`（HEAD 快照：PASS 10/11 + FAIL 行）与 `/tmp/p5d_macbeth.log`（当前树：同一 FAIL）；wrapper `/tmp/p5d_tests.out`（`macbeth EXIT 1 36.9s`）。
- **human closeout：FAIL 1/3**（第三测因生成器退出非 0 失败；保护/元数据 2 测 PASS）。

## 5. 不一致清单（需 P5-D 注意）

1. **isolates.csv 过时**：仍 65 行，实际有效 64（SRC-0013 已被 MAT-0018 引用）。
2. **source-audit 白名单 211**：新 23 源（SRC-0530..0552）未纳入。
3. **9 本书源仍 0 内容引用**（仅研究文档；非强制引用）。
4. 2 条 uses_material 关系（§2）正文不可见（WARN/P2）。
5. **P4-MACBETH 回归 FAIL 10/11**（`stage_changes_Lady_Macbeth` A-look rise==guilt；当前树 + HEAD 快照双证据）——P5-C 新增 35 卡后出现，P5-D 必须先定位/修复（P1）；human closeout 测试因此 FAIL（非 hash 覆盖）。
6. quality_eval PASS 但 precision 0.92（P5-B 0.929；轻微漂移，仍 PASS）。
7. GUI 未执行；PUBLIC 门禁未解除。
