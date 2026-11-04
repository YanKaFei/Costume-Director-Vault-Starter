# T40 — query 排序：1930s 上海 top5 必须含 GAR-0031 且无 example

- 运行时间：2026-11-05T00:45:46+08:00
- 测试类型：query_ranking, M8
- 模式：standard
- 输入文件：`11-验收/测试输入/T40-query排序1930s上海.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T40-query排序1930s上海.json --json`
- 退出码：**0**（耗时 1.27s）

## 实际输入

```json
{
  "character": {
    "name": "Shen",
    "occupation": "journalist",
    "economic_status": "middle",
    "arc": "chasing a story"
  },
  "scene": "rain-soaked newspaper alley",
  "time": "night",
  "weather": "rain",
  "action": "walking quickly",
  "location": "shanghai alley",
  "season": "autumn",
  "period": "1930s",
  "region": "shanghai",
  "art_direction": "restrained historical noir",
  "lighting": "sodium street light",
  "camera": "medium tracking",
  "budget": "medium",
  "fidelity_mode": "historical",
  "tool": "generic"
}
```

## 已知输入

以下字段来自测试输入文件，是**已知条件**（不是模型推断）：

- 角色名（`character.name`）："Shen"
- 职业（`character.occupation`）："journalist"
- 经济状态（`character.economic_status`）："middle"
- 人物弧线（`character.arc`）："chasing a story"
- 年代（`period`）："1930s"
- 地域（`region`）："shanghai"
- 季节（`season`）："autumn"
- 美术方向（`art_direction`）："restrained historical noir"
- 摄影光线（`lighting`）："sodium street light"
- 景别（`camera`）："medium tracking"
- 预算（`budget`）："medium"
- 严格度模式（`fidelity_mode`）："historical"
- 生成工具（`tool`）："generic"

## 假设

- 人物弧线（chasing a story）对服装的映射属于导演/设计解释，不是服饰史事实。
- historical 模式：年代/文化可行性优先于视觉表现；证据不足时按脚本警告处理，不把推断写成史实。
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
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T40-query排序1930s上海.json --json` | 0 | 1.27s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py 1930s 上海 --limit 5 --json` | 0 | 0.94s |

- `query.py` 命中数量：**5**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0031, LOOK-0008, LOOK-0009, LOOK-0012, LOOK-0015
- `recommend.py` 候选池：accessory=GAR-0066, GAR-0067, GAR-0068, GAR-0021, GAR-0028, GAR-0070, GAR-0026, GAR-0074, GAR-0086, GAR-0073; carried_prop=GAR-0048, GAR-0087, GAR-0047; footwear=GAR-0035, GAR-0022, GAR-0060, GAR-0058, GAR-0023; inner_layer=GAR-0012, GAR-0078, GAR-0020; lower_body=GAR-0072, GAR-0014, GAR-0010, GAR-0077, GAR-0011; one_piece=GAR-0031, GAR-0032, GAR-0064, GAR-0063, GAR-0071, GAR-0069, GAR-0053, GAR-0055, GAR-0056, GAR-0052, GAR-0054; outerwear=GAR-0045; set=GAR-0065, GAR-0001; upper_body=GAR-0008, GAR-0034, GAR-0007, GAR-0006
- 三套推荐选中：A: GAR-0031, GAR-0045, GAR-0035, GAR-0047; B: GAR-0031, GAR-0045, GAR-0035, GAR-0048; C: GAR-0031, GAR-0045, GAR-0022

## 候选造型 A/B/C

### Look A（score 50.2/100，cost 0.358，source_look=LOOK-0012）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |
| carried_prop | `GAR-0047` | 雨伞 / umbrella | black, silver | silk, silver, wood | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0025
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012

### Look B（score 50.8/100，cost 0.317，source_look=LOOK-0015）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |
| carried_prop | `GAR-0048` | 手提包 / handbag | multicolor | canvas, wool | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0025, STR-0019, STR-0026
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011

### Look C（score 48.2/100，cost 0.282，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| outerwear | `GAR-0045` | 风衣 / trench coat | khaki, beige, lavender | gabardine, cotton, lace | verified |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |

- 结构卡：STR-0011, STR-0016, STR-0023, STR-0021, STR-0025
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0001

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 14.2 | 14.4 | 14.5 |
| 角色身份 | 5.2 | 5.0 | 5.2 |
| 环境气候 | 7.8 | 8.4 | 8.8 |
| 美术方向 | 6.5 | 6.4 | 6.4 |
| 动作可行 | 4.6 | 4.7 | 4.3 |
| 剧情弧线 | 3.5 | 3.5 | 3.5 |
| 摄影/一致性 | 6.5 | 6.5 | 6.5 |
| **总计** | 50.2 | 50.8 | 48.2 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Shen, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: black silk umbrella, silver handle with engraved hunting scenes, slim wooden shaft, rain-wet silk canopy, carried in one hand, palette: beige, black, khaki, lavender, mid blue, orange red, pink, red, silver, white, setting: rain-soaked newspaper alley, night, rain, art direction: restrained historical noir, lighting: sodium street light, camera: medium tracking, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); ease and fit (STR-0025), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0047 umbrella [black, silver; silk, silver, wood; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012
```

**Video prompt (EN):**

```
Shen, walking quickly, scene: rain-soaked newspaper alley, night, rain, camera: medium tracking, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: black silk umbrella, silver handle with engraved hunting scenes, slim wooden shaft, rain-wet silk canopy, carried in one hand, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: sodium street light, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0047 umbrella [black, silver; silk, silver, wood; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Shen, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: 1930s embroidered canvas handbag, cross-stitch wool floral pattern, fabric handle, small framed purse, carried in hand or on wrist, palette: beige, black, khaki, lavender, mid blue, multicolor, orange red, pink, red, silver, white, setting: rain-soaked newspaper alley, night, rain, art direction: restrained historical noir, lighting: sodium street light, camera: medium tracking, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); ease and fit (STR-0025); zipper (STR-0019); handbag construction (STR-0026), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0048 handbag [multicolor; canvas, wool; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011
```

**Video prompt (EN):**

```
Shen, walking quickly, scene: rain-soaked newspaper alley, night, rain, camera: medium tracking, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling; carried prop: 1930s embroidered canvas handbag, cross-stitch wool floral pattern, fabric handle, small framed purse, carried in hand or on wrist, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: sodium street light, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear] | GAR-0048 handbag [multicolor; canvas, wool; carried prop]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Shen, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: beige, black, brown, khaki, lavender, mid blue, orange red, pink, white, setting: rain-soaked newspaper alley, night, rain, art direction: restrained historical noir, lighting: sodium street light, camera: medium tracking, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); cuff (STR-0023); seams and darts (STR-0021); ease and fit (STR-0025), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001
```

**Video prompt (EN):**

```
Shen, walking quickly, scene: rain-soaked newspaper alley, night, rain, camera: medium tracking, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; outer layer: trench coat, double-breasted, belted waist, storm flap, epaulettes, cuff straps, knee-length gabardine, khaki or dark, rain-beaded surface; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 长下摆与腰带限制大步; 肩部覆片/袖口扣在抬臂时拉扯; 雨天湿重贴身。; 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: sodium street light, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0045 trench coat [khaki, beige, lavender; gabardine, cotton, lace; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0001, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories, no instant drying between shots; wetness changes only on an explicit state transition
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

- [context_gap/medium] no reliable style card for art direction 'restrained historical noir'
- [period_era_level/low] period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- [region_mismatch/medium] cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- [conflict_weather_vs_material/medium] wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- no reliable style card for art direction 'restrained historical noir'
- period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot

## 证据

### Look A

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 14.2/25, 环境气候 7.8/15
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由（解释性，不是史实）：携带物: GAR-0047 雨伞 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011, MAT-0012
- 理由（解释性，不是史实）：based on curated vault look card LOOK-0012
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
- 单件证据状态：GAR-0031=verified; GAR-0045=verified; GAR-0035=verified; GAR-0047=verified

### Look B

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 14.4/25, 环境气候 8.4/15
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由（解释性，不是史实）：携带物: GAR-0048 手提包 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0025, STR-0019, STR-0026
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001, MAT-0011
- 理由（解释性，不是史实）：based on curated vault look card LOOK-0015
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
- 单件证据状态：GAR-0031=verified; GAR-0045=verified; GAR-0035=verified; GAR-0048=verified

### Look C

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 14.5/25, 环境气候 8.8/15
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：外层: GAR-0045 风衣 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0023, STR-0021, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0001
- source_ids：SRC-0200, SRC-0201, SRC-0405, SRC-0123, SRC-0202, SRC-0486, SRC-0484, SRC-0412, SRC-0520, SRC-0521, SRC-0141, SRC-0143, SRC-0423, SRC-0142, SRC-0102
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0405 → https://collections.vam.ac.uk/item/O1295635/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
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
- 单件证据状态：GAR-0031=verified; GAR-0045=verified; GAR-0022=verified

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| three_looks | PASS | looks=3, distinct=True, checks={'three_looks': True, 'looks_distinct': True} |
| no_crash | PASS | recommend.py exit=0 (must be 0, no KeyError/uncaught exception) |
| no_example_in_a | PASS | Look A example ids=[] contains_example=False |
| query_hits | PASS | query.py exit=0, hits=5, ids=GAR-0031, LOOK-0008, LOOK-0009, LOOK-0012, LOOK-0015 |
| query_top5_contains:GAR-0031 | PASS | query top5=['GAR-0031', 'LOOK-0008', 'LOOK-0009', 'LOOK-0012', 'LOOK-0015'] (wanted GAR-0031) |
| query_no_example_top | PASS | example ids in query top5=[] |
| query_no_duplicate_names | PASS | duplicate names in query top5=[] |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable style card for art direction 'restrained historical noir'
- 脚本警告：period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- 脚本警告：cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- 脚本警告：wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

