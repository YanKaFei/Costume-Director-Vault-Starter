## Brief
- 角色：1930 年代上海女记者（外勤采访、伏案写稿、夜间奔波）
- 设定依据：用户给定年代/地域/职业；季节、预算、具体剧本场景均为 unknown
- 结构证据：经 `python3 scripts/query.py --id` 调取，三卡均为 **verified**

## 引用结构卡（真实查询结果）
| ID | 名称 | 结构说明（卡内要点） | SRC |
|---|---|---|---|
| **STR-0012** | 翻领与驳领 turndown collar and lapel | 翻领=领座+领面沿领口翻折；驳领=门襟外翻驳头，分平驳/戗驳/青果领；领面领底用衬控挺度，驳头领边明线 | SRC-0118（FIT，frock coat：https://fashionhealth.fitnyc.edu/frock-coat/） |
| **STR-0013** | 装袖与插肩袖 set-in / raglan sleeve | 装袖：袖山吃势缝入袖窿、肩缝独立；插肩袖：袖片延伸至领口、领口到腋下斜缝无肩缝，活动量大 | SRC-0406（V&A 约1920橡胶丝雨衣 raglan shoulders，O361727）；SRC-0484（V&A 1618 doublet 两片弯装袖，O356786） |
| **STR-0014** | 肩线与肩垫 shoulder line & pad | 肩缝位置+肩垫（羊毛毡/马尾衬）决定轮廓；1930—40 年代方肩、肩点抬高，可拆或缝死；限制抬臂 | SRC-0412（V&A 1942 Utility 日装裙 padded shoulders，O15693） |

## 结构方案（女记者）
- **领口 STR-0012**：及膝修身旗袍或羊毛日装裙外，配一件精纺羊毛西装外套，取**平驳领（notched lapel）**、领座偏低、驳头窄而利落——报馆职业感、可迅速整理；内搭衬衫翻领露出领尖。避免戗驳领（过于正式晚宴化）。
- **袖型 STR-0013 分场景双配置**：
  - A 报馆/采访：外套用**装袖**，袖窿明确、配 defined armhole，剪裁专业；
  - B 雨夜外勤/黄包车奔波：备用**插肩袖雨衣**（raglan，领口至腋下斜缝），抬臂记录、撑伞不受限——直接对应 SRC-0406 的 1920 雨衣先例。
- **肩线 STR-0014**：采用 1930 年代平直**薄垫肩方肩**（羊毛毡、可拆式），肩点微抬不夸张，塑造独立、职业化的"新女性"权力轮廓；动作戏时拆除。装袖与垫肩同框时袖窿须归拔到位。
- 英文提示词可用三卡原句组合：`1930s tailored wool jacket, notched lapel, set-in sleeve with defined armhole, padded squared shoulders`；雨备选 `raglan-sleeve raincoat, diagonal shoulder seams`。

## 证据与缺口
- **verified 证据**：结构本身及年代适用性来自 STR-0012/13/14 与上述 SRC。
- **interpretive（设计推断）**：三卡来源均为英国/欧洲馆藏（FIT、V&A），"1930s 上海女记者采用西装剪裁+旗袍叠穿"属跨地域推断；库内无上海本地结构来源卡，不得声称为本地实物佐证。
- **unknown**：季节、预算、昼夜、天气、动作量、是否真有旗袍层——建议据此再跑 `recommend.py` 补齐全套件 ID。
