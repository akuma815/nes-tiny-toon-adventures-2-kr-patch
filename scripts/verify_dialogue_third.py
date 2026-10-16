"""Independent preserved008/runtime gate for third012; ROM bytes equal verified011."""
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
 directory='build/dialogue_kr_poc_012';b=ROOT/directory;rom=read(directory+'/TinyToon2_dialogue_kr_poc.nes');report=j(directory+'/build_report.json');assert sha(rom)==report['output_sha256'] and len(rom)==401424
 assert read('build/dialogue_kr_poc_011/TinyToon2_dialogue_kr_poc.nes')==rom # Only CSV context note differs; reuse byte-identical011 captures.
 prior=read('build/dialogue_kr_poc_008/TinyToon2_dialogue_kr_poc.nes');assert sha(prior)==report['prior_adopted_sha256']=='4d4b2f4ab979585432d44f52432d85cebc83afa4a25e58a2e692b0227351e314'
 expected=bytearray(source);owned=set();writes=j(directory+'/expected_writes.json')
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region
  assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 listing=j(directory+'/asm_listing.json')
 def code(k):return b''.join(bytes.fromhex(x['hex']) for x in listing[k])
 helper_code,_,_=assemble((b/'page_font_used.asm').read_text('utf-8'),0x95f9);assert helper_code==code('helper') and sha((b/'page_font_used.asm').read_bytes())==report['asm_sha256']
 irq,_,_=assemble((b/'font_irq_used.asm').read_text('utf-8'),0xfb97);assert irq==code('font_irq')
 base=read('build/dialogue_kr_poc_003/TinyToon2_dialogue_kr_poc.nes');assert sha(base)==report['base_sha256']
 helper=bytearray(base[0x4010:0x6010]);helper[0]=2;helper[0x15f9:0x15f9+len(helper_code)]=helper_code
 init=code('init_bootstrap').ljust(25,b'\xea');setup=code('setup_bootstrap').ljust(27,b'\xea');helper[0x1430:0x1449]=init;helper[0xe88:0xea3]=setup
 third=j(directory+'/third_glyph_mapping.json');body=bytes.fromhex(third['body_hex']);assert len(body)==24 and body[-1]==255 and body.count(0)==3
 fonts=bytearray(source[0x36810:0x37010]);fonts[0x7a*16:0x7b*16]=bytes(16)
 for g in third['glyphs']:fonts[g['code']*16:(g['code']+1)*16]=bytes.fromhex(g['chr_hex'])
 # Compare the entire adopted008 image, changing only these composed inputs.
 prior_model=bytearray(prior);prior_model[0x4010:0x6010]=helper;prior_model[0x25440:0x25459]=init;prior_model[0x24e98:0x24eb3]=setup;prior_model[0x2564d:0x25665]=body;prior_model[0x61810:0x62010]=fonts
 assert bytes(prior_model)==rom
 assert rom[0x40010:0x61810]==prior[0x40010:0x61810] and rom[0x3fb97:0x3fbe3]==prior[0x3fb97:0x3fbe3]
 assert rom[0x1e168:0x1e258]==rom[0x3e168:0x3e258]==source[0x1e168:0x1e258]
 before=list(csv.DictReader((ROOT/'backups/translation/text_ja_before_third_001.csv').open(encoding='utf-8-sig',newline='')))
 after=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(before)==len(after)==54
 for x,y in zip(before,after):
  for k in x:
   if x['entry_id']=='MAIN_0564D' and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k],(x['entry_id'],k)
 assert sum(x['status']=='draft' for x in after)==4 and sum(x['status']=='untranslated' for x in after)==50
 assert read(directory+'/translation_used.csv')==read('workspace/translation/text_ja.csv') and sha(read(directory+'/translation_used.csv'))==report['csv_sha256']
 view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];cycles={}
 for ptr in (0x95f9,0x9615,0x963d,0x9731):
  old=reader(source,ptr);new=reader(view,ptr);assert len(old)==len(new)
  assert all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(old,new))
  cycles[hex(ptr)]={'calls':len(new),'cycles':sum(x['cycles'] for x in new)}
 assert read('build/dialogue_kr_poc_012_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom
 assert read('qa/dialogue/한글 패치 적용 012/TinyToon2_third012_applied.nes')==rom
 routes={};total=0;font_samples=0
 for route in ('attract','start','introstart','preskip'):
  actual=ROOT/f'qa/dialogue/pages011_{route}';ref=ROOT/f'qa/dialogue/pages010_reference_{route}'
  ae=json.loads((actual/'environment.json').read_text('utf-8'));re=json.loads((ref/'environment.json').read_text('utf-8'));assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior)
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted(actual.glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted(ref.glob('frame_*.png'))];changed=0
  for f in files:
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB'))
   if diff.getbbox():changed+=1;assert route!='start';diff.paste(0,(32,116,224,124));assert diff.getbbox() is None,(route,f.name)
   tag=f.stem;r=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes();p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes()
   assert r[0x6cf]==rr[0x6cf] and r[0x6cd:0x6cf]==rr[0x6cd:0x6cf]
   assert p[0x3f00:0x3f20]==rp[0x3f00:0x3f20] and (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes()
   nt=bytearray(p[0x2000:0x3000]);rnt=bytearray(rp[0x2000:0x3000])
   for off in (0x1e4,0x9e4):nt[off:off+24]=rnt[off:off+24]
   assert nt==rnt,('NT protection',route,tag)
   maps=(actual/(tag+'_mapping.csv')).read_text();offset=int(next(x for x in csv.DictReader(maps.splitlines()) if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
   if r[0xc6]==0x86 and offset==0x21800:assert p[:0x800]==fonts;font_samples+=1
  routes[route]={'samples':len(files),'third_line_only_changes':changed,'whole_image_equal':len(files)-changed,'frames':ae['frames'],'start_frame':ae['input']['start_frame']};total+=len(files)
 for frame in (1560,4280):
  p=read(f'qa/dialogue/pages011_attract/frame_{frame:05d}_ppu.bin');r=read(f'qa/dialogue/pages011_attract/frame_{frame:05d}_ram.bin');assert p[0x21e4:0x21fc]==body[:-1]+b'\0' and not any(p[0x2224:0x223c]);assert r[0xc6]==0x86 and r[0x6cf]==4 and r[0x6cd:0x6cf]==bytes.fromhex('3d96')
 for frame in (1623,1629):
  p=read(f'qa/dialogue/pages011_attract/frame_{frame:05d}_ppu.bin');r=read(f'qa/dialogue/pages011_attract/frame_{frame:05d}_ram.bin');assert not any(p[0x21e4:0x21fc]) and r[0xc6]==0x86
 r=read('qa/dialogue/pages011_attract/frame_01630_ram.bin');p=read('qa/dialogue/pages011_attract/frame_01680_ppu.bin');assert r[0xc6]==0x5a and r[0x6cd:0x6cf]==bytes.fromhex('5596') and p[:0x800]==source[0x36810:0x37010]
 for route,frame in [('introstart',1680),('preskip',1440)]:
  r=read(f'qa/dialogue/pages011_{route}/frame_{frame:05d}_ram.bin');assert r[0x6cf]==0 and r[0xc6]==0
 events=list(csv.DictReader((ROOT/'qa/dialogue/pages011_lifetime/page_events.csv').open()));active=None;balanced=0
 for e in events:
  if e['kind']!='exec':continue
  if e['address']=='9417':assert active is None;active=e
  if e['address']=='9445':assert active and all(e[k]==active[k] for k in ('sp','bank8000','bankA000','return_bank'));active=None;balanced+=1
 assert active is None and balanced==19
 traces=[]
 for name in ('pages010_reference_irq','pages011_irq'):
  rows=list(csv.DictReader((ROOT/f'qa/dialogue/{name}/irq_phase.csv').open()));traces.append([e for e in rows if e['kind']=='write' or (e['kind']=='exec' and e['address']=='FB97')])
 assert len(traces[0])==len(traces[1])==8973;substitutions=0
 for x,y in zip(*traces):
  assert all(x[k]==y[k] for k in ('frame','kind','address','scanline','dot','cycles'))
  if x['value']!=y['value']:assert (x['address'],x['value'],y['value']) in [('A000','5A','86'),('A008','5B','87')];substitutions+=1
 cpu=j('qa/reports/pages011_hooks_final.json');assert cpu['abi_cases']==1072 and cpu['all_page_cycles_equal_adopted008']
 result={'status':'PASS','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(directory+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':report['csv_sha256'],'source_units':54,'draft':4,'untranslated':50,'ROM_size':len(rom),'expected_writes':len(writes),'whole_diff_bytes':report['whole_diff_bytes'],'entire_prior008_preserved_except_composed_third_changes':True,'rebuild_actual_IPS_apply_equal':True,'native_reader':cycles,'matched_screens':total,'routes':routes,'outside_third_line_pixels':0,'palette_OAM_native_ids_pointers_equal':True,'actual_third_font_samples':font_samples,'balanced_runtime_page_returns':balanced,'actual_IRQ_timestamps_equal':8973,'expected_third_font_register_substitutions':substitutions,'CPU_ABI_cases':1072,'lifetime':'FF advances ID while font86 retained; clear1623; native next-init1629 callback restores5A; snapshot1630 new pointer9655; repeated third4280; Start1530 clears by1680 and restarts intro; Start1300 clears by1440','visual_review':'Native third1560 and4280, Japanese fourth1680 and home1080 inspected separately; final human wording review pending','limits':['Development build, four drafts; 50 source units and remaining scene mapping unresolved','No full playthrough, audio, reset/savestate or physical-console QA','Existing PRG expansion and RNG22 idle-iteration caveat unchanged; CPU model excludes async interrupts and real PPU','Third font consumes last2KiB CHR padding; further fonts require planned CHR growth','No release or external publishing']}
 result.update(adopted_build='dialogue_kr_poc_012',runtime_capture_build='dialogue_kr_poc_011',runtime_capture_ROM_byte_identical_to_adopted=True)
 (ROOT/'qa/reports/dialogue_third012_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
