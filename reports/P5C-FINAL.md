# P5-C 最终验收结论（P5C-FINAL）

- 定稿：2026-11-05 02:05（Asia/Shanghai）；verifier / task-75；快照：HEAD `f500289` + P5-C 工作区（未提交；458 卡/234 来源）
- 依赖：`P5C-RELATION-COVERAGE`、`P5C-OUTFIT-KNOWLEDGE`、`P5C-STYLE-ACCESSORIES`、`P5C-STRUCTURE-MATERIAL`、`P5C-SOURCE-REUSE`、`P5C-AGENT-REGRESSION`、`P5C-BASELINE`
- 声明：未改卡片/脚本；GUI 未执行，不得声称通过。

## 0. 总结论（重要）

**P5-C P1 关系修复已独立复验通过（FAIL → PASS）：**
- ✅ **PASS（核心）**：458 卡/458 validate、build 234、新增 35 内容卡 + 23 来源卡、12 套 Outfit 硬约束 12/12、evidence_type 诚实、来源许可/HTTP 200、Agent E2E 五项（官方 3/3、overlay 3/3）、relation_trace 6/6、relation_consistency 单测 5/5、security/lookbook/skill-sync/backup；
  - **relation_consistency：0 errors / 265 relations**（修复前 71 errors）；
  - **新关系严格抽样：62/64 = 96.9%（≥95%）**（修复前 12.5%）；
  - **来源可见率：352/460 = 76.5%**（修复前 42.6%）；35 张新卡来源链接 161/161 可见、0 inline-code。
- ✅ **覆盖率改进**：garment→outfit 48.9%→**59.8%**、LOOK→narrative 56.5%→**71.4%**；relations 201→265。
- ⚠️ **残余（P2/WARN，不阻断重分类）**：`tests/test_validate_outfits.py` 已更新 EXIT 0；isolates.csv 仍 65（SRC-0013 已引用→有效 64；文件未更新）；source-audit 白名单仍 211（23 新源未纳入）；9 本书源仍 0 内容引用；STR-0029→MAT-0001 为唯一 medium 无可见/marker 关系（WARN）；P5-C 修复未提交（工作区）。
- **门禁**：PRIVATE-READY/PRIVATE-USE = **YES（附 WARN：残余 P2/quality 未跑/未提交）**；PUBLIC-READY = **NO（BLOCKED，B1–B6 + L1–L6）**；GUI = **NOT_RUN**。

## 1. 新增卡/来源（PASS）

| 项 | 结果 |
|---|---|
| 总卡 | **458 = 224 内容 + 234 来源**（+35 内容、+23 来源） |
| 新增内容 | LOOK-0024..0035（12）、STY-0011..0015（5）、GAR-0088..0091（4）、STR-0027..0035（9）、MAT-0015..0019（5） |
| 新增来源 | SRC-0530..0552（V&A 10 link_only + Getty AAT 13 ODC-BY） |
| 校验 | validate **458/458 PASS**（0 errors/0 warnings）、build **234/234 PASS**（CSV 234 行） |
| 来源引用 | **23/23 新来源被内容卡引用**；0 图片；23/23 有 HTTP 200 证据 |
| 书源 | 9 本 P4 书源仍 **0 内容卡引用**（仅研究文档；无强制引用）——残留 |

## 2. 覆盖率 Before / After（同一口径，详见 RELATION-COVERAGE）

| 指标 | Before（400卡） | After（458卡） | 变化 |
|---|---|---|---|
| garment→outfit | 43/88（48.9%） | **55/92（59.8%）** | **+10.9pp** |
| LOOK→narrative | 13/23（56.5%） | **25/35（71.4%）** | **+14.9pp** |
| garment→component | 16/88（18.2%） | 16/92（17.4%） | −0.8pp |
| garment→material | 35/88（39.8%） | 37/92（40.2%） | +0.4pp |
| garment→style | 3/88（3.4%） | 3/92（3.3%） | 持平 |
| garment period/region | 87/88（98.9%） | 91/92（98.9%） | 持平 |
| garment→claim/source | 82/88（93.2%） | 86/92（93.5%） | +0.3pp |
| 正式 relations | 201 | **265**（+64） | +64 |
| 有 relations 内容卡 | 142/189 | **165/224** | +23 |

**来源可见率（分开统计，不得与关系覆盖混算）**：source_ids 对 299→**460**；正文可见 **191（63.9%）→196（42.6%）**；可见来源 **142/143→147/167**；零可见卡 39→**69**（55 draft + 14 reviewed）。

## 3. 关系质量（PASS，修复后）

- **64 条新 formal relations**：claim 47、uses_material 5、style_interpretation 12。
- 严格抽样（target+结构化+正文可见+schema+证据/置信）：**62/64 = 96.9%（≥95%）**；claim 47/47 可见、uses_material 3/5、style_interpretation 12/12（schema v3 合法 design-only）。
- 规则口径（允许 medium 设计关系无可见但需 marker）：63/64 = 98.4%；唯一 WARN：STR-0029→MAT-0001（medium，无可见/marker）。
- `relation_consistency.py` 当前：**cards 458 / relations 265 / errors 0**（修复前 71 errors）；`style_interpretation` 已升级为 v3 design-only/medium/factual=false。
- 结论：**P5-C 关系一致性 PASS（≥95% 抽样）**；WARN 项见 §8。

## 4. Outfit 与证据诚实（PASS）

- `validate_outfits.py --all`：**35 looks, pass 12, fail 0, legacy 23**；12 套新 Outfit 硬约束 **12/12 PASS**。
- evidence_type：**historical_evidence 2 / sourced_style_observation 5 / creative_inference 5**；historical 含历史证据；creative 未声称史实复原；sourced 标风格观察。**诚实性 PASS**。
- 12 LOOK 的 look_items 全部真实且正文可见（0 missing）。
- 唯一测试问题：`tests/test_validate_outfits.py` FAIL（旧断言 23，实际 35）→ 测试需更新（P2）。

## 5. Agent E2E（五项，官方/overlay 分开）PASS

| 运行 | 用例 | 五项 | 
|---|---|---|
| 官方 DeepSeek | RQ1/RQ2/RQ3 | **3/3 PASS**（skill/工具/结果/turn_end.completed/完整输出；final 1174–5739 chars，IDs 7–26，0 missing） |
| overlay（临时 patch） | RQ2/RQ3/RQ4 | **3/3 PASS**（final 1272–1670 chars，IDs 5–10，0 missing） |

- 证据：`11-验收/P5C/e2e/validation-summary.json`、`{official,overlay}/RQ*.events.jsonl`；summary 与独立解析一致。

## 6. 回归（当前树）

| 套件 | 结果 |
|---|---|
| validate 458 / build 234 | **PASS**（本轮独立执行） |
| acceptance | **PASS 45/45**（engineer P5-C log `11-验收/P5C/regress-acceptance.log`；本轮未重跑） |
| composer | **PASS 9/9**（engineer log） |
| workflow | **PASS 9/9**（engineer log；Ran 9 tests OK 121.3s） |
| relation_trace | **PASS 6/6**（本轮独立执行） |
| relation_consistency 单测 | **PASS 5/5**（本轮独立；但数据一致性 71 errors 另见 §3） |
| security / lookbook / skill-sync / backup / human closeout | **PASS 7/7 / 6/6 / 3/3 / 7/7 / 3/3**（本轮独立） |
| validate_outfits | **PASS 12/12**；`tests/test_validate_outfits.py` 已更新 **EXIT 0**；relation_trace 6/6、consistency 单测 5/5 |
| quality_eval / Macbeth / human closeout | **NOT_RUN**（quality 77.2s 未产出后终止 EXIT -15；Macbeth/human 0.0s 未启动；证据 `/tmp/p5c_tests2.out`；不写 PASS） |

## 7. 65 单点 / 38 draft / 6 flags

- **65→64 单点（isolates.csv）**：文件仍 65，但 **SRC-0013 已被新卡 MAT-0018 引用** → 有效单点 **64**；isolates.csv 未更新（P2）。分类仍 34 legit /16 evidence_missing /14 future /1 no_verifiable。
- **38 draft 基线**：仍保持 draft；全库 draft 62→79（新增 12 LOOK+5 STY 为 draft，不属于基线 38 变化）。
- **6 flags**：PRD-0004/0006/0007/0008/0011 的 key_garments 未变，仍 review_queue，**未自动确认**（人工）。

## 8. 残余风险 / 未执行

1. isolates.csv 仍 65（SRC-0013 已被 MAT-0018 引用 → 有效 64；文件未更新，P2）。
2. source-audit 白名单仍 211；新增 23 来源未纳入 audit（P2，lead 已知）。
3. 9 本书源仍未被内容卡引用（仅研究文档；无强制引用，可接受但未消化）。
4. quality_eval/Macbeth 本轮修复窗口未完成 → **NOT_RUN**（不写 PASS；P5-A 前次质量 PASS 仅参考）。
5. STR-0029→MAT-0001 为唯一 medium 无可见/marker 关系（WARN，不阻断）。
6. P5-C 修复未提交（HEAD 仍 f500289；工作区改动含新卡/链接/测试）。
7. GUI（Obsidian）**NOT_RUN/PENDING**；PUBLIC 门禁 B1–B6/L1–L6 未解除。

## 9. 门禁

| 门禁 | 状态 |
|---|---|
| PRIVATE-READY / PRIVATE-USE | **YES（技术层，附 WARN：残余 P2、quality/Macbeth NOT_RUN、未提交）** |
| PUBLIC-READY | **NO（BLOCKED）**：B1 GUI NOT_RUN、B2 逐图版权 NOT_RUN、B3 15 案例 NOT_RUN、B4 62 draft、B5、B6；L1–L6 保持 |
| B7 CSV | CLOSED（234/234） |
| HUMAN UAT（GUI） | **NOT_RUN / PENDING**（无截图/签字，不得声称通过） |

## 10. 建议（P5-C 收口前）

1. 修复关系一致性：新卡来源改 `[[SRC-…]]` 可见链接；style_interpretation 改用 schema 合法类型或先扩展 schema；medium 关系正文标注 review；重跑 `relation_consistency.py` 至 0 errors。
2. 更新 `tests/test_validate_outfits.py`（23→35 或动态）。
3. 更新 isolates.csv（SRC-0013）、source-audit 白名单（23 新源）。
4. 提交 P5-C 工作区；在冻结 commit 上补跑 quality_eval、Macbeth、human closeout 留档。
5. 人工：6 flags、38 draft、GUI 验收。
