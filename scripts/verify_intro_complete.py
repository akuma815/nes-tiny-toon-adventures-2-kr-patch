"""Independent full-prior-image, native-reader and matched runtime gates for intro014."""
import csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageChops
from verify_dialogue_home import reader
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def main():
 directory='build/dialogue_kr_poc_014';report=j(directory+'/build_report.json');pages=j(directory+'/intro_page_mapping.json');rom=read(directory+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes');m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256'] and sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']
 assert len(rom)==0x66010 and rom[4:6]==bytes.fromhex('10 13')
 expected=bytearray(source);owned=set();writes=j(directory+'/expected_writes.json')
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not owned&region;owned|=region;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 expected=bytearray(prior);expected.extend(bytes(len(rom)-len(prior)));expected[5]=19;fonts={};byfont={};byptr={};cycles={};view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010]
 for page in pages:
  p=page['profile'];start,end=p['file_offset'],p['end_exclusive'];body=bytes.fromhex(page['body_hex']);assert len(body)==end-start and body[-1]==255
  assert sha(source[start:end])==p['source_raw_sha256'];expected[start+0x20000:end+0x20000]=body;expected[0x5710+2*p['slot']]=p['font_bank']
  font=bytearray(source[0x36810:0x37010])
  for g in page['glyphs']:font[g['code']*16:(g['code']+1)*16]=bytes.fromhex(g['chr_hex'])
  off=0x40010+p['font_bank']*0x400;expected[off:off+0x800]=font;fonts[p['font_bank']]=bytes(font);byfont[p['font_bank']]=page;byptr[p['pointer']]=page
  old,new=reader(source,p['pointer']),reader(view,p['pointer']);assert len(old)==len(new) and all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(old,new));cycles[p['entry_id']]={'calls':len(new),'cycles':sum(x['cycles'] for x in new)}
  rawcontrols=[];newcontrols=[]
  def controls(b):
   out=[];i=0
   while i<len(b):
    c=b[i]
    if c==253:out.append((i,c,b[i+1]));i+=2
    else:
     if c>=0x7f:out.append((i,c))
     i+=1
   return out
  assert controls(source[start:end])==controls(body)
 assert bytes(expected)==rom # Whole prior image admitted changes only.
 assert rom[0x40010:0x62810]==prior[0x40010:0x62810] and rom[0x261b1:0x261ff]==source[0x61b1:0x61ff]
 for ptr in (0x95f9,0x9615,0x963d,0x9655,0x9731):
  a,b=reader(source,ptr),reader(view,ptr);assert len(a)==len(b) and all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(a,b))
 before=list(csv.DictReader(io.StringIO(read('backups/translation/text_ja_before_intro_complete_001.csv').decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));assert len(before)==len(after)==54
 keys={p['profile']['entry_id'] for p in pages}
 for x,y in zip(before,after):
  for k in x:
   if x['entry_id'] in keys and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k]
 assert sum(x['status']=='draft' for x in after)==10 and sum(x['status']=='untranslated' for x in after)==44
 assert read(directory+'/translation_used.csv')==read('workspace/translation/text_ja.csv') and sha(read(directory+'/translation_used.csv'))==report['csv_sha256']
 assert read('build/dialogue_kr_poc_014_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 014/TinyToon2_intro014_applied.nes')==rom
 routes={};samples=0;observed={str(k):0 for k in fonts}
 for route in ('attract','start','letterstart','villainstart'):
  actual=ROOT/f'qa/dialogue/intro014_{route}';ref=ROOT/f'qa/dialogue/intro014_reference_{route}';ae=json.loads((actual/'environment.json').read_text('utf-8'));re=json.loads((ref/'environment.json').read_text('utf-8'));assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior)
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention')) and ae['exit_code']==re['exit_code']==0
  files=sorted(actual.glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted(ref.glob('frame_*.png'))];changed=0
  for f in files:
   tag=f.stem;r=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes();p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes();font=r[0xc6];page=byfont.get(font)
   assert r[0x6cf]==rr[0x6cf] and r[0x6cd:0x6cf]==rr[0x6cd:0x6cf] and p[0x3f00:0x3f20]==rp[0x3f00:0x3f20] and (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes()
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB'));nt=bytearray(p[0x2000:0x3000]);rnt=bytearray(rp[0x2000:0x3000])
   if diff.getbbox():
    assert page and route!='start',(route,tag,font);changed+=1
    for row in range(len(page['layout'])):diff.paste(0,(32,116+16*row,224,124+16*row))
    assert diff.getbbox() is None,(route,tag)
   if page:
    for row in range(len(page['layout'])):
     for off in (0x1e4+0x40*row,0x9e4+0x40*row):nt[off:off+24]=rnt[off:off+24]
   assert nt==rnt,('protected nametables',route,tag)
   if page:
    maps=list(csv.DictReader((actual/(tag+'_mapping.csv')).read_text().splitlines()));offset=int(next(x for x in maps if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
    if offset==font*0x400:assert p[:0x800]==fonts[font];observed[str(font)]+=1
  routes[route]={'screens':len(files),'intro05_to09_rows_only_changes':changed,'whole_image_equal':len(files)-changed,'start_frame':ae['input']['start_frame'],'frames':ae['frames']};samples+=len(files)
 assert all(n>0 for n in observed.values())
 for frame in (1980,2160,2400,2640,2760,4704,4884,5124,5364,5484):
  r=read(f'qa/dialogue/intro014_attract/frame_{frame:05d}_ram.bin');p=read(f'qa/dialogue/intro014_attract/frame_{frame:05d}_ppu.bin');page=byptr[int.from_bytes(r[0x6cd:0x6cf],'little')];assert r[0xc6]==page['profile']['font_bank']
  for row,line in enumerate(page['layout']):assert p[0x21e4+row*0x40:0x21fc+row*0x40]==bytes.fromhex(line['expanded_hex']).ljust(24,b'\0')
 traces=[]
 for name in ('intro014_reference_irq','intro014_irq'):traces.append(list(csv.DictReader((ROOT/f'qa/dialogue/{name}/irq_phase.csv').open())))
 assert len(traces[0])==len(traces[1])>30000;changed=0
 for a,b in zip(*traces):
  assert all(a[k]==b[k] for k in ('frame','kind','address','scanline','dot','cycles')),(a,b)
  if a['value']!=b['value']:
   assert (a['address']=='A000' and a['value']=='5A' and int(b['value'],16) in fonts) or (a['address']=='A008' and a['value']=='5B' and int(b['value'],16)-1 in fonts);changed+=1
 events=list(csv.DictReader((ROOT/'qa/dialogue/intro014_lifetime/page_events.csv').open()));active=None;balanced=0;init_fonts={}
 for e in events:
  if e['kind']!='exec':continue
  if e['address']=='9417':assert active is None;active=e
  if e['address']=='9445':
   assert active and all(active[k]==e[k] for k in ('sp','bank8000','bankA000','return_bank'));ptr=int(e['pointer'],16)
   if ptr in byptr:assert int(e['C6'],16)==byptr[ptr]['profile']['font_bank'];init_fonts[e['pointer']]=init_fonts.get(e['pointer'],0)+1
   balanced+=1;active=None
 assert active is None and all(n>=2 for n in init_fonts.values()) and len(init_fonts)==5
 cpu=j('qa/reports/intro014_hooks1408.json');assert cpu['abi_cases']==1408 and cpu['initial_latch_seed_cases']==624
 result={'status':'PASS','adopted_build':'dialogue_kr_poc_014','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(directory+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':report['csv_sha256'],'source_units':54,'draft':10,'untranslated':44,'scope':'All9 observed natural intro paragraphs plus home and title003; development draft, not total-game completion','ROM_size':len(rom),'CHR_KiB':152,'expected_writes':len(writes),'prior013_entire_image_preserved_except_five_texts_font_table_five_fonts_CHR_header_and_padding':True,'all_global_macro_bytes_preserved':True,'rebuild_actual_IPS_apply_equal':True,'native_reader':cycles,'matched_screens':samples,'routes':routes,'outside_changed_intro_rows_pixels':0,'palette_OAM_native_ids_pointers_equal':True,'actual_font_samples':observed,'balanced_runtime_page_returns':balanced,'repeated_intro_pointer_initializations':init_fonts,'actual_IRQ_timestamps_equal':len(traces[0]),'expected_font_register_changes':changed,'CPU_ABI_cases':1408,'visual_review':'Source scenes and actual1980/2160/2400/2640/2760 inspected; Korean proper name, letter tone and final human review remain drafts','limits':['44 source units and total game text/graphics inventory unresolved','No full playthrough, audio, reset/savestate or physical-console QA','Home/ticket/stage dialogue font selection uses distinct IRQ; requires consumer survey before translation','PRG expansion and RNG22 idle-iteration caveat inherited; no release or external posting']}
 (ROOT/'qa/reports/intro014_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
