#!/usr/bin/env python3
"""costume_lib.py - shared vault loading/search helpers for the Costume Director vault.

Standard library + PyYAML only.  The vault root is the parent directory of this
scripts/ folder, so both query.py and recommend.py work from any cwd.

The library deliberately tolerates imperfect cards: a card with broken YAML is
skipped with a warning instead of crashing retrieval.  A separate validator
(task-6) owns strict 0-YAML-error enforcement.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML 6.x is available in the project environment
except ImportError:  # pragma: no cover - documented fallback
    yaml = None

# Directories that hold knowledge-base cards.  00-系统/10/11/reports/TASKS/skills
# hold docs, not cards, and are excluded from retrieval.
CARD_DIRS = [
    "01-服装单品",
    "02-结构细节",
    "03-材质纹样",
    "04-来源",
    "05-风格体系",
    "06-时代地域",
    "07-剧情场景",
    "09-造型组合",
]

# A trailing zero-padded card id such as GAR-0001 / LOOK-EXAMPLE-001 / SRC-0099.
ID_RE = re.compile(
    r"\b((?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)(?:-[A-Z0-9]+)*-[0-9]{3,4})\b"
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")

# Fields that are officially lists in the data dictionary.
LIST_FIELDS = [
    "aliases", "periods", "regions", "style_tags", "colors", "materials",
    "source_ids", "tags", "season",
]

# Weighted text fields used by keyword search.  Higher = more meaningful hit.
FIELD_WEIGHTS = [
    ("id", 10),
    ("name_zh", 8),
    ("name_en", 8),
    ("aliases", 7),
    ("style_tags", 5),
    ("category", 4),
    ("subcategory", 4),
    ("colors", 4),
    ("materials", 4),
    ("periods", 4),
    ("regions", 4),
    ("tags", 3),
    ("formality", 3),
    ("silhouette", 3),
    ("fit", 3),
    ("prompt_en", 3),
    ("movement_notes", 2),
    ("lighting_notes", 2),
]


def vault_root():
    """Absolute vault root (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, (list, tuple, set)):
        out = []
        for v in value:
            if v is None:
                continue
            if isinstance(v, str):
                if v.strip():
                    out.append(v.strip())
            elif isinstance(v, (int, float)):
                out.append(str(v))
            else:
                out.append(str(v))
        return out
    return [str(value)]


def _fallback_flat_yaml(text):
    """Very small flat-YAML parser used only when PyYAML is unavailable/broken."""
    meta = {}
    key = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and key and line.lstrip().startswith("- "):
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = [meta[key]]
            meta[key].append(line.lstrip()[2:].strip())
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            if val == "":
                meta[key] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                meta[key] = [p.strip().strip("'\"") for p in inner.split(",") if p.strip()]
            else:
                meta[key] = val.strip("'\"")
    return meta


def split_frontmatter(text):
    """Return (frontmatter_text, body_text) or (None, text) when absent."""
    if text.startswith("\ufeff"):
        text = text[1:]
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines(True)
    if lines[0].strip() != "---":
        return None, text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm = "".join(lines[1:idx])
            body = "".join(lines[idx + 1:])
            return fm, body
    return None, text


def parse_card(path):
    """Parse one markdown card.

    Returns dict: meta, body, path (absolute Path), rel (vault-relative str),
    error (str or None).
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = split_frontmatter(text)
    meta = {}
    error = None
    if fm is not None:
        try:
            loaded = yaml.safe_load(fm) if yaml is not None else _fallback_flat_yaml(fm)
            if loaded is None:
                loaded = {}
            if not isinstance(loaded, dict):
                error = "frontmatter is not a mapping"
                loaded = {}
            meta = loaded
        except Exception as exc:  # noqa: BLE001 - tolerate broken cards
            error = "yaml parse error: %s" % (exc,)
            meta = _fallback_flat_yaml(fm)
    else:
        error = "missing frontmatter"
    return {
        "meta": meta,
        "body": body,
        "path": path,
        "rel": path.relative_to(vault_root()).as_posix()
        if _is_relative_to(path, vault_root()) else path.as_posix(),
        "error": error,
    }


def _is_relative_to(path, root):
    try:
        Path(path).resolve().relative_to(Path(root).resolve())
        return True
    except ValueError:
        return False


def iter_markdown(root=None, dirs=None):
    root = Path(root or vault_root())
    dirs = dirs or CARD_DIRS
    seen = set()
    for d in dirs:
        base = root / d
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.startswith("."):
                continue
            key = path.resolve()
            if key in seen:
                continue
            seen.add(key)
            yield path


def load_cards(root=None, dirs=None, required=True):
    """Load all card files.  Returns (cards, errors).

    required=True keeps only files that have an 'id' in frontmatter.
    """
    cards = []
    errors = []
    for path in iter_markdown(root, dirs):
        card = parse_card(path)
        meta = card["meta"]
        if not meta.get("id"):
            # Docs such as 04-来源/README.md legitimately have no frontmatter;
            # only warn about files that look like cards but fail to parse.
            if card["error"] and card["error"] != "missing frontmatter":
                errors.append({"path": card["rel"], "error": card["error"]})
            continue
        if card["error"]:
            errors.append({"path": card["rel"], "error": card["error"]})
        cards.append(card)
    return cards, errors


# ---------------------------------------------------------------------------
# normalization helpers
# ---------------------------------------------------------------------------
_CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


def norm_text(value):
    """Lowercase, normalise separators and collapse whitespace."""
    if value is None:
        return ""
    s = str(value)
    s = _CAMEL_RE.sub(" ", s)
    s = s.replace("_", " ").replace("-", " ").replace("/", " ").replace("·", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def tokens(value):
    """Return a set of normalized search tokens from a string or list."""
    out = set()
    for item in _as_list(value):
        s = norm_text(item)
        if not s:
            continue
        out.add(s)
        for part in re.split(r"[^\w\u4e00-\u9fff]+", s):
            if len(part) >= 2:
                out.add(part)
    return out


def card_tokens(card):
    """All normalized tokens for keyword matching, with per-field provenance."""
    meta = card["meta"]
    fields = {}
    for key in [
        "id", "type", "name_zh", "name_en", "category", "subcategory",
        "aliases", "periods", "regions", "style_tags", "colors", "materials",
        "source_ids", "tags", "season", "formality", "silhouette", "fit",
        "prompt_en", "movement_notes", "lighting_notes", "note",
    ]:
        if key in meta:
            fields[key] = tokens(meta.get(key))
    fields["body"] = tokens(card.get("body", ""))
    return fields


def get_list(meta, key):
    return _as_list(meta.get(key))


def get_str(meta, key, default=""):
    value = meta.get(key)
    if value is None:
        return default
    if isinstance(value, (list, tuple, dict)):
        return default
    return str(value).strip()


def card_ids_in(text):
    """Extract canonical card ids from free text / wikilinks."""
    found = []
    for match in ID_RE.finditer(text or ""):
        cid = match.group(1)
        if cid not in found:
            found.append(cid)
    return found


def find_wikilink_ids(body):
    """Extract ids from [[...]] wikilinks, keeping order and deduping."""
    ids = []
    for target in WIKILINK_RE.findall(body or ""):
        for cid in card_ids_in(target):
            if cid not in ids:
                ids.append(cid)
    return ids


def unique_ordered(seq):
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def load_sources(cards=None, root=None):
    """Map source_id -> source card metadata."""
    if cards is None:
        cards, _ = load_cards(root)
    out = {}
    for card in cards:
        if norm_text(card["meta"].get("type")) == "source":
            out[card["meta"]["id"]] = card
    return out


def source_urls(source_ids, sources):
    urls = []
    for sid in source_ids:
        card = sources.get(sid)
        if not card:
            continue
        url = get_str(card["meta"], "url")
        if url:
            urls.append((sid, url))
    return urls


def safety_line(text):
    return re.sub(r"\s+", " ", text or "").strip()


def main():  # pragma: no cover - tiny diagnostic CLI
    cards, errors = load_cards()
    print("vault_root:", vault_root())
    print("cards:", len(cards))
    for err in errors:
        print("WARN", err["path"], err["error"], file=sys.stderr)
    for card in cards[:5]:
        print("-", card["meta"].get("id"), card["rel"])


if __name__ == "__main__":
    main()
