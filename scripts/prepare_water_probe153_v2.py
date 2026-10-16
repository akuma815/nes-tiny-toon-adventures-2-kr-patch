from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=R/'scripts/trace_water_progress153_v2.lua';assert not p.exists()
 old=R/'scripts/trace_water_progress153.lua';s=old.read_text('utf-8')
 fixes=["life,clear_count\n')","vertical_hi,vertical_lo\n')"]
 for x in fixes:assert s.count(x)==1;s=s.replace(x,x.replace('\n','\\n'))
 # Guard every short quoted literal against an accidental actual line break.
 for quote in ["'",'"']:
  opened=False;escaped=False
  for ch in s:
   if opened:
    assert ch not in '\r\n','Actual newline in short Lua literal'
    if escaped:escaped=False
    elif ch=='\\':escaped=True
    elif ch==quote:opened=False
   elif ch==quote:opened=True
  assert not opened
 p.write_text(s,'utf-8')
 verify=R/'scripts/verify_water_probe153_v2.py';assert not verify.exists()
 vs=(R/'scripts/verify_water_probe153.py').read_text('utf-8').replace("d=R/'qa/dialogue/water153_jump049'","d=R/'qa/dialogue/water153_jump049_v2'")
 verify.write_text(vs,'utf-8')
 d=R/'qa/dialogue/water153_jump049';env=json.loads((d/'environment.json').read_text('utf-8'))
 assert env['exit_code']==4294967295 and not list(d.glob('frame_*'))and not(d/'trace_complete.txt').exists()
 report=R/'qa/reports/water153_v1_observer_error.json';assert not report.exists()
 report.write_text(json.dumps({'work':153,'status':'OBSERVER_V1_PREEXECUTION_SYNTAX_ERROR','exit_code':env['exit_code'],'preserved_QA':d.relative_to(R).as_posix(),'frozen_environment_sha256':sha(d/'environment.json'),'v1_observer_sha256':sha(old),'v2_observer_sha256':sha(p),'cause':'Python non-raw triple string turned two CSV-header backslash-n sequences into actual newlines inside Lua short quoted strings. No emulator frames or native records produced.','fix':'Escape only these two line breaks in a new v2 observer; guard every short quoted literal before rerunning. Original capture/script/plan preserved.','claim':'Script failure, not ROM/gameplay failure'},ensure_ascii=False,indent=2)+'\n','utf-8')
 plan=R/'work/water153/run_plan_v2.json';assert not plan.exists()
 plan.write_text(json.dumps({'work':153,'revision':'v2','command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water153_jump049_v2 --frames 6000 --inputs config/water_jump_probe153.json --script scripts/trace_water_progress153_v2.lua','observer_sha256':sha(p),'input_sha256':sha(R/'config/water_jump_probe153.json'),'scope':'Same controller-only hypothesis; v1 observer syntax fixed, no evidence overwritten'},indent=2)+'\n','utf-8')
 print('PASS153 v2 Lua short-string newline guard')
if __name__=='__main__':main()
