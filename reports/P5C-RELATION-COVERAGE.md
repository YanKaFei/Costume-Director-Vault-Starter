# P5-C 关系覆盖与一致性验收（P5C-RELATION-COVERAGE）

- 生成：2026-11-05 02:02（Asia/Shanghai）；verifier / task-75（P5-C 最终验收，只读）
- 快照：HEAD `f500289`（P5-B 已提交）+ P5-C 工作区（**未提交**：458 卡 = 224 内容 + 234 来源）；validate **PASS 458/458**、build **PASS 234/234**
- 方法：同一独立脚本对 `f500289` 快照（/tmp/p5c-before，400 卡）与当前树（458 卡）计算，口径一致；来源可见率与关系覆盖率**分开统计**。

## 1. 新增卡/来源核对（PASS）

| 项 | 结果 |
|---|---|
| 内容卡总数 | **224**（+35） |
| 新增内容卡 | **LOOK-0024..0035（12）+ STY-0011..0015（5）+ GAR-0088..0091（4）+ STR-0027..0035（9）+ MAT-0015..0019（5）= 35** |
| 来源卡 | **234**（+23：SRC-0530..0552） |
| ID 唯一 / validate | **458/458 PASS**；0 错误/0 警告 |
| build_sources | **PASS 234/234**；CSV 234 行 |
| 新来源许可 | V&A 10 张 **link_only**；Getty AAT 13 张 **ODC-BY / other_permission**；23/23 正文有 HTTP 200 证据；0 图片策略保持 |
| 新来源引用 | **23/23 被新内容卡 source_ids 引用**（无新建未用来源）；9 本 P4 书源仍未被内容卡引用（仅研究文档） |
| source-audit 白名单 | **仍 211 行**；新增 SRC-0530..0552 **未纳入** audit 白名单（残留，见 §6） |

## 2. 覆盖率 Before / After（同一口径；数字为卡数/占比）

| 指标 | f500289（400 卡） | **P5-C（458 卡）** | 变化 |
|---|---|---|---|
| 内容卡 | 189 | **224** | +35 |
| garment | 88 | **92** | +4 |
| garment→component（STR） | 16/88（18.2%） | **16/92（17.4%）** | −0.8pp（分母增） |
| garment→material（MAT/PAT） | 35/88（39.8%） | **37/92（40.2%）** | +0.4pp |
| garment→style（in_style/STY 精确） | 3/88（3.4%） | **3/92（3.3%）** | −0.1pp |
| garment→outfit（被 LOOK 引用） | 43/88（48.9%） | **55/92（59.8%）** | **+10.9pp** |
| garment period | 87/88（98.9%） | **91/92（98.9%）** | 持平 |
| garment region | 87/88（98.9%） | 91/92（98.9%） | 持平 |
| garment→claim/source | 82/88（93.2%） | **86/92（93.5%）** | +0.3pp |
| LOOK→narrative | 13/23（56.5%） | **25/35（71.4%）** | **+14.9pp** |
| 正式 relations 总数 | 201 | **265**（+64） | +64 |
| 有 relations 的内容卡 | 142/189 | **165/224** | +23 卡 |
| draft 卡 | 62 | **79**（+17 新 LOOK/STY） | +17 |

### 2.1 来源可见率（单独口径，不与关系覆盖混算）

| 指标 | f500289 | **P5-C** | 变化 |
|---|---|---|---|
| source_ids 引用对 | 299 | **460** | +161 |
| 正文可见 SRC 对 | 191（63.9%） | **352（76.5%，修复后）** | **+12.6pp** |
| 被引用唯一来源 | 143 | **167** | +24 |
| 正文可见唯一来源 | 142/143 | **167/167（100%）** | 全部被引用来源可见 |
| 零可见 SRC 链接的卡 | 39（38 draft + GAR-0045） | **39（38 draft + GAR-0045）** | 与 P5-B 基线一致（new cards 0 缺失） |

**修复后**：35 张新卡来源链接全部 `[[SRC-…]]` 可见（161/161；166 个 SRC wikilink、0 inline-code），relation_consistency **0 errors**。**来源可见率不是关系覆盖率，不能混算**。

## 3. 新关系抽样准确率（PASS，修复后 ≥95%）

对 **64 条新 formal relations**（P5-C 新卡）逐条核对：target 存在、结构化依据、正文可见、schema 类型、evidence/confidence：

| 类型 | 总数 | 正文可见 | 严格通过 | 失败原因 |
|---|---:|---:|---:|---|
| claim_supported_by | 47 | **47** | **47** | 修复后全部可见 |
| uses_material | 5 | 3 | **3** | 2 条 medium 仍无可见/正文 marker（review） |
| style_interpretation | 12 | **12** | **12** | v3 schema 合法（design-only/medium/factual=false），有可见链接 |
| **合计** | **64** | **62** | **62/64 = 96.9%（≥95%）** | **PASS** |

- 规则口径（允许 medium 设计关系无可见但需正文 marker）：63/64 = 98.4%；唯一 WARN STR-0029→MAT-0001（medium，无可见/marker）。
- `style_interpretation` 修复后为 v3 合法 design 关系（interpretive/medium/factual=false），12/12 可见。
- 结论：**P5-C 关系抽样准确率 PASS（96.9% ≥ 95%）**，1 条 medium WARN。

## 4. relation_consistency 全量校验（PASS，修复后）

`python3 scripts/relation_consistency.py`（当前 458 卡）：

- **cards 458 / relations 265 / errors 0 / moc_skipped 9**（修复前 71 errors）。
- 12 条 `style_interpretation` 已按 v3 schema 合法化（design-only、medium、factual=false）；42 条 missing_visible 已由新卡 `[[SRC-…]]` 链接消除；medium/低置信标记已补齐或按 v3 规则允许。
- **判定：关系一致性 PASS（0 errors）**。

## 5. Outfit / 来源复用（PASS 部分）

- **12 套新 Outfit**：`validate_outfits.py --all` → **summary: 35 looks, pass 12, fail 0, legacy 23**；12/12 硬约束 PASS，0 violations。
- evidence_type 分布：**historical_evidence 2 / sourced_style_observation 5 / creative_inference 5**；historical 2 套含 `historical_evidence` 字段；creative 5 套标 `creative_inference`，未声称历史复原；sourced 5 套标 `style_observation`。**诚实性 PASS**。
- 12 LOOK 的 `look_items` 全部真实 ID（0 missing）且正文可见（6/6、7/7 等全部可见）。
- 来源复用：23 新来源均有许可字段/HTTP 200；9 本书仍零内容引用（仅研究文档；无强制引用）；0 图片。
- **测试缺陷**：`tests/test_validate_outfits.py` **FAIL 1/10**（`test_all_legacy_looks_do_not_fail` 断言 summary.looks==23，实际 35）——测试未随新 LOOK 更新（P2）。

## 6. 残留与不一致（修复后）

1. **source-audit 白名单仍 211**：SRC-0530..0552 已建卡/被引用，但未进入 `11-验收/P5/source-audit.csv` 白名单（P2）。
2. **isolates.csv 仍 65**，但 **SRC-0013 已被 MAT-0018 引用 → 有效 64**；文件未更新（P2）。
3. 38 张 draft 基线卡仍保持 draft；全库 draft 62→79（新 12 LOOK+5 STY 为 draft，属新增，不是基线 38 变化）。
4. 6 组 key_garments flag 未变（PRD-0004/0006/0007/0008/0011），仍 review_queue，未自动确认。
5. STR-0029→MAT-0001（uses_material medium，无可见/marker）为唯一 WARN；quality_eval/Macbeth 本轮 NOT_RUN。

---

## 8. 来源侧刷新（task-78，2026-11-05 02:05；与关系覆盖分开）

> 本节只更新**来源白名单/来源可见率**，不改动上面的关系覆盖率数字（关系侧仍以 task-75 的 P5-C 验收为准）。

### 8.1 来源白名单（234）

| 分类 | 数量 | 说明 |
|---|---|---|
| whitelist_connected | **167** | 143 旧 + 23 新（SRC-0530..0552）+ SRC-0013（MAT-0018） |
| whitelist_independent | **48** | 词典/背景/实践/图像许可/覆盖缺口 |
| action_should_connect | **7** | SRC-0028/29/30/37/41/50/59，仍未迁移 |
| action_needs_citation | **9** | P4 书 SRC-0061..0069（仅研究文档引用） |
| blacklist_duplicate | **3** | SRC-0157/0163/0175（canonical 0115/0022/0036） |
| 合计 | **234** | `11-验收/P5/source-audit.csv` 234 行 |

### 8.2 语义单点（isolates）：65 → 有效 64

- 基线 65 条语义单点（`11-验收/P5B/isolates.csv`）；SRC-0013 已由 `MAT-0018 丝绸` 引用 → 解除 1 条，**有效 64**（`11-验收/P5C/isolates.csv`）。
- 保留分类：legit_reference 33、future_topic 14、evidence_missing_expression 16、no_verifiable_relation 1。
- 9 本 P4 书仍在 isolates（needs-citation），不强制迁移。

### 8.3 来源可见率（单独口径）

| 指标 | 数值 | 定义 |
|---|---|---|
| content 卡 | 224 | 全部内容卡 |
| 有 source_ids 的卡 | 199 | frontmatter `source_ids` 非空 |
| `source_ids` 引用对 | **346** | Σ len(source_ids) |
| 正文 wikilink 可见对 | **196（56.6%）** | body 含 `[[SRC-xxxx` 且该 SRC 在 source_ids |
| 正文任意 SRC 文本可见对 | **346（100%）** | body 含 SRC 字符串（含纯文本；engineer 链接修复后全覆盖） |
| 唯一可见来源 | **147/167** | body wikilink 出现的被引用来源 |
| 零 wikilink 可见卡 | **52** | 有 source_ids 但正文无 `[[SRC-`（多为 draft LOOK/STY） |

> 说明：上表的分母/口径与 `P5-SOURCE-RELATIONS.md` 的 P5-C 刷新节一致（均按 frontmatter `source_ids` 逐项计）。task-75 验收 §2.1 曾报「source_ids 引用对 460」，其口径包含正文引用计数（与纯 frontmatter 计数不同）；比较时须先统一口径。**不得**把「可见率」当作「关系覆盖率」。关系覆盖仍见 §2（garment→component/material/style/outfit、LOOK→narrative 等）。

---

## 9. isolates 刷新（P5-D 书籍应用后，2026-11-05 10:40）

- `11-验收/P5C/isolates.csv`：**64 → 有效 59**（移除已 connected 的 5 本书：SRC-0061/0062/0064/0066/0069；其余分类保持不变）。
- 新分布（59）：legit_reference 33、future_topic 14、evidence_missing_expression **11**（原 16 − 5 本）、no_verifiable_relation 1。
- 仍为背景/needs-citation 的 4 本书保留在 isolates：SRC-0063 PG33020、SRC-0065 PG49559、SRC-0067 PG56978、SRC-0068 PG76717。
- 与 source-audit 对齐：whitelist 234、connected **172**、needs-citation **4**；本轮无卡片改动。
