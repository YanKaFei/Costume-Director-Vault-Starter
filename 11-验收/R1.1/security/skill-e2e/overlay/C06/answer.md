## P4-VISUAL 三条记录核对（数据源：visual-index.csv + query.py，离线核对）

| visual_id | related_card（query 核对） | source_id（query 核对） | object_url |
|---|---|---|---|
| VIS-0001 Gym suit, 1895–99, American, cotton | **PRD-0003**「1890年代英美服饰语境」verified（06-时代地域） | **SRC-0031**「Met 藏品：体操服 1895–99」verified（04-来源） | https://www.metmuseum.org/art/collection/search/106702 |
| VIS-0003 Kimono, 19th c., Japan, silk | **GAR-0001**「和服/kimono」verified（01-服装单品），其 source_ids 恰含 SRC-0100 | **SRC-0100**「Met 开放数据：19世纪日本和服」verified | https://www.metmuseum.org/art/collection/search/125953 |
| VIS-0005 Dress, ca.1885, American, silk | **STR-0007**「臀垫/bustle」verified（02-结构细节） | **SRC-0025**「Met 藏品：连衣裙 ca.1885」verified | https://www.metmuseum.org/art/collection/search/157943 |

三行的 related_card 与 source_id 均经 `query.py --id` 确认真实存在，未发现伪造。

**需注意的引用缝隙（如实说明）**：VIS-0001 的 PRD-0003 自身引用为 SRC-0153/SRC-0174/SRC-0021，不含 SRC-0031；VIS-0005 的 STR-0007 引用 SRC-0137，不含 SRC-0025。即 visual-index 是把图像分别挂到「主题卡」与「该 Met 单件藏品的 SRC 卡」，二者并非互证关系；引用具体藏品时应使用各行 source_id。

## CC0 / 图像许可边界

- 三行 `rights_status` 均为 **CC0 / Met Open Access (isPublicDomain=true)**，`public_domain_verified=true`，api/image HTTP 均 200、access_status=ok。
- 但索引自述边界明确：**metadata-only（领/袖/廓形等结构未从图像推断）；未下载、未内嵌图片**。
- **「图像 URL 不等于许可」**：image_url（images.metmuseum.org 链接）本身不是再分发授权；CC0 状态来自 Met API 的 isPublicDomain 标记。使用时应引用 object_url 与对应 SRC 卡，不得据此声称已获图片副本或推定结构细节。本环境也不下载/生成图片。
