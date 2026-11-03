# T08 — 冷光肖像：同一角色的冷暖光对照（cool lighting）

- 运行时间：2026-11-04T03:12:44+08:00
- 测试类型：warm_cool_lighting
- 模式：standard
- 输入文件：`11-验收/测试输入/T08-冷光 noir 肖像.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T08-冷光 noir 肖像.json --json`
- 退出码：**0**（耗时 1.51s）

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
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T08-冷光 noir 肖像.json --json` | 0 | 1.51s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py noir coat --limit 6 --json` | 0 | 0.76s |

- `query.py` 命中数量：**3**（验收要求 ≥1）
- `query.py` 命中卡片 ID：STY-0005, LOOK-0021, LOOK-0007
- `recommend.py` 候选池：accessory=GAR-0070, GAR-0021, GAR-0027, GAR-0026, GAR-0068, GAR-0074, GAR-0073, GAR-0067, GAR-0066, GAR-0028, GAR-0025; carried_prop=GAR-0047, GAR-0048, GAR-0049; footwear=GAR-0022, GAR-0023, GAR-0035, GAR-0060, GAR-0058, GAR-0024; inner_layer=GAR-0012, GAR-0020; lower_body=GAR-0014, GAR-0010, GAR-0011, GAR-0072, GAR-0013; one_piece=GAR-0063, GAR-0064, GAR-0069, GAR-0031, GAR-0032, GAR-0056, GAR-0015, GAR-0055, GAR-0052, GAR-0071, GAR-0053, GAR-0004, GAR-0054, GAR-0062, GAR-0061, GAR-0009, GAR-0029; outerwear=GAR-0045, GAR-0019, GAR-0046, GAR-0057, GAR-0017, GAR-0033, GAR-0016, GAR-0018; set=GAR-0005, GAR-0001, GAR-0065, GAR-0030; upper_body=GAR-EXAMPLE-001, GAR-0006, GAR-0008, GAR-0007, GAR-0034, GAR-0002, GAR-0003
- 三套推荐选中：A: GAR-0006, GAR-0014, GAR-0045, GAR-0022; B: GAR-0063, GAR-0045, GAR-0022; C: GAR-0031, GAR-0045, GAR-0022

## 候选造型 A/B/C

### Look A（score 49.4/100，cost 0.241，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0006` | 达希基套衫 / dashiki | multicolor, solid_color | cotton, printed_cotton | verified |
| lower_body | `GAR-0014` | 牛仔裤 / jeans | indigo, blue_black | denim, cotton | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
- 材质卡：MAT-0001, MAT-0003, MAT-0002

### Look B（score 49.2/100，cost 0.345，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0063` | 纱丽 / sari | purple, pink, gold | silk, gold_thread | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
- 材质卡：MAT-0002, MAT-0001

### Look C（score 47.3/100，cost 0.282，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0011
- 材质卡：MAT-0002, MAT-0003, MAT-0001

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 23.0 | 23.0 | 17.9 |
| 角色身份 | 4.4 | 4.0 | 4.4 |
| 环境气候 | 1.8 | 1.8 | 3.5 |
| 美术方向 | 4.8 | 5.4 | 4.9 |
| 动作可行 | 4.5 | 4.3 | 5.4 |
| 剧情弧线 | 6.2 | 6.0 | 6.4 |
| 摄影/一致性 | 6.7 | 6.6 | 6.8 |
| **总计** | 49.4 | 49.2 | 47.3 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, blue black, brown, indigo, khaki, lavender, multicolor, solid color, setting: S7, night, dry, art direction: restrained urban noir, lighting: cool blue moonlight, cyan neon rim light, low saturation, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 丹宁较硬，新裤在蹲坐时有明显折痕; 旧化后膝部与裆部会形成固定褶皱，跨镜头需保持一致。; 宽松套头，手臂活动自由; 下摆与袖口在动作中易上移，需确认长度。, lighting: cool blue moonlight, cyan neon rim light, low saturation, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Lin, one-piece: purple silk sari with shocking pink border and pallav, woven gold zari, temple sari, South Indian styling; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, brown, gold, khaki, lavender, pink, purple, setting: S7, night, dry, art direction: restrained urban noir, lighting: cool blue moonlight, cyan neon rim light, low saturation, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-0063 sari [purple, pink, gold; silk, gold_thread; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0001 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: one-piece: purple silk sari with shocking pink border and pallav, woven gold zari, temple sari, South Indian styling; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 长幅布缠绕，行走时需整理褶裥; 金线织边较重、垂坠明显。, lighting: cool blue moonlight, cyan neon rim light, low saturation, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0063 sari [purple, pink, gold; silk, gold_thread; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Lin, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, brown, khaki, lavender, mid blue, orange red, pink, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: cool blue moonlight, cyan neon rim light, low saturation, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: cool blue moonlight, cyan neon rim light, low saturation, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.7/10
- 理由：上装: GAR-0006 达希基套衫 (casual)
- 理由：下装: GAR-0014 牛仔裤 (casual)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked material cards: MAT-0001, MAT-0003, MAT-0002
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0006, GAR-0014, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0107, SRC-0115, SRC-0405, SRC-0123, SRC-0102, SRC-0142, SRC-0141
- 来源链接：SRC-0107 → https://fashionhistory.fitnyc.edu/dashiki/
- 来源链接：SRC-0115 → https://fashionhistory.fitnyc.edu/1950-1959/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/

### Look B

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.6/10
- 理由：连身: GAR-0063 纱丽 (ceremonial)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked material cards: MAT-0002, MAT-0001
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0063, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0424, SRC-0405, SRC-0123, SRC-0141, SRC-0102
- 来源链接：SRC-0424 → https://collections.vam.ac.uk/item/O84377/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/

### Look C

- 理由：highest scoring dimensions: 年代/文化 17.9/25, 摄影/一致性 6.8/10
- 理由：连身: GAR-0031 旗袍 (smart_casual)
- 理由：外层: GAR-0045 风衣 (smart_casual)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked structure cards: STR-0011
- 理由：linked material cards: MAT-0002, MAT-0003, MAT-0001
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0031, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0200, SRC-0201, SRC-0405, SRC-0123, SRC-0202, SRC-0141, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
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
| fidelity_matches | PASS | expected=fictional got=fictional |
| prompts | PASS | all prompts complete |
| query_hits | PASS | query.py exit=0, hits=3, ids=STY-0005, LOOK-0021, LOOK-0007 |
| lighting_pair（pair） | PASS | A item overlap=4, prompts differ=True |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable style card for art direction 'restrained urban noir'
- 脚本警告：the vault has no 'private investigator'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

