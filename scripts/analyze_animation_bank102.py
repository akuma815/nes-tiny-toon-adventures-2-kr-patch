"""Work102 native bank38 animation tables; values bounded by actual masks/counters."""
from pathlib import Path
import hashlib,json
from verify_dialogue_home import MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def memory(rom):
 m=bytearray(65536);offset=0x10010+(0x20000 if len(rom)!=262160 else 0);m[0x8000:0xc000]=rom[offset:offset+0x4000];return m

def execute(rom,pc,end,course=0,phase=0,mode=0,delay=0,full=False):
 m=memory(rom);m[0x25]=course;m[0x440]=phase;m[0x441]=phase;m[0x721]=1;m[0x722]=mode;m[0x451]=delay;m[0x1fe:0x200]=bytes.fromhex('ff c0');c=MPU(memory=m);c.pc=pc;c.sp=0xfd;c.x=1;c.p=0x30;steps=0
 while c.pc!=end:c.step();steps+=1;assert steps<1000,(hex(pc),hex(c.pc),phase,mode,delay)
 return c,m,steps

def main():
 out=R/'qa/reports/animation102_bank36.json';assert not out.exists();meta=j('manifests/source_rom.json');src=(R/meta['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(src)==meta['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256'];m=memory(src);n=memory(rom)
 assert m[0x8015:0x801a]==bytes.fromhex('ad40042903')and m[0x9326:0x932b]==bytes.fromhex('bd4004c907');pairs=[];actions=[]
 for selector in range(2):
  p=int.from_bytes(m[0x803f+selector*2:0x8041+selector*2],'little');assert p==(0x8043 if selector==0 else 0x804b)
  for phase in range(4):
   data=m[p+phase*2:p+phase*2+2];assert data==n[p+phase*2:p+phase*2+2];pairs.append({'selector_RAM25_zero':selector==0,'phase_0440_mask3':phase,'CPU_descriptor':p+phase*2,'source_file_offset':0x10010+p+phase*2-0x8000,'pose':data[0],'bank36':data[1],'raw_hex':data.hex()})
  p=int.from_bytes(m[0x93f0+selector*2:0x93f2+selector*2],'little');assert p==(0x93f4 if selector==0 else 0x9417)
  for phase in range(7):
   data=m[p+phase*5:p+phase*5+5];assert data==n[p+phase*5:p+phase*5+5];actions.append({'mode0722':selector,'phase0441_0to6':phase,'CPU_descriptor':p+phase*5,'source_file_offset':0x10010+p+phase*5-0x8000,'actor1_pose':data[0],'bank36':data[1],'actor0_pose':data[2],'relative_x_raw':data[3],'relative_y_raw':data[4],'raw_hex':data.hex()})
 assert{p['bank36']for p in pairs}=={8,9,24}and{p['bank36']for p in actions}=={12,13,14}
 table_cases=[];transition=[]
 # Each slice uses its genuine bounds. Native 803C writes actor0, and native
 #92D6 fixes X=1 before the transformation branch; arbitrary actors not needed.
 for course in range(6):
  for phase in range(4):
   a,x,steps=execute(src,0x801d,0x803e,course,phase);b,y,ns=execute(rom,0x801d,0x803e,course,phase);expected=pairs[(0 if course==0 else 1)*4+phase];assert x[0x400]==expected['pose']and x[0x36]==expected['bank36'];assert(a.a,a.x,a.y,a.p,a.sp,a.processorCycles,steps)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles,ns)and x[:2048]==y[:2048];table_cases.append({'kind':'pair','course':course,'phase':phase,'bank36':x[0x36],'cycles':a.processorCycles})
 for mode in range(2):
  for phase in range(7):
   a,x,steps=execute(src,0x9341,0x9364,phase=phase,mode=mode);b,y,ns=execute(rom,0x9341,0x9364,phase=phase,mode=mode);expected=actions[mode*7+phase];assert x[0x401]==expected['actor1_pose']and x[0x36]==expected['bank36'];assert(a.a,a.x,a.y,a.p,a.sp,a.processorCycles,steps)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles,ns)and x[:2048]==y[:2048];table_cases.append({'kind':'action','mode':mode,'phase':phase,'bank36':x[0x36],'cycles':a.processorCycles})
   for delay in range(3):
    a,x,steps=execute(src,0x92d6,0xc100,phase=phase,mode=mode,delay=delay);b,y,ns=execute(rom,0x92d6,0xc100,phase=phase,mode=mode,delay=delay);assert(a.a,a.x,a.y,a.p,a.sp,a.processorCycles,steps)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles,ns)and x[:2048]==y[:2048];assert x[0x441]<=6 and x[0x722]in(0,1)and x[0x36]in(0,12,13,14)
    toggled=phase==6 and delay==2;assert(x[0x721]==0)==toggled and(x[0x722]!=mode)==toggled;transition.append({'mode_before':mode,'phase_before':phase,'delay_before':delay,'mode_after':x[0x722],'phase_after':x[0x441],'bank36_after':x[0x36],'transition_finished':x[0x721]==0,'cycles':a.processorCycles})
 assert len(table_cases)==38 and len(transition)==42
 result={'work':102,'status':'PASS_BOUNDED_NATIVE_ANIMATION_BANK36_TABLES','source_sha256':sha(src),'ROM047_sha256':sha(rom),'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'native_PRG_window_source_base':0x10010,'native_PRG_window_current047_base':0x30010,'pair_pointer_table_CPU':0x803f,'pair_records':pairs,'pair_banks_decimal':[8,9,24],'action_pointer_table_CPU':0x93f0,'action_records':actions,'action_banks_decimal':[12,13,14],'CPU_slices':table_cases,'CPU_transitions':transition,'source_current_native_CPU_case_pairs':80,'full_RAM_registers_cycles_equal':True,'native_phase_bounds':'0440 AND03→four pairs; transformationCMP07 and reset/toggle→seven records per mode; mode0/1 from EOR01 selector','PAUSE120121_supplied_by_these_tables':False,'ROM_CSV_edited':False,'limits':['Original bank38 window only. CPU9417 here is descriptor data, not the dialogue9417 in different PRGwindow','80bounded modelcasepairs withDclear30 and no asynchronousIRQ/PPU; not whole engine or all flag/entry RAM/caller reachability proof','Some completed-mode branch keeps prior bank36; artificial zero seed recorded, not a new font demand','Other bank36 indexed tables, stage-specific indirect aliases and source/currentC6/C7 supplies remain distinct open populations','No new actual runtime/full natural game/global-unused/final human preservation/release claim'],'next_action':'Inventory sourceC6/C7 font-latch producers and distinguish the native IRQ font range from PAUSE bank120121; keep previously scoped animation evidence frozen.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in('pair_records','action_records','CPU_slices','CPU_transitions')},indent=2))
if __name__=='__main__':main()