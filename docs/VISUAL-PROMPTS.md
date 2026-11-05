# Visual prompt generator (R1.3-D)

`python3 scripts/visual_prompt.py --id CARD --kind KIND --lang en|zh [--json|--markdown]`

Kinds: `material_macro`, `component_detail`, `garment_flat`, `garment_worn`,
`accessory`, `style`, `outfit`.

Examples:
```bash
python3 scripts/visual_prompt.py --id GAR-0015 --kind garment_worn --lang en --json
python3 scripts/visual_prompt.py --id MAT-0017 --kind material_macro --lang zh --markdown
python3 scripts/visual_prompt.py --id LOOK-0001 --kind outfit --period 1770s --json
```

Every module carries evidence tags: `FACT` (verified structured/source fields),
`OBSERVATION` (card visual/lighting/movement prose), `INFERENCE` (interpretive
combination), `CREATIVE` (staging/art-direction choice). Conflicts reported:
missing material/structure/source, period/region mismatch, low-confidence/example,
kind/card type mismatch.

**No image generation:** output contains `"image_generation": false` and
`"delivery": "text prompt only"`. If the environment has no image model, deliver the
prompt and explicitly say no image was generated. Never present INFERENCE/CREATIVE
as historical fact; low-confidence/example cards stay warnings.

Visual references: `11-验收/P4-VISUAL/visual-index.csv` (link-only; `MET-API` rows
have no independent SRC card). Approved Look Bible hard anchors must not be silently
changed by a prompt.
