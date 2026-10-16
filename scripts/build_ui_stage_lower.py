"""Five observed castle drafts; preserve Japanese fallback and008 exact-time helper."""
import argparse,csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode,decode
from verify_dialogue_home import reader
from verify_gate_font_tag_hooks import run,irq
def compare(old,new,pc,slot,arg,p,counter,initial_font=0x80):
 a,x=run(old,pc,slot,arg,p,counter,initial_font);b,y=run(new,pc,slot,arg,p,counter,initial_font)
 assert (a.a,a.x,a.y,a.sp,a.p)==(b.a,b.x,b.y,b.sp,b.p) and x.banks==y.banks
 for i in range(0x800):
  if i in (0xc6,0x6f3,0x34):continue
  assert x.ram[i]==y.ram[i],(slot,hex(i))
 # Cost1D deliberately becomes lower-only. Test the tag contract against
 # initial RAM34 (zero in run), rather than the prior odd-tag result193.
 assert y.ram[0x34]==(y.ram[0xc6] if pc==0x9417 and y.ram[0xc6]&1 else 0)
 return b.processorCycles-a.processorCycles,y.ram[0xc6]
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
from compile_ui_stage_lower import group

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();plan=j('workspace/translation/ui_stage_lower_plan_001.json');m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==plan['source_sha256']==m['sha256']
 prior_dir=ROOT/'build'/plan['prior_build'];prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==plan['prior_ROM_sha256'];writes=json.loads((prior_dir/'expected_writes.json').read_text('utf-8'));model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 csv_bytes=(ROOT/'workspace/translation/text_ja.csv').read_bytes();before=(ROOT/'backups/translation/text_ja_before_ui_stage_lower_001.csv').read_bytes();assert sha(csv_bytes)==plan['CSV_sha256'] and sha(before)==plan['backup_CSV_sha256']
 rows=list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8-sig'))));oldrows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));selected={p['entry_id']:p for p in plan['profiles']};assert len(rows)==len(oldrows)==54 and len(selected)==5
 for x,y in zip(oldrows,rows):
  for k in x:
   if x['entry_id'] in selected and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k]
  if y['entry_id'] in selected and not selected[y['entry_id']]['technical']:assert y['status']=='draft' and y['translation_ko']==selected[y['entry_id']]['text']
 assert sum(r['status']=='draft' for r in rows)==42
 png=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png';ttf=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 data=j('build/dialogue_kr_poc_019/ui_macro_mapping.json');output=bytearray(prior);output.extend(bytes(0x72010-len(output)));output[5]=25;pages=[]
 font,pages,font_info=group(prior,source,plan,data,png,ttf)
 for info in pages:
  p=info['profile'];start,end=p['source_file_offset'],p['end_exclusive'];output[start+0x20000:end+0x20000]=bytes.fromhex(info['body_hex']);
  for slot in p['slots']:output[0x5710+2*slot]=196
 output[0x71010:0x71810]=font
 assert len(pages)==5 and len({p['profile']['entry_id'] for p in pages})==5
 expected=bytearray(prior);expected.extend(bytes(len(output)-len(prior)));expected[5]=25
 for info in pages:
  p=info['profile'];expected[p['source_file_offset']+0x20000:p['end_exclusive']+0x20000]=bytes.fromhex(info['body_hex']);
  for slot in p['slots']:expected[0x5710+2*slot]=p['font_bank']
  off=0x40010+p['font_bank']*0x400
  expected[off:off+0x800]=font
 assert expected==output and output[0x40010:0x70010]==prior[0x40010:0x70010] and output[0x261ce:0x261ff]==prior[0x261ce:0x261ff] and not any(output[0x70c10:0x71010]) and not any(output[0x71810:0x72010]) and not any(output[0x70010:0x70410]) and not any(output[0x6ec10:0x6f010]) and not any(output[0x6a810:0x6ac10])
 for initial in (0,1,90,128,130,132,134,136,138,140,142,144,146,148,255):
  for slot in range(48):assert compare(prior,output,0x9417,slot,0,0x34,0,initial)[0]==0
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 for w in writes:
  p,n=w['file_offset'],w['length']
  if p==5:w['owner']='CHR_128_to200_KiB'
  if p==0x20010:n=len(output)-p;w['length']=n
  w['final_hex']=output[p:p+n].hex()
 expected=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 report={'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','csv_sha256':sha(csv_bytes),'plan_sha256':sha((ROOT/'workspace/translation/ui_stage_lower_plan_001.json').read_bytes()),'PRG_KiB':256,'CHR_KiB':200,'draft':42,'untranslated':12,'expected_writes':len(writes),'selected_entries':list(selected),'font_banks':[[196,197]],'font_glyphs_Hangul':font_info['Hangul_unique'],'native_reader_state_cases':font_info['state_cases'],'reserved_remaining_KiB':6,'CPU_page_seed_cases':720,'all_page_setup_cycles_equal_prior033':True,'scope':'Work35 shared stage lower font196 across five native units/six slots, exact native timing;42drafts retained; technical F9 unchanged status; no release','runtime':'NOT YET RUN; scene review/timing/matched protected pixels required'}
 for name,value in [('build_report.json',report),('expected_writes.json',writes),('ui_korean_page_mapping.json',pages),('ui_stage_lower_shared_font.json',font_info)]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('plan_used.json',ROOT/'workspace/translation/ui_stage_lower_plan_001.json'),('builder_used.py',Path(__file__))]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
