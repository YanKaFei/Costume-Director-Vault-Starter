## 查询结果

执行命令：

```bash
python3 scripts/query.py --id GAR-0008 \
  --relation-type claim_supported_by \
  --related-to SRC-0109 \
  --confidence high --json
```

### 类型化关系

- **主体卡片**：`GAR-0008`（马甲 / waistcoat）
- **关系类型**：`claim_supported_by`
- **关系目标**：`SRC-0109`
- **目标名称**：FIT：vest/waistcoat（马甲）
- **目标类型**：`source`
- **证据等级**：`verified`
- **置信度**：`high`
- **方向**：`outgoing`（另有一条等价的 `subject_to_object` candidate 记录，`review_status: migration_ready`）
- **规则来源**：`R-SOURCE-IDS`
- **来源 ID**：`SRC-0109`

### 真实来源文件路径

关系解析出的 Vault 相对路径为：

```text
04-来源/SRC-0109-FIT-vest-waistcoat.md
```

我已通过 `scripts/path_guard.py check` 验证，并确认该文件实际存在；绝对路径为：

```text
/Users/coffee/Desktop/Costume-Director-Vault-Starter/04-来源/SRC-0109-FIT-vest-waistcoat.md
```

### 来源卡信息

- **ID**：`SRC-0109`
- **名称**：FIT：vest/waistcoat（马甲）
- **英文名称**：`vest-waistcoat | Fashion History Timeline`
- **发布方**：Fashion History Timeline, FIT/SUNY
- **来源类型**：`academic_reference`
- **证据状态**：`verified`
- **审核状态**：`reviewed`
- **许可状态**：`link_only`
- **URL**：https://fashionhistory.fitnyc.edu/vest-waistcoat/
- **访问日期 / HTTP 记录**：2026-11-04，卡片注明实测 HTTP 200

结论：`GAR-0008` 的高置信度、已验证 `claim_supported_by` 类型化关系明确指向 **`SRC-0109`**，其真实来源文件是 **`04-来源/SRC-0109-FIT-vest-waistcoat.md`**。该结论来自 `query.py` 返回的类型化关系字段，而不是正文 wikilink 推断。
