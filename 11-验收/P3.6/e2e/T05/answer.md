已运行 `query.py` 与 3 次 `recommend.py`（均 exit 0；产物在 `projects/space-repair/`）。recommender 对未来场景只给历史代用卡并警告"no future-base garment cards"，故 A/B/C 以库内唯一为 SCN-0006 编的 **LOOK-0011（interpretive）** 真实卡做状态变体。

## Brief
虚构角色：废弃空间站维修工（占位名 Vega）；22 世纪／fictional_world；低预算实拍科幻，STY-0009；时间、机构、重力/氧气制度 = unknown。

## A/B/C 造型（基座 LOOK-0011，跨态锚点 GAR-0038/GAR-0022/GAR-0050）
| 态 | 真实卡配置 | 状态锁 |
|---|---|---|
| **A 失重** | GAR-0038 + GAR-0022 + GAR-0050；GAR-0039 摘下挂腰、GAR-0037 不穿 | 背后系带固定防勾挂*；卷袖 |
| **B 维修** | A + GAR-0037 临时防护外层；GAR-0039 手提 | 油污、渗水、系带位置不变 |
| **C 危险** | 全套，GAR-0039 戴上（仅失压/危险区，合 continuity_lock） | 眼孔映警报光 |

`*`=设计推断。单品均 verified：GAR-0038 连体工作服→[SRC-0402](https://collections.vam.ac.uk/item/O1276042/)（V&A 1960s 花店罩衣）；GAR-0039→[SRC-0403](https://collections.vam.ac.uk/item/O1386978/)（V&A **1969 儿童手工纸浆玩具头盔**）；GAR-0037 消防外套→[SRC-0401](https://collections.vam.ac.uk/item/O1803042/)（1870–1900 日本 hikeshi-banten，结构性借用）；GAR-0022→[SRC-0123](https://fashionhistory.fitnyc.edu/wellington-boot/)（FIT）；GAR-0050→[SRC-0410](https://collections.vam.ac.uk/item/O1114148/)（V&A ENSA 布章）。

## English prompts
**A image:** fictional technician drifting in a zero-g derelict station corridor, pale-blue cotton coveralls with long back ties taped down (GAR-0038), rubber wellington boots (GAR-0022), small cloth badge (GAR-0050), white papier-mâché helmet clipped at belt, not worn, single cold work light, handheld medium shot.
**B image:** same technician crawling a greasy maintenance duct, improvised quilted firefighter-style coat (GAR-0037) over the coveralls, helmet carried under arm, rolled sleeves, water sheen, work-light close shot.
**C image:** alarm-lit airlock emergency, full layered look, white handmade papier-mâché helmet with two black eye holes worn (GAR-0039), red alarm glow in the eye holes; visibly a scavenged prop, not a sealed suit.
**video:** handheld drift→crawl→sprint progression; continuity lock: tie position, badge, boot grease, helmet eye-hole angle. **negative:** no sleek armor/LEDs/branding, no oxygen tanks or pressure seals implied, no helmet off in vacuum.

## 虚构/证据边界
verified 仅证明五件历史实物存在；LOOK-0011 与 SCN-0006 整体为 interpretive 虚构。纸浆头盔是玩具、消防外套为借用，**不代表真实舱外航天安全性**。缺口：无工作手套、工具腰带、供氧/通讯接口、真实压力服卡；recommend.py 无法自动召回 LOOK-0011，未来场景仅给时代级假设。
