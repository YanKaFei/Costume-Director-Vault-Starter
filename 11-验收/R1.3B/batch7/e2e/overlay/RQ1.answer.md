## Visual prompt run results (text only — no image generated)

Both commands were run exactly as specified from the Vault root. Each output declares `"image_generation": false`, `"delivery": "text prompt only"`; **no image was generated** in either run.

### 1. MAT-0017 — `material_macro`

- **Real card ID:** MAT-0017
- **Card path:** `03-材质纹样/材料/MAT-0017-皮革.md` (leather)
- **Evidence status:** verified
- **Source IDs (real):** SRC-0549, SRC-0489, SRC-0538
- **Evidence tags (card-level):** FACT, OBSERVATION, INFERENCE, CREATIVE
- **Conflicts:** none (errors 0 / warnings 0 / notices 0)

**Prompt — module `material_surface`** (evidence: FACT, OBSERVATION; source: materials/colors + lighting_notes)
- EN: `extreme macro of leather leather focus on fiber weave sheen and surface irregularity neutral 5600K light shallow depth of field no logos`
- ZH: `材质微距：leather，皮革；聚焦纤维、织法、光泽与表面不均；中性 5600K 光、浅景深、无标识`

Card evidence fields:
- OBSERVATION: "leather material tanned hide soft kid leather gloves or boots matte or polished surface stitched seams"
- INFERENCE: same text (interpretive reading)
- CREATIVE: staging and art-direction choices; not a historical claim

### 2. STR-0028 — `component_detail`

- **Real card ID:** STR-0028
- **Card path:** `02-结构细节/STR-0028-青果领-披肩领.md` (shawl collar)
- **Evidence status:** verified
- **Source IDs (real):** SRC-0532, SRC-0539
- **Evidence tags (card-level):** FACT, OBSERVATION, INFERENCE, CREATIVE
- **Conflicts:** none (errors 0 / warnings 0 / notices 0)

**Prompts by module**

1. Module `structure_detail` (evidence: FACT, OBSERVATION; source: card type + structured fields)
   - EN: `detail of shawl collar on garment part construction seams closures edge finish and hardware orthographic clarity no stylisation`
   - ZH: `结构细节：青果领/披肩领；缝线、闭合、边缘处理与五金；正交清晰、不风格化`

2. Module `construction_note` (evidence: INFERENCE; source: prompt_en)
   - EN: `construction note from card prompt shawl collar jacket continuous rolled collar no notch front facing period or modern tailoring`
   - ZH: `卡片结构提示：shawl collar jacket, continuous rolled collar, no notch, front facing, period or modern tailoring`

Card evidence fields:
- OBSERVATION / INFERENCE: "shawl collar jacket continuous rolled collar no notch front facing period or modern tailoring"
- CREATIVE: staging and art-direction choices; not a historical claim

**Note:** Both outputs are model-agnostic English text prompts (`lang: en` default). INFERENCE/CREATIVE content is not historical fact, and no image generation, image testing, or visual approval occurred.
