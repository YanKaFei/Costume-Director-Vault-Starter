## Command result

`python3 scripts/visual_prompt.py --id LOOK-0001 --kind outfit --json` ran from the Vault root and exited **0**.

- Card: **LOOK-0001** 洛可可沙龙女主人 / rococo salon hostess look (`09-造型组合/LOOK-0001-洛可可沙龙女主人.md`)
- Kind: `outfit` · lang `en` · `model_agnostic: true`
- **`image_generation: false`** · delivery: `text prompt only`

## Material / item / accessory IDs

`look_items` has exactly 6 entries: `GAR-0015, STR-0009, STR-0006, GAR-0028, GAR-0024, MAT-0002`.

| Role | ID | Name | Card type | Evidence | Source |
|---|---|---|---|---|---|
| Main garment | **GAR-0015** | 法式长袍 / robe à la française | garment | verified | SRC-0116 |
| Structure | **STR-0009** | 裙侧撑 / panniers | garment_part | verified | SRC-0139 |
| Structure | **STR-0006** | 胸衣插片 / stomacher | garment_part | verified | SRC-0136, SRC-0064 |
| Accessory | **GAR-0028** | 手笼 / muff | garment (配饰) | verified | SRC-0129 |
| Footwear | **GAR-0024** | 穆勒鞋 / mule | garment (足部) | verified | SRC-0125 |
| Material | **MAT-0002** | 尚蒂伊蕾丝 / Chantilly lace | material | verified | SRC-0141 |

Look-level source: **SRC-0150** — FIT 1770–1779 decade overview, <https://fashionhistory.fitnyc.edu/1770-1779/>.

## Style basis

- **STY-0010** 时代剧历史考据造型 / period drama historical costume — **verified**, sources **SRC-0167, SRC-0168, SRC-0169**.
- Style tags: `STY-0010`, `rococo`, `court_dress`
- Period/region: `1770s`, `18th_century` / `france`
- Palette: `cream`, `pastel`, `gold`; materials: `silk`, `brocade`, `lace`
- `look_role`: 1770s French salon hostess (fictional character, **historical mode**)
- Method basis: verified individual cards + an **interpretive** combination; the look does not reproduce a surviving ensemble.
- Prompt profile: `outfit_character_scene`; `visual_prompt_type: [character_scene, detail, video]`.

## Evidence

Builder evidence tags: **FACT, OBSERVATION, INFERENCE, CREATIVE**; card `evidence_status: interpretive`, `review_status: draft`.

- **FACT** — card IDs, `look_items` count = 6, palette (`cream pastel gold`), materials (`silk, brocade, lace`), period/region/style tags, continuity-lock text.
- **OBSERVATION** — silhouette/visual prose: skirt widened sideways, relatively flat front-to-back; rear box pleats shoulder-to-floor; decorated triangular stomacher; Chantilly lace at neckline/cuffs; fur muff and silk mule sheen under candlelight; continuity locks on pannier width, pleat fall, stomacher shape, muff/shoe colour, headpiece height.
- **INFERENCE** — assembling these verified parts into one complete salon-hostess look, and reading the result through STY-0010, is design interpretation, **not a historical claim**.
- **CREATIVE** — candlelit interior staging, light/camera framing, and the negative prompt.

**Conflict check:** `0 errors / 0 warnings / 1 notice` — `low_confidence`: `evidence_status=interpretive; not verified`. The GAR-0015→LOOK-0001 relation is `interpretive / medium / review_queue / design_only=true`, so it is not factual evidence. SRC-0150 supports the 1770s robe à la française/panniers context, not this exact assembled outfit.

## Prompt

Primary module **`outfit_hero`** (verbatim `prompt_en`):

```text
complete outfit rococo salon hostess look items GAR-0015 STR-0009 STR-0006 GAR-0028 GAR-0024 MAT-0002 palette cream pastel gold reference prompt 1770s French salon hostess robe à la française in cream silk brocade panniers widening the skirt sideways decorated stomacher Chantilly lace trim fur muff silk mule slippers candlelit interior historical mode
```

**`continuity`** (`prompt_en`, verbatim):

```text
continuity locks recorded in card preserve slot state
```

The concrete lock text lives on the card (and in the module's `prompt_zh`): pannier width fixed within a scene; rear pleat fall, stomacher exposure, muff and shoe colours held consistent; headpiece height must not change between shots.

**`negative`** (`prompt_en`, verbatim):

```text
negative no modern shoes no machine lace no zippers or visible elastic no anachronistic jewelry no changed pannier width between shots no symmetrical wide skirt front
```

The JSON also contains Chinese variants (`prompt_zh`); the English variants above are the primary `lang=en` output.

## Gaps / limitations

- The look is **interpretive/draft**, not verified; the single builder notice reflects that.
- Card coverage gap: no 18th-century women's headwear/wig card and no stays card — headwear must not be invented; the prompt omits it rather than guessing.
- MAT-0002 is bobbin lace, often black silk, while the look palette is cream/pastel/gold; the prompt names "Chantilly lace trim" without assigning a lace colour. This is an unstated design choice, not a builder-flagged conflict.
- Observation and inference fields repeat the same card phrase; evidence layering is carried by the module tags, not by distinct prose.
- No registered ASSET on the card; only SRC-0150 as a textual reference, no downloaded or embedded image.

**No image generation is claimed.** The output is a text prompt only; no image/video was generated, no image test was run, and no visual approval (`IMAGE_TESTED` / `HUMAN_VISUAL_APPROVED`) is asserted.
