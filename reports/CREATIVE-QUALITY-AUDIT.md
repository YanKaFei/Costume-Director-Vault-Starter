# R1 审计五：影视创作质量、连续性与 Costume Look Bible 可行性

- 日期：2026-11-04（Asia/Shanghai）；审计者：narrator（独立于 P4 worker 自评）
- 性质：**只读审计**。仅写本文件；未修改卡片、脚本、验收材料；未代填任何导演评分。
- 范围：
  - P3.5《麦克白》18 套人工策展造型：`11-验收/P3.5/Macbeth/LOOKS.md`、`EVIDENCE.md`、`CASE.md`、`SCENE-TABLE.md`、`HUMAN-SCORE.md`
  - P4 11 例：`11-验收/P4-MACBETH/SUMMARY.md`、`inputs/`、`outputs/`、`validation.json`
  - P4 Composer 9 例：`11-验收/P4-COMPOSER/SUMMARY.md`、`runs/`；schema 见 `docs/OUTFIT-COMPOSER.md`
  - 历史/当代/科幻案例：P2.5 的 C01–C10（`11-验收/P2.5-案例/SUMMARY.md`）；P4 Composer 的 ghana/rain/nurse/dance/conflict 例
  - 上下文报告：`reports/P4-REPORT.md`、`P4-COVERAGE.md`、`P4-REGRESSION.md`、`P2.5-AUDIT.md`、`P3.5-REPORT.md`、`P3.6-REPORT.md`
- 方法：逐文件核对 + 在 `/tmp` 重跑 composer 输入做稳定性/单件修改实验（未写回仓库）+ 对 LOOKS 槽位做类别映射统计 + 对 P4 输出做槽位/差异/anchor/prompt/warning 抽检。
- 判定说明：本文的 PASS / WARN / FAIL 是**审计判断**，不是导演评分，也不是 1–5 分；导演评分仍以 `11-验收/P3.6/导演评分表.md`（NOT_SCORED）为准。

## 0. 执行摘要

1. **P3.5 的 18 套人工策展在“叙事与证据诚实”上明显强于自动 composer**：三阶段有明确人物/心理/世界设定，证据三分与缺口逐套标注；但**槽位完整性有 2 套硬缺口**（M2-B 无鞋、L3-A 无躯干层），且 M1-A 在风暴荒野无外层。
2. **P4 Composer 的“完整搭配”是机械完整**：14 个 P4-MACBETH 输出中 12 个 5 槽全满，但常见跨时代/角色错配（Macbeth 穿 GAR-0079 基尔特长袍 + GAR-0045 风衣 + GAR-0048 1930s 手袋；Lady 罪疚段拿 GAR-0028 18 世纪手笼；Macbeth 覆灭段穿 GAR-0033 20 世纪西装）。`checks` 仍全绿。
3. **A/B/C “有差异”指标失真**：`item_diff` 统计的是两个 look 的 ID 对称差集大小；**只换 1 件 = 2 分，刚好通过 ≥2**。`ensure_abc_difference()` 的注释明确写“swap one shared slot … yields exactly two symmetric differences”。因此“A/B/C 有意义差异”不能由该指标证明。
4. **身份/心理变化没有被数据模型表达**：三阶段靠换主件，但 anchor 集随可用卡漂移（Macbeth rise anchors `GAR-0045/GAR-0048/GAR-0080` → guilt `GAR-0045/GAR-0080/GAR-0082` → downfall `GAR-0080/GAR-0082`），没有“已批准 anchor”概念。
5. **单件修改行为**：只改 lighting/camera/state/budget 时输出 ID 完全不变（好）；只改 weather 会重写外层/鞋（合理但无锁定规则）；composer **没有 item 级覆盖/锁定接口**，无法表达“只改一条腰带、其余冻结”。
6. **prompt 可执行但语义会自相矛盾**：P4 生图 prompt 直接把卡片文案拼起来，出现 “medieval kirtle … trench coat … 1930s embroidered canvas handbag” 同框；prompt 可被机器执行，但不能被导演当作可信造型方案。
7. **证据缺口诚实度：总体较好，局部不足**。composer 对 11th-c Scotland 会降级为 1 套 + 14 条 warnings，不硬凑 A/B/C（诚实）；但“完整 5 槽”的 look 仍会静默使用跨时代卡，只在 warnings 里泛泛提示；P2.5 C08 仍有假阴性（1580s vs 16th_century 全部拒绝）。
8. **Look Bible 可行**：现有平铺 YAML + 可选字段 + validate 的架构足以承载“造型版本 + 已批准 anchor + item 锁 + 状态矩阵 + 导演签核”；但当前**没有**版本、审批、diff、单件变更、锁定字段。建议作为独立 P5 数据模型实现，不在本次实现。

---

## 1. 评估维度与判定

| # | 维度 | 判定 | 一句话理由 |
|---|---|---|---|
| 1 | 完整组合合理性（槽位/配饰/鞋） | **WARN** | 机械槽位覆盖高，但“完整”不等于“可穿/可信”；P3.5 有 2 套硬缺口 |
| 2 | A/B/C 有意义差异 | **FAIL** | 指标把“换 1 件”计为 2 差异并通过；结构与叙事差异未被强制 |
| 3 | 身份/心理三阶段 | **WARN** | P3.5 人工策展成立；P4 自动三阶段漂移、跨时代错配 |
| 4 | 已批准 continuity anchors | **FAIL** | 无“approved anchor”概念；anchor 自动推导且逐阶段漂移 |
| 5 | 单件修改行为 | **WARN** | 光照/状态/预算稳定（好），无 item 锁/覆盖；weather 会级联重写 |
| 6 | 生图/视频 prompt 可执行性 | **WARN** | 英文长 prompt 可执行；拼接导致语义矛盾与年代混搭 |
| 7 | 动作/布光/场景适配 | **WARN** | domain_fit 只是记录，不是硬约束；动作场景仍可能选高跟/拖地/长层 |
| 8 | 证据不足主动声明 | **WARN** | 降级/拒绝诚实；但“完整 look 内的错配”只进 warnings，不阻断 |

---

## 2. 维度 1：完整组合合理性

### 2.1 P3.5 18 套（LOOKS.md）

按卡片 `category` 映射槽位（torso = upper_body 或 one_piece；footwear；outerwear；accessory/headwear；carried_prop）：

| 指标 | 结果 | 说明 |
|---|---|---|
| 有躯干层（upper/one-piece） | 17/18 | L3-A 只有 inner_layer + outerwear + footwear，缺 torso |
| 有鞋 | 17/18 | M2-B 缺 footwear（虽为室内宴会，仍属组合缺口） |
| 有外层 | 11/18 | 室内场景可接受；但 M1-A（风暴荒野）无 outerwear，天气不匹配 |
| 有配饰/头饰 | 17/18 | L3-A 无 |
| 有携带道具 | 7/18 | 多数手部为空；舞台上可接受，镜头连续戏剧本需补 |
| 躯干+鞋同时满足 | **16/18** | M2-B、L3-A 为硬缺口 |

具体证据：
- `LOOKS.md` §M2-B：`GAR-0075, GAR-0076, GAR-0077, GAR-0080, GAR-0082, MAT-0011` —— 无 footwear；
- `LOOKS.md` §L3-A：`GAR-0078`（chemise/inner_layer）+ `GAR-0076` + `GAR-0024` —— 无 torso/upper，`inner_layer` 不能替代外衣层；
- `LOOKS.md` §M1-A：风暴荒野场景（`SCENE-TABLE.md` 1.3）但无 outerwear，与天气/动作不符。

### 2.2 P4-MACBETH 11 例（outputs）

- 14 个输出中 **12 个** `completeness` 的 5 项全为 true（torso/footwear/outer/accessory/carried），但 `historical_gap`、`evidence_refusal` 各只有 1 个不完整 look（仅 `GAR-0077` lower_body），被 `validation.json` 记为 PASS（因为断言是“诚实降级”而不是“完整”）。
- 通过 `full_slots_accessories` 的设计目标时，槽位确实补齐；但补的件可能不匹配（见 §3/§4）。

### 2.3 P4-COMPOSER 9 例

- 6/9 `completeness` 全 true；`action_dance`、`cross_cultural_ghana` 缺 outer/carried；`conflict_reject` 只有 1 个不完整 look（诚实）。
- 结论：**槽位覆盖是可执行的 engineering 指标，但不能代表“完整可信造型”**；WARN。

---

## 3. 维度 2：A/B/C 是否有意义差异

### 3.1 指标实现（关键缺陷）

`scripts/outfit.py`：

- `difference_count(left, right)` = `len(ids(left) symmetric_difference ids(right))`；
- `checks.abc_pairwise_ge_2 = all(item_diff >= 2)`；
- `ensure_abc_difference()` 注释：*"If A/B/C collapse to <2 item differences, swap one shared slot for a real unused candidate. This changes one ID only, yielding exactly two symmetric differences."*

也就是说：**只换一件**（一个 ID 移除 + 一个 ID 加入）→ `item_diff = 2` → 判定“有差异”。指标能区分“完全相同”，但不能证明“结构/轮廓/叙事有实质不同”。

### 3.2 实证

`python3 scripts/outfit.py --input 11-验收/P4-MACBETH/inputs/macbeth_rise.json --json` 输出：

- A：`GAR-0079, GAR-0045, GAR-0081, GAR-0080, GAR-0048`
- B：`GAR-0009, GAR-0045, GAR-0081, GAR-0080, GAR-0048`
- A/B 实际只差一件（`GAR-0079` ↔ `GAR-0009`），但 `abc_metrics.a_b.item_diff = 2`，`all_pairwise_ge_2 = true`。

同类：
- Lady rise A `[GAR-0079, GAR-0076, GAR-0081, GAR-0080, GAR-0082]` vs B `[GAR-0079, GAR-0017, ...]` —— 只换外层；
- 多个 P4 输出的 A/B/C 差异集中在 1–2 件（palette/silhouette 有变化，但轮廓推断是启发式默认值，见 `docs/OUTFIT-COMPOSER.md` Limitations）。

### 3.3 结论

- **FAIL**：当前 `abc_metrics` 不能作为“有意义 A/B/C”的验收依据；它只证明“不完全相同”。
- 建议（Look Bible/后续）：A/B/C 差异至少要求“轮廓形态不同（A/H/X 至少 2 种）+ 主件年代/结构轴不同 + 叙事意图字段”，并区分 `swap_count` 与 `symmetric_diff`。

---

## 4. 维度 3：身份与心理变化（三阶段）

### 4.1 P3.5（人工策展）

- 18 套按 M1/M2/M3、L1/L2/L3 分组；每套有明确的叙事意义（如 M1“刚从战场回来，衣服的功能性优先”、M2“借来的王袍”、M3“剥掉王权只剩功能层”），阶段之间有色彩/层搭/道具的连续变化；
- 但**不是严格证明**：文本叙事是设计意图，不是镜头语义；`HUMAN-SCORE.md` 尚未有导演评分；C 套的 theatrical 选择（如 L2-C 1902 头纱）需要导演确认。
- 判定：**WARN（人工策展成立，待人工评分）**。

### 4.2 P4 自动三阶段（关键失败证据）

抽取 `11-验收/P4-MACBETH/outputs/macbeth_{rise,guilt,downfall}.json`：

| 阶段 | A look 单品 | anchors | 问题 |
|---|---|---|---|
| rise | GAR-0079 基尔特长袍（kirtle）、GAR-0045 风衣、GAR-0081 靴、GAR-0080 腰带、GAR-0048 1930s 手袋 | GAR-0045, GAR-0048, GAR-0080 | Macbeth 为男性领主，主件却是 kirtle；20 世纪风衣/手袋 |
| guilt | GAR-0009 dalmatic、GAR-0045 风衣、GAR-0081 靴、GAR-0080 腰带、GAR-0082 匕首 | GAR-0045, GAR-0080, GAR-0082 | 风衣仍在；罪疚段没有血/污状态输入 |
| downfall | GAR-0079 kirtle、GAR-0033 20 世纪休闲西装、GAR-0081 靴、GAR-0080 腰带、GAR-0082 匕首 | GAR-0080, GAR-0082 | 主外层变 20 世纪西装；arc 没有被编码 |

Lady Macbeth：

| 阶段 | A look 单品 | anchors | 问题 |
|---|---|---|---|
| rise | GAR-0079 kirtle、GAR-0076 斗篷、GAR-0081 靴、GAR-0080 腰带、GAR-0082 匕首 | GAR-0079, GAR-0080, GAR-0081, GAR-0082 | 匕首对 Lady 不合适（除非明确导演选择） |
| guilt | GAR-0009 dalmatic、GAR-0076 斗篷、GAR-0084 18 世纪高跟鞋、GAR-0028 18 世纪手笼、GAR-0082 匕首 | GAR-0028, GAR-0082 | “罪疚段”拿手笼，语义不成立；18 世纪物件进中世纪 |
| downfall | GAR-0009 dalmatic、GAR-0045 风衣、GAR-0081 靴、GAR-0068 1902 头纱、GAR-0048 手袋 | GAR-0045, GAR-0048, GAR-0081 | 梦游/死亡段出现 1902 头纱与 1930s 手袋 |

- 判定：**FAIL（自动）**。三阶段是“每次 recommend 的可用候选不同”，不是“人物心理变化驱动”；anchor 集随阶段漂移，无 approved anchor。
- P4 `pair_relationship` 输出：shared anchors `['GAR-0079','GAR-0080','GAR-0081']` —— 把 GAR-0079 基尔特长袍当作 Macbeth 与 Lady 的共同锚点，角色/性别适配性未被过滤。

---

## 5. 维度 4：已批准的 continuity anchors

现状：

- P3.5 `LOOKS.md` 有 `continuity_lock` 文本（血、泥、头发、披法、道具位置），但**没有“approved anchors”字段**、没有版本或导演签核；
- P4 Composer 的 `continuity.anchors` 是自动推导（`GAR-0045/GAR-0080/...`），随阶段/输入变化；没有“哪些 anchor 不可变、哪些可替换”的标注；
- P4-MACBETH `video_continuity` 输出的 anchors 为 `['GAR-0045','GAR-0080','GAR-0081']`，states 显式（`checks.continuity_states_explicit=true`），但 anchors 本身没有审批/锁定；
- P3.6 `导演评分表.md` 为 NOT_SCORED，不能当作批准。

判定：**FAIL**。建议的 Look Bible 必须有 `anchors[] = {slot, card_id, lock: hard/soft, approved_by, approved_at, note}`，且 composer 必须把 hard anchor 作为硬约束。

---

## 6. 维度 5：修改单件是否错误重写整个造型

### 6.1 实验（只读，输出在 /tmp）

| 输入变化 | 输出 A/B/C 单品 ID | 结论 |
|---|---|---|
| 基线 `macbeth_rise` | 见 §3.2 | — |
| 只改 `lighting` → "single candle" | 与基线完全相同 | **稳定（好）** |
| 只改 `camera` → "extreme close-up" | 与基线完全相同 | **稳定（好）** |
| 只改 `state`（S1 wet→dry） | 与基线完全相同 | **稳定（好）** |
| 只改 `budget` → low | 与基线完全相同 | **稳定（好）**，但也没体现预算降级（见 P2.5 C09） |
| 只改 `weather` → "indoor, dry" | A/B/C 的外层/鞋被整体替换（GAR-0081→GAR-0035 等） | 天气驱动可解释，但**没有“只换鞋/只换外层”的锁定/差异预览** |

### 6.2 判定

- **WARN**：光照/状态/预算稳定是优点；但 composer **没有 item 级覆盖、没有 lock/anchor 机制、没有 diff 预览**，用户无法表达“修改单件（如换一条腰带）而其余保持”。`ensure_abc_difference` 甚至会在 A/B/C 差异不足时**自动**换一件共享件——这会悄悄改变整套，而不是只改用户指定的单件。
- Look Bible 必须提供：单件 change request → diff 只显示该 slot + 受影响 prompt/continuity；未解锁 anchor 不允许变；版本 +1。

---

## 7. 维度 6：生图/视频 prompt 可执行性

### 7.1 优点

- P3.5 18 套每套有英文 image prompt + video prompt + negative prompt，包含角色、场景、镜头、服装结构、材质、光；文本完整；
- P4 Composer 也输出 `prompt_image/prompt_video/prompt_outfit/prompt_negative`，均为英文、含负向约束（no costume morphing / no extra layers / no logo…）；
- 无版权风险文本：prompt 为本库自写描述，不引用受版权保护剧本/译本。

### 7.2 失败证据

`outputs/macbeth_rise.json` A 的 image prompt（截取）：

> “one-piece: medieval kirtle … outer layer: trench coat, double-breasted, belted waist, storm flap … carried prop: 1930s embroidered canvas handbag …”

同一 prompt 内出现“medieval kirtle + 20 世纪 trench coat + 1930s handbag”，机器可生成一张图，但**语义自相矛盾**；`domain_fit` 同时显示 `outerwear: "none"`（无年代证据）却仍被拼进 prompt。负向 prompt 只有通用条目，无法纠正跨时代混搭。

判定：**WARN**。建议 prompt 生成前做“冲突消解”：若某 slot 的 evidence tier 为 none/era 且与主件年代差 > N，必须删除或替换，并在 prompt 里保留缺口声明。

---

## 8. 维度 7：动作/布光/场景适配

- P4 `domain_fit` 记录 weather/action/lighting/camera，但 composer 的硬约束主要覆盖天气/职业锚点/槽位；**action 与 lighting 不阻断**候选（`docs/OUTFIT-COMPOSER.md` 也说明 silhouette 是启发式）。
- 抽检 `movement_action.json`（battle/running/riding/climbing stairs）仍包含长层/靴/匕首等未做动作安全评估；`action_dance.json` A 套是 `GAR-0079` kirtle + `GAR-0022` 靴（contemporary dance 语境），warnings 自己承认“period evidence approximate/none”。
- P3.5 有动作/安全备注（GAR-0082 必须未开刃；M3-B 三层衣摆、L3-B 拖地裙摆、GAR-0024 穆勒鞋需走位测试），但只是文字风险，不是硬约束。
- P2.5 C08（1580s 宫廷舞者）显示库内其实有 16 世纪 doublet/jerkin/mule/美第奇领，却因 `1580s vs 16th_century` 全部拒绝并 exit 3 —— **假阴性**：动作/年代约束过严，未做合理近似。
- 判定：**WARN**。

---

## 9. 维度 8：证据不足是否主动声明

### 9.1 做得好的

- P4-MACBETH `historical_gap.json` / `evidence_refusal.json`：只有 1 套 `GAR-0077`（lower_body），`completeness` 全 false，`checks.three_looks=false`，14 条 warnings（no reliable period/region context card；cross-region borrowing flagged），**没有硬凑 A/B/C**；
- P4 Composer `conflict_reject`：1 套 + 15 warnings，明确冲突；
- P3.5 每套都有 historical=无直接证据 / evidence=类比 / theatrical=戏剧选择的拆分，并逐套列缺口；
- P4 新增来源卡与视觉索引均逐件核验 PD/URL；`P4-REPORT` 明确 public-ready=NO。

### 9.2 不足

- “完整 5 槽”的 look 内，跨时代/角色错配只出现在 `warnings`（如 “period evidence is approximate/none for GAR-0045…”），**不阻断、不降级、不标在具体 slot/prompt**；导演很容易忽略；
- P2.5 C08 假阴性（有 16 世纪卡却全部拒绝）；
- P2.5 C07 跨文化随机拼贴（kente/adinkra 卡未被使用，无文化语义警告）；
- P2.5 C05 连续性机械 PASS（同一套旗袍贯穿富太→难民），说明“证据/连续性脚本 PASS”不等于叙事正确；
- P2.5 C10 冲突未被识别（1930s 上海 + 赛博朋克），静默产出。

判定：**WARN**（主动声明有，但“完整 look 内错配”的阻断/标注不足）。

---

## 10. P4 11 例逐例审计

| 案例 | 槽位 | A/B/C | anchor/身份 | prompt/动作 | 证据 | 审计 |
|---|---|---|---|---|---|---|
| stage_changes_Macbeth | 3×5 满 | item_diff≥2 但多为 1 件换 | 跨时代（kirtle/trench/suit） | prompt 混搭 | warnings 有 | **WARN** |
| stage_changes_Lady_Macbeth | 3×5 满 | 同上 | 手笼/1902 头纱/匕首 | 语义错配 | warnings 有 | **WARN** |
| two_character_relationship | 3×5 满 | 共享 GAR-0079 作为两角色 anchor | 角色/性别适配失败 | — | 有 | **WARN** |
| full_slots_accessories | 满 5 槽 | 有差异 | 槽位补齐但件不匹配 | — | 有 | **WARN** |
| historical_evidence_gap | 1×1 不完整 | n/a | GAR-0077 仅 lower_body | 诚实降级 | 14 warnings | **PASS（诚实）** |
| minimal_vs_complex | 3×5 满 | 有差异 | 选件随 budget/art direction 变 | — | 有 | **WARN** |
| closeup_detail | 3×5 满 | 有差异 | 中世纪出现 GAR-0084 18 世纪高跟 | prompt 细节可执行 | 有 | **WARN** |
| movement_action | 3×5 满 | 有差异 | 动作安全未校验 | — | 有 | **WARN** |
| video_continuity | 3×5 满 | 有差异 | anchors 有但未批准 | states 显式 | 有 | **WARN** |
| bilingual_term_search | 工具级 | n/a | 中英命中一致 | n/a | 通过 | **PASS（工具级）** |
| evidence_insufficient_refusal | 1×1 不完整 | n/a | 拒绝硬凑 | 诚实输出 | 14 warnings | **PASS（诚实）** |

注：11/11 PASS 是 `validation.json` 的**脚本断言通过**，不等于 11 例的创作质量全部可接受；本表给出独立审计判定。

---

## 11. P3.5 18 套逐套审计

图例：槽位 = 躯干+鞋是否齐；AB C = A/B/C 差异是否叙事成立；锚 = continuity lock 是否具体；证据 = 三分/缺口；动作 = 动作/安全备注。判定是创作审计，不是导演评分。

| Look | 槽位 | A/B/C | 锚 | Prompt | 动作 | 证据 | 判定 |
|---|---|---|---|---|---|---|---|
| M1-A | 躯干+鞋（无外层；风暴荒野） | A 实用 vs B 领主 vs C 预言轮廓，成立 | 有血/泥/汗/斗篷 | 完整英/负向 | 有战场磨损 | historical=0/类比清楚 | **WARN（无外层）** |
| M1-B | 满 5 槽 | 成立 | 有 | 完整 | 有 | 清楚 | PASS（策展） |
| M1-C | 躯干+外层+鞋（无 lower，one-piece 覆盖） | 成立 | 有 | 完整 | 有 | 标 theatrical | PASS（策展） |
| M2-A | 躯干+鞋（室内可无外层） | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| M2-B | **缺鞋** | 成立 | 有 | 完整 | 有 | 清楚 | **WARN** |
| M2-C | 满槽 | 成立 | 有 | 完整 | 有 | 标 theatrical | PASS |
| M3-A | 躯干+鞋（战场可无外层） | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| M3-B | 满槽 | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| M3-C | 满槽 | 成立 | 有 | 完整 | 有 | theatrical | PASS |
| L1-A | 躯干+鞋（室内） | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| L1-B | 满槽 | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| L1-C | 躯干+鞋（室内） | 成立 | 有 | 完整 | 有 | theatrical | PASS |
| L2-A | 躯干+鞋（室内） | 成立 | 血手/头发 | 完整 | 有 | 清楚 | PASS |
| L2-B | 满槽 | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| L2-C | 躯干+鞋（室内） | 成立 | 有 | 完整 | 有 | theatrical（1902 头纱） | **WARN（需导演确认）** |
| L3-A | **无躯干层（仅 chemise+mantle+mule）** | 成立（梦游） | 散发/烛光 | 完整 | 有 | 清楚 | **WARN** |
| L3-B | 满槽 | 成立 | 有 | 完整 | 有 | 清楚 | PASS |
| L3-C | 满槽 | 成立 | 有 | 完整 | 有 | theatrical | PASS |

合计：槽位硬缺口 2/18（M2-B、L3-A）；天气/动作不匹配 1/18（M1-A）；theatrical 需导演确认 2 套（L2-C、L3-C）。

---

## 12. 历史/当代/科幻案例（P2.5 与 P4 交叉）

| 案例 | 类型 | 主要失败/通过点 | 对 Look Bible 的启示 |
|---|---|---|---|
| C01 历史（明末清初江南文人） | 历史 | WARN（证据不足声明正确；但引用 1770s 英法/1930s 上海/维多利亚丧服语境，误导） | 需版本化证据快照 + 地域/年代归一化 |
| C02 当代（急诊护士） | 当代 | FAIL（北极兽皮派克+牛仔裤+example 白衬衫当护士服；无 PPE/工牌） | 职业 uniform anchor 必须硬约束 |
| C03 科幻（零重力歌剧女伶） | 科幻 | FAIL（白衬衫+牛仔裤+雨靴 / 19 世纪内衣+波克帽；仅声明 fictional） | 需 fictional 模式 + 明确非历史声明 + 科幻卡 |
| C04 表现主义 1920s | 历史/艺术 | FAIL（16 世纪袋 + 18 世纪马甲/三角帽 + 19 世纪大衣混搭） | Look Bible 必须锁年代轴 |
| C05 身份下滑 + 连续性 | 历史/当代 | FAIL（同一旗袍贯穿富太→难民；连续性机械 PASS） | 状态矩阵/版本必须绑定叙事阶段 |
| C06 当代夜班信使 | 当代 | WARN（连续性正确；A 主体 example、缺头盔/箱包） | item 证据级别要进 Look Bible |
| C07 跨文化加纳婚礼 | 文化 | FAIL（白衬衫+牛仔裤+雨靴；kente/adinkra 未用；无文化警告） | 文化 anchor + 语义 guard |
| C08 1580s 舞蹈 | 历史/动作 | FAIL（1580s vs 16th_century 假阴性，exit 3） | 年代归一化 + 动作安全 |
| C09 低预算科幻 | 科幻/预算 | WARN（成本差 1.2%，非可执行预算替代） | budget 轴应影响版本变体 |
| C10 冲突约束（1930s+赛博） | 冲突 | FAIL（未识别，静默 historical 输出） | 冲突检测必须在版本层 |

P4 例补充：`conflict_reject` 已能诚实降级（PASS 诚实）；`action_dance` 的 contemporary 语境仍用 medieval kirtle（WARN）；`cross_cultural_ghana` B/C 出现 agbada/boubou 混搭但 warnings 未标文化边界（WARN）。

---

## 13. 问题登记（Problems）

> 严重度：P0 阻断创作可信/导致错误验收；P1 高影响；P2 中影响。状态：OPEN（本次不修，只审计）。

| ID | 严重度 | 维度 | 证据 | 复现 | 修复建议 | 验收标准 | 状态 |
|---|---|---|---|---|---|---|---|
| AUD-001 | **P0** | A/B/C | `difference_count` 为对称差；`macbeth_rise` A/B 仅差 `GAR-0079↔GAR-0009`，`item_diff=2`，`all_pairwise_ge_2=true` | `python3 scripts/outfit.py --input 11-验收/P4-MACBETH/inputs/macbeth_rise.json --json`，比对 A/B 单品与 `abc_metrics.a_b` | 分离 `swap_count` 与 `symmetric_diff`；要求至少 2 个不同 slot 的主件变化 + 轮廓/叙事轴 | 单换一件不得判 PASS；3 套轮廓形态 ≥2 种；人工抽检 5 例 0 误判 | OPEN |
| AUD-002 | **P0** | 完整组合/身份 | `macbeth_rise` A：kirtle+trench+1930s handbag；`lady_guilt` A：muff；`macbeth_downfall` A：20 世纪西装；`closeup` GAR-0084 18 世纪高跟 | 同 AUD-001 命令；另跑 `lady_guilt`、`macbeth_downfall`、`closeup_detail` 输入 | era/gender/role 硬约束；跨时代件需显式 override + 导演确认；prompt 冲突消解 | 主件/外层/鞋与主年代差 ≤1 世纪层级；0 角色性别错配；抽检 10 look 0 严重错配 | OPEN |
| AUD-003 | **P0** | anchors/版本 | 无 `approved_anchors`；P4 anchors 随阶段漂移（rise 0045/0048/0080 → guilt 0045/0080/0082 → downfall 0080/0082） | 对比 `outputs/macbeth_rise.json`、`macbeth_guilt.json`、`macbeth_downfall.json` 的 `continuity.anchors` | Look Bible 增加 `anchors[] {card, lock, approved_by/at}`；composer 消费 hard lock | 三阶段 hard anchors 一致；未批准 anchor 变更被拒 | OPEN |
| AUD-004 | P1 | 完整组合 | `LOOKS.md` M2-B 无 footwear；L3-A 无 torso；M1-A 风暴无 outer | 打开 `11-验收/P3.5/Macbeth/LOOKS.md` 对应小节，按 `category` 映射槽位 | 补鞋/躯干/外层，或在评分表标“有意省略 + 理由” | 18/18 躯干+鞋；天气场景 100% outer 或被批准豁免 | OPEN |
| AUD-005 | P1 | 验收口径 | `validation.json` 11/11 PASS；但 2 例仅 1 套、多例跨时代 | 读 `11-验收/P4-MACBETH/validation.json` 与 `outputs/` | 验收增加创作质量门（人工抽检 + 语义规则） | 每例含人工抽检记录；P0 问题 0 | OPEN |
| AUD-006 | P1 | 单件修改 | 改 lighting/camera/state/budget ID 不变；改 weather 级联；无 item override；`ensure_abc_difference` 自动换件 | 在 `/tmp` 复制 `inputs/macbeth_rise.json`，逐次只改一个字段后重跑 composer，比对 A/B/C ID | 支持锁 item/anchor + diff 预览；单件变更只允许该 slot 变 | 单件 change request 的 diff 仅 1 slot；未锁 anchor 不变 | OPEN |
| AUD-007 | P2 | prompt | `macbeth_rise` A prompt 同段 kirtle+trench+1930s bag；负向 prompt 通用 | 读 `outputs/macbeth_rise.json` 的 `looks[0].prompt_image/prompt_negative` | 结构化生成 prompt；冲突 slot 删除/替换；负向含年代/角色约束 | 抽检 10 prompt 无自相矛盾；负向覆盖关键约束 | OPEN |
| AUD-008 | P2 | 动作/布光 | `movement_action` 长层/靴未评估；`action_dance` 用 medieval kirtle；C08 假阴性 | 读 `outputs/movement_action.json`、`11-验收/P4-COMPOSER/runs/action_dance.json`、P2.5 SUMMARY C08 | action-safety 规则（鞋跟/裙摆/束缚）+ 年代归一化 | 动作场景 0 不安全鞋/拖地；C08 类案例回归通过 | OPEN |
| AUD-009 | P2 | 证据诚实 | composer 完整 look 仍用 era=none 件；P2.5 C08 假阴性；C07 文化随机 | 读 `macbeth_rise` warnings 与 items；读 `P2.5-案例/C07.md`、`C08.md` | 每 slot 标 evidence tier；era=none 件不得进主件/外层；文化 anchor 校验 | 完整 look 0 个 era=none 主件；C07/C08 回归通过 | OPEN |
| AUD-010 | P2 | 身份/心理 | 三阶段主件随候选漂移；无 psychology/beat 字段 | 对比 `macbeth_rise/guilt/downfall` 的 A 套主件与 anchors | Look Bible 增加 `stage_intent` + 允许的变体轴 | 每阶段有 intent 字段；A/B/C 轴受 intent 约束 | OPEN |
| AUD-011 | P2 | 审批 | P3.6 评分表 NOT_SCORED；P3.5 无 version/approval | 打开 `11-验收/P3.6/导演评分表.md`、`11-验收/P3.5/Macbeth/HUMAN-SCORE.md`；`grep version` LOOKS 无结果 | Look Bible 增加 signoff 区块（非分数） | 每套有 approved/revoked 记录；无代填分数 | OPEN |

## 14. Costume Look Bible / 版本管理 / 导演批准模型（可行性与建议，不实现）

### 14.1 可行性结论

**可行，且与现有架构兼容**：现有卡片为平铺 YAML，validator 允许额外扁平标量字段（`00-系统/数据字典.md`），LOOK 卡已有 `look_items/continuity_lock/prompt_en/negative_prompt_en` 等字段；缺的是**版本、审批、anchor 锁定、单件 diff、状态矩阵**。

### 14.2 建议数据模型（P5 候选，未实现）

**Look（版本化实体）**

| 字段 | 类型 | 说明 |
|---|---|---|
| `look_id` | string | 全局 ID（如 LOOK-BIBLE-0001），与现有 LOOK-xxxx 可映射 |
| `version` | string | `v1`, `v1.1`；每次审批/变更递增 |
| `status` | enum | `draft` / `review` / `approved` / `locked` / `retired` |
| `stage_intent` | string | 角色/心理/剧情 beat（如“野心上升—仍属战场”） |
| `scene_refs` | list | 场次 ID（SCN-xxxx） |
| `slots` | flat list | 每槽：`slot` / `card_id`（GAR/STR/MAT）/ `role`（主件/配饰/道具）/ `evidence_tier` |
| `alternates` | list | A/B/C 变体：`variant_id`, `axis`（era/silhouette/formality）, `overrides` |
| `anchors` | flat list | `{slot, card_id, lock: hard/soft, reason, approved_by, approved_at}` |
| `continuity_matrix` | list | 每场：wetness/drying、blood/dirt/damage、hair/makeup、道具位置 |
| `prompt_image/video/negative` | text | 版本化 prompt（与 look 同步） |
| `evidence_snapshot` | list | `source_ids`、`evidence_status`、`gaps`、核验日期 |
| `approval` | map | `decision`（approve/revise/reject）、`reviewer`、`role`、`date`、`signature_ref`、`notes`（**不写导演分数**；分数仍用 P3.6 表） |
| `change_log` | list | `version`, `change_type`(item/colour/state/prompt), `from`, `to`, `requested_by`, `approved_by`, `date`, `affected_slots` |

**版本规则（建议）**

1. **单件修改 = patch**：只改指定 slot，其余 slot 与 hard anchor 冻结；自动生成 diff（旧/新 ID、prompt 变化、continuity 影响），需 costume designer + director 签核后才升 `version`。
2. **hard anchor 不可静默变**：任何 anchor 变更需要 `change_type=anchor`，升级 minor 版本，并在 diff 中高亮。
3. **A/B/C 是变体，不是三套无关 look**：同一 look 的 `alternates` 共享 anchors/continuity，只允许声明轴（轮廓/年代/正式度）上的差异。
4. **审批状态与证据状态分离**：`approved` 不等于 `verified`；`evidence_status` 仍由来源规则决定；导演签核只表示创作决策。
5. **单件修改可回滚**：保留版本链，支持 `revert to vN`。
6. **composer 必须消费 Look Bible**：输入改为“approved look + 允许的变体轴 + 锁定 anchors”，禁止重新发明主件；未批准 look 只能作为 proposal 输出。
7. **验收**：validate 增加 Look Bible schema 校验；composer 增加 lock/diff 测试；P3.6 评分表与 approval 分离（分数可选、签核必须）。

### 14.3 实施建议（不在本次实现）

- 先做 **P5-0 数据模型草案**（JSON/YAML schema + 2 个样例 look：Macbeth M1-A、Lady L3-A），不接 composer；
- 再做 **P5-1 composer 锁定/diff**（hard anchors + item override，输出 change_log）；
- 最后做 **P5-2 导演审批流**（approve/revise/reject + 签名记录，和 P3.6 评分表联动但不代填）；
- 风险：审批权限/签名真实性、版本爆炸、与现有 LOOK 卡兼容、composer 候选池不足导致锁定后无替代件（需 graceful gap）。

---

## 15. 结论与优先级

**质量结论**：

- P3.5 18 套：**创作叙事与证据诚实最好的一批**，可作为 Look Bible 的“人工基准”；但有 2 套槽位硬缺口、1 套天气不匹配、2 套 theatrical 待导演确认。
- P4 自动输出：**工程覆盖强（槽位/ID/SRC/连续性状态），创作语义弱（跨时代/角色/叙事）**；`checks` 全绿会给出错误的安全感。
- P2.5 历史/当代/科幻：暴露系统性问题（年代假阴性、跨文化随机、连续性机械、冲突静默），与 P4 的问题同源。

**最严重问题（按优先级）**：

1. **AUD-001** A/B/C 指标把“单件替换”判为有意义差异；
2. **AUD-002** 完整 look 内的跨时代/角色错配不被阻断；
3. **AUD-003** 无 approved anchor / 版本 / 审批模型，单件修改无法安全表达。

**Look Bible 建议**：**建议做，但先做数据模型与 composer 锁定，不要先做 UI/审批界面**；版本化 look + hard anchors + change_log + 单件 diff 是解决上述三项的最小闭环；导演评分仍走 P3.6 空白评分表，不得由 AI 代填。

---

## 16. 限制

- 本审计未做导演/设计评审，不产生导演分数；所有 PASS/WARN/FAIL 为审计判断。
- P4 输出抽检为主（14 个 P4-MACBETH 输出 + 9 个 composer runs）；未覆盖全部历史输入组合。
- 单件修改实验在 `/tmp` 重跑，未写回仓库；composer 行为可能随版本变化（本次基于 P4 当前代码）。
- P3.5 槽位映射基于卡片 `category`，个别卡（inner_layer）归类可能有人为判断；已在文中标出。
- 未验证实际拍摄可行性（面料/预算/演员），仅审计文本与数据层面。
