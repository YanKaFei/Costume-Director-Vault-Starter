## Card result

**Card ID: `STR-0028`** — 青果领/披肩领 / **shawl collar**
- Path: `02-结构细节/STR-0028-青果领-披肩领.md`
- Type: `garment_part`
- Evidence status: **`verified`**
- Source IDs: **`SRC-0532`**, **`SRC-0539`**
- Query score: `0.0` (returned by exact `--id` lookup, not a relevance ranking)

## Evidence / source

`visual_prompt.py` confirms the same provenance:
- `card_id`: `STR-0028`
- `evidence_status`: `verified`
- `source_ids`: `SRC-0532`, `SRC-0539`
- Evidence tags used: `FACT`, `OBSERVATION`, `INFERENCE`, `CREATIVE`
- Conflicts: **0 errors / 0 warnings / 0 notices**

Module provenance:
| Module | Evidence tags | Source |
|---|---|---|
| `structure_detail` | `FACT`, `OBSERVATION` | card type + structured fields |
| `construction_note` | `INFERENCE` | card `prompt_en` |

## English structure prompt

**`structure_detail` (FACT/OBSERVATION-based):**

> detail of shawl collar on garment part construction seams closures edge finish and hardware orthographic clarity no stylisation

**`construction_note` (INFERENCE — card's own `prompt_en`):**

> construction note from card prompt shawl collar jacket continuous rolled collar no notch front facing period or modern tailoring

The second module is explicitly tagged `INFERENCE`, so it should not be presented as historical fact.

## Image generation

**No image was generated.** The tool returned:
- `image_generation: false`
- `model_agnostic: true`
- `delivery: "text prompt only"`

This is a text-only, model-agnostic prompt; no image, image test, or visual approval exists.
