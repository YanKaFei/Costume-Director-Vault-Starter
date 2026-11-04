# Obsidian 人工验收（UAT）—《麦克白》P3.5/P3.6 材料

> **状态：HUMAN_UAT_PENDING（等待人工执行）。**
> 本材料由 AI 在无 GUI 终端环境生成，**没有实际打开 Obsidian、没有截图、没有执行点击/搜索/Properties 检查**。任何“PASS”都必须由人工在 Obsidian 中实际操作后填写；在人工签核之前，一律视为未验证（NOT_TESTED）。

- 项目根：`/Users/coffee/Desktop/Costume-Director-Vault-Starter`
- 被测对象：
  - `11-验收/P3.5/Macbeth/LOOKS.md`（18 套，draft）
  - `11-验收/P3.6/导演审阅-麦克白18套.md`
  - `11-验收/P3.6/导演评分表.md`
  - 相关卡片：`01-服装单品/`、`02-结构细节/`、`03-材质纹样/`、`04-来源/`
- 环境事实：本会话无 Obsidian GUI、无浏览器自动化；仅能读取文件、运行 Python 脚本与 `curl`。因此 GUI 步骤全部为 **HUMAN_UAT_PENDING**，不虚构通过。

## 1. 人工执行前置条件

- [ ] macOS（或 Windows/Linux）已安装 Obsidian（记录版本：__________）
- [ ] 已用 Obsidian “Open folder as vault” 打开 `/Users/coffee/Desktop/Costume-Director-Vault-Starter`
- [ ] 未强制依赖第三方插件（Dataview/Templater 等）；本 Vault 的标准属性应在无插件下可读
- [ ] 有权限截图（用于每一步的证据）

## 2. 逐步验收清单

> 状态填写规则：`PASS`（有截图/记录）、`FAIL`（有问题 + 截图）、`BLOCKED`（环境原因）、`NOT_TESTED`（未做）。**AI 不得代填 PASS。**

| # | 操作 | 预期结果 | 状态 | 人工证据（截图路径/说明） |
|---|---|---|---|---|
| 1 | Obsidian 打开 Vault | 左侧文件树显示 `00-系统` … `11-验收`；无“无法读取 vault”错误 | HUMAN_UAT_PENDING |  |
| 2 | 打开 `11-验收/P3.5/Macbeth/LOOKS.md` | 18 个二级标题（M1-A…L3-C）正常渲染；表格/代码块/反引号正常 | HUMAN_UAT_PENDING |  |
| 3 | 打开 `11-验收/P3.6/导演审阅-麦克白18套.md` | 总览表 18 行、6 个阶段分组、每套含关键单品/颜色/叙事/连续性/风险/提示词摘要/证据 | HUMAN_UAT_PENDING |  |
| 4 | 打开 `11-验收/P3.6/导演评分表.md` | 18 行 ×7 维均显示 `NOT_SCORED`；评审信息/签名栏可见 | HUMAN_UAT_PENDING |  |
| 5 | wikilink：在 LOOKS/审阅文档中点击 `GAR-0075`、`MAT-0011`、`STR-0006`、`SCN-0005` 等 | 跳转到对应卡片；无“Unresolved link”（红色/虚线） | HUMAN_UAT_PENDING |  |
| 6 | 反向链接（Backlinks）：打开 `GAR-0075-束腰长袍` | Backlinks 面板能看到 LOOKS/审阅/评分等引用它的笔记 | HUMAN_UAT_PENDING |  |
| 7 | Properties（属性）面板：打开 LOOKS 或任一卡 | 显示扁平 YAML：id/type/name_zh/name_en/look_items/continuity_lock 等；无嵌套对象报错；`source_ids`/`look_items` 为列表 | HUMAN_UAT_PENDING |  |
| 8 | 搜索：`GAR-0075`、`LOOK-0010`、`tag:#costume`、`麦克白` | 能命中对应卡片/笔记；结果数量合理，无“索引失败” | HUMAN_UAT_PENDING |  |
| 9 | 外链：点击 `https://collections.vam.ac.uk/...` / `https://www.gutenberg.org/...` 等来源链接 | 系统浏览器打开对应页面；Vault 内不要求、也不应内嵌版权不明图片 | HUMAN_UAT_PENDING |  |
| 10 | 图片/附件核查 | Vault 内无本地侵权图片；图片仅以原始 URL 出现（`license_status: link_only` 等） | HUMAN_UAT_PENDING |  |
| 11 | 图谱视图（可选） | `LOOKS`/`GAR`/`SRC` 节点连通，无孤立关键卡（可截图） | HUMAN_UAT_PENDING |  |
| 12 | 目录/索引一致性 | `00-系统/索引.md` 的计数/目录与实际文件不矛盾（记录差异） | HUMAN_UAT_PENDING |  |

## 3. 已在终端完成的机器检查（可复核，不替代 GUI UAT）

以下为 AI 在终端实际执行过的检查；只能证明文件层/脚本层，不证明 Obsidian 渲染：

| 检查 | 结果 | 复核方式 |
|---|---|---|
| 全库 `scripts/validate.py` | **PASS**（363 cards，0 errors；frontmatter/YAML/枚举/链接/source_ids 全部通过） | `python3 scripts/validate.py` |
| LOOKS 18 套齐全 | 18 个 `##` 标题（M1-A…L3-C），md5 `53549992cef442d2d3267a4506b3903b` | `grep -c '^## ' LOOKS.md` |
| 卡片 ID 真实性 | LOOKS 引用的 17 个 GAR/STR/MAT 均在 01–03 存在；GAR-0079 为 interpretive | `grep`/`validate.py` |
| 来源 URL 可达 | Macbeth 用例的 V&A/Met/SRC 均由来源卡记录 HTTP 200（本次未逐条重跑全部 URL） | 见 `04-来源/` 与 `EVIDENCE.md` |
| 无本地内嵌图片 | validate.py 第 14 项通过 | `python3 scripts/validate.py` |
| 未执行 GUI | 本会话无 Obsidian 进程/无截图 | 环境事实，见文首 |

## 4. 人工签核

| 项 | 内容 |
|---|---|
| 验收人姓名 | ______________________ |
| 角色（导演/制片/技术） | ______________________ |
| Obsidian 版本 / OS | ______________________ |
| 执行日期 | ______________________ |
| 总结果 | [ ] PASS（12 步均 PASS） [ ] PARTIAL（有 FAIL/BLOCKED，见下） [ ] FAIL |
| 失败/阻塞明细（步骤号 + 现象 + 截图） |  |
| 签名 | ______________________ |

> 判定规则：仅当第 1–10 步全部有人工证据（截图/录屏）且无 FAIL 时，才能填 PASS；任一步未做即 `PARTIAL`/`NOT_TESTED`。AI 生成的本文件不构成验收结论。

## 5. 失败处理

- 若出现 YAML/Properties 解析错误：记录文件名与报错截图，停止 UAT，回到 `00-系统/数据字典.md` 检查字段。
- 若出现坏链：记录 `[[目标]]`、所在文件、期望目标；运行 `python3 scripts/validate.py` 复核是否脚本层也报错。
- 若搜索/索引异常：记录搜索词、Obsidian 版本、vault 大小；必要时重启 Obsidian 后复测。
- 任何修复都应重新执行本清单；不得只修一处就宣布 PASS。
