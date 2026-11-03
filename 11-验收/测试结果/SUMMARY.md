# P2 验收测试 SUMMARY

- 运行时间：2026-11-04T02:25:39+08:00
- Python：3.9.6
- 测试数：30
- 结果目录：`11-验收/测试结果/`
- 重跑命令：`python3 scripts/run_acceptance.py`

## 知识库快照

- 卡片总数：328
  - `garment`: 71
  - `garment_part`: 11
  - `look`: 23
  - `material`: 8
  - `pattern`: 3
  - `period_region`: 11
  - `scene`: 16
  - `source`: 174
  - `style`: 11
- 来源卡：174

## 逐例结果

| 用例 | 标题 | 模式 | recommend exit | query exit | query hits | VERDICT | 失败项 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | 1930 年代上海知识分子：历史准确（historical） | standard | 0 | 0 | 6 | PASS | - |
| T02 | 1930 年代上海知识分子：艺术化再造（inspired，与 T01 对照） | standard | 0 | 0 | 5 | PASS | - |
| T03 | 现代雨夜调查者：雨前 / 雨中 / 室内三场连续性（fictional） | continuity | 0 | 0 | 1 | PASS | - |
| T04 | 当代舞者：动作空间、鞋底防滑、衣物扫动（dance movement） | standard | 0 | 0 | 6 | PASS | - |
| T05 | 未来虚构城市信使：明确虚构、不伪造史料（fictional） | standard | 0 | 0 | 2 | PASS | - |
| T06 | 低预算现实主义室内剧：复用单品、保留角色弧线 | standard | 0 | 0 | 2 | PASS | - |
| T07 | 暖光肖像：同一角色的冷暖光对照（warm lighting） | standard | 0 | 0 | 5 | PASS | - |
| T08 | 冷光肖像：同一角色的冷暖光对照（cool lighting） | standard | 0 | 0 | 5 | PASS | - |
| T09 | 雨夜湿衣特写：wetness 状态显式锁定 | standard | 0 | 0 | 5 | PASS | - |
| T10 | 阶层变化（上行）：寒门职员到体面绅士（1890s，class change） | standard | 0 | 0 | 1 | PASS | - |
| T11 | 阶层变化（下行）：富商之家到没落绅士（1890s，class change） | standard | 0 | 0 | 4 | PASS | - |
| T12 | 1920 年代爵士舞者：年代 + 舞蹈动作可行性 | standard | 0 | 0 | 5 | PASS | - |
| T13 | 低预算年代剧：有限置装量下的复用与美术替代 | standard | 0 | 0 | 6 | PASS | - |
| T14 | 冬季户外追逐：保暖、行动自由与鞋履安全 | standard | 0 | 0 | 2 | PASS | - |
| T15 | 当代建筑师：职业身份与正式度（modern realism） | standard | 0 | 0 | 6 | PASS | - |
| T16 | 表现主义黑色电影：美术风格驱动 vs 现实主义的冲突（inspired） | standard | 0 | 0 | 2 | PASS | - |
| T17 | 完整多场次服装连续性（4 场：干→湿→阴干→次日，含破损） | continuity | 0 | 0 | 1 | PASS | - |
| T18 | 当代生活流现实主义：日常场景的可信度（modern realism） | standard | 0 | 0 | 5 | PASS | - |
| T19 | 1940s 英国战时职员：历史模式不再崩溃 | standard | 0 | 0 | 3 | PASS | - |
| T20 | 1950s 美国家庭主妇：历史模式与年龄层级证据 | standard | 0 | 0 | 4 | PASS | - |
| T21 | 1960s 伦敦摄影师：青年文化历史造型 | standard | 0 | 0 | 2 | PASS | - |
| T22 | 1970s 伦敦朋克：历史模式修复崩溃探针 | standard | 0 | 0 | 2 | PASS | - |
| T23 | 1580s 意大利宫廷舞者：年代归一化修复假阴性 | standard | 0 | 0 | 6 | PASS | - |
| T24 | 拜占庭帝国晚期宫廷：区域/时代归一化不再假阴性 | standard | 0 | 0 | 6 | PASS | - |
| T25 | 太空歌剧女伶：未来基底缺卡必须显式警告 | standard | 0 | 0 | 2 | PASS | - |
| T26 | 急诊科护士夜班：职业服缺卡必须显式警告 | standard | 0 | 0 | 6 | PASS | - |
| T27 | 加纳-英国跨文化婚礼：文化场合警告与地域证据 | standard | 0 | 0 | 6 | PASS | - |
| T28 | 1930s 男职员雨夜：男性鞋履/雨具缺卡必须警告 | standard | 0 | 0 | 6 | PASS | - |
| T29 | 1930s 上海 + 赛博朋克义体：冲突必须显式识别 | standard | 0 | 0 | 6 | PASS | - |
| T30 | 自由文本 --brief：规则化剧本/人物解析 | standard | 0 | 0 | 6 | PASS | - |

## 统计

- PASS：30 / 30
- FAIL：0 / 30
- query.py 命中总数：124（逐例：T01=6, T02=5, T03=1, T04=6, T05=2, T06=2, T07=5, T08=5, T09=5, T10=1, T11=4, T12=5, T13=6, T14=2, T15=6, T16=2, T17=1, T18=5, T19=3, T20=4, T21=2, T22=2, T23=6, T24=6, T25=2, T26=6, T27=6, T28=6, T29=6, T30=6）
- 每个场景 query 步骤均返回 ≥1 命中：是

## 失败明细

- 无失败项。

## 知识库缺口汇总（来自脚本 warnings）

- ×18 no upper_body candidates retrieved
- ×18 no lower_body candidates retrieved
- ×11 No cheaper distinct combination was available in the vault; Look C is an art-direction alternative at equivalent cost, explicitly explained.
- ×5 period evidence is approximate/none for GAR-0037 (requested 1930s); treat these as era-level hypotheses, not exact period matches
- ×5 outerwear GAR-0037 has no documented weather protection; rainwear cards are missing
- ×5 outerwear GAR-0041 has no documented weather protection; rainwear cards are missing
- ×4 wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- ×3 no occupational garment cards match 'journalist and writer'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×3 no reliable style card for art direction 'restrained urban noir'
- ×3 no occupational garment cards match 'private investigator'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×3 cards document other regions for GAR-0022, GAR-0041, GAR-0042, GAR-0044 (requested east_asia); cross-region borrowing is flagged, not silently accepted
- ×2 no reliable style card for art direction 'restrained urban period drama'
- ×2 no occupational garment cards match 'courier'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×2 fictional/future setting has no future-base garment cards; current pieces are historical/contemporary stand-ins
- ×2 no occupational garment cards match 'student then clerk'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×2 cards document other regions for GAR-0022 (requested united_states); cross-region borrowing is flagged, not silently accepted
- ×2 no occupational garment cards match 'architect'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×2 period evidence is era-level (century bucket) for GAR-0022; exact-decade cards are missing
- ×1 period evidence is era-level (century bucket) for GAR-0022, GAR-0045; exact-decade cards are missing
- ×1 cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'stylised period drama, heightened contrast and saturated accents'
- ×1 cards document other regions for GAR-0035, GAR-0058, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 identity/economic arc present but one locked wardrobe spans all scenes; wardrobe-stage change not modeled
- ×1 no reliable period/region context card after period/region normalization (requested: future_fictional / fictional city)
- ×1 period evidence is approximate/none for GAR-0014, GAR-0022, GAR-0041, GAR-0042, GAR-0043, GAR-0044, GAR-0056 (requested future_fictional); treat these as era-level hypotheses, not exact period matches
- ×1 no reliable style card for art direction 'naturalistic low-budget realism'
- ×1 no reliable style card for art direction 'gritty urban realism'
- ×1 cards document other regions for GAR-0022, GAR-0036, GAR-0041, GAR-0042, GAR-0044 (requested east_asia); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'naturalistic tenement period drama'
- ×1 period evidence is era-level (century bucket) for GAR-0008, GAR-0010, GAR-0017, GAR-0019, GAR-0023; exact-decade cards are missing
- ×1 no reliable style card for art direction 'genteel period drama'
- ×1 period evidence is era-level (century bucket) for GAR-0010, GAR-0011, GAR-0017, GAR-0022, GAR-0023; exact-decade cards are missing
- ×1 no reliable style card for art direction '1920s dance-hall glamour'
- ×1 no occupational garment cards match 'jazz dancer'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction 'intimate low-budget period drama'
- ×1 no occupational garment cards match 'clerk'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction 'cold naturalistic thriller'
- ×1 cards document other regions for GAR-0019, GAR-0041, GAR-0042, GAR-0044 (requested northern europe); cross-region borrowing is flagged, not silently accepted
- ×1 no occupational garment cards match 'bounty hunter'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction 'clean minimalist realism'
- ×1 no reliable style card for art direction 'expressionist noir, distorted shadows, stark geometry'
- ×1 period evidence is era-level (century bucket) for GAR-0008, GAR-0010, GAR-0017, GAR-0022, GAR-0023; exact-decade cards are missing
- ×1 no reliable style card for art direction 'naturalistic slice-of-life realism'
- ×1 no occupational garment cards match 'primary school teacher'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction 'restrained wartime realism'
- ×1 period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0058; exact-decade cards are missing
- ×1 no occupational garment cards match 'factory clerk'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction '1950s domestic realism'
- ×1 period evidence is era-level (century bucket) for GAR-0023; exact-decade cards are missing
- ×1 no occupational garment cards match 'homemaker'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction 'swinging sixties youth culture'
- ×1 period evidence is era-level (century bucket) for GAR-0022, GAR-0035, GAR-0047; exact-decade cards are missing
- ×1 no occupational garment cards match 'photographer'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction '1970s London punk'
- ×1 period evidence is era-level (century bucket) for GAR-0035, GAR-0045, GAR-0046, GAR-0047, GAR-0052, GAR-0053; exact-decade cards are missing
- ×1 no reliable period/region context card after period/region normalization (requested: 1580s / italy)
- ×1 no reliable style card for art direction 'renaissance court, candlelight and brocade'
- ×1 period evidence is approximate/none for GAR-0008 (requested 1580s); treat these as era-level hypotheses, not exact period matches
- ×1 period evidence is era-level (century bucket) for GAR-0002, GAR-0013, GAR-0024, GAR-0062; exact-decade cards are missing
- ×1 dance/action scene with heeled or backless footwear GAR-0024 — suggested resolution: choose flat secure shoes; if no card exists, log the safety gap and test the movement
- ×1 no footwear candidates retrieved
- ×1 no reliable style card for art direction 'late byzantine court, gold and deep colours'
- ×1 period evidence is era-level (century bucket) for GAR-0009; exact-decade cards are missing
- ×1 looks are missing required layers: footwear, outerwear (no invented replacements)
- ×1 no occupational garment cards match 'court attendant'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 only 1 distinct look(s) could be assembled after hard constraints; inspect the knowledge-base gaps above
- ×1 no reliable period/region context card after period/region normalization (requested: 23rd century / orbital opera house)
- ×1 period evidence is approximate/none for GAR-0022, GAR-0031, GAR-0042, GAR-0044 (requested 23rd century); treat these as era-level hypotheses, not exact period matches
- ×1 no reliable style card for art direction 'handheld documentary, cool fluorescent realism'
- ×1 cards document other regions for GAR-0014, GAR-0022, GAR-0041, GAR-0042, GAR-0043, GAR-0044 (requested urban china shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 no occupational garment cards match '急诊科护士'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 no reliable style card for art direction 'documentary wedding photography, natural light'
- ×1 cards document other regions for GAR-0014, GAR-0042, GAR-0043 (requested london and accra); cross-region borrowing is flagged, not silently accepted
- ×1 cross-cultural wedding brief: confirm which ceremony (traditional / white wedding / both) and whether kente or adinkra is appropriate; the vault has no wedding-ceremony garment cards
- ×1 wedding/ceremonial brief lacks ceremonial-grade garment cards; confirm cultural details with the family/community before shoot
- ×1 no reliable style card for art direction 'restrained historical noir'
- ×1 period evidence is era-level (century bucket) for GAR-0045; exact-decade cards are missing
- ×1 cards document other regions for GAR-0035, GAR-0045, GAR-0048, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 no occupational garment cards match 'male bank clerk'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 male-presenting brief but the look uses documented women's pieces (GAR-0031, GAR-0035); men's/neutral cards are missing for this category
- ×1 no reliable style card for art direction 'historical noir + cyberpunk neon and body modification'
- ×1 cards document other regions for GAR-0022, GAR-0035, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 no occupational garment cards match 'newspaper editor and body-modded courier'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 historical fidelity conflicts with science-fiction / body-mod / neon elements in the brief — suggested resolution: split the brief: historical base costume + explicit fictional overlay; or set fidelity_mode=inspired/fictional and declare the anachronism
- ×1 no reliable style card for art direction 'noir'
- ×1 cards document other regions for GAR-0022, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 no occupational garment cards match 'journalist / editor'; the look is assembled from generic/historical pieces and must be reviewed as a non-occupational substitute
- ×1 wet/snow weather with delicate footwear GAR-0060 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- ×1 brief parser left these fields unknown: season

## 配对检查

- T02 → `stylisation_pair`：PASS（modes=historical/inspired historical phrase=True inspired phrase=True）
- T07 → `lighting_pair`：PASS（A item overlap=3, prompts differ=True）
- T08 → `lighting_pair`：PASS（A item overlap=3, prompts differ=True）
- T10 → `class_pair`：PASS（A missing/extra ids: none; per-look differences: none | GAR-0010, GAR-0011, GAR-0017, GAR-0019 | GAR-0007, GAR-0008, GAR-0017, GAR-0019, GAR-0022, GAR-0023 (A is the same anchor look; class difference is in B/C)）
- T11 → `class_pair`：PASS（A missing/extra ids: none; per-look differences: none | GAR-0010, GAR-0011, GAR-0017, GAR-0019 | GAR-0007, GAR-0008, GAR-0017, GAR-0019, GAR-0022, GAR-0023 (A is the same anchor look; class difference is in B/C)）

## 说明与限制

- 所有命令均为真实 `python3` 子进程，退出码与原始输出见各用例文件与 `raw/`。
- 测试只验证 P2 决策闭环（检索/评分/提示词/连续性）；Obsidian GUI、图片授权与史学正确性需另行人工核验。
- 若知识库新增卡片，必须重跑 `python3 scripts/run_acceptance.py` 更新本 SUMMARY。

