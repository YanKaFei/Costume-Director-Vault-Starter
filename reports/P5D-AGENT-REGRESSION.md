# P5-D — Agent relation retrieval E2E + full regression

- Date: 2026-11-05
- Scope: read-only retrieval/E2E and full regression; no cards/scripts edited by this
  task. Evidence: `11-验收/P5D/`.
- Semantic mislinks found by lead review were corrected before E2E finalization
  (see §5).

## 1. Relation retrieval verification

| Capability | Sample result |
| --- | --- |
| garment → part | GAR-0002/GAR-0003 → STR-0001 `may_have_part` medium (candidate/design) |
| garment → material/accessory | GAR-0088 → MAT-0017 `uses_material` medium, visible marker; STR-0029 → MAT-0001 medium, visible marker |
| style → garment | LOOK-0001 → STY-0010 `in_style` medium (card+candidate); LOOK-0003 etc via `--related-to STY-0010` |
| period → outfit | PRD-0001 → GAR-0015 `context_includes` high (evidence level context, not per-garment historical proof) |
| character → outfit | "沙龙女主人" → LOOK-0001, 6 real items (GAR-0015, STR-0009, STR-0006, GAR-0028, GAR-0024, MAT-0002), prompts/conflicts |
| approved anchors | Look Bible template loads but `hard: []`, `soft: []`; no anchors invented |
| design vs history | `--factual-only` trace returns only factual paths; design/co-occurrence edges are `factual=false` and labelled |
| book sources | 18 exact book-source references across 17 cards (SRC-0061/62/64/66/69); real paths and `source_ids` verified |

Examples files: `query-part.json`, `query-style.json`, `query-period.json`,
`trace-character.json`, `trace-factual.json`, `trace-anchors.json`,
`SEMANTIC-FIXES.csv`.

Historical judgment rule: only high + factual + direct evidence is historical;
`uses_material/may_have_part/ensemble_with/in_style/style_interpretation` design
relations are never presented as historical facts.

## 2. Real DSH Agent E2E — five criteria

The broad three-prompt batch was too exploratory and left incomplete runs (retained
but **not counted**). Final evidence uses simpler direct prompts per route.

| Case | Route | skill | tools | result | turn_end | output | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RQ4 paths | official | PASS | 2 | PASS | completed | 3235 chars | **PASS** |
| RQ5 character | official | PASS | 2 | PASS | completed | 2141 chars | **PASS** |
| RQ6 style query | official | PASS | 1 | PASS | completed | 4944 chars | **PASS** |
| RQ4 paths | overlay | PASS | 1 | PASS | completed | 1173 chars | **PASS** |
| RQ7 paths replacement | overlay | PASS | 1 | PASS | completed | 339 chars | **PASS** |
| RQ8 style replacement | overlay | PASS | 1 | PASS | completed | 298 chars | **PASS** |

- **Official 3/3 PASS; overlay 3/3 PASS; no intermediate-call PASS.**
- Required all five: skill call, relation tool execution, completed result,
  `turn_end.completed`, complete user output (>=120 chars, >=2 real IDs).
- Validator: `11-验收/P5D/e2e/validate_e2e.py`; summary
  `validation-summary.json`.
- Overlay uses temporary `/tmp/dsh-doubao.yml`; no profile changes. Official route
  no 402 in this batch.

## 3. Full regression matrix

| Check | Result | Evidence |
| --- | --- | --- |
| validate.py | **PASS 458/458, 0 errors** | `regress-validate.log` |
| build_sources.py | **PASS 234 sources** | `regress-build.log` |
| acceptance | **PASS 45/45** | `regress-acceptance.log` |
| quality_eval | **PASS** | `regress-quality.log` |
| quality_eval_audit | **exit 0** (probes ran) | `regress-quality-audit.log` |
| composer | **9/9 PASS** | `regress-composer.log` |
| workflow | **9/9 PASS in 152.5s** | `regress-workflow.log` |
| P4-MACBETH | **11/11 PASS** | `regress-macbeth.log` |
| relation_trace tests | **6/6 PASS** (part of unit batch) | `regress-tests.log` |
| relation_consistency | **0 errors** (458 cards, 308 relations, 9 MOC skipped) | `regress-consistency.log` |
| security/lookbook/skill-sync/backup/human closeout | **50/50 unit tests PASS** | `regress-tests.log` |
| backfill + consistency post-fix | **14/14 PASS** | `test-semantic-fix.log` |
| validate_outfits | **35 looks (12 pass / 23 legacy / 0 fail)** | `validate-outfits.json` |

No NOT_RUN items remained after completion; all commands returned within the run.

## 4. Semantic corrections (P1 review)

- Removed 5 invalid design relations + markers: SCN-0001→STY-0005 `in_style`;
  LOOK-0019/0003/0017/0008→STR `may_have_part`.
- GAR-0079→SRC-0069 downgraded **medium/interpretive** (book_fact, not standalone
  verified).
- GAR-0033→SRC-0066 removed relation, visible link, and SRC-0066 from `source_ids`
  (only 1908 terminology; not 1940s).
- Added subject-type validation: scene `in_style` rejected; LOOK `may_have_part`
  rejected; `period_region` in_style allowed as historical context; design medium
  allowed only with explicit review/evidence; high facts still require visible links.
- Design pilot: 30 applied, **25 valid** after semantic removal; 5 removed.
  Final coverage split: formal high **262**, design/review medium **46**,
  review queue **239**. No high/historical additions.

## 5. Limits

- Broad E2E prompts were abandoned as exploratory; simple direct prompts were used
  and counted only with all five criteria.
- `context_includes` is context-level evidence, not per-garment historical proof.
- Design/co-occurrence relations remain review-layer; never historical facts.
- Approved anchors were empty in the only available Look Bible template; no
  anchors were invented.
- Concurrent edits can change the relation graph; re-run consistency before any
  final claim.
