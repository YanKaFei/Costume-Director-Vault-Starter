## Query run

From the Vault root:

```bash
python3 scripts/query.py --id GAR-0002 --relation-type may_have_part --json
python3 scripts/query.py --id GAR-0002 --relation-type ensemble_with --json
```

I also re-ran both together with `--limit 0` to rule out truncation. Exactly **two** relations were returned.

## Returned relations

| Requested relation | Target | Target resolves to a real card? | Target card | Relation metadata |
|---|---|---|---|---|
| `may_have_part` | `STR-0001` | **Yes** | `02-结构细节/STR-0001-美第奇领.md` — 美第奇领 / Medici collar; type `garment_part`; card `evidence_status: verified`; card source `SRC-0101` | `interpretive` / `medium`; `origin: candidate`; `review_status: review_queue`; rule `R-LOOK-PART-COOCCUR`; relation sources `SRC-0101`, `SRC-0103` |
| `ensemble_with` | `GAR-0024` | **Yes** | `01-服装单品/足部/GAR-0024-穆勒鞋.md` — 穆勒鞋 / mule; type `garment`; card `evidence_status: verified`; card source `SRC-0125` | `interpretive` / `medium`; `origin: candidate`; `review_status: review_queue`; rule `R-LOOK-ENSEMBLE`; relation sources `SRC-0101`, `SRC-0103` |

## Resolution checks

- **`STR-0001`**: `query.py --id STR-0001` returns `name_zh: 美第奇领`, `name_en: Medici collar`, `type: garment_part`, `evidence_status: verified`, `source_ids: [SRC-0101]`, path `02-结构细节/STR-0001-美第奇领.md`. The file exists and its frontmatter `id` is `STR-0001`.
- **`GAR-0024`**: `query.py --id GAR-0024` returns `name_zh: 穆勒鞋`, `name_en: mule`, `type: garment`, `evidence_status: verified`, `source_ids: [SRC-0125]`, path `01-服装单品/足部/GAR-0024-穆勒鞋.md`. The file exists and its frontmatter `id` is `GAR-0024`.

So both returned targets resolve to real, existing cards.

## Important qualification

These two relations are **candidate relations**, not relations stored in GAR-0002’s card YAML:

- `--relations-from cards` returns `[]` for both relation types.
- GAR-0002’s own frontmatter contains only one relation: `claim_supported_by → SRC-0103` (`verified`, `high`).
- The two requested relations come from the structured candidate index (`11-验收/P5/RELATION-CANDIDATES.csv`) and are still `review_queue`.

They are candidate-level “look co-occurrence” relations, not reviewed historical assertions such as `has_part` or proof of a historical ensemble.

## Wikilinks excluded

GAR-0002’s `## 相关卡片` section links to:

`GAR-0003`, `GAR-0008`, `STR-0003`, `STR-0005`, `SRC-0103`

These are navigational wikilinks. Neither relation query returned them, so they are **not** counted as structured relations. No inbound candidate relations of these two types targeting GAR-0002 were found either.
