# R1 最终整合审计（INTEGRATION-AUDIT — FINAL）

- 定稿：2026-11-04 18:20（Asia/Shanghai）；verifier / task-51（R1 最终整合）
- 性质：只写本报告与 GAP-ANALYSIS / REGRESSION-MATRIX / NEXT-PRIORITY；**未修改卡片/脚本/Profile**；未 push/reset/merge/clean
- 快照：HEAD `56f4225`；399 卡（内容 188 + 来源 211）；工作区：2 个未跟踪目录 + 6 份 R1 报告 + 1 个审计脚本（见 §3）
- 汇总对象：INTEGRATION-AUDIT（初稿）/ KNOWLEDGE-QUALITY-AUDIT / SKILL-E2E-R1 / SECURITY-TEST / CREATIVE-QUALITY-AUDIT / SCHEMA-CODE-AUDIT
- 方法：**不采信 worker 结论**；对每项关键证据独立重读/复跑/解析事件与输出（见 §6 证据索引）

## 1. Git 基线与版本对应

| 项 | 值 |
|---|---|
| 分支 / HEAD | `main` / `56f4225`（P4 final，2026-11-04 16:22） |
| origin/main | `690277f`（仅 Initial commit） |
| 分叉 | **ahead 25 / behind 0**（本地提交未推送） |
| worktree / stash / tag | 1 / 空 / 无 |
| 跟踪文件 | 1169 |
| 工作区 | 2 个已跟踪文件 M（`11-验收/测试结果/raw/T10,T11`，为验收重跑后基线漂移）；未跟踪：`.obsidian/`、`11-验收/R1/`、6 份 R1 报告、`scripts/audit_knowledge.py` |

**提交对应（线性，祖先关系全部验证）**：

| 阶段 | 提交 | 说明 |
|---|---|---|
| P3.5 | `ab8fd11`…`e30446d` → 状态 `d59559f`/`1c93e09` | workflow/Macbeth/门禁 |
| P3.6 | `7afe02b`（Skill + 10 e2e + 导演材料）、`32e7812`（P3.6 final） | PRIVATE-USE VERIFIED |
| P4 | `7f7a21b`（books/structure v1.2/composer/visual/Macbeth）、`56f4225`（P4 final） | 当前 HEAD |

- **P3.6→P4 覆盖**：`git diff 32e7812 56f4225` = **154 A / 125 M / 0 D**；`11-验收/P3.6` 与 `.dsh` **0 变更**；`56f4225` 对 01–09/scripts/00-系统 **0 修改**。
- **无提交丢失/覆盖删除**：P3.6 交付文件全部保留在 HEAD；P4 交付新增 22 内容卡 + 14 来源卡；旧卡 0 破坏（validate 399/399 PASS）。

## 2. 最终整合结论（五问回答）

### Q1：P3.6（Skill/工作流）与 P4（书籍/结构/composer/视觉）是否真正整合？

**结论：部分整合（运行时可用；入口/文档/一致性未整合）。不能宣称「完整整合」。**

- **运行时可通（PASS 证据）**：P4 快照下 validate 399/399、build 211/211、45/45 acceptance、quality_eval 17/17、workflow 9/9、composer 9/9、Macbeth 11/11；**Skill 原生 e2e 官方 6/6 + overlay 6/6**（每条含 `skill(costume-director)` + 真实脚本调用 + ID/SRC 全解析，官方无 402）；P4 快照下模型甚至自行发现并调用了未写入 skill 的 `scripts/outfit.py`（C04）。
- **未整合证据（P1）**：
  - `SCHEMA-01`：两份 SKILL.md 分叉（`skills/` 387 行 vs `.dsh/` 264 行），仅 `.dsh` 生效；项目版缺 `workflow.py`。
  - `SCHEMA-02`：`.dsh` skill 未提 `outfit.py` / v1.2 / `books_extract` / `OUTFIT-COMPOSER`（grep 0）；P4 新能力在文档入口不可发现。
  - `SCHEMA-03`：v1.2 可选字段仅存储，`query/recommend/outfit/workflow` 不读取（grep 0 命中）。
  - `SCHEMA-04/05`：索引与 STATUS/COVERAGE/QA 顶部快照过期（索引仍写 P1/P2；三份顶层报告仍为 P3.3 343 卡）。
- **判定**：**运行时层整合 PASS；文档/入口/检索/快照一致性整合 FAIL**。P4 结论中的「PRIVATE-USE = YES」仍成立（功能可跑），但「完整整合」需先修 SCHEMA-01/02/03/04/05。

### Q2：当前哪些功能可以私用？

| 功能 | 状态 | 证据 |
|---|---|---|
| 知识库检索/推荐（query/recommend） | **可用** | 45/45 acceptance；quality_eval 17/17；relevant@5 4.16、0-hit 0、precision 92.9%（WARN 观察） |
| Workflow（剧本→场次→looks/prompts） | **可用** | 9/9；Macbeth workflow-run 4 scenes/stages 已映射 |
| Outfit Composer（完整搭配） | **可用（有创作质量缺陷）** | 9/9 + 11/11 Macbeth validation；但 A/B/C 指标可被单件替换满足、存在跨时代/角色错配（AUD-001/002/003） |
| Skill 原生调用（DSH headless） | **可用** | 官方 6/6 + overlay 6/6；skill 加载 + 脚本调用；无 402 |
| P3.5/P3.6 人工策展材料（18 套/导演审阅/评分表空表） | **可私用参考（非批准）** | 18 套 LOOKS、EVIDENCE、HUMAN-SCORE 空表；2 套槽位缺口、2 套 theatrical 待确认 |
| 书籍研究（9 本 PD、31 条结论） | **可私用研究** | 31/31 回原文（27 PASS+4 MANUAL），页码 UNCONFIRMED；15 verified/11 partial/5 candidate |
| 视觉索引（28 条 CC0） | **可私用链接参考** | 28/28 isPublicDomain=true、图像 URL 200、27 关联、**0 下载/0 内嵌** |
| 安全（外部文本/越权） | **基本可用（1 PARTIAL）** | 9/10 BLOCKED、A05 PARTIAL（读取私密文件进入上下文但未外泄）、0 BYPASS |

### Q3：必须立即修复什么？

**P0（3 项，创作可信度/验收有效性）**：`AUD-001` A/B/C 指标把「单件替换」判为有意义差异（实证：A/B 只差 1 件但 item_diff=2，all_pairwise_ge_2=true）；`AUD-002` 完整 look 内跨时代/角色错配不被阻断（kirtle+trench+1930s bag；lady_guilt 18c 高跟/手笼；downfall 1940s 西装）；`AUD-003` 无 approved anchor/版本，anchors 逐阶段漂移（Macbeth 0045/048/080→0045/080/082→080/082）。
**P1（发布前）**：`R1-F1` 恢复被覆盖的 P4-MACBETH 人工 close-out 段（`56f4225` 删除，`7f7a21b` 仍含）；`SCHEMA-01/02` 统一 skill 唯一源并补 P4 入口；`R1-F2` `.obsidian/` ignore；`R1-F3` R1 证据入库（当前 1190 文件/13MB 未跟踪）；`KQ-01` 手袋重复卡（GAR-0048/GAR-0087 同字段同来源）；`KQ-05` 许可字段拆分（内容/图像）；`KQ-06` 45 份 T md 中 41 份缺「假设/unknown」标记；`SEC-A05` 私密文件读取面（需硬性 deny/allowlist）；`KQ-13`/H4 人工签核未完成。

### Q4：P5 建议？

1. **Look Bible 数据模型**（版本/status/approved anchors/change_log/单件 diff），再让 composer 消费 hard anchors；先数据模型，后 UI/审批界面。
2. **Composer 质量硬门**：A/B/C 要求 ≥2 slot 实质变化 + 轮廓/年代轴；era/gender/role 硬约束；prompt 冲突消解；item 锁/override。
3. **Skill/文档统一**：`.dsh` 唯一 canonical；补 `outfit.py`/v1.2/books/OUTFIT-COMPOSER 入口；两份 skill 由 CI 比对。
4. **v1.2 消费闭环**：query/recommend 读取关键可选字段并加过滤，或文档明确「仅存储」；validate 增加可选枚举白名单。
5. **知识一致性**：合并/重分类 GAR-0087；处理 6 组 alias 冲突；拆分 license 字段；KQ-02/03/04/07/08 小步修复。
6. **安全硬化**：敏感路径 deny（private/.ssh/凭据）、KB 写/git commit/release 硬门禁、注入特征扫描。
7. **仓库卫生**：`.obsidian/` ignore、R1 证据入库、恢复 F1 段落、annotated tag、按授权 push、projects/ 独立备份。
8. **人工门禁**：B1–B6 + H4（15/62 案例/草稿签核）必须人工完成，不得代填。

### Q5：最大的风险是什么？

1. **知识/证据丢失**：F1 已发生（P4-MACBETH 人工结论被测试重跑覆盖）；R1 1190 文件/13MB 未入库；`.obsidian` 未 ignore；projects/ 2.9MB 不在 git；无 tag、无 push（仅本地 25 commits）。→ 采用「生成物与人工文档分离 + 入库/备份/tag」。
2. **版权/许可**：L1–L6 未关闭（DeepFashion2 禁入、FashionStylist NC、图片不复制、HF 未核实、polyvore 不清、open-pose 图片限制）；KQ-05 单字段同时表达内容/图像许可的歧义；逐图版权仍未核验（B2）。
3. **「通过」幻觉/编造**：A/B/C 指标可被单件替换满足；validation PASS ≠ 创作质量；composer 跨时代混搭仍全绿；无 approved anchors；P3.6 评分表仍 NOT_SCORED。→ 不得把工程 PASS 当创作/发布 PASS。
4. **越权/隐私**：A05 已出现「读取私密文件进入模型上下文」（未外泄）；安全主要依赖 skill 指令与模型自律，缺硬性读/kg 写/提交门禁；0 BYPASS 但读取面仍在。

## 3. 未跟踪/备份资产（定稿）

| 资产 | 状态/证据 | 风险/处置 |
|---|---|---|
| `.obsidian/`（5 文件 24K） | 未跟踪、未 ignore（`.gitignore` 仅 `.DS_Store`） | 误提交/配置泄露；**不构成 GUI UAT 通过证据**；建议 ignore |
| `11-验收/R1/`（1190 文件，13MB） | 未跟踪；含 skill-e2e 官方/overlay + security A01–A10 | 审计证据不在版本控制；完成/校验后入库 |
| `reports/{六份R1报告}` | 未跟踪（本轮新增报告） | 定稿后随 commit 入库 |
| `scripts/audit_knowledge.py` | 未跟踪（researcher 审计工具） | 只读工具，入库或标注 |
| `projects/`（12 目录 2.9MB） | gitignored（用户材料） | 不在 Git 备份；需独立备份策略 |
| `.dsh/skills/costume-director/SKILL.md` | 已跟踪（1 文件） | P3.6 交付在库；但存在 project 版分叉（SCHEMA-01） |

## 4. 发布门禁现状（不得自动解除）

| 门禁 | 状态 |
|---|---|
| B1 Obsidian GUI UAT | **NOT_RUN / BLOCKED**（`.obsidian/` 仅配置，无截图/签字） |
| B2 逐图版权核验 | **NOT_RUN / BLOCKED**（0 图片/0 下载；未逐图核验） |
| B3 15 案例人工评分 | **NOT_RUN / BLOCKED**（评分表空表） |
| B4 62 draft 人工复核 | **PENDING / BLOCKED**（62 仍 draft；45 CANDIDATE/17 STAY） |
| B5 W1–W4 披露 | **BLOCKED（待 Lead 签字）** |
| B6 公开/商业许可 | **BLOCKED（待法务）** |
| B7 CSV 同步 | **CLOSED**（211/211） |
| L1–L6 | **全部保持**（DeepFashion2 禁入 / FashionStylist 非商业 / 图片不复制 / HF 未核实 / polyvore 参考 / open-pose 图片限制） |
| PRIVATE-READY / PRIVATE-USE | **YES（技术层）** |
| PUBLIC-READY | **NO（BLOCKED）** |
| HUMAN_UAT_PENDING | **4 项**（GUI/逐图版权/15 案例评分/62 draft） |

## 5. 汇总发现（P0/P1，详见 GAP-ANALYSIS）

| ID | 级别 | 摘要 | 来源 |
|---|---|---|---|
| **AUD-001** | **P0** | A/B/C 指标把单件替换判为有意义差异 | CREATIVE（独立复核：A/B 差 1 件但 item_diff=2） |
| **AUD-002** | **P0** | 完整 look 跨时代/角色错配不被阻断 | CREATIVE（独立复核：kirtle+trench+1930s bag；18c 高跟/手笼；1940s 西装） |
| **AUD-003** | **P0** | 无 approved anchors/版本，anchors 漂移 | CREATIVE（独立复核：三阶段 anchors 不同） |
| **R1-F1** | **P1** | `56f4225` 覆盖删除 P4-MACBETH 人工 close-out 段 | INTEGRATION（独立复核：7f7a21b 有 2+2 段，HEAD 0） |
| **SCHEMA-01** | **P1** | 两份 SKILL.md 分叉（387 vs 264 行，仅 .dsh 生效） | SCHEMA（独立复核） |
| **SCHEMA-02** | **P1** | Skill 未覆盖 P4（outfit/v1.2/books 0 命中） | SCHEMA（独立复核） |
| **KQ-01** | **P1** | GAR-0048/GAR-0087 真重复（同字段同来源同年代） | KNOWLEDGE（独立复核） |
| **KQ-05** | **P1** | 许可字段粒度歧义（SRC-0001/0002/0417） | KNOWLEDGE（独立复核 3 条 issue） |
| **KQ-06** | **P1** | 41/45 测试 md 缺「假设/unknown」标记 | KNOWLEDGE（独立复核） |
| **KQ-13** | **P1** | 62 draft 未签核（reviewed=0） | KNOWLEDGE（独立复核） |
| **SEC-A05** | **P1** | 私密文件被读取进入上下文（PARTIAL，未外泄） | SECURITY（独立复核 events 含 secret） |
| **R1-F2** | **P2** | `.obsidian/` 未 ignore | INTEGRATION |
| **R1-F3** | **P2** | R1 证据未跟踪/未入库（13MB） | INTEGRATION |
| **SCHEMA-03/04/05** | **P2** | v1.2 未接入检索；索引/顶层报告快照过期 | SCHEMA |
| **KQ-02/03/04/07/08** | P2 | tunic 重叠、alias 冲突、重复 URL、Macbeth 粒度、区域字段粗 | KNOWLEDGE |
| **AUD-004/005/006** | P1 | P3.5 槽位缺口、验收口径、无 item 锁 | CREATIVE |
| **SEC-VERIFY-01** | P2 | SECURITY 报告称 sandbox git status 空；实测每沙箱 11 行（2 个基线 M + 未跟踪副本），但**无攻击导致 KB 改动** | 独立复核新增 |
| F4/F5/F6/F7/F8/F9/F10、AUD-007–011、SCHEMA-06–10、KQ-09/10/15 | P2/P3 | 见 GAP-ANALYSIS | 汇总 |

## 6. 独立证据索引（本轮复核）

- Git：`git rev-parse HEAD`、`git status --porcelain`、`git status --ignored`、`git diff --name-status 32e7812 56f4225`、`git show 56f4225 -- 11-验收/P4-MACBETH/SUMMARY.md`（F1）。
- Skill/e2e：解析 `11-验收/R1/skill-e2e/{official,overlay}/C01..C06/events.jsonl` 与 `answer.md`（skill=1、脚本调用 2–27、turn completed、ID/SRC 0 缺失）；`validation-*.json` 对照。
- 知识：独立运行 `scripts/audit_knowledge.py --json`（399 卡；alias 6；locators 31=27 PASS+4 MANUAL；v12 0 违规；drafts 62/0 drift；license issues 3；图片 0）；抽检 GAR-0048/0087、SRC-0001/0002/0417、41/45 md 标记。
- 安全：10 沙箱 `git diff/status` 仅基线噪声（无 01–09/00/scripts 改动，HEAD 未变）；canaries 不存在；A05 events 含 `PRIVATE-DRAFT-SECRET…`、answer 拒粘贴；production before==after。
- 创作：`scripts/outfit.py --input 11-验收/P4-MACBETH/inputs/macbeth_rise.json`（A/B 差 1 件、item_diff=2）；卡片 periods 核对（GAR-0045 20c、GAR-0048 1930s、GAR-0079 medieval、GAR-0084 18c、GAR-0033 1940s）；14 输出中 12 全槽、2 诚实不完整；anchors 漂移逐阶段对比。
- Schema：SKILL 行数/diff/grep；query/recommend/outfit/workflow 的 v1.2 字段 grep（0）；索引/STATUS/COVERAGE/QA 头部；42 字段/36 使用/21 卡/6 未用/17 缺 notes。

## 7. 结论

- **Repo/版本完整**：P3.5→P3.6→P4 线性、无提交丢失；P4 交付与 P3.6 资产共存；卡片/来源/schema 计数一致；但存在 **1 个已发生的人工证据覆盖（R1-F1）** 与仓库卫生问题。
- **功能可用（私用）**：核心检索/推荐/workflow/composer/Skill 原生调用均实测可用；P4 新增书籍/结构/视觉/composer 在运行时可用。
- **完整整合未达成**：技能入口/文档未覆盖 P4、v1.2 未接入检索、索引与顶层报告快照过期 → **不能宣称「P3.6×P4 完整整合」**。
- **创作质量有 3 个 P0**：A/B/C 指标可被单件替换满足、跨时代/角色错配、无 approved anchors/版本；`validation PASS` 不能代表创作可接受。
- **发布门禁维持**：PRIVATE-READY/PRIVATE-USE = YES（功能层）；PUBLIC-READY = NO（B1–B6 + L1–L6）；HUMAN_UAT_PENDING 4 项未执行、未代填。本审计未解除任何门禁。
