# P3 质量评估 SUMMARY

- 评估脚本：`scripts/quality_eval.py`（独立子进程）
- 输入：25 个 query 探针 + 45 个推荐用例（11-验收/测试输入）

## 指标前后对比（P2.5 审计 → 当前）

| 指标 | P2.5 基线 | 当前 |
| --- | --- | --- |
| query relevant@5 (0-5) | 3.0 | 4.24 |
| query precision | 0.862 | 0.93 |
| query zero-hit rate | 0.16 | 0.0 |
| recommend crash rate | 1.0 | 0.0 |
| example card in A rate | 0.7222222222222222 | 0.0 |
| warning coverage | 0.0 | 1.0 |
| A/B/C all-pairwise distinct rate | 0.0 | 0.9777777777777777 |
| prompt contamination count | 0.11 | 0 |
| occupation mismatch cases (P3-QA D2) | 9 | 0 |
| false rainwear-missing claims (P3-QA D4) | 2 | 0 |
| arctic outerwear indoors (P3-QA M6) | 2 | 0 |
| context mismatch cases (P3-QA M4) | 1 | 0 |
| SOURCES.csv sync gate (R5) | not gated | PASS |

## 当前推荐质量

- SOURCES.csv 同步（R5 质量门）：PASS（`build_sources.py --check` exit=0；RESULT: PASS（CSV 与全部来源卡一致））
- 用例数：45；崩溃：0；证据覆盖率：0.947；警告覆盖率：1.0；A/B/C 全差异率：0.9777777777777777；narrative 覆盖率：1.0；context 引用清洁率：1.0；预算替代满足率：0.956；prompt 串文数：0；编造违规：0；职业错配：0；虚假 rainwear 声明：0；室内极地派克：0；context 错配：0

## 逐用例（推荐）

| 用例 | exit | looks | example in A | A/B/C diffs | budget | warnings |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | period_era_level,region_mismatch,conflict_weather_vs_material |
| T02 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,region_mismatch,occupation_coverage_gap,conflict_weather_vs_material |
| T03 | 0 | 1 | False | {'a_b': 3, 'a_c': 2, 'b_c': 5} | equivalent_cost | context_gap,period_approximate,occupation_coverage_gap,budget_equivalent,identity_arc_continuity |
| T04 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 2} | cheaper | period_approximate,knowledge_gap_slots,occupation_coverage_gap |
| T05 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,period_approximate,occupation_coverage_gap,future_wardrobe_gap |
| T06 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch |
| T07 | 0 | 3 | False | {'a_b': 3, 'a_c': 3, 'b_c': 2} | cheaper | context_gap,period_approximate,occupation_coverage_gap |
| T08 | 0 | 3 | False | {'a_b': 4, 'a_c': 5, 'b_c': 3} | cheaper | context_gap,period_approximate,occupation_coverage_gap |
| T09 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 5} | cheaper | context_gap,period_approximate,region_mismatch,occupation_coverage_gap |
| T10 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 5} | cheaper | context_gap,period_approximate,period_era_level,region_mismatch,occupation_coverage_gap |
| T11 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,period_era_level,region_mismatch,occupation_coverage_gap |
| T12 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,occupation_coverage_gap |
| T13 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,region_mismatch,occupation_coverage_gap |
| T14 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch |
| T15 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch,occupation_coverage_gap |
| T16 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap |
| T17 | 0 | 1 | False | {'a_b': 3, 'a_c': 2, 'b_c': 5} | cheaper | context_gap,period_approximate,period_era_level,region_mismatch,occupation_coverage_gap |
| T18 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,region_mismatch,occupation_coverage_gap |
| T19 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,period_era_level,occupation_coverage_gap |
| T20 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,period_era_level |
| T21 | 0 | 3 | False | {'a_b': 3, 'a_c': 3, 'b_c': 2} | cheaper | context_gap,period_approximate,period_era_level,occupation_coverage_gap |
| T22 | 0 | 3 | False | {'a_b': 5, 'a_c': 7, 'b_c': 2} | cheaper | context_gap,period_era_level,occupation_coverage_gap |
| T23 | 0 | 3 | False | {'a_b': 3, 'a_c': 3, 'b_c': 2} | cheaper | context_gap,context_gap,period_era_level,knowledge_gap_slots,occupation_coverage_gap,conflict_movement_vs_footwear |
| T24 | 0 | 1 | False | {'a_b': None, 'a_c': None, 'b_c': None} | none | context_gap,period_era_level,knowledge_gap_slots,looks_incomplete |
| T25 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 2} | cheaper | context_gap,period_approximate,occupation_coverage_gap,future_wardrobe_gap |
| T26 | 0 | 3 | False | {'a_b': 7, 'a_c': 5, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch |
| T27 | 0 | 3 | False | {'a_b': 6, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,cross_cultural_wedding |
| T28 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | period_era_level,region_mismatch,occupation_coverage_gap,gender_coverage_gap,conflict_weather_vs_material |
| T29 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | period_era_level,region_mismatch,occupation_coverage_gap,conflict_historical_vs_scifi,conflict_weather_vs_material |
| T30 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | period_era_level,region_mismatch,conflict_weather_vs_material,brief_unknown_fields |
| T31 | 0 | 3 | False | {'a_b': 7, 'a_c': 5, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch |
| T32 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch |
| T33 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | equivalent_cost | context_gap,period_approximate,region_mismatch,budget_equivalent |
| T34 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | context_gap,period_approximate,region_mismatch |
| T35 | 0 | 3 | False | {'a_b': 6, 'a_c': 7, 'b_c': 3} | cheaper | context_gap,context_gap,period_approximate,future_wardrobe_gap |
| T36 | 0 | 3 | False | {'a_b': 6, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,cross_cultural_wedding |
| T37 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | period_era_level,region_mismatch,conflict_weather_vs_material |
| T38 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,region_mismatch,occupation_coverage_gap |
| T39 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | equivalent_cost | context_gap,context_gap,period_approximate,period_era_level,region_mismatch,knowledge_gap_slots |
| T40 | 0 | 3 | False | {'a_b': 2, 'a_c': 3, 'b_c': 3} | cheaper | period_era_level,region_mismatch,conflict_weather_vs_material |
| T41 | 0 | 3 | False | {'a_b': 2, 'a_c': 2, 'b_c': 4} | cheaper | context_gap,region_mismatch,occupation_coverage_gap |
| T42 | 0 | 3 | False | {'a_b': 3, 'a_c': 2, 'b_c': 5} | equivalent_cost | context_gap,period_approximate,region_mismatch,budget_equivalent |
| T43 | 0 | 3 | False | {'a_b': 2, 'a_c': 4, 'b_c': 2} | cheaper | context_gap,period_approximate,region_mismatch |
| T44 | 0 | 3 | False | {'a_b': 6, 'a_c': 5, 'b_c': 3} | cheaper | context_gap,period_approximate,future_wardrobe_gap |
| T45 | 0 | 3 | False | {'a_b': 3, 'a_c': 2, 'b_c': 5} | equivalent_cost | context_gap,period_approximate,region_mismatch,budget_equivalent |

## 阈值与结论

- query_relevant_at_5：当前=4.24，阈值=4.0 → PASS
- query_precision：当前=0.93，阈值=0.8 → PASS
- query_zero_hit_rate：当前=0.0，阈值=0.2 → PASS
- recommend_crash_rate：当前=0.0，阈值=0.0 → PASS
- example_in_a_rate：当前=0.0，阈值=0.0 → PASS
- warning_coverage_rate：当前=1.0，阈值=0.8 → PASS
- abc_all_pairwise_distinct_rate：当前=0.9777777777777777，阈值=0.8 → PASS
- evidence_coverage：当前=0.947，阈值=0.65 → PASS
- context_ref_clean_rate：当前=1.0，阈值=1.0 → PASS
- narrative_presence_rate：当前=1.0，阈值=1.0 → PASS
- prompt_contamination_count：当前=0，阈值=0 → PASS
- fabrication_violations：当前=0，阈值=0 → PASS
- occupation_mismatch_cases：当前=0，阈值=0 → PASS
- rainwear_false_claim_cases：当前=0，阈值=0 → PASS
- arctic_indoor_cases：当前=0，阈值=0 → PASS
- context_mismatch_cases：当前=0，阈值=0 → PASS
- sources_csv_sync：当前=1.0，阈值=1.0 → PASS

**OVERALL: PASS**
