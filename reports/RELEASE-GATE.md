# 发布门禁报告（RELEASE GATE）

- 生成时间：2026-11-04 13:55；**最终复核 2026-11-04 14:05（task-33 / D5 关闭）**
- 快照：**363 卡**（内容 166 + 来源 197）；45 例验收；9 例 workflow tests；git HEAD `e30446d`（D5 doc 修正已提交）
- 注：本报告基于 `d56b05d` 快照；复核期间工作区出现其他成员 WIP（architect 新卡 GAR-0075..0082/SRC-0480..0491、engineer `scripts/workflow.py`/`tests/`），**不属于本次门禁评估范围**，门禁结论以该 commit 快照为准。
- 结论（2026-11-04 15:56 P3.6 复核）：**PRIVATE-USE VERIFIED = YES；PUBLIC-READY = NO（BLOCKED，B1–B6）**
- P3.6 证据：Skill 安装并可原生调用（2 次独立 headless 请求均 exit 0，事件含 `skill(costume-director)` + `scripts/query.py` bash 调用）；10/10 e2e 独立审计通过（ID/SRC 0 缺失、无错误）；KB 安全（纯新增 commit、projects 隔离、未推送、无许可改动）；validate 363/363、build_sources 197/197、acceptance 45/45、quality_eval OVERALL PASS（17/17）、workflow tests 9/9；**D1–D5 全部 CLOSED**
- 依据：技术/数据/质量门在 P3.3 已 PASS（`reports/P3-QA.md`），本轮补完 WARN 处置、62 张 draft 复核、GUI 清单、人工评分表、版权矩阵；**4 项人工门禁仍未执行**。
- 声明：本报告不修改任何卡片/脚本；所有「未执行」均如实标注，**无编造 PASS**。

## 1. 门禁总览

| 门禁 | 状态 | 证据 |
|---|---|---|
| 结构校验 `validate.py` | **PASS** | 343/343；17/17 PASS；0 错误 0 警告 |
| 来源对账 `build_sources.py --check` | **PASS** | 185/185 一致；CSV 186 行；R5 质量门有效 |
| 验收 `run_acceptance.py` | **PASS** | 45/45；query 命中 187+ |
| 质量评估 `quality_eval.py` | **PASS** | OVERALL PASS：relevant@5 4.16、precision 0.945、0-hit 0% |
| 回归 F1/F2/F3 | **PASS** | 4/4 exit0、1580s 3 looks、6/6 warnings |
| D2/D4/R1–R5/M1–M7 | **CLOSED** | 详见 `reports/P3-DEFECTS.md` |
| **H1 Obsidian GUI 人工验收** | **NOT_EXECUTED（HUMAN_UAT_PENDING）** | `reports/OBSIDIAN-UAT-CHECKLIST.md`（未执行） |
| **H2 逐图版权核验** | **NOT_EXECUTED（HUMAN_UAT_PENDING）** | `reports/COPYRIGHT-MATRIX.md`（0 图片/0 下载 = 现状安全，但未逐图核验） |
| **H3 15 案例人工评分签核** | **NOT_SCORED（HUMAN_UAT_PENDING）** | `11-验收/P3.5/人工评分表.md`（空白待填） |
| **H4 62 张 draft 人工复核** | **PENDING SIGN-OFF** | `reports/DRAFT-REVIEW.csv`（62 张已机械复核：38 建议 reviewed / 24 保持 draft；**未改任何卡**） |

## 2. 4 个 WARN 的处置（逐项）

> 来源：`reports/P3-QA.md` §0 W1–W4 / §5；P3-DEFECTS.md §4。处置状态定义：RESOLVED=已修复验证；ACCEPTED=书面接受为已知限制/非阻断；OPEN=仍需修复。

| ID | WARN | 处置 | 依据与后续 |
|---|---|---|---|
| **W1** | 15 案例中 8 例 rubric WARN（切题 0–1）：明制/未来基底/身份弧线 wardrobe-stage/跨文化仪式礼服 | **ACCEPTED（记为已知 KB 覆盖限制）** | 自动 rubric 7 PASS / 8 WARN / 0 FAIL；C01/C03/C04/C05/C06/C10/N4/N5 均有 warnings 诚实声明缺卡；不属于「编造/错配未声明」。**非发布阻断项**；P4 补卡（明/清、未来基底、弧线阶段化）后复评 |
| **W2** | C01 明末清初 A 套选莫卧儿 jama GAR-0071（跨文化近似） | **ACCEPTED（带 P4 动作）** | C01 有 region_mismatch/period 近似 warnings；context_refs={} 无假引用；属「最近可用证据」而非事实错标。P4 补明/清服饰卡或提高 region 硬约束；发布说明需注明该近似 |
| **W3** | P14/P24/P25 等 filtered 查询仅 3–4 条结果 | **ACCEPTED（非错误）** | P14 3 条全非 example 且全相关；T41 `query_no_example_top` PASS；属库内条目少 + example 默认排除的设计结果；不误导用户（无 0 命中、无错误排序）。P4 可补 pattern/style 条目 |
| **W4** | 证据覆盖 0.94（example/设计推断件无来源） | **ACCEPTED（符合设计）** | 验收阈值 evidence_coverage ≥0.65 已 PASS；4 张 example 卡按设计无来源；interpretive 42 张明确标注；validate 0 错误。发布说明需保留「example/interpretive」标签语义 |

**WARN 结论：W1–W4 全部 ACCEPTED（非阻断，附 P4 行动），无 OPEN。**

## 3. 62 张 draft 复核统计（`reports/DRAFT-REVIEW.csv`）

| 指标 | 数值 | 说明 |
|---|---|---|
| draft 总数 | **62** | garment 1 / look 23 / period_region 11 / scene 16 / style 11 |
| source_ids 引用总数 | **144** | 非 example 卡均解析到真实来源卡 |
| unresolved source_ids | **0** | 全部可解析 |
| 独立来源 URL | **53** | 全部 **HTTP 200**（curl -m 10 -L） |
| 建议 **REVIEWED-CANDIDATE** | **38** | 来源真实、URL 200、支持事实性引用；interpretive 已标注 → **待人工签核后**可 reviewed |
| 保持 **STAY_DRAFT** | **24** | 4 张 example（无来源属设计）+ 7 张 LOOK（来源与断言不匹配/弱）+ 13 张 SCN（虚构场景不可核实） |
| evidence_status 变更 | **0** | 全部保持原值；**未自动提升**任何卡 |
| 卡片/脚本修改 | **0** | 只读复核；review_status 亦未改（需人工） |

**STAY_DRAFT 明细（24）**：
- example（4）：GAR-EXAMPLE-001、LOOK-EXAMPLE-001、STY-EXAMPLE-001、SCN-0001；
- 来源弱/不匹配 LOOK（7）：LOOK-0011（1969 儿童玩具头盔作空间站证据）、LOOK-0013（混入日本 obi/中国云肩/1920s 女雨衣）、LOOK-0016（SRC-0409 实为 1600–1700 手杖，误标 1940s 军装外套）、LOOK-0017（1980s 阶段无 1980s 来源）、LOOK-0018（kente/adinkra 断言无对应来源）、LOOK-0021（SRC-0115 为 1950s 概览误标牛仔裤语境）、LOOK-0022（SRC-0409 误标军装外套）；
- 虚构场景（13）：SCN-0004/0005/0006/0007/0008/0009/0010/0011/0012/0013/0014/0015/0016（场景/人物不可由来源核实；SCN-0008/0012 另含不匹配引用）。

**建议（H4 人工复核动作）**：对 38 张 REVIEWED-CANDIDATE 逐张签核后改 `review_status: reviewed`（evidence_status 不变）；对 24 张 STAY_DRAFT 重配来源/重写断言或保留 draft 并标注「设计推测」。**verifier 不执行任何改动。**

## 4. 版权门禁（`reports/COPYRIGHT-MATRIX.md`）

- 现状：**0 本地图片、0 内嵌、0 批量下载**；185 张来源卡全部外链。
- 许可分布：link_only 124 / other_permission 41 / cc0 17 / cc_by 3（内容卡 not_applicable 158）。
- 场景：A 外链引用 **允许**；B 内部研究 **允许**；C 公开传播：非商业 **条件性（须逐图核验 + 署名）**；商业 **阻断**（FIT NC 文本/other_permission/link_only 图像需许可或改写）。
- 关键待办：H2 逐图核验、FIT NC 许可复核、AAT/Fashionpedia 署名、法务签字。

## 4.5 P3.5 最终验证更新（2026-11-04 14:00，task-28）

| 项 | 结果 | 证据 |
|---|---|---|
| workflow 回归测试 | **9/9 PASS** | `python3 tests/test_workflow.py`（97.6s，含 `test_act_scene_stage_mapping`） |
| workflow fixture（Macbeth） | **PASS** | 11-验收/P3.5/workflow-runs/macbeth：scenes=3、stages rise/fall 分配、IDs/SRC 真实、evidence_complete、abc_distinct、continuity_issues=0、exit 0 |
| workflow 真实案例 | **PASS（D2 CLOSED）** | meta→S-id；resolver 支持 act-scene（`1-3→S1` 等）；案例 workflow-run 已重生成：scenes=4、stages `M1→S1/M2→S3/L1→S2/L3→S4`、exit 0 |
| LOOK+SCN 来源修复 | **7 LOOK + 2 SCN（=9 处）已修（D4 CLOSED）** | LOOK-0011/0013/0016/0017/0018/0021/0022 + SCN-0008/0012；新 SRC 全部解析、26 条 URL 抽验 200、与 items 匹配；DRAFT-REVIEW 45 CANDIDATE / 17 STAY |
| Macbeth 案例 | **完整性 PASS，产物一致性 FAIL（D2）** | 18 套 × 2 角色 × 3 阶段 × A/B/C；50 引用 ID 0 缺失；EVIDENCE 18 行 + 8 全局缺口；HUMAN-SCORE 18 行全空；6 组抽样 SRC URL 200；**case workflow-run 仍是修复前旧产物** |
| SOURCES.csv | **PASS（D1 CLOSED）** | 197/197 一致（CSV 198 行）；`quality_eval` **OVERALL PASS（17/17）**，`sources_csv_sync=1.0` |
| D5 文档（EVIDENCE §3.4 / CASE §4.4） | **CLOSED（doc-only）** | 文本已准确：支持 S-id + act-scene（1-3/1.3/1/3/1_3/Act 1 Scene 3）、映射 M1→S1/M2→S3/L1→S2/L3→S4；resolver 直接验证通过；LOOKS md5 未变（18 套） |

以上证据详见 `reports/P3.5-REPORT.md`（含缺陷 D1–D4）。

## 4.6 P3.6 复核（2026-11-04 15:56，task-37）

| 项 | 结果 | 证据 |
|---|---|---|
| Skill 安装/格式 | **PASS** | `.dsh/skills/costume-director/SKILL.md`（264 行；frontmatter name/description/whenToUse）；provider `skill`/`skill-filesystem`/`tool-skill` 已挂载 |
| 原生 headless 调用（独立） | **PASS（2 次请求）** | 我的 2 次 `dsh --profile headless --json`（Vault cwd）均 exit 0；事件含 `tool_call tool=skill name=costume-director` + `tool_result <skill_content>` + bash `scripts/query.py`；答案 ID/SRC 全部可解析、0 编造 |
| 10 例 E2E | **PASS 10/10** | 每例 1 skill + 4–10 脚本调用；8–22 个 ID、0 缺失；SRC 全解析；stderr 空、0 错误；T07 同 session、T08 缺口诚实、T09 冲突拒绝、T10 连续性与 English prompts |
| KB 安全 | **PASS** | commit `7afe02b` 纯新增 69 文件（无 M/D）；01–09/00-系统/scripts 无改动；`projects/` 用户资料 gitignore；`main` ahead 22 → 未推送；既有 license 未改；外部文本注入策略已写入 SKILL.md（运行时未测） |
| 导演材料 | **PASS（空白）** | 18/18 审阅；评分表 18×7 全 NOT_SCORED（无数字分）；OBSIDIAN-UAT 明确 HUMAN_UAT_PENDING/NOT_TESTED |
| 回归 | **PASS** | validate 363/363；build 197/197；acceptance 45/45；quality_eval 17/17 OVERALL PASS；workflow tests 9/9 |

**兼容性 caveat（必须披露）**：原 smoke 在 DeepSeek 官方路由 27 步后 **402 QUOTA**；e2e 改用 **Doubao Seed 2.1 临时 overlay**（`11-验收/P3.6/smoke/dsh-doubao.overlay.yml`，无 profile 改动）；我的独立原生验证需从本机 credentials store 注入 `DEEPSEEK_API_KEY`。**不声称 DeepSeek 官方路由已完成 10 例长会话。**

**P3.6 结论**：**PRIVATE-USE VERIFIED = YES**（Skill 可被 DSH 发现并原生调用、10/10 e2e 可用、KB 安全、无回归）；**PUBLIC-READY 仍为 NO/BLOCKED（B1–B6）**；HUMAN_UAT_PENDING 4 项不变。

## 5. 门禁结论

### PRIVATE-READY：**YES（可私有/内部使用）**

依据：
- 技术门禁全 PASS（validate / build_sources / 45/45 acceptance / quality_eval OVERALL PASS）；
- 版权矩阵 A/B 场景（外链引用、内部研究）现状合规：0 图片、0 下载、全部 link_only URL、署名保留；
- 62 张 draft 已逐卡给出复核结论（38 建议 reviewed、24 保持 draft），draft 状态不会误导（`review_status`/`evidence_status` 明确）；
- 已知限制 W1–W4 已书面接受并列入 P4；使用时需保留 example/interpretive 标签与 warnings。

**私有使用注意**：内部演示/研究中引用事实时保留来源链接与署名；不得把 warnings 中「缺口声明」误读为「已覆盖」。

### PUBLIC-READY：**NO（BLOCKED）**

阻断项（全部为人工/法务门禁，不是技术缺陷）：

| # | 阻断项 | 状态 | 解除条件 | Owner |
|---|---|---|---|---|
| B7 | SOURCES.csv 同步（D1） | **CLOSED** | 197 行、`--check` PASS、`quality_eval` 17/17 PASS | — |
| B1 | Obsidian GUI 人工验收（H1） | NOT_EXECUTED | 按 `OBSIDIAN-UAT-CHECKLIST.md` 执行 §2–§6，坏链 0、无解析错误、两人签字 | 人工/QA |
| B2 | 逐图版权核验（H2） | NOT_EXECUTED | 按 `COPYRIGHT-MATRIX.md` 逐图记录许可；无授权仅 link_only；确认 0 图片策略或取得授权 | 版权/法务 |
| B3 | 15 案例人工评分签核（H3） | NOT_SCORED | `11-验收/P3.5/人工评分表.md` 两名评分人完成 + Lead 复核签字 | 导演/服装/Lead |
| B4 | 62 张 draft 人工复核（H4） | PENDING SIGN-OFF | 对 38 建议 reviewed 逐张签核；24 STAY_DRAFT 处置（重配来源或保留 draft 说明） | Lead/architect |
| B5 | W1–W4 书面接受/发布说明披露 | ACCEPTED 待签字 | Lead 在发布说明中接受 W1–W4 与已知缺口（Mughal/明制/未来基底等） | Lead |
| B6 | 公开/商业传播许可复核 | PENDING | 非商业：FIT CC BY-NC-SA 署名+同方式共享；商业：FIT/other_permission 逐条许可或改写；法务签字 | 法务 |

**公开传播发布说明必须包含**：
1. 343 卡中 4 example / 42 interpretive 的标签含义；
2. 已知 KB 缺口（明/清、未来基底、身份弧线阶段化、跨文化仪式礼服）；
3. 所有来源许可状态与署名清单（cc0/cc_by/AAT/FIT 等）；
4. 「本库不内嵌第三方图片，仅外链；图片权利未逐图核验」的声明；
5. draft 卡（若保留）明确为「未人工复核」。

## 6. 签字与状态记录（人工填写）

| 角色 | 姓名 | 结论（PRIVATE/PUBLIC） | 签名/日期 |
|---|---|---|---|
| verifier（本报告） | verifier | PRIVATE-READY=YES；PUBLIC-READY=NO（技术门禁 PASS，人工门禁未执行） | 2026-11-04（机器生成，无签字效力） |
| Lead（发布决策） |  |  |  |
| QA/复核 |  |  |  |
| 法务（公开传播） |  |  |  |

> 本报告所有「PASS」仅指已执行的技术/数据检查；H1–H4 均为 **HUMAN_UAT_PENDING**，不得写成 PASS。PUBLIC-READY 在 B1–B6 全部关闭前保持 **BLOCKED**。
