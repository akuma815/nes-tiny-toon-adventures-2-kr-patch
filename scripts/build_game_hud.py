"""Immutable039 baseline, planned isolated HUD font206 and two IRQ operands."""
import json,hashlib,argparse
from pathlib import Path
from compile_game_hud import compile_hud
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def irq(rom,flags,counter):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xfccf;c.p=flags;c.sp=0xf6;c.a=19;c.x=83;c.y=93;m.ram[0x47]=counter
 while c.pc!=0xfd13:c.step()
 return c,m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists();m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));s=(R/m['path']).read_bytes();assert sha(s)==m['sha256'];prior=(R/'build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='6b4b9150ff55140d959a12938dc549a58c8ebb6bdb0007c31f4a242e711f066b';plan=compile_hud(prior,s);target=bytearray(prior);owned=set()
 def change(p,old,new):
  assert len(old)==len(new) and prior[p:p+len(old)]==old;area=set(range(p,p+len(old)));assert not owned.intersection(area);owned.update(area);target[p:p+len(new)]=new
 change(0x73810,bytes(0x800),bytes.fromhex(plan['font_hex']))
 for p in plan['producers']:change(p['file'],bytes([p['old']]),bytes([p['new']]))
 assert {i for i,(a,b) in enumerate(zip(prior,target)) if a!=b}<=owned;cases=0
 for p in range(256):
  for count in (1,4,255):
   ca,ma=irq(prior,p,count);cb,mb=irq(target,p,count);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles) and ma.ram==mb.ram and ma.banks==mb.banks
   assert len(ma.writes)==len(mb.writes)
   for old,new in zip(ma.writes,mb.writes):
    addr,v,t=old;wanted=(v+82 if addr in (0xa000,0xa008) else 15 if addr==0x2006 and v==47 else v);assert new==(addr,wanted,t),(old,new)
   cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_039/expected_writes.json').read_text('utf-8'));expected=bytearray(s);areas=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert s[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==target;out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);report={'work':44,'source_sha256':sha(s),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'new_font_banks':[206,207],'labels':len(plan['labels']),'IRQ_CPU_ABI_cases':cases,'IRQ_write_cycles_exact':True,'native_digit_multiplier_hearts_punctuation_tiles_unchanged':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'HUD development draft, runtime and visual QA pending; geometry intentionally body2px lower'}
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('hud_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('compiler_used.py',R/'scripts/compile_game_hud.py'),('translation_used.csv',R/'workspace/translation/text_ja.csv')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
