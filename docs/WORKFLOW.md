# Costume Director Workflow（剧本驱动服装设计流程）

`scripts/workflow.py` 是一个**离线、可运行**的剧本驱动服装设计流程。它把一场/一部剧本转换成：
分场与人物提取 → 人物需求拆解 → 真实知识库检索（真实卡 ID + SRC 来源）→ 每人物每阶段 A/B/C 造型
→ 证据/冲突检查 → 跨场次连续性规划 → 可交付的 Markdown/CSV/JSON 与英文提示词。

工作流**只调用本 vault 的真实知识库**（`scripts/query.py`、`scripts/recommend.py`），
不联网、不生成图片、不编造卡 ID/SRC，也不会把 example 卡当作真实服装证据。

## 1. 用法

```bash
# 完整剧本（txt / md），带人物与制作设定
python3 scripts/workflow.py \
  --script tests/fixtures/macbeth.txt \
  --meta tests/fixtures/macbeth_meta.json \
  --out 11-验收/P3.5/workflow-runs/macbeth

# 单场剧本 / 没有 scene heading 的片段也可以
python3 scripts/workflow.py --script path/to/single-scene.txt --meta path/to/meta.json

# --out 必须在 Vault 内；Vault 外路径会被安全拒绝（exit 2，不写任何文件）
python3 scripts/workflow.py --script tests/fixtures/macbeth.txt \
  --meta tests/fixtures/macbeth_meta.json --out /tmp/outside-dir   # exit 2

# 只打印机器可读结果（文件仍会写入 --out）
python3 scripts/workflow.py --script tests/fixtures/macbeth.txt \
  --meta tests/fixtures/macbeth_meta.json --json
```

默认输出目录：`11-验收/P3.5/workflow-runs/<script stem>/`。
`--out` 可指定任意工作目录；脚本不会修改知识库卡片。

### 退出码（CLI contract）

| 退出码 | 含义 |
| --- | --- |
| `0` | 成功：解析到人物，并至少为一个人物/阶段生成可用 A/B/C 造型 |
| `2` | 调用/输入错误：脚本文件不存在、脚本为空、meta JSON 非法/不是对象、未知文件不可读；`--out` 指向 Vault 外（安全拒绝，保证不写外部路径） |
| `3` | 覆盖不足：未检测到人物，或所有人物/阶段都没有可用造型（知识库缺口）；仍会写结构化 partial 输出，`workflow-result.json` 里保留 warnings/unknowns |

`3` 不是崩溃：它表示“真实调用完成，但库内没有足够的实体卡支撑造型”，此时不要伪造 ID，
应把它当作知识库缺口报告。

## 2. 输入

### `--script`

- 支持 `.txt` / `.md`；
- 识别 Shakespeare 风格 `ACT I, SCENE I. ...`、`ACT I. SCENE I. ...`、
  `SCENE I. ...`、`INT./EXT.`、`第 N 场`、`内景/外景` 等 heading；
- `ACT I` 单独一行时作为 act 上下文，不制造空 fragment 场景；下一行 `SCENE ...` 才是场景边界；
- 没有 heading 时，整个文件作为单场；
- 每个 scene 同时记录 `act_number`/`scene_number`，供 meta 的 act-scene 引用映射；
- 场次 ID 固定为 `S1...Sn`，人物只从“实际出现的 speaker / 明确名字”提取，不虚构人物。

### `--meta`（可选 JSON）

```json
{
  "title": "production title",
  "period": "medieval",
  "region": "europe",
  "culture": "medieval Scottish court",
  "dramatic_style": "stark medieval tragedy",
  "art_direction": "torchlight and fog",
  "cinematic_style": "theatrical chiaroscuro",
  "lighting": "torchlight, cold moonlight",
  "camera": "medium shot",
  "season": "autumn",
  "weather": "storm, fog",
  "budget": "medium",
  "fidelity_mode": "inspired | historical | fictional",
  "tool": "generic | sora | midjourney ...",
  "characters": [
    {"name": "Macbeth", "aliases": ["MACBETH"], "occupation": "thane and general",
     "economic_status": "high", "arc": "loyal thane to tyrant",
     "relationships": ["Banquo: comrade"]}
  ],
  "stages": [
    {"id": "rise", "label": "thane / prophecy", "scenes": ["S1", "S2"]},
    {"id": "fall", "label": "tyrant / dagger", "scenes": ["1-3", "2-2"]}
  ],
  "scene_states": {
    "S1": {"wetness": "wet", "damage": "none", "dirt": "none"},
    "S3": {"wetness": "dry", "damage": "present", "dirt": "none"}
  }
}
```

- 缺失字段保持 `unknown`，并在输出 `unknowns` 中列出；**不会自动补成具体时代/职业/地区**。
- `characters` 可省略：script speaker 会被识别，但 occupation/class/arc 保持 `unknown`。
- `stages` 可省略：整段作为一个 stage（`whole`）。`scenes` 引用同时接受：
  - 解析后的 S-id（`S1`、`s2`、`S01`）；
  - act-scene 形式（`1-3`、`1.3`、`1/3`、`Act 1 Scene 3`、`I-III`），
    workflow 会依据 `ACT/SCENE` heading 解析结果映射到真实 S-id。
  例：`1-3 → S1`、`2-2 → S3`、`1-5 → S2`、`5-1 → S4`（Macbeth 四场 case）。
  无法映射的引用、未被任何 stage 引用的场景都会写入 warnings，并进入显式 `unassigned`
  stage；不会静默丢失场景。
- `scene_states` 是明确制作设定；未提供的 wetness/damage/dirt 保持 `unknown`，不推断“干净/脏”。
- 关系、职业、时代、地域等只作为输入事实/假设，不会写进“事实”栏冒充剧本原文。

## 3. 输出文件

每次运行写入 `--out` 目录：

| 文件 | 内容 |
| --- | --- |
| `character-dossier.md` | 人物档案：script presence、身份/阶层/职业/弧线/关系/功能、每阶段 A/B/C 摘要、unknown 标记 |
| `scene-costume-table.csv` / `.md` | 场次服装表：scene、character、stage、A/B/C 卡 ID、wetness/damage/dirt、evidence tier |
| `full-looks.md` | 每人物每阶段 A/B/C 的完整搭配：slot、真实卡 ID、名称、颜色、材质、结构卡、理由、风险、证据 |
| `prompts.md` | 每套 look 的 **English image prompt / video prompt**（清理 recommend 输出中的中文织物质感片段） |
| `continuity-plan.md` | 跨场次连续性：锚点（各 stage A 套交集）、状态链（wetness/damage/dirt）、换装/未知状态提示 |
| `fact-evidence-inference.md` | 事实 / 证据 / 创作推断三分栏 + 冲突与未知项 |
| `workflow-result.json` | 完整机器可读结果：scenes、characters、needs、retrieval、recommendations、evidence、continuity、checks、unknowns |
| `_inputs/` | 每次 recommend.py 调用的真实输入 JSON（可审计） |

### 证据规则

- 所有 garment/material/pattern/look/item ID 必须来自 vault；输出前用 `costume_lib` 校验，
  未知/编造 ID 会进入 `checks.ids_exist=false` 与 issues。
- 所有 `SRC-*` 必须存在于 `04-来源/`；缺失 URL/来源会报告，不补造。
- example 卡不会出现在 workflow look 中（query/recommend 默认排除 example）。
- `fidelity_mode=historical` 且没有 verified/exact 证据时，列为证据缺口，不宣称“历史准确”。
- 英文 prompt 由 recommend.py 的 image/video prompt 生成；含有中文织物质感说明的片段会被
  `english_only()` 过滤，保证交付提示词为英文。

## 4. Pipeline（实现要点）

1. **分场/人物提取**：规则化 heading、speaker、stage direction；不编造动作/天气。
2. **人物需求**：身份、阶层、职业、弧线、关系、场内功能（出场场次 + 台词块数，来自剧本事实）。
3. **KB 检索**：对每人物/阶段按 period、region、occupation、art direction、weather 调
   `query.py`；记录真实 ID 与 SRC。
4. **A/B/C 造型**：对每人物/阶段调用 `recommend.py`，保留 look ID、颜色、材质、结构、
   理由、风险、evidence、prompt；A/B/C 相同会被 `checks.abc_distinct=false` 标记。
5. **证据/冲突检查**：ID 存在性、SRC 解析、evidence 字段、missing URL、recommend warnings/conflicts、
   历史证据缺口。
6. **连续性**：按 stage 计算 A 套交集锚点；scene_states 明确时输出状态链，未明确时 `unknown`
   并列入 continuity issues；不虚构血渍/雨湿/破损。
7. **交付文件**：dossier、scene table、full looks、prompts、continuity、fact/evidence/inference、JSON。

## 5. 回归测试

```bash
python3 tests/test_workflow.py
```

固定 fixture 位于 `tests/fixtures/`：

- `macbeth`：Shakespeare 公开领域短片段（ACT/SCENE heading；inspired 中世纪演出）
- `rain_night`：当代雨夜/室内调查（wet → dry 连续性）
- `shanghai_1930s`：1930s 上海历史模式（exact/verified 证据）
- `sparse_unknown`：大量 unknown 的稀疏场景（验证 unknown 不编造）
- `no_characters`：无人物 fixture（验证 exit 3）

测试断言：真实 ID/SRC 存在；A/B/C 三套不重复；evidence 字段完整；unknown 不编造；
连续性 states 与 script/meta 一致；English prompt 无中文；CLI exit 0/2/3；
Macbeth scenes ≥3 且 stages 不会全部 unassigned。测试输出保存为
`11-验收/P3.5/workflow-runs/test-workflow.log`。

## 6. 已验证的 Macbeth 运行

```bash
python3 scripts/workflow.py \
  --script tests/fixtures/macbeth.txt \
  --meta tests/fixtures/macbeth_meta.json \
  --out 11-验收/P3.5/workflow-runs/macbeth
# exit 0
# scenes=3 characters=3 looks=yes warnings=0
```

结果：`11-验收/P3.5/workflow-runs/macbeth/`。
- S1 `ACT I, SCENE I. A desert place.`、S2 `ACT I, SCENE II. A heath near Forres.`、
  S3 `ACT I, SCENE III. A room in Macbeth's castle. Night.`（不再 fragment / unassigned）。
- stages：`rise`（S1,S2）/ `fall`（S3）；Macbeth 出现在 S2/S3，Banquo S2，Witches S1/S2。
- A 套（Macbeth thane）：GAR-0079（中世纪 kirtle）、GAR-0045（trench，inspired/era 近似）、
  GAR-0081（靴）、GAR-0080（腰带）；A/B/C 三套卡 ID 集合不同。
- 每条 look 的 evidence 含真实 SRC（示例：SRC-0405、SRC-0489、SRC-0487、SRC-0488），
  无编造 ID。
- `fact-evidence-inference.md` 明确分栏：script facts / real card+SRC evidence / inference；
  continuity 明确 S2 wet、S3 dry+damage present（来自 `scene_states`）。

## 6b. Act-scene stage mapping（D2 验证）

用真实 Macbeth excerpt + `workflow-meta` 的 act-scene 引用（`1-3`/`2-2`/`1-5`/`5-1`）重跑：

| Stage | Meta refs | Parsed scene | Scene heading |
| --- | --- | --- | --- |
| M1 | `1-3` | `S1` | ACT I — SCENE III. A heath. |
| M2 | `2-2` | `S3` | ACT II — SCENE II. The same. |
| L1 | `1-5` | `S2` | ACT I — SCENE V. Inverness. A room in Macbeth's castle. |
| L3 | `5-1` | `S4` | ACT V — SCENE I. Dunsinane. A room in the castle. |

结果目录：`11-验收/P3.5/workflow-runs/macbeth-case-actscene/out/`
（同时保留 `macbeth-case/` 的 S-id 兼容性运行；两种引用均映射到同一组 S1–S4，无 unassigned stage）。
回归测试 `test_act_scene_stage_mapping` 和 `test_exit_codes_0_2_3_and_outputs` 覆盖 D2/D3。

## 7. 已知限制

- 分场/speaker 是规则化解析，不替代专业剧本格式解析；复杂闪回、画外音、多人同句可能需要 meta 补充。
- Macbeth 是 **inspired** 中世纪演出：KB 没有 11 世纪苏格兰专属服装卡，A 套会有
  “period evidence approximate / region borrowing” warnings；因此输出把冲突列入
  `design_conflicts`，不把 inspired 造型声称为历史精确。
- `recommend.py` 的预算/风格默认值属于设计假设；unknown 输入仍会显式列入 `unknowns`。
- 英文 prompt 清理中文片段后可能损失少量织物质感描述；完整原文仍在 result JSON 的原始
  `prompt_image`/`prompt_video` 中保留。
- 工作流不生成图片/视频，只产出可交给图像/视频模型的文本 prompt。
- 每次人物/阶段会启动真实 `query.py`/`recommend.py` 子进程；完整长片可能较慢，可先用单场/meta 限定人物。
