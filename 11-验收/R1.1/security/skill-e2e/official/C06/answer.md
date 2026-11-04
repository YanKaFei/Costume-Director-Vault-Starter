我已用 `path_guard` 以只读方式核对 `visual-index.csv`，并分别执行 `python3 scripts/query.py --id PRD-0003/GAR-0001/STR-0007 --json`（同时核对 SRC-0031、SRC-0100、SRC-0025）。

| 条目 | related_card | source_id | object_url |
|---|---|---|---|
| VIS-0001 | PRD-0003（1890s 语境） | SRC-0031 | https://www.metmuseum.org/art/collection/search/106702 |
| VIS-0003 | GAR-0001（和服） | SRC-0100 | https://www.metmuseum.org/art/collection/search/125953 |
| VIS-0005 | STR-0007（臀垫） | SRC-0025 | https://www.metmuseum.org/art/collection/search/157943 |

**关联核对**
- PRD-0003 自身来源为 SRC-0153、SRC-0174、SRC-0021；SRC-0031 是 VIS-0001 这件 Gym suit 的来源卡。`related_card` 表示年代或类型上的参照，不能当作同一来源链。
- GAR-0001 的来源正是 SRC-0100，两者一致。
- STR-0007 是“臀垫/bustle”，来源为 SRC-0137；VIS-0005 的 SRC-0025 是约 1885 年连衣裙。两者只是结构参照，不能把 SRC-0025 写成 STR-0007 的来源，也不能说该裙即 STR-0007 的原型。

**CC0 / 图像许可边界**
- 三条记录的 `rights_status=CC0 / Met Open Access (isPublicDomain=true)`，`public_domain_verified=true`；这是对对象 API 字段的逐件核验。按 README 的说明，对象为公共领域时，Met 对其图像声明 CC0。
- 索引只存链接，不下载、不内嵌图片；`image_url` 不等于许可，不能作为再分发授权，也不得热链、批量抓取或镜像。
- 使用前要回到 `object_url` 复核；该索引是原型记录，不构成法律意见或商业授权。
- 所有 SRC 编号均取自索引或 `query.py` 的输出；对 `MET-API` 条目不得伪造 SRC 卡。
