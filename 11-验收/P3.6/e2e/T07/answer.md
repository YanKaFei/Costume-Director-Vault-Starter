已运行 `scripts/recommend.py`（输入：`projects/shanghai-rain/input.json`，checks 全过：`three_looks/abc_distinct/complete_looks/history_evidence=true`，无冲突），并用 `scripts/query.py` 核验全部卡 ID 与 SRC 真实存在（evidence=verified）。

## Brief
- 1930s / 上海 / 历史考据（historical）/ 中预算；雨夜街道、夜景、步行；秋、艺术指导等为推断（unknown）。

## A 套造型（LOOK-0012，exact 级，无 example 卡）
| 层 | 卡 ID | 名称 | 色/材质 | SRC（均 V&A） |
|---|---|---|---|---|
| 主体 | **GAR-0031** | 旗袍 qipao | 白/橘红/粉/中蓝；丝、绉、花缎 | SRC-0200（[O1151302](https://collections.vam.ac.uk/item/O1151302/)，约1930上海新新公司）、SRC-0201（[O107537](https://collections.vam.ac.uk/item/O107537/)，1930s末花缎） |
| 外套 | **GAR-0045** | 风衣 trench coat | 卡其/米；华达呢、棉 | SRC-0405（[O1295635](https://collections.vam.ac.uk/item/O1295635/)） |
| 鞋 | **GAR-0035** | 女式皮鞋 | 黑/红/银 | SRC-0205（[O350849](https://collections.vam.ac.uk/item/O350849/)）、SRC-0206（[O350850](https://collections.vam.ac.uk/item/O350850/)） |
| 道具 | **GAR-0047** | 雨伞 umbrella | 黑/银；丝绸、银柄、木 | SRC-0407（[O470711](https://collections.vam.ac.uk/item/O470711/)，约1927） |

**设计理由**：旗袍立裁便利步行，华达呢风衣挡雨，米色/卡其/黑压控夜色温度，银柄伞呼应湿地反光，契合"赶稿"叙事。

**风险/冲突**：SRC-0405 实为 2014 Burberry Prorsum **蕾丝**风衣，仅时代廓形依据（period_tier=era, region=none），实拍应改用棉华达呢；SRC-0206 为晚宴鞋，雨夜宜取 SRC-0205 平底便鞋。

## Gaps
记者职业无专属卡（occupation_match=false，37 卡被拒）；风衣/伞/鞋非上海地域卡；湿态为场景设定（推断）。

（正文约 480 字）

---

## Follow-up (same session)

## A 套·雨夜实用版（基于 LOOK-0012 手工替换，ID 均经 query.py 核验为 verified）

**保留（连续性锚点）**
- **GAR-0031** 旗袍（SRC-0200 / SRC-0201）：仍是人物身份锚点；雨夜下摆提高 3–5 cm、露出湿痕。
- **GAR-0047** 雨伞（SRC-0407）：道具连续性保留，作为风大时的备用而非主防雨。

**改动点（2 处）**
1. 外套 **GAR-0045** 蕾丝风衣（SRC-0405 为 2014 蕾丝款，不挡雨）→ **GAR-0046 雨衣**，橡胶化丝绸，verified，SRC-0406（V&A，约1920英国，[O361727](https://collections.vam.ac.uk/item/O361727/)）——真正防水、利于夜行。
2. 鞋 **GAR-0035** 女式皮鞋（SRC-0206 系晚宴鞋）→ **GAR-0022 威灵顿靴**，verified，SRC-0123（FIT，[链接](https://fashionhistory.fitnyc.edu/wellington-boot/)）——橡胶涉水、防滑。

**状态链（continuity）**：旗袍肩背被雨衣覆盖处干、前襟与下摆渐湿；鞋面水亮→后巷可积泥点，供后续场次承接。

**冲突/缺口（不夸大）**：GAR-0046 为 1920 英国、GAR-0022 无时代/地域标注，二者仅 era/generic 级，非上海本地实证；靴型偏男装感，建议选及踝低筒、配旗袍色以减突兀。记者职业仍无专属卡。

（约 390 字）
