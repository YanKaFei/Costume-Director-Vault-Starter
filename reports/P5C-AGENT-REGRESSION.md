# P5-C — Relation-path retrieval + character/outfit Agent regression

- Date: 2026-11-05
- New script: `scripts/relation_trace.py` (read-only; no card/00-system writes)
- Evidence: `11-验收/P5C/` (traces, tests, regression logs, E2E)
- No existing CLI/JSON changed; query/recommend/outfit/workflow code untouched.

## 1. Capabilities

`relation_trace.py` builds a typed relation index from:
- migrated card YAML `relations:` (corrections-aware), and
- structured `11-验收/P5/RELATION-CANDIDATES.csv`.

It does **not** infer relations from wikilinks. Edges carry type, direction,
evidence, confidence, source_ids, origin, and `factual` flag.

### Depth-limited paths
- `--start ID --max-depth N` (capped at **3**)
- filters **low confidence** (always) and supports `--factual-only` to exclude
  design/co-occurrence edges;
- dedupes node sequences, limits result count, resolves every target to a real
  card or `04-来源` source with path/name;
- returns `paths[]`, `related_ids[]`, `related[]`, and `limits`.

Example `GAR-0015` (see `trace-GAR-0015.json`):
- paths include `GAR-0015 → PRD-0001 → STY-0010 → SRC-0167` with high/verified
  factual edges (source path `04-来源/SRC-0167-…`), capped at depth 3;
- design/co-occurrence edges are marked `factual=false` and excluded by
  `--factual-only`.
- Note: one path cannot traverse the full 7-node chain because the depth cap is 3;
  the supported pattern is a <=3-hop slice such as garment→part→material or
  garment→outfit→scene.

### Character brief → complete outfit
- `--character TEXT` matches LOOK cards by `look_role`/name/body (no invented
  character entity; no new engine).
- returns `look_id`, complete `look_items` with real paths, `prompt_image`,
  `prompt_negative`, `continuity_lock`, conflicts/不适用 conditions, evidence,
  source_ids.
- Example "沙龙女主人" → `LOOK-0001` with 6 items (GAR-0015, STR-0009, STR-0006,
  GAR-0028, GAR-0024, MAT-0002), prompts and conflict notes
  (`trace-character.json`).

### Garment → related outfits
- `--garment ID` returns complete LOOKs whose `look_items` include that garment,
  with full item paths/prompts/conflicts.
- Example GAR-0015 → LOOK-0001 (`trace-garment.json`).

### Look Bible approved anchors
- optional `--look-bible PATH`; consumes `approved_anchors` from a look-bible
  version/project JSON and returns hard/soft anchors.
- Current template's approved anchors are empty (`hard: [], soft: []`), so the
  capability is demonstrated without inventing anchors.

## 2. Regression

| Check | Result |
| --- | --- |
| P4 composer 9 cases | **9/9 PASS** (`regress-composer.log`) |
| 45 acceptance | **45/45 PASS** (`regress-acceptance.log`) |
| Workflow 9 tests | **9/9 PASS, 121.3s** (`regress-workflow.log`) |
| Query/relation/P5B combined tests | **25/25 PASS** (`regress-tests.log`) |
| New relation_trace tests | **6/6 PASS** (`test-relation-trace.log`) |
| validate.py | PASS 400/400 (`validate.log`) |

`relation_trace` tests cover: depth cap/real IDs/SRC, dedupe, low filtered,
`--factual-only`, character→complete look, garment→related look, approved-anchor
loader, and depth cap for max-depth=99.

## 3. Real DSH Agent E2E (five criteria)

Validator: `11-验收/P5C/e2e/validate_e2e.py`; requires all five:
skill call, `relation_trace.py` tool executed, result success,
`turn_end.completed`, complete user output (>=120 chars, >=2 real IDs).

| Case | Route | skill | trace tools | result | turn_end | output | Overall |
|---|---|---|---|---|---|---|---|
| RQ1 paths | official | PASS | 5 | PASS | completed | 5739 chars | **PASS** |
| RQ2 character | official | PASS | 2 | PASS | completed | 4568 chars | **PASS** |
| RQ3 garment/anchors | official | PASS | 1 | PASS | completed | 1174 chars | **PASS** |
| RQ2 character | overlay | PASS | 1 | PASS | completed | 1670 chars | **PASS** |
| RQ3 garment/anchors | overlay | PASS | 1 | PASS | completed | 1558 chars | **PASS** |
| RQ4 paths replacement | overlay | PASS | 1 | PASS | completed | 1272 chars | **PASS** |

- **Official 3/3 PASS; overlay 3/3 PASS; no intermediate-call PASS.**
- Overlay RQ2/RQ3/RQ4 used because overlay RQ1 (paths) did not finish in time; it
  is retained as incomplete evidence and not counted.
- Official/overlay separate; overlay uses temporary `/tmp/dsh-doubao.yml`, no user
  profile changes.
- Summary: `11-验收/P5C/e2e/validation-summary.json`.

## 4. Limits (honest)

1. Depth cap 3 means the seven-type chain is supported as a slice, not one path;
   `garment→part→material→period` ends before accessory/outfit/scene.
2. Relation paths mix explicit card relations and structured candidate rows; only
   high factual edges are `factual=true`. `may_have_part`/`ensemble_with` are
   co-occurrence design relations (medium), never claimed as `has_part`.
3. Character lookup uses LOOK role/name/body text; the Vault has no independent
   character entity IDs, so this is retrieval, not a new character composer.
4. Approved anchors come only from an external Look Bible JSON; the template
   currently has empty anchors. No anchors are invented.
5. Low confidence filtered; medium design edges are visible/marked and excluded
   only with `--factual-only`.
6. Concurrent relation edits by other tasks can change the graph; re-run
   `relation_trace` after migration/corrections. P5-C itself writes no cards.
