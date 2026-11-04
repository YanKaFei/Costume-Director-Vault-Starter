# P5-A 图谱 QA（P5-GRAPH-QA）

- 生成：2026-11-05 01:24；verifier / task-63；快照：最终工作区（迁移后 400 卡 / 211 来源；HEAD 仍 `1acb4d3`，迁移 174 项未提交）
- 性质：只读验收；证据：`/tmp/p5_after.json`、`/tmp/p5_after.csv`、`/tmp/p5_relation_sample.json`、`11-验收/P5/*`、各回归日志
- 结论：**关系迁移抽样 26/26 PASS；图谱 After 指标显著改善（见 P5-GRAPH-AFTER）；R1.1 回归除 workflow 外全 PASS（workflow NOT_RUN，见 §4）；Agent 检索 PARTIAL/BLOCKED（见 §5）。**

## 1. 新关系抽样（≥20：实际 26 条）

从当前树 142 张卡 / 201 条 `relations` 中抽 **26 条**（16 `claim_supported_by` + 8 `in_style` + 2 `uses_material`），逐条回到真实卡/源验证：

| 检查项 | 结果 |
|---|---|
| target ID 真实存在（GAR/STR/MAT/STY/PRD/LOOK/SCN/SRC 文件） | **26/26 PASS** |
| 结构化依据：`claim_supported_by` → 同卡 `source_ids`；`in_style` → `style_tags` 精确 STY；`uses_material` → materials token 映射 | **26/26 PASS** |
| 正文可见 `[[target]]` 链接存在 | **26/26 PASS** |
| 元数据：direction/evidence/confidence/rule 齐全且 high/verified | **26/26 PASS** |
| 无关键词硬连/无猜测（仅结构化字段生成） | **26/26 PASS** |

抽样代表：GAR-0072→SRC-0453/0454；GAR-0014→SRC-0115；GAR-0074→SRC-0458/0459/0460；PRD-0002→STY-0001、PRD-0001→STY-0010；GAR-0020→MAT-0001、PRD-0002→MAT-0001。逐条明细 `/tmp/p5_relation_sample.json`。

## 2. 事实/原文完整性

- 卡片 diff：**142 文件，+536 / −0**（无任何删除行）。
- 无 `id/type/evidence_status/review_status/license_status` 改动；`source_ids` 字段未被修改（仅追加 `relations` 与来源链接）。
- 无卡片删除；`git status` 中内容卡均为 M，无 D。
- 迁移备份：`11-验收/P5/backup.json` = 1455 文件/23,890,769 bytes，`backup-restore.json` 恢复 **0 mismatches**；rollback 目录/清单存在（`rollback-20261105-011701` 等）。
- 迁移 artifacts：`migration-report.json`（dry-run，queue 981）、`pilot-report.json`（pilot 30 卡/34 关系/34 链接、non_idempotent 43）、`full-report.json`（113 卡/168 关系/157 链接）、`graph-summary.json`（nodes 400/edges 201/unresolved 0）、`RELATION-CANDIDATES.csv` 677、`REVIEW-QUEUE.csv` 981、`source-audit.csv` 211。
- **迁移报告**：`reports/P5-RELATION-MIGRATION.md` 已生成（01:18），与 `11-验收/P5/*.json` 一致；其 §0 记录 **P0 事故**：首轮全量写入产生 **29 张坏 frontmatter**（closing fence 缺换行），`validate` 371/400 失败；**未提交**，从 `/tmp/p5-backup` 恢复后重跑，现 validate **400/400 PASS**、`build_sources` PASS，0 source_ids 差异。**P0 已修复，但提示迁移写入必须带 fence 校验**。

## 3. 迁移一致性

- 当前树实际合并：**142 卡 / 201 关系**（claim 191 / style 8 / material 2；全部 high+verified）；来源可见链接 **191 条新增**（+原有 2 = 193 content→source 对）。
- 38 张 draft 卡（look 22 / scene 15 / style 1）未迁移（source_ids 106 条仍不可见）——按策略保留至审核；不是伪造/丢失。
- 幂等/回滚：迁移工具有 rollback 目录与 manifest；pilot 记录 non_idempotent 列表（43 卡），full 批次记录 0；回滚未在本次 QA 执行（只读）。

## 4. R1.1 回归（当前树）

| 套件 | 结果 | 证据 |
|---|---|---|
| validate | **PASS 400/400**（211 来源，0 错误 0 警告） | `/tmp/p5qa_validate.txt` |
| build_sources | **PASS 211/211**（CSV 212 行） | `/tmp/p5qa_build.txt` |
| acceptance | **PASS 45/45** | `/tmp/p5qa_acc.log` |
| quality_eval | **PASS 17/17**（relevant@5 4.16、precision 0.929、0-hit 0） | `/tmp/p5qa_qeval.txt` |
| workflow | **NOT_RUN/INCOMPLETE（当前树 hang：test_workflow.py 进程 0% CPU >5min，已终止；不写 PASS）**；迁移前 R1.1 基线 9/9 PASS（`/tmp/r1f_wftest.log`） | `/tmp/p5v3_wf.log` |
| composer | **PASS 9/9** | `/tmp/p5qa_composer.log` |
| Macbeth | **PASS 11/11** | `/tmp/p5v4_macbeth.log` |
| Look Bible | **PASS 6/6** | `/tmp/p5qa_lookbook.log` |
| hard constraints/abc_eval | **PASS 7/7** | `/tmp/p5qa_cd.log` |
| path_guard/security | **PASS 7/7** | `/tmp/p5qa_sec.log` |
| skill sync | **PASS 3/3** | `/tmp/p5qa_sync.log` |
| backup | **PASS 7/7** | `/tmp/p5qa_backup.log` |
| human closeout | **PASS 3/3** | `/tmp/p5qa_human.log` |
| relation migration tests | **PASS 8/8**（dry-run/幂等/rollback/仅引用来源/保留 source_ids 与原文） | `/tmp/p5v4_relation.log` |

> 注：并发/重复进程导致部分套件首轮日志混杂；已清理并用独立输出重跑，以最终数字为准。**workflow 当前树 hang 未能复跑通过，明确标 NOT_RUN，不写 PASS。**

## 5. Agent 关系检索（真实 headless）

- **官方 DeepSeek**：`skill=1`、tool_calls=46、events=163；**已产生 final 答案**；但事件流无 `turn_end`（进程在 final 后被终止/不完整），**不能计 PASS** → 判定 **PARTIAL（内容部分可核）**。
  - 可核内容：GAR-0002 仅有 1 条 `claim_supported_by → SRC-0103`（与真实 `relations`/`source_ids` 一致）；GAR-0084 仅有 `claim_supported_by → SRC-0524`（一致）；提到 LOOK-0003，实测其 `look_items` 含 GAR-0002；并明确指出「没有 has_part/uses 关系」——与当前 frontmatter 一致（未编造）。
  - 结论：**答案内容未发现编造；但 run 不完整，正式判定 BLOCKED/PARTIAL，不算 Agent E2E PASS。**
- **Doubao overlay**（临时 `--patch /tmp/dsh-doubao.yml`，未改 profile）：`skill=1`、tool_calls=22、events=86；产生 final（约 334 字符，内容截断）；**无 turn_end**、无完整答案回填 → 判定 **PARTIAL/BLOCKED（传输/执行不完整）**。
- 判定：**Agent 关系检索本轮不能宣称可靠 PASS**；仅能说「官方 final 中的可核声明与真实数据一致，overlay 未完成」。需要在稳定网络/更长时间下重跑，完成 `turn_end.completed` 后再评。

## 6. QA 结论

- 关系迁移：**抽样 26/26 PASS**；事实零删除、evidence_status 未改、备份/回滚证据在。
- 图谱 After：来源可见引用 2→143（100% 机器引用来源可见），内容 SRC 不可见 180→38（draft 保留）；语义分量不变属正确设计（MOC ≠ 语义）。
- 回归：**核心套件除 workflow 外全部 PASS**（validate 400、build 211、acceptance 45、quality 17/17、composer 9/9、Macbeth 11/11、relation 8/8、R1.1 新测试全 PASS）；**workflow 当前树多轮重跑均未完成（慢/挂起），判 NOT_RUN，不写 PASS**（迁移前基线 9/9）。
- **遗留**：38 draft 未迁移；65 来源单点/68 未引用属真实独立/待接入；迁移树未提交（HEAD 1acb4d3，235 项工作区改动）；**workflow 当前树 hang（NOT_RUN）**；**Agent headless 两路均无 turn_end（PARTIAL/BLOCKED，不写 PASS）**。
