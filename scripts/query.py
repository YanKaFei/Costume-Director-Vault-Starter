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
        terms = raw_terms
    else:
        terms = []
        for raw in raw_terms:
            terms.extend(part for part in raw.split() if part.strip())
    results = []
    for card in cards:
        if not apply_filter(card, args):
            continue
        haystacks = build_haystacks(card)
        if terms:
            hits = []
            field_hits = []
            for term in terms:
                score, field = term_score(term, haystacks)
                hits.append(score)
                field_hits.append(field)
            if args.match == "all":
                if any(score == 0 for score in hits):
                    continue
            else:
                if all(score == 0 for score in hits):
                    continue
            score = sum(hits) / float(len(hits)) if hits else 0.0
        else:
            score = 0.0
        row = card_to_row(card, score)
        row["snippet"] = make_snippet(card, terms) if terms else lib.safety_line(
            card.get("body", ""))[:150]
        row["_fields"] = [f for f in (field_hits if terms else []) if f]
        results.append(row)

    if terms:
        results.sort(key=lambda r: (-r["score"], r["id"]))
    else:
        results.sort(key=lambda r: r["id"])
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
