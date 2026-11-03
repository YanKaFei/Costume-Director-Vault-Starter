#!/usr/bin/env python3
"""query.py - stdlib-only keyword + field retrieval over the Costume Director vault.

Usage examples
--------------
    python3 scripts/query.py "立领 shirt"            # -> AND(立领, shirt)
    python3 scripts/query.py "stand collar" --phrase  # exact phrase
    python3 scripts/query.py "rain" --type look,style --limit 5
    python3 scripts/query.py --type garment --category outerwear --style-tag noir --json
    python3 scripts/query.py "羊毛" --period 1930s --region shanghai --evidence verified
    python3 scripts/query.py --type source --json > /tmp/sources.json

Semantics
---------
* Positional QUERY terms are case-insensitive substrings matched against
  frontmatter text fields and body text.  Whitespace inside a positional term
  is split into separate AND terms (so "立领 shirt" means 立领 AND shirt).
  Use --phrase to keep each positional argument as one exact phrase.
  Default across all terms is AND (every term must hit at least one field);
  use --match any for OR.
* Field hits are weighted (name/id/tags beat body text).
* --json prints a JSON array with exactly the contract keys plus "score":
  id, path, name_zh, name_en, type, evidence_status, source_ids, snippet.
* Cards with broken YAML are skipped with a warning on stderr; run
  scripts/validate.py for the strict schema check.
"""

import argparse
import json
import sys
from pathlib import Path

import costume_lib as lib

QUERY_ALIASES = {
    "上海": ["shanghai"], "北京": ["beijing"], "中国": ["china"],
    "旗袍": ["qipao", "cheongsam"], "长衫": ["changshan"],
    "和服": ["kimono"], "汉服": ["hanfu"], "韩服": ["hanbok"],
    "纱丽": ["sari"], "头巾": ["turban", "gele"],
    "立领": ["stand collar", "stand-up collar"],
    "盘扣": ["frog closure", "frog fastening"],
    "雨衣": ["raincoat", "rain coat"], "风衣": ["trench coat", "trench"],
    "护士": ["nurse"], "医生": ["doctor"], "警察": ["police"],
    "厨师": ["chef"], "婚礼": ["wedding"], "新娘": ["bride"],
    "太空": ["space"], "宇航": ["astronaut"],
    "1930年代": ["1930s"], "1920年代": ["1920s"], "1940年代": ["1940s"],
    "1950年代": ["1950s"], "1960年代": ["1960s"], "1970年代": ["1970s"],
    "文艺复兴": ["renaissance"], "拜占庭": ["byzantine"], "维多利亚": ["victorian"],
    "黑色电影": ["noir", "film noir"],
}

TYPE_WEIGHT = {
    "garment": 1.05,
    "look": 1.0,
    "period_region": 1.03,
    "style": 1.0,
    "material": 1.01,
    "pattern": 1.0,
    "garment_part": 1.01,
    "scene": 1.0,
    "source": 0.96,
}

CONTRACT_KEYS = [
    "id", "path", "name_zh", "name_en", "type",
    "evidence_status", "source_ids", "snippet",
]


def build_haystacks(card):
    """field name -> normalized text (str) for weighted substring matching."""
    meta = card["meta"]
    fields = {}
    for key in [
        "id", "type", "name_zh", "name_en", "category", "subcategory",
        "aliases", "periods", "regions", "style_tags", "colors", "materials",
        "source_ids", "tags", "season", "formality", "silhouette", "fit",
        "prompt_en", "movement_notes", "lighting_notes", "note",
    ]:
        if key in meta:
            fields[key] = lib.norm_text(" ".join(lib._as_list(meta.get(key))))
    fields["body"] = lib.norm_text(card.get("body", ""))
    return fields


def term_score(term, haystacks):
    """Best weighted hit for one normalized term, plus matched field name."""
    best = 0
    best_field = None
    t = lib.norm_text(term)
    if not t:
        return 0, None
    for field, weight in lib.FIELD_WEIGHTS:
        text = haystacks.get(field, "")
        if text and t in text:
            if weight > best:
                best = weight
                best_field = field
    if best == 0:
        body = haystacks.get("body", "")
        if body and t in body:
            best = 1
            best_field = "body"
    return best, best_field


def make_snippet(card, terms):
    body = lib.safety_line(card.get("body", ""))
    prompt = lib.safety_line(card["meta"].get("prompt_en", ""))
    hay = (body + " " + prompt).lower()
    for term in terms:
        t = lib.norm_text(term)
        if not t:
            continue
        idx = hay.find(t)
        if idx >= 0:
            start = max(0, idx - 45)
            end = min(len(hay), idx + len(t) + 75)
            prefix = "…" if start > 0 else ""
            suffix = "…" if end < len(hay) else ""
            return prefix + lib.safety_line(hay[start:end]) + suffix
    return lib.safety_line(body + " " + prompt)[:150]


def card_to_row(card, score):
    meta = card["meta"]
    return {
        "id": lib.get_str(meta, "id"),
        "path": card["rel"],
        "name_zh": lib.get_str(meta, "name_zh"),
        "name_en": lib.get_str(meta, "name_en"),
        "type": lib.get_str(meta, "type"),
        "evidence_status": lib.get_str(meta, "evidence_status") or "unknown",
        "source_ids": lib.get_list(meta, "source_ids"),
        "snippet": "",
        "score": round(score, 3),
        "_card": card,
    }


def list_overlap(card_values, wanted_values):
    have = set(lib.norm_text(v) for v in lib._as_list(card_values) if lib.norm_text(v))
    for raw in wanted_values:
        n = lib.norm_text(raw)
        if not n:
            continue
        for h in have:
            if n == h or n in h or h in n:
                return True
    return False


def apply_filter(card, args):
    meta = card["meta"]
    if args.type:
        wanted = [lib.norm_text(x) for x in args.type]
        if lib.norm_text(meta.get("type")) not in wanted:
            return False
    if args.category:
        got = [lib.norm_text(meta.get("category")), lib.norm_text(meta.get("subcategory"))]
        wanted = [lib.norm_text(x) for x in args.category]
        if not any(w == g or w in g or g in w for w in wanted for g in got if g):
            return False
    if args.subcategory:
        got = lib.norm_text(meta.get("subcategory"))
        wanted = [lib.norm_text(x) for x in args.subcategory]
        if not any(w == got or w in got or got in w for w in wanted if w):
            return False
    if args.style_tag and not list_overlap(meta.get("style_tags", []), args.style_tag):
        return False
    if args.period and not list_overlap(meta.get("periods", []), args.period):
        return False
    if args.region and not list_overlap(meta.get("regions", []), args.region):
        return False
    if args.evidence:
        got = lib.norm_text(meta.get("evidence_status")) or "unknown"
        wanted = [lib.norm_text(x) for x in args.evidence]
        if got not in wanted:
            return False
    if args.tag and not list_overlap(meta.get("tags", []), args.tag):
        return False
    if args.id:
        wanted = [x.strip() for x in args.id if x.strip()]
        if lib.get_str(meta, "id") not in wanted:
            return False
    return True


def run_query(args):
    cards, errors = lib.load_cards()
    for err in errors:
        print("WARN skipped card %s: %s" % (err["path"], err["error"]),
              file=sys.stderr)
    raw_terms = [t for t in args.terms if t and t.strip()]
    if args.phrase:
        base_terms = raw_terms
    else:
        base_terms = []
        for raw in raw_terms:
            base_terms.extend(part for part in raw.split() if part.strip())
    term_groups = []
    for term in base_terms:
        variants = [term]
        norm_term = lib.norm_text(term)
        for zh, aliases in QUERY_ALIASES.items():
            if zh in term or lib.norm_text(zh) == norm_term:
                variants.extend(aliases)
        term_groups.append(variants)
    terms = [variant for group in term_groups for variant in group]
    results = []
    for card in cards:
        if not apply_filter(card, args):
            continue
        haystacks = build_haystacks(card)
        if term_groups:
            hits = []
            field_hits = []
            for group in term_groups:
                best_score = 0
                best_field = None
                for variant in group:
                    score, field = term_score(variant, haystacks)
                    if score > best_score:
                        best_score = score
                        best_field = field
                hits.append(best_score)
                field_hits.append(best_field)
            if args.match == "all":
                if any(score == 0 for score in hits):
                    continue
            else:
                if all(score == 0 for score in hits):
                    continue
            score = sum(hits) / float(len(hits)) if hits else 0.0
            score *= TYPE_WEIGHT.get(lib.norm_text(card["meta"].get("type")), 1.0)
        else:
            score = 0.0
        row = card_to_row(card, score)
        row["snippet"] = make_snippet(card, terms) if terms else lib.safety_line(
            card.get("body", ""))[:150]
        row["_fields"] = [f for f in (field_hits if terms else []) if f]
        results.append(row)

    if term_groups:
        for row in results:
            if row["evidence_status"] == "example":
                row["score"] = round(row["score"] * 0.65, 3)
        # Example cards must never outrank real cards for ordinary retrieval.
        results.sort(key=lambda r: (r["evidence_status"] == "example",
                                    -r["score"], r["id"]))
    else:
        # filter-only queries have no score; still keep real cards before example
        results.sort(key=lambda r: (r["evidence_status"] == "example", r["id"]))
    # Deduplicate semantically identical content cards (e.g. two kimono cards
    # with the same name_zh); keep the higher-ranked one.
    deduped = []
    seen_names = set()
    for row in results:
        key = (row["type"],
               lib.norm_text(row["name_zh"]) or
               lib.norm_text(row["name_en"]) or row["id"])
        if key in seen_names:
            continue
        seen_names.add(key)
        deduped.append(row)
    results = deduped
    if args.limit and args.limit > 0:
        results = results[: args.limit]
    return results


def render_text(results, args):
    if not results:
        print("No matching cards.")
        return
    if args.phrase:
        display_terms = list(args.terms)
    else:
        display_terms = [part for raw in args.terms for part in raw.split()]
    print("%d result(s)%s" % (
        len(results), "" if not display_terms else " for: " + " ".join(display_terms)))
    print("")
    for idx, row in enumerate(results, 1):
        print("[%d] %s  %s / %s" % (
            idx, row["id"], row["name_zh"] or "-", row["name_en"] or "-"))
        print("    type=%s  evidence=%s  score=%s" % (
            row["type"] or "-", row["evidence_status"], row.get("score", 0)))
        print("    path: %s" % row["path"])
        print("    sources: %s" % (", ".join(row["source_ids"]) if row["source_ids"] else "(none)"))
        if args.verbose and row.get("_fields"):
            print("    matched_fields: %s" % ", ".join(row["_fields"]))
        print("    snippet: %s" % row["snippet"])
        print("")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Keyword + field search over Costume Director vault cards.")
    parser.add_argument("terms", nargs="*",
                        help="search terms; whitespace is split into AND words "
                             "(use --phrase for exact phrases)")
    parser.add_argument("--phrase", action="store_true",
                        help="treat each positional argument as one exact phrase")
    parser.add_argument("--type", action="append", default=[],
                        help="filter by card type (garment|garment_part|material|style|period_region|look|scene|source); repeatable")
    parser.add_argument("--category", action="append", default=[],
                        help="filter by category (also matches subcategory)")
    parser.add_argument("--subcategory", action="append", default=[],
                        help="filter by subcategory")
    parser.add_argument("--style-tag", action="append", default=[],
                        dest="style_tag", help="match any style_tags value")
    parser.add_argument("--period", action="append", default=[],
                        help="match any periods value")
    parser.add_argument("--region", action="append", default=[],
                        help="match any regions value")
    parser.add_argument("--evidence", action="append", default=[],
                        help="evidence_status (verified|interpretive|example|unverified)")
    parser.add_argument("--tag", action="append", default=[],
                        help="match any tags value")
    parser.add_argument("--id", action="append", default=[],
                        help="exact card id(s)")
    parser.add_argument("--match", choices=["all", "any"], default="all",
                        help="AND/OR across terms (default all)")
    parser.add_argument("--limit", type=int, default=10,
                        help="max results; 0 = all (default 10)")
    parser.add_argument("--json", action="store_true",
                        help="emit JSON array with contract keys")
    parser.add_argument("--out", help="write output to file instead of stdout")
    parser.add_argument("--verbose", action="store_true",
                        help="show matched frontmatter fields in text mode")
    args = parser.parse_args(argv)
    results = run_query(args)
    if args.json:
        payload = []
        for row in results:
            item = {key: row[key] for key in CONTRACT_KEYS}
            item["score"] = row["score"]
            payload.append(item)
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        if not args.out:
            render_text(results, args)
        text = None
    if args.out:
        Path(args.out).write_text(
            text if args.json else render_text_text(results, args), encoding="utf-8")
        print("wrote %d result(s) to %s" % (len(results), args.out))
    elif args.json:
        print(text)
    return 0


def render_text_text(results, args):
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        render_text(results, args)
    return buf.getvalue()


if __name__ == "__main__":
    sys.exit(main())
