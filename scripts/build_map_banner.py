"""Build from verified037 with only mapped original banner tiles changed."""
import json,hashlib,argparse
from pathlib import Path
from compile_map_banner import compile_banner
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists()
 m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();assert sha(source)==m['sha256'];prior=(R/'build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='401626540d7995a0e5c672f5aec1dec1737a60bce631f8c89e68b742631bb752';plan=compile_banner();target=bytearray(prior);owned=set()
 for c in plan['changes']:
  p=c['expanded_file_offset'];raw=bytes.fromhex(c['source_raw_hex']);final=bytes.fromhex(c['final_hex']);assert prior[p:p+16]==raw and not set(range(p,p+16))&owned;owned.update(range(p,p+16));target[p:p+16]=final
 assert len(target)==len(prior) and target[:0x40010]==prior[:0x40010] and {i for i,(x,y) in enumerate(zip(prior,target)) if x!=y}<=owned
 writes=json.loads((R/'build/dialogue_kr_poc_037/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];assert not set(range(p,p+n))&areas;areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==target;out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target)
 report={'work':40,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'changed_banner_tiles':len(plan['changes']),'changed_ROM_bytes':sum(x!=y for x,y in zip(prior,target)),'unchanged_PRG_pointer_fonts_controls_palette_NT':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'draft':45,'untranslated':9,'scope':'Map banner generated Korean raster draft, 037 credits/all text/title preserved; runtime pending'}
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('banner_plan_used.json',plan)]: (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('compiler_used.py',R/'scripts/compile_map_banner.py'),('translation_used.csv',R/'workspace/translation/text_ja.csv'),('banner_prompt_used.txt',R/'workspace/graphics/map_banner_prompt_001.txt')]: (out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
