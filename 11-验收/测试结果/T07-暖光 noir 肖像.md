# T07 — 暖光肖像：同一角色的冷暖光对照（warm lighting）

- 运行时间：2026-11-04T01:49:16+08:00
- 测试类型：warm_cool_lighting
- 模式：standard
- 输入文件：`11-验收/测试输入/T07-暖光 noir 肖像.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T07-暖光 noir 肖像.json --json`
- 退出码：**0**（耗时 0.66s）

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
  "lighting": "warm tungsten key light, golden amber practicals, deep shadow",
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
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T07-暖光 noir 肖像.json --json` | 0 | 0.66s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py noir coat --limit 6 --json` | 0 | 0.51s |

- `query.py` 命中数量：**4**（验收要求 ≥1）
- `query.py` 命中卡片 ID：STY-0005, STY-EXAMPLE-001, LOOK-EXAMPLE-001, LOOK-0007
- `recommend.py` 候选池：accessory=GAR-0021, GAR-0026, GAR-0025, GAR-0028; footwear=GAR-0022, GAR-0023, GAR-0035, GAR-0024; inner_layer=GAR-0020, GAR-0012; lower_body=GAR-0014, GAR-0010, GAR-0011, GAR-0013; one_piece=GAR-0031, GAR-0032, GAR-0015, GAR-0029; outerwear=GAR-0019, GAR-0033, GAR-0018, GAR-0017, GAR-0016; upper_body=GAR-EXAMPLE-001, GAR-0006, GAR-0008, GAR-0002, GAR-0007, GAR-0003, GAR-0034
- 三套推荐选中：A: GAR-EXAMPLE-001, GAR-0014, GAR-0019, GAR-0022; B: GAR-0006, GAR-0010, GAR-0033, GAR-0023, GAR-0021; C: GAR-0006, GAR-0014, GAR-0019, GAR-0022

## 候选造型 A/B/C

### Look A（score 50.8/100，cost 0.244，source_look=LOOK-0007）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-EXAMPLE-001` | 白色立领衬衫 / white stand-collar shirt | off_white | cotton | example |
| lower_body | `GAR-0014` | 牛仔裤 / jeans | indigo, blue_black | denim, cotton | verified |
| outerwear | `GAR-0019` | 派克大衣 / anorak | white, natural_hide, beaded_contrast | seal_skin, caribou_fur, wool, cotton | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
- 材质卡：MAT-0001, MAT-0003

### Look B（score 41.1/100，cost 0.328，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0006` | 达希基套衫 / dashiki | multicolor, solid_color | cotton, printed_cotton | verified |
| lower_body | `GAR-0010` | 灯笼裤 / bloomers | white, black, dark | cotton, wool, linen | verified |
| outerwear | `GAR-0033` | 西式休闲西装 / lounge suit | brown, herringbone | tweed, wool, sateen | verified |
| footwear | `GAR-0023` | 莫卡辛鞋 / moccasins | tan, buckskin, beaded | leather, beads, silk_ribbon | verified |
| accessory | `GAR-0021` | 围裙裙 / pinafore | white, printed, navy | cotton, linen | verified |

- 结构卡：STR-0003
- 材质卡：MAT-0001, MAT-0003, MAT-0002

### Look C（score 46.0/100，cost 0.244，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0006` | 达希基套衫 / dashiki | multicolor, solid_color | cotton, printed_cotton | verified |
| lower_body | `GAR-0014` | 牛仔裤 / jeans | indigo, blue_black | denim, cotton | verified |
| outerwear | `GAR-0019` | 派克大衣 / anorak | white, natural_hide, beaded_contrast | seal_skin, caribou_fur, wool, cotton | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
- 材质卡：MAT-0001, MAT-0003

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 19.5 | 15.8 | 21.5 |
| 角色身份 | 3.8 | 3.5 | 3.6 |
| 环境气候 | 3.0 | 1.8 | 1.8 |
| 美术方向 | 4.7 | 3.5 | 3.7 |
| 动作可行 | 5.0 | 4.3 | 4.3 |
| 剧情弧线 | 6.2 | 6.2 | 6.2 |
| 摄影/一致性 | 6.7 | 7.4 | 7.0 |
| **总计** | 50.8 | 41.1 | 46.0 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: off-white cotton stand-collar shirt, straight fit, slightly wrinkled fabric; lower body: 1950s blue denim jeans, straight or slim cut, worn with a white t-shirt and leather jacket, working-class youth styling, visible wear at knees; outer layer: Arctic anorak parka, hooded, made of layered animal hides with fur inside, geometric beadwork at neckline, windproof, worn in snow; footwear: calf-length Wellington boots, water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beaded contrast, black, blue black, brown, indigo, natural hide, off white, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-EXAMPLE-001 white stand-collar shirt [off_white; cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0019 anorak [white, natural_hide, beaded_contrast; seal_skin, caribou_fur, wool, cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: off-white cotton stand-collar shirt, straight fit, slightly wrinkled fabric; lower body: 1950s blue denim jeans, straight or slim cut, worn with a white t-shirt and leather jacket, working-class youth styling, visible wear at knees; outer layer: Arctic anorak parka, hooded, made of layered animal hides with fur inside, geometric beadwork at neckline, windproof, worn in snow; footwear: calf-length Wellington boots, water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 厚重兽皮限制大幅动作；毛边在风雪中会结冰，镜头间需保持湿润/结冰状态一致。; 丹宁较硬，新裤在蹲坐时有明显折痕；旧化后膝部与裆部会形成固定褶皱，跨镜头需保持一致。; 抬臂时肩背与袖山出现拉扯褶皱；下摆易从裤腰滑出，连续镜头需锁定塞入状态。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-EXAMPLE-001 white stand-collar shirt [off_white; cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0019 anorak [white, natural_hide, beaded_contrast; seal_skin, caribou_fur, wool, cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: loose pullover dashiki shirt, colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: loose bloomers gathered below the knee or at the ankle, worn under a knee-length skirt, white cotton or dark wool, full trouser legs; outer layer: 1930s lounge suit, single-breasted jacket with wide trousers, brown herringbone tweed, generous cut, worn with shirt and tie, no waistcoat, urban professional; footwear: soft-soled leather moccasins, one-piece hide wrapped around the foot, floral beadwork and silk ribbon ties, no separate heel; accessory: sleeveless pinafore apron over a dress, ruffled hem curving up at the sides, white cotton or printed fabric, tied at the back, palette: beaded, black, brown, buckskin, dark, herringbone, multicolor, navy, printed, solid color, tan, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: ruff (STR-0003), continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0010 bloomers [white, black, dark; cotton, wool, linen; lower body] | GAR-0033 lounge suit [brown, herringbone; tweed, wool, sateen; outer layer] | GAR-0023 moccasins [tan, buckskin, beaded; leather, beads, silk_ribbon; footwear] | GAR-0021 pinafore [white, printed, navy; cotton, linen; accessory]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: loose pullover dashiki shirt, colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: loose bloomers gathered below the knee or at the ankle, worn under a knee-length skirt, white cotton or dark wool, full trouser legs; outer layer: 1930s lounge suit, single-breasted jacket with wide trousers, brown herringbone tweed, generous cut, worn with shirt and tie, no waistcoat, urban professional; footwear: soft-soled leather moccasins, one-piece hide wrapped around the foot, floral beadwork and silk ribbon ties, no separate heel; accessory: sleeveless pinafore apron over a dress, ruffled hem curving up at the sides, white cotton or printed fabric, tied at the back, fabric motion: 宽松剪裁与宽裤便于行走，但粗花呢厚重、抬臂时肩背起褶；三件套在 1930 年代后期常省略马甲，需锁定是否穿马甲。; 宽松裤腿在膝/踝处收口，跑动时裤腿鼓起；骑行时需确认不会卷入车轮。; 宽松套头，手臂活动自由；下摆与袖口在动作中易上移，需确认长度。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0010 bloomers [white, black, dark; cotton, wool, linen; lower body] | GAR-0033 lounge suit [brown, herringbone; tweed, wool, sateen; outer layer] | GAR-0023 moccasins [tan, buckskin, beaded; leather, beads, silk_ribbon; footwear] | GAR-0021 pinafore [white, printed, navy; cotton, linen; accessory]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: loose pullover dashiki shirt, colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, worn with a white t-shirt and leather jacket, working-class youth styling, visible wear at knees; outer layer: Arctic anorak parka, hooded, made of layered animal hides with fur inside, geometric beadwork at neckline, windproof, worn in snow; footwear: calf-length Wellington boots, water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beaded contrast, black, blue black, brown, indigo, multicolor, natural hide, solid color, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0019 anorak [white, natural_hide, beaded_contrast; seal_skin, caribou_fur, wool, cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: loose pullover dashiki shirt, colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, worn with a white t-shirt and leather jacket, working-class youth styling, visible wear at knees; outer layer: Arctic anorak parka, hooded, made of layered animal hides with fur inside, geometric beadwork at neckline, windproof, worn in snow; footwear: calf-length Wellington boots, water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 厚重兽皮限制大幅动作；毛边在风雪中会结冰，镜头间需保持湿润/结冰状态一致。; 丹宁较硬，新裤在蹲坐时有明显折痕；旧化后膝部与裆部会形成固定褶皱，跨镜头需保持一致。; 宽松套头，手臂活动自由；下摆与袖口在动作中易上移，需确认长度。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0019 anorak [white, natural_hide, beaded_contrast; seal_skin, caribou_fur, wool, cotton; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 19.5/25, 摄影/一致性 6.7/10
- 理由：上装: GAR-EXAMPLE-001 白色立领衬衫 (smart_casual)
- 理由：下装: GAR-0014 牛仔裤 (casual)
- 理由：外层: GAR-0019 派克大衣 (functional)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked material cards: MAT-0001, MAT-0003
- 理由：based on curated vault look card LOOK-0007
- 风险：look includes example cards, not historical evidence
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0014, GAR-0019, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0120, SRC-0115, SRC-0123, SRC-0102, SRC-0142
- 来源链接：SRC-0120 → https://fashionhistory.fitnyc.edu/anorak/
- 来源链接：SRC-0115 → https://fashionhistory.fitnyc.edu/1950-1959/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/

### Look B

- 理由：highest scoring dimensions: 年代/文化 15.8/25, 摄影/一致性 7.4/10
- 理由：上装: GAR-0006 达希基套衫 (casual)
- 理由：下装: GAR-0010 灯笼裤 (casual)
- 理由：外层: GAR-0033 西式休闲西装 (business)
- 理由：足部: GAR-0023 莫卡辛鞋 (casual)
- 理由：配饰: GAR-0021 围裙裙 (casual)
- 理由：linked structure cards: STR-0003
- 理由：linked material cards: MAT-0001, MAT-0003, MAT-0002
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0006, GAR-0010, GAR-0033, GAR-0023, GAR-0021: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0107, SRC-0111, SRC-0204, SRC-0155, SRC-0124, SRC-0122, SRC-0133, SRC-0102, SRC-0142, SRC-0141
- 来源链接：SRC-0107 → https://fashionhistory.fitnyc.edu/dashiki/
- 来源链接：SRC-0111 → https://fashionhistory.fitnyc.edu/bloomers/
- 来源链接：SRC-0204 → https://collections.vam.ac.uk/item/O110441/
- 来源链接：SRC-0155 → https://fashionhistory.fitnyc.edu/1930-1939/
- 来源链接：SRC-0124 → https://fashionhistory.fitnyc.edu/moccasins/
- 来源链接：SRC-0122 → https://fashionhistory.fitnyc.edu/pinafore/
- 来源链接：SRC-0133 → https://fashionhistory.fitnyc.edu/ruff/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/

### Look C

- 理由：highest scoring dimensions: 年代/文化 21.5/25, 摄影/一致性 7.0/10
- 理由：上装: GAR-0006 达希基套衫 (casual)
- 理由：下装: GAR-0014 牛仔裤 (casual)
- 理由：外层: GAR-0019 派克大衣 (functional)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked material cards: MAT-0001, MAT-0003
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0006, GAR-0014, GAR-0019, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0107, SRC-0115, SRC-0120, SRC-0123, SRC-0102, SRC-0142
- 来源链接：SRC-0107 → https://fashionhistory.fitnyc.edu/dashiki/
- 来源链接：SRC-0115 → https://fashionhistory.fitnyc.edu/1950-1959/
- 来源链接：SRC-0120 → https://fashionhistory.fitnyc.edu/anorak/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| three_looks | PASS | looks=3, distinct=True, checks={'three_looks': True, 'looks_distinct': True} |
| ids_exist | PASS | all garment ids resolvable: True |
| fidelity_matches | PASS | expected=fictional got=fictional |
| prompts | PASS | all prompts complete |
| query_hits | PASS | query.py exit=0, hits=4, ids=STY-0005, STY-EXAMPLE-001, LOOK-EXAMPLE-001, LOOK-0007 |
| lighting_pair（pair） | PASS | A item overlap=4, prompts differ=True |

**VERDICT: PASS**

## 备注

- 脚本无警告。
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

