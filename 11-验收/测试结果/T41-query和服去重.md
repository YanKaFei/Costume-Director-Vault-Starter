# T41 — query 去重：同名和服卡不得重复占据 top5

- 运行时间：2026-11-05T01:20:09+08:00
- 测试类型：query_dedup, D3
- 模式：standard
- 输入文件：`11-验收/测试输入/T41-query和服去重.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T41-query和服去重.json --json`
- 退出码：**0**（耗时 1.86s）

## 实际输入

```json
{
  "character": {
    "name": "Aiko",
    "occupation": "dancer",
    "economic_status": "middle",
    "arc": "performing in a period drama"
  },
  "scene": "theatre stage",
  "time": "evening",
  "weather": "indoor",
  "action": "walking across the stage",
  "location": "theatre",
  "season": "spring",
  "period": "1920s",
  "region": "japan",
  "art_direction": "theatre period drama",
  "lighting": "warm stage light",
  "camera": "medium shot",
  "budget": "medium",
  "fidelity_mode": "inspired",
  "tool": "generic"
}
```

## 已知输入

以下字段来自测试输入文件，是**已知条件**（不是模型推断）：

- 角色名（`character.name`）："Aiko"
- 职业（`character.occupation`）："dancer"
- 经济状态（`character.economic_status`）："middle"
- 人物弧线（`character.arc`）："performing in a period drama"
- 年代（`period`）："1920s"
- 地域（`region`）："japan"
- 季节（`season`）："spring"
- 美术方向（`art_direction`）："theatre period drama"
- 摄影光线（`lighting`）："warm stage light"
- 景别（`camera`）："medium shot"
- 预算（`budget`）："medium"
- 严格度模式（`fidelity_mode`）："inspired"
- 生成工具（`tool`）："generic"

## 假设

- 人物弧线（performing in a period drama）对服装的映射属于导演/设计解释，不是服饰史事实。
- inspired 模式：允许对历史元素做艺术化重构；卡片中的 verified 事实只作为灵感锚点。
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
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T41-query和服去重.json --json` | 0 | 1.86s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py 和服 --limit 5 --json` | 0 | 0.99s |

- `query.py` 命中数量：**5**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0001, GAR-0065, GAR-0066, SRC-0009, SRC-0028
- `recommend.py` 候选池：accessory=GAR-0067, GAR-0066, GAR-0068, GAR-0074, GAR-0086, GAR-0073, GAR-0070, GAR-0028, GAR-0026, GAR-0080, GAR-0021, GAR-0083, GAR-0085, GAR-0025; carried_prop=GAR-0048, GAR-0087, GAR-0049, GAR-0047, GAR-0082; footwear=GAR-0035, GAR-0058, GAR-0022, GAR-0060, GAR-0024, GAR-0023, GAR-0084, GAR-0081; inner_layer=GAR-0020, GAR-0078, GAR-0012; lower_body=GAR-0072, GAR-0014, GAR-0010, GAR-0011, GAR-0077, GAR-0013; one_piece=GAR-0031, GAR-0032, GAR-0063, GAR-0064, GAR-0071, GAR-0054, GAR-0056, GAR-0055, GAR-0069, GAR-0015, GAR-0053, GAR-0062, GAR-0052, GAR-0029, GAR-0075, GAR-0079; outerwear=GAR-0057, GAR-0045, GAR-0017, GAR-0046, GAR-0016, GAR-0018, GAR-0033, GAR-0076; set=GAR-0065, GAR-0001; upper_body=GAR-EXAMPLE-001, GAR-0008, GAR-0007, GAR-0034, GAR-0006, GAR-0002, GAR-0003
- 三套推荐选中：A: GAR-0065, GAR-0035; B: GAR-0031, GAR-0035; C: GAR-0065, GAR-0058

## 候选造型 A/B/C

### Look A（score 46.0/100，cost 0.486，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| set | `GAR-0065` | 出口和服 / export kimono | cream, red, gold | silk_crepe, silk | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |

- 结构卡：STR-0016, STR-0017, STR-0025
- 材质卡：MAT-0002, MAT-0003, MAT-0011, MAT-0014

### Look B（score 44.6/100，cost 0.393，source_look=LOOK-0009）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0031` | 旗袍 / qipao | white, orange_red, pink, mid_blue | silk, synthetic_velvet, crepe, silk_damask | verified |
| footwear | `GAR-0035` | 女式皮鞋 / 1930s women’s shoes | black, red, silver | lace, sequins, silk, metallic_brocade | verified |

- 结构卡：STR-0011, STR-0016, STR-0025
- 材质卡：MAT-0002, MAT-0014, MAT-0003, MAT-0011

### Look C（score 43.6/100，cost 0.390，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| set | `GAR-0065` | 出口和服 / export kimono | cream, red, gold | silk_crepe, silk | verified |
| footwear | `GAR-0058` | 1970 年代厚底鞋 / 1970s platform shoe | black, gold | leather, metal, rubber | verified |

- 结构卡：STR-0016, STR-0017
- 材质卡：MAT-0002, MAT-0003, MAT-0004

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 15.8 | 13.8 | 15.8 |
| 角色身份 | 3.4 | 3.4 | 3.4 |
| 环境气候 | 3.8 | 6.3 | 1.8 |
| 美术方向 | 6.3 | 3.9 | 6.3 |
| 动作可行 | 5.0 | 4.4 | 4.6 |
| 剧情弧线 | 4.8 | 4.8 | 4.8 |
| 摄影/一致性 | 6.9 | 6.9 | 6.9 |
| **总计** | 46.0 | 44.6 | 43.6 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Aiko, complete set: early 20th-century Japanese kimono, cream silk crepe, silk embroidery, small gold crests, red silk lining, narrow western-style sash, export market; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling, palette: black, cream, gold, red, silver, setting: theatre stage, evening, indoor, art direction: theatre period drama, lighting: warm stage light, camera: medium shot, period-inspired modern interpretation, historical silhouette cues mixed with contemporary construction, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); placket (STR-0017); ease and fit (STR-0025), continuity lock: GAR-0065 export kimono [cream, red, gold; silk_crepe, silk; complete set] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0011, MAT-0014
```

**Video prompt (EN):**

```
Aiko, walking across the stage, scene: theatre stage, evening, indoor, camera: medium shot, costume: complete set: early 20th-century Japanese kimono, cream silk crepe, silk embroidery, small gold crests, red silk lining, narrow western-style sash, export market; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling, fabric motion: natural fabric response to the action, gravity and wind, lighting: warm stage light, period-inspired modern interpretation, historical silhouette cues mixed with contemporary construction, single continuous take, consistent costume and accessories, continuity lock: GAR-0065 export kimono [cream, red, gold; silk_crepe, silk; complete set] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0011, MAT-0014, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Aiko, one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling, palette: black, mid blue, orange red, pink, red, silver, white, setting: theatre stage, evening, indoor, art direction: theatre period drama, lighting: warm stage light, camera: medium shot, period-inspired modern interpretation, historical silhouette cues mixed with contemporary construction, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: frog closure (STR-0011); hem and vents/slits (STR-0016); ease and fit (STR-0025), continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0011
```

**Video prompt (EN):**

```
Aiko, walking across the stage, scene: theatre stage, evening, indoor, camera: medium shot, costume: one-piece: 1930s Shanghai qipao, high stiff stand-up collar, right-side fastening with loop-and-knot buttons, side slits, short sleeves or long tight sleeves, printed devoré velvet or silk damask, art deco lace trim; footwear: 1930s women’s shoes, black lace overlay flat pumps with small pink and green sequins, alternative red and silver floral brocade evening shoes with a silver buckle, art deco styling, fabric motion: 侧衩限制步幅，跨步/上下楼梯时最明显; 贴身剪裁在坐姿时前襟与腰腹起皱; 长紧袖款限制手腕动作; 右衽盘扣与隐藏拉链的开合状态必须跨镜头锁定。, lighting: warm stage light, period-inspired modern interpretation, historical silhouette cues mixed with contemporary construction, single continuous take, consistent costume and accessories, continuity lock: GAR-0031 qipao [white, orange_red, pink, mid_blue; silk, synthetic_velvet, crepe, silk_damask; one-piece] | GAR-0035 1930s women’s shoes [black, red, silver; lace, sequins, silk, metallic_brocade; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0014, MAT-0003, MAT-0011, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Aiko, complete set: early 20th-century Japanese kimono, cream silk crepe, silk embroidery, small gold crests, red silk lining, narrow western-style sash, export market; footwear: 1970s black leather platform shoe, thick rubber sole, twisted gold U-shaped buckle, bold glam rock styling, visible height and weight, palette: black, cream, gold, red, setting: theatre stage, evening, indoor, art direction: theatre period drama, lighting: warm stage light, camera: medium shot, period-inspired modern interpretation, historical silhouette cues mixed with contemporary construction, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: hem and vents/slits (STR-0016); placket (STR-0017), continuity lock: GAR-0065 export kimono [cream, red, gold; silk_crepe, silk; complete set] | GAR-0058 1970s platform shoe [black, gold; leather, metal, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0004
```

**Video prompt (EN):**

```
Aiko, walking across the stage, scene: theatre stage, evening, indoor, camera: medium shot, costume: complete set: early 20th-century Japanese kimono, cream silk crepe, silk embroidery, small gold crests, red silk lining, narrow western-style sash, export market; footwear: 1970s black leather platform shoe, thick rubber sole, twisted gold U-shaped buckle, bold glam rock styling, visible height and weight, fabric motion: natural fabric response to the action, gravity and wind, lighting: warm stage light, period-inspired modern interpretation, historical silhouette cues mixed with contemporary construction, single continuous take, consistent costume and accessories, continuity lock: GAR-0065 export kimono [cream, red, gold; silk_crepe, silk; complete set] | GAR-0058 1970s platform shoe [black, gold; leather, metal, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0004, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

## 风险

### Look A

- 风险：region mismatch in GAR-0035: cards document their own regions, not japan
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look B

- 风险：region mismatch in GAR-0031, GAR-0035: cards document their own regions, not japan
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### Look C

- 风险：region mismatch in GAR-0058: cards document their own regions, not japan
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault

### 脚本级风险与缺口

- [context_gap/medium] no reliable style card for art direction 'theatre period drama'
- [region_mismatch/medium] cards document other regions for GAR-0035, GAR-0058 (requested japan); cross-region borrowing is flagged, not silently accepted
- [occupation_coverage_gap/medium] the vault has no 'dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- no reliable style card for art direction 'theatre period drama'
- cards document other regions for GAR-0035, GAR-0058 (requested japan); cross-region borrowing is flagged, not silently accepted
- the vault has no 'dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted

## 证据

### Look A

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 15.8/25, 摄影/一致性 6.9/10
- 理由（解释性，不是史实）：成套: GAR-0065 出口和服 (ceremonial)
- 理由（解释性，不是史实）：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0016, STR-0017, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0003, MAT-0011, MAT-0014
- source_ids：SRC-0426, SRC-0205, SRC-0206, SRC-0202, SRC-0201, SRC-0108, SRC-0412, SRC-0521, SRC-0520, SRC-0141, SRC-0142, SRC-0423, SRC-0143
- 来源链接：SRC-0426 → https://collections.vam.ac.uk/item/O25781/
- 来源链接：SRC-0205 → https://collections.vam.ac.uk/item/O350849/
- 来源链接：SRC-0206 → https://collections.vam.ac.uk/item/O350850/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0108 → https://fashionhistory.fitnyc.edu/shirtwaist/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 单件证据状态：GAR-0065=verified; GAR-0035=verified

### Look B

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 13.8/25, 摄影/一致性 6.9/10
- 理由（解释性，不是史实）：连身: GAR-0031 旗袍 (smart_casual)
- 理由（解释性，不是史实）：足部: GAR-0035 女式皮鞋 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0011, STR-0016, STR-0025
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0014, MAT-0003, MAT-0011
- 理由（解释性，不是史实）：based on curated vault look card LOOK-0009
- source_ids：SRC-0200, SRC-0201, SRC-0205, SRC-0206, SRC-0202, SRC-0521, SRC-0520, SRC-0141, SRC-0143, SRC-0423, SRC-0142
- 来源链接：SRC-0200 → https://collections.vam.ac.uk/item/O1151302/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0205 → https://collections.vam.ac.uk/item/O350849/
- 来源链接：SRC-0206 → https://collections.vam.ac.uk/item/O350850/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0521 → https://freesewing.dev/howtos/design/fit-sleeve/
- 来源链接：SRC-0520 → https://freesewing.dev/howtos/design/seam-allowance/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 单件证据状态：GAR-0031=verified; GAR-0035=verified

### Look C

- 理由（解释性，不是史实）：highest scoring dimensions: 年代/文化 15.8/25, 摄影/一致性 6.9/10
- 理由（解释性，不是史实）：成套: GAR-0065 出口和服 (ceremonial)
- 理由（解释性，不是史实）：足部: GAR-0058 1970 年代厚底鞋 (smart_casual)
- 理由（解释性，不是史实）：linked structure cards: STR-0016, STR-0017
- 理由（解释性，不是史实）：linked material cards: MAT-0002, MAT-0003, MAT-0004
- source_ids：SRC-0426, SRC-0418, SRC-0202, SRC-0201, SRC-0108, SRC-0412, SRC-0141, SRC-0142, SRC-0143
- 来源链接：SRC-0426 → https://collections.vam.ac.uk/item/O25781/
- 来源链接：SRC-0418 → https://collections.vam.ac.uk/item/O1380038/
- 来源链接：SRC-0202 → https://collections.vam.ac.uk/item/O80590/
- 来源链接：SRC-0201 → https://collections.vam.ac.uk/item/O107537/
- 来源链接：SRC-0108 → https://fashionhistory.fitnyc.edu/shirtwaist/
- 来源链接：SRC-0412 → https://collections.vam.ac.uk/item/O15693/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0143 → https://fashionhistory.fitnyc.edu/lurex/
- 单件证据状态：GAR-0065=verified; GAR-0058=verified

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| ids_exist | PASS | all garment ids resolvable: True |
| no_crash | PASS | recommend.py exit=0 (must be 0, no KeyError/uncaught exception) |
| query_hits | PASS | query.py exit=0, hits=5, ids=GAR-0001, GAR-0065, GAR-0066, SRC-0009, SRC-0028 |
| query_no_duplicate_names | PASS | duplicate names in query top5=[] |
| query_no_example_top | PASS | example ids in query top5=[] |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable style card for art direction 'theatre period drama'
- 脚本警告：cards document other regions for GAR-0035, GAR-0058 (requested japan); cross-region borrowing is flagged, not silently accepted
- 脚本警告：the vault has no 'dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

