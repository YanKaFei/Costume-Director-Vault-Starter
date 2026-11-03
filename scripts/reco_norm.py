#!/usr/bin/env python3
"""reco_norm.py - normalization, brief parsing, conflict detection and prompt hygiene.

A helper module for recommend.py (P3 fixes).  It deliberately contains no I/O and
no vault access: callers pass parsed card metadata / item dicts.

Main APIs
---------
period_profile(*values) -> dict     parse "1580s", "16th_century", "late Ming" ...
period_tier(want, have) -> str      exact | era | approximate | none | unknown
region_profile(*values) -> dict     parse "italy", "london and accra", "shanghai" ...
region_tier(want, have) -> str      exact | regional | approximate | none | unknown
parse_brief(text) -> dict           rule-based script/character extraction
detect_conflicts(inp, looks, ...) -> list[dict]
sanitize_prompt_fragment(...) / sanitize_motion_notes(...)
narrative_meaning(look, inp) -> str
"""

import re

import costume_lib as lib

# ---------------------------------------------------------------------------
# period normalization
# ---------------------------------------------------------------------------
# Canonical era keys with broad century spans.  These are *compatibility
# buckets*, not precise historical claims.
NAMED_PERIODS = [
    # (keyword(s), era_key, centuries, decade_hint)
    (("late byzantine", "byzantine", "拜占庭", "东罗马"), "byzantine", set(range(4, 16))),
    (("late antiquity", "late_antiquity"), "late_antiquity", set(range(3, 8))),
    (("early middle ages", "middle ages", "medieval", "中世纪"), "medieval", set(range(5, 16))),
    (("ottoman", "奥斯曼"), "ottoman", set(range(14, 21))),
    (("renaissance", "文艺复兴"), "renaissance", {15, 16, 17}),
    (("baroque", "巴洛克"), "baroque", {17, 18}),
    (("rococo", "洛可可"), "rococo", {18}),
    (("neoclassical", "neoclassicism", "新古典"), "neoclassical", {18, 19}),
    (("regency", "摄政"), "regency", {18, 19}),
    (("victorian", "维多利亚"), "victorian", {19}),
    (("edwardian", "爱德华"), "edwardian", {20}),
    (("hollywood", "好莱坞"), "hollywood", {20}),
    (("jazz age", "爵士时代", "flapper"), "jazz_age", {20}),
    (("republican era", "republican", "民国"), "republican", {20}),
    (("ming", "明代", "明朝"), "ming", set(range(14, 18))),
    (("qing", "清代", "清朝"), "qing", set(range(17, 21))),
    (("tang", "唐代", "唐朝"), "tang", set(range(7, 10))),
    (("song", "宋代", "宋朝"), "song", set(range(10, 14))),
    (("han dynasty", "汉代", "汉朝"), "han", set(range(-3, 4))),
    (("ancient rome", "roman", "古罗马"), "roman", set(range(-5, 6))),
    (("islamic", "伊斯兰"), "islamic", set(range(7, 21))),
    (("pre columbian", "pre-columbian", "前哥伦布"), "precolumbian", set()),
    (("colonial", "殖民"), "colonial", set(range(16, 21))),
    (("contemporary", "present day", "当代", "现代"), "contemporary", {20, 21}),
    (("futuristic", "future", "未来", "sci fi", "sci-fi", "科幻"), "future", {21, 22, 23, 24}),
    (("space", "太空", "orbital", "轨道"), "future", {21, 22, 23, 24}),
    (("victorian era",), "victorian", {19}),
]


def _century_of_decade(decade):
    return decade // 100 + 1


def period_profile(*values):
    """Parse one or more period strings into comparable sets.

    Returns {decades:set[int], centuries:set[int], eras:set[str],
             future:bool, unknown:bool, raw:list[str]}.
    Decade = 1580, century = 16.
    """
    out = {"decades": set(), "centuries": set(), "eras": set(),
           "future": False, "unknown": False, "raw": []}
    for value in values:
        for raw in lib._as_list(value):
            raw = str(raw).strip()
            if not raw:
                continue
            out["raw"].append(raw)
            norm = lib.norm_text(raw)
            if norm in ("", "unknown", "unspecified", "未定", "未知"):
                out["unknown"] = True
                continue
            # decade e.g. 1580s / 1930s / 1970s
            for match in re.finditer(r"\b(\d{4})s\b", norm):
                decade = int(match.group(1)) // 10 * 10
                out["decades"].add(decade)
                out["centuries"].add(_century_of_decade(decade))
            # year e.g. 1644 -> century 17, approximate decade 1640
            for match in re.finditer(r"\b(1[0-9]{3}|20[0-9]{2})\b", norm):
                year = int(match.group(1))
                out["decades"].add(year // 10 * 10)
                out["centuries"].add(_century_of_decade(year // 10 * 10))
            # explicit century e.g. 16th_century / 16th century / early 20th century
            for match in re.finditer(
                    r"\b(\d{1,2})(?:st|nd|rd|th)[\s_-]*century\b", norm):
                out["centuries"].add(int(match.group(1)))
            for match in re.finditer(
                    r"\b(\d{1,2})(?:st|nd|rd|th)\b", norm):
                number = int(match.group(1))
                if number <= 25:
                    out["centuries"].add(number)
                    out["decades"].add((number - 1) * 100 + 50)
                    if number >= 22:
                        out["future"] = True
            # named eras
            for keywords, era, centuries in NAMED_PERIODS:
                if any(keyword in norm for keyword in keywords):
                    out["eras"].add(era)
                    # Broad named eras (byzantine/medieval/ottoman/dynasties) are
                    # compatibility buckets, not century claims; only narrow
                    # eras contribute centuries, otherwise "late Ming" would
                    # falsely match any 20th-century card.
                    if 0 < len(centuries) <= 2:
                        out["centuries"] |= centuries
                    if era == "future":
                        out["future"] = True
    # broad "20th century" labels may already be in centuries; keep decades empty
    if out["centuries"] and not out["decades"]:
        # century-level only: no decade precision
        pass
    return out


def _profile_empty(profile):
    return not (profile["decades"] or profile["centuries"] or profile["eras"])


def period_tier(want, have):
    """Compatibility tier between a requested period and a card period."""
    if _profile_empty(want) or _profile_empty(have):
        return "unknown"
    if want["decades"] & have["decades"]:
        return "exact"
    if want["centuries"] & have["centuries"]:
        return "era"
    if want["eras"] & have["eras"]:
        return "era"
    if want["future"] and have["future"]:
        return "fictional"
    # adjacent centuries are an approximate (not exact) evidence tier
    for a in want["centuries"]:
        for b in have["centuries"]:
            if abs(a - b) <= 1:
                return "approximate"
    return "none"


TIER_SCORE = {"exact": 1.0, "era": 0.75, "approximate": 0.45,
              "fictional": 0.6, "unknown": 0.5, "none": 0.0}


# ---------------------------------------------------------------------------
# region normalization
# ---------------------------------------------------------------------------
# child -> hierarchy (broadest last).  Keys are normalized phrases.
REGION_HIERARCHY = {
    "italy": ["italy", "western_europe", "europe"],
    "italian": ["italy", "western_europe", "europe"],
    "florence": ["florence", "italy", "western_europe", "europe"],
    "venice": ["venice", "italy", "western_europe", "europe"],
    "rome": ["rome", "italy", "western_europe", "europe"],
    "france": ["france", "western_europe", "europe"],
    "french": ["france", "western_europe", "europe"],
    "paris": ["paris", "france", "western_europe", "europe"],
    "england": ["england", "britain", "united_kingdom", "western_europe", "europe"],
    "english": ["england", "britain", "united_kingdom", "western_europe", "europe"],
    "britain": ["britain", "united_kingdom", "western_europe", "europe"],
    "british": ["britain", "united_kingdom", "western_europe", "europe"],
    "london": ["london", "england", "britain", "united_kingdom", "western_europe", "europe"],
    "united kingdom": ["united_kingdom", "western_europe", "europe"],
    "europe": ["europe", "western_europe"],
    "western europe": ["western_europe", "europe"],
    "northern europe": ["northern_europe", "europe"],
    "central europe": ["central_europe", "europe"],
    "germany": ["germany", "central_europe", "europe"],
    "german": ["germany", "central_europe", "europe"],
    "spain": ["spain", "western_europe", "europe"],
    "netherlands": ["netherlands", "western_europe", "europe"],
    "scandinavia": ["scandinavia", "northern_europe", "europe"],
    "united states": ["united_states", "north_america", "americas"],
    "american": ["united_states", "north_america", "americas"],
    "america": ["united_states", "north_america", "americas"],
    "new york": ["new_york", "united_states", "north_america", "americas"],
    "canada": ["canada", "north_america", "americas"],
    "shanghai": ["shanghai", "china", "east_asia", "asia"],
    "beijing": ["beijing", "china", "east_asia", "asia"],
    "china": ["china", "east_asia", "asia"],
    "chinese": ["china", "east_asia", "asia"],
    "hong kong": ["hong_kong", "china", "east_asia", "asia"],
    "japan": ["japan", "east_asia", "asia"],
    "japanese": ["japan", "east_asia", "asia"],
    "korea": ["korea", "east_asia", "asia"],
    "east asia": ["east_asia", "asia"],
    "asia": ["asia"],
    "india": ["india", "south_asia", "asia"],
    "south asia": ["south_asia", "asia"],
    "ghana": ["ghana", "west_africa", "africa"],
    "ghanaian": ["ghana", "west_africa", "africa"],
    "accra": ["accra", "ghana", "west_africa", "africa"],
    "asen": ["ghana", "west_africa", "africa"],
    "nigeria": ["nigeria", "west_africa", "africa"],
    "west africa": ["west_africa", "africa"],
    "africa": ["africa"],
    "african": ["africa"],
    "senegal": ["senegal", "west_africa", "africa"],
    "mali": ["mali", "west_africa", "africa"],
    "ottoman empire": ["ottoman_empire", "middle_east", "west_asia"],
    "ottoman": ["ottoman_empire", "middle_east", "west_asia"],
    "turkey": ["turkey", "middle_east", "west_asia"],
    "middle east": ["middle_east", "west_asia"],
    "north africa": ["north_africa", "africa"],
    "morocco": ["morocco", "north_africa", "africa"],
    "arabia": ["arabia", "middle_east", "west_asia"],
    "persia": ["persia", "middle_east", "west_asia"],
    "byzantium": ["byzantium", "eastern_mediterranean", "europe", "middle_east"],
    "byzantine": ["byzantium", "eastern_mediterranean", "europe", "middle_east"],
    "eastern mediterranean": ["eastern_mediterranean", "europe", "middle_east"],
    "mexico": ["mexico", "mesoamerica", "latin_america", "americas"],
    "mesoamerica": ["mesoamerica", "latin_america", "americas"],
    "guatemala": ["guatemala", "mesoamerica", "latin_america", "americas"],
    "inuit": ["inuit", "arctic", "north_america"],
    "arctic": ["arctic", "northern_regions"],
    "alaska": ["alaska", "united_states", "north_america", "americas"],
    "greenland": ["greenland", "arctic", "northern_regions"],
    "japan": ["japan", "east_asia", "asia"],
    "latin america": ["latin_america", "americas"],
}

REGION_ALIASES = {
    "意大利": "italy", "佛罗伦萨": "florence", "威尼斯": "venice", "罗马": "rome",
    "法国": "france", "巴黎": "paris", "英国": "britain", "伦敦": "london",
    "英格兰": "england", "德国": "germany", "西班牙": "spain",
    "美国": "united_states", "纽约": "new york", "加拿大": "canada",
    "上海": "shanghai", "北京": "beijing", "中国": "china", "香港": "hong kong",
    "日本": "japan", "韩国": "korea", "东亚": "east asia", "亚洲": "asia",
    "印度": "india", "加纳": "ghana", "阿克拉": "accra", "西非": "west africa",
    "非洲": "africa", "塞内加尔": "senegal", "马里": "mali", "奥斯曼": "ottoman",
    "中东": "middle east", "北非": "north africa", "摩洛哥": "morocco",
    "阿拉伯": "arabia", "波斯": "persia", "拜占庭": "byzantium",
    "墨西哥": "mexico", "中美洲": "mesoamerica", "危地马拉": "guatemala",
    "北极": "arctic", "格陵兰": "greenland", "阿拉斯加": "alaska",
    "欧洲": "europe", "西欧": "western europe",
    "unknown": None, "unspecified": None, "未知": None,
}


def region_profile(*values):
    """Parse region text into canonical hierarchy sets."""
    entities = set()
    unknown = False
    raw_values = []
    for value in values:
        for raw in lib._as_list(value):
            raw = str(raw).strip()
            if not raw:
                continue
            raw_values.append(raw)
            if raw.lower() in ("unknown", "unspecified", "未知", "未定", ""):
                unknown = True
                continue
            norm = lib.norm_text(raw)
            if not norm or norm in ("unknown", "unspecified"):
                unknown = True
                continue
            # Fictional/unspecified geographies are not real region constraints.
            if any(marker in norm for marker in
                   ("unspecified", "unknown", "fictional", "虚构", "架空",
                    "orbital", "space station", "future city", "derelict")):
                unknown = True
                # still allow real entities inside a mixed string if present
                if not any(key in norm for key in REGION_HIERARCHY):
                    continue
            matched = False
            # Chinese aliases
            for zh, en in REGION_ALIASES.items():
                if zh in raw:
                    if en is None:
                        unknown = True
                    else:
                        entities |= set(REGION_HIERARCHY.get(en, [en]))
                        matched = True
            # English/known labels: whole-key and word matches
            for key, chain in REGION_HIERARCHY.items():
                if key in norm:
                    # avoid matching "asia" inside "caucasus" etc. only word-ish keys
                    entities |= set(chain)
                    matched = True
            # direct values with no hierarchy (preserve label but mark regional generic)
            if not matched and len(norm) >= 3:
                entities.add(norm)
    return {"entities": entities, "unknown": unknown, "raw": raw_values}


def region_tier(want, have):
    if want["unknown"] and not want["entities"]:
        return "unknown"
    if have["unknown"] and not have["entities"]:
        return "unknown"
    if not want["entities"] or not have["entities"]:
        return "unknown"
    if want["entities"] & have["entities"]:
        # exact when a requested concrete label equals a card label; broad
        # hierarchy overlap is "regional"
        concrete_want = {e for e in want["entities"]
                         if e not in ("europe", "asia", "africa", "americas",
                                      "western_europe", "east_asia",
                                      "north_america", "west_africa",
                                      "middle_east", "south_asia",
                                      "latin_america", "arctic",
                                      "northern_regions", "west_asia")}
        concrete_have = {e for e in have["entities"]
                         if e not in ("europe", "asia", "africa", "americas",
                                      "western_europe", "east_asia",
                                      "north_america", "west_africa",
                                      "middle_east", "south_asia",
                                      "latin_america", "arctic",
                                      "northern_regions", "west_asia")}
        if concrete_want & concrete_have:
            return "exact"
        return "regional"
    return "none"


REGION_TIER_SCORE = {"exact": 1.0, "regional": 0.8, "approximate": 0.45,
                     "unknown": 0.5, "none": 0.0}


# ---------------------------------------------------------------------------
# brief parsing (rule based)
# ---------------------------------------------------------------------------
PERIOD_WORDS = [
    (r"\b(1[0-9]{3}|20[0-9]{2})s\b", None),
    (r"\b\d{1,2}(?:st|nd|rd|th)\s*century\b", None),
    (r"\b(?:late|early|mid)[-_ ]?\d{1,2}(?:st|nd|rd|th)?[-_ ]?century\b", None),
    (r"\b(?:late|early|mid)[-_ ]?(?:ming|qing|tang|song)\b", None),
    (r"\b(?:ming|qing|tang|song)\s+(?:dynasty|era)\b", None),
    (r"\b(?:byzantine|ottoman|victorian|edwardian|regency|renaissance|baroque|rococo)\b", None),
    (r"\b(?:contemporary|present[- ]day|modern)\b", None),
    (r"\b(?:future|futuristic|sci[- ]?fi|cyberpunk|22nd|23rd|24th)\b", None),
    (r"\b(?:19[0-9]{2}|20[0-9]{2})\b", None),
]
PERIOD_ZH = ["明末", "清初", "明代", "清代", "唐代", "宋代", "民国", "当代", "现代",
             "未来", "文艺复兴", "巴洛克", "洛可可", "维多利亚", "爱德华", "摄政",
             "拜占庭", "奥斯曼", "二战", "战后", "千禧"]

REGION_WORDS = list(REGION_ALIASES.keys()) + [
    "italy", "italian", "france", "french", "london", "britain", "british",
    "england", "europe", "germany", "spain", "united states", "america",
    "new york", "shanghai", "beijing", "china", "chinese", "hong kong", "japan",
    "japanese", "korea", "east asia", "asia", "india", "ghana", "accra",
    "west africa", "africa", "senegal", "mali", "ottoman", "middle east",
    "north africa", "morocco", "arabia", "persia", "byzantium", "mexico",
    "mesoamerica", "guatemala", "arctic", "greenland", "alaska", "latin america",
    "paris", "rome", "venice", "florence", "netherlands", "scandinavia",
    "canada", "australia", "orbital", "space station", "lunar", "mars",
]

OCCUPATION_WORDS = [
    (("nurse", "护士", "急诊"), "nurse / emergency nurse"),
    (("doctor", "physician", "医生"), "doctor"),
    (("journalist", "reporter", "记者", "编辑"), "journalist / editor"),
    (("detective", "investigator", "侦探", "调查员"), "detective / investigator"),
    (("dancer", "ballet", "舞者", "舞蹈"), "dancer"),
    (("soldier", "officer", "military", "军人", "士兵"), "soldier / officer"),
    (("teacher", "professor", "教师", "老师"), "teacher / professor"),
    (("worker", "labourer", "laborer", "工人", "维修", "mechanic"), "worker / mechanic"),
    (("student", "学生"), "student"),
    (("servant", "maid", "butler", "仆人", "佣人"), "servant"),
    (("aristocrat", "noble", "countess", "贵族", "伯爵"), "aristocrat"),
    (("banker", "businessman", "executive", "banker", "银行家", "商人"), "banker / merchant"),
    (("merchant", "shopkeeper", "商人", "店主"), "merchant"),
    (("artist", "painter", "writer", "艺术家", "画家", "作家"), "artist / writer"),
    (("singer", "opera", "diva", "女伶", "歌手", "歌剧"), "singer / opera performer"),
    (("courier", "delivery", "骑手", "信使", "快递"), "courier / delivery rider"),
    (("architect", "建筑师"), "architect"),
    (("lawyer", "律师"), "lawyer"),
    (("farmer", "peasant", "农民"), "farmer"),
    (("clerk", "职员", "文书"), "clerk"),
    (("refugee", "难民"), "refugee"),
    (("spy", "特工", "间谍"), "spy"),
]
CLASS_WORDS = [
    (("wealthy", "rich", "elite", "aristocrat", "upper class", "贵族", "富裕", "富有", "豪门", "上层"), "high"),
    (("middle class", "middle", "bourgeois", "中产", "小康", "中下"), "middle"),
    (("poor", "working class", "destitute", "refugee", "low income", "贫困", "穷", "底层", "工薪", "难民"), "low"),
]
WEATHER_WORDS = [
    (("heavy rain", "rain", "rainy", "storm", "暴雨", "下雨", "雨夜", "雨中"), "rain"),
    (("snow", "snowy", "blizzard", "雪"), "snow"),
    (("cold", "freezing", "winter", "冷", "寒", "冬"), "cold"),
    (("hot", "summer", "heat", "炎热", "夏"), "hot"),
    (("humid", "潮湿"), "humid"),
    (("wind", "windy", "风"), "wind"),
    (("overcast", "多云", "阴天"), "overcast"),
    (("indoor", "interior", "室内", "室内"), "indoor"),
]
SEASON_WORDS = [
    (("spring", "春"), "spring"),
    (("summer", "夏"), "summer"),
    (("autumn", "fall", "秋"), "autumn"),
    (("winter", "冬"), "winter"),
]
ART_WORDS = [
    (("noir", "黑色电影"), "noir"),
    (("expressionist", "expressionism", "表现主义"), "expressionist"),
    (("cyberpunk", "赛博朋克", "义体"), "cyberpunk"),
    (("minimal", "简约", "极简"), "minimal"),
    (("period drama", "年代剧", "historical drama"), "period drama"),
    (("documentary", "纪实"), "documentary realism"),
    (("neoclassical", "新古典"), "neoclassical"),
    (("dystopian", "反乌托邦"), "dystopian"),
    (("fairy tale", "童话"), "fairy tale"),
    (("wuxia", "武侠"), "wuxia"),
    (("surreal", "超现实"), "surreal"),
]
FIDELITY_WORDS = [
    (("historically accurate", "historical reconstruction", "史实", "历史准确", "真实历史"), "historical"),
    (("period-inspired", "inspired by", "艺术化", "灵感"), "inspired"),
    (("fictional", "虚构", "架空"), "fictional"),
]
BUDGET_WORDS = [
    (("micro budget", "micro-budget", "no budget", "极低预算", "零预算"), "low"),
    (("low budget", "tight budget", "低预算", "预算紧"), "low"),
    (("high budget", "premium budget", "高预算"), "high"),
]
ACTION_WORDS = [
    (("dance", "dancing", "芭蕾", "舞蹈", "旋转", "跳跃"), "dance"),
    (("run", "running", "chase", "追逐", "奔跑", "逃跑"), "running / chase"),
    (("fight", "combat", "打斗", "战斗"), "fight"),
    (("walk", "walking", "行走", "步行"), "walking"),
    (("sit", "sitting", "坐"), "sitting"),
    (("sing", "singing", "演唱", "唱歌"), "singing"),
]


def _first_match(text, table, field):
    for keys, value in table:
        for key in keys:
            if key in text:
                return value
    return None


def parse_brief(text):
    """Rule-based script/character extraction.  Unknown values stay unknown."""
    text = str(text or "")
    norm = lib.norm_text(text)
    parsed = {}
    matched = {}

    # period
    period_hits = []
    for pattern, _ in PERIOD_WORDS:
        for m in re.finditer(pattern, norm, flags=re.I):
            hit = m.group(0)
            if hit not in period_hits:
                period_hits.append(hit)
    for zh in PERIOD_ZH:
        if zh in text and zh not in period_hits:
            period_hits.append(zh)
    parsed["period"] = ", ".join(period_hits) if period_hits else "unknown"
    matched["period"] = period_hits

    # region
    region_hits = []
    for word in REGION_WORDS:
        if word and word in norm and word not in region_hits:
            region_hits.append(word)
    for zh, en in REGION_ALIASES.items():
        if en and zh in text and en not in region_hits:
            region_hits.append(en)
    parsed["region"] = ", ".join(region_hits) if region_hits else "unknown"
    matched["region"] = region_hits

    parsed["occupation"] = _first_match(norm, OCCUPATION_WORDS, "occupation") or "unknown"
    parsed["economic_status"] = _first_match(norm, CLASS_WORDS, "class") or "unknown"
    parsed["weather"] = _first_match(norm, WEATHER_WORDS, "weather") or "unknown"
    parsed["season"] = _first_match(norm, SEASON_WORDS, "season") or "unknown"
    parsed["art_direction"] = _first_match(norm, ART_WORDS, "art") or "unknown"
    parsed["action"] = _first_match(norm, ACTION_WORDS, "action") or "unknown"
    parsed["budget"] = _first_match(norm, BUDGET_WORDS, "budget") or "unknown"
    fidelity = _first_match(norm, FIDELITY_WORDS, "fidelity")
    if not fidelity:
        if any(word in norm for word in ("cyberpunk", "sci fi", "sci-fi", "future",
                                          "space", "赛博朋克", "未来", "太空")):
            fidelity = "fictional"
        elif any(word in norm for word in ("historical", "史实", "历史准确")):
            fidelity = "historical"
    parsed["fidelity_mode"] = fidelity or "unknown"
    parsed["unknown_fields"] = sorted(
        key for key, value in parsed.items() if value == "unknown")
    parsed["matched_terms"] = {key: value for key, value in matched.items() if value}
    parsed["brief"] = text
    return parsed


# ---------------------------------------------------------------------------
# conflict detection
# ---------------------------------------------------------------------------
SCIFI_WORDS = ("cyberpunk", "cyber", "sci fi", "sci-fi", "科幻", "义体", "body mod",
               "implant", "android", "robot", "space station", "太空", "orbital",
               "hologram", "neon", "未来", "future", "exoskeleton", "机械臂")
MOURNING_WORDS = ("funeral", "mourning", "丧", "葬礼", "哀悼", "丧服")
WEDDING_WORDS = ("wedding", "bride", "marriage", "婚礼", "新娘", "结婚")
ARCTIC_WORDS = ("arctic", "inuit", "snow", "snowy", "极地", "北极", "雪")
INDOOR_WORDS = ("indoor", "interior", "室内", "室内")
DANCE_WORDS = ("dance", "dancing", "ballet", "舞", "旋转", "跳跃")


def _joined(inp, *keys):
    return lib.norm_text(" ".join(str(inp.get(key, "")) for key in keys))


def detect_conflicts(inp, looks, cards_by_id):
    """Detect contradictory requirements and return structured conflicts."""
    conflicts = []
    text = _joined(inp, "occupation", "action", "scene", "art_direction",
                   "lighting", "notes", "weather", "period", "region")
    mode = inp.get("fidelity_mode", "inspired")

    if mode == "historical" and any(word in text for word in SCIFI_WORDS):
        conflicts.append({
            "code": "historical_vs_scifi",
            "severity": "high",
            "message": ("historical fidelity conflicts with science-fiction / body-mod / "
                        "neon elements in the brief"),
            "resolution": ("split the brief: historical base costume + explicit fictional "
                           "overlay; or set fidelity_mode=inspired/fictional and declare "
                           "the anachronism"),
        })

    period_profile_inp = period_profile(inp.get("period", ""))
    if mode == "historical" and period_profile_inp.get("future"):
        conflicts.append({
            "code": "historical_future_period",
            "severity": "high",
            "message": "historical mode requested with a future period",
            "resolution": "use fictional mode or remove the future setting",
        })

    weather_text = _joined(inp, "weather", "season")
    indoor = any(word in _joined(inp, "scene", "weather") for word in INDOOR_WORDS)
    snow = any(word in weather_text for word in ("snow", "雪", "arctic", "北极", "cold", "寒"))
    wet = any(word in weather_text for word in ("rain", "storm", "雨", "wet", "snow", "雪"))
    action_text = _joined(inp, "action", "occupation", "scene")
    dance = any(word in action_text for word in DANCE_WORDS)
    physical = any(word in action_text for word in
                   ("run", "chase", "fight", "奔跑", "追逐", "打斗"))
    wedding = any(word in text for word in WEDDING_WORDS)
    mourning = any(word in text for word in MOURNING_WORDS)

    if indoor:
        for look in looks:
            for slot, item in look["items"].items():
                if not item:
                    continue
                item_text = lib.norm_text(
                    item["name_en"] + " " + item["name_zh"] + " " +
                    " ".join(item["materials"]) + " " + item.get("prompt_en", ""))
                if any(word in item_text for word in
                       ("arctic", "anorak", "parka", "fur", "seal skin", "caribou",
                        "极地", "兽皮")):
                    conflicts.append({
                        "code": "indoor_arctic_gear",
                        "severity": "medium",
                        "message": "indoor scene uses arctic/snow outerwear (%s)" % item["id"],
                        "resolution": "remove the arctic layer indoors; keep only if the "
                                      "scene explicitly involves snow/outdoor cold",
                    })
                    break
            break
    if snow or wet:
        for look in looks:
            footwear = look["items"].get("footwear")
            if footwear:
                materials = [lib.norm_text(m) for m in footwear["materials"]]
                if any(m in ("silk", "lace", "suede", "satin") for m in materials):
                    conflicts.append({
                        "code": "weather_vs_material",
                        "severity": "medium",
                        "message": "wet/snow weather with delicate footwear %s" % footwear["id"],
                        "resolution": "use leather/rubber boots or declare a dry interior shot",
                    })
                    break
    if dance or physical:
        for look in looks:
            footwear = look["items"].get("footwear")
            if footwear:
                name = lib.norm_text(footwear["name_en"] + " " + footwear["name_zh"])
                if any(word in name for word in ("heel", "stiletto", "高跟", "mule", "穆勒")):
                    conflicts.append({
                        "code": "movement_vs_footwear",
                        "severity": "high",
                        "message": "dance/action scene with heeled or backless footwear %s"
                                   % footwear["id"],
                        "resolution": "choose flat secure shoes; if no card exists, log "
                                      "the safety gap and test the movement",
                    })
                    break
    if wedding and mourning:
        conflicts.append({
            "code": "occasion_conflict",
            "severity": "high",
            "message": "wedding and mourning references appear in the same brief",
            "resolution": "separate ceremonial looks or confirm which occasion applies",
        })
    if wedding:
        culture_missing = inp.get("region", "")
        for look in looks:
            item_ids = [item["id"] for item in look["items"].values() if item]
            if culture_missing and not any(
                    id_ in cards_by_id for id_ in item_ids):
                continue
        # cross-cultural awareness gap is surfaced as a warning elsewhere; only
        # explicit contradictory colour/occasion references are conflicts here.
    if mode == "historical" and any(word in text for word in ("cyberpunk", "义体", "neon")):
        pass
    if inp.get("budget") == "low":
        for look in looks:
            if look.get("cost_total", 0) > 2.4:  # rough absolute proxy
                conflicts.append({
                    "code": "budget_vs_materials",
                    "severity": "low",
                    "message": "low budget look with comparatively expensive materials",
                    "resolution": "prefer cotton/wool/canvas and reuse existing pieces",
                })
                break
    return conflicts


# ---------------------------------------------------------------------------
# prompt hygiene
# ---------------------------------------------------------------------------
GARMENT_NOUNS = ("t-shirt", "tshirt", "shirt", "blouse", "jacket", "waistcoat",
                 "vest", "trousers", "pants", "jeans", "skirt", "dress", "gown",
                 "coat", "overcoat", "cloak", "cape", "hat", "cap", "bonnet",
                 "gloves", "boots", "shoes", "sandals", "bag", "umbrella", "muff",
                 "scarf", "tie", "corset", "petticoat", "breeches", "robes")
BAD_CONTEXT_PHRASES = (
    "worn in snow", "worn in the snow", "worn for snow", "in the snow",
    "worn in winter", "worn in rain", "for snowy weather",
)


def _clause_selected(clause, own_text, selected_text):
    clause_norm = lib.norm_text(clause)
    for noun in GARMENT_NOUNS:
        if noun in clause_norm:
            if noun in own_text:
                continue
            if noun in selected_text:
                continue
            return False
    return True


def sanitize_prompt_fragment(fragment, item, inp, selected_items):
    """Keep only clauses that describe this item in this scene.

    Removes card-text leakage such as "worn in snow" in an indoor scene or
    "worn with a white t-shirt and leather jacket" when those pieces are not
    part of the selected look.
    """
    if not fragment:
        return ""
    weather = lib.norm_text(inp.get("weather", "") + " " + inp.get("season", ""))
    scene_text = lib.norm_text(" ".join(str(inp.get(key, "")) for key in
                                        ("scene", "location", "weather")))
    indoor = any(marker in scene_text for marker in
                 ("indoor", "interior", "室内", "office", "corridor", "room",
                  "kitchen", "hospital", "ward", "studio", "lobby", "hall",
                  "basement", "apartment", "shelter", "病房", "办公室", "走廊"))
    snow_ok = (not indoor) and any(word in weather for word in
                                   ("snow", "snowy", "雪"))
    own_text = lib.norm_text(item.get("name_en", "") + " " + item.get("name_zh", ""))
    selected_text = lib.norm_text(" ".join(
        other.get("name_en", "") + " " + other.get("name_zh", "")
        for other in selected_items if other))
    kept = []
    for clause in re.split(r"[,;]", fragment):
        clause = clause.strip()
        if not clause:
            continue
        norm = lib.norm_text(clause)
        if any(phrase in norm for phrase in BAD_CONTEXT_PHRASES) and not snow_ok:
            continue
        if "worn with" in norm or "worn over" in norm or "worn under" in norm:
            if not _clause_selected(clause, own_text, selected_text):
                continue
        if not _clause_selected(clause, own_text, selected_text):
            continue
        kept.append(clause)
    return ", ".join(kept)


def sanitize_motion_notes(notes, inp):
    if not notes:
        return ""
    weather = lib.norm_text(inp.get("weather", "") + " " + inp.get("season", ""))
    scene_text = lib.norm_text(" ".join(str(inp.get(key, "")) for key in
                                        ("scene", "location", "weather")))
    indoor = any(marker in scene_text for marker in
                 ("indoor", "interior", "室内", "office", "corridor", "room",
                  "kitchen", "hospital", "ward", "studio", "lobby", "hall",
                  "basement", "apartment", "shelter", "病房", "办公室", "走廊"))
    snow_ok = (not indoor) and any(word in weather for word in ("snow", "snowy", "雪"))
    kept = []
    for clause in re.split(r"[;；]", notes):
        clause = clause.strip()
        if not clause:
            continue
        norm = lib.norm_text(clause)
        if not snow_ok and any(word in norm for word in
                               ("snow", "风雪", "雪", "winter", "snowy")):
            continue
        kept.append(clause)
    return "; ".join(kept)


# ---------------------------------------------------------------------------
# narrative meaning
# ---------------------------------------------------------------------------
def narrative_meaning(look, inp):
    """Short directorial reading.  Clearly labelled as interpretation."""
    items = [item for item in look.get("items", {}).values() if item]
    if not items:
        return "No narrative reading: the look has no concrete garment cards."
    slots = sorted(look.get("items", {}).keys())
    palette = look.get("colors", [])
    formality = [item.get("formality") for item in items if item.get("formality")]
    arc = inp.get("arc", "unknown")
    occupation = inp.get("occupation", "unknown")
    econ = inp.get("economic_status", "unknown")
    example = any(item.get("evidence_status") == "example" for item in items)
    parts = []
    if occupation != "unknown":
        parts.append("the silhouette is cut to serve %s" % occupation)
    if econ != "unknown":
        parts.append("the %s economic register shows through material and finish" % econ)
    if formality:
        parts.append("formality runs from %s" % " / ".join(formality))
    if palette:
        parts.append("the %s palette controls the emotional temperature" % ", ".join(palette[:3]))
    if arc != "unknown":
        parts.append("against the arc (%s) the look functions as a visible state that "
                     "can be tracked or deliberately broken in later scenes" % arc)
    if example:
        parts.append("an example-grade card is involved, so this reading is a design "
                     "hypothesis, not historical evidence")
    if look.get("missing"):
        parts.append("the missing layers mark a production gap rather than a design choice")
    return ("Narrative meaning (directorial interpretation, not clothing-history fact): "
            + "; ".join(parts) + ".")
