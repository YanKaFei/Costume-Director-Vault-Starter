Both commands ran successfully (exit 0). Here is the complete, evidence-based report.

## Brief
- Request: verify card `MAT-0017` (皮革 / leather) and produce a `material_macro` visual prompt, plus answer whether a real reference image/asset exists.
- Scope: read-only KB query; no project script, period/region/character brief supplied — **unknowns:** none needed for this lookup.
- Commands run exactly as given (from Vault root):
  - `python3 scripts/query.py --id MAT-0017 --json`
  - `python3 scripts/visual_prompt.py --id MAT-0017 --kind material_macro --json`

## Returned card data (query.py)
| Field | Value |
|---|---|
| id | `MAT-0017` |
| name | 皮革 / leather |
| type | material |
| path | `03-材质纹样/材料/MAT-0017-皮革.md` |
| evidence_status | `verified` |
| source_ids | `SRC-0549`, `SRC-0489`, `SRC-0538` |
| score | 0.0 |

Card frontmatter (read-only inspection) confirms: `review_status: reviewed`, `license_status: not_applicable`, `material_family: leather`, `fiber_content: [animal_hide]`, periods `15th_century / 1910s / 1970s`, regions `britain / france / europe`, `visual_prompt_profile: material_macro`.

## Prompt output (visual_prompt.py)
- `kind`: `material_macro`, `lang`: `en`, `model_agnostic`: true
- `image_generation`: **false** — `delivery`: "text prompt only"
- Evidence tags: FACT, OBSERVATION, INFERENCE, CREATIVE
- Conflicts: **0 errors / 0 warnings / 0 notices**

**Prompt (material_surface module, FACT + OBSERVATION):**
> extreme macro of leather leather focus on fiber weave sheen and surface irregularity neutral 5600K light shallow depth of field no logos

Chinese: 材质微距：leather，皮革；聚焦纤维、织法、光泽与表面不均；中性 5600K 光、浅景深、无标识。

Supporting observation string (card-derived, not new evidence): *tanned hide, soft kid leather gloves or boots, matte or polished surface, stitched seams.*

## Verified local image / asset: **NO**
From the returned data there is **no verified local image or asset**:

1. `query.py` returns only `id / path / name_zh / name_en / type / evidence_status / source_ids / snippet / score` — **no image, asset, or file-reference field**.
2. `visual_prompt.py` returns `image_generation: false`, `delivery: "text prompt only"`, and **no asset/image path** — it is a text-prompt builder, not an image tool.
3. Cross-check: `11-验收/P4-VISUAL/visual-index.csv` contains **no `MAT-0017` row** (verified via `path_guard` ALLOW, then text search).
4. The card has no image field and `license_status: not_applicable`; KB status is **0 local images / 0 downloads**.

**No image was generated. No image was downloaded or fetched. No local asset was invented or implied.** SRC-0549 / SRC-0489 / SRC-0538 are bibliographic source cards, not image files, and no image URL was returned.

## Evidence vs inference
- **FACT (card/source fields):** MAT-0017 is a verified `material` card for leather; AAT definition (SRC-0549); V&A 15th-c. London leather ankle boots (SRC-0489); 1910s French/London kid-leather evening gloves (SRC-0538).
- **OBSERVATION (card prose):** tanned hide, soft kid leather, matte or polished, stitched seams.
- **INFERENCE:** the macro staging (fiber/sheen/surface irregularity, 5600K, shallow DOF) is an interpretive visual reading — not a historical claim.
- **CREATIVE:** lighting/framing choices are art-direction only.

## Gaps / caveats
- **No reference image exists** in the returned data or the visual index, so this prompt cannot be image-matched or visually verified against a real asset.
- Card explicitly does **not** distinguish vegetable vs chrome tanning, finish, or thickness — those remain **unknown** and must not be asserted in a prompt as fact.
- Minor consistency note: the card body cites `SRC-0537` (1970s black leather loafers) but `source_ids` lists only `SRC-0549/0489/0538`; I did not treat SRC-0537 as a returned/verified source.
- Visual QA status cannot exceed `TEXT_VALID`; `DOMAIN_REVIEWED`, `IMAGE_TESTED`, and `HUMAN_VISUAL_APPROVED` are all **NOT_RUN**.
