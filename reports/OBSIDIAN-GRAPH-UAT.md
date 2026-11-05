# Obsidian GUI 验收（OBSIDIAN-GRAPH-UAT）

- 环境：macOS，Obsidian **1.14.5**，Vault 已真实打开。
- 状态：**部分执行**。默认图谱和布局参数已实际截图；hide-orphans/content-only/local-graph 的图形切换未通过键鼠完成（osascript 无辅助功能权限），列入手工清单，**不得宣称全部 GUI PASS**。

## 1. 已执行

| 视图 | 操作 | 结果 | 证据 |
|---|---|---|---|
| 默认全局图谱 | Obsidian 打开 Vault → Graph view（工作区图叶） | 修复前全 Vault 有 571 个外围零度点；修复后知识范围紧凑连通 | `before-graph-all.png` / `graph-after-all-links.png` |
| 调整布局参数 | `repelStrength=4`、`linkStrength=2`、`linkDistance=120`、`centerStrength=0.9` | 外围散点消失，节点聚为连通团；缩放可读 | `graph-after-final.png` |

## 2. 手工验收清单（未执行，HUMAN_UAT_PENDING）

1. **默认全局图谱**：打开 Graph view，确认无 `11-验收/reports/projects` 节点；预期 488 节点、0 零度。
2. **隐藏 Orphans**：Graph 设置 → Filters → 关闭 “Orphans”；预期几乎不变（知识范围零孤立）；若仍出现点，记录路径到 `reports/OBSIDIAN-FLOATING-NODES.csv` 对照。
3. **仅内容卡**：Graph 搜索框输入 `-path:"04-来源"`（或 `path:"01-服装单品" OR ...` 按 Obsidian 语法），预期 224 卡、1 分量、0 零度。
4. **布局参数**：Forces 面板调整 repel/link/center；确认不会因参数把连通节点甩到视口外；截图保存。
5. **典型单品局部图**：打开 `GAR-0008-马甲` → Local Graph（深度 2），预期出现 GAR-0008、SRC-0109、LOOK/PRD 相关卡；记录缺失链。
6. **Properties/Backlinks**：抽查 `GAR-0077`、`GAR-0022`、`STR-0003`、`LOOK-0024`、`SRC-0062`、`MAT-0017`；Properties 显示 id/type/evidence_status/source_ids；Backlinks 至少有内容卡/MOC。
7. **来源反链**：打开 `SRC-0109-FIT-vest-waistcoat`，确认 `## 相关卡片` 有引用它的内容卡。
8. **MOC**：9 页全部可打开；`服装单品`/`结构细节`/`材质纹样`/`风格体系`/`造型组合`/`来源证据` 计数分别为 92/35/19/16/35+16/234。
9. **坏链/未解析**：Graph 设置 `hideUnresolved=false`；预期无红色未解析节点；当前静态 0。
10. **性能**：打开全局图与局部图，记录卡顿/帧率；488 节点应为可交互范围。
11. **截图与签核**：保存到 `reports/obsidian-graph/uat-screenshots/`；两人签核到 `reports/obsidian-graph/UAT-SIGNOFF.md`（未创建签字，禁止代签）。

## 3. 通过/失败标准

- 通过：默认/内容视图无知识卡零度点；局部图能显示真实来源/关联卡；Properties/Backlinks 与 `OBSIDIAN-FLOATING-NODES.csv` 一致；无坏链；MOC 计数正确。
- 失败：仍出现 10 个以上无链接知识卡；来源链接显示为代码；MOC 缺 P5-C 新卡；Properties 缺 id/type；出现未授权图片或历史断言。
- 当前结论：**静态与默认截图符合；完整 GUI 11 项仍 HUMAN_UAT_PENDING，不得声称全部通过。**
