# T30 — 自由文本 --brief：规则化剧本/人物解析

- 运行时间：2026-11-04T02:25:39+08:00
- 测试类型：brief_parsing, 1930s_shanghai
- 模式：standard
- 输入文件：`11-验收/测试输入/T30-自由文本brief解析.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py --brief 1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office --json`
- 退出码：**0**（耗时 1.47s）

## 实际输入

```json
{
  "brief": "1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office"
}
```

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py --brief 1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office --json` | 0 | 1.47s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py 1930s --type garment --limit 6 --json` | 0 | 0.73s |

- `query.py` 命中数量：**6**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0035, GAR-0060, GAR-0034, GAR-0048, GAR-0031, GAR-0032
- `recommend.py` 候选池：accessory=GAR-0066, GAR-0067, GAR-0068, GAR-0021, GAR-0028, GAR-0050, GAR-0051, GAR-0039, GAR-0026, GAR-0070; carried_prop=GAR-0048, GAR-0047; footwear=GAR-0060, GAR-0022, GAR-0058, GAR-0044, GAR-0023, GAR-0035; inner_layer=GAR-0012, GAR-0020; lower_body=GAR-0014, GAR-0010, GAR-0011, GAR-0059; one_piece=GAR-0031, GAR-0064, GAR-0032, GAR-0063, GAR-0069, GAR-0053, GAR-0055, GAR-0056, GAR-0052, GAR-0054; outerwear=GAR-0037, GAR-0045, GAR-0057, GAR-0019, GAR-0033, GAR-0041, GAR-0040, GAR-0017; set=GAR-0065, GAR-0001, GAR-0042, GAR-0036; upper_body=GAR-0008, GAR-0034, GAR-0007, GAR-0006, GAR-0043
- 三套推荐选中：A: GAR-0032, GAR-0037, GAR-0060; B: GAR-0031, GAR-0037, GAR-0060; C: GAR-0031, GAR-0037, GAR-0022

## 候选造型 A/B/C

### Look A（score 50.6/100，cost 0.401，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0032` | 长衫 / changshan | cream_white | silk, gauze_silk | verified |
| outerwear | `GAR-0037` | 消防防护外套 / firefighter jacket | indigo, white | cotton | verified |
| footwear | `GAR-0060` | 1930 年代男式皮鞋 / 1930s men’s Oxford shoes | tan, white, brown | leather, suede | verified |

- 结构卡：STR-0011
- 材质卡：MAT-0002, MAT-0003, MAT-0001

### Look B（score 50.5/100，cost 0.351，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0037` | 消防防护外套 / firefighter jacket | indigo, white | cotton | verified |
| footwear | `GAR-0060` | 1930 年代男式皮鞋 / 1930s men’s Oxford shoes | tan, white, brown | leather, suede | verified |

- 结构卡：STR-0011
- 材质卡：MAT-0002, MAT-0003, MAT-0001

### Look C（score 50.4/100，cost 0.287，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0037` | 消防防护外套 / firefighter jacket | indigo, white | cotton | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0011
- 材质卡：MAT-0002, MAT-0003, MAT-0001

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 17.7 | 17.7 | 17.2 |
| 角色身份 | 2.8 | 3.4 | 3.9 |
| 环境气候 | 9.6 | 9.7 | 10.0 |
| 美术方向 | 5.2 | 6.7 | 6.3 |
| 动作可行 | 4.4 | 4.0 | 4.0 |
| 剧情弧线 | 3.5 | 3.5 | 3.5 |
| 摄影/一致性 | 6.5 | 6.5 | 6.5 |
| **总计** | 50.6 | 50.5 | 50.4 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Chinese man’s changshan, full-length cream-white figured gauze silk robe, small stand-up collar, right-side fastening with five loop-and-knot buttons, long tight sleeves, straight cuffs, side slits, unlined; outer layer: Japanese firefighter’s jacket, indigo resist-dyed quilted cotton, reversible, matoi crest on back, sashiko stitching, heavy and water-soaked; footwear: 1930s men’s Oxford shoes, polished tan leather with white suede panels, narrow pointed toe, six pairs of lace holes, leather sole, closed-tab construction, palette: brown, cream white, indigo, tan, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011), continuity lock: GAR-0032 changshan [cream_white; silk, gauze_silk; one-piece] | GAR-0037 firefighter jacket [indigo, white; cotton; outer layer] | GAR-0060 1930s men’s Oxford shoes [tan, white, brown; leather, suede; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Chinese man’s changshan, full-length cream-white figured gauze silk robe, small stand-up collar, right-side fastening with five loop-and-knot buttons, long tight sleeves, straight cuffs, side slits, unlined; outer layer: Japanese firefighter’s jacket, indigo resist-dyed quilted cotton, reversible, matoi crest on back, sashiko stitching, heavy and water-soaked; footwear: 1930s men’s Oxford shoes, polished tan leather with white suede panels, narrow pointed toe, six pairs of lace holes, leather sole, closed-tab construction, fabric motion: 厚绗缝棉限制抬臂; 浸湿后重量大增、行动变慢，镜头需体现湿重感。; 两侧开衩提供步幅，但仍限制大步/跑动; 长而紧的袖限制手腕; 长摆上下楼梯需提摆，镜头间需保持提摆/放下状态一致。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0032 changshan [cream_white; silk, gauze_silk; one-piece] | GAR-0037 firefighter jacket [indigo, white; cotton; outer layer] | GAR-0060 1930s men’s Oxford shoes [tan, white, brown; leather, suede; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: Japanese firefighter’s jacket, indigo resist-dyed quilted cotton, reversible, matoi crest on back, sashiko stitching, heavy and water-soaked; footwear: 1930s men’s Oxford shoes, polished tan leather with white suede panels, narrow pointed toe, six pairs of lace holes, leather sole, closed-tab construction, palette: brown, indigo, mid blue, orange red, pink, tan, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0037 firefighter jacket [indigo, white; cotton; outer layer] | GAR-0060 1930s men’s Oxford shoes [tan, white, brown; leather, suede; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: Japanese firefighter’s jacket, indigo resist-dyed quilted cotton, reversible, matoi crest on back, sashiko stitching, heavy and water-soaked; footwear: 1930s men’s Oxford shoes, polished tan leather with white suede panels, narrow pointed toe, six pairs of lace holes, leather sole, closed-tab construction, fabric motion: 厚绗缝棉限制抬臂; 浸湿后重量大增、行动变慢，镜头需体现湿重感。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0037 firefighter jacket [indigo, white; cotton; outer layer] | GAR-0060 1930s men’s Oxford shoes [tan, white, brown; leather, suede; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: Japanese firefighter’s jacket, indigo resist-dyed quilted cotton, reversible, matoi crest on back, sashiko stitching, heavy and water-soaked; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: black, brown, indigo, mid blue, orange red, pink, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0037 firefighter jacket [indigo, white; cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: Japanese firefighter’s jacket, indigo resist-dyed quilted cotton, reversible, matoi crest on back, sashiko stitching, heavy and water-soaked; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 厚绗缝棉限制抬臂; 浸湿后重量大增、行动变慢，镜头需体现湿重感。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0037 firefighter jacket [indigo, white; cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 17.7/25, 环境气候 9.6/15
- 理由：连身: GAR-0032 长衫 (formal)
- 理由：外层: GAR-0037 消防防护外套 (functional)
- 理由：足部: GAR-0060 1930 年代男式皮鞋 (smart_casual)
- 理由：linked structure cards: STR-0011
- 理由：linked material cards: MAT-0002, MAT-0003, MAT-0001
- 风险：region mismatch in GAR-0037, GAR-0060: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0202, SRC-0401, SRC-0420, SRC-0200, SRC-0141, SRC-0142, SRC-0102
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0401 → https://collections.vam.ac.uk/item/O1803042/
- 来源链接：SRC-0420 → https://collections.vam.ac.uk/item/O135417/
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

### Look B

- 理由：highest scoring dimensions: 年代/文化 17.7/25, 环境气候 9.7/15
- 理由：连身: GAR-0031 旗袍 (smart_casual)
- 理由：外层: GAR-0037 消防防护外套 (functional)
- 理由：足部: GAR-0060 1930 年代男式皮鞋 (smart_casual)
- 理由：linked structure cards: STR-0011
- 理由：linked material cards: MAT-0002, MAT-0003, MAT-0001
- 风险：region mismatch in GAR-0037, GAR-0060: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0200, SRC-0201, SRC-0401, SRC-0420, SRC-0202, SRC-0141, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0401 → https://collections.vam.ac.uk/item/O1803042/
- 来源链接：SRC-0420 → https://collections.vam.ac.uk/item/O135417/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

### Look C

- 理由：highest scoring dimensions: 年代/文化 17.2/25, 环境气候 10.0/15
- 理由：连身: GAR-0031 旗袍 (smart_casual)
- 理由：外层: GAR-0037 消防防护外套 (functional)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked structure cards: STR-0011
- 理由：linked material cards: MAT-0002, MAT-0003, MAT-0001
- 风险：region mismatch in GAR-0037, GAR-0022: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0200, SRC-0201, SRC-0401, SRC-0123, SRC-0202, SRC-0141, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0401 → https://collections.vam.ac.uk/item/O1803042/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| three_looks | PASS | looks=3, distinct=True, checks={'three_looks': True, 'looks_distinct': True} |
| ids_exist | PASS | all garment ids resolvable: True |
| no_crash | PASS | recommend.py exit=0 (must be 0, no KeyError/uncaught exception) |
| no_example_in_a | PASS | Look A example ids=[] contains_example=False |
| abc_distinct | PASS | checks.abc_distinct=True differences={'a_b': 2, 'a_c': 4, 'b_c': 2} |
| narrative_present | PASS | missing narrative for none |
| warnings_present | PASS | wytyczne count=8 codes=['context_gap', 'period_approximate', 'period_era_level', 'region_mismatch', 'occupation_coverage_gap', 'rainwear_gap', 'conflict_weather_vs_material', 'brief_unknown_fields'] |
| prompts | PASS | all prompts complete |
| no_prompt_contamination | PASS | no cross-scene/card-text contamination |
| context_refs_clean | PASS | refs=2 bad=[] example_refs=[] |
| evidence_coverage | PASS | items with source_ids=9/9; looks with evidence=3/3 |
| query_hits | PASS | query.py exit=0, hits=6, ids=GAR-0035, GAR-0060, GAR-0034, GAR-0048, GAR-0031, GAR-0032 |
| brief_parsed | PASS | brief_parse fields=['period', 'region', 'occupation'] acknowledged_unknown=['season'] |
| period_coverage | PASS | period evidence tiers={'one_piece': 'exact', 'outerwear': 'approximate', 'footwear': 'era'} |

**VERDICT: PASS**

## 备注

- 脚本警告：no upper_body candidates retrieved
- 脚本警告：no lower_body candidates retrieved
- 脚本警告：no reliable style card for art direction 'noir'
- 脚本警告：period evidence is approximate/none for GAR-0037 (requested 1930s); treat these as era-level hypotheses, not exact period matches
- 脚本警告：period evidence is era-level (century bucket) for GAR-0022; exact-decade cards are missing
- 脚本警告：cards document other regions for GAR-0022, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- 脚本警告：no occupational garment cards match 'journalist / editor'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- 脚本警告：outerwear GAR-0037 has no documented weather protection; rainwear cards are missing
- 脚本警告：wet/snow weather with delicate footwear GAR-0060 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- 脚本警告：brief parser left these fields unknown: season
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

