"""Isolated AI gameover/logo/labels fromimmutable041, originalsource ExpectedWrites."""
import argparse,json,hashlib
from pathlib import Path
from compile_gameover import compile_gameover
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def producer(rom,flags,initial):
 m=Memory(rom);m.banks[:2]=[0x36,0x37];c=MPU(memory=m);m.cpu=c;c.pc=0x93ac;c.p=flags;c.a=31;c.x=17;c.y=67;c.sp=0xf7;m.ram[0x34]=m.ram[0x35]=initial
 while c.pc!=0x93b8:c.step()
 return c,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists();m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();assert sha(source)==m['sha256'];prior=(R/'build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='535fa114952587dfc0a6394ddff21b1aede053ade3dc0d3d9dfda77ed5888eae';plan=compile_gameover(prior,source);target=bytearray(prior);owned=set()
 def change(p,old,new):
  assert len(old)==len(new) and prior[p:p+len(old)]==old;area=set(range(p,p+len(old)));assert not owned.intersection(area);owned.update(area);target[p:p+len(new)]=new
 for p,old,new in zip(plan['producer']['expanded_immediates'],plan['producer']['old'],plan['producer']['new']):
  change(p,bytes([old]),bytes([new]));change(p-0x20000,bytes([old]),bytes([new]))
 change(0x74810,bytes(2048),bytes.fromhex(plan['font210_hex']));change(0x75010,bytes(2048),bytes.fromhex(plan['font212_hex']))
 for z in plan['labels']:
  for p in (z['expanded_file_offset'],z['source_file_offset']):change(p,bytes.fromhex(z['source_hex']),bytes.fromhex(z['body_hex']))
 assert {i for i,(a,b) in enumerate(zip(prior,target)) if a!=b}<=owned and not any(target[0x75810:]);cases=0
 for flags in range(256):
  for initial in (0,120,255):
   ca,ma=producer(prior,flags,initial);cb,mb=producer(target,flags,initial);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles) and ca.processorCycles==15 and ma.banks==mb.banks;assert {i for i in range(65536) if ma.ram[i]!=mb.ram[i]}=={0x34,0x35} and (ma.ram[0x34],mb.ram[0x34],ma.ram[0x35],mb.ram[0x35])==(124,210,122,212);cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_041/expected_writes.json').read_text('utf-8'));assert prior[0xc010:0xe010]==source[0xc010:0xe010];writes.append({'owner':'native_gameover_low_bank06_compatibility','file_offset':0xc010,'length':8192,'expected_hex':source[0xc010:0xe010].hex(),'final_hex':target[0xc010:0xe010].hex()});expected=bytearray(source);areas=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==target;out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);report={'work':48,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'font_banks':[210,211,212,213],'CHR_KiB':216,'source_CHR_and_prior_Korean_fonts_unchanged':True,'logo':'게임 오버','distinct_labels':3,'literal_blocks':3,'literal_cells':21,'Hangul_unique':8,'native_producer_ABI_cases':cases,'producer_15_cycles_exact':True,'NT_logo_codes_geometry_palette_controls_lengths_and_ALL_other_prior_bytes_unchanged':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'Gameover AI art andcontinue3captions developmentdraft; actualnativefailure sourceconsumerknown, runtimepending'}
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('gameover_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('compiler_used.py',R/'scripts/compile_gameover.py'),('converter_used.py',R/'scripts/convert_gameover_art.py'),('translation_used.csv',R/'workspace/translation/text_ja.csv')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
