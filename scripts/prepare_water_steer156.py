from pathlib import Path
import hashlib,json
from analyze_river120_v2 import machine
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 report=R/'qa/reports/water156_air_steer_model.json';inp=R/'config/water_first_hazard_steer156.json';plan=R/'work/water156/run_plan.json'
 assert not report.exists()and not inp.exists()and not plan.exists()
 ps=[R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'];roms=[p.read_bytes()for p in ps]
 assert sha(ps[0])=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'and sha(ps[1])=='31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa'
 assert roms[0][0x12759:0x12789]==roms[1][0x32759:0x32789]
 fixture=R/'qa/dialogue/water155_firsthazard049/frame_02892_ram.bin';base=fixture.read_bytes();env=json.loads((fixture.parent/'environment.json').read_text('utf-8'));assert sha(fixture)==env['files'][fixture.name]
 cases=[]
 for boat in [0,260,0xfefc]:
  for held in [0,0x80,1,0x81,2,0x82,3,0x83]:
   pair=[]
   for rom in roms:
    m,c=machine(rom);m.ram[:2048]=base;m.ram[0x52]=held;m.ram[0x4e1]=boat&255;m.ram[0x4f1]=boat>>8;m.ram[0x4e0]=m.ram[0x4f0]=0;c.pc=0xa749;c.p=0x30
    trace=[]
    while c.pc!=0xa779:trace.append(c.pc);c.step();assert len(trace)<100
    pair.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram)))
   assert pair[0]==pair[1]
   expected=0 if held&3==0 else (boat+(-192 if held&2 else 192))&65535
   actual=pair[0][-1][0x4e0]+256*pair[0][-1][0x4f0];assert actual==expected
   cases.append({'boat_velocity':boat,'held':held,'player_velocity':actual,'model_cycles':pair[0][-2]})
 report.write_text(json.dumps({'work':156,'status':'PASS_BOUNDED_AIR_STEERING_MODEL','source_sha256':sha(ps[0]),'ROM_sha256':sha(ps[1]),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'fixture':fixture.relative_to(R).as_posix(),'fixture_sha256':sha(fixture),'CPU_case_pairs':cases,'finding':'Held right updates playerVx=boatVx+192/256; left=boatVx-192/256; no horizontal input preserves prior zero velocity. At observed boat260, right produces452 (1.765625px/frame), allowing player to follow boat during jump.','limits':['Named native A749..A779 D-clear CPU arithmetic only; asynchronous physics, full landing and natural clear pending','No model or emulator coordinate/RAM/ROM intervention']},ensure_ascii=False,indent=2)+'\n','utf-8')
 seq=json.loads((R/'config/water_first_hazard_jump155.json').read_text('utf-8'));seq.append({'frame':2890,'duration':8,'button':'right'});inp.write_text(json.dumps(seq,indent=2)+'\n','utf-8')
 plan.parent.mkdir(parents=True,exist_ok=False)
 plan.write_text(json.dumps({'work':156,'input_sha256':sha(inp),'observer_sha256':sha(R/'scripts/trace_water_damage154.lua'),'model_report_sha256':sha(report),'command':'python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/water156_firsthazard_steer049 --frames 3300 --inputs config/water_first_hazard_steer156.json --script scripts/trace_water_damage154.lua','scope':'Only right8 added to known jump2890; native relative velocity grounded by24CPUcases, verify real avoidance/landing separately'},indent=2)+'\n','utf-8');print('PASS156 air steering24source/current CPU pairs')
if __name__=='__main__':main()
