## 核对结果（数据均来自 visual-index.csv 与 `query.py` 实查，未伪造）

| VIS | related_card（query 实查） | source_id（query 实查） | object_url |
|---|---|---|---|
| VIS-0001 Gym suit, 1895–99, American, cotton | **PRD-0003**「1890年代英美服饰语境」，type=period_region，**verified**；卡内 source_ids=SRC-0153/SRC-0174/SRC-0021 | **SRC-0031**「Met藏品：体操服1895–99」，verified（该 SRC 不在 PRD-0003 卡内，CSV 关联为时代语境级，非卡内引用） | metmuseum.org/art/collection/search/**106702** |
| VIS-0003 Kimono, 19th c., Japan, silk | **GAR-0001**「和服/kimono」，garment，**verified**；卡内 source_ids 恰含 **SRC-0100**，三方一致 | **SRC-0100**「Met开放数据：19世纪日本和服」，verified | …/search/**125953** |
| VIS-0005 Dress, ca.1885, American, silk | **STR-0007**「臀垫/bustle」，garment_part，**verified**；卡内 source_ids=**SRC-0137**（非 SRC-0025，故为结构例证级关联） | **SRC-0025**「Met藏品：连衣裙 ca.1885」，verified | …/search/**157943** |

三条 ID 全部真实存在且 verified；其中仅 VIS-0003 达到「卡↔SRC」直接互引，另两条的 source_id 是**视觉对象自身来源**，与卡片是主题关联，不应表述为卡片引证。

## CC0 / 图像许可边界（据 CSV 字段，非自行推断）

- 三行 rights_status 均为 **CC0 / Met Open Access (isPublicDomain=true)**，`public_domain_verified=true`，API 与图像 URL 均 HTTP 200，access_status=ok。
- 边界（verification_note 明示）：**图像 URL 不等于许可本身**；CC0 状态以 Met API 的 isPublicDomain 字段为准。
- 当前库内**未下载、未内嵌图片**，仅记录 `images.metmuseum.org` 图像链接；本环境也不抓取图片。
- 结构信息一律 **metadata-only**：领/袖/廓形等「未从图像推断」，不得据图补编形制。
- 使用时应署名 The Metropolitan Museum of Art 并保留 object_url；CC0 覆盖的是该公共领域对象的 Met 数字影像，**不得外推**为所有 Met 图片或第三方用途（如人物商标、隐私）均无限制；CSV 之外的许可承诺均属伪造，我不提供。
