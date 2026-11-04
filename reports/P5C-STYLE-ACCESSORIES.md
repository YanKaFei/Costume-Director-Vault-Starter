# P5-C 完整 Outfit 与风格知识扩建（试点 12 套 + 5 风格卡）

- 日期：2026-11-05（Asia/Shanghai）；执行：narrator（P5-C）
- 写入范围：`05-风格体系/`、`09-造型组合/`、本报告；未改 00–04、07、scripts；未改既有卡片正文/事实。
- 基线：本任务新增 **12 LOOK + 5 STY = 17 卡**；当前工作区 **440 卡**（含并行新增；本任务未改既有卡）。`validate.py` PASS 440/440、0 错误；`validate_outfits.py --all` 中本批 **12/12 pass**（旧 LOOK 为 legacy_warn，不是 fail）。
- 证据原则：所有 LOOK 的 `look_items` 为真实 GAR/STR/MAT ID；组合/舞台/人物设定为 `creative_inference` 时明确标注；11 世纪苏格兰无直接证据处不声称历史复原。
- **未做导演评分**；本报告只记录创作设计/硬约束/证据类型。

## 0. 交付与计数

| 项 | 数量 | 说明 |
|---|---:|---|
| 完整 Outfit 卡 | **12** | LOOK-0024..LOOK-0035；全部 `type=look`、`category=character_look`、`review_status=draft` |
| 风格卡 | **5** | STY-0011..STY-0015；`evidence_status=interpretive`，关系为 `style_interpretation`（设计解释，不是史实） |
| 覆盖主题 | 6 类 | Macbeth 3 阶段、Lady Macbeth 3 阶段、1930s 上海雨夜（女/男记者各 1）、当代职业（夜班护士）、跨文化婚礼（加纳-英国）、科幻/艺术剧场（零重力歌剧、表现主义 Lady Macbeth） |
| 真实 item ID | **33 个唯一** | 30 GAR + 0 STR + 3 MAT（GAR/STR/MAT 全部可解析） |
| 真实 SRC | **39 个唯一** | 来自 item/style 卡 source_ids；无编造 SRC |
| 硬约束 | **12/12 PASS** | 用 `scripts/validate_outfits.py`（内部调用 R1.1 `outfit.validate_hard_constraints`）验证；0 violations；旧的 23 LOOK 为 legacy_warn |

## 1. 12 套 Outfit 清单与证据分布

| LOOK | 主题/阶段 | evidence_type | 核心槽位（真实 ID） | hard status |
|---|---|---|---|---|
| LOOK-0024 | Macbeth 野心上升（荒原） | sourced_style_observation | one_piece=GAR-0075；outer=GAR-0076；footwear=GAR-0081；accessory=GAR-0080；carried=GAR-0082；MAT-0011 | **PASS** |
| LOOK-0025 | Macbeth 罪恶危机（借来的王袍） | sourced_style_observation | one_piece=GAR-0009；outer=GAR-0076；footwear=GAR-0081；accessory=GAR-0080；carried=GAR-0082；MAT-0011 | **PASS** |
| LOOK-0026 | Macbeth 覆灭（剥落王权） | creative_inference | one_piece=GAR-0061；outer=GAR-0076；footwear=GAR-0081；accessory=GAR-0080；carried=GAR-0082 | **PASS** |
| LOOK-0027 | Lady Macbeth 野心上升（读信） | sourced_style_observation | inner=GAR-0078；one_piece=GAR-0079；outer=GAR-0076；footwear=GAR-0024；accessory=GAR-0080；carried=GAR-0082；MAT-0011 | **PASS** |
| LOOK-0028 | Lady Macbeth 罪恶危机（血手） | creative_inference | one_piece=GAR-0079；outer=GAR-0076；footwear=GAR-0024；accessory=GAR-0080；carried=GAR-0082；headwear=GAR-0068（theatrical）；MAT-0011 | **PASS** |
| LOOK-0029 | Lady Macbeth 覆灭（梦游） | creative_inference | inner=GAR-0078；one_piece=GAR-0079；outer=GAR-0076；footwear=GAR-0024；accessory=GAR-0080；carried=GAR-0082（象征） | **PASS** |
| LOOK-0030 | 1930s 上海雨夜·女记者 | historical_evidence | one_piece=GAR-0031；outer=GAR-0046；footwear=GAR-0022；accessory=GAR-0086；carried=GAR-0047；MAT-0002 | **PASS** |
| LOOK-0031 | 当代夜班护士·雨夜交班 | sourced_style_observation | one_piece=GAR-0036；outer=GAR-0046；footwear=GAR-0044；accessory=GAR-0050；carried=GAR-0048 | **PASS** |
| LOOK-0032 | 加纳-英国婚礼·新娘并置 | sourced_style_observation | one_piece=GAR-0005；headwear=GAR-0070；footwear=GAR-0035；accessory=GAR-0086；carried=GAR-0048；MAT-0005/MAT-0006 | **PASS** |
| LOOK-0033 | 零重力歌剧女伶 | creative_inference | one_piece=GAR-0038；outer=GAR-0037；footwear=GAR-0022；headwear=GAR-0039；accessory=GAR-0050；carried=GAR-0048 | **PASS** |
| LOOK-0034 | 表现主义·Lady Macbeth 终局 | creative_inference | one_piece=GAR-0009；outer=GAR-0076；footwear=GAR-0024；accessory=GAR-0080；carried=GAR-0082；MAT-0011 | **PASS** |
| LOOK-0035 | 1930s 上海雨夜·男记者 | historical_evidence | one_piece=GAR-0032；outer=GAR-0046；footwear=GAR-0060；accessory=GAR-0083；carried=GAR-0047；MAT-0002 | **PASS** |

### 证据分布（evidence_type）

| evidence_type | 数量 | LOOK |
|---|---:|---|
| `historical_evidence` | **2** | LOOK-0030、LOOK-0035（1930s 上海雨夜） |
| `sourced_style_observation` | **5** | LOOK-0024、0025、0027、0031、0032 |
| `creative_inference` | **5** | LOOK-0026、0028、0029、0033、0034 |

> 分布偏向“有来源的历史/风格观察”而非纯创作；所有 LOOK 的 `evidence_status` 仍为 `interpretive`（组合/人物/舞台是设计），不把组合误标 verified。无直接证据的 11 世纪与虚构科幻明确标 creative_inference。

## 2. R1.1 完整 Look 硬约束验证（12/12 PASS）

### 2.1 方法

- 先按 Outfit v1.4 槽位写 `outfit_slots`：`one_piece`（含 `specialised` 传统长袍按 one_piece 语义）/`inner_layer`/`outerwear`/`footwear`/`accessory`（含 headwear）/`carried_prop`；同时保留 `look_items`。
- 用 **`python3 scripts/validate_outfits.py --vault . --look <ID>`**（Outfit 模型 v1.4，内部调用 R1.1 `outfit.validate_hard_constraints`）逐套验证；`historical_evidence` 用 historical 模式 + 卡级 tiers，`sourced_style_observation`/`creative_inference` 用 inspired/fictional。另用同一 `validate_hard_constraints` 做一次手工 synthetic 复核（槽位/雨/动作）。
- 记录每套 `violations` 数量；0 即 PASS；状态写入卡内 `hard_constraint_status` 字段（可追溯）。
- 检查项包括：torso/footwear 是否齐、duplicate item、outer/rainwear（rain/cold）、action 鞋履安全（battle/dance）、strict occupation anchor（护士）、approved anchors、example/unknown ID、historical 分支 period/region tiers。

### 2.2 结果

| LOOK | status | violations |
|---|---|---:|
| LOOK-0024..LOOK-0035（12 套） | **全部 PASS** | **0** |

- 雨景（LOOK-0030/0031/0035）使用 `GAR-0046 雨衣` 作为 rainwear outer；鞋为 GAR-0022/GAR-0044/GAR-0060（非高跟/非开口）。
- 护士（LOOK-0031）用 `GAR-0036` 作为职业 anchor，满足 `OCCUPATIONAL_STRICT` 的 nurse 要求。
- 战斗（LOOK-0024/0026）鞋为 GAR-0081 皮靴，非高跟/开口；冷/风暴场景均有 outer。
- 婚礼、科幻、艺术剧场为室内，无 rain/cold 强制；torso/footwear 齐。

### 2.3 边界（诚实声明）

- `historical_evidence`（LOOK-0030/0035）走 historical 模式，tiers 由已 verified 卡推导；仍不把 1930s 上海组合当“逐件史实”。
- Macbeth/Lady 的类比造型使用 `sourced_style_observation`/`creative_inference`（inspired/fictional），**不声称 11 世纪苏格兰历史复原**；若硬按 historical 模式会触发 `historical_period_unverified`，因此不写“历史准确”。
- `hard_constraint_status` 只代表 R1.1 的规则层通过，不等于导演/史实审查通过；导演评分入口仍是 P3.6 空白评分表。

## 3. 5 张风格卡（设计解释关系）

| STY | 名称 | category | source_ids | style_interpretation 关系 |
|---|---|---|---|---|
| STY-0011 | 北方中世纪戏剧性极简 | cinematic_style | SRC-0110/0421/0480/0482/0487/0489 | LOOK-0024/0025/0026/0027/0028/0029（6 条） |
| STY-0012 | 1930s 上海雨夜黑色电影 | cinematic_style | SRC-0200/0201/0405/0407/0408 | LOOK-0030/0035（2 条） |
| STY-0013 | 当代职业制服现实主义 | occupational | SRC-0400/0410 | LOOK-0031（1 条） |
| STY-0014 | 跨文化婚礼并置 | cinematic_style | SRC-0106/0430/0431/0144/0145 | LOOK-0032（1 条） |
| STY-0015 | 零重力歌剧科幻剧场 | fictional_world | SRC-0402/0403/0401 | LOOK-0033/0034（2 条） |

- 关系 type 为 `style_interpretation`、evidence=`interpretive`、confidence=`medium`、rule=`R-CURATED-DESIGN`；这是**设计解释关系**，不是 P5-A 的 `in_style` 事实关系，也不是史实归属。
- 每张风格卡正文明确“设计解释，不是历史事实”；不能把风格标签当来源或年代证据。
- 5 张卡覆盖：学院/极简/表现主义（STY-0011/0015）、黑色电影（STY-0012）、职业（STY-0013）、跨文化并置（STY-0014）。

## 4. 覆盖与缺口

**已覆盖（12 套）**：
- Macbeth 三阶段（LOOK-0024/25/26）+ Lady Macbeth 三阶段（LOOK-0027/28/29）；
- 1930s 上海雨夜（LOOK-0030 女记者、LOOK-0035 男记者）；
- 当代职业（LOOK-0031 夜班护士）；
- 跨文化婚礼（LOOK-0032 加纳-英国新娘并置）；
- 科幻/艺术剧场（LOOK-0033 零重力歌剧、LOOK-0034 表现主义 Lady Macbeth）。

**缺口（卡内已写 `evidence_limits`）**：
1. 11 世纪苏格兰无直接服饰证据；Macbeth/Lady 使用欧洲/地中海/拜占庭**类比卡**，不得称历史复原。
2. GAR-0079 基尔特长袍为 **interpretive**（无 SRC）；Lady 造型中作为躯干层，不当史实。
3. GAR-0068 为 **1902 婚礼头纱**，仅 LOOK-0028 theatrical 使用；不是中世纪头纱。
4. GAR-0039 为 **1969 儿童玩具头盔**，LOOK-0033 仅作道具结构参考；无真实 EVA/供氧/通讯卡。
5. Macbeth/Lady/艺术剧场没有对应 **SCN 场景卡**（`look_scene: []`）；场景在 `11-验收/P3.5/Macbeth/SCENE-TABLE.md`，不在本库卡片层。需要时再补 SCN。
6. 护士 LOOK 用 1960s V&A 护士装 + interpretive 医疗鞋；无现代 scrub/PPE/口罩；不得声称某医院真实制服。
7. 婚礼为文化并置创作；gele 为西非/约鲁巴头饰，不是阿散蒂专属；需文化顾问确认，不把并列当混搭许可。
8. 科幻为虚构；现实工作服/防护服卡只作结构类比。
9. Lady 的匕首（GAR-0082）在 L1/L2/L3 为**象征性/创作道具**，不是梦游史实；必须未开刃。
10. 5 张风格卡均为 interpretive 设计解释；不提供史实来源断言。

## 5. 复现/验证

```bash
python3 scripts/validate.py                         # PASS 440/440（当前树）
python3 scripts/validate_outfits.py --vault . --all  # 本批 12/12 pass；旧 LOOK legacy_warn
# validate_outfits 按 evidence_type 选择 historical/inspired/fictional，并调用 outfit.validate_hard_constraints
# 说明：Macbeth/Lady 的类比造型以 sourced/creative 验证，不声称 strict historical
```

- 12/12 `hard_constraint_status` 均写入卡内（`PASS (R1.1 outfit.validate_hard_constraints; validate_outfits 12/12; 0 violations; 2026-11-05)`）。
- `validate.py` 的 8 节、wikilink、source_ids、ID/枚举全部 PASS；新增 17 卡不改变既有卡片。

## 6. 结论

- P5-C 试点完成 **12 套完整 Outfit + 5 张风格卡**；12/12 通过 R1.1 硬约束（`validate_outfits`，0 violations；historical 分支用 historical tiers，sourced/creative 用 inspired/fictional），evidence 分布 2 historical / 5 sourced / 5 creative；所有创作/类比/虚构处已标 `evidence_type` 与缺口。
- 关系层只新增 **12 条 `style_interpretation` 设计解释关系**，不新增史实断言；风格卡不与 `in_style` 事实关系混用。
- 后续（P5-D/扩建）：补 Macbeth SCN 场景卡、现代护士 PPE/scrub 卡、非西方婚礼配件（串珠/扇/凉鞋）、真实舱外/太空结构卡；在此之前不把现有类比当史实。
