# P5-A 关系本体 / 候选生成 / MOC 报告

- 任务：task-61（P5-A 关系本体与 MOC）；快照 HEAD `1acb4d3` + 工作区（engineer task-60 并行）
- 交付：`00-系统/关系类型.md`、`00-系统/MOC/`、`11-验收/P5/RELATION-CANDIDATES.csv`、本报告
- 原则：只从结构化字段生成关系；不做关键词历史推断；**不修改卡片正文/事实**（本任务 0 卡片编辑）
- 源白名单：`11-验收/P5/source-audit.csv`（researcher/task-62）— `whitelist_connected` 143 / `whitelist_independent` 49 / `action_needs_citation` 9 / `action_should_connect` 7 / `blacklist_duplicate` 3；`reports/SOURCES.csv` 为登记快照
- 校验：`python3 scripts/validate.py` → **PASS 400/400, 211 sources, 0 errors, 0 warnings**；候选 CSV 结构自检 677 行/ID 唯一/全部 subject·object·source_ids 可解析/无 deprecated 端点/high 均含来源；MOC 9 文件 `[[...]]` 0 broken。

## 1. 关系类型（8 个，详见 `00-系统/关系类型.md`）

| relation_type | subject → object | 结构化来源 | 证据/置信上限 |
|---|---|---|---|
| `appears_in_look` | look → garment/part/material/pattern | `LOOK.look_items` | 组合是设计解释；不自动史实 |
| `look_appears_in_scene` | look → scene | `LOOK.look_scene` | 显式场景使用 |
| `context_includes` | period_region → garment/part | `PRD.key_garments` + PRD.source_ids | 语境级；不是逐单品历史证明 |
| `in_style` | garment/part/look → style | subject `style_tags` 精确 `STY-xxxx` | 风格归属；自由 tag 不自动成关系 |
| `uses_material` | content → material | `materials` token ↔ MAT `materials`/`fiber_content` | token 非 canonical ID；多义→low |
| `may_have_part` | garment → garment_part | 同 LOOK `look_items` 共现（无 `has_part` 字段） | 仅候选，最高 medium |
| `ensemble_with` | garment → footwear/accessory/headwear/carried_prop | 同 LOOK `look_items` 共现 | 搭配候选，最高 medium |
| `claim_supported_by` | content → source | subject `source_ids`（source-audit whitelist） | 证据取两者最弱；high 需源在 whitelist |

通用字段：`relation_type, direction, subject_id/type, object_id/type, evidence(verified/interpretive/example), confidence(high/medium/low), rationale, source_ids, rule_id, review_status`；CSV 见 §3。

## 2. 候选生成结果（`11-验收/P5/RELATION-CANDIDATES.csv`）

**总计 677 条：high 244（migration_ready）/ medium 408 / low 25（review_queue 433）**；evidence：verified 273 / interpretive 388 / example 16。

| relation_type | total | high | medium | low | 说明 |
|---|---:|---:|---:|---:|---|
| claim_supported_by | 298 | 191 | 106 | 1 | 内容卡 `source_ids` → 来源；高置信 191 |
| appears_in_look | 122 | 0 | 115 | 7 | LOOK 多 interpretive；无 high |
| context_includes | 45 | 45 | 0 | 0 | PRD.key_garments，语境级 high |
| ensemble_with | 74 | 0 | 70 | 4 | LOOK 共现，设计候选 |
| in_style | 47 | 8 | 38 | 1 | 仅精确 STY ID 才 high |
| look_appears_in_scene | 22 | 0 | 20 | 2 | 显式 look_scene |
| may_have_part | 31 | 0 | 30 | 1 | 共现候选，不能当 has_part |
| uses_material | 38 | 0 | 29 | 9 | 唯一 token 映射；多义 token 跳过 |
| **合计** | **677** | **244** | **408** | **25** | high 全在 whitelist source；review 433 |

- **high 仅 3 类**：claim 191、context 45、style 8；`appears_in_look`/`ensemble_with`/`may_have_part`/`uses_material` 最高 medium（设计/映射性质），符合“high 才迁移”。
- 高置信行的 source 全部来自 `source-audit.csv` 的 `whitelist_*`（309 次引用，0 action/blacklist）。
- 重复来源黑名单（`SRC-0157/0163/0175`）不作为对象；`GAR-0087` deprecated 不作为 subject/object。

## 3. MOC 导航页（`00-系统/MOC/`，9 个文件，纯导航）

| 页面 | 覆盖 | 数量 |
|---|---|---:|
| `README.md` | MOC 总览 + 浏览路径 + 维护规则 | 9 页入口 |
| `服装单品.md` | 01 garment，按 category/subcategory | 88 |
| `结构细节.md` | 02 garment_part，按 part_family | 26 |
| `材质纹样.md` | 03 material/pattern | 14 |
| `鞋履配饰.md` | footwear 9 / headwear 7 / accessory 11 / carried_prop 5 | 32 |
| `时代地域.md` | 06 period_region，按 period | 11 |
| `风格体系.md` | 05 style，按 category | 11 |
| `造型组合.md` | LOOK 23 + SCN 16；SCN 页含 look_scene 反向链 | 23+16 |
| `来源证据.md` | SRC 211，按 source_kind，含被引次数 | 211 |

- 只列真实卡片/分类，不做连通率硬连；页内明确“导航，非事实断言；关系候选见 CSV”。
- 每个 MOC 提供下一步路径（单品→结构/材质/鞋履配饰/时代/风格/造型/来源），从任何卡可回跳。
- 链接自检：9 个 MOC 文件的 `[[...]]` 目标全部存在（0 broken）。

## 4. 冲突点 / 缺口（需 lead/engineer 决策）

1. **garment↔part 无结构化字段**：卡片没有 `part_ids`/`has_part` 字段；`may_have_part` 仅 31 条 medium/low，来自同一 LOOK 共现，不能升级为 `has_part`。MOC 只做导航；迁移工具不得消费为结构事实。
2. **material token 不是 canonical ID**：`uses_material` 仅保留唯一 token 映射 38 条（medium/low）；`cotton`、`silk`、`metal_film` 多义映射被跳过（不造假行）——若需 garment→material 迁移，需先建 canonical material ID/映射表（后续任务）。
3. **LOOK 证据多为 interpretive**：`appears_in_look` 122 条全部 medium/low（无 high），`look_appears_in_scene` 22 条同为中/低；设计组合与史实套装需分开表述；不得当 historical fact 迁移。
4. **context_includes 45 high 是“语境级”**：来自 `PRD.key_garments` + PRD.source_ids，不等于“逐单品被证实穿于该年代”；迁移/发布需人工确认语义，报告已标注。
5. **character↔look 不可生成**：`scene_character`/`look_role` 是自由文本，无结构化 character ID；本任务不伪造 `character_wears_look`，仅用 `look_scene` 关联场景；需要角色 ID schema 后再做。
6. **style 高置信仅 8 条**：只有精确 `STY-xxxx` 在 `style_tags` 才算；大量自由 tag（rococo/victorian 等）未自动成关系（避免 alias/关键词误连），仅作导航与后续审核。
7. **并行迁移冲突**：engineer/task-60 正在把 `claim_supported_by` 写入卡片（审计时 30 卡/34 条，flat string、`R-SOURCE-IDS`、`direction=outgoing`）；本任务 CSV 的 high claim 191 与其同 schema，但其余 high（context 45/style 8）尚未迁移。请迁移工具只消费 `migration_ready` 且按类型过滤；不要让 task-60 覆盖本 CSV（本任务路径 `11-验收/P5/RELATION-CANDIDATES.csv`）。
8. **源审计有 action 类**：9 条 `action_needs_citation` + 7 条 `action_should_connect` 未进入关系白名单；如后续补来源，由 researcher 更新 `source-audit.csv` 后再重生成候选。

## 5. 复现/验证

```bash
python3 scripts/validate.py                  # PASS 400/400, 211 sources, 0 warnings
python3 - <<'PY' ... RELATION-CANDIDATES.csv  # 677 rows; unique relation_id; all IDs/source_ids resolve; no deprecated; high source nonempty
PY
# MOC: 00-系统/MOC/*.md → all [[...]] targets exist (0 broken)
```

- 生成规则/字段/迁移格式：`00-系统/关系类型.md`。
- 源侧权威：`11-验收/P5/source-audit.csv`（whitelist/blacklist/action 分类）。
- 本任务未写 `00-系统/索引.md`（不在 task-61 写范围）；MOC 总览入口为 `00-系统/MOC/README.md`。
