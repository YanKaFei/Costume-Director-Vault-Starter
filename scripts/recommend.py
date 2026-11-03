#!/usr/bin/env python3
"""recommend.py - evidence-linked costume recommendation over the vault cards.

Input: a JSON file describing a character/scene (see skills/costume-director/SKILL.md
for the full schema).  Both flat keys and nested character/scene objects work.

Behaviour:
  1. hard constraints first (period/culture, weather, movement/safety,
     historical-evidence strictness, budget)
  2. 100-point explainable soft score
     period/culture 25 | character identity 15 | environment 15 |
     art direction 15 | movement 10 | arc 10 | camera/continuity 10
  3. three distinct looks: A preferred, B clearly different alternative,
     C budget/art-direction alternative.  Every garment/part/material ID in
     the output is read from a real vault card; IDs are never invented.
  4. English image prompt, English video prompt, continuity lock fields,
     negative constraints, risks, evidence/source URLs, uncertainty notes.

Modes:
  standard     one scene recommendation (default)
  --continuity input contains "scenes": [ ... ]; one base look is locked and
               re-used across all scenes with explicit per-scene states.

Exit codes:
  0  recommendation produced (warnings may exist)
  2  invalid input JSON / missing file
  3  no wardrobe candidates at all (knowledge base gap)
"""

import argparse
import json
import sys
from pathlib import Path

import costume_lib as lib

# ---------------------------------------------------------------------------
# constants
# ---------------------------------------------------------------------------
DIM_ORDER = [
    ("period", "年代/文化", 25),
    ("identity", "角色身份", 15),
    ("environment", "环境气候", 15),
    ("art", "美术方向", 15),
    ("movement", "动作可行", 10),
    ("arc", "剧情弧线", 10),
    ("camera", "摄影/一致性", 10),
]
DIM_WEIGHTS = {key: weight for key, _label, weight in DIM_ORDER}

SLOT_LABELS = {
    "inner_layer": "内层",
    "upper_body": "上装",
    "lower_body": "下装",
    "one_piece": "连身",
    "set": "成套",
    "outerwear": "外层",
    "footwear": "足部",
    "accessory": "配饰",
    "carried_prop": "携带物",
}
SLOT_ORDER = ["inner_layer", "upper_body", "lower_body", "one_piece", "set",
              "outerwear", "footwear", "accessory", "carried_prop"]
SLOT_EN = {
    "inner_layer": "inner layer", "upper_body": "upper body",
    "lower_body": "lower body", "one_piece": "one-piece",
    "set": "complete set", "outerwear": "outer layer",
    "footwear": "footwear", "accessory": "accessory",
    "carried_prop": "carried prop",
}
ITEM_WEIGHTS = {
    "inner_layer": 0.7, "upper_body": 1.2, "lower_body": 1.1,
    "one_piece": 1.4, "set": 1.4, "outerwear": 1.3, "footwear": 1.1,
    "accessory": 0.6, "carried_prop": 0.5,
}

CATEGORY_TO_SLOT = {
    "upper_body": "upper_body", "upper": "upper_body", "top": "upper_body",
    "lower_body": "lower_body", "lower": "lower_body", "bottom": "lower_body",
    "one_piece": "one_piece", "onepiece": "one_piece",
    "full_body": "one_piece", "dress": "one_piece",
    "outerwear": "outerwear", "outer_layer": "outerwear", "outer": "outerwear",
    "inner_layer": "inner_layer", "inner": "inner_layer",
    "underwear": "inner_layer", "base_layer": "inner_layer",
    "footwear": "footwear", "shoes": "footwear", "foot": "footwear",
    "accessory": "accessory", "accessories": "accessory",
    "headwear": "accessory",
    "carried_prop": "carried_prop", "prop": "carried_prop",
    "set": "set", "suit": "set", "uniform": "set", "costume_set": "set",
    "specialised": "set", "specialized": "set",
}
SUBCATEGORY_TO_SLOT = {
    "shirt": "upper_body", "t shirt": "upper_body", "tshirt": "upper_body",
    "blouse": "upper_body", "knit": "upper_body", "sweater": "upper_body",
    "vest": "upper_body", "waistcoat": "upper_body", "bodice": "upper_body",
    "corset": "upper_body", "jacket": "outerwear", "coat": "outerwear",
    "overcoat": "outerwear", "trench": "outerwear", "cape": "outerwear",
    "cloak": "outerwear", "blazer": "outerwear", "parka": "outerwear",
    "trousers": "lower_body", "pants": "lower_body", "skirt": "lower_body",
    "shorts": "lower_body", "culottes": "lower_body",
    "dress": "one_piece", "gown": "one_piece", "jumpsuit": "one_piece",
    "overalls": "one_piece", "robe": "one_piece", "qipao": "one_piece",
    "cheongsam": "one_piece", "hanfu": "set", "kimono": "set",
    "uniform": "set", "suit": "set",
    "boots": "footwear", "shoes": "footwear", "sneakers": "footwear",
    "sandals": "footwear", "slippers": "footwear", "socks": "footwear",
    "hat": "accessory", "cap": "accessory", "scarf": "accessory",
    "gloves": "accessory", "glasses": "accessory", "tie": "accessory",
    "belt": "accessory", "jewelry": "accessory", "brooch": "accessory",
    "watch": "accessory", "bag": "carried_prop", "umbrella": "carried_prop",
    "cane": "carried_prop", "handbag": "carried_prop",
}
SLOT_NAME_HINTS = [
    ("shirt", "upper_body"), ("blouse", "upper_body"), ("sweater", "upper_body"),
    ("衬衫", "upper_body"), ("上衣", "upper_body"), ("马甲", "upper_body"),
    ("trousers", "lower_body"), ("pants", "lower_body"), ("skirt", "lower_body"),
    ("裤", "lower_body"), ("裙", "lower_body"),
    ("dress", "one_piece"), ("gown", "one_piece"), ("jumpsuit", "one_piece"),
    ("连衣裙", "one_piece"), ("旗袍", "one_piece"), ("长袍", "one_piece"),
    ("coat", "outerwear"), ("jacket", "outerwear"), ("overcoat", "outerwear"),
    ("大衣", "outerwear"), ("外套", "outerwear"), ("风衣", "outerwear"),
    ("boots", "footwear"), ("shoes", "footwear"), ("sneakers", "footwear"),
    ("鞋", "footwear"), ("靴", "footwear"), ("袜", "footwear"),
    ("hat", "accessory"), ("cap", "accessory"), ("scarf", "accessory"),
    ("gloves", "accessory"), ("belt", "accessory"), ("tie", "accessory"),
    ("帽", "accessory"), ("围巾", "accessory"), ("手套", "accessory"),
    ("bag", "carried_prop"), ("umbrella", "carried_prop"), ("cane", "carried_prop"),
    ("包", "carried_prop"), ("伞", "carried_prop"),
]

WET_TOKENS = {"rain", "raining", "rainy", "storm", "stormy", "drizzle",
              "drizzling", "monsoon", "typhoon", "wet", "sleet", "snow",
              "snowy", "shower", "downpour", "雨", "暴雨", "大雪", "雪"}
COLD_TOKENS = {"cold", "freezing", "winter", "snow", "snowy", "chill",
               "icy", "冷", "冬", "寒"}
HOT_TOKENS = {"hot", "summer", "heat", "humid", "tropical", "sunny",
              "热", "夏", "暑"}
WIND_TOKENS = {"wind", "windy", "storm", "typhoon", "风"}

WEATHER_MATERIALS = {
    "rain": {"wool": 0.9, "leather": 0.9, "gabardine": 1.0, "nylon": 0.9,
             "canvas": 0.85, "waxed cotton": 1.0, "oilskin": 1.0,
             "rubber": 1.0, "cotton": 0.55, "denim": 0.6, "linen": 0.3,
             "silk": 0.15, "suede": 0.05, "velvet": 0.2},
    "cold": {"wool": 1.0, "cashmere": 1.0, "down": 1.0, "fur": 1.0,
             "leather": 0.9, "tweed": 0.9, "cotton": 0.6, "linen": 0.1,
             "silk": 0.3, "nylon": 0.7},
    "hot": {"linen": 1.0, "cotton": 0.9, "silk": 0.85, "seersucker": 1.0,
            "mesh": 0.9, "wool": 0.2, "leather": 0.3, "fur": 0.05,
            "down": 0.05},
    "wind": {"wool": 0.9, "gabardine": 0.9, "nylon": 0.9, "leather": 0.8,
             "canvas": 0.8, "silk": 0.4},
}
MATERIAL_COST = {
    "cotton": 0.25, "linen": 0.3, "wool": 0.5, "denim": 0.35,
    "canvas": 0.2, "leather": 0.6, "silk": 0.7, "cashmere": 0.8,
    "fur": 0.9, "velvet": 0.7, "brocade": 0.8, "polyester": 0.15,
    "nylon": 0.2, "rubber": 0.15, "metal": 0.5, "tweed": 0.5,
    "suede": 0.55, "lace": 0.6, "chiffon": 0.4, "jersey": 0.25,
}
FORMALITY_COST = {"casual": 0.15, "everyday": 0.15, "smart_casual": 0.3,
                  "business": 0.5, "formal": 0.75, "black_tie": 0.9,
                  "ceremonial": 0.9, "workwear": 0.2, "functional": 0.2,
                  "theatrical": 0.6, "uniform": 0.4}
WARM_COLORS = {"amber", "rust", "crimson", "gold", "cream", "brown", "tan",
               "camel", "orange", "red", "burgundy", "wine", "ochre",
               "yellow", "beige", "ivory", "peach", "rose", "copper"}
COOL_COLORS = {"charcoal", "navy", "blue", "steel", "grey", "gray", "black",
               "white", "silver", "teal", "green", "indigo", "slate",
               "ice", "aqua"}
NEUTRAL_COLORS = {"black", "white", "grey", "gray", "beige", "charcoal",
                  "cream", "off white", "ivory"}

STOPWORDS = {
    "a", "an", "and", "or", "of", "to", "in", "on", "at", "for", "from",
    "with", "without", "by", "as", "is", "are", "be", "the", "this", "that",
    "it", "its", "while", "into", "over", "under", "through", "across",
    "during", "then", "than", "but", "not", "no", "very", "slightly", "also",
    "unknown", "adult", "character", "scene", "street", "location",
}

TERM_ALIASES = {
    "1930年代": "1930s", "1920年代": "1920s", "1940年代": "1940s",
    "1950年代": "1950s", "1960年代": "1960s", "1970年代": "1970s",
    "上海": "shanghai", "民国": "republic of china", "北京": "beijing",
    "香港": "hong kong", "巴黎": "paris", "伦敦": "london", "纽约": "new york",
    "唐朝": "tang dynasty", "宋代": "song dynasty", "明代": "ming dynasty",
    "清代": "qing dynasty", "汉朝": "han dynasty", "战国": "warring states",
    "雨": "rain", "夜": "night", "冬": "winter", "夏": "summer",
    "舞": "dance", "舞蹈": "dance", "贫": "poor", "穷": "poor",
    "富": "wealthy", "贵族": "aristocrat", "落魄": "decline",
    "工人": "worker", "学生": "student", "记者": "journalist",
    "侦探": "detective", "医生": "doctor", "艺术家": "artist",
    "商人": "merchant", "军人": "soldier", "农民": "farmer",
    "仆人": "servant", "律师": "lawyer", "银行家": "banker",
}

OCCUPATION_HINTS = [
    ({"detective", "investigator", "police", "cop", "调查", "侦探", "警察"},
     ["practical", "restrained", "coat", "dark", "noir", "trench"]),
    ({"doctor", "nurse", "medical", "医生", "护士"},
     ["clean", "practical", "uniform", "white", "modest"]),
    ({"dancer", "ballet", "choreographer", "舞者", "舞蹈"},
     ["movement", "flowing", "performance", "stretch", "light"]),
    ({"worker", "laborer", "factory", "miner", "工人", "劳工"},
     ["workwear", "durable", "denim", "canvas", "worn", "practical"]),
    ({"aristocrat", "noble", "countess", "duke", "贵族", "伯爵"},
     ["formal", "tailored", "silk", "velvet", "jewelry", "elegant"]),
    ({"business", "executive", "banker", "lawyer", "商人", "律师", "银行家"},
     ["tailored", "business", "formal", "structured", "suit"]),
    ({"student", "学生"}, ["casual", "neat", "modest", "simple"]),
    ({"artist", "writer", "painter", "bohemian", "艺术家", "作家", "画家"},
     ["relaxed", "expressive", "bohemian", "layered", "loose"]),
    ({"soldier", "officer", "military", "军人", "士兵"},
     ["uniform", "practical", "structured", "boots"]),
    ({"servant", "maid", "butler", "仆人", "女佣", "管家"},
     ["uniform", "modest", "apron", "service", "plain"]),
    ({"farmer", "peasant", "农民", "农夫"},
     ["practical", "coarse", "straw", "earth", "durable"]),
    ({"merchant", "shopkeeper", "店主", "商户"},
     ["practical", "modest", "apron", "plain"]),
    ({"journalist", "reporter", "记者"},
     ["practical", "layered", "coat", "camera", "restrained"]),
]

ECONOMIC_HINTS = {
    "low": ({"poor", "working class", "working_class", "low", "poverty",
             "destitute", "broke", "拮据", "贫困", "工薪", "底层"},
            ["worn", "repaired", "faded", "durable", "practical", "plain"]),
    "high": ({"wealthy", "rich", "aristocrat", "upper class", "upper_class",
              "high", "富裕", "贵族", "上层"},
             ["tailored", "fine", "silk", "velvet", "jewelry", "elegant",
              "formal", "polished"]),
}

ARC_HINTS = [
    ({"decline", "fall", "downfall", "落魄", "失势", "衰败", "没落"},
     ["worn", "repaired", "faded", "stained", "shabby"]),
    ({"rise", "success", "崛起", "成功", "翻身", "上升"},
     ["tailored", "polished", "fine", "clean"]),
    ({"grief", "mourning", "哀", "丧", "悲"}, ["dark", "black", "plain", "modest", "veil"]),
    ({"freedom", "liberation", "自由", "解放"}, ["loose", "flowing", "relaxed", "open"]),
    ({"survival", "survive", "struggle", "挣扎", "生存"},
     ["layered", "durable", "practical", "worn"]),
    ({"transformation", "change", "蜕变", "转变"},
     ["contrast", "layered", "transitional"]),
]

LIGHTING_TOKEN_HINTS = {
    "warm": {"warm", "golden", "amber", "tungsten", "candle", "sunset",
             "暖", "暖光", "黄昏", "烛"},
    "cool": {"cool", "blue", "moonlight", "cold", "neon", "steel", "冷",
             "冷光", "月光", "霓虹"},
    "contrast": {"contrast", "chiaroscuro", "noir", "hard light", "high contrast",
                 "强烈", "高反差", "明暗"},
}

NEGATIVES_BASE = [
    "no costume morphing between shots",
    "no unexpected accessories",
    "no color shift",
    "no logo, text or watermark",
    "no extra layers appearing or disappearing",
    "no warped hands, no deformed body",
    "no changing hairstyle between shots",
]
NEGATIVES_HISTORICAL = [
    "no modern zippers, no modern sneakers, no printed t-shirts",
    "no anachronistic plastic accessories",
]
NEGATIVES_RAIN = [
    "no instant drying between shots; wetness changes only on an explicit state transition",
]
NEGATIVES_DANCE = [
    "no unstable footwear, no wardrobe malfunction",
    "no rigid garment that blocks movement",
]


# Coarse period/region hierarchy: labels in the vault are intentionally broad,
# so "shanghai" must be compatible with "east_asia", "1930s" with
# "early_20th_century".  This is a *compatibility* check, not a precision claim.
PERIOD_PARENTS = {
    "1770s": {"1770s", "late 18th century", "18th century"},
    "1790s": {"1790s", "late 18th century", "18th century"},
    "1800s": {"1800s", "early 19th century", "19th century"},
    "1810s": {"1810s", "early 19th century", "19th century"},
    "1890s": {"1890s", "late 19th century", "19th century"},
    "1920s": {"1920s", "early 20th century", "20th century"},
    "1930s": {"1930s", "early 20th century", "20th century"},
    "1940s": {"1940s", "mid 20th century", "20th century"},
    "1950s": {"1950s", "mid 20th century", "20th century"},
    "1960s": {"1960s", "mid 20th century", "20th century"},
    "contemporary": {"contemporary", "21st century", "early 21st century", "present"},
    "late 19th century": {"late 19th century", "19th century"},
    "early 20th century": {"early 20th century", "20th century"},
    "mid 20th century": {"mid 20th century", "20th century"},
    "20th century": {"20th century"},
    "19th century": {"19th century"},
    "18th century": {"18th century"},
}
REGION_PARENTS = {
    "shanghai": {"shanghai", "china", "east asia", "asia"},
    "beijing": {"beijing", "china", "east asia", "asia"},
    "hong kong": {"hong kong", "china", "east asia", "asia"},
    "china": {"china", "east asia", "asia"},
    "japan": {"japan", "east asia", "asia"},
    "korea": {"korea", "east asia", "asia"},
    "east asia": {"east asia", "asia", "china", "japan", "korea",
                  "shanghai", "beijing", "hong kong"},
    "asia": {"asia", "east asia", "south asia", "southeast asia"},
    "united states": {"united states", "north america", "america", "us"},
    "north america": {"north america", "united states", "canada", "america"},
    "western europe": {"western europe", "europe", "france", "england",
                       "united kingdom", "italy", "germany", "spain"},
    "europe": {"europe", "western europe", "france", "england",
               "united kingdom", "italy", "germany", "spain",
               "northern europe", "central europe"},
    "northern europe": {"northern europe", "europe", "western europe",
                        "scandinavia"},
    "central europe": {"central europe", "europe", "western europe",
                       "germany", "austria"},
    "united kingdom": {"united kingdom", "england", "britain",
                       "western europe", "europe"},
    "france": {"france", "western europe", "europe"},
    "italy": {"italy", "western europe", "europe"},
    "middle east": {"middle east", "west asia", "ottoman empire", "turkey"},
    "ottoman empire": {"ottoman empire", "middle east", "west asia", "turkey"},
    "byzantine empire": {"byzantine empire", "eastern mediterranean",
                         "middle east", "europe"},
}


def pair_compatible(wanted, have, parents):
    """True when at least one wanted/have token pair is equal or hierarchically related."""
    if not wanted or not have:
        return True
    for a in wanted:
        for b in have:
            if a == b or (len(a) >= 2 and a in b) or (len(b) >= 2 and b in a):
                return True
            if b in parents.get(a, set()) or a in parents.get(b, set()):
                return True
    return False


def period_compatible(wanted, have):
    return pair_compatible(wanted, have, PERIOD_PARENTS)


def region_compatible(wanted, have):
    return pair_compatible(wanted, have, REGION_PARENTS)


def labels(values):
    """Normalised whole labels (no token splitting) for hierarchy checks."""
    out = set()
    for value in lib._as_list(values):
        norm = lib.norm_text(value)
        if norm:
            out.add(norm)
    return out


def card_period_labels(card):
    meta = card["meta"]
    return labels(list(lib.get_list(meta, "periods")) +
                  list(lib.get_list(meta, "period_label")))


def card_region_labels(card):
    meta = card["meta"]
    return labels(list(lib.get_list(meta, "regions")) +
                  list(lib.get_list(meta, "region_label")))


def label_pair_compatible(wanted, have, parents):
    """Whole-label compatibility via the coarse hierarchy maps."""
    if not wanted or not have:
        return True
    for a in wanted:
        for b in have:
            if a == b or a in parents.get(b, set()) or b in parents.get(a, set()):
                return True
            if (len(a) >= 4 and a in b) or (len(b) >= 4 and b in a):
                return True
    return False


def period_compatible_labels(wanted, have):
    return label_pair_compatible(wanted, have, PERIOD_PARENTS)


def region_compatible_labels(wanted, have):
    return label_pair_compatible(wanted, have, REGION_PARENTS)


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def expand_tokens(*values):
    """Token set plus a few Chinese<->English alias expansions."""
    out = set()
    raw = []
    for value in values:
        raw.extend(lib._as_list(value))
    for item in raw:
        norm = lib.norm_text(item)
        if not norm:
            continue
        out |= lib.tokens(item)
        for zh, en in TERM_ALIASES.items():
            if zh in str(item):
                out |= lib.tokens(en)
    # remove English filler words that would create false matches against card text
    return {token for token in out
            if token not in STOPWORDS and not (len(token) == 1 and token.isascii())}


def overlap_frac(wanted, have):
    """Fraction of wanted tokens matched in have; None when wanted empty."""
    wanted = {w for w in wanted if w}
    if not wanted:
        return None
    if not have:
        return 0.0
    hits = 0
    for w in wanted:
        for h in have:
            if w == h or (len(w) >= 2 and w in h) or (len(h) >= 2 and h in w):
                hits += 1
                break
    return hits / float(len(wanted))


def any_overlap(wanted, have):
    frac = overlap_frac(wanted, have)
    return bool(frac)


def meta_tokens(card, *keys):
    meta = card["meta"]
    values = []
    for key in keys:
        values.extend(lib._as_list(meta.get(key)))
    return expand_tokens(*values)


def value_frac(value, candidates, default=0.5):
    value = lib.norm_text(value)
    if not value:
        return default
    for candidate in candidates:
        c = lib.norm_text(candidate)
        if c and (value in c or c in value):
            return 1.0
    return 0.0


def material_weather_score(materials, weather_tokens):
    best = 0.0
    for material in materials:
        key = lib.norm_text(material)
        for weather, table in WEATHER_MATERIALS.items():
            if weather not in weather_tokens:
                continue
            for name, score in table.items():
                if key == name or key in name or name in key:
                    best = max(best, score)
    return best


def formality_value(card):
    raw = lib.norm_text(lib.get_str(card["meta"], "formality"))
    if not raw:
        return 0.4
    for key, value in FORMALITY_COST.items():
        if key in raw or raw in key:
            return value
    return 0.4


def cheap_material_score(card):
    materials = [lib.norm_text(m) for m in lib.get_list(card["meta"], "materials")]
    if not materials:
        return 0.5
    best = 0.5
    for material in materials:
        for key, cost in MATERIAL_COST.items():
            if material == key or material in key or key in material:
                best = min(best, cost)
    return best


def has_warm_color(colors):
    return any(c in WARM_COLORS or any(w in c for w in WARM_COLORS)
               for c in (lib.norm_text(x) for x in colors))


def has_cool_color(colors):
    return any(c in COOL_COLORS or any(w in c for w in COOL_COLORS)
               for c in (lib.norm_text(x) for x in colors))


def card_label(card):
    return (lib.get_str(card["meta"], "name_zh") or
            lib.get_str(card["meta"], "name_en") or
            lib.get_str(card["meta"], "id"))


def classify_slot(card):
    """Map a garment card to a wardrobe slot; returns None when unknown."""
    meta = card["meta"]
    cat = lib.norm_text(lib.get_str(meta, "category"))
    sub = lib.norm_text(lib.get_str(meta, "subcategory"))
    if cat in ("specialised", "specialized"):
        for key, slot in SUBCATEGORY_TO_SLOT.items():
            if key in sub:
                return slot
        if "protective" in sub or "防护" in sub:
            return "outerwear"
        if "uniform" in sub or "制服" in sub:
            return "set"
        return "set"
    if cat in CATEGORY_TO_SLOT:
        return CATEGORY_TO_SLOT[cat]
    for key, slot in CATEGORY_TO_SLOT.items():
        if key and (key in cat or cat in key):
            return slot
    if sub in SUBCATEGORY_TO_SLOT:
        return SUBCATEGORY_TO_SLOT[sub]
    for key, slot in SUBCATEGORY_TO_SLOT.items():
        if key and (key in sub or sub in key):
            return slot
    text = " ".join([
        cat, sub,
        lib.norm_text(lib.get_str(meta, "name_en")),
        lib.norm_text(lib.get_str(meta, "name_zh")),
    ])
    for hint, slot in SLOT_NAME_HINTS:
        if hint in text:
            return slot
    return None


REGION_SPECIFIC_WORDS = (
    "traditional", "regional", "ethnic", "folk", "民族", "传统", "地域",
    "kimono", "hanfu", "qipao", "cheongsam", " Ottoman", "ottoman",
    "byzantine", "japanese", "chinese", "korean", "和服", "汉服", "旗袍",
)


def is_region_specific(card):
    """Culture-specific garments need a region-compatible card; global staples do not."""
    meta = card["meta"]
    cat = lib.norm_text(lib.get_str(meta, "category"))
    sub = lib.norm_text(lib.get_str(meta, "subcategory"))
    if cat in ("specialised", "specialized"):
        return True
    if sub in ("traditional regional", "ceremonial"):
        return True
    tags = " ".join(lib._as_list(meta.get("style_tags")) +
                    lib._as_list(meta.get("tags"))).lower()
    return any(word.lower() in tags for word in REGION_SPECIFIC_WORDS)


def is_heels(card):
    sub = lib.norm_text(lib.get_str(card["meta"], "subcategory"))
    name = lib.norm_text(lib.get_str(card["meta"], "name_en") + " " +
                         lib.get_str(card["meta"], "name_zh"))
    return any(x in sub + " " + name for x in
               ["heel", "stiletto", "高跟", "pump"])


def is_open_footwear(card):
    sub = lib.norm_text(lib.get_str(card["meta"], "subcategory"))
    name = lib.norm_text(lib.get_str(card["meta"], "name_en") + " " +
                         lib.get_str(card["meta"], "name_zh"))
    return any(x in sub + " " + name for x in
               ["sandal", "flip", "slipper", "凉鞋", "拖鞋"])


# ---------------------------------------------------------------------------
# input normalisation
# ---------------------------------------------------------------------------
def first_present(*mappings):
    """Return the first non-empty value from candidate (mapping, keys) pairs."""
    for mapping, keys in mappings:
        if not isinstance(mapping, dict):
            continue
        for key in keys:
            value = mapping.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, (int, float)):
                return str(value)
            if isinstance(value, list) and value:
                return value
    return ""


def normalise_input(raw):
    if not isinstance(raw, dict):
        raise ValueError("input JSON must be an object")
    character = raw.get("character")
    if isinstance(character, str):
        character = {"name": character}
    if not isinstance(character, dict):
        character = {}
    scene = raw.get("scene") if isinstance(raw.get("scene"), dict) else {}
    period_obj = raw.get("period") if isinstance(raw.get("period"), dict) else {}

    def get(*keys):
        return first_present(
            (raw, keys), (character, keys), (scene, keys), (period_obj, keys))

    def as_text(value):
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        return str(value).strip()

    inp = {
        "character_name": as_text(get("character_name", "name", "character_id")) or "unnamed character",
        "age": as_text(get("age")) or "unknown",
        "gender_presentation": as_text(get("gender_presentation", "gender")) or "unknown",
        "occupation": as_text(get("occupation", "profession", "role")) or "unknown",
        "economic_status": as_text(get("economic_status", "economic", "social_class", "class")) or "unknown",
        "period": as_text(get("period", "time_period", "era", "story_period")) or "unknown",
        "region": as_text(get("region", "location", "geography", "city")) or "unknown",
        "season": as_text(get("season")) or "unknown",
        "scene": as_text(get("scene", "scene_id", "setting", "location_detail")) or "",
        "time": as_text(get("time", "time_of_day")) or "unknown",
        "weather": as_text(get("weather", "climate")) or "unknown",
        "action": as_text(get("action", "movement", "performance_requirements")) or "unknown",
        "arc": as_text(get("arc", "character_arc", "dramatic_arc")) or "unknown",
        "art_direction": as_text(get("art_direction", "visual_style", "style", "look_direction")) or "unknown",
        "lighting": as_text(get("lighting", "light")) or "unknown",
        "camera": as_text(get("camera", "camera_distance", "shot")) or "medium shot",
        "budget": as_text(get("budget", "production_budget")) or "medium",
        "fidelity_mode": as_text(get("fidelity_mode", "fidelity", "mode")) or "inspired",
        "tool": as_text(get("tool", "image_tool", "video_tool", "generator")) or "generic",
        "story_day": as_text(get("story_day", "day")) or "1",
        "gender": None,
        "state": raw.get("state") if isinstance(raw.get("state"), dict) else {},
        "notes": as_text(get("notes", "brief")) or "",
    }
    inp["gender"] = inp["gender_presentation"]
    mode = lib.norm_text(inp["fidelity_mode"])
    if mode.startswith("hist") or "史实" in inp["fidelity_mode"] or "历史" in inp["fidelity_mode"]:
        inp["fidelity_mode"] = "historical"
    elif mode.startswith("fict") or "虚构" in inp["fidelity_mode"] or "未来" in inp["fidelity_mode"]:
        inp["fidelity_mode"] = "fictional"
    else:
        inp["fidelity_mode"] = "inspired"
    budget = lib.norm_text(inp["budget"])
    if any(x in budget for x in ["low", "tight", "micro", "低", "紧"]):
        inp["budget"] = "low"
    elif any(x in budget for x in ["high", "premium", "高"]):
        inp["budget"] = "high"
    else:
        inp["budget"] = "medium"
    if isinstance(raw.get("scenes"), list) and raw["scenes"]:
        inp["scenes"] = raw["scenes"]
    return inp


# ---------------------------------------------------------------------------
# context retrieval (style / period / scene cards)
# ---------------------------------------------------------------------------
def rank_context_cards(cards, inp):
    """Score style/period_region/scene/look cards against the input."""
    art_tokens = expand_tokens(inp["art_direction"], inp["scene"],
                               inp["period"], inp["region"], inp["arc"])
    period_tokens = expand_tokens(inp["period"], inp["region"])
    want_period_only = expand_tokens(inp["period"])
    want_region_only = expand_tokens(inp["region"])
    scene_tokens = expand_tokens(inp["scene"], inp["time"], inp["weather"],
                                 inp["action"], inp["region"])
    style_scored = []
    period_scored = []
    scene_scored = []
    look_scored = []
    for card in cards:
        ctype = lib.norm_text(card["meta"].get("type"))
        if ctype == "style":
            hay = meta_tokens(card, "style_tags", "name_zh", "name_en", "aliases",
                              "tags", "colors", "materials", "style_period",
                              "design_language", "style_family")
            frac = overlap_frac(art_tokens, hay) or 0.0
            direct = overlap_frac(art_tokens, meta_tokens(card, "name_zh", "name_en",
                                                          "aliases")) or 0.0
            score = 0.6 * frac + 0.4 * direct
            style_scored.append((score, card))
        elif ctype == lib.norm_text("period_region"):
            period_hay = meta_tokens(card, "periods", "period_label",
                                     "name_zh", "name_en", "aliases")
            region_hay = meta_tokens(card, "regions", "region_label")
            p_frac = overlap_frac(want_period_only, period_hay)
            r_frac = overlap_frac(want_region_only, region_hay)
            p_frac = 0.0 if p_frac is None else p_frac
            r_frac = 0.0 if r_frac is None else r_frac
            # period must dominate: a 1920s request must not surface a 1930s card.
            score = 0.75 * p_frac + 0.25 * r_frac
            if p_frac == 0.0 and want_period_only:
                score = min(score, 0.2)
            period_scored.append((score, card))
        elif ctype == "scene":
            hay = meta_tokens(card, "name_zh", "name_en", "aliases", "tags",
                              "style_tags", "periods", "regions", "actions",
                              "weather", "time_place", "camera_lighting",
                              "scene_character")
            frac = overlap_frac(scene_tokens, hay) or 0.0
            scene_scored.append((frac, card))
        elif ctype == "look":
            hay = meta_tokens(card, "name_zh", "name_en", "aliases", "tags",
                              "style_tags", "periods", "regions", "materials",
                              "colors", "look_role", "look_items")
            frac = overlap_frac(art_tokens | period_tokens, hay) or 0.0
            look_scored.append((frac, card))
    for bucket in (style_scored, period_scored, scene_scored, look_scored):
        bucket.sort(key=lambda item: (-item[0], lib.get_str(item[1]["meta"], "id")))
    return {
        "style": style_scored, "period_region": period_scored,
        "scene": scene_scored, "look": look_scored,
    }


def build_context(cards, inp):
    ranked = rank_context_cards(cards, inp)
    top_styles = [card for score, card in ranked["style"] if score > 0][:2]
    top_periods = [card for score, card in ranked["period_region"] if score > 0][:1]
    top_scenes = [card for score, card in ranked["scene"] if score > 0][:1]
    ctx = {"input": inp, "styles": top_styles, "period_cards": top_periods,
           "scene_cards": top_scenes, "ranked": ranked}
    preferred = set()
    colors = set()
    materials = set()
    for card in top_styles + top_periods + top_scenes:
        preferred |= meta_tokens(card, "style_tags", "tags")
        colors |= meta_tokens(card, "colors")
        materials |= meta_tokens(card, "materials")
    direct = expand_tokens(inp["art_direction"])
    ctx["style_tags"] = preferred | direct
    ctx["style_colors"] = colors
    ctx["style_materials"] = materials
    ctx["style_refs"] = [lib.get_str(c["meta"], "id") for c in top_styles]
    ctx["period_refs"] = [lib.get_str(c["meta"], "id") for c in top_periods]
    ctx["scene_refs"] = [lib.get_str(c["meta"], "id") for c in top_scenes]
    return ctx


# ---------------------------------------------------------------------------
# hard constraints
# ---------------------------------------------------------------------------
def hard_filter(card, slot, ctx):
    """Return list of rejection reasons (empty list = pass)."""
    inp = ctx["input"]
    meta = card["meta"]
    mode = inp["fidelity_mode"]
    period_labels = card_period_labels(card)
    region_labels = card_region_labels(card)
    want_period_labels = labels([inp["period"]])
    want_region_labels = labels([inp["region"]])
    reasons = []

    if mode == "historical":
        if lib.get_str(meta, "evidence_status") == "example":
            reasons.append("historical mode: example card is not historical evidence")
        if (period_labels and want_period_labels and
                not period_compatible_labels(want_period_labels, period_labels)):
            reasons.append("historical mode: period mismatch (%s vs %s)" % (
                inp["period"], ", ".join(lib.get_list(meta, "periods"))))
    if (region_labels and want_region_labels and is_region_specific(card) and
            not region_compatible_labels(want_region_labels, region_labels)):
        reasons.append("region-specific card incompatible with %s (%s)" % (
            inp["region"], ", ".join(lib.get_list(meta, "regions"))))

    weather = expand_tokens(inp["weather"])
    action = expand_tokens(inp["action"])
    wet = bool(weather & WET_TOKENS)
    cold = bool(weather & COLD_TOKENS)
    dance = bool(action & {"dance", "dancing", "ballet", "choreography"}) or "舞" in inp["action"]
    physical = bool(action & {"run", "running", "chase", "fight", "combat",
                              "escape", "climb", "battle"})

    if wet:
        if slot == "footwear" and is_open_footwear(card):
            reasons.append("rain: open footwear is unsafe/wet")
        if slot == "outerwear":
            mats = [lib.norm_text(m) for m in lib.get_list(meta, "materials")]
            if any(m in ("suede", "silk") for m in mats):
                reasons.append("rain: suede/silk outer layer unsuitable")
    if cold:
        if slot == "footwear" and is_open_footwear(card):
            reasons.append("cold: open footwear unsuitable")
    if dance and slot == "footwear" and is_heels(card):
        reasons.append("dance: heels unsafe for dance movement")
    if physical and slot == "footwear" and is_heels(card):
        reasons.append("action: heels unsafe for running/fight action")

    movement_notes = lib.norm_text(lib.get_str(meta, "movement_notes"))
    if (dance or physical) and movement_notes:
        safe_phrases = ("不限制", "不受限", "不影响", "可自由")
        if not any(phrase in movement_notes for phrase in safe_phrases):
            for bad in ("not suitable", "unsuitable", "restrict movement",
                        "limited movement", "cannot move", "无法活动", "行动受限",
                        "不适合运动", "不便动作"):
                if bad in movement_notes:
                    reasons.append("movement: card notes restrict movement")
                    break
    return reasons


# ---------------------------------------------------------------------------
# item soft scoring
# ---------------------------------------------------------------------------
def dim_period(card, ctx):
    inp = ctx["input"]
    mode = inp["fidelity_mode"]
    periods = meta_tokens(card, "periods")
    regions = meta_tokens(card, "regions")
    want_period = expand_tokens(inp["period"])
    want_region = expand_tokens(inp["region"])
    p_frac = overlap_frac(want_period, periods)
    r_frac = overlap_frac(want_region, regions)
    if (want_period and periods and
            not period_compatible_labels(labels([inp["period"]]),
                                         card_period_labels(card))):
        p_frac = 0.0
    if p_frac is None:
        base = 0.5
    elif not periods:
        base = {"historical": 0.25, "inspired": 0.45, "fictional": 0.6}[mode]
    else:
        base = {"historical": 0.15 + 0.85 * p_frac,
                "inspired": 0.35 + 0.55 * p_frac,
                "fictional": 0.5 + 0.5 * p_frac}[mode]
    if (p_frac == 0.0 and periods and
            period_compatible_labels(labels([inp["period"]]), card_period_labels(card))):
        p_frac = 0.5
    if (r_frac == 0.0 and regions and
            region_compatible_labels(labels([inp["region"]]), card_region_labels(card))):
        r_frac = 0.5
    if r_frac is not None:
        base = 0.8 * base + 0.2 * (0.3 + 0.7 * r_frac)
    status = lib.get_str(card["meta"], "evidence_status")
    if mode == "historical" and status == "verified":
        base += 0.08
    return clamp(base)


def occupation_hint_tags(inp):
    text = lib.norm_text(inp["occupation"] + " " + inp["character_name"] + " " +
                         inp["arc"])
    tags = []
    for keys, hints in OCCUPATION_HINTS:
        for key in keys:
            if key in text:
                tags.extend(hints)
                break
    return tags


def economic_signal(inp):
    text = lib.norm_text(inp["economic_status"])
    if not text:
        return None
    for level, (keys, hints) in ECONOMIC_HINTS.items():
        for key in keys:
            if key in text:
                return level, hints
    return None


def dim_identity(card, ctx):
    inp = ctx["input"]
    hints = occupation_hint_tags(inp)
    occ_tokens = expand_tokens(inp["occupation"]) | set(hints)
    hay = meta_tokens(card, "style_tags", "tags", "aliases", "name_zh",
                      "name_en", "category", "subcategory", "formality",
                      "materials", "prompt_en")
    occ_frac = overlap_frac(occ_tokens, hay)
    if occ_frac is None:
        occ_frac = 0.5
    econ = economic_signal(inp)
    if econ is None:
        econ_frac = 0.5
    else:
        level, econ_hints = econ
        econ_frac = overlap_frac(econ_hints, hay)
        if econ_frac is None:
            econ_frac = 0.5
        formality = formality_value(card)
        if level == "low":
            econ_frac = 0.45 * econ_frac + 0.55 * (1.0 - formality)
        else:
            econ_frac = 0.45 * econ_frac + 0.55 * formality
    return clamp(0.55 * occ_frac + 0.45 * econ_frac)


def dim_environment(card, ctx):
    inp = ctx["input"]
    weather = expand_tokens(inp["weather"])
    season = expand_tokens(inp["season"])
    materials = lib.get_list(card["meta"], "materials")
    mat_score = material_weather_score(materials, weather)
    if weather:
        env = 0.65 * mat_score + 0.35 * 0.5
    else:
        env = 0.5
    season_frac = overlap_frac(season, meta_tokens(card, "season"))
    if season_frac is not None:
        env = 0.7 * env + 0.3 * season_frac
    scene = lib.norm_text(inp["scene"])
    cat = lib.norm_text(lib.get_str(card["meta"], "category"))
    if any(x in scene for x in ["indoor", "interior", "室内"]) and cat in (
            "outerwear", "carried_prop"):
        env -= 0.05
    if any(x in scene for x in ["outdoor", "exterior", "户外", "street"]) and cat == "outerwear":
        env += 0.05
    if cat == "outerwear" and weather & (WET_TOKENS | COLD_TOKENS | WIND_TOKENS):
        env += 0.1
    return clamp(env)


def dim_art(card, ctx):
    style_tags = ctx.get("style_tags", set())
    style_colors = ctx.get("style_colors", set())
    hay = meta_tokens(card, "style_tags", "tags", "prompt_en", "name_zh",
                      "name_en", "aliases")
    frac = overlap_frac(style_tags, hay) or 0.0
    colors = meta_tokens(card, "colors")
    color_frac = overlap_frac(style_colors, colors) or 0.0
    return clamp(0.6 * frac + 0.25 * color_frac + 0.15 * (1.0 if hay & style_tags else 0.0))


def dim_movement(card, ctx):
    inp = ctx["input"]
    action = expand_tokens(inp["action"])
    if not action:
        return 0.5
    hay = meta_tokens(card, "movement_notes", "materials", "silhouette", "fit",
                      "subcategory", "prompt_en", "tags", "style_tags")
    frac = overlap_frac(action, hay) or 0.0
    score = 0.4 + 0.6 * frac
    notes = lib.norm_text(lib.get_str(card["meta"], "movement_notes"))
    if notes and any(x in notes for x in ["flow", "stretch", "twirl", "spin",
                                          "unrestricted", "flexible", "sweep",
                                          "飘", "摆", "弹性"]):
        score += 0.1
    dance = bool(action & {"dance", "dancing", "ballet"}) or "舞" in inp["action"]
    if dance and is_heels(card):
        score -= 0.35
    if dance and "stretch" in notes:
        score += 0.1
    return clamp(score)


def dim_arc(card, ctx):
    inp = ctx["input"]
    arc = lib.norm_text(inp["arc"])
    if not arc:
        return 0.5
    hints = []
    for keys, tags in ARC_HINTS:
        for key in keys:
            if key in arc:
                hints.extend(tags)
    want = set(lib.tokens(inp["arc"])) | set(hints)
    hay = meta_tokens(card, "tags", "style_tags", "materials", "colors",
                      "silhouette", "name_zh", "name_en", "prompt_en",
                      "movement_notes")
    frac = overlap_frac(want, hay)
    if frac is None:
        return 0.5
    return clamp(0.35 + 0.65 * frac)


def lighting_kind(inp):
    text = lib.norm_text(inp["lighting"])
    if not text:
        return None, set()
    found = []
    tokens = set()
    for kind, words in LIGHTING_TOKEN_HINTS.items():
        for w in words:
            if w in text:
                found.append(kind)
                tokens.add(kind)
                break
    return (found[0] if found else None), tokens


def dim_camera(card, ctx):
    inp = ctx["input"]
    meta = card["meta"]
    base = 0.4
    lighting_notes = meta_tokens(card, "lighting_notes")
    kind, kinds = lighting_kind(inp)
    colors = [lib.norm_text(c) for c in lib.get_list(meta, "colors")]
    if kind == "warm":
        base += 0.2 * (1.0 if has_warm_color(colors) else 0.0)
    elif kind == "cool":
        base += 0.2 * (1.0 if has_cool_color(colors) else 0.0)
    elif kind == "contrast":
        if has_warm_color(colors) or has_cool_color(colors):
            base += 0.1
    if lighting_notes:
        frac = overlap_frac(expand_tokens(inp["lighting"]), lighting_notes) or 0.0
        base += 0.2 * frac
    else:
        base += 0.1
    if lib.get_str(meta, "prompt_en"):
        base += 0.15
    if lib.get_list(meta, "source_ids") or lib.get_str(meta, "review_status") == "reviewed":
        base += 0.1
    return clamp(base)


ITEM_SCORERS = [
    ("period", dim_period),
    ("identity", dim_identity),
    ("environment", dim_environment),
    ("art", dim_art),
    ("movement", dim_movement),
    ("arc", dim_arc),
    ("camera", dim_camera),
]


def score_item(card, slot, ctx):
    scores = {}
    for dim, func in ITEM_SCORERS:
        scores[dim] = func(card, ctx)
    total = sum(scores[dim] * DIM_WEIGHTS[dim] for dim in scores)
    return {
        "card": card,
        "slot": slot,
        "scores": scores,
        "total": total,
        "id": lib.get_str(card["meta"], "id"),
        "name_zh": lib.get_str(card["meta"], "name_zh"),
        "name_en": lib.get_str(card["meta"], "name_en"),
        "evidence_status": lib.get_str(card["meta"], "evidence_status") or "unknown",
        "source_ids": lib.get_list(card["meta"], "source_ids"),
        "colors": lib.get_list(card["meta"], "colors"),
        "materials": lib.get_list(card["meta"], "materials"),
        "prompt_en": lib.get_str(card["meta"], "prompt_en"),
        "movement_notes": lib.get_str(card["meta"], "movement_notes"),
        "lighting_notes": lib.get_str(card["meta"], "lighting_notes"),
        "formality": lib.get_str(card["meta"], "formality"),
        "cost": 0.55 * cheap_material_score(card) + 0.25 * formality_value(card) + 0.2 * 0.4,
    }


# ---------------------------------------------------------------------------
# candidate pool
# ---------------------------------------------------------------------------
def build_pools(cards, ctx):
    inp = ctx["input"]
    pools = {}
    rejected = []
    unslotted = []
    for card in cards:
        if lib.norm_text(card["meta"].get("type")) != "garment":
            continue
        slot = classify_slot(card)
        if not slot:
            unslotted.append(lib.get_str(card["meta"], "id"))
            continue
        reasons = hard_filter(card, slot, ctx)
        if reasons:
            rejected.append({"id": lib.get_str(card["meta"], "id"),
                             "slot": slot, "reasons": reasons})
            continue
        item = score_item(card, slot, ctx)
        pools.setdefault(slot, []).append(item)
    for slot in pools:
        pools[slot].sort(key=lambda item: (-item["total"], item["id"]))
    ctx["rejected"] = rejected
    ctx["unslotted"] = unslotted
    return pools


def needs_outer(ctx):
    inp = ctx["input"]
    weather = expand_tokens(inp["weather"])
    season = expand_tokens(inp["season"])
    return bool(weather & (WET_TOKENS | COLD_TOKENS | WIND_TOKENS)) or bool(
        season & {"winter", "autumn", "冬", "秋"})


# ---------------------------------------------------------------------------
# look assembly and scoring
# ---------------------------------------------------------------------------
def item_signature_ids(items):
    return [item["id"] for item in items.values() if item]


def look_colors(items):
    colors = set()
    for item in items.values():
        if not item:
            continue
        for color in item["colors"]:
            norm = lib.norm_text(color)
            if norm:
                colors.add(norm)
    return colors


def look_style_tags(items):
    tags = set()
    for item in items.values():
        if item:
            tags |= meta_tokens(item["card"], "style_tags")
    return tags


PART_FAMILIES_BY_SLOT = {
    "upper_body": {"collar", "neckline", "sleeve", "placket", "closure",
                   "pleats", "ornament", "shoulder"},
    "inner_layer": {"collar", "neckline", "sleeve", "closure", "pleats"},
    "lower_body": {"waistline", "pleats", "pocket", "closure", "length",
                   "support"},
    "outerwear": {"collar", "placket", "closure", "pocket", "vent",
                  "length", "shoulder"},
    "one_piece": {"collar", "neckline", "sleeve", "closure", "waistline",
                  "pleats", "length", "ornament"},
    "set": {"collar", "sleeve", "closure", "waistline", "length", "ornament"},
    "footwear": {"closure", "ornament"},
    "accessory": {"ornament", "closure"},
}


def resolve_part_links(items, cards, ctx, extra_ids=None):
    """Attach garment_part cards to garments.

    Priority 1: explicit wikilink/name mention in the garment card (confidence=explicit).
    Priority 2: same period + a part family that belongs to the garment slot
                (confidence=suggested; surfaced as a suggestion, never as史实).
    """
    parts = []
    part_cards = [c for c in cards if lib.norm_text(c["meta"].get("type")) == lib.norm_text("garment_part")]
    if not part_cards:
        return parts
    for slot in SLOT_ORDER:
        item = items.get(slot)
        if not item:
            continue
        card = item["card"]
        body = lib.norm_text(card.get("body", "") + " " + card["meta"].get("prompt_en", ""))
        linked_here = 0
        for part in part_cards:
            pid = lib.get_str(part["meta"], "id")
            if pid in [p[0] for p in parts]:
                continue
            aliases = lib.get_list(part["meta"], "aliases")
            names = [lib.get_str(part["meta"], "name_zh"),
                     lib.get_str(part["meta"], "name_en")] + aliases
            linked = pid in lib.card_ids_in(card.get("body", ""))
            if not linked:
                for name in names:
                    norm = lib.norm_text(name)
                    if len(norm) >= 2 and norm in body:
                        linked = True
                        break
            if linked:
                parts.append((pid, part, slot, "explicit"))
                linked_here += 1
                if linked_here >= 2:
                    break
        if linked_here:
            continue
        # fallback: period-matched structure families relevant to this slot.
        # Both the garment and the requested period must support the part, so an
        # example/generic card never gets an arbitrary historical structure.
        slot_families = PART_FAMILIES_BY_SLOT.get(slot, set())
        item_periods = card_period_labels(card)
        if not item_periods:
            continue
        inp = ctx["input"]
        target_periods = labels([inp["period"]])
        for part in part_cards:
            pid = lib.get_str(part["meta"], "id")
            if pid in [p[0] for p in parts]:
                continue
            family = lib.norm_text(lib.get_str(part["meta"], "part_family"))
            if family not in slot_families:
                continue
            part_periods = card_period_labels(part)
            if not part_periods:
                continue
            if not period_compatible_labels(item_periods, part_periods):
                continue
            if target_periods and not period_compatible_labels(target_periods, part_periods):
                continue
            parts.append((pid, part, slot, "suggested"))
            break
    if extra_ids:
        for pid in extra_ids:
            if pid in [p[0] for p in parts]:
                continue
            for part in part_cards:
                if lib.get_str(part["meta"], "id") == pid:
                    parts.append((pid, part, "look_card", "explicit"))
                    break
    return parts


def resolve_material_links(items, cards):
    """Attach material cards matching the garment material names."""
    mats = []
    material_cards = [c for c in cards if lib.norm_text(c["meta"].get("type")) == "material"]
    if not material_cards:
        return mats
    for slot in SLOT_ORDER:
        item = items.get(slot)
        if not item:
            continue
        for material in item["materials"]:
            m_norm = lib.norm_text(material)
            for mat in material_cards:
                mid = lib.get_str(mat["meta"], "id")
                if mid in [m[0] for m in mats]:
                    continue
                names = ([lib.get_str(mat["meta"], "name_zh"),
                          lib.get_str(mat["meta"], "name_en")] +
                         lib.get_list(mat["meta"], "aliases") +
                         lib.get_list(mat["meta"], "fiber_content") +
                         lib.get_list(mat["meta"], "material_family"))
                if any(m_norm and (m_norm in lib.norm_text(n) or lib.norm_text(n) in m_norm)
                       for n in names if lib.norm_text(n)):
                    mats.append((mid, mat, slot))
                    break
    return mats


def score_look(items, ctx, cards, source_look_id=None, full=True, extra_part_ids=None,
               extra_material_ids=None):
    inp = ctx["input"]
    fractions = {}
    weighted_sum = 0.0
    weight_total = 0.0
    for dim, _label, _weight in DIM_ORDER:
        weight = 0.0
        total = 0.0
        for slot, item in items.items():
            if not item or dim not in item["scores"]:
                continue
            w = ITEM_WEIGHTS.get(slot, 1.0)
            weight += w
            total += w * item["scores"][dim]
        if weight == 0:
            fractions[dim] = 0.0
        else:
            fractions[dim] = total / weight
            weighted_sum += fractions[dim] * DIM_WEIGHTS[dim]
            weight_total += DIM_WEIGHTS[dim]

    base_score = weighted_sum
    missing = []
    has_upper = items.get("upper_body")
    has_lower = items.get("lower_body")
    has_full = items.get("one_piece") or items.get("set")
    if not has_full and not (has_upper and has_lower):
        missing.append("upper_body+lower_body or one_piece")
    elif not has_full and not has_upper:
        missing.append("upper_body")
    elif not has_full and not has_lower:
        missing.append("lower_body")
    if not items.get("footwear"):
        missing.append("footwear")
    if needs_outer(ctx) and not items.get("outerwear"):
        missing.append("outerwear")
    if missing:
        weighted_sum -= min(45.0, 9.0 * len(missing))
    total = clamp(weighted_sum, 0.0, 100.0)

    colors = look_colors(items)
    if len(colors) <= 3:
        total += 2.0
    elif len(colors) >= 6:
        total -= 2.0
    tags = look_style_tags(items)
    if ctx.get("style_tags") and tags & ctx["style_tags"]:
        total += 1.0
    evidence_verified = sum(1 for item in items.values() if item and item["evidence_status"] == "verified")
    if len(items) >= 5:
        total -= 0.5
    total = clamp(total, 0.0, 100.0)

    scores = {}
    for dim, _label, _weight in DIM_ORDER:
        scores[dim] = round(fractions.get(dim, 0.0) * DIM_WEIGHTS[dim], 1)

    parts = resolve_part_links(items, cards, ctx, extra_ids=extra_part_ids) if full else []
    mats = resolve_material_links(items, cards) if full else []
    if full and extra_material_ids:
        material_cards = {lib.get_str(c["meta"], "id"): c for c in cards
                          if lib.norm_text(c["meta"].get("type")) == "material"}
        for mid in extra_material_ids:
            if mid in [m[0] for m in mats] or mid not in material_cards:
                continue
            mats.append((mid, material_cards[mid], "look_card"))
    look = {
        "items": items,
        "item_ids": item_signature_ids(items),
        "missing": missing,
        "scores": scores,
        "base_score": round(base_score, 1),
        "total": round(total, 1),
        "colors": sorted(colors),
        "style_tags": sorted(tags),
        "parts": parts,
        "materials": mats,
        "source_look_id": source_look_id,
        "evidence_verified": evidence_verified,
        "cost": round(sum(item["cost"] for item in items.values() if item) /
                      max(1, len([i for i in items.values() if i])), 3),
    }
    if full:
        look["prompt_image"] = build_image_prompt(look, ctx)
        look["prompt_video"] = build_video_prompt(look, ctx)
        look["continuity_lock"] = build_continuity_lock(look, ctx)
        look["reasons"], look["risks"] = build_explanations(look, ctx)
        look["evidence"] = collect_evidence(look, ctx)
    return look


def combo_key(items):
    return tuple(sorted((slot, item["id"]) for slot, item in items.items() if item))


def build_combos(pools, ctx, cards):
    """Enumerate plausible wardrobe combinations, including curated look cards."""
    if not pools:
        return [], []
    def top(slot, k=4):
        return pools.get(slot, [])[:k]

    combos = []
    seen = set()

    def add(items):
        key = combo_key(items)
        if key in seen:
            return
        seen.add(key)
        combos.append(items)

    uppers = top("upper_body")
    lowers = top("lower_body")
    fulls = top("one_piece") + top("set")
    outer_all = top("outerwear", 3)
    boots = top("footwear", 3)
    accessories = top("accessory", 2)
    props = top("carried_prop", 2)
    required_outer = needs_outer(ctx)

    outer_options = outer_all if outer_all else [None]
    if not required_outer:
        outer_options = list(outer_options) + [None]

    core_sets = []
    for full in fulls:
        core_sets.append({"one_piece": full} if full["slot"] == "one_piece" else {"set": full})
    for upper in uppers:
        for lower in lowers:
            core_sets.append({"upper_body": upper, "lower_body": lower})
    if not fulls and not (uppers and lowers):
        for full in fulls:
            core_sets.append({"one_piece": full})
        for upper in uppers:
            core_sets.append({"upper_body": upper})
        for lower in lowers:
            core_sets.append({"lower_body": lower})

    if not boots:
        boots = [None]
    for core in core_sets:
        for outer in outer_options:
            for boot in boots:
                base = dict(core)
                if outer:
                    base["outerwear"] = outer
                if boot:
                    base["footwear"] = boot
                add(base)
                for acc in accessories:
                    with_acc = dict(base)
                    with_acc["accessory"] = acc
                    add(with_acc)
                for prop in props:
                    with_prop = dict(base)
                    with_prop["carried_prop"] = prop
                    add(with_prop)
                for acc in accessories:
                    for prop in props:
                        both = dict(base)
                        both["accessory"] = acc
                        both["carried_prop"] = prop
                        add(both)

    # Curated look cards that resolve to >=2 real garment cards.
    id_to_card = {lib.get_str(c["meta"], "id"): c for c in cards
                  if lib.norm_text(c["meta"].get("type")) == "garment"}
    curated = []
    for card in cards:
        if lib.norm_text(card["meta"].get("type")) != "look":
            continue
        if hard_filter(card, "look", ctx):
            continue
        items = {}
        candidate_ids = lib.get_list(card["meta"], "look_items") + \
            lib.find_wikilink_ids(card.get("body", ""))
        for gid in candidate_ids:
            if gid not in id_to_card:
                continue
            garment = id_to_card[gid]
            slot = classify_slot(garment)
            if slot and slot not in items and not hard_filter(garment, slot, ctx):
                item = score_item(garment, slot, ctx)
                items[slot] = item
        if len(items) < 2:
            continue
        # A curated look is a fixed composition: skip it when the current scene
        # hard-requires a layer it does not contain (e.g. no outerwear in rain).
        if needs_outer(ctx) and not items.get("outerwear"):
            continue
        if not items.get("footwear"):
            continue
        curated.append((lib.get_str(card["meta"], "id"), card, items))
    return combos, curated


def pick_looks(combos, curated, ctx, cards):
    scored = []
    for items in combos:
        scored.append(score_look(items, ctx, cards, full=False))
    for look_id, card, items in curated:
        look = score_look(items, ctx, cards, source_look_id=look_id, full=False)
        look["total"] = clamp(look["total"] + 3.0, 0.0, 100.0)  # curated coherence bonus
        scored.append(look)
    scored.sort(key=lambda look: (-look["total"], tuple(look["item_ids"])))

    def sig(look):
        return tuple(sorted(look["item_ids"]))

    def palette_distance(x, y):
        cx, cy = set(x["colors"]), set(y["colors"])
        if not cx and not cy:
            return 1.0
        return 1.0 - len(cx & cy) / float(len(cx | cy))

    # Deduplicate identical combinations (same garment ids) before picking A/B/C.
    unique = []
    seen = set()
    for look in scored:
        key = sig(look)
        if key in seen:
            continue
        seen.add(key)
        unique.append(look)
    scored = unique
    if not scored:
        return []
    a = scored[0]
    a_ids = set(a["item_ids"])

    # B: clearly different composition (different garment ids), prefer different palette.
    candidates_b = [look for look in scored[1:] if set(look["item_ids"]) != a_ids]
    if not candidates_b:
        return [a]
    threshold = max(0.0, a["total"] - 22.0)
    viable_b = [look for look in candidates_b if look["total"] >= threshold]
    if viable_b:
        b = max(viable_b, key=lambda look: (
            palette_distance(a, look) >= 0.34,
            len(set(look["item_ids"]) ^ a_ids),
            look["total"]))
    else:
        b = candidates_b[0]
    b_ids = set(b["item_ids"])

    # C: budget/art-direction alternative, distinct from both A and B.
    candidates_c = [look for look in scored[1:]
                    if set(look["item_ids"]) != a_ids and
                    set(look["item_ids"]) != b_ids]
    if not candidates_c:
        return [a, b]
    c_threshold = max(32.0, a["total"] - 45.0)
    feasible = [look for look in candidates_c if look["total"] >= c_threshold]
    pool_c = feasible or candidates_c
    c = min(pool_c, key=lambda look: (look["cost"], -look["total"]))
    chosen = [a, b, c]
    # Upgrade the chosen looks with full prompts/parts/materials/evidence.
    full_looks = []
    card_by_id = {lib.get_str(c["meta"], "id"): c for c in cards}
    for look in chosen:
        source_look_id = look.get("source_look_id")
        extra_parts, extra_mats = [], []
        if source_look_id and source_look_id in card_by_id:
            source_card = card_by_id[source_look_id]
            refs = lib.get_list(source_card["meta"], "look_items") + \
                lib.find_wikilink_ids(source_card.get("body", ""))
            extra_parts = [ref for ref in refs
                           if ref.startswith("STR-") and ref in card_by_id]
            extra_mats = [ref for ref in refs
                          if ref.startswith("MAT-") and ref in card_by_id]
        rebuilt = score_look(look["items"], ctx, cards,
                             source_look_id=source_look_id, full=True,
                             extra_part_ids=extra_parts,
                             extra_material_ids=extra_mats)
        if source_look_id:
            rebuilt["total"] = clamp(rebuilt["total"] + 3.0, 0.0, 100.0)
        full_looks.append(rebuilt)
    return full_looks


# ---------------------------------------------------------------------------
# prompts / lock / explanations / evidence
# ---------------------------------------------------------------------------
def item_prompt_phrase(item):
    meta = item["card"]["meta"]
    prompt = lib.get_str(meta, "prompt_en")
    if prompt:
        return prompt
    bits = []
    name = lib.get_str(meta, "name_en") or lib.get_str(meta, "name_zh")
    if name:
        bits.append(name)
    if item["colors"]:
        bits.append(", ".join(item["colors"]))
    if item["materials"]:
        bits.append(", ".join(item["materials"]))
    silhouette = lib.get_str(meta, "silhouette")
    if silhouette:
        bits.append(silhouette + " silhouette")
    return ", ".join(bits) if bits else item["id"]


def look_pieces(items):
    parts = []
    for slot in SLOT_ORDER:
        item = items.get(slot)
        if not item:
            continue
        parts.append("%s: %s" % (SLOT_EN.get(slot, slot),
                                 item_prompt_phrase(item)))
    return "; ".join(parts)


def fidelity_phrase(mode):
    if mode == "historical":
        return ("historically grounded period costume, period-accurate construction "
                "and materials, no modern fashion elements")
    if mode == "fictional":
        return ("original fictional-world costume design, explicitly not a historical "
                "reconstruction, internally consistent world-building")
    return ("period-inspired modern interpretation, historical silhouette cues mixed "
            "with contemporary construction")


def build_image_prompt(look, ctx):
    inp = ctx["input"]
    age = lib.norm_text(inp.get("age", ""))
    if age and age != "unknown":
        subject = "full-body character design of a %s-year-old %s" % (
            inp["age"], inp["character_name"])
    else:
        subject = "full-body character design of an adult %s" % inp["character_name"]
    bits = [
        subject,
        look_pieces(look["items"]),
        "palette: %s" % (", ".join(look["colors"]) if look["colors"] else "as specified"),
        "setting: %s, %s, %s" % (inp["scene"] or "unspecified location",
                                 inp["time"], inp["weather"]),
        "art direction: %s" % inp["art_direction"],
        "lighting: %s" % inp["lighting"],
        "camera: %s" % inp["camera"],
        fidelity_phrase(inp["fidelity_mode"]),
        "realistic fabric texture, visible seams and construction details, "
        "cinematic costume reference",
    ]
    if look["parts"]:
        bits.append("construction details: " + "; ".join(
            "%s (%s)" % (lib.get_str(p[1]["meta"], "name_en") or
                         lib.get_str(p[1]["meta"], "name_zh"), p[0])
            for p in look["parts"]))
    bits.append(build_continuity_lock(look, ctx))
    prompt = ", ".join(bit for bit in bits if bit)
    tool = lib.norm_text(inp["tool"])
    if "midjourney" in tool or tool == "mj":
        prompt += " --ar 2:3 --style raw --v 6"
    elif "dall" in tool:
        prompt += ""
    elif "sdxl" in tool or "stable diffusion" in tool or tool == "sd":
        prompt += ", ultra detailed costume sheet"
    return prompt


def build_video_prompt(look, ctx):
    inp = ctx["input"]
    motion = []
    for slot in ("outerwear", "lower_body", "one_piece", "upper_body"):
        item = look["items"].get(slot)
        if item and item["movement_notes"]:
            motion.append(item["movement_notes"])
    bits = [
        "%s, %s" % (inp["character_name"], inp["action"]),
        "scene: %s, %s, %s" % (inp["scene"] or "unspecified location",
                               inp["time"], inp["weather"]),
        "camera: %s" % inp["camera"],
        "costume: " + look_pieces(look["items"]),
        "fabric motion: " + ("; ".join(motion) if motion else
                             "natural fabric response to the action, gravity and wind"),
        "lighting: %s" % inp["lighting"],
        fidelity_phrase(inp["fidelity_mode"]),
        "single continuous take, consistent costume and accessories",
        build_continuity_lock(look, ctx),
        "negative constraints: " + ", ".join(video_negatives(inp)),
    ]
    return ", ".join(bit for bit in bits if bit)


def video_negatives(inp):
    negatives = list(NEGATIVES_BASE)
    if inp["fidelity_mode"] == "historical":
        negatives += NEGATIVES_HISTORICAL
    if expand_tokens(inp["weather"]) & WET_TOKENS:
        negatives += NEGATIVES_RAIN
    if expand_tokens(inp["action"]) & {"dance", "dancing", "ballet"} or "舞" in inp["action"]:
        negatives += NEGATIVES_DANCE
    return negatives


def build_continuity_lock(look, ctx):
    state = ctx["input"].get("state") or {}
    wetness = state.get("wetness", "dry")
    damage = state.get("damage", "none")
    dirt = state.get("dirt", "none")
    pieces = []
    for slot in SLOT_ORDER:
        item = look["items"].get(slot)
        if not item:
            continue
        material = ", ".join(item["materials"]) if item["materials"] else "unspecified"
        color = ", ".join(item["colors"]) if item["colors"] else "unspecified"
        pieces.append("%s %s [%s; %s; %s]" % (
            item["id"], item["name_en"] or item["name_zh"], color, material,
            SLOT_EN.get(slot, slot)))
    lock = ("continuity lock: " + " | ".join(pieces) +
            "; wetness=" + str(wetness) + "; damage=" + str(damage) +
            "; dirt=" + str(dirt) +
            "; keep all IDs, colors, materials, trims and accessory positions constant "
            "across shots")
    if look["materials"]:
        lock += "; fabric links: " + ", ".join(m[0] for m in look["materials"])
    return lock


def collect_evidence(look, ctx):
    sources = ctx["sources"]
    source_ids = []
    for item in look["items"].values():
        if item:
            source_ids.extend(item["source_ids"])
    for part in look["parts"]:
        source_ids.extend(lib.get_list(part[1]["meta"], "source_ids"))
    for mat in look["materials"]:
        source_ids.extend(lib.get_list(mat[1]["meta"], "source_ids"))
    source_ids = lib.unique_ordered(source_ids)
    urls = lib.source_urls(source_ids, sources)
    return {
        "source_ids": source_ids,
        "source_urls": [{"source_id": sid, "url": url} for sid, url in urls],
        "context_style_ids": ctx.get("style_refs", []),
        "context_period_ids": ctx.get("period_refs", []),
        "context_scene_ids": ctx.get("scene_refs", []),
        "item_evidence": {item["id"]: item["evidence_status"]
                          for item in look["items"].values() if item},
        "missing_urls": [sid for sid in source_ids if sid not in sources],
    }


def build_explanations(look, ctx):
    inp = ctx["input"]
    reasons = []
    risks = []
    scores = look["scores"]
    top_dims = sorted(scores.items(), key=lambda kv: -kv[1])[:2]
    top_keys = set(key for key, _score in top_dims)
    reasons.append("highest scoring dimensions: " + ", ".join(
        "%s %s/%d" % (label, scores[key], weight) for key, label, weight in DIM_ORDER
        if key in top_keys))
    for slot in SLOT_ORDER:
        item = look["items"].get(slot)
        if item:
            reasons.append("%s: %s %s (%s)" % (
                SLOT_LABELS.get(slot, slot), item["id"],
                item["name_zh"] or item["name_en"], item["formality"] or "formality unknown"))
    if look["parts"]:
        reasons.append("linked structure cards: " + ", ".join(p[0] for p in look["parts"]))
    if look["materials"]:
        reasons.append("linked material cards: " + ", ".join(m[0] for m in look["materials"]))
    if look["source_look_id"]:
        reasons.append("based on curated vault look card %s" % look["source_look_id"])
    if scores.get("period", 0) >= 18 and inp["fidelity_mode"] == "historical":
        reasons.append("period/culture score is supported by period-tagged cards")

    if look["missing"]:
        risks.append("incomplete look, missing: " + ", ".join(look["missing"]) +
                     " (knowledge-base gap, do not invent items)")
    if inp["fidelity_mode"] == "historical" and look["evidence_verified"] == 0:
        risks.append("no verified historical evidence in this look; treat as design hypothesis only")
    statuses = [item["evidence_status"] for item in look["items"].values() if item]
    if "example" in statuses:
        risks.append("look includes example cards, not historical evidence")
    if "unverified" in statuses:
        risks.append("look includes unverified cards")
    if inp["fidelity_mode"] == "inspired" and any(
            "_" not in status for status in statuses):
        pass
    weather = expand_tokens(inp["weather"])
    if weather & WET_TOKENS and not look["items"].get("outerwear"):
        risks.append("rain/weather exposure without outer layer")
    if inp["budget"] == "low":
        if len(look["items"]) > 5:
            risks.append("low budget: %d pieces may exceed wardrobe budget" % len(look["items"]))
        if look["cost"] > 0.55:
            risks.append("low budget: relatively expensive materials")
    if inp["fidelity_mode"] == "fictional":
        risks.append("fictional mode: no historical claim is made for this design")
    if inp["fidelity_mode"] == "historical" and inp["period"] == "unknown":
        risks.append("historical mode without a concrete period: cannot verify period accuracy")
    if expand_tokens(inp["action"]) & {"dance", "dancing", "ballet"} or "舞" in inp["action"]:
        if any(look["items"].get(slot) and is_heels(look["items"][slot]["card"])
               for slot in ("footwear",)):
            risks.append("dance: heeled footwear in the look")
    want_region_labels = labels([inp["region"]])
    region_mismatch = []
    for slot in SLOT_ORDER:
        item = look["items"].get(slot)
        if not item:
            continue
        item_region_labels = card_region_labels(item["card"])
        if (item_region_labels and want_region_labels and
                not region_compatible_labels(want_region_labels, item_region_labels)):
            region_mismatch.append(item["id"])
    if region_mismatch:
        risks.append("region mismatch in %s: cards document %s, not %s" % (
            ", ".join(region_mismatch), "their own regions", inp["region"]))
    risks.append("character psychology is a directorial interpretation, not a clothing-history fact")
    risks.append("all images remain external links; no third-party images are embedded in the vault")
    return reasons, risks


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------
def fmt_list(values):
    return ", ".join(str(v) for v in values) if values else "(none)"


def item_line(item):
    return "- **%s** `%s` — %s / %s; colors: %s; materials: %s; evidence: %s; sources: %s" % (
        SLOT_LABELS.get(item["slot"], item["slot"]), item["id"],
        item["name_zh"] or "-", item["name_en"] or "-",
        fmt_list(item["colors"]), fmt_list(item["materials"]),
        item["evidence_status"], fmt_list(item["source_ids"]))


def render_look(look, label):
    lines = []
    title = "Look %s" % label
    if look["source_look_id"]:
        title += " — curated card %s" % look["source_look_id"]
    lines.append("### %s | score %.1f/100" % (title, look["total"]))
    lines.append("")
    for slot in SLOT_ORDER:
        item = look["items"].get(slot)
        if item:
            lines.append(item_line(item))
    if look["parts"]:
        lines.append("- linked structure cards: " + ", ".join(
            "%s (%s%s)" % (lib.get_str(p[1]["meta"], "name_zh") or
                           lib.get_str(p[1]["meta"], "name_en"), p[0],
                           ", suggested" if len(p) > 3 and p[3] == "suggested" else "")
            for p in look["parts"]))
    if look["materials"]:
        lines.append("- linked material cards: " + ", ".join(
            "%s (%s)" % (lib.get_str(m[1]["meta"], "name_zh") or
                         lib.get_str(m[1]["meta"], "name_en"), m[0])
            for m in look["materials"]))
    lines.append("- palette: %s" % fmt_list(look["colors"]))
    lines.append("- score breakdown: " + ", ".join(
        "%s %s" % (label2, look["scores"].get(key, 0))
        for key, label2, _w in DIM_ORDER))
    lines.append("- why: " + " ".join(look["reasons"]))
    if look["risks"]:
        lines.append("- risks: " + " ".join(look["risks"]))
    lines.append("")
    lines.append("**Image prompt (EN):**")
    lines.append("")
    lines.append("```")
    lines.append(look["prompt_image"])
    lines.append("```")
    lines.append("")
    lines.append("**Video prompt (EN):**")
    lines.append("")
    lines.append("```")
    lines.append(look["prompt_video"])
    lines.append("```")
    lines.append("")
    return lines


def render_markdown(result):
    inp = result["input"]
    lines = []
    lines.append("# 造型推荐 — %s / %s" % (inp["character_name"], inp["scene"] or "unspecified scene"))
    lines.append("")
    lines.append("## 1. 角色与剧情理解（已知 / 假设）")
    lines.append("")
    lines.append("- 已知：角色 `%s`；职业/身份 `%s`；经济状态 `%s`；时代 `%s`；地域 `%s`；场景 `%s`；时间 `%s`；天气 `%s`；动作 `%s`；人物弧线 `%s`；美术 `%s`；光线 `%s`；预算 `%s`；严格度 `%s`；工具 `%s`。" % (
        inp["character_name"], inp["occupation"], inp["economic_status"],
        inp["period"], inp["region"], inp["scene"] or "unknown", inp["time"],
        inp["weather"], inp["action"], inp["arc"], inp["art_direction"],
        inp["lighting"], inp["budget"], inp["fidelity_mode"], inp["tool"]))
    unknowns = [key for key in ("occupation", "economic_status", "period", "region",
                                "weather", "action", "arc", "art_direction", "lighting")
                if inp[key] in ("", "unknown")]
    if unknowns:
        lines.append("- unknown / 待补：%s（不得自行断言，按缺省假设处理并标注）。" % ", ".join(unknowns))
    lines.append("- 假设：%s" % ("无明确假设" if not unknowns else
                                "unknown 字段按中性默认值处理，不构成史实或心理断言"))
    lines.append("")
    lines.append("## 2. 不可违反的约束")
    lines.append("")
    lines.append("- 严格度模式：`%s`（historical=有史实依据；inspired=时代灵感再造；fictional=虚构，不主张史实）。" % inp["fidelity_mode"])
    lines.append("- 硬约束过滤：年代/地域可行性、天气防护、动作/安全、史实证据门槛、预算限制。")
    lines.append("- 未命中卡片的品类必须显式标为知识库缺口（gap），不得编造单品 ID 或馆藏来源。")
    if result["rejected"]:
        lines.append("- 被硬约束拒绝的候选 %d 个：%s" % (
            len(result["rejected"]),
            "; ".join("%s (%s)" % (r["id"], "；".join(r["reasons"]))
                      for r in result["rejected"][:8])))
    lines.append("")
    lines.append("## 3. 候选造型 A/B/C")
    lines.append("")
    if not result["looks"]:
        lines.append("**无可用造型** — 知识库缺少必需品类，见第 8 节缺口。")
    for label, look in zip(["A", "B", "C"], result["looks"]):
        lines.extend(render_look(look, label))
    lines.append("## 4. 最终推荐 + 解释性评分")
    lines.append("")
    lines.append("| 维度 (满分) | A | B | C |")
    lines.append("| --- | --- | --- | --- |")
    for key, label, weight in DIM_ORDER:
        cells = []
        for look in result["looks"]:
            cells.append(str(look["scores"].get(key, 0)))
        lines.append("| %s (%d) | %s |" % (label, weight, " | ".join(cells)))
    lines.append("| **总计 (100)** | %s |" % " | ".join(
        "%.1f" % look["total"] for look in result["looks"]))
    lines.append("")
    if result["looks"]:
        a = result["looks"][0]
        lines.append("**推荐 %s**：%s。备选 B 用于明确不同的视觉方向，C 用于预算/美术替代；三者不共享同一套完整组合。" % (
            "Look A", "综合得分最高，且通过全部硬约束" if not a["missing"] else
            "综合得分最高，但存在知识库缺口（见风险）"))
    lines.append("")
    lines.append("## 5. 生图 Prompt (EN)")
    lines.append("")
    for label, look in zip(["A", "B", "C"], result["looks"]):
        lines.append("**Look %s**" % label)
        lines.append("")
        lines.append("```")
        lines.append(look["prompt_image"])
        lines.append("```")
        lines.append("")
    lines.append("## 6. 视频 Prompt (EN)")
    lines.append("")
    for label, look in zip(["A", "B", "C"], result["looks"]):
        lines.append("**Look %s**" % label)
        lines.append("")
        lines.append("```")
        lines.append(look["prompt_video"])
        lines.append("```")
        lines.append("")
    lines.append("## 7. 连续性检查点")
    lines.append("")
    lines.append("```")
    lines.append(result["looks"][0]["continuity_lock"] if result["looks"] else "no look produced")
    lines.append("```")
    lines.append("")
    lines.append("- 衣物 ID、颜色、材质、纽扣/闭合、配饰位置必须在所有镜头保持一致。")
    lines.append("- 湿度/污渍/破损只在显式状态切换时改变；默认 `wetness=dry, damage=none`。")
    lines.append("")
    lines.append("## 8. 数据证据 / 来源 / uncertainty")
    lines.append("")
    all_source_ids = []
    for look in result["looks"]:
        all_source_ids.extend(look["evidence"]["source_ids"])
    all_source_ids = lib.unique_ordered(all_source_ids)
    lines.append("- 检索命中的语境卡：styles=%s；period_region=%s；scene=%s" % (
        fmt_list(result["context"]["style_refs"]),
        fmt_list(result["context"]["period_refs"]),
        fmt_list(result["context"]["scene_refs"])))
    lines.append("- 造型数据证据 source_ids：%s" % fmt_list(all_source_ids))
    if result["source_urls"]:
        for entry in result["source_urls"]:
            lines.append("  - %s: %s" % (entry["source_id"], entry["url"]))
    if result["missing_urls"]:
        lines.append("- **来源缺口**：source_ids 在 04-来源/ 中找不到对应卡片：%s（不得编造链接）" % fmt_list(result["missing_urls"]))
    lines.append("- 未命中/缺口：%s" % (fmt_list(result["warnings"])))
    lines.append("- uncertainty：推荐为可解释的设计决策支持，不是服饰史定论；心理与叙事解读属于导演解释。")
    lines.append("")
    return "\n".join(lines)


def render_continuity_markdown(result):
    inp = result["input"]
    lines = []
    lines.append("# 多场次服装连续性 — %s" % inp["character_name"])
    lines.append("")
    lines.append("## 基础 Look（全片锁定）")
    lines.append("")
    lines.append("- 严格度：`%s`；时代=%s；地域=%s；美术=%s；光线=%s；预算=%s" % (
        inp["fidelity_mode"], inp["period"], inp["region"],
        inp["art_direction"], inp["lighting"], inp["budget"]))
    base = result["looks"][0] if result["looks"] else None
    if not base:
        lines.append("**FAIL** — 无可用基础 Look（知识库缺口）。")
        return "\n".join(lines)
    for slot in SLOT_ORDER:
        item = base["items"].get(slot)
        if item:
            lines.append(item_line(item))
    lines.append("")
    lines.append("```")
    lines.append(base["continuity_lock"])
    lines.append("```")
    lines.append("")
    lines.append("## 分场次状态与 Prompt")
    lines.append("")
    for scene in result["continuity"]["scenes"]:
        lines.append("### %s — %s / %s / %s" % (
            scene["scene_id"], scene["time"], scene["weather"], scene["action"]))
        lines.append("")
        lines.append("- 状态：wetness=%s, damage=%s, dirt=%s, accessories=%s" % (
            scene["state"].get("wetness", "dry"),
            scene["state"].get("damage", "none"),
            scene["state"].get("dirt", "none"),
            fmt_list(scene["state"].get("accessories", []))))
        lines.append("- 锁定衣物：%s" % fmt_list(scene["item_ids"]))
        lines.append("")
        lines.append("**Image prompt**")
        lines.append("")
        lines.append("```")
        lines.append(scene["prompt_image"])
        lines.append("```")
        lines.append("")
        lines.append("**Video prompt**")
        lines.append("")
        lines.append("```")
        lines.append(scene["prompt_video"])
        lines.append("```")
        lines.append("")
    lines.append("## 连续性检查")
    lines.append("")
    lines.append("| 属性 | " + " | ".join(
        scene["scene_id"] for scene in result["continuity"]["scenes"]) + " | 一致 |")
    lines.append("| --- | " + " | ".join("---" for _ in result["continuity"]["scenes"]) + " | --- |")
    for slot in SLOT_ORDER:
        row = []
        consistent = True
        first = None
        for scene in result["continuity"]["scenes"]:
            value = scene["items"].get(slot)
            value = value["id"] if value else "-"
            if first is None:
                first = value
            elif value != first:
                consistent = False
            row.append(value)
        if first == "-":
            continue
        lines.append("| %s | %s | %s |" % (
            SLOT_LABELS.get(slot, slot), " | ".join(row), "PASS" if consistent else "FAIL"))
    lines.append("| wetness | " + " | ".join(
        scene["state"].get("wetness", "dry") for scene in result["continuity"]["scenes"]) + " | explicit transitions |")
    lines.append("")
    lines.append("**Continuity verdict:** %s" % result["continuity"]["verdict"])
    if result["continuity"]["issues"]:
        lines.append("")
        lines.append("Issues:")
        for issue in result["continuity"]["issues"]:
            lines.append("- %s" % issue)
    return "\n".join(lines)


def result_to_json(result):
    def slim_look(look):
        return {
            "look_ref": look.get("look_ref"),
            "source_look_id": look["source_look_id"],
            "total": look["total"],
            "scores": look["scores"],
            "missing": look["missing"],
            "cost": look["cost"],
            "colors": look["colors"],
            "style_tags": look["style_tags"],
            "items": [
                {
                    "slot": slot,
                    "id": item["id"],
                    "name_zh": item["name_zh"],
                    "name_en": item["name_en"],
                    "colors": item["colors"],
                    "materials": item["materials"],
                    "evidence_status": item["evidence_status"],
                    "source_ids": item["source_ids"],
                    "scores": item["scores"],
                }
                for slot, item in sorted(look["items"].items(),
                                         key=lambda kv: SLOT_ORDER.index(kv[0]))
                if item
            ],
            "parts": [{"id": p[0], "slot": p[2],
                       "confidence": p[3] if len(p) > 3 else "explicit"}
                      for p in look["parts"]],
            "materials": [{"id": m[0], "slot": m[2]} for m in look["materials"]],
            "prompt_image": look["prompt_image"],
            "prompt_video": look["prompt_video"],
            "continuity_lock": look["continuity_lock"],
            "reasons": look["reasons"],
            "risks": look["risks"],
            "evidence": look["evidence"],
        }

    payload = {
        "input": result["input"],
        "fidelity_mode": result["input"]["fidelity_mode"],
        "looks": [slim_look(look) for look in result["looks"]],
        "context": {
            "style_refs": result["context"]["style_refs"],
            "period_refs": result["context"]["period_refs"],
            "scene_refs": result["context"]["scene_refs"],
        },
        "retrieved_ids": result["retrieved_ids"],
        "rejected": result.get("rejected", []),
        "warnings": result.get("warnings", []),
        "sources": result.get("source_urls", []),
        "missing_urls": result.get("missing_urls", []),
        "checks": result.get("checks", {}),
    }
    if "continuity" in result:
        payload["continuity"] = {
            "verdict": result["continuity"]["verdict"],
            "issues": result["continuity"]["issues"],
            "scenes": [
                {
                    "scene_id": scene["scene_id"],
                    "item_ids": scene["item_ids"],
                    "state": scene["state"],
                    "prompt_image": scene["prompt_image"],
                    "prompt_video": scene["prompt_video"],
                }
                for scene in result["continuity"]["scenes"]
            ],
        }
    return payload


# ---------------------------------------------------------------------------
# recommendation driver
# ---------------------------------------------------------------------------
def make_result(inp, cards, sources):
    ctx = build_context(cards, inp)
    ctx["sources"] = sources
    pools = build_pools(cards, ctx)
    retrieved = {slot: [item["id"] for item in items] for slot, items in pools.items()}
    combos, curated = build_combos(pools, ctx, cards)
    looks = pick_looks(combos, curated, ctx, cards)
    for idx, label in enumerate("ABC"):
        if idx < len(looks):
            looks[idx]["look_ref"] = label
    result = {
        "input": inp,
        "context": ctx,
        "looks": looks,
        "retrieved_ids": retrieved,
        "rejected": ctx.get("rejected", []),
        "warnings": [],
        "checks": {},
    }
    if not looks:
        result["warnings"].append("no wardrobe candidates: check card coverage for %s" % (
            "period " + inp["period"] if inp["fidelity_mode"] == "historical" else "required slots"))
        return result
    # Checks used by acceptance tests and by humans.
    all_ids = set()
    for card in cards:
        all_ids.add(lib.get_str(card["meta"], "id"))
    result["checks"]["ids_all_exist"] = all(
        item["id"] in all_ids for look in looks for item in look["items"].values())
    result["checks"]["three_looks"] = len(looks) == 3
    result["checks"]["all_have_garment"] = all(look["items"] for look in looks)
    result["checks"]["scores_sum_100"] = all(
        abs(sum(look["scores"].values()) - look["base_score"]) < 1.0 for look in looks)
    result["checks"]["looks_distinct"] = (
        len(looks) >= 2 and len({tuple(look["item_ids"]) for look in looks}) == len(looks))
    result["checks"]["fidelity_mode"] = inp["fidelity_mode"]
    result["checks"]["history_evidence"] = (
        inp["fidelity_mode"] != "historical" or
        all(look["evidence_verified"] > 0 for look in looks))
    source_ids = []
    for look in looks:
        source_ids.extend(look["evidence"]["source_ids"])
    result["source_urls"] = [{"source_id": sid, "url": url}
                             for sid, url in lib.source_urls(
                                 lib.unique_ordered(source_ids), sources)]
    result["missing_urls"] = [sid for sid in lib.unique_ordered(source_ids)
                              if sid not in sources]
    if result["missing_urls"]:
        result["warnings"].append("source_ids missing from 04-来源/: " +
                                  ", ".join(result["missing_urls"]))
    for slot in ("upper_body", "lower_body", "footwear"):
        if not any(look["items"].get(slot) for look in looks):
            result["warnings"].append("no %s candidates retrieved" % slot)
    if inp["fidelity_mode"] == "historical":
        if not any(item["evidence_status"] == "verified"
                   for look in looks for item in look["items"].values()):
            result["warnings"].append(
                "historical mode: no verified card in any look (knowledge-base gap)")
    if not result["checks"]["three_looks"]:
        result["warnings"].append("only %d distinct look(s) assembled" % len(looks))
    return result


def build_continuity_result(inp, cards, sources):
    scenes = inp.get("scenes", [])
    merged = dict(inp)
    weathers = " ".join(str(s.get("weather", "")) for s in scenes if isinstance(s, dict))
    actions = " ".join(str(s.get("action", "")) for s in scenes if isinstance(s, dict))
    if weathers:
        merged["weather"] = weathers
    if actions:
        merged["action"] = actions
    base_result = make_result(merged, cards, sources)
    if not base_result["looks"]:
        return base_result
    base = base_result["looks"][0]
    scene_results = []
    issues = []
    first_ids = None
    for idx, raw_scene in enumerate(scenes, 1):
        if not isinstance(raw_scene, dict):
            continue
        scene_input = dict(inp)
        for key in ("time", "weather", "action", "scene", "scene_id", "state",
                    "camera", "lighting", "story_day"):
            if raw_scene.get(key):
                scene_input[key] = raw_scene[key]
        raw_state = raw_scene.get("state")
        state = raw_state if isinstance(raw_state, dict) else {}
        state_explicit = isinstance(raw_state, dict) and bool(raw_state)
        if not state_explicit:
            issues.append("scene %s has no explicit state; defaulted to dry/none" %
                          raw_scene.get("scene_id", idx))
        scene_input["state"] = state
        scene_input.pop("scenes", None)
        scene_look = {
            "items": base["items"],
            "colors": base["colors"],
            "parts": base["parts"],
            "materials": base["materials"],
        }
        image = build_image_prompt(scene_look, {"input": scene_input})
        video = build_video_prompt(scene_look, {"input": scene_input})
        lock = build_continuity_lock(scene_look, {"input": scene_input})
        ids = item_signature_ids(base["items"])
        if first_ids is None:
            first_ids = ids
        elif ids != first_ids:
            issues.append("scene %s item ids differ from scene 1" % raw_scene.get("scene_id", idx))
        scene_results.append({
            "scene_id": raw_scene.get("scene_id", "S%d" % idx),
            "state_explicit": state_explicit,
            "time": scene_input.get("time", "unknown"),
            "weather": scene_input.get("weather", "unknown"),
            "action": scene_input.get("action", "unknown"),
            "state": {
                "wetness": state.get("wetness", "dry"),
                "damage": state.get("damage", "none"),
                "dirt": state.get("dirt", "none"),
                "accessories": state.get("accessories", []),
            },
            "items": base["items"],
            "item_ids": ids,
            "prompt_image": image,
            "prompt_video": video,
            "lock": lock,
        })
    wetness_sequence = [scene["state"]["wetness"] for scene in scene_results]
    # Explicit state switches are legal; only implicit defaults or item changes fail.
    verdict = "PASS" if not issues else "FAIL"
    continuity = {"scenes": scene_results, "issues": issues, "verdict": verdict,
                  "wetness_sequence": wetness_sequence}
    base_result["continuity"] = continuity
    base_result["looks"] = [base]
    base_result["checks"]["continuity_verdict"] = verdict
    return base_result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Evidence-linked costume recommendation over the vault cards.")
    parser.add_argument("input", help="path to input JSON")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument("--out", help="write output to file")
    parser.add_argument("--continuity", action="store_true",
                        help="force multi-scene continuity mode (input has 'scenes')")
    args = parser.parse_args(argv)

    try:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("ERROR: input file not found: %s" % args.input, file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print("ERROR: invalid JSON: %s" % exc, file=sys.stderr)
        return 2
    try:
        inp = normalise_input(raw)
    except ValueError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2

    cards, card_errors = lib.load_cards()
    for err in card_errors:
        print("WARN card parse: %s: %s" % (err["path"], err["error"]), file=sys.stderr)
    sources = lib.load_sources(cards=cards)
    multi = args.continuity or bool(inp.get("scenes"))
    if multi and inp.get("scenes"):
        result = build_continuity_result(inp, cards, sources)
    else:
        result = make_result(inp, cards, sources)

    if not result["looks"]:
        payload = result_to_json(result)
        text = (json.dumps(payload, ensure_ascii=False, indent=2) if args.json
                else "**FAIL** — no wardrobe candidates; see warnings.\n\n" +
                "\n".join("- " + w for w in result["warnings"]))
        if args.out:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
        return 3

    if multi and inp.get("scenes"):
        text = (json.dumps(result_to_json(result), ensure_ascii=False, indent=2)
                if args.json else render_continuity_markdown(result))
    else:
        text = (json.dumps(result_to_json(result), ensure_ascii=False, indent=2)
                if args.json else render_markdown(result))
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print("wrote %s" % args.out)
    else:
        print(text)
    if result["checks"].get("three_looks") is False and not multi:
        print("WARN: fewer than three distinct looks were possible (KB coverage).",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
