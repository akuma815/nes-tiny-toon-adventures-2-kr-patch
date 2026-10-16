"""Independent gate023 exact two-byte model, CPU flags and native/runtime gates."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
from verify_ui_native_latch_hooks import Memory,MPU
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def env(prefix,rom):
 e=j('qa/dialogue/'+prefix+'/environment.json');assert e['exit_code']==0 and e['rom_sha256']==sha(rom)
 for n,h in e['files'].items():assert sha(read('qa/dialogue/'+prefix+'/'+n))==h,(prefix,n)
 return e
def cpu(rom,p):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x9ff7;c.p=p;c.a=0x73;c.x=0x34;c.y=0x81;c.sp=0xf5
 while c.pc!=0x9fff:c.step()
 return c,m

def main():
 d='build/dialogue_kr_poc_023';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_022/TinyToon2_dialogue_kr_poc.nes');native=read('build/dialogue_kr_poc_017/TinyToon2_dialogue_kr_poc.nes');meta=j('manifests/source_rom.json');source=read(meta['path']);assert sha(source)==meta['sha256'];model=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not owned&area;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==rom;assert [i for i,(a,b) in enumerate(zip(prior,rom)) if a!=b]==[0x6008,0x26008] and len(prior)==len(rom)
 assert rom[0x40010:]==prior[0x40010:] and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_022/translation_used.csv')
 assert read('build/dialogue_kr_poc_023_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 023/TinyToon2_gate023_applied.nes')==rom
 for p in range(256):
  a,am=cpu(prior,p);b,bm=cpu(rom,p);assert (a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles);assert am.banks==bm.banks
  assert am.ram[0x34]==90 and bm.ram[0x34]==148 and all(am.ram[i]==bm.ram[i] for i in range(2048) if i!=0x34)
 pages=j(d+'/ui_korean_page_mapping.json');byfont={p['profile']['font_bank']:p for p in pages};result_routes={};total=0;gate_whole=0
 for route in ('castle','train','water'):
  prefix='gate023_'+route;reference='consumers017_castle' if route=='castle' else 'consumers022_'+route;refrom=native if route=='castle' else prior
  ae=env(prefix,rom);re=env(reference,refrom);assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted((ROOT/'qa/dialogue'/prefix).glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted((ROOT/'qa/dialogue'/reference).glob('frame_*.png'))];changed=0;whole=0
  for f in files:
   tag=f.stem;base='qa/dialogue/'+prefix+'/'+tag;ref='qa/dialogue/'+reference+'/'+tag;r=read(base+'_ram.bin');rr=read(ref+'_ram.bin');p=read(base+'_ppu.bin');rp=read(ref+'_ppu.bin');diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ROOT/(ref+'.png')).convert('RGB'))
   assert r[0x25]==rr[0x25] and r[0x6cf]==rr[0x6cf]  and r[0x6ea]==rr[0x6ea] and r[0xc7]==rr[0xc7] and r[0x7d0:0x7d3]==rr[0x7d0:0x7d3] and r[0x7e0]==rr[0x7e0] and r[0x7f2:0x7f7]==rr[0x7f2:0x7f7]
   if r[0x6cd:0x6cf]!=rr[0x6cd:0x6cf]:
    assert route=='castle' and r[0x6df] in (0,1,2)
    frame=int(tag.split('_')[1]);press=[x['frame'] for x in ae['input']['sequence'] if x['button']=='a' and 1800<=x['frame']<=3300];assert any(start<=frame<start+7 for start in press)
    ptr=int.from_bytes(source[0x55a9+2*r[0x6cf]:0x55ab+2*r[0x6cf]],'little');assert int.from_bytes(rr[0x6cd:0x6cf],'little')==ptr
    returns=[x for x in rows('qa/dialogue/'+prefix+'/menu_events.csv') if x['kind']=='exec' and x['address']=='9445' and int(x['frame'])<frame];assert int.from_bytes(r[0x6cd:0x6cf],'little')==int(returns[-1]['pointer'],16)
   assert read(base+'_oam.bin')==read(ref+'_oam.bin') and p[0x3f00:0x3f20]==rp[0x3f00:0x3f20]
   if diff.getbbox():
    assert route=='castle';page=byfont.get(r[0x6f3]);assert page,(tag,r[0x6f3],diff.getbbox());changed+=1
    for line,layout in enumerate(page['layout']):diff.paste(0,(64,163+16*line,64+8*layout['expanded_tiles'],171+16*line))
   else:
    whole+=1
    if route=='castle' and r[0x34]==148:gate_whole+=1
   assert diff.getbbox() is None,(route,tag,diff.getbbox())
   if route!='castle':assert p==rp and r==rr
  result_routes[route]={'screens':len(files),'known_Korean_home_rows_changed':changed,'whole_frames_equal':whole};total+=len(files)
 assert gate_whole>180
 # Exact023-vs022 gate nametables/palette/OAM and pointer; corrected top RAM34 only.
 ae=env('consumers022_castle',prior)
 for f in sorted((ROOT/'qa/dialogue/gate023_castle').glob('frame_*.png')):
  tag=f.stem;r=read('qa/dialogue/gate023_castle/'+tag+'_ram.bin');rr=read('qa/dialogue/consumers022_castle/'+tag+'_ram.bin');assert all(r[i]==rr[i] for i in range(2048) if i not in (0x34,0x3a));assert all(r[i]==rr[i] or (r[i],rr[i])==(148,90) for i in (0x34,0x3a));p=read('qa/dialogue/gate023_castle/'+tag+'_ppu.bin');q=read('qa/dialogue/consumers022_castle/'+tag+'_ppu.bin');assert p[0x2000:]==q[0x2000:];assert read('qa/dialogue/gate023_castle/'+tag+'_oam.bin')==read('qa/dialogue/consumers022_castle/'+tag+'_oam.bin')
 old=rows('qa/dialogue/gate022_castle_irq/irq_phase.csv');new=rows('qa/dialogue/gate023_castle_irq/irq_phase.csv');assert len(old)==len(new);changes=0
 for a,b in zip(old,new):
  assert all(a[k]==b[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(a,b)
  if a['value']!=b['value']:assert (a['pc'],a['address'],a['value'],b['value']) in [('FD77','A000','5A','94'),('FD92','A008','5B','95')];changes+=1
 gate1920=[x for x in new if x['frame']=='1920' and x['address']=='A000'];assert len(gate1920)==1 and gate1920[0]['pc']=='FD77'
 from build_ui_post_clear import run
 pre=read('build/dialogue_kr_poc_020/TinyToon2_dialogue_kr_poc.nes');cases=0;allowed={0x6,0x7,0xc6,0x6f3,0x6c0,0x6c1,0x6d1,0x6d2,0x6cd,0x6ce,0x6c3,0x6c4}
 for slot in (13,14,15,0x17,0x18,0x19,0x1a,0x1b,0x1c):
  for carry in (False,True):
   for overflow in (False,True):
    for tickets in ((0,0,0),(9,9,9),(1,2,3)):
     for low_points in (0,10,99):
      a,am=run(pre,slot,carry,overflow,tickets,low_points);b,bm=run(rom,slot,carry,overflow,tickets,low_points)
      assert (a.a,a.x,a.y,a.sp,a.p)==(b.a,b.x,b.y,b.sp,b.p) and b.processorCycles-a.processorCycles==-209 and am.banks==bm.banks
      assert all(am.ram[i]==bm.ram[i] for i in range(2048) if i not in allowed and not 0x100<=i<0x200);cases+=1
 result={'status':'PASS','work':25,'adopted_build':'dialogue_kr_poc_023','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'scope':'Correct native Japanese castle font missed by prior visited-route QA; Korean18 drafts unchanged','changed_bytes_from022':2,'ExpectedWrites_whole_source_and_protected_CHR_equal':True,'CPU_full_initial_flag_cases':256,'CPU_extra_cycles':0,'CPU_common_pre_clear_full_branch_cases':cases,'pre_clear_register_seed_note':'Function parameter names in work23 were reversed:07D0..2 ticket digits,07F2 low points;10/99 are synthetic stress values, not valid single decimal digits','native17_pointer_deferred_only_during_common_gate_clear':True,'rebuild_actual_IPS_apply_equal':True,'matched_screens':total,'routes':result_routes,'native_Japanese_gate_whole_frames_equal':gate_whole,'outside_current_home_rows_pixels':0,'actual_IRQ_NMI_PPU_mapper_timestamps_equal':len(old),'NMI_top_font_changes_only':changes,'RAM34_and_native_NMI_cache3A_changes_only':True,'gate_active_display_consumer':'At1920 only FD77 NMI A000 write, no FB0D IRQ or late font switch; gate34 supplies both text rows168..191.06F3 alone is insufficient','visual_review':'Actual023 1920 four-gold-ticket message viewed at integer4x, matches native017 pixels; source-normal versus022 regression observed','limits':['No new Korean gate draft or final translation review; gate remains native Japanese','Only normal insufficient route, no gold4/normal50 success or points exchange success','No full play/audio/reset/savestate/physical console; previous PRG/RNG caveat; development only']}
 (ROOT/'qa/reports/gate023_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='limits'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
