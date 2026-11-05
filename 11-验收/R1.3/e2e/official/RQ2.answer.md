## LOOK-0001 / outfit — visual prompt result

**Command run (exact):**
```
python3 scripts/visual_prompt.py --id LOOK-0001 --kind outfit --json
```

**Card:** `09-造型组合/LOOK-0001-洛可可沙龙女主人.md`
**Kind:** `outfit` · **Lang:** `en` · **Evidence status:** `interpretive` · **Source:** `SRC-0150`
**Look items:** `GAR-0015`, `STR-0009`, `STR-0006`, `GAR-0028`, `GAR-0024`, `MAT-0002`
**Palette:** cream, pastel, gold

### Outfit modules (3)

| Module | Evidence tags | Source field |
|---|---|---|
| `outfit_hero` | FACT, OBSERVATION, INFERENCE, CREATIVE | `LOOK look_items + prompt_en` |
| `continuity` | FACT | `continuity_lock` |
| `negative` | CREATIVE | `negative_prompt_en` |

**`outfit_hero` — prompt_en:**
> complete outfit 洛可可沙龙女主人; items GAR-0015, STR-0009, STR-0006, GAR-0028, GAR-0024, MAT-0002; palette cream, pastel, gold; 1770s French salon hostess, robe à la française in cream silk brocade, panniers widening the skirt sideways, decorated stomacher, Chantilly lace trim, fur muff, silk mule slippers, candlelit interior, historical mode

**`continuity` — prompt_en (verbatim locks):**
> continuity locks: 裙侧撑宽度固定在同场次内不变；后方箱褶垂坠位置、stomacher 暴露形状、手笼与鞋的颜色保持一致；发饰高度不得在镜头间变化

**`negative` — prompt_en:**
> negative: no modern shoes, no machine lace, no zippers or visible elastic, no anachronistic jewelry, no changed pannier width between shots, no symmetrical wide skirt front

### Continuity / approved-anchor notes

- Four continuity locks are carried: (1) pannier/skirt-side width fixed within the scene; (2) rear box-pleat fall position, exposed stomacher shape, and muff + shoe colors held consistent; (3) hair-ornament height must not change between shots.
- **Approved anchors:** the JSON contains **no `approved_anchors` field**, and this run supplied no Look Bible anchor input. The only frozen instructions emitted are the `continuity_lock` module above. No approved hard anchors were altered — because none were present in this call; they should not be assumed to exist from this output.

### Text-only / no image — confirmed

- `image_generation: false`
- `delivery: "text prompt only"`
- `model_agnostic: true`
- No image or video was generated, fetched, or embedded. This is prompt text only.

### Evidence / conflicts

- Observation: wide lateral front silhouette, thin side profile, large floor-sweeping hem arc, contrasting decorative triangular stomacher panel, soft silk/velvet sheen on muff and mule slippers under candlelight.
- Overall evidence tags: OBSERVATION, INFERENCE, CREATIVE.
- Conflict check: **0 errors, 0 warnings, 1 notice** — `low_confidence`: `evidence_status=interpretive; not verified`. Treat the historical reading as interpretive, not verified fact.
