"""Correct little-endian native925E NT coordinates; historical model erratum."""
import json,hashlib
from pathlib import Path
from verify_gate_font_tag_hooks import Memory,MPU
ROOT=Path(__file__).resolve().parents[1]
def run(rom,p,ride):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x925e;c.sp=0xfd;m.ram[0x1fe:0x200]=bytes.fromhex('ff c0');m.ram[0x6cd:0x6cf]=p['pointer'].to_bytes(2,'little');m.ram[0x25]=ride
 for a in (0x6c0,0x6d1):m.ram[a:a+2]=p['NT'].to_bytes(2,'little')
 n=0
 while c.pc!=0xc100:c.step();n+=1;assert n<30000,(p['entry_id'],hex(c.pc))
 data=m.ram[0x100:0x100+m.ram[0x1e]];i=0;addresses=[]
 while i<len(data):
  assert data[i]==1,(p['entry_id'],i,data.hex());addresses.append(data[i+1]*256+data[i+2]);i+=3
  while data[i]!=255:i+=1;assert i<len(data)
  i+=1
 assert addresses==[p['NT']+0x40*row for row in range(len(addresses))],(p['entry_id'],addresses)
 return c,m,addresses
def main():
 cases=[]
 for current,prior in [('033','032'),('036','033')]:
  old=(ROOT/f'build/dialogue_kr_poc_{prior}/TinyToon2_dialogue_kr_poc.nes').read_bytes();new=(ROOT/f'build/dialogue_kr_poc_{current}/TinyToon2_dialogue_kr_poc.nes').read_bytes();pages=json.loads((ROOT/f'build/dialogue_kr_poc_{current}/ui_korean_page_mapping.json').read_text('utf-8'))
  for page in pages:
   p=page['profile']
   for ride in range(6):
    a,x,aa=run(old,p,ride);b,y,bb=run(new,p,ride);assert aa==bb and (a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles);cases.append({'build':current,'entry_id':p['entry_id'],'ride':ride,'cycles':b.processorCycles,'native_NT_addresses':aa})
 rom=(ROOT/'build/dialogue_kr_poc_036/TinyToon2_dialogue_kr_poc.nes').read_bytes();draft=json.loads((ROOT/'work/credits_group_001/draft_plan.json').read_text('utf-8'));credits=[]
 for p in draft['profiles']:
  p={**p,'pointer':p['source_file_offset']+0x3ff0,'NT':0x2005 if p['slot']==46 else 0x2805};c,m,nt=run(rom,p,0);credits.append({'entry_id':p['entry_id'],'cycles':c.processorCycles,'native_NT_addresses':nt})
 out={'status':'PASS','scope':'Correct little-endian6C0/1 and6D1/2 native immediate925E coordinates; exact parsed NT command addresses plus paired source/current cycle/register equality','historical_erratum':'Earlier033/036 standalone printer models seeded these two-byte coordinates in reversed order. Their paired cycle equality was genuine for that synthetic state, but not real NT geometry. Historical reports/scripts remain immutable; this report supplies corrected geometry evidence. Actual runtime pixel/NT/IRQ proofs were separate and unaffected.','corrected_paired_cases':len(cases),'cases':cases,'native_credits_source_printer':credits,'ROM_sha256':hashlib.sha256(rom).hexdigest(),'limits':'Official synchronous CPU model, no asynchronous PPU/interrupts; real scene traces separately required'};p=ROOT/'qa/reports/native_printer_geometry_corrected_20261005.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps({'status':'PASS','corrected_paired_cases':len(cases),'credit_source_cases':len(credits)},indent=2))
if __name__=='__main__':main()
