已通过 skill 脚本完成：`python3 scripts/workflow.py`（exit 0，checks 全过），产出在 `projects/nurse-rain-shift/outputs/`。

## Brief
当代/全球/职业写实/fictional/中预算；季节、文化、具体城市、灯光**unknown**。角色 Lin：急诊护士、工薪、撑过雨夜班。

## 场景表（真实 ID，脚本输出）
| 场景 | A | B | C | 状态 |
|---|---|---|---|---|
| S1 雨夜街道 | 0079+0045+0044 | 0036+0041+0044+0050+0048 | 0036+0045+0044 | 全湿/无/净 |
| S2 急诊夜班 | 0079+0045+0044+0080 | 0079+0076+0044 | 0079+0045+0044+0048 | 发湿汗潮/**血点**/轻污 |
| S3 下班黎明 | 0036+0041+0044+0050+0048 | 0079+0044 | 0079+0022 | 外套潮+干水渍/血点仍在/褶皱疲惫 |

## 推荐连续链（设计锁定，非脚本交叉项）
锚点 **GAR-0036 护士制服**(verified, SRC-0400)+**GAR-0044 医疗工作鞋**(interpretive, 无SRC)+**GAR-0045 风衣**(verified, SRC-0405)。S1=C（制服外压风衣、手袋 GAR-0048 顶头）；S2 脱风衣，可加 **GAR-0050 徽章**(SRC-0410) 替代胸牌；S3=A（套件仍潮的 **GAR-0041 白袍** interpretive，携 GAR-0048）。**弃用 GAR-0079 中世纪基尔特/GAR-0076 斗篷/GAR-0080 古腰带/GAR-0022 威灵顿靴**：KB 无当代刷手服，引擎回退年代卡（GAR-0022 有 SRC-0123），与当代设定冲突，仅作时代级假设。

## 连续性状态链
湿：soaked(S1)→damp hair/sweat(S2，风衣脱在储物柜)→damp coat+dried tide marks cuffs/hem(S3)；损：none→**血点出现于上衣左胸**→血点保留；污：none→轻污/消毒水痕→褶皱。锚点 GAR-0036/0044 三场均在，不得瞬干/换装（脚本机检 anchor 仅 GAR-0044，因逐场独立检索，已在此人工补强）。

## English prompts
- **S1 img**: contemporary ER nurse Lin running in heavy rain at night, 1960s-cut nurse uniform `GAR-0036` white-blue polyester under belted khaki gabardine trench `GAR-0045`, white non-slip medical shoes `GAR-0044`, canvas handbag held over head `GAR-0048`; wetness=soaked, damage=none, street reflections, medium shot.
- **S2 img**: same Lin in cold fluorescent ER, trench removed, `GAR-0036` with cloth badge `GAR-0050`, hair tied; wetness=damp hair+sweat, damage=fresh blood spots left chest, antiseptic damp; handheld medium close-up.
- **S3 img**: Lin exits at dawn, `GAR-0036` under creased white coat `GAR-0041` and still-damp `GAR-0045`, `GAR-0044`, `GAR-0048`, hair looser; blood spots retained, dried rain tide marks on cuffs/hem.
- **video（三场通用）**：lock `GAR-0036|GAR-0045|GAR-0044` colors/materials/positions; wetness changes only on S1→S2→S3 transitions; no instant drying, no costume morph, no color/logo/text.

## 证据/unknown
SRC：[0400](https://collections.vam.ac.uk/item/O1224877/)、[0405](https://collections.vam.ac.uk/item/O1295635/)、[0408](https://collections.vam.ac.uk/item/O367714/)、[0410](https://collections.vam.ac.uk/item/O1114148/)、[0123](https://fashionhistory.fitnyc.edu/wellington-boot/)。GAR-0044/0041 为 interpretive 无 SRC；血点/心理为导演推断。**Gap：KB 无当代刷手服与当代护士鞋 verified 卡**，需补库或按 fictional 自制。
