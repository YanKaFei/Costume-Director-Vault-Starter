# P5-B — Relation consistency, relation query filters, Workflow & Agent E2E

- Date: 2026-11-05
- Scope: `scripts/relation_consistency.py`, `scripts/query.py` relation filters,
  workflow regression, official/overlay Agent relation-query E2E
- No cards/00-system edited for P5-B. Existing P5-A corrections were applied
  separately (39 rows) and are consumed by migration/query/graph/consistency.
- Evidence root: `11-验收/P5B/`

## 1. Relation consistency

`scripts/relation_consistency.py` validates:
- every YAML relation target resolves to a real content card or `04-来源` source;
- every high-confidence relation has a visible wikilink in the body;
- every visible `cited source` wikilink has a matching `claim_supported_by` relation;
- no duplicate relation; no duplicate bidirectional fact;
- no medium/low relation in cards except explicit P5-B corrections
  (`reports/P5B-RELATION-CORRECTIONS.csv`, 3 downgraded rows allowed as review-queue
  exceptions);
- MOC pages (`00-系统/MOC/`) are navigation only: skipped and never used as facts.

Result: **400 cards, 202 relations, 0 errors** (`11-验收/P5B/relation-consistency.json`).
Corrected downgrades: 3; stale P5-A candidate rows are filtered by the corrections
CSV in query/graph/consistency. GAR-0045 remains `confidence=medium` and its
high-only visible source link was removed; GAR-0033/SRC-0155 removed relation/link
is absent.

Tests `tests/test_relation_consistency.py` (5/5):
clean relation; missing visible link; orphan cited-source link; duplicate relation;
low-confidence-in-body (synthetic) detection; MOC skipped.

## 2. Relation query filters

`query.py` now supports:
- `--relation-type` (all v2 types), `--related-to`, `--confidence`,
  `--relation-evidence`, `--relations-from cards|candidates|all`;
- JSON result rows include `relations[]` with type/direction/evidence/confidence,
  real target ID, `target_type`, `target_path`, `target_name_zh`, `origin`
  (`card` vs structured `candidate`); no relation is inferred from a wikilink.
- Candidate rows are filtered/adjusted by P5-B corrections (rejected/excluded rows
  cannot appear; downgraded rows carry corrected confidence/evidence).

Examples verified:
```bash
python3 scripts/query.py --relation-type claim_supported_by --related-to SRC-0109 --confidence high --json
# -> GAR-0008, target SRC-0109, path 04-来源/SRC-0109-FIT-vest-waistcoat.md
python3 scripts/query.py --relation-type may_have_part --confidence medium --limit 2 --json
# -> GAR-0002/GAR-0003 -> STR-0001 (medium, candidate)
python3 scripts/query.py --relation-type context_includes --limit 5 --json
python3 scripts/query.py --relation-type appears_in_look --related-to GAR-0002 --json
```
Tests `tests/test_query_relations.py` (5/5): garment→part, garment→accessory,
material, context/period, outfit LOOK, exact source target path, related-to, and
no-wikilink-only inference.
Combined P5-B tests: **19/19 PASS**
(`11-验收/P5B/test-relation-consistency-query.log`).

## 3. Workflow regression diagnosis

Reported symptom: 9 workflow tests slow/hang at 0% CPU. Investigation:
- No deadlock found; the suite is **slow**, not hung. Each test spawns several
  `workflow.py` subprocesses, each of which runs multiple `query.py`/`recommend.py`
  child processes; CPU is on short-lived children, so a parent can appear at 0%.
- A 90-second per-test wrapper timed out while running a multi-workflow case; this
  was a timeout-policy artifact, not a product failure.
- Full suite with a 300-second timeout:
  `Ran 9 tests in 111.573s — OK`; **9/9 PASS**.
- Evidence: `11-验收/P5B/workflow/full-test.log`; per-test logs under
  `11-验收/P5B/workflow/` (the 90s wrapper timeouts are retained as diagnosis
  evidence and are not counted as PASS).
- No code change was required for workflow itself; recommendation: keep CI timeout
  ≥180s (current suite ~112s) and avoid 90s per-case wrappers. If future CI shows
  true 0%-CPU >300s, capture child PIDs/`sample` output before killing.

## 4. Real DSH Agent E2E (official vs Doubao overlay)

Three relation-query prompts per route; each run is a real headless DSH session with
the Vault skill. Five criteria are checked by
`11-验收/P5B/agent-e2e/validate_e2e.py`:
1. skill call (`tool_call.skill`);
2. tools executed (`bash` query.py with `--relation-type` and completed results);
3. result success (completed tool results);
4. `turn_end.completed` (not merely a final/intermediate event);
5. complete user output (≥120 chars, ≥2 real IDs).

| Case | Route | skill | query tools | result | turn_end | output | Overall |
|---|---|---|---|---|---|---|---|
| RQ1 | official | PASS | 2 | PASS | completed | 2108 chars | **PASS** |
| RQ2 | official | PASS | 4 | PASS | completed | 2597 chars | **PASS** |
| RQ3 | official | PASS | 4 | PASS | completed | 8293 chars | **PASS** |
| RQ1 | overlay | PASS | 1 | PASS | completed | 1287 chars | **PASS** |
| RQ2 | overlay | PASS | 2 | PASS | completed | 2607 chars | **PASS** |
| RQ3 | overlay | PASS | 3 | PASS | completed | 5263 chars | **PASS** |

- **Official: 3/3 PASS; overlay: 3/3 PASS; no intermediate-call PASS used.**
- Returned real IDs include GAR-0008→SRC-0109, GAR-0002/GAR-0003→STR-0001,
  GAR-0024, STR-0003/0005, PRD-0001 context relations, LOOK-0001 appears_in_look,
  and real `04-来源` paths.
- Evidence: `11-验收/P5B/agent-e2e/{official,overlay}/RQ1..RQ3.{txt,events.jsonl,stderr.log,answer/validation}`;
  validator summary `validation-summary.json` / `.txt`.
- Official and overlay recorded separately; overlay used temporary
  `/tmp/dsh-doubao.yml`, no user profile edits. RQ4/RQ5 overlay replacement runs
  (simpler prompts) also completed; not needed for the 3-case minimum.

## 5. P5-B corrections integration

`reports/P5B-RELATION-CORRECTIONS.csv` has 39 rows: 19 reject_candidate, 6 flag_review,
4 remove_key_garment, 3 downgrade_relation, 2 keep_review, 2 keep_review_design,
1 replace_key_garment, 1 remove_relation, 1 exclude_from_migration.

Consumption:
- `relation_migrate.py`: corrections map suppresses removed/rejected relation additions;
  downgraded relation never re-added as high; rerun `--dry-run --full` is idempotent
  (`changed_cards=0, non_idempotent=[]`). Test `test_corrections_cannot_be_readded`
  confirms GAR-0045/SRC-0405 is not re-added high and GAR-0033/SRC-0155 relation/link
  stays absent; GAR-0045 card remains medium.
- `graph_apply.py`: rejected/excluded edges filtered; downgraded confidence applied.
- `query.py`: stale P5-A candidate rows filtered/adjusted; `relation_consistency.py`
  accepts only correction-listed downgrades and filters candidate review rows.
- No corrections CSV or schema file was overwritten.

## 6. Residual / honest caveats

1. Workflow suite is slow (~112s), not hung; 90s per-case wrapper is too short.
2. E2E overlay RQ2/RQ3 initially explored for long; they completed with turn_end and
   passed; slower overlay/routing remains environment-dependent. Intermediate
   events were never counted as PASS.
3. Query relation filters use migrated card YAML plus structured
   `RELATION-CANDIDATES.csv`, never wikilink inference. Candidate rows remain
   candidates (medium/low unless migrated) and do not create card facts.
4. Corrections are applied as review exceptions; relation semantics still require
   human/architect review for medium/low contexts (`context_includes` etc.).
