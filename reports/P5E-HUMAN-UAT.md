# P5-E Obsidian 人工验收清单（P5E-HUMAN-UAT）

- 状态：**NOT_RUN / PENDING**（本环境无 Obsidian GUI；未打开 vault、无截图、无签字）
- 日期：2026-11-05；verifier / task-92；**不得把本清单当 PASS**
- 机器预检（已执行）：458 卡 / 234 来源；validate **458/458 PASS**；build **234 PASS**；consistency **0 errors / 334 relations**；MOC 9 页（导航 26 节点）；backlinks/Properties/局部图需 **Obsidian 内人工执行**。

## 使用方式

1. 用 Obsidian 打开 vault：`/Users/coffee/Desktop/Costume-Director-Vault-Starter`（建议备份 `.obsidian` 后测试）。
2. 按 §1–§8 逐项执行；每项记录 **Observed（实际）/ Status（PASS/FAIL/BLOCKED）/ 截图路径 / 操作人 / 日期**。
3. 任一 FAIL 或 BLOCKED → 整体仍 **NOT_RUN/PENDING**，不得写入 RELEASE-GATE 的 PASS。

## 验收项

| # | 检查项 | 操作步骤 | 预期 | 结果（Observed） | 状态 |
|---|---|---|---|---|---|
| 1 | Vault 入口/README | 打开 vault；打开 `README.md` 或 `00-系统/索引.md` | 无解析错误；能看到入口说明/导航 | — | **NOT_RUN** |
| 2 | MOC 导航（9 页） | 打开 `00-系统/MOC/` 各页，点击各分区链接 | 9 页可打开；链接到内容/来源；无坏链 | — | **NOT_RUN** |
| 3 | Properties 面板 | 打开 GAR-0077 / LOOK-0024 / SRC-0062 | Properties 显示 id/type/periods/source_ids/relations 等；字段可读、无 YAML 报错 | — | **NOT_RUN** |
| 4 | Backlinks | 在 GAR-0077、MAT-0016、LOOK-0024 查看 Backlinks | 显示来源卡/LOOK/关系卡的反向链接；无空/错乱 | — | **NOT_RUN** |
| 5 | 局部图（Local Graph） | 对 GAR-0015/LOOK-0024 打开 Local Graph（深度 1–2） | 节点/边可读；design/关系不过度密集；无红色未解析节点 | — | **NOT_RUN** |
| 6 | 关系/证据可见性 | 打开 P5-E 深化卡（如 GAR-0077、GAR-0022、STR-0003） | 正文可见 MAT/STR Wikilink；medium/review 关系有标注；无“假 high” | — | **NOT_RUN** |
| 7 | 孤立/单点 | 用 Graph 或搜索检查 59 个 isolates（如 SRC-0002） | 单点可打开、有说明；不从界面强造关系 | — | **NOT_RUN** |
| 8 | 搜索/过滤 | 搜索 `GAR-0077`、`MAT-0016`、`design-only` | 能找到卡与关系说明；design 不显示为历史事实 | — | **NOT_RUN** |
| 9 | 坏链/未解析 | 检查 graph 红色节点/未解析链接（机器报告 1 unresolved wikilink / 5 typed_unresolved） | 无新增坏链；已知项有记录 | — | **NOT_RUN** |
| 10 | 性能/稳定性 | 打开 458 卡 vault，滚动/切换 5 个页面 | 无明显卡顿/崩溃；插件不报错 | — | **NOT_RUN** |
| 11 | 截图与签字 | 为 #1–#10 保存截图；两名验收人签字 | 截图齐全、签字 | — | **NOT_RUN** |

## 结论

- **11/11 项 NOT_RUN**；无 Obsidian 运行证据、无截图、无签字。
- 在人工完成前：**GUI/H1 = NOT_RUN/PENDING**，PUBLIC-READY 继续保持 BLOCKED（B1 未关闭）。
- 本清单不替代自动化测试；自动化结果见 P5E-FINAL §回归。
