# P4-VISUAL — CC0 博物馆视觉索引（Met Collection API 原型）

- 版本：2026-11-04（Asia/Shanghai）
- 状态：**PROTOTYPE / 原型**；28 条已核对 `isPublicDomain=true`，不下载、不内嵌图片。
- 文件：
  - `visual-index.csv` — 主索引（28 行，字段见下）
  - `verification-log.csv` — 逐条 URL/许可核验记录（API HTTP、图像 HTTP、isPublicDomain、access_status）
  - `README.md` — 本文件
  - `docs/VISUAL-REFERENCE.md` — 给设计/美术/导演团队的使用说明与许可边界

## 1. 用途与边界

**用途**：为服装设计、角色造型和镜头参考提供一个**可检索、可溯源、标明 CC0 状态**的博物馆图像链接索引；每条都能回链到知识库卡片（GAR/STR/PRD/STY 等），并与来源 URL 分离。

**边界（重要）**：

1. **只存链接，不下载、不内嵌**。CSV 中的 `image_url` 是 Met 官方图像 URL；Vault 内没有复制任何博物馆图片。
2. **图像 URL ≠ 许可**。即便对象 `isPublicDomain=true`，使用前仍应回到 `object_url`/Met Open Access 页面核对；本索引只声明该对象的 API 字段 `isPublicDomain` 为 true，不替代独立法律审查。
3. **不把 `image_url` 当作可再分发许可**；不要批量抓取、热链或镜像到其他站点。
4. 本索引是**原型**：`source_id` 为 `MET-API` 的条目尚未建立独立 `SRC-` 来源卡（见 §6 缺口）；引用时应以 `object_id`/`object_url` 为准，不能伪造 SRC 编号。

## 2. 数据来源与方法

- API 基址：`https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}`；检索用 `/public/collection/v1.1/search`（按服装/配饰关键词 + `departmentId=8` + `hasImages=true`）。
- 选件标准：
  - API `isPublicDomain=true`（逐件核对）；
  - `primaryImageSmall` 非空（可提供官方图像 URL）；
  - 覆盖多个品类（连衣裙、外套、马甲、胸衣、靴、鞋、扇、阳伞、和服、束腰长袍等）与年代（4–7 世纪至 1890 年代）。
- 核验（2026-11-04）：
  - 28/28 件：API `isPublicDomain=true`；
  - 28/28 件：对象 API HTTP **200**；
  - 28/28 件：`image_url` HTTP **200**（VIS-0008 / object 159244 首次请求超时，重试 200；见 verification-log）；
  - **inaccessible = 0**；若再次出现失败，`access_status=inaccessible` 并保留原始状态码。

## 3. 字段说明（visual-index.csv）

| 字段 | 说明 |
|---|---|
| `visual_id` | 本索引稳定 ID：`VIS-0001`…`VIS-0028` |
| `object_id` | Met objectID（权威键，可重建） |
| `title` / `date` / `culture` | Met API 的标题/年代/文化（缺失写 unknown） |
| `classification` | Met `classification`；Costume Institute 常为空时用 `department / objectName` 派生并标明 |
| `structure_features` | **metadata-only**：objectName、medium、dimensions/measurements；领/袖/廓形等细节未从图像推断（因为不下载图片），不编造 |
| `keywords_zh` / `keywords_en` | 类型/材质/文化/年代关键词，用于检索 |
| `image_url` | Met 官方图像 URL（仅链接，不下载） |
| `rights_status` | `CC0 / Met Open Access (isPublicDomain=true)` |
| `public_domain_verified` | `true` 表示已逐件通过 API 核验（核验日期见 README/verification-log） |
| `related_card` | 可关联的知识库卡 ID（GAR/STR/MAT/LOOK 等）；空白表示未建立可靠关联 |
| `source_id` | 已有来源卡时填 `SRC-xxxx`；原型阶段未建卡时填 `MET-API`（以 object_id 为锚） |
| `object_url` | Met 对象页（人工核对/引用入口） |
| `api_http_status` / `image_http_status` | 本次核验的 HTTP 状态码 |
| `access_status` | `ok` / `inaccessible` |
| `verification_note` | 核验说明与限制 |

## 4. 交叉关联（≥10 条）

- **27/28 条**有 `related_card`；共 **14 个唯一真实卡 ID**：
  `GAR-0001, GAR-0008, GAR-0015, GAR-0017, GAR-0022, GAR-0047, GAR-0061, PRD-0003, STR-0004, STR-0007, STR-0008, STY-0001, STY-0002, LOOK-0002`
- 仅 VIS-0024（Met 156570 扇子）暂无对应卡（本库无扇类卡），保留空白而不是硬配。
- 关联是**类型/年代相近的参考**，不是“该馆藏就是该卡的原型”；具体断言以卡片自身来源为准。

## 5. 复用与许可

- 权利基础：Met Open Access；对象 `isPublicDomain=true` 时，Met 对其图像声明 CC0。**数据与图像权利分别核验**（本索引只核验对象字段与 URL 状态）。
- 引用建议格式：
  > The Metropolitan Museum of Art, [Title], [Date], [Object ID]. https://www.metmuseum.org/art/collection/search/[objectID]
- 不得：
  - 把图片复制进 Vault、博客或生成式服务；
  - 用 `image_url` 替代许可说明；
  - 将本索引当作法律意见或商业使用许可；
  - 把 `public_domain_verified=true` 扩展到同一批次的其它对象（必须逐件核验）。

## 6. 缺口与下一步

1. **source_id 缺口**：15 条为 `MET-API`（无独立 SRC 卡）。下一步可为每条建 `SRC-` 卡（建议 SRC-0500+ 段位由来源组统一分配），纳入 reports/SOURCES.csv。
2. **structure_features 受限**：不下载图片 → 只能给 metadata-only 结构；若需领型/袖型/廓形，应由人工对照 `object_url` 图像补充，并在备注标 `visual_reviewed`。
3. **分类字段**：Costume Institute 的 `classification` 多为空，已用 `department / objectName` 派生；不要把它当 Met 原始分类。
4. **卡关联**：尚无 MAT/LOOK 级关联；可优先把纺织/纹样类对象（如 475116 科普特织物）关联到 MAT 卡，把整套装束关联到 LOOK 卡。
5. **图像可用性**：个别 Met 图像 URL 可能慢/超时（VIS-0008 已复测 200）；`access_status` 记录本次结果，不保证长期稳定。
6. **仅 Met**：本原型没有 V&A/其他馆藏；跨馆索引需各自核验许可（V&A 多为 link_only）。

## 7. 复核命令（示例，stdlib/curl）

```bash
# 单条对象核验
curl -sS -m 10 -L "https://collectionapi.metmuseum.org/public/collection/v1/objects/159230" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['objectID'], d['isPublicDomain'], d['objectURL'])"

# 图像 URL 状态（不落盘）
curl -sS -m 20 -L -o /dev/null -w "%{http_code}\n" "<image_url>"

# CSV 完整性（stdlib）
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('visual-index.csv',encoding='utf-8')))
print(len(rows), all(r['public_domain_verified']=='true' for r in rows), sum(1 for r in rows if r['access_status']=='ok'))
PY
```
