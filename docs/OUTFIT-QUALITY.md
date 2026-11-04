# Outfit Quality — R1.1 C/D

## 1. Generation vs evaluation (AUD-001)

`scripts/outfit.py` generates a complete outfit; `scripts/abc_eval.py` evaluates it
independently. The evaluator never edits or re-ranks the generated looks, and its
`automated_score` is explicitly **not a director score**; human review remains required.

```bash
# quality-evaluate one composer input
python3 scripts/abc_eval.py --input input.json --json

# evaluate an existing composer output
python3 scripts/abc_eval.py --outfit outfit.json --json

# independent held-out set
python3 scripts/abc_eval.py --heldout 11-验收/R1.1/CD/heldout --json
```

## 2. Post-composition hard constraints (AUD-002)

After all slots are filled, `outfit.py` validates:

- torso core: one-piece/set or top+bottom; footwear; no duplicate item IDs; no
  one-piece+top/bottom stacking;
- weather: rain requires rainwear outer when outdoors; cold/storm requires an outer
  layer when outdoors (indoor rain-outside is excluded);
- action safety: heeled/open footwear blocked for battle/dance constraints;
- occupation identity / approved anchors: strict professions and
  `approved_anchors` must be present in every look;
- period/region: historical mode requires at least one evidence-tier period and
  region anchor per look;
- item compatibility: unknown IDs and example cards are violations; source IDs and
  evidence coverage are reported.
- `approved_anchors` input is an explicit list of IDs that must appear.

### Per-item compatibility declarations (inspired too)

Every selected item gets an `item_compatibility` entry
(`slot,id,period_ok,region_ok,period_tier,status`). Period/region mismatches are
collected in `declared_mismatches`; they cannot be silently hidden.

Status semantics:
- `ok`: no hard violations, no declared item mismatches;
- `declared_mismatch`: inspired/fictional design with explicit per-item
  era/region mismatches; `hard_constraints_passed=false` (not a normal `ok`,
  not historical accuracy);
- `blocked`: hard violations or historical mode mismatches without
  Creative Override; `looks=[]`, attempted looks in `blocked_looks`;
- `override`: explicit Creative Override (valid intent/conflicts,
  `historical_accuracy=false`), violations retained.

On violation the normal output is suppressed:

```json
{
  "status": "blocked",
  "checks": {"hard_constraints_passed": false},
  "constraint_violations": [{"code": "...", "look": "A", "items": []}],
  "looks": [],
  "blocked_looks": [ ... attempted looks ... ]
}
```

CLI exit `3` for blocked output (same family as no-candidate), so a caller cannot
mistake it for an approved recommendation.

### Creative override

Only an explicit override may show a blocked design:

```json
"creative_override": {
  "intent": "stylized stage Macbeth",
  "conflicts": ["11th c Scotland has no exact garment cards", "inspired analogue wardrobe"],
  "historical_accuracy": false
}
```

Then output `status=override`, keeps `constraint_violations`, records `creative_override`,
and forces `historical_accuracy=false`. An override with
`historical_accuracy: true`, missing `intent`, or empty `conflicts` is rejected and
the output remains blocked. It can never claim historical accuracy.

## 3. A/B/C quality metrics (AUD-001)

`abc_eval.py` reports, per pair:

- actual item ID difference (`item_diff`);
- structural slot difference (`slot_diff`);
- silhouette difference (`silhouette_diff`);
- palette difference (`palette_diff`) and material difference (`material_diff`);
- independent axes: `items` requires **>=2 actual item replacements (`item_diff >=4`)**,
  `slots` requires **>=2 changed slots**; additional axes are silhouette,
  materials, palette, narrative;
- `meaningful`: must have both `items` and `slots` axes (>=2 independent axes);
  a one-item swap fails even if silhouette differs;
- `one_item_swap_gaming`: `item_diff <=2` or `slot_diff <2` is not a meaningful
  costume direction;
- duplicate looks / synonym-or-reorder-only detection;
- hard-constraint pass/override and violation count;
- source validity/coverage, palette/material harmony, narrative presence;
- `automated_score` + explicit `not_for_director_review: true` note.

The held-out set (`11-验收/R1.1/CD/heldout/`, 6 cases not used for tuning) produces
`heldout-results.json`: 6/6 pass, all pairs meaningful (2+ items across 2+ slots),
no one-item-swap gaming, declared mismatches explicit, source coverage 1.0.

## 4. Tests / evidence

```bash
python3 -m unittest tests.test_r1_1_cd -v
```

`tests/test_r1_1_cd.py` covers:
normal hard constraints; cross-era block; valid override; invalid override
(`historical_accuracy=true`) rejected; synthetic one-item-swap gaming rejected;
5-case held-out evaluation; source validity/narrative.

Evidence:
- `11-验收/R1.1/CD/test-output.log` — 7/7 PASS;
- `11-验收/R1.1/CD/heldout-results.json`;
- `11-验收/R1.1/CD/regression-composer.log` (9/9), `regression-macbeth.log`
  (P4-5), `regression-acceptance.log` (45/45), `regression-workflow.log` (9/9).

## 5. Limitations

- Hard constraints are rule-based; culture/era compatibility uses KB tier evidence,
  not a full historical ontology.
- `period_tiers`/`region_tiers` are card-level evidence; a mixed look may pass with
  one anchor while retaining analogue pieces, which are still reported as risks.
- A blocked output keeps attempted looks in `blocked_looks` for debugging but not in
  `looks`; consumers must check `status`/exit code.
- Override is a design/authorization escape hatch, not evidence; it always sets
  `historical_accuracy=false`.
- The automated score cannot substitute for director review; it is intentionally
  conservative on one-item gaming.
