# P5-C Outfit 知识对象与硬约束验证器（task-70）

- 任务：P5-C Outfit 数据模型；快照 HEAD `f500289`（P5-B 完成后）+ 本任务工作区
- 性质：**只新增模型/验证器/测试/文档**；不改 `01-09` 卡片；旧 LOOK 卡保持合法
- 交付：`00-系统/Outfit模型.md`、`00-系统/数据字典-v1.4-扩展.md`、`scripts/validate_outfits.py`、`tests/test_validate_outfits.py`、本报告
- 验证：`validate.py` PASS 400/400（0 errors/0 warnings）；`validate_outfits.py --all` 23 LOOK 全部 legacy 接受（0 fail）；单测 **10/10 OK**

## 1. 字段清单（全部 optional，仅 `type=look`）

| 组 | 字段 | 说明 |
|---|---|---|
| 槽位 | `outfit_slots` | `slot=ID` 列表；slot: inner_layer/upper_body/lower_body/one_piece/set/outerwear/footwear/accessory/carried_prop；旧卡无此字段时从 `look_items` 推导（legacy 提示） |
| 证据分层 | `evidence_type` | `historical_evidence` / `sourced_style_observation` / `creative_inference`；新对象必填 |
| 历史证据 | `historical_evidence` | 来源/断言列表（`SRC-xxxx` 或 `CARD:SRC`）；historical 分支必填 |
| 风格观察 | `style_observation` | 有来源的风格/视觉观察；不得写成逐件史实 |
| 创作推断 | `creative_inference` | 设计/戏剧推断；必须显式标注 |
| 约束 | `constraints_checked` | `period` `region` `identity` `weather` `action` `compatibility` `approved_anchors` |
| 证据层级 | `period_tiers` / `region_tiers` | `slot=tier`；tier: exact/era/approximate/none/unknown |
| 批准锚点 | `approved_anchors` | 必须出现在 slots 的已批准 ID |
| 语境 | `context` | 场景/场合/戏剧设定 |
| 角色功能 | `character_function` | 身份/职业/阶级/叙事功能（非人格判断） |
| 连续性 | `continuity_state` | wetness/damage/dirt/accessories 等状态 |
| 廓形 | `outfit_silhouette` | 整体轮廓（A/H/Y/X 等），不替代结构卡 |
| 提示词 | `prompt_image` / `prompt_video` | 生图/视频英文 prompt（既有字段复用） |
| 关系 | `relations` | 与 `00-系统/关系类型.md` 一致；Outfit 不改变证据规则 |
| 既有复用 | `periods`/`regions`/`style_tags`/`look_items`/`look_scene`/`continuity_lock` | 不新增重复字段 |

详细规则：`00-系统/Outfit模型.md`；兼容字段表：`00-系统/数据字典-v1.4-扩展.md`。

## 2. 三层证据语义

| evidence_type | 必备 | 允许结论 |
|---|---|---|
| `historical_evidence` | slots、historical_evidence、constraints_checked、period/region tiers | 可称历史造型候选；**硬约束失败不得当合格历史造型** |
| `sourced_style_observation` | slots、style_observation | 风格/视觉参考；不得说“当时实际穿着” |
| `creative_inference` | slots、creative_inference | 设计建议；不得进入历史结论 |
| 缺省（旧卡） | — | `legacy`：仅兼容/导航，不得当历史证据 |

`evidence_status`（卡片级 verified/interpretive/example）与 `evidence_type`（对象级分层）同时保留：Outfit 模型不替代卡片证据。

## 3. `scripts/validate_outfits.py`

```bash
python3 scripts/validate_outfits.py --vault . --all --json
python3 scripts/validate_outfits.py --vault . --look LOOK-0001
python3 scripts/validate_outfits.py --vault . --input /tmp/outfit.json --json
```

- 复用 `scripts/outfit.py` 的 `validate_hard_constraints`：torso/鞋/重复 ID、rain/cold 外层、动作鞋履、occupational/approved anchors、historical period/region tiers、item compatibility。
- 新对象（任一新字段）必须：`evidence_type`；完整 slots（one_piece/set 或 top+bottom；footwear）；分支必备字段；`approved_anchors` 全含。
- `historical_evidence` 分支 + 硬约束 violations → **fail**；`sourced_style_observation`/`creative_inference` 的 violations 记 warning（仍不得当历史）。
- 旧卡（无新字段）→ `legacy_warn`，不 fail；`--all` 结果：23 LOOK / 0 fail / 23 legacy。
- 输出每 LOOK：`status`、`legacy`、`slots`、`errors`、`warnings`、`hard_constraints{violations,item_compatibility,declared_mismatches}`；退出码 1=任一 fail。

## 4. 兼容性/测试证据

- 旧卡：23/23 LOOK 卡无 v1.4 字段仍合法（`legacy_warn`；0 fail）；未修改任何卡片。
- 旧卡结构冲突（如 LOOK-0008 one_piece + top/bottom）在 legacy 下为 warning，不阻塞旧卡；新对象同类冲突为 fail（由新字段触发严格模式）。
- 新对象单测 10/10：
  1. valid historical pass
  2. missing footwear fail
  3. historical without historical_evidence fail
  4. new outfit without evidence_type fail
  5. approved anchor missing fail
  6. rain without rainwear in historical fail（hard constraint）
  7. sourced_style_observation without style_observation fail
  8. creative_inference with note pass
  9. LOOK-0001 legacy accepted
  10. all 23 legacy LOOKs 0 fail
- 命令：`python3 -m unittest tests.test_validate_outfits -v` → `Ran 10 tests ... OK`；`python3 scripts/validate.py` → PASS 400/400。

## 5. 与 narrator LOOK 卡字段对齐

- 复用 narrator 既有字段：`look_items`、`look_scene`、`periods`、`regions`、`style_tags`、`continuity_lock`、`prompt_en`/`negative_prompt_en`。
- 新增字段为叠加：`outfit_slots` 把 `look_items` 槽位化；`evidence_type` 标注对象级事实/观察/推断；`historical_evidence` 指向来源；不删除/重命名旧字段。
- 迁移建议：先给首批 historical LOOK 补 `evidence_type/outfit_slots/historical_evidence/constraints_checked/period_tiers/region_tiers`；补前 validator 仍兼容。字段由 narrator 在 LOOK 卡任务中采用，本任务未改卡片。

## 6. 已知限制 / 剩余风险

1. **未迁移任何 LOOK 卡**：当前 23 张仍是 legacy；模型/验证器已就绪，需 narrator 后续补字段后才能标 historical/sourced/creative。
2. `outfit_slots` 由 `look_items` 推导只用于 legacy 提示；推导可能与 narrator 的真实槽位意图不同，不能当事实。
3. 硬约束是规则集合，不是完整历史本体；`period_tiers/region_tiers` 仍依赖卡片证据质量。
4. `style_observation`/`creative_inference` 是自由文本；validator 不判断文本真伪，需人工审阅。
5. `approved_anchors` 只做存在性检查，不验证审批签名/来源；审批流程见 Look Bible/task-55。
6. 未运行 GUI/工作流；本任务仅模型/验证器静态测试。
