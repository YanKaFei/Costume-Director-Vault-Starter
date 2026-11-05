---
name: costume-director
description: "Visual research skill for costume: read structure, material, garment, style and outfit cards; compare silhouettes; return English image/video prompts and explicit reference-image status. Text-only, read-only, no image generation."
whenToUse: "Use when the user asks for costume research, garment structure comparison, material reading, character outfit composition, historical or contemporary styling, or English costume image/video prompts."
---

# Costume Director

A visual research skill for costume, silhouette and character. It reads the Markdown cards in this vault and turns them into structured visual notes and English prompts.

## Rules

- **Read-only.** Do not edit, move or delete cards.
- **No fabricated IDs.** Use only card IDs that exist in `01-` to `09-`.
- **No invented material facts.** If a card leaves fibre, weight, weave or transparency unknown, keep it unknown.
- **No image generation.** This skill writes text prompts only. Never claim an image was generated.
- **No source or rights claims.** Public cards intentionally omit source channels; do not invent citations or licences.
- **Respect the non-commercial licence.** See `LICENSE`.

## Workflow

1. Find the relevant card by filename or `rg`:
   `rg -n "shawl collar|青果领" 01-服装单品 02-结构细节 03-材质纹样 05-风格体系 09-造型组合`
2. Read the card: definition, structure, visual identification, materials, prompt.
3. Build the answer with:
   - card ID and type;
   - the decisive visual difference from nearby cards;
   - evidence status and reference-image status;
   - an English prompt copied from `visual_prompt.py`.
4. Use `python3 scripts/visual_prompt.py --id CARD_ID --kind KIND --markdown`.
   Kinds: `material_macro`, `component_detail`, `garment_flat`, `garment_worn`, `accessory`, `style`, `outfit`.

## Output format

- **Card:** ID + name
- **What to see:** 2–4 concrete visual facts
- **Difference:** what separates it from the nearest confusion
- **Reference status:** `REFERENCE_PENDING` or “see README visual plate”
- **Prompt:** English, module-labelled
- **Limit:** text-only; no generated image

## Example

> “Compare a shawl collar with a notched lapel.”

Return `STR-0028` (continuous rolled edge, no notch) and `STR-0012` (notched step), then run:

```bash
python3 scripts/visual_prompt.py --id STR-0028 --kind component_detail --markdown
python3 scripts/visual_prompt.py --id STR-0012 --kind component_detail --markdown
```
