# P3.6 Skill smoke evidence (task-34)

## Install
- Skill: `.dsh/skills/costume-director/SKILL.md`
- DSH project root (nearest `.git`): `/Users/coffee/Desktop/Costume-Director-Vault-Starter`
- Provider config includes `@deepseek-ai/dsh-skill-filesystem` and `@deepseek-ai/dsh-tool-skill`
  (see `dsh-dump-config.txt`, `skill-plugin-evidence.txt`).

## Smoke command
```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
dsh --profile headless --json "请使用 costume-director skill：为《麦克白》第一幕的麦克白夫人设计 A/B/C 三套服装..."
```
Evidence: `headless-events.jsonl` (171 events, exit was 0 from the CLI wrapper but the turn ended with QUOTA).

## Catalog / skill evidence
- Session cwd = Vault root.
- Agent's first text: “I'll load the costume-director skill first”.
- `tool_call` with `tool: "skill"`, `input.name: "costume-director"`; `tool_result` status completed
  and body contains `<skill_content name="costume-director">` + the skill's Base directory.
- 15 bash tool calls ran real `scripts/query.py`, `scripts/recommend.py`,
  `scripts/workflow.py` commands; outputs were read from the vault.
- Agent created `projects/macbeth-lady-act1/` with script, meta, recommend/workflow outputs.

## Result
- Skill discovery/load: PASS.
- Real script usage: PASS.
- Final natural-language answer: **not produced** — the turn ended with
  `QUOTA: Insufficient Balance (402)` from the DeepSeek provider after 27 steps
  (~120k tokens). A later tiny headless call succeeded, so quota is intermittent /
  balance-limited, not catalog-related. This is the only compatibility blocker
  observed for the smoke test; the skill itself loaded and orchestrated scripts.
- Files: `.dsh/skills/costume-director/SKILL.md`, `docs/SKILL-USAGE.md`,
  `projects/README.md`, `projects/.gitignore`, `projects/_template/README.md`.

## Follow-up (task-35 workaround)
- DeepSeek official key stayed balance-limited. E2E runs used an **existing Doubao
  gateway** via temporary `--patch 11-验收/P3.6/smoke/dsh-doubao.overlay.yml`
  (no user profile changes); 10/10 real headless sessions completed and are in
  `11-验收/P3.6/e2e/T01..T10` with `SUMMARY.md`.
