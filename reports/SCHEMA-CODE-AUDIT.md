# SCHEMA / CODE AUDIT — P4 v1.2 扩展、校验器、脚本与技能文档（R1）

- 审计性质：**只读支持任务**（未修改任何卡片、脚本、索引或技能文件；仅新增本报告）
- 审计时间：2026-11-04 17:12–17:4x（Asia/Shanghai）
- 快照：**399 卡（内容 188 + 来源 211）**；HEAD `56f4225`；工作区仅 `.obsidian/` untracked
- 环境：macOS，Python 3.9.6 + PyYAML 6.0.3；无 Obsidian GUI；所有结论基于实际命令输出，不采信报告自述
- 审计对象：`00-系统/数据字典.md`、`00-系统/数据字典-v1.2-扩展.md`、`00-系统/索引.md`、`00-系统/卡片模板.md`、`scripts/{validate,query,recommend,workflow,outfit,books_extract}.py`、`skills/costume-director/SKILL.md`、`.dsh/skills/costume-director/SKILL.md`、`docs/{SKILL-USAGE,WORKFLOW,OUTFIT-COMPOSER}.md`、`reports/{STATUS,COVERAGE,QA,P4-REPORT,P4-COVERAGE}.md`

## 0. 结论摘要

| 域 | 结论 | 关键证据 |
|---|---|---|
| 旧/新 Schema 兼容 | **PASS** | `validate.py` 399/399 PASS，0 错误 0 警告；旧卡 0 张含 v1.2 可选字段；P4 提交对 01–09 卡片 0 个 `M` |
| 卡片/来源/索引计数 | **PARTIAL** | 实际 399（188 内容 + 211 来源），P4 报告/COVERAGE 一致；索引 01–03 计数正确但状态/目录元数据过期；STATUS/COVERAGE/QA 顶部仍是 P3.3 343 快照 |
| v1.2 字段实际使用/联动 | **PARTIAL** | 36/42 字段被使用（21 张卡，非报告所称 22 张）；6 字段未用；`query/recommend/outfit/workflow` **不读取**这些字段；`validate.py` 不校验其枚举 |
| CLI/路径死链 | **PASS（无死链）** | 技能引用的 `scripts/*.py`、`tests/*`、`11-验收/*`、`docs/*` 均存在；query/recommend/workflow 文档化参数实测可用、退出码符合文档 |
| 技能文档一致性 | **FAIL（文档层）** | 两份 SKILL.md 内容分叉（264 行 vs 387 行）；DSH 只加载 `.dsh/...`；项目 `skills/...` 仍写“P2 正式版 / 30 例”，且缺 `workflow.py`；两份都未覆盖 `outfit.py`、v1.2、books_extract |
| P4 结构 vs P3.6 skill workflow | **PARTIAL** | 旧脚本 0 行变更（无破坏）；但 P3.6 workflow skill 未纳入 P4 outfit composer / v1.2 字段 / books 工具；新能力不可被发现 |

**总体判定**：`PRIVATE-USE` 技术兼容性 **PASS**（校验器与旧 CLI 未被 P4 结构扩展破坏）；文档/索引/技能集成存在 **2 HIGH + 4 MEDIUM + 4 LOW** 缺口，需在 P5 修复后才适合作为对外使用说明。

## 1. Findings（ID / 严重度 / 证据 / 复现 / 修复 / 验收 / 状态）

### SCHEMA-01 [HIGH] 两份 SKILL.md 分叉，存在两个“事实来源”
- **证据**
  - `skills/costume-director/SKILL.md` = **387 行**，无 YAML frontmatter，标题「P2 正式版」；`.dsh/skills/costume-director/SKILL.md` = **264 行**，有 `name/description/whenToUse` frontmatter。
  - `docs/SKILL-USAGE.md:6,19,149` 明确 DSH 加载 `<vault>/.dsh/skills/costume-director/SKILL.md`；`reports/P3.6-REPORT.md:12,24` 同。
  - 两份 diff 非空：项目版有 `query.py`/`recommend.py` 用法与质量章节，缺 `scripts/workflow.py`（grep 0 命中）；native 版有 workflow 全流程，缺项目版的部分背景章节。
- **复现**：`wc -l skills/costume-director/SKILL.md .dsh/skills/costume-director/SKILL.md; diff -q ...`
- **修复**：确定 `.dsh` 为唯一 canonical；`skills/` 改为短指针（指向 `.dsh` 与 docs）或删除重复正文；在两份的 CI/QA 中比对关键命令清单。
- **验收**：仓库仅一份完整技能正文；`grep -c 'workflow.py|outfit.py'` 在两处一致；skills/ 文件首行含“canonical = .dsh/...”。
- **状态**：OPEN（只读审计未改）

### SCHEMA-02 [HIGH] P4 新能力未进入技能/入口文档（P3.6 workflow skill 与 P4 结构不兼容）
- **证据**
  - `.dsh/skills/costume-director/SKILL.md` 的脚本引用仅有 `scripts/query.py`、`scripts/recommend.py`、`scripts/workflow.py`；`outfit`/`v1.2`/`books_extract`/`OUTFIT-COMPOSER` 均 **0 命中**（仅 frontmatter 的 “outfits” 一词）。
  - `skills/costume-director/SKILL.md` 同样未提 `outfit.py`、v1.2；`grep -c 'workflow.py'` = **0**。
  - 但 P4 已交付 `scripts/outfit.py`（CLI 可用，`--help` exit 0）、`docs/OUTFIT-COMPOSER.md`、`scripts/books_extract.py`、22 张 v1.2 新卡；`docs/OUTFIT-COMPOSER.md` 未被任何 skill/索引链接（index grep 0）。
- **复现**：`grep -nE 'outfit|v1\.2|books_extract|OUTFIT-COMPOSER' .dsh/skills/costume-director/SKILL.md skills/costume-director/SKILL.md 00-系统/索引.md`
- **修复**：native skill 增加 “§3.4 P4 composer / v1.2 fields / books” 入口与示例；skill 末尾链接 `docs/OUTFIT-COMPOSER.md`、`docs/WORKFLOW.md`；索引增加 P4 文档入口。
- **验收**：skill 内可检索到 outfit.py 与 v1.2 字段说明；按 skill 命令跑 composer 一次 exit 0；索引链接 docs 可达。
- **状态**：OPEN

### SCHEMA-03 [MEDIUM] v1.2 可选字段未接入检索/推荐/校验（“used”仅限存储）
- **证据**
  - `query.py` 的 `build_haystacks()` 只索引 v1.1 字段（id/type/name/category/aliases/periods/regions/style_tags/colors/materials/source_ids/tags/season/formality/silhouette/fit/prompt_en/movement_notes/lighting_notes/note + body；见 `scripts/query.py:82-96`），**不含任何 v1.2 可选字段**；CLI 无 `--collar-shape` 等过滤。
  - `grep -nE 'collar_shape|sleeve_set|hem_type|closure_types|weave_type|heel_type|hat_brim_class' scripts/query.py scripts/recommend.py scripts/outfit.py scripts/workflow.py` → **0 命中**；`waistline` 仅作为 recommend/outfit 的 NLP 关键词（非字段读取）。
  - `validate.py` 无 v1.2 可选字段枚举校验（grep `collar_shape|v1.2|optional` 无命中）；即字段值写错不会被校验。
  - 实际使用：**36/42** 字段、**21** 张卡使用；6 字段从未使用：`belt_width_class` `buckle_type` `handle_type` `neckline_shape` `prop_closure` `stretch_class`。
- **复现**：见上 grep + `python3 scripts/query.py --id GAR-0084 --json`（JSON 契约无 v1.2 字段）。
- **修复**：二选一——(a) 明确 v1.2 为“存储/未来扩展”并在扩展文档写明不参与检索；或 (b) 在 query 加可选字段过滤与 haystack、recommend/outfit 读取关键字段；同时给 validate 增加可选值白名单。
- **验收**：文档明确消费范围；若 (b)，新增 `--collar-shape` 等测试、validate 对非法值报错；(a) 则无代码改动但文档消除误导。
- **状态**：OPEN

### SCHEMA-04 [MEDIUM] 索引（00-系统/索引.md）状态/元数据过期，缺 v1.2 入口
- **证据**
  - `索引.md:9`：`00-系统/` 标“4（P0）”，实际 **5** 个文件（新增 `数据字典-v1.2-扩展.md`）。
  - `索引.md:78` 标题仍为「当前状态（P1 服装卡完成）」；`:87` 下一步仍写「P2 检索/推荐/提示词/15 例测试；P3 扩充…」——与 P4 现状（45 例验收、9 composer、11 Macbeth）不符。
  - `索引.md:49` 写「每张卡正文必须有 8 个标准小节」，与字典 v1.1 的 source 卡豁免冲突（会误导 QA）。
  - `索引.md:13` 04-来源 仅写 `SRC-0001..0099`/`SRC-0100..0199`，漏 P4 书源 `SRC-0061..0069` 等当前段位描述；**无任何 v1.2/扩展文档/OUTFIT-COMPOSER 链接**。
  - 正面：01–03 计数本身正确（87 GAR / 25 STR / 14 MAT；121 verified + 5 interpretive）。
- **复现**：`ls 00-系统 | wc -l`；`grep -nE '4（P0）|P1 服装卡完成|下一步|8 个标准小节|v1.2' 00-系统/索引.md`
- **修复**：更新目录表/状态/下一步/质量门（source 豁免）；增加 v1.2 扩展与 P4 文档链接；04-来源描述补 0061..0069 与 0520..0524 段位。
- **验收**：索引计数与 `ls`/validate 一致；点击 v1.2/P4 文档链接可达；grep “8 个标准小节” 附 source 豁免说明。
- **状态**：OPEN

### SCHEMA-05 [MEDIUM] 顶层摘要报告快照漂移（STATUS/COVERAGE/QA 顶部仍是 P3.3 343）
- **证据**
  - `reports/STATUS.md:1-4`：标题「P3.3 最终复验后」、更新 03:26、快照 **343 卡（158+185）**；同文件 §10 已追加 P4 快照 **399（188+211）** → 同一文件两个快照，读者按标题会误读。
  - `reports/COVERAGE.md:1-3`、`reports/QA.md:1-3`：仍为 P3.3 343 卡 / 185 来源，未更新到 P4；P4 数据在 `reports/P4-COVERAGE.md`、`reports/P4-REPORT.md`。
  - P4-REPORT/P4-COVERAGE 本身与实际一致（399/188/211）。
- **复现**：`head -5 reports/STATUS.md reports/COVERAGE.md reports/QA.md`；对比 P4 报告。
- **修复**：更新三份顶层摘要的 header/快照，或改为“当前快照入口 + 历史章节”的结构，并链接 P4 报告。
- **验收**：三份文件顶部快照均显示 399/188/211 与 HEAD；无自相矛盾数字。
- **状态**：OPEN

### SCHEMA-06 [MEDIUM] P4-2 新卡未满足“movement/lighting notes”要求（17/22 缺失）
- **证据**
  - P4-2 任务要求每张新卡含 `prompt_en`、`movement/lighting` notes。实际 22 张新卡中，**17 张**（STR-0012..0025 + MAT-0012..0014）均无 `movement_notes`/`lighting_notes`；仅 5 张 GAR-0083..0087（garment 必填字段）有。
  - `validate.py` 对 garment_part/material 不要求这两字段，所以 **PASS 不覆盖该要求**（验收盲区）。
  - 复现脚本见 §2.4。
- **修复**：为 17 张卡补 `movement_notes`/`lighting_notes`，或修改任务口径（若结构/材料卡不需要）并在 P4 报告中声明例外。
- **验收**：22/22 新卡含两字段（或书面例外）；validate 增加可选检查或 QA 抽检。
- **状态**：OPEN

### SCHEMA-07 [LOW] P4 报告“22 张卡覆盖 36/42 字段”与实际不符（实际 21 张）
- **证据**：`reports/P4-REPORT.md:45` 写“22 张覆盖 36/42”；实际使用 v1.2 字段的 new 卡为 **21** 张（STR-0024 结构属性词表未填可选字段），字段数 36/42 正确。
- **复现**：run 脚本统计 new IDs × optional keys。
- **修复**：报告改为“21 张覆盖 36/42（STR-0024 为纯词表卡，未填）”，或给 STR-0024 加一个可选字段。
- **验收**：报告数字与脚本一致。
- **状态**：OPEN

### SCHEMA-08 [LOW] v1.2 扩展回滚说明的来源段位范围错误
- **证据**：`00-系统/数据字典-v1.2-扩展.md:84` 写“删除…`04-来源/SRC-0520..0539`”，但本批实际来源为 **SRC-0520..0524（5 张）**；SRC-0061..0069 是 P4-1 书源（另一批），不属 v1.2 回滚范围。
- **修复**：改为 `SRC-0520..0524`，并注明 P4-1 书源（0061..0069）不随 v1.2 回滚。
- **验收**：按回滚步骤演练后，仅 22 卡 + 5 来源消失，旧卡/书源不受影响。
- **状态**：OPEN

### SCHEMA-09 [LOW] 卡片模板未同步 v1.2 可选字段
- **证据**：`00-系统/卡片模板.md` 无 `v1.2`/可选字段说明（grep 0）；但 21 张新卡实际使用 v1.2 字段，模板是用户复制入口，缺入口会降低字段采用率。
- **修复**：在模板头部加“v1.2 可选字段见 [[数据字典-v1.2-扩展]]”，并给 STR/garment/material 模板加可选字段示例行。
- **验收**：模板可检索到 v1.2 链接；新建卡可按模板填可选字段。
- **状态**：OPEN

### SCHEMA-10 [LOW] 来源段位/登记描述与现状不一致（索引 + 扩展文档）
- **证据**：`00-系统/索引.md:13` 04-来源描述只有 `0001..0099`/`0100..0199`；实际 211 来源含 `0061..0069`（P4 书源）、`0520..0524`（P4-2）；`00-系统/数据字典.md` §2 列到 `SRC-0520..0529`，但实际仅用到 0524（build_sources 报 gap 属预期，但文档未说明“段位预留≠必须连续”）。
- **修复**：在索引/来源规范中补“当前实际使用段位”与“预留段位可空”的说明。
- **验收**：读者可从索引/规范推断实际来源分布；build_sources gap 有解释。
- **状态**：OPEN

### 正向兼容性（PASS，非缺陷）
- `python3 scripts/validate.py` → **PASS：399/399，来源卡 211，0 错误 0 警告**。
- `python3 scripts/build_sources.py --check` → **PASS：CSV 与全部来源卡一致（212 行含表头）**。
- 旧卡未被 v1.2 污染：全库 **0 张旧卡**含 v1.2 可选字段（仅 21 张 P4-2 新卡）；P4 提交 `7f7a21b`、`56f4225` 对 `01/02/03/05/06/07/09` 卡片 **0 个 M**。
- P4 不改旧 CLI：`7f7a21b` 仅新增 `scripts/books_extract.py`、`scripts/outfit.py`；`query/recommend/workflow/validate` 0 行变更。
- CLI 文档化命令实测：`query.py --id GAR-0084 --json` exit 0，契约键与 skill 一致；`recommend.py --brief ... --json` exit 0（3 looks）；`workflow.py` 缺输入 exit **2**（与文档一致）；`outfit.py --help` exit 0；`tests/test_workflow.py`、`11-验收/P4-COMPOSER/test_outfit.py`、`11-验收/P4-MACBETH/test_macbeth_p4.py` 均存在。
- 无死链：两份 skill 引用的脚本/测试/验收/文档路径全部存在（逐项 `test -e` = OK）。

## 2. 复现与原始证据

### 2.1 计数（实际）
```bash
# 实际：399 = 188 内容 + 211 来源
python3 - <<'PY'
import glob,yaml
from collections import Counter
content=[];sources=[]
for d in ['01-服装单品','02-结构细节','03-材质纹样','05-风格体系','06-时代地域','07-剧情场景','09-造型组合']:
    for f in glob.glob(d+'/**/*.md',recursive=True):
        t=open(f,encoding='utf-8').read()
        if t.startswith('---'): content.append(yaml.safe_load(t.split('---',2)[1]))
for f in glob.glob('04-来源/*.md'):
    t=open(f,encoding='utf-8').read()
    if t.startswith('---'):
        fm=yaml.safe_load(t.split('---',2)[1])
        if fm.get('type')=='source': sources.append(fm)
print(len(content),len(sources),len(content)+len(sources),Counter(c['type'] for c in content))
PY
```
输出：`188 211 399 {'garment': 88（含 1 张 example）, 'garment_part': 25, 'material': 11, 'pattern': 3, 'style': 11, 'period_region': 11, 'scene': 16, 'look': 23}`。

### 2.2 校验/来源对账
```bash
python3 scripts/validate.py        # exit 0, 399/399, 211 sources, 0 errors/warnings
python3 scripts/build_sources.py --check  # exit 0, CSV 212 lines, PASS
```

### 2.3 v1.2 使用/缺失
```bash
# 36/42 fields used; 21 cards; 6 unused: belt_width_class buckle_type handle_type neckline_shape prop_closure stretch_class
# 17 new STR/MAT cards missing movement_notes/lighting_notes
# old cards with any v1.2 optional field: 0
```
（完整脚本见本次审计命令记录；输出已在 §1 SCHEMA-03/06 引用。）

### 2.4 Skill 分叉 / 能力缺口
```bash
wc -l skills/costume-director/SKILL.md .dsh/skills/costume-director/SKILL.md
#  387 skills/costume-director/SKILL.md
#  264 .dsh/skills/costume-director/SKILL.md
diff -q skills/costume-director/SKILL.md .dsh/skills/costume-director/SKILL.md  # differ
grep -c 'workflow.py' skills/costume-director/SKILL.md   # 0
grep -cE 'outfit|v1\.2|books_extract' .dsh/skills/costume-director/SKILL.md  # 0 relevant (only "outfits" in whenToUse)
grep -n '30 例' skills/costume-director/SKILL.md         # line 345/350, actual acceptance = 45
```

### 2.5 索引/报告快照
```bash
ls 00-系统 | wc -l          # 5 (index says 4)
grep -n 'P1 服装卡完成\|下一步：P2\|8 个标准小节' 00-系统/索引.md
head -4 reports/STATUS.md   # 343/185
head -3 reports/COVERAGE.md # 343/185
head -3 reports/QA.md       # 343/185
```

## 3. 优先级与建议修复顺序

1. **P0（本周）**：SCHEMA-01/02——统一 skill 为 `.dsh` 单源，补 workflow/outfit/v1.2/books 入口；否则 Agent/用户按项目 skill 会漏掉 P4 能力（最影响可用性）。
2. **P1**：SCHEMA-03/04/05——明确 v1.2 消费范围或接入 query/validate；更新索引与 STATUS/COVERAGE/QA 快照。
3. **P2**：SCHEMA-06/07/08/09/10——补 17 张卡的 movement/lighting 或声明例外；修报告/回滚/模板/段位说明。
4. **回归门槛**：修复后重跑 `validate.py`、`build_sources --check`、`run_acceptance.py`、`rewrite quality_eval` 与 skill smoke；`validate` 需保持 0 错误 0 警告。

## 4. 声明

本报告为**只读审计产物**：未修改任何卡片、`scripts/`、`skills/`、`00-系统/` 或既有报告；未提交 git；未联网修改数据。所有计数/退出码/路径检查均在本快照（HEAD `56f4225`）执行。
