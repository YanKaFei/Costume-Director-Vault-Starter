# P5-F 长期维护规则（P5F-MAINTENANCE）

- 生成：2026-11-05 11:58（Asia/Shanghai）；verifier / task-95；只读报告，未改卡片/脚本
- 原则：**单一 vault（Obsidian + 仓库内脚本/测试/验收报告）**；不新建第二套知识系统、不引入独立数据库/外部 wiki；**不以卡片数量为目标**；先证据、后关系、再展示。
- 当前基线（维护起点）：458 卡/234 来源/334 relations；validate 458 PASS；consistency 0；MOC 覆盖 189/224 内容、211/234 来源（待补）；59 isolates；38 基线 draft；6 flags；quality_eval 当前 NOT_RUN；GUI NOT_RUN。

## 0. 维护流水线（8 步，每批小步执行）

```
发现(discover) → 许可(license) → 事实提取(extract) → 去重(dedupe)
→ 关系校验(relation validation) → 人工审核(human review)
→ 自动测试(tests) → 入库(ingest/commit)
```

**每步有退出条件；任一步不满足不得进入下一步。**

### 1. discover（发现）
- 输入渠道：既有来源卡（`04-来源/`）、`reports/SOURCES.csv`、P4 审计来源、博物馆/AAT/V&A/FIT、9 本公版书。
- 动作：记录候选来源 URL/书目；判断“补哪类真实缺口”（用 `11-验收/P5E/eligibility.csv` 的 INSUFFICIENT/REVIEW，不按卡数）。
- 禁止：用风格想象/相似度生成“事实”；为降低孤立数而硬找来源。
- 退出：候选有明确主题 + 预期可定位证据 + 许可可判定。

### 2. license（许可）
- 分类：`link_only`（V&A 等）、`ODC-BY`/`other_permission`（AAT）、`public_domain`（PG 书）、`unknown`（不得入库）。
- 记录：`license_status`、rights_statement、URL、date_accessed、HTTP 状态；**0 图片下载/内嵌**（本库策略）。
- 限制：书 page UNCONFIRMED；现代译注/图版单独判断。
- 退出：许可可引用且已写来源卡；不可引用则停止。

### 3. extract（事实提取）
- 区分三类：`historical_evidence`（来源可定位）/`sourced_style_observation`（观察）/`creative_inference`（设计推断）。
- 每条事实必须有 locator：book_fact（PG 书号/章/段/行；page UNCONFIRMED）或 URL；单件实例不得外推时代通例。
- 卡片写法：只改目标字段/相关小节；不改 ID、evidence_status、既有事实；样式/设计关系标 `factual=false/design_only=true`。
- 退出：每个断言有来源/定位；事实与解释分栏。

### 4. dedupe（去重/同义词）
- 查：重复 ID、重复 URL、name_zh/name_en、aliases、同义概念。
- 当前已知（需处理）：**3 对重复来源 URL**（SRC-0036↔0175、SRC-0163↔0022、SRC-0115↔0157）；**6 组别名冲突**（腰带/着物/tunic/长袍/gigot/seam allowance）；2 组跨类型同名（gloves/leather，非重复卡）。
- 规则：同 URL 只能保留 1 个 canonical 来源卡（其余标 `canonical_id`/alias，不重复计数）；同义概念在 aliases/定义中互指；**不合并不同历史概念**（如 MAT-0012/0013 物性卡与材料卡）。
- 退出：无重复 URL/ID；同义冲突有说明或 canonical。

### 5. relation validation（关系校验）
- schema：`00-系统/关系类型.md` v3；类型/方向/主语类型/证据/置信上限；`style_interpretation` 固定 design-only/medium/factual=false。
- 可见性：高置信 claim 正文必须有 `[[target]]`；medium/design 关系在正文标 review/marker；draft 卡可不渲染但需 review。
- 工具：`python3 scripts/relation_consistency.py`（必须 0 errors）、`scripts/relation_trace.py`、`scripts/graph_analyze.py`（图指标只读）。
- 禁止：关键词/相似度自动建历史事实；`may_have_part` 不得写成 `has_part`；`in_style` 不得作历史事实。
- 退出：consistency 0；无未解析 target；无自动 high。

### 6. human review（人工审核）
- 队列：6 key_garments flags（PRD-0004/0006/0007/0008/0011）、38 基线 draft、59 isolates、239 候选（39 source_verifiable/163 needs_human/37 reject）。
- 规则：medium/review **不得自动升 high/verified**；必须引用真实来源/可见链接；draft 提升需人工签署；flags 需人工证据（不自动确认）。
- 产物：`11-验收/P5D/REVIEW-QUEUE.csv` / `11-验收/P5E/candidate-review.csv`；新增决策写入 review 记录。
- 退出：每批有明确结论（保留 review/移除/补证），无“静默升级”。

### 7. tests（自动测试/门禁）
- 必跑：`validate.py`（458）、`build_sources.py --check`（234）、`relation_consistency.py`（0 errors）、`tests/test_relation_consistency.py`、`tests/test_relation_trace.py`。
- 全回归（发布前/大批次）：`run_acceptance.py` 45、`quality_eval.py`、composer 9、workflow 9、P4-MACBETH 11、security/lookbook/skill-sync/backup/human、`validate_outfits.py --all`。
- 现状：quality_eval **NOT_RUN**（超时，需稳定环境重跑）；GUI 另见 UAT 手册。
- 退出：门禁 PASS 或明确 NOT_RUN + 原因；不得把 NOT_RUN 写 PASS。

### 8. ingest（入库/提交）
- 先备份：`python3 scripts/backup_restore.py backup`（verify PASS；restore 可用）。
- 变更范围：只 stage 目标卡片/来源/报告/脚本；禁止顺手改无关卡。
- 提交前：validate/build/consistency + diff 复核 + 报告更新（P5F-RELEASE-CHECK/STATUS/RELEASE-GATE）。
- 提交信息：批次主题 + 指标（卡/来源/关系/覆盖/测试）。
- 回滚：`backup_restore.py restore` 或按 manifest 回滚；记录 rollback dir。
- 退出：commit + 报告一致 + 备份可还原。

## 1. MOC / 导航维护（每批必做）

- 新增/改名内容卡或来源卡后：更新对应 `00-系统/MOC/*.md` 与 `00-系统/MOC/来源证据.md`（只加导航链接，不改事实/不加 frontmatter）。
- 当前缺口：35 内容（LOOK-0024..0035、STY-0011..0015、GAR-0088..0091、STR-0027..0035、MAT-0015..0019）+ 23 来源（SRC-0530..0552）未进 MOC → **发布/GUI UAT 前必须补齐**。
- 检查：MOC 链接全部解析（当前 482/482）；根 README/入口是否有链接（当前 0 链接，P3）。

## 2. 维护指标与停止规则

- 每次批次记录：新增/修改卡数、来源数、关系数（按类型/置信）、覆盖（适用性分母）、来源可见率（单列）、consistency errors、测试 PASS/NOT_RUN、review 决策。
- 停止规则：证据不足不进库；关系弱/共现不进 high；MOC/UAT 未完成不宣称发布；**不以增加卡数/全图连通率为目标**。
- 质量优先：**一个可定位证据 > 十条无源关系**；**review 队列可长期存在**，不强行清零。

## 3. 角色与节奏

- 角色：architect（结构与 schema）、narrator（知识/卡片）、researcher（来源/许可）、engineer（工具/回归）、verifier（独立验收/报告）、human reviewer（flags/draft/GUI 签字）。
- 节奏：小批次（≤20–30 卡或 ≤30 关系）→ 人工复核 → 测试 → 提交；每季度/里程碑做一次全量健康检查（本报告 §1–§8）。

## 4. 风险与限制

- quality_eval 未在当前树通过（NOT_RUN）；GUI 未验收；MOC 覆盖缺口；重复 URL/别名；4 本背景书未接卡；page UNCONFIRMED。
- 维护时不得新造第二套系统（无独立 DB/外部 wiki/影子卡片）；所有状态以本 vault + `reports/` + `11-验收/` 为准。
