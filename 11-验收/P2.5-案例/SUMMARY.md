# P2.5 语义质量案例 SUMMARY（C01–C10）

- 运行时间：2026-11-04（Asia/Shanghai）
- Python：3.9.6；（脚本未改动；`recommend.py` / `query.py` 以只读方式调用）
- 案例目录：`11-验收/P2.5-案例/`
  - 输入：`inputs/C01..C10.json`
  - 原始输出与退出码：`raw/Cxx-recommend.json`、`raw/Cxx-query.json`、`raw/runs.log`
  - 逐案例报告：`C01.md .. C10.md`
- 运行命令（项目根目录）：`python3 scripts/recommend.py 11-验收/P2.5-案例/inputs/Cxx.json --json` 及 `python3 scripts/query.py <terms> --json`
- 判定：本文件与逐例报告评估的是**语义质量**（切题、差异、冲突、刻板、证据诚实），不是脚本的机械 checks（后者 10 例均通过 `ids_all_exist / three_looks / scores_sum_100 / looks_distinct` 等）。

## 1. 总览

| 案例 | 类型 | recommend exit | 严格 query 命中 | 判定 | 核心语义问题 |
| --- | --- | --- | --- | --- | --- |
| C01 | 历史薄弱年代/地域（明末清初江南文人） | 3 | 0 | **WARN** | 证据不足声明正确；但 context 引用 1770s 英法/1930s 上海/维多利亚丧服，误导且无可替代建议 |
| C02 | 当代现实主义（急诊护士） | 0 | 0 | **FAIL** | 北极兽皮派克大衣 + 牛仔裤 + example 白衬衫充当护士服；无 PPE/工牌；warnings 为空 |
| C03 | 科幻/虚构（零重力歌剧女伶） | 0 | 0 | **FAIL** | 太空歌剧院女伶 = 白衬衫 + 牛仔裤 + 雨靴（A）/ 19 世纪内衣 + 波克帽（B）；仅声明 fictional 无历史断言 |
| C04 | 表现主义/艺术片（1920s 梦游者） | 0 | 0 | **FAIL** | 16 世纪遮阴袋 + 18 世纪马甲/三角帽 + 19 世纪大衣混搭；art direction 只有形容词 |
| C05 | 身份下滑 + 多场次连续性（1930s 上海富太→难民） | 0 | 5 | **FAIL** | 同一套旗袍 + 派克大衣 + 女鞋贯穿晚宴/轰炸/收容所；continuity 机械 PASS |
| C06 | 多场次连续性（当代夜班信使） | 0 | 0 | **WARN** | 干→湿→阴干→湿+破损连续性执行正确；但 A 套主体为 example 卡、极地派克“worn in snow”、缺头盔/箱包 |
| C07 | 跨文化传统服饰（加纳-英国婚礼） | 0 | 0 | **FAIL** | 白衬衫 + 牛仔裤 + 雨靴（A）/ 多文化随机拼贴（B）；库内 kente/adinkra 卡未被使用，无文化语义警告 |
| C08 | 历史 + 动作/舞蹈安全（1580s 意大利宫廷舞者） | 3 | 1 | **FAIL** | 假阴性：库内有 16 世纪 doublet/jerkin/mule/美第奇领，却因 `1580s vs 16th_century` 全部拒绝并 exit 3 |
| C09 | 低预算 + 科幻 + 复用（太空站维修工） | 0 | 0 | **WARN** | C 套成本仅比 A 低 1.2%，A/C 共享 2 件，非可执行预算替代；无预算决策解释 |
| C10 | 冲突约束（1930s 上海 + 赛博朋克义体） | 0 | 0 | **FAIL** | 冲突未被识别：静默按 historical 产出旗袍 + 派克 + 女鞋，无义体接口，warnings 为空 |

## 2. 统计

- 判定：**PASS 0 / WARN 3 / FAIL 7**（10/10 真实运行，均记录退出码与原始输出）。
- recommend 退出码：0 × 8；3 × 2（C01 为真实缺口，C08 为假阴性）。
- query 严格命中：0 条 × 8 例；C05 命中 5 条（1930s 上海 GAR）、C08 命中 1 条（GAR-0009）。
- warnings：仅 C01、C08（exit 3）非空；**8/8 个成功输出案例 warnings 全部为空**。
- A 套高频单品（8 个有方案案例）：`GAR-EXAMPLE-001` 5、`GAR-0014` 5、`GAR-0019` 5、`GAR-0022` 5；其余 `GAR-0035` 3、`GAR-0031` 2、`GAR-0008/0013/0017` 各 1。
- 全 look 单品频次（A+B+C，含连续性的重复使用）：`GAR-0022` 11、`GAR-0019` 10、`GAR-EXAMPLE-001` 8、`GAR-0014` 8、`GAR-0010` 8。
- A 套包含 example 卡：5/8（C02、C03、C06、C07、C09）。
- 成本输出（A/B/C）：C02 0.244/0.328/0.244；C03 0.237/0.343/0.237；C04 0.433/0.337/0.244；C05 0.351（单套连续性）；C06 0.244（单套）；C07 0.237/0.370/0.237；C09 0.244/0.385/0.241；C10 0.351/0.327/0.293。
- context 引用质量：C01、C02、C03、C04、C06、C07、C09 至少 1 个 style/period/scene 引用与场景无关或误导；C05、C10 部分相关但仍有不匹配项（如 C05 的 STY-0004 好莱坞 1930s vs 上海银行家之妻）。
- 证据不足行为：**C01 诚实**（exit 3 + 明确 warning，未编造）；**C08 错误声明**（把检索归一化失败说成知识库无覆盖）；**其余 8 例静默**（缺职业服/未来基底/文化服饰/难民服装/义体卡均未声明）。

## 3. 失败模式（按严重度排序）

1. **历史检索假阴性（C08）**：`period` 字符串未归一化（1580s ≠ 16th_century）、`region` 未做层级归并（italy ⊄ europe），导致本可命中的 16 世纪卡被全部拒绝；exit 3 的“知识库缺口”声明是**错误的**。这是最危险的一类，因为它让使用者以为知识库没有证据。
2. **现代/职业/科幻/文化语境缺卡时静默套用不相关单品**（C02、C03、C07、C09、C10）：`GAR-0019 派克大衣`（北极兽皮）与 `GAR-EXAMPLE-001`（example 卡）成为万能填充；8/8 成功案例 warnings 为空，没有“该职业/文化/未来语境无卡”的声明。
3. **连续性只验证 ID 与状态，不验证叙事弧线（C05）**：机械 PASS 掩盖“富太→难民”身份变化的缺失；同一套旗袍 + 派克大衣贯穿三场。
4. **冲突约束未识别（C10）**：historical 与 cyberpunk 义体/霓虹的冲突没有 warning，也没有模式拆分建议。
5. **跨文化传统服饰被当作随机拼贴（C07）**：kente/adinkra 卡存在却未使用；dashiki、moccasins、18 世纪手笼、北极派克大衣混搭；无文化语义/场合边界声明。
6. **context 引用与 prompt 串文**：C01 引用 1770s 英法；C02 prompt 出现 `worn with a white t-shirt and leather jacket`（皮革夹克不在 items）与 `worn in snow`（急诊室内）；材料卡（Chantilly 蕾丝、passementerie、muslin）被随机挂到旗袍/西装。
   - **连续性顶层 prompt_video 拼接（C05/C06）**：把多场动作与天气拼成一句（如 C05 的“晚宴…逃离…收容所”+“indoor, dry / heavy rain, bombing nearby / cold, overcast”），无法直接用于单场生成；逐场可用的 prompt 只存在于 `continuity.scenes[].prompt_image`（C06 的逐场 prompt 正确带 `wetness=`/`damage=`/`dirt=` 状态令牌）。
7. **预算替代名不副实（C09）**：C 套成本仅低 1.2%，A/C 共享白衬衫与雨靴；无成本明细与复用策略。
8. **三套差异多为“随机历史单品差异”而非叙事差异**：C02 B 套、C03 B 套、C04 A/B、C07 B 套均出现跨时代/跨文化随机组合。

## 4. 对 recommend 逻辑的具体改进建议（不修改脚本，供排期）

**P0 — 检索与证据诚实**
1. 建立 period 归一化表（decade→century→era；如 1580s→16th_century，1930s→20th_century）与 region 层级（italy⊂europe、shanghai⊂china）；严格匹配失败时进入“近似证据”层并输出 warning，而不是直接 exit 3。
2. 只有当归一化后仍无任何候选时才返回 exit 3；否则输出“最接近证据 + 近似原因 + 需要补卡的字段”。
3. warnings 必须覆盖：example 卡入 A、职业/文化/年代缺口、跨 region 借用、极端气候面料出现在室内、冲突的 art_direction。
4. context_refs 加最低分阈值与语义过滤；不达阈值时输出“无可靠上下文”，不要输出 1770s 英法/1930s 上海这类误导引用。

**P1 — 选品与约束**
5. 给 garment 增加 `environment_constraints`（indoor/outdoor/rain/snow/hospital/ballroom）与 `occupation_tags`；北极兽皮派克大衣在 indoor/ER/ballroom 场景中硬性降权或排除。
6. example 卡不得进入 A 套；若只能使用，整 Look 标 example 并输出 warning、限制总分。
7. 性别/解剖一致性检查：遮阴袋（codpiece）与 1930s 女鞋同套出现时应报警或修正。
8. 补建现代/职业/未来基底卡（scrub、PPE、工牌、防滑鞋、雨衣、头盔、配送箱、义体外骨骼、kente/adinkra 可穿戴卡）；在缺卡时输出明确 gap 而不是用派克大衣顶替。

**P2 — 连续性、弧线与冲突**
9. continuity 模式支持“衣柜阶段（wardrobe_stage）”：允许每场替换单品集，但保留锚点物（如一件外套/配饰）与状态连续性；检测 economic_status/occupation 变化并要求阶段切换，否则 warning。
10. 增加约束冲突检测：historical + body-mod/sci-fi/霓虹 art direction、时代与 art_direction 不匹配、宗教/丧仪色彩与婚礼场合冲突；输出“模式拆分”建议（historical 基底 + fictional overlay）。

**P3 — 预算、文化与 prompt**
11. 成本模型公开：返回单品成本明细；要求 C 套比 A 套低 ≥10% 或复用 A 的 ≥2 件单品，否则重算并 warning。
12. 文化约束：为传统服饰建 culture 字段与场合（婚礼/丧仪/日常）；禁止跨文化随机混搭（C07 的 muff + moccasins + dashiki）；引用 MAT-0005/0006 的文化语义并提示 adinkra 丧服/节庆区别。
13. prompt 组装按 look_items 过滤卡片正文：剔除未选中的“worn in snow”“with leather jacket”等串文；逐场注入 state tokens；example 卡加 `[EXAMPLE]` 标记。
14. continuity 模式：顶层 `prompt_video` 不应拼接多场；应为每场输出独立 prompt_video（或明确字段指向 `scenes[].prompt_video`），并把 state tokens 写入每个单场 prompt。

## 5. 本报告的局限

- 每个案例仅运行一次，未做随机性/参数敏感性测试；结果反映当前 KB 与脚本版本。
- query 使用固定关键词（AND 语义），0 命中部分反映查询词表与 KB 词汇差距，不等同于 recommend 内部检索完全失败。
- 语义判定由人工评审完成，不是自动指标；C05/C06 的 continuity PASS 是脚本原生 verdict，本报告另行做叙事语义判断。
- 未进行 Obsidian UI 验证；所有英文 prompt 均为脚本实际输出节选，完整原文见 `raw/Cxx-recommend.json`。
- 本报告只评估，不修改 `scripts/`；改进建议需 lead/engineer 排期实现并由 validate.py + 回归测试验证。
