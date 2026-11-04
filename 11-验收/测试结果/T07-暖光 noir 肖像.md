# T07 — 暖光肖像：同一角色的冷暖光对照（warm lighting）

- 运行时间：2026-11-05T01:18:43+08:00
- 测试类型：warm_cool_lighting
- 模式：standard
- 输入文件：`11-验收/测试输入/T07-暖光 noir 肖像.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T07-暖光 noir 肖像.json --json`
- 退出码：**0**（耗时 1.77s）

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

## 已知输入

以下字段来自测试输入文件，是**已知条件**（不是模型推断）：

- 角色名（`character.name`）："Lin"
- 职业（`character.occupation`）："private investigator"
- 经济状态（`character.economic_status`）："low"
- 人物弧线（`character.arc`）："closing in on the truth"
- 年代（`period`）："contemporary"
- 地域（`region`）："unspecified city"
- 季节（`season`）："autumn"
- 场次（`scene.scene_id`）："S7"
- 时间（`scene.time`）："night"
- 天气（`scene.weather`）："dry"
- 动作（`scene.action`）："standing still under a streetlamp"
- 地点（`scene.location`）："empty street"
- 美术方向（`art_direction`）："restrained urban noir"
- 摄影光线（`lighting`）："warm tungsten key light, golden amber practicals, deep shadow"
- 景别（`camera`）："close-up"
- 预算（`budget`）："low"
- 严格度模式（`fidelity_mode`）："fictional"
- 生成工具（`tool`）："midjourney"
- 湿度状态（`state.wetness`）："dry"

## 假设

- 人物弧线（closing in on the truth）对服装的映射属于导演/设计解释，不是服饰史事实。
- fictional 模式：不主张历史准确性，只要求内部一致与可拍摄性。
- 年代/地域匹配为近似层级（脚本警告：period evidence is approximate/none for GAR-0079 (requested contemporary); treat these as era-level hypotheses, not exact period matches）。
- 输入未提供的属性保持 unknown，不向服装史或剧作事实补造；本文件的推荐是设计建议而非史料。

## unknown

- 性别呈现（`character.gender_presentation`）：未指定 / unknown，未向生成器发明取值。
- 年龄（`character.age`）：未指定 / unknown，未向生成器发明取值。
- 破损状态（`state.damage`）：未指定 / unknown，未向生成器发明取值。
- 污渍状态（`state.dirt`）：未指定 / unknown，未向生成器发明取值。

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T07-暖光 noir 肖像.json --json` | 0 | 1.77s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py noir coat --limit 6 --json` | 0 | 0.97s |

- `query.py` 命中数量：**3**（验收要求 ≥1）
- `query.py` 命中卡片 ID：STY-0005, LOOK-0021, LOOK-0007
- `recommend.py` 候选池：accessory=GAR-0080, GAR-0070, GAR-0027, GAR-0021, GAR-0026, GAR-0068, GAR-0074, GAR-0067, GAR-0086, GAR-0073, GAR-0066, GAR-0083, GAR-0028, GAR-0085, GAR-0025; carried_prop=GAR-0082, GAR-0047, GAR-0048, GAR-0087, GAR-0049; footwear=GAR-0022, GAR-0023, GAR-0035, GAR-0060, GAR-0058, GAR-0024, GAR-0084, GAR-0081; inner_layer=GAR-0078, GAR-0020, GAR-0012; lower_body=GAR-0014, GAR-0077, GAR-0010, GAR-0011, GAR-0072, GAR-0013; one_piece=GAR-0063, GAR-0079, GAR-0069, GAR-0064, GAR-0031, GAR-0032, GAR-0015, GAR-0056, GAR-0055, GAR-0052, GAR-0071, GAR-0004, GAR-0053, GAR-0054, GAR-0062, GAR-0061, GAR-0009, GAR-0075, GAR-0029; outerwear=GAR-0045, GAR-0076, GAR-0019, GAR-0046, GAR-0057, GAR-0033, GAR-0017, GAR-0016, GAR-0018; set=GAR-0005, GAR-0065, GAR-0001, GAR-0030; upper_body=GAR-EXAMPLE-001, GAR-0006, GAR-0008, GAR-0007, GAR-0034, GAR-0002, GAR-0003
- 三套推荐选中：A: GAR-0006, GAR-0014, GAR-0045, GAR-0022; B: GAR-0063, GAR-0045, GAR-0022; C: GAR-0079, GAR-0045, GAR-0022

## 候选造型 A/B/C

### Look A（score 49.5/100，cost 0.241，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0006` | 达希基套衫 / dashiki | multicolor, solid_color | cotton, printed_cotton | verified |
| lower_body | `GAR-0014` | 牛仔裤 / jeans | indigo, blue_black | denim, cotton | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0016, STR-0023, STR-0018, STR-0022, STR-0021, STR-0025
- 材质卡：MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002

### Look B（score 49.5/100，cost 0.345，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0063` | 纱丽 / sari | purple, pink, gold | silk, gold_thread | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0023, STR-0021, STR-0025
- 材质卡：MAT-0002, MAT-0001

### Look C（score 49.5/100，cost 0.250，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0079` | 基尔特长袍 / kirtle | wool, linen | wool, linen | interpretive |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0016, STR-0023, STR-0021, STR-0025
- 材质卡：MAT-0013, MAT-0001, MAT-0002

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 23.0 | 23.0 | 23.0 |
| 角色身份 | 4.4 | 4.0 | 4.7 |
| 环境气候 | 1.8 | 1.8 | 1.8 |
| 美术方向 | 4.8 | 5.4 | 4.9 |
| 动作可行 | 4.5 | 4.3 | 4.3 |
| 剧情弧线 | 6.2 | 6.0 | 6.0 |
| 摄影/一致性 | 6.7 | 6.9 | 6.8 |
| **总计** | 49.5 | 49.5 | 49.5 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, blue black, brown, indigo, khaki, lavender, multicolor, solid color, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); cuff (STR-0023); buttons and buttonholes (STR-0018); waistband (STR-0022); seams and darts (STR-0021); ease and fit (STR-0025), continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: colorful African-inspired cotton print, patch pockets, embroidered neckline and cuffs, short sleeves; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 丹宁较硬，新裤在蹲坐时有明显折痕; 旧化后膝部与裆部会形成固定褶皱，跨镜头需保持一致。; 宽松套头，手臂活动自由; 下摆与袖口在动作中易上移，需确认长度。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0006 dashiki [multicolor, solid_color; cotton, printed_cotton; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Lin, one-piece: purple silk sari with shocking pink border and pallav, woven gold zari, temple sari, South Indian styling; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, brown, gold, khaki, lavender, pink, purple, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: cuff (STR-0023); seams and darts (STR-0021); ease and fit (STR-0025), continuity lock: GAR-0063 sari [purple, pink, gold; silk, gold_thread; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0001 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: one-piece: purple silk sari with shocking pink border and pallav, woven gold zari, temple sari, South Indian styling; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 长幅布缠绕，行走时需整理褶裥; 金线织边较重、垂坠明显。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0063 sari [purple, pink, gold; silk, gold_thread; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Lin, one-piece: medieval kirtle, side lacing or belt, long sleeves, worn over a linen chemise, earth-toned or muted colour; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, brown, khaki, lavender, linen, wool, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); cuff (STR-0023); seams and darts (STR-0021); ease and fit (STR-0025), continuity lock: GAR-0079 kirtle [wool, linen; wool, linen; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0013, MAT-0001, MAT-0002 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: one-piece: medieval kirtle, side lacing or belt, long sleeves, worn over a linen chemise, earth-toned or muted colour; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 及踝长袍限制步幅; 系带/腰带影响腰线; 外裙在转身时展开。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0079 kirtle [wool, linen; wool, linen; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0013, MAT-0001, MAT-0002, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

## 风险

### Look A

- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0006, GAR-0014, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look B

- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0063, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look C

- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0079, GAR-0045, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### 脚本级风险与缺口

- [context_gap/medium] no reliable style card for art direction 'restrained urban noir'
- [period_approximate/medium] period evidence is approximate/none for GAR-0079 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- [occupation_coverage_gap/medium] the vault has no 'private investigator'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- no reliable style card for art direction 'restrained urban noir'
- period evidence is approximate/none for GAR-0079 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- the vault has no 'private investigator'-specific garment cards; generic pieces are used and no other profession's uniform is substituted

## 证据

### Look A

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.7/10
- 理由（解释性，不是史实）：上装: GAR-0006 达希基套衫 (casual)
- 理由（解释性，不是史实）：下装: GAR-0014 牛仔裤 (casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0016, STR-0023, STR-0018, STR-0022, STR-0021, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0001, MAT-0003, MAT-0012, MAT-0013, MAT-0002
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
- 单件证据状态：GAR-0006=verified; GAR-0014=verified; GAR-0045=verified; GAR-0022=verified

### Look B

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.9/10
- 理由（解释性，不是史实）：连身: GAR-0063 纱丽 (ceremonial)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0023, STR-0021, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0001
- source_ids：SRC-0424, SRC-0405, SRC-0123, SRC-0486, SRC-0202, SRC-0484, SRC-0412, SRC-0520, SRC-0521, SRC-0141, SRC-0102
- 来源链接：SRC-0424 → https://collections.vam.ac.uk/item/O84377/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0484 → https://collections.vam.ac.uk/item/O356786/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 单件证据状态：GAR-0063=verified; GAR-0045=verified; GAR-0022=verified

### Look C

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.8/10
- 理由（解释性，不是史实）：连身: GAR-0079 基尔特长袍 (functional)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0016, STR-0023, STR-0021, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0013, MAT-0001, MAT-0002
- source_ids：SRC-0405, SRC-0123, SRC-0202, SRC-0201, SRC-0486, SRC-0484, SRC-0412, SRC-0520, SRC-0521, SRC-0102, SRC-0483, SRC-0141
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0486 → https://collections.vam.ac.uk/item/O137793/
- 来源链接：SRC-0484 → https://collections.vam.ac.uk/item/O356786/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0483 → https://collections.vam.ac.uk/item/O356064/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 单件证据状态：GAR-0079=interpretive; GAR-0045=verified; GAR-0022=verified

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
- 脚本警告：period evidence is approximate/none for GAR-0079 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- 脚本警告：the vault has no 'private investigator'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

