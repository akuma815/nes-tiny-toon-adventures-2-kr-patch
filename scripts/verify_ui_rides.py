"""Independent two-name024 font/source/cycle/apply and matched-route verification."""
import csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageChops
from verify_dialogue_home import reader
from extract_title_png import encode
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def env(prefix,rom):
 e=j('qa/dialogue/'+prefix+'/environment.json');assert e['exit_code']==0 and e['rom_sha256']==sha(rom)
 for n,h in e['files'].items():assert sha(read('qa/dialogue/'+prefix+'/'+n))==h,(prefix,n)
 return e
def main():
 d='build/dialogue_kr_poc_024';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_023/TinyToon2_dialogue_kr_poc.nes');meta=j('manifests/source_rom.json');source=read(meta['path']);assert sha(source)==meta['sha256'];model=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==rom;pages=j(d+'/ui_korean_page_mapping.json');assert len(pages)==2;expected=bytearray(prior);expected.extend(bytes(0x6c010-len(prior)));expected[5]=22;sheet=Image.open(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');fonts={};cycles={}
 oldview=bytearray(source);oldview[0x4010:0xc000-0x8000+0x4010]=prior[0x24010:0x28010];newview=bytearray(oldview)
 for page in pages:
  p=page['profile'];font=bytearray(prior[0x65010:0x65810]);mapping={int(k):v for k,v in page['forced_macro_glyphs'].items()};mapping.update({int(x['code']):x['char'] for x in page['glyphs']});mapping[0]=' '
  for g in page['glyphs']:
   if g['char']==' ':data=bytes(16)
   else:
    n=ord(g['char'])-0xac00;assert 0<=n<=0xd7a3-0xac00;x=n%64*8;y=n//64*8;pixels=[int(v[3]>0 and max(v[:3])>127)*2 for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];assert any(pixels);data=encode(bytes(pixels))
   assert data==bytes.fromhex(g['chr_hex']);font[g['code']*16:(g['code']+1)*16]=data
  start,end=p['source_file_offset'],p['end_exclusive'];body=bytes.fromhex(page['body_hex']);assert sha(source[start:end])==p['source_raw_sha256'] and body==prior[start+0x20000:end+0x20000], 'Macro-only name body must stay exact'
  newview[start:end]=body;old=reader(oldview,p['pointer']);new=reader(newview,p['pointer']);assert old==new
  text=''.join(mapping[e['value']] for e in new if e['value']!=255);assert text==page['layout'][0]['desired'] and text.rstrip()==p['text'];cycles[p['entry_id']]={'calls':len(new),'cycles':sum(x['cycles'] for x in new)}
  off=0x40010+p['font_bank']*0x400;assert rom[off:off+0x800]==font;expected[off:off+0x800]=font;expected[0x5710+2*p['slot']]=p['font_bank'];fonts[p['font_bank']]=bytes(font)
 assert bytes(expected)==rom and len(rom)==442384 and rom[5]==22 and not any(rom[0x6a810:]);assert rom[0x40010:0x69810]==prior[0x40010:0x69810] and rom[0x26007:0x2600b]==prior[0x26007:0x2600b]
 before=list(csv.DictReader(io.StringIO(read('backups/translation/text_ja_before_ui_rides_001.csv').decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));ids={p['profile']['entry_id'] for p in pages};assert len(before)==len(after)==54
 for a,b in zip(before,after):
  for k in a:
   if a['entry_id'] in ids and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert a[k]==b[k]
 assert sum(x['status']=='draft' for x in after)==20 and sum(x['status']=='untranslated' for x in after)==34 and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')
 assert read('build/dialogue_kr_poc_024_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 024/TinyToon2_rides024_applied.nes')==rom
 byfont={p['profile']['font_bank']:p for p in pages};observed={k:0 for k in fonts};routes={};total=0
 for route in ('train','water','castle'):
  prefix='rides024_'+route;reference='gate023_'+route;ae=env(prefix,rom);re=env(reference,prior);assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted((ROOT/'qa/dialogue'/prefix).glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted((ROOT/'qa/dialogue'/reference).glob('frame_*.png'))];changed=0
  for f in files:
   base='qa/dialogue/'+prefix+'/'+f.stem;ref='qa/dialogue/'+reference+'/'+f.stem;r=read(base+'_ram.bin');rr=read(ref+'_ram.bin');p=read(base+'_ppu.bin');rp=read(ref+'_ppu.bin');font=r[0x6f3];page=byfont.get(font);diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ROOT/(ref+'.png')).convert('RGB'))
   assert all(r[i]==rr[i] for i in range(2048) if i not in (0xc6,0x6f3)),(route,f.name,'game RAM')
   assert p[0x800:]==rp[0x800:] and read(base+'_oam.bin')==read(ref+'_oam.bin'),(route,f.name,'protected PPU/OAM')
   if diff.getbbox():assert page;changed+=1
   if page:
    count=page['layout'][0]['expanded_tiles'];diff.paste(0,(64,163,64+8*count,171));assert (r[0x6f3],rr[0x6f3])==(font,148)
    maps=rows(base+'_mapping.csv');off=int(next(x for x in maps if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
    if off==font*0x400:assert p[:0x800]==fonts[font];observed[font]+=1
   else:assert p[:0x800]==rp[:0x800]
   assert diff.getbbox() is None,(route,f.name,diff.getbbox())
  a=[x for x in rows('qa/dialogue/'+prefix+'/menu_events.csv') if x['kind']=='exec'];b=[x for x in rows('qa/dialogue/'+reference+'/menu_events.csv') if x['kind']=='exec'];assert len(a)==len(b)
  for x,y in zip(a,b):assert all(x[k]==y[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc','phase','ride','head_font','caller'))
  routes[route]={'screens':len(files),'current_selection_rows_changed':changed,'whole_frames_equal':len(files)-changed};total+=len(files)
 assert all(n>0 for n in observed.values());timing={}
 for route in ('train','water'):
  a=env('rides023_'+route+'_irq',prior);b=env('rides024_'+route+'_irq',rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));old=rows('qa/dialogue/rides023_'+route+'_irq/irq_phase.csv');new=rows('qa/dialogue/rides024_'+route+'_irq/irq_phase.csv');assert len(old)==len(new);changed=0
  for x,y in zip(old,new):
   assert all(x[k]==y[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(x,y)
   if x['value']!=y['value']:
    assert (x['address']=='A000' and x['value']=='94' and int(y['value'],16) in fonts) or (x['address']=='A008' and x['value']=='95' and int(y['value'],16)-1 in fonts);changed+=1
  timing[route]={'actual_timestamps_equal':len(old),'private_font_changes_only':changed}
 hooks=j('qa/reports/rides024_hooks1504.json');assert hooks['abi_cases']==1504 and hooks['initial_latch_seed_cases']==720
 result={'status':'PASS','work':26,'adopted_build':'dialogue_kr_poc_024','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'plan_sha256':sha(read('workspace/translation/ui_rides_plan_001.json')),'scope':'Home train/water name drafts only; previous18 drafts and gate Japanese retained','source_units':54,'draft':20,'untranslated':34,'CHR_KiB':176,'ROM_size':len(rom),'reserved_remaining_KiB':6,'ExpectedWrites_whole_and_prior_admitted_changes_only':True,'source_fields_controls_macros_previous_fonts_and_gate_top_font_preserved':True,'native_reader':cycles,'CPU_ABI_cases':1504,'rebuild_actual_IPS_apply_equal':True,'matched_screens':total,'routes':routes,'outside_current_selection_rows_pixels':0,'game_RAM_except_two_font_latches_and_all_protected_PPU_OAM_equal':True,'actual_font_samples':observed,'actual_timing':timing,'visual_review':'Actual024 train1350 and water1200 viewed at integer4x; clean readable Korean; proper names and source explanatory suffix omitted in drafts pending final review','limits':['20 drafts are registered-source-row status, not whole-game percentage; other shared-macro consumers retain Japanese','v3 numeric header erratum preserved; numeric findings use rawRAM/native addresses; corrected v4 available','No gate Korean, top cards, successful exchange/gold success, full corpus/fullplay/audio/reset/savestate/physical console/final human review; prior PRG/RNG caveat','This run structurally preserves intro helper/font/text and title; fresh intro runtime not repeated; prior022 intro runtime belongs to022']}
 (ROOT/'qa/reports/rides024_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
