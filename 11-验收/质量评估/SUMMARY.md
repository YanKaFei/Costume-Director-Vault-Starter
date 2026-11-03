# P3 质量评估 SUMMARY

- 评估脚本：`scripts/quality_eval.py`（独立子进程）
- 输入：25 个 query 探针 + 30 个推荐用例（11-验收/测试输入）

## 指标前后对比（P2.5 审计 → 当前）

| 指标 | P2.5 基线 | 当前 |
| --- | --- | --- |
| query relevant@5 (0-5) | 3.0 | 3.84 |
| query precision | 0.862 | 0.941 |
| query zero-hit rate | 0.16 | 0.12 |
| recommend crash rate | 1.0 | 0.0 |
| example card in A rate | 0.7222222222222222 | 0.0 |
| warning coverage | 0.0 | 1.0 |
| A/B/C all-pairwise distinct rate | 0.0 | 0.9666666666666667 |
| prompt contamination count | 0.11 | 0 |

## 当前推荐质量

- 用例数：30；崩溃：0；证据覆盖率：0.702；警告覆盖率：1.0；A/B/C 全差异率：0.9666666666666667；narrative 覆盖率：1.0；context 引用清洁率：1.0；预算替代满足率：0.933；prompt 串文数：0；编造违规：0

## 逐用例（推荐）

| 用例 | exit | looks | example in A | A/B/C diffs | budget | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | 0 | 3 | False | {'a_b': 3, 'a_c': 2, 'b_c': 5} | cheaper | context_gap,period_approximate,period_era_level,region_mismatch,occupation_coverage_gap,rainwear_gap |
| T02 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch,occupation_coverage_gap,rainwear_gap,conflict_weather_vs_material |
| T03 | 0 | 1 | False | {'a_b': 4, 'a_c': 2, 'b_c': 2} | equivalent_cost | context_gap,occupation_coverage_gap,rainwear_gap,budget_equivalent,identity_arc_continuity |
| T04 | 0 | 3 | False | {'a_b': 3, 'a_c': 3, 'b_c': 4} | cheaper |  |
| T05 | 0 | 3 | False | {'a_b': 5, 'a_c': 4, 'b_c': 3} | equivalent_cost | context_gap,period_approximate,occupation_coverage_gap,future_wardrobe_gap,rainwear_gap,budget_equivalent |
| T06 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | equivalent_cost | context_gap,region_mismatch,budget_equivalent |
| T07 | 0 | 3 | False | {'a_b': 5, 'a_c': 2, 'b_c': 3} | equivalent_cost | context_gap,occupation_coverage_gap,budget_equivalent |
| T08 | 0 | 3 | False | {'a_b': 5, 'a_c': 2, 'b_c': 3} | equivalent_cost | context_gap,occupation_coverage_gap,budget_equivalent |
| T09 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | equivalent_cost | context_gap,region_mismatch,occupation_coverage_gap,rainwear_gap,budget_equivalent |
| T10 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,period_era_level,occupation_coverage_gap |
| T11 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,period_era_level,region_mismatch,occupation_coverage_gap |
| T12 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,occupation_coverage_gap |
| T13 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,occupation_coverage_gap |
| T14 | 0 | 3 | False | {'a_b': 2, 'a_c': 6, 'b_c': 4} | cheaper | context_gap,region_mismatch,occupation_coverage_gap,rainwear_gap |
| T15 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 5} | cheaper | context_gap,region_mismatch,occupation_coverage_gap |
| T16 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap |
| T17 | 0 | 1 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,period_era_level,region_mismatch,occupation_coverage_gap |
| T18 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | equivalent_cost | context_gap,region_mismatch,occupation_coverage_gap,budget_equivalent |
| T19 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,period_era_level,occupation_coverage_gap |
| T20 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,period_era_level,occupation_coverage_gap |
| T21 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,period_era_level,occupation_coverage_gap |
| T22 | 0 | 3 | False | {'a_b': 8, 'a_c': 5, 'b_c': 3} | cheaper | context_gap,period_era_level |
| T23 | 0 | 3 | False | {'a_b': 3, 'a_c': 2, 'b_c': 3} | equivalent_cost | context_gap,context_gap,period_approximate,period_era_level,conflict_movement_vs_footwear,budget_equivalent |
| T24 | 0 | 1 | False | {'a_b': None, 'a_c': None, 'b_c': None} | none | context_gap,period_era_level,knowledge_gap_slots,occupation_coverage_gap,looks_incomplete |
| T25 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | equivalent_cost | context_gap,period_approximate,future_wardrobe_gap,budget_equivalent |
| T26 | 0 | 3 | False | {'a_b': 3, 'a_c': 2, 'b_c': 5} | equivalent_cost | context_gap,region_mismatch,occupation_coverage_gap,rainwear_gap,budget_equivalent |
| T27 | 0 | 3 | False | {'a_b': 3, 'a_c': 2, 'b_c': 3} | equivalent_cost | context_gap,region_mismatch,occupation_coverage_gap,cross_cultural_wedding,ceremonial_coverage_gap,budget_equivalent |
| T28 | 0 | 3 | False | {'a_b': 3, 'a_c': 5, 'b_c': 2} | cheaper | context_gap,period_approximate,period_era_level,region_mismatch,occupation_coverage_gap,rainwear_gap |
| T29 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 2} | cheaper | context_gap,period_approximate,period_era_level,region_mismatch,occupation_coverage_gap,rainwear_gap |
| T30 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,period_approximate,period_era_level,region_mismatch,occupation_coverage_gap,rainwear_gap |

## 阈值与结论

- query_relevant_at_5：当前=3.84，阈值=3.8 → PASS
- query_precision：当前=0.941，阈值=0.8 → PASS
- query_zero_hit_rate：当前=0.12，阈值=0.2 → PASS
- recommend_crash_rate：当前=0.0，阈值=0.0 → PASS
- example_in_a_rate：当前=0.0，阈值=0.0 → PASS
- warning_coverage_rate：当前=1.0，阈值=0.8 → PASS
- abc_all_pairwise_distinct_rate：当前=0.9666666666666667，阈值=0.8 → PASS
- evidence_coverage：当前=0.702，阈值=0.65 → PASS
- context_ref_clean_rate：当前=1.0，阈值=1.0 → PASS
- narrative_presence_rate：当前=1.0，阈值=1.0 → PASS
- prompt_contamination_count：当前=0，阈值=0 → PASS
- fabrication_violations：当前=0，阈值=0 → PASS

**OVERALL: PASS**
