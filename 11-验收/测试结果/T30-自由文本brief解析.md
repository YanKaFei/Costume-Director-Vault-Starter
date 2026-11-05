# T30 — 自由文本 --brief：规则化剧本/人物解析

- 运行时间：2026-11-05T16:00:44+08:00
- 测试类型：brief_parsing, 1930s_shanghai
- 模式：standard
- 输入文件：`11-验收/测试输入/T30-自由文本brief解析.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py --brief 1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office --json`
- 退出码：**0**（耗时 1.54s）

## 实际输入

```json
{
  "brief": "1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office"
}
```

## 已知输入

以下字段来自测试输入文件，是**已知条件**（不是模型推断）：

- （输入中没有可用的已知字段）

## 假设

- 预算未在输入中给出：按库内默认成本策略处理，C 套仅作低预算替代提示。
- 输入未提供的属性保持 unknown，不向服装史或剧作事实补造；本文件的推荐是设计建议而非史料。

## unknown

- 角色名（`character.name`）：未指定 / unknown，未向生成器发明取值。
- 性别呈现（`character.gender_presentation`）：未指定 / unknown，未向生成器发明取值。
- 年龄（`character.age`）：未指定 / unknown，未向生成器发明取值。
- 职业（`character.occupation`）：未指定 / unknown，未向生成器发明取值。
- 经济状态（`character.economic_status`）：未指定 / unknown，未向生成器发明取值。
- 人物弧线（`character.arc`）：未指定 / unknown，未向生成器发明取值。
- 年代（`period`）：未指定 / unknown，未向生成器发明取值。
- 地域（`region`）：未指定 / unknown，未向生成器发明取值。
- 季节（`season`）：未指定 / unknown，未向生成器发明取值。
- 场次（`scene.scene_id`）：未指定 / unknown，未向生成器发明取值。
- 时间（`scene.time`）：未指定 / unknown，未向生成器发明取值。
- 天气（`scene.weather`）：未指定 / unknown，未向生成器发明取值。
- 动作（`scene.action`）：未指定 / unknown，未向生成器发明取值。
- 地点（`scene.location`）：未指定 / unknown，未向生成器发明取值。
- 美术方向（`art_direction`）：未指定 / unknown，未向生成器发明取值。
- 摄影光线（`lighting`）：未指定 / unknown，未向生成器发明取值。
- 景别（`camera`）：未指定 / unknown，未向生成器发明取值。
- 预算（`budget`）：未指定 / unknown，未向生成器发明取值。
- 严格度模式（`fidelity_mode`）：未指定 / unknown，未向生成器发明取值。
- 生成工具（`tool`）：未指定 / unknown，未向生成器发明取值。
- 湿度状态（`state.wetness`）：未指定 / unknown，未向生成器发明取值。
- 破损状态（`state.damage`）：未指定 / unknown，未向生成器发明取值。
- 污渍状态（`state.dirt`）：未指定 / unknown，未向生成器发明取值。

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py --brief 1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office --json` | 0 | 1.54s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py 1930s --type garment --limit 6 --json` | 0 | 1.17s |

- `query.py` 命中数量：**6**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0031, GAR-0032, GAR-0034, GAR-0035, GAR-0048, GAR-0060
- `recommend.py` 候选池：accessory=GAR-0066, GAR-0067, GAR-0021, GAR-0068, GAR-0088, GAR-0028, GAR-0089, GAR-0026, GAR-0070, GAR-0086, GAR-0073, GAR-0074, GAR-0090; carried_prop=GAR-0048, GAR-0087, GAR-0047; footwear=GAR-0022, GAR-0060, GAR-0058, GAR-0091, GAR-0023, GAR-0035; inner_layer=GAR-0012, GAR-0078, GAR-0020; lower_body=GAR-0072, GAR-0014, GAR-0010, GAR-0011, GAR-0077; one_piece=GAR-0031, GAR-0064, GAR-0032, GAR-0071, GAR-0063, GAR-0069, GAR-0053, GAR-0055, GAR-0056, GAR-0052, GAR-0054; outerwear=GAR-0045; set=GAR-0065, GAR-0001; upper_body=GAR-0008, GAR-0034, GAR-0007, GAR-0006
- 三套推荐选中：A: GAR-0031, GAR-0045, GAR-0035, GAR-0047; B: GAR-0031, GAR-0045, GAR-0035, GAR-0048; C: GAR-0031, GAR-0045, GAR-0022

## 候选造型 A/B/C

### Look A（score 47.1/100，cost 0.358，source_look=LOOK-0012）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |
| carried_prop | `GAR-0047` | 雨伞 / umbrella | black, silver | silk, silver, wood | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0025
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012

### Look B（score 48.3/100，cost 0.317，source_look=LOOK-0015）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |
| carried_prop | `GAR-0048` | 手提包 / handbag | multicolor | canvas, wool | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0025, STR-0019, STR-0026
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0015

### Look C（score 46.9/100，cost 0.282，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0021, STR-0025
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0017, MAT-0019

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 14.2 | 14.4 | 14.5 |
| 角色身份 | 4.1 | 4.1 | 4.2 |
| 环境气候 | 7.2 | 8.1 | 10.0 |
| 美术方向 | 5.1 | 5.1 | 4.8 |
| 动作可行 | 4.6 | 4.7 | 4.3 |
| 剧情弧线 | 3.5 | 3.5 | 3.5 |
| 摄影/一致性 | 6.5 | 6.5 | 6.5 |
| **总计** | 47.1 | 48.3 | 46.9 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: black silk umbrella, silver handle with engraved hunting scenes, slim wooden shaft, rain-wet silk canopy, carried in one hand, palette: beige, black, khaki, lavender, mid blue, orange red, pink, red, silver, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); ease and fit (STR-0025), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0047 umbrella [black, silver; silk, silver, wood; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: black silk umbrella, silver handle with engraved hunting scenes, slim wooden shaft, rain-wet silk canopy, carried in one hand, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0047 umbrella [black, silver; silk, silver, wood; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: 1930s embroidered canvas handbag, cross-stitch wool floral pattern, fabric handle, small framed purse, carried in hand or on wrist, palette: beige, black, khaki, lavender, mid blue, multicolor, orange red, pink, red, silver, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); ease and fit (STR-0025); zipper (STR-0019); handbag construction (STR-0026), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0048 handbag [multicolor; canvas, wool; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0015
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: 1930s embroidered canvas handbag, cross-stitch wool floral pattern, fabric handle, small framed purse, carried in hand or on wrist, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0048 handbag [multicolor; canvas, wool; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0015, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, brown, khaki, lavender, mid blue, orange red, pink, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); seams and darts (STR-0021); ease and fit (STR-0025), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0017, MAT-0019
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0017, MAT-0019, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

## 风险

### Look A

- 风险：region mismatch in GAR-0045, GAR-0035, GAR-0047: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look B

- 风险：region mismatch in GAR-0045, GAR-0035, GAR-0048: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look C

- 风险：region mismatch in GAR-0045, GAR-0022: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### 脚本级风险与缺口

- [period_era_level/low] period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- [region_mismatch/medium] cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- [conflict_weather_vs_material/medium] wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- [brief_unknown_fields/info] brief parser left these fields unknown: season
- period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot

## 证据

### Look A

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 14.2/25, 环境气候 7.2/15
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由（解释性，不是史实）：携带物: GAR-0047 雨伞 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012
- 理由（解释性，不是史实）：based on curated vault look card LOOK-0012
- source_ids：SRC-0200, SRC-0201, SRC-0405, SRC-0205, SRC-0206, SRC-0407, SRC-0202, SRC-0062, SRC-0486, SRC-0521, SRC-0520, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0205 → https://collections.vam.ac.uk/item/O350849/
- 来源链接：SRC-0206 → https://collections.vam.ac.uk/item/O350850/
- 来源链接：SRC-0407 → https://collections.vam.ac.uk/item/O470711/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0062 → https://www.gutenberg.org/cache/epub/21534/pg21534.txt
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 单件证据状态：GAR-0031=verified; GAR-0045=verified; GAR-0035=verified; GAR-0047=verified

### Look B

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 14.4/25, 环境气候 8.1/15
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由（解释性，不是史实）：携带物: GAR-0048 手提包 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0025, STR-0019, STR-0026
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0015
- 理由（解释性，不是史实）：based on curated vault look card LOOK-0015
- source_ids：SRC-0200, SRC-0201, SRC-0205, SRC-0206, SRC-0408, SRC-0405, SRC-0202, SRC-0062, SRC-0486, SRC-0521, SRC-0520, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102, SRC-0547, SRC-0534, SRC-0204, SRC-0066
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0205 → https://collections.vam.ac.uk/item/O350849/
- 来源链接：SRC-0206 → https://collections.vam.ac.uk/item/O350850/
- 来源链接：SRC-0408 → https://collections.vam.ac.uk/item/O367714/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0062 → https://www.gutenberg.org/cache/epub/21534/pg21534.txt
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0547 → https://vocab.getty.edu/page/aat/300243430
- 来源链接：SRC-0534 → https://collections.vam.ac.uk/item/O353447/
- 来源链接：SRC-0204 → https://collections.vam.ac.uk/item/O110441/
- 来源链接：SRC-0066 → https://www.gutenberg.org/cache/epub/76299/pg76299.txt
- 单件证据状态：GAR-0031=verified; GAR-0045=verified; GAR-0035=verified; GAR-0048=verified

### Look C

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 14.5/25, 环境气候 10.0/15
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0021, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0017, MAT-0019
- source_ids：SRC-0200, SRC-0201, SRC-0405, SRC-0123, SRC-0202, SRC-0062, SRC-0486, SRC-0484, SRC-0412, SRC-0520, SRC-0521, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102, SRC-0549, SRC-0489, SRC-0538, SRC-0550, SRC-0417, SRC-0406
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0062 → https://www.gutenberg.org/cache/epub/21534/pg21534.txt
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0484 → https://collections.vam.ac.uk/item/O356786/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0549 → https://vocab.getty.edu/page/aat/300011845
- 来源链接：SRC-0489 → https://collections.vam.ac.uk/item/O107847/
- 来源链接：SRC-0538 → https://collections.vam.ac.uk/item/O356431/
- 来源链接：SRC-0550 → https://vocab.getty.edu/page/aat/300014058
- 来源链接：SRC-0417 → https://fashionhistory.fitnyc.edu/1963-1969-andre-courreges-coat/
- 来源链接：SRC-0406 → https://collections.vam.ac.uk/item/O361727/
- 单件证据状态：GAR-0031=verified; GAR-0045=verified; GAR-0022=verified

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| three_looks | PASS | looks=3, distinct=True, checks={'three_looks': True, 'looks_distinct': True} |
| ids_exist | PASS | all garment ids resolvable: True |
| no_crash | PASS | recommend.py exit=0 (must be 0, no KeyError/uncaught exception) |
| no_example_in_a | PASS | Look A example ids=[] contains_example=False |
| abc_distinct | PASS | checks.abc_distinct=True differences={'a_b': 2, 'a_c': 3, 'b_c': 3} |
| narrative_present | PASS | missing narrative for none |
| warnings_present | PASS | wytyczne count=4 codes=['period_era_level', 'region_mismatch', 'conflict_weather_vs_material', 'brief_unknown_fields'] |
| prompts | PASS | all prompts complete |
| no_prompt_contamination | PASS | no cross-scene/card-text contamination |
| context_refs_clean | PASS | refs=3 bad=[] example_refs=[] |
| evidence_coverage | PASS | items with source_ids=11/11; looks with evidence=3/3 |
| query_hits | PASS | query.py exit=0, hits=6, ids=GAR-0031, GAR-0032, GAR-0034, GAR-0035, GAR-0048, GAR-0060 |
| brief_parsed | PASS | brief_parse fields=['period', 'region', 'occupation'] acknowledged_unknown=['season'] |
| period_coverage | PASS | period evidence tiers={'one_piece': 'exact', 'outerwear': 'era', 'footwear': 'era', 'carried_prop': 'exact'} |

**VERDICT: PASS**

## 备注

- 脚本警告：period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- 脚本警告：cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- 脚本警告：wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

