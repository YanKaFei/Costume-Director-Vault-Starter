# P5-E E4/E6 — Candidate review + Agent evidence-retrieval regression

- Date: 2026-11-05
- Script: `scripts/candidate_review.py` (read-only; no card writes, no promotion)
- Evidence: `11-验收/P5E/`
- Candidate input: `11-验收/P5D/DESIGN-QUEUE-REMAINING.csv` (239 rows)
- Final consistency state after E3: 458 cards / **334 relations** / 0 errors

## 1. Candidate review tiers

| Tier | Count | Meaning |
| --- | ---: | --- |
| source_verifiable | **39** | real target + verified endpoints + source/audit available; **human review only**, no auto promotion |
| needs_human | **163** | design/co-occurrence or interpretive evidence; keep queued |
| reject_or_rework | **37** | missing/invalid target or invalid subject type; do not migrate |
| **Total** | **239** | all 239 design_only candidates separately counted |

- **0 auto-promotions; 0 card writes.** Policy string: `NEVER auto-promote
  medium/review to high/verified`.
- `design_only=true` on all 239; relation tools can filter them.
- Reject examples: scene `in_style` (15), LOOK `may_have_part` (5), historical
  endpoints not verified (17; overlapping reasons).
- Tool/tests: `candidate_review.py`, `tests/test_candidate_review.py` **5/5 PASS**
  (239 rows, tiers, no promotion/writes, invalid subject rejection, design filter).

## 2. Agent E2E — all five criteria

| Case | Route | skill | tools | result | turn_end | output | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RQ3 character/anchors/design | official | PASS | 2 | PASS | completed | 5765 chars | **PASS** |
| RQ4 garment→part/material | official | PASS | 3 | PASS | completed | 2098 chars | **PASS** |
| RQ5 character/continuity | official | PASS | 4 | PASS | completed | 1049 chars | **PASS** |
| RQ1 garment→structure/material | overlay | PASS | 6 | PASS | completed | 5702 chars | **PASS** |
| RQ2 style→garment + period refusal | overlay | PASS | 11 | PASS | completed | 5250 chars | **PASS** |
| RQ3 character/anchors/design | overlay | PASS | 2 | PASS | completed | 2701 chars | **PASS** |

- **Official 3/3 PASS; overlay 3/3 PASS.**
- Criteria enforced: skill call, relation/candidate tool execution, completed
  result, `turn_end.completed`, complete output (>=120 chars, >=2 real IDs).
- No intermediate-call PASS. Two official attempts hit QUOTA 402 and are retained
  as failed evidence but not counted; the counted runs completed.
- Validator: `11-验收/P5E/e2e/validate_e2e.py`;
  `validation-summary.json`; answers/events under `e2e/{official,overlay}`.

Coverage in prompts/results: garment→structure/material, style→garment, period
refusal (GAR-0015 is not a 1950s qipao), character→complete outfit, fact vs
interpretation vs design, approved anchors (template empty; not invented),
continuity lock, scene continuity.

## 3. Full regression

| Check | Result | Evidence |
| --- | --- | --- |
| validate.py | **PASS 458/458, 0 errors** (after E3) | `regress-validate-final.log` |
| build_sources.py | **PASS 234 sources** | `regress-build.log` |
| acceptance | **PASS 45/45** | `regress-acceptance.log` |
| quality_eval | **NOT_RUN — current run exceeded timeout (>2.5 min)**; previous full-run PASS at 10:35, before E3 relation-only changes; not counted as current PASS | `regress-quality.log` |
| composer | **9/9 PASS** | `regress-composer.log` |
| workflow | **9/9 PASS (130.1s)** | `regress-workflow.log` |
| P4-MACBETH | **11/11 PASS** | `regress-macbeth.log` |
| relation_trace | **6/6 PASS** (in 56-test batch) | `regress-tests.log` |
| relation_consistency | **0 errors** (458 cards, 334 relations, 9 MOC skipped) | `regress-consistency-final.log` |
| security/lookbook/skill-sync/backup/human closeout | **56/56 unit tests PASS** | `regress-tests.log` |
| candidate review | **5/5 PASS** | `test-candidate-review.log` |

No hidden/NOT_RUN PASS: quality is explicitly NOT_RUN for this run.

## 4. Limits

1. Candidate review is triage only: `source_verifiable` is a review label, not a
   promotion; all 239 remain design/review and no card was changed.
2. 37 rejects are conservative; overlapping reasons mean counts are not additive.
3. Current quality_eval did not finish within the run timeout; the earlier PASS was
   before E3 and is not presented as a current pass. Re-run scheduled separately.
4. E2E broad prompts were exploratory; only the final six completed runs count.
5. Approved anchors are empty in the only Look Bible template; no anchors were
   invented.
6. `context_includes` is context evidence, not per-garment historical proof;
   design/co-occurrence relations are never historical facts.
