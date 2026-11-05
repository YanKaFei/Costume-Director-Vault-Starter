# Obsidian 图谱修复（OBSIDIAN-GRAPH-FIX）

- 基线：HEAD `385e2bd`；实际 Obsidian 1.14.5；Vault 已打开。
- 目标：只修真实图谱，不扩卡、不改事实、不伪造关系。

## 1. 根因

1. Obsidian 默认把 Vault 内全部 `.md` 纳入图谱：**1435 个**，其中 **947 个**是 `11-验收`（812）、`reports`（89）、`projects`（37）、`docs`（5）、`skills/.dsh/TASKS/AGENTS`（4）等非知识文件。它们产生 **571 个零度节点/573 个分量**。
2. 知识卡内部还有两类“有数据无可见链接”：
   - 105 张来源卡有被引用入链、但没有反链到内容卡；
   - 174 张内容卡的 `## 来源链接` 仍是反引号 `SRC-xxxx`（代码），Obsidian 不认作链接；17 张场景卡因此是 YAML-only。

## 2. 修复

### 2.1 Obsidian 范围（本地配置，非 Git）
`.obsidian/app.json` 增加 `userIgnoreFilters`：
`11-验收/`、`reports/`、`projects/`、`docs/`、`tests/`、`skills/`、`.dsh/`、`TASKS/`、`TASKS.md`、`AGENTS.md`。
`.obsidian/graph.json` 清理错误 search，力参数调整为可读的紧凑布局（`repelStrength=4`、`linkStrength=2`、`linkDistance=120`、`centerStrength=0.9`）。
**配置备份**：`/tmp/obsidian-p5f-backup/{app.json,graph.json,workspace.json}`。

### 2.2 合法可见链接回填
- **来源→内容反链 324 条**，覆盖 105 张来源卡：仅使用内容卡已存在的 `source_ids`，按真实来源 ID 生成 `## 相关卡片` 的 `[[GAR-…]]`/`[[LOOK-…]]` 等；不改 source_ids、不改事实。
- **来源链接 295 条**，覆盖 174 张内容卡：把 `## 来源链接` 中的 `` `SRC-xxxx` `` 代码改成真实 `[[SRC-xxxx-文件名]]`；仅精确 ID，不猜测。
- **MOC/系统页链接**：补 35 张 P5-C 新内容、23 张新来源（P5-F 已有）、12 个系统/研究页的入口；MOC 仍只做导航，不写专业关系断言。
- 未新建知识卡；未增删 `source_ids`；未提升 draft/verified。

### 2.3 结果

| 指标 | 修复前（全 Vault） | 修复后（知识范围） |
|---|---:|---:|
| 节点 | 1435 | **488** |
| 零度节点 | 571 | **0** |
| 无入链 | 388 | **0** |
| 连通分量 | 573 | **1** |
| 单点分量 | 571 | **0** |
| YAML-only 卡 | 283（含非知识） | **0** |
| 未解析 wikilink | 401（含代码/非知识） | **0** |
| 可见边 | 4021 | **2673** |

内容卡单独视图：**224 卡 / 1 分量 / 0 零度**。

明细：限定范围 488 行 `reports/OBSIDIAN-FLOATING-NODES.csv`；全 Vault 1435 行 `reports/OBSIDIAN-FLOATING-NODES-ALL.csv`。

## 3. 校验

- `validate.py`：**PASS 458/458**（0 errors；12 个图片文件仅警告，均为本报告截图）。
- `relation_consistency.py`：**0 errors / 334 relations**。
- 未改 `source_ids`/`evidence_status`/`review_status`；未新建/删除任何卡。

## 4. GUI 证据

- 修复前默认图谱（全 Vault）：`reports/obsidian-graph/before-graph-all.png`（可见 571 个外围孤立点）。
- 修复后默认图谱：`reports/obsidian-graph/graph-after-all-links.png`（知识范围紧凑连通，无外围孤立环）。
- 另有 `after-graph-window.png`、`graph-after-final.png`、`graph-filtered.png`。
- 说明：Obsidian 的 `userIgnoreFilters` 是本地配置（`.obsidian` 不入 Git）；换机器/换 Vault 需按本报告重新设置，或在 Obsidian 设置中手动排除同样的目录。
