## Brief
- Card: `LOOK-0011` — 废弃空间站维修工 / derelict space station repair technician look
- Type: `look` · `category: character_look` · `subcategory: fictional`
- Evidence status: `interpretive` (not production-verified, explicitly not real spaceflight research)
- Period/region: 22nd century, fictional world · Style: `STY-0009`, sci_fi, functional

## Role
`look_role`: **22 世纪废弃空间站维修工（虚构角色，fictional 模式）**
— 22nd-century derelict-space-station repair technician; a five-slot "assembled from scavenged gear" look, deliberately low-tech rather than sleek sci-fi.

## Item IDs (all five slots)
| Slot | Item ID | Name |
| --- | --- | --- |
| 连身 (base) | `GAR-0038` | 连体工作服 |
| 外层 (outer) | `GAR-0037` | 消防防护外套 (used as improvised protective layer) |
| 头部 (head) | `GAR-0039` | 安全头盔 |
| 鞋 (footwear) | `GAR-0022` | 威灵顿靴 (used as work boots) |
| 配饰 (accessory) | `GAR-0050` | 制服徽章 (station ID badge) |

Every item ID: **GAR-0038, GAR-0039, GAR-0037, GAR-0022, GAR-0050**

Source IDs on the card: `SRC-0402`, `SRC-0401`, `SRC-0123`, `SRC-0410`.

## Gaps (from the card's own `evidence_limits`)
- No work gloves, tool belt, real work boots, oxygen/comms interface, or real EVA helmet in the KB.
- `GAR-0039` is a 1960s papier-mâché toy helmet — fictional/theatrical prop only; not EVA evidence.
- `GAR-0037` (19th-c. Japanese firefighter coat) and `GAR-0022` (Wellington boot) are structural borrowings, marked interpretive.

Note: I ran the exact command requested (`python3 scripts/query.py --id LOOK-0011 --json`), which returns only the card summary; the role and `look_items` fields were read from the card itself via the Vault path guard.
