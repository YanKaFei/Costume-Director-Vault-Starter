#!/usr/bin/env python3
"""audit_knowledge.py - R1 knowledge-quality audit (read-only).

Eight check domains (task-48):
  1. duplicate / near-duplicate / conflicting cards (e.g. GAR-0001 vs GAR-0065)
  2. book citation locators: verify claims back to Project Gutenberg text
     (chapter / paragraph / line; page must be UNCONFIRMED)
  3. period / region / culture mislabels
  4. v1.2 optional attributes, wikilinks, source_ids completeness
  5. fact / evidence / inference separation (cards + recommendation outputs)
  6. P3.5 62 draft traceability vs reports/DRAFT-REVIEW.csv
  7. license_status vs rights_statement mislabels + 0-image policy
  8. proposal data: per-card suggested data_status / content_verified /
     license_verified (audit-only, schema unchanged)

The script NEVER writes to the vault. It prints a human summary and can emit
JSON with --json (caller may redirect to /tmp).

Usage:
  python3 scripts/audit_knowledge.py            # summary + findings
  python3 scripts/audit_knowledge.py --json     # machine-readable report
Exit code: 0 always (report generator); 2 on fatal load error.
"""

import argparse
import csv
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARD_DIRS = ["01-服装单品", "02-结构细节", "03-材质纹样", "04-来源", "05-风格体系",
             "06-时代地域", "07-剧情场景", "09-造型组合"]
SKIP_DIRS = ("00-系统", "TASKS", "skills", "docs", "projects", "reports", "tests",
             "11-验收", ".git", "scripts")
CARD_EXTS = (".md",)
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".bmp", ".tif", ".tiff")

V12_DOC = "00-系统/数据字典-v1.2-扩展.md"
DRAFT_CSV = "reports/DRAFT-REVIEW.csv"
BOOK_NOTES = "06-时代地域/书籍研究/书籍研究-历史服饰术语与结构.md"
EXTRACT_DIR = "11-验收/P4-BOOKS/extracted"
BOOK_CACHE = "/tmp/audit_books"

PG_BOOKS = {
    "34903": "https://www.gutenberg.org/cache/epub/34903/pg34903.txt",
    "21534": "https://www.gutenberg.org/cache/epub/21534/pg21534.txt",
    "33020": "https://www.gutenberg.org/cache/epub/33020/pg33020.txt",
    "48551": "https://www.gutenberg.org/cache/epub/48551/pg48551.txt",
    "49559": "https://www.gutenberg.org/cache/epub/49559/pg49559.txt",
    "76299": "https://www.gutenberg.org/cache/epub/76299/pg76299.txt",
    "56978": "https://www.gutenberg.org/cache/epub/56978/pg56978.txt",
    "76717": "https://www.gutenberg.org/cache/epub/76717/pg76717.txt",
    "46949": "https://www.gutenberg.org/cache/epub/46949/pg46949.txt",
}


def norm_id(s):
    return str(s).strip()


def load_cards():
    cards = {}
    dups = []
    for d in CARD_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for path in sorted(glob.glob(os.path.join(base, "**", "*.md"), recursive=True)):
            txt = open(path, encoding="utf-8", errors="ignore").read()
            m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
            if not m:
                continue
            fm = parse_yaml_min(m.group(1))
            if not fm or "id" not in fm:
                continue
            cid = norm_id(fm["id"])
            if cid in cards:
                dups.append(dict(id=cid, first=cards[cid]["rel"], second=os.path.relpath(path, ROOT)))
                continue
            cards[cid] = dict(id=cid, rel=os.path.relpath(path, ROOT), dir=d, fm=fm,
                              body=txt[m.end():], text=txt)
    return cards, dups


def parse_yaml_min(y):
    """Small YAML subset parser (flat scalars/lists) - no PyYAML dependency."""
    out = {}
    for line in y.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            continue
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if not m:
            continue
        k, v = m.group(1), m.group(2).strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            vals = []
            if inner:
                for part in re.split(r",(?![^'\"]*['\"])", inner):
                    p = part.strip().strip("'\"")
                    if p:
                        vals.append(p)
            out[k] = vals
        elif v.startswith(("'", '"')) and v.endswith(("'", '"')) and len(v) >= 2:
            out[k] = v[1:-1]
        elif v == "":
            out[k] = ""
        else:
            out[k] = v
    return out


def load_v12_schema():
    path = os.path.join(ROOT, V12_DOC)
    schema = {}
    if not os.path.exists(path):
        return schema
    for line in open(path, encoding="utf-8"):
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        field = cells[0].strip("` ")
        typ = cells[1]
        applies = cells[2]
        values = re.findall(r"`([a-z0-9_']+)`", cells[3])
        list_field = "list" in typ
        schema[field] = dict(type=typ, applies=applies, values=set(values), list_field=list_field, raw=cells[3])
    return schema


def as_list(v):
    if isinstance(v, list):
        return v
    if v in ("", None):
        return []
    return [str(v)]


# ---------------- 1. duplicates / conflicts ----------------
def check_duplicates(cards):
    findings = []
    by_type = {}
    for cid, c in cards.items():
        by_type.setdefault(c["fm"].get("type"), []).append(cid)
    name_dups, alias_coll, near_dups = [], [], []
    for typ, ids in by_type.items():
        nz, ne = {}, {}
        for cid in ids:
            fm = cards[cid]["fm"]
            if fm.get("name_zh"):
                nz.setdefault(str(fm["name_zh"]).strip(), []).append(cid)
            if fm.get("name_en"):
                ne.setdefault(str(fm["name_en"]).strip().lower(), []).append(cid)
        for k, v in nz.items():
            if len(v) > 1:
                name_dups.append(dict(kind="name_zh", value=k, ids=v))
        for k, v in ne.items():
            if len(v) > 1:
                name_dups.append(dict(kind="name_en", value=k, ids=v))
        # alias collisions
        alias_map = {}
        for cid in ids:
            fm = cards[cid]["fm"]
            for a in as_list(fm.get("aliases")):
                alias_map.setdefault(str(a).strip().lower(), []).append(cid)
        for cid in ids:
            fm = cards[cid]["fm"]
            names = {str(fm.get("name_zh", "")).strip().lower(), str(fm.get("name_en", "")).strip().lower()}
            for a in as_list(fm.get("aliases")):
                owners = alias_map.get(str(a).strip().lower(), [])
                if len(owners) > 1 and cid in owners:
                    for other in owners:
                        if other != cid:
                            alias_coll.append(dict(alias=a, ids=sorted([cid, other])))
    # de-dup alias collisions
    seen = set()
    uniq_alias = []
    for a in alias_coll:
        key = tuple(a["ids"])
        if key in seen:
            continue
        seen.add(key)
        uniq_alias.append(a)
    # near duplicates: same type + category/subcategory + token overlap of names
    ids_all = [cid for cid in cards]
    for i in range(len(ids_all)):
        for j in range(i + 1, len(ids_all)):
            a, b = cards[ids_all[i]], cards[ids_all[j]]
            if a["fm"].get("type") != b["fm"].get("type"):
                continue
            if a["fm"].get("category") != b["fm"].get("category") or a["fm"].get("subcategory") != b["fm"].get("subcategory"):
                continue
            ta = tokens(a["fm"].get("name_en", "") + " " + a["fm"].get("name_zh", ""))
            tb = tokens(b["fm"].get("name_en", "") + " " + b["fm"].get("name_zh", ""))
            if not ta or not tb:
                continue
            inter = len(ta & tb)
            union = len(ta | tb)
            if inter and union and inter / union >= 0.6:
                near_dups.append(dict(ids=[a["id"], b["id"]], names=[a["fm"].get("name_zh"), b["fm"].get("name_zh")],
                                      category=a["fm"].get("category"), jaccard=round(inter / union, 2)))
    return dict(name_dups=name_dups, alias_collisions=uniq_alias, near_dups=near_dups)


def tokens(s):
    s = unicodedata.normalize("NFKC", str(s or "")).lower()
    latin = re.findall(r"[a-z0-9]{3,}", s)
    cjk = re.findall(r"[\u4e00-\u9fff]{2,4}", s)
    stop = {"the", "and", "for", "with", "garment", "card", "example", "look"}
    return set(w for w in latin if w not in stop) | set(cjk)


def compare_pair(cards, id_a, id_b):
    a, b = cards[id_a]["fm"], cards[id_b]["fm"]
    keys = ["type", "category", "subcategory", "periods", "regions", "materials", "colors",
            "silhouette", "fit", "formality", "evidence_status", "source_ids"]
    diff = {}
    for k in keys:
        va, vb = a.get(k), b.get(k)
        if str(va) != str(vb):
            diff[k] = [str(va), str(vb)]
    overlap_periods = set(as_list(a.get("periods"))) & set(as_list(b.get("periods")))
    overlap_aliases = set(x.lower() for x in as_list(a.get("aliases"))) & set(x.lower() for x in as_list(b.get("aliases")))
    if a.get("name_zh") == b.get("name_zh") and a.get("name_en") == b.get("name_en"):
        verdict = "CONFLICT: same name_zh+name_en"
    elif overlap_aliases and overlap_periods:
        verdict = "ALIAS-OVERLAP: distinct names but shared alias + overlapping periods (needs scope disambiguation)"
    elif overlap_aliases:
        verdict = "ALIAS-ONLY: shared alias, periods disjoint (likely distinct variants)"
    elif overlap_periods:
        verdict = "SCOPE-OVERLAP: same period/type, different names"
    else:
        verdict = "DISTINCT: different names, disjoint periods"
    return dict(ids=[id_a, id_b], verdict=verdict, field_diff=diff,
                shared_aliases=sorted(overlap_aliases), shared_periods=sorted(overlap_periods))


# ---------------- 2. book locator checks ----------------
def _valid_pg(path):
    """A PG text is complete only if it has the START marker, the END marker and >100KB."""
    if not path or not os.path.exists(path) or os.path.getsize(path) < 100000:
        return False
    try:
        head = open(path, encoding="utf-8", errors="ignore").read(200000)
    except Exception:
        return False
    if "START OF THE PROJECT GUTENBERG" not in head and "START OF THIS PROJECT GUTENBERG" not in head:
        return False
    tail = open(path, encoding="utf-8", errors="ignore").read()[-300000:]
    return ("END OF THE PROJECT GUTENBERG" in tail or "END OF THIS PROJECT GUTENBERG" in tail)


def ensure_book_text(pg):
    """Return path to a COMPLETE PG text, reusing /tmp/p4books or downloading with validation.

    Truncated downloads (the Gutenberg host occasionally resets long transfers) are
    rejected: a text without the END marker would produce false locator failures.
    """
    os.makedirs(BOOK_CACHE, exist_ok=True)
    for candidate in (os.path.join("/tmp/p4books", "pg%s.txt" % pg),
                      os.path.join(BOOK_CACHE, "pg%s.txt" % pg)):
        if _valid_pg(candidate):
            return candidate
    path = os.path.join(BOOK_CACHE, "pg%s.txt" % pg)
    url = PG_BOOKS[pg]
    for _ in range(3):
        p = subprocess.run(["curl", "-sS", "-m", "300", "-L", "-o", path, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        if (p.stdout or "").strip() == "200" and _valid_pg(path):
            return path
    return None


def split_pg(raw):
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start, end = 0, len(lines)
    for i, ln in enumerate(lines):
        if re.search(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", ln, re.I):
            start = i + 1
            break
    for i in range(len(lines) - 1, start, -1):
        if re.search(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", lines[i], re.I):
            end = i
            break
    return lines[start:end]


def load_chapters(pg):
    p = os.path.join(ROOT, EXTRACT_DIR, "%s.json" % pg)
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    return [dict(index=c["index"], heading=c["heading"], start=c["line_start"], end=c["line_end"])
            for c in d["chapters"]], d


def paragraphs_for(body, chapters):
    para = {}
    for c in chapters:
        n = 0
        prev_blank = True
        for i in range(c["start"], min(c["end"], len(body))):
            if not body[i].strip():
                prev_blank = True
                continue
            if prev_blank:
                n += 1
                prev_blank = False
            para[i] = n
    return para


def parse_book_conclusions():
    path = os.path.join(ROOT, BOOK_NOTES)
    if not os.path.exists(path):
        return []
    txt = open(path, encoding="utf-8").read()
    blocks = re.split(r"^## (C\d+) ", txt, flags=re.M)
    out = []
    for i in range(1, len(blocks), 2):
        cid = blocks[i]
        block = blocks[i + 1]
        head = block.split("\n", 1)[0]
        m = re.search(r"PG (\d+)", head)
        if not m:
            continue
        pg = m.group(1)
        loc = re.search(r"- 定位：(.+?) / 段 (\d+) / 行 (\d+)（页码 (UNCONFIRMED|PAGE)）", block)
        stmt = re.search(r"- \*\*书内事实\*\*：(.+)", block)
        if not loc or not stmt:
            continue
        out.append(dict(id=cid, pg=pg, chapter=loc.group(1).strip(), para=int(loc.group(2)),
                        line=int(loc.group(3)), page=loc.group(4), stmt=stmt.group(1).strip()))
    return out


def check_book_locators(conclusions):
    results = []
    cache = {}
    for c in conclusions:
        pg = c["pg"]
        if pg not in cache:
            path = ensure_book_text(pg)
            cache[pg] = dict(path=path)
            if path:
                cache[pg]["body"] = split_pg(open(path, encoding="utf-8", errors="ignore").read())
                ch = load_chapters(pg)
                cache[pg]["chapters"] = ch[0] if ch else None
                cache[pg]["extract"] = ch[1] if ch else None
                if cache[pg]["chapters"]:
                    cache[pg]["para"] = paragraphs_for(cache[pg]["body"], cache[pg]["chapters"])
        ent = cache[pg]
        r = dict(id=c["id"], pg=pg, line=c["line"], para=c["para"], chapter=c["chapter"], page=c["page"],
                 status="PASS", notes=[])
        if not ent.get("body"):
            r.update(status="FAIL", notes=["book text unavailable (network/cache)"])
            results.append(r)
            continue
        body, chapters = ent["body"], ent.get("chapters")
        if not chapters:
            r.update(status="FAIL", notes=["chapter metadata missing"])
            results.append(r)
            continue
        if not (0 <= c["line"] < len(body)):
            r.update(status="FAIL", notes=["line out of range %d/%d" % (c["line"], len(body))])
            results.append(r)
            continue
        actual_para = ent["para"].get(c["line"])
        ch = [x for x in chapters if x["start"] <= c["line"] < x["end"]]
        actual_ch = ch[0] if ch else None
        # paragraph check
        if actual_para is not None and actual_para != c["para"]:
            r["status"] = "WARN"
            r["notes"].append("paragraph mismatch cited=%s actual=%s" % (c["para"], actual_para))
        # chapter check
        if actual_ch:
            cited = c["chapter"]
            if cited.startswith("词条「"):
                hw = cited.strip("词条「」")
                entries = (ent.get("extract") or {}).get("dictionary_entries") or []
                best = None
                for e in entries:
                    if e["line_no"] <= c["line"]:
                        best = e
                    else:
                        break
                if not best or best["headword"].strip().lower() != hw.strip().lower():
                    r["status"] = "WARN"
                    r["notes"].append("dictionary headword mismatch cited=%s actual=%s" % (hw, best["headword"] if best else None))
            elif actual_ch["heading"].strip() != cited.strip() and not cited.startswith("文集"):
                # tolerate numbering/format differences: compare core words
                if tokens(actual_ch["heading"]) and not (tokens(actual_ch["heading"]) & tokens(cited)):
                    r["status"] = "WARN"
                    r["notes"].append("chapter mismatch cited=%r actual=%r" % (cited, actual_ch["heading"]))
        # content check: ascii keywords from the claim must appear in the located paragraph
        i = c["line"]
        a = i
        while a > 0 and body[a - 1].strip():
            a -= 1
        b = i
        while b < len(body) and body[b].strip():
            b += 1
        para_txt = " ".join(x.strip() for x in body[a:b]).lower()
        win_a, win_b = max(0, a - 12), min(len(body), b + 12)
        window_txt = " ".join(x.strip() for x in body[win_a:win_b]).lower()
        para_norm = re.sub(r"[^a-z0-9]", "", para_txt)
        win_norm = re.sub(r"[^a-z0-9]", "", window_txt)
        ascii_tokens = [w for w in re.findall(r"[a-z][a-z\-]{3,}", c["stmt"].lower())]
        quoted = re.findall(r"[`\"“]([^`\"”]{3,60})[`\"”]", c["stmt"])
        checks = []
        for q in quoted:
            qn = re.sub(r"[^a-z0-9]", "", q.lower())
            checks.append((q.lower() in para_txt or (qn and qn in para_norm),
                           "quote:%s" % q[:40]))
        hit = sum(1 for w in ascii_tokens if w in para_txt or w.replace("-", "") in para_norm)
        if ascii_tokens:
            checks.append((hit >= max(1, min(2, len(ascii_tokens))), "ascii_hits=%d/%d" % (hit, len(ascii_tokens))))
            if hit == 0:
                win_hit = sum(1 for w in ascii_tokens if w in window_txt or w.replace("-", "") in win_norm)
                if win_hit:
                    r["status"] = "WARN"
                    r["notes"].append("keyword found in ±12-line window, not in cited paragraph")
                    checks.append((True, "window_hits=%d" % win_hit))
        if not checks:
            r["status"] = "MANUAL"
            r["notes"].append("no machine-checkable quote/keyword (needs human)")
        else:
            ok = any(ok_ for ok_, _ in checks)
            r["notes"].extend(desc for ok_, desc in checks)
            if not ok and r["status"] == "PASS":
                r["status"] = "FAIL"
        if c["page"] != "UNCONFIRMED":
            if r["status"] == "PASS":
                r["status"] = "WARN"
            r["notes"].append("page locator not marked UNCONFIRMED")
        r["actual_chapter"] = actual_ch["heading"] if actual_ch else None
        r["actual_para"] = actual_para
        results.append(r)
    return results


# ---------------- 3. period / region / culture ----------------
REGION_GROUPS = {
    "china": r"china|chinese|shanghai|beijing|qing|qipao|changshan|\u4e2d\u56fd|\u4e0a\u6d77|\u65d7\u888d|\u957f\u886b",
    "japan": r"japan|japanese|edo|meiji|kimono|\u65e5\u672c|\u548c\u670d",
    "korea": r"korea|korean|hanbok|\u671d\u9c9c|\u97e9\u56fd|\u97e9\u670d",
    "india": r"india|indian|mughal|jama|sari|angarkha|\u5370\u5ea6|\u83ab\u5367\u513f",
    "nigeria": r"nigeria|yoruba|agbada|gele|\u5c3c\u65e5\u5229\u4e9a",
    "turkey": r"ottoman|turkish|fez|\u5965\u65af\u66fc|\u571f\u8033\u5176",
    "scotland": r"scotland|scottish|macbeth|\u82cf\u683c\u5170",
    "france": r"france|french|paris|\u6cd5\u56fd|\u5df4\u9ece",
    "england": r"england|english|british|britain|london|\u82f1\u56fd|\u82f1\u683c\u5170",
    "italy": r"italy|italian|florence|venice|\u610f\u5927\u5229",
    "egypt": r"egypt|egyptian|coptic|\u57c3\u53ca",
    "byzantium": r"byzantine|byzantium|\u62dc\u5360\u5ead",
    "america": r"american|united states|u\.s\.|\u7f8e\u56fd",
}
REGION_ALIASES = {  # field region value -> canonical group
    "china": "china", "japan": "japan", "korea": "korea", "india": "india",
    "nigeria": "nigeria", "turkey": "turkey", "ottoman": "turkey", "scotland": "scotland",
    "france": "france", "england": "england", "britain": "england", "united_kingdom": "england",
    "uk": "england", "italy": "italy", "egypt": "egypt", "byzantium": "byzantium",
    "united_states": "america", "usa": "america", "america": "america",
    "europe": "europe", "western_europe": "europe", "northern_europe": "europe",
    "north_america": "america", "japan_export": "japan",
}
NEGATION_LINES = ("\u4e0d\u9002\u7528", "\u6613\u6df7", "\u6df7\u6dc6", "\u53ca\u4ee5\u540e", "\u4e4b\u540e", "\u5bf9\u6bd4", "\u53cd\u4f8b", "\u907f\u514d", "\u4e0d\u5f97", "\u4e0d\u80fd", "\u7981\u6b62")


def check_period_region(cards):
    issues = []
    for cid, c in cards.items():
        fm = c["fm"]
        if fm.get("type") == "source":
            continue
        regions = [str(x).lower() for x in as_list(fm.get("regions"))]
        periods = [str(x).lower() for x in as_list(fm.get("periods"))]
        body = c["text"].lower()
        body_lines = c["text"].splitlines()
        # score canonical region groups with word boundaries
        scores = {}
        for grp, pat in REGION_GROUPS.items():
            scores[grp] = len(re.findall(pat, body, re.I))
        own = set()
        for r in regions:
            if r in REGION_ALIASES:
                own.add(REGION_ALIASES[r])
            else:
                for grp in REGION_GROUPS:
                    if grp in r:
                        own.add(grp)
        if regions and own:
            own_score = sum(scores.get(g, 0) for g in own)
            other = {g: sc for g, sc in scores.items() if g not in own and sc > 0}
            if other:
                top = max(other, key=other.get)
                if own_score == 0 and other[top] >= 3:
                    issues.append(dict(id=cid, kind="region_words_absent", regions=regions,
                                       body_top_region=top, body_score=other[top], severity="P1"))
                elif other[top] >= 5 and other[top] > own_score * 2:
                    issues.append(dict(id=cid, kind="region_dominant_other", regions=regions,
                                       body_top_region=top, body_score=other[top], own_score=own_score,
                                       severity="P2"))
        # period check: ignore negation/contrast lines
        kept = [ln for ln in body_lines if not any(neg in ln for neg in NEGATION_LINES)]
        kept_text = "\n".join(kept).lower()
        body_decades = set(re.findall(r"\b(1[5-9]\d0|20[0-2]0)s\b", kept_text))
        card_decades = set()
        for p in periods:
            m = re.match(r"^(1[5-9]\d0|20[0-2]0)s$", p)
            if m:
                card_decades.add(m.group(1))
        if card_decades and body_decades:
            unknown = body_decades - card_decades
            if unknown and len(unknown) >= 2:
                issues.append(dict(id=cid, kind="body_decades_not_in_periods", periods=periods,
                                   body_decades=sorted(unknown), severity="P2"))
        # missing dimensions (examples excluded)
        if fm.get("type") in ("garment", "look", "period_region", "style", "scene"):
            if not periods and not regions and fm.get("evidence_status") != "example":
                issues.append(dict(id=cid, kind="missing_period_and_region", severity="P2"))
    return issues


def check_period_region_targeted(cards):
    """Targeted culture/period spot checks requested by task-48."""
    groups = [
        dict(label="1930s Shanghai / qipao / changshan", kw=["上海", "旗袍", "长衫", "qipao", "changshan", "shanghai"],
             need_periods={"1930s"}, need_regions={"china"}),
        dict(label="Macbeth (11th century Scotland)", kw=["macbeth", "麦克白"],
             need_periods={"11th_century", "middle_ages", "medieval"}, need_regions={"scotland"}),
        dict(label="Japanese kimono", kw=["和服", "kimono", "着物"], need_periods=set(), need_regions={"japan"}),
        dict(label="Korean hanbok", kw=["hanbok", "韩服", "한복"], need_periods=set(), need_regions={"korea"}),
        dict(label="Indian jama / angarkha", kw=["jama", "angarkha", "莫卧儿", "mughal"], need_periods=set(), need_regions={"india"}),
        dict(label="Nigerian agbada", kw=["agbada", "agbádá", "尼日利亚"], need_periods=set(), need_regions={"nigeria"}),
        dict(label="P4 v1.2 new cards", kw=[], need_periods=set(), need_regions=set()),
    ]
    out = []
    for g in groups:
        rows = []
        if g["label"].startswith("P4"):
            cand = [cid for cid, c in cards.items() if re.match(r"^(GAR-0(07[5-9]|0[89]\d|1\d\d)|STR-00(1[2-9]|2[0-9])|MAT-00(1[2-9]))$", cid)]
        else:
            def hay(c):
                fm = c["fm"]
                return " ".join([str(fm.get("name_zh", "")), str(fm.get("name_en", "")),
                                 " ".join(str(x) for x in as_list(fm.get("aliases"))),
                                 " ".join(str(x) for x in as_list(fm.get("tags")))]).lower()
            cand = [cid for cid, c in cards.items()
                    if c["fm"].get("type") != "source"
                    and any(str(k).lower() in hay(c) for k in g["kw"])]
        for cid in cand:
            fm = cards[cid]["fm"]
            periods = set(str(x).lower() for x in as_list(fm.get("periods")))
            regions = set(str(x).lower() for x in as_list(fm.get("regions")))
            ok_p = (not g["need_periods"]) or bool(periods & g["need_periods"]) or bool(periods & {"early_20th_century"}) and ("1930s" in g["need_periods"])
            ok_r = (not g["need_regions"]) or bool(regions & g["need_regions"])
            if not (ok_p and ok_r):
                rows.append(dict(id=cid, name_zh=fm.get("name_zh"), periods=sorted(periods), regions=sorted(regions),
                                 ok_period=ok_p, ok_region=ok_r))
        out.append(dict(label=g["label"], candidates=len(cand), violations=rows))
    return out



# ---------------- 4. v1.2 attributes / links / source_ids ----------------
def check_v12(cards, schema):
    issues = []
    link_targets = {cid for cid in cards}
    files = set()
    for cid, c in cards.items():
        base = os.path.basename(c["rel"])
        files.add(os.path.splitext(base)[0])
    for cid, c in cards.items():
        fm, body = c["fm"], c["body"]
        # optional field values
        used = 0
        for field, spec in schema.items():
            if field not in fm:
                continue
            used += 1
            val = fm[field]
            if spec["list_field"]:
                if not isinstance(val, list):
                    issues.append(dict(id=cid, kind="v12_type", field=field, value=str(val), severity="P2"))
                    continue
                vals = [str(x) for x in val]
            else:
                vals = [str(val)]
            if field == "panel_count":
                if not all(re.fullmatch(r"\d+|unknown", v) for v in vals):
                    issues.append(dict(id=cid, kind="v12_value", field=field, value=str(val), severity="P2"))
                continue
            bad = [v for v in vals if v.strip("'") not in spec["values"]]
            if bad:
                issues.append(dict(id=cid, kind="v12_value", field=field, value=", ".join(bad), severity="P1"))
            # applies-to type check
            if fm.get("type") not in spec["applies"]:
                issues.append(dict(id=cid, kind="v12_applies", field=field, type=fm.get("type"), severity="P2"))
        if used:
            c["_v12_used"] = used
        # v1.2 conflicts with required fit
        fc, fit = fm.get("fit_class"), fm.get("fit")
        if fc and fit:
            mapping = {"slim": {"slim", "fitted", "tailored"},
                       "regular": {"regular", "straight", "semi_fitted"},
                       "relaxed": {"relaxed", "loose", "oversized"},
                       "oversized": {"oversized", "loose", "relaxed"},
                       "bodycon": {"bodycon", "fitted", "slim"}}
            if str(fit) not in mapping.get(str(fc), set()):
                issues.append(dict(id=cid, kind="v12_conflict_fit", fit_class=fc, fit=fit, severity="P2"))
        # wikilinks resolve
        for target in re.findall(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]", body):
            t = target.strip().split("/")[0]
            if t not in link_targets and t not in files:
                issues.append(dict(id=cid, kind="broken_wikilink", target=t, severity="P1"))
        # source_ids resolve
        if fm.get("type") != "source":
            for sid in as_list(fm.get("source_ids")):
                if sid not in cards:
                    issues.append(dict(id=cid, kind="unresolved_source_id", source_id=sid, severity="P0"))
            if fm.get("evidence_status") == "verified" and not as_list(fm.get("source_ids")):
                issues.append(dict(id=cid, kind="verified_without_source", severity="P0"))
        # required sections + related links for content cards
        if fm.get("type") != "source":
            for sec in ("定义", "来源链接"):
                if sec not in body:
                    issues.append(dict(id=cid, kind="missing_section", section=sec, severity="P1"))
            if "相关卡片" not in body:
                issues.append(dict(id=cid, kind="missing_section", section="相关卡片", severity="P2"))
    return issues


# ---------------- 5. fact / evidence / inference separation ----------------
def check_separation(cards):
    issues = []
    boundary = ["interpretive", "解释", "推断", "设计", "假设", "限制", "不适用", "风险", "unknown",
                "不得", "不能", "unknown", "unverified"]
    neg = ("不得", "不是", "禁止", "避免", "切勿", "不应", "不可", "不能", "避免把")
    for cid, c in cards.items():
        fm = c["fm"]
        if fm.get("type") == "source":
            continue
        es = fm.get("evidence_status")
        body = c["body"]
        low = body.lower()
        if es == "verified":
            if not any(b in low for b in boundary):
                issues.append(dict(id=cid, kind="verified_no_boundary_marker", severity="P3"))
        if es in ("interpretive", "example"):
            bad_lines = [ln for ln in body.splitlines()
                         if re.search(r"(已核实|经验证(?!明)|经核实|确证为)", ln)]
            if bad_lines:
                issues.append(dict(id=cid, kind="interpretive_claims_verified",
                                   lines=[l.strip()[:110] for l in bad_lines[:3]], severity="P1"))
    return issues


def check_output_separation():
    """Check recommendation / scene outputs for explicit fact / evidence / inference separation."""
    out = dict(files=[], json_outputs=[])
    base = os.path.join(ROOT, "11-验收/测试结果")
    if os.path.isdir(base):
        for path in sorted(glob.glob(os.path.join(base, "T*.md"))):
            txt = open(path, encoding="utf-8", errors="ignore").read()
            low = txt.lower()
            markers = dict(
                known=("实际输入" in txt or "已知" in txt),
                assumption=("假设" in txt or "unknown" in low or "假定" in txt),
                evidence=("证据" in txt or "来源" in txt or "source" in low),
                risk=("风险" in txt or "限制" in txt or "unconfirmed" in low or "不确定" in txt),
                interpretation=("解释" in txt or "推断" in txt or "导演" in txt or "interpret" in low),
            )
            out["files"].append(dict(id=os.path.relpath(path, ROOT), markers=markers,
                                     missing=[k for k, v in markers.items() if not v],
                                     has_missing_baseline=not markers["assumption"]))
    jdir = os.path.join(ROOT, "11-验收/P4-MACBETH/outputs")
    if os.path.isdir(jdir):
        for path in sorted(glob.glob(os.path.join(jdir, "*.json"))):
            try:
                d = json.load(open(path, encoding="utf-8"))
            except Exception:
                continue
            keys = set(d.keys())
            comp = d.get("composer") if isinstance(d.get("composer"), dict) else {}
            looks = comp.get("looks") or d.get("looks") or []
            risk_in_looks = False
            if isinstance(looks, list):
                for lk in looks:
                    if isinstance(lk, dict) and (lk.get("risks") or (lk.get("evidence") and lk["evidence"].get("source_ids"))):
                        risk_in_looks = True
                        break
            ok = bool({"evidence", "risks", "warnings"} <= keys or ({"evidence"} <= keys and risk_in_looks))
            out["json_outputs"].append(dict(id=os.path.relpath(path, ROOT), separation_ok=ok,
                                            keys=sorted(k for k in ("evidence", "risks", "warnings", "input") if k in keys)))
    return out


# ---------------- 6. 62 drafts traceability ----------------
def check_drafts(cards):
    path = os.path.join(ROOT, DRAFT_CSV)
    rows = list(csv.DictReader(open(path, encoding="utf-8"))) if os.path.exists(path) else []
    ids = {r["card_id"] for r in rows}
    missing = [cid for cid in ids if cid not in cards]
    current = {}
    for cid in ids:
        if cid not in cards:
            continue
        fm = cards[cid]["fm"]
        current[cid] = dict(review=fm.get("review_status"), evidence=fm.get("evidence_status"))
    drift = []
    for r in rows:
        cid = r["card_id"]
        if cid not in current:
            continue
        if r.get("current_review_status") != current[cid]["review"]:
            drift.append(dict(id=cid, csv=r.get("current_review_status"), now=current[cid]["review"]))
        if r.get("current_evidence_status") != current[cid]["evidence"]:
            drift.append(dict(id=cid, field="evidence_status", csv=r.get("current_evidence_status"), now=current[cid]["evidence"]))
    drafts_now = [cid for cid, c in cards.items() if c["fm"].get("review_status") == "draft"]
    drafts_no_record = [cid for cid in drafts_now if cid not in ids]
    conclusions = {}
    for r in rows:
        c = (r.get("conclusion") or "").split(" —")[0].strip()
        conclusions[c] = conclusions.get(c, 0) + 1
    return dict(rows=len(rows), csv_ids=sorted(ids), missing_in_cards=missing, drift=drift,
                drafts_now=len(drafts_now), drafts_no_record=drafts_no_record,
                conclusions=conclusions,
                reviewed_now=sum(1 for c in current.values() if c["review"] == "reviewed"),
                still_draft=sum(1 for c in current.values() if c["review"] == "draft"))


# ---------------- 7. license / images ----------------
def check_license(cards):
    issues = []
    for cid, c in cards.items():
        fm = c["fm"]
        lic = str(fm.get("license_status", ""))
        rights = str(fm.get("rights_statement", ""))
        low = rights.lower()
        if fm.get("type") == "source":
            if lic in ("cc0", "cc_by") and ("©" in rights or "仅可链接" in rights or "不得复制" in low):
                issues.append(dict(id=cid, kind="license_cc_vs_restrictive_rights", license=lic,
                                   rights=rights[:120], severity="P1"))
            if lic == "link_only" and any(k in low for k in ("cc0", "public domain", "cc by", "cc-by")):
                issues.append(dict(id=cid, kind="license_linkonly_vs_open_rights", license=lic,
                                   rights=rights[:120], severity="P1"))
            if lic not in ("cc0", "cc_by", "other_permission", "link_only", "not_applicable", "unknown"):
                issues.append(dict(id=cid, kind="license_enum", license=lic, severity="P0"))
        else:
            if lic not in ("not_applicable", "unknown"):
                issues.append(dict(id=cid, kind="content_card_license_status", license=lic, severity="P2"))
    # 0-image policy
    embedded, image_files = [], []
    for path in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, ROOT)
        if rel.startswith(".git"):
            continue
        txt = open(path, encoding="utf-8", errors="ignore").read()
        if re.search(r"!\[[^\]]*\]\([^)]+\)", txt):
            embedded.append(rel)
    for path in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        if os.path.isfile(path) and path.lower().endswith(IMAGE_EXTS) and "/.git/" not in path:
            image_files.append(os.path.relpath(path, ROOT))
    return dict(issues=issues, embedded_images=embedded, image_files=image_files)


# ---------------- 8. proposed independent statuses ----------------
def propose_status(cards, dup_info, loc_results, lic_info):
    v = {}
    for cid, c in cards.items():
        fm = c["fm"]
        checks = []
        content = "unverified"
        if fm.get("type") == "source":
            lic = str(fm.get("license_status", ""))
            content = "source_card"
        else:
            srcs = as_list(fm.get("source_ids"))
            if fm.get("evidence_status") == "verified" and srcs and all(s in cards for s in srcs):
                content = "verified_with_sources"
            elif srcs and all(s in cards for s in srcs):
                content = "interpretive_with_sources"
            elif fm.get("evidence_status") == "example":
                content = "example"
            else:
                content = "no_source"
        lic_state = "not_applicable" if fm.get("type") != "source" else (
            "verified" if fm.get("license_status") in ("cc0", "cc_by", "other_permission", "link_only", "not_applicable", "unknown") else "missing")
        data_state = "ambiguous"
        if fm.get("type") == "source":
            data_state = "present"
        if fm.get("periods") or fm.get("regions") or fm.get("category"):
            data_state = "stated"
        v[cid] = dict(data_status=data_state, content_verified=content, license_verified=lic_state)
    return v


def main():
    ap = argparse.ArgumentParser(description="R1 knowledge-quality audit (read-only)")
    ap.add_argument("--json", action="store_true", help="emit JSON report")
    ap.add_argument("--section", choices=["dups", "locators", "periods", "v12", "sep", "drafts", "license", "proposal"],
                    help="run one section only")
    args = ap.parse_args()

    cards, id_dups = load_cards()
    if not cards:
        print("FATAL: no cards loaded", file=sys.stderr)
        return 2
    schema = load_v12_schema()
    off = args.section
    report = dict(meta=dict(root=ROOT, cards=len(cards), id_dups=id_dups,
                            schema_fields=len(schema), v12_cards=0))
    if not off or off == "dups":
        dup = check_duplicates(cards)
        pairs = []
        known = [("GAR-0001", "GAR-0065"), ("SRC-0022", "SRC-0163"), ("SRC-0115", "SRC-0157"), ("SRC-0036", "SRC-0175")]
        for a, b in known:
            if a in cards and b in cards:
                pairs.append(compare_pair(cards, a, b))
        # add near-duplicate pairs from detection
        for nd in dup["near_dups"]:
            a, b = nd["ids"]
            if a in cards and b in cards:
                pairs.append(compare_pair(cards, a, b))
        report["duplicates"] = dict(id_dups=id_dups, name_dups=dup["name_dups"],
                                    alias_collisions=dup["alias_collisions"], near_dups=dup["near_dups"],
                                    pair_verdicts=pairs)
    if not off or off == "locators":
        conc = parse_book_conclusions()
        locres = check_book_locators(conc)
        report["locators"] = locres
    if not off or off == "periods":
        report["period_region"] = check_period_region(cards)
        report["period_region_targeted"] = check_period_region_targeted(cards)
    if not off or off == "v12":
        report["v12"] = check_v12(cards, schema)
    if not off or off == "sep":
        report["separation"] = check_separation(cards)
        report["output_separation"] = check_output_separation()
    if not off or off == "drafts":
        report["drafts"] = check_drafts(cards)
    if not off or off == "license":
        report["license"] = check_license(cards)
    if not off or off == "proposal":
        dup_info = report.get("duplicates", {})
        locres = report.get("locators", [])
        lic_info = report.get("license", {})
        report["proposal"] = propose_status(cards, dup_info, locres, lic_info)
        report["meta"]["v12_cards"] = sum(1 for c in cards.values() if c.get("_v12_used"))

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0

    # human summary
    print("cards:", len(cards), "| duplicate IDs:", len(id_dups), "| v1.2 fields:", len(schema))
    if "duplicates" in report:
        d = report["duplicates"]
        print("[dups] same-name:", len(d["name_dups"]), "alias collisions:", len(d["alias_collisions"]),
              "near-dups:", len(d["near_dups"]))
        for p in d["pair_verdicts"]:
            print("   ", p["ids"], "->", p["verdict"], "| diff:", {k: v for k, v in list(p["field_diff"].items())[:4]})
    if "locators" in report:
        from collections import Counter
        cnt = Counter(r["status"] for r in report["locators"])
        print("[locators]", dict(cnt))
        for r in report["locators"]:
            if r["status"] != "PASS":
                print("    %s PG%s line %s -> %s %s" % (r["id"], r["pg"], r["line"], r["status"], r["notes"][:2]))
    if "period_region" in report:
        from collections import Counter
        print("[period/region] issues:", len(report["period_region"]),
              dict(Counter(i["kind"] for i in report["period_region"])))
        for i in report["period_region"][:12]:
            print("   ", i)
    if "period_region_targeted" in report:
        print("[period/region targeted]")
        for g in report["period_region_targeted"]:
            print("   %s: candidates=%d violations=%d" % (g["label"], g["candidates"], len(g["violations"])))
            for v in g["violations"][:6]:
                print("      ", v)
    if "output_separation" in report:
        os_ = report["output_separation"]
        print("[output separation] test md:", len(os_["files"]),
              "| missing assumption:", sum(1 for f in os_["files"] if "assumption" in f["missing"]),
              "| json outputs ok:", sum(1 for j in os_["json_outputs"] if j["separation_ok"]), "/", len(os_["json_outputs"]))
    if "v12" in report:
        from collections import Counter
        print("[v1.2] issues:", len(report["v12"]), dict(Counter(i["kind"] for i in report["v12"])))
        for i in report["v12"][:12]:
            print("   ", i)
    if "separation" in report:
        from collections import Counter
        print("[separation] issues:", len(report["separation"]), dict(Counter(i["kind"] for i in report["separation"])))
        for i in report["separation"][:8]:
            print("   ", i)
    if "drafts" in report:
        d = report["drafts"]
        print("[drafts]", {k: d[k] for k in ("rows", "drafts_now", "reviewed_now", "still_draft", "conclusions")})
        print("   missing in cards:", d["missing_in_cards"], "| no record:", d["drafts_no_record"], "| drift:", d["drift"][:5])
    if "license" in report:
        from collections import Counter
        l = report["license"]
        print("[license] issues:", len(l["issues"]), dict(Counter(i["kind"] for i in l["issues"])))
        for i in l["issues"][:10]:
            print("   ", i)
        print("   embedded images:", l["embedded_images"], "| image files:", l["image_files"])
    if "proposal" in report:
        from collections import Counter
        p = report["proposal"]
        print("[proposal] data:", dict(Counter(x["data_status"] for x in p.values())))
        print("           content:", dict(Counter(x["content_verified"] for x in p.values())))
        print("           license:", dict(Counter(x["license_verified"] for x in p.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
