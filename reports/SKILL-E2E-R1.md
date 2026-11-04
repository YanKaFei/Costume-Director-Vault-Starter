# R1 — Costume Director Skill real E2E（官方 DeepSeek vs Doubao overlay）

- 日期：2026-11-04（Asia/Shanghai）
- Skill：`.dsh/skills/costume-director/SKILL.md`（只读取/调用，**未修改**）
- 用户 profile：未修改；overlay 仅用临时 `--patch` 文件
- 证据目录：`11-验收/R1/skill-e2e/`
  - `official/C01..C06/{prompt.txt,events.jsonl,answer.md,stderr.log}`
  - `overlay/C01..C06/{prompt.txt,events.jsonl,answer.md,stderr.log}`
  - `validation-official.json`, `validation-overlay.json`, `SUMMARY.md`, `doubao-overlay.yml`
- 校验器：`11-验收/R1/skill-e2e/validate_r1.py`（JSONL 事件 + 真实卡/SRC/术语覆盖）

## 1. 运行命令

官方路由（DeepSeek key 从本机 credential service 注入，不打印值）：
```bash
cd /Users/coffee/Desktop/Costume-Director-Vault-Starter
DEEPSEEK_API_KEY="$(python3 -c 'import yaml,pathlib;print(yaml.safe_load((pathlib.Path.home()/".dsh/.credentials.yaml").read_text())["refs"]["DEEPSEEK_API_KEY"])')" \
dsh --profile headless --json "$(cat 11-验收/R1/skill-e2e/official/C0N/prompt.txt)" \
  > 11-验收/R1/skill-e2e/official/C0N/events.jsonl \
  2> 11-验收/R1/skill-e2e/official/C0N/stderr.log
```

Overlay（同一 prompt，临时 provider 切换；不改 `~/.dsh/profiles`）：
```bash
DOUBAO_API_KEY="$(python3 -c '...DOUBAO_API_KEY...')" \
dsh --profile headless --patch /tmp/dsh-doubao.yml --json \
  "$(cat 11-验收/R1/skill-e2e/overlay/C0N/prompt.txt)" \
  > 11-验收/R1/skill-e2e/overlay/C0N/events.jsonl \
  2> 11-验收/R1/skill-e2e/overlay/C0N/stderr.log
```
overlay 定义见 `11-验收/R1/skill-e2e/doubao-overlay.yml`（Doubao Seed 2.1 gateway；
仅临时用于本机 E2E）。

## 2. 两栏结果

| 用例 | 覆盖 | 官方 DeepSeek | Doubao overlay |
| --- | --- | --- | --- |
| C01 | PG76299 / English Costume 书籍术语 | **PASS**（未 402） | **PASS** |
| C02 | v1.2 结构 STR-0012/0013/0014 | **PASS** | **PASS** |
| C03 | 配饰 GAR-0083..0087 | **PASS** | **PASS** |
| C04 | outfit composer 完整搭配 | **PASS** | **PASS** |
| C05 | 中英服饰术语检索 | **PASS** | **PASS** |
| C06 | 视觉索引 VIS/related_card | **PASS** | **PASS** |

- 官方：**6 PASS / 0 BLOCKED / 0 FAIL**。本次官方路由**没有返回 402**：
  `events.jsonl` 的 `turn_end.reason.kind == "completed"`，无 QUOTA/Insufficient Balance。
  这是与 task-34 smoke 时 402 不同的实时配额状态；按实测记录，未伪造 BLOCKED。
- Overlay：**6 PASS / 0 BLOCKED / 0 FAIL**。
- 两个模式的 C01–C06 均有：`skill("costume-director")` 调用、真实 `python3 scripts/query.py`
  （C04 另有 `scripts/outfit.py`）执行、最终 answer 非空、turn completed。
- 所有 answer 引用的 GAR/STR/MAT/STY/PRD/LOOK/SCN/SRC 均通过 `costume_lib` 校验存在；
  SRC 均可解析；无 example 卡作为证据。

## 3. 事件证据摘要

| 用例 | 官方 events / skill / script calls / final chars | Overlay events / skill / script calls / final chars |
| --- | --- | --- |
| C01 | 146 / 1 / 6 / 1467 | 46 / 1 / 4 / 1334 |
| C02 | 131 / 1 / 8 / 744 | 31 / 1 / 2 / 1348 |
| C03 | 66 / 1 / 7 / 1274 | 24 / 1 / 2 / 1133 |
| C04 | 190 / 1 / 28 / 2880 | 108 / 1 / 12 / 1762 |
| C05 | 106 / 1 / 10 / 915 | 22 / 1 / 3 / 1018 |
| C06 | 81 / 1 / 7 / 704 | 26 / 1 / 2 / 1437 |

- 官方 C04 的 28 次脚本调用包含 `outfit.py` 和多次 `query.py --id` 校验；overlay C04 12 次。
- 官方与 overlay 的 `answer.md` 均由 `final` 事件提取；每条 `events.jsonl` 保留原始工具调用/返回。

## 4. P4 数据覆盖

- **书籍**：C01 读取 `11-验收/P4-BOOKS/extracted/76299.json` 与 `TERMS-GLOSSARY.md`，
  核对 blazer / waistcoat / trousers / frock coat；并纠正：**PG76299 是 W. H. Baker
  《A Dictionary of Men's Wear》(1908)，不是《English Costume》**；English Costume
  对应 PG33020 / SRC-0063。引用 SRC-0066 等真实来源。
- **v1.2 结构**：C02 实查并引用 STR-0012（翻领/驳领）、STR-0013（装袖/插肩袖）、
  STR-0014（肩线/肩垫），给出真实结构卡与 SRC。
- **配饰**：C03 逐条核对 GAR-0083 手套、GAR-0084 高跟鞋、GAR-0085 帽子结构、
  GAR-0086 胸针结构、GAR-0087 手袋结构，全部为真实 verified 卡 + SRC；同时指出
  其年代多为 17–20 世纪，不适合直接当 1930s 上海配饰（诚实迁移风险）。
- **完整搭配**：C04 真实调用 `scripts/outfit.py`，输出 A/B/C 完整槽位/配饰/英文
  image/video prompt；明确 11 世纪苏格兰无直接证据（historical/analogue gap）。
- **双语检索**：C05 实跑 `query.py`：旗袍/qipao 命中一致（GAR-0031、LOOK-0009 等），
  立领/stand collar 与腰带/belt 列出真实卡与 SRC；指出中文/英文召回差异。
- **视觉索引**：C06 实读 `11-验收/P4-VISUAL/visual-index.csv`，核对 VIS-0001/0003/0005
  的 related_card、source_id、object_url；用 `query.py` 验证 PRD-0003/GAR-0001/STR-0007；
  说明 CC0/图像 URL ≠ 再分发许可，`MET-API` 行不能伪造成 SRC。

## 5. 局限/缺口

- 官方路由本次没有 402，因此**未产生 BLOCKED 证据**；若后续官方额度耗尽，重跑可复现
  task-34 的 402 情形（环境问题，不是 Skill 安装问题）。
- C01 发现用户原始表述把 PG76299 与《English Costume》混为一谈；Agent 诚实纠正并
  给出正确 PG33020/SRC-0063，避免把错误书名当事实。
- 配饰 GAR-0083..0087 是结构/历史配饰卡，并非 1930s 上海专属；用于 1930s 角色时
  属于跨年代借用，答案已标注。
- C04 11 世纪苏格兰无直接实物证据，输出为 inspired/analogue，非历史精确复刻。
- 视觉索引是 CC0 原型：只存链接、不下载/内嵌图像；`MET-API` 来源尚未建独立 SRC 卡，
  C06 已明确不能伪造 SRC 编号。
- 所有运行只读取卡片/脚本/Skill，未修改知识库或用户 profile；overlay 用临时 patch。
