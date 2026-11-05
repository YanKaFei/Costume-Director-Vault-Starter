## Brief
- Two style cards, both `type: style`, `evidence_status: interpretive`, `review_status: draft`, `periods: ["2025","2026"]`, `regions: [global]`, `license_status: not_applicable`.
- Both are 2025–26 runway trend observations, explicitly **not** historical costume facts; both source pages are Vogue Runway `link_only` and images were not individually verified.
- Query `score: 0.0` on both is an ID-lookup artifact, not a relevance ranking.

## IDs returned

| Query | ID | Name | Path |
|---|---|---|---|
| 1 | **STY-0024** | 现代极简精炼工装 / modern minimal refined utility | `05-风格体系/STY-0024-现代极简精炼工装.md` |
| 2 | **STY-0025** | 当代解构 / contemporary deconstruction | `05-风格体系/STY-0025-当代解构.md` |

Both `source_ids` exist and are cited as: STY-0024 → `SRC-0553`, `SRC-0554`; STY-0025 → `SRC-0554`, `SRC-0557`.

## Differences

| Dimension | STY-0024 modern minimal refined utility | STY-0025 contemporary deconstruction |
|---|---|---|
| Core idea | Compresses utility's storage/abrasion function into clean lines and precise proportion: fewer pockets, hidden storage, low contrast | Names 2025–26 runway methods: exposed seams, displaced panels, raw edges, inside/outside structure flipped |
| Structural signature | Clean-lined utility jacket, straight/slightly relaxed, clear shoulder, pockets de-emphasized | Asymmetric panelled construction, shifted panels, asymmetric placket, half-finished edges; width may be wide or narrow — structure is the identifier |
| Palette/material (body text, marked INFERENCE, not fact) | Stiff cotton / nylon blend / light wool; black, grey, bone, low-saturation khaki | Cotton / wool / silk juxtaposed with crisp interlining; black, white, grey, desaturated |
| What it is NOT | Not historical workwear or military dress study | Not a 1990s deconstructionist revival |
| Intended character use | Contemporary workplace / urban action role needing "functional but not heavy" | Contemporary stage / editorial / conceptual role needing unfinished, structure-exposed tension |
| Not applicable when | Historical workwear/military accuracy is required; using a trend word in place of actual structure | Historical precision is required; treating deconstruction as 1990s fact; copying a brand's distinctive cut |
| Visual reading | Look for hidden storage, clean front panel, precise shoulder, monochrome proportion | Look for displacement, exposed seams, asymmetry — not just holes or black |
| `prompt_en` | `contemporary modern minimal refined utility, clean-lined utility jacket, hidden pockets, precise shoulder, monochrome neutral palette, editorial studio, no logos` | `contemporary deconstruction, exposed seams, asymmetric panelled construction, raw edges, monochrome palette, editorial studio, no logos` |
| Sources | `SRC-0553` (Fall 2025 RTW), `SRC-0554` (Spring 2026 RTW) | `SRC-0554` (Spring 2026 RTW, shared), `SRC-0557` (Spring 2026 Couture) |

**Shared:** same category/subcategory (`art_movement` / `contemporary_runway_trend`), same empty frontmatter `colors: []` and `materials: []` (all color/material content is body-level INFERENCE), same `REFERENCE_PENDING` visual status with no downloaded or embedded image, and the same related cards (`STY-0008`, `STY-0019`, `STY-0023`).

**Data-quality flag (reported, not fixed):** STY-0025's `查重说明` (line 41) contains copy-pasted text from STY-0024 — it says "本卡聚焦极简/精炼/隐藏收纳" and compares itself to STY-0019, which contradicts its own deconstruction definition. It also carries a second, correct sentence distinguishing it from STY-0008's deconstruction tag. Since this is a draft KB card and the KB is read-only for this workflow, this is a maintainer/verification task, not something I will silently edit.

## Image-generation refusal

**I will not and cannot generate an image.** There is no image tool in this environment, no network image fetch, and no install path; producing or claiming a rendered image, a film still, or a "tested" visual would be fabrication. This applies to any request to render these looks or attach generated visuals. The only deliverable is **text** — prompts as plain text, model-agnostic, with `image_generation: false`.

## Text prompts only (verbatim card content, no rendering)

**STY-0024**
```text
SUBJECT (INFERENCE): contemporary runway reference board for STY-0024; no specific designer/brand copied.
STRUCTURE (INFERENCE): clean-lined utility jacket silhouette, straight/relaxed shoulder, hidden pockets, precise proportions
MATERIAL (INFERENCE): durable cotton/nylon blend, light wool; black/grey/bone/low-saturation khaki (design hypothesis only, not material fact)
COLOR (INFERENCE): palette hypothesis only; do not treat as source-verified color of a specific garment.
LIGHT (CREATIVE): soft editorial key, low-to-medium contrast, gentle falloff.
CAMERA (CREATIVE): 35–50mm editorial framing, eye level, full-body or 3/4.
BACKGROUND (CREATIVE): neutral studio or restrained contemporary interior; no historical set implied.
STYLE (INFERENCE): modern minimal refined utility; 2025–26 trend language, not historical fact.
NEGATIVE (CREATIVE): no brand logos, no copied distinctive designs, no invented material properties, no extra accessories, no costume morphing, no fake historical detail.
CONSISTENCY (OBSERVATION): keep silhouette family, palette, layering and proportion identical across frames.
```

**STY-0025**
```text
SUBJECT (INFERENCE): contemporary runway reference board for STY-0025; no specific designer/brand copied.
STRUCTURE (INFERENCE): asymmetric panelled silhouette, shifted panels, exposed seams, unfinished edges, layered inside/outside construction
MATERIAL (INFERENCE): cotton/wool/silk with crisp interlining; black/white/grey/desaturated palette (design hypothesis only, not material fact)
COLOR (INFERENCE): palette hypothesis only; do not treat as source-verified color of a specific garment.
LIGHT (CREATIVE): soft editorial key, low-to-medium contrast, gentle falloff.
CAMERA (CREATIVE): 35–50mm editorial framing, eye level, full-body or 3/4.
BACKGROUND (CREATIVE): neutral studio or restrained contemporary interior; no historical set implied.
STYLE (INFERENCE): contemporary deconstruction; 2025–26 trend language, not historical fact.
NEGATIVE (CREATIVE): no brand logos, no copied distinctive designs, no invented material properties, no extra accessories, no costume morphing, no fake historical detail.
CONSISTENCY (OBSERVATION): keep silhouette family, palette, layering and proportion identical across frames.
```

Both prompt blocks are tagged FACT/OBSERVATION/INFERENCE/CREATIVE as shown; material and color lines are hypotheses, not verified facts, and neither block should be read as historical accuracy or as visual approval.
