## Brief

- **Look:** `LOOK-0008` — 1930 年代上海长衫知识分子 / 1930s Shanghai changshan intellectual look.
- **Role:** 1930 年代上海/香港知识分子（虚构角色，historical 模式）.
- **Period/region:** 1930s, republican era; China/Shanghai (production setting).
- **Scene:** `SCN-0004` 1930 年代上海知识分子对话 — interpretive, draft; venue, story day and weather are `unknown`.
- **Evidence status:** look is **interpretive**, `review_status: draft`; all three component cards are **verified**, `review_status: reviewed`.
- **Trace result:** `relation_trace.py` returned three character looks: `LOOK-0008`, `LOOK-0009` (female qipao intellectual), `LOOK-0035` (rainy-night male reporter). This report covers `LOOK-0008` as requested.
- **Query result:** `query.py --id LOOK-0008 --json` returned one record with a snippet only (`score 0.0`); the full card was then read through `path_guard.py` (`ALLOW`).
- **Vault root for all paths below:** `/Users/coffee/Desktop/Costume-Director-Vault-Starter`

## Outfit IDs and real paths

`LOOK-0008` has exactly **three** linked item IDs. The prompt also names trousers and leather shoes, but those have **no GAR cards** — see Gaps.

| Slot | ID | Name | Real path | Card evidence | SRC |
|---|---|---|---|---|---|
| Main robe | `GAR-0032` | 长衫 / changshan | `01-服装单品/连身/GAR-0032-长衫.md` | verified / reviewed | `SRC-0202` |
| Inner layer | `GAR-0034` | 针织背心 / knitted vest | `01-服装单品/上装/GAR-0034-针织背心.md` | verified / reviewed | `SRC-0203` |
| Closure | `STR-0011` | 盘扣 / frog closure | `02-结构细节/STR-0011-盘扣.md` | verified / reviewed | `SRC-0200`, `SRC-0202` |

Look card path: `09-造型组合/LOOK-0008-1930年代上海长衫知识分子.md`
Look source IDs: `SRC-0202`, `SRC-0203`
Look scenes: `SCN-0004`
Look palette: `cream_white`, `grey`
Look materials: `gauze_silk`, `wool`

**Named in the prompt but ID-less (coverage gap):** inner short jacket/undershirt (短上衣), trousers (长裤), leather shoes. The card itself says the inner short jacket and trousers have no GAR cards, and that the Vault has no 1930s Republican-era shoe card. Do not assign invented IDs to these.

## SRC and evidence

| SRC | Real path | URL | Evidence | License | What it supports | What it cannot support |
|---|---|---|---|---|---|---|
| `SRC-0202` | `04-来源/SRC-0202-V&A-1930年代长衫.md` | [V&A O80590](https://collections.vam.ac.uk/item/O80590/) | verified / reviewed | `link_only` | 1930s Hong Kong men’s changshan: cream-white figured gauze silk (luo), small stand collar, right-side five loop-and-knot buttons, long tight sleeves, straight cuffs, side slits, inner pocket, unlined; worn over short jacket and trousers; shoulder width 149 cm, total length 133 cm (museum measurement, 2020); bamboo motif associated with scholars/urban elite | Shanghai-specific wearing practice; that all Republican-era men wore changshan |
| `SRC-0203` | `04-来源/SRC-0203-V&A-1930年代男式针织背心.md` | [V&A O235319](https://collections.vam.ac.uk/item/O235319/) | verified / reviewed | `link_only` | 1930s English men’s wool jersey-knit vest, Meridian brand: sleeveless, V-neck, ribbed hem; chest 78 cm, waist 76 cm, back neck-to-hem 70 cm, back width 40 cm | Wearing in Shanghai/China; a fixed pairing with changshan or suit |
| `SRC-0200` | `04-来源/SRC-0200-V&A-上海新新公司旗袍1930.md` | [V&A O1151302](https://collections.vam.ac.uk/item/O1151302/) — URL as linked from `STR-0011` | verified (per query) | `link_only` (per linked conventions) | Shanghai Sun Sun Company qipao, ca. 1930; supports frog-closure construction/count on a qipao (ten, four at collar) | Not cited by `LOOK-0008`; it is a qipao source, not direct evidence for five closures on this changshan |

**Evidence layering**

- **Card-verified:** the three item IDs, their paths, their existence, `GAR-0032` construction/measurements, `GAR-0034` construction/measurements, `STR-0011` loop-and-knot construction and five-closure changshan count, V&A URLs and 2026-11-04 access date.
- **Interpretive:** the assembly of these three items into a complete intellectual look; wearing a knitted vest under a changshan; the “traditional/poor” side of the class contrast; Shanghai-local use; the grey vest colour.
- **Draft:** `LOOK-0008` itself is `review_status: draft` — it is a design sample, not a production-verified costume.
- **Design-edge caveat:** `GAR-0032`’s relation to `STR-0011` is recorded as `evidence=interpretive`, `factual=false`, `design_only=true`. The five-closure count is verified by `SRC-0202`; the specific garment-to-closure link is a design relation.

## Construction, colour, material

- **`GAR-0032` 长衫:** straight silhouette, relaxed fit, formal, all-season. Cream-white figured gauze silk (luo), small stand collar, right-side fastening with **five** paired loop-and-knot buttons, long tight sleeves, straight cuffs, side slits, inner chest pocket, unlined. Museum object: shoulder width 149 cm, total length 133 cm, chest 96 cm, waist 98 cm. These are object measurements, **not** actor measurements.
- **`GAR-0034` 针织背心:** straight/slim, casual, all-season. Wool jersey knit, sleeveless, V-neck, ribbed hem. Worn as a warming layer under the robe, with a narrow V-neck band visible at the collar. The card has **no colour value** (`colors: []`); the look supplies `grey`, and the card text suggests grey/beige as readable options.
- **`STR-0011` 盘扣:** paired loop-and-knot buttons of folded silk/cotton cord along the right front; five on this changshan; collar area is the densest. Must read as actual cord loops and knots in close-up, not moulded plastic snaps or machine faux frogs.
- **Layer logic:** `SRC-0202` describes the changshan as a formal outer robe worn over a short jacket and trousers. The vest is an added warm layer; that layering is interpretive, not documented.

## Continuity limits

**Card `continuity_lock` (verbatim):**

> 长衫立领高度、右衽五枚盘扣的位置与开合状态、袖长与直袖口、侧衩长度固定；针织背心领口露出宽度一致；提摆/放摆状态在上下楼梯镜头间必须一致

**Locked across shots**

1. Stand-collar height — no change between takes.
2. Right-front **five** frog closures — exact count, position and open/closed state. A collar close-up and a medium shot must agree.
3. Sleeve length and straight cuff — long, tight, straight; no rolled or pushed-up sleeves.
4. Side-slit length — fixed; slit opening changes only through movement, not alteration.
5. Knitted vest neckline exposure — same narrow band width at the collar in every shot.
6. Hem lift/drop state — if a stair shot is added, the front hem must be lifted on the same step and lowered at the same point across cuts.

**Item-level movement limits**

- `GAR-0032`: side slits allow a stride but restrict large steps/running; long tight sleeves restrict wrist action; the long hem requires lifting on stairs; cream-white clips under strong light; the sheer gauze shows its weave in backlight.
- `GAR-0034`: knit stretches and the hem/armhole rides up when the arms lift; lock garment length and neckline position between takes; dark knit loses detail in low light, so light grey/beige reads better.
- `STR-0011`: close-ups expose fake closures; use functional paired loop-and-knot construction.

**What continuity cannot cover**

- No wetness / damage / dirt state chain exists for this look; `LOOK-0008` is an indoor `SCN-0004` look. Do not assume “clean and dry” for a rain scene — that would be a different look (`LOOK-0035`).
- No early-1930s vs late-1930s menswear version split is defined here; there is only one version.
- No actor fitting, no budget, no fabric-source or making constraints.
- Retrieval limits from `relation_trace.py`: `max_depth: 3`, low-confidence edges filtered, design edges included but marked `factual=false`; results may therefore omit deeper or lower-confidence relations.

## English image prompt

**Card `prompt_en` (verbatim, historical mode):**

```text
1930s Shanghai intellectual, cream-white gauze-silk changshan with small stand collar and five silk frog closures, long tight sleeves, side slits, worn over a muted knitted wool vest and trousers, leather shoes, historical mode
```

**Card `negative_prompt_en` (verbatim):**

```text
no modern slim-fit suit, no printed T-shirt, no sneakers, no zippers on the robe, no changed frog closure count, no anachronistic accessories
```

**Inspired variant on the card (verbatim; not historical accuracy):**

```text
inspired 1930s Shanghai scholar, ivory long robe with subtle bamboo damask, high collar, frog closures, layered knit vest, cinematic warm lantern light, lightly stylized fabric sheen
```

The inspired variant changes fabric sheen and lighting only; collar shape, robe cut and closure count stay unchanged.

## English video prompt

`LOOK-0008` stores **no video prompt field**. The following is derived from `prompt_en`, `continuity_lock`, `GAR-0032`/`GAR-0034` movement notes, and `SCN-0004` actions — label it as a design draft, not card-verbatim.

```text
1930s Shanghai, interior study or newspaper office (venue not fixed), historical mode. A slim intellectual in a cream-white figured gauze-silk changshan (GAR-0032) with a small stand collar, right-side fastening of exactly five silk frog closures (STR-0011), long tight sleeves, straight cuffs, side slits, unlined, worn over a muted grey wool V-neck jersey-knit vest (GAR-0034) whose narrow ribbed V-neck band shows at the collar, trousers and leather shoes. He sits reading a newspaper, looks up to argue, hands over a tea cup, then rises to take a book from a shelf; the rise lifts the front hem and opens the side slits, then the hem settles. Slow lateral tracking medium shot, then static medium-close, then a collar-and-hands insert. Warm desk lamp plus cool window side light; the gauze weave reads in backlight but the cream-white never clips. Locks: collar height, the five closures and their open/closed state, sleeve length, straight cuff, side-slit length, vest neckline exposure, hem state. No fast movement, no running, no modern slim suit, no printed T-shirt, no sneakers, no zipper on the robe, no changed closure count.
```

If a stair shot is added, keep the card’s stair rule: lift the front hem on the same step going up/down and lower it at the same point in every take.

## Evidence vs inference

- **Facts (card/meta):** the look’s fictional intellectual role, historical mode, `SCN-0004` setting, item IDs/paths, `GAR-0032` and `GAR-0034` construction and museum measurements, five closures on the changshan, V&A URLs, `interpretive`/`draft` look status.
- **Evidence (IDs + SRC):** `GAR-0032` ← `SRC-0202`; `GAR-0034` ← `SRC-0203`; `STR-0011` ← `SRC-0200` + `SRC-0202`; look itself ← `SRC-0202` + `SRC-0203`.
- **Inference:** combining robe + vest + frog closures into one outfit; the “traditional vs Westernised” class contrast; wearing this in Shanghai; grey vest; trousers and leather shoes named in the prompt; the scholar reading/debating action.
- **Conflicts / cautions:**
  1. The prompt names **trousers and leather shoes** but no GAR cards exist, and the look card’s own “不适用条件” says **do not shoot full body without a shoe card**. Either restrict to medium/close shots or add a verified shoe card.
  2. `GAR-0034` is documented as **England**, not Shanghai; the Shanghai layering is interpretive.
  3. `GAR-0032` is documented as **Hong Kong**; Shanghai wearing is not supported by `SRC-0202`.
  4. `STR-0011` cites `SRC-0200` (a qipao with ten closures); the direct evidence for **five** closures on a changshan is `SRC-0202`.
  5. `LOOK-0008` lists `grey`, but `GAR-0034` has no colour metadata.
  6. The 149 cm shoulder width is a museum object measurement; do not treat it as an actor’s measurement.

## Gaps

- **Coverage gap:** no GAR IDs for undershirt/短上衣, trousers, or leather shoes; therefore the outfit is **not a complete ID-resolved outfit**.
- **Full-body block:** the card forbids full-body shooting while no shoe card exists.
- **Region gap:** Hong Kong robe source + English vest source; no Shanghai-local menswear object in this look.
- **Evidence gap:** `LOOK-0008` is interpretive/draft, not verified production evidence; `SCN-0004` is also interpretive/draft.
- **Unknown production fields:** character name/age/build, venue (study/newsroom/teahouse), story day, season, weather, budget, actor measurements.
- **No stored video prompt:** the video text above is a derived draft.
- **Source licensing:** V&A records are `link_only`; images are not embedded, and image rights are separate from the catalogue metadata.
