# P5-F 最终收口结论（P5F-FINAL）

- 定稿：2026-11-05 12:02（Asia/Shanghai）；verifier / task-96；快照：**HEAD `4128266`**（P5-E 已提交）+ P5-F 工作区（MOC 导航更新、graph 工具修复、报告）
- 规模：**458 卡 = 224 内容 + 234 来源；334 relations**；validate **458/458**、build **234**、consistency **0 errors / 334**
- 声明：本报告只读；未改卡片/事实；GUI 未执行，不得声称通过。

## 0. 结论摘要（PASS，附 WARN）

| 项 | 结果 |
|---|---|
| 未解析关闭 | **5 typed_unresolved → 0；1 unresolved_wikilink → 0（6/6 CLOSED）**；根因是 EXAMPLE 索引 + inline-code 示例，**不是缺失知识对象**；未新建卡/假关系 |
| 39 候选裁决 | **VERIFIED 18 / REVIEW_REQUIRED 15 / REJECTED 6 / INSUFFICIENT 0**；18 条仅“medium design 建议”，**0 写卡/0 自动提升**；38 draft、6 flags 独立 |
| 健康指标 | validate/consistency PASS；**MOC 224/224 内容 + 234/234 来源（544 链接、0 未解析）**；source_ids 478 对（172/234 被引；370 可见 77.4%）；59 isolates/38 draft/6 flags |
| 适用性覆盖 | present **474/775（61.2%）**；APPLICABLE 380 / REVIEW 94 / INSUFFICIENT 301 / N/A 1017（不以全连通率为目标） |
| 回归 | acceptance 45/45、quality **PASS 4.16/0.92/0**（E3 后）、composer 9/9、workflow 9/9、Macbeth 11/11、relation_trace 6/6、单元 56/56、graph 测试 4/4、validate 458、build 234、consistency 0/334 |
| E2E | official **3/3**、overlay **3/3**，五项全 true |
| GUI | **NOT_RUN / HUMAN_UAT_PENDING**（11 项无截图/签字） |
| 门禁 | PRIVATE-READY/PRIVATE-USE = **YES（附 WARN）**；PUBLIC-READY = **NO（B1–B6 + L1–L6）**；**GUI = NOT_RUN** |

## 1. 未解析关闭（问题 1）

| 项 | 修复前 | 当前 | 根因/证据 |
|---|---:|---:|---|
| typed_unresolved | 5 | **0** | graph `ID_RE`/`by_id` 不认 `GAR-EXAMPLE-001`；5 条 LOOK→example `look_items` 边；修复后 typed_edges **737→742（+5 恢复，不是新关系）** |
| unresolved_wikilink | 1 | **0（{}）** | `00-系统/关系类型.md` 的 inline-code 示例 `[[target]]` 被旧解析器当链接；修复为扫描前剥离 fenced/inline code |

- 独立复核：`scripts/graph_analyze.py`（当前修复版）→ **typed_unresolved 0 / unresolved {} / typed_edges 742 / components 60 / singletons 59 / source_ids 478**。
- 未新建卡片或关系；内容卡 0 改动（`git status` 无 01–09 内容修改）；EXAMPLE 卡仍 `review_status=draft`/`evidence_status=example`，恢复索引≠提升证据。
- 残余边界：graph 工具 `typed_edges` 不含卡片 `relations`（334 需另计）；不要相加。

## 2. 39 候选裁决（问题 2）

| 裁决 | 数量 | 含义/动作 |
|---|---:|---|
| **VERIFIED** | **18** | 主体/目标 verified、共享真实材料 token、target 为材料实体（非 MAT-0012/0013 物性、非 pattern）、无自指；**仅建议**以 medium/interpretive/factual=false/design_only=true 入库；**本轮未写卡/未升级** |
| REVIEW_REQUIRED | 15 | 6 条 target 为 trim/金属纤维（MAT-0003/0004），9 条 subject 为 style/PRD；保留 review，人工确认语义，不得 high |
| REJECTED | 6 | 5 条自指（MAT-0003/0004/0008/0009/0010→自身）+ 1 条 subject 为 material_property（MAT-0013）；do_not_propose |
| INSUFFICIENT | 0 | — |

- 独立核对：18 VERIFIED 全部 target 为 material 实体、非自指、relation=uses_material、proposed medium；6 REJECTED 原因全部成立；**git 内容卡 0 修改**。
- **无自动提升**：38 基线 draft、6 key_garments flags、163 needs_human、37 reject 均独立；18 条 VERIFIED 只是建议（正式入库需另任务 + 备份/回归）。
- 残留：source-audit 白名单仍 211（`source_audit_ok=false` 不代表来源不存在）；SRC-0530..0552 未入 audit。

## 3. 健康指标（问题 3）

- **基础**：458 卡/234 来源；validate 458/458；build 234；consistency 0/334。
- **MOC（已更新）**：9 页均无 frontmatter（navigation-only）；**544 链接、0 未解析**；**内容 224/224、来源 234/234 全覆盖**（lead 补齐 35 内容 + 23 来源）；此前 P2-1 缺口已关闭。
- **source_ids**：478 对、0 缺失；被引 172/234；可见 370/478（77.4%）；可见来源 172/172；零可见 SRC 卡 39（38 draft + GAR-0045）。
- **重复/同义词**：0 重复 ID；**3 对重复来源 URL**（SRC-0036↔0175、SRC-0163↔0022、SRC-0115↔0157）仍待合并/canonical（P2）；6 组别名冲突（腰带/着物/tunic/长袍/gigot/seam allowance）；2 组跨类型同名（gloves/leather，非重复卡）。
- **type/category**：3 张 MAT 前缀卡 type=pattern（MAT-0005/6/7，P3，不建议改 ID）；92/234 来源缺 category 字段（用 source_kind，P3）。
- **wikilink/backlinks**：真实 unresolved 0；可见对 1663，互链 682、非对称 981（内容→来源 370、来源→内容 186、来源→来源 16、内容→内容 1071）——非对称是引用模型，不追求全互链。
- **专业 vs 导航**：语义卡 458 vs 导航 26 + 研究 5；MOC 仅导航；11 个导航文档零链接（根 README/AGENTS/Outfit模型/数据字典扩展/4 模板/来源规范）P3。
- **适用性覆盖（E1/E3 后）**：present **474/775（61.2%）**；component 16/92（17.4%）、material 53/92（57.6%）、silhouette 74/92（80.4%）、style 3/92（3.3%）、accessory 31/56（55.4%）、outfit 55/92（59.8%）、narrative 25/35（71.4%）、claim 217/224（96.9%）；part→material 10/35（28.6%）。
- **遗留**：59 isolates（+3 uncited 未分类=62 uncited）、38 基线 draft（全库 79）、6 flags 未确认；4 本背景书未接卡；page UNCONFIRMED。

## 4. GUI / UAT（问题 4）

- **NOT_RUN / HUMAN_UAT_PENDING**：`P5F-OBSIDIAN-UAT.md` 11 项（Vault 入口、MOC 9 页、Properties、Backlinks、Local Graph、关系/证据诚实、孤立节点、搜索、坏链、性能、截图/签核）**全部 NOT_RUN**；无截图、无签字。
- MOC 已补齐 224/234，UAT 第 2 项**预期改为 PASS**（仍需人工执行确认）；其余项需在 Obsidian 内逐项执行。
- **在 11/11 PASS + 两人签字前不得声称 GUI 通过**；PUBLIC 门禁 B1 保持 NOT_EXECUTED。

## 5. 回归（问题 5）

| 套件 | 结果 | 证据 |
|---|---|---|
| validate 458 / build 234 | **PASS** | 本轮独立 |
| consistency | **0 errors / 334** | 本轮独立 |
| graph | **typed 0 / unresolved 0 / typed_edges 742** | 本轮独立（修复版） |
| graph tests | **4/4 PASS** | `11-验收/P5F/test-graph-analyze.log` |
| acceptance | **45/45 PASS** | P5-E 全量 log（P5-F 未改内容/脚本逻辑） |
| quality_eval | **PASS 4.16 / 0.92 / 0**（E3 后重跑；`/tmp/p5e_quality.log`；P5-F 仅改 graph 工具） | lead 提供 + 本轮日志复核 |
| composer | **9/9 PASS** | P5-E log |
| workflow | **9/9 PASS** | P5-E log |
| Macbeth | **11/11 PASS** | P5-E log |
| relation_trace | **6/6 PASS** | P5-E 单元批 |
| security/lookbook/skill-sync/backup/human | **56/56 unit PASS** | P5-E 单元批 |
| E2E official / overlay | **3/3 / 3/3**，五项全 true | `11-验收/P5F/e2e/validation-summary.json` |
| GUI | **NOT_RUN** | P5F-OBSIDIAN-UAT |

- 说明：P5-F 只改 graph 工具/测试与 MOC 导航、报告，不改卡片/关系/证据；P5-E 全量回归矩阵仍适用；graph/validate/consistency/E2E/quality 有当前证据。

## 6. 维护规则（问题 6）

- 8 步：**发现→许可→事实提取→去重→关系校验→人工审核→自动测试→入库**；每步退出条件与命令见 `P5F-MAINTENANCE.md`。
- 单一系统：Obsidian vault + 仓库内脚本/测试/验收报告；**不新建第二套系统**；**不以卡数为目标**；review 队列可长期存在。
- 批次后必做：MOC 同步（本次已补齐）、validate/build/consistency、备份/回滚、报告/STATUS 一致；medium/review 不自动升 high/verified。
- 已知维护项：3 对重复来源 URL（P2）、别名消歧、质量/回归留档、GUI 人工验收。

## 7. 剩余风险与门禁（问题 7）

| 风险 | 级别/状态 |
|---|---|
| 3 对重复来源 URL 未合并 | **P2/WARN**（SRC-0036↔0175、SRC-0163↔0022、SRC-0115↔0157） |
| 18 条 VERIFIED 仍为“建议”、source-audit 白名单 211 | **P2/WARN**；正式入库需另任务 + audit 刷新 |
| 3 张 MAT 前缀 pattern 卡、92 来源缺 category、6 别名冲突、11 导航零链接 | P3/信息 |
| 59 isolates / 62 uncited / 38 draft / 6 flags / 4 背景书 | 遗留，需人工/后续 |
| quality_eval | 当前 PASS（4.16/0.92/0）；P5-E 曾 NOT_RUN，现已有当前证据 |
| GUI/H1 | **NOT_RUN/PENDING**（无截图/签字） |
| P5-F 工作区未提交 | WARN（MOC + graph + 报告未 commit） |

- **PRIVATE-READY / PRIVATE-USE = YES（附 WARN：重复 URL、18 VERIFIED 未入库、59 isolates/38 draft/6 flags、P5-F 未提交、GUI NOT_RUN）**
- **PUBLIC-READY = NO（BLOCKED）**：B1 GUI NOT_EXECUTED、B2 逐图版权 NOT_RUN、B3 15 案例 NOT_SCORED、B4 62 draft、B5、B6；L1–L6 保持
- **GUI/UAT = NOT_RUN/PENDING**

## 8. 建议

1. 合并 3 对重复来源 URL（canonical/alias），不重复计数。
2. 对 18 条 VERIFIED 单独立项入库（备份 + 写卡 + 可见链接 + validate/consistency + 回归）；先刷新 source-audit（含 SRC-0530..0552）。
3. 按 `P5F-OBSIDIAN-UAT.md` 执行 11 项 GUI 验收并两人签字；MOC 第 2 项预期 PASS。
4. 提交 P5-F（MOC + graph 工具/测试 + 报告）。
5. 保留 38 draft/6 flags/59 isolates 的人工队列；不自动提升。
