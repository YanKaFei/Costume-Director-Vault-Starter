## Brief
- Requested: `GAR-0015`, kind `garment_flat`, period `1930s`, English prompt, JSON output.
- Card: `01-服装单品/连身/GAR-0015-法式长袍.md`
- Card type: 法式长袍 (robe à la française) — card periods: `18th_century`, `rococo`.

## Conflict
**1 error, 0 warnings, 0 notices**

| Code | Severity | Detail |
|---|---|---|
| `period_conflict` | **error** | requested `1930s` vs card periods `['18th_century', 'rococo']` |

The card is an 18th-century Rococo gown, not a 1930s garment. Using it for a 1930s brief would be an anachronism; the generated prompt is therefore not period-valid for 1930s.

## Evidence
- `evidence_status`: **verified**
- `source_ids`: **SRC-0116**
- Evidence tags present: `FACT`, `OBSERVATION`, `INFERENCE`, `CREATIVE`
- Card source basis: `YAML + body`
- Card `observation` (OBSERVATION): 背面像“瀑布”一样垂下的宽褶；正面 V 形开口与装饰插片；侧面因裙撑而极宽。
- Card `inference` (INFERENCE): 18th-century robe à la française, fitted front bodice, loose back with two box pleats falling from shoulders to hem, open front revealing stomacher and petticoat, panniers, silk brocade.
- `creative`: staging/art-direction choices; **not** a historical claim.

The `FACT`/`OBSERVATION` fields describe the 18th-century construction; the `INFERENCE` explicitly names it as 18th-century. No 1930s evidence exists in this card.

## Generated prompt (text only)
`prompt_en`:
> 法式长袍, flat lay on neutral background, front/back, true scale, no model; silhhouette X_line; - 前身合体、后身宽松；背部两片箱形褶（box pleats）从肩线垂至地面。 - 前开 V 形，露出 stomacher 与衬裙；可配 paniers 撑起侧宽。 - 材质以丝绸、织锦、蕾丝为主，纹样与配色随年代变化。 - 19 世纪复刻/仿制时也称 Watteau gown。; 背面像“瀑布”一样垂下的宽褶；正面 V 形开口与装饰插片；侧面因裙撑而极宽。; materials silk, brocade, lace; palette pastel, silk_floral, cream; 背部箱褶与裙撑使转身半径大；快走时裙摆与后褶大幅摆动，需固定裙撑位置。

(Metadata output also contains `prompt_zh`, which mirrors the same content. Note the source text includes the typo `silhhouette`.)

## Image generation
**No image was generated.**
- `image_generation`: `false`
- `delivery`: `text prompt only`
- `model_agnostic`: `true`

This was a prompt-building run only; the output is text, not an image or video.

## Gaps
- The period mismatch is unresolved: no 1930s-compatible `GAR-0015` interpretation was produced, and the builder did not substitute another card.
- No alternative 1930s garment card was selected by this command. A correct 1930s flat requires a separately verified 1930s card.
