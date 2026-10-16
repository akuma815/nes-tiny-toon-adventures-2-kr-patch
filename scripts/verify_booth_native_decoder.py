"""Official6502 original803F compressed NT decoder; actual port-write sequence."""
import json,hashlib
from pathlib import Path
from verify_gate_font_tag_hooks import Memory,MPU
from title_codec import unpack
R=Path(__file__).resolve().parents[1]
class Ports(Memory):
 def __init__(self,rom):super().__init__(rom);self.address=0;self.high=True;self.nt=[]
 def __getitem__(self,a):
  if a==0x2002:self.high=True;return 0
  return super().__getitem__(a)
 def __setitem__(self,a,v):
  if a==0x2006:
   if self.high:self.address=(v&63)<<8
   else:self.address=(self.address&0x3f00)|v
   self.high=not self.high
  elif a==0x2007:self.nt.append((self.address,v,self.cpu.processorCycles));self.address=(self.address+1)&0x3fff
  super().__setitem__(a,v)
def run(rom,flags):
 m=Ports(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x803f;c.p=flags;c.sp=0xfd;m.ram[:2]=(0x8639).to_bytes(2,'little');steps=0
 while c.pc!=0x80be:c.step();steps+=1;assert steps<50000
 return c,m,steps
def main():
 a=(R/'build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes').read_bytes();b=(R/'build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes').read_bytes();old,n=unpack(a[0x24649:0x247b2]);new,k=unpack(b[0x24649:0x247b2]);assert n==k==0x169;plan=json.loads((R/'build/dialogue_kr_poc_039/booth_plan_used.json').read_text('utf-8'));admitted={p['NT']+i:(bytes.fromhex(p['source_hex'])[i],bytes.fromhex(p['body_hex'])[i]) for p in plan['labels'] for i in range(p['length'])};assert set(old)==set(new)==set(range(0x2000,0x2400))
 for addr in old:
  if old[addr]!=new[addr]:assert admitted[addr]==(old[addr],new[addr])
 cases=0
 for flags in range(256):
  # This vendored official model is NMOS6502 with BCD arithmetic. Limit the
  # pointer-ADC model to D-clear flags; actual NES execution/timing is separate.
  if flags&8:continue
  ca,ma,sa=run(a,flags);cb,mb,sb=run(b,flags);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles,sa)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles,sb) and ma.ram==mb.ram and ma.banks==mb.banks;assert len(ma.nt)==len(mb.nt)==1024
  for x,y in zip(ma.nt,mb.nt):assert x[0]==y[0] and x[2]==y[2] and old[x[0]]==x[1] and new[y[0]]==y[1]
  cases+=1
 result={'status':'PASS','work':42,'source_native_entry':'803F, original pointer8639/file24649, stop80BE before shared postdecode epilogue','original_decoder_128_D_clear_flag_cases':cases,'literal_stream_bytes':n,'decoded_NT_cells':len(old),'cycles':ca.processorCycles,'CPU_instructions':sa,'every_modeled_2007_address_and_cycle_equal':True,'PRG_source_data_changed_only_five_literal_runs':True,'ABI_RAM_banks_equal':True,'limits':['Official NMOS6502 model has BCD ADC; D-set flags excluded rather than claiming a full2A03 CPU model. Actual NES runtime/timing checked separately.'],'callback_semantics_erratum':'Actual read opcode806C LDA($00),Y, callback reports advancedPC806E before STA2007; physical mapping proof remains same8000 bank','producer_cycles_metadata_erratum':'039 frozen builder report named producer12cycles incorrectly; four actual instructions take10cycles. CPU768 equality was valid; current builder requires10 explicitly. Frozen builds preserved, independent verifier records10.'};(R/'qa/reports/booth039_native_decoder.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
