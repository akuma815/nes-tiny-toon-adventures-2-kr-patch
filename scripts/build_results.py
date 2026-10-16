"""Native bonus captions, immutable040, isolated208/209,8KiB CHR extension."""
import argparse,json,hashlib
from pathlib import Path
from compile_results import compile_results
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def producer(rom,flags,initial):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xf8cf;c.p=flags;c.a=31;c.x=17;c.y=67;c.sp=0xf7;m.ram[0x34]=initial
 while c.pc!=0xf8d8:c.step()
 return c,m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists();m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();assert sha(source)==m['sha256'];prior=(R/'build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='bdf5ca3a986d50b145571db13dfc75b58d3d2e4d140ae7805ef4a3f4f494ae0c';plan=compile_results(prior,source);base=prior+bytes(8192);target=bytearray(base);owned=set()
 def change(p,old,new):
  assert len(old)==len(new) and base[p:p+len(old)]==old;area=set(range(p,p+len(old)));assert not owned.intersection(area);owned.update(area);target[p:p+len(new)]=new
 change(5,b'\x1a',b'\x1b');change(0x3f8e0,b'\x7c',b'\xd0');change(0x74010,bytes(2048),bytes.fromhex(plan['font_hex']))
 for p in plan['labels']:change(p['expanded_file_offset'],bytes.fromhex(p['source_hex']),bytes.fromhex(p['body_hex']))
 assert target[0x44a0b:0x44aa5].hex()==plan['stream_hex'] and {i for i,(a,b) in enumerate(zip(base,target)) if a!=b}<=owned and not any(target[0x74810:]);cases=0
 for p in range(256):
  for initial in (0,76,255):
   ca,ma=producer(prior,p,initial);cb,mb=producer(target,p,initial);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles) and ca.processorCycles==11;assert (ma.ram[0x34],mb.ram[0x34])==(124,208) and {i for i in range(65536) if ma.ram[i]!=mb.ram[i]}=={0x34} and ma.banks==mb.banks;cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_040/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for w in writes:
  p,n=w['file_offset'],w['length']
  if p==0x20010:n+=8192;w['length']=n
  assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==target;out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);report={'work':46,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'font_banks':[208,209],'CHR_KiB':216,'source_CHR_and_prior_Korean_fonts_unchanged':True,'distinct_labels':7,'literal_blocks':8,'Hangul_unique':plan['Hangul_unique'],'native_producer_ABI_cases':cases,'producer_11_cycles_exact':True,'source_asset_length_controls_addresses_palette_digit_cells_unchanged':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'Korean bonus captions development draft; native phase seed access, notnaturalclear/fullgame; runtimepending'}
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('results_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('compiler_used.py',R/'scripts/compile_results.py'),('translation_used.csv',R/'workspace/translation/text_ja.csv')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
