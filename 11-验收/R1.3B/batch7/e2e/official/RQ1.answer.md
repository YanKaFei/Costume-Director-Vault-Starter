## Visual prompt run — MAT-0017 & STR-0028

Both commands completed successfully (exit 0). No image was generated; `image_generation: false`, `delivery: "text prompt only"`, `model_agnostic: true`, `lang: "en"`.

### 1. MAT-0017 — material macro

| Field | Value |
|---|---|
| Real card ID | `MAT-0017` |
| Card | `03-材质纹样/材料/MAT-0017-皮革.md` (皮革 / leather) |
| Kind | `material_macro` |
| Evidence status | `verified` |
| Source IDs | `SRC-0549`, `SRC-0489`, `SRC-0538` |
| Evidence tags (card) | `FACT`, `OBSERVATION`, `INFERENCE`, `CREATIVE` |
| Module evidence | `material_surface` → `FACT`, `OBSERVATION` |
| Conflicts | 0 errors / 0 warnings / 0 notices |

**Prompt (EN, verbatim):**
> extreme macro of leather leather focus on fiber weave sheen and surface irregularity neutral 5600K light shallow depth of field no logos

**Prompt (ZH, verbatim):**
> 材质微距：leather，皮革；聚焦纤维、织法、光泽与表面不均；中性 5600K 光、浅景深、无标识

*Note: the doubled “leather leather” appears in the script output as generated; it was not corrected here.*
Observation / inference fields both read: `leather material tanned hide soft kid leather gloves or boots matte or polished surface stitched seams`.

### 2. STR-0028 — component detail

| Field | Value |
|---|---|
| Real card ID | `STR-0028` |
| Card | `02-结构细节/STR-0028-青果领-披肩领.md` (shawl collar / 青果领) |
| Kind | `component_detail` |
| Evidence status | `verified` |
| Source IDs | `SRC-0532`, `SRC-0539` |
| Evidence tags (card) | `FACT`, `OBSERVATION`, `INFERENCE`, `CREATIVE` |
| Module evidence | `structure_detail` → `FACT`, `OBSERVATION`; `construction_note` → `INFERENCE` |
| Conflicts | 0 errors / 0 warnings / 0 notices |

**Prompt — structure_detail (EN, verbatim):**
> detail of shawl collar on garment part construction seams closures edge finish and hardware orthographic clarity no stylisation

**Prompt — structure_detail (ZH, verbatim):**
> 结构细节：青果领/披肩领；缝线、闭合、边缘处理与五金；正交清晰、不风格化

**Prompt — construction_note (EN, verbatim):**
> construction note from card prompt shawl collar jacket continuous rolled collar no notch front facing period or modern tailoring

**Prompt — construction_note (ZH):** identical to the EN string (as emitted).

Observation / inference fields both read: `shawl collar jacket continuous rolled collar no notch front facing period or modern tailoring`.

### Status

- IDs above are real card/source IDs returned by `scripts/visual_prompt.py`; no IDs were invented.
- Evidence tags are reported per module exactly as returned.
- **No image or video was generated**; these are text-only prompts.
