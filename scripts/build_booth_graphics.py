"""Clone038, five native compressed literals, font204/205 and AI header."""
import json,hashlib,argparse
from pathlib import Path
from compile_booth_graphics import compile_booth
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def producer(rom,p,initial):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x9c95;c.p=p;c.a=37;c.x=13;c.y=91;c.sp=0xf7;m.ram[0x34]=initial
 while c.pc!=0x9c9d:c.step()
 return c,m
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists();m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();assert sha(source)==m['sha256'];prior=(R/'build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='33b11de02e390d9617812350198bf60b023b64d65db9f1ea9bb5534a34f265d1';plan=compile_booth(prior,source);target=bytearray(prior);owned=set()
 def change(p,old,final):
  assert len(old)==len(final) and prior[p:p+len(old)]==old;area=set(range(p,p+len(old)));assert not area&owned;owned.update(area);target[p:p+len(final)]=final
 for label in plan['labels']:
  for p in (label['source_file_offset'],label['expanded_file_offset']):change(p,bytes.fromhex(label['source_hex']),bytes.fromhex(label['body_hex']))
 for p in plan['producer']['source_file_offsets']:change(p,b'\x7c',b'\xcc')
 change(0x73010,bytes(0x800),bytes.fromhex(plan['font_hex']))
 for c in plan['header']['changes']:change(c['expanded_file_offset'],bytes.fromhex(c['source_raw_hex']),bytes.fromhex(c['final_hex']))
 assert len(target)==len(prior) and {i for i,(x,y) in enumerate(zip(prior,target)) if x!=y}<=owned
 cases=0
 for flags in range(256):
  for initial in (0,124,255):
   ca,ma=producer(prior,flags,initial);cb,mb=producer(target,flags,initial);assert (ca.a,ca.x,ca.y,ca.sp,ca.p,ca.processorCycles)==(cb.a,cb.x,cb.y,cb.sp,cb.p,cb.processorCycles) and ca.processorCycles==10 and (ma.ram[0x34],mb.ram[0x34])==(124,204);assert {i for i in range(2048) if ma.ram[i]!=mb.ram[i]}=={0x34};cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_038/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];assert not set(range(p,p+n))&areas;areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==target;out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);report={'work':42,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'selected_labels':5,'generated_header_tiles':len(plan['header']['changes']),'new_font_banks':[204,205],'Hangul_unique':plan['Hangul_unique'],'native_producer_CPU_cases':cases,'producer_10_cycles_and_post_LDA66_ABI_equal':True,'unchanged_dialogue_title_map_credits_native_digits_other_fonts':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'draft':45,'untranslated':9,'scope':'Five native booth graphic labels and generated header draft; observed native consumer, compression length/controls/numbers unchanged; runtime pending'}
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('booth_plan_used.json',plan)]: (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('compiler_used.py',R/'scripts/compile_booth_graphics.py'),('translation_used.csv',R/'workspace/translation/text_ja.csv'),('header_prompt_used.txt',R/'workspace/graphics/booth_header_prompt_001.txt')]: (out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
