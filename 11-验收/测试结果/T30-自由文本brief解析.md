# T30 — 自由文本 --brief：规则化剧本/人物解析

- 运行时间：2026-11-04T16:19:51+08:00
- 测试类型：brief_parsing, 1930s_shanghai
- 模式：standard
- 输入文件：`11-验收/测试输入/T30-自由文本brief解析.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py --brief 1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office --json`
- 退出码：**0**（耗时 1.27s）

## 实际输入

```json
{
  "brief": "1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office"
}
```

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py --brief 1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate, walking to the newspaper office --json` | 0 | 1.27s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py 1930s --type garment --limit 6 --json` | 0 | 0.91s |

- `query.py` 命中数量：**6**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0031, GAR-0032, GAR-0034, GAR-0035, GAR-0048, GAR-0060
- `recommend.py` 候选池：accessory=GAR-0066, GAR-0067, GAR-0068, GAR-0021, GAR-0028, GAR-0026, GAR-0070, GAR-0086, GAR-0074, GAR-0073; carried_prop=GAR-0048, GAR-0087, GAR-0047; footwear=GAR-0060, GAR-0022, GAR-0058, GAR-0023, GAR-0035; inner_layer=GAR-0012, GAR-0078, GAR-0020; lower_body=GAR-0072, GAR-0014, GAR-0010, GAR-0011, GAR-0077; one_piece=GAR-0031, GAR-0064, GAR-0032, GAR-0071, GAR-0063, GAR-0069, GAR-0053, GAR-0055, GAR-0056, GAR-0052, GAR-0054; outerwear=GAR-0045; set=GAR-0065, GAR-0001; upper_body=GAR-0008, GAR-0034, GAR-0007, GAR-0006
- 三套推荐选中：A: GAR-0031, GAR-0045, GAR-0035, GAR-0047; B: GAR-0031, GAR-0045, GAR-0035, GAR-0048; C: GAR-0031, GAR-0045, GAR-0060

## 候选造型 A/B/C

### Look A（score 48.1/100，cost 0.358，source_look=LOOK-0012）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |
| carried_prop | `GAR-0047` | 雨伞 / umbrella | black, silver | silk, silver, wood | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0025
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012

### Look B（score 49.3/100，cost 0.317，source_look=LOOK-0015）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |
| carried_prop | `GAR-0048` | 手提包 / handbag | multicolor | canvas, wool | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0025, STR-0019
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011

### Look C（score 48.0/100，cost 0.347，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0060` | 1930 年代男式皮鞋 / 1930s men’s Oxford shoes | tan, white, brown | leather, suede | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0020
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 14.2 | 14.4 | 14.9 |
| 角色身份 | 4.1 | 4.1 | 3.8 |
| 环境气候 | 7.2 | 8.1 | 9.7 |
| 美术方向 | 6.1 | 6.1 | 6.2 |
| 动作可行 | 4.6 | 4.7 | 4.3 |
| 剧情弧线 | 3.5 | 3.5 | 3.5 |
| 摄影/一致性 | 6.5 | 6.5 | 6.5 |
| **总计** | 48.1 | 49.3 | 48.0 |

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
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: 1930s embroidered canvas handbag, cross-stitch wool floral pattern, fabric handle, small framed purse, carried in hand or on wrist, palette: beige, black, khaki, lavender, mid blue, multicolor, orange red, pink, red, silver, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); ease and fit (STR-0025); zipper (STR-0019), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0048 handbag [multicolor; canvas, wool; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: 1930s embroidered canvas handbag, cross-stitch wool floral pattern, fabric handle, small framed purse, carried in hand or on wrist, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0048 handbag [multicolor; canvas, wool; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult unnamed character, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s men’s Oxford shoes, polished tan leather with white suede panels, narrow pointed toe, six pairs of lace holes, leather sole, closed-tab construction, palette: beige, brown, khaki, lavender, mid blue, orange red, pink, tan, white, setting: unspecified location, unknown, rain, art direction: noir, lighting: unknown, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); panels and gores (STR-0020), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0060 1930s men’s Oxford shoes [tan, white, brown; leather, suede; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001
```

**Video prompt (EN):**

```
unnamed character, walking, scene: unspecified location, unknown, rain, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s men’s Oxford shoes, polished tan leather with white suede panels, narrow pointed toe, six pairs of lace holes, leather sole, closed-tab construction, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: unknown, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0060 1930s men’s Oxford shoes [tan, white, brown; leather, suede; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 14.2/25, 环境气候 7.2/15
- 理由：连身: GAR-0031 旗袍 (smart_casual)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由：携带物: GAR-0047 雨伞 (smart_casual)
- 理由：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0025
- 理由：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012
- 理由：based on curated vault look card LOOK-0012
- 风险：region mismatch in GAR-0045, GAR-0035, GAR-0047: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0200, SRC-0201, SRC-0405, SRC-0205, SRC-0206, SRC-0407, SRC-0202, SRC-0486, SRC-0521, SRC-0520, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0205 → https://collections.vam.ac.uk/item/O350849/
- 来源链接：SRC-0206 → https://collections.vam.ac.uk/item/O350850/
- 来源链接：SRC-0407 → https://collections.vam.ac.uk/item/O470711/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

### Look B

- 理由：highest scoring dimensions: 年代/文化 14.4/25, 环境气候 8.1/15
- 理由：连身: GAR-0031 旗袍 (smart_casual)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由：携带物: GAR-0048 手提包 (smart_casual)
- 理由：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0025, STR-0019
- 理由：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011
- 理由：based on curated vault look card LOOK-0015
- 风险：region mismatch in GAR-0045, GAR-0035, GAR-0048: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0200, SRC-0201, SRC-0205, SRC-0206, SRC-0408, SRC-0405, SRC-0202, SRC-0486, SRC-0521, SRC-0520, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0205 → https://collections.vam.ac.uk/item/O350849/
- 来源链接：SRC-0206 → https://collections.vam.ac.uk/item/O350850/
- 来源链接：SRC-0408 → https://collections.vam.ac.uk/item/O367714/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

### Look C

- 理由：highest scoring dimensions: 年代/文化 14.9/25, 环境气候 9.7/15
- 理由：连身: GAR-0031 旗袍 (smart_casual)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0060 1930 年代男式皮鞋 (smart_casual)
- 理由：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0020
- 理由：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001
- 风险：region mismatch in GAR-0045, GAR-0060: cards document their own regions, not shanghai
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0200, SRC-0201, SRC-0405, SRC-0420, SRC-0202, SRC-0486, SRC-0451, SRC-0453, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0420 → https://collections.vam.ac.uk/item/O135417/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0451 → https://collections.vam.ac.uk/item/O109190/
- 来源链接：SRC-0453 → https://collections.vam.ac.uk/item/O163754/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| three_looks | PASS | looks=3, distinct=True, checks={'three_looks': True, 'looks_distinct': True} |
| ids_exist | PASS | all garment ids resolvable: True |
| no_crash | PASS | recommend.py exit=0 (must be 0, no KeyError/uncaught exception) |
| no_example_in_a | PASS | Look A example ids=[] contains_example=False |
| abc_distinct | PASS | checks.abc_distinct=True differences={'a_b': 2, 'a_c': 3, 'b_c': 3} |
| narrative_present | PASS | missing narrative for none |
| warnings_present | PASS | wytyczne count=5 codes=['context_gap', 'period_era_level', 'region_mismatch', 'conflict_weather_vs_material', 'brief_unknown_fields'] |
| prompts | PASS | all prompts complete |
| no_prompt_contamination | PASS | no cross-scene/card-text contamination |
| context_refs_clean | PASS | refs=2 bad=[] example_refs=[] |
| evidence_coverage | PASS | items with source_ids=11/11; looks with evidence=3/3 |
| query_hits | PASS | query.py exit=0, hits=6, ids=GAR-0031, GAR-0032, GAR-0034, GAR-0035, GAR-0048, GAR-0060 |
| brief_parsed | PASS | brief_parse fields=['period', 'region', 'occupation'] acknowledged_unknown=['season'] |
| period_coverage | PASS | period evidence tiers={'one_piece': 'exact', 'outerwear': 'era', 'footwear': 'exact', 'carried_prop': 'exact'} |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable style card for art direction 'noir'
- 脚本警告：period evidence is era-level (century bucket) for GAR-0045, GAR-0047; exact-decade cards are missing
- 脚本警告：cards document other regions for GAR-0035, GAR-0045, GAR-0047, GAR-0048, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- 脚本警告：wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

