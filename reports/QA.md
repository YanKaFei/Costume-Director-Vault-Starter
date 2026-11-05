# QA 报告（R1.1 快照索引）

- 更新时间：2026-11-05 01:03；快照 **400 卡 / 211 来源 / 45 例验收（PASS 45/45）**；git HEAD **`567ec8b`**（R1.1 已提交）
- 详细独立验收：[P3-QA.md](P3-QA.md)；缺陷：[P3-DEFECTS.md](P3-DEFECTS.md)；R1.1 修复证据：[R1.1-KNOWLEDGE-REPO.md](R1.1-KNOWLEDGE-REPO.md)；知识质量审计：[KNOWLEDGE-QUALITY-AUDIT.md](KNOWLEDGE-QUALITY-AUDIT.md)


## 0. R1.1 机械验收（2026-11-05）

| 项 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | **400/400 PASS；17/17 PASS；0 错误 0 警告；来源卡 211** |
| 来源对账 | `python3 scripts/build_sources.py` | 0 | **PASS（CSV 212 行 = 表头 + 211；0 缺失/0 多余/0 差异）** |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | **PASS 45/45**（重建；每份结果含 已知输入/假设/unknown/风险/证据） |
| 知识质量审计 | `python3 scripts/audit_knowledge.py` | 0 | 8 域；书籍定位 31/31；v1.2 0 违规；62 draft 可追溯（0 reviewed） |
| 索引/快照 | `00-系统/索引.md`、STATUS/COVERAGE/QA | — | R1.1 快照 400/189/211 一致（见 R1.1-KNOWLEDGE-REPO.md） |

### AUD-005（口径声明）

- **`11/11 PASS`（以及 45/45 PASS）是脚本断言结果，不等于导演/服装设计的艺术评价。** 脚本只验证：检索是否命中、是否给出 A/B/C、是否包含必要字段、连续性是否显式、prompt 是否可执行等机械条件。
- 艺术评价必须由人类填写：空白导演评分表见 [`11-验收/P3.6/导演评分表.md`](../11-验收/P3.6/导演评分表.md)（状态 **NOT_SCORED**，AI 不得代填；7 维 × 18 套）。
- 在导演评分表完成前，任何“PASS”均不得被解释为“造型可用/好看/符合导演意图”。

## 1. 机械验收（PASS）

| 项 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | 343/343；17/17 PASS；0 错误 0 警告 |
| 来源对账 | `python3 scripts/build_sources.py --check` | 0 | 185/185 一致（CSV 186 行含表头） |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | **PASS 45/45** |
| 质量评估 | `python3 scripts/quality_eval.py --no-write` | 0 | **OVERALL PASS**：relevant@5 4.16、precision .945、0 命中 0、CSV gate PASS |

## 2. 独立质量结论（P3.3）：PASS 24 / WARN 4 / FAIL 0 / HUMAN_UAT_PENDING 4

- **R7 关闭**：独立 raw relevant@5 **4.16（104/125）≥4.0**；precision **94.5%**；0 命中 **0%**；P21 Mughal 3 命中（GAR-0071/SRC-0450/GAR-0072）、P22 mourning jewelry 2 命中（GAR-0073/GAR-0074）均相关；与 engineer 自评一致。
- **R1/R2/R3/R4/R5 全部关闭**：六类职业含同义词匹配；P14 无 example、P02/T41 无同名重复；GAR-0065 改名「出口和服」；噪声 warning 移除；R5 质量门经「漂移→FAIL→恢复→PASS」实测有效。
- **D2/D4/M1–M7/F1–F3** 保持关闭；45/45、validate、build 全 PASS。
- **15 案例 rubric**：7 PASS / 8 WARN / 0 FAIL（切题均值 1.33/2）。
- **WARN 4**：W1 rubric 覆盖限制、W2 C01 跨文化近似、W3 filtered 结果数有限、W4 证据覆盖 0.94。

## 3. 结论

**技术/数据/质量门 PASS**（R7 关闭、R1–R5 关闭、45/45 验收、validate/build/quality_eval 全 PASS）。发布仍需完成 **HUMAN_UAT_PENDING 4 项**（Obsidian GUI、逐图版权、语义评分签核、62 draft 复核）；完成前不得对外宣布「全量 PASS」。


---

## 4. P3.6 Skill 原生调用验收（2026-11-04 15:56，task-37）

- 快照：363 卡（内容 166 + 来源 197）；45 例验收；9 workflow tests；HEAD `7afe02b`。
- **机械验收**：validate **PASS**（363/363，17/17）；build_sources **PASS**（197/197，CSV 198 行）；acceptance **PASS 45/45**；quality_eval **OVERALL PASS（17/17）**；workflow tests **9/9 OK**。
- **Skill 原生调用**：独立 2 次 Vault-cwd headless 请求 exit 0，事件含 `skill(costume-director)` + `<skill_content>` + bash `scripts/query.py`；答案 ID/SRC 全解析、0 编造。
- **10 例 e2e**：10/10 通过（skill+脚本调用、ID/SRC 0 缺失、无 stderr/错误；T07 同会话、T08 缺口诚实、T09 冲突拒绝、T10 连续性与 prompts）。
- **安全**：commit 纯新增（无既有卡/脚本修改）；projects 隔离；未推送（ahead 22）；无许可改动；注入策略有文档但未运行时验证。
- **导演材料**：18/18 审阅完整；评分表 18×7 NOT_SCORED（无数字分）；OBSIDIAN-UAT 为 HUMAN_UAT_PENDING/NOT_TESTED。
- **结论**：**PRIVATE-USE VERIFIED = YES；PUBLIC-READY = NO（BLOCKED，B1–B6）**；HUMAN_UAT_PENDING 4 项未变；兼容性 caveat（DeepSeek 402 / Doubao overlay）已披露。
- 详见 `reports/P3.6-REPORT.md`。


---

## 5. P4 最终验收（2026-11-04 16:26，task-45）

- 快照：399 卡（内容 188 + 来源 211）；45 acceptance；9 workflow；9 composer；11 Macbeth；HEAD `7f7a21b`。
- **机械门禁**：validate **PASS** 399/399（0 错误 0 警告）；build_sources **PASS** 211/211（CSV 212 行）；acceptance **PASS 45/45**；quality_eval **OVERALL PASS（17/17）**。
- **P4 专项**：许可审计 20 源分流（PASS 15/WARN 2/RESTRICTED 3，无 verified 误标）；9 本 PD 书/31 结论（15 verified，3/3 抽检原文行一致，页码 UNCONFIRMED）；结构 v1.2（42 可选字段、22 新卡、旧卡 0 破坏）；composer 9/9 + 独立 3 例（0 缺失 ID/0 未解析 SRC/A-B-C 差异/连续性）；视觉 28/28 CC0、27 关联、0 下载；Macbeth 11/11 + P3.5 基线对比（looks/avg_items/abc_diff/unique_src 提升）。
- **回归指标**：relevant@5 4.16 持平、0-hit 0 持平、recommend 指标全持平；**precision 94.5%→92.9%（−1.6pp，仍 ≥0.8）** → WARN 观察，非阻断。
- **门禁**：PRIVATE-READY/PRIVATE-USE = YES（不变）；PUBLIC-READY = NO（BLOCKED B1–B6 + L1–L6）；HUMAN_UAT_PENDING 4 项未执行、未代填。
- 详见 `reports/P4-REPORT.md`。


## 6. R1.1 最终验收（2026-11-05 00:55，task-58）

- 快照：400 卡（189 内容 + 211 来源）；HEAD **`567ec8b`**（R1.1 已提交）。
- **机械门禁**：validate **PASS** 400/400；build **PASS** 211/211；acceptance **PASS 45/45**；quality_eval **PASS 17/17**（relevant@5 4.16、precision 0.929、0-hit 0）。
- **R1.1 专项**：安全 path_guard 7/7 + A01–A10 全 BLOCKED；跨时代 blocked/declared + Override + A/B/C 单件 gaming；Look Bible 6/6；Skill 同步 MATCH + 官方/overlay 3/3；KQ-01/05/06 PASS、KQ-13/H4 BLOCKED；R1-F1 受保护 hash 稳定。
- **回归**：workflow 9/9、composer 9/9、Macbeth 11/11；新测试 5 套 PASS；**backup PASS（7/7；真实仓库 1438 文件 backup/verify/restore 全 0）**。
- **门禁**：PRIVATE-USE = YES（WARN）；PUBLIC-READY = NO（B1–B6 + L1–L6）；HUMAN_UAT_PENDING 4 项未执行。
- 详见 `reports/R1.1-REPORT.md` / `R1.1-REGRESSION.md` / `R1.1-DEFECT-CLOSURE.md`。


## R1.2 机械验收（2026-11-05 15:47）

| 项 | 结果 |
|---|---|
| validate | **PASS 458/458**（0 错误） |
| build_sources | **PASS 234/234**（CSV） |
| relation_consistency | **0 errors / 345 relations** |
| graph_analyze | **typed_unresolved 0 / unresolved {} / typed_edges 748 / components 60 / singletons 59** |
| acceptance | **PASS 45/45**（R1.2 log） |
| workflow | **PASS 9/9（141.9s OK）** |
| composer / Macbeth | **9/9 / 11/11 PASS** |
| quality_eval | **PASS**（lead 复跑：relevant@5 4.2、precision 0.921、0-hit 0） |
| E2E | **engineer R1.2-AGENT-REGRESSION：official 3/3、overlay 3/3 五项全 true**（selected final；早期探索失败不计） |
| GUI | **NOT_RUN/HUMAN_UAT_PENDING**（11 项：3 PARTIAL 截图、8 NOT_RUN；无签字） |

- 说明：PASS 仅指脚本/数据检查，不是艺术/历史评价；quality/E2E/GUI 未闭合项不得写成 PASS。


## R1.3 机械验收（2026-11-05 16:05）

| 项 | 结果 |
|---|---|
| validate | **471/471 PASS** |
| build_sources | **239 PASS**（CSV 与来源一致） |
| relation_consistency | **0 errors / 345 relations** |
| graph | **0 unresolved / 0 typed unresolved / 748 typed / 60 components / 59 singletons** |
| acceptance | **PASS 45/45（134.2s）** |
| quality_eval | **PASS（4.20 / 0.921 / 0）** |
| prompt tool | `visual_prompt.py` 测试 **9/9 PASS**；20/20 抽样无 CJK/wikilink/typo/截断，evidence tags 正确 |
| prompt 卡片块 | **21/23 含旧 CJK** → WARN；不得宣称 copy-ready English |
| E2E | official **3/3**、overlay **3/3** 五项全 true；no_image_claim_ok |
| 其他回归 | workflow 9/9（130.7s）、Macbeth 11/11（32.4s）、composer 9/9、relation_trace 6/6、security 7/7、lookbook 6/6、skill-sync 3/3、backup 7/7、human 3/3；prompt tool 9/9 |
| Obsidian scope | **501 / 0 zero / 1 component / 0 unresolved**（visuals 排除） |
| GUI | **NOT_RUN/HUMAN_UAT_PENDING**（3 PARTIAL 截图、8 NOT_RUN；无签核） |

- PASS 仅脚本/数据检查，不是艺术/历史评价；AI 未生图、未评分；人工视觉评分 **N/A**。


## R1.3B Batch2 QA（2026-11-05 17:35）

- 独立 20 条 Prompt QA：**18/20 通过**；2 失败 = STR-0023/STR-0011 缺 front/side/back（仅 45° detail）；CJK/坏链/typo/截断 **0**；evidence tags 正确；材质/颜色空字段写 unknown；同质化 3 对 >0.9（无精确重复）。
- engineer task-111：143 prompts；TEXT_VALID 139 / TEXT_INVALID 4；warnings 141；同质化 Jaccard≥0.80 597 对、scaffold≥0.82 1122 对 → **WARN**；DOMAIN_REVIEWED/IMAGE_TESTED/HUMAN_VISUAL_APPROVED = NOT_RUN；生图 0。
- 回归：validate 471、build 239、consistency 0/345、graph 0/0/764、Macbeth 11/11；task-111 的 acceptance/quality/workflow 日志为空 → **NOT_RUN**（另有当前独立重跑见 R1.3B-BATCH2-REPORT）；E2E Batch2 **official 3/3、overlay 3/3 五项全 true（no_image_claim）**；GUI NOT_RUN。


## R1.3B Batch3 QA（2026-11-05 18:00）

- 视觉 89/207；prompt **209**；TEXT_VALID **209/209**；warnings **192**；同质化 content Jaccard≥0.80 **650 对**、scaffold≥0.82 **1348 对** → WARN。
- 独立 20 样本 **20/20**；无 CJK/坏链/typo；evidence tags 齐全；REFERENCE_PENDING 正确；2 个曾 invalid（STY-0024/25）已由 task-114 修复为 TEXT_VALID。
- DOMAIN_REVIEWED/IMAGE_TESTED/HUMAN_VISUAL_APPROVED = **NOT_RUN**；生图 **0**；人工视觉评分 **N/A**。
- 不一致：`11-验收/R1.3B/summary.json` 仍 179/74/0/536/1149，未同步 209/89；以 PROMPT-QA.csv/header 为准。
- 回归：validate 473、build 239、consistency 0/345、graph 0、acceptance 45/45、quality PASS、workflow 9/9、Macbeth 11/11；E2E 最近 3/3+3/3（Batch3 专属报告未落盘→NOT_RUN/PARTIAL）；GUI NOT_RUN。
