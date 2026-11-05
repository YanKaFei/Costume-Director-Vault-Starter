## GAR-0015 — garment_flat prompt run

**Command:** `python3 scripts/visual_prompt.py --id GAR-0015 --kind garment_flat --period 1930s --json` (ran from Vault root, exit 0)

### Card / evidence
- **Card:** GAR-0015 `法式长袍` (robe à la française; 19th-century reproductions also called Watteau gown)
- **Path:** `01-服装单品/连身/GAR-0015-法式长袍.md`
- **Evidence status:** `verified`
- **Source:** **SRC-0116**
- **Evidence tagging in module:** FACT / OBSERVATION / INFERENCE (+ CREATIVE for staging)
  - **FACT (structured card fields):** silhouette X-line; fitted front bodice, loose back with two box pleats falling from shoulder to hem; open V-front revealing stomacher and petticoat; paniers for side width; materials silk, brocade, lace; palette pastel, silk_floral, cream.
  - **OBSERVATION (card prose):** back pleats fall like a "waterfall"; V-shaped front opening with decorative stomacher panel; extremely wide silhouette at the sides from panniers.
  - **INFERENCE (design reading):** 18th-century robe à la française; large turning radius; skirt and back pleats swing with fast movement, panniers must be secured.
  - **CREATIVE:** flat-lay staging (neutral background, front/back, true scale, no model) — not a historical claim.
- No missing-material, missing-structure, missing-source, low-confidence/example-card, or wrong-kind warnings were raised.

### Conflicts
- **1 error / 0 warnings / 0 notices**
- `period_conflict` (**error**): requested **1930s** vs card periods **['18th_century', 'rococo']**. GAR-0015 is an 18th-century Rococo garment, so it must not be presented as 1930s period-correct evidence; any 1930s use would be a deliberate anachronism requiring a creative override, not historical accuracy.

### Output
- Text-only flat-lay prompt generated (model-agnostic, English + Chinese); `delivery: "text prompt only"`.
- **No image was generated** — `image_generation: false`; this environment delivers the prompt text only and runs no image model.
