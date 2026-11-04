## Query

```bash
python3 scripts/query.py --id GAR-0008 \
  --relation-type claim_supported_by \
  --related-to SRC-0109 \
  --confidence high
```

Result: **1 matching card**, `GAR-0008` (`01-服装单品/上装/GAR-0008-马甲.md`).

## Typed relation

| Field | Value |
|---|---|
| Subject | `GAR-0008` 马甲 / waistcoat |
| Relation type | `claim_supported_by` |
| Direction | `outgoing` |
| **Target** | **`SRC-0109`** |
| Target title | FIT：vest/waistcoat（马甲） |
| Target type | `source` |
| Evidence | `verified` |
| Confidence | `high` |
| Rule | `R-SOURCE-IDS` |
| Relation origin | `card` (frontmatter `relations:`) |
| Source IDs | `SRC-0109` |

## Real 04-来源 file path

```text
04-来源/SRC-0109-FIT-vest-waistcoat.md
```

Absolute path:

```text
/Users/coffee/Desktop/Costume-Director-Vault-Starter/04-来源/SRC-0109-FIT-vest-waistcoat.md
```

The file exists (1,991 bytes) and was confirmed through `scripts/path_guard.py check`, which returned `ALLOW` for both the card and this source file.

## Source card facts

- `id`: `SRC-0109`
- `name_zh`: `FIT：vest/waistcoat（马甲）`
- `name_en`: `vest-waistcoat | Fashion History Timeline`
- `url`: `https://fashionhistory.fitnyc.edu/vest-waistcoat/`
- `publisher`: Fashion History Timeline, FIT/SUNY
- `evidence_status`: `verified`
- `license_status`: `link_only`
- `date_accessed`: `2026-11-04`

## Note on how this was established

The relation was **not inferred from the body wikilink** `[[SRC-0109-FIT-vest-waistcoat]]`. It is an explicit typed relation in `GAR-0008`’s YAML frontmatter:

```yaml
relations:
  - 'target=SRC-0109; type=claim_supported_by; direction=outgoing; evidence=verified; confidence=high; source_ids=SRC-0109; rule=R-SOURCE-IDS'
```

`query.py` also returned a second, `candidate`-origin entry for the same target (`origin: candidate`, `review_status: migration_ready`). That is a duplicate index record, **not a second target** — both resolve to `SRC-0109` and the same `target_path`, `04-来源/SRC-0109-FIT-vest-waistcoat.md`.

**Bottom line:** the `claim_supported_by` target is `SRC-0109`, and its real file is `04-来源/SRC-0109-FIT-vest-waistcoat.md`.
