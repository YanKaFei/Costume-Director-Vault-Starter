# P2 验收测试 SUMMARY

- 运行时间：2026-11-04T15:51:45+08:00
- Python：3.9.6
- 测试数：45
- 结果目录：`11-验收/测试结果/`
- 重跑命令：`python3 scripts/run_acceptance.py`

## 知识库快照

- 卡片总数：363
  - `garment`: 83
  - `garment_part`: 11
  - `look`: 23
  - `material`: 8
  - `pattern`: 3
  - `period_region`: 11
  - `scene`: 16
  - `source`: 197
  - `style`: 11
- 来源卡：197

## 逐例结果

| 用例 | 标题 | 模式 | recommend exit | query exit | query hits | VERDICT | 失败项 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | 1930 年代上海知识分子：历史准确（historical） | standard | 0 | 0 | 6 | PASS | - |
| T02 | 1930 年代上海知识分子：艺术化再造（inspired，与 T01 对照） | standard | 0 | 0 | 5 | PASS | - |
| T03 | 现代雨夜调查者：雨前 / 雨中 / 室内三场连续性（fictional） | continuity | 0 | 0 | 6 | PASS | - |
| T04 | 当代舞者：动作空间、鞋底防滑、衣物扫动（dance movement） | standard | 0 | 0 | 6 | PASS | - |
| T05 | 未来虚构城市信使：明确虚构、不伪造史料（fictional） | standard | 0 | 0 | 1 | PASS | - |
| T06 | 低预算现实主义室内剧：复用单品、保留角色弧线 | standard | 0 | 0 | 2 | PASS | - |
| T07 | 暖光肖像：同一角色的冷暖光对照（warm lighting） | standard | 0 | 0 | 3 | PASS | - |
| T08 | 冷光肖像：同一角色的冷暖光对照（cool lighting） | standard | 0 | 0 | 3 | PASS | - |
| T09 | 雨夜湿衣特写：wetness 状态显式锁定 | standard | 0 | 0 | 5 | PASS | - |
| T10 | 阶层变化（上行）：寒门职员到体面绅士（1890s，class change） | standard | 0 | 0 | 1 | PASS | - |
| T11 | 阶层变化（下行）：富商之家到没落绅士（1890s，class change） | standard | 0 | 0 | 4 | PASS | - |
| T12 | 1920 年代爵士舞者：年代 + 舞蹈动作可行性 | standard | 0 | 0 | 5 | PASS | - |
| T13 | 低预算年代剧：有限置装量下的复用与美术替代 | standard | 0 | 0 | 6 | PASS | - |
| T14 | 冬季户外追逐：保暖、行动自由与鞋履安全 | standard | 0 | 0 | 4 | PASS | - |
| T15 | 当代建筑师：职业身份与正式度（modern realism） | standard | 0 | 0 | 6 | PASS | - |
| T16 | 表现主义黑色电影：美术风格驱动 vs 现实主义的冲突（inspired） | standard | 0 | 0 | 1 | PASS | - |
| T17 | 完整多场次服装连续性（4 场：干→湿→阴干→次日，含破损） | continuity | 0 | 0 | 1 | PASS | - |
| T18 | 当代生活流现实主义：日常场景的可信度（modern realism） | standard | 0 | 0 | 6 | PASS | - |
| T19 | 1940s 英国战时职员：历史模式不再崩溃 | standard | 0 | 0 | 3 | PASS | - |
| T20 | 1950s 美国家庭主妇：历史模式与年龄层级证据 | standard | 0 | 0 | 4 | PASS | - |
| T21 | 1960s 伦敦摄影师：青年文化历史造型 | standard | 0 | 0 | 2 | PASS | - |
| T22 | 1970s 伦敦朋克：历史模式修复崩溃探针 | standard | 0 | 0 | 2 | PASS | - |
| T23 | 1580s 意大利宫廷舞者：年代归一化修复假阴性 | standard | 0 | 0 | 6 | PASS | - |
| T24 | 拜占庭帝国晚期宫廷：区域/时代归一化不再假阴性 | standard | 0 | 0 | 6 | PASS | - |
| T25 | 太空歌剧女伶：未来基底缺卡必须显式警告 | standard | 0 | 0 | 1 | PASS | - |
| T26 | 急诊科护士夜班：职业服缺卡必须显式警告 | standard | 0 | 0 | 6 | PASS | - |
| T27 | 加纳-英国跨文化婚礼：文化场合警告与地域证据 | standard | 0 | 0 | 6 | PASS | - |
| T28 | 1930s 男职员雨夜：男性鞋履/雨具缺卡必须警告 | standard | 0 | 0 | 6 | PASS | - |
| T29 | 1930s 上海 + 赛博朋克义体：冲突必须显式识别 | standard | 0 | 0 | 6 | PASS | - |
| T30 | 自由文本 --brief：规则化剧本/人物解析 | standard | 0 | 0 | 6 | PASS | - |
| T31 | 急诊护士：职业匹配到护士制服/LOOK-0010，不用警察/白袍替代 | standard | 0 | 0 | 6 | PASS | - |
| T32 | 医生：职业匹配到医生白袍 GAR-0041 | standard | 0 | 0 | 5 | PASS | - |
| T33 | 警察：职业匹配到警察制服 GAR-0042 | standard | 0 | 0 | 3 | PASS | - |
| T34 | 厨师：职业匹配到厨师服 GAR-0043 | standard | 0 | 0 | 1 | PASS | - |
| T35 | 太空站维修工：职业匹配到连体工作服/安全头盔（GAR-0038/0039） | standard | 0 | 0 | 6 | PASS | - |
| T36 | 加纳-英国婚礼新郎：场合匹配（agbada/gele/LOOK-0013/0018） | standard | 0 | 0 | 6 | PASS | - |
| T37 | 1930s 上海雨夜：优先风衣/雨衣，不虚报 rainwear 缺口 | standard | 0 | 0 | 6 | PASS | - |
| T38 | 室内走廊：不得选极地派克，prompt 不得出现 worn in snow | standard | 0 | 0 | 5 | PASS | - |
| T39 | 明末清初：context_refs 不得引用 1770s/维多利亚等无关卡 | standard | 0 | 0 | 6 | PASS | - |
| T40 | query 排序：1930s 上海 top5 必须含 GAR-0031 且无 example | standard | 0 | 0 | 5 | PASS | - |
| T41 | query 去重：同名和服卡不得重复占据 top5 | standard | 0 | 0 | 5 | PASS | - |
| T42 | 职业同义词：巡警→police，A 套含 GAR-0042 且无旗袍/派克 | standard | 0 | 0 | 2 | PASS | - |
| T43 | 职业同义词：医师→doctor，A 套含 GAR-0041 且无韩服/长衫 | standard | 0 | 0 | 1 | PASS | - |
| T44 | 职业同义词：宇航员→astronaut，A 套含 GAR-0038/0039 | standard | 0 | 0 | 6 | PASS | - |
| T45 | 职业同义词：民警→police，A 套含 GAR-0042 且无旗袍/派克 | standard | 0 | 0 | 2 | PASS | - |

## 统计

- PASS：45 / 45
- FAIL：0 / 45
- query.py 命中总数：190（逐例：T01=6, T02=5, T03=6, T04=6, T05=1, T06=2, T07=3, T08=3, T09=5, T10=1, T11=4, T12=5, T13=6, T14=4, T15=6, T16=1, T17=1, T18=6, T19=3, T20=4, T21=2, T22=2, T23=6, T24=6, T25=1, T26=6, T27=6, T28=6, T29=6, T30=6, T31=6, T32=5, T33=3, T34=1, T35=6, T36=6, T37=6, T38=5, T39=6, T40=5, T41=5, T42=2, T43=1, T44=6, T45=2）
- 每个场景 query 步骤均返回 ≥1 命中：是

## 失败明细

- 无失败项。

## 知识库缺口汇总（来自脚本 warnings）

- ×10 period evidence is approximate/none for GAR-0079 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- ×7 wet/snow weather with delicate footwear GAR-0035 — suggested resolution: use leather/rubber boots or declare a dry interior shot
- ×7 No cheaper distinct combination was available in the vault; Look C is an art-direction alternative at equivalent cost, explicitly explained.
- ×5 cards document other regions for GAR-0035, GAR-0045, GAR-0047, GAR-0048, GAR-0060 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×4 period evidence is era-level (century bucket) for GAR-0045, GAR-0047; exact-decade cards are missing
- ×4 fictional/future setting has no future-base garment cards; current pieces are historical/contemporary stand-ins
- ×3 the vault has no 'journalist and writer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×3 no reliable style card for art direction 'restrained urban noir'
- ×3 the vault has no 'private investigator'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×3 no reliable style card for art direction 'gritty urban realism'
- ×3 cards document other regions for GAR-0022 (requested united_states); cross-region borrowing is flagged, not silently accepted
- ×3 period evidence is approximate/none for GAR-0079, GAR-0082 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- ×3 no reliable style card for art direction 'restrained historical noir'
- ×2 no reliable style card for art direction 'restrained urban period drama'
- ×2 the vault has no 'courier'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×2 period evidence is approximate/none for GAR-0045 (requested 1890s); treat these as era-level hypotheses, not exact period matches
- ×2 the vault has no 'student then clerk'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×2 no reliable style card for art direction 'intimate low-budget period drama'
- ×2 the vault has no 'clerk'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×2 no reliable style card for art direction 'handheld documentary, cool fluorescent realism'
- ×2 cards document other regions for GAR-0036, GAR-0041, GAR-0044, GAR-0045, GAR-0048, GAR-0050, GAR-0079, GAR-0082 (requested urban china shanghai); cross-region borrowing is flagged, not silently accepted
- ×2 no reliable style card for art direction 'documentary wedding photography, natural light'
- ×2 cross-cultural wedding brief: confirm which ceremony (traditional / white wedding / both) and whether kente or adinkra is appropriate; the vault has no wedding-ceremony garment cards
- ×2 no reliable style card for art direction 'clinical realism'
- ×2 cards document other regions for GAR-0022, GAR-0041, GAR-0044, GAR-0076, GAR-0079 (requested urban china); cross-region borrowing is flagged, not silently accepted
- ×2 period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0047; exact-decade cards are missing
- ×2 cards document other regions for GAR-0022, GAR-0035, GAR-0045, GAR-0047, GAR-0048 (requested shanghai); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'stylised period drama, heightened contrast and saturated accents'
- ×1 identity/economic arc present but one locked wardrobe spans all scenes; wardrobe-stage change not modeled
- ×1 the vault has no 'contemporary dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable period/region context card after period/region normalization (requested: future_fictional / fictional city)
- ×1 period evidence is approximate/none for GAR-0006, GAR-0014, GAR-0022, GAR-0045, GAR-0079 (requested future_fictional); treat these as era-level hypotheses, not exact period matches
- ×1 no reliable style card for art direction 'naturalistic low-budget realism'
- ×1 period evidence is approximate/none for GAR-0079, GAR-0080, GAR-0082 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- ×1 cards document other regions for GAR-0022, GAR-0023, GAR-0076, GAR-0079, GAR-0080, GAR-0082 (requested east_asia); cross-region borrowing is flagged, not silently accepted
- ×1 period evidence is approximate/none for GAR-0079, GAR-0080 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- ×1 cards document other regions for GAR-0006, GAR-0022, GAR-0023, GAR-0045, GAR-0077, GAR-0079 (requested east_asia); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'naturalistic tenement period drama'
- ×1 period evidence is era-level (century bucket) for GAR-0008, GAR-0010, GAR-0011, GAR-0021, GAR-0023; exact-decade cards are missing
- ×1 cards document other regions for GAR-0045 (requested united_states); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'genteel period drama'
- ×1 period evidence is era-level (century bucket) for GAR-0010, GAR-0011, GAR-0017, GAR-0022, GAR-0023; exact-decade cards are missing
- ×1 no reliable style card for art direction '1920s dance-hall glamour'
- ×1 the vault has no 'jazz dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable style card for art direction 'cold naturalistic thriller'
- ×1 cards document other regions for GAR-0019, GAR-0023 (requested northern europe); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'clean minimalist realism'
- ×1 cards document other regions for GAR-0022, GAR-0069, GAR-0079 (requested east_asia); cross-region borrowing is flagged, not silently accepted
- ×1 the vault has no 'architect'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable style card for art direction 'expressionist noir, distorted shadows, stark geometry'
- ×1 period evidence is era-level (century bucket) for GAR-0008, GAR-0010, GAR-0021, GAR-0022, GAR-0023; exact-decade cards are missing
- ×1 cards document other regions for GAR-0022, GAR-0045 (requested united_states); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'naturalistic slice-of-life realism'
- ×1 cards document other regions for GAR-0006, GAR-0022, GAR-0023, GAR-0045, GAR-0076, GAR-0077 (requested east_asia); cross-region borrowing is flagged, not silently accepted
- ×1 the vault has no 'primary school teacher'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable style card for art direction 'restrained wartime realism'
- ×1 period evidence is era-level (century bucket) for GAR-0022, GAR-0045, GAR-0058; exact-decade cards are missing
- ×1 the vault has no 'factory clerk'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable style card for art direction '1950s domestic realism'
- ×1 period evidence is era-level (century bucket) for GAR-0023; exact-decade cards are missing
- ×1 no reliable style card for art direction 'swinging sixties youth culture'
- ×1 period evidence is era-level (century bucket) for GAR-0022, GAR-0035, GAR-0054; exact-decade cards are missing
- ×1 the vault has no 'photographer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable style card for art direction '1970s London punk'
- ×1 period evidence is era-level (century bucket) for GAR-0035, GAR-0045, GAR-0046, GAR-0047, GAR-0052, GAR-0053; exact-decade cards are missing
- ×1 the vault has no 'punk musician'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable period/region context card after period/region normalization (requested: 1580s / italy)
- ×1 no reliable style card for art direction 'renaissance court, candlelight and brocade'
- ×1 period evidence is approximate/none for GAR-0008 (requested 1580s); treat these as era-level hypotheses, not exact period matches
- ×1 period evidence is era-level (century bucket) for GAR-0002, GAR-0013, GAR-0024, GAR-0062; exact-decade cards are missing
- ×1 the vault has no 'court dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 dance/action scene with heeled or backless footwear GAR-0024 — suggested resolution: choose flat secure shoes; if no card exists, log the safety gap and test the movement
- ×1 no reliable style card for art direction 'late byzantine court, gold and deep colours'
- ×1 period evidence is era-level (century bucket) for GAR-0009; exact-decade cards are missing
- ×1 looks are missing required layers: footwear (no invented replacements)
- ×1 only 1 distinct look(s) could be assembled after hard constraints; inspect the knowledge-base gaps above
- ×1 no reliable period/region context card after period/region normalization (requested: 23rd century / orbital opera house)
- ×1 period evidence is approximate/none for GAR-0005, GAR-0022, GAR-0063, GAR-0079 (requested 23rd century); treat these as era-level hypotheses, not exact period matches
- ×1 the vault has no 'orbital opera singer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 the vault has no 'male bank clerk'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 male-presenting brief but the look uses documented women's pieces (GAR-0031, GAR-0035); men's/neutral cards are missing for this category
- ×1 no reliable style card for art direction 'historical noir + cyberpunk neon and body modification'
- ×1 the vault has no 'newspaper editor and body-modded courier'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 historical fidelity conflicts with science-fiction / body-mod / neon elements in the brief — suggested resolution: split the brief: historical base costume + explicit fictional overlay; or set fidelity_mode=inspired/fictional and declare the anachronism
- ×1 no reliable style card for art direction 'noir'
- ×1 cards document other regions for GAR-0023, GAR-0042 (requested britain); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable style card for art direction 'warm documentary kitchen realism'
- ×1 cards document other regions for GAR-0014, GAR-0043 (requested italy); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable period/region context card after period/region normalization (requested: 22nd century / derelict space station)
- ×1 no reliable style card for art direction 'minimal staged science fiction'
- ×1 period evidence is approximate/none for GAR-0022, GAR-0023, GAR-0037, GAR-0038, GAR-0039, GAR-0045, GAR-0079, GAR-0080 (requested 22nd century); treat these as era-level hypotheses, not exact period matches
- ×1 no reliable period/region context card after period/region normalization (requested: 1644 late Ming early Qing / jiangnan china)
- ×1 no reliable style card for art direction '文人水墨、克制、低饱和'
- ×1 period evidence is approximate/none for GAR-0071 (requested 1644 late Ming early Qing); treat these as era-level hypotheses, not exact period matches
- ×1 period evidence is era-level (century bucket) for GAR-0024, GAR-0028, GAR-0049, GAR-0062; exact-decade cards are missing
- ×1 cards document other regions for GAR-0024, GAR-0028, GAR-0049, GAR-0062 (requested jiangnan china); cross-region borrowing is flagged, not silently accepted
- ×1 the vault has no '书院教师、江南文人'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 no reliable style card for art direction 'theatre period drama'
- ×1 cards document other regions for GAR-0035, GAR-0058 (requested japan); cross-region borrowing is flagged, not silently accepted
- ×1 the vault has no 'dancer'-specific garment cards; generic pieces are used and no other profession's uniform is substituted
- ×1 cards document other regions for GAR-0022, GAR-0023, GAR-0042, GAR-0045, GAR-0079, GAR-0082 (requested china); cross-region borrowing is flagged, not silently accepted
- ×1 no reliable period/region context card after period/region normalization (requested: 22nd century / orbital station)
- ×1 period evidence is approximate/none for GAR-0022, GAR-0037, GAR-0038, GAR-0039, GAR-0045, GAR-0079, GAR-0080 (requested 22nd century); treat these as era-level hypotheses, not exact period matches
- ×1 no reliable style card for art direction 'documentary urban realism'
- ×1 period evidence is approximate/none for GAR-0082 (requested contemporary); treat these as era-level hypotheses, not exact period matches
- ×1 cards document other regions for GAR-0022, GAR-0023, GAR-0042, GAR-0045, GAR-0055, GAR-0082 (requested china); cross-region borrowing is flagged, not silently accepted

## 配对检查

- T02 → `stylisation_pair`：PASS（modes=historical/inspired historical phrase=True inspired phrase=True）
- T07 → `lighting_pair`：PASS（A item overlap=4, prompts differ=True）
- T08 → `lighting_pair`：PASS（A item overlap=4, prompts differ=True）
- T10 → `class_pair`：PASS（A missing/extra ids: GAR-0017, GAR-0021, GAR-0045; per-look differences: GAR-0017, GAR-0021, GAR-0045 | GAR-0017, GAR-0021, GAR-0045 | GAR-0007, GAR-0008, GAR-0017, GAR-0022, GAR-0023, GAR-0045）
- T11 → `class_pair`：PASS（A missing/extra ids: GAR-0017, GAR-0021, GAR-0045; per-look differences: GAR-0017, GAR-0021, GAR-0045 | GAR-0017, GAR-0021, GAR-0045 | GAR-0007, GAR-0008, GAR-0017, GAR-0022, GAR-0023, GAR-0045）

## 说明与限制

- 所有命令均为真实 `python3` 子进程，退出码与原始输出见各用例文件与 `raw/`。
- 测试只验证 P2 决策闭环（检索/评分/提示词/连续性）；Obsidian GUI、图片授权与史学正确性需另行人工核验。
- 若知识库新增卡片，必须重跑 `python3 scripts/run_acceptance.py` 更新本 SUMMARY。

