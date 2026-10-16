"""Bank-aware NMOS6502 hook ABI and IRQ write-offset verification; no PPU emulation."""
import argparse,json,sys,hashlib
from pathlib import Path
from asm6502 import MPU,verify_profile
ROOT=Path(__file__).resolve().parents[1]
class Memory:
 def __init__(self,rom):
  self.rom=rom;self.count=rom[4]*2;self.ram=bytearray(65536);self.banks=[0x32,0x33,0x3e,self.count-1];self.writes=[];self.cpu=None
 def __getitem__(self,a):
  if a>=0x8000:return self.rom[0x10+(self.banks[(a-0x8000)//8192]&63)%self.count*8192+(a%8192)]
  return self.ram[a%2048 if a<8192 else a]
 def __setitem__(self,a,v):
  if a in (0x8000,0x8008):self.banks[0 if a==0x8000 else 1]=v
  elif a<0x8000:self.ram[a%2048 if a<8192 else a]=v
  if a>=0x2000:self.writes.append((a,v,self.cpu.processorCycles if self.cpu else 0))
def run(rom,pc,slot=1,arg=0,p=0x34,counter=0,initial_font=0x80):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=pc;c.sp=0xfd;c.a=arg;c.x=0x73;c.y=0x92;c.p=p
 m.ram[0x1fe]=0xff;m.ram[0x1ff]=0xc0;m.ram[0x2b]=0x36;m.ram[0x6cf]=slot;m.ram[0x6de]=counter;m.ram[0xc6]=initial_font
 steps=0
 while c.pc!=0xc100:
  c.step();steps+=1;assert steps<10000,(hex(c.pc),steps)
 return c,m
def compare(old,new,pc,slot,arg,p,counter,initial_font=0x80):
 a,x=run(old,pc,slot,arg,p,counter,initial_font);b,y=run(new,pc,slot,arg,p,counter,initial_font)
 assert (a.a,a.x,a.y,a.sp,a.p)==(b.a,b.x,b.y,b.sp,b.p),((pc,slot,arg,p,counter),(a.a,a.x,a.y,a.sp,a.p),(b.a,b.x,b.y,b.sp,b.p))
 assert x.ram[0x2b]==y.ram[0x2b]==0x36
 for i in range(0x800):
  if i==0xc6 or 0x100<=i<0x200:continue
  assert x.ram[i]==y.ram[i],(hex(pc),slot,hex(i),x.ram[i],y.ram[i])
 assert x.banks[:2]==y.banks[:2]==[0x32,0x33]
 return b.processorCycles-a.processorCycles,y.ram[0xc6]
def irq(rom):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xfb97;m.ram[0xc6]=0x80;c.sp=0xf6
 while c.pc!=0xfd13:c.step()
 assert c.sp==0xf6 and m.ram[0x47]==0
 return c.processorCycles,[(a,v,t) for a,v,t in m.writes if a in (0x2000,0x2005,0x2006,0xa000,0xa008,0xb000,0xb008)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--report',type=Path);z=ap.parse_args()
 old=(ROOT/'build/dialogue_kr_poc_003/TinyToon2_dialogue_kr_poc.nes').read_bytes();new=(z.build/'TinyToon2_dialogue_kr_poc.nes').read_bytes();results={};cases=0
 for slot in range(48):
  for arg in (0,1,2,3):
   for p in (0x30,0x31,0x70,0xb5):
    delta,font=compare(old,new,0x9417,slot,arg,p,0);cases+=1;results[str(slot)]={'extra_cycles':delta,'mod19':delta%19,'font':font}
 setup={}
 for p in (0x30,0x31,0x70,0xb5):
  for counter in (0,0x7f,0xfe,0xff):
   delta,font=compare(old,new,0x8e88,1,0,p,counter);cases+=1;setup[str(counter)]={'extra_cycles':delta,'mod19':delta%19,'font':font}
 adopted=(ROOT/'build/dialogue_kr_poc_008/TinyToon2_dialogue_kr_poc.nes').read_bytes();seeded_cases=0
 for initial_font in (0,1,0x5a,0x80,0x84,0x86,0x88,0xff):
  for slot in range(48):
   pointer=int.from_bytes(old[0x55a9+slot*2:0x55ab+slot*2],'little');expected_font={0x95f9:0x80,0x9615:0x84,0x963d:0x86,0x9655:0x88}.get(pointer,0x5a)
   delta,font=compare(old,new,0x9417,slot,0,0x34,0,initial_font);assert delta%19==0 and font==expected_font,(slot,initial_font,delta,font,expected_font);cases+=1;seeded_cases+=1
   assert compare(adopted,new,0x9417,slot,0,0x34,0,initial_font)[0]==0
 assert all(x['mod19']==0 for x in results.values()) and all(x['mod19']==0 for x in setup.values()),'Idle-loop phase must remain aligned'
 assert irq(old)==irq(new),(irq(old),irq(new))
 try:run((ROOT/'build/dialogue_kr_poc_004/TinyToon2_dialogue_kr_poc.nes').read_bytes(),0x8e88)
 except AssertionError:negative_rejected=True
 else:raise AssertionError('Broken004 trampoline was not rejected')
 result={'rom_sha256':hashlib.sha256(new).hexdigest(),'abi_cases':cases,'broken004_control_rejected':negative_rejected,'idle_loop_period':19,'all_added_hook_cycles_multiple_of19':True,'page_cases':results,'setup_cases':setup,'irq_cycles':irq(new)[0],'irq_all_ppu_chr_write_offsets_equal':True,'isa':verify_profile(),'limitations':'CPU model excludes asynchronous interrupts, actual PPU, RNG side effects; real emulator traces separately required.'}
 result.update(initial_latch_seed_cases=seeded_cases,expected_pointer_font_selection=True,all_page_cycles_equal_adopted008=True)
 if z.report:z.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
