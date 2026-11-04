# P5-C 关系修复复验（P5C-RELATION-FIX）

- 生成：2026-11-05 02:10（Asia/Shanghai）；verifier / task-79（P5-C P1 修复后独立复验）
- 快照：HEAD `f500289` + P5-C 修复工作区（未提交）；**458 卡 = 224 内容 + 234 来源**
- 性质：只读复验；未改卡片/脚本；不重复跑 Agent E2E（核对已有证据）。

## 1. 修复前后对比（P1）

| 项 | 修复前（task-75） | **修复后（本轮独立）** | 判定 |
|---|---|---|---|
| `relation_consistency.py` | **71 errors**（missing_visible 42 / low_conf 17 / invalid_type 12） | **0 errors / cards 458 / relations 265 / moc_skipped 9** | **PASS** |
| 35 张新卡来源链接 | 纯文本 `SRC-xxxx`，42 条 relation 无可见链接 | **166 个 `[[SRC-…]]` wikilink；0 个 inline-code `SRC-`；新卡零可见缺失** | **PASS** |
| 整体 source_ids 可见率 | 196/460（42.6%） | **352/460（76.5%）**；可见来源 **167/167**（100%） | **PASS（来源可见）** |
| 零可见 SRC 卡 | 69（55 draft + 14 reviewed） | **39（38 draft + GAR-0045 medium review）** | 与 P5-B 基线一致（GAR-0045 为 review） |
| 新 relation 严格抽样 | 8/64 = 12.5% | **62/64 = 96.9%（严格可见口径）**；规则口径 63/64 = 98.4% | **PASS（≥95%）** |
| style_interpretation | 非法类型 12 errors | **schema v3 合法**：design-only、evidence=interpretive、confidence=medium、factual=false；12/12 有可见链接 | **PASS** |
| validate / build | 458 PASS / 234 PASS | **458/458 PASS / 234/234 PASS** | PASS |
| validate_outfits | 35 looks（12 pass/23 legacy） | **35 looks，pass 12，fail 0，legacy 23** | PASS |
| `tests/test_validate_outfits.py` | FAIL（断言 23） | **EXIT 0**（已更新） | PASS |

## 2. 新关系抽样明细（64 条，全部核对）

| 类型 | 总数 | target 存在 | 正文可见 | 严格通过 |
|---|---:|---:|---:|---:|
| claim_supported_by | 47 | 47 | **47** | **47** |
| uses_material（medium） | 5 | 5 | 3 | 3（2 条 medium 无可见/无正文 marker，remain review） |
| style_interpretation（design-only medium） | 12 | 12 | **12** | **12** |
| **合计** | **64** | **64** | **62** | **62/64 = 96.9%（≥95%）** |

- 规则口径（允许 medium 设计关系无可见，但需正文 review/解释 marker）：63/64 = 98.4%。
- 唯一严格失败：STR-0029→MAT-0001（uses_material medium；正文无可见 MAT 链接/marker）——consistency 脚本 0 errors 因其按 v2 规则允许 medium 设计关系；建议后续补正文 marker（WARN，不影响 ≥95%）。

## 3. style_interpretation 语义（PASS）

- `00-系统/关系类型.md` v3：style_interpretation 固定 **design-only、factual=false、evidence=interpretive、confidence=medium、禁止 high**；Agent 过滤规则明确「不得作为年代/地域/穿着事实」。
- STY-0011..0015 正文明确「设计解释，不是历史事实」；12 条关系均 medium/interpretive、均有可见 LOOK 链接。
- 结论：**未把 creative/design 当史实**（诚实性 PASS）。

## 4. 覆盖率（修复仅改可见链接，卡/关系数不变）

| 指标 | 数值 |
|---|---|
| 内容卡 | 224（+35） |
| garment→outfit | 55/92（**59.8%**；P5-B 48.9%） |
| LOOK→narrative | 25/35（**71.4%**；P5-B 56.5%） |
| garment→component/material/style | 16/92（17.4%）/37/92（40.2%）/3/92（3.3%） |
| garment period/region | 91/92（98.9%） |
| garment→claim/source | 86/92（93.5%） |
| relations | 265（claim 238 / style_interpretation 12 / in_style 8 / uses_material 7） |
| source_ids 对 / 可见 | **460 / 352（76.5%）**（修复前 196/460=42.6%） |

## 5. 回归（本轮独立）

- **PASS（本轮独立）**：validate 458/458、build 234/234、relation_consistency **0 errors**、relation_consistency 单测 5/5、relation_trace 6/6、validate_outfits validator 12/12 与测试 EXIT 0、security 7/7、lookbook 6/6、skill-sync 3/3、backup 7/7、human closeout 3/3。
- **engineer logs（当前 P5-C 树，未本轮重跑）**：acceptance 45/45、composer 9/9、workflow 9/9（`11-验收/P5C/regress-*.log`，01:51–01:54；P5-C 修复仅改正文 SRC 链接，未改脚本/测试）。
- **NOT_RUN**：quality_eval、Macbeth（P5-C 修复窗口未运行；不写 PASS）。

## 6. 65→64 单点 / 38 draft / 6 flags

- isolates.csv 仍 65 行，但 **SRC-0013 已被 MAT-0018 引用 → 有效 64**（P2：文件未更新）；未引用来源 67。
- 38 张基线 draft 仍 draft（零可见 SRC，保持）；全库 draft 79（新增 12 LOOK+5 STY）。
- 6 flags（PRD-0004/0006/0007/0008/0011）key_garments 未变，仍 review_queue，未自动确认。

## 7. Agent E2E（核对已有证据，不重跑）

- 官方 RQ1–3 **3/3 PASS**、overlay RQ2–4 **3/3 PASS**；五项（skill/工具/结果/turn_end.completed/完整输出）全满足；IDs 0 missing（`11-验收/P5C/e2e/validation-summary.json` + events 解析一致）。

## 8. 残余风险

1. quality_eval/Macbeth 本轮未跑 → NOT_RUN。
2. isolates.csv 65 未更新为 64；source-audit 白名单仍 211（23 新源未纳入）。
3. 9 本 P4 书源仍 0 内容引用（仅研究文档，无强制引用）。
4. STR-0029→MAT-0001 为唯一 medium 无可见/marker 关系（WARN）。
5. P5-C 修复未提交（HEAD 仍 f500289）。
6. GUI NOT_RUN/PENDING；PUBLIC 门禁 B1–B6/L1–L6 保持。
