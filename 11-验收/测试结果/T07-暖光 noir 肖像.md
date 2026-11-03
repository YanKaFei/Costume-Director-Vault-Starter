# T07 — 暖光肖像：同一角色的冷暖光对照（warm lighting）

- 运行时间：2026-11-04T02:24:49+08:00
- 测试类型：warm_cool_lighting
- 模式：standard
- 输入文件：`11-验收/测试输入/T07-暖光 noir 肖像.json`
- 运行命令：`/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T07-暖光 noir 肖像.json --json`
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
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/recommend.py /Users/coffee/Desktop/Costume-Director-Vault-Starter/11-验收/测试输入/T07-暖光 noir 肖像.json --json` | 0 | 1.51s |
| `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/query.py noir coat --limit 6 --json` | 0 | 0.75s |

- `query.py` 命中数量：**5**（验收要求 ≥1）
- `query.py` 命中卡片 ID：STY-0005, LOOK-0021, STY-EXAMPLE-001, LOOK-0007, LOOK-EXAMPLE-001
- `recommend.py` 候选池：accessory=GAR-0070, GAR-0050, GAR-0051, GAR-0039, GAR-0027, GAR-0021, GAR-0026, GAR-0068, GAR-0067, GAR-0066, GAR-0028, GAR-0025; carried_prop=GAR-0047, GAR-0048, GAR-0049; footwear=GAR-0022, GAR-0044, GAR-0023, GAR-0035, GAR-0060, GAR-0058, GAR-0024; inner_layer=GAR-0020, GAR-0012; lower_body=GAR-0014, GAR-0010, GAR-0011, GAR-0059, GAR-0013; one_piece=GAR-0063, GAR-0069, GAR-0064, GAR-0031, GAR-0032, GAR-0015, GAR-0056, GAR-0055, GAR-0052, GAR-0004, GAR-0053, GAR-0054, GAR-0062, GAR-0061, GAR-0009, GAR-0029; outerwear=GAR-0045, GAR-0041, GAR-0019, GAR-0046, GAR-0057, GAR-0033, GAR-0017, GAR-0040, GAR-0016, GAR-0037, GAR-0018; set=GAR-0042, GAR-0005, GAR-0065, GAR-0001, GAR-0036, GAR-0030; upper_body=GAR-EXAMPLE-001, GAR-0043, GAR-0006, GAR-0008, GAR-0007, GAR-0034, GAR-0002, GAR-0003
- 三套推荐选中：A: GAR-0042, GAR-0041, GAR-0044; B: GAR-0043, GAR-0014, GAR-0041, GAR-0022; C: GAR-0042, GAR-0041, GAR-0022

## 候选造型 A/B/C

### Look A（score 50.4/100，cost 0.213，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| set | `GAR-0042` | 警察制服 / police uniform | navy, black | wool, polyester, cotton | interpretive |
| outerwear | `GAR-0041` | 医生白袍 / doctor’s white coat | white | cotton, polyester | interpretive |
| footwear | `GAR-0044` | 医疗工作鞋 / medical work shoes | white, black | leather, rubber, synthetic | interpretive |
- 材质卡：MAT-0001, MAT-0003

### Look B（score 49.8/100，cost 0.220，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| upper_body | `GAR-0043` | 厨师服 / chef’s jacket | white, black | cotton, polyester | interpretive |
| lower_body | `GAR-0014` | 牛仔裤 / jeans | indigo, blue_black | denim, cotton | verified |
| outerwear | `GAR-0041` | 医生白袍 / doctor’s white coat | white | cotton, polyester | interpretive |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
- 材质卡：MAT-0001, MAT-0003

### Look C（score 49.3/100，cost 0.208，source_look=assembled）

| 层级 | ID | 名称 | 颜色 | 材质 | 证据 |
| --- | --- | --- | --- | --- | --- |
| set | `GAR-0042` | 警察制服 / police uniform | navy, black | wool, polyester, cotton | interpretive |
| outerwear | `GAR-0041` | 医生白袍 / doctor’s white coat | white | cotton, polyester | interpretive |
| footwear | `GAR-0022` | 威灵顿靴 / wellington boot | black, brown | leather, rubber | verified |
- 材质卡：MAT-0001, MAT-0003

### 评分明细

| 维度 | A | B | C |
| --- | --- | --- | --- |
| 年代/文化 | 23.0 | 23.0 | 23.0 |
| 角色身份 | 4.0 | 4.0 | 4.2 |
| 环境气候 | 1.8 | 1.8 | 1.8 |
| 美术方向 | 3.4 | 4.1 | 4.1 |
| 动作可行 | 4.0 | 4.0 | 4.0 |
| 剧情弧线 | 5.6 | 6.2 | 5.6 |
| 摄影/一致性 | 6.5 | 6.6 | 6.6 |
| **总计** | 50.4 | 49.8 | 49.3 |

## 生图 / 视频 Prompt（实际输出）

### Look A

**Image prompt (EN):**

```
full-body character design of an adult Lin, complete set: police uniform, badge and number, belt with equipment, polished shoes, high-visibility variant; outer layer: knee-length white medical coat, button front, breast pocket with pen, side pockets, clean or slightly worn cotton, stethoscope around neck; footwear: white closed-toe medical work shoes, low heel, non-slip rubber sole, lace-up or slip-on, clean but worn, hospital lighting, palette: black, navy, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-0042 police uniform [navy, black; wool, polyester, cotton; complete set] | GAR-0041 doctor’s white coat [white; cotton, polyester; outer layer] | GAR-0044 medical work shoes [white, black; leather, rubber, synthetic; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: complete set: police uniform, badge and number, belt with equipment, polished shoes, high-visibility variant; outer layer: knee-length white medical coat, button front, breast pocket with pen, side pockets, clean or slightly worn cotton, stethoscope around neck; footwear: white closed-toe medical work shoes, low heel, non-slip rubber sole, lace-up or slip-on, clean but worn, hospital lighting, fabric motion: 及膝/大腿长度限制快走; 口袋负重会拉扯衣身; 扣合状态需跨镜头锁定。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0042 police uniform [navy, black; wool, polyester, cotton; complete set] | GAR-0041 doctor’s white coat [white; cotton, polyester; outer layer] | GAR-0044 medical work shoes [white, black; leather, rubber, synthetic; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look B

**Image prompt (EN):**

```
full-body character design of an adult Lin, upper body: white chef’s jacket, double-breasted front, mandarin collar, long sleeves, cloth buttons, apron and tall toque, kitchen setting; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: knee-length white medical coat, button front, breast pocket with pen, side pockets, clean or slightly worn cotton, stethoscope around neck; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: black, blue black, brown, indigo, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-0043 chef’s jacket [white, black; cotton, polyester; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0041 doctor’s white coat [white; cotton, polyester; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: upper body: white chef’s jacket, double-breasted front, mandarin collar, long sleeves, cloth buttons, apron and tall toque, kitchen setting; lower body: 1950s blue denim jeans, straight or slim cut, working-class youth styling, visible wear at knees; outer layer: knee-length white medical coat, button front, breast pocket with pen, side pockets, clean or slightly worn cotton, stethoscope around neck; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 及膝/大腿长度限制快走; 口袋负重会拉扯衣身; 扣合状态需跨镜头锁定。; 丹宁较硬，新裤在蹲坐时有明显折痕; 旧化后膝部与裆部会形成固定褶皱，跨镜头需保持一致。; 双排扣与长袖在炉灶旁限制动作; 围裙/帽子的系带需锁定。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0043 chef’s jacket [white, black; cotton, polyester; upper body] | GAR-0014 jeans [indigo, blue_black; denim, cotton; lower body] | GAR-0041 doctor’s white coat [white; cotton, polyester; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

### Look C

**Image prompt (EN):**

```
full-body character design of an adult Lin, complete set: police uniform, badge and number, belt with equipment, high-visibility variant; outer layer: knee-length white medical coat, button front, breast pocket with pen, side pockets, clean or slightly worn cotton, stethoscope around neck; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, palette: black, brown, navy, white, setting: S7, night, dry, art direction: restrained urban noir, lighting: warm tungsten key light, golden amber practicals, deep shadow, camera: close-up, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, realistic fabric texture, visible seams and construction details, cinematic costume reference, continuity lock: GAR-0042 police uniform [navy, black; wool, polyester, cotton; complete set] | GAR-0041 doctor’s white coat [white; cotton, polyester; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003 --ar 2:3 --style raw --v 6
```

**Video prompt (EN):**

```
Lin, standing still under a streetlamp, scene: S7, night, dry, camera: close-up, costume: complete set: police uniform, badge and number, belt with equipment, high-visibility variant; outer layer: knee-length white medical coat, button front, breast pocket with pen, side pockets, clean or slightly worn cotton, stethoscope around neck; footwear: water-repellent leather, seam at the ankle, boot pulls at the top, oak-tanned soles and rubber heels, fabric motion: 及膝/大腿长度限制快走; 口袋负重会拉扯衣身; 扣合状态需跨镜头锁定。, lighting: warm tungsten key light, golden amber practicals, deep shadow, original fictional-world costume design, explicitly not a historical reconstruction, internally consistent world-building, single continuous take, consistent costume and accessories, continuity lock: GAR-0042 police uniform [navy, black; wool, polyester, cotton; complete set] | GAR-0041 doctor’s white coat [white; cotton, polyester; outer layer] | GAR-0022 wellington boot [black, brown; leather, rubber; footwear]; wetness=dry; damage=none; dirt=none; keep all IDs, colors, materials, trims and accessory positions constant across shots; fabric links: MAT-0001, MAT-0003, negative constraints: no costume morphing between shots, no unexpected accessories, no color shift, no logo, text or watermark, no extra layers appearing or disappearing, no warped hands, no deformed body, no changing hairstyle between shots
```

## 风险与证据

### Look A

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.5/10
- 理由：成套: GAR-0042 警察制服 (functional)
- 理由：外层: GAR-0041 医生白袍 (functional)
- 理由：足部: GAR-0044 医疗工作鞋 (functional)
- 理由：linked material cards: MAT-0001, MAT-0003
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0042, GAR-0041, GAR-0044: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0102, SRC-0142
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/

### Look B

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.6/10
- 理由：上装: GAR-0043 厨师服 (functional)
- 理由：下装: GAR-0014 牛仔裤 (casual)
- 理由：外层: GAR-0041 医生白袍 (functional)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked material cards: MAT-0001, MAT-0003
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0043, GAR-0014, GAR-0041, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0115, SRC-0123, SRC-0102, SRC-0142
- 来源链接：SRC-0115 → https://fashionhistory.fitnyc.edu/1950-1959/
- 来源链接：SRC-0123 → https://fashionhistory.fitnyc.edu/wellington-boot/
- 来源链接：SRC-0102 → https://fashionhistory.fitnyc.edu/muslin/
- 来源链接：SRC-0142 → https://fashionhistory.fitnyc.edu/passementerie/

### Look C

- 理由：highest scoring dimensions: 年代/文化 23.0/25, 摄影/一致性 6.6/10
- 理由：成套: GAR-0042 警察制服 (functional)
- 理由：外层: GAR-0041 医生白袍 (functional)
- 理由：足部: GAR-0022 威灵顿靴 (smart_casual)
- 理由：linked material cards: MAT-0001, MAT-0003
- 风险：fictional mode: no historical claim is made for this design
- 风险：region mismatch in GAR-0042, GAR-0041, GAR-0022: cards document their own regions, not unspecified city
- 风险：character psychology is a directorial interpretation, not a clothing-history fact
- 风险：all images remain external links; no third-party images are embedded in the vault
- source_ids：SRC-0123, SRC-0102, SRC-0142
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
| query_hits | PASS | query.py exit=0, hits=5, ids=STY-0005, LOOK-0021, STY-EXAMPLE-001, LOOK-0007, LOOK-EXAMPLE-001 |
| lighting_pair（pair） | PASS | A item overlap=3, prompts differ=True |

**VERDICT: PASS**

## 备注

- 脚本警告：no reliable style card for art direction 'restrained urban noir'
- 脚本警告：no occupational garment cards match 'private investigator'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- 脚本警告：No cheaper distinct combination was available in the vault; Look C is an art-direction alternative at equivalent cost, explicitly explained.
- 本文件由 `scripts/run_acceptance.py` 依据真实子进程输出生成；PASS/FAIL 只对应上方检查项。
- 知识库为运行时刻快照；新增卡片后必须重跑本测试。

