#!/usr/bin/env python3
import json, re
from pathlib import Path
BASE=Path(__file__).resolve().parent
ID_RE=re.compile(r'\b(?:GAR|STR|MAT|STY|PRD|LOOK|SCN|SRC)-\d{3,4}\b')
def load(p):
 rows=[]
 if p.exists():
  for line in p.read_text(encoding='utf-8').splitlines():
   try:rows.append(json.loads(line))
   except:pass
 return rows
def validate(rows):
 calls=[r for r in rows if r.get('type')=='tool_call']; results=[r for r in rows if r.get('type')=='tool_result']
 skill=[r for r in calls if r.get('tool')=='skill']; tools=[]
 for r in calls:
  if r.get('tool')=='bash':
   cmd=json.dumps(r.get('input',{}),ensure_ascii=False)
   if any(x in cmd for x in ('visual_prompt.py','query.py','prompt_qa.py')):tools.append(r)
 completed=[r for r in results if r.get('status') in ('completed','success')]
 finals=[r.get('text','') for r in rows if r.get('type')=='final'];final=finals[-1] if finals else ''
 ends=[r for r in rows if r.get('type')=='status' and r.get('phase')=='turn_end']
 turn=bool(ends and (ends[-1].get('reason') or {}).get('kind')=='completed')
 ids=sorted(set(ID_RE.findall(final)))
 crit={'skill_call':bool(skill),'tools_executed':bool(tools and completed),'result_success':bool(completed),'turn_end_completed':turn,'complete_user_output':bool(len(final.strip())>=120 and len(ids)>=1)}
 no=('no image' in final.lower() or 'not generate' in final.lower() or 'text-only' in final.lower() or 'text prompt only' in final.lower())
 return {'criteria':crit,'ids':ids,'final_chars':len(final),'skill_calls':len(skill),'tool_calls':len(tools),'completed_tool_results':len(completed),'no_image_claim_ok':no,'pass':all(crit.values()),'final_preview':final[:400]}
def main():
 sets={'official':('RQ1','RQ2','RQ3'),'overlay':('RQ1','RQ4','RQ5')};out={}
 for mode,cases in sets.items():
  out[mode]={}
  for c in cases:
   v=validate(load(BASE/mode/(c+'.events.jsonl')));out[mode][c]=v
   (BASE/mode/(c+'.validation.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (BASE/'validation-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({m:{k:v['pass'] for k,v in cs.items()} for m,cs in out.items()},ensure_ascii=False,indent=2))
 return 0 if all(v['pass'] for cs in out.values() for v in cs.values()) else 1
if __name__=='__main__': raise SystemExit(main())
