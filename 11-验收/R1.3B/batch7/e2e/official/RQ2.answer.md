## Brief

All three commands exited `0`; no images or videos were generated.

| Command | Result |
|---|---|
| `query.py --id LOOK-0031 --json` | 1 card hit |
| `query.py --id LOOK-0008 --json` | 1 card hit |
| `visual_prompt.py --id LOOK-0031 --kind outfit --json` | text prompt only, `image_generation: false` |

## Modern vs historical outfit IDs

| | LOOK-0031 | LOOK-0008 |
|---|---|---|
| ID / name | `LOOK-0031` — contemporary night-shift nurse, rainy handover | `LOOK-0008` — 1930s Shanghai changshan intellectual look |
| Era class | **Modern / contemporary** (`subcategory: contemporary`; `periods: [contemporary]`; `regions: [britain, global]`) | **Historical** (`subcategory: historical`; `periods: [1930s, republican_era]`; `regions: [china, shanghai]`) |
| Card path | `09-造型组合/LOOK-0031-contemporary-night-shift-nurse,-rainy-handover.md` | `09-造型组合/LOOK-0008-1930年代上海长衫知识分子.md` |
| Evidence / review | `interpretive` / `draft` | `interpretive` / `draft` |
| Items | `GAR-0036`, `GAR-0046`, `GAR-0044`, `GAR-0050`, `GAR-0048` | `GAR-0032`, `GAR-0034`, `STR-0011` |
| Sources | `SRC-0400`, `SRC-0406`, `SRC-0410`, `SRC-0408` | `SRC-0202`, `SRC-0203` |

Modern = `LOOK-0031`; historical = `LOOK-0008`. Both are interpretive draft looks, not verified historical evidence.

## Video prompt availability

| Card | Video prompt? | Detail |
|---|---|---|
| `LOOK-0031` | **Yes — both structured and prose** | Frontmatter `prompt_video`: “nurse walking quickly into an emergency department in rain, raincoat over white uniform, badge catching light, bag set down, handheld medium shot, continuity on uniform and badge.” Also has a `## 视频提示词` block (SUBJECT / CONSISTENCY / LIGHT / CAMERA / NEGATIVE); `visual_prompt_type` includes `video`. |
| `LOOK-0008` | **Yes — section block only; no frontmatter field** | Has a `## 视频提示词` block (“slow 180-degree turn”, same `look_items=GAR-0032, GAR-0034, STR-0011`, no morphing), but **no `prompt_video` key** in frontmatter. No one-line prose video prompt exists. |

Note on the builder: `visual_prompt.py --kind outfit` for `LOOK-0031` emitted only `outfit_hero`, `continuity`, and `negative` modules — **no video module was returned** by this `outfit` call, even though the card itself stores video text.

## Approved anchors

| Card | Approved anchors |
|---|---|
| `LOOK-0031` | **Empty** — explicit `approved_anchors: []` |
| `LOOK-0008` | **Absent** — no `approved_anchors` field in frontmatter (treated as empty) |

The `continuity_lock` lines on both cards (e.g. uniform collar/badge/raincoat wetness for `LOOK-0031`; collar height, five frog closures, sleeve/slit for `LOOK-0008`) are continuity constraints, **not** approved anchors — do not conflate them.

## Visual prompt result (`LOOK-0031`, outfit)

- `kind: outfit`, `lang: en`, `model_agnostic: true`, `image_generation: false`, `delivery: text prompt only`
- `evidence_status: interpretive`; tags `OBSERVATION`, `INFERENCE`, `CREATIVE`
- Hero prompt preserves `GAR-0036 GAR-0046 GAR-0044 GAR-0050 GAR-0048`, palette `white navy pale blue black`
- Conflicts: `low_confidence` notice only (“evidence_status=interpretive; not verified”); `0` errors, `0` warnings, `1` notice
- **No image generated**; no video generated.
