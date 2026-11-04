# R1 Skill E2E — official vs Doubao overlay

- Official: `dsh --profile headless --json` (DeepSeek key, no overlay)
- Overlay: same prompts + temporary `--patch /tmp/dsh-doubao.yml`
- Skill: `.dsh/skills/costume-director/SKILL.md` (not modified)

| Case | Coverage | Official | Overlay |
| --- | --- | --- | --- |
| C01 | books | PASS | PASS |
| C02 | structures | PASS | PASS |
| C03 | accessories | PASS | PASS |
| C04 | outfit | PASS | PASS |
| C05 | bilingual | PASS | PASS |
| C06 | visual | PASS | PASS |

- Official: 6 PASS / 0 BLOCKED / 0 FAIL
- Overlay: 6 PASS / 0 BLOCKED / 0 FAIL

## Official mode details
- C01: PASS
- C02: PASS
- C03: PASS
- C04: PASS
- C05: PASS
- C06: PASS

## Overlay mode details
- C01: PASS
- C02: PASS
- C03: PASS
- C04: PASS
- C05: PASS
- C06: PASS

