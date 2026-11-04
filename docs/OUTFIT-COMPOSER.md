# Outfit Composer（P4-3）— 完整搭配而不是单件推荐

`scripts/outfit.py` 是建立在**既有** `scripts/recommend.py` / `costume_lib.py` /
`reco_norm.py` 之上的 P4 组合层。它不替换、不修改旧 `query/recommend/workflow` CLI；
旧的 JSON/退出码/测试保持不变。

## 1. 用法

```bash
# 从已有 recommend 输入 JSON
python3 scripts/outfit.py --input input.json --json > outfit.json

# 人读 Markdown
python3 scripts/outfit.py --input input.json --md

# 从自由文本 brief（复用 recommend 的 brief 解析）
python3 scripts/outfit.py --brief "1930s Shanghai female journalist, rainy night, low budget"

# 写文件（JSON 或 Markdown 由 --json/--md 决定）
python3 scripts/outfit.py --input input.json --json --out 11-验收/P4-COMPOSER/runs/example.json
```

退出码：
- `0`：至少组装出一套完整/可报告 look；
- `2`：输入文件不存在、JSON 非法、brief 为空等调用错误；
- `3`：所有硬约束之后无候选（知识库缺口）；仍输出结构化 warnings。

## 2. 输入

沿用 recommend 的扁平/嵌套输入（`character`/`scene`/period/region/culture/
art_direction/lighting/camera/budget/weather/action/fidelity_mode/tool`），并新增：

```json
{
  "scenes": [
    {"id": "S1", "wetness": "wet", "damage": "none", "dirt": "none"},
    {"id": "S2", "wetness": "dry", "damage": "none", "dirt": "none"}
  ],
  "state": {"wetness": "dry", "damage": "none", "dirt": "none"}
}
```

- `scenes[]` 或 `states[]` 提供跨场状态链；未提供时状态保持 `unknown`，**不推断干净/脏/破损**。
- 所有未知字段保持 unknown；不编造职业、时代、地域、预算、卡 ID、SRC。

## 3. 输出契约

JSON 顶层：

```json
{
  "composer": "P4-3 outfit-composer",
  "input": {...},
  "occupation_anchor": "GAR-0036",
  "looks": [
    {
      "look_ref": "A",
      "items": [{"slot":"one_piece","id":"GAR-0036","source_ids":["SRC-0400"], ...}],
      "slot_ids": {...}, "covered_slots": [...],
      "palette": {"colors": [...], "families": {...}, "dominant_family": "...",
                   "dominant_share": 0.42, "harmony": 0.92},
      "materials": {"materials": [...], "families": {...}, "harmony": 0.9},
      "silhouette": {"shape": "H|A|X|Y|O|I", "proportion": 0.85, ...},
      "domain_fit": {"period": "...", "region": "...", "occupation": "...",
                      "occasion": true, "weather": "...", "action": "...",
                      "lighting": "...", "camera": "..."},
      "evidence": {...}, "source_ids": [...], "missing_source_ids": [...],
      "prompt_image": "...", "prompt_video": "...",
      "prompt_outfit": "...", "prompt_negative": "...",
      "reasons": [...], "risks": [...]
    }
  ],
  "abc_metrics": {
    "a_b": {"item_diff": 2, "palette_diff": 3, "silhouette": ["H","A"]},
    "a_c": {"item_diff": 3, ...},
    "b_c": {"item_diff": 2, ...},
    "all_pairwise_ge_2": true
  },
  "completeness": {"all_have_torso": true, "all_have_footwear": true,
                    "all_have_outerwear": true, "all_have_accessory": true,
                    "all_have_carried_prop": true},
  "continuity": {"states": [...], "anchors": [...], "warnings": [...]},
  "evidence": {"source_ids": [...], "source_urls": [...], "missing_source_ids": []},
  "warnings": [...],
  "checks": {"three_looks": true, "abc_pairwise_ge_2": true,
              "ids_all_exist": true, "source_ids_resolve": true,
              "continuity_states_explicit": true}
}
```

`--md` 输出 same data 的 Markdown 表：每套 look 的槽位/ID/颜色/材质/证据/来源、
palette/materials/silhouette、A/B/C 指标、连续性、warnings。

## 4. 槽位与完整搭配

必需槽位：
- `one_piece` **或** `set` **或** `upper_body + lower_body`；
- `footwear`；
- 天气/季节需要时 `outerwear`（cold/rain/wind/秋冬）。

可选补齐：
- `accessory`、`carried_prop` — 旧 recommend 可能留空；composer 从同一真实候选池
  补一个**语境兼容**的候选（地区标签严格相交、时期层级兼容），否则保留空缺并
  warning，不塞跨文化单品。
- 职业严控场景：`OCCUPATIONAL_STRICT`（护士/医生/警察/厨师/太空等）会把
  occupation affinity 最高的制服件作为 **occupation anchor** 注入 A/B/C，
  避免 B/C 退化成无关服装；`occupation_anchor` 字段报告锚点。

## 5. 协调性指标

- **配色**：颜色家族（neutral/warm/cool）、dominant family share、different colors、
  harmony 0–1；同色堆叠或单色占比过高会降低 harmony 并 warning。
- **材质**：family（wool/linen/cotton/silk/leather/metal/synthetic）、distinct 数、
  常见兼容 pair 加分；全同材质降分。
- **轮廓**：从 card `silhouette`/名称/subcategory/tags 推断 `A/H/X/Y/O/I`；
  proportion 依据 has_defined_waist / balanced torso / layered。
- **场合适配**：`domain_fit` 汇总 period/region 证据 tier、occupation/occasion check、
  weather/action/lighting/camera 输入；风险仍保留在 `risks`。

## 6. A/B/C 差异

- 以 item ID 对称差计算结构差异，要求 pairwise `>= 2`（避免只换色/同义词）。
- 若旧组合退化到 <2，composer 会从真实 unused pool 换一个共享槽位（只换一个 ID
  即产生 2 个对称差），记录 `A/B/C difference repaired ...` warning。
- `abc_metrics` 同时报告 palette 差异和 silhouette；不强行制造不存在的 item。

## 7. 连续性

- 输入 `scenes[]`/`states[]` 显式给出 wetness/damage/dirt；composer 生成状态链和
  anchors（A/B/C 共享 item 交集）。
- 未提供时 `unknown`；不会自动写成 dry/none，也不会编造血迹/雨湿/破损。
- `checks.continuity_states_explicit` 报告是否所有状态都来自输入事实。

## 8. 证据与 prompt

- 每个 item 必须有真实 GAR/STR/MAT ID；来源 SRC 从 `04-来源/` 解析，缺失记入
  `missing_source_ids` 并 warning。
- `prompt_image`/`prompt_video` 由 recommend 生成并做英文过滤；composer 额外给
  `prompt_outfit`（完整搭配 + palette/material/silhouette）和 `prompt_negative`
  （no morphing/extra layers/colour shift/invented accessories/logo/text）。
- example 卡不会进入 composed look；历史模式没有 verified 证据时显式 warning。

## 9. 测试与指标

```bash
python3 11-验收/P4-COMPOSER/test_outfit.py
```

9 个真实 KB 用例：Macbeth / Lady Macbeth、Ghana 跨文化、雨夜连续性、低预算、
近景细节、动作舞蹈、护士职业、historical+cyberpunk 冲突拒绝。全部 PASS。
每次输出在 `11-验收/P4-COMPOSER/runs/`，汇总见 `SUMMARY.md`。

A/B/C 指标（测试结果）：
- 所有正常 3-look 用例 `all_pairwise_ge_2 = true`，最小 pairwise item diff = **2**；
- Macbeth / Lady Macbeth 也经过 `ensure_abc_difference` 修复到 diff=2；
- conflict 用例只有 1 look，明确报告 historical/science-fiction 冲突与知识库缺口。

旧版 vs 新版（同一输入，`scripts/recommend.py` → `scripts/outfit.py`）：

| Case | legacy slots | composer slots | slot gain | legacy min diff | composer min diff |
| --- | --- | --- | --- | --- | --- |
| Macbeth | 4 | 5 | +1 | 2 | 2 |
| Ghana cross-cultural | 4 | 4 | 0 | 2 | 2 |
| Nurse | 5 | 5 | 0 | 2 | 2 |

旧版 A/B/C 差异和 three_looks 已满足；composer 主要增加 accessory/carried 补齐、
配色/材质/轮廓/场合适配指标、连续性状态、英文 outfit prompt 和证据 gap 报告。
旧 `recommend.py` 的 CLI/JSON 未修改，45 acceptance + 9 workflow 回归另行运行。

## 10. 限制

- 轮廓/比例是启发式（卡片没有完整版型数据时默认 `I`）；不是 CAD/打版输出。
- 配色/材质 harmony 是确定性规则，不是色彩科学或面料物理模拟。
- accessory/carried 若库内没有语境兼容候选，保留空缺 + warning，不跨文化硬塞。
- 职业锚点只对严格职业生效；婚礼/文化场合依赖已有 curated look，不强行注入。
- 连续性状态只来自显式 scenes/states；未提供就是 unknown，输出不会替用户做制作决定。
- 不生成图片/视频，只输出可交给模型的英文 prompt。
