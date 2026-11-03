# 运行状态（STATUS）— Costume Director Knowledge System

- 更新时间：2026-11-04 01:45（Asia/Shanghai）
- 更新人：`verifier`（task-6 独立验收；未修改卡片/`00-系统/`/他人工件）
- 快照：235 张卡（内容卡 93 + 来源卡 142）；最新写入卡 `SCN-0004` @ 01:37:20；字典 v1.1 @ 01:38:14；验收 SUMMARY @ 01:38:16
- 总体状态：**P0/P1/P2 完成，P3 部分完成；结构验收 PASS、证据链 PARTIAL、GUI NOT_TESTED**

## 1. 阶段与完成度

| 阶段 | 状态 | 证据 |
|---|---|---|
| P0 架构 | **DONE** | 数据字典 v1.1、卡片模板、索引、来源规范、`reports/SOURCES.csv`（142 行）、`scripts/validate.py`/`query.py`/`recommend.py`、初始测试 |
| P1 种子知识库 | **DONE（数量）** | 单品 36、结构 11、材质/纹样 10、风格 11、时代地域 11、Look 10、场景 4、来源 142 |
| P2 决策闭环 | **DONE（有已知缺陷）** | 3 套推荐 A/B/C + 评分 + prompt + 风险 + 证据；3 个提示词模板 + SKILL.md；**18/18 测试 PASS，exit 0**；query.py 引号多词检索缺陷未修 |
| P3 扩充与集成 | **PARTIAL** | 235/250 总卡；`carried_prop` 0、结构 10 族系空、59 张来源未引用、37 张 draft 待人工复核 |

## 2. 当前可用的东西（用户可直接打开/执行）

1. **知识库**：`00-系统/索引.md` 为导航入口；按 `GAR-/STR-/MAT-/STY-/PRD-/LOOK-/SCN-/SRC-` 前缀检索。235 张卡全部带合法 YAML frontmatter；609 条 `[[wikilink]]` 目标存在（0 坏链）。
2. **来源登记**：`reports/SOURCES.csv`（142 行，8 列：`source_id,title,publisher,url,accessed_at,source_kind,rights_statement,note`），与 `04-来源/*.md` 单源生成、字段一致。
3. **检索/推荐**（Python 3.9 标准库 + PyYAML，无需联网/安装）：
   ```bash
   cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
   python3 scripts/query.py "旗袍" --limit 5
   python3 scripts/query.py 1930s 上海 --type garment --json      # 多词请分开传参
   python3 scripts/recommend.py 11-验收/测试输入/T01-1930s上海知识分子-历史准确.json --json
   python3 scripts/run_acceptance.py                              # 18 例验收，exit 0
   python3 scripts/validate.py                                    # 结构校验（当前 exit 1，见 §3.1）
   python3 scripts/build_sources.py --check                       # SOURCES.csv 对账
   ```
4. **提示词模板**：`10-提示词模板/01-角色设计模板.md`、`02-静态生图提示词模板.md`、`03-视频提示词模板.md`。
5. **验收材料**：`11-验收/测试场景.md`、`11-验收/测试输入/T01..T18.json`、`11-验收/测试结果/T01..T18.md` + `raw/` + `SUMMARY.md`（18/18 PASS）。
6. **证据抽查记录**：`reports/EVIDENCE-SPOTCHECK.csv`（14 张卡、19 个卡-来源对、21 个 URL 实测 200 的原文引用）。
7. **AI 调用指南**：`skills/costume-director/SKILL.md`。

## 3. 已知限制与未完成项

### 3.1 结构/数据
- `scripts/validate.py` 当前 **exit 1**：49 张 researcher 来源卡（`SRC-0001..0060` 中的 49 张）`source_kind` 使用字典外扩展标签（`controlled_vocabulary` 等 10 种）。需字典扩枚举或卡片归一化（QA §1.3）。
- 3 处列表值未加引号（`STR-0004`/`STR-0008` `construction_era`、`MAT-0010` `periods`）被解析为 int，违反 list[string]（警告级）。
- `00-系统/卡片模板.md`（01:26）未同步字典 v1.1（01:38）：来源卡仍按 v1.0 的强制字段/8 节模板书写。
- 59/142 来源卡未被任何内容卡引用，**全部 19 张 Getty AAT 卡均未被引用**；researcher 来源包与内容卡证据链未打通。
- 3 组重复 URL：`SRC-0115/SRC-0157`、`SRC-0036/SRC-0175`、`SRC-0022/SRC-0163`（后两组各一张未被引用，可退休合并）。
- `SRC-0204` 来源卡已改名（1930→1940 年代），git 中为「旧名 deleted + 新名 untracked」，待 lead 版本收口。

### 3.2 检索/推荐
- **`query.py` 引号多词查询恒 0 命中**（`query.py "1930s 上海"` → 0；`query.py 1930s 上海` → 5）。docstring 示例 `query.py "立领 shirt"` 不可用。18 例验收的 query 子命令全部 0 命中（验收仅校验退出码），检索证据为空；recommend.py 内部检索不受影响。
- 推荐算法仅验证可运行/结构完整/ID 真实/退出码 0，未做评分权重调参评估。

### 3.3 内容覆盖
- P3 250+ 未达：总卡 235（差 15）；内容卡仅 93。
- `carried_prop`（包袋/伞/手杖）0 张；结构 16 族系中 10 族为 0；材质仅 4/8 族、纹样仅 1/11 族。
- Look 完整拆解口径未定：严格五槽 0/10、四槽 5/10（目标「至少 6 套」未达）；宽松口径 10/10 可拆解。
- 37 张卡 `review_status: draft`（全部 PRD/STY/LOOK/SCN 与 example 卡），未经人工复核。

### 3.4 未测试（NOT_TESTED）
- **Obsidian GUI 打开/跳转未测试**（本环境无 GUI；仅结构层验证）。
- 逐图版权授权未核验（策略为不下载、不内嵌；Vault 内 0 图片文件）。
- 史学方法学/叙事正确性未审（只验证「来源页是否支撑卡片断言」）。
- 网络稳定性：抽查时 21 URL 全 200；Met 人类可读页有过 429 限流（来源卡已注明以 API 为核验对象）。

## 4. 本轮实际执行（命令与退出码）

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python3 scripts/validate.py` | 1 | 235 卡；错误级 49（全为 source_kind 枚举）；警告 3 |
| `python3 scripts/build_sources.py --check` | 1 → 重建后 0 | 重建前缺 82 行；`--write` 后 142/142 一致，3 组重复 URL 警告 |
| `python3 scripts/query.py "旗袍" --limit 3` | 0 | 3 命中（GAR-0031/0032、LOOK-0009） |
| `python3 scripts/query.py --type garment --category footwear --json` | 0 | 4 命中 |
| `python3 scripts/query.py "1930s 上海" …` | 0 | 0 命中（缺陷，见 §3.2） |
| `python3 scripts/recommend.py T01/T03/T05 --json` | 0 | 3 套 Look / continuity 3 场 / fictional 3 套；0 未知 ID |
| `python3 scripts/run_acceptance.py` | **0** | **PASS 18/18，FAIL 0/18**，23.16s；SUMMARY 与逐例文件一致；快照不陈旧 |
| curl 证据抽查（21 URL） | 0 | 21/21 HTTP 200；19 对中 18 PASS / 1 PARTIAL（GAR-0034） |

## 5. 下一轮最有价值的行动（按优先级）

1. **修 `query.py` 多词 split** + 验收增加 query 命中断言，然后重跑 18 例（影响检索可用性与验收证据真实性）。
2. **统一 `source_kind`**（字典 v1.2 扩枚举或归一化 49 张卡）；同步 `00-系统/卡片模板.md` 到 v1.1；修正 3 处数字加引号。
3. **打通来源链**：把 19 张 AAT 与高价值未引用来源接入内容卡，或显式标注「保留备用」；合并 3 组重复 URL。
4. **补内容缺口**：carried_prop（包袋/伞/手杖）、结构族系（领口/肩线/口袋/腰线/褶裥/缝线/长度）、材质族系（leather/fur/metal/finish）与纹样族系。
5. **明确 Look「完整拆解」验收口径**，补齐 5 张低槽位 Look 的鞋/配饰/外层条目。
6. **人工复核 37 张 draft 卡** 后更新 `review_status`；在有 GUI 的环境中完成 Obsidian 打开与 wikilink 跳转实测。
7. **版本收口**：lead 提交 2 个新脚本、6 张新增卡、SRC-0204 改名与 4 份 reports（本轮不执行 git 操作）。

## 6. 状态标签

- 结构/数据一致性：**PASS**（除 49 张来源卡枚举；0 YAML 错、0 重复 ID、0 坏链、0 内嵌图片）
- 证据链：**PARTIAL**（14 卡抽查 13 PASS/1 PARTIAL；59 张来源未引用；逐图授权未测）
- P2 决策闭环：**PASS（有 query 缺陷）**
- P3 覆盖：**PARTIAL**
- Obsidian GUI：**NOT_TESTED**
