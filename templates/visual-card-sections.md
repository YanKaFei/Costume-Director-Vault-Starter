# 视觉卡模板（R1.3-B，可选层；不替代 8 节）

> 将本文件内容**追加**到既有内容卡；没有视觉层的旧卡仍合法。不得用视觉提示替代 `prompt_en`/结构/材料事实。
> `ASSET-0001` 仅为示例占位；真实资产需另登记/许可核验，禁止内嵌图片。

## 1. 可选 frontmatter

```yaml
visual_prompt_profile: garment_full_body
visual_prompt_type: [full_body, detail]
visual_assets:
  - "id=ASSET-0001; kind=external_reference; source_ids=SRC-0100; url=https://collections.vam.ac.uk/item/O.../; license=link_only; note=object page only"
visual_evidence: [FACT, OBSERVATION, INFERENCE, CREATIVE]
```

## 2. 可选正文区域

### ## 视觉参考

- `ASSET-0001`（external_reference；link_only；SRC-0100）：对象页轮廓/结构参考；仅链接，不复制图片。
- 资产许可与 `source_ids` 分离；图片权利另审。

### ## 生图提示词

```text
SUBJECT (FACT): full-body adult figure, standing, neutral pose, centered vertical frame.
STRUCTURE (FACT): <只写卡内有的领/袖/肩/腰/摆/门襟/裁片；未知写 unknown>
MATERIAL (FACT): <只写 materials/fiber_content/来源支持的物性；未知写 unknown>
COLOR (FACT): <只写 colors 字段/来源支持的颜色>
LIGHT (CREATIVE): soft directional daylight, low contrast, gentle falloff.
CAMERA (CREATIVE): 50mm lens, full-body, eye level, f/4, clean background separation.
BACKGROUND (CREATIVE): neutral studio wall; no props unless specified.
STYLE (INFERENCE): restrained period styling; no theatrical exaggeration.
NEGATIVE (CREATIVE): no anachronistic closures, no extra jewelry, no invented pattern, no costume morphing.
CONSISTENCY (OBSERVATION): keep silhouette, palette, structure and accessory positions identical across shots.
```

### ## 视频提示词

```text
SUBJECT (FACT): <同一主体/角色/单品>
CONSISTENCY (OBSERVATION): preserve card ID, color, material, structure and accessory placement across frames.
LIGHT (CREATIVE): <光源/色温/变化；不声称服装史事实>
CAMERA (CREATIVE): <运动/景别/机位；保持主体不漂移>
NEGATIVE (CREATIVE): no costume morphing, no colour shift, no extra layers, no logo/text/watermark.
```

## 3. 按域的最小模块集

| 域 | profile 示例 | 必须模块（有证据才写） |
|---|---|---|
| material | `material_macro` | SUBJECT/MATERIAL/COLOR/LIGHT/CAMERA/NEGATIVE |
| component | `component_closeup` | SUBJECT/STRUCTURE/MATERIAL/COLOR/LIGHT/CAMERA/CONSISTENCY |
| garment | `garment_full_body` | SUBJECT/STRUCTURE/MATERIAL/COLOR/LIGHT/CAMERA/BACKGROUND/STYLE/NEGATIVE/CONSISTENCY |
| accessory/footwear | `accessory_object` / `footwear_detail` | SUBJECT/STRUCTURE/MATERIAL/COLOR/LIGHT/CAMERA/NEGATIVE |
| style | `style_abc` / `style_character_scene` | SUBJECT/STYLE/COLOR/LIGHT/CAMERA/BACKGROUND/NEGATIVE/CONSISTENCY |
| outfit | `outfit_abc` / `outfit_consistency` | SUBJECT/STRUCTURE/MATERIAL/COLOR/LIGHT/CAMERA/BACKGROUND/STYLE/NEGATIVE/CONSISTENCY |

## 4. 反编造检查（复制前逐条勾）

- [ ] 每个 `FACT` 都能在卡片字段或 `source_ids` 找到依据；
- [ ] 未支撑的纤维/克重/反光/透明度/部件写 `unknown` 或省略；
- [ ] `LIGHT/CAMERA/BACKGROUND/STYLE/NEGATIVE` 没有冒充历史/物理事实；
- [ ] `visual_assets` 只含元数据，未嵌入/下载图片；许可与来源分离；
- [ ] 保留原文 8 节与原有 `prompt_en`；视觉层为追加内容。

## 5. 中文术语对照（速查）

- SUBJECT=主体；STRUCTURE=结构；MATERIAL=材料/物性；COLOR=颜色；LIGHT=光线；CAMERA=镜头；BACKGROUND=背景；STYLE=风格；NEGATIVE=负向约束；CONSISTENCY=一致性。
- FACT=事实（有字段/来源）；OBSERVATION=观察；INFERENCE=推断；CREATIVE=创作选择。
