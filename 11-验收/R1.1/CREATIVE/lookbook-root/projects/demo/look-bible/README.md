# Look Bible — %s

项目级 Look Bible（不写入 01–09 公共卡）。

状态：Draft → Proposed → Approved；Approved 需 human reviewer + signature JSON。
anchors：slot 级 lock `hard`/`soft`；Approved 后 hard anchor 不能被静默覆盖。
命令：`python3 scripts/lookbook.py init|add|patch|propose|approve|diff|validate --project <slug>`
