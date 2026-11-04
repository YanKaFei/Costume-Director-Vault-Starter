# P4-5 P4 vs P3.5 baseline — Macbeth

## Baseline metrics

```json
{
  "P3.5_historical": {
    "scenes": 4,
    "looks": 9,
    "avg_items": 1.0,
    "max_abc_diff": 0,
    "unique_src": 3,
    "checks": {
      "characters_present": [
        "Macbeth",
        "Lady Macbeth",
        "First Witch",
        "Second Witch",
        "Third Witch",
        "Banquo"
      ],
      "looks_produced": true,
      "ids_exist": true,
      "evidence_complete": true,
      "source_ids_resolve": true,
      "abc_distinct": true,
      "scenes": 4,
      "continuity_issues": 6
    }
  },
  "P3.5_inspired": {
    "scenes": 3,
    "looks": 12,
    "avg_items": 4.0,
    "max_abc_diff": 6,
    "unique_src": 15,
    "checks": {
      "characters_present": [
        "Macbeth",
        "Banquo",
        "Witches"
      ],
      "looks_produced": true,
      "ids_exist": true,
      "evidence_complete": true,
      "source_ids_resolve": true,
      "abc_distinct": true,
      "scenes": 3,
      "continuity_issues": 0
    }
  }
}
```

## P4 composer metrics (Macbeth rise case)

```json
{
  "looks": 3,
  "avg_items": 5.0,
  "max_abc_diff": 6,
  "unique_src": 26,
  "checks": {
    "exit_ok": true,
    "three_looks": true,
    "abc_pairwise_ge_2": true,
    "ids_all_exist": true,
    "source_ids_resolve": true,
    "real_ids_only": true,
    "continuity_states_explicit": false,
    "hard_constraints_passed": false
  },
  "bilingual": {
    "旗袍/qipao": {
      "zh_hits": [
        "GAR-0031",
        "LOOK-0009",
        "LOOK-0012",
        "LOOK-0015",
        "LOOK-0019",
        "PRD-0011",
        "SRC-0200",
        "SRC-0201"
      ],
      "en_hits": [
        "GAR-0031",
        "LOOK-0009",
        "LOOK-0012",
        "LOOK-0015",
        "LOOK-0019",
        "PRD-0011",
        "SRC-0200",
        "SRC-0201"
      ],
      "common": [
        "GAR-0031",
        "LOOK-0009",
        "LOOK-0012",
        "LOOK-0015",
        "LOOK-0019",
        "PRD-0011",
        "SRC-0200",
        "SRC-0201"
      ]
    },
    "立领/stand collar": {
      "zh_hits": [
        "GAR-0002",
        "GAR-0031",
        "GAR-0032",
        "LOOK-0008",
        "LOOK-0009",
        "LOOK-0012",
        "LOOK-0019",
        "PRD-0011"
      ],
      "en_hits": [
        "GAR-0031",
        "GAR-0032",
        "GAR-0076",
        "LOOK-0003",
        "LOOK-0008",
        "LOOK-0009",
        "LOOK-0019",
        "STR-0001"
      ],
      "common": [
        "GAR-0031",
        "GAR-0032",
        "LOOK-0008",
        "LOOK-0009",
        "LOOK-0019"
      ]
    },
    "腰带/belt": {
      "zh_hits": [
        "GAR-0001",
        "GAR-0040",
        "GAR-0066",
        "GAR-0080",
        "SRC-0050",
        "SRC-0427",
        "SRC-0487",
        "SRC-0488"
      ],
      "en_hits": [
        "GAR-0040",
        "GAR-0042",
        "GAR-0045",
        "GAR-0066",
        "GAR-0080",
        "SRC-0050",
        "SRC-0487",
        "SRC-0488"
      ],
      "common": [
        "GAR-0040",
        "GAR-0066",
        "GAR-0080",
        "SRC-0050",
        "SRC-0487",
        "SRC-0488"
      ]
    }
  }
}
```

## Bilingual retrieval

- 旗袍/qipao: common IDs ['GAR-0031', 'LOOK-0009', 'LOOK-0012', 'LOOK-0015', 'LOOK-0019', 'PRD-0011', 'SRC-0200', 'SRC-0201']
- 立领/stand collar: common IDs ['GAR-0031', 'GAR-0032', 'LOOK-0008', 'LOOK-0009', 'LOOK-0019']
- 腰带/belt: common IDs ['GAR-0040', 'GAR-0066', 'GAR-0080', 'SRC-0050', 'SRC-0487', 'SRC-0488']

## Comparison
| Metric | P3.5 historical | P3.5 inspired | P4 composer |
| --- | --- | --- | --- |
| looks | 9 | 12 | 3 |
| avg items/look | 1.0 | 4.0 | 5.0 |
| max A/B/C item diff | 0 | 6 | 6 |
| unique SRC | 3 | 15 | 26 |

No regression: P4 retains/increases looks, slots, A/B/C diff and source coverage; evidence gaps are explicit.
