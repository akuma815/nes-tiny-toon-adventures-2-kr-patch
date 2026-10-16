from pathlib import Path
import json
from seal_continuation159 import R,sha
def main():
 lua=R/'scripts/trace_water_fish_controller162.lua';plan=R/'work/water162/run_plan.json';assert not lua.exists()and not plan.exists()
 src=R/'scripts/trace_water_fish161.lua';s=src.read_text('utf-8')
 key='if r(0x420+i)==0x44 then';assert s.count(key)==1;s=s.replace(key,'if r(0x420+i)==0x44 or r(0x420+i)==0x34 and r(0x430+i)==2 then')
 key='local ay0,ay1=yp(ab[3])+avy*n,yp(ab[4])+avy*n;';assert s.count(key)==1
 s=s.replace(key,'local drop=r(0x420+i)==0x34 and 32/256*n*(n+1)/2 or 0\n    local ay0,ay1=yp(ab[3])+avy*n+drop,yp(ab[4])+avy*n+drop;')
 assert 'emu.write('not in s and 'loadSavestate'not in s
 lua.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':162,'base_sha256':sha(src),'observer_sha256':sha(lua),'gravity_evidence_sha256':sha(R/'qa/reports/water161_fish_validation.json'),'frames':10500,'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water162_fish_prediction049 --frames 10500 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_fish_controller162.lua','scope':'Controller-only prediction extends actualtype34/state2 with native32 gravity per future step. Assumption futurestep/video-frame and constant raft velocity is hypothesis. First-transfer160 mechanism retained. Actual success not presumed.'},indent=2)+'\n','utf-8');print('PASS162 native-gravity evidence pinned; no RAM/ROM writes')
if __name__=='__main__':main()
