# P4 回归报告（REGRESSION）

- 生成：2026-11-04 16:26；verifier / task-45；快照 **399 卡（内容 188 + 来源 211）**；HEAD `7f7a21b`
- 目的：确认 P4（书籍/结构/组合器/视觉/Macbeth）未破坏 P3.6 既有功能与指标。

## 1. 套件结果（全部独立重跑）

| # | 套件 | 命令 | 退出码 | 结果 |
|---|---|---|---|---|
| 1 | 结构校验 | `python3 scripts/validate.py` | 0 | **PASS**：399/399；来源卡 211；0 错误 0 警告 |
| 2 | 来源对账 | `python3 scripts/build_sources.py --check` | 0 | **PASS**：211/211；CSV 212 行 |
| 3 | 验收 | `python3 scripts/run_acceptance.py` | 0 | **PASS 45/45** |
| 4 | 质量评估 | `python3 scripts/quality_eval.py --no-write` | 0 | **OVERALL PASS（17/17）** |
| 5 | Workflow | `python3 tests/test_workflow.py` | 0 | **9/9 OK**（106.8s） |
| 6 | Composer | `python3 11-验收/P4-COMPOSER/test_outfit.py` | 0 | **9/9 PASS** |
| 7 | Macbeth P4 | `python3 11-验收/P4-MACBETH/test_macbeth_p4.py` | 0 | **11/11 PASS** |
| 8 | 独立 composer 抽检 | `scripts/outfit.py` ×3（macbeth/rain_continuity/conflict） | 0 | 0 缺失 ID、0 未解析 SRC、A/B/C 项差 ≥2、连续性显式 |

## 2. 旧检索/推荐指标对比（P3.6 → P4）

| 指标 | P3.6 | **P4** | 变化 | 阈值 | 判定 |
|---|---|---|---|---|---|
| query relevant@5 | 4.16 | **4.16** | 0 | ≥4.0 | PASS |
| query precision | 0.945 | **0.929** | **−0.016（−1.6pp）** | ≥0.8 | PASS（轻微漂移，WARN 观察） |
| query zero-hit rate | 0.0 | **0.0** | 0 | ≤0.2 | PASS |
| recommend crash rate | 0.0 | 0.0 | 0 | 0 | PASS |
| example in A rate | 0.0 | 0.0 | 0 | 0 | PASS |
| warning coverage | 1.0 | 1.0 | 0 | ≥0.8 | PASS |
| A/B/C all-pairwise distinct | 0.9778 | **0.9778** | 0 | ≥0.8 | PASS |
| evidence coverage | 0.868 | **0.868** | 0 | ≥0.65 | PASS |
| context ref clean | 1.0 | 1.0 | 0 | 1.0 | PASS |
| narrative presence | 1.0 | 1.0 | 0 | 1.0 | PASS |
| prompt contamination | 0 | 0 | 0 | 0 | PASS |
| fabrication violations | 0 | 0 | 0 | 0 | PASS |
| occupation mismatch | 0 | 0 | 0 | 0 | PASS |
| rainwear false claim | 0 | 0 | 0 | 0 | PASS |
| arctic indoor | 0 | 0 | 0 | 0 | PASS |
| context mismatch | 0 | 0 | 0 | 0 | PASS |
| SOURCES.csv sync | 1.0 | 1.0 | 0 | 1.0 | PASS |

**结论**：
- **无功能性回归**：17 项质量指标中 16 项完全持平/保持 PASS；唯一漂移为 **precision −1.6pp**（仍在阈值 0.8 之上），最可能由检索池从 363→399 卡（新增 22 内容卡 + 14 来源卡）导致相关源卡排序被稀释；**不构成发布阻断**，列入 P5 观察（NEXT-PLAN-P4）。
- 旧 CLI/退出码/JSON 契约未变：`recommend.py`/`query.py`/`workflow.py` 未修改（P4 commit 只新增 `scripts/books_extract.py`、`scripts/outfit.py`；旧脚本 0 行变更）。
- 45 例验收全部 PASS，query 命中数（见 `11-验收/测试结果/SUMMARY.md`）未出现 0 命中场景。

## 3. P4 专项与 P3.5 基线对比（Macbeth）

| 指标 | P3.5 historical（baseline） | **P4 composer（Macbeth rise）** | 结论 |
|---|---|---|---|
| looks | 9（每 stage 1 套，不完整） | **3（完整 A/B/C）** | 结构更完整 |
| avg_items/look | 1.0 | **5.0** | 槽位显著填充 |
| max A/B/C diff | 0 | **4** | A/B/C 有实质差异 |
| unique SRC | 3 | **21** | 来源覆盖大幅提升 |
| 证据完整性/ID 真实性 | true | **true** | 保持 |
| continuity explicit | 6 issues（P3.5 workflow） | 该对比用例 `false`（输入未给 states） | 输入缺口，非 composer 回归 |

## 4. 残余风险

1. precision −1.6pp：非阻断，P5 观察（新增卡可能需权重/过滤微调，不得为此改旧 CLI 契约）。
2. 62 draft 未人工复核；四套人工门禁（GUI/逐图版权/评分/draft）未执行 → 不得宣称 public ready。
3. 书籍 5 条 candidate、11 条 partial 未进入 verified 结论；需 architect 二次核实后再建卡。
4. HF 许可未核实（Garments2Look/fashion-clip 权重）与 NC/无许可来源不得进入卡/公开物。

## 5. 复现

见 `reports/P4-REPORT.md` §11（全部命令），日志：`/tmp/p4_validate.txt`、`/tmp/p4_build.txt`、`/tmp/p4_acc.log`、`/tmp/p4_qeval.txt`、`/tmp/p4_wftest.log`、`/tmp/p4_composer_test.log`、`/tmp/p4_macbeth_test.log`、`/tmp/p4_outfit_*.json`。
