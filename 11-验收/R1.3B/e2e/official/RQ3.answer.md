# STR-0012 → Modern Women's Blazer — CREATIVE/INFERENCE Proposal

## 1. Commands run (exact order)

### 1.1 `python3 scripts/query.py --id STR-0012 --json`

Returned one card:

| field | value |
|---|---|
| id | `STR-0012` |
| path | `02-结构细节/STR-0012-翻领与驳领.md` |
| name | 翻领与驳领 / **turndown collar and lapel** |
| type | `garment_part` |
| evidence_status | `verified` |
| source_ids | `SRC-0118` |
| part_family | `collar` |
| periods / regions | 19th–20th c. / Europe, Britain |
| aliases | turn-down collar, lapel, **notched lapel**, 翻领, 驳领 |

Card structure (verbatim meaning): a **turndown collar** is a stand + fall folding along the neckline; a **lapel** is the front edge folded outward, typed as notched / peak / shawl. They often co-occur but are different structures. Under-collar and topside may use different interlinings to control stiffness; lapel edges are often hand- or machine-stitched. The cited FIT frock-coat page (`SRC-0118`) distinguishes “flat, turned down collar and no lapels” as an early-18th-c. feature — used only to separate the two structures.

Card prompt phrase: `tailored jacket with flat turndown collar and lapels, notched lapel, front opening, crisp edge stitching, wool suiting`

Note: STR-0012's YAML has **no `materials` and no `colors`**. “wool suiting” exists only inside `prompt_en`, so it is **not** material evidence.

### 1.2 `python3 scripts/visual_prompt.py --id GAR-0033 --kind garment_worn --json`

| field | value |
|---|---|
| card | `GAR-0033` — 西式休闲西装 / **lounge suit** (`01-服装单品/外层/GAR-0033-西式休闲西装.md`) |
| evidence_status | `verified` |
| source_ids | `SRC-0204`, `SRC-0155` |
| kind | `garment_worn` |
| image_generation | **`false`** |
| delivery | `text prompt only` |
| conflicts | 0 errors / 0 warnings / 0 notices |
| silhouette / fit | `H_line` / `regular` |
| materials / colors | tweed, wool, sateen / brown, herringbone |
| structure | single-breasted jacket, wide trousers, shirt + tie, no waistcoat |

Module 1, `garment_worn.prompt_en`, verbatim:

> `lounge suit full-body neutral model front side and back natural stance face out of frame no identity silhouette H line fit regular category outerwear/suit jacket materials tweed wool sateen palette brown herringbone reference prompt 1930s lounge suit single-breasted jacket with wide trousers brown herringbone tweed generous cut worn with shirt and tie no waistcoat urban professional`

Module 2, `movement_note`, Chinese text is coherent: loose cut and wide trousers aid walking, but heavy tweed creases across the shoulder/back on arm-raise; late-1930s suits often omit the waistcoat, so waistcoat presence must be locked.

**Output defect worth flagging:** `movement_note.prompt_en` is `"movement observation ， 、 ； 1930 ， 。"` — punctuation-only CJK residue, not usable English. This matches the known R1.3 generator issue (CJK left in some prompt blocks). I have not reproduced it as a prompt.

---

## 2. Real-card evidence base

| Claim | Card | Source | Tag |
|---|---|---|---|
| Turndown collar = stand + fall; lapel = folded-out front edge; notched/peak/shawl types | `STR-0012` | `SRC-0118` (FIT frock coat) | **FACT** |
| Under-collar/topside may differ in interlining; lapel edge stitching | `STR-0012` | `SRC-0118` | **OBSERVATION** |
| H-line, regular fit, single-breasted, brown herringbone tweed, sateen lining, shirt + tie, no waistcoat | `GAR-0033` | `SRC-0204` (V&A O110441, 1940–49 British suit), `SRC-0155` (FIT 1930–1939) | **FACT** |
| Heavy tweed creases at shoulder on arm-raise; waistcoat omission must be locked | `GAR-0033` | card `movement_notes` | **OBSERVATION** |
| 1930s–40s outerwear uses padded, squared shoulders | `STR-0014` | `SRC-0412` (V&A 1942 Utility dress) | **FACT** |

Source links as listed on the cards: [SRC-0118](https://fashionhistory.fitnyc.edu/frock-coat/), [SRC-0204](https://collections.vam.ac.uk/item/O110441/), [SRC-0155](https://fashionhistory.fitnyc.edu/1930-1939/).

**Coverage gap:** `query.py "女西装"` returned **0 hits**. `"blazer"` returned only `SRC-0066` (1908 *A Dictionary of Men's Wear*), a source card, not a women's-blazer garment card. There is **no modern women's blazer card** in the KB. The proposal below is therefore a design hypothesis, not a card lookup.

---

## 3. Design proposal — clearly labelled

> **STATUS: CREATIVE / INFERENCE. Not a KB card. Not verified. Not a historical claim.**
> This transfers a verified **structural principle** (`STR-0012`) onto a **modern women's blazer**, using `GAR-0033` only for documented material/colour/fit anchors. The target garment is cross-gender (menswear card → womenswear), cross-era (1930s–40s → modern), and has no supporting women's-blazer card. Every applied dimension below is a design decision, not evidence.

### 3.1 Structure transfer

| STR-0012 element | Application to modern women's blazer | Tag |
|---|---|---|
| Turndown collar: stand + fall folding along neckline | Two-piece collar: stand ≈ 2.5 cm, fall ≈ 4 cm, folding cleanly along the neckline | structure **FACT**; dimensions **CREATIVE** |
| Lapel: front edge folded outward | Self-faced notched lapel, pressed roll to the upper button | **FACT** / **INFERENCE** |
| Notched lapel type | Moderate notch, ≈ 7.5 cm at widest; gorge seam at collarbone level | notch type **FACT**; width/gorge **CREATIVE** |
| Under-collar vs topside interlining | Firmer melton undercollar, softer topside; controlled lapel roll | **OBSERVATION**; melton choice **CREATIVE** |
| Edge stitching on lapel/collar | 2 mm pick-stitch along lapel and collar edge; clean, crisp finish | **OBSERVATION**; spacing **CREATIVE** |
| Front opening with buttons | Single-breasted, 2-button, low stance; hip-length body | buttons **FACT**; stance/length **CREATIVE** |

### 3.2 Material and silhouette anchors

- **FACT (from `GAR-0033`):** brown herringbone tweed (wool/tweed) with sateen lining; H-line; regular fit.
- **INFERENCE:** keep the H-line and regular fit so the blazer reads as modern relaxed tailoring, not 1930s generous cut.
- **CREATIVE departure:** use a **soft natural shoulder**, explicitly *not* the 1930s–40s padded square shoulder documented in `STR-0014` (`SRC-0412`). This is a deliberate modernisation, not a period claim.
- **CREATIVE styling:** `GAR-0033` documents shirt + tie, no waistcoat. For the women's blazer, reinterpret as an open-collar poplin shirt or fine silk shell, no tie, no waistcoat. The tie removal is styling, not evidence.
- **Caution:** heavy tweed in a fitted women's blazer may reproduce the card's noted shoulder/back creasing on arm-raise. A lighter suiting version would be a **new material decision**, not supported by `GAR-0033`; do not present it as the card's tweed.

---

## 4. English image prompt — text only

Module tags follow the Vault's FACT / OBSERVATION / INFERENCE / CREATIVE convention. This prompt is authored here from the two cards; it is **not** output of `visual_prompt.py` for the blazer.

```text
SUBJECT (FACT — STR-0012, GAR-0033): modern women's single-breasted blazer, hip length,
H-line, regular fit; full-body neutral model, front three-quarter and back, natural stance,
face out of frame, no identity.

STRUCTURE (FACT/OBSERVATION — STR-0012): two-piece turndown collar with stand and fall
folding along the neckline; notched lapel folded outward from the front edge; distinct
gorge seam where collar meets lapel; crisp edge stitching along collar and lapel;
firmer undercollar than the topside; front opening with buttons.
CREATIVE structure values: notch approx. 7.5 cm at widest; gorge at collarbone level;
2-button single-breasted, low stance; self-faced lapel rolled to the upper button.

MATERIAL (FACT — GAR-0033): brown herringbone tweed, wool/tweed; sateen lining.
Do not invent fiber, weave or weight beyond the card.

COLOR (OBSERVATION — GAR-0033): brown herringbone; tonal, no invented color.

LIGHT (CREATIVE): soft directional 5600K key from camera left, gentle falloff; raking
side light to reveal herringbone texture; no claim about historical lighting.

CAMERA (CREATIVE): 50 mm, f/4, eye level; full-body front three-quarter and back;
neutral orthographic clarity, no stylisation.

BACKGROUND (CREATIVE): neutral mid-grey studio; no historical set implied.

STYLE (INFERENCE): modern womenswear tailoring translation of verified menswear
structure and material; soft natural shoulder — deliberately not the 1930s–40s padded
square shoulder of STR-0014. This is a design interpretation, not a historical garment.

NEGATIVE (CREATIVE): no logos, text or brand-specific design; no invented fiber, weave,
weight, seams, closures or insignia; no extra garments or props; no period costume
styling; no claim of 1930s women's-blazer authenticity.

CONSISTENCY (OBSERVATION): preserve card IDs, brown herringbone palette, H-line
proportion, notch/gorge geometry and 2-button stance across frames.
```

Optional motion note (text only): slow 180° turn; tweed should crease naturally at the shoulder on arm-raise per `GAR-0033` movement observation; no morphing of lapel shape.

---

## 5. Evidence vs inference vs gaps

- **Facts:** `STR-0012` lapel/collar definitions and `SRC-0118`; `GAR-0033` verified material/colour/fit/source data from `SRC-0204` and `SRC-0155`; `STR-0014` padded-shoulder fact from `SRC-0412`.
- **Observation:** undercollar interlining, edge stitching, tweed side-light behaviour, arm-raise creasing.
- **Inference:** any modern women's-blazer application; cross-gender and cross-era transfer; the soft-shoulder decision; the styling change from shirt-and-tie to open-collar shirt/shell.
- **Creative:** all dimensions (notch width, gorge height, button stance, pick-stitch spacing), lighting, camera, background, negative constraints.

**Known tensions, not hidden:**
1. `GAR-0033` YAML says `periods: [1940s]`, while its prompt/aliases say 1930s; the card body states the V&A object is 1940–49 British and the 1930s attribution is contextual. Do not present it as a 1930s-made garment.
2. `STR-0012` has no materials/colors; “wool suiting” is prompt text only.
3. No women's-blazer card exists; `query.py "女西装"` returned zero.
4. `visual_prompt.py` `movement_note.prompt_en` contains CJK punctuation residue.
5. Prompt QA (`prompt_qa.py`) was **not** run on this new blazer text; `TEXT_VALID`, `DOMAIN_REVIEWED`, `IMAGE_TESTED`, and `HUMAN_VISUAL_APPROVED` are all **not claimed**.

**No image was generated.** Both commands are text-only; `visual_prompt.py` reported `image_generation: false` and `delivery: "text prompt only"`. No files were written and no knowledge-base card was modified.
