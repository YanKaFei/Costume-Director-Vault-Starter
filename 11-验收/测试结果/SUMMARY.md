# P2 验收测试 SUMMARY

- 运行时间：2026-11-04T01:38:16+08:00
- Python：3.9.6
- 测试数：18
- 结果目录：`11-验收/测试结果/`
- 重跑命令：`python3 scripts/run_acceptance.py`

## 知识库快照

- 卡片总数：235
  - `garment`: 36
  - `garment_part`: 11
  - `look`: 10
  - `material`: 7
  - `pattern`: 3
  - `period_region`: 11
  - `scene`: 4
  - `source`: 142
  - `style`: 11
- 来源卡：142

## 逐例结果

| 用例 | 标题 | 模式 | recommend exit | query exit | VERDICT | 失败项 |
| --- | --- | --- | --- | --- | --- | --- |
| T01 | 1930 年代上海知识分子：历史准确（historical） | standard | 0 | 0 | PASS | - |
| T02 | 1930 年代上海知识分子：艺术化再造（inspired，与 T01 对照） | standard | 0 | 0 | PASS | - |
| T03 | 现代雨夜调查者：雨前 / 雨中 / 室内三场连续性（fictional） | continuity | 0 | 0 | PASS | - |
| T04 | 当代舞者：动作空间、鞋底防滑、衣物扫动（dance movement） | standard | 0 | 0 | PASS | - |
| T05 | 未来虚构城市信使：明确虚构、不伪造史料（fictional） | standard | 0 | 0 | PASS | - |
| T06 | 低预算现实主义室内剧：复用单品、保留角色弧线 | standard | 0 | 0 | PASS | - |
| T07 | 暖光肖像：同一角色的冷暖光对照（warm lighting） | standard | 0 | 0 | PASS | - |
| T08 | 冷光肖像：同一角色的冷暖光对照（cool lighting） | standard | 0 | 0 | PASS | - |
| T09 | 雨夜湿衣特写：wetness 状态显式锁定 | standard | 0 | 0 | PASS | - |
| T10 | 阶层变化（上行）：寒门职员到体面绅士（1890s，class change） | standard | 0 | 0 | PASS | - |
| T11 | 阶层变化（下行）：富商之家到没落绅士（1890s，class change） | standard | 0 | 0 | PASS | - |
| T12 | 1920 年代爵士舞者：年代 + 舞蹈动作可行性 | standard | 0 | 0 | PASS | - |
| T13 | 低预算年代剧：有限置装量下的复用与美术替代 | standard | 0 | 0 | PASS | - |
| T14 | 冬季户外追逐：保暖、行动自由与鞋履安全 | standard | 0 | 0 | PASS | - |
| T15 | 当代建筑师：职业身份与正式度（modern realism） | standard | 0 | 0 | PASS | - |
| T16 | 表现主义黑色电影：美术风格驱动 vs 现实主义的冲突（inspired） | standard | 0 | 0 | PASS | - |
| T17 | 完整多场次服装连续性（4 场：干→湿→阴干→次日，含破损） | continuity | 0 | 0 | PASS | - |
| T18 | 当代生活流现实主义：日常场景的可信度（modern realism） | standard | 0 | 0 | PASS | - |

## 统计

- PASS：18 / 18
- FAIL：0 / 18

## 失败明细

- 无失败项。

## 知识库缺口汇总（来自脚本 warnings）

- 无脚本警告。

## 配对检查

- T02 → `stylisation_pair`：PASS（modes=historical/inspired historical phrase=True inspired phrase=True）
- T07 → `lighting_pair`：PASS（A item overlap=4, prompts differ=True）
- T08 → `lighting_pair`：PASS（A item overlap=4, prompts differ=True）
- T10 → `class_pair`：PASS（A missing/extra ids: GAR-0010, GAR-0011, GAR-0022, GAR-0023; per-look differences: GAR-0010, GAR-0011, GAR-0022, GAR-0023 | GAR-0010, GAR-0011, GAR-0022, GAR-0023 | none）
- T11 → `class_pair`：PASS（A missing/extra ids: GAR-0010, GAR-0011, GAR-0022, GAR-0023; per-look differences: GAR-0010, GAR-0011, GAR-0022, GAR-0023 | GAR-0010, GAR-0011, GAR-0022, GAR-0023 | none）

## 说明与限制

- 所有命令均为真实 `python3` 子进程，退出码与原始输出见各用例文件与 `raw/`。
- 测试只验证 P2 决策闭环（检索/评分/提示词/连续性）；Obsidian GUI、图片授权与史学正确性需另行人工核验。
- 若知识库新增卡片，必须重跑 `python3 scripts/run_acceptance.py` 更新本 SUMMARY。

