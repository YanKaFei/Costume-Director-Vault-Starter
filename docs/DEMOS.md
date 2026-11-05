# Three copyable demos

## Demo 1 — Compare two collars

```bash
python3 scripts/visual_prompt.py --id STR-0028 --kind component_detail --markdown
python3 scripts/visual_prompt.py --id STR-0012 --kind component_detail --markdown
```

Look for:

- `STR-0028` shawl collar: continuous rolled edge, **no notch**.
- `STR-0012` notched lapel: visible step/notch and a separate lapel.

This is the difference an image model most often collapses.

## Demo 2 — Complete 1930s Shanghai outfit

```bash
python3 scripts/visual_prompt.py --id LOOK-0009 --kind outfit --markdown
```

The card contains the outfit IDs and the visual composition. The prompt covers:

- ankle-length fitted qipao;
- small stand collar, two frog closures;
- long tight sleeves and side slits;
- black lace flat pumps with sequin detail;
- mid-blue / cream / black / red palette.

Reference status is explicit; no image is generated.

## Demo 3 — Modern minimal vs deconstruction, same character

```bash
python3 scripts/visual_prompt.py --id STY-0024 --kind style --markdown
python3 scripts/visual_prompt.py --id STY-0025 --kind style --markdown
```

Read the two prompts side by side:

- `STY-0024`: clean utility, controlled volume, low-saturation palette, precise closures.
- `STY-0025`: displaced seams, raw edges, layered fragments, asymmetric balance.

The point is not “more adjectives”; it is two different construction logics.
