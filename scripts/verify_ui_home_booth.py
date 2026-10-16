"""Independent text/font reconstruction and narrowly bounded real-scene UI gates."""
import csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageChops
from extract_title_png import decode
from verify_dialogue_home import reader
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def main():
 d='build/dialogue_kr_poc_020';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_019/TinyToon2_dialogue_kr_poc.nes');report=j(d+'/build_report.json');plan=j(d+'/plan_used.json');pages=j(d+'/ui_korean_page_mapping.json');m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256'] and sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']
 expected=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 expected=bytearray(prior);expected.extend(bytes(len(rom)-len(prior)));expected[5]=21;byfont={};fonts={};cycles={};atlas=Image.open(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010]
 for page in pages:
  p=page['profile'];start,end=p['source_file_offset'],p['end_exclusive'];body=bytes.fromhex(page['body_hex']);assert len(body)==end-start and sha(source[start:end])==p['source_raw_sha256'];expected[start+0x20000:end+0x20000]=body;expected[0x5710+2*p['slot']]=p['font_bank']
  font=bytearray(prior[0x65010:0x65810]);reverse={0:' '}
  for g in page['glyphs']:
   raw=bytes.fromhex(g['chr_hex']);c=g['char'];code=g['code'];reverse[code]=c
   if c==' ':assert raw==bytes(16)
   elif c in plan['native_punctuation']:
    old=plan['native_punctuation'][c];assert raw==source[0x36810+old*16:0x36810+(old+1)*16]
   else:
    assert '\uac00'<=c<='\ud7a3';n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=bytes(2*int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data());assert any(bits) and decode(raw)==bits
   font[code*16:(code+1)*16]=raw
  for code in (0,*range(0x41,0x4b),*range(0x70,0x7a)):assert font[code*16:(code+1)*16]==source[0x36810+code*16:0x36810+(code+1)*16]
  off=0x40010+p['font_bank']*0x400;expected[off:off+0x800]=font;fonts[p['font_bank']]=bytes(font);byfont[p['font_bank']]=page
  a,b=reader(oldview,p['pointer']),reader(view,p['pointer']);assert len(a)==len(b) and all(all(u[k]==v[k] for k in ('cycles','cursor','buffer_cursor')) for u,v in zip(a,b));actual=[];line=[]
  for event in b:
   if event['value'] in (0xfe,0xff):actual.append(''.join(line));line=[]
   else:line.append(reverse[event['value']])
  assert actual==[row['desired'] for row in page['layout']]
  # All macro/control positions and literal-zero positions stay exact.
  oldbody=prior[start+0x20000:end+0x20000]
  def controls(data):
   i=0;out=[]
   while i<len(data):
    v=data[i]
    if v==253:out.append((i,v,data[i+1]));i+=2
    else:
     if v==0 or v>=127:out.append((i,v))
     i+=1
   return out
  assert controls(oldbody)==controls(body);cycles[p['entry_id']]={'calls':len(b),'cycles':sum(e['cycles'] for e in b)}
 assert bytes(expected)==rom and len(rom)==0x6a010 and rom[4:6]==bytes.fromhex('10 15') and not any(rom[0x69810:])
 assert rom[0x40010:0x65810]==prior[0x40010:0x65810] and rom[0x261b1:0x261ff]==prior[0x261b1:0x261ff]
 before=list(csv.DictReader(io.StringIO(read('backups/translation/text_ja_before_ui_home_booth_001.csv').decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));keys={p['profile']['entry_id'] for p in pages};assert len(before)==len(after)==54
 for a,b in zip(before,after):
  for k in a:
   if a['entry_id'] in keys and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert a[k]==b[k]
 assert sum(r['status']=='draft' for r in after)==18 and sum(r['status']=='untranslated' for r in after)==36 and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')
 assert read('build/dialogue_kr_poc_020_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 020/TinyToon2_ui020_applied.nes')==rom
 observed={str(font):0 for font in fonts};routes={};total=0
 for route in ('tour','ticket'):
  actual=ROOT/f'qa/dialogue/ui020_{route}';ref=ROOT/f'qa/dialogue/macro019_{route}';ae=j(f'qa/dialogue/ui020_{route}/environment.json');re=j(f'qa/dialogue/macro019_{route}/environment.json');assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior) and ae['exit_code']==re['exit_code']==0 and all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted(actual.glob('frame_*.png'));assert [f.name for f in files]==[f.name for f in sorted(ref.glob('frame_*.png'))];changed=0
  for f in files:
   tag=f.stem;r=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes();p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes();font=r[0xc6];page=byfont.get(font)
   assert r[0x6cd:0x6d0]==rr[0x6cd:0x6d0] and r[0x6ea]==rr[0x6ea] and r[0xc7]==rr[0xc7] and r[0x34:0x3a]==rr[0x34:0x3a] and p[0x3f00:0x3f20]==rp[0x3f00:0x3f20] and (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes()
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB'));nt=bytearray(p[0x2000:0x3000]);rnt=bytearray(rp[0x2000:0x3000])
   if diff.getbbox():assert page,(route,tag,font);changed+=1
   if page:
    for row,line in enumerate(page['layout']):
     # Native UI logical NT22A8; scroll produces screen top163; each line advances40h.
     diff.paste(0,(64,163+16*row,64+8*line['expanded_tiles'],171+16*row))
     for alias in range(0,0x1000,0x400):
      off=alias+0x2a8+0x40*row;nt[off:off+line['expanded_tiles']]=rnt[off:off+line['expanded_tiles']]
   assert diff.getbbox() is None,(route,tag,'outside current native row',diff.getbbox())
   assert nt==rnt,(route,tag,'protected nametables')
   maps=rows(f'qa/dialogue/ui020_{route}/{tag}_mapping.csv');off=int(next(e for e in maps if e['kind']=='chr' and e['cpu_or_ppu_address']=='0000')['relative_offset'],16)
   if page and off==font*0x400:assert p[:0x800]==fonts[font];observed[str(font)]+=1
  old=[e for e in rows(f'qa/dialogue/macro019_{route}/menu_events.csv') if e['kind']=='exec'];new=[e for e in rows(f'qa/dialogue/ui020_{route}/menu_events.csv') if e['kind']=='exec'];assert len(old)==len(new)
  for a,b in zip(old,new):assert all(a[k]==b[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc'))
  routes[route]={'screens':len(files),'changed_current_paragraph_rows':changed,'whole_frame_equal':len(files)-changed};total+=len(files)
 assert all(n>0 for n in observed.values())
 timing={};selected_banks=set(fonts)
 for route in ('tour','ticket'):
  a=rows(f'qa/dialogue/macro019_{route}_irq/irq_phase.csv');b=rows(f'qa/dialogue/ui020_{route}_irq/irq_phase.csv');assert len(a)==len(b)>30000;changed=0
  for x,y in zip(a,b):
   assert all(x[k]==y[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(x,y)
   if x['value']!=y['value']:
    assert (x['address']=='A000' and x['value']=='94' and int(y['value'],16) in selected_banks) or (x['address']=='A008' and x['value']=='95' and int(y['value'],16)-1 in selected_banks),(x,y);changed+=1
  timing[route]={'actual_IRQ_NMI_PPU_mapper_timestamps_equal':len(a),'private_font_changes_only':changed}
 cpu=j('qa/reports/ui020_hooks1408.json');assert cpu['abi_cases']==1408
 result={'status':'PASS','adopted_build':'dialogue_kr_poc_020','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':report['csv_sha256'],'source_units':54,'draft':18,'untranslated':36,'scope':'Work21 eight observed lower-window home/booth drafts; title and all9 intro retained; other UI Japanese passthrough','CHR_KiB':168,'ROM_size':len(rom),'whole_prior_image_admitted_changes_only':True,'all_existing_fonts_macros_stage_NMI_font_preserved':True,'rebuild_actual_IPS_apply_equal':True,'CPU_ABI_cases':1408,'native_reader':cycles,'matched_screens':total,'routes':routes,'outside_current_native_UI_rows_pixels':0,'protected_nametables_palette_OAM_native_indices_pointers_head_font_equal':True,'actual_font_samples':observed,'actual_timing':timing,'visual_review':'Pending actual8-page review','limits':['Selection shows names only; original explanatory suffix omitted to preserve macro83 leading00 and natural Korean spacing; final proper-name/service-tone review pending','Macro SSOT entries retain untranslated status because other consumers still Japanese; counts are registered source rows, not whole-game percentage','Other rides, gate, variables/successful exchange, top instruction cards, English picture boards/credits remain pending','No full playthrough/audio/reset/savestate/physical console; prior PRG/RNG caveat; development only']}
 (ROOT/'qa/reports/ui020_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
