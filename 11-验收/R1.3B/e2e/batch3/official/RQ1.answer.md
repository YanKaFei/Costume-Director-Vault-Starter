## Scope and commands run

| Step | Command | Result |
|---|---|---|
| 1 | `python3 scripts/query.py --id STR-0028 --json` | 1 hit, exact-ID lookup (`score 0.0` = exact match, not low relevance) |
| 2 | `python3 scripts/query.py --id STR-0003 --json` | 1 hit, exact-ID lookup |
| 3 | `python3 scripts/visual_prompt.py --id STR-0028 --kind component_detail --json` | `image_generation: false`, `delivery: "text prompt only"`, `conflicts: []` |

## The two cards

| Field | STR-0028 | STR-0003 |
|---|---|---|
| Name | 青果领/披肩领 — **shawl collar** | 拉夫领 — **ruff** |
| Type | `garment_part`, `part_family: collar` | `garment_part`, `part_family: collar` |
| Path | `02-结构细节/STR-0028-青果领-披肩领.md` | `02-结构细节/STR-0003-拉夫领.md` |
| Evidence / review | `verified` / `reviewed` | `verified` / `reviewed` |
| Periods | 1940s, 2000s | 1560s–1600s (16th–17th c.) |
| Regions | france, belgium | europe, england |
| Materials | velvet, linen | linen, lawn, lace |
| Colors | none recorded | white, yellow, blue, green |
| Sources | SRC-0532, SRC-0539 | SRC-0133 |
| Visual reference status | `SOURCE_LINK_ONLY`, no asset | `SOURCE_LINK_ONLY`, no asset |

## Differences that matter for design

1. **Era and function.** STR-0028 is a *flat, continuous rolled lapel*: the collar and front edge run as one unbroken curve with **no notch**, usually with a front facing/placket. Evidence spans a 1944 stage/evening jacket and a 2002 designer jacket. STR-0003 is a *detachable, three-dimensional wheel collar*: circular, stiffened with starch and wire, pleated into figure-eight folds, tied at the neck, sometimes open at the chin for women. It is a period marker, not modern daywear.
2. **Construction logic.** Shawl collar = tailoring: pressed roll, break line, facing, undercollar. Ruff = textile manipulation: fine linen/lawn, starch + heat setting, setting sticks, wire support, 18–19 yards of cloth at 1580s extremes.
3. **Silhouette effect.** Shawl collar frames the face and closes the chest vertically; ruff displaces the head upward and outward as a horizontal disc — a completely different proportion and movement profile.
4. **Interchangeability.** None. The STR-0028 card explicitly warns not to confuse it with notched/peak lapel (STR-0012) and not to add satin automatically. The STR-0003 card rules out post-mid-17th century (falling band), everyday labour, and modern use.
5. **Evidence depth.** STR-0028 has two object-level museum records with quoted `physicalDescription`. STR-0003 rests on one **secondary academic compilation** (FIT Fashion History Timeline), which the source card itself says cannot support a specific surviving object or screen use. STR-0003 also carries an interpretive `uses_material` link to MAT-0016 at `medium` confidence with `review_status: review_queue` — the linen/lawn/lace fibre claim is therefore not independently object-verified.

## Evidence and provenance

- **SRC-0532** — V&A object `O102166`, *Jacket, The Great Masoni, ca. 1944*, black velvet; museum text: “Black velvet evening jacket with shawl collar, front facings, pocket flaps and cuffs of scarlet satin.” https://collections.vam.ac.uk/item/O102166/ — `link_only`, © V&A.
- **SRC-0539** — V&A object `O1242729`, Dries van Noten, 2002, green linen with embroidery; museum text: “Jacket, of green linen, with pink red and black embroidery and shawl collar.” https://collections.vam.ac.uk/item/O1242729/ — `link_only`, © V&A.
- **SRC-0133** — FIT Fashion History Timeline, “ruff”. https://fashionhistory.fitnyc.edu/ruff/ — `link_only`, © FIT/SUNY; secondary compilation, original page citations still need checking.
- Coverage file `reports/R1.3-VISUAL-COVERAGE.csv` lists both as `visual_layer=True`, `reference_status=SOURCE_LINK_ONLY`, `asset_ids` empty, `prompt_blocks=2`, `text_status=TEXT_VALID`.

## STR-0028 component-detail prompt (verbatim from the builder)

| Module | Prompt (EN) | Tag | Source |
|---|---|---|---|
| `structure_detail` | “detail of shawl collar on garment part construction seams closures edge finish and hardware orthographic clarity no stylisation” | FACT, OBSERVATION | card type + structured fields |
| `construction_note` | “construction note from card prompt shawl collar jacket continuous rolled collar no notch front facing period or modern tailoring” | INFERENCE | `prompt_en` |

Builder metadata: `evidence_status: verified`, `source_ids: [SRC-0532, SRC-0539]`, `model_agnostic: true`, `conflicts: []` (0 errors / 0 warnings / 0 notices), `generated_at: 2026-11-05T17:54:44+0800`. Tag vocabulary returned includes CREATIVE, whose declared scope is “staging and art-direction choices; not a historical claim.” **No image was generated.**

## Reference images: none exist for either collar

- Both cards state: “无已核验匹配 ASSET；当前仅来源链接/专业描述，待后续逐图匹配.”
- `11-验收/P4-VISUAL/visual-index.csv` contains 28 link-only rows and **no row for STR-0028 or STR-0003**.
- `reports/R1.3-VISUAL-COVERAGE.csv` gives both `SOURCE_LINK_ONLY` with empty `asset_ids`.
- The three source cards are `license_status: link_only`; SRC-0532/SRC-0539 say images were not downloaded or embedded, and SRC-0133 states that any page images have separate rights and only the URL is retained.

So the honest status is **no real, verified reference image in the Vault** for either card — only citable museum/encyclopaedia page links. A V&A object page is not a licensed asset, and I did not verify or fetch an image URL; do not present one as a reference image.

## Caveats before using the prompt

- The `MATERIAL (FACT): velvet, linen` line merges **two different objects** (1944 velvet jacket and 2002 linen jacket) into one frame. That can yield a hybrid that matches neither artifact; pick one object per render.
- The generic `component_detail` template asks for “closures and hardware,” which is meaningful for a jacket collar but a poor fit if reused for STR-0003 (a ruff has ties and wire, not hardware).
- QA ladder stops at `TEXT_VALID`; `DOMAIN_REVIEWED`, `IMAGE_TESTED`, and `HUMAN_VISUAL_APPROVED` are all **NOT_RUN**.
