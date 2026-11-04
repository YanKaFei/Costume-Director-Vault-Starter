# AUD-004 — P3.5 Macbeth slot fix（用既有卡，不改叙事）

原审计：`reports/GAP-ANALYSIS.md` AUD-004（S1 创作）——18 套 Macbeth look 中 M2-B 无 footwear、L3-A 无 torso 槽位；人工基准 2/18 不完整。本文件是**迁移补丁**：不重写 `11-验收/P3.5/Macbeth/LOOKS.md`（任务写入范围不含 11-验收），只给出可应用的 slot 修订。

| Look | 缺口 | 修订（既有卡） | 证据/定位 |
|---|---|---|---|
| M2-B（Macbeth / M2 罪恶危机 / B 伪装贵族层） | 无 footwear | `footwear = GAR-0081 皮靴`（15 世纪伦敦皮革踝靴，欧洲中世纪 analogue；lock: soft） | GAR-0081；SRC-0489；`11-验收/P3.5/Macbeth/LOOKS.md` M2-B |
| L3-A（Lady Macbeth / L3 覆灭 / A 梦游基础层） | 无 torso | `torso = GAR-0079 基尔特长袍`（interpretive，作为 chemise 外的躯干层；lock: soft） | GAR-0079；`11-验收/P3.5/Macbeth/LOOKS.md` L3-A |

- 不改叙事：M2-B 仍是“斗篷遮血迹”的伪装层；L3-A 仍是“剥离社会装饰”的梦游基础层（torso 只补合法性，不改变动作/台词/心理描述）。
- 不伪造史实：两卡都是欧洲中世纪/早期近代 analogue；L3-A 的 GAR-0079 为 interpretive，不当作 11 世纪苏格兰实证。
- 可应用方式：在 Look Bible 中按 `patch` 单件加入；或在重新生成 P3.5 LOOKS.md 时合并（需对应 owner 执行，不在本次只读范围）。

机器可读补丁：`aud-004-slotfix.json`。
