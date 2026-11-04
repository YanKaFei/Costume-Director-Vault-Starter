真实调用已完成（exit 0）：`python3 scripts/outfit.py --input projects/lady-macbeth-act1-abc/input.json --json`，并用 `query.py --id` 逐一核验全部卡/SRC。产物：`projects/lady-macbeth-act1-abc/outfit.{json,md}`。

## Brief
麦克白夫人，11世纪苏格兰因弗内斯城堡，第一幕5–7场（读信/接驾/怂恿），夜间室内、干冷石堡；历史考据模式、中等预算。未知：季节、室外天气。

## A/B/C 完整搭配（槽位全覆盖：连身/外层/鞋/配饰/携带物）
固定锚点（三场不变）：**GAR-0076** 斗篷（verified; SRC-0482/0483）、**GAR-0081** 皮靴（SRC-0489）、**GAR-0080** 腰带（SRC-0487/0488）、**GAR-0082** 匕首（SRC-0490/0491）。

- **A 考证款**：连身 **GAR-0075** T形束腰长袍（natural wool/indigo，羊毛亚麻；verified, SRC-0480/0481）+上述锚点。叙事：克制、北地硬度，靛蓝压猩红。
- **B 女性合体款**：连身换 **GAR-0079** 基尔特长袍（侧系带、长袖；**interpretive，无 SRC，不可作考证证据**）+同锚点。
- **C 美术变体**：脚本警告库内无更廉价组合，C 与 A 同 ID（a_c item_diff=0），按等价成本的色彩/披法变体使用；须如实标注此局限。

## English prompts（脚本生成，已锁 ID/色/材质）
- Image：“full-body character design … early medieval tunic GAR-0075 … half-circle crimson satin mantle GAR-0076 … leather ankle boots GAR-0081 … iron/silver-gilt belt GAR-0080 … dagger GAR-0082 … candle and hearth warm key, cold moonlight, matte wool/linen”；Negative：“no costume morphing, no extra layers, no colour shift, no invented accessories, no tartan”。
- Video：同锁定 + 动作 read letter/pace/greet/urge Macbeth，medium close-up，跨镜保持 IDs/colors/materials 恒定。

## 连续性（输入显式状态，脚本未臆造）
1.5/1.6/1.7 均 wetness=dry, damage=none, dirt=none；锚点 GAR-0076/0080/0081/0082 贯穿。血污要到后幕才允许出现。

## 11世纪苏格兰证据缺口（query.py 实证）
1. `06-时代地域/` 无苏格兰语境卡（最近仅 PRD-0010 拜占庭）；脚本警告 `context_gap`、无 11th/Scotland 命中。
2. 全部衣物均为他地他时代 analogue：SRC-0480/0481 是**埃及450–650年童袍**、SRC-0482/0483 为1580–1610 法/葡斗篷、SRC-0487 为7世纪墨洛温扣、SRC-0488 为16世纪挪威扣、SRC-0489 为15世纪伦敦靴、SRC-0490/0491 为14–15世纪意/佛兰德斯匕首；脚本逐条标记 `region_mismatch`、年代仅世纪级。
3. 无中世纪女性头饰/盖头卡（GAR-0070 头巾非此语境）；B 款 GAR-0079 无来源；A=C 区分度不足（checks.abc_pairwise_ge_2=false）。结论：这是**有据类比设计，不是11世纪苏格兰实物复原**。
