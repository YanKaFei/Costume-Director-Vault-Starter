#!/usr/bin/env python3
"""validate.py - strict offline conformance validator for the Costume Director vault.

Validates every card (.md with YAML frontmatter) in the eight knowledge
directories against 00-系统/数据字典.md (v1.1) and 00-系统/卡片模板.md.

v1.1 rule split implemented here:
  * all types          : id, type, name_zh, name_en, evidence_status,
                         review_status, license_status, tags (§3.1)
  * content types only : category, subcategory, aliases, periods, regions,
                         style_tags, colors, materials, source_ids (§3.2)
  * source cards only  : url, publisher, date_accessed, rights_statement,
                         source_kind, note (§4.9); category/aliases/... exempt
  * body sections      : 8 "## " sections for content types only; source
                         cards need (可支撑事实|定义) AND (验证记录|来源链接)

Checks (per 数据字典 §10):
  1. frontmatter parses with PyYAML and is a dict
  2. frontmatter is flat (scalars or lists of scalars only, no nesting)
  3. required fields present (8 universal + 9 content-only or 6 source-only)
  4. enum values legal (type/category/evidence/review/license/source_kind/...)
  5. id format is PREFIX-9999 or PREFIX-EXAMPLE-999 and matches `type`
  6. ids globally unique
  7. filename == "<id>-<中文名>.md" (filename starts with id + "-")
  8. every [[wikilink]] target exists inside the vault
  9. every source_ids entry of a content card resolves to a source card
 10. evidence_status=verified: content => >=1 resolvable source_id with
     non-empty URL and verified source card; source => own URL + HTTP record
 11. evidence/review/license allowed values
 12. date_accessed is YYYY-MM-DD
 13. body contains the eight required "## " sections (§9, content types) or
     the §4.9 minimum sections (source cards)
 14. verified card's "## 来源链接" section mentions every source_id
 15. no locally embedded copyrighted images (![[...]], ![](local), <img src=local>)
 16. source cards: url is http(s) and note/body records an HTTP status (§7.2)
 17. tags are lowercase, underscore-separated (warning only)
 18. field scalar types: strings / list[string] only, numbers quoted (warning only)

Exit code: 0 when every check passes, 1 when any error-level check fails.
Warnings are printed but do not fail the run.

Usage:
    python3 scripts/validate.py                 # full run
    python3 scripts/validate.py --json          # machine-readable summary
    python3 scripts/validate.py --quiet         # only failures + summary
    python3 scripts/validate.py --list-files    # also list skipped non-card .md
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("FATAL: PyYAML is required (python3 -m pip install PyYAML)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent

# Directories that hold knowledge cards (数据字典 §2).
CARD_DIRS = [
    "01-服装单品", "02-结构细节", "03-材质纹样", "04-来源",
    "05-风格体系", "06-时代地域", "07-剧情场景", "09-造型组合",
]
# Directories that hold docs, not cards; excluded from card validation.
NON_CARD_DIRS = ["00-系统", "10-提示词模板", "11-验收", "skills", "reports", "TASKS"]

TYPE_PREFIX = {
    "garment": "GAR", "garment_part": "STR", "material": "MAT", "pattern": "MAT",
    "style": "STY", "period_region": "PRD", "look": "LOOK", "scene": "SCN",
    "source": "SRC", "rule": "RUL",
}

# §3.1 所有类型必备（含 source）
UNIVERSAL_FIELDS = [
    "id", "type", "name_zh", "name_en",
    "evidence_status", "review_status", "license_status", "tags",
]
# §3.2 仅内容类型必备（source 豁免）
CONTENT_FIELDS = [
    "category", "subcategory", "aliases", "periods", "regions", "style_tags",
    "colors", "materials", "source_ids",
]
CONTENT_TYPES = {
    "garment", "garment_part", "material", "pattern", "style",
    "period_region", "look", "scene", "rule",
}

TYPE_FIELDS = {
    "garment": ["silhouette", "fit", "season", "formality", "movement_notes",
                "lighting_notes", "prompt_en"],
    "garment_part": ["part_family", "structural_notes", "construction_era", "prompt_en"],
    "material": ["material_family", "fiber_content", "hand_feel", "care_notes", "prompt_en"],
    "pattern": ["pattern_family", "repeat_type", "symbolism", "prompt_en"],
    "style": ["style_family", "style_period", "design_language", "prompt_en"],
    "period_region": ["period_label", "region_label", "social_context",
                      "key_garments", "prompt_en"],
    "look": ["look_role", "look_items", "look_scene", "continuity_lock",
             "prompt_en", "negative_prompt_en"],
    "scene": ["scene_character", "story_day", "time_place", "weather", "actions",
              "camera_lighting"],
    "source": ["url", "publisher", "date_accessed", "rights_statement",
               "source_kind", "note"],  # §4.9
    "rule": ["rule_scope", "rule_statement", "rule_check"],
}

LIST_FIELDS = [
    "aliases", "periods", "regions", "style_tags", "colors", "materials",
    "source_ids", "tags", "season", "construction_era", "fiber_content",
    "style_period", "key_garments", "look_items", "look_scene", "actions",
]

ENUMS = {
    "type": set(TYPE_PREFIX),
    "evidence_status": {"verified", "interpretive", "example", "unverified"},
    "review_status": {"draft", "reviewed", "needs_review"},
    "license_status": {"cc0", "cc_by", "other_permission", "link_only",
                       "not_applicable", "unknown"},
    "source_kind": {"museum_collection", "academic_reference", "vocabulary",
                    "industry_framework", "image_repository", "dataset",
                    "reference_work", "other"},
    "silhouette": {"A_line", "H_line", "X_line", "Y_line", "straight", "flared",
                   "hourglass", "cocoon", "asymmetric", "unknown"},
    "fit": {"slim", "regular", "relaxed", "oversized", "bodycon",
            "unstructured", "unknown"},
    "formality": {"casual", "smart_casual", "business", "formal", "ceremonial",
                  "theatrical", "functional", "unknown"},
    "season": {"spring", "summer", "autumn", "winter", "all_season"},
    "part_family": {"neckline", "collar", "shoulder", "sleeve", "placket",
                    "pocket", "waistline", "pleats", "vent", "seam", "ornament",
                    "closure", "length", "layering", "support", "silhouette"},
    "material_family": {"fiber", "textile", "leather", "fur", "metal", "dye",
                        "finish", "trim"},
    "pattern_family": {"geometric", "floral", "animal", "abstract", "figurative",
                       "stripe", "check", "paisley", "border", "allover",
                       "placement"},
    "repeat_type": {"tossed", "half_drop", "full_drop", "border", "engineered",
                    "unknown"},
    "style_family": {"historical_style", "art_movement", "subculture",
                     "occupational", "cinematic_genre", "fictional_world"},
    "rule_scope": {"data_entry", "sourcing", "recommendation", "continuity",
                   "licensing"},
}

CATEGORY_BY_TYPE = {
    "garment": {"upper_body", "lower_body", "one_piece", "outerwear",
                "inner_layer", "footwear", "headwear", "accessory",
                "carried_prop", "specialised"},
    "garment_part": {"construction"},
    "material": {"material"},
    "pattern": {"pattern"},
    "style": {"cinematic_style", "historical_style", "art_movement",
              "subculture", "occupational", "fictional_world"},
    "period_region": {"period_region"},
    "look": {"character_look"},
    "scene": {"scene"},
    "source": {"source"},
    "rule": {"rule"},
}

REQUIRED_SECTIONS = [
    "定义", "结构要点", "视觉辨识", "适用条件", "不适用条件",
    "提示词短语", "来源链接", "相关卡片",
]

ID_RE = re.compile(r"^(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC|RUL)-(\d{4}|EXAMPLE-\d{3})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*#*\s*$")


class Result:
    """One named check plus its failures/warnings."""

    def __init__(self, name, severity="error", description=""):
        self.name = name
        self.severity = severity  # error | warning
        self.description = description
        self.total = 0
        self.passed = 0
        self.failures = []  # (subject, message)
        self.warnings = []  # (subject, message)

    def ok(self, subject):
        self.total += 1
        self.passed += 1

    def fail(self, subject, message):
        self.total += 1
        self.failures.append((subject, message))

    def warn(self, subject, message):
        self.warnings.append((subject, message))

    @property
    def status(self):
        if self.failures:
            return "FAIL" if self.severity == "error" else "WARN"
        if self.warnings:
            return "PASS (warnings)"
        return "PASS"


def read_frontmatter(path):
    """Return (meta dict, body str, error str|None)."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return None, "", f"UTF-8 解码失败: {exc}"
    if text.startswith("\ufeff"):
        return None, "", "文件含 UTF-8 BOM（规定无 BOM）"
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, "", "文件不以 '---' frontmatter 开头"
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "", "frontmatter 缺少结束 '---'"
    raw = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1:])
    try:
        meta = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, body, f"YAML 解析失败: {exc.__class__.__name__}: {exc}"
    if not isinstance(meta, dict):
        return None, body, f"frontmatter 不是映射（得到 {type(meta).__name__}）"
    return meta, body, None


def flat_violations(meta):
    """Return list of nested paths (数据字典 §1: 禁止嵌套)."""
    bad = []

    def walk(value, path):
        if isinstance(value, dict):
            bad.append(path)
            for k, v in value.items():
                walk(v, f"{path}.{k}" if path else str(k))
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                if isinstance(item, (dict, list)):
                    bad.append(f"{path}[{idx}]")
                    walk(item, f"{path}[{idx}]")

    for key, value in meta.items():
        walk(value, key)
    return bad


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def norm_date(value):
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d"), True
    if isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d"), True
    return str(value), False


ID_PREFIX_RE = re.compile(r"^(GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC|RUL)-")


def collect_cards():
    """Return (card_paths, skipped_non_card_paths, suspect_paths).

    A file is a card when it opens with a '---' frontmatter fence.  Files that
    do not, but whose filename starts with a known card ID prefix, are reported
    as suspicious ("card missing frontmatter") instead of being skipped.
    """
    cards, skipped, suspect = [], [], []
    for rel_dir in CARD_DIRS:
        base = ROOT / rel_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            head = path.read_text(encoding="utf-8", errors="replace")[:4]
            if head.startswith("---"):
                cards.append(path)
            elif ID_PREFIX_RE.match(path.stem):
                suspect.append(path)
            else:
                skipped.append(path)
    return cards, skipped, suspect


def rel(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def build_vault_index():
    """basename (no .md) -> list of paths; plus relative-path set."""
    by_name, by_rel = {}, {}
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        rel_no_ext = str(path.relative_to(ROOT))[:-3]
        by_name.setdefault(path.stem, []).append(path)
        by_rel[rel_no_ext] = path
    return by_name, by_rel


def local_image_refs(body):
    """Yield (kind, target) for image embeds that are NOT remote http(s)."""
    refs = []
    for m in WIKILINK_RE.finditer(body):
        if not m.group(0).startswith("!"):
            continue
        target = m.group(1).split("|")[0].strip()
        if target.lower().startswith(("http://", "https://")):
            continue  # remote embed attempt, not a local file
        refs.append(("wikilink-embed", target))
    for m in MD_IMAGE_RE.finditer(body):
        target = m.group(1).strip()
        if target.lower().startswith(("http://", "https://", "data:")):
            continue
        refs.append(("markdown-image", target))
    for m in HTML_IMAGE_RE.finditer(body):
        target = m.group(1).strip()
        if target.lower().startswith(("http://", "https://", "data:")):
            continue
        refs.append(("html-img", target))
    return refs


def local_image_files():
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
    found = []
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in exts:
            found.append(path)
    return found


def main():
    ap = argparse.ArgumentParser(description="Validate Costume Director knowledge cards.")
    ap.add_argument("--json", action="store_true", help="print JSON summary")
    ap.add_argument("--quiet", action="store_true", help="hide passing checks")
    ap.add_argument("--list-files", action="store_true", help="list skipped non-card files")
    args = ap.parse_args()

    checks = {
        "frontmatter": Result("1. frontmatter 可解析为 YAML dict"),
        "flat": Result("2. frontmatter 扁平（无嵌套对象/列表）"),
        "fields": Result("3. 必填字段齐全（§3.1 通用 + §3.2 内容类型 / §4.9 来源卡）"),
        "enums": Result("4. 枚举值合法（type/category/evidence/review/license/source_kind/属性枚举）"),
        "id_format": Result("5. id 格式合法且前缀与 type 匹配"),
        "id_unique": Result("6. id 全局唯一"),
        "filename": Result("7. 文件名以 id- 开头"),
        "wikilinks": Result("8. [[wikilink]] 目标存在"),
        "source_refs": Result("9. source_ids 均解析到 04-来源/ 来源卡"),
        "verified_evidence": Result("10. verified ⇒ 证据可解析（内容卡 ≥1 来源 / 来源卡 url+HTTP 记录）"),
        "date": Result("11. date_accessed 为 YYYY-MM-DD（来源卡）"),
        "sections": Result("12. 正文小节（内容卡 8 节 / 来源卡 §4.9 最低要求）"),
        "source_link_section": Result("13. verified 卡 ## 来源链接 提及全部 source_ids"),
        "images": Result("14. 无本地内嵌图片"),
        "source_url": Result("15. 来源卡 url 为 http(s)、§4.9 字段非空且记录 HTTP 状态"),
        "tags": Result("16. tags 小写/下划线规范", severity="warning"),
        "types": Result("17. 字段类型（list[string]/string，数字需加引号）", severity="warning"),
    }

    cards, skipped_files, suspect_files = collect_cards()
    for path in suspect_files:
        checks["frontmatter"].fail(rel(path), "疑似卡片但缺少 '---' frontmatter")
    parsed = []  # (path, meta, body)
    for path in cards:
        meta, body, err = read_frontmatter(path)
        if err:
            checks["frontmatter"].fail(rel(path), err)
            continue
        checks["frontmatter"].ok(rel(path))
        parsed.append((path, meta, body))

    source_cards = {}
    for path, meta, body in parsed:
        if meta.get("type") == "source":
            source_cards.setdefault(str(meta.get("id")), (path, meta, body))
    basename_index, rel_index = build_vault_index()

    seen_ids = {}
    for path, meta, body in parsed:
        subject = rel(path)
        card_id = str(meta.get("id", "?"))
        ctype = meta.get("type")

        # 2 flat
        nests = flat_violations(meta)
        if nests:
            checks["flat"].fail(subject, "嵌套字段: " + ", ".join(nests))
        else:
            checks["flat"].ok(subject)

        # 3 required fields（v1.1: §3.1 所有类型；§3.2 内容类型；§4.9 source）
        missing = [f for f in UNIVERSAL_FIELDS if f not in meta]
        if ctype in CONTENT_TYPES:
            missing += [f for f in CONTENT_FIELDS if f not in meta]
        missing += [f for f in TYPE_FIELDS.get(ctype, []) if f not in meta]
        if missing:
            checks["fields"].fail(card_id, "缺字段: " + ", ".join(missing))
        else:
            checks["fields"].ok(card_id)

        # 4 enums
        enum_bad = []
        if ctype not in ENUMS["type"]:
            enum_bad.append(f"type={ctype}")
        for field in ("evidence_status", "review_status", "license_status"):
            value = meta.get(field)
            if value is not None and value not in ENUMS[field]:
                enum_bad.append(f"{field}={value}")
        if ctype == "source" and meta.get("source_kind") not in ENUMS["source_kind"]:
            enum_bad.append(f"source_kind={meta.get('source_kind')}")
        for field in ("silhouette", "fit", "formality", "part_family",
                      "material_family", "pattern_family", "repeat_type",
                      "style_family", "rule_scope"):
            if field in meta and meta[field] not in ENUMS.get(field, set()):
                enum_bad.append(f"{field}={meta[field]}")
        if isinstance(meta.get("season"), list):
            bad_season = [s for s in meta["season"] if s not in ENUMS["season"]]
            if bad_season:
                enum_bad.append("season=" + ",".join(map(str, bad_season)))
        if ctype in CONTENT_TYPES and ctype in CATEGORY_BY_TYPE:
            category = meta.get("category")
            if category not in CATEGORY_BY_TYPE[ctype]:
                enum_bad.append(f"category={category} 不属于 type={ctype}")
        if enum_bad:
            checks["enums"].fail(card_id, "; ".join(enum_bad))
        else:
            checks["enums"].ok(card_id)

        # list-typed fields must be lists of scalars
        list_bad = [f for f in LIST_FIELDS if f in meta and not isinstance(meta[f], list)]
        if list_bad:
            checks["flat"].warn(card_id, "列表字段不是 YAML 列表: " + ", ".join(list_bad))

        # 5 id format + prefix
        id_ok = bool(ID_RE.match(card_id))
        if not id_ok:
            checks["id_format"].fail(subject, f"id 格式非法: {card_id}")
        else:
            expected = TYPE_PREFIX.get(ctype)
            got = card_id.split("-")[0]
            if expected and got != expected:
                checks["id_format"].fail(subject, f"前缀 {got} 与 type={ctype} 不匹配（应为 {expected}）")
            else:
                checks["id_format"].ok(card_id)

        # 6 unique
        if card_id in seen_ids:
            checks["id_unique"].fail(card_id, f"重复 id（另一文件: {seen_ids[card_id]}）")
        else:
            seen_ids[card_id] = subject
            checks["id_unique"].ok(card_id)

        # 7 filename
        stem = path.stem
        if stem == card_id or stem.startswith(card_id + "-"):
            checks["filename"].ok(card_id)
        else:
            checks["filename"].fail(subject, f"文件名与 id 不一致（应为 {card_id}-中文名.md）")

        # 8 wikilinks
        bad_links = []
        for m in WIKILINK_RE.finditer(body):
            raw = m.group(1)
            target = raw.split("|")[0].strip()
            target = target.split("#")[0].strip()
            if not target:
                continue  # heading-only link within same file
            if target.endswith(".md"):
                target = target[:-3]
            if target in rel_index:
                continue
            if target in basename_index:
                continue
            if "/" in target:
                candidate = path.parent / (target + ".md")
                if candidate.exists():
                    continue
            bad_links.append(raw)
        if bad_links:
            checks["wikilinks"].fail(card_id, "坏链: " + ", ".join(sorted(set(bad_links))))
        else:
            checks["wikilinks"].ok(card_id)

        # 9 source_ids resolve（§10.4：仅内容卡；source 卡 source_ids 可省略）
        sids = as_list(meta.get("source_ids"))
        unresolved = [s for s in sids if str(s) not in source_cards]
        if ctype in CONTENT_TYPES:
            if unresolved:
                checks["source_refs"].fail(card_id, "source_ids 无对应 04-来源/ 卡: " + ", ".join(map(str, unresolved)))
            else:
                checks["source_refs"].ok(card_id)
        else:
            if unresolved:
                checks["source_refs"].warn(card_id, "source 卡 source_ids 虽有但无对应卡（v1.1 允许省略）: "
                                           + ", ".join(map(str, unresolved)))
            else:
                checks["source_refs"].ok(card_id)

        # 10 verified evidence + 13 source link section
        if meta.get("evidence_status") == "verified" and ctype != "source":
            problems = []
            if not sids:
                problems.append("verified 但 source_ids 为空")
            for s in sids:
                entry = source_cards.get(str(s))
                if entry is None:
                    continue  # already reported under check 9
                _, src_meta, _ = entry
                if not str(src_meta.get("url", "")).strip():
                    problems.append(f"{s} 来源卡 url 为空")
                if src_meta.get("evidence_status") != "verified":
                    problems.append(f"{s} 来源卡 evidence_status={src_meta.get('evidence_status')}")
            if problems:
                checks["verified_evidence"].fail(card_id, "; ".join(problems))
            else:
                checks["verified_evidence"].ok(card_id)
            # check 13: 来源链接 section mentions all source ids
            section_text = body
            m = re.search(r"^##\s+来源链接\s*$", body, re.M)
            if m:
                section_text = body[m.end():]
                nxt = re.search(r"^##\s+", section_text, re.M)
                if nxt:
                    section_text = section_text[:nxt.start()]
            missing_mentions = [str(s) for s in sids if str(s) not in section_text]
            if missing_mentions:
                checks["source_link_section"].fail(card_id, "## 来源链接 未提及: " + ", ".join(missing_mentions))
            else:
                checks["source_link_section"].ok(card_id)

        # 11 date_accessed (§4.9 source only)
        if "date_accessed" in meta:
            value, was_date = norm_date(meta["date_accessed"])
            if DATE_RE.match(value):
                checks["date"].ok(card_id)
            elif ctype == "source":
                checks["date"].fail(card_id, f"date_accessed 非 YYYY-MM-DD: {value}")
        elif ctype == "source":
            checks["date"].fail(card_id, "来源卡缺 date_accessed")

        # 12 sections
        headings = []
        for line in body.splitlines():
            m = HEADING_RE.match(line)
            if m:
                headings.append(m.group(1))
        if ctype in CONTENT_TYPES:
            missing_sections = [s for s in REQUIRED_SECTIONS if s not in headings]
            if missing_sections:
                checks["sections"].fail(card_id, "内容卡缺 8 节: " + ", ".join(missing_sections))
            else:
                checks["sections"].ok(card_id)
        elif ctype == "source":
            # §4.9: (可支撑事实|定义) AND (验证记录|来源链接)
            has_claims = any(h.startswith("可支撑事实") for h in headings) or "定义" in headings
            has_evidence = ("验证记录" in headings) or ("来源链接" in headings)
            problems = []
            if not has_claims:
                problems.append("缺「可支撑事实」或「定义」小节")
            if not has_evidence:
                problems.append("缺「验证记录」或「来源链接」小节")
            if problems:
                checks["sections"].fail(card_id, "来源卡正文: " + "; ".join(problems))
            else:
                checks["sections"].ok(card_id)
        else:
            checks["sections"].fail(card_id, f"未知 type={ctype}，无法判定正文规则")

        # 15 source: url http(s) + §4.9 required non-empty + HTTP evidence trail
        if ctype == "source":
            url = str(meta.get("url", "")).strip()
            note_and_body = str(meta.get("note", "")) + "\n" + body
            plain_evidence = note_and_body.replace("*", "").replace("`", "")
            has_http_status = bool(re.search(r"HTTP\s*[1-5]\d{2}", plain_evidence))
            problems = []
            if not re.match(r"^https?://", url):
                problems.append(f"url 非 http(s): {url!r}")
            for field in ("url", "publisher", "date_accessed",
                          "rights_statement", "source_kind", "note"):
                if field not in meta or not str(meta.get(field) or "").strip():
                    problems.append(f"§4.9 必填字段为空: {field}")
            if not has_http_status:
                problems.append("note/正文未记录 HTTP 状态码（§7.2/§4.9）")
            if meta.get("evidence_status") == "verified" and not has_http_status:
                problems.append("verified 来源卡缺核验记录")
            if problems:
                checks["source_url"].fail(card_id, "; ".join(problems))
            else:
                checks["source_url"].ok(card_id)
            # source 卡的 verified 判定并入本项（§10.5）
            if meta.get("evidence_status") == "verified":
                checks["verified_evidence"].ok(card_id)

        # 16 tags style (warning)
        tags = meta.get("tags")
        if isinstance(tags, list) and tags:
            bad_tags = [t for t in tags if not re.match(r"^[a-z0-9_]+$", str(t))]
            if bad_tags:
                checks["tags"].fail(card_id, "tags 非小写/下划线: " + ", ".join(map(str, bad_tags)))
            else:
                checks["tags"].ok(card_id)

        # 17. field scalar types (dictionary §3: list[string] / string)
        type_bad = []
        for field, value in meta.items():
            if isinstance(value, list):
                for item in value:
                    if not isinstance(item, str):
                        type_bad.append(f"{field}[]={item!r}（应为字符串）")
            elif isinstance(value, (bool, int, float)):
                type_bad.append(f"{field}={value!r}（应为字符串）")
        if type_bad:
            checks["types"].fail(card_id, "; ".join(type_bad))
        else:
            checks["types"].ok(card_id)

    # 14 no embedded local images (inspect all card bodies + filesystem)
    image_files = local_image_files()
    for path in cards:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        body = text
        refs = local_image_refs(body)
        if refs:
            checks["images"].fail(rel(path), "本地图片引用: " + ", ".join(f"{k}:{t}" for k, t in refs))
        else:
            checks["images"].ok(rel(path))
    if image_files:
        for img in image_files:
            checks["images"].warn(rel(img), "Vault 内存在图片文件（需人工确认授权；禁止内嵌未授权图片）")

    # ---- output ----
    error_failures = sum(len(c.failures) for c in checks.values() if c.severity == "error")
    warn_count = sum(len(c.warnings) + (len(c.failures) if c.severity == "warning" else 0)
                     for c in checks.values())

    if not args.json:
        print("=" * 78)
        print("Costume Director Vault — validate.py（数据字典 v1.0 §10）")
        print(f"根目录: {ROOT}")
        print(f"扫描卡片文件: {len(cards)} 个（{', '.join(CARD_DIRS)}）")
        print("=" * 78)
        for key in checks:
            chk = checks[key]
            line = f"[{chk.status}] {chk.name}: {chk.passed}/{chk.total}"
            if chk.severity == "warning":
                line += "（警告级，不影响退出码）"
            print(line)
            if chk.failures and not args.quiet:
                label = "FAIL" if chk.severity == "error" else "WARN"
                for subject, msg in chk.failures[:60]:
                    print(f"    {label} {subject}: {msg}")
                if len(chk.failures) > 60:
                    print(f"    ... 另有 {len(chk.failures) - 60} 条失败")
            for subject, msg in chk.warnings[:10]:
                print(f"    WARN {subject}: {msg}")
            if len(chk.warnings) > 10:
                print(f"    ... 另有 {len(chk.warnings) - 10} 条警告")
        print("-" * 78)
        print(f"卡片总数: {len(cards)}；frontmatter 通过: {len(parsed)}；"
              f"来源卡: {len(source_cards)}")
        print(f"错误级失败项: {error_failures}；警告: {warn_count}")
        print(f"跳过的非卡片 .md（无 frontmatter）: {len(skipped_files)}")
        if args.list_files:
            for s in skipped_files:
                print(f"    SKIP {rel(s)}")
        if suspect_files:
            print(f"疑似卡片但无 frontmatter: {len(suspect_files)}")
        print("-" * 78)
        if error_failures:
            print("RESULT: FAIL（存在错误级问题，见上方失败清单）")
        else:
            print("RESULT: PASS（0 个错误级失败；若有警告见上）")

    summary = {
        "root": str(ROOT),
        "cards_scanned": len(cards),
        "frontmatter_ok": len(parsed),
        "source_cards": len(source_cards),
        "skipped_non_card": [rel(p) for p in skipped_files],
        "suspect_missing_frontmatter": [rel(p) for p in suspect_files],
        "checks": {
            key: {
                "name": chk.name,
                "severity": chk.severity,
                "status": chk.status,
                "passed": chk.passed,
                "total": chk.total,
                "failures": [{"subject": s, "message": m} for s, m in chk.failures],
                "warnings": [{"subject": s, "message": m} for s, m in chk.warnings],
            }
            for key, chk in checks.items()
        },
        "error_failures": error_failures,
        "warnings": warn_count,
        "exit_code": 1 if error_failures else 0,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if error_failures else 0


if __name__ == "__main__":
    sys.exit(main())
