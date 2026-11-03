# 运行状态（STATUS）— Costume Director Knowledge System

- 更新时间：2026-11-04 01:52（Asia/Shanghai，修复后复验轮）
- 更新人：`verifier`（task-6 首验 + task-7 复验；未修改卡片、`00-系统/`、他人工件）
- 快照：**235 张卡**（内容卡 93 + 来源卡 142）；最新卡片写入 @ 01:47:05 / 模板 @ 01:47:15；本 worker 独立重跑验收 SUMMARY @ 01:49:29；复验期间无卡片再变更
- 总体状态：**P0/P1/P2 完成；P3 部分完成；结构校验 0 错误 0 警告 PASS；证据抽查 19/19 PASS；Obsidian GUI NOT_TESTED**

## 1. 阶段与完成度

| 阶段 | 状态 | 证据 |
|---|---|---|
| P0 架构 | **DONE** | 数据字典 v1.1、卡片模板（已同步 v1.1）、索引、来源规范、`reports/SOURCES.csv`（142 行）、`scripts/validate.py`/`query.py`/`recommend.py`、初始测试 |
| P1 种子知识库 | **DONE（数量）** | 单品 36、结构 11、材质/纹样 10、风格 11、时代地域 11、Look 10、场景 4、来源 142 |
| P2 决策闭环 | **DONE** | 3 套推荐 A/B/C + 评分 + prompt + 风险 + 证据；3 个提示词模板 + SKILL.md；query 多词检索已修；**18/18 测试 PASS，exit 0，query 逐例 ≥1 命中（合计 53）** |
| P3 扩充与集成 | **PARTIAL** | 235/250 总卡；`carried_prop` 0、结构 10 族系空、60 张来源未被引用、37 张 draft 待人工复核 |

## 2. 当前可用的东西（用户可直接打开/执行）

1. **知识库**：`00-系统/索引.md` 为导航入口；按 `GAR-/STR-/MAT-/STY-/PRD-/LOOK-/SCN-/SRC-` 前缀检索。235 张卡全部带合法 YAML frontmatter；609 条 `[[wikilink]]` 目标存在（0 坏链）；0 内嵌图片。
2. **来源登记**：`reports/SOURCES.csv`（142 行，8 列：`source_id,title,publisher,url,accessed_at,source_kind,rights_statement,note`），与 `04-来源/*.md` 单源生成、字段一致（142/142）。
3. **检索/推荐**（Python 3.9 标准库 + PyYAML，无需联网/安装）：
   ```bash
   cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
   python3 scripts/validate.py                                    # exit 0：17/17 PASS，0 错误 0 警告
   python3 scripts/build_sources.py --check                       # exit 0：142/142 一致
   python3 scripts/query.py "旗袍" --limit 5
   python3 scripts/query.py "1930s 上海" --type garment --json     # 多词 AND，5 命中
   python3 scripts/query.py --phrase "1930s 上海" --json           # 精确短语
   python3 scripts/recommend.py 11-验收/测试输入/T01-1930s上海知识分子-历史准确.json --json
   python3 scripts/run_acceptance.py                              # 18 例验收，exit 0，query 命中逐例 ≥1
   ```
4. **提示词模板**：`10-提示词模板/01-角色设计模板.md`、`02-静态生图提示词模板.md`、`03-视频提示词模板.md`。
5. **验收材料**：`11-验收/测试场景.md`、`11-验收/测试输入/T01..T18.json`、`11-验收/测试结果/T01..T18.md` + `raw/` + `SUMMARY.md`（18/18 PASS，query 命中合计 53、逐例 ≥1）。
6. **证据抽查记录**：`reports/EVIDENCE-SPOTCHECK.csv`（14 张卡、19 个卡-来源对，19/19 PASS；含 GAR-0034 修复复核记录）。
7. **AI 调用指南**：`skills/costume-director/SKILL.md`。

## 3. 已知限制与未完成项

### 3.1 已修复（本轮关闭）
- ✅ 49 张 researcher 来源卡 `source_kind` 越界 → 已归一化，枚举 235/235 合法。
- ✅ `query.py` 引号多词恒 0 命中 → 已按空白拆分 AND 词、新增 `--phrase`；验收新增 `query_hits ≥1` 断言，18/18 PASS。
- ✅ GAR-0034 「FIT 支撑传统 waistcoat/vest 减少」无依据从属断言 → 已删去，`source_ids` 改为 `[SRC-0203]`，叙事标 interpretive。
- ✅ 3 处列表数字未加引号（`STR-0004`/`STR-0008`/`MAT-0010`）→ 已加引号，警告清零。
- ✅ `00-系统/卡片模板.md` 未同步字典 v1.1 → 已同步（来源卡豁免与双正文写法）。
- ✅ `SRC-0157` 重复未标注 → 已标 canonical=SRC-0115，`PRD-0007` 改用 `SRC-0115`；`SRC-0163`/`SRC-0175` 亦标 canonical。

### 3.2 仍存在
- **60/142 来源卡未被任何内容卡引用**（42.3%），含**全部 19 张 Getty AAT 卡**；researcher 来源包与内容卡证据链未打通。
- **P3 250+ 未达**：总卡 235（差 15）；内容卡 93（按此口径差 157）。
- **分类缺口**：`carried_prop`（包袋/伞/手杖）0 张；结构 16 族系中 10 族为 0；材质仅 4/8 族、纹样仅 1/11 族。
- **Look 完整拆解口径未定**：严格五槽 0/10、四槽 5/10（「至少 6 套完整拆解」需 lead 裁定）。
- **37 张卡 `review_status: draft`**（全部 PRD/STY/LOOK/SCN 与 example 卡），未经人工复核。
- 3 组重复 URL 保留为交叉引用（已标 canonical）；是否物理合并由 lead 决定。
- `00-系统/来源规范.md` 仍为启动模板（2026-11-03），未记录 SRC-0200..0299 段位。
- `SRC-0204` 来源卡改名（1930→1940 年代）在 git 中为「旧名 deleted + 新名 untracked」，待 lead 版本收口。

### 3.3 未测试（NOT_TESTED）
- **Obsidian GUI 打开/跳转未测试**（本环境无 GUI；仅结构层验证 YAML/Markdown/wikilink）。
- 逐图版权授权未核验（策略为不下载、不内嵌；Vault 内 0 图片文件）。
- 史学方法学/叙事正确性未审（只验证「来源页是否支撑卡片断言」）。
- 推荐评分权重合理性未做调参评估（仅验证可运行、结构完整、ID 真实、退出码 0）。
- 网络稳定性：抽查 21 URL 全 200；Met 人类可读页有过 429 限流（来源卡已注明以 API 为核验对象）。

## 4. 本轮实际执行（命令与退出码）

| 命令 | 退出码 | 结果 |
|---|---|---|
| `python3 scripts/validate.py` | **0** | 235 卡；17/17 检查项 PASS；**0 错误级失败、0 警告** |
| `python3 scripts/build_sources.py --write` / `--check` | 0 / 0 | 从 142 张来源卡重建 CSV；142/142 一致；3 组重复 URL 已标 canonical |
| `python3 scripts/query.py "1930s 上海" --type garment --json` | 0 | 5 命中（修复前 0） |
| `python3 scripts/query.py "立领 shirt" --json` | 0 | 7 命中（修复前 0） |
| `python3 scripts/query.py --phrase "1930s 上海" --json` | 0 | 1 命中 |
| `python3 scripts/recommend.py T01/T03/T05 --json` | 0 | 3 套 / continuity 3 场 / fictional 3 套；0 未知 ID |
| `python3 scripts/run_acceptance.py` | **0** | **PASS 18/18，FAIL 0/18**，21.56s；query 命中合计 53、逐例最小 1；SUMMARY 与 engineer 末次仅运行时间不同 |
| curl 证据抽查 / 修复复测 | 0 | 首轮 21 URL + 修复复测 4 URL 均 HTTP 200；19/19 对 PASS |

## 5. 下一轮最有价值的行动（按优先级）

1. **打通来源链**：把 19 张 AAT 与高价值未被引用来源（60 张）接入内容卡，或显式标注「保留备用」。
2. **补内容缺口**：carried_prop（包袋/伞/手杖）、结构族系（领口/肩线/口袋/腰线/褶裥/缝线/长度）、材质族系（leather/fur/metal/finish）与纹样族系。
3. **明确 Look「完整拆解」验收口径**，补齐 5 张低槽位 Look 的鞋/配饰/外层条目。
4. **人工复核 37 张 draft 卡** 后更新 `review_status`；在有 GUI 的环境中完成 Obsidian 打开与 wikilink 跳转实测。
5. **更新 `00-系统/来源规范.md`**（SRC 段位 0200..0299）；决定 3 组重复 URL 是否物理合并。
6. **版本收口**：lead 提交 2 个新脚本、6 张新增卡、SRC-0204 改名与 4 份 reports（本轮不执行 git 操作）。

## 6. 状态标签

- 结构/数据一致性：**PASS**（validate exit 0；0 YAML 错、0 重复 ID、0 坏链、0 内嵌图片、0 枚举违规、0 类型警告）
- 证据链抽查：**PASS**（14 卡 / 19 对 / 21+4 URL 全 200；19/19 PASS）；来源覆盖 **PARTIAL**（60 张未引用）
- P2 决策闭环：**PASS**（18/18，query 逐例 ≥1）
- P3 覆盖：**PARTIAL**（235/250；分类缺口）
- Obsidian GUI：**NOT_TESTED**
