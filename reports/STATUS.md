# 运行状态（STATUS）— Costume Director Knowledge System（P3.3 最终复验后）

- 更新时间：2026-11-04 03:26（Asia/Shanghai）；P3.3 最终复验（task-22）
- 快照：**343 张卡**（内容 158 + 来源 185）；**45 例验收**；git HEAD `171efb6`（工作区 clean）
- 外观：**PASS 24 / WARN 4 / FAIL 0 / HUMAN_UAT_PENDING 4（32 项）**
- **发布门槛：技术/数据/质量门 PASS**；发布仍需完成 HUMAN_UAT_PENDING 4 项
- 报告：[P3-QA.md](P3-QA.md) · [P3-DEFECTS.md](P3-DEFECTS.md) · [P3-COVERAGE.md](P3-COVERAGE.md) · [CHANGELOG-P3.md](CHANGELOG-P3.md) · [NEXT-PLAN.md](NEXT-PLAN.md)

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
