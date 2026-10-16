"""Independent whole-image, translation, native reader and matched real-Mesen gates."""
import csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageChops
from asm6502 import assemble
from verify_dialogue_home import reader
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def main():
 source_info=j('manifests/source_rom.json');source=read(source_info['path']);assert sha(source)==source_info['sha256']
 directory='build/dialogue_kr_poc_013';rom=read(directory+'/TinyToon2_dialogue_kr_poc.nes');report=j(directory+'/build_report.json');prior=read('build/dialogue_kr_poc_012/TinyToon2_dialogue_kr_poc.nes')
 assert sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']=='c516074626df8890900f8c2db532ae9d844aaeb6c775c5f17d53d5d55bea992a'
 assert len(rom)==409616 and rom[4:6]==bytes.fromhex('10 12')
 writes=j(directory+'/expected_writes.json');model=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not owned&region;owned|=region
  assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==rom
 info=j(directory+'/fourth_glyph_mapping.json');body=bytes.fromhex(info['body_hex']);fonts=bytearray(source[0x36810:0x37010])
 for code in [0x7a,*info['blank_macro_codes']]:fonts[code*16:(code+1)*16]=bytes(16)
 for g in info['glyphs']:fonts[g['code']*16:(g['code']+1)*16]=bytes.fromhex(g['chr_hex'])
 listing=j(directory+'/asm_listing.json');code,_,_=assemble(read(directory+'/page_font_used.asm').decode('utf-8'),0x95f9)
 assert sha(read(directory+'/page_font_used.asm'))==report['asm_sha256'] and len(code)==107
 def emitted(k):return b''.join(bytes.fromhex(x['hex']) for x in listing[k])
 assert emitted('helper')==code
 init=emitted('init_bootstrap').ljust(25,b'\xea');setup=emitted('setup_bootstrap').ljust(27,b'\xea')
 table=bytearray([0x5a]*256);selections={0x95f9:0x80,0x9615:0x84,0x963d:0x86,0x9655:0x88}
 for slot in range(48):table[2*slot]=selections.get(int.from_bytes(source[0x55a9+slot*2:0x55ab+slot*2],'little'),0x5a)
 assert bytes(table)==bytes.fromhex(listing['font_table_hex'])
 helper=bytearray(prior[0x4010:0x6010]);helper[0x15f9:0x168a]=source[0x5609:0x569a];helper[0x15f9:0x15f9+len(code)]=code;helper[0x1700:0x1800]=table;helper[0x1430:0x1449]=init;helper[0xe88:0xea3]=setup
 # This whole-image model admits ONLY the new helper, bootstraps, one text,
 # CHR length byte and appended font/padding; all other prior bytes must match.
 model=bytearray(prior);model[5]=0x12;model[0x4010:0x6010]=helper;model[0x25440:0x25459]=init;model[0x24e98:0x24eb3]=setup;model[0x25665:0x2568b]=body;model.extend(fonts+bytes(0x1800));assert bytes(model)==rom
 assert rom[0x40010:0x62010]==prior[0x40010:0x62010] and rom[0x261b1:0x261ff]==source[0x61b1:0x61ff]
 assert rom[0x1e168:0x1e258]==rom[0x3e168:0x3e258]==source[0x1e168:0x1e258]
 backup=read('backups/translation/text_ja_before_fourth_001.csv');assert sha(backup)=='ac801c8b980a2298cccc3108a14e03c64df2d959fe3eb8ffc48fe35777ebd2b9'
 before=list(csv.DictReader(io.StringIO(backup.decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));assert len(before)==len(after)==54
 for x,y in zip(before,after):
  for k in x:
   if x['entry_id']=='MAIN_05665' and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k],(x['entry_id'],k)
 assert sum(x['status']=='draft' for x in after)==5 and sum(x['status']=='untranslated' for x in after)==49
 assert read(directory+'/translation_used.csv')==read('workspace/translation/text_ja.csv') and sha(read(directory+'/translation_used.csv'))==report['csv_sha256']
 view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];cycles={}
 for ptr in (0x95f9,0x9615,0x963d,0x9655,0x9731):
  old,new=reader(source,ptr),reader(view,ptr);assert len(old)==len(new)
  assert all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(old,new));cycles[hex(ptr)]={'calls':len(new),'cycles':sum(x['cycles'] for x in new)}
 expanded=[x['value'] for x in reader(view,0x9655)];fe=expanded.index(0xfe);line1=bytes(expanded[:fe]).ljust(24,b'\0');line2=bytes(expanded[fe+1:-1]).ljust(24,b'\0');assert fe==22 and len(expanded)==44
 # Decode the expanded stream's glyph identity, with original macro five tiles blank.
 reverse={v:k for k,v in info['mapping'].items()};reverse.update({v:' ' for v in info['blank_macro_codes']});reverse[0]=' '
 assert ''.join(reverse[x] for x in line1).strip()==info['text'].split('\n')[0]
 assert ''.join(reverse[x] for x in line2).strip()==info['text'].split('\n')[1]
 assert read('build/dialogue_kr_poc_013_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 013/TinyToon2_fourth013_applied.nes')==rom
 routes={};total=0;font_samples=0
 for route in ('attract','start','introstart','preskip'):
  actual=ROOT/f'qa/dialogue/pages013_{route}';ref=ROOT/f'qa/dialogue/pages013_reference_{route}';ae=json.loads((actual/'environment.json').read_text('utf-8'));re=json.loads((ref/'environment.json').read_text('utf-8'))
  assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior) and ae['exit_code']==re['exit_code']==0
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted(actual.glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted(ref.glob('frame_*.png'))];changed=0
  for f in files:
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB'))
   if diff.getbbox():
    changed+=1;assert route!='start';diff.paste(0,(32,116,224,124));diff.paste(0,(32,132,224,140));assert diff.getbbox() is None,(route,f.name)
   tag=f.stem;r=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes();p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes()
   assert r[0x6cf]==rr[0x6cf] and r[0x6cd:0x6cf]==rr[0x6cd:0x6cf] and p[0x3f00:0x3f20]==rp[0x3f00:0x3f20] and (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes()
   nt=bytearray(p[0x2000:0x3000]);rnt=bytearray(rp[0x2000:0x3000])
   for off in (0x1e4,0x224,0x9e4,0xa24):nt[off:off+24]=rnt[off:off+24]
   assert nt==rnt,('Protected NT',route,tag)
   maps=list(csv.DictReader((actual/(tag+'_mapping.csv')).read_text().splitlines()));offset=int(next(x for x in maps if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
   if r[0xc6]==0x88 and offset==0x22000:assert p[:0x800]==fonts;font_samples+=1
  routes[route]={'samples':len(files),'fourth_two_rows_only_changes':changed,'whole_image_equal':len(files)-changed,'frames':ae['frames'],'start_frame':ae['input']['start_frame']};total+=len(files)
 for frame in (1790,4500):
  p=read(f'qa/dialogue/pages013_attract/frame_{frame:05d}_ppu.bin');r=read(f'qa/dialogue/pages013_attract/frame_{frame:05d}_ram.bin');assert p[0x21e4:0x21fc]==line1 and p[0x2224:0x223c]==line2 and r[0xc6]==0x88 and r[0x6cf]==5 and r[0x6cd:0x6cf]==bytes.fromhex('5596')
 # The native engine clears the first row1815, the second row1817.
 assert not any(read('qa/dialogue/pages013_attract/frame_01815_ppu.bin')[0x21e4:0x21fc])
 for frame in (1817,1821):
  p=read(f'qa/dialogue/pages013_attract/frame_{frame:05d}_ppu.bin');r=read(f'qa/dialogue/pages013_attract/frame_{frame:05d}_ram.bin');assert not any(p[0x21e4:0x21fc]+p[0x2224:0x223c]) and r[0xc6]==0x88
 for frame in (1822,4545):
  r=read(f'qa/dialogue/pages013_attract/frame_{frame:05d}_ram.bin');p=read(f'qa/dialogue/pages013_attract/frame_{frame:05d}_ppu.bin');assert r[0xc6]==0x5a and r[0x6cd:0x6cf]==bytes.fromhex('7b96') and p[:0x800]==source[0x36810:0x37010]
 for route in ('introstart','preskip'):
  r=read(f'qa/dialogue/pages013_{route}/frame_01800_ram.bin');assert r[0x6cf]==0 and r[0xc6]==0
 events=list(csv.DictReader((ROOT/'qa/dialogue/pages013_lifetime/page_events.csv').open()));active=None;balanced=0
 for e in events:
  if e['kind']!='exec':continue
  if e['address']=='9417':assert active is None;active=e
  if e['address']=='9445':assert active and all(e[k]==active[k] for k in ('sp','bank8000','bankA000','return_bank'));active=None;balanced+=1
 assert active is None and balanced==19
 traces=[]
 for name in ('pages013_reference_irq','pages013_irq'):
  entries=list(csv.DictReader((ROOT/f'qa/dialogue/{name}/irq_phase.csv').open()));traces.append([e for e in entries if e['kind']=='write' or (e['kind']=='exec' and e['address']=='FB97')])
 assert len(traces[0])==len(traces[1])>8000;substitutions=0
 for x,y in zip(*traces):
  assert all(x[k]==y[k] for k in ('frame','kind','address','scanline','dot','cycles')),(x,y)
  if x['value']!=y['value']:assert (x['address'],x['value'],y['value']) in [('A000','5A','88'),('A008','5B','89')];substitutions+=1
 cpu=j('qa/reports/pages013_hooks_1168.json');assert cpu['abi_cases']==1168 and cpu['all_page_cycles_equal_adopted008'] and font_samples>0
 result={'status':'PASS','adopted_build':'dialogue_kr_poc_013','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(directory+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':report['csv_sha256'],'source_units':54,'draft':5,'untranslated':49,'ROM_size':len(rom),'CHR_KiB':144,'expected_writes':len(writes),'whole_diff_bytes':report['whole_diff_bytes'],'entire_prior012_preserved_except_composed_fourth_changes':True,'all_original_macro_bytes_preserved':True,'rebuild_actual_IPS_apply_equal':True,'native_reader':cycles,'matched_screens':total,'routes':routes,'outside_fourth_rows_pixels':0,'palette_OAM_native_ids_pointers_equal':True,'actual_fourth_font_samples':font_samples,'balanced_runtime_page_returns':balanced,'actual_IRQ_timestamps_equal':len(traces[0]),'expected_fourth_font_register_substitutions':substitutions,'CPU_ABI_cases':1168,'lifetime':'Fourth pointer9655 latch88; FF increments ID5 without changing font; first row clears1815 and second1817, latch88 through1821; next init1821 callback restores5A, snapshot1822 pointer967B; repeated full page4500; Start1740 and1530 clear by1800 and restart intro','visual_review':'Separate direct native1790/4x and repeated4500, Japanese next1920, home1080 review; final human wording review pending','limits':['Development build, five drafts; 49 source units and total game corpus/scene mapping unresolved','No full playthrough, ride-transition, audio, reset/savestate or physical-console QA','Existing PRG expansion and RNG22 idle-iteration caveat retained; CPU model excludes async interrupts and real PPU','Font136/137 consumes2KiB of8KiB CHR growth; 6KiB reserved padding; global name macro untranslated outside this page','No release or external publishing']}
 (ROOT/'qa/reports/dialogue_fourth013_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
