## LOOK-0001 — Outfit visual prompt (`--kind outfit --json`)

**Card:** LOOK-0001 (`09-造型组合/LOOK-0001-洛可可沙龙女主人.md`) · evidence_status: **interpretive** · source: **SRC-0150**
Evidence tags present: OBSERVATION, INFERENCE, CREATIVE (FACT appears within modules). Conflicts: **0 errors, 0 warnings, 1 notice** — `low_confidence`: evidence is interpretive, not verified.

### Outfit modules

1. **outfit_hero** — FACT / OBSERVATION / INFERENCE / CREATIVE
   - Items: **GAR-0015, STR-0009, STR-0006, GAR-0028, GAR-0024, MAT-0002**
   - Palette: cream, pastel, gold
   - Prompt: complete 1770s French salon hostess outfit — robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode
   - Source: LOOK look_items + prompt_en
   - Card observation: extremely wide front silhouette, relatively narrow side profile; skirt forms a large ground arc; contrasting decorative triangular stomacher panel; muff and mules show soft silk/velvet sheen in candlelight.

2. **continuity** — FACT (source: continuity_lock)
   - Pannier side width fixed within the same scene
   - Back box-pleat drape position, stomacher exposure shape, and muff/shoe colors stay consistent
   - Hair-ornament height must not change between shots

3. **negative** — CREATIVE
   - No modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front

### Continuity / approved-anchor notes

- The JSON returns **no separate `approved_anchors` field**; the frozen anchors are expressed via the **continuity module** (tagged FACT): pannier width, back box-pleat drape position, stomacher shape, muff/shoe color, and hair-ornament height.
- The prompt therefore preserves the continuity lock and does not silently alter those hard anchors. Because the look is `interpretive` (not verified), these locks should be treated as Look Bible continuity locks, not as independently verified historical evidence.

### Delivery confirmation

- `image_generation: false` · `delivery: "text prompt only"` · `model_agnostic: true`
- **Text-only: confirmed — no image or video was generated.** The interpretive/not-verified notice means this prompt must not be presented as verified historical fact.
