# P3 独立质量验收报告（QA）

- 验收人：`verifier`（独立复跑与评分；只写 reports/，未改卡片/脚本/`00-系统`）
- 时间：2026-11-04 02:27–02:50（Asia/Shanghai）
- 环境：macOS，Python 3.9.6，PyYAML 6.0.3；网络可用；无 Obsidian GUI
- 快照：**328 张卡（内容 154 + 来源 174）**；git HEAD `0345f05`（P3 commit，工作区 clean）
- 输入：`reports/P2.5-ACCEPTANCE.md`、`11-验收/P2.5-案例/`、`11-验收/测试输入 T01–T30`、`11-验收/质量评估/`（engineer 自评，**未采信**）、本人独立探针/案例

## 0. 结论摘要：PASS 12 / WARN 7 / FAIL 2 / HUMAN_UAT_PENDING 4

| # | 项 | 判定 | 证据 |
|---|---|---|---|
| P1 | `validate.py` 结构校验 | **PASS** | 328/328 卡；17/17 检查 PASS；0 错误级 0 警告 |
| P2 | `build_sources.py` 一致性 | **PASS（修复后）** | 初始 CSV 仅 142 行（缺 32 行，FAIL）→ 本轮 `--write` 重建 174 行后 `--check` PASS |
| P3 | 30 例验收 | **PASS** | `run_acceptance.py` exit 0；PASS 30/30；query 命中合计 124、逐例 ≥1 |
| P4 | F1 崩溃回归 | **PASS** | historical 1940s/1950s/1960s/1970s：**4/4 exit 0、3 looks**（P2.5 为 4/4 exit 1） |
| P5 | F2 period/region 假阴性回归 | **PASS** | 1580s 意大利（T23/C08）与拜占庭（T24/我的探针）exit 0；无「no wardrobe candidates」假声明；改用 `period_era_level`/`knowledge_gap_slots` 诚实声明 |
| P6 | F3 证据不足行为回归 | **PASS** | 6 个未覆盖探针全部 exit 0 且**每个 3–8 条 warnings**（P2.5 为 4 个静默 0 warning）；无静默套用声明 |
| P7 | example 卡禁入 A | **PASS** | 30/30 T 用例 + 15 个语义案例 A 套 example=0（P2.5 为 13/18） |
| P8 | 新增来源 URL 抽样 | **PASS** | 32 个新来源 URL **32/32 HTTP 200**（curl -m 10 -L）+ 页面标题/对象描述与卡名逐条吻合（抽样 ≥15 要求超额） |
| P9 | 证据可追溯（15 案例） | **PASS** | 所有推荐单品 ID 存在、带 source_ids；`missing_urls=[]`；编造=0 |
| P10 | A/B/C 实质差异（度量） | **PASS** | 27/27 非连续性 T 用例 A-B/A-C/B-C 对称差 ≥2 件（P2.5：B-C 10/16 仅差 1 件） |
| P11 | warnings 覆盖率 | **PASS** | 30/30 T 用例均有 warnings（P2.5 0/18） |
| P12 | P3 体量目标 | **PASS** | 328 ≥ 250；新增 carried_prop 3、scene +12、look +13、source +32 |
| W1 | query 相关性 | **WARN** | 我的独立复评：relevant@5 **3.64/5**、precision **89.2%**、0 命中 **12%**（P2.5：3.0/86.2%/16%）→ 改善但低于 engineer 自评 3.84/94.1%（评分标准更宽） |
| W2 | query 排序/重复 | **WARN** | example 卡仍在 P14「noir」第 1、4 名；P07「1930s 上海」top5 仍无 GAR-0031；GAR-0001/GAR-0065 两卡同名「和服」（重复内容） |
| W3 | 15 案例 6 维语义 rubric | **WARN** | 1 PASS / 14 WARN / 0 FAIL；但**切题维度均值仅 0.53/2**、约束 1.0/2；诚实/证据 2.0/2（详见 §3） |
| W4 | M4 context 过滤 | **WARN** | C01（1644 明末）context 仍引用 STY-EXAMPLE-001/STY-0002（维多利亚丧服）/PRD-0001（1770s）→ 未修复 |
| W5 | M6 派克大衣语义 | **WARN** | GAR-0019 仍被用于 1890s 室内/1930s 雨景外层（T10/T13）；部分 warning 提及但不具体 |
| W6 | M7 prompt 串文 | **WARN** | T13（室内走廊）prompt 仍出现 anorak 的「worn in snow」×2；T14 雪景属合理；「neon」来自输入光照规格（非串文） |
| W7 | M1/M2 数据错标 | **WARN** | GAR-0010「用于运动与童装」仍在；SRC-0046/0047 仍 `not_applicable`（应为 public domain/cc0） |
| F1 | D2 职业服万能填充 | **FAIL** | 当代/职业请求 A 套普遍为 警察制服 + 医生白袍 + 医疗工作鞋：T04 舞者、T15 建筑师、T18 小学教师、T26/C02/N1 急诊护士、T05/C03/N2 太空、C07/T27 婚礼……同时 warning 自称「no occupational garment cards match X」，但库内已有 护士制服 GAR-0036/医生白袍 GAR-0041 等 → 自相矛盾+切题错误 |
| F2 | D4 虚假「rainwear cards are missing」 | **FAIL** | T01/T02（1930s 上海雨）warning 称「rainwear cards are missing」，但库内已有 GAR-0045 风衣、GAR-0046 雨衣（tags 含 rain）→ 错误证据声明（mislabel 级） |
| H1 | Obsidian GUI | **HUMAN_UAT_PENDING** | 无 GUI；仅结构层 609+ 链接可达 |
| H2 | 逐图版权授权 | **HUMAN_UAT_PENDING** | 0 下载/0 内嵌保证；未逐图核验 |
| H3 | 语义评分人工签核 | **HUMAN_UAT_PENDING** | 15 案例 6 维评分为 verifier 人工判断，需 lead 签核 |
| H4 | 62 张 draft 复核 | **HUMAN_UAT_PENDING** | `review_status: draft` 62 张（新增卡多为 draft） |

> 计数：PASS 12 + WARN 7 + FAIL 2 + HUMAN_UAT_PENDING 4 = 25 项。
> 声明：**exit 0 / 30-30 PASS 不等于质量达标**；F1/F2 是本轮发现的语义级 FAIL（诚实性已改善，但推荐切题与证据声明仍有严重问题）。GUI/逐图版权/签核/draft 复核均不得写成 PASS。

## 1. 方法与真实命令

| 步骤 | 命令 | 退出码 | 结果 |
|---|---|---|---|
| 结构校验 | `python3 scripts/validate.py` | 0 | 328 卡 17/17 PASS，0 错误 0 警告 |
| 来源对账（初始） | `python3 scripts/build_sources.py --check` | **1** | CSV 142 行 vs 174 来源卡（缺 SRC-0400..0431 共 32 行）→ 记为 D1 |
| 来源对账（修复后） | `python3 scripts/build_sources.py --write` → `--check` | 0 / 0 | 重建 174 行 + 表头（175 行）；一致性 PASS；3 组重复 URL 已标 canonical |
| 验收 | `python3 scripts/run_acceptance.py` | 0 | PASS 30/30，FAIL 0/30；query 命中总 124 |
| F1/F2/F3 回归 | 4 个 historical mid-century 输入 + C08 + Byzantine + I1–I6 | 全 0 | 见 §2 |
| query 探针 | 25 条固定探针 + 6 条未覆盖探针（`--limit 5 --json`） | 全 0 | 见 §3.1；relevant@5 3.64、precision 89.2%、0-hit 12% |
| 语义案例 | 10 个 P2.5 C 案例 + 5 个新 N 案例（N1 ER 护士 / N2 火星技师 / N3 加纳婚礼新郎 / N4 身份下滑 / N5 历史+义体冲突） | 15/15 exit 0 | 6 维 rubric 见 §3.2 |
| 新来源 URL | 32 个 SRC-0400..0431，`curl -sS -m 10 -L` | 0 | 32/32 HTTP 200；页面标题/描述与卡名吻合 |

## 2. P2.5 回归验证（F1/F2/F3）

| 回归项 | P2.5 基线 | P3 实测 | 结论 |
|---|---|---|---|
| F1 historical 1940s–70s 崩溃 | 4/4 exit 1（KeyError evidence） | **4/4 exit 0、3 looks、warnings 3** | **FIXED** |
| F2 1580s 意大利 | exit 3「no wardrobe candidates」假阴性 | T23/C08 exit 0、3 looks，使用 doublet/codpiece/文艺复兴长袍/穆勒鞋 + `period_era_level` 警告 | **FIXED** |
| F2 拜占庭 | exit 3 假阴性 | T24/我的探针 exit 0、1 look（dalmatic）+ `knowledge_gap_slots` + 「looks are missing required layers … no invented replacements」 | **FIXED（诚实部分输出）** |
| F3 6 个未覆盖探针 | 4/6 静默（warnings=[]） | **6/6 均有 3–8 条 warnings**（职业/文化/未来/年代/天气缺口） | **FIXED（诚实性）** |
| example 卡进 A | 13/18 T 用例 | 0/30 T 用例、0/15 语义案例 | **FIXED** |
| M3 false-negative 措辞 | 有 | T23/T24/Byzantine 无「no wardrobe candidates」；改为近似/缺口声明 | **FIXED** |
| M5 example 污染 | 13/18、5/8 | 0/30、0/15 | **FIXED** |
| A/B/C 差异（度量） | B-C 10/16 仅差 1 件 | 27/27 用例 A-B/A-C/B-C 对称差 ≥2 件 | **FIXED（度量）** |
| 冲突检测 | C10 未识别 | C10/T29/N5 warnings 含「historical vs sci-fi/neon/body-mod 冲突 + 拆分建议」 | **FIXED** |
| 叙事意义（身份弧线） | C05 未检测 | C05/N4/T03 warning：「identity/economic arc present but one locked wardrobe spans all scenes; wardrobe-stage change not modeled」+ LOOK-0015/0016/0017 弧线卡 | **PARTIAL（已声明，未建模）** |
| brief 自由文本解析 | T30 无 | T30 exit 0、3 looks，warning「brief parser left these fields unknown: season」——未知字段明确标 unknown，未猜测 | **PASS** |

**未修复的 M 项**：M1（GAR-0010「运动与童装」）、M2（SRC-0046/0047 许可）、M4（C01 context 引用 1770s/维多利亚）、M6（GAR-0019 仍作室内/雨景外层）、M7（T13 prompt「worn in snow」）、M8（query example 排序、GAR-0031 掉榜、和服重复卡）。详见 `P3-DEFECTS.md`。

## 3. 质量度量（独立复算）

### 3.1 query.py：25 探针 + 6 未覆盖探针

| 指标 | P2.5 | P3 本轮（verifier 独立） | engineer 自评 |
|---|---|---|---|
| relevant@5（0–5） | 3.0 | **3.64**（91/125） | 3.84 |
| precision（返回结果中相关比例） | 86.2% | **89.2%**（91/102） | 94.1% |
| 0 命中率 | 16%（4/25） | **12%**（3/25：P20 spacesuit / P21 Mughal / P22 mourning） | 12% |
| 未覆盖主题 6 探针命中 | 男鞋 0、太空 0、雨衣 0 等 | **Q26 男鞋 1、Q27 拜占庭 5、Q28 非洲仪式 5、Q29 太空站 1、Q30 朋克 5、Q31 雨衣 1（全部 ≥1）** | — |

- 改善点：徽章（P06 0→5）、风衣/雨衣（P03 2→5）、1930s 上海（P07 top5 全为上海主题）、拜占庭/非洲/太空站/雨衣均新增 LOOK 卡命中。
- 剩余：P14「noir」top5 仍含 2 张 example 卡（真实 STY-0005 不在 top5）；P07 top5 仍无 GAR-0031；GAR-0001 与 GAR-0065 同为「和服」卡（重复内容）；P09/P10 多词跨文化检索仍混入不相干品类（纱丽/韩服 vs 和服）。
- 相关性评分由人工判定（无标注集），口径与 engineer 的自评不同，故 3.64 vs 3.84 的差异属评分严格度差异，非执行错误。

### 3.2 15 案例 6 维语义 rubric（切题/差异/约束/证据/诚实/叙事，各 0–2）

评级阈值：总分 ≥10 PASS；7–9 WARN；≤6 FAIL。

| 案例 | 切题 | 差异 | 约束 | 证据 | 诚实 | 叙事 | 总分 | 判定 | 关键观察 |
|---|---|---|---|---|---|---|---|---|---|
| C01 明末清初文人 | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 用欧洲 doublet/codpiece/mule 顶替明代；context 仍引 1770s/维多利亚 |
| C02 急诊护士 | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | A=警察制服+医生白袍+医疗鞋（护士制服卡 GAR-0036 未被选中）；warnings 诚实 |
| C03 零重力歌剧女伶 | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 未来基底缺失，warnings 声明 future_wardrobe_gap |
| C04 1920s 表现主义梦游者 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 混入 1930s/1950s 单品；风格卡缺失已警告 |
| C05 富太→难民 | 1 | 0 | 1 | 2 | 2 | 1 | 7 | WARN | 1 套贯穿三场；新增「identity arc not modeled」warning（诚实但未解决） |
| C06 夜班信使连续性 | 0 | 1 | 1 | 2 | 2 | 2 | 8 | WARN | 状态连续性正确；主体为警察制服/白袍（职业误配） |
| C07 加纳-英国婚礼 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | A 用布布长袍（相关）+ 威灵顿靴；B/C 警察制服；文化 warning 有 |
| C08 1580s 意大利舞者 | 2 | 2 | 1 | 2 | 2 | 1 | **10** | **PASS** | 使用 doublet/codpiece/文艺复兴长袍/穆勒鞋；舞蹈-鞋跟冲突有 warning |
| C09 低预算太空站 | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 职业/未来误配；预算 C=A 成本已声明 |
| C10 1930s 上海+赛博义体 | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 冲突检测 warning 已出现（历史 vs 科幻拆分建议）；单品仍错配 |
| N1 ER 创伤护士（新） | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 同 C02；职业缺口已警告 |
| N2 火星技师（新） | 0 | 2 | 1 | 2 | 2 | 1 | 8 | WARN | 未来基底缺失，warnings 诚实 |
| N3 加纳婚礼新郎（新） | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | agbada（GAR-0069）相关；婚礼仪式缺口已警告 |
| N4 爵士名媛→大萧条女工（新） | 0 | 1 | 1 | 2 | 2 | 1 | 7 | WARN | 1920s 名媛用马甲+牛仔裤+军大衣；身份弧线未建模已警告 |
| N5 1920s 上海+义体（新） | 1 | 2 | 1 | 2 | 2 | 1 | 9 | WARN | 冲突检测/湿鞋警告均出现；外层仍为消防防护外套 |

**汇总**：PASS 1 / WARN 14 / FAIL 0（对 rubric）；维度均值：**切题 0.53/2、差异 1.73/2、约束 1.00/2、证据 2.00/2、诚实 2.00/2、叙事 1.00/2**。
- 结论：P3 把 P2.5 的 FAIL 从「静默/崩溃」提升为「诚实 WARN」，**但切题与硬约束仍显著低于可交付标准**（多数现代/职业/未来案例的 A 套为职业制服错配）。不得以 30/30 或 rubric 无 FAIL 认定为质量通过。

### 3.3 新增来源 URL 抽样（≥15 要求）

- SRC-0400..SRC-0431 共 32 条新来源：`curl -sS -m 10 -L` **32/32 HTTP 200**。
- 内容核验（页面标题/对象描述 vs 来源卡名，抽样 20+，覆盖全部类型）：V&A 护士戏服/Emergency Ward 10、日本消防外套、Victor Stiebel 罩衣、儿童宇航员头盔、Burberry 蕾丝风衣、1920s 橡胶绸雨衣、1927 雨伞、刺绣手袋、手杖、ENSA 徽章、John Cooper Clarke 徽章、Utility 裙、Molyneux 鸡尾酒裙、英国节童裙、Twiggy 迷你裙、Courrèges 外套页、Rayne 厚底鞋、Liberty 背带裤、Saxone 男鞋、Met 科普特长袍（4th–7th c）、意大利 1600–10 丝袍、拜占庭 samite、Mysore 寺庙纱丽、1970s 韩服、1910–30 出口和服、1930–45 obi、1875–1911 云肩、1902 婚纱、2022 拉各斯 agbádá、1980s gele —— **逐条吻合**；Met JSON 中 `isPublicDomain` 与卡片许可标注一致（cc0 / link_only）。

## 4. M1–M8 修复状态

| 编号 | 内容 | 状态 | 证据 |
|---|---|---|---|
| M1 | GAR-0010「用于运动与童装」扩写 | **未修复** | 卡片 `## 来源链接` 原文仍在；FIT bloomers 页 0 次 sport/children |
| M2 | SRC-0046/0047 许可错标 | **未修复** | 仍 `license_status: not_applicable`（rights=Public domain） |
| M3 | 假阴性「无覆盖」声明 | **已修复** | 1580s/拜占庭均输出近似/缺口诚实声明（§2） |
| M4 | C01 context 误导引用 | **未修复** | 仍 STY-EXAMPLE-001/STY-0002/PRD-0001 |
| M5 | example 卡进 A 套 | **已修复** | 0/30 + 0/15 |
| M6 | GAR-0019 作室内/雨景外层 | **未修复** | T10 look2/3、T13 look2/3 使用；T10 prompt 出现 Arctic anorak |
| M7 | prompt 串文「worn in snow」 | **部分** | T13 室内场景 ×2 仍在；T14 雪景属合理；neon 属输入光照规格 |
| M8 | query 排序/重复 | **部分** | 徽章/风衣/雨衣检索已修复；P14 example 排序、P07 漏 GAR-0031、和服重复卡仍在 |

## 5. 数据/报表一致性

- `validate.py`：PASS（328/328，0 错误 0 警告）。
- `run_acceptance.py`：PASS 30/30，query 命中 124、逐例 ≥1；SUMMARY 与实测一致。
- `build_sources.py`：**初始 FAIL（CSV 142 vs 174，D1）→ 本轮重建后 PASS**；`reports/SOURCES.csv` 现 175 行（174+表头）。3 组重复 URL 仍为 canonical 交叉引用。
- `11-验收/质量评估/` engineer 自评为 OVERALL PASS（relevant@5 3.84 等）；本报告独立复算为 3.64/89.2%，并指出 F1/F2 语义 FAIL 未被其指标覆盖 → **不采信其 OVERALL PASS 作为验收结论**。

## 6. 局限与 HUMAN_UAT_PENDING（不得写成 PASS）

1. **Obsidian GUI**：打开/渲染/`[[wikilink]]` 点击跳转未测试（无 GUI；仅结构层验证）。
2. **逐图版权授权**：未逐图核验（当前策略 0 下载/0 内嵌）。
3. **语义评分签核**：本报告 15 案例 6 维评分为 verifier 人工判断，需 lead 签核。
4. **62 张 draft 卡复核**：`review_status: draft` 62 张（328 中），未人工复核。
- 其它限制：query 相关性无标注集；推荐评分只审计当前 KB/脚本版本；未做随机性/参数敏感性测试；未修改 `scripts/`（只读审计）。

## 7. 建议（按严重度）

**P0（阻断）**
1. **修职业匹配**：建立 occupation→card 映射（护士→GAR-0036、医生→GAR-0041+N95 口罩/PPE、厨师→GAR-0043、警察→GAR-0042 仅警察场景）；禁止跨职业制服作为通用填充；warning 不得再声称「no occupational garment cards match」当对应卡存在。
2. **修「rainwear cards are missing」虚假声明**（GAR-0045/0046 存在）：改用「有雨具卡但年代/地域不匹配」的准确措辞。
3. **prompt/context 过滤**：T13 室内场景剔除 anorak「worn in snow」；C01 只挂匹配的 period/style 引用（去掉 1770s/维多利亚）。
4. **M1/M2/M4** 数据与文档错标修正。

**P1（质量）**
5. A/B/C 差异已达度量化目标，但需提升「切题」：新增 occupational/环境/文化约束字段，按场景硬过滤（室内禁用极地派克、医院禁用厨师服）。
6. 未覆盖主题（spacesuit/Mughal/mourning）继续补卡或保持诚实 0 命中；example 卡排序降权。
7. 和服重复卡（GAR-0001/GAR-0065）合并或标 canonical；补 pattern/material 族系（见 COVERAGE）。

**P2（收尾）**
8. 完成 HUMAN_UAT_PENDING（GUI/版权/签核/draft 复核）；更新 `reports/SOURCES.csv` 重建流程纳入验收步骤（避免 D1 复发）。

## 8. 附录：原始证据位置与复现

- **复现脚本**：`python3 scripts/quality_eval_audit.py --quick`（F1/F2/F3 回归探针）、`python3 scripts/quality_eval_audit.py`（回归 + 25+6 query 探针 + 15 语义案例）、`--urls`（SRC-0400..0431 URL 检查）。脚本为审计辅助：exit 0 仅代表跑完。
- 回归/探针原始输出：`/tmp/p3_audit.json`、`/tmp/p3_query_probes.json`、`/tmp/p3new/*.out.json`、`/tmp/ev3/results.tsv`（32 URL）。
- 说明：QA 期间按任务要求重跑 `run_acceptance.py`，会按 runner 设计重写 `11-验收/测试结果/SUMMARY.md`、T01–T30 结果 MD 与 `raw/`（本轮 git 工作区中 35 个该目录文件为 M，属预期产物，不是卡片改动）。
- acceptance：`11-验收/测试结果/SUMMARY.md`（30 例）、`raw/T01..T30.json`。
- 版本：v1.0（2026-11-04，verifier/task-14）。
