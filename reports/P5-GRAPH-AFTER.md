# P5-A 图谱 After 指标（P5-GRAPH-AFTER）

- 生成：2026-11-05 01:24（Asia/Shanghai）；verifier / task-63（P5-A 第七阶段验收）
- **基线**：HEAD `1acb4d3` 快照（`P5-GRAPH-DIAGNOSIS`，416 节点：content 189 / source 211 / nav 14 / research 2）
- **After**：当前最终树（P5 关系迁移后；400 卡不变，导航新增 MOC 9 页 + 关系类型 1 页；`validate PASS 400/400`）
- 工具：`scripts/graph_analyze.py --root <final> --csv /tmp/p5_after.csv --json /tmp/p5_after.json`（live 树，只读）
- 注：当前 After 树为**未提交工作区**（迁移 174 项改动；HEAD 仍 `1acb4d3`）；提交前数字以本报告为准。

## 1. Before / After 总表

| 指标 | Before（HEAD 1acb4d3） | **After（迁移后）** | 变化 |
|---|---|---|---|
| 扫描节点 | 416（nav 14 / research 2） | **426（nav 24 / research 2）** | +10 导航（MOC 9 + 关系类型 1） |
| Wikilink 出现次数 | 1271 | **1944** | +673 |
| 去重可见边 | 1114（语义 1090 + 导航 24） | **1775（语义 1281 + 导航 494）** | +661（语义 +191、导航 +470） |
| 内容卡零可见链接 | 0/189 | **0/189** | 0（仍全部连通） |
| 来源卡零可见链接 | 58/211 | **0/211** | **−58（全部来源至少被 MOC 可见链到）** |
| source_ids 机器对 | 299 | **299** | 0（未改事实字段） |
| source_ids 有可见链接 | 2/299（0.7%） | **193/299（64.5%）** | **+191** |
| 有 source_ids 但无可见来源链接的卡 | 180/181（99.4%） | **38/181（21.0%）** | **−142（剩余 38 张均为 draft：look 22 / scene 15 / style 1）** |
| 被机器引用来源 | 143 | **143** | 0 |
| 其中同时可见 | 2 | **143（100%）** | **+141** |
| typed 边 | 485 | **485** | 0（schema 未变） |
| typed 边无可见链接 | 313（64.5%） | **122（25.2%）** | **−191** |
| 其中 source_ids 无可见 | 297 | **106** | −191 |
| 其中 key_garments 无可见 | 16 | 16 | 0 |
| 语义分量数 | 66 | **66** | 0 |
| 最大分量 | 335（189 content + 146 source） | **335（189 content + 146 source）** | 0 |
| 单点分量 | 65（全部 source） | **65（全部 source）** | 0 |
| 导航文档零可见链接 | 9/14 | **9/24** | 新增 MOC 均有链接 |

**新增来源/专业关系计数（迁移产物）**：
- 新增 frontmatter `relations`：**201 条**，覆盖 **142 张内容卡**（claim_supported_by 191、in_style 8、uses_material 2；**全部 confidence=high、evidence=verified**）。
- 新增可追溯来源可见链接：**191 条 content→source**（加上原有 2 条 = 193 对）；引用来源可见覆盖率 2/143 → **143/143 (100%)**。
- 新增导航：`00-系统/MOC/` 9 页（README + 8 分类：服装单品 88、结构细节 26、材质纹样 14、鞋履配饰 32、时代地域 11、风格体系 11、造型组合 23+16、来源证据 211）+ `00-系统/关系类型.md`。
- 新增来源/专业关系：迁移工具记录 pilot 30 卡/34 关系/34 链接；full 最后一批 changed 113/relations 168/links 157；实际当前树合并 142 卡/201 关系（多轮 apply 覆盖）。

## 2. After 的关键解释

### 2.1 已修复（相对诊断）

1. **citation 可见性**：`source_ids`（YAML）—正文可见 SRC 链接的缺口从 297/299（99.3%）降到 **106/299（35.5%）**；来源被可见引用从 2 → 143（100% 的机器引用来源现在都有正文链接）。
2. **内容卡专业关系**：142/189（75.1%）内容卡新增结构化 `relations`，高置信/已验证；单卡级可审计（target/type/direction/evidence/confidence/rule）。
3. **导航入口**：MOC 覆盖全部 8 类内容与全部 211 来源；从「索引只链 7 条」变为 9 页导航（来源证据页 218 链接、服装单品页 95 链接）。
4. **未破坏事实**：卡片 diff **+536 / −0**（142 文件，无删除）；`type/id/evidence_status/review_status/license_status` 无改动；`source_ids` 未被改。

### 2.2 未变/仍散落（外围节点真实原因）

- **语义分量不变：66 = 335 主分量 + 65 单点来源**。迁移把来源可见链接补进内容卡（内容→来源），但 65 个「卡片级无关系」的来源仍未进入 content+source 语义图——**MOC 属于导航层，不计入语义分量**；这不是迁移失败，而是「这些来源本身没有被任何内容卡 source_ids 引用」：
  - 28 `isolated_source`（无关系、source 卡也无出链）
  - 27 `background_or_dictionary_uncited`（vocabulary/academic reference 背景源，未被引用）
  - 9 `navigation_only`（P4 书源 SRC-0061..0069，仅研究文档可见）
  - 1 `book_source_no_card_integration`
- **未引用来源 68 个**（211−143）：vocabulary 19、museum_collection 12、academic_reference 10、reference_work 9、other 8、image_repository 5、industry_framework 4、dataset 1（含 9 本 P4 书源）。
- **38 张 draft 卡**仍有 source_ids 无可见 SRC 链接（look 22 / scene 15 / style 1）——迁移策略未对 draft 卡片写入关系/来源链接，保留给审阅/后续批次；对应 **106 条 source_ids 不可见**。
- **top isolates（After）全部是 10 个未链接导航文档**（模板/README/AGENTS/来源规范/验证记录/书籍研究 README），无来源/内容卡零总度（因为 MOC 给全部来源至少一条导航入链；语义上仍 65 个 source 单点）。

## 3. 结论：外围散落的真实原因（修复 vs 合理独立）

| 类别 | 状态 | 依据 |
|---|---|---|
| 内容卡「零链接」 | **不存在**（Before/After 均 0） | 189/189 内容卡有可见边，188/189 双向 |
| 来源「图谱不可见」 | **已修复（主体）** | 来源可见引用 2→143；source_ids 可见覆盖率 0.7%→64.5% |
| 来源「卡片级孤立」 | **部分真实独立 + 部分待接入** | 28 isolated + 27 background 属真实未引用的参考源；9 书源仅研究文档可见；需内容接入，不是硬连 |
| 导航可达性 | **已修复** | MOC 9 页覆盖 8 类 + 211 来源；nav 可见边 24→494 |
| 语义分量 | **保持不变（合理）** | 65 单点来源没有内容卡关系；不应通过 MOC 强行计入语义分量 |
| draft 卡 | **未迁移（显式保留）** | 38 draft 卡 source_ids 不可见；应人工复核后再决定 |

**总体**：P5-A 修复了「机器引用不可见 / 导航缺失」这两类真实问题（内容卡专业关系覆盖 +143，来源可见引用 +141，导航 +470 边）；**65 个来源单点是「未被内容引用的参考/背景/书源」，属于合理独立或待接入，而不是链接 bug**；语义分量不因 MOC 变化是正确设计（导航 ≠ 语义）。

## 3.1 Agent 关系检索结果（headless，详见 P5-GRAPH-QA §5）

- 官方/overlay 均 `skill=1` 且执行工具/产生 final；但均**无 turn_end** → 判 **PARTIAL/BLOCKED，不写 PASS**；官方 final 中可核声明（GAR-0002→SRC-0103、GAR-0084→SRC-0524、LOOK-0003 含 GAR-0002）与真实数据一致。
- 结论：静态关系/图谱可核；**Agent 端到端关系检索可靠性本轮未被证明**，需稳定网络重跑。

## 3.2 迁移 P0 事故（已修复，记录备查）

- 首轮全量写入产生 29 张卡片 closing YAML fence 缺换行 → `validate` 371/400；**未提交**，从 `/tmp/p5-backup` 恢复后重跑；当前 **validate 400/400 PASS**、`build_sources` PASS、source_ids 0 差异（`reports/P5-RELATION-MIGRATION.md` §0）。迁移写入流程必须保留 fence/validate 校验。

## 4. 局限

- After 树尚未提交（工作区 174 项改动；HEAD 仍 `1acb4d3`）；提交后需用同一命令复跑确认数字。
- MOC 链接计入导航边（494），不计入 content+source 语义分量；若未来要把 MOC 也计入语义，应另立指标，不能与语义分量混用。
- 迁移报告 `reports/P5-RELATION-MIGRATION.md` 已生成（含 P0 事故说明）；本报告数字来自最终树 + 迁移 artifacts。
- 38 draft 卡未迁移是策略性保留（未见其关系写入），需在 P5 后续批次按审核队列处理。
