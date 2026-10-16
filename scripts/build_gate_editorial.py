"""Work90 manual single-entry castle-gate prose edit; source controls/timing preserved."""
from pathlib import Path
import argparse,csv,io,json,hashlib
from build_ui_home_booth import page
from build_dialogue_poc import FONT_SHA,TTF_SHA
from verify_gate_font_tag_hooks import compare,irq
from dialogue_ips import make as make_ips,apply as apply_ips
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to(R/'build');assert not out.exists()
 plan=json.loads((R/'workspace/translation/gate_editorial_plan_001.json').read_text('utf-8'));manifest=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/manifest['path']).read_bytes();assert sha(source)==manifest['sha256']==plan['source_sha256']
 prior_dir=R/'build/dialogue_kr_poc_046';prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==plan['prior_ROM_sha256'];csvbytes=(R/'workspace/translation/text_ja.csv').read_bytes();assert sha(csvbytes)==plan['CSV_sha256'];before=(R/plan['backup_CSV']).read_bytes();assert sha(before)==plan['backup_CSV_sha256']
 old=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));new=list(csv.DictReader(io.StringIO(csvbytes.decode('utf-8-sig'))));assert len(old)==len(new)==54 and sum(r['status']=='draft'for r in new)==45
 for x,y in zip(old,new):
  for k in x:
   if x['entry_id']=='MAIN_057C1'and k in ('translation_ko','notes'):continue
   assert x[k]==y[k]
 p=plan['profile'];assert next(x['translation_ko']for x in new if x['entry_id']==p['entry_id'])==p['text']
 png=R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png';ttf=R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 nativeplan=json.loads((R/'workspace/translation/ui_gate_plan_001.json').read_text('utf-8'));macrodata=json.loads((R/'build/dialogue_kr_poc_019/ui_macro_mapping.json').read_text('utf-8'))
 body,font,info=page(prior,source,p,nativeplan,macrodata,png,ttf);output=bytearray(prior);start=p['source_file_offset']+0x20000;end=p['end_exclusive']+0x20000;off=0x40010+p['font_bank']*0x400
 output[start:end]=body;output[off:off+0x800]=font
 changes=[i for i,(x,y)in enumerate(zip(prior,output))if x!=y];assert changes and all(start<=i<end or off<=i<off+0x800 for i in changes)
 assert output[:16]==prior[:16] and len(output)==499728 and output[0x5710+2*p['slot']]==p['font_bank']==175
 CPUcases=0
 for slot in range(48):
  for flags in (0x30,0x31,0x70,0xb5):
   for seed in (0,0x5a,0x80,0xaf,0xff):assert compare(prior,output,0x9417,slot,0,flags,0,seed)[0]==0;CPUcases+=1
 assert irq(prior)==irq(output)
 writes=json.loads((prior_dir/'expected_writes.json').read_text('utf-8'));expected=bytearray(source);owned=set()
 for w in writes:
  pos,n=w['file_offset'],w['length'];area=set(range(pos,pos+n));assert not area&owned;owned|=area;assert source[pos:pos+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(output[pos:pos+n]).hex();expected[pos:pos+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==bytes(output)
 out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output);patch=make_ips(source,bytes(output));assert apply_ips(source,patch)==bytes(output);(out/'TinyToon2_dialogue_kr_poc.ips').write_bytes(patch)
 (out/'TinyToon2_dialogue_kr_poc.json').write_text(json.dumps({'source_sha256':sha(source),'output_sha256':sha(output),'output_size':len(output),'patch_sha256':sha(patch),'scope':'Manual single gate prose edit plus prior046; draft not final release'},indent=2)+'\n','utf-8')
 report={'work':90,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','IPS_sha256':sha((out/'TinyToon2_dialogue_kr_poc.ips').read_bytes()),'csv_sha256':sha(csvbytes),'plan_sha256':sha((R/'workspace/translation/gate_editorial_plan_001.json').read_bytes()),'PRG_KiB':256,'CHR_KiB':232,'draft':45,'untranslated':9,'selected_entries':['MAIN_057C1'],'changed_bytes':len(changes),'admitted_prior_ranges':[[start,end],[off,off+0x800]],'font_banks':[175,176],'CPU_page_setup_cases':CPUcases,'all_page_setup_cycles_equal_prior046':True,'IRQ_all_write_offsets_equal':True,'native_reader_calls':info['reader_calls'],'native_reader_per_call_cycles_cursor_equal':True,'expected_writes':len(writes),'human_final_review':False,'scope':'Manual source-context single sentence edit, private existing175/176 font. Prior title/notices/other53SSOT units preserved. Runtime pending.'}
 for name,value in [('build_report.json',report),('expected_writes.json',writes),('gate_editorial_mapping.json',info)]: (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf-8')
 for name,path in [('translation_used.csv',R/'workspace/translation/text_ja.csv'),('plan_used.json',R/'workspace/translation/gate_editorial_plan_001.json'),('builder_used.py',Path(__file__))]:(out/name).write_bytes(path.read_bytes())
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
