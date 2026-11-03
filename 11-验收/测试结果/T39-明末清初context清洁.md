# T39 — 明末清初：context_refs 不得引用 1770s/维多利亚等无关卡

- 运行时间：2026-11-04T03:02:24+08:00
- 测试类型：historical_weak_coverage, context, M4
- 模式：standard
- 输入文件：`11-验收/测试输入/T39-明末清初context清洁.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T39-明末清初context清洁.json --json`
- 退出码：**0**（耗时 0.84s）

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

## 检索执行记录

| 命令 | 退出码 | 耗时 |
| --- | --- | --- |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T39-明末清初context清洁.json --json` | 0 | 0.84s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py china --limit 6 --json` | 0 | 0.77s |

- `query.py` 命中数量：**6**（验收要求 ≥1）
- `query.py` 命中卡片 ID：GAR-0031, GAR-0032, GAR-0067, LOOK-0008, LOOK-0009, LOOK-0012
- `recommend.py` 候选池：accessory=GAR-0028, GAR-0021, GAR-0025, GAR-0026; carried_prop=GAR-0049; footwear=GAR-0024; inner_layer=GAR-0020; lower_body=GAR-0013; one_piece=GAR-0062, GAR-0015; outerwear=GAR-0016, GAR-0017, GAR-0018; upper_body=GAR-0002, GAR-0008, GAR-0003
- 三套推荐选中：A: GAR-0002, GAR-0013, GAR-0024; B: GAR-0015, GAR-0024, GAR-0028; C: GAR-0062, GAR-0024

## 候选造型 A/B/C

### Look A（score 28.2/100，cost 0.477，source_look=LOOK-0003）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0002` | 达布里特 / doublet | black, red, slashed_contrast | wool, silk, linen | verified |
| lower_body | `GAR-0013` | 遮阴袋 / codpiece | contrast_color, gold | wool, silk, velvet | verified |
| footwear | `GAR-0024` | 穆勒鞋 / mule | red, silk, gold | leather, silk, velvet | verified |

- 结构卡：STR-0003, STR-0005, STR-0006, STR-0010, STR-0001
- 材质卡：MAT-0002, MAT-0003, MAT-0011

### Look B（score 28.0/100，cost 0.555，source_look=LOOK-0001）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0015` | 法式长袍 / robe à la française | pastel, silk_floral, cream | silk, brocade, lace | verified |
| footwear | `GAR-0024` | 穆勒鞋 / mule | red, silk, gold | leather, silk, velvet | verified |
| accessory | `GAR-0028` | 手笼 / muff | fur_brown, white, silk | fur, silk, wool | verified |

- 结构卡：STR-0006, STR-0009
- 材质卡：MAT-0002, MAT-0003, MAT-0011

### Look C（score 26.1/100，cost 0.542，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| one_piece | `GAR-0062` | 意大利文艺复兴长袍 / Italian Renaissance gown | cream, green, pink, yellow, blue | silk, fustian | verified |
| footwear | `GAR-0024` | 穆勒鞋 / mule | red, silk, gold | leather, silk, velvet | verified |

- 结构卡：STR-0001, STR-0003
- 材质卡：MAT-0002, MAT-0003

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 7.6 | 7.4 | 8.3 |
| 角色身份 | 3.4 | 3.4 | 3.4 |
| 环境气候 | 1.8 | 1.8 | 1.8 |
| 美术方向 | 0.0 | 0.0 | 0.0 |
| 动作可行 | 4.4 | 4.5 | 4.6 |
| 剧情弧线 | 3.5 | 3.5 | 3.5 |
| 摄影/一致性 | 6.5 | 6.5 | 6.5 |
| **总计** | 28.2 | 28.0 | 26.1 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult 顾砚秋, upper body: men’s fitted doublet, long sleeves, standing neckband, center-front lacing or buttons, nipped waist; lower body: padded Renaissance codpiece, prominent front pouch at the fork of the hose, decorated with slashing, embroidery or jewels; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, palette: black, contrast color, gold, red, silk, slashed contrast, setting: 书院讲堂, day, overcast, dry, art direction: 文人水墨、克制、低饱和, lighting: 阴天窗光, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: ruff (STR-0003); leg-of-mutton sleeves (STR-0005); stomacher (STR-0006); slashing (STR-0010); Medici collar (STR-0001), continuity lock: GAR-0002 doublet [black, red, slashed_contrast; wool, silk, linen; upper body] | GAR-0013 codpiece [contrast_color, gold; wool, silk, velvet; lower body] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0011 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
顾砚秋, 讲学、整理书箱, scene: 书院讲堂, day, overcast, dry, camera: medium shot, costume: upper body: men’s fitted doublet, long sleeves, standing neckband, center-front lacing or buttons, nipped waist; lower body: padded Renaissance codpiece, prominent front pouch at the fork of the hose, decorated with slashing, embroidery or jewels; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, fabric motion: 固定在长袜/裤裆前，行走与坐下时位置明显; 不能在高动作镜头中忽略其体积。; 合体收腰，抬臂时肩袖与后背拉扯明显; 下摆短或带垂片，需与袜带/裤装固定关系。, lighting: 阴天窗光, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0002 doublet [black, red, slashed_contrast; wool, silk, linen; upper body] | GAR-0013 codpiece [contrast_color, gold; wool, silk, velvet; lower body] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0011, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult 顾砚秋, one-piece: 18th-century robe à la française, fitted front bodice, loose back with two box pleats falling from shoulders to hem, panniers, silk brocade; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court; accessory: fur muff, cylindrical hand warmer, hands inserted from both ends, suspended by a silk cord, 18th-century winter accessory, palette: cream, fur brown, gold, pastel, red, silk, silk floral, white, setting: 书院讲堂, day, overcast, dry, art direction: 文人水墨、克制、低饱和, lighting: 阴天窗光, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: stomacher (STR-0006); panniers (STR-0009), continuity lock: GAR-0015 robe à la française [pastel, silk_floral, cream; silk, brocade, lace; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear] | GAR-0028 muff [fur_brown, white, silk; fur, silk, wool; accessory]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0011 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
顾砚秋, 讲学、整理书箱, scene: 书院讲堂, day, overcast, dry, camera: medium shot, costume: one-piece: 18th-century robe à la française, fitted front bodice, loose back with two box pleats falling from shoulders to hem, panniers, silk brocade; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court; accessory: fur muff, cylindrical hand warmer, hands inserted from both ends, suspended by a silk cord, 18th-century winter accessory, fabric motion: 背部箱褶与裙撑使转身半径大; 快走时裙摆与后褶大幅摆动，需固定裙撑位置。, lighting: 阴天窗光, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0015 robe à la française [pastel, silk_floral, cream; silk, brocade, lace; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear] | GAR-0028 muff [fur_brown, white, silk; fur, silk, wool; accessory]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, MAT-0011, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult 顾砚秋, one-piece: late Renaissance Italian silk gown, cream brocaded floral motifs, diagonal slashing between motifs, sleeveless open front, small upright back collar, shoulder wings, box-pleated back; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, palette: blue, cream, gold, green, pink, red, silk, yellow, setting: 书院讲堂, day, overcast, dry, art direction: 文人水墨、克制、低饱和, lighting: 阴天窗光, camera: medium shot, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, realistic fabric texture, visible seams and construction details, cinematic costume reference, construction details: Medici collar (STR-0001); ruff (STR-0003), continuity lock: GAR-0062 Italian Renaissance gown [cream, green, pink, yellow, blue; silk, fustian; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
顾砚秋, 讲学、整理书箱, scene: 书院讲堂, day, overcast, dry, camera: medium shot, costume: one-piece: late Renaissance Italian silk gown, cream brocaded floral motifs, diagonal slashing between motifs, sleeveless open front, small upright back collar, shoulder wings, box-pleated back; footwear: backless mule slippers, vamp only with no quarters, silk or velvet, embroidered, high heel, worn indoors or at court, fabric motion: 无袖开襟长袍依赖内层固定; 剪口与金属饰边易勾挂; 长摆限制步幅。, lighting: 阴天窗光, historically grounded period costume, period-accurate construction and materials, no modern fashion elements, single continuous take, consistent costume and accessories, continuity lock: GAR-0062 Italian Renaissance gown [cream, green, pink, yellow, blue; silk, fustian; one-piece] | GAR-0024 mule [red, silk, gold; leather, silk, velvet; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0002, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots, no modern zippers, no modern sneakers, no printed t-shirts, no anachronistic plastic accessories
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 7.6/25, 摄影/一致性 6.5/10
- 理由：上装: GAR-0002 达布里特 (formal)
- 理由：下装: GAR-0013 遮阴袋 (unknown)
- 理由：足部: GAR-0024 穆勒鞋 (formal)
- 理由：linked structure cards: STR-0003, STR-0005, STR-0006, STR-0010, STR-0001
- 理由：linked material cards: MAT-0002, MAT-0003, MAT-0011
- 理由：based on curated vault look card LOOK-0003
- 风险：region mismatch in GAR-0002, GAR-0013, GAR-0024: cards document their own regions, not jiangnan china
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0103, SRC-0114, SRC-0125, SRC-0133, SRC-0135, SRC-0136, SRC-0140, SRC-0101, SRC-0141, SRC-0142, SRC-0423
- 来源链接：SRC-0103 → https://fashionhistory.fitnyc.edu/doublet/
- 来源链接：SRC-0114 → https://fashionhistory.fitnyc.edu/codpiece/
- 来源链接：SRC-0125 → https://fashionhistory.fitnyc.edu/mule/
- 来源链接：SRC-0133 → https://fashionhistory.fitnyc.edu/ruff/
- 来源链接：SRC-0135 → https://fashionhistory.fitnyc.edu/leg-of-mutton-sleeves/
- 来源链接：SRC-0136 → https://fashionhistory.fitnyc.edu/stomacher/
- 来源链接：SRC-0140 → https://fashionhistory.fitnyc.edu/slashing/
- 来源链接：SRC-0101 → https://fashionhistory.fitnyc.edu/medici-collar/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/

### Look B

- 理由：highest scoring dimensions: 年代/文化 7.4/25, 摄影/一致性 6.5/10
- 理由：连身: GAR-0015 法式长袍 (ceremonial)
- 理由：足部: GAR-0024 穆勒鞋 (formal)
- 理由：配饰: GAR-0028 手笼 (formal)
- 理由：linked structure cards: STR-0006, STR-0009
- 理由：linked material cards: MAT-0002, MAT-0003, MAT-0011
- 理由：based on curated vault look card LOOK-0001
- 风险：low budget: relatively expensive materials
- 风险：region mismatch in GAR-0015, GAR-0024, GAR-0028: cards document their own regions, not jiangnan china
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0116, SRC-0129, SRC-0125, SRC-0136, SRC-0139, SRC-0141, SRC-0142, SRC-0423
- 来源链接：SRC-0116 → https://fashionhistory.fitnyc.edu/robe-a-la-francaise/
- 来源链接：SRC-0129 → https://fashionhistory.fitnyc.edu/muff/
- 来源链接：SRC-0125 → https://fashionhistory.fitnyc.edu/mule/
- 来源链接：SRC-0136 → https://fashionhistory.fitnyc.edu/stomacher/
- 来源链接：SRC-0139 → https://fashionhistory.fitnyc.edu/panniers/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/
- 来源链接：SRC-0423 → https://collections.vam.ac.uk/item/O315431/

### Look C

- 理由：highest scoring dimensions: 年代/文化 8.3/25, 摄影/一致性 6.5/10
- 理由：连身: GAR-0062 意大利文艺复兴长袍 (formal)
- 理由：足部: GAR-0024 穆勒鞋 (formal)
- 理由：linked structure cards: STR-0001, STR-0003
- 理由：linked material cards: MAT-0002, MAT-0003
- 风险：region mismatch in GAR-0062, GAR-0024: cards document their own regions, not jiangnan china
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0422, SRC-0125, SRC-0101, SRC-0133, SRC-0141, SRC-0142
- 来源链接：SRC-0422 → https://collections.vam.ac.uk/item/O74085/
- 来源链接：SRC-0125 → https://fashionhistory.fitnyc.edu/mule/
- 来源链接：SRC-0101 → https://fashionhistory.fitnyc.edu/medici-collar/
- 来源链接：SRC-0133 → https://fashionhistory.fitnyc.edu/ruff/
- 来源链接：SRC-0141 → https://fashionhistory.fitnyc.edu/chantilly-lace/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/

## 验收判定

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| structured_result | PASS | exit=0 looks=3 ids_exist=True warnings=True |
| warning_absent:rainwear_gap | PASS | warning 'rainwear_gap' present? False (codes=['context_gap', 'context_gap', 'period_approximate', 'period_era_level', 'region_mismatch', 'occupation_coverage_gap']) |
| warnings_present | PASS | wytyczne count=6 codes=['context_gap', 'context_gap', 'period_approximate', 'period_era_level', 'region_mismatch', 'occupation_coverage_gap'] |
| context_refs_clean | PASS | refs=0 bad=[] example_refs=[] |
| no_example_in_a | PASS | Look A example ids=[] contains_example=False |
| narrative_present | PASS | missing narrative for none |
| no_prompt_contamination | PASS | no cross-scene/card-text contamination |
| query_hits | PASS | query.py exit=0, hits=6, ids=GAR-0031, GAR-0032, GAR-0067, LOOK-0008, LOOK-0009, LOOK-0012 |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable period/region context card after period/region normalization (requested: 1644 late Ming early Qing / jiangnan china)
- 脚本警告：no reliable style card for art direction '文人水墨、克制、低饱和'
- 脚本警告：period evidence is approximate/none for GAR-0013, GAR-0015 (requested 1644 late Ming early Qing); treat these as era-level hypotheses, not exact period matches
- 脚本警告：period evidence is era-level (century bucket) for GAR-0002, GAR-0024, GAR-0028, GAR-0062; exact-decade cards are missing
- 脚本警告：cards document other regions for GAR-0002, GAR-0013, GAR-0015, GAR-0024, GAR-0028, GAR-0062 (requested jiangnan china); cross-region borrowing is flagged, not silently accepted
- 脚本警告：the vault has no '书院教师、江南文人'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

