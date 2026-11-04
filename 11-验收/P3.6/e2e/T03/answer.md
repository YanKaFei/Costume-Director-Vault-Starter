All scripts run; here is the design report.

## Brief
- 1930s / 上海 / 民国写实（historical）/ medium 预算；脚本事实=雨、风、夜、街道→报馆。
- unknowns：季节、美术风格、灯光、人物社会关系（脚本未给，不臆造）。

## Characters
沈宜（Shen Yi）：女记者，中产，截稿前抢发头条；两场均在场。脚本两场均在，无遗漏角色。

## Scene table
| Scene | Character | Stage | A | B | C | State |
|---|---|---|---|---|---|---|
| S1 雨夜街道 | 沈宜 | ST1 | GAR-0031/0045/0035/**0047** | GAR-0031/0045/0035/**0048** | GAR-0031/0045/**0060** | wet/none/none |
| S2 报馆办公室 | 沈宜 | ST2 | 同上 A | 同上 B | 同上 C | damp/none/none |

checks：three_looks / abc_distinct / complete_looks / evidence_complete 均 true，continuity_issues=0。

## Looks（均 verified 单品；造型卡 LOOK-0012 为 interpretive）
- 共有：GAR-0031 旗袍（silk/crepe/damask，SRC-0200 vam.ac.uk/item/O1151302、SRC-0201 /O107537）；GAR-0045 风衣（gabardine，SRC-0405 /O1295635）。
- **A**：+GAR-0035 黑蕾丝平底女鞋（SRC-0205 /O350849、SRC-0206 /O350850）+GAR-0047 1927 丝面银柄雨伞（SRC-0407 /O470711）。
- **B**：+GAR-0035 +GAR-0048 刺绣帆布手袋（SRC-0408 /O367714）；携带手袋替代雨伞。
- **C**：+GAR-0060 约1935 男式牛津皮鞋（leather/suede，SRC-0420 /O135417）；中性、行动感，缺伞/包。
- 叙事理由（导演推断，非服装史）：旗袍示职业女性身份，风衣统一雨夜类型，A/B/C 在"携带物+鞋"上分情绪温度。

## Continuity
- anchors：同一套 ID 贯穿 S1→S2（无换装，仅脱衣动作：风衣搭椅背、伞收拢）。
- state chain：S1 wet（风衣雨珠、鞋踩水）→ S2 damp（旗袍肩部洇深、地板水印）；damage/dirt=none。禁止镜头间瞬干。

## English prompts
**Image (A/ST1):** `1930s Shanghai woman journalist, GAR-0031 fitted qipao (silk damask, mandarin collar, side slits) under GAR-0045 belted double-breasted khaki gabardine trench, GAR-0035 black lace flat pumps, holding GAR-0047 black silk silver-handled umbrella; rain-soaked street, neon reflected in puddles, night; wetness=wet, damage=none, dirt=none.`
**Video:** 同描述 + `walking briskly, entering office, closing dripping umbrella, draping coat on chair, wetness wet→damp, qipao shoulders darken; negative: no costume morphing, no color shift, no instant drying, no modern zippers/sneakers/plastic, no logos/watermark.`
（B 换 GAR-0048 handbag；C 换 GAR-0060 men’s Oxfords，damp 状态同锁。）

## Evidence vs inference
事实：雨/风/夜/湿（脚本、meta）。证据：上列 GAR/SRC 均经 query.py 解析，URL 为 V&A 藏品页。推断：心理与阶级叙事、A/B/C 情绪分工。

## Gaps / 缺证据
1. GAR-0045、0047 仅"世纪级"年代证据，无精确十年卡；SRC-0405 实为 2014 Burberry（形制借用，非1930实物）。
2. 除 GAR-0031 外，0035/0045/0047/0048/0060 均非上海地区卡，属跨地域借用（脚本已标记）。
3. GAR-0035 精致蕾丝鞋与雨天冲突（severity medium）；更合适的 GAR-0046 橡胶雨衣（SRC-0406，约1920）因年代/评分被引擎拒用，可作现场备选，但同样非上海精确证据。
4. 无上海本地产雨靴/女记者专用职业装卡，此为知识库真实缺口，未以虚构卡填补。

输出存于 `projects/shanghai-journalist/outputs/`。
