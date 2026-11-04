# P3.6 Agent-native E2E — 10 real headless runs

- Command: real `dsh --profile headless --json` sessions in the Vault
- Checker: `scripts/check_skill_e2e.py`

| Case | Scenario | Skill | Scripts | IDs/SRC | Answer | PASS/FAIL |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | Macbeth Lady - three-stage contemporary theatre A/B/C | yes | query.py, recommend.py, workflow.py | yes | yes | PASS |
| T02 | Macbeth - three-stage A/B/C | yes | query.py, recommend.py, workflow.py | yes | yes | PASS |
| T03 | 1930s Shanghai rainy-night journalist + continuity | yes | query.py, workflow.py | yes | yes | PASS |
| T04 | ER nurse night shift | yes | query.py, recommend.py | yes | yes | PASS |
| T05 | space-station mechanic | yes | query.py, recommend.py | yes | yes | PASS |
| T06 | Ghana-UK wedding groom | yes | query.py, recommend.py | yes | yes | PASS |
| T07 | same-session modification | yes | query.py, recommend.py | yes | yes | PASS |
| T08 | insufficient historical evidence | yes | query.py, recommend.py | yes | yes | PASS |
| T09 | historical+cyberpunk conflict request | yes | query.py | yes | yes | PASS |
| T10 | multi-scene continuity + image/video prompts | yes | query.py, workflow.py | yes | yes | PASS |

- PASS: 10 / 10
- FAIL: 0 / 10
