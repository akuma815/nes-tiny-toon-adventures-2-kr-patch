"""Two home train/water labels; keeps all023 native gate and previous Korean glyphs."""
import argparse,csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode,decode
from verify_dialogue_home import reader
from verify_ui_native_latch_hooks import compare,irq
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
from build_ui_home_booth import page

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();plan=j('workspace/translation/ui_rides_plan_001.json');m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==plan['source_sha256']==m['sha256']
 prior_dir=ROOT/'build'/plan['prior_build'];prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==plan['prior_ROM_sha256'];writes=json.loads((prior_dir/'expected_writes.json').read_text('utf-8'));model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 csv_bytes=(ROOT/'workspace/translation/text_ja.csv').read_bytes();before=(ROOT/'backups/translation/text_ja_before_ui_rides_001.csv').read_bytes();assert sha(csv_bytes)==plan['CSV_sha256'] and sha(before)==plan['backup_CSV_sha256']
 rows=list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8-sig'))));oldrows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));selected={p['entry_id']:p for p in plan['profiles']};assert len(rows)==len(oldrows)==54 and len(selected)==2
 for x,y in zip(oldrows,rows):
  for k in x:
   if x['entry_id'] in selected and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k]
  if y['entry_id'] in selected:assert y['status']=='draft' and y['translation_ko']==selected[y['entry_id']]['text']
 assert sum(r['status']=='draft' for r in rows)==20
 png=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png';ttf=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 data=j('build/dialogue_kr_poc_019/ui_macro_mapping.json');output=bytearray(prior);output.extend(bytes(0x6c010-len(output)));output[5]=22;pages=[]
 for p in plan['profiles']:
  body,font,info=page(prior,source,p,plan,data,png,ttf);start,end=p['source_file_offset'],p['end_exclusive'];output[start+0x20000:end+0x20000]=body;off=0x40010+p['font_bank']*0x400;output[off:off+0x800]=font;output[0x5710+2*p['slot']]=p['font_bank'];pages.append(info)
 expected=bytearray(prior);expected.extend(bytes(len(output)-len(prior)));expected[5]=22
 for info in pages:
  p=info['profile'];expected[p['source_file_offset']+0x20000:p['end_exclusive']+0x20000]=bytes.fromhex(info['body_hex']);expected[0x5710+2*p['slot']]=p['font_bank'];off=0x40010+p['font_bank']*0x400
  for g in info['glyphs']:expected[off:off+0x800]=output[off:off+0x800]
 assert expected==output and output[0x40010:0x69810]==prior[0x40010:0x69810] and output[0x261ce:0x261ff]==prior[0x261ce:0x261ff] and not any(output[0x6a810:])
 for initial in (0,1,90,128,130,132,134,136,138,140,142,144,146,148,255):
  for slot in range(48):assert compare(prior,output,0x9417,slot,0,0x34,0,initial)[0]==0
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 for w in writes:
  p,n=w['file_offset'],w['length']
  if p==5:w['owner']='CHR_128_to176_KiB'
  if p==0x20010:n=len(output)-p;w['length']=n
  w['final_hex']=output[p:p+n].hex()
 expected=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 report={'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','csv_sha256':sha(csv_bytes),'plan_sha256':sha((ROOT/'workspace/translation/ui_rides_plan_001.json').read_bytes()),'PRG_KiB':256,'CHR_KiB':176,'draft':20,'untranslated':34,'expected_writes':len(writes),'selected_entries':list(selected),'font_banks':[[p['font_bank'],p['font_bank']+1] for p in plan['profiles']],'reserved_remaining_KiB':6,'CPU_page_seed_cases':720,'all_page_setup_cycles_equal_prior023':True,'scope':'Work26 two observed home train/water names; retains corrected gate Japanese and all18 drafts; no release','runtime':'NOT YET RUN; scene review/timing/matched protected pixels required'}
 for name,value in [('build_report.json',report),('expected_writes.json',writes),('ui_korean_page_mapping.json',pages)]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('plan_used.json',ROOT/'workspace/translation/ui_rides_plan_001.json'),('builder_used.py',Path(__file__))]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
