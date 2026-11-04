# P4-5 Macbeth validation — SUMMARY

- Command: `python3 11-验收/P4-MACBETH/test_macbeth_p4.py`
- Composer: `scripts/outfit.py` (real KB IDs/SRC only)
- Inputs: `11-验收/P4-MACBETH/inputs/`; outputs: `outputs/`; queries: `query/`

| Case | Result | Detail |
| --- | --- | --- |
| stage_changes_Macbeth | PASS | - |
| stage_changes_Lady_Macbeth | PASS | - |
| two_character_relationship | PASS | - |
| full_slots_accessories | PASS | - |
| historical_evidence_gap | PASS | - |
| minimal_vs_complex | PASS | - |
| closeup_detail | PASS | - |
| movement_action | PASS | - |
| video_continuity | PASS | - |
| bilingual_term_search | PASS | - |
| evidence_insufficient_refusal | PASS | - |

- PASS: 11 / 11
- FAIL: 0 / 11

## movement_action root cause / fix
- Root cause: the test joined `prompt_outfit` with `" ".join(...)` (iterating characters) and only inspected `risks`, so an existing `prompt_outfit`/`movement_note` was invisible to the assertion.
- Fix: (a) test now inspects `str(look["prompt_outfit"]).lower()` and `movement_note`; (b) composer now emits an explicit `movement_note` and includes the action adaptation in `prompt_outfit` for action-constrained briefs (`battle, running, riding, climbing stairs`).
- After fix: `movement_action` PASS; P4-5 11/11.

## Final regression matrix
| Suite | Result |
| --- | --- |
| P4-5 Macbeth validation (`test_macbeth_p4.py`) | PASS 11/11 |
| P4-3 Outfit Composer (`P4-COMPOSER/test_outfit.py`) | PASS 9/9 |
| P3 acceptance (`run_acceptance.py --no-write`) | PASS 45/45 |
| P3.5 workflow (`tests/test_workflow.py`) | 9/9 PASS |
