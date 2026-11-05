# P5-F 未解析关闭：5 typed_unresolved + 1 unresolved_wikilink

- 任务：task-94（P5-F 任务一）；日期 2026-11-05（Asia/Shanghai）
- 快照：**458 卡 = 224 内容 + 234 来源**；当前图工具运行 `scanned_files=489`，`typed_edges=742`，`typed_unresolved=0`，`unresolved_wikilinks={}`。
- 性质：**只读记录**；engineer 修的是 `scripts/graph_analyze.py`；本任务不改卡片/来源/脚本、不建卡、不造关系。
- 输入基线：`reports/P5E-BASELINE.md`、`reports/P5E-GRAPH-COMPARISON.md`（旧计数 5 + 1）。

## 0. 关闭结论

| 未解析项 | 旧数量 | 根因 | 当前 | 状态 |
|---|---:|---|---:|---|
| `typed_unresolved` | **5** | graph index 的 ID 正则只接受 `GAR-0001` 式纯数字 ID，`GAR-EXAMPLE-001` 未进入 `by_id`；5 个 LOOK 的 `look_items` 引用 example 卡时无法解析 | **0** | **CLOSED** |
| `unresolved_wikilink` | **1** | 旧解析器未剥离 inline-code/fenced code，把 `00-系统/关系类型.md` 里代码示例 `[[target]]` 当真实 wikilink | **0**（`{}`） | **CLOSED** |

- 共 **6/6** 关闭；未新建卡片/关系，未改内容卡；图节点仍 489，typed edges **737→742（+5）**（恢复 example 卡的 5 条 `look_items` typed 边，不新增语义关系）。

## 1. typed_unresolved 5：GAR-EXAMPLE-001 索引 bug

- 旧代码（P5-A 版）`ID_RE = ^(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-(\d{3,4})$`，只匹配纯数字 ID；graph 的 `by_id` 依赖该正则建立倒排索引。
- `GAR-EXAMPLE-001` 的文件/卡片是真实的 `example` 卡（`01-服装单品/上装/GAR-EXAMPLE-001-白色立领衬衫.md`），但 ID 含 `EXAMPLE`；解析 `look_items` 时 `by_id.get("GAR-EXAMPLE-001")` 为 None，产生 **5 条 typed_unresolved**。
- 受影响引用（5 个 LOOK，均为 `look_items` 指向 example 卡）：
  1. `LOOK-0006`（1977 伦敦朋克青年）
  2. `LOOK-0007`（当代雨夜调查者连续性造型）
  3. `LOOK-0017`（1977 朋克青年到 1980 年代职业人）
  4. `LOOK-0021`（当代雨夜调查者·四场连续性升级）
  5. `LOOK-EXAMPLE-001`（雨夜调查者）
- 分类：**graph index / ID 正则 bug**（数据卡真实存在；不是坏 ID、不是内容卡缺卡）。
- 影响：typed 边计数少 5；旧报告 `typed_edges=737` 少算 LOOK→example 的 5 条结构化边；不改变语义/可见链接（这些 LOOK 正文仍可见）。

### engineer 修复
`scripts/graph_analyze.py`（engineer，未改卡）：

```diff
-ID_RE = re.compile(r"^(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-(\d{3,4})$", re.I)
+ID_RE = re.compile(r"^((?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-[A-Z0-9][A-Z0-9-]*)$", re.I)
...
+        node_id = str((n.get("fm") or {}).get("id") or "")
+        if node_id:
+            by_id[node_id.upper()] = key
```

- 结果：`GAR-EXAMPLE-001` 进入 `by_id`；5 条 LOOK→example typed 边恢复；`typed_unresolved=0`。

## 2. unresolved_wikilink 1：inline-code 示例

- 旧解析器直接对整段 body 做 `WIKILINK_RE`，未排除 inline code/fenced code。
- `00-系统/关系类型.md` 的 visibility 规则含代码示例：`` `[[target]]` ``（行 123），被当作真实 wikilink；`target` 不是卡/来源 → **1 条 unresolved_wikilink**。
- 分类：**解析器未剥离 code span**（不是坏链、不是卡片编辑问题）；示例文本本身合法。

### engineer 修复
```diff
+CODE_SPAN = re.compile(r"`[^`\n]*`")
+FENCED = re.compile(r"(?ms)^```.*?^```")
...
+visible_body = FENCED.sub("", CODE_SPAN.sub("", body))
-for raw in WIKILINK_RE.findall(body):
+for raw in WIKILINK_RE.findall(visible_body):
```
- 结果：`unresolved_wikilinks={}`；示例代码不再污染可见链接计数。

## 3. 关闭验证（当前树）

```bash
python3 scripts/graph_analyze.py --root . --json /tmp/p5f_graph.json
# scanned_files 489; typed_edges 742; typed_unresolved 0; unresolved_wikilinks {}
```

- 与旧基线对比：typed_unresolved **5→0**，unresolved_wikilink **1→0**；typed_edges **737→742**（+5 恢复，不是新增关系）。
- 未新建卡/来源/关系；内容卡无改动（`git status` 无 01-09 修改由本任务产生）；graph tool 修复由 engineer 提交/保留。
- 恢复的 5 条边全部是 **LOOK→GAR-EXAMPLE-001 的 `look_items`**；example 卡仍是 `review_status=draft`/`evidence_status=example`，不能当历史证据；恢复索引≠提升证据等级。

## 4. 残余/边界

1. graph 工具的 `typed_edges` **不包含卡片 `relations` 字段**（只计 `source_ids`/`look_items`/`look_scene`/`key_garments`/`superseded/canonical`）；卡片 308 条 relations 需另计，不可相加。
2. 未解析归零只说明 ID 索引/code-span 解析修复；不代表 example 卡可作事实、也不代表其他关系候选已审核。
3. 当前 `scripts/graph_analyze.py` 仍为 engineer 工作区修改（未由本任务提交）；本任务只写报告，不改脚本。
