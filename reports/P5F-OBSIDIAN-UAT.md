# P5-F Obsidian GUI 人工验收手册（P5F-OBSIDIAN-UAT）

- 状态：**NOT_RUN / PENDING**（本环境无 Obsidian GUI；未打开 vault、无截图、无签字）
- 日期：2026-11-05；verifier / task-95；**本手册不得当作 PASS**
- Vault 路径：`/Users/coffee/Desktop/Costume-Director-Vault-Starter`（建议复制一份再测；不要直接改生产 vault）
- 先决条件：备份（`python3 scripts/backup_restore.py backup`）；记录 Obsidian 版本、操作人、日期、vault 路径
- 证据目录：`11-验收/P5F/uat-screenshots/`（人工创建；每项截图文件名见各条）
- 签核文件：`11-验收/P5F/UAT-SIGNOFF.md`（两名验收人签字、日期、Obsidian 版本、结论 PASS/FAIL）
- 通过/失败标准：满足“预期”且截图/签核齐全 = PASS；否则 FAIL；环境缺失 = BLOCKED；全部完成后才能把 GUI 从 NOT_RUN 改为 PASS。

## 自动化预检（已 PASS，仅作前提）

- 458 卡 = 224 内容 + 234 来源；validate 458/458；build 234；consistency 0/334。
- MOC 已补齐：**224/224 内容 + 234/234 来源**（lead 更新，544 链接/0 未解析）；第 2 项预期 **PASS**（仍需人工执行确认）。

## 11 项可操作验收

### 1. Vault 入口与根导航

- 打开：Obsidian → Open folder as vault → 上述路径。
- 检查文件：`README.md`、`00-系统/MOC/README.md`、`00-系统/索引.md`。
- 步骤：打开 README；点击任意入口链接；确认不出现 “file not found”。
- 预期：vault 正常打开；README/索引可读；无解析错误弹窗。
- 失败标准：vault 打不开、YAML 报错、入口链接失效。
- 截图：`01-vault-root.png`（根目录 + README 打开）。
- 结果：**NOT_RUN**

### 2. MOC 导航（9 页）

- 路径：`00-系统/MOC/`：README、时代地域、服装单品、材质纹样、来源证据、结构细节、造型组合、鞋履配饰、风格体系。
- 步骤：逐页打开；点击 3–5 个分类/卡片链接；检查来源证据页是否列 SRC。
- 预期：9 页无 frontmatter（Properties 为空）；链接可跳转；**内容覆盖 224、来源覆盖 234**（当前独立复算 224/224、234/234、544 链接/0 未解析）。
- 失败标准：MOC 页打不开/链接失效/缺新卡（LOOK-0024..0035、STY-0011..0015、GAR-0088..0091、STR-0027..0035、MAT-0015..0019、SRC-0530..0552）。
- 截图：`02-moc-<page>.png`（至少 3 页）。
- 结果：**NOT_RUN**

### 3. Properties（frontmatter 面板）

- 打开卡：`GAR-0077`（紧身长袜）、`GAR-0022`（威灵顿靴）、`STR-0003`（拉夫领）、`LOOK-0024`（Macbeth 野心）、`SRC-0062`（Textiles and Clothing）、`MAT-0017`（皮革）。
- 预期 Properties：
  - 内容卡：`id/type/name_zh/periods/regions/source_ids/relations/evidence_status/review_status`；GAR-0077 另有 materials/silhouette；LOOK-0024 有 `outfit_slots/evidence_type/constraints_checked/approved_anchors/context/character_function/continuity_state`。
  - SRC-0062：`id/type/source_kind/url/license_status/date_accessed/http_status`（按来源规范）。
  - 无 YAML 解析错误/红色报错。
- 失败标准：Properties 空白、字段缺失、YAML 报错。
- 截图：`03-properties-GAR-0077.png`、`03-properties-LOOK-0024.png`、`03-properties-SRC-0062.png`。
- 结果：**NOT_RUN**

### 4. Backlinks（反向链接）

- 打开：`GAR-0077`、`MAT-0016`（亚麻织物）、`LOOK-0024`；查看右侧 Backlinks。
- 预期：GAR-0077 显示来自 LOOK/来源卡的反链；MAT-0016 显示来自 GAR/STR 的关系与来源；LOOK-0024 显示 STY/来源反向；无“无反向链接”异常（除真实单点）。
- 失败标准：Backlinks 为空/错乱/指向不存在文件。
- 截图：`04-backlinks-GAR-0077.png`、`04-backlinks-MAT-0016.png`。
- 结果：**NOT_RUN**

### 5. 局部图（Local Graph）

- 打开 `GAR-0015`（法式长袍）与 `LOOK-0024`，Local Graph 深度 1–2。
- 预期：节点/边可读；无红色未解析节点；关系密度可接受；设计关系可见但不冒充历史事实。
- 失败标准：红色未解析节点、图空白、频繁卡死。
- 截图：`05-local-graph-GAR-0015.png`、`05-local-graph-LOOK-0024.png`。
- 结果：**NOT_RUN**

### 6. 关系/证据可见性与诚实性

- 打开 P5-E 深化卡：`GAR-0077`（uses_material→MAT-0016，medium/review）、`GAR-0001`（may_have_part→STR-0003，review）、`STY-0001`（风格解释，design-only）、`GAR-0045`（medium SRC-0405 例外）。
- 预期：正文有对应 `[[MAT-0016-…]]`/`[[STR-0003-…]]` 可见链接；medium/review 有文字标注；STY 说明“设计解释不是史实”；无“假 high/假历史事实”。
- 失败标准：关系到来源/材料不可见、design 被写成史实、无 review 标记。
- 截图：`06-relation-GAR-0077.png`、`06-relation-STY-0001.png`。
- 结果：**NOT_RUN**

### 7. 孤立/单点节点

- 打开：`SRC-0002`（Fashionpedia 词典，legit_reference）、`SRC-0063`（背景书，navigation_only）、`SRC-0163`（未分类/重复 URL 候选）。
- 预期：卡片可打开、有说明；从 MOC/来源页可到达；不要求强造语义关系；记录是否应在 MOC 标注用途。
- 失败标准：孤立卡无说明/无法打开/被误当强证据。
- 截图：`07-isolate-SRC-0002.png`、`07-isolate-SRC-0063.png`。
- 结果：**NOT_RUN**

### 8. 搜索/过滤

- 搜索：`GAR-0077`、`MAT-0016`、`STY-0001`、`style_interpretation`、`design-only`。
- 预期：命中卡与关系说明；能区分事实/设计；无重复结果异常。
- 失败标准：搜索结果为空/错乱、design 被标为历史事实。
- 截图：`08-search-GAR-0077.png`、`08-search-style_interpretation.png`。
- 结果：**NOT_RUN**

### 9. 坏链/未解析

- 检查：Local Graph 红色节点；Backlinks 中 “Unlinked mentions”；已知 graph 工具误报（1 code 示例 + 5 GAR-EXAMPLE-001 正则）应在 task-93 修复。
- 预期：**真实未解析 = 0**；已知示例/误报不作为坏链；若有真实坏链记录 ID。
- 失败标准：存在真实 `[[...]]` 无法跳转。
- 截图：`09-unresolved-check.png`。
- 结果：**NOT_RUN**

### 10. 性能/稳定性

- 打开 vault，快速切换 5 个不同页面 + 全局搜索 3 次；观察卡顿/崩溃/插件报错。
- 预期：无明显卡死/崩溃；可接受的手感（不设硬性 FPS 指标，定性记录）。
- 失败标准：崩溃/长时间无响应/插件错误阻断。
- 截图：`10-performance.png`。
- 结果：**NOT_RUN**

### 11. 截图归档与两人签核

- 按 §1–§10 保存截图至 `11-验收/P5F/uat-screenshots/`；在 `11-验收/P5F/UAT-SIGNOFF.md` 记录：日期、Obsidian 版本、vault 路径、逐项 PASS/FAIL、截图文件名、操作人 A/B 签名。
- 预期：11/11 项有结论且截图齐全；两人签字。
- 失败标准：缺截图/缺签字/结论与截图不一致。
- 截图：目录一览 `11-signoff-index.png`。
- 结果：**NOT_RUN**

## 状态汇总

| # | 项 | 状态 |
|---|---|---|
| 1 | Vault 入口 | NOT_RUN |
| 2 | MOC 9 页 | NOT_RUN（MOC 已补齐 224/234，预期 PASS；待人工执行） |
| 3 | Properties | NOT_RUN |
| 4 | Backlinks | NOT_RUN |
| 5 | Local Graph | NOT_RUN |
| 6 | 关系/证据诚实 | NOT_RUN |
| 7 | 孤立节点 | NOT_RUN |
| 8 | 搜索/过滤 | NOT_RUN |
| 9 | 坏链/未解析 | NOT_RUN |
| 10 | 性能/稳定 | NOT_RUN |
| 11 | 截图/签核 | NOT_RUN |

**GUI 总体：NOT_RUN / HUMAN_UAT_PENDING；在 11/11 PASS + 两人签字前不得声称 GUI 通过。**
