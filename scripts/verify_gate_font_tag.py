"""Independent whole-image, official6502 and exact real-execution checks for tag027."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
from asm6502 import assemble
from verify_gate_font_tag_hooks import Memory,MPU
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def env(prefix,rom):
 e=j('qa/dialogue/'+prefix+'/environment.json');assert e['exit_code']==0 and e['rom_sha256']==sha(rom)
 for n,h in e['files'].items():assert sha(read('qa/dialogue/'+prefix+'/'+n))==h,(prefix,n)
 return e
def run(rom,slot,phase,active,mode):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x9417;c.sp=0xfd;c.a=0;c.x=0x73;c.y=0x92;c.p=0x34;m.ram[0x1fe:0x200]=bytes.fromhex('ff c0');m.ram[0x2b]=0x36;m.ram[0x6cf]=slot;m.ram[0x6df]=phase;m.ram[0xc6]=active;m.ram[0x6f3]=active;m.ram[0x34]=90;m.ram[0x6d0]=mode
 while c.pc!=0xc100:c.step();assert c.processorCycles<10000
 return c,m

def main():
 d='build/dialogue_kr_poc_027';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_024/TinyToon2_dialogue_kr_poc.nes');old22=read('build/dialogue_kr_poc_022/TinyToon2_dialogue_kr_poc.nes');meta=j('manifests/source_rom.json');source=read(meta['path']);assert sha(source)==meta['sha256'];model=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not owned&area;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==rom;code,_,symbols=assemble(read('workspace/asm/dialogue_page_font_008.asm').decode('utf-8'),0x95f9);assert len(code)==135 and 0x95f9+len(code)<0x9700;expected=bytearray(prior);expected[0x5609:0x5609+len(code)]=code
 init,_,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @page_init\nPLA\nSTA $2B\nLDA $06CE\nPLP\nLDY #$00\nRTS',0x9430,symbols)
 setup,_,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @intro_setup\nPLA\nSTA $2B\nPLP\nLDA #$01\nLDY #$FF\nCLC\nCLV\nINC $06DE\nRTS',0x8e88,symbols)
 for base in (0x10,0x20010):expected[base+0x5430:base+0x5449]=init.ljust(25,b'\xea');expected[base+0x4e88:base+0x4ea3]=setup.ljust(27,b'\xea')
 gate_slots=(22,23,24,25,26,27,28,44);off=0x40010+171*0x400;assert not any(prior[off:off+0x800]);expected[off:off+0x800]=prior[0x65010:0x65810]
 for slot in gate_slots:assert prior[0x5710+2*slot]==148;expected[0x5710+2*slot]=171
 assert bytes(expected)==rom and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_024/translation_used.csv')
 assert read('build/dialogue_kr_poc_027_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 027/TinyToon2_tag027_applied.nes')==rom
 cases=0
 for slot in range(48):
  for phase in (0,1,3,4):
   for active in (90,148,166):
    for mode in (0,16,18):
     a,am=run(prior,slot,phase,active,mode);b,bm=run(rom,slot,phase,active,mode);assert (a.a,a.x,a.y,a.sp,a.p,a.processorCycles)==(b.a,b.x,b.y,b.sp,b.p,b.processorCycles) and am.banks==bm.banks
     assert all(am.ram[i]==bm.ram[i] for i in range(2048) if i not in (0x34,0xc6,0x6f3) and not 0x100<=i<0x200)
     assert bm.ram[0x34]==(171 if slot in gate_slots else 90);assert bm.ram[0xc6]==bm.ram[0x6f3]==(171 if slot in gate_slots else am.ram[0xc6]);cases+=1
 hooks=j('qa/reports/tag027_hooks1504.json');assert hooks['abi_cases']==1504 and hooks['initial_latch_seed_cases']==720
 # Original22 intro payload/fonts match024; reuse that frozen runtime reference with explicit byte proof.
 assert prior[0x25609:0x25741]==old22[0x25609:0x25741] and prior[0x60010:0x65810]==old22[0x60010:0x65810] and prior[0x40010:0x60010]==old22[0x40010:0x60010]
 routes={};total=0
 for route,ref,refrom in [('castle','commit024_castle',prior),('attract','ui022_attract',old22),('tour','ui022_tour',old22),('ticket','ui022_ticket',old22)]:
  prefix='tag027_'+route;ae=env(prefix,rom);re=env(ref,refrom);assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted((ROOT/'qa/dialogue'/prefix).glob('frame_*.png'));assert [f.name for f in files]==[f.name for f in sorted((ROOT/'qa/dialogue'/ref).glob('frame_*.png'))]
  for f in files:
   a='qa/dialogue/'+prefix+'/'+f.stem;b='qa/dialogue/'+ref+'/'+f.stem;assert ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ROOT/(b+'.png')).convert('RGB')).getbbox() is None,(route,f.name)
   assert read(a+'_ppu.bin')==read(b+'_ppu.bin') and read(a+'_oam.bin')==read(b+'_oam.bin')
   ram=read(a+'_ram.bin');rr=read(b+'_ram.bin');assert all(ram[i]==rr[i] for i in range(2048) if i not in (0x34,0x3a,0xc6,0x6f3) and not 0x100<=i<0x200),(route,f.name,'gameRAM')
   for field in (0x34,0x3a,0xc6,0x6f3):assert ram[field]==rr[field] or (route=='castle' and (ram[field],rr[field])==(171,148)),(route,f.name,field,ram[field],rr[field])
  if route!='attract':
   a=[x for x in rows('qa/dialogue/'+prefix+'/menu_events.csv') if x['kind']=='exec'];b=[x for x in rows('qa/dialogue/'+ref+'/menu_events.csv') if x['kind']=='exec'];assert len(a)==len(b)
   for x,y in zip(a,b):assert all(x[k]==y[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc'))
  routes[route]={'whole_screens_equal':len(files),'complete_PPU_OAM_equal':True};total+=len(files)
 timing={}
 for route,ref,refrom in [('castle','commit024_castle_irq',prior),('intro','ui022_intro_irq',old22),('tour','ui022_tour_irq',old22),('ticket','ui022_ticket_irq',old22)]:
  prefix='tag027_'+route+'_irq';aenv=env(prefix,rom);renv=env(ref,refrom);assert all(aenv[k]==renv[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));old=rows('qa/dialogue/'+ref+'/irq_phase.csv');new=rows('qa/dialogue/'+prefix+'/irq_phase.csv');assert len(old)==len(new);changes=0
  for a,b in zip(old,new):
   assert all(a[k]==b[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(a,b)
   if a['value']!=b['value']:
    assert route=='castle' and ((a['address'],a['value'],b['value']) in [('A000','94','AB'),('A008','95','AC')]);changes+=1
  timing[route]={'actual_timestamps_equal':len(old),'identical_Japanese_font_clone_values_only':changes}
 result={'status':'PASS','work':28,'adopted_build':'dialogue_kr_poc_027','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'scope':'Exact-time font-bank parity dispatch and gate Japanese clone171/172;20 drafts unchanged','ExpectedWrites_whole_and_prior_protected_image_match':True,'helper_bytes':135,'all_page_cycles_exact024':True,'CPU_page_phase_active_mode_cases':cases,'CPU_ABI_cases':1504,'rebuild_actual_IPS_apply_equal':True,'matched_screens':total,'whole_frame_pixel_differences':0,'routes':routes,'actual_timing':timing,'font_latches_only171_vs148_and_stack_return_addresses_may_differ_game_RAM_otherwise_equal':True,'all_previous_text_fonts_macros_title_preserved':True,'gate_slots_top_Japanese_clone':list(gate_slots),'font_policy':'All lower-only/default/intro fonts remain even; odd custom pairs also commit RAM34 atnative post-clear init; paired bank+1 can be even; Japanese fallback also tagged','reserved_remaining_KiB':4,'reserved_ranges':[[0x6a810,0x6ac10],[0x6b410,0x6c010]],'visual_review':'Actual027 gate1920, Korean intro1980 and booth1680 inspected at integer4x:tag027_actual_scenes.png; unchanged pixels and readable glyphs','limits':['Only insufficient castle route; no gate Korean or success branch yet;20 registered drafts not whole-game percentage','No fullplay/audio/reset/savestate/physical console/final translation review; previous PRG/RNG caveat; development only','025/026 failed NMI candidates preserved; timing masks not widened; old references belong to named builds']}
 (ROOT/'qa/reports/tag027_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
