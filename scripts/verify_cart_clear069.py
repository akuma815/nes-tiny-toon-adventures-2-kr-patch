"""Native cart clearance branch/inline-pointer interpretation; offline CPU evidence only."""
from pathlib import Path
import json,hashlib,itertools
from verify_gate_font_tag_hooks import Memory,MPU
from py65.disassembler import Disassembler
R=Path(__file__).resolve().parents[1]
def run(blob,pc,stop,init):
 m=Memory(blob);m.banks=[0x38,0x39,0x3e,31]
 for a,v in init.items():m.ram[a]=v
 c=MPU(memory=m);c.pc=pc
 for _ in range(1000):
  if c.pc==stop:return m,c
  c.step()
 raise AssertionError(hex(c.pc))
def main():
 out=R/'qa/reports/cart_clear069_validation.json';assert not out.exists();blob=(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes').read_bytes();cases=0
 for types in itertools.product((0,1,0x2d,0x2e,0x2f),repeat=3):
  for state in (0,3,4,5):
   init={0x42d:types[0],0x42e:types[1],0x42f:types[2],0x430:state,0x550:7,0x56:0xfe,0x725:0xff}
   m,c=run(blob,0x9540,0x9561,init);clear=not any(types)and state!=5
   assert(m.ram[0x430],m.ram[0x550],m.ram[0x56],m.ram[0x725])==((5,0,0xff,0)if clear else(state,7,0xfe,0xff))
   for a in init:
    if a not in(0x430,0x550,0x56,0x725):assert m.ram[a]==init[a]
   cases+=1
 stage_cases=[]
 for level in(0,1,2):
  for command in(0,):
   m,c=run(blob,0x9d8f,0x9db4,{0x306:command,0x79:level,0x54:5,0x725:1,0x56:1})
   assert m.ram[0x79]==level+1 and m.ram[0x54]==(0x14 if level==2 else 0x0e)and m.ram[0x725]==m.ram[0x56]==0
   stage_cases.append({'level_before':level,'level_after':m.ram[0x79],'phase_after':m.ram[0x54]})
 for level in(0,1,2):
  for command in(0x80,0xac):
   init={0x306:command,0x79:level,0x54:5,0x725:1,0x56:1}
   m,c=run(blob,0x9d8f,0x9db5,init)
   assert all(m.ram[a]==v for a,v in init.items())
 # Pointer tables are data immediately after JSR CFC2, never linear instructions.
 m=Memory(blob);m.banks=[0x38,0x39,0x3e,31];d=Disassembler(MPU(memory=m))
 def ptrs(a,n):return[m[a+i*2]+256*m[a+i*2+1]for i in range(n)]
 mainptr=ptrs(0x9567,6);subptr=ptrs(0x9cd6,4);assert mainptr==[0x9587,0x95d4,0x95e9,0x9673,0x9b50,0x9cd0]and subptr==[0x9cde,0x9d3f,0x9d74,0x9d8f]
 rows=[]
 for start,end in((0x9540,0x9567),(0x9d8f,0x9db6)):
  pc=start
  while pc<end:
   n,s=d.instruction_at(pc);rows.append({'CPU':f'{pc:04X}','instruction':s});pc+=n
  assert pc==end
 p=R/'work/cart_clear_001/native_branch_and_tables.json';assert not p.exists();p.parent.mkdir(exist_ok=True);p.write_text(json.dumps({'rows':rows,'player_state_ptrs':[f'{x:04X}'for x in mainptr],'clear_substate_ptrs':[f'{x:04X}'for x in subptr]},indent=2)+'\n')
 report={'work':69,'status':'OFFLINE_NATIVE_CLEAR_BRANCH_PASS','ROM_SSOT_changes':0,'remaining_enemy_branch_cases':cases,'stage_transition_cases':stage_cases,'source_consumers':'Actual bank38/9540 types042D/E/F, state5->9CD0 four-substate inline dispatch;9D8F advances79 and phase0E or14','scope':'Offline unchanged native CPU execution. Actual game memory was not seeded. Type-read runtime evidence in68; all-zero/round-completion branches not yet natural runtime evidence.','limits':['No natural full cartclear/bonus/gold/history','No new emulator/direct visual/build/apply/PCM/listening/humanreview'],'next_action':'Generate source-derived per-level geometry and apply improved full-charge/intercept control, tracking actual native round progress.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
