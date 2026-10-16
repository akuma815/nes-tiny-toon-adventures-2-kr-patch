"""Independent guarded-image and full-frame runtime checks for font latch015."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
from asm6502 import assemble
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def main():
 d='build/dialogue_kr_poc_017';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes');report=j(d+'/build_report.json');m=j('manifests/source_rom.json');source=read(m['path'])
 assert sha(source)==m['sha256'] and sha(prior)==report['prior_adopted_sha256'] and sha(rom)==report['output_sha256']
 model=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==rom
 helper,_,symbols=assemble(read(d+'/page_font_used.asm').decode('utf-8'),0x95f9)
 home,_,_=assemble('LDA $06F3',0xfb12)
 home_init,_,_=assemble(read(d+'/home_font_used.asm').decode('utf-8'),0x9800)
 home_boot,_,_=assemble('LDA #$02\nJSR $FE00\nJSR $9800',0x9b0f)
 init,_,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @page_init\nPLA\nSTA $2B\nLDA $06CE\nPLP\nLDY #$00\nRTS',0x9430,symbols)
 setup,_,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @intro_setup\nPLA\nSTA $2B\nPLP\nLDA #$01\nLDY #$FF\nCLC\nCLV\nINC $06DE\nRTS',0x8e88,symbols)
 model=bytearray(prior);model[0x5609:0x5609+len(helper)]=helper;model[0x5710+20]=130;model[0x4010]=2;model[0x5810:0x5810+len(home_init)]=home_init
 for base in (0x10,0x20010):
  model[base+0x5430:base+0x5449]=init.ljust(25,b'\xea');model[base+0x4e88:base+0x4ea3]=setup.ljust(27,b'\xea');model[base+0x1fb12:base+0x1fb15]=home;model[base+0x5b0f:base+0x5b17]=home_boot
 assert bytes(model)==rom and len(helper)==107 and len(home)==3
 assert rom[:0x10]==prior[:0x10] and rom[0x40010:]==prior[0x40010:]
 assert read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_014/translation_used.csv')
 assert read('build/dialogue_kr_poc_017_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 017/TinyToon2_latch017_applied.nes')==rom
 counts={};total=0;writes={};profiles=set()
 for a,b in [('latch015_reference_tour','latch017_tour'),('latch015_reference_ticket','latch017_ticket'),('intro014_attract','latch017_attract'),('intro014_letterstart','latch017_letterstart'),('intro014_villainstart','latch017_villainstart')]:
  ref=ROOT/'qa/dialogue'/a;actual=ROOT/'qa/dialogue'/b;ae=j(f'qa/dialogue/{b}/environment.json');re=j(f'qa/dialogue/{a}/environment.json')
  assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior) and ae['exit_code']==re['exit_code']==0
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted(actual.glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted(ref.glob('frame_*.png'))]
  changed_chr=0
  for f in files:
   tag=f.stem;assert ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB')).getbbox() is None,(b,tag)
   p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes();r=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes()
   assert p[0x800:]==rp[0x800:] and (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes(),(b,tag,'protected PPU/OAM')
   assert r[0x6cd:0x6d0]==rr[0x6cd:0x6d0] and r[0x6ea]==rr[0x6ea] and r[0xc7]==rr[0xc7]
   maps=rows(f'qa/dialogue/{b}/{tag}_mapping.csv')
   for entry in maps:
    if entry['kind']=='chr':
     address=int(entry['cpu_or_ppu_address'],16);off=int(entry['relative_offset'],16)+0x40010
     assert p[address:address+0x400]==rom[off:off+0x400],(b,tag,address)
   if p[:0x800]!=rp[:0x800]:changed_chr+=1
   if b in ('latch017_tour','latch017_ticket') and int(tag[6:])>=930:profiles.add(r[0x6ea]);assert r[0x6f3]==r[0xc6],(b,tag,'encoded font')
  if b in ('latch017_tour','latch017_ticket'):
   old=rows(f'qa/dialogue/{a}/menu_events.csv');new=rows(f'qa/dialogue/{b}/menu_events.csv');x=[e for e in old if e['kind']=='exec'];y=[e for e in new if e['kind']=='exec'];assert len(x)==len(y)
   for u,v in zip(x,y):assert all(u[k]==v[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc')),(u,v)
   latch=[e for e in new if e['address']=='06F3' and e['kind']=='write'];assert {e['pc'] for e in latch}=={'FE40','CFB4','9616','980E'}
   assert all(int(e['value'],16)==int(e['font'],16) for e in latch if e['pc']=='9616');writes[b]={'latch_writes':len(latch),'native_clear_writes':sum(e['pc'] in ('FE40','CFB4') for e in latch),'balanced_init_returns':len(x)//2}
  counts[b]={'screens':len(files),'whole_image_equal':len(files),'lower_unused_CHR_bank_differences':changed_chr};total+=len(files)
 assert profiles=={0,1,2}
 phases={}
 for route in ('tour','ticket'):
  a=f'latch015_reference_{route}_irq';b=f'latch017_{route}_irq';ae=j(f'qa/dialogue/{b}/environment.json');re=j(f'qa/dialogue/{a}/environment.json')
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention')) and ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior)
  x=rows(f'qa/dialogue/{a}/irq_phase.csv');y=rows(f'qa/dialogue/{b}/irq_phase.csv');assert len(x)==len(y)>10000;changed=0
  for u,v in zip(x,y):
   assert all(u[k]==v[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(u,v)
   if u['value']!=v['value']:
    assert (u['address'],u['value'],v['value']) in {('A000','82','5A'),('A008','83','5B')},(u,v);changed+=1
  phases[route]={'actual_IRQ_PPU_mapper_timestamps_equal':len(x),'expected_lower_font_changes':changed}
 intro_old=rows('qa/dialogue/intro014_irq/irq_phase.csv');intro_new=rows('qa/dialogue/latch017_intro_irq/irq_phase.csv');assert intro_old==intro_new and len(intro_old)==41034
 phases['intro']={'actual_IRQ_PPU_mapper_timestamps_equal':len(intro_old),'expected_lower_font_changes':0}
 cpu=j('qa/reports/latch017_hooks1408.json');assert cpu['abi_cases']==1408 and cpu['initial_latch_seed_cases']==624 and report['home_IRQ_font_profile_cases']==36
 result={'status':'PASS','adopted_build':'dialogue_kr_poc_017','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':report['csv_sha256'],'scope':'Work18 native-read lower-font latch infrastructure; no new text/art;10 draft44 untranslated','whole_prior_image_admitted_changes_only':True,'original_header_CHR_fonts_text_macros_preserved':True,'rebuild_actual_IPS_apply_equal':True,'CPU_ABI_cases':1408,'page_seed_cases':624,'home_IRQ_font_profile_cases':36,'home_init_ABI_cases':report['home_init_ABI_cases'],'home_init_added_cycles':76,'matched_screens':total,'outside_text_pixels':0,'whole_frame_pixel_differences':0,'routes':counts,'profiles_observed':sorted(profiles),'latch_writes':writes,'actual_timing':phases,'visual_review':'Actual home greeting, booth welcome and cart instructions reviewed; all frames mechanically equal prior014','limits':['06F3 active ownership and native PPU2002 reads retained; ownership verified only on recorded intro/home/booth/cart routes','Other stages, variables, successful ticket exchange, graphics and full corpus remain pending','No full playthrough/audio/reset/savestate/physical-console/final human review','Prior PRG expansion and RNG22 idle-loop caveat inherited; not a release']}
 (ROOT/'qa/reports/latch017_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
