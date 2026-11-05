## Run

`python3 scripts/visual_prompt.py --id GAR-0015 --kind garment_worn --json` — exit 0.

- **Card:** GAR-0015 — 法式长袍 (robe à la française), `01-服装单品/连身/GAR-0015-法式长袍.md`
- **Kind / language:** `garment_worn` / en; model-agnostic, text prompt only
- **Evidence status:** verified · **Source:** SRC-0116

## Modules

1. **garment_worn** (source: YAML + body)
   - English prompt: full-body neutral model, front/side/back, natural stance, face out of frame, no identity; X-line silhouette; fitted front bodice, loose back with two box pleats falling from shoulder line to floor; open V-front revealing stomacher and petticoat; panniers creating extreme side width; materials silk, brocade, lace; palette pastel, silk_floral, cream; wide turning radius and strong skirt/panel swing when walking, panniers must stay fixed.
   - **Observation:** back pleats fall like a "waterfall"; V-shaped front opening with decorative stomacher panel; very wide silhouette at the sides from panniers.
   - **Inference:** 18th-century robe à la française reading — fitted front, loose pleated back, open front over stomacher/petticoat, panniers, silk brocade.
   - **Creative:** staging/art-direction choices (neutral model, face out of frame, front/side/back views); explicitly not a historical claim.

## Evidence tags

- Overall tag set present: **FACT, OBSERVATION, INFERENCE, CREATIVE**
- Module-level tags (`garment_worn`): **FACT, OBSERVATION, INFERENCE**
- FACT = verified structured card fields; OBSERVATION = card visual/movement prose; INFERENCE = interpretive design reading; CREATIVE = requested staging only (must not be presented as historical fact).

## Conflicts

- **None.** `conflicts: []`; conflict summary: **0 errors, 0 warnings, 0 notices** (no missing material/structure/source, no period/region mismatch, no low-confidence/example-card issue, kind/card type valid).

## Image generation

**No image was generated.** `image_generation: false`, `delivery: "text prompt only"` — output is a model-agnostic text prompt; no image model/tool was invoked.
