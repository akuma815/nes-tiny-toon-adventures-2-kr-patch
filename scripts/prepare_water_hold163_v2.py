from pathlib import Path
import json
from analyze_river120_v2 import machine
from seal_continuation159 import R,sha
def main():
 lua=R/'scripts/trace_water_hold163.lua';report=R/'qa/reports/water163_hold_model.json';plan=R/'work/water163/run_plan.json';assert not lua.exists()and not report.exists()and not plan.exists()
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';roms=[p.read_bytes()for p in [sp,rp]]
 for a,b in [(0x12889,0x12899),(0x1f142,0x1f156)]:assert roms[0][a:b]==roms[1][a+0x20000:b+0x20000]
 fixture=R/'qa/dialogue/water162_fish_prediction049/frame_04890_ram.bin';base=fixture.read_bytes();env=json.loads((fixture.parent/'environment.json').read_text('utf-8'));assert sha(fixture)==env['files'][fixture.name]
 cases=[]
 for vy in [-1024,-1,0,127,1024]:
  for held in [0,128]:
   b=bytearray(base);b[0x52]=held;b[0x4c0]=vy&255;b[0x4d0]=(vy>>8)&255;pair=[]
   for data in roms:
    m,c=machine(data);m.ram[:2048]=b;c.pc=0xa779;n=0
    while c.pc!=0xa789:c.step();n+=1;assert n<30
    v=m.ram[0x4c0]+256*m.ram[0x4d0];expected=(vy+(48 if held else 80))&65535;assert v==expected
    pair.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram)))
   assert pair[0]==pair[1];cases.append({'Vy_before_signed':vy,'held_A':held!=0,'gravity_increment':48 if held else 80,'after_word':v,'cycles':pair[0][-2]})
 report.write_text(json.dumps({'work':163,'status':'PASS_NATIVE_HELD_A_GRAVITY','source_sha256':sha(sp),'ROM_sha256':sha(rp),'fixture_sha256':sha(fixture),'CPU_pairs':cases,'scope':'Native gravity per executed step; future trajectory/landing not proven by hold20 request'},indent=2)+'\n','utf-8')
 src=R/'scripts/trace_water_fish_controller162.lua';s=src.read_text('utf-8');key="untilA=frame+8;lastjump=frame;target=i;reason='predicted_actor'";assert s.count(key)==1
 s=s.replace(key,"untilA=frame+(r(0x420+i)==0x34 and 20 or 8);lastjump=frame;target=i;reason='predicted_actor'")
 assert 'emu.write('not in s and 'loadSavestate'not in s;lua.write_text(s,'utf-8');plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':163,'base_sha256':sha(src),'observer_sha256':sha(lua),'hold_model_sha256':sha(report),'frames':18000,'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water163_held_jump049 --frames 18000 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_hold163.lua','scope':'Onlytype34 predicted jump heldA20 instead8. Native gravity48vs80 verified10CPU pairs. Transfer/fixed/type44 inputs retained; no outcome assumed.'},indent=2)+'\n','utf-8');print('PASS163 10 source/current CPU pairs; native heldA gravity48 vs release80')
if __name__=='__main__':main()
