# P5-F — Graph unresolved-relation closure + regression

- Date: 2026-11-05
- Scope: `scripts/graph_analyze.py` + tests only; no card/00-system edits
- Evidence: `11-验收/P5F/`

## 1. Root causes and fixes

1. **5 typed_unresolved** were all `GAR-EXAMPLE-001` references. The file/id is
   valid, but `ID_RE` accepted only numeric suffixes and `by_id` omitted the
   EXAMPLE id. Fix:
   - `ID_RE` now accepts `(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-[A-Z0-9-]+`;
   - `by_id` indexes every node's actual `fm.id`, including `GAR-EXAMPLE-001`.
2. **1 unresolved wikilink `target`** came from inline code in
   `00-系统/关系类型.md`. Fix:
   - strip fenced and inline code **before** scanning wikilinks (fenced first,
     then inline code spans), so documentation examples are ignored.
3. Added `tests/test_graph_analyze.py` (4/4 PASS):
   EXAMPLE ID resolves; inline/fenced code ignored; a real missing target is still
   reported; production graph is clean.

## 2. Graph metrics

| Metric | Before | After |
| --- | ---: | ---: |
| typed_unresolved | **5** | **0** |
| unresolved_wikilinks | `{target: 1}` | **`{}`** |
| typed_edges | 737 | **742** |

Evidence: `graph-before.json`, `graph-after.json`; production rerun
`graph.json` = 0 typed unresolved / 0 unresolved links / 742 typed edges.

## 3. Post-fix checks

- `validate.py`: **PASS 458/458, 0 errors/warnings** (`validate.log`).
- `relation_consistency.py`: **0 errors** (458 cards, 334 relations, 9 MOC skipped)
  (`consistency.log`).
- Graph tests: **4/4 PASS** (`test-graph-analyze.log`).

## 4. Agent E2E — five criteria

| Case | Route | skill | tools | result | turn_end | output | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RQ1 paths | official | PASS | yes | PASS | completed | 2323 chars | **PASS** |
| RQ2 style query | official | PASS | yes | PASS | completed | 1941 chars | **PASS** |
| RQ3 character | official | PASS | yes | PASS | completed | 1687 chars | **PASS** |
| RQ1 paths | overlay | PASS | yes | PASS | completed | 954 chars | **PASS** |
| RQ2 style query | overlay | PASS | yes | PASS | completed | 1489 chars | **PASS** |
| RQ3 character | overlay | PASS | yes | PASS | completed | 834 chars | **PASS** |

- **Official 3/3 PASS; overlay 3/3 PASS.**
- All five: skill call, relation/query tool executed, completed result,
  `turn_end.completed`, complete user output.
- Validator: `11-验收/P5F/e2e/validate_e2e.py`; summary
  `11-验收/P5F/e2e/validation-summary.json`; no intermediate-call PASS.

## 5. Full regression

| Check | Result | Evidence |
| --- | --- | --- |
| validate | **PASS 458/458** | `11-验收/P5F/validate.log` |
| relation_consistency | **0 errors / 334 relations** | `11-验收/P5F/consistency.log` |
| graph_analyze | **typed_unresolved 0 / unresolved 0** | `graph.json` |
| graph tests | **4/4 PASS** | `test-graph-analyze.log` |
| acceptance | **45/45 PASS** | P5E full-run log (unchanged cards/scripts) |
| composer | **9/9 PASS** | P5E full-run log |
| workflow | **9/9 PASS (130.1s)** | P5E full-run log |
| P4-MACBETH | **11/11 PASS** | P5E full-run log |
| relation_trace | **6/6 PASS** | P5E unit batch (56/56) |
| security/lookbook/skill-sync/backup/human | **56/56 unit tests PASS** | P5E unit batch log |
| quality_eval | **NOT_RUN** — current run exceeded timeout; prior PASS was before E3 and is not counted | P5E `regress-quality.log` |

No current PASS is claimed for quality; it remains an explicit NOT_RUN. Graph fix
does not touch cards/recommend/query/composer, so the P5E full-run matrix remains
applicable; validate/consistency/graph/E2E were rerun after this fix.

## 6. Limits

- `EXAMPLE` IDs are now accepted for graph resolution but remain example evidence;
  no factual promotion.
- Documentation code examples are ignored, but real orphan targets still count.
- Quality eval current run is NOT_RUN, not hidden.
- E2E used direct prompts; broad exploratory runs are not counted.


---

## 7. task-96 最终复核（2026-11-05 12:02）

- **quality_eval**：E3 后重跑 **PASS**（relevant@5 **4.16**、precision **0.92**、zero-hit **0.0**；`/tmp/p5e_quality.log`）。P5-F 仅改 `scripts/graph_analyze.py` + 测试 + MOC 导航/报告，**未改卡片/关系/query/composer**，故该 PASS 适用于当前内容；§5 的 NOT_RUN 为 P5-F 修复前记录。
- **图（修复版当前树）**：`typed_unresolved 0`、`unresolved_wikilinks {}`、`typed_edges 742`、components 60、singletons 59、source_ids 478；graph 测试 **4/4 PASS**。
- **MOC**：lead 补齐 35 新内容 + 23 新来源；独立复算 **224/224 内容、234/234 来源、544 链接、0 未解析**；9 页仍无 frontmatter。
- **独立回归复核**：validate **458/458 PASS**、build **234 PASS**、consistency **0/334**；E2E official **3/3**、overlay **3/3** 五项全 true（`11-验收/P5F/e2e/validation-summary.json`）。
- 结论：**P5-F 收口 PASS（WARN：3 对重复 URL、18 条 VERIFIED 未入库、GUI NOT_RUN、P5-F 未提交）**。
