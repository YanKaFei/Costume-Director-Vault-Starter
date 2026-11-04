# P5-A 图谱诊断（P5-GRAPH-DIAGNOSIS）

- 生成：2026-11-05 01:20（Asia/Shanghai）；verifier / task-59（P5-A 只读诊断）
- **基线快照：HEAD `1acb4d3`（1acb4d397906b82941cf4debe0a0c58ff8de34b4，"R1.1: final report consistency"）**，通过 `git archive HEAD` 导出到临时目录分析（只读；未修改卡片）
- 快照规模：**400 卡（内容 189 + 来源 211）**；扫描 Markdown **416 个节点**（内容 189 / 来源 211 / 导航 14 / 研究 2）
- 产物：本报告 + `reports/P5-GRAPH-BASELINE.csv`（416 行，逐节点基线）+ `scripts/graph_analyze.py`（可复跑）

## 0. P0 基线告警（必须先读）

> **工作区当时被 P5 迁移临时破坏（lead 报告：validate 371/400、29 个卡片缺 closing fence）**，因此本诊断**不使用 live 卡片**；全部数字来自 **HEAD `1acb4d3` 的干净快照**。
> 诊断期间我于 01:16 对 live 树跑 `validate.py` 得到 PASS 400/400（工程师可能已部分修复/继续改动），说明 **live 树在诊断期间仍在变化**。**在 P5 迁移完成并冻结前，不得用 live 数据做图谱结论**；迁移完成后建议用本脚本对最终 commit 重跑（`--root <snapshot>`）。
> 本 P0 = 基线不稳定/数据不可解析风险，不是本报告分析的 HEAD 快照缺陷。

## 1. 方法与口径（机器数据 ≠ Obsidian 链接）

- 扫描范围（按 task-59）：`00-系统/ 01-服装单品/ 02-结构细节/ 03-材质纹样/ 04-来源/ 05-风格体系/ 06-时代地域/ 07-剧情场景/ 09-造型组合/ 10-提示词模板/ + README.md/AGENTS.md`。
- 排除：`.git`、`projects/`、`11-验收/`、`reports/`、`tests/`、`docs/`、`.dsh/`、`skills/`、`.obsidian/`、`sandbox-*` 副本、`__pycache__`。
- 角色分类：
  - **content**：frontmatter `type ∈ {garment, garment_part, material, pattern, style, period_region, scene, look}`（189）
  - **source**：`type=source`（211）
  - **navigation**：`00-系统/`、`10-提示词模板/`、根 README/AGENTS（14）
  - **research**：`06-时代地域/书籍研究/`（2；其中书籍研究主文档是 P4 书籍结论）
- **visible edge（可见 Wikilink）**：正文 `[[...]]`，按文件名 stem / ID 前缀解析到节点；同一对节点去重计度，出现次数另计；**unresolved=0**。
- **typed edge（机器/类型化关系）**：frontmatter 的 `source_ids`、`look_items`、`look_scene`、`key_garments`、`superseded_by`、`canonical_id`；所有引用均解析到真实 ID。
- **核心口径**：YAML 里的 `source_ids` 是**机器数据关系**，不是 Obsidian 内部链接；只有正文 `[[...]]` 才是可见链接。诊断把二者分列，避免把「有 citation 字段」误当「图谱连通」。
- 连通分量只在**语义图（content+source 卡片）**上计算（导航/研究文档不参与分量），把「导航可达」与「卡片语义关系」分开。

## 2. 总量与零链接/入出度

| 指标 | 数值 |
|---|---|
| 扫描 Markdown 节点 | **416**（content 189 / source 211 / navigation 14 / research 2） |
| 正文 Wikilink 出现次数 | **1271** |
| 去重可见边 | **1114**（语义卡-卡 **1090** + 导航/研究 **24**） |
| unresolved wikilink | **0** |
| 机器 typed 边 | **485**（source_ids 299、look_items 117、look_scene 22、key_garments 45、superseded_by 1、canonical_id 1） |

### 2.1 按角色的可见入/出度（首次进入图谱的关键数字）

| 角色 | 节点 | 零可见链接 | 只入链 | 只出链 | 双向 |
|---|---|---|---|---|---|
| **content** | 189 | **0** | 0 | 1 | **188** |
| **source** | 211 | **58**（其中 56 零总度） | 11 | 129 | 13 |
| **navigation** | 14 | 9 | 2 | 1 | 2 |
| **research** | 2 | 1 | 0 | 1 | 0 |

- **内容卡没有「零链接」**（189/189 至少一条可见边；188 双向）；但**来源卡 58/211（27.5%）没有任何可见链接**，129 张只出链（source→content 有出链但无入链）。
- 来源卡的可见出链（source→content 186 对）是 source 卡正文在「关联卡片/实例」处主动链到内容卡；内容卡很少反向可见链到 source（content→source 仅 **2** 对）。

### 2.2 source_ids 有、可见链接无

- **181 张内容卡有 source_ids**；其中 **180 张（99.4%）没有任何可见 SRC Wikilink**，仅 **2 张**内容卡在正文链到来源：
  - `PRD-0003` → `[[SRC-0021-…]]`
  - `SCN-0001` → `[[SRC-0036-…]]`
- source_ids 机器对数 **299**；其中 **297 对（99.3%）**在对应卡片正文中没有可见 `[[SRC-…]]`；143 个不同来源被机器引用，但**仅 2 个**来源同时被可见引用（SRC-0021、SRC-0036）。
- 结论：**citation 存在于 YAML，不在 Obsidian 图谱中**——这是「知识库看似大量引用、图谱却稀疏」的首要原因。

## 3. 类型化关系 vs 可见 Wikilink

| 关系（typed） | 边数 | 无对应可见链接 | 说明 |
|---|---|---|---|
| `source_ids` | 299 | **297（99.3%）** | 内容→来源；绝大多数只在 YAML |
| `key_garments` | 45 | **16（35.6%）** | PRD→内容；部分已可见 |
| `look_items` | 117 | **0** | LOOK 正文已逐件链到卡（可见） |
| `look_scene` | 22 | **0** | LOOK 正文链到 SCN |
| `superseded_by` / `canonical_id` | 1 / 1 | **0** | GAR-0087 → STR-0026 / GAR-0048，正文已有链接说明 |
| **合计** | **485** | **313（64.5%）** | 机器关系大量「不可见」 |

- **导航 vs 专业语义**：可见边中导航/研究 24（navigation→content 9、navigation→navigation 6、research→source 9）；专业语义 **1090**（content→content 886、source→content 186、source→source 16、content→source 2）。
- **独立专题的证据关系**：书籍研究（research 文档）以 9 条可见边链到 SRC-0061..0069（P4 九本 PD 书），但这些书源**不在任何内容卡的 source_ids 或可见链中**；它们只在「研究文档」层可见——属于**证据在知识层存在、但在卡片图未接入**。

## 4. 连通分量（语义卡片图 content+source）

| 指标 | 数值 |
|---|---|
| 语义节点 | 400（189 content + 211 source） |
| 分量数 | **66** |
| 最大分量 | **335**（**189 content + 146 source**；所有内容卡都在其中） |
| 分量大小分布 | `{335: 1, 1: 65}`（1 个主分量 + 65 个孤立单点） |
| 其它含 content 的分量 | **0**（所有 content 都在主分量） |
| 65 个单点分量 | **全部是 source**（28 isolated + 27 background + 9 navigation-only 书源 + 1 book）；按 source_kind：vocabulary 19、museum_collection 12、reference_work 9、academic_reference 8、other 8、image_repository 5、industry_framework 3、dataset 1 |

- **内容图基本连通**（189 内容卡全部在主分量，188 双向），主要问题不在内容-内容，而在**来源接入**：146 来源进入主分量（通过机器 source_ids 或可见链），**65 来源完全孤立**。
- 没有「独立的内容专题分量」：独立专题目前表现为**来源孤岛**而非内容孤岛；若 P5 要建 MOC/专题，需优先把孤立来源挂到内容卡/专题页。

## 5. 来源孤岛原因分类（211 来源）

| 原因 | 数量 | 含义/证据 |
|---|---|---|
| `source_ids_only_no_visible_link` | **128** | 仅被内容卡 YAML source_ids 引用；正文无可见 SRC 链接（机器可见、图谱不可见） |
| `source_ids_only_mixed` | **13** | 机器引用且部分可见/导航混合，但内容可见入链仍不足 |
| `isolated_source` | **28** | 无任何入链/出链；source 卡自身也无到内容的可见链 |
| `background_or_dictionary_uncited` | **29** | 无 citation；多为 vocabulary/academic reference（供检索/背景，未被卡片引用） |
| `navigation_only` | **9** | 只被「研究/导航文档」链接（正是 SRC-0061..0069 九本 P4 书源，被书籍研究文档链到） |
| `linked_visible_from_content` | **2** | 内容卡正文可见链到来源（SRC-0021、SRC-0036） |
| `book_source_no_card_integration` | **1** | 书源未被卡片或研究文档接入（SRC-0060 等） |
| `outbound_only_no_incoming` | **1** | 来源卡出链到内容但无入链 |

**原因归纳**：
1. **引用习惯**：内容卡把来源放 `source_ids`（YAML），不在正文渲染 `[[SRC-…]]`（180/181 卡）→ 机器关系 297 对不可见。
2. **方向不对称**：source 卡正文经常链到内容卡（186 对），内容卡几乎不链回（2 对）→ 来源「只出链/零入链」。
3. **背景/字典源**：29 张 vocabulary/reference 天然是检索背景，未被任何卡引用（合理但需在专题/MOC 标注用途）。
4. **P4 书源未接入卡片**：9 本 PD 书只在研究文档可见，未进入 content source_ids → 卡片图缺书源证据。
5. **索引/MOC 覆盖不足**：14 个导航文档中 9 个零可见边（模板/扩展文档等），导航未承担图谱连接职责。

## 6. Top 20 孤立卡（零总度，按角色/来源优先）

| # | ID | 原因 | in/out | 分量 |
|---|---|---|---|---|
| 1 | SRC-0002 | isolated_source | 0/0 | 单点 |
| 2 | SRC-0003 | isolated_source | 0/0 | 单点 |
| 3 | SRC-0004 | background_or_dictionary_uncited | 0/0 | 单点 |
| 4 | SRC-0005 | background_or_dictionary_uncited | 0/0 | 单点 |
| 5 | SRC-0006 | background_or_dictionary_uncited | 0/0 | 单点 |
| 6 | SRC-0007 | background_or_dictionary_uncited | 0/0 | 单点 |
| 7 | SRC-0008 | background_or_dictionary_uncited | 0/0 | 单点 |
| 8 | SRC-0009 | background_or_dictionary_uncited | 0/0 | 单点 |
| 9 | SRC-0010 | background_or_dictionary_uncited | 0/0 | 单点 |
| 10 | SRC-0011 | background_or_dictionary_uncited | 0/0 | 单点 |
| 11 | SRC-0012 | background_or_dictionary_uncited | 0/0 | 单点 |
| 12 | SRC-0013 | background_or_dictionary_uncited | 0/0 | 单点 |
| 13 | SRC-0014 | background_or_dictionary_uncited | 0/0 | 单点 |
| 14 | SRC-0015 | background_or_dictionary_uncited | 0/0 | 单点 |
| 15 | SRC-0016 | background_or_dictionary_uncited | 0/0 | 单点 |
| 16 | SRC-0017 | background_or_dictionary_uncited | 0/0 | 单点 |
| 17 | SRC-0018 | background_or_dictionary_uncited | 0/0 | 单点 |
| 18 | SRC-0019 | background_or_dictionary_uncited | 0/0 | 单点 |
| 19 | SRC-0020 | background_or_dictionary_uncited | 0/0 | 单点 |
| 20 | SRC-0023 | isolated_source | 0/0 | 单点 |

- 其余 36 个零总度来源见 CSV（`zero_total=1`，共 56）。65 个单点来源分解：**28 isolated + 27 background + 9 navigation-only（书源）+ 1 book**；零总度 56 = 28 isolated + 27 background + 1 book。Top 列表按 ID 排序，完整原因见基线 CSV `reason` 列。

## 7. 对 P5 的直接含义（诊断结论，不实施）

1. **先修可见引用**：把内容卡 source_ids 的关键来源渲染为正文 `[[SRC-…]]`（或生成「来源链接」小节），否则图谱永远无法反映 143 个被引用来源中的 141 个。
2. **来源接入专题/MOC**：28 isolated + 29 background + 9 书源应挂到专题页/内容卡；书源（SRC-0061..0069）优先补入内容卡或 book MOC，否则 P4 书籍证据在卡片图不可见。
3. **导航承担连接职责**：14 个导航文档中 9 个零可见边；索引/MOC 应显式链到孤立来源与专题入口。
4. **区分「机器关系」与「图谱连通」**：P5 的连通性指标必须同时报告 typed 与 visible 两套；仅用 source_ids 会高估连通性，仅用可见链接会低估引用完整性。
5. **基线冻结后重跑**：P5 迁移完成、live 树 validate 400/400 且冻结后，应对最终 commit 重新 `git archive` + 本脚本复跑，比较零链接/分量变化。

## 8. 复现

```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
# 1) 导出干净基线（只读）
rm -rf /tmp/p5-head-snapshot && mkdir -p /tmp/p5-head-snapshot
git archive 1acb4d3 | tar -x -C /tmp/p5-head-snapshot
# 2) 诊断
python3 scripts/graph_analyze.py --root /tmp/p5-head-snapshot \
  --csv reports/P5-GRAPH-BASELINE.csv --json /tmp/p5_graph.json
```

- 基线 CSV 列：`id,type,role,path,in,out,source_ids,wikilinks,component,component_size,in_typed,out_typed,zero_visible,zero_total,reason`
- 证据 JSON：`/tmp/p5_head2.json`；stdout：`/tmp/p5_head2.out`；live 树 validate 记录：`/tmp/p5_live_validate.txt`（01:16，PASS 400/400，但 live 仍有 29 项未提交 P5 迁移改动）。

## 9. 限制

- 本报告是**只读诊断**，不修改卡片/脚本行为；所有数字基于 HEAD `1acb4d3` 快照，而非 live 树。
- 可见链接解析按 stem/ID 前缀；unresolved=0，但若未来出现跨文件别名链接需扩展解析。
- 未扫描 `11-验收/`/`reports/`/`docs/` 等（按任务口径排除）；这些目录的链接未计入连通性。
- `source_kind` 分类来自来源卡字段，未人工逐条复核 29 background 源的使用意图。
- 机器关系计数为 frontmatter 字段条目；同一对节点多种关系时分别计入。
