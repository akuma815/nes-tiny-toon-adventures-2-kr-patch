"""Independent protected-region, SSOT, native reader and matched runtime gate for pages008."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
from asm6502 import assemble
from verify_dialogue_home import reader
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return (ROOT/p).read_bytes()
def j(p):return json.loads(read(p).decode('utf-8'))
def main():
 m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256']
 b=ROOT/'build/dialogue_kr_poc_008';rom=(b/'TinyToon2_dialogue_kr_poc.nes').read_bytes();report=j('build/dialogue_kr_poc_008/build_report.json');assert sha(rom)==report['output_sha256'] and len(rom)==401424
 base=read('build/dialogue_kr_poc_003/TinyToon2_dialogue_kr_poc.nes');assert sha(base)==report['base_sha256']
 expected=bytearray(source);owned=set();writes=j('build/dialogue_kr_poc_008/expected_writes.json')
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region
  assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 # Independently restrict the large extension write to known mirror modifications.
 listing=j('build/dialogue_kr_poc_008/asm_listing.json')
 def code(k):return b''.join(bytes.fromhex(x['hex']) for x in listing[k])
 helper_code,_,_=assemble((b/'page_font_used.asm').read_text('utf-8'),0x95f9)
 assert helper_code==code('helper') and sha((b/'page_font_used.asm').read_bytes())==report['asm_sha256']
 irq,_,_=assemble((b/'font_irq_used.asm').read_text('utf-8'),0xfb97);assert irq==code('font_irq')
 helper=bytearray(base[0x4010:0x6010]);helper[0]=2;helper[0x15f9:0x15f9+len(helper_code)]=helper_code
 init=code('init_bootstrap').ljust(25,b'\xea');setup=code('setup_bootstrap').ljust(27,b'\xea')
 helper[0x1430:0x1449]=init;helper[0xe88:0xea3]=setup;assert rom[0x4010:0x6010]==helper
 mirrors=bytearray(base[0x10:0x20010]);mirrors[0x5430:0x5449]=init;mirrors[0x4e88:0x4ea3]=setup
 mapping=j('build/dialogue_kr_poc_008/second_glyph_mapping.json');body=bytes.fromhex(mapping['body_hex']);assert len(body)==40
 mirrors[0x5615:0x563d]=body;mirrors[0x1fb97:0x1fbe3]=irq;assert rom[0x20010:0x40010]==mirrors
 low=bytearray(base[:0x20010]);low[4]=16;low[0x4010:0x6010]=helper;assert rom[:0x20010]==low
 assert rom[0x40010:0x60010]==base[0x20010:0x40010] # All original CHR, including title003.
 assert rom[0x60010:0x61010]==base[0x40010:0x41010] # First and home clones.
 second=bytearray(source[0x36810:0x37010]);second[0x7a*16:0x7b*16]=bytes(16)
 for g in mapping['glyphs']:second[g['code']*16:(g['code']+1)*16]=bytes.fromhex(g['chr_hex'])
 assert rom[0x61010:0x61810]==second and rom[0x61810:]==bytes(0x800)
 assert rom[0x1e168:0x1e258]==rom[0x3e168:0x3e258]==source[0x1e168:0x1e258]
 old=list(csv.DictReader((ROOT/'backups/translation/text_ja_before_pages_001.csv').open(encoding='utf-8-sig',newline='')))
 new=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(old)==len(new)==54
 for x,y in zip(old,new):
  for k in x:
   if x['entry_id']=='MAIN_05625' and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k],(x['entry_id'],k)
 assert sum(x['status']=='draft' for x in new)==3 and sum(x['status']=='untranslated' for x in new)==51
 assert sha(read('workspace/translation/text_ja.csv'))==report['csv_sha256']
 view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];cycles={}
 for ptr in (0x95f9,0x9615,0x9731):
  original=reader(source,ptr);modified=reader(view,ptr);assert len(original)==len(modified)
  assert all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(original,modified))
  cycles[hex(ptr)]={'calls':len(modified),'cycles':sum(x['cycles'] for x in modified)}
 assert read('build/dialogue_kr_poc_008_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom
 assert read('qa/dialogue/한글 패치 적용 008/TinyToon2_pages008_applied.nes')==rom
 routes={};total=0;font_samples=0
 for route in ('attract','start','introstart'):
  actual=ROOT/f'qa/dialogue/pages008_{route}';ref=ROOT/f'qa/dialogue/pages008_reference_{route}'
  ae=json.loads((actual/'environment.json').read_text('utf-8'));re=json.loads((ref/'environment.json').read_text('utf-8'))
  assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(base)
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted(actual.glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted(ref.glob('frame_*.png'))]
  changes=0;equal=0
  for f in files:
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB'))
   if diff.getbbox():changes+=1;assert route!='start';diff.paste(0,(32,116,224,124));diff.paste(0,(32,132,224,140));assert diff.getbbox() is None,f.name
   else:equal+=1
   tag=f.stem;r=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes();p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes()
   assert r[0x6cf]==rr[0x6cf] and r[0x6cd:0x6cf]==rr[0x6cd:0x6cf]
   assert p[0x3f00:0x3f20]==rp[0x3f00:0x3f20] and (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes()
   nt=bytearray(p[0x2000:0x3000]);rnt=bytearray(rp[0x2000:0x3000])
   for off in (0x1e4,0x224,0x9e4,0xa24):nt[off:off+24]=rnt[off:off+24]
   assert nt==rnt,('NT protection',route,tag)
   maps=(actual/(tag+'_mapping.csv')).read_text();first=next(x for x in csv.DictReader(maps.splitlines()) if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000');offset=int(first['relative_offset'],16)
   if route!='start' and offset in (0x20000,0x21000,0x16800) and r[0xc6] in (0x80,0x84,0x5a):
    assert offset==r[0xc6]*1024 and p[:0x800]==rom[0x40010+offset:0x40810+offset];font_samples+=1
  routes[route]={'samples':len(files),'text_only_changes':changes,'whole_image_equal':equal,'frames':ae['frames'],'start_frame':ae['input']['start_frame']};total+=len(files)
 # Native rendered24-cell rows must equal the actual reader's decoded output.
 values=[x['value'] for x in reader(view,0x9615)];sep=values.index(0xfe);lines=[bytes(values[:sep]),bytes(values[sep+1:-1])]
 for frame in (1320,4040):
  p=read(f'qa/dialogue/pages008_attract/frame_{frame:05d}_ppu.bin')
  for off,line in zip((0x21e4,0x2224),lines):assert p[off:off+24]==line.ljust(24,b'\0')
 for frame,font,pointer in ((1080,0x80,0x95f9),(1103,0x80,0x95f9),(1108,0x84,0x9615),(1320,0x84,0x9615),(1440,0x5a,0x963d),(3720,0x80,0x95f9),(4040,0x84,0x9615)):
  r=read(f'qa/dialogue/pages008_attract/frame_{frame:05d}_ram.bin');assert r[0xc6]==font and r[0x6cd]+256*r[0x6ce]==pointer
 for frame in (1103,1107):
  p=read(f'qa/dialogue/pages008_attract/frame_{frame:05d}_ppu.bin');assert not any(p[0x21e4:0x21fc]+p[0x2224:0x223c])
 r=read('qa/dialogue/pages008_introstart/frame_01440_ram.bin');assert r[0x6cf]==0 and r[0xc6]==0 # Actual Start skip cleared the scene.
 events=list(csv.DictReader((ROOT/'qa/dialogue/pages008_lifetime_v2/page_events.csv').open()))
 active=None;completed=[]
 for e in events:
  if e['kind']!='exec':continue
  if e['address']=='9417':assert active is None;active=e
  if e['address']=='9445':
   assert active and all(e[k]==active[k] for k in ('sp','bank8000','bankA000','return_bank'));completed.append(e);active=None
 assert active is None and len(completed)>10
 irq_events=[e for e in events if e['kind']=='exec' and e['address']=='FB97'];assert irq_events
 phases=[]
 for name in ('irq_phase003','irq_phase008'):
  rows=list(csv.DictReader((ROOT/f'qa/dialogue/{name}/irq_phase.csv').open()))
  phases.append([(e['frame'],e['kind'],e['address'],e['value'],e['scanline'],e['dot'],e['cycles']) for e in rows if e['kind']=='write' or (e['kind']=='exec' and e['address']=='FB97')])
 assert phases[0]==phases[1] and len(phases[0])==2820
 result={'status':'PASS','source_sha256':sha(source),'output_sha256':sha(rom),'ips_sha256':sha((b/'TinyToon2_dialogue_kr_poc.ips').read_bytes()),'csv_sha256':report['csv_sha256'],'source_units':54,'draft':3,'untranslated':51,'protected_mirrors_original_CHR_title_and_clones_equal':True,'shared_zero_asset_preserved':True,'expected_writes':len(writes),'rebuild_actual_IPS_apply_equal':True,'native_reader':cycles,'matched_screens':total,'routes':routes,'outside_text_pixels':0,'palette_OAM_ids_pointer_equal':True,'native_NT_rendered_rows_equal_reader':True,'actual_font_samples':font_samples,'balanced_runtime_page_returns':len(completed),'latch_lifetime':'FF advances id while font remains; rows clear1103; completed native pointer1107 callback selects84; original5A on third init1431; natural repeat first/second restored; Start1300 clears scene','ABI_report':'pages008_hooks_aligned.json','visual_review':'Directly reviewed native1320,1560,4040 and home1080; second two lines legible; third Japanese fallback and reentry observed. Final human translation/title approval pending.','limits':['Development only; three translation drafts','51 source units untranslated; remaining scene mappings incomplete','CPU test excludes async interrupts and PPU; runtime observed bounded native paths only','RNG22 idle-loop iteration count can change despite phase alignment; unobserved gameplay/audio/reset/savestate/physical hardware not tested','No full playthrough or release package']}
 result.update(ABI_report='pages008_hooks_final.json',actual_IRQ_entry_and_write_timestamps_equal=2820)
 (ROOT/'qa/reports/dialogue_pages008_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
