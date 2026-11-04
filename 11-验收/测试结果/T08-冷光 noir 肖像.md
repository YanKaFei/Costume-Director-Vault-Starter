# T08 — 冷光肖像：同一角色的冷暖光对照（cool lighting）

- 运行时间：2026-11-04T16:18:57+08:00
- 测试类型：warm_cool_lighting
- 模式：standard
- 输入文件：`11-验收/测试输入/T08-冷光 noir 肖像.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T08-冷光 noir 肖像.json --json`
- 退出码：**0**（耗时 1.79s）

## 实际输入

```json
{
  "character": {
    "name": "Lin",
    "occupation": "private investigator",
    "economic_status": "low",
    "arc": "closing in on the truth"
  },
  "scene": {
    "scene_id": "S7",
    "time": "night",
    "weather": "dry",
    "action": "standing still under a streetlamp",
    "location": "empty street"
  },
  "period": "contemporary",
  "region": "unspecified city",
  "season": "autumn",
  "art_direction": "restrained urban noir",
  "lighting": "cool blue moonlight, cyan neon rim light, low saturation",
  "camera": "close-up",
  "budget": "low",
  "fidelity_mode": "fictional",
  "tool": "midjourney",
  "state": {
    "wetness": "dry"
  }
}
```

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T08-冷光 noir 肖像.json --json` | 0 | 1.79s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py noir coat --limit 6 --json` | 0 | 0.95s |

- `query.py` 命中数量：**3**（验收要求 ≥1）
- `query.py` 命中卡片 ID：STY-0005, LOOK-0021, LOOK-0007
- `recommend.py` 候选池：accessory=GAR-0080, GAR-0070, GAR-0021, GAR-0027, GAR-0026, GAR-0068, GAR-0074, GAR-0073, GAR-0086, GAR-0067, GAR-0066, GAR-0083, GAR-0085, GAR-0028, GAR-0025; carried_prop=GAR-0082, GAR-0047, GAR-0048, GAR-0087, GAR-0049; footwear=GAR-0022, GAR-0023, GAR-0035, GAR-0060, GAR-0058, GAR-0024, GAR-0084, GAR-0081; inner_layer=GAR-0078, GAR-0012, GAR-0020; lower_body=GAR-0014, GAR-0077, GAR-0010, GAR-0011, GAR-0072, GAR-0013; one_piece=GAR-0079, GAR-0063, GAR-0064, GAR-0069, GAR-0031, GAR-0032, GAR-0056, GAR-0015, GAR-0055, GAR-0052, GAR-0071, GAR-0053, GAR-0004, GAR-0054, GAR-0062, GAR-0061, GAR-0075, GAR-0009, GAR-0029; outerwear=GAR-0045, GAR-0076, GAR-0019, GAR-0046, GAR-0057, GAR-0017, GAR-0033, GAR-0016, GAR-0018; set=GAR-0005, GAR-0001, GAR-0065, GAR-0030; upper_body=GAR-EXAMPLE-001, GAR-0006, GAR-0008, GAR-0007, GAR-0034, GAR-0002, GAR-0003
- 三套推荐选中：A: GAR-0006, GAR-0014, GAR-0045, GAR-0022; B: GAR-0079, GAR-0045, GAR-0022, GAR-0080; C: GAR-0079, GAR-0019, GAR-0022

## 候选造型 A/B/C

### Look A（score 49.4/100，cost 0.241，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0006` | 达希基套衫 / dashiki | multicolor, solid_color | cotton, printed_cotton | verified |
| lower_body | `GAR-0014` | 牛仔裤 / jeans | indigo, blue_black | denim, cotton | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0016, STR-0023, STR-0018, STR-0022, STR-0021, STR-0025
- 材质卡：MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002

### Look B（score 49.3/100，cost 0.289，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0079` | 基尔特长袍 / kirtle | wool, linen | wool, linen | interpretive |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
| accessory | `GAR-0080` | 腰带 / belt | iron, silver, gold | iron, silver, leather | verified |

- 结构卡：STR-0016, STR-0023, STR-0021, STR-0025, STR-0015
- 材质卡：MAT-0013, MAT-0001, MAT-0002

### Look C（score 46.9/100，cost 0.254，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0079` | 基尔特长袍 / kirtle | wool, linen | wool, linen | interpretive |
| outerwear | `GAR-0019` | 派克大衣 / anorak | white, natural_hide, beaded_contrast | seal_skin, caribou_fur, wool, cotton | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0016, STR-0023, STR-0025, STR-0021
- 材质卡：MAT-0013, MAT-0001

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 23.0 | 23.0 | 23.0 |
| 角色身份 | 4.4 | 4.4 | 3.5 |
| 环境气候 | 1.8 | 1.8 | 1.8 |
| 美术方向 | 4.8 | 4.9 | 3.7 |
| 动作可行 | 4.5 | 4.4 | 4.0 |
| 剧情弧线 | 6.2 | 6.1 | 6.0 |
| 摄影/一致性 | 6.7 | 6.7 | 6.8 |
| **总计** | 49.4 | 49.3 | 46.9 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, blue black, brown, indigo, khaki, lavender, multicolor, solid color, setting: S7, night, dry, art direction: restrained urban noir, lighting: cool blue moonlight, cyan neon rim light, low saturation, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); cuff (STR-0023); buttons and buttonholes (STR-0018); waistband (STR-0022); seams and darts (STR-0021); ease and fit (STR-0025), continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 丹宁较硬，新裤在蹲坐时有明显折痕; 旧化后膝部与裆部会形成固定褶皱，跨镜头需保持一致。; 宽松套头，手臂活动自由; 下摆与袖口在动作中易上移，需确认长度。, lighting: cool blue moonlight, cyan neon rim light, low saturation, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Lin, one-piece: medieval kirtle, side lacing or belt, long sleeves, worn over a linen chemise, earth-toned or muted colour; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels; accessory: medieval or early modern belt, iron buckle with silver inlay or silver-gilt buckle and belt end, dagger hung at the back or side, palette: beige, black, brown, gold, iron, khaki, lavender, linen, silver, wool, setting: S7, night, dry, art direction: restrained urban noir, lighting: cool blue moonlight, cyan neon rim light, low saturation, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); cuff (STR-0023); seams and darts (STR-0021); ease and fit (STR-0025); waistline (STR-0015), continuity lock: GAR-0079 kirtle [wool, linen; wool, linen; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear] | GAR-0080 belt [iron, silver, gold; iron, silver, leather; accessory]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0013, MAT-0001, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: one-piece: medieval kirtle, side lacing or belt, long sleeves, worn over a linen chemise, earth-toned or muted colour; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels; accessory: medieval or early modern belt, iron buckle with silver inlay or silver-gilt buckle and belt end, dagger hung at the back or side, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 及踝长袍限制步幅; 系带/腰带影响腰线; 外裙在转身时展开。, lighting: cool blue moonlight, cyan neon rim light, low saturation, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0079 kirtle [wool, linen; wool, linen; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear] | GAR-0080 belt [iron, silver, gold; iron, silver, leather; accessory]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0013, MAT-0001, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Lin, one-piece: medieval kirtle, side lacing or belt, long sleeves, worn over a linen chemise, earth-toned or muted colour; outer layer: Arctic anorak parka, hooded, made of layered animal hides with fur inside, geometric beadwork at neckline, windproof; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beaded contrast, black, brown, linen, natural hide, white, wool, setting: S7, night, dry, art direction: restrained urban noir, lighting: cool blue moonlight, cyan neon rim light, low saturation, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); cuff (STR-0023); ease and fit (STR-0025); seams and darts (STR-0021), continuity lock: GAR-0079 kirtle [wool, linen; wool, linen; one-piece] | GAR-0019 anorak [white, natural_hide, beaded_contrast; seal_skin, caribou_fur, wool, cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0013, MAT-0001 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: one-piece: medieval kirtle, side lacing or belt, long sleeves, worn over a linen chemise, earth-toned or muted colour; outer layer: Arctic anorak parka, hooded, made of layered animal hides with fur inside, geometric beadwork at neckline, windproof; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 厚重兽皮限制大幅动作; 及踝长袍限制步幅; 系带/腰带影响腰线; 外裙在转身时展开。, lighting: cool blue moonlight, cyan neon rim light, low saturation, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0079 kirtle [wool, linen; wool, linen; one-piece] | GAR-0019 anorak [white, natural_hide, beaded_contrast; seal_skin, caribou_fur, wool, cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0013, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.7/10
- 理由：上装: GAR-0006 达希基套衫 (casual)
- 理由：下装: GAR-0014 牛仔裤 (casual)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked structure cards: STR-0016, STR-0023, STR-0018, STR-0022, STR-0021, STR-0025
- 理由：linked material cards: MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0006, GAR-0014, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0107, SRC-0115, SRC-0405, SRC-0123, SRC-0202, SRC-0201, SRC-0486, SRC-0413, SRC-0200, SRC-0454, SRC-0484, SRC-0412, SRC-0520, SRC-0521, SRC-0102, SRC-0142, SRC-0423, SRC-0483, SRC-0141
- 来源链接：SRC-0107 → https://fashionhistory.fitnyc.edu/dashiki/
- 来源链接：SRC-0115 → https://fashionhistory.fitnyc.edu/1950-1959/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0413 → https://collections.vam.ac.uk/item/O15667/
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0454 → https://collections.vam.ac.uk/item/O1240056/
- 来源链接：SRC-0484 → https://collections.vam.ac.uk/item/O356786/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0483 → https://collections.vam.ac.uk/item/O356064/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/

### Look B

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.7/10
- 理由：连身: GAR-0079 基尔特长袍 (functional)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：配饰: GAR-0080 腰带 (functional)
- 理由：linked structure cards: STR-0016, STR-0023, STR-0021, STR-0025, STR-0015
- 理由：linked material cards: MAT-0013, MAT-0001, MAT-0002
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0079, GAR-0045, GAR-0022, GAR-0080: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0405, SRC-0123, SRC-0487, SRC-0488, SRC-0202, SRC-0201, SRC-0486, SRC-0484, SRC-0412, SRC-0520, SRC-0521, SRC-0200, SRC-0102, SRC-0483, SRC-0141
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0487 → https://collections.vam.ac.uk/item/O112685/
- 来源链接：SRC-0488 → https://collections.vam.ac.uk/item/O126654/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0484 → https://collections.vam.ac.uk/item/O356786/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0483 → https://collections.vam.ac.uk/item/O356064/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/

### Look C

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.8/10
- 理由：连身: GAR-0079 基尔特长袍 (functional)
- 理由：外层: GAR-0019 派克大衣 (functional)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked structure cards: STR-0016, STR-0023, STR-0025, STR-0021
- 理由：linked material cards: MAT-0013, MAT-0001
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0079, GAR-0019, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0120, SRC-0123, SRC-0202, SRC-0201, SRC-0486, SRC-0521, SRC-0520, SRC-0484, SRC-0412, SRC-0102, SRC-0483
- 来源链接：SRC-0120 → https://fashionhistory.fitnyc.edu/anorak/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0484 → https://collections.vam.ac.uk/item/O356786/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0483 → https://collections.vam.ac.uk/item/O356064/

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| three_looks | PASS | looks=3, distinct=True, checks={'three_looks': True, 'looks_distinct': True} |
| ids_exist | PASS | all garment ids resolvable: True |
| fidelity_matches | PASS | expected=fictional got=fictional |
| prompts | PASS | all prompts complete |
| query_hits | PASS | query.py exit=0, hits=3, ids=STY-0005, LOOK-0021, LOOK-0007 |
| lighting_pair（pair） | PASS | A item overlap=4, prompts differ=True |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable style card for art direction 'restrained urban noir'
- 脚本警告：period evidence is approximate/none for GAR-0079, GAR-0080 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- 脚本警告：the vault has no 'private investigator'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

