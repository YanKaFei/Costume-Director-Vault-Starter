# P5-E E4 239 候选关系风险审查（P5E-CANDIDATE-REVIEW）

- 生成：2026-11-05（Asia/Shanghai）；worker：researcher（task-89，P5-E E2/E4）
- 输入：`11-验收/P5D/DESIGN-QUEUE-REMAINING.csv`（**239 行**，medium/interpretive design 候选）
- 工具：`scripts/candidate_review.py`（保守三分类；不写卡、不自动提升）
- 产物：`11-验收/P5E/candidate-review.csv`、`11-验收/P5E/candidate-review.json`、`11-验收/P5E/summary.json`
- 原则：**NEVER auto-promote medium/review → high/verified**；全部 239 条 `design_only=true`、`auto_promotion=false`；本轮 **0 卡写入**。

## 1. 总览

| 分层（tier） | 数量 | 处理建议（proposal） | 含义 |
|---|---:|---|---|
| **source_verifiable** | **39** | **verify**（source-checkable；仅人工审核，design-only） | 端点 verified + 主体有 source_ids 或来源审计通过；可作为“可现源核实”候选，但仍不得写卡/升级 |
| **needs_human** | **163** | **review**（保留人工队列） | 设计/共现或证据不足；需人工语义复核，维持 medium/review |
| **reject_or_rework** | **37** | **reject/rework**（do_not_migrate） | 主体类型不合法/端点未验证/可能误导；不得迁移 |
| 合计 | **239** | | 0 自动提升、0 卡写入 |

## 2. 按关系类型的风险分层

| relation_type | 数量 | source_verifiable | needs_human | reject_or_rework | 风险要点 |
|---|---:|---:|---:|---:|---|
| appears_in_look | 116 | 0 | 116 | 0 | 只证明“该 LOOK 的组合清单包含该件”，**不是历史/穿着事实**；需人工确认组合价值 |
| uses_material | 70 | 39 | 31 | 0 | material/结构误导风险（见 §3）；39 条字段/来源可核实但仍是 design-only |
| in_style | 32 | 0 | 0 | 32 | 场景主体类型不合法（scene 不在 in_style 允许主体）+ 历史端点未双 verified；**不得当历史风格关系** |
| look_appears_in_scene | 16 | 0 | 16 | 0 | 场景归属可字段级核实，但 LOOK 为 interpretive；需人工 |
| may_have_part | 5 | 0 | 0 | 5 | 仅共现，**绝不能变成 has_part**；主体类型（look）不合法 |
| 合计 | 239 | 39 | 163 | 37 | |

## 3. 风险层（risks 标记）

| 风险标记 | 命中数 | 说明 |
|---|---:|---|
| `design_interpretation_not_fact` | **239** | 全部候选都是设计/共现/解释层，不是史实关系 |
| `material_structure_misleading` | **75** | uses_material 70 + may_have_part 5；不得从风格/共现反推“材质-结构”事实 |
| `historical_misleading` | **37** | in_style 32 + may_have_part 5；不得把风格标签/共现当历史断代或结构证据 |

### 典型拒绝原因（reject_or_rework 37）
- `invalid subject type scene for in_style`：15 条（scene 不是 in_style 的合法主体）；
- `historical/evidence endpoints not both verified`：32 条（含上条重叠；端点未双 verified）；
- `invalid subject type look for may_have_part`：5 条（LOOK 不是 garment，不能挂 has_part/may_have_part）。

### 典型候选
- **verify 例**：`GAR-0077 → MAT-0016 uses_material`（GAR-0077 source_ids 含 SRC-0066/0484/0485，MAT-0016 有来源审计；字段级 token=linen）——仍 `design_only`，人工确认后才可写 medium，不升 high。
- **review 例**：`GAR-0043 → MAT-0004 uses_material`（GAR-0043 source_ids 为空、MAT-0004 为金属线；只能作设计解释）。
- **reject 例**：`SCN-0002 → STY-0010 in_style`（scene 主体不合法 + 端点未双 verified）。

## 4. 处置建议（不自动执行）

1. **39 条 source_verifiable**：进入“人工核实批次”；由卡片 owner 核对源文与字段后，最多写 **medium design** 关系并补可见链接；**不得**升 high/verified。
2. **163 条 needs_human**：保留在人工队列，按关系类型分批语义复核（appears_in_look 116 优先筛“组合价值”，look_scene 16 次之）；复核前 Agent 不可见。
3. **37 条 reject_or_rework**：不迁移；in_style 的 scene 主体需重生成或删除；may_have_part 不得改写为 has_part。
4. **任何写卡**都需另立任务、备份、validate/build/relation_consistency 回归；本任务不做。

## 5. 6 key_garments flags：无新证据，保持人工

沿用 `reports/P5D-RELATION-QA.md` §2，**不自动确认/不强关**：

| flag | 目标 | 现状 | 建议（人工） |
|---|---|---|---|
| FLAG-KG-04 | PRD-0004 → GAR-0007 | GAR-0007 periods 无 1920s 精确重叠 | 移除或补 1920s 来源 |
| FLAG-KG-06B | PRD-0006 → GAR-0022 | Wellington 19c/contemporary 与 1940s 无重叠 | 移除/替换有源 1940s 鞋 |
| FLAG-KG-07 | PRD-0007 → GAR-0023 | moccasin 19c/contemporary，region 不兼容 | 移除，除非补跨文化/年代证据 |
| FLAG-KG-08 | PRD-0008 → GAR-0014 | 牛仔裤 1950s/contemporary，无 1960s 字段 | 条件保留/补证，否则移除 |
| FLAG-KG-08B | PRD-0008 → MAT-0004 | Lurex 1940s/1970s，无 1960s 精确重叠 | 移除/补证 |
| FLAG-KG-11 | PRD-0011 → GAR-0033 | GAR-0033 periods=1940s，PRD 1930s 上海 | 移除/补 1930s 上海证据 |

> 本轮未发现可关闭 6 flags 的新证据；保持 `review_queue`，不自动确认。

## 6. 仍缺证据 / 后续

- **163 条需人工语义复核**：尤其 116 条 appears_in_look（组合价值判断）与 31 条 uses_material（主体无 source_ids）。
- **37 条需重做**：in_style 的 scene 主体来源设计有误；may_have_part 需排除共现语义。
- **可现源核实 39 条仍非史实**：即使核实字段/来源，也只是 design/material 解释，不能进入历史断言。
- 研究侧事实缺口见 `reports/P5E-SOURCE-RESEARCH.md` §7（廓形分类、鱼尾剪裁、鞣制、具体聚合物、布光/动作）。
- 当前 CSV/JSON 由 `scripts/candidate_review.py` 生成；重跑：`python3 scripts/candidate_review.py`（幂等，输出同格式）。
