"""Work25 native gate top-font immediate correction; all other022 bytes preserved."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=ROOT/'build/dialogue_kr_poc_022';meta=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));source=(ROOT/meta['path']).read_bytes();assert sha(source)==meta['sha256'];prior=(p/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='88dada01f379ca25abb9cee08793b372fbe9508ba6d1581b131c9d07ff90ba08';assert (ROOT/'workspace/translation/text_ja.csv').read_bytes()==(p/'translation_used.csv').read_bytes();writes=json.loads((p/'expected_writes.json').read_text('utf-8'));model=bytearray(source)
 for w in writes:
  off,n=w['file_offset'],w['length'];assert source[off:off+n]==bytes.fromhex(w['expected_hex']);model[off:off+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior;out=bytearray(prior)
 for base in (0,0x20000):assert prior[0x6007+base:0x600b+base]==bytes.fromhex('a95a8534');out[0x6008+base]=148
 assert [i for i,(x,y) in enumerate(zip(prior,out)) if x!=y]==[0x6008,0x26008]
 for w in writes:
  off,n=w['file_offset'],w['length'];w['final_hex']=out[off:off+n].hex()
 model=bytearray(source);owned=set()
 for w in writes:
  off,n=w['file_offset'],w['length'];area=set(range(off,off+n));assert not owned&area;owned|=area;assert source[off:off+n]==bytes.fromhex(w['expected_hex']);model[off:off+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==out
 target=a.output.resolve();target.relative_to((ROOT/'build').resolve());target.mkdir(parents=True,exist_ok=False)
 (target/'TinyToon2_dialogue_kr_poc.nes').write_bytes(out)
 report=json.loads((p/'build_report.json').read_text('utf-8'));report.update(output_sha256=sha(out),prior_adopted_sha256=sha(prior),gate_top_font_correction={'CPU':'9FF7 LDA immediate','source_font':90,'output_font':148,'offsets':[0x6008,0x26008],'extra_instructions':0,'extra_cycles':0},scope='Work25 native castle top font148; Korean scope remains18 drafts; no release',runtime='Pending actual gate native Japanese017 comparison and022 regressions')
 for name,data in [('build_report.json',report),('expected_writes.json',writes)]:(target/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name in ['translation_used.csv','plan_used.json','ui_korean_page_mapping.json']:(target/name).write_bytes((p/name).read_bytes())
 (target/'builder_used.py').write_bytes(Path(__file__).read_bytes());print(json.dumps({'output_sha256':sha(out),'output_size':len(out),'changed_bytes_from022':2},indent=2))
if __name__=='__main__':main()
