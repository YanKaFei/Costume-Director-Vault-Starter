#!/usr/bin/env python3
"""quality_eval_audit.py - reproducible P3 audit probes (verifier, task-14).

AUDIT helper, NOT an acceptance gate: exit 0 only means probes ran, not that
quality is good. Results feed reports/P3-QA.md / P3-DEFECTS.md.

Sections
--------
1. regression  : F1 historical 1940s-1970s crash probe (expect exit 0 + 3 looks);
                 F2 1580s-Italy and Byzantine no-false-negative probe;
                 F3 six uncovered-topic probes (expect warnings, not silence).
2. query       : 25 fixed probes + 6 uncovered-topic probes (--limit 5 --json).
3. cases       : 15 semantic cases = 10 P2.5 C cases + 5 built-in new cases
                 (ER nurse / Mars technician / Ghana wedding groom /
                  identity descent / 1920s+cyberpunk conflict).
4. urls        : optional --urls: curl each SRC-0400..0431 URL (HTTP status).

Usage:
    python3 scripts/quality_eval_audit.py --quick     # regression probes only
    python3 scripts/quality_eval_audit.py             # regression + query + cases
    python3 scripts/quality_eval_audit.py --urls      # also check new source URLs
    ... --json /tmp/out.json
"""
import argparse, glob, json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
CASES_DIR = os.path.join(ROOT, "11-验收/P2.5-案例/inputs")
NEW_CASES = {
 "N1_ER_trauma_nurse.json": {
  "_case": {"id":"N1","title":"ER trauma nurse (occupational gap)","mode":"standard"},
  "character": {"name":"Zhou Min","occupation":"急诊创伤抢救区护士","economic_status":"working class","arc":"night shift"},
  "period":"contemporary","region":"urban china shanghai","season":"autumn",
  "scene":"trauma bay","time":"03:10 night","weather":"indoor, rain outside",
  "action":"gloves on, moving fast, lifting stretcher",
  "location":"hospital trauma bay","art_direction":"handheld documentary, cool fluorescent",
  "lighting":"cool fluorescent","camera":"handheld","budget":"low",
  "fidelity_mode":"inspired","tool":"midjourney",
  "state":{"wetness":"dry","damage":"none","dirt":"blood"}},
 "N2_mars_technician.json": {
  "_case": {"id":"N2","title":"Mars colony technician (future base gap)","mode":"standard"},
  "character": {"name":"Kai","occupation":"Mars colony technician","economic_status":"unknown","arc":"repair life support"},
  "period":"fictional","region":"fictional_world","season":"all_season",
  "scene":"Mars airlock","time":"day","weather":"dust storm outside",
  "action":"exoskeleton, valves, filters","location":"Mars colony",
  "art_direction":"hard sci-fi industrial","lighting":"red ambient","camera":"wide",
  "budget":"medium","fidelity_mode":"fictional","tool":"midjourney",
  "state":{"wetness":"dry","damage":"slight","dirt":"red dust"}},
 "N3_ghana_uk_wedding_groom.json": {
  "_case": {"id":"N3","title":"Ghana-UK wedding groom (cross-cultural)","mode":"standard"},
  "character": {"name":"Kofi","occupation":"architect","economic_status":"middle","arc":"between traditions"},
  "period":"contemporary","region":"ghana, united_kingdom","season":"summer",
  "scene":"family wedding rite, Accra","time":"afternoon","weather":"hot dry",
  "action":"rite, toasts, photos","location":"family courtyard",
  "art_direction":"documentary wedding, saturated cloth","lighting":"warm sun",
  "camera":"medium","budget":"medium","fidelity_mode":"inspired","tool":"midjourney",
  "state":{"wetness":"dry","damage":"none","dirt":"none"}},
 "N4_identity_descent.json": {
  "_case": {"id":"N4","title":"1920s socialite to 1930s factory worker","mode":"continuity"},
  "character": {"name":"Clara","occupation":"socialite then factory worker","economic_status":"wealthy to destitute","arc":"descent"},
  "period":"1920s, 1930s","region":"united_states","season":"autumn",
  "art_direction":"period drama, art deco to documentary","lighting":"warm ballroom to cold factory",
  "camera":"medium","budget":"medium","fidelity_mode":"historical","tool":"sora",
  "scenes":[
    {"scene_id":"S1","story_day":1,"time":"night","weather":"indoor","action":"jazz club dancing","scene":"jazz club","state":{"wetness":"dry","damage":"none","dirt":"none"}},
    {"scene_id":"S2","story_day":400,"time":"morning","weather":"cold","action":"factory assembly line","scene":"factory floor","state":{"wetness":"dry","damage":"slight","dirt":"oil"}},
    {"scene_id":"S3","story_day":401,"time":"evening","weather":"rain","action":"breadline queue","scene":"breadline","state":{"wetness":"wet","damage":"worn","dirt":"mud"}}]},
 "N5_historical_cyberpunk_conflict.json": {
  "_case": {"id":"N5","title":"1920s Shanghai + cyberpunk prosthetics (conflict)","mode":"standard"},
  "character": {"name":"Gu Si","occupation":"dock worker, body-modded","economic_status":"low","arc":"survive"},
  "period":"1920s","region":"shanghai","season":"winter",
  "scene":"neon wharf at night","time":"night","weather":"rain",
  "action":"climb crates, grab cable","location":"wharf shanghai",
  "art_direction":"historical base + cyberpunk neon, prosthetics","lighting":"magenta cyan neon",
  "camera":"wide and close","budget":"high","fidelity_mode":"historical","tool":"midjourney",
  "state":{"wetness":"wet","damage":"none","dirt":"none"}},
}
CRASH_PERIODS = ["1940s", "1950s", "1960s", "1970s"]
CRASH_TEMPLATE = json.loads(json.dumps(NEW_CASES["N5_historical_cyberpunk_conflict.json"]))
CRASH_TEMPLATE.update({"period": "1970s", "region": "london", "season": "autumn",
                       "fidelity_mode": "historical"})
CRASH_TEMPLATE["scene"] = {"scene_id": "S1", "time": "night", "weather": "dry",
                           "action": "walking", "location": "london club"}
UNCOVERED = {
 "I1_1930s_mens_shoes": {"occupation":"male bank clerk","period":"1930s","region":"shanghai","scene":"street"},
 "I2_byzantine_court": {"occupation":"byzantine courtier","period":"late_byzantine_empire","region":"byzantine_empire","scene":"palace"},
 "I3_west_africa_ritual": {"occupation":"ritual dancer","period":"19th_century","region":"west_africa","scene":"masquerade"},
 "I4_spacesuit": {"occupation":"astronaut","period":"fictional","region":"fictional_world","scene":"orbit","fidelity_mode":"fictional"},
 "I5_1990s_hiphop": {"occupation":"rapper","period":"1990s","region":"united_states","scene":"street"},
 "I6_1930s_raincoat": {"occupation":"detective","period":"1930s","region":"britain","scene":"rainy street"},
}
QUERY_PROBES = [
 ("P01",["旗袍"]),("P02",["和服"]),("P03",["风衣"]),("P04",["蕾丝"]),("P05",["朋克"]),
 ("P06",["徽章"]),("P07",["1930s","上海"]),("P08",["立领","盘扣"]),("P09",["蕾丝","晚装"]),
 ("P10",["丝绸","和服"]),("P11",["--phrase","stand-up collar"]),("P12",["--phrase","right side fastening"]),
 ("P13",["--type","garment","--category","footwear"]),("P14",["--style-tag","noir"]),
 ("P15",["--period","1930s","--region","shanghai"]),("P16",["--type","source","--evidence","verified"]),
 ("P17",["--type","look"]),("P18",["--category","accessory"]),("P19",["--type","garment","--category","outerwear"]),
 ("P20",["spacesuit"]),("P21",["Mughal"]),("P22",["mourning","jewelry"]),("P23",["--match","any","旗袍","太空服"]),
 ("P24",["--type","pattern"]),("P25",["雨","夜","调查"]),
 ("Q26",["1930s","男鞋"]),("Q27",["拜占庭","宫廷"]),("Q28",["非洲","仪式"]),("Q29",["太空站"]),("Q30",["1970s","朋克"]),("Q31",["1930s","雨衣"]),
]

def run(cmd, timeout=60):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)

def recommend(path, tmpdir=None):
    p = run([PY, "scripts/recommend.py", path, "--json"])
    rec = None
    try: rec = json.loads(p.stdout)
    except Exception: pass
    return {"exit": p.returncode, "looks": len((rec or {}).get("looks") or []),
            "warnings": len((rec or {}).get("warnings") or []),
            "example_in_A": any("EXAMPLE" in it["id"] for it in ((rec or {}).get("looks") or [{}])[0].get("items", [])) if (rec or {}).get("looks") else None,
            "err": (p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "")}

def regression():
    rows = {}
    tmp = tempfile.mkdtemp(prefix="p3audit_")
    for period in CRASH_PERIODS:
        payload = json.loads(json.dumps(CRASH_TEMPLATE)); payload["period"] = period
        path = os.path.join(tmp, "hist_%s.json" % period)
        json.dump(payload, open(path, "w"), ensure_ascii=False)
        rows["F1_%s" % period] = recommend(path)
    rows["F2_1580s"] = recommend(os.path.join(ROOT, "11-验收/测试输入/T23-1580s意大利宫廷舞者-历史.json"))
    rows["F2_byzantine"] = recommend(os.path.join(ROOT, "11-验收/测试输入/T24-拜占庭帝国晚期宫廷-历史.json"))
    for name, base in UNCOVERED.items():
        payload = {
          "_case": {"id": name},
          "character": {"name": "A", "occupation": base["occupation"], "economic_status": "middle", "arc": "x"},
          "scene": {"scene_id": "S1", "time": "night", "weather": "rain", "action": "walking", "location": base["scene"]},
          "period": base["period"], "region": base["region"], "season": "autumn",
          "art_direction": "realist", "lighting": "cool", "camera": "medium", "budget": "medium",
          "fidelity_mode": base.get("fidelity_mode", "historical"), "tool": "midjourney",
          "state": {"wetness": "dry", "damage": "none", "dirt": "none"}}
        path = os.path.join(tmp, name + ".json"); json.dump(payload, open(path, "w"), ensure_ascii=False)
        rows[name] = recommend(path)
    return rows

def query_probes():
    out = []
    for pid, args in QUERY_PROBES:
        p = run([PY, "scripts/query.py"] + args + ["--limit", "5", "--json"])
        try: hits = json.loads(p.stdout)
        except Exception: hits = []
        out.append({"probe": pid, "exit": p.returncode, "n": len(hits), "ids": [h.get("id") for h in hits]})
    return out

def cases():
    out = {}
    files = sorted(glob.glob(os.path.join(CASES_DIR, "C*.json")))
    tmp = tempfile.mkdtemp(prefix="p3cases_")
    for name, payload in NEW_CASES.items():
        path = os.path.join(tmp, name); json.dump(payload, open(path, "w"), ensure_ascii=False)
        files.append(path)
    for path in files:
        out[os.path.basename(path)[:-5]] = recommend(path)
    return out

def new_source_urls():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "04-来源/SRC-04*.md"))):
        head = open(f, encoding="utf-8").read()
        import yaml
        meta = yaml.safe_load(head.split("---", 2)[1])
        if not isinstance(meta, dict) or meta.get("type") != "source":
            continue
        p = run(["curl", "-sS", "-m", "10", "-L", "-o", "/dev/null", "-w", "%{http_code}", meta.get("url")])
        out.append({"id": meta.get("id"), "status": p.stdout.strip(), "url": meta.get("url")})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--urls", action="store_true")
    ap.add_argument("--json", help="write JSON result to this path")
    args = ap.parse_args()
    result = {"regression": regression()}
    if not args.quick:
        result["query"] = query_probes()
        result["cases"] = cases()
    if args.urls:
        result["new_source_urls"] = new_source_urls()
    if args.json:
        json.dump(result, open(args.json, "w"), ensure_ascii=False, indent=1)
    for name, row in result["regression"].items():
        print("%-24s exit=%s looks=%s warnings=%s exampleA=%s %s" % (
            name, row["exit"], row["looks"], row["warnings"], row["example_in_A"], row["err"]))
    if "query" in result:
        for row in result["query"]:
            print("%s n=%d %s" % (row["probe"], row["n"], row["ids"]))
    if "cases" in result:
        for name, row in result["cases"].items():
            print("%-28s exit=%s looks=%s warnings=%s exampleA=%s" % (
                name, row["exit"], row["looks"], row["warnings"], row["example_in_A"]))
    if "new_source_urls" in result:
        bad = [r for r in result["new_source_urls"] if r["status"] != "200"]
        print("new source URLs: %d checked, %d non-200 %s" % (
            len(result["new_source_urls"]), len(bad), bad[:5]))
    print("NOTE: exit 0 = probes ran; quality must be judged via reports/P3-QA.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
