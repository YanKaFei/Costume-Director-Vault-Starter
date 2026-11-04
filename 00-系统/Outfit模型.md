# Outfit 知识对象模型（P5-C / task-70）

- 版本：v1（2026-11-05）；目标：把现有 `type=look` 卡升级为**向后兼容**的 Outfit 知识对象，同时不破坏旧 LOOK 卡。
- 数据字典：`00-系统/数据字典-v1.4-扩展.md`（全部 optional 字段）。
- 验证器：`scripts/validate_outfits.py`（复用 `scripts/outfit.py` 的 `validate_hard_constraints`）。
- 原则：**事实 / 风格观察 / 创作推断分层**；旧卡无新字段时标 `legacy`，不判失败；历史造型不得用创作推断冒充。

## 1. 核心分层：evidence_type

| evidence_type | 含义 | 必备字段 | 允许的结论 |
|---|---|---|---|
| `historical_evidence` | 由来源/证据卡支撑的历史组合 | `outfit_slots`、`historical_evidence`、`constraints_checked`、`period_tiers`/`region_tiers` | 可称“历史造型候选”，但必须通过硬约束与来源 scope 检查 |
| `sourced_style_observation` | 有来源的风格/视觉观察（非逐件史实） | `outfit_slots`、`style_observation` | 可称“风格观察/参考”，不得写成“当时实际穿着” |
| `creative_inference` | 设计/策展推断（LOOK 组合、色彩、戏剧化） | `outfit_slots`、`creative_inference` | 只能作为设计建议；不得进入历史结论 |

旧 LOOK 卡（无 `evidence_type`）保持合法，validator 标 `legacy` 并给 warning；不得把 legacy 自动当 historical_evidence。

## 2. 字段（全部 optional，除 `historical_evidence` 分支的必备组合）

### 2.1 槽位与物项

```yaml
outfit_slots:            # flat list; one "slot=card_id" per item
  - "one_piece=GAR-0075"
  - "outerwear=GAR-0076"
  - "footwear=GAR-0081"
  - "accessory=GAR-0080"
  - "carried_prop=GAR-0082"
```

- 允许 slot：`inner_layer` `upper_body`（top）`lower_body`（bottom）`one_piece` `set` `outerwear` `footwear` `accessory` `carried_prop`；`material`/`color`/`silhouette` 不是 item slot，分别用现有 `materials`/`colors` 字段与可选 `outfit_silhouette` 表达。
- 完整组合最低要求：`one_piece`/`set` 或 `upper_body`+`lower_body`；必须 `footwear`；不得同一 ID 重复；不得 one_piece/set 与 top/bottom 叠用（与 `outfit.py` 硬约束一致）。
- 旧卡兼容：无 `outfit_slots` 时 validator 尝试从 `look_items` + `recommend.classify_slot` 推导（仅作 legacy 提示；新对象必须显式写 `outfit_slots`）。

### 2.2 证据字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `evidence_type` | enum | `historical_evidence` / `sourced_style_observation` / `creative_inference` |
| `historical_evidence` | list[string] | 支撑该组合的来源 ID/证据断言（如 `SRC-0480`、`"GAR-0075:SRC-0480"`）；historical 分支必填 |
| `style_observation` | list[string] / string | 有来源的风格观察（不得当史实） |
| `creative_inference` | list[string] / string | 设计/戏剧化推断（必须显式标注） |
| `constraints_checked` | list[string] | 已检查：`period` `region` `identity` `weather` `action` `compatibility` `approved_anchors`；historical 分支应全含 |
| `period_tiers` | list[string] `slot=tier` | 硬约束用；tier: `exact`/`era`/`approximate`/`none`/`unknown` |
| `region_tiers` | list[string] `slot=tier` | 同上 |
| `approved_anchors` | list[string] | 必须出现在 slots 中的已批准 anchor ID |

### 2.3 语境/角色/连续性

| 字段 | 类型 | 说明 |
|---|---|---|
| `periods` / `regions` | 既有 list | 复用 LOOK 卡字段；不新增重复字段 |
| `context` | string/list | 使用语境（场景/场合/戏剧设定） |
| `character_function` | string | 角色功能（身份/职业/阶级/叙事功能）；不是人格判断 |
| `continuity_state` | string/list | 跨场状态（wetness/damage/dirt/accessories） |
| `look_scene` | 既有 list | 显式场景 ID；复用 |
| `relations` | list[string] | flat 关系字符串（与 `00-系统/关系类型.md` 一致；high 才可迁移） |
| `prompt_image` / `prompt_video` | string | 生图/视频英文 prompt（复用/可选） |

### 2.4 事实/观察/推断的最小写法

```yaml
evidence_type: historical_evidence
historical_evidence: [SRC-0480, SRC-0481]
constraints_checked: [period, region, identity, weather, action, compatibility, approved_anchors]
period_tiers: ["one_piece=era", "footwear=era"]
region_tiers: ["one_piece=none", "footwear=era"]
outfit_slots: ["one_piece=GAR-0075", "outerwear=GAR-0076", "footwear=GAR-0081"]
```

```yaml
evidence_type: creative_inference
creative_inference: ["用 1930s 手提包搭配 1770s 裙装，属于跨时代设计对比"]
outfit_slots: ["one_piece=GAR-0015", "footwear=GAR-0024", "accessory=GAR-0048"]
```

## 3. 校验规则（`scripts/validate_outfits.py`）

1. 旧卡（无新字段）：`legacy` + warning；不因缺少 v1.4 字段失败。
2. 新对象（任一新字段出现）：必须 `evidence_type`；分支必备字段见 §1；否则 fail。
3. `outfit_slots`：槽位合法/ID 存在/无重复/完整组合；缺 torso 或 footwear → fail。
4. 硬约束：调用 `outfit.validate_hard_constraints`（rain/cold/action/occupational/approved anchors/historical period/region tiers）。violations 非空：
   - `evidence_type=historical_evidence` → **fail**（不得当合格历史造型）；
   - `sourced_style_observation` / `creative_inference` → warning/`creative`（仍不得称历史）。
5. `approved_anchors`：每个 ID 必须出现在 slots；缺失 → fail（approved anchor 保护）。
6. 历史分支物品：允许 verified/interpretive 但必须在 `historical_evidence` 有来源；example 卡 → fail。
7. 输出：`--json` 每 LOOK 含 status/legacy/errors/warnings/hard_constraints；退出码 0=全 PASS，1=任一 fail。

## 4. 与现有 LOOK / narrator 字段对齐

- 复用：`look_items`（物项候选）、`look_scene`、`periods`、`regions`、`style_tags`、`continuity_lock`、`prompt_en`/`negative_prompt_en`。
- 新增是**叠加**：`outfit_slots` 是对 `look_items` 的显式槽位化；`evidence_type` 等不替代 `evidence_status`（卡片级证据仍由 `evidence_status` 表达）。
- narrator 可将 LOOK 卡逐步补 `evidence_type`/`outfit_slots`/`historical_evidence`；未补前 validator 仍接受旧卡。
- `relations` 与 P5-A/B 同一格式/规则；不因 Outfit 模型放宽历史断言。

## 5. 已知限制

- 槽位完整性不等于语义正确；结构/时代错配仍需 `period_tiers/region_tiers` 与人工判断。
- 硬约束是规则集合，不是完整历史本体；`legacy` 卡不能作为历史证据。
- `style_observation`/`creative_inference` 是文本，含来源的观察需人工核对；validator 不判断文本真伪。
- 不新增卡片/不修改旧卡；模型字段先作为可选层，由后续 LOOK 编写任务采用。
