#!/usr/bin/env python3
"""workflow.py - script-driven Costume Director workflow.

Runs the full offline pipeline:
  script -> scene/speaker extraction -> character needs -> real KB retrieval
  -> per-character/stage A/B/C looks via scripts/recommend.py
  -> evidence/conflict checks -> cross-scene continuity plan
  -> dossier / scene table / full looks / prompts / fact-evidence-inference.

Inputs
------
  --script FILE   plain text or Markdown script (required; may be a single scene)
  --meta FILE     optional JSON with characters, relationships, period, region,
                  culture, art/cinematic style, environment, weather, lighting,
                  budget, action, fidelity_mode, stages, scene states, ...
                  Missing fields stay "unknown" and are reported as such.
  --out DIR       output directory (default: 11-验收/P3.5/workflow-runs/<script stem>)
  --json          print the machine-readable result to stdout (files always written)

Exit codes
----------
  0  workflow completed with at least one usable look
  2  invalid invocation / missing or unreadable script / invalid meta JSON / empty script
  3  character or wardrobe coverage insufficient: no characters, or recommend.py
     produced no looks for every character/stage (structured partial output is written)

The workflow never invents card IDs or source IDs.  Every garment/source ID in the
outputs comes from the vault, and missing evidence is reported as a gap.
"""

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

import costume_lib as lib

ROOT = lib.vault_root()
DEFAULT_OUT_ROOT = ROOT / "11-验收/P3.5/workflow-runs"

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def norm(value):
    return lib.norm_text(value) if value is not None else ""


def s(value, default="unknown"):
    if value is None:
        return default
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value) if value else default
    text = str(value).strip()
    return text if text else default


def is_unknown(value):
    return norm(value) in ("", "unknown", "unspecified", "未知", "未定")


def has_word(text, word):
    """Word-boundary match for ASCII terms, substring for CJK terms.  This keeps
    e.g. 'heath' from matching the weather token 'heat'."""
    word = str(word)
    if re.fullmatch(r"[A-Za-z][A-Za-z '\-]*", word):
        return re.search(r"\b%s\b" % re.escape(word), text, re.IGNORECASE) is not None
    return word.lower() in text.lower()


def as_list(value):
    return lib._as_list(value)


def slug(text, fallback="workflow"):
    text = re.sub(r"[^\w\u4e00-\u9fff\-]+", "-", str(text)).strip("-")
    return text[:80] or fallback


CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")


def english_only(text):
    """Keep the English portions of a recommend.py prompt (prompt fields are
    English-first but may contain Chinese fabric-motion notes)."""
    text = str(text or "")
    parts = re.split(r"(?<=[.;])\s+", text)
    kept = [part for part in parts if part.strip() and not CJK_RE.search(part)]
    cleaned = " ".join(kept).strip()
    if not cleaned:
        cleaned = CJK_RE.sub("", text)
    return re.sub(r"\s+", " ", cleaned).strip()


def roman_to_int(value):
    if value is None:
        return None
    text = str(value).strip().upper()
    if text.isdigit():
        return int(text)
    numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not text or any(char not in numerals for char in text):
        return None
    total = 0
    previous = 0
    for char in reversed(text):
        current = numerals[char]
        if current < previous:
            total -= current
        else:
            total += current
            previous = current
    return total


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + ("\n" if text and not text.endswith("\n") else ""),
                    encoding="utf-8")


# ---------------------------------------------------------------------------
# scenario / script parsing
# ---------------------------------------------------------------------------
ACT_RE = re.compile(r"^\s*ACT\s+[IVXLC0-9]+\b", re.IGNORECASE)
SCENE_HEADING_RE = re.compile(
    r"^\s*(?:SCENE\s+[IVXLC0-9]+\.?|"
    r"第[一二三四五六七八九十0-9]+[场幕]|场[：:]|"
    r"INT\.|EXT\.|内景|外景)\b.*$",
    re.IGNORECASE,
)
COMBINED_RE = re.compile(
    r"^\s*ACT\s+[IVXLC0-9]+\s*[,.;:]?\s*SCENE\s+[IVXLC0-9]+\.?\b.*$",
    re.IGNORECASE,
)
SPEAKER_ALLCAPS_RE = re.compile(
    r"^\s*(?P<name>[A-Z][A-Z '\-]{1,30})\s*[.:]\s+(?P<line>.+)$")
SPEAKER_MIXED_RE = re.compile(
    r"^\s*(?P<name>[A-Z][\w '\-]{1,30})\s*[.:]\s+(?P<line>.+)$")
SPEAKER_ZH_RE = re.compile(
    r"^\s*(?P<name>[\u4e00-\u9fff]{2,6}|[A-Za-z][\w '\-]{1,24})\s*[:：]\s*(?P<line>.+)$")

STOP_SPEAKERS = {
    "scene", "act", "enter", "exit", "exeunt", "thunder", "lightning",
    "int", "ext", "note", "time", "place", "the", "and", "all",
}
WEATHER_WORDS = {
    "rain": ("rain", "rainy", "drizzle", "downpour", "wet", "雨", "下雨", "雨夜"),
    "storm": ("storm", "thunder", "lightning", "tempest", "风暴", "雷雨", "雷电"),
    "snow": ("snow", "snowy", "blizzard", "雪"),
    "cold": ("cold", "freezing", "chill", "winter", "冷", "寒", "冬"),
    "heat": ("hot", "heat", "summer", "炎热", "夏"),
    "wind": ("wind", "windy", "gale", "风"),
    "fog": ("fog", "foggy", "mist", "雾"),
}
TIME_WORDS = {
    "night": ("night", "midnight", "夜"),
    "day": ("day", "daylight", "白天", "日"),
    "evening": ("evening", "dusk", "twilight", "傍晚", "黄昏"),
    "morning": ("morning", "dawn", "sunrise", "早晨", "清晨", "黎明"),
    "afternoon": ("afternoon", "下午"),
}
ACTION_WORDS = {
    "battle": ("battle", "fight", "combat", "war", "战斗", "打斗", "厮杀"),
    "murder": ("murder", "kill", "stab", "谋杀", "刺杀"),
    "dance": ("dance", "dancing", "ballet", "舞蹈", "舞"),
    "run": ("run", "running", "chase", "奔跑", "追逐"),
    "walk": ("walk", "walking", "行走", "步行"),
    "ride": ("ride", "riding", "horse", "骑马"),
    "banquet": ("banquet", "feast", "dinner", "宴会", "晚宴"),
    "sleep": ("sleep", "sleeping", "bed", "睡"),
}
INDOOR_WORDS = ("castle", "room", "hall", "chamber", "house", "indoor",
                "interior", "室内", "城堡", "房间", "大厅", "卧室")
OUTDOOR_WORDS = ("heath", "camp", "forest", "street", "field", "battlefield",
                 "outdoor", "exterior", "荒野", "营地", "森林", "街道", "战场")
STATE_RAIN = ("rain", "wet", "damp", "soaked", "雨", "湿")
STATE_DAMAGE = ("blood", "wound", "torn", "bruise", "gash", "cut", "血", "伤", "撕裂")
STATE_DIRT = ("mud", "dirt", "soot", "dust", "泥", "污", "尘")


def split_scenes(text):
    """Split a script into ordered scenes.  No invented scenes: if there are no
    headings the whole input is one scene."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    scenes = []
    current = None
    preamble = []
    current_act = ""
    for raw in lines:
        # tolerate Markdown heading decoration: "## ACT I, SCENE I. ..."
        line = re.sub(r"^\s*(?:#{1,6}\s*|\*\*|__)+", "", raw.rstrip()).strip()
        line = re.sub(r"(?:\*\*|__)\s*$", "", line).strip()
        if not line:
            if current is not None:
                current["lines"].append("")
            else:
                preamble.append("")
            continue
        combined = COMBINED_RE.match(line)
        act_only = ACT_RE.match(line) and not SCENE_HEADING_RE.match(line) and not combined
        if act_only:
            # "ACT I" alone is an act marker, not a scene boundary; keep it as
            # context for the next SCENE heading (avoids empty fragment scenes).
            current_act = line.strip()
            continue
        if combined or SCENE_HEADING_RE.match(line):
            if current is not None:
                scenes.append(current)
            title = line.strip()
            if current_act and not combined:
                title = "%s — %s" % (current_act, title)
            current = {"title": title, "lines": []}
        else:
            if current is None:
                preamble.append(line)
            else:
                current["lines"].append(line)
    if current is not None:
        scenes.append(current)
    if not scenes:
        scenes = [{"title": "single scene (no scene heading in input)",
                   "lines": lines}]
    for index, scene in enumerate(scenes, 1):
        scene["id"] = "S%d" % index
        scene["body"] = "\n".join(scene.pop("lines"))
        scene["preamble"] = "\n".join(preamble) if index == 1 else ""
        act_match = re.search(r"ACT\s+([IVXLC0-9]+)", scene["title"], re.IGNORECASE)
        scene_match = re.search(r"SCENE\s+([IVXLC0-9]+)", scene["title"], re.IGNORECASE)
        scene["act_number"] = roman_to_int(act_match.group(1)) if act_match else None
        scene["scene_number"] = roman_to_int(scene_match.group(1)) if scene_match else None
    return scenes


def _match_name_at_start(line, names):
    for name in sorted(names, key=len, reverse=True):
        pattern = re.compile(r"^\s*%s\s*[:.]\s+(.+)$" % re.escape(name),
                             re.IGNORECASE)
        match = pattern.match(line)
        if match:
            return name, match.group(1)
    return None, None


def parse_scene(scene, characters, meta):
    """Extract speakers, stage directions and environment facts from one scene."""
    names = [c["name"] for c in characters] + [alias for c in characters
                                               for alias in c.get("aliases", [])]
    speakers = {}
    stage_directions = []
    for line in scene["body"].split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("[") or stripped.startswith("("):
            stage_directions.append(stripped.strip("[]()"))
            continue
        name, dialogue = _match_name_at_start(stripped, names)
        if not name:
            match = SPEAKER_ALLCAPS_RE.match(stripped)
            if match:
                candidate = match.group("name").strip().title()
                if norm(candidate) not in STOP_SPEAKERS:
                    name, dialogue = candidate, match.group("line")
                    if not any(norm(candidate) == norm(n) for n in names):
                        names.append(candidate)
            if not name:
                match = SPEAKER_ZH_RE.match(stripped)
                if match and norm(match.group("name")) not in STOP_SPEAKERS:
                    name, dialogue = match.group("name").strip(), match.group("line")
        if name:
            # map aliases to the canonical character name
            canonical = name
            for character in characters:
                if norm(name) == norm(character["name"]) or any(
                        norm(name) == norm(alias) for alias in character.get("aliases", [])):
                    canonical = character["name"]
                    break
            speakers.setdefault(canonical, []).append(dialogue)
    heading = scene["title"]
    full_text = (heading + "\n" + scene["body"]).lower()
    environment = {
        "weather": [label for label, words in WEATHER_WORDS.items()
                    if any(has_word(full_text, word) for word in words)],
        "time": [label for label, words in TIME_WORDS.items()
                 if any(has_word(full_text, word) for word in words)],
        "actions": [label for label, words in ACTION_WORDS.items()
                    if any(has_word(full_text, word) for word in words)],
        "indoor": ("indoor" if any(has_word(full_text, word) for word in INDOOR_WORDS)
                   else "outdoor" if any(has_word(full_text, word) for word in OUTDOOR_WORDS)
                   else "unknown"),
        "location": "unknown",
    }
    # heading often carries the location after the scene number, e.g.
    # "SCENE I. A desert place."
    heading_clean = re.sub(r"^(ACT|SCENE)\s+[IVXLC0-9]+\.?\s*", "", heading,
                           flags=re.IGNORECASE)
    if heading_clean and heading_clean != heading:
        environment["location"] = heading_clean.strip(" .")
        for label, words in WEATHER_WORDS.items():
            if any(has_word(heading_clean, word) for word in words):
                if label not in environment["weather"]:
                    environment["weather"].append(label)
        for label, words in TIME_WORDS.items():
            if any(has_word(heading_clean, word) for word in words):
                if label not in environment["time"]:
                    environment["time"].append(label)
    # meta may supply explicit environment facts; those are recorded as meta facts
    meta_env = meta.get("environment") if isinstance(meta.get("environment"), dict) else {}
    if meta_env.get("weather") and not environment["weather"]:
        environment["weather"] = [s(meta_env["weather"])]
    if meta_env.get("location") and environment["location"] == "unknown":
        environment["location"] = s(meta_env["location"])
    scene["environment"] = environment
    scene["speakers"] = {name: len(lines) for name, lines in speakers.items()}
    scene["speaker_lines"] = speakers
    scene["stage_directions"] = stage_directions
    scene["facts"] = []
    scene["facts"].append("Scene heading: %s" % heading)
    if speakers:
        scene["facts"].append("Speakers: " + ", ".join(sorted(speakers)))
    for direction in stage_directions:
        scene["facts"].append("Stage direction: %s" % direction)
    for label in environment["weather"]:
        scene["facts"].append("Environment (script): weather=%s" % label)
    for label in environment["time"]:
        scene["facts"].append("Environment (script): time=%s" % label)
    # state only from explicit words; otherwise unknown (never invent)
    state = {"wetness": "unknown", "damage": "unknown", "dirt": "unknown"}
    if any(has_word(full_text, word) for word in STATE_RAIN):
        state["wetness"] = "wet"
    if any(has_word(full_text, word) for word in STATE_DAMAGE):
        state["damage"] = "present"
    if any(has_word(full_text, word) for word in STATE_DIRT):
        state["dirt"] = "present"
    scene["state"] = state
    return scene


# ---------------------------------------------------------------------------
# meta / characters / stages
# ---------------------------------------------------------------------------
def normalise_character(item):
    if isinstance(item, str):
        item = {"name": item}
    if not isinstance(item, dict):
        return None
    name = s(item.get("name") or item.get("character_name"))
    if is_unknown(name):
        return None
    return {
        "name": name,
        "aliases": [s(a) for a in as_list(item.get("aliases")) if not is_unknown(a)],
        "occupation": s(item.get("occupation")),
        "economic_status": s(item.get("economic_status") or item.get("class")),
        "arc": s(item.get("arc") or item.get("character_arc")),
        "relationships": as_list(item.get("relationships")),
        "notes": s(item.get("notes") or "", default=""),
        "meta": item,
    }


def load_meta(path):
    if not path:
        return {}
    meta = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(meta, dict):
        raise ValueError("meta JSON must be an object")
    return meta


def build_characters(scenes, meta):
    characters = []
    meta_characters = meta.get("characters") or []
    if isinstance(meta_characters, dict):
        meta_characters = [dict(value, name=key) if isinstance(value, dict) else key
                           for key, value in meta_characters.items()]
    for item in meta_characters:
        character = normalise_character(item)
        if character:
            characters.append(character)
    # speakers detected in the script are script facts; add them (fields unknown)
    detected = []
    for scene in scenes:
        for name in scene["speakers"]:
            if not any(norm(name) == norm(c["name"]) or
                       norm(name) in [norm(a) for a in c["aliases"]]
                       for c in characters):
                detected.append(name)
    for name in lib.unique_ordered(detected):
        characters.append({
            "name": name, "aliases": [], "occupation": "unknown",
            "economic_status": "unknown", "arc": "unknown",
            "relationships": [], "notes": "",
            "meta": {}, "detected_only": True,
        })
    warnings = []
    for character in characters:
        present = []
        for scene in scenes:
            if norm(character["name"]) in [norm(n) for n in scene["speakers"]] or any(
                    norm(alias) in [norm(n) for n in scene["speakers"]]
                    for alias in character["aliases"]):
                present.append(scene["id"])
        character["present_scenes"] = present
        character["script_status"] = "present" if present else "not_in_excerpt"
        if character.get("detected_only"):
            warnings.append("character %r detected from script speakers but missing "
                            "from meta; occupation/class/arc stay unknown" %
                            character["name"])
        if not present:
            warnings.append("character %r is in meta but not detected in the "
                            "provided excerpt; dossier only, no looks" %
                            character["name"])
    return characters, warnings


def resolve_scene_ref(ref, scenes):
    """Resolve a meta stage scene reference to a parsed S-id.

    Supported forms (S-id compatibility first):
      S1, s1, S01
      1-3, 1.3, 1/3, 1_3          (act-scene)
      Act 1 Scene 3, act I scene iii, 1 scene 3
    """
    ref = str(ref or "").strip()
    if not ref:
        return None
    sid_match = re.fullmatch(r"[Ss]0*(\d+)", ref)
    if sid_match:
        sid = "S%d" % int(sid_match.group(1))
        return sid if any(scene["id"] == sid for scene in scenes) else None
    match = re.match(
        r"^\s*(?:act\s*)?([0-9]+|[ivxlcdm]+)\s*[,.;:/_ -]*\s*"
        r"(?:scene\s*)?([0-9]+|[ivxlcdm]+)\s*$", ref, re.IGNORECASE)
    if not match:
        return None
    act = roman_to_int(match.group(1))
    scene_no = roman_to_int(match.group(2))
    if act is None or scene_no is None:
        return None
    for scene in scenes:
        if scene.get("act_number") == act and scene.get("scene_number") == scene_no:
            return scene["id"]
    return None


def build_stages(scenes, meta):
    raw = meta.get("stages")
    stage_list = []
    if isinstance(raw, list) and raw:
        for index, item in enumerate(raw, 1):
            if isinstance(item, str):
                stage_list.append({"id": "stage-%d" % index, "label": item,
                                   "refs": [], "scenes": []})
            elif isinstance(item, dict):
                stage_list.append({
                    "id": s(item.get("id"), "stage-%d" % index),
                    "label": s(item.get("label") or item.get("name"), "stage %d" % index),
                    "refs": [str(x) for x in as_list(item.get("scenes")) if x],
                    "scenes": [],
                })
    if not stage_list:
        stage_list = [{"id": "whole", "label": "whole excerpt",
                       "refs": [scene["id"] for scene in scenes],
                       "scenes": [scene["id"] for scene in scenes]}]
    scene_ids = [scene["id"] for scene in scenes]
    mapping = {}
    warnings = []
    assigned = set()
    for stage in stage_list:
        resolved = []
        for ref in stage["refs"]:
            sid = resolve_scene_ref(ref, scenes)
            if sid:
                if sid not in resolved:
                    resolved.append(sid)
            else:
                warnings.append("stage %r scene ref %r could not be mapped to a parsed "
                                "S-id; supported forms are S1 or act-scene (1-3)" %
                                (stage["id"], ref))
        stage["scenes"] = resolved
        mapping[stage["id"]] = {"refs": stage["refs"], "scenes": resolved}
        assigned.update(resolved)
    unassigned = [sid for sid in scene_ids if sid not in assigned]
    if unassigned:
        stage_list.append({"id": "unassigned", "label": "unassigned scenes",
                           "refs": unassigned, "scenes": unassigned})
        mapping["unassigned"] = {"refs": unassigned, "scenes": unassigned}
        warnings.append("scenes %s are not referenced by any meta stage; they were "
                        "placed in an explicit 'unassigned' stage" % ", ".join(unassigned))
    return stage_list, mapping, warnings


def stage_for_scene(stage_list, scene_id):
    for stage in stage_list:
        if scene_id in stage["scenes"]:
            return stage
    return stage_list[-1]


def merged_stage_environment(scenes, stage, character, meta):
    stage_scenes = [scene for scene in scenes
                    if scene["id"] in stage["scenes"] and
                    scene["id"] in character.get("present_scenes", [])]
    if not stage_scenes:
        stage_scenes = [scene for scene in scenes if scene["id"] in stage["scenes"]]
    weather = []
    times = []
    actions = []
    locations = []
    for scene in stage_scenes:
        for value in scene["environment"]["weather"]:
            if value not in weather:
                weather.append(value)
        for value in scene["environment"]["time"]:
            if value not in times:
                times.append(value)
        for value in scene["environment"]["actions"]:
            if value not in actions:
                actions.append(value)
        if scene["environment"]["location"] != "unknown":
            if scene["environment"]["location"] not in locations:
                locations.append(scene["environment"]["location"])
    # explicit meta environment overrides/extends script facts
    if not weather and meta.get("weather"):
        weather = [s(meta["weather"])]
    if not times and meta.get("time"):
        times = [s(meta["time"])]
    if not actions and meta.get("action"):
        actions = [s(meta["action"])]
    if not locations and meta.get("location"):
        locations = [s(meta["location"])]
    state = {}
    for key in ("wetness", "damage", "dirt"):
        values = [scene["state"].get(key, "unknown") for scene in stage_scenes]
        explicit = [value for value in values if value != "unknown"]
        state[key] = explicit[0] if explicit else "unknown"
    return {
        "scene": "; ".join("%s: %s" % (scene["id"], scene["title"]) for scene in stage_scenes),
        "time": ", ".join(times) if times else "unknown",
        "weather": ", ".join(weather) if weather else "unknown",
        "action": ", ".join(actions) if actions else "unknown",
        "location": ", ".join(locations) if locations else "unknown",
        "state": state,
        "scenes": [scene["id"] for scene in stage_scenes],
    }


def character_needs(character, scenes, stages, meta):
    present = character.get("present_scenes", [])
    lines = 0
    for scene in scenes:
        lines += sum(count for name, count in scene["speakers"].items()
                     if norm(name) == norm(character["name"]))
    needs = {
        "identity": {
            "occupation": character["occupation"],
            "economic_status": character["economic_status"],
            "social_role_stated": character["notes"] or "unknown",
        },
        "arc": character["arc"],
        "relationships": character["relationships"] or ["unknown"],
        "function": ("appears in %s; speaks/acts in %d dialogue blocks" %
                     (", ".join(present) if present else "no scenes", lines)),
        "stages": [stage["label"] for stage in stages
                   if any(sid in stage["scenes"] for sid in present)],
        "unknown": [key for key in ("occupation", "economic_status", "arc")
                    if is_unknown(character[key])],
    }
    return needs


# ---------------------------------------------------------------------------
# real vault calls
# ---------------------------------------------------------------------------
def run_subprocess(args):
    proc = subprocess.run([sys.executable] + args, cwd=str(ROOT),
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def run_query(args):
    code, out, err = run_subprocess(["scripts/query.py"] + args)
    try:
        rows = json.loads(out)
    except json.JSONDecodeError:
        rows = []
    return code, rows if isinstance(rows, list) else [], err


def retrieve_for_stage(character, stage_env, meta):
    """Real query.py calls; returns records of hits (IDs verified against cards)."""
    calls = []
    query_terms = []
    period = meta.get("period")
    region = meta.get("region")
    occupation = character.get("occupation")
    art = meta.get("art_direction")
    weather = stage_env.get("weather")
    if not is_unknown(period):
        query_terms.append([s(period), "--limit", "8", "--json"])
    if not is_unknown(region):
        query_terms.append([s(region), "--limit", "6", "--json"])
    if not is_unknown(occupation):
        query_terms.append([s(occupation), "--limit", "6", "--json"])
    if not is_unknown(art):
        query_terms.append([s(art).split(",")[0], "--limit", "6", "--json"])
    if not is_unknown(weather):
        query_terms.append([s(weather).split(",")[0], "--type", "garment",
                            "--limit", "6", "--json"])
    if not query_terms:
        query_terms.append(["--type", "garment", "--limit", "8", "--json"])
    seen = set()
    hits = []
    for terms in query_terms:
        code, rows, err = run_query(terms)
        ids = [row.get("id") for row in rows if isinstance(row, dict)]
        calls.append({"args": terms, "exit": code, "hits": len(rows),
                      "ids": ids, "stderr": err.strip()[-300:]})
        for row in rows:
            rid = row.get("id")
            if rid and rid not in seen:
                seen.add(rid)
                hits.append(row)
    return {"calls": calls, "hits": hits}


def run_recommend(character, stage, stage_env, meta, out_dir):
    rec_input = {
        "character": {
            "name": character["name"],
            "occupation": character["occupation"],
            "economic_status": character["economic_status"],
            "arc": character["arc"],
        },
        "period": s(meta.get("period")),
        "region": s(meta.get("region")),
        "season": s(meta.get("season")),
        "scene": stage_env.get("scene") or s(meta.get("environment")),
        "time": stage_env.get("time") or s(meta.get("time")),
        "weather": stage_env.get("weather") or s(meta.get("weather")),
        "action": stage_env.get("action") or s(meta.get("action")),
        "location": stage_env.get("location") or s(meta.get("location")),
        "art_direction": s(meta.get("art_direction") or meta.get("dramatic_style")),
        "lighting": s(meta.get("lighting")),
        "camera": s(meta.get("camera"), "medium shot"),
        "budget": s(meta.get("budget"), "medium"),
        "fidelity_mode": s(meta.get("fidelity_mode"), "inspired"),
        "tool": s(meta.get("tool"), "generic"),
        "state": stage_env.get("state", {}),
        "notes": "workflow stage=%s; relationships=%s" % (
            stage["label"], ", ".join(character["relationships"]) or "unknown"),
    }
    input_dir = out_dir / "_inputs"
    input_dir.mkdir(parents=True, exist_ok=True)
    input_path = input_dir / ("%s_%s.json" % (
        slug(character["name"]), slug(stage["id"])))
    write_text(input_path, json.dumps(rec_input, ensure_ascii=False, indent=2))
    code, out, err = run_subprocess(["scripts/recommend.py", str(input_path), "--json"])
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        data = None
    return {
        "input_path": str(input_path.relative_to(ROOT)),
        "input": rec_input,
        "exit": code,
        "data": data,
        "stderr": err.strip()[-500:],
    }


# ---------------------------------------------------------------------------
# validation / checks / continuity
# ---------------------------------------------------------------------------
def card_inventory():
    cards, _ = lib.load_cards()
    by_id = {lib.get_str(card["meta"], "id"): card for card in cards}
    sources = {lib.get_str(card["meta"], "id"): card for card in cards
               if norm(card["meta"].get("type")) == "source"}
    return by_id, sources


def validate_recommendation(data, by_id, sources):
    issues = []
    evidence_complete = True
    source_ids = set()
    if not isinstance(data, dict):
        return {"valid": False, "issues": ["recommend.py produced no JSON"],
                "evidence_complete": False, "source_ids": []}
    looks = data.get("looks") or []
    if not looks:
        issues.append("no looks returned")
    for look in looks:
        label = look.get("look_ref", "?")
        for item in look.get("items", []):
            cid = item.get("id")
            if cid not in by_id:
                issues.append("fabricated/unknown card ID %s in Look %s" % (cid, label))
            for sid in item.get("source_ids") or []:
                source_ids.add(sid)
                if sid not in sources:
                    issues.append("unknown source ID %s on %s" % (sid, cid))
        evidence = look.get("evidence")
        if not isinstance(evidence, dict):
            evidence_complete = False
            issues.append("Look %s has no evidence object" % label)
            continue
        if "source_ids" not in evidence or "item_evidence" not in evidence:
            evidence_complete = False
            issues.append("Look %s evidence fields incomplete" % label)
        source_ids.update(evidence.get("source_ids") or [])
        if evidence.get("source_urls"):
            for entry in evidence["source_urls"]:
                if not str(entry.get("url", "")).startswith("http"):
                    issues.append("bad source URL %s" % entry)
        if evidence.get("missing_urls"):
            issues.append("Look %s has missing source URLs: %s" % (
                label, evidence["missing_urls"]))
    return {
        "valid": not issues,
        "issues": issues,
        "evidence_complete": evidence_complete,
        "source_ids": sorted(source_ids),
    }


def check_continuity(characters, stages, recommendations, scenes):
    plan = {}
    issues = []
    for character in characters:
        if not character.get("present_scenes"):
            continue
        character_stages = []
        for stage in stages:
            stage_scene_ids = [sid for sid in stage["scenes"]
                               if sid in character["present_scenes"]]
            if not stage_scene_ids:
                continue
            rec = recommendations.get(character["name"], {}).get(stage["id"])
            look_ids = []
            if rec and isinstance(rec.get("data"), dict):
                for look in rec["data"].get("looks", []):
                    look_ids.append([item.get("id") for item in look.get("items", [])])
            character_stages.append({
                "stage": stage["label"],
                "stage_id": stage["id"],
                "scenes": stage_scene_ids,
                "look_ids": look_ids,
            })
        if not character_stages:
            continue
        anchor_sets = [set(ids) for ids in
                       [entry["look_ids"][0] for entry in character_stages
                        if entry["look_ids"]]]
        anchors = sorted(set.intersection(*anchor_sets)) if anchor_sets else []
        if not anchors:
            issues.append("character %r has no single anchor item shared across "
                          "stages; stage wardrobe changes must be explicit" %
                          character["name"])
        states = []
        for scene_id in character["present_scenes"]:
            scene = next((scene for scene in scenes if scene["id"] == scene_id), None)
            if scene:
                states.append({"scene": scene_id, "state": scene["state"]})
        if any(value == "unknown" for scene in states for value in scene["state"].values()):
            issues.append("character %r continuity states contain unknown values "
                          "(not invented; mark for production review)" %
                          character["name"])
        plan[character["name"]] = {
            "stages": character_stages,
            "anchors": anchors,
            "scene_states": states,
            "issues": [issue for issue in issues
                       if character["name"] in issue or "character" not in issue],
        }
    return plan, issues


# ---------------------------------------------------------------------------
# markdown / csv rendering
# ---------------------------------------------------------------------------
def render_dossier(result):
    lines = ["# Character Dossier — %s" % result["title"], ""]
    lines.append("- Script: `%s`" % result["script_path"])
    if result.get("meta_path"):
        lines.append("- Meta: `%s`" % result["meta_path"])
    lines.append("- Mode: %s" % result["meta"].get("fidelity_mode", "unknown"))
    lines.append("")
    for character in result["characters"]:
        needs = result["needs"][character["name"]]
        lines.append("## %s" % character["name"])
        lines.append("")
        lines.append("- Script presence: %s" % (
            ", ".join(character["present_scenes"]) or "not in excerpt"))
        lines.append("- Occupation: %s" % needs["identity"]["occupation"])
        lines.append("- Economic status: %s" % needs["identity"]["economic_status"])
        lines.append("- Arc: %s" % needs["arc"])
        lines.append("- Relationships: %s" % ", ".join(needs["relationships"]))
        lines.append("- Function (script fact): %s" % needs["function"])
        lines.append("- Stages: %s" % ", ".join(needs["stages"]) or "none")
        if needs["unknown"]:
            lines.append("- **Unknown / not provided:** %s" % ", ".join(needs["unknown"]))
        lines.append("")
        lines.append("### Looks")
        lines.append("")
        rec_stages = result["recommendations"].get(character["name"], {})
        if not rec_stages:
            lines.append("_No recommendation run: character not present in excerpt._")
            lines.append("")
            continue
        lines.append("| Stage | A | B | C | Evidence tier |")
        lines.append("| --- | --- | --- | --- | --- |")
        for stage in result["stages"]:
            rec = rec_stages.get(stage["id"])
            if not rec or not isinstance(rec.get("data"), dict):
                continue
            looks = rec["data"].get("looks", [])
            cells = []
            for index in range(3):
                if index < len(looks):
                    cells.append("`%s` / %s" % (
                        looks[index].get("look_ref"),
                        ", ".join(item.get("id") for item in looks[index].get("items", []))))
                else:
                    cells.append("—")
            tier = looks[0].get("evidence_tier", "unknown") if looks else "none"
            lines.append("| %s | %s | %s | %s | %s |" % (
                stage["label"], cells[0], cells[1], cells[2], tier))
        lines.append("")
    return "\n".join(lines)


def render_scene_table_csv(result):
    rows = []
    for scene in result["scenes"]:
        present = [character["name"] for character in result["characters"]
                   if scene["id"] in character["present_scenes"]]
        for character in result["characters"]:
            if scene["id"] not in character["present_scenes"]:
                continue
            stage = stage_for_scene(result["stage_list"], scene["id"])
            rec = result["recommendations"].get(character["name"], {}).get(stage["id"])
            looks = rec["data"].get("looks", []) if rec and isinstance(rec.get("data"), dict) else []
            ids = []
            for look in looks:
                ids.append(";".join(item.get("id") for item in look.get("items", [])))
            while len(ids) < 3:
                ids.append("")
            state = scene["state"]
            rows.append({
                "scene_id": scene["id"],
                "scene_title": scene["title"],
                "characters_present": " / ".join(present) or "unknown",
                "character": character["name"],
                "stage": stage["label"],
                "look_A_ids": ids[0],
                "look_B_ids": ids[1],
                "look_C_ids": ids[2],
                "wetness": state.get("wetness", "unknown"),
                "damage": state.get("damage", "unknown"),
                "dirt": state.get("dirt", "unknown"),
                "evidence_tier": looks[0].get("evidence_tier", "none") if looks else "none",
            })
    return rows


def render_scene_table_md(result):
    lines = ["# Scene Costume Table — %s" % result["title"], ""]
    lines.append("| Scene | Character | Stage | A | B | C | State (wet/damage/dirt) |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    rows = render_scene_table_csv(result)
    for row in rows:
        lines.append("| %s — %s | %s | %s | %s | %s | %s | %s / %s / %s |" % (
            row["scene_id"], row["scene_title"][:40], row["character"],
            row["stage"], row["look_A_ids"] or "—", row["look_B_ids"] or "—",
            row["look_C_ids"] or "—", row["wetness"], row["damage"], row["dirt"]))
    lines.append("")
    return "\n".join(lines)


def render_full_looks(result):
    lines = ["# Full Looks — %s" % result["title"], ""]
    for character in result["characters"]:
        rec_stages = result["recommendations"].get(character["name"], {})
        if not rec_stages:
            continue
        lines.append("## %s" % character["name"])
        lines.append("")
        for stage in result["stages"]:
            rec = rec_stages.get(stage["id"])
            if not rec or not isinstance(rec.get("data"), dict):
                continue
            lines.append("### %s — %s" % (character["name"], stage["label"]))
            lines.append("")
            for look in rec["data"].get("looks", []):
                lines.append("#### Look %s — score %.1f/100" % (
                    look.get("look_ref"), look.get("total", 0)))
                lines.append("")
                lines.append("| Slot | ID | Name | Colors | Materials | Evidence | Sources |")
                lines.append("| --- | --- | --- | --- | --- | --- | --- |")
                for item in look.get("items", []):
                    lines.append("| %s | `%s` | %s | %s | %s | %s | %s |" % (
                        item.get("slot"), item.get("id"),
                        item.get("name_zh") or item.get("name_en"),
                        ", ".join(item.get("colors") or []),
                        ", ".join(item.get("materials") or []),
                        item.get("evidence_status"),
                        ", ".join(item.get("source_ids") or [])))
                if look.get("parts"):
                    lines.append("")
                    lines.append("- Structure cards: " + ", ".join(
                        "`%s`" % part.get("id") for part in look["parts"]))
                if look.get("materials"):
                    lines.append("- Material cards: " + ", ".join(
                        "`%s`" % material.get("id") for material in look["materials"]))
                lines.append("- Missing layers: %s" % (
                    ", ".join(look.get("missing") or []) or "none"))
                lines.append("- Narrative meaning: %s" % look.get("narrative_meaning", ""))
                for reason in look.get("reasons") or []:
                    lines.append("- Reason: %s" % reason)
                for risk in look.get("risks") or []:
                    lines.append("- Risk: %s" % risk)
                lines.append("")
    return "\n".join(lines)


def render_prompts(result):
    lines = ["# English Prompts — %s" % result["title"], ""]
    for character in result["characters"]:
        rec_stages = result["recommendations"].get(character["name"], {})
        if not rec_stages:
            continue
        lines.append("## %s" % character["name"])
        lines.append("")
        for stage in result["stages"]:
            rec = rec_stages.get(stage["id"])
            if not rec or not isinstance(rec.get("data"), dict):
                continue
            for look in rec["data"].get("looks", []):
                lines.append("### %s / %s / Look %s" % (
                    character["name"], stage["label"], look.get("look_ref")))
                lines.append("")
                lines.append("**Image prompt**")
                lines.append("")
                lines.append("```")
                lines.append(look.get("prompt_image_en") or look.get("prompt_image", ""))
                lines.append("```")
                lines.append("")
                lines.append("**Video prompt**")
                lines.append("")
                lines.append("```")
                lines.append(look.get("prompt_video_en") or look.get("prompt_video", ""))
                lines.append("```")
                lines.append("")
    return "\n".join(lines)


def render_continuity(result):
    lines = ["# Cross-scene Continuity Plan — %s" % result["title"], ""]
    lines.append("- State tokens are script/meta facts when stated; otherwise `unknown` "
                 "(never invented).")
    lines.append("- Anchor items are the intersection of A-look IDs across stages.")
    lines.append("")
    for character, plan in result["continuity"]["plan"].items():
        lines.append("## %s" % character)
        lines.append("")
        lines.append("- Anchor items: %s" % (", ".join(plan["anchors"]) or "none"))
        lines.append("")
        lines.append("| Stage | Scenes | Look A items |")
        lines.append("| --- | --- | --- |")
        for stage in plan["stages"]:
            lines.append("| %s | %s | %s |" % (
                stage["stage"], ", ".join(stage["scenes"]),
                ", ".join(stage["look_ids"][0]) if stage["look_ids"] else "—"))
        lines.append("")
        lines.append("| Scene | Wetness | Damage | Dirt |")
        lines.append("| --- | --- | --- | --- |")
        for state in plan["scene_states"]:
            lines.append("| %s | %s | %s | %s |" % (
                state["scene"], state["state"].get("wetness"),
                state["state"].get("damage"), state["state"].get("dirt")))
        lines.append("")
        for issue in plan["issues"]:
            lines.append("- Continuity note: %s" % issue)
        lines.append("")
    for issue in result["continuity"]["issues"]:
        lines.append("- Global continuity note: %s" % issue)
    lines.append("")
    return "\n".join(lines)


def render_fact_evidence(result):
    lines = ["# Facts / Evidence / Inference — %s" % result["title"], ""]
    lines.append("## 1. Facts (script / meta; no invented claims)")
    lines.append("")
    for scene in result["scenes"]:
        lines.append("### %s — %s" % (scene["id"], scene["title"]))
        for fact in scene["facts"]:
            lines.append("- %s" % fact)
        if scene["speakers"]:
            lines.append("- Dialogue blocks per speaker: %s" % ", ".join(
                "%s=%d" % (name, count) for name, count in scene["speakers"].items()))
        lines.append("")
    lines.append("## 2. Evidence (real card IDs + source IDs only)")
    lines.append("")
    lines.append("| Character | Stage | Evidence tier | Item IDs | Source IDs |")
    lines.append("| --- | --- | --- | --- | --- |")
    for character in result["characters"]:
        rec_stages = result["recommendations"].get(character["name"], {})
        for stage in result["stages"]:
            rec = rec_stages.get(stage["id"])
            if not rec or not isinstance(rec.get("data"), dict):
                continue
            looks = rec["data"].get("looks", [])
            if not looks:
                continue
            items = [item.get("id") for look in looks for item in look.get("items", [])]
            sources = []
            for look in looks:
                sources.extend((look.get("evidence") or {}).get("source_ids") or [])
            lines.append("| %s | %s | %s | %s | %s |" % (
                character["name"], stage["label"], looks[0].get("evidence_tier"),
                ", ".join(lib.unique_ordered(items)),
                ", ".join(lib.unique_ordered(sources)) or "(none)"))
    lines.append("")
    lines.append("### Evidence status notes")
    lines.append("")
    for note in result["evidence"]["notes"]:
        lines.append("- %s" % note)
    lines.append("")
    lines.append("## 3. Inference (directorial/design interpretation, not clothing history)")
    lines.append("")
    for character in result["characters"]:
        rec_stages = result["recommendations"].get(character["name"], {})
        for stage in result["stages"]:
            rec = rec_stages.get(stage["id"])
            if not rec or not isinstance(rec.get("data"), dict):
                continue
            for look in rec["data"].get("looks", []):
                lines.append("- %s / %s / Look %s: %s" % (
                    character["name"], stage["label"], look.get("look_ref"),
                    look.get("narrative_meaning", "no narrative note")))
    lines.append("")
    lines.append("## 3b. Design conflicts / risks (from recommend.py)")
    lines.append("")
    if result.get("design_conflicts"):
        for conflict in result["design_conflicts"]:
            lines.append("- %s" % conflict)
    else:
        lines.append("- none reported")
    lines.append("")
    lines.append("## 4. Unknowns / gaps (not invented)")
    lines.append("")
    for item in result["unknowns"]:
        lines.append("- %s" % item)
    for warning in result["warnings"]:
        lines.append("- Warning: %s" % warning)
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def run_workflow(script_path, meta_path, out_dir):
    script_file = Path(script_path)
    if not script_file.exists():
        raise FileNotFoundError("script not found: %s" % script_path)
    text = script_file.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("script is empty")
    meta = load_meta(meta_path) if meta_path else {}
    scenes = split_scenes(text)
    # First parse with meta characters to detect speakers, then build the full
    # character list (meta + script-detected), then re-parse to resolve aliases.
    provisional = []
    for item in meta.get("characters") or []:
        character = normalise_character(item)
        if character:
            provisional.append(character)
    for scene in scenes:
        parse_scene(scene, provisional, meta)
    characters, character_warnings = build_characters(scenes, meta)
    for scene in scenes:
        parse_scene(scene, characters, meta)
    # explicit scene states from meta are facts; they override script-derived state
    scene_states = meta.get("scene_states") if isinstance(meta.get("scene_states"), dict) else {}
    for scene in scenes:
        override = scene_states.get(scene["id"])
        if isinstance(override, dict):
            for key in ("wetness", "damage", "dirt"):
                if override.get(key):
                    scene["state"][key] = s(override[key])
    if not characters:
        return {
            "title": s(meta.get("title"), script_file.stem),
            "meta": meta, "stage_list": [], "stage_mapping": {}, "retrieval": {},
            "recommendations": {}, "evidence": {"notes": [], "checks": {},
                                                "source_ids": []},
            "continuity": {"plan": {}, "issues": []},
            "script_path": str(script_file),
            "meta_path": str(meta_path) if meta_path else None,
            "scenes": [], "characters": [], "needs": {}, "stages": [],
            "stage_list": [], "recommendations": {}, "retrieval": {},
            "evidence": {"notes": [], "checks": {}}, "continuity": {"plan": {}, "issues": []},
            "warnings": character_warnings + ["no characters detected in script/meta"],
            "unknowns": ["characters"], "checks": {"characters": False},
        }
    stage_list, stage_mapping, stage_warnings = build_stages(scenes, meta)
    by_id, sources = card_inventory()
    recommendations = {}
    retrieval = {}
    warnings = list(character_warnings) + stage_warnings
    design_conflicts = []
    unknowns = []
    for character in characters:
        recommendations[character["name"]] = {}
        if not character["present_scenes"]:
            continue
        for stage in stage_list:
            stage_scene_ids = [sid for sid in stage["scenes"]
                               if sid in character["present_scenes"]]
            if not stage_scene_ids:
                continue
            stage_env = merged_stage_environment(scenes, stage, character, meta)
            retrieval[character["name"] + "/" + stage["id"]] = {
                "queries": retrieve_for_stage(character, stage_env, meta)["calls"],
                "kinds": [],
            }
            rec = run_recommend(character, stage, stage_env, meta, out_dir)
            recommendations[character["name"]][stage["id"]] = rec
            if isinstance(rec.get("data"), dict):
                for warning in rec["data"].get("warnings") or []:
                    design_conflicts.append("%s/%s: %s" % (
                        character["name"], stage["id"], warning))
                for conflict in rec["data"].get("conflicts") or []:
                    design_conflicts.append("%s/%s conflict: %s" % (
                        character["name"], stage["id"], conflict))
            if rec["exit"] not in (0, 3):
                warnings.append("recommend.py failed for %s/%s with exit %s" %
                                (character["name"], stage["id"], rec["exit"]))
            if rec["exit"] == 3 or not (isinstance(rec.get("data"), dict) and
                                        rec["data"].get("looks")):
                warnings.append("no wardrobe looks for %s/%s (knowledge-base gap)" %
                                (character["name"], stage["id"]))
    # English prompt fields + ABC distinctness (for outputs/tests)
    abc_distinct = True
    for character_name, stage_map in recommendations.items():
        for stage_id, rec in stage_map.items():
            if not isinstance(rec.get("data"), dict):
                continue
            looks = rec["data"].get("looks") or []
            for look in looks:
                look["prompt_image_en"] = english_only(look.get("prompt_image", ""))
                look["prompt_video_en"] = english_only(look.get("prompt_video", ""))
            if len(looks) >= 3:
                sets = [set(item.get("id") for item in look.get("items", []))
                        for look in looks[:3]]
                if sets[0] == sets[1] or sets[0] == sets[2] or sets[1] == sets[2]:
                    abc_distinct = False
    checks_abc = abc_distinct
    # evidence checks
    evidence_notes = []
    checks_ok = True
    all_source_ids = set()
    evidence_checks = {}
    for character in characters:
        for stage in stage_list:
            rec = recommendations.get(character["name"], {}).get(stage["id"])
            if not rec or not isinstance(rec.get("data"), dict):
                continue
            validation = validate_recommendation(rec["data"], by_id, sources)
            evidence_checks[character["name"] + "/" + stage["id"]] = validation
            checks_ok = checks_ok and validation["valid"]
            all_source_ids.update(validation["source_ids"])
            if not validation["evidence_complete"]:
                evidence_notes.append("evidence fields incomplete for %s/%s" %
                                      (character["name"], stage["id"]))
            statuses = [item.get("evidence_status")
                        for look in rec["data"].get("looks", [])
                        for item in look.get("items", [])]
            if meta.get("fidelity_mode") == "historical" and "verified" not in statuses:
                evidence_notes.append("historical mode: no verified card for %s/%s" %
                                      (character["name"], stage["id"]))
    evidence_notes.append("Source IDs resolve via 04-来源 cards when present; "
                          "no images embedded.")
    # continuity
    continuity_plan, continuity_issues = check_continuity(
        characters, stage_list, recommendations, scenes)
    # unknown collection
    for key in ("period", "region", "culture", "art_direction", "lighting",
                "budget", "fidelity_mode", "weather", "season"):
        if is_unknown(meta.get(key)):
            unknowns.append("%s: unknown (not provided in meta/script)" % key)
    for character in characters:
        for key in ("occupation", "economic_status", "arc"):
            if is_unknown(character[key]):
                unknowns.append("%s.%s: unknown" % (character["name"], key))
    for scene in scenes:
        for key in ("wetness", "damage", "dirt"):
            if scene["state"].get(key) == "unknown":
                unknowns.append("%s.state.%s: unknown (not stated in script/meta)" %
                                (scene["id"], key))
    # build result
    title = s(meta.get("title"), script_file.stem)
    result = {
        "title": title,
        "script_path": str(script_file),
        "meta_path": str(meta_path) if meta_path else None,
        "meta": meta,
        "scenes": scenes,
        "characters": characters,
        "needs": {character["name"]: character_needs(character, scenes, stage_list, meta)
                  for character in characters},
        "stage_list": stage_list,
        "stage_mapping": stage_mapping,
        "stages": stage_list,
        "recommendations": recommendations,
        "retrieval": retrieval,
        "evidence": {"notes": evidence_notes, "checks": evidence_checks,
                     "source_ids": sorted(all_source_ids)},
        "continuity": {"plan": continuity_plan, "issues": continuity_issues},
        "warnings": lib.unique_ordered(warnings),
        "design_conflicts": lib.unique_ordered(design_conflicts),
        "unknowns": lib.unique_ordered(unknowns),
        "checks": {
            "characters_present": [character["name"] for character in characters
                                   if character["present_scenes"]],
            "looks_produced": any(
                rec and isinstance(rec.get("data"), dict) and rec["data"].get("looks")
                for stages in recommendations.values() for rec in stages.values()),
            "ids_exist": checks_ok,
            "evidence_complete": all(
                check["evidence_complete"] for check in evidence_checks.values()),
            "source_ids_resolve": all(
                not check["issues"] for check in evidence_checks.values()),
            "abc_distinct": checks_abc,
            "scenes": len(scenes),
            "continuity_issues": len(continuity_issues),
        },
    }
    return result


def write_outputs(result, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    write_text(out_dir / "character-dossier.md", render_dossier(result))
    write_text(out_dir / "scene-costume-table.md", render_scene_table_md(result))
    rows = render_scene_table_csv(result)
    with (out_dir / "scene-costume-table.csv").open("w", encoding="utf-8",
                                                    newline="") as handle:
        if rows:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    write_text(out_dir / "full-looks.md", render_full_looks(result))
    write_text(out_dir / "prompts.md", render_prompts(result))
    write_text(out_dir / "continuity-plan.md", render_continuity(result))
    write_text(out_dir / "fact-evidence-inference.md", render_fact_evidence(result))
    serializable = json.loads(json.dumps(result, ensure_ascii=False, default=str))
    write_text(out_dir / "workflow-result.json",
               json.dumps(serializable, ensure_ascii=False, indent=2))
    return out_dir


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Script-driven Costume Director workflow (offline, real KB).")
    parser.add_argument("--script", required=True,
                        help="plain text / Markdown script or single scene")
    parser.add_argument("--meta", help="optional JSON with characters, period, region, "
                                      "style, environment, budget, stages, ...")
    parser.add_argument("--out", help="output directory (default under 11-验收/P3.5/workflow-runs)")
    parser.add_argument("--json", action="store_true",
                        help="print the machine-readable result JSON to stdout")
    args = parser.parse_args(argv)

    script_path = Path(args.script)
    if not script_path.exists():
        print("ERROR: script not found: %s" % args.script, file=sys.stderr)
        return 2
    if args.meta and not Path(args.meta).exists():
        print("ERROR: meta JSON not found: %s" % args.meta, file=sys.stderr)
        return 2
    try:
        if args.meta:
            load_meta(args.meta)
    except json.JSONDecodeError as exc:
        print("ERROR: invalid meta JSON: %s" % exc, file=sys.stderr)
        return 2
    except ValueError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    if not args.script or not Path(args.script).read_text(encoding="utf-8").strip():
        print("ERROR: script is empty", file=sys.stderr)
        return 2
    out_dir = Path(args.out) if args.out else (
        DEFAULT_OUT_ROOT / slug(script_path.stem))
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir = out_dir.expanduser()
    # D3: never write outside the vault.  This is checked before any KB call
    # or directory creation, so a rejected --out leaves no partial files.
    try:
        out_dir.resolve().relative_to(ROOT.resolve())
    except ValueError:
        print("ERROR: --out must be inside the vault (%s); refusing to write "
              "outside. No files were created." % ROOT, file=sys.stderr)
        return 2
    try:
        result = run_workflow(args.script, args.meta, out_dir)
    except FileNotFoundError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    except ValueError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    produced = bool(result.get("checks", {}).get("looks_produced"))
    result["exit_code"] = 0 if produced else 3
    write_outputs(result, out_dir)
    if args.json:
        print(json.dumps(json.loads(json.dumps(result, ensure_ascii=False, default=str)),
                         ensure_ascii=False, indent=2))
    else:
        print("wrote workflow outputs to %s" % out_dir.relative_to(ROOT))
        print("scenes=%d characters=%d looks=%s warnings=%d" % (
            len(result["scenes"]), len(result["characters"]),
            "yes" if produced else "no", len(result["warnings"])))
        if not produced:
            print("ERROR: no usable looks were produced; see workflow-result.json "
                  "warnings and knowledge-base gaps.", file=sys.stderr)
    return 0 if produced else 3


if __name__ == "__main__":
    sys.exit(main())
