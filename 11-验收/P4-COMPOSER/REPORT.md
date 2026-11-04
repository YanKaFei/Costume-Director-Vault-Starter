# P4-3 Outfit Composer — report

## Deliverables
- `scripts/outfit.py` — full-slot composer built on `recommend.py` / `costume_lib.py`
  (no changes to legacy recommend/query/workflow CLIs).
- `docs/OUTFIT-COMPOSER.md` — usage, schema, metrics, warnings, exit codes.
- `11-验收/P4-COMPOSER/test_outfit.py` — 9 regression scenarios.
- `11-验收/P4-COMPOSER/runs/` — per-case composer JSON.
- `SUMMARY.md`, `comparison.json`, `regression-acceptance.log`, `regression-workflow.log`.

## Composer test result
`python3 11-验收/P4-COMPOSER/test_outfit.py` → **PASS 9 / 9** (exit 0).
Cases: Macbeth, Lady Macbeth, Ghana cross-cultural, rain continuity, low budget,
close-up, action/dance, nurse occupation, historical+cyberpunk conflict.
Each normal 3-look case: complete torso/footwear, A/B/C pairwise item diff >=2,
real GAR/STR/MAT IDs, resolvable SRC, palette/material/silhouette metrics,
English prompts + negative constraints, evidence gaps surfaced.

## A/B/C difference metrics
- All normal 3-look cases: `abc_metrics.all_pairwise_ge_2 = true`, minimum pairwise
  item difference = **2**.
- `ensure_abc_difference()` repairs collapsed alternatives by swapping one shared
  slot for a real unused candidate (one swap yields exactly two symmetric differences).
- A/B/C palette differences and silhouette are reported per pair; conflict case has
  only 1 look and explicitly reports the historical/science-fiction conflict.

## Old vs new (same inputs)
| Case | legacy slots | composer slots | slot gain | legacy min pair diff | composer min pair diff |
| --- | --- | --- | --- | --- | --- |
| Macbeth | 4 | 5 | +1 | 2 | 2 |
| Ghana cross-cultural | 4 | 4 | 0 | 2 | 2 |
| Nurse | 5 | 5 | 0 | 2 | 2 |

Legacy already had three looks and >=2 differences on these cases. Composer adds:
accessory/carried completion when context-compatible, occupational anchor enforcement
(e.g. nurse GAR-0036, space GAR-0038), palette/material/silhouette/proportion metrics,
continuity states, English outfit/negative prompts, and evidence-gap reporting.
It does not reduce legacy A/B/C differences.

## Regression
- `python3 scripts/run_acceptance.py --no-write` → **PASS 45 / 45**, FAIL 0.
- `python3 tests/test_workflow.py` → **9/9 PASS**, exit 0.
- Legacy `recommend.py` CLI/JSON untouched.

## Limitations
- Silhouette/proportion are deterministic heuristics (default `I` when cards lack
  silhouette data); not pattern-cutting.
- Harmony scores are rule-based, not colour science/fabric physics.
- Accessory/carried prop can stay missing with an explicit warning when no
  context-compatible candidate exists; no cross-cultural hard-fill.
- Continuity states only come from explicit `scenes`/`states`; absent values remain
  `unknown`.
- Conflict case may return only one look; this is honest KB/context insufficiency.
- Text prompts only; no image/video generation.
