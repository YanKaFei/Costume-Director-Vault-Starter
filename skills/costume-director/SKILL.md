# Costume Director — 项目内技能使用说明（P2 正式版）

**用途**：当用户问“这个角色穿什么 / 如何符合剧本 / 为图像或视频生成服装提示词 / 检查多场次服装连续性”时，用本 Vault 的卡片检索 + 推荐脚本给出可解释、可溯源、可复制的造型方案。

**适用项目根目录**：`/Users/coffee/Desktop/Costume-Director-Vault-Starter`（唯一允许写入的项目目录；本技能不依赖任何网络服务、第三方安装或 Obsidian 插件）。

**依赖**：Python 3.9+ 标准库 + 已安装 PyYAML 6.x。无需联网即可运行核心脚本。

---

## 1. 知识库结构

| 目录 | 内容 | 卡片 type |
|---|---|---|
| `01-服装单品/` | 物理单品 | `garment` |
| `02-结构细节/` | 领/袖/门襟/褶/闭合等结构 | `garment_part` |
| `03-材质纹样/` | 材料/织造/纹样 | `material` / `pattern` |
| `04-来源/` | 真实来源登记卡（含 URL、许可、核验命令） | `source` |
| `05-风格体系/` | 历史/艺术/亚文化/职业/电影类型/虚构风格 | `style` |
| `06-时代地域/` | 年代+地域文化语境 | `period_region` |
| `07-剧情场景/` | 剧本场次/情境约束 | `scene` |
| `09-造型组合/` | 可直接拆解到单品/结构/材质的完整 Look | `look` |
| `00-系统/` | 数据字典、卡片模板、索引、来源规范（只读） | — |

卡片为扁平 YAML frontmatter + Markdown；`evidence_status` 区分 `verified` / `interpretive` / `example` / `unverified`。**检索与推荐只使用真实存在的卡片 ID，禁止编造 ID 或来源链接。**

---

## 2. `scripts/query.py` — 检索

### 2.1 基本用法

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter

# 关键词（默认 AND；中英文子串、大小写不敏感）
# 位置参数中的空格会拆成多个 AND 词："立领 shirt" = 立领 AND shirt
python3 scripts/query.py "立领 shirt"
# 需要精确短语时用 --phrase
python3 scripts/query.py "stand collar" --phrase
python3 scripts/query.py "rain" --limit 5

# 字段过滤（可重复/逗号分隔）
python3 scripts/query.py --type garment --category outerwear --limit 10
python3 scripts/query.py --type look --style-tag noir
python3 scripts/query.py "1930s" --period 1930s --region shanghai --json
python3 scripts/query.py --type source --evidence verified --json

# 只看指定卡片
python3 scripts/query.py --id GAR-0001 --json

# 机器可读输出 / 写文件
python3 scripts/query.py "dance" --json > /tmp/dance.json
python3 scripts/query.py "领" --limit 0 --json --out /tmp/collars.json
```

### 2.2 参数

| 参数 | 说明 |
|---|---|
| `terms` | 位置参数，检索词；词内空格按 AND 拆分；`--match any` 改 OR；`--phrase` 把每个参数当作精确短语 |
| `--type` | 卡片类型（garment/garment_part/material/pattern/style/period_region/look/scene/source），可重复 |
| `--category` | 同时匹配 category 与 subcategory |
| `--subcategory` | 匹配 subcategory |
| `--style-tag` | 命中任一 style_tags |
| `--period` / `--region` | 命中任一 periods / regions |
| `--evidence` | evidence_status（verified/interpretive/example/unverified） |
| `--tag` / `--id` | 命中 tags / 精确 ID |
| `--limit` | 返回上限，默认 10；`0` 表示全部 |
| `--phrase` | 每个位置参数作为完整短语（不拆词） |
| `--json` | 输出 JSON 数组；每项含契约字段 + `score` |
| `--verbose` | 文本模式显示命中字段 |

### 2.3 输出契约（`--json`）

```json
[
  {
    "id": "GAR-0001",
    "path": "01-服装单品/专门类型/GAR-0001-和服.md",
    "name_zh": "和服",
    "name_en": "kimono",
    "type": "garment",
    "evidence_status": "verified",
    "source_ids": ["SRC-0100"],
    "snippet": "…命中的正文片段…",
    "score": 8.0
  }
]
```

- `path` 为相对 Vault 根目录的路径；`source_ids` 可能为空数组（表示无来源，不表示编造）。
- 解析失败的卡片会跳过并在 stderr 打 `WARN`，不会静默当作正常卡。

---

## 3. `scripts/recommend.py` — 造型推荐

### 3.1 输入 JSON

支持扁平字段与嵌套 `character` / `scene` / `period` 对象，常见写法：

```json
{
  "character": {
    "name": "沈砚",
    "occupation": "journalist",
    "economic_status": "middle",
    "arc": "preserve dignity under pressure"
  },
  "scene": {
    "scene_id": "S1",
    "time": "night",
    "weather": "rain",
    "action": "walking",
    "location": "shanghai street"
  },
  "period": "1930s",
  "region": "shanghai",
  "season": "autumn",
  "art_direction": "restrained urban period drama",
  "lighting": "cool moonlight with warm practicals",
  "camera": "medium shot",
  "budget": "medium",
  "fidelity_mode": "historical",
  "tool": "midjourney",
  "state": {"wetness": "dry", "damage": "none", "dirt": "none"}
}
```

- 必填意图：`fidelity_mode`（historical / inspired / fictional）与场景描述；缺失字段自动记为 `unknown`，输出中显式标注，**不会猜成史实**。
- `character` 也可以直接是字符串；`period` 也可以是 `{"value": "1930s", "region": "shanghai"}`。
- `economic_status` 支持 low/middle/high 或 poor/working class/wealthy 等表述。
- `budget`：low/medium/high。
- `tool`：midjourney / sdxl / dalle / sora / runway / generic（影响提示词后缀与视频结构）。

### 3.1b 自由文本 `--brief`（P3）

```bash
python3 scripts/recommend.py --brief "1930s Shanghai, a poor journalist in the rain, noir period drama, low budget, historically accurate" --json
python3 scripts/recommend.py --brief-file myscript.txt
```

规则化提取 period / region / occupation / economic_status / weather / season /
art_direction / action / budget / fidelity_mode；未识别项保持 `unknown` 并在
JSON/正文中输出 `brief_parse`（含 `unknown_fields`）。显式 JSON 字段优先于 brief 解析。

### 3.2 运行

```bash
# Markdown 输出（TASK §7 稳定格式）
python3 scripts/recommend.py input.json

# JSON 输出（供其他脚本/Agent 消费）
python3 scripts/recommend.py input.json --json

# 写入文件
python3 scripts/recommend.py input.json --out result.md
```

### 3.3 硬约束（先过滤，再评分）

1. **年代文化**：`historical` 模式下，年代不匹配的卡片直接拒绝；`example` 卡不得作为历史证据。
2. **天气防护**：雨/雪/冷/风环境下要求外层；雨雪拒绝开放鞋履、拒绝麂皮/丝绸外层。
3. **动作/安全**：舞蹈/追逐/战斗拒绝高跟鞋、限制行动的结构；不因性别/国籍/职业刻板印象做判断。
4. **史实证据**：历史模式要求年代匹配卡；若知识库确无，输出缺口并标记 uncertainty，**不编造**。
5. **预算**：低预算时 C 套优先低成本材质与更少件数。

### 3.4 软评分（合计 100）

| 维度 | 权重 | 依据 |
|---|---|---|
| 年代/文化 | 25 | periods / regions / PRD 卡 / evidence 级别 |
| 角色身份 | 15 | 职业线索、经济状态、正式度、风格标签（启发式，不推断性格） |
| 环境气候 | 15 | 天气/季节与材质、外层、场景室内外 |
| 美术方向 | 15 | STY 卡 style_tags / 色彩 / 材质、art_direction 词 |
| 动作可行 | 10 | movement_notes、鞋履、结构限制 |
| 剧情弧线 | 10 | arc 关键词与磨损/整洁/层次等标签（导演解释，不是史实） |
| 摄影/一致性 | 10 | lighting_notes、prompt_en、source_ids、review 状态、色彩一致性 |

- A（首选）= 综合得分最高且通过硬约束；B = 与 A 明确不同（颜色/结构/风格）的次选；C = 预算或美术方向替代。
- 三套都输出真实卡片 ID；若某品类无卡，标记 `missing`，不虚构补齐。

### 3.5 输出契约（`--json`）

```json
{
  "input": { "...": "规范化后的输入，unknown 会显式出现" },
  "fidelity_mode": "historical",
  "looks": [
    {
      "look_ref": "A",
      "source_look_id": "LOOK-0001 或 null（assembled）",
      "total": 78.5,
      "base_score": 80.0,
      "scores": {"period": 22.0, "identity": 12.0, "environment": 11.0,
                 "art": 12.0, "movement": 8.0, "arc": 7.0, "camera": 7.5},
      "missing": [],
      "cost": 0.42,
      "colors": ["charcoal"],
      "style_tags": ["noir"],
      "items": [{"slot": "outerwear", "id": "GAR-0004", "name_zh": "...",
                 "name_en": "...", "colors": ["charcoal"], "materials": ["wool"],
                 "evidence_status": "verified", "source_ids": ["SRC-0100"],
                 "scores": {"period": 0.9, "...": 0.8}}],
      "parts": [{"id": "STR-0002", "slot": "outerwear"}],
      "materials": [{"id": "MAT-0001", "slot": "outerwear"}],
      "prompt_image": "full-body character design ... continuity lock: ...",
      "prompt_video": "... negative constraints: ...",
      "continuity_lock": "continuity lock: GAR-... [color; material; slot]; wetness=dry; ...",
      "reasons": ["..."],
      "risks": ["..."],
      "evidence": {"source_ids": [], "source_urls": [], "item_evidence": {}}
    }
  ],
  "context": {"style_refs": [], "period_refs": [], "scene_refs": []},
  "retrieved_ids": {"upper_body": [], "lower_body": [], "outerwear": [], "footwear": []},
  "rejected": [{"id": "GAR-0002", "slot": "upper_body", "reasons": ["historical mode: period mismatch"]}],
  "warnings": [],
  "sources": [{"source_id": "SRC-0100", "url": "https://..."}],
  "missing_urls": [],
  "checks": {
    "ids_all_exist": true, "three_looks": true, "all_have_garment": true,
    "scores_sum_100": true, "looks_distinct": true,
    "fidelity_mode": "historical", "history_evidence": true
  }
}
```

- `look_ref` 的 A/B/C 是本次推荐序号；`source_look_id` 只有命中真实 `LOOK-` 卡时才有值。**不存在“组装 Look 的伪造 ID”**：assembled 组合用 `look_ref`，不冒充卡片 ID。
- 所有 `items[].id` / `parts[].id` / `materials[].id` 都能在 Vault 文件中找到。
- `missing` 非空表示知识库缺口，必须在交付时说明。

### 3.6 多场次连续性（同一 Look 跨场锁定）

输入 JSON 顶层加 `scenes` 数组（每个场景可覆盖 time/weather/action/scene/state）：

```json
{
  "character": {"name": "Lin", "occupation": "private investigator"},
  "period": "contemporary",
  "fidelity_mode": "fictional",
  "scenes": [
    {"scene_id": "S1", "weather": "dry", "action": "walking",
     "state": {"wetness": "dry", "damage": "none"}},
    {"scene_id": "S2", "weather": "heavy rain", "action": "running",
     "state": {"wetness": "wet", "damage": "none"}},
    {"scene_id": "S3", "weather": "indoor", "action": "searching a desk",
     "state": {"wetness": "drying", "damage": "none"}}
  ]
}
```

```bash
python3 scripts/recommend.py continuity.json --continuity > continuity.md
python3 scripts/recommend.py continuity.json --continuity --json
```

- 先为全部场景选一套基础 Look，所有场景锁定同一批衣物 ID。
- 每个场景只允许 `state`（wetness/damage/dirt/accessories）显式变化；未显式给出 state 的场景会被判 FAIL 并记录 issue。
- 输出 verdict：`PASS` / `FAIL`，附逐场状态表与每场 prompt（都含同一段 continuity lock）。

### 3.6b P3 输出字段（向后兼容新增）

- `context_refs`：已按 period/region 兼容度过滤的语境卡（style / period_region / scene），
  含 `period_tier`、`region_tier`、score；不匹配的卡被移除，不再输出误导性 1770s 英法引用。
- `warnings` / `warnings_detail`：显式警告（code/severity/message/items/look），覆盖：
  example 卡进入方案、知识库缺层、年代/地域不匹配、era-level/approximate 证据、
  职业/未来/雨具/性别/文化覆盖缺口、约束冲突、A/B/C 或预算不足、brief unknown 字段。
- `conflicts`：冲突检测（historical vs sci-fi、室内 vs 北极装备、天气 vs 材质、
  动作 vs 鞋履、婚礼 vs 丧仪、预算 vs 材质），附建议解决方式。
- 每套 look 新增：`evidence_tier`（exact/era/approximate/none）、`period_tiers`、
  `region_tiers`、`contains_example`、`cost_total`、`differences`、`budget_mode`、
  `budget_explanation`、`narrative_meaning`（导演解释，不是史实）。
- example 卡策略：A 套不使用 example 卡；若知识库只有 example 候选，会显式 warning 并标
  `contains_example`（仅 B/C 或缺口场景）。
- A/B/C 差异：合约校验 pairwise ≥2 件单品差异（`checks.abc_distinct`）；
  C 套优先比 A 便宜 ≥10%，否则为 `equivalent_cost` 并明确说明等价原因。
- 连续性：顶层 prompt 仅为参考表（不含多场动作/天气）；逐场 prompt 在
  `continuity.scenes[].prompt_image/prompt_video`，各自带 state token 与 continuity lock。
- 稀疏覆盖：允许结构化 1–2 套 Look（不崩溃），warning 明示 `looks_incomplete` 与缺口。

### 3.6c 语义质量评估（独立于 exit code）

```bash
python3 scripts/quality_eval.py            # 写 11-验收/质量评估/
python3 scripts/quality_eval.py --no-write # 只打印摘要
```

指标：query relevant@5 / precision / zero-hit、推荐崩溃率、example-in-A 率、
warning 覆盖率、A/B/C 全差异率、证据覆盖率、context 引用清洁率、narrative 覆盖率、
prompt 串文数、编造违规；基线为 P2.5 审计（235 卡）并输出前后对比表。
退出码：0 全部质量阈值通过，1 至少一项不通过。

### 3.7 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 推荐成功（可能有 warnings/缺口） |
| 2 | 输入文件不存在 / JSON 非法 / 输入不是对象 |
| 3 | 无任何可用候选（知识库缺口，缺必需品类） |

---

## 4. 提示词模板

- `10-提示词模板/01-角色设计模板.md` — 输入字段、A/B/C 组装、连续性锁定、严格度措辞
- `10-提示词模板/02-静态生图提示词模板.md` — 生图结构公式、负向约束
- `10-提示词模板/03-视频提示词模板.md` — 镜头/动作/布料动态/状态切换/多场次分镜表

推荐结果中的 `prompt_image` / `prompt_video` 已与这些模板同构，可直接复制。

---

## 5. 验收测试

```bash
python3 scripts/run_acceptance.py            # 30 例全跑，写 11-验收/测试结果/（P3: ≥24 例）
python3 scripts/run_acceptance.py --only T03,T17
python3 scripts/run_acceptance.py --no-write # 只看判定
```

- 定义见 `11-验收/测试场景.md`（30 例：18 例 P2 回归 + 12 例 P2.5/P3 回归：1940s–70s、1580s 意大利、拜占庭、太空、急诊护士、加纳婚礼、1930s 男鞋/雨衣、冲突约束、--brief）。
- 结果见 `11-验收/测试结果/SUMMARY.md` 与逐例文件；语义质量见 `11-验收/质量评估/SUMMARY.md`。
- 每个用例记录实际命令、退出码、`query.py` 命中数量与 ID、A/B/C、评分、Prompt、风险、PASS/FAIL。
- 验收断言：每个场景的 `query.py` 步骤必须退出码 0 且命中 ≥1 张卡（`query_hits` 检查项）；SUMMARY 汇总每例命中数。
- `run_acceptance.py` 退出码：0 全部 PASS；1 至少一项 FAIL。

---

## 6. 工作流程（Agent 使用顺序）

1. 从剧本/描述解析：角色、剧情日、时间地点、阶层职业、动作/气候、美术/摄影、预算、严格度、工具；缺项标 `unknown`。
2. 用 `query.py` 查真实卡片（服装/结构/材质/风格/时代/Look/来源），确认证据与缺口。
3. 用 `recommend.py` 生成 A/B/C 与评分；**不得手工编造 ID**。
4. 把 `prompt_image` / `prompt_video` 与 `continuity_lock` 写入交付；严格区分 historical / inspired / fictional。
5. 多场次时运行 continuity 模式，逐场复制同一段 continuity lock。
6. 若知识库缺证据：明确写“缺少证据 / KB gap”，提出补卡任务；不得把 example/interpretive 卡标成 verified。
7. 交付前跑 `run_acceptance.py` 并核对 SUMMARY。

---

## 7. P3 质量语义限制（如实记录）

- 年代/地域归一化是**兼容性层级**（decade→century→era），不是精确断代：era-level / approximate
  证据会在 warnings 与 `evidence_tier` 中明示，不能当作精确年代结论。
- context_refs 仍可能有粗粒度（如 europe）匹配；已过滤 period/region=none 的引用，但
  “同一时代不同地域”的细微差异仍需人工复核。
- narrative_meaning 与冲突建议是导演/设计解释，不是服饰史事实；冲突检测是规则集，不是全语义理解。
- example 卡在 B/C 或稀疏覆盖时仍可能出现（有 warning 与 `contains_example` 标记），A 套禁止。
- 质量指标（relevant@5、precision、warning 覆盖率）含人工定义的探针/expected 集合，不是绝对真理。
- 生图/视频成品效果、Obsidian GUI、逐图版权仍需人工 UAT；脚本不能代替真实拍摄验证。

## 7. 已知限制

- 检索是关键词/字段匹配，不是语义 embedding；同义词需通过 `aliases`、`style_tags`、`tags` 或中英文别名覆盖。
- 评分是**可解释启发式**，不是导演判断；身份/阶层线索不构成性格或心理断言。
- 年代/地域硬约束依赖卡片字段质量；粗粒度地域标签（如 `east_asia`）不会因城市名不同被硬拒绝。
- 视觉验证（Obsidian GUI、生图实际效果、图片授权）不在本技能内自动完成；不得声称已验证 UI 或图像版权。
- 知识库持续更新：每次新增卡片后重跑推荐与验收测试，SUMMARY 才有效。
