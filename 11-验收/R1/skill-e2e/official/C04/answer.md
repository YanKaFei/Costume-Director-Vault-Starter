## Brief
11 世纪苏格兰，historical / medium；年龄、季节与户外天气 **unknown**；“冷石厅堂”是制作假设，不是史料。人物是领主之妻，性格线为野心—操纵—“去性别化”。

## 五槽表（`outfit.py` completeness 5/5）
| 场 | Look | one_piece / outerwear / footwear / accessory / carried_prop | State |
|---|---|---|---|
| 1.5 读信 | A | GAR-0075 / GAR-0076 白 / GAR-0081 / GAR-0080 / GAR-0082 | dry/none/none |
| 1.6 迎邓肯 | B | GAR-0079 / GAR-0076 深红 / GAR-0081 / GAR-0080 / GAR-0082 | dry/none/none |
| 1.7 激将 | C | GAR-0075 / GAR-0076 深红 / GAR-0081 / GAR-0080 / GAR-0082 | dry/none/none |

**材质/色**：GAR-0075 natural_wool+indigo（wool/linen/cotton）；GAR-0079 wool/linen（interpretive）；GAR-0076 crimson/white（satin/silk/linen/metal_thread）；GAR-0080 iron/silver/gold；GAR-0081 brown/tan leather；GAR-0082 steel/ivory/silver。

**叙事**：A 用白披肩和束带，表现私室里的克制；B 用 kirtle 搭配深红缎，借男性化外袍作权力表演；C 换回 tunic、保留深红，同时腰带松、披风单肩、头发露出，进入“去性别化”的激将。KB 只有两件 one-piece，C 与 A 共用卡组、只换 GAR-0076 的色 variant，**不是第三套独立卡组**。

## English prompts
`IMAGE A`: Lady Macbeth, 1.5, Inverness chamber, candlelight; GAR-0075 natural wool/indigo tunic, GAR-0076 white linen mantle, GAR-0080 iron/silver belt, GAR-0081 brown leather boots, GAR-0082 dagger; matte wool, no tartan, medium close-up, dry clean.

`IMAGE B`: 1.6 hall; GAR-0079 muted wool kirtle, GAR-0076 crimson satin cloak with silver-gilt trim, GAR-0080 belt, GAR-0081 boots, GAR-0082 dagger; hearth key, public formality, controlled.

`IMAGE C`: 1.7; GAR-0075 tunic, GAR-0076 crimson cloak off one shoulder, GAR-0080 belt loosened, GAR-0081 boots, GAR-0082 dagger; indigo/crimson, close two-shot, hair uncovered.

`VIDEO`: GAR-0075/0079, GAR-0076, GAR-0080, GAR-0081, GAR-0082; same colors/materials; 24fps slow push-in; A letter, B greeting, C goading lean; dry, no damage/blood; no morphing, no extra jewelry, no tartan, no modern soles.

## 连续性
锚点为 **GAR-0076 / 0080 / 0081 / 0082**。A→B：tunic→kirtle，白→深红；B→C：kirtle→tunic，保留深红，腰带松、披风单肩、头发露出。三场均 **dry/none/none**，第一幕无血污。

## 11 世纪苏格兰证据缺口
已实际运行命令：`python3 scripts/outfit.py --input projects/lady-macbeth-act1-outfit/input.json --json --out projects/lady-macbeth-act1-outfit/outfit.json`，退出 0；五槽全 true，但 `abc_metrics.all_pairwise_ge_2=false`。`python3 scripts/query.py --id ...` 取 15 张卡并存入 `query-evidence.json`；`--type period_region --region scotland` 和 `"scotland" --type garment` 均返回 `[]`：**库内没有 11 世纪苏格兰卡**。

可用实物全是近似：SRC-0480/0481 埃及 450–650；SRC-0482 法国 1580–1600；SRC-0483 葡萄牙 1590–1610；SRC-0487 7 世纪；SRC-0488 挪威 1500–1600；SRC-0489 伦敦 15 世纪；SRC-0490 意大利 1360–1400；SRC-0491 佛兰德斯 1475–1500。GAR-0079 无 SRC、为 interpretive；GAR-0075 卡面自述“不是 11 世纪苏格兰实物”。因此只能标 **historical analogue**，不能称复原；深红缎斗篷原为男装、GAR-0082 原为男性腰带匕首，用于女性角色属导演性跨用。信纸/钥匙无卡，carried_prop 只能以 GAR-0082 代用。

来源：[SRC-0480](https://collections.vam.ac.uk/item/O119606/)、[SRC-0483](https://collections.vam.ac.uk/item/O356064/)、[SRC-0489](https://collections.vam.ac.uk/item/O107847/)、[SRC-0490](https://collections.vam.ac.uk/item/O165105/)。
