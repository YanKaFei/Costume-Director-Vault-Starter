#!/usr/bin/env python3
"""books_extract.py - P4-1 public-domain book extractor (stdlib only).

Only the 9 books confirmed as public domain by reports/P4-SOURCE-AUDIT.md:
  GITenberg mirrors : 34903, 21534, 33020, 48551, 49559
  Project Gutenberg : 76299, 56978, 76717, 46949
No other editions are downloaded or quoted. Images are never extracted.

The script parses Project Gutenberg plain text into:
  * metadata (title/author/year/release/credits, from the PG header)
  * table of contents (raw + normalised entries)
  * chapters/sections with line ranges
  * paragraphs (numbered per chapter) for locators
  * term / garment-description hits with locators
        book ID, chapter (index + heading), paragraph number, line number
  * dictionary headwords (book 76299 is a dictionary of men's wear)

Locators are line/paragraph based because PG plain text has no reliable
page numbers; a page locator must be reported as UNCONFIRMED, never
invented.

Usage
  python3 scripts/books_extract.py --download            # fetch the 9 PD texts
  python3 scripts/books_extract.py                       # parse all + write outputs
  python3 scripts/books_extract.py --book 46949          # one book
  python3 scripts/books_extract.py --search "farthingale"
  python3 scripts/books_extract.py --locate 46949:2352   # chapter/para for a line
  python3 scripts/books_extract.py --json                # machine-readable summary

Exit codes: 0 ok, 1 usage/data error, 2 fatal parse error.
"""

import argparse
import json
import os
import re
import subprocess
import sys

BOOKS = [
    # ---- GITenberg mirrors (audit A12) ----
    dict(id="34903", repo="GITenberg/Dress-designAn-Account-of-Costume-for-Artists--amp--Dressmakers_34903",
         family="gitenberg", title="Dress Design: An Account of Costume for Artists & Dressmakers",
         author="Talbot Hughes", year="1919", publisher="The Artistic Crafts Series of Technical Handbooks",
         chapter_re="^CHAPTER\\s+([IVXL]+)\\s*$", chapter_prefix="CHAPTER"),
    dict(id="21534", repo="GITenberg/Textiles-and-Clothing_21534",
         family="gitenberg", title="Textiles and Clothing", author="Kate Heintz Watson",
         year="1907", publisher="American School of Home Economics",
         toc_anchor=True, chapter_prefix="SECTION"),
    dict(id="33020", repo="GITenberg/English-Costume_33020",
         family="gitenberg", title="English Costume", author="Dion Clayton Calthrop",
         year="1907", publisher="Adam & Charles Black, London",
         toc_anchor=True, chapter_prefix="REIGN"),
    dict(id="48551", repo="GITenberg/Costume-Fanciful-Historical-and-Theatrical_48551",
         family="gitenberg", title="Costume: Fanciful, Historical and Theatrical", author="Mrs. Aria",
         illustrator="Percy Anderson", year="1906", publisher="Macmillan and Co., London",
         chapter_re="^CHAPTER\\s+([IVXL]+)\\s*$", chapter_prefix="CHAPTER"),
    dict(id="49559", repo="GITenberg/Modern-Design-in-Jewellery-and-Fans_49559",
         family="gitenberg", title="Modern Design in Jewellery and Fans", author="Charles Holme (ed.)",
         year="1902", publisher="Offices of 'The Studio', London/Paris/New York",
         chapter_re=None, chapter_prefix="SECTION"),
    # ---- Project Gutenberg (audit B) ----
    dict(id="76299", family="gutenberg", title="A Dictionary of Men's Wear",
         author="William Henry Baker", year="1908", publisher="William Henry Baker, Cleveland",
         chapter_re=None, chapter_prefix="ENTRY", dictionary=True),
    dict(id="56978", family="gutenberg", title="The Book of the Feet: A History of Boots and Shoes",
         author="Joseph Sparkes Hall", year="1847", publisher="J. S. Redfield, New York",
         chapter_re="^CHAPTER\\s+([IVXL]+)\\.?\\s*$", chapter_prefix="CHAPTER"),
    dict(id="76717", family="gutenberg", title="The History of Fashion in France",
         author="Augustin Challamel (trans. Frances Cashel Hoey & John Lillie)",
         year="1882", publisher="Sampson Low, Marston, Searle & Rivington, London",
         chapter_re="^\\s*CHAPTER\\s+([IVXL]+)\\.\\s*$", chapter_prefix="CHAPTER"),
    dict(id="46949", family="gutenberg", title="Chats on Costume",
         author="G. Woolliscroft Rhead", year="1906", publisher="T. Fisher Unwin, London",
         split_chapter_re="^(I|II|III|IV|V|VI|VII|VIII|IX|X)$", chapter_prefix="CHAT"),
]

DEFAULT_TERMS = [
    # garments / main types
    "dress", "costume", "gown", "robe", "tunic", "mantle", "cloak", "doublet", "hose",
    "kirtle", "petticoat", "crinoline", "farthingale", "ruff", "stomacher", "bodice",
    "skirt", "train", "bustle", "waistcoat", "breeches", "coat", "trousers", "pantaloons",
    "shirt", "chemise", "corset", "sleeve", "collar", "cuff",
    # head / feet / accessories
    "headdress", "head-dress", "hat", "cap", "bonnet", "hood", "veil", "wig",
    "shoe", "boot", "slipper", "sandal", "stocking", "glove", "fan", "muff", "girdle",
    "belt", "buckle", "button", "jewel", "jewellery", "jewelry", "necklace", "bracelet",
    "earring", "ring", "brooch", "purse",
    # materials / techniques
    "embroidery", "lace", "silk", "velvet", "satin", "wool", "linen", "cotton",
    "brocade", "damask", "taffeta", "muslin", "calico", "frieze", "cloth", "trimming",
    "fringe", "ribbon", "pattern", "cutting", "fitting",
    # context
    "peasant", "servant", "citizen", "noble", "mourning", "wedding", "theatrical", "fancy dress",
]

START_RE = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.I)
END_RE = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.I)
TOC_RE = re.compile(r"^\s*(CONTENTS\.?|Contents\.?|Table of Literary Contents\.?)\s*$")
PAGE_NUM_RE = re.compile(r"\.{2,}\s*\d+\s*$|\s{2,}\d{1,4}\s*$")
ROMAN_RE = re.compile(r"^[IVXL]+$")


def read_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        raw = fh.read()
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    if "\x0c" in raw:
        raw = raw.replace("\x0c", "\n")
    return raw


def split_pg(raw):
    lines = raw.split("\n")
    start = 0
    end = len(lines)
    for i, ln in enumerate(lines):
        if START_RE.search(ln):
            start = i + 1
            break
    for i in range(len(lines) - 1, start, -1):
        if END_RE.search(lines[i]):
            end = i
            break
    header = lines[:start]
    body = lines[start:end]
    return header, body


def pg_metadata(header):
    meta = {}
    for ln in header:
        m = re.match(r"^(Title|Author|Editor|Illustrator|Release date|Language|Original publication|Credits|Character set encoding):\s*(.+)$", ln.strip())
        if not m:
            continue
        key, val = m.group(1).lower(), m.group(2).strip()
        if key in meta:
            if isinstance(meta[key], list):
                meta[key].append(val)
            else:
                meta[key] = [meta[key], val]
        else:
            meta[key] = val
    return meta


def first_line(meta, key):
    v = meta.get(key, "")
    if isinstance(v, list):
        v = v[0]
    return re.sub(r"\s+", " ", v).strip()


def normalise(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("_", "").replace("=", "")
    s = re.sub(r"\.{2,}\s*\d+\s*$", "", s)
    s = re.sub(r"\s{2,}\d{1,4}\s*$", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_toc(body):
    """Return (toc_lines_raw, toc_entries, toc_end_index)."""
    body_start = 0
    for i, ln in enumerate(body[:600]):
        if TOC_RE.match(ln):
            body_start = i + 1
            break
    if not body_start:
        return [], [], 0
    raw, entries = [], []
    blanks = 0
    for ln in body[body_start:body_start + 220]:
        if not ln.strip():
            blanks += 1
            if blanks > 4 and entries:
                break
            continue
        blanks = 0
        raw.append(ln.rstrip())
        n = normalise(ln)
        if n and not re.match(r"^(PAGE|LIST OF|ILLUSTRATIONS?)", n, re.I):
            entries.append(n)
        if len(raw) > 200:
            break
    return raw, entries, body_start + len(raw) + 2


ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8,
         "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16,
         "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20, "XXI": 21, "XXII": 22, "XXIII": 23,
         "XXIV": 24, "XXV": 25, "XXVI": 26, "XXVII": 27, "XXVIII": 28, "XXIX": 29, "XXX": 30,
         "XXXI": 31, "XXXII": 32, "XXXIII": 33, "XXXIV": 34, "XXXV": 35, "XXXVI": 36,
         "XXXVII": 37, "XXXVIII": 38, "XXXIX": 39, "XL": 40, "XLI": 41}


def _num(v):
    v = v.strip().rstrip(".")
    if v.isdigit():
        return int(v)
    return ROMAN.get(v.upper(), 0)


def detect_chapters(body, book, toc_entries, toc_end=0):
    """Return list of {index, heading, start, end} (line indexes into body)."""
    chapters = []
    if book.get("chapter_re"):
        rx = re.compile(book["chapter_re"])
        cand = []
        for i, ln in enumerate(body):
            m = rx.match(ln)
            if not m:
                continue
            num = _num(m.group(1))
            heading = ln.strip()
            if len(m.groups()) > 1 and m.group(2):
                heading = m.group(2).strip(" .")
            cand.append((i, num, heading))
        # TOC and body may both contain "CHAPTER I." — start at the LAST chapter I,
        # then accept only a monotonically increasing sequence (body order).
        start_pos = 0
        for k, (i, num, _h) in enumerate(cand):
            if num == 1:
                start_pos = k
        last = 0
        for i, num, heading in cand[start_pos:]:
            if num and last < num <= last + 2:
                chapters.append(dict(index=len(chapters) + 1, heading=heading, start=i))
                last = num
    elif book.get("split_chapter_re"):
        rx = re.compile(book["split_chapter_re"])
        lines = [x.strip() for x in body]
        for i, ln in enumerate(body):
            if i < toc_end:
                continue
            if not rx.match(ln.strip()):
                continue
            # heading is split over the following short upper-case lines
            parts = [ln.strip()]
            j = i + 1
            while j < len(body) and len(parts) < 6:
                t = lines[j]
                if not t:
                    j += 1
                    if j - i > 8:
                        break
                    continue
                if len(t) <= 40 and t == t.upper():
                    parts.append(t)
                    j += 1
                else:
                    break
            num = _num(ln.strip())
            if not num:
                continue
            if chapters and num != len(chapters) + 1:
                continue
            if not chapters and num != 1:
                continue
            chapters.append(dict(index=len(chapters) + 1, heading=" ".join(parts), start=i))
    elif book.get("toc_anchor") and toc_entries:
        keys = []
        for e in toc_entries:
            k = e.lower().strip(" .")
            if len(k) < 4 or k.startswith(("preface", "list of", "index", "bibliography", "facing page", "page")):
                continue
            keys.append((k, e))
        used = set()
        for i, ln in enumerate(body):
            if i < toc_end:
                continue
            stripped = ln.strip()
            # body section headings in these books are ALL-CAPS short lines
            if len(stripped) < 4 or len(stripped) > 70 or stripped != stripped.upper() or not re.search(r"[A-Z]", stripped):
                continue
            s = re.sub(r"\s+", " ", stripped).lower().strip(" .:")
            for idx, (k, orig) in enumerate(keys):
                if idx in used:
                    continue
                if s == k:
                    chapters.append(dict(index=len(chapters) + 1, heading=orig.strip(), start=i))
                    used.add(idx)
                    break
    if not chapters:
        chapters.append(dict(index=1, heading="(whole text)", start=0))
    chapters.sort(key=lambda c: c["start"])
    for i, c in enumerate(chapters):
        c["end"] = chapters[i + 1]["start"] if i + 1 < len(chapters) else len(body)
        c["index"] = i + 1
    return chapters


def build_paragraphs(body, chapters):
    """Attach paragraph numbers to chapter line ranges. Returns list of (line, para_no)."""
    para_by_line = {}
    for c in chapters:
        para = 0
        prev_blank = True
        for i in range(c["start"], c["end"]):
            if not body[i].strip():
                prev_blank = True
                continue
            if prev_blank:
                para += 1
                prev_blank = False
            para_by_line[i] = para
    return para_by_line


def locate(chapters, line):
    if chapters and line < chapters[0]["start"]:
        return dict(index=0, heading="(front matter: contents / illustrations)"), line
    for c in chapters:
        if c["start"] <= line < c["end"]:
            return c, line - c["start"]
    return chapters[-1], line - chapters[-1]["start"]


def snippet(lines, i, before=1, after=2, width=400):
    a = max(0, i - before)
    b = min(len(lines), i + after + 1)
    txt = " ".join(x.strip() for x in lines[a:b] if x.strip())
    return re.sub(r"\s+", " ", txt)[:width]


def extract_dictionary_entries(body):
    entries = []
    for i, ln in enumerate(body):
        m = re.match(r"^=([^=]{1,90})=[—\-]", ln)
        if not m:
            continue
        term = re.sub(r"\s+", " ", m.group(1)).strip()
        entries.append(dict(headword=term, line_no=i, snippet=snippet(body, i, 0, 1, 160)))
    return entries


def extract_terms(body, chapters, para_by_line, terms, max_hits=2000):
    hits = []
    for term in terms:
        rx = re.compile(r"(?<![\w-])" + re.escape(term) + r"(?![\w-])", re.I)
        for i, ln in enumerate(body):
            if not rx.search(ln):
                continue
            c, _ = locate(chapters, i)
            hits.append(dict(term=term, chapter_index=c["index"], chapter=c["heading"],
                             paragraph=para_by_line.get(i), line_no=i,
                             snippet=snippet(body, i, 1, 1, 240)))
    hits.sort(key=lambda h: (h["line_no"], h["term"]))
    return hits[:max_hits]


def find_entries(body, chapters, para_by_line, phrase):
    rx = re.compile(re.escape(phrase), re.I)
    out = []
    for i, ln in enumerate(body):
        if not rx.search(ln):
            continue
        c, _ = locate(chapters, i)
        out.append(dict(chapter_index=c["index"], chapter=c["heading"],
                        paragraph=para_by_line.get(i), line_no=i,
                        snippet=snippet(body, i, 1, 2, 500)))
    return out


def data_path(datadir, book_id):
    return os.path.join(datadir, "pg%s.txt" % book_id)


def ebook_url(book_id):
    return "https://www.gutenberg.org/cache/epub/%s/pg%s.txt" % (book_id, book_id)


def download(datadir):
    os.makedirs(datadir, exist_ok=True)
    for b in BOOKS:
        dest = data_path(datadir, b["id"])
        if os.path.exists(dest) and os.path.getsize(dest) > 10000:
            print("[skip] %s already present" % dest)
            continue
        url = ebook_url(b["id"])
        cmd = ["curl", "-sS", "-m", "60", "-L", "-o", dest, "-w", "%{http_code}", url]
        p = subprocess.run(cmd, capture_output=True, text=True)
        code = (p.stdout or "").strip()
        size = os.path.getsize(dest) if os.path.exists(dest) else 0
        print("[fetch] %s -> HTTP %s (%d bytes)" % (url, code, size))
        if code != "200" or size < 10000:
            print("  ERROR: download failed", file=sys.stderr)
            return 1
    return 0


def parse_book(book, datadir):
    path = data_path(datadir, book["id"])
    if not os.path.exists(path):
        raise SystemExit("missing text file: %s (run --download)" % path)
    raw = read_text(path)
    header, body = split_pg(raw)
    meta = pg_metadata(header)
    toc_raw, toc_entries, toc_end = extract_toc(body)
    chapters = detect_chapters(body, book, toc_entries, toc_end)
    para_by_line = build_paragraphs(body, chapters)
    hits = extract_terms(body, chapters, para_by_line, DEFAULT_TERMS)
    info = dict(
        book_id=book["id"], family=book.get("family", ""), repo=book.get("repo", ""),
        title=first_line(meta, "title") or book["title"],
        subtitle="",
        author=first_line(meta, "author") or book["author"],
        editor=first_line(meta, "editor"),
        illustrator=first_line(meta, "illustrator"),
        year=book.get("year", ""),
        publisher=book.get("publisher", ""),
        release_date=first_line(meta, "release date"),
        language=first_line(meta, "language"),
        original_publication=first_line(meta, "original publication"),
        credits=first_line(meta, "credits"),
        text_url=ebook_url(book["id"]),
        ebook_page="https://www.gutenberg.org/ebooks/%s" % book["id"],
        license="Public domain in the USA (Project Gutenberg); PG License applies to redistribution of PG-prepared text",
        lines_total=len(body),
        chapters=[dict(index=c["index"], heading=c["heading"], line_start=c["start"], line_end=c["end"]) for c in chapters],
        toc=[normalise(x) for x in toc_raw if normalise(x)][:120],
        terms=DEFAULT_TERMS,
        stats=dict(hits=len(hits), terms_hit=len(set(h["term"] for h in hits))),
        hits=hits,
    )
    if book.get("dictionary"):
        entries = extract_dictionary_entries(body)
        info["dictionary_entries"] = entries
        info["stats"]["dictionary_entries"] = len(entries)
    return info


def write_outputs(books, outdir):
    os.makedirs(outdir, exist_ok=True)
    for b in books:
        with open(os.path.join(outdir, "%s.json" % b["book_id"]), "w", encoding="utf-8") as fh:
            json.dump(b, fh, ensure_ascii=False, indent=1)
    summary_books = []
    for b in books:
        sb = {k: v for k, v in b.items() if k not in ("hits", "dictionary_entries", "terms")}
        sb["stats"] = dict(b["stats"])
        summary_books.append(sb)
    with open(os.path.join(outdir, "books_extract.json"), "w", encoding="utf-8") as fh:
        json.dump(summary_books, fh, ensure_ascii=False, indent=1)
    lines = ["# 公版书术语/结构命中摘要（books_extract.py 自动生成）", ""]
    lines.append("定位格式：`书ID / 章 / 段 / 行`。源文本为 Project Gutenberg 纯文本，无页码；页码需标 UNCONFIRMED。")
    lines.append("")
    for b in books:
        lines.append("## %s %s（%s，%s）" % (b["book_id"], b["title"], b["author"], b["year"]))
        lines.append("")
        lines.append("- 章节数：%d；术语命中：%d 条（%d 个不同术语）" % (
            len(b["chapters"]), b["stats"]["hits"], b["stats"]["terms_hit"]))
        if "dictionary_entries" in b:
            lines.append("- 词典词条数：%d" % b["stats"]["dictionary_entries"])
        lines.append("- 章节：" + "；".join("%d. %s" % (c["index"], c["heading"]) for c in b["chapters"][:40]))
        lines.append("")
    with open(os.path.join(outdir, "TERMS-HITS.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return outdir


def main():
    ap = argparse.ArgumentParser(description="Extract metadata/TOC/chapters/terms from audited public-domain books.")
    ap.add_argument("--dir", default="/tmp/p4books", help="directory holding pg<id>.txt (default /tmp/p4books)")
    ap.add_argument("--out", default="11-验收/P4-BOOKS/extracted", help="output directory")
    ap.add_argument("--book", help="only this book id")
    ap.add_argument("--download", action="store_true", help="download the 9 audited PD texts first")
    ap.add_argument("--search", help="substring search across parsed books, with locators")
    ap.add_argument("--locate", help="BOOKID:LINE -> chapter/paragraph locator")
    ap.add_argument("--json", action="store_true", help="print JSON summary")
    ap.add_argument("--max-hits", type=int, default=2000, help="cap term hits recorded per book")
    args = ap.parse_args()

    if args.download:
        rc = download(args.dir)
        if rc:
            return rc
    selected = [b for b in BOOKS if not args.book or b["id"] == args.book]
    if not selected:
        print("unknown book id: %s (known: %s)" % (args.book, ", ".join(b["id"] for b in BOOKS)), file=sys.stderr)
        return 1
    books = []
    for b in selected:
        info = parse_book(b, args.dir)
        info["hits"] = info["hits"][:args.max_hits]
        info["stats"]["hits"] = len(info["hits"])
        books.append(info)
    write_outputs(books, args.out)

    if args.search:
        for b in books:
            hits = find_entries(b["hits"] and b["hits"] and [] or [], [], {}, args.search) if False else []
        # direct text search with locators (independent of default terms)
        for b in books:
            path = data_path(args.dir, b["book_id"])
            raw = read_text(path)
            _, body = split_pg(raw)
            chapters = [dict(index=c["index"], heading=c["heading"], start=c["line_start"], end=c["line_end"]) for c in b["chapters"]]
            para = build_paragraphs(body, chapters)
            for h in find_entries(body, chapters, para, args.search):
                print("%s | %s | ch%d %s | para %s | line %d\n    %s" % (
                    b["book_id"], b["title"], h["chapter_index"], h["chapter"], h["paragraph"], h["line_no"], h["snippet"]))
        return 0

    if args.locate:
        m = re.match(r"^(\d+)[:,](\d+)$", args.locate)
        if not m:
            print("--locate expects BOOKID:LINE", file=sys.stderr)
            return 1
        bid, line = m.group(1), int(m.group(2))
        b = [x for x in books if x["book_id"] == bid]
        if not b:
            print("book not selected/parsed:", bid, file=sys.stderr)
            return 1
        b = b[0]
        path = data_path(args.dir, bid)
        _, body = split_pg(read_text(path))
        for c in b["chapters"]:
            if c["line_start"] <= line < c["line_end"]:
                chapters = [dict(index=x["index"], heading=x["heading"], start=x["line_start"], end=x["line_end"]) for x in b["chapters"]]
                para = build_paragraphs(body, chapters)
                print("book %s %s\nchapter %d: %s\nparagraph: %s\nline %d\n%s" % (
                    bid, b["title"], c["index"], c["heading"], para.get(line), line, snippet(body, line, 1, 2, 600)))
                return 0
        print("line out of range", file=sys.stderr)
        return 1

    summary = [dict(book_id=b["book_id"], title=b["title"], author=b["author"], year=b["year"],
                    lines=b["lines_total"], chapters=len(b["chapters"]), hits=b["stats"]["hits"],
                    terms_hit=b["stats"]["terms_hit"],
                    dictionary_entries=b["stats"].get("dictionary_entries"))
               for b in books]
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
    else:
        print("parsed %d books -> %s" % (len(books), args.out))
        for s in summary:
            print("  %-6s %-55s ch=%-3d hits=%-5d terms=%-3d entries=%s" % (
                s["book_id"], s["title"][:55], s["chapters"], s["hits"], s["terms_hit"], s["dictionary_entries"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
