# 运行状态（STATUS）— Costume Director Knowledge System（R1.1 快照）

- 更新时间：2026-11-05 00:33（Asia/Shanghai）；R1.1-G（task-56）快照
- 快照：**400 张卡**（内容 189 + 来源 211）；**45 例验收，PASS 45/45**；git HEAD **`567ec8b`**（R1.1 已提交）
- 外观：**PASS 24 / WARN 4 / FAIL 0 / HUMAN_UAT_PENDING 4（32 项）**（沿用 P3.3 外观结论，未重评）
- **发布门槛：技术/数据/质量门 PASS**；发布仍需完成 HUMAN_UAT_PENDING 4 项（H1 GUI / H2 逐图授权 / H3 15 例语义 / H4 62 张 draft 签核）
- R1.1 报告：[R1.1-KNOWLEDGE-REPO.md](R1.1-KNOWLEDGE-REPO.md) · [KNOWLEDGE-QUALITY-AUDIT.md](KNOWLEDGE-QUALITY-AUDIT.md) · [DRAFT-SIGNOFF-R1.1.md](DRAFT-SIGNOFF-R1.1.md)
- P3/P4 子报告：[P3-QA.md](P3-QA.md) · [P3-DEFECTS.md](P3-DEFECTS.md) · [P3-COVERAGE.md](P3-COVERAGE.md) · [P4-REPORT.md](P4-REPORT.md) · [CHANGELOG-P3.md](CHANGELOG-P3.md) · [NEXT-PLAN.md](NEXT-PLAN.md)


## 0. R1.1 快照（2026-11-05，task-56）

| 项 | 值 | 证据 |
|---|---|---|
| 卡片 | **400**（内容 189 + 来源 211） | `scripts/validate.py` 400/400 PASS；`run_acceptance.py` SUMMARY 卡片总数 400 |
| 前缀 | GAR 88（87 正式 + 1 example；GAR-0087 为 deprecated 重定向）/ STR 26 / MAT 14 / LOOK 23 / PRD 11 / SCN 16 / STY 11 / SRC 211 | `scripts/audit_knowledge.py` 加载统计 |
| 验收 | **45/45 PASS**（生成器重建，含 已知输入/假设/unknown/风险/证据 段） | `python3 scripts/run_acceptance.py` exit 0；`11-验收/测试结果/SUMMARY.md` |
| 来源对账 | PASS（CSV 212 行 = 表头 + 211） | `python3 scripts/build_sources.py` exit 0 |
| 质量审计 | KQ-06/KQ-13 修复、AUD-005 声明、索引/快照更新 | `reports/R1.1-KNOWLEDGE-REPO.md` |
| 仍开放 | H2 逐图授权、H4 62 张 draft 人工签核；P2 项（KQ-02/03/04/08）见知识质量审计 | 本报告第 4 节 + `reports/KNOWLEDGE-QUALITY-AUDIT.md` |

## 1. 阶段状态

| 阶段 | 状态 | 证据 |
|---|---|---|
| P0/P1/P2 | DONE | 字典/模板/索引、种子库、闭环 |
| P2.5 | DONE（历史） | 审计报告保留 |
| P3/P3.1/P3.2 | DONE | 修复与回归全部关闭 |
| **P3.3 最终复验** | **技术/质量门 PASS** | R7 关闭（relevant@5 4.16、0 命中 0%）；45/45；validate/build/quality_eval 全 PASS |
| 发布 | **待 HUMAN_UAT_PENDING 4 项** | NEXT-PLAN |

## 2. 当前可用

- 知识库 343 卡；`validate.py` exit 0（17/17 PASS，0 错误 0 警告）；链接可达；0 内嵌图片。
- 来源 185 张；`SOURCES.csv` 186 行（`build_sources --check` PASS；R5 质量门实测有效）；新增 11 张 V&A 来源 11/11 HTTP 200。
- 检索/推荐：**45/45 验收 PASS**；query relevant@5 **4.16**、precision **94.5%**、0 命中 **0%**；职业匹配（护士/医生/警察/厨师/宇航员/婚礼 + 巡警/民警/医师同义词）、雨具、室内禁极地派克、context 清洁、example 排除、查询去重均 PASS。
- 提示词 3 模板 + SKILL.md。

## 3. 已知问题（WARN 4，非阻断）

1. W1：15 案例中 8 例 rubric WARN（切题 0–1）——明制/未来基底/身份弧线/跨文化仪式礼服受 KB 覆盖限制（诚实声明）。
2. W2：C01 明末清初 A 套选莫卧儿 jama（跨文化近似，有 warnings）。
3. W3：P14/P24/P25 等 filtered 查询结果数仅 3–4 条（example 已排除，库内条目少）。
4. W4：证据覆盖 0.94（example/设计推断件无来源属预期）。

## 4. HUMAN_UAT_PENDING（不得写成 PASS）

- H1 Obsidian GUI 打开/渲染/wikilink 跳转
- H2 逐图版权授权核验
- H3 15 案例语义评分人工签核
- H4 62 张 draft 卡人工复核

## 5. 下一步

完成 4 项 HUMAN_UAT_PENDING → 发布清单签字；P4 可选改进见 NEXT-PLAN（W1–W4 与覆盖扩展）。


---

## 6. P3.5 最终验证（2026-11-04 14:00，task-28）

- 快照：**363 卡**（内容 166 + 来源 197）；45 例验收；git HEAD `04778f8`（工作区 clean）。
- 技术门禁：`validate.py` PASS（363/363）；`run_acceptance.py` **45/45 PASS**；`tests/test_workflow.py` **8/8 PASS**；`build_sources --check` **FAIL（缺 12 行 SRC-0480..0491）**；`quality_eval` **OVERALL FAIL（仅 sources_csv_sync=0）**。
- workflow：fixture Macbeth scenes=3、stages rise/fall 分配、IDs/SRC 真实、exit 0；**真实案例 meta 的 `"1-3"` 引用导致 stage 全 unassigned（D2）**，S-id 修正后分配正确。
- LOOK 修复：**7 张**（LOOK-0011/0013/0016/0017/0018/0021/0022）来源已对齐、URL 200；`reports/DRAFT-REVIEW.csv` 更新为 **45 REVIEWED-CANDIDATE / 17 STAY_DRAFT**（4 example + 13 虚构 SCN）；未改任何卡片。
- Macbeth 案例：18 套（2 角色×3 阶段×A/B/C）、50 引用 ID 0 缺失、EVIDENCE 18 行 + 8 缺口、HUMAN-SCORE 18 行空白（0 预填）、6 组抽样 SRC 200；产物 workflow-run 旧版需重生成（D2）。
- **发布门禁：PRIVATE-READY = YES（条件：先修 D1 CSV）；PUBLIC-READY = NO（BLOCKED）**。
- 阻断项：**B7 CSV 同步（新）**、B1 GUI UAT、B2 逐图版权、B3 人工评分签核、B4 draft 复核、B5 WARN 披露、B6 许可/法务。
- HUMAN_UAT_PENDING 4 项保持：Obsidian GUI / 逐图版权 / 15 案例人工评分 / 62 draft 复核。
- 详见 `reports/P3.5-REPORT.md`。


---

## 7. P3.5 收尾复验（2026-11-04 14:05，task-31）

- 快照：**363 卡**（内容 166 + 来源 197）；45 例验收；git HEAD 以 `git log -1` 为准（工作区 clean）。
- 门禁全部重跑：`validate.py` **PASS**（363/363，17/17）；`build_sources --check` **PASS**（197/197，CSV 198 行）；`run_acceptance` **45/45 PASS**；`quality_eval --no-write` **OVERALL PASS（17/17，sources_csv_sync=1.0）**；`tests/test_workflow.py` **9/9 OK**（97.6s）。
- workflow：案例 meta→S-id；resolver 支持 act-scene（1-3→S1 等）；Macbeth `workflow-run/` 已重生成（scenes=4、M1→S1/M2→S3/L1→S2/L3→S4、exit 0）；独立复跑一致。
- LOOK+SCN：**7 LOOK + 2 SCN（SCN-0008/0012）= 9 处来源修正**，URL 抽验 200；DRAFT-REVIEW 45 REVIEWED-CANDIDATE / 17 STAY_DRAFT；未改卡片。
- Macbeth 案例：18 套 × 2 角色 × 3 阶段 × A/B/C；50 引用 ID 0 缺失；HUMAN-SCORE 18 行全空（0 预填）。
- 缺陷：**D1–D4 全部 CLOSED**；D5（EVIDENCE §3.4 过时措辞）当时 OPEN（doc，非阻断）→ **已于 §8 关闭（CLOSED，doc-only）**。
- **发布门禁：PRIVATE-READY = YES；PUBLIC-READY = NO（BLOCKED）**；阻断 B1 GUI UAT、B2 逐图版权、B3 人工评分、B4 draft 复核、B5 WARN 披露、B6 许可/法务；**HUMAN_UAT_PENDING 4 项**保持。
- 详见 `reports/P3.5-REPORT.md`。


## 8. 最终收尾（2026-11-04 14:05，task-33）

- **HEAD**：本地最新提交（P3.5 修复 + 报告同步）；narrator 的 D5 文档修正（`EVIDENCE.md §3.4`、`CASE.md §4.4`）已随本提交收口。
- **快照一致性核对**：**363 卡**（内容 166 + 来源 197）；**45 例验收**；**9 例 workflow tests**；18 套 Macbeth LOOKS；HUMAN-SCORE 18 行空表；`SOURCES.csv` 198 行（197 + 表头）。
- **D5 CLOSED（doc-only）**：EVIDENCE §3.4 / CASE §4.4 已准确描述「workflow 支持 S-id 与 act-scene（1-3/1.3/1/3/1_3/Act 1 Scene 3），案例映射 M1→S1/M2→S3/L1→S2/L3→S4」；直接调用 `resolve_scene_ref` 验证全部写法正确（`9-9`→None 触发 warning）；LOOKS md5 `53549992cef442d2d3267a4506b3903b` 未变。
- **D1–D5 状态**：D1 CLOSED；D2 CLOSED；D3 CLOSED；D4 CLOSED；**D5 CLOSED**。
- **门禁**：PRIVATE-READY = YES；PUBLIC-READY = NO（BLOCKED，B1–B6；B7 已 CLOSED）。
- **HUMAN_UAT_PENDING 4**：Obsidian GUI / 逐图版权 / 15 案例人工评分 / 62 draft 复核；均未执行，未编造 PASS 或分数。
- 详见 `reports/P3.5-REPORT.md` 与 `reports/RELEASE-GATE.md`。


## 9. P3.6 Skill 原生调用验收（2026-11-04 15:56，task-37）

- **HEAD**：`7afe02b`（P3.6 commit：native costume-director skill、10 headless e2e、director materials）。
- **快照一致性**：**363 卡**（内容 166 + 来源 197）；**45 例验收**；**9 例 workflow tests**；18 套 Macbeth LOOKS；HUMAN-SCORE 18 行空表；`SOURCES.csv` 198 行。
- **Skill 安装与发现**：`.dsh/skills/costume-director/SKILL.md`（264 行）；provider `skill`/`skill-filesystem`/`tool-skill` 已挂载。
- **原生调用（独立验证）**：2 次 Vault-cwd `dsh --profile headless --json` 均 exit 0；事件含 `skill(costume-director)` + `tool_result <skill_content>` + bash `scripts/query.py`；答案 ID/SRC 全部解析、0 编造。
- **10 例 E2E**：10/10 通过（skill + 脚本调用、ID/SRC 0 缺失、无错误；T07 同会话、T08 缺口诚实、T09 冲突拒绝、T10 连续性与 prompts；写盘仅 projects/）。
- **KB 安全**：commit 纯新增 69 文件（无既有卡/脚本修改）；`projects/` gitignore；`main` ahead 22（未推送）；既有 license 未改；外部文本注入策略在 SKILL.md（运行时未测）。
- **导演材料**：18/18 审阅完整；评分表 18×7 全 NOT_SCORED（无数字）；OBSIDIAN-UAT 明确 HUMAN_UAT_PENDING/NOT_TESTED。
- **回归**：validate 363/363；build 197/197；acceptance **45/45**；quality_eval **OVERALL PASS（17/17）**；workflow tests **9/9**。
- **兼容性 caveat**：DeepSeek 官方路由曾 402 QUOTA（smoke）；e2e 用 Doubao 临时 overlay（无 profile 改动）；我的原生验证需从 credentials store 注入 key。**不声称 DeepSeek 官方路由已完成 10 例长会话。**
- **门禁**：**PRIVATE-USE VERIFIED = YES；PUBLIC-READY = NO（BLOCKED，B1–B6）**；HUMAN_UAT_PENDING 4 项保持（未执行、未代填分数）。
- 详见 `reports/P3.6-REPORT.md`。


## 10. P4 最终验收（2026-11-04 16:26，task-45）

- **HEAD**：`7f7a21b`（P4 commit：source audit、9 PD books、structure v1.2 + 22 cards、outfit composer、visual index、Macbeth validation）。
- **快照**：**399 卡**（内容 188 + 来源 211）；**45 例验收**；9 workflow tests；9 composer tests；11 Macbeth tests；SOURCES.csv 212 行。
- **独立验收全部 PASS**：许可审计 20 源（PASS 15/WARN 2/RESTRICTED 3，无 verified 误标）；书籍 9/9/31 结论（15 交叉验证，3/3 抽检原文）；结构 v1.2（42 可选字段、22 新卡、旧卡 0 破坏、validate 399/399）；Composer 9/9 + 独立 3 例（0 缺失 ID/0 未解析 SRC/A-B-C 差异/连续性）；视觉 28 CC0/27 关联/0 下载；Macbeth 11/11 + 基线对比提升。
- **全回归**：validate/build/45 acceptance/quality_eval(17/17)/9 workflow/9 composer/11 Macbeth 全 PASS；旧 relevant@5 4.16 持平、0-hit 0；**precision 94.5%→92.9%（−1.6pp，仍 PASS）→ WARN 观察**。
- **发布门禁**：**PRIVATE-READY / PRIVATE-USE = YES（状态不变）**；**PUBLIC-READY = NO（BLOCKED，B1–B6 + P4 L1–L6：DeepFashion2 禁入、FashionStylist 非商业、图片不复制、HF 许可未核实、polyvore 条款不清、open-pose 图片限制）**。
- **HUMAN_UAT_PENDING 4 项**：Obsidian GUI、逐图版权、15 案例人工评分、62 draft 复核 —— 未执行、未代填分数。
- 详见 `reports/P4-REPORT.md`、`P4-COVERAGE.md`、`P4-REGRESSION.md`、`CHANGELOG-P4.md`、`NEXT-PLAN-P4.md`。


## 11. R1.1 最终整合验收（2026-11-05 00:55，task-58）

- **HEAD**：**`567ec8b`**（R1.1 commit）；快照 **400 卡**（内容 189 + 来源 211）；45 acceptance；9 workflow；9 composer；11 Macbeth。
- **独立验收**：安全 10/10 BLOCKED（A05 读取阻断）；跨时代 blocked/declared、Override 记录、A/B/C 单件 gaming、Look Bible tests 6/6；Skill `sync_skill` MATCH + official/overlay 各 3/3（C03/C04 NOT_RUN）；KQ-01/05/06 PASS，KQ-13/H4 BLOCKED；index/STATUS/COVERAGE/QA 400/189/211。
- **回归**：validate 400/400、build 211/211、acceptance 45/45、quality_eval 17/17（relevant@5 4.16、precision 92.9%、0-hit 0）、workflow 9/9、composer 9/9、Macbeth 11/11；新测试 lookbook 6/6、cd 7/7、security 7/7、skill-sync 3/3、human-closeout 3/3；**backup PASS（7/7；修复后真实仓库 1438 文件 backup/verify/restore 全 0）**。
- **R1-F1**：受保护文件 `11-验收/P4-MACBETH/HUMAN-CLOSEOUT.md` hash 稳定、人工签名 PENDING。
- **门禁**：PRIVATE-READY/PRIVATE-USE = YES（附 WARN）；PUBLIC-READY = NO（B1–B6 + L1–L6）；HUMAN_UAT_PENDING 4 项未执行、未代填。
- **重要**：R1.1 修复已提交为 `567ec8b`；工作区仅剩报告类编辑与可再生成 sandbox（未跟踪）。
- 详见 `reports/R1.1-REPORT.md`、`R1.1-DEFECT-CLOSURE.md`、`R1.1-SECURITY.md`、`R1.1-SKILL-INTEGRATION.md`、`R1.1-REGRESSION.md`、`R1.1-DATA-SAFETY.md`。


## 12. P5-A 图谱验收（2026-11-05 01:25，task-63）

- **快照**：最终工作区（P5 关系迁移后；HEAD 仍 `1acb4d3`，迁移 174 项未提交）；400 卡（189 内容 + 211 来源）；validate **PASS 400/400**。
- **After 指标（vs HEAD 1acb4d3 基线）**：内容卡零可见链接 0→0；来源可见引用 2→**143**（100% 机器引用来源）；source_ids 可见 2/299→**193/299（64.5%）**；有 source_ids 无可见来源链接的卡 180→**38（全部 draft）**；typed 无可见 313→**122**；导航可见边 24→**494**（MOC 9 页 + 关系类型页）；语义分量仍 **66（335 主 + 65 source 单点）**。
- **迁移产物**：142 卡 / **201 条 relations**（claim 191、style 8、material 2；全 high+verified）；新增可见 SRC 链接 **191**；卡片 diff **+536/−0**，无 evidence_status/type/source_ids 改动。
- **抽样**：26 条关系回真实卡/源 **26/26 PASS**（结构化字段匹配 + 可见链接 + target 存在）；relation migration tests **8/8 PASS**；迁移备份恢复 0 mismatch（1455 文件）。
- **回归**：validate 400/400、build 211/211、acceptance 45/45、quality_eval 17/17（relevant@5 4.16、precision 0.929、0-hit 0）、composer 9/9、Macbeth 11/11、lookbook 6/6、cd 7/7、security 7/7、skill-sync 3/3、backup 7/7、human 3/3 全 PASS；**workflow 当前树重跑未完成（慢/挂起）→ NOT_RUN（迁移前基线 9/9）**。
- **Agent 关系检索（headless）**：官方/overlay 均 `skill=1` + 工具调用并产生 final，但均无 `turn_end`（官方 final 可核声明与真实数据一致：GAR-0002→SRC-0103、GAR-0084→SRC-0524、LOOK-0003 含 GAR-0002）；**判 PARTIAL/BLOCKED，不写 PASS**。
- **剩余孤岛/原因**：65 个 source 语义单点（28 无关系、27 背景/字典、9 P4 书源仅研究文档、1 书源）；68 个未被内容引用来源（vocabulary 19、museum 12、academic 10、reference 9、other 8、image 5、industry 4、dataset 1）；38 draft 卡未迁移（106 source_ids 不可见）。属**真实独立/待接入**，非链接 bug。
- **门禁**：PRIVATE-READY/PRIVATE-USE = YES（附 WARN：迁移未提交、workflow 未复跑、Agent 检索未完成、GUI NOT_RUN）；PUBLIC-READY = NO（B1–B6 + L1–L6）；**Obsidian GUI UAT = NOT_RUN**（不得声称通过）。
- 详见 `reports/P5-GRAPH-AFTER.md`、`P5-GRAPH-QA.md`、`P5-COVERAGE-GAPS.md`、`P5-HUMAN-UAT.md`。
- **P0 事故记录**：迁移首轮产生 29 张坏 frontmatter（closing fence 缺换行），validate 371/400；未提交，已从备份恢复并重跑，当前 validate 400/400 PASS（详见 P5-RELATION-MIGRATION §0）。


## 13. P5-B 最终验收（2026-11-05 01:38，task-68）

- **快照**：HEAD `afcd9ec`（P5-A commit）+ P5-B 修正（工作区未提交）；**400 卡（189 内容 + 211 来源）**；validate **PASS 400/400**、build_sources PASS。
- **关系抽样准确率**：48 条/7 域（历史地域 8、结构 6、面料 6、鞋履配饰 6、风格 6、完整造型 6、来源 10）→ **48/48 = 100%**（目标 ≥95%）。
- **4 MISLINK**：2 closed（PRD-0007 移除 GAR-0006；PRD-0010 替换 MAT-0011）+ 2 rejected（物性卡 token、codpiece→collar 共现）→ **0 残留正式关系**。
- **8 WEAK**：1 closed（GAR-0033→SRC-0155 移除）、3 降 medium/review、4 候选 review/design、1 example 排除 → **全部处置合理**；3 条 medium 全在 review_queue，formal 198 high/verified。
- **一致性**：YAML relations 200/201 有可见链接（唯一例外 GAR-0045→SRC-0405 medium review）；0 重复 relation、0 双向同类型重复事实、MOC 9 页仅导航（无 frontmatter/relations）。
- **高风险年代/地域**：6 对冲突已移除/替换；6 对 flag review 保留（review_queue，recommend/outfit 不读 key_garments，不进正式推荐主路径）→ WARN 待人工。
- **Agent E2E**：官方 RQ1–3 **3/3 PASS**、overlay RQ1–5 **5/5 PASS**（skill/工具/结果/turn_end.completed/完整输出五项，独立事件解析，IDs 0 missing）。
- **After 指标**：内容零链接 0/189；来源可见（含 MOC）0/211 零链接；source_ids 可见 **191/299（63.9%）**；有 source_ids 无可见来源链接的卡 **40/181（22.1%，全 draft + WEAK-07 连带）**；typed 无可见 **123/480**；语义分量 **66（335+65，不变）**；65 单点分类 34 legit_reference/16 evidence_missing_expression/14 future_topic/1 no_verifiable。
- **回归**：validate 400/400、build 211/211、relation migration 8/8、security 7/7、lookbook 6/6、skill-sync 3/3、backup 7/7、human closeout 3/3、composer 9/9 **PASS**（当前树）；acceptance **45/45 PASS**（lead 报告后复跑）；quality/workflow/Macbeth 未独立复跑（workflow engineer 9/9），不写 PASS。
- **门禁**：PRIVATE-READY/PRIVATE-USE = YES（附 WARN：修正未提交、flag review、GUI NOT_RUN）；PUBLIC-READY = NO（B1–B6 + L1–L6）；**GUI = NOT_RUN/PENDING**。
- 详见 `reports/P5B-GRAPH-QA.md`、`P5B-FINAL.md`。


## 14. P5-C 最终验收（2026-11-05 02:05，task-75）

- **快照**：HEAD `f500289` + P5-C 工作区（未提交）；**458 卡 = 224 内容 + 234 来源**；validate **PASS 458/458**、build **PASS 234/234**；新增 35 内容卡（LOOK 12/STY 5/GAR 4/STR 9/MAT 5）+ 23 来源（SRC-0530..0552）。
- **PASS**：新增卡/来源/ID/许可/HTTP、12 套 Outfit 硬约束 **12/12**、evidence_type（historical 2/sourced 5/creative 5）诚实、Agent E2E 五项（官方 3/3、overlay 3/3）、relation_trace 6/6、relation_consistency 单测 5/5、security/lookbook/skill-sync/backup、acceptance 45/45/composer 9/9/workflow 9/9（engineer P5-C logs）。
- **P1 修复后 PASS**：`relation_consistency.py` **0 errors / 265 relations**（修复前 71）；新关系严格抽样 **62/64 = 96.9%（≥95%）**；来源可见率 **352/460 = 76.5%**（修复前 42.6%）；35 张新卡来源链接 **161/161 可见、0 inline-code**；style_interpretation 已为 v3 design-only/medium/factual=false。
- **覆盖率（同口径）**：garment→outfit 48.9%→**59.8%**、LOOK→narrative 56.5%→**71.4%**；component/material/style 基本持平；relations 201→**265**。
- **WARN/P2**：`tests/test_validate_outfits.py` FAIL（stale 23 vs 35）；isolates.csv 过时（SRC-0013 已引用，有效 65→64）；source-audit 白名单仍 211；9 本书源仍 0 内容引用；quality_eval/Macbeth/human closeout 本轮 **NOT_RUN**（quality 77.2s 无输出后终止 EXIT -15；Macbeth/human 未启动；不写 PASS）。
- **65 单点/38 draft/6 flags**：65 文件仍在但有效 64（SRC-0013 已引用）；38 基线 draft 未变（全库 draft 79）；6 flags 仍 review_queue 未确认。
- **门禁**：PRIVATE-READY/PRIVATE-USE = YES（附 WARN：残余 P2、quality/Macbeth NOT_RUN、未提交）；PUBLIC-READY = NO（B1–B6 + L1–L6）；**GUI NOT_RUN/PENDING**。
- 详见 `reports/P5C-RELATION-COVERAGE.md`、`P5C-FINAL.md`。
