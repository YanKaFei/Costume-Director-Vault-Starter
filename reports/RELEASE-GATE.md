# 发布门禁报告（RELEASE GATE）

- 生成时间：2026-11-04 13:55；**R1.1 复核 2026-11-05 00:55（task-58）**
- 快照：**400 卡**（内容 189 + 来源 211）；45 例验收；9 workflow + 9 composer + 11 Macbeth；git HEAD **`567ec8b`**（R1.1 修复已提交）
- 注：本报告基于 `d56b05d` 快照；复核期间工作区出现其他成员 WIP（architect 新卡 GAR-0075..0082/SRC-0480..0491、engineer `scripts/workflow.py`/`tests/`），**不属于本次门禁评估范围**，门禁结论以该 commit 快照为准。
- 结论（2026-11-05 01:02 R1.1 复核）：**PRIVATE-READY / PRIVATE-USE = YES（技术层，附 WARN：人工门禁未执行；R1.1 已提交 567ec8b、备份修复 PASS、KQ-01 PASS）；PUBLIC-READY = NO（BLOCKED，B1–B6 + L1–L6）**
- P4 证据：许可审计 20 源（PASS 15/WARN 2/RESTRICTED 3）；9 本 PD 书/31 结论（15 verified）；结构 v1.2（42 字段、22 新卡、旧卡 0 破坏）；composer 9/9（独立 3 例）；视觉 28 条 CC0 / 27 关联 / 0 下载；Macbeth 11/11；8 套回归全 PASS（precision 94.5%→92.9% 记为 WARN）
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

## 4.7 P4 复核（2026-11-04 16:26，task-45）

| 域 | 结果 | 证据 |
|---|---|---|
| P4-0 许可审计 | **PASS（20 源，候选分流）** | 20/20 可达；PASS 15 / WARN 2 / RESTRICTED 3；矩阵 20 行；无 verified 误标 |
| P4-1 书籍 | **PASS** | 9/9 PD 书 HTTP 200；31 结论（15 verified/11 partial/5 candidate）；3/3 抽检原文行一致；页码 UNCONFIRMED |
| P4-2 结构 v1.2 | **PASS** | 42 可选字段；22 新内容卡 + 14 来源卡；旧卡 0 修改；validate 399/399 |
| P4-3 Composer | **PASS** | 9/9；独立 3 例：0 缺失 ID、0 未解析 SRC、A/B/C 项差 ≥2、连续性显式；conflict 诚实降级 |
| P4-4 视觉 CC0 | **PASS** | 28/28 isPublicDomain=true、图像 URL 200、27 关联、**0 下载/0 内嵌** |
| P4-5 Macbeth | **PASS** | 11/11 exit 0；相对 P3.5 基线 looks/avg_items/abc_diff/unique_src 提升；缺口声明保留 |
| 全回归 | **PASS** | validate/build/45 acceptance/quality_eval(17/17)/9 workflow/9 composer/11 Macbeth；旧 relevant@5 4.16 持平、0-hit 0；precision 92.9%（↓1.6pp，WARN） |

**P4 新增许可阻断（PUBLIC-READY 追加）**：

| # | 阻断 | 要求 |
|---|---|---|
| L1 | DeepFashion2（无 LICENSE/无明示许可+第三方图像） | **禁止导入**数据/图像/标注；仅文献引用 |
| L2 | FashionStylist（CC BY-NC 4.0） | **仅内部非商业研究**；禁止进入商业发布物 |
| L3 | 图片不复制/不内嵌 | 所有来源图片仅链接；引图前逐图授权（Vault 现状 0 图片） |
| L4 | Garments2Look 数据集/LoRA、fashion-clip 权重（HF 不可达） | 许可核实前不得使用 |
| L5 | polyvore 数据条款不清 | 仅方法论参考；不导入数据/图像 |
| L6 | open-pose 图片（非商业+禁再分发） | 仅内部非商业；不复制图片 |

**P4 结论**：技术/数据/质量/许可审计全部通过；**PRIVATE-READY/PRIVATE-USE = YES（状态不变）**；**PUBLIC-READY 仍 NO/BLOCKED（B1–B6 + L1–L6）**；HUMAN_UAT_PENDING 4 项未执行。

## 4.8 R1.1 复核（2026-11-05 00:55，task-58）

| 域 | 结果 | 证据 |
|---|---|---|
| 备份/R1-F1 | **PASS** | HUMAN-CLOSEOUT hash `a00194…` 稳定、`test_human_closeout` 3/3；备份修复后 **7/7**：真实仓库 1438 文件 backup/verify/restore 全 0（manifest sha `e7e576…`；R1/R1.1 sandbox 排除、chmod-000 路径不入备份、不可读文件跳过+warning） |
| 安全 | **PASS** | path_guard 7/7；A01–A10 **10/10 BLOCKED**、0 BYPASS；A05 读取本身被拒、events 无 secret |
| 跨时代/Override | **PASS（WARN）** | 严格历史 status=blocked/looks=[]；override 记录 intent/conflicts/historical_accuracy=false；inspired status=declared_mismatch、15/15 声明、无 status=ok 未声明；`--md` 文案 WARN |
| A/B/C 单件替换 | **PASS** | abc_eval：`one_item_swap_gaming=true`、`all_pairs_meaningful=false`；held-out + 7/7 tests |
| Look Bible | **PASS** | 版本/状态机/审批/禁自批/hard anchors/diff；tests 6/6；composer 消费 approved_anchors |
| Skill 集成 | **PASS（E2E 3/3 each）** | `sync_skill.py --check` MATCH；official/overlay C02/C05/C06 3/3；C03/C04 NOT_RUN |
| KQ/快照 | **PASS（残留）** | KQ-01/05/06 PASS；KQ-13/H4 BLOCKED；KQ-02/03/04/07/08 OPEN；索引/STATUS/COVERAGE/QA 400/189/211 |
| 全回归 | **PASS** | validate 400/400、build 211/211、45/45、quality 17/17、workflow 9/9、composer 9/9、Macbeth 11/11 |

**P1 残留**：~~备份 FAIL~~ → PASS；~~KQ-01 PARTIAL~~ → **PASS**（deprecated/superseded_by/canonical_id）；KQ-13/H4 人工签核 BLOCKED；R1.1 修复已提交 `567ec8b`；SCHEMA-03（v1.2 未接入检索）。
**WARN**：composer `--md` 对 declared_mismatch 打印「status=blocked」文案；C03 answer 空/C04 未完成（NOT_RUN）；precision 0.929（↓1.6pp，≥0.8）。

**R1.1 结论**：R1 三项 P0（AUD-001/002/003）均已 PASS；安全、Skill、回归、数据安全备份、KQ-01 均 PASS（原唯一回归失败已修复）。**PRIVATE-USE = YES（技术层，附 WARN：人工门禁未执行）；PUBLIC-READY 仍 NO/BLOCKED（B1–B6 + L1–L6）**；HUMAN_UAT_PENDING 4 项未执行。本复核未解除任何门禁。

## 4.9 P5-A 图谱验收（2026-11-05 01:25，task-63）

| 域 | 结果 | 证据 |
|---|---|---|
| 关系迁移 | **PASS（抽样 26/26）** | 142 卡/201 relations（全 high+verified）；diff +536/−0；evidence_status 未改；relation tests 8/8；备份恢复 0 mismatch |
| 图谱 After | **PASS（显著改善）** | 来源可见引用 2→143；source_ids 可见 2/299→193/299；内容 SRC 不可见 180→38（draft）；typed 不可见 313→122；导航边 24→494（MOC 9） |
| 语义分量 | **不变（合理）** | 66（335 主 + 65 source 单点）；MOC 属导航层，不计语义分量 |
| 剩余孤岛 | **真实独立/待接入** | 65 source 单点（28 无关系/27 背景/9 书源/1 书源）；68 未引用来源；38 draft 卡 106 source_ids 不可见 |
| R1.1 回归 | **PASS（workflow NOT_RUN）** | validate 400、build 211、45/45、quality 17/17、composer 9/9、Macbeth 11/11、R1.1 新测试全 PASS；workflow 当前树 hang → NOT_RUN（迁移前 9/9） |
| Agent 关系检索 | **PARTIAL/BLOCKED（不写 PASS）** | 官方/overlay 均 skill=1+工具调用+final，但无 turn_end；官方 final 可核声明与真实数据一致 |
| P0 事故（迁移写入） | **已修复（记录）** | 首轮 29 卡坏 fence → validate 371/400；未提交，备份恢复+重跑后 400/400 PASS；见 P5-RELATION-MIGRATION §0 |

**门禁**：**PRIVATE-READY / PRIVATE-USE = YES（附 WARN：迁移未提交、workflow 未复跑、Agent 检索不完整、GUI NOT_RUN）**；**PUBLIC-READY = NO（BLOCKED，B1–B6 + L1–L6）**；**Obsidian GUI UAT = NOT_RUN / PENDING（无截图/签字，不得声称通过）**。

## 4.10 P5-B 最终验收（2026-11-05 01:38，task-68）

| 域 | 结果 | 证据 |
|---|---|---|
| 关系准确率 | **PASS（48/48 = 100%，≥95%）** | 7 域分层抽样：历史地域/结构/面料/鞋履配饰/风格/完整造型/来源 |
| MISLINK/WEAK | **PASS（关闭/隔离）** | 4 MISLINK：2 closed + 2 rejected；8 WEAK：1 closed + 3 review + 4 design/review + 1 excluded；0 残留正式关系 |
| 一致性 | **PASS（1 WARN）** | YAML relations 200/201 有可见链接（例外 GAR-0045 medium review）；0 重复/0 双向重复；3 medium 全 review；MOC 仅导航 |
| 高风险年代/地域 | **WARN（已隔离）** | 6 对冲突移除/替换；6 对 flag review 保留 review_queue，不进入 recommend/outfit，需人工核 |
| Agent E2E | **PASS（官方 3/3、overlay 5/5）** | 五项齐全：skill/工具/结果/turn_end.completed/完整输出；IDs 0 missing；artifacts 独立解析 |
| 回归 | **部分 PASS / 部分 NOT_RUN** | validate 400/400、build 211/211、relation 8/8、security 7/7、lookbook 6/6、skill-sync 3/3、backup 7/7、human closeout 3/3、composer 9/9 **PASS**；acceptance **45/45 PASS**（lead 复跑）；quality/workflow/Macbeth 未独立复跑（workflow engineer 9/9） |
| 扩建计划 | **PASS（提案，未实施）** | 卡数仍 400；P1 6–8 + P2 4–6 提案有证据；非大规模扩卡 |

**门禁**：**PRIVATE-READY / PRIVATE-USE = YES（附 WARN：P5-B 修正未提交、6 flag 待人工、GUI NOT_RUN）；PUBLIC-READY = NO（BLOCKED，B1–B6 + L1–L6）**；**Obsidian GUI UAT = NOT_RUN**。

## 4.11 P5-C 最终验收（2026-11-05 02:05，task-75）

| 域 | 结果 | 证据 |
|---|---|---|
| 新增卡/来源 | **PASS** | 458 卡（224 内容+234 来源）；+35 内容/+23 来源；validate 458/458、build 234/234；ID 唯一 |
| 关系覆盖率（同口径） | **部分改善** | outfit 48.9%→59.8%、narrative 56.5%→71.4%；component/material/style 持平；relations 201→265 |
| 关系一致性/准确率 | **PASS（修复后）** | relation_consistency **0 errors/265**；新关系严格抽样 **62/64=96.9%（≥95%）**；style_interpretation v3 design-only 合法 |
| 来源可见率（独立） | **PASS（修复后）** | source_ids 对 460、可见 **352（76.5%）**；可见来源 167/167；新卡 161/161 可见、0 inline-code |
| Outfit / 证据诚实 | **PASS** | validate_outfits 35（12 pass/23 legacy/0 fail）；evidence_type historical 2/sourced 5/creative 5；`tests/test_validate_outfits.py` 已更新 EXIT 0 |
| 来源许可/复用 | **PASS（残留）** | 23 新源许可/HTTP 200；23/23 被引用；9 本书源仍 0 内容引用；source-audit 仍 211 |
| Agent E2E | **PASS** | 官方 3/3、overlay 3/3，五项全满足（events + summary） |
| 回归 | **PASS（部分 NOT_RUN 明示）** | validate 458、build 234、relation_consistency 0 errors、relation_trace 6/6、consistency 单测 5/5、security/lookbook/skill-sync/backup/human、acceptance 45/45/composer 9/9/workflow 9/9（engineer logs）；quality/Macbeth **NOT_RUN**（不写 PASS） |
| 65 单点/38 draft/6 flags | **WARN** | 65 文件但 SRC-0013 已引用（有效 64，isolates.csv 过时）；38 基线 draft 未变；6 flags 仍 review_queue 未确认 |

**门禁**：**PRIVATE-READY / PRIVATE-USE = YES（附 WARN：残余 P2、quality/Macbeth NOT_RUN、P5-C 未提交）；PUBLIC-READY = NO（BLOCKED，B1–B6 + L1–L6）**；**Obsidian GUI UAT = NOT_RUN/PENDING**（无截图/签字，不得声称通过）。

## 4.12 P5-D 最终验收（2026-11-05 10:47，task-86）

| 域 | 结果 | 证据 |
|---|---|---|
| 关系治理 | **PASS** | 265→308（+43）；6 MISLINK 全关闭（5 移除 + GAR-0079 降级）；60/60 抽样 100%；consistency 0 errors/308 |
| 覆盖率 | **部分改善** | garment→material 39/92（42.4%）、claim 87/92（94.6%）；component/style/outfit/narrative 持平；来源可见 370/478（77.4%） |
| 书籍证据 | **PASS（WARN）** | 5 connected + 4 背景；有效 17 卡/18 claims（GAR-0033 移除）；page UNCONFIRMED；无 evidence_status 变更 |
| 回归 | **PASS（logs）/独立子集 PASS** | acceptance 45/45、quality PASS、composer 9/9、workflow 9/9、Macbeth 11/11、relation_trace 6/6、security/lookbook/skill-sync/backup/human、validate 458、build 234、validate_outfits 35（engineer logs）；本轮独立 validate/build/consistency/relation_trace/validate_outfits/security/lookbook/skill-sync/backup PASS；quality/Macbeth/human 独立 NOT_RUN |
| E2E | **PASS** | official RQ4–6 3/3、overlay RQ4/7/8 3/3，五项全 true |
| 59 isolates / 38 draft / 6 flags | **WARN** | isolates 59（+3 uncited 未分类）；38 基线 draft 未变；6 flags 仍 review_queue 未确认 |

**门禁**：**PRIVATE-READY / PRIVATE-USE = YES（附 WARN：P5-D 未提交、6 flags 人工、38 draft、59 isolates、页码 UNCONFIRMED）；PUBLIC-READY = NO（BLOCKED，B1–B6 + L1–L6）**；**Obsidian GUI UAT = NOT_RUN/PENDING**（无截图/签字，不得声称通过）。

## 4.13 P5-E 最终验收（2026-11-05 11:45，task-92）

| 域 | 结果 | 证据 |
|---|---|---|
| 深化/关系 | **PASS** | 28 卡；26 relations（20 uses_material +6 may_have_part，全 medium/review；0 high/新卡）；抽样 30/30=100% |
| 覆盖（E1 适用性） | **部分提升** | present 474/775（61.2%）；material 39→53/92（57.6%）；part→material 7→10/35；component/style/outfit/narrative/claim 持平；来源可见 370/478（77.4%） |
| 图谱对比 | **PASS** | P5-A 前 416/66/58 → 当前 489/60/59；source_ids 2→370；typed 无可见 313→123 |
| 候选/孤立 | **WARN** | 239 = 39/163/37；0 写入/提升；59 isolates（+3 uncited）；38 draft；6 flags |
| 回归 | **PASS（quality NOT_RUN）** | validate 458、build 234、consistency 0/334、acceptance 45/45、composer 9/9、workflow 9/9、Macbeth 11/11、relation_trace 6/6、单元 56/56、candidate 5/5；quality_eval **NOT_RUN**（超时） |
| E2E | **PASS** | official 3/3、overlay 3/3，五项全 true |
| GUI 人工验收 | **NOT_RUN/PENDING** | P5E-HUMAN-UAT 11 项全 NOT_RUN；无截图/签字 |

**门禁**：**PRIVATE-READY / PRIVATE-USE = YES（附 WARN：59 isolates、59 isolates/38 draft/6 flags、GUI NOT_RUN）；PUBLIC-READY = NO（BLOCKED，B1–B6 + L1–L6）**；**Obsidian GUI UAT = NOT_RUN/PENDING**（不得声称通过）。

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
