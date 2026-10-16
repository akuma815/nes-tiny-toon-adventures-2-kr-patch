"""Original803F decoder fed actual copied154-byte results asset inRAM0400."""
import json,hashlib
from pathlib import Path
from verify_booth_native_decoder import Ports
from verify_gate_font_tag_hooks import MPU
from title_codec import unpack
R=Path(__file__).resolve().parents[1]
def run(rom,stream,flags):
 m=Ports(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x803f;c.p=flags;c.sp=0xfd;m.ram[:2]=(0x400).to_bytes(2,'little');m.ram[0x400:0x400+len(stream)]=stream;steps=0
 while c.pc!=0x80be:c.step();steps+=1;assert steps<50000
 return c,m,steps
def main():
 a=(R/'build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes').read_bytes();b=(R/'build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes').read_bytes();sa=a[0x44a0b:0x44aa5];sb=b[0x44a0b:0x44aa5];old,n=unpack(sa);new,k=unpack(sb);assert n==k==154
 plan=json.loads((R/'build/dialogue_kr_poc_041/results_plan_used.json').read_text('utf-8'));admitted={p['NT']+i:(bytes.fromhex(p['source_hex'])[i],bytes.fromhex(p['body_hex'])[i]) for p in plan['labels'] for i in range(p['length'])};buf={0x400+i:(x,y) for i,(x,y) in enumerate(zip(sa,sb)) if x!=y};cases=0
 for flags in range(256):
  if flags&8:continue
  ca,ma,na=run(a,sa,flags);cb,mb,nb=run(b,sb,flags);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles,na)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles,nb) and ma.banks==mb.banks
  assert {i for i in range(65536) if ma.ram[i]!=mb.ram[i]}==set(buf)
  for i,pair in buf.items():assert (ma.ram[i],mb.ram[i])==pair
  assert len(ma.nt)==len(mb.nt)==1024
  for x,y in zip(ma.nt,mb.nt):
   assert x[0]==y[0] and x[2]==y[2] and old[x[0]]==x[1] and new[y[0]]==y[1]
   if x[1]!=y[1]:assert admitted[x[0]]==(x[1],y[1])
  cases+=1
 result={'work':46,'status':'PASS','native_entry':'803F, actual copied154-byte stream seededRAM0400, stop80BE before epilogue','D_clear_flag_cases':cases,'cycles':ca.processorCycles,'CPU_instructions':na,'PPU_writes':1024,'every_write_address_and_cycle_equal':True,'ABI_PRG_and_all_RAM_except_exact_input_literal_pairs_equal':True,'input_literal_changed_bytes':len(buf),'limits':['NMOS6502 D-set model excluded; actual NES emulator validates2A03 timing separately','No PPU raster emulation in this CPU model']}
 (R/'qa/reports/results041_native_decoder.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
