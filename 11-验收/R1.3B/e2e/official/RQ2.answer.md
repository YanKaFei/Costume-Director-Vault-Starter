## Card identity

Commands run exactly as specified:

- `python3 scripts/query.py --id STR-0029 --json` → **1 hit**, `score: 0.0`
- `python3 scripts/visual_prompt.py --id STR-0029 --kind component_detail --json` → `image_generation: false`, `delivery: "text prompt only"`

| Field | Value |
|---|---|
| ID | **STR-0029** |
| Name | **泡泡袖 / puff sleeve** |
| Type | `garment_part` / `sleeve`; `part_family: sleeve` |
| Path | `02-结构细节/STR-0029-泡泡袖.md` |
| Evidence | **verified**; `review_status: reviewed`; `license_status: not_applicable` |
| Period / region | **1820s** / **britain** |
| Material field | **muslin** |
| Source | **SRC-0533** → V&A object **O353415**, white muslin dress, England c.1825–30, <https://collections.vam.ac.uk/item/O353415/> |
| Palette | `colors: []` — no colour asserted |

“Stage sleeve” here resolves to the sleeve construction type **STR-0029 泡泡袖**, not a separate stage-sleeve garment ID.

## Structure

Fresh `component_detail` output, module `structure_detail` — evidence tags **FACT, OBSERVATION**:

```text
detail of puff sleeve on garment part; construction seams, closures, edge finish and hardware; orthographic clarity, no stylisation
```

Chinese module:

```text
结构细节：泡泡袖；缝线、闭合、边缘处理与五金；正交清晰、不风格化
```

Second fresh module, `construction_note` — evidence tag **INFERENCE**:

```text
construction note from card prompt long puffed and pleated sleeves on a high-waisted muslin dress gathered sleeve head period 1820s
```

Card structure facts from **STR-0029**:

- Volume is formed at the sleeve head/body by gathers, pleats, or padding; the cuff narrows (`structural_notes`).
- **SRC-0533 / V&A O353415** records: white muslin dress, high round neckline, **long puffed and pleated sleeves**, high waistline, back fastening.
- Distinguish from **STR-0004 / STR-0005** 羊腿袖 (gigot): gigot has extreme upper-arm volume with a tight forearm; a puff sleeve can puff at the sleeve head or the whole sleeve, so volume and position vary.
- Thin fabric puffs more easily; a large puff in stiff, heavy fabric without support is listed as unsuitable (`interpretive`).
- Visual identification: gathered sleeve head, upper-arm volume, narrowed cuff, long sleeve, natural shoulder line, high waist, visible gather lines in close-up.

## Material

- `materials: [muslin]` — **FACT**, card YAML for **STR-0029**.
- Card-stored prompt line: `MATERIAL (FACT): muslin.`
- Related material card: **MAT-0001 平纹细布**, via `uses_material`. The relation records `evidence=verified` but **`confidence=medium`** and rule `R-MAT-TOKEN`; the card itself labels it a “medium material token relation (design/review; **not historical fact**)”. Do not upgrade it to independent historical proof.
- No colour is given: `COLOR (OBSERVATION): neutral; do not invent color.`
- Important generator gap: the fresh `component_detail` JSON emitted only `structure_detail` and `construction_note` — it did **not** emit a material, colour, light, or camera module. The material assertion comes from the verified card fields and the card’s stored prompt block, not from a fresh material module.

## Front prompt

The fresh `component_detail` run has **no standalone front-view module**; its structure prompt is an orthographic detail prompt. The card’s stored 生图提示词 supplies the front/side framing — `CAMERA (CREATIVE): 85mm detail, f/5.6, orthogonal front/side.`

Exact card-stored prompt block for the front/side plate:

```text
SUBJECT (FACT): detail of puff sleeve on garment part construction seams closures edge finish and hardware orthographic clarity no stylisation.
STRUCTURE (OBSERVATION): construction note from card prompt long puffed and pleated sleeves on a high-waisted muslin dress gathered sleeve head period 1820s
MATERIAL (FACT): muslin.
COLOR (OBSERVATION): neutral; do not invent color.
LIGHT (CREATIVE): neutral 5600K studio light with soft directional falloff; no claim about historical lighting.
CAMERA (CREATIVE): 85mm detail, f/5.6, orthogonal front/side.
BACKGROUND (CREATIVE): neutral mid-grey studio; no historical set implied.
STYLE (INFERENCE): professional reference plate; art direction only.
NEGATIVE (CREATIVE): no invented fiber, weave, weight, transparency, seams or closures; no logos, text or brand-specific design; no extra objects.
CONSISTENCY (OBSERVATION): preserve card ID, material tokens, palette and proportions across frames.
```

This is a **front/side** plate, not a strict front-only plate. A front-only variant would be a **CREATIVE** camera edit, not a historical or card fact. The 5600K light, 85mm/f/5.6, mid-grey background, and orthographic framing are staging choices — not claims about 1820s lighting or photography.

## Evidence ledger

| Claim | Tag | Real evidence |
|---|---|---|
| STR-0029 is a puff sleeve, `garment_part/sleeve` | FACT | **STR-0029** YAML; query hit |
| Period 1820s, region Britain | FACT | **STR-0029** YAML `periods` / `regions` |
| Sleeve head/body gathers, pleats or padding; narrowed cuff | FACT | **STR-0029** `structural_notes` |
| V&A O353415 is a white muslin dress with long puffed and pleated sleeves, high waist, back fastening | FACT | **SRC-0533** |
| Material is muslin | FACT | **STR-0029** `materials`; **SRC-0533** |
| Puff sleeve differs from gigot | OBSERVATION / card comparison | **STR-0029**; related **STR-0004**, **STR-0005** |
| Thin fabric puffs more easily; volume via gathers/pleats/lining | INFERENCE | **STR-0029** body, explicitly marked `interpretive`; fresh `construction_note` is tagged INFERENCE |
| Front/side 85mm f/5.6 plate, 5600K, mid-grey background | CREATIVE | **STR-0029** card 生图提示词 |
| MAT-0001 material-token relation | Relation evidence verified, **confidence medium**; design/review, not historical fact | **MAT-0001** relation in **STR-0029** |

Related IDs present on the card but not used as independent evidence: **STR-0013** (set-in/raglan sleeve), **GAR-0015** (法式长袍).

## Conflicts, gaps and tag caveats

- Fresh generator `conflict_summary`: **0 errors, 0 warnings, 0 notices**.
- **Tag mismatch:** the card block labels the construction note `STRUCTURE (OBSERVATION)`, while the fresh `construction_note` module — derived from the same `prompt_en` — is tagged **INFERENCE**. The conservative reading is INFERENCE; do not treat the card label as stronger evidence.
- In the fresh JSON, `observation` and `inference` are **verbatim identical** (`"long puffed and pleated sleeves..."`), so they are not independent corroboration.
- Only one cited source: **SRC-0533**. No second independent source is present.
- The card’s 视觉参考 section says there is **no verified matching ASSET** — only the source link/professional description.
- Alias risk: `aliases` includes `gigot` / `羊腿袖`; the card explicitly warns not to conflate **STR-0029** with **STR-0004/STR-0005**.
- The `component_detail` builder omitted material/colour/light/camera modules; therefore the material line and front camera line come from the verified card/stored prompt, not from freshly generated modules.

## No image generated

**No image was generated.** The builder returned `"image_generation": false` and `"delivery": "text prompt only"`; no image model/tool was invoked, no image was downloaded, and no local image file was created. This report is text and card evidence only.
