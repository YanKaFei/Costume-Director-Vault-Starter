# P5-D 回填关系语义审查（P5D-SEMANTIC）

- 日期：2026-11-05（Asia/Shanghai）；执行：narrator（P5-D 独立复核）
- 快照：Before `5ae2c52`（265 relations）；After 当前树（314 relations；**+49**：30 design + 19 book claim）
- 只读；未改卡片/脚本；不提升 draft/verified；未新增卡；GUI NOT_RUN。
- 数据：
  - 回填差异由 before/after frontmatter relations 逐条 diff 得出（`/tmp` 只读快照 + 当前树；49 条新关系）
  - 30 条 **design backfill 已写入卡**；19 条 **book claim 已写入卡**；239 条仍在 `11-验收/P5D/REVIEW-QUEUE.csv`（未写卡）
  - 关系一致性：`relation_consistency.py` **0 errors / 314 relations**（当前树）；`validate.py` 458/458 PASS

## 0. 抽样结论

| 样本 | 数量 | PASS | WEAK | MISLINK | 通过率 |
|---|---:|---:|---:|---:|---:|
| 30 条 design backfill（已写入卡） | 30 | 25 | 0 | **5** | 83.3% |
| 10 条 book claim（已写入卡；从 19 条中抽） | 10 | 8 | **1** | **1** | 80.0% |
| **合计** | **40** | **33** | **1** | **6** | **82.5%** |

- 30 design 样本覆盖：6 appears_in_look / 7 in_style / 6 look_appears_in_scene / 4 may_have_part / 7 uses_material。
- 6 MISLINK 中 **5 条是类型/主语错误**（SCN→STY、LOOK→STR），1 条是 book claim 的 evidence/confidence 越级（GAR-0079 interpretive 却 high）；1 条 WEAK 是 1940s 卡引用 1908 词典（GAR-0033→SRC-0066）。
- 没有发现 **关键词/相似度自动建历史事实**：`uses_material` 为 materials token 精确匹配（medium/interpretive，候选）；`in_style`/`look_scene`/`appears_in_look` 均来自显式字段；未出现高置信历史断言。

## 1. 已写入卡的 30 条 design 关系

- 25 条语义成立：7 uses_material（garment/part→MAT 实体）、6 in_style（LOOK→STY，design-only）、6 look_appears_in_scene、6 appears_in_look。
- 5 条 **MISLINK（主语类型不符 schema）**：
  - **SCN-0001 → STY-0005**（in_style）：schema subject 允许 garment/part/look，不允许 scene。
  - **LOOK-0019 → STR-0011**、**LOOK-0003 → STR-0001**、**LOOK-0017 → STR-0010**、**LOOK-0008 → STR-0011**（may_have_part）：schema subject 应是 garment，LOOK 共现不能推出“服装有该部件”。
- 影响：这 5 条会出现在“已迁移/正式”关系集合中，Agent/relation_trace 可能把 scene→style、look→part 当作设计路径；`relation_consistency` 不检查 subject type，因此 0 errors 未能拦截。建议回滚或改型（LOOK→STY 已存在；SCN→STY 应删除；LOOK→part 应删除/改为 appears_in_look）。

## 2. 已写入卡的 19 条 book claim（抽 10）

- 8 PASS：MAT-0012/MAT-0016/MAT-0015/MAT-0018→SRC-0062（Textiles and Clothing）、MAT-0015→SRC-0066、GAR-0077/GAR-0011/GAR-0017→SRC-0066；均为 book_fact/词条级，不冒充分历史事实。
- 1 **MISLINK**：**GAR-0079 → SRC-0069**：claim 的 evidence=`interpretive` 却 confidence=`high`；schema high 要求两端 verified，book_fact 也不是 standalone verified——应降 medium 或移除。
- 1 **WEAK**：**GAR-0033（1940s 西装）→ SRC-0066（1908 男装词典）**：书只能支撑“sack coat”词义，不能支撑 1940s 具体断言；建议保留为背景/词义，不作为 1940s high 证据。
- 其余 9 条未逐条列出，但同规则抽检结论一致：book claim 必须显式标注 book_fact/位置，不能升卡级 verified。

## 3. 抽样明细（40 条）

| # | card → target | type | judgement | reason |
|---|---|---|---|---|
| 1 | `GAR-0010` → `MAT-0016` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 2 | `GAR-0021` → `MAT-0016` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 3 | `GAR-0020` → `MAT-0016` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 4 | `GAR-0012` → `MAT-0016` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 5 | `GAR-0007` → `MAT-0016` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 6 | `GAR-0003` → `MAT-0017` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 7 | `GAR-0002` → `MAT-0016` | uses_material | **PASS** | garment/part materials token 精确命中 MAT 实体卡；medium/interpretive，候选材料族，不是材料事实。 |
| 8 | `SCN-0001` → `STY-0005` | in_style | **MISLINK** | in_style subject 应为 garment/part/look；SCN→STY 是风格标签外推，不是类型化关系。 |
| 9 | `LOOK-0020` → `STY-0010` | in_style | **PASS** | style_tags 精确 STY ID；design-only/medium，不当历史事实。 |
| 10 | `LOOK-0014` → `SCN-0009` | look_appears_in_scene | **PASS** | LOOK.look_scene 显式引用；medium，不存在关键词推断。 |
| 11 | `LOOK-0002` → `GAR-0018` | appears_in_look | **PASS** | LOOK.look_items 显式共现；medium/interpretive 设计候选，不是历史套装。 |
| 12 | `LOOK-0012` → `STY-0010` | in_style | **PASS** | style_tags 精确 STY ID；design-only/medium，不当历史事实。 |
| 13 | `LOOK-0001` → `STY-0010` | in_style | **PASS** | style_tags 精确 STY ID；design-only/medium，不当历史事实。 |
| 14 | `LOOK-0019` → `STR-0011` | may_have_part | **MISLINK** | may_have_part subject 应为 garment；LOOK 共现不能推出“服装有该部件”。 |
| 15 | `LOOK-0011` → `SCN-0006` | look_appears_in_scene | **PASS** | LOOK.look_scene 显式引用；medium，不存在关键词推断。 |
| 16 | `LOOK-0006` → `GAR-EXAMPLE-001` | appears_in_look | **PASS** | LOOK.look_items 显式共现；medium/interpretive 设计候选，不是历史套装。 |
| 17 | `LOOK-0016` → `GAR-0040` | appears_in_look | **PASS** | LOOK.look_items 显式共现；medium/interpretive 设计候选，不是历史套装。 |
| 18 | `LOOK-0015` → `STY-0010` | in_style | **PASS** | style_tags 精确 STY ID；design-only/medium，不当历史事实。 |
| 19 | `LOOK-0003` → `STR-0001` | may_have_part | **MISLINK** | may_have_part subject 应为 garment；LOOK 共现不能推出“服装有该部件”。 |
| 20 | `LOOK-0010` → `GAR-0036` | appears_in_look | **PASS** | LOOK.look_items 显式共现；medium/interpretive 设计候选，不是历史套装。 |
| 21 | `LOOK-0022` → `SCN-0009` | look_appears_in_scene | **PASS** | LOOK.look_scene 显式引用；medium，不存在关键词推断。 |
| 22 | `LOOK-0017` → `STR-0010` | may_have_part | **MISLINK** | may_have_part subject 应为 garment；LOOK 共现不能推出“服装有该部件”。 |
| 23 | `LOOK-0009` → `STY-0010` | in_style | **PASS** | style_tags 精确 STY ID；design-only/medium，不当历史事实。 |
| 24 | `LOOK-0021` → `GAR-0045` | appears_in_look | **PASS** | LOOK.look_items 显式共现；medium/interpretive 设计候选，不是历史套装。 |
| 25 | `LOOK-0013` → `GAR-0005` | appears_in_look | **PASS** | LOOK.look_items 显式共现；medium/interpretive 设计候选，不是历史套装。 |
| 26 | `LOOK-0007` → `SCN-0001` | look_appears_in_scene | **PASS** | LOOK.look_scene 显式引用；medium，不存在关键词推断。 |
| 27 | `LOOK-0008` → `STR-0011` | may_have_part | **MISLINK** | may_have_part subject 应为 garment；LOOK 共现不能推出“服装有该部件”。 |
| 28 | `LOOK-0005` → `SCN-0002` | look_appears_in_scene | **PASS** | LOOK.look_scene 显式引用；medium，不存在关键词推断。 |
| 29 | `LOOK-0004` → `STY-0006` | in_style | **PASS** | style_tags 精确 STY ID；design-only/medium，不当历史事实。 |
| 30 | `LOOK-0018` → `SCN-0012` | look_appears_in_scene | **PASS** | LOOK.look_scene 显式引用；medium，不存在关键词推断。 |
| 31 | `MAT-0012` → `SRC-0062` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 32 | `MAT-0016` → `SRC-0062` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 33 | `MAT-0015` → `SRC-0062` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 34 | `MAT-0015` → `SRC-0066` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 35 | `MAT-0018` → `SRC-0062` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 36 | `GAR-0077` → `SRC-0066` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 37 | `GAR-0011` → `SRC-0066` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 38 | `GAR-0017` → `SRC-0066` | claim_supported_by | **PASS** | book_fact claim；SRC-0062/0066 可定位，high/verified 针对词条/纤维事实；不冒充 1940s/11c 史实。 |
| 39 | `GAR-0033` → `SRC-0066` | claim_supported_by | **WEAK** | GAR-0033 是 1940s 西装，SRC-0066 是 1908 男士服饰词典；书只能支撑 sack coat 词义，不能支撑 1940s 断言。 |
| 40 | `GAR-0079` → `SRC-0069` | claim_supported_by | **MISLINK** | claim high 但 evidence=interpretive；schema high 要求两端 verified；book_fact 不是 standalone verified。 |

## 4. relation_trace / query 可用性

| 命令 | 退出码 | 结果 |
|---|---:|---|
| `python3 scripts/relation_trace.py --start GAR-0015 --max-depth 2 --json` | 0 | paths 含 `context_includes`/`claim_supported_by`，design edges 标 `factual=false`；真实 ID/SRC |
| `python3 scripts/relation_trace.py --garment GAR-0015 --json` | 0 | `garment_looks` 找到 LOOK-0001 等，带 items/路径 |
| `python3 scripts/relation_trace.py --character "1930s Shanghai female reporter in rain" --json` | 0 | 找到 **LOOK-0030**（P5-C 新 Outfit），items 为 GAR-0031/0046/0022 等；叙事可用 |
| `python3 scripts/query.py "1930s 上海 雨 旗袍" --limit 5` | 0 | 命中 LOOK-0012、**LOOK-0030**、STY-0012 等；相关性可接受 |
| `python3 tests/test_relation_trace.py` | 0 | **6/6 PASS** |

- relation_trace 明确区分 `factual=false` 的 design 边，未把 design 关系当史实；旧卡与新 Outfit 都能被找到；**Outfit 叙事改善**：LOOK→narrative 25/35（71.4%），P5-B 基线 13/23（56.5%）。
- 局限：query 仍按关键词/文本，不保证关系路径；`relation_trace` 不校验已写卡 relation 的 subject type，故 §1 的 5 条 MISLINK 仍会被展示（虽标 design）。

## 5. 仍缺的语义/知识（只建议，不扩卡）

1. **结构（component）**：garment→component 16/92；结构卡→material 7/35、→style 0/35；需要“部件-服装/材料”的人工/结构字段，不是再堆 design 边。
2. **材料**：garment→material 39/92；19 条 material review 仍未卡；`material/pattern→style` 0；需要 canonical material/风格映射。
3. **风格**：garment→style 2/92；新 STY-0011..0015 只服务 P5-C 主题；旧 LOOK 的风格仍有自由 tag 漂移。
4. **Outfit 叙事**：10 套旧 LOOK 仍无 narrative；新 12 套已覆盖，但旧卡需人工补。
5. **来源**：39 张零可见 SRC 卡（38 draft + GAR-0045）；239 条 queue；9 本书源虽接入 19 条 book claim，仍不能当 standalone verified。
6. **独立专题**：拜占庭/莫卧儿/日本/奥斯曼/非西方没有区域 MOC；关系不应为连通率硬连。
7. **6 flags**（PRD-0004/0006/0007/0008/0011）仍 review_queue；38 基线 draft 未改；不得自动提升。

## 6. 结论与建议

- P5-D 的回填**不是零变化**：30 design + 19 book claim 已写入；但其中 **5 条 design 类型错误 + 1 条 claim 证据层级错误**，必须修正后才可作为 Agent 可信图。
- 建议优先级：
  1. **P1**：移除/改型 SCN→STY、LOOK→STR 的 5 条；GAR-0079 降 medium；GAR-0033 book claim 标 book_fact 背景。
  2. **P1**：relation_trace/relation_consistency 增加 subject type 校验（避免“0 errors 但语义错误”）。
  3. **P2**：239 条 queue 按 subject type 重分类/过滤；不要为降低 queue 数量硬迁移。
  4. **P2**：结构/材料/风格/Outfit narrative 仍是最重要的知识缺口；只建议，不扩卡。
- 未改任何卡片/脚本；未提升 draft/verified；GUI NOT_RUN。
