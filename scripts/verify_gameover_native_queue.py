"""Native93AC/9412 page0100 command queues, officialNMOS D-clear equivalence."""
import json
from pathlib import Path
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
class Queue(Memory):
 def __init__(self,rom):super().__init__(rom);self.banks[:2]=[0x36,0x37];self.qwrites=[]
 def __setitem__(self,a,v):
  if 0x100<=a<0x200:self.qwrites.append((a,v,self.cpu.processorCycles))
  super().__setitem__(a,v)
def run(rom,flags,base):
 m=Queue(rom);c=MPU(memory=m);m.cpu=c;c.p=flags;c.sp=0xf7;m.ram[0x1e]=base;steps=0
 for entry in (0x93ac,0x9412):
  c.sp=0xf7;m.ram[0x1f8]=0xff;m.ram[0x1f9]=0xc0;c.pc=entry
  while c.pc!=0xc100:c.step();steps+=1;assert steps<10000
 return c,m,steps

def parse(raw,base,memory):
 result={};pos=base
 for width in (16,16,16,16,10,6,5):
  assert raw[pos]==4;nt=raw[pos+1]*256+raw[pos+2];assert raw[pos+3]==memory[0xd17d+width*2] and raw[pos+4]==memory[0xd17e+width*2];start=pos+5
  for i in range(width):result[0x100+start+i]=(nt+i,raw[start+i])
  pos=start+width;assert raw[pos]==255;pos+=1
 return result,pos

def main():
 old=(R/'build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes').read_bytes();new=(R/'build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes').read_bytes();plan=json.loads((R/'build/dialogue_kr_poc_042/gameover_plan_used.json').read_text('utf-8'));admitted={p['NT']+i:(a,b) for p in plan['labels'] for i,(a,b) in enumerate(zip(bytes.fromhex(p['source_hex']),bytes.fromhex(p['body_hex'])))};cases=0;cycles=set();stepsset=set()
 for flags in range(256):
  if flags&8:continue
  for base in (0,32,64):
   ca,ma,na=run(old,flags,base);cb,mb,nb=run(new,flags,base);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles,na)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles,nb) and ma.banks==mb.banks and len(ma.qwrites)==len(mb.qwrites);xa,ea=parse(ma.ram[0x100:0x200],base,ma);xb,eb=parse(mb.ram[0x100:0x200],base,mb);assert ea==eb==ma.ram[0x1e]==mb.ram[0x1e]==base+127;allowed={0x34:(124,210),0x35:(122,212)}
   for p,(nt,va) in xa.items():
    ntb,vb=xb[p];assert nt==ntb
    if va!=vb:assert admitted[nt]==(va,vb);allowed[p]=(va,vb)
   for i,(a,b) in enumerate(zip(ma.ram,mb.ram)):
    if a!=b:assert allowed.get(i)==(a,b),(base,flags,hex(i),a,b)
   for a,b in zip(ma.qwrites,mb.qwrites):
    assert (a[0],a[2])==(b[0],b[2])
    if a[1]!=b[1]:assert allowed.get(a[0])==(a[1],b[1])
   cases+=1;cycles.add(ca.processorCycles);stepsset.add(na)
 result={'work':48,'status':'PASS','native_entries':['93AC','9412'],'D_clear_flags_queue_bases_cases':cases,'queue_bases':[0,32,64],'queue_length':127,'commands':7,'logo_NT_codes_64_cells_unchanged':True,'literal_cells':21,'every_queue_write_address_and_cycle_equal':True,'all_ABI_PRG_and_RAM_except_exact_font_values_and_owned_caption_pairs_equal':True,'cycles':sorted(cycles),'CPU_instructions':sorted(stepsset),'limits':['OfficialNMOS6502 D-clear model; actualNES interrupt/raster proof separate','Command producer only, nativePPU dispatcher timing checked in emulator']}
 out=R/'qa/reports/gameover042_native_queue.json';assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
