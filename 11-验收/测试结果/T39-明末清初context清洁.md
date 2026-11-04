# T39 — 明末清初：context_refs 不得引用 1770s/维多利亚等无关卡

- 运行时间：2026-11-05T01:20:04+08:00
- 测试类型：historical_weak_coverage, context, M4
- 模式：standard
- 输入文件：`11-验收/测试输入/T39-明末清初context清洁.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T39-明末清初context清洁.json --json`
- 退出码：**0**（耗时 1.18s）

## 实际输入

```json
{
  "character": {
    "name": "顾砚秋",
    "occupation": "书院教师、江南文人",
    "economic_status": "中下",
    "arc": "朝代更替中保持读书人的体面与犹疑"
  },
  "period": "1644 late Ming early Qing",
  "region": "jiangnan china",
  "season": "spring",
  "scene": "书院讲堂",
  "time": "day",
  "weather": "overcast, dry",
  "action": "讲学、整理书箱",
  "location": "江南书院",
  "art_direction": "文人水墨、克制、低饱和",
  "lighting": "阴天窗光",
  "camera": "medium shot",
  "budget": "low",
  "fidelity_mode": "historical",
  "tool": "midjourney"
}
```

## 已知输入

以下字段来自测试输入文件，是**已知条件**（不是模型推断）：

- 角色名（`character.name`）："顾砚秋"
- 职业（`character.occupation`）："书院教师、江南文人"
- 经济状态（`character.economic_status`）："中下"
- 人物弧线（`character.arc`）："朝代更替中保持读书人的体面与犹疑"
- 年代（`period`）："1644 late Ming early Qing"
- 地域（`region`）："jiangnan china"
- 季节（`season`）："spring"
- 美术方向（`art_direction`）："文人水墨、克制、低饱和"
- 摄影光线（`lighting`）："阴天窗光"
- 景别（`camera`）："medium shot"
- 预算（`budget`）："low"
- 严格度模式（`fidelity_mode`）："historical"
- 生成工具（`tool`）："midjourney"

## 假设

- 人物弧线（朝代更替中保持读书人的体面与犹疑）对服装的映射属于导演/设计解释，不是服饰史事实。
- historical 模式：年代/文化可行性优先于视觉表现；证据不足时按脚本警告处理，不把推断写成史实。
- 年代/地域匹配为近似层级（脚本警告：no reliable period/region context card after period/region normalization (requested: 1644 late Ming early Qing / jiangnan china)）。
- 年代/地域匹配为近似层级（脚本警告：period evidence is approximate/none for GAR-0071, GAR-0084 (requested 1644 late Ming early Qing); treat these as era-level hypotheses, not exact period matches）。
- 输入未提供的属性保持 unknown，不向服装史或剧作事实补造；本文件的推荐是设计建议而非史料。

## unknown

- 性别呈现（`character.gender_presentation`）：未指定 / unknown，未向生成器发明取值。
- 年龄（`character.age`）：未指定 / unknown，未向生成器发明取值。
- 场次（`scene.scene_id`）：未指定 / unknown，未向生成器发明取值。
- 时间（`scene.time`）：未指定 / unknown，未向生成器发明取值。
- 天气（`scene.weather`）：未指定 / unknown，未向生成器发明取值。
- 动作（`scene.action`）：未指定 / unknown，未向生成器发明取值。
- 地点（`scene.location`）：未指定 / unknown，未向生成器发明取值。
- 湿度状态（`state.wetness`）：未指定 / unknown，未向生成器发明取值。
- 破损状态（`state.damage`）：未指定 / unknown，未向生成器发明取值。
- 污渍状态（`state.dirt`）：未指定 / unknown，未向生成器发明取值。

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T39-明末清初context清洁.json --json` | 0 | 1.18s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py china --limit 6 --json` | 0 | 1.0s |

- `query.py` 命中数量：**6**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0031, GAR-0032, GAR-0067, LOOK-0008, LOOK-0009, LOOK-0012
- `recommend.py` 候选池：accessory=GAR-0028, GAR-0083, GAR-0085, GAR-0021, GAR-0025, GAR-0026; carried_prop=GAR-0049; footwear=GAR-0024, GAR-0084; inner_layer=GAR-0078, GAR-0020; lower_body=GAR-0077, GAR-0013; one_piece=GAR-0071, GAR-0062, GAR-0015; outerwear=GAR-0016, GAR-0076, GAR-0017, GAR-0018; upper_body=GAR-0002, GAR-0008, GAR-0003
- 三套推荐选中：A: GAR-0071, GAR-0024; B: GAR-0071, GAR-0084; C: GAR-0062, GAR-0024

## 候选造型 A/B/C

### Look A（score 32.6/100，cost 0.474，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0071` | 莫卧儿jama / Mughal jama | white, gold, red | cotton_muslin, gold_thread, satin | verified |
| footwear | `GAR-0024` | 穆勒鞋 / mule | red, silk, gold | leather, silk, velvet | verified |

- 结构卡：STR-0016, STR-0017, STR-0025
- 材质卡：MAT-0001, MAT-0012, MAT-0002

### Look B（score 31.7/100，cost 0.474，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0071` | 莫卧儿jama / Mughal jama | white, gold, red | cotton_muslin, gold_thread, satin | verified |
| footwear | `GAR-0084` | 高跟鞋 / high-heeled shoes | black | silk_satin, leather | verified |

- 结构卡：STR-0016, STR-0017
- 材质卡：MAT-0001, MAT-0012, MAT-0002

### Look C（score 26.1/100，cost 0.542，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0062` | 意大利文艺复兴长袍 / Italian Renaissance gown | cream, green, pink, yellow, blue | silk, fustian | verified |
| footwear | `GAR-0024` | 穆勒鞋 / mule | red, silk, gold | leather, silk, velvet | verified |

- 结构卡：STR-0001, STR-0003, STR-0025
- 材质卡：MAT-0002, MAT-0003

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 12.8 | 11.9 | 8.3 |
| 角色身份 | 3.4 | 3.4 | 3.4 |
| 环境气候 | 1.8 | 1.8 | 1.8 |
| 美术方向 | 0.0 | 0.0 | 0.0 |
| 动作可行 | 4.6 | 4.6 | 4.6 |
| 剧情弧线 | 3.5 | 3.5 | 3.5 |
| 摄影/一致性 | 6.5 | 6.5 | 6.5 |
| **总计** | 32.6 | 31.7 | 26.1 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult 顾砚秋, one-piece: Mughal jama, white cotton muslin with gold embroidery, red satin facings at hem and cuffs, courtly South Asian menswear; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, palette: gold, red, silk, white, setting: 书院讲堂, day, overcast, dry, art direction: 文人水墨、克制、低饱和, lighting: 阴天窗光, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); placket (STR-0017); ease and fit (STR-0025), continuity lock: GAR-0071 Mughal jama [white, gold, red; cotton_muslin, gold_thread, satin; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0012, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
顾砚秋, 讲学、整理书箱, scene: 书院讲堂, day, overcast, dry, camera: medium shot, costume: one-piece: Mughal jama, white cotton muslin with gold embroidery, red satin facings at hem and cuffs, courtly South Asian menswear; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, fabric motion: 长袍及膝/及踝、裙摆宽大，快走时下摆展开; 交叉襟与侧系在抬臂时拉扯，需锁定系合位置。, lighting: 阴天窗光, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0071 Mughal jama [white, gold, red; cotton_muslin, gold_thread, satin; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0012, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult 顾砚秋, one-piece: Mughal jama, white cotton muslin with gold embroidery, red satin facings at hem and cuffs, courtly South Asian menswear; footwear: 18th-century women’s black silk satin high-heeled shoes, slender heel, pointed tongue, leather sole, buckled or slip-on, palette: black, gold, red, white, setting: 书院讲堂, day, overcast, dry, art direction: 文人水墨、克制、低饱和, lighting: 阴天窗光, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); placket (STR-0017), continuity lock: GAR-0071 Mughal jama [white, gold, red; cotton_muslin, gold_thread, satin; one-piece] | GAR-0084 high-heeled shoes [black; silk_satin, leather; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0012, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
顾砚秋, 讲学、整理书箱, scene: 书院讲堂, day, overcast, dry, camera: medium shot, costume: one-piece: Mughal jama, white cotton muslin with gold embroidery, red satin facings at hem and cuffs, courtly South Asian menswear; footwear: 18th-century women’s black silk satin high-heeled shoes, slender heel, pointed tongue, leather sole, buckled or slip-on, fabric motion: 长袍及膝/及踝、裙摆宽大，快走时下摆展开; 交叉襟与侧系在抬臂时拉扯，需锁定系合位置。, lighting: 阴天窗光, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0071 Mughal jama [white, gold, red; cotton_muslin, gold_thread, satin; one-piece] | GAR-0084 high-heeled shoes [black; silk_satin, leather; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0012, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult 顾砚秋, one-piece: late Renaissance Italian silk gown, cream brocaded floral motifs, diagonal slashing between motifs, sleeveless open front, small upright back collar, shoulder wings, box-pleated back; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, palette: blue, cream, gold, green, pink, red, silk, yellow, setting: 书院讲堂, day, overcast, dry, art direction: 文人水墨、克制、低饱和, lighting: 阴天窗光, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: Medici collar (STR-0001); ruff (STR-0003); ease and fit (STR-0025), continuity lock: GAR-0062 Italian Renaissance gown [cream, green, pink, yellow, blue; silk, fustian; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
顾砚秋, 讲学、整理书箱, scene: 书院讲堂, day, overcast, dry, camera: medium shot, costume: one-piece: late Renaissance Italian silk gown, cream brocaded floral motifs, diagonal slashing between motifs, sleeveless open front, small upright back collar, shoulder wings, box-pleated back; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, fabric motion: 无袖开襟长袍依赖内层固定; 剪口与金属饰边易勾挂; 长摆限制步幅。, lighting: 阴天窗光, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0062 Italian Renaissance gown [cream, green, pink, yellow, blue; silk, fustian; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories
```

## 风险

### Look A

- 风险：region mismatch in GAR-0071, GAR-0024: cards document their own regions, not jiangnan china
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look B

- 风险：region mismatch in GAR-0071, GAR-0084: cards document their own regions, not jiangnan china
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look C

- 风险：region mismatch in GAR-0062, GAR-0024: cards document their own regions, not jiangnan china
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### 脚本级风险与缺口

- [context_gap/medium] no reliable period/region context card after period/region normalization (requested: 1644 late Ming early Qing / jiangnan china)
- [context_gap/medium] no reliable style card for art direction '文人水墨、克制、低饱和'
- [period_approximate/medium] period evidence is approximate/none for GAR-0071, GAR-0084 (requested 1644 late Ming early Qing); treat these as era-level hypotheses, not exact period matches
- [period_era_level/low] period evidence is era-level (century bucket) for GAR-0024, GAR-0062; exact-decade cards are missing
- [region_mismatch/medium] cards document other regions for GAR-0024, GAR-0062, GAR-0084 (requested jiangnan china); cross-region borrowing is flagged, not silently accepted
- [occupation_coverage_gap/medium] the vault has no '书院教师、江南文人'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- [budget_equivalent/medium] No cheaper distinct combination was available in the vault; Look C is an art-direction alternative at equivalent cost, explicitly explained.
- no reliable period/region context card after period/region normalization (requested: 1644 late Ming early Qing / jiangnan china)
- no reliable style card for art direction '文人水墨、克制、低饱和'
- period evidence is approximate/none for GAR-0071, GAR-0084 (requested 1644 late Ming early Qing); treat these as era-level hypotheses, not exact period matches
- period evidence is era-level (century bucket) for GAR-0024, GAR-0062; exact-decade cards are missing
- cards document other regions for GAR-0024, GAR-0062, GAR-0084 (requested jiangnan china); cross-region borrowing is flagged, not silently accepted
- the vault has no '书院教师、江南文人'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- No cheaper distinct combination was available in the vault; Look C is an art-direction alternative at equivalent cost, explicitly explained.

## 证据

### Look A

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 12.8/25, 摄影/一致性 6.5/10
- 理由（解释性，不是史实）：连身: GAR-0071 莫卧儿jama (formal)
- 理由（解释性，不是史实）：足部: GAR-0024 穆勒鞋 (formal)
- 理由（解释性，不是史实）：linked structure cards: STR-0016, STR-0017, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0001, MAT-0012, MAT-0002
- source_ids：SRC-0450, SRC-0451, SRC-0452, SRC-0125, SRC-0202, SRC-0201, SRC-0108, SRC-0412, SRC-0521, SRC-0520, SRC-0102, SRC-0423, SRC-0141
- 来源链接：SRC-0450 → https://collections.vam.ac.uk/item/O144142/
- 来源链接：SRC-0451 → https://collections.vam.ac.uk/item/O109190/
- 来源链接：SRC-0452 → https://collections.vam.ac.uk/item/O438362/
- 来源链接：SRC-0125 → https://fashionhistory.fitnyc.edu/mule/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0108 → https://fashionhistory.fitnyc.edu/shirtwaist/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 单件证据状态：GAR-0071=verified; GAR-0024=verified

### Look B

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 11.9/25, 摄影/一致性 6.5/10
- 理由（解释性，不是史实）：连身: GAR-0071 莫卧儿jama (formal)
- 理由（解释性，不是史实）：足部: GAR-0084 高跟鞋 (formal)
- 理由（解释性，不是史实）：linked structure cards: STR-0016, STR-0017
- 理由（解释性，不是史实）：linked material cards: MAT-0001, MAT-0012, MAT-0002
- source_ids：SRC-0450, SRC-0451, SRC-0452, SRC-0524, SRC-0202, SRC-0201, SRC-0108, SRC-0412, SRC-0102, SRC-0423, SRC-0141
- 来源链接：SRC-0450 → https://collections.vam.ac.uk/item/O144142/
- 来源链接：SRC-0451 → https://collections.vam.ac.uk/item/O109190/
- 来源链接：SRC-0452 → https://collections.vam.ac.uk/item/O438362/
- 来源链接：SRC-0524 → https://collections.vam.ac.uk/item/O74856/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0108 → https://fashionhistory.fitnyc.edu/shirtwaist/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 单件证据状态：GAR-0071=verified; GAR-0084=verified

### Look C

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 8.3/25, 摄影/一致性 6.5/10
- 理由（解释性，不是史实）：连身: GAR-0062 意大利文艺复兴长袍 (formal)
- 理由（解释性，不是史实）：足部: GAR-0024 穆勒鞋 (formal)
- 理由（解释性，不是史实）：linked structure cards: STR-0001, STR-0003, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0003
- source_ids：SRC-0422, SRC-0125, SRC-0101, SRC-0133, SRC-0521, SRC-0520, SRC-0141, SRC-0142
- 来源链接：SRC-0422 → https://collections.vam.ac.uk/item/O74085/
- 来源链接：SRC-0125 → https://fashionhistory.fitnyc.edu/mule/
- 来源链接：SRC-0101 → https://fashionhistory.fitnyc.edu/medici-collar/
- 来源链接：SRC-0133 → https://fashionhistory.fitnyc.edu/ruff/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 单件证据状态：GAR-0062=verified; GAR-0024=verified

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| structured_result | PASS | exit=0 looks=3 ids_exist=True warnings=True |
| warning_absent:rainwear_gap | PASS | warning 'rainwear_gap' present? False (codes=['context_gap', 'context_gap', 'period_approximate', 'period_era_level', 'region_mismatch', 'occupation_coverage_gap', 'budget_equivalent']) |
| warnings_present | PASS | wytyczne count=7 codes=['context_gap', 'context_gap', 'period_approximate', 'period_era_level', 'region_mismatch', 'occupation_coverage_gap', 'budget_equivalent'] |
| context_refs_clean | PASS | refs=0 bad=[] example_refs=[] |
| no_example_in_a | PASS | Look A example ids=[] contains_example=False |
| narrative_present | PASS | missing narrative for none |
| no_prompt_contamination | PASS | no cross-scene/card-text contamination |
| query_hits | PASS | query.py exit=0, hits=6, ids=GAR-0031, GAR-0032, GAR-0067, LOOK-0008, LOOK-0009, LOOK-0012 |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable period/region context card after period/region normalization (requested: 1644 late Ming early Qing / jiangnan china)
- 脚本警告：no reliable style card for art direction '文人水墨、克制、低饱和'
- 脚本警告：period evidence is approximate/none for GAR-0071, GAR-0084 (requested 1644 late Ming early Qing); treat these as era-level hypotheses, not exact period matches
- 脚本警告：period evidence is era-level (century bucket) for GAR-0024, GAR-0062; exact-decade cards are missing
- 脚本警告：cards document other regions for GAR-0024, GAR-0062, GAR-0084 (requested jiangnan china); cross-region borrowing is flagged, not silently accepted
- 脚本警告：the vault has no '书院教师、江南文人'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- 脚本警告：No cheaper distinct combination was available in the vault; Look C is an art-direction alternative at equivalent cost, explicitly explained.
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

