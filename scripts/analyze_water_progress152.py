"""Bounded source/current CPU probes discriminate jumping, drowning and clear."""
from pathlib import Path
import hashlib,json
from analyze_river120_v2 import machine
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def execute(rom,ram,pc,stops):
 m,c=machine(rom);m.ram[:2048]=ram;c.pc=pc;c.p=0x30;c.x=0;c.y=0
 trace=[]
 while c.pc not in stops:
  trace.append(c.pc);c.step();assert len(trace)<2000,(hex(c.pc),len(trace))
 return (c.a,c.x,c.y,c.p,c.sp,c.pc,c.processorCycles,bytes(m.ram)),trace
def main():
 out=R/'qa/reports/water152_progress_model.json';assert not out.exists()
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
 src,rom=sp.read_bytes(),rp.read_bytes();assert sha(sp)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
 spans=[(0x12655,0x126ae),(0x12811,0x1283d),(0x12cef,0x12d68),(0x13883,0x139e0)]
 for a,b in spans:assert src[a:b]==rom[a+0x20000:b+0x20000]
 q=R/'qa/dialogue/world043_water_controller';e=json.loads((q/'environment.json').read_text('utf-8'))
 observations=[];refs={}
 for frame in range(2790,3001,30):
  p=q/f'frame_{frame:05d}_ram.bin';assert sha(p)==e['files'][p.name];b=p.read_bytes();refs[p.relative_to(R).as_posix()]=sha(p)
  observations.append({'snapshot':frame,'root':b[0x18],'phase':b[0x54],'player_state':b[0x430],'held_buttons_RAM52':b[0x52],'jump_flag_RAM99':b[0x99],'support_RAMC1':b[0xc1],'support_RAMC9':b[0xc9],'vertical_hi_RAM69':b[0x69],'vertical_lo_RAM6D':b[0x6d],'life_RAM7C0':b[0x7c0]})
 base=(R/'qa/dialogue/water143_native_049/frame_02790_ram.bin').read_bytes()
 be=json.loads((R/'qa/dialogue/water143_native_049/environment.json').read_text('utf-8'));assert hashlib.sha256(base).hexdigest()==be['files']['frame_02790_ram.bin']
 refs['qa/dialogue/water143_native_049/frame_02790_ram.bin']=hashlib.sha256(base).hexdigest()
 jumps=[]
 for pressed in [0,0x40,0x80,0xc0]:
  for held in [0,0x80]:
   for flag in [0,1]:
    b=bytearray(base);b[0x50]=pressed;b[0x52]=held;b[0x99]=flag
    a,t=execute(src,b,0xa801,{0xa82d,0xa945,0xa744});z,t2=execute(rom,b,0xa801,{0xa82d,0xa945,0xa744});assert a==z and t==t2
    trigger=not flag and bool(pressed&0x80)
    assert (a[5]==0xa945)==trigger
    if trigger:assert a[7][0x99]==1 and a[7][0x4d0]==0xfc and a[7][0x4c0]==0 and a[7][0x400]==0xd3
    jumps.append({'pressed':pressed,'held':held,'previous_jump_flag':flag,'triggered':trigger,'stop_PC':f'{a[5]:04X}','cycles':a[6]})
 clears=[]
 for state in [0,3,9]:
  for support in [0,1,255]:
   for hi in [0,11,21,22,23]:
    b=bytearray(base);b[0x430]=state;b[0xc1]=support;b[0x69]=hi;b[0x550]=5
    a,t=execute(src,b,0xa67b,{0xa696});z,t2=execute(rom,b,0xa67b,{0xa696});assert a==z and t==t2
    trigger=state!=9 and support!=0 and hi==22
    assert a[7][0x430]==(9 if trigger else state)and a[7][0x550]==(0 if trigger else 5)
    clears.append({'previous_state':state,'support':support,'vertical_hi':hi,'clear_triggered':trigger,'cycles':a[6]})
 m,c=machine(src)
 states=[m[0xa69e+i*2]+256*m[0xa69f+i*2]for i in range(10)]
 sub=[m[0xb879+i*2]+256*m[0xb87a+i*2]for i in range(8)]
 assert states==[0xa6bc,0xa6eb,0xa6f2,0xa801,0xac8c,0xac8c,0xac8c,0xad5c,0xacdf,0xb873]
 result={'work':152,'status':'PASS_BOUNDED_WATER_JUMP_CLEAR_DISCRIMINATION','source_sha256':sha(sp),'ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'guarded_source_spans':spans,'jump_CPU_case_pairs':jumps,'clear_CPU_case_pairs':clears,'state_pointer_table_CPU':'A69E..A6B2','state_targets_hex':[f'{z:04X}'for z in states],'clear_subphase_pointer_table_CPU':'B879..B889','clear_subphase_targets_hex':[f'{z:04X}'for z in sub],'historical_controller_failure_snapshots':observations,'verified_inputs':refs,'finding':'Held left without any jump leads state3→8 drowning by2850, phase09 by2970 with life still3. Phase09 alone is failure return, not clear. Natural clear requires native player state09 reached at supportC1!=0 and vertical69==16hex. Jump starts only pressedRAM50 bit80 with jumpflag99==0; heldRAM52 bit80 alone does not initiate it.','next_discrimination':'Fresh current049 read-only water trace with one A jump at2800 and no blind horizontal movement; record first support/loss/state8/state9 and vertical progress before designing longer controls.','human_approved':False,'release_eligible':False,'limits':['Offline NMOS6502 D-clear model/selected historical snapshots; no new emulator or complete water route','A69E and B879 tables parsed as pointer data, not instructions','Original/source current named spans only; no asynchronousIRQ/PPU/audio/global equivalence','No ROM/CSV edits or release approval']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in ['jump_CPU_case_pairs','clear_CPU_case_pairs','historical_controller_failure_snapshots','verified_inputs']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
