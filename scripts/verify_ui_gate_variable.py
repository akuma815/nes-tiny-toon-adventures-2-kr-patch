"""Independent text/font reconstruction and narrowly bounded real-scene UI gates."""
import csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageChops
from extract_title_png import decode
from verify_dialogue_home import reader
from verify_ui_macro_passthrough import state_reader
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def main():
 d='build/dialogue_kr_poc_031';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_028/TinyToon2_dialogue_kr_poc.nes');report=j(d+'/build_report.json');plan=j(d+'/plan_used.json');pages=j(d+'/ui_korean_page_mapping.json');assert read('build/dialogue_kr_poc_029/TinyToon2_dialogue_kr_poc.nes')==read('build/dialogue_kr_poc_030/TinyToon2_dialogue_kr_poc.nes')==rom and len(pages)==2 and len({p['profile']['entry_id'] for p in pages})==2 and all(p['variable_state_cases']==48 for p in pages); m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256'] and sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']
 expected=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 expected=bytearray(prior);expected.extend(bytes(len(rom)-len(prior)));expected[5]=24;byfont={};fonts={};cycles={};atlas=Image.open(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010]
 for page in pages:
  p=page['profile'];start,end=p['source_file_offset'],p['end_exclusive'];body=bytes.fromhex(page['body_hex']);assert len(body)==end-start and sha(source[start:end])==p['source_raw_sha256'];expected[start+0x20000:end+0x20000]=body;
  for slot in p['slots']:expected[0x5710+2*slot]=p['font_bank']
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
  reverse.update({0x70+i:str(i) for i in range(10)})
  a,b=state_reader(oldview,p['pointer'],(0,5,0),0,p['ride']),state_reader(view,p['pointer'],(0,5,0),0,p['ride']);assert len(a)==len(b) and all(all(u[k]==v[k] for k in ('cycles','cursor','buffer_cursor')) for u,v in zip(a,b));actual=[];line=[]
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
  assert controls(oldbody)==controls(body);cycles[p['entry_id']]={'calls':len(b),'cycles':sum(e['cycles'] for e in b),'state_cases':48}
  for digits in ((0,0,0),(9,9,9),(1,2,3),(0,1,9)):
   for offset in (0,0x2f):
    for ride in range(6):
     x,y=state_reader(oldview,p['pointer'],digits,offset,ride),state_reader(view,p['pointer'],digits,offset,ride);assert len(x)==len(y) and all(all(u[k]==v[k] for k in ('cycles','cursor','buffer_cursor')) for u,v in zip(x,y))
     assert all(u['value']==v['value'] for u,v in zip(x,y) if 0x70<=u['value']<=0x79)
 assert bytes(expected)==rom and len(rom)==0x70010 and rom[4:6]==bytes.fromhex('10 18') and not any(rom[0x6ec10:])
 assert rom[0x40010:0x6dc10]==prior[0x40010:0x6dc10] and not any(rom[0x6a810:0x6ac10]) and rom[0x261b1:0x261ff]==prior[0x261b1:0x261ff]
 before=list(csv.DictReader(io.StringIO(read('backups/translation/text_ja_before_ui_gate_variable_001.csv').decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));keys={p['profile']['entry_id'] for p in pages};assert len(before)==len(after)==54
 for a,b in zip(before,after):
  for k in a:
   if a['entry_id'] in keys and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert a[k]==b[k]
 assert sum(r['status']=='draft' for r in after)==27 and sum(r['status']=='untranslated' for r in after)==27 and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')
 assert read('build/dialogue_kr_poc_031_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 031/TinyToon2_variable031_applied.nes')==rom
 routes={};font_observed={str(k):0 for k in fonts};matched=changed_total=0
 for prefix,ref in [('variable029_castle','gate028_castle'),('variable029_gold4','branch028_gold4'),('variable029_normal50','branch028_normal50')]:
  # Native reader replays constrain each changed glyph scratch/buffer byte pair.
  from verify_dialogue_home import MPU
  seed=read(f'qa/dialogue/{ref}/frame_01590_ram.bin');oldmem=bytearray(65536);newmem=bytearray(65536)
  oldmem[:2048]=newmem[:2048]=seed;oldmem[0x8000:0xc000]=oldview[0x4010:0x8010];newmem[0x8000:0xc000]=view[0x4010:0x8010]
  admitted=(0,*range(0x740,0x754));pairs={i:{(seed[i],seed[i])} for i in admitted}
  for event in [x for x in rows(f'qa/dialogue/{ref}/menu_events.csv') if x['kind']=='exec' and x['address']=='9417']:
   slot=int(event['id'],16);assert slot<48
   ptr=int.from_bytes(prior[0x55a9+2*slot:0x55ab+2*slot],'little')
   for mem in (oldmem,newmem):mem[0x6cd:0x6cf]=ptr.to_bytes(2,'little');mem[0x6c3]=mem[0x6c4]=0
   cpus=[MPU(memory=m) for m in (oldmem,newmem)]
   for call in range(200):
    for c,mem in zip(cpus,(oldmem,newmem)):
     c.pc=0x937c;c.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');steps=0
     while c.pc!=0xc100:c.step();steps+=1;assert steps<10000
    assert cpus[0].processorCycles==cpus[1].processorCycles
    pairs[0].add((cpus[0].a,cpus[1].a))
    for i in admitted:pairs[i].add((oldmem[i],newmem[i]))
    assert (cpus[0].a in (254,255))==(cpus[1].a in (254,255))
    if cpus[0].a==254:oldmem[0x6c4]=newmem[0x6c4]=0
    if cpus[0].a==255:break
   else:raise AssertionError('reader did not terminate')
  observed={str(font):0 for font in fonts}
  from verify_gate_font_tag import env
  ae=env(prefix,rom);re=env(ref,prior)
  if 'seed' in ae:assert ae['seed']==re['seed'] and ae['seed_file_sha256']==re['seed_file_sha256']
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  actual=ROOT/'qa/dialogue'/prefix;reference=ROOT/'qa/dialogue'/ref;files=sorted(actual.glob('frame_*.png'));assert [p.name for p in files]==[p.name for p in sorted(reference.glob('frame_*.png'))]
  changed=0;ramdiff={};fallback=0
  for f in files:
   tag=f.stem;rb=read(f'qa/dialogue/{prefix}/{tag}_ram.bin');rr=read(f'qa/dialogue/{ref}/{tag}_ram.bin');ppu=read(f'qa/dialogue/{prefix}/{tag}_ppu.bin');rp=read(f'qa/dialogue/{ref}/{tag}_ppu.bin');font=rb[0x34];page=byfont.get(font)
   assert read(f'qa/dialogue/{prefix}/{tag}_oam.bin')==read(f'qa/dialogue/{ref}/{tag}_oam.bin')
   for i in range(2048):
    if rb[i]==rr[i] or 0x100<=i<0x200:continue
    ramdiff[hex(i)]=ramdiff.get(hex(i),0)+1
    if i in (0x34,0x3a,0xc6,0x6f3):assert rr[i]==171 and rb[i] in fonts,(tag,hex(i));continue
    assert i in pairs and (rr[i],rb[i]) in pairs[i],(tag,'non-native buffer pair',hex(i),rr[i],rb[i])
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(reference/f.name).convert('RGB'));nt=bytearray(ppu[0x2000:0x3f00]);rnt=rp[0x2000:0x3f00]
   if diff.getbbox():assert page,(tag,font,diff.getbbox());changed+=1
   if page:
    for row,line in enumerate(page['layout']):
     diff.paste(0,(64,168+16*row,64+8*line['expanded_tiles'],176+16*row))
     for alias in range(0,0x1c01,0x400):
      off=alias+0x2a8+0x40*row;nt[off:off+line['expanded_tiles']]=rnt[off:off+line['expanded_tiles']]
   assert diff.getbbox() is None,(tag,'outside current native gate rows',diff.getbbox())
   assert nt==rnt and ppu[0x800:0x2000]==rp[0x800:0x2000] and ppu[0x3f00:]==rp[0x3f00:],(tag,'protected PPU')
   maps=rows(f'qa/dialogue/{prefix}/{tag}_mapping.csv');off=int(next(x for x in maps if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
   if off//0x400 in fonts:assert ppu[:0x800]==fonts[off//0x400];observed[str(off//0x400)]+=1
   else:assert ppu[:0x800]==rp[:0x800]
   if rb[0x6cf]==26 and font==171:assert ImageChops.difference(Image.open(f).convert('RGB'),Image.open(reference/f.name).convert('RGB')).getbbox() is None;fallback+=1
  # A route may omit price or permission; union across routes must cover both fonts.
  old=[x for x in rows(f'qa/dialogue/{ref}/menu_events.csv') if x['kind']=='exec'];new=[x for x in rows(f'qa/dialogue/{prefix}/menu_events.csv') if x['kind']=='exec'];assert len(old)==len(new)
  for a,b in zip(old,new):assert all(a[k]==b[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc','phase','ride','caller','gold_tickets','points_low','normal_ticket0','normal_ticket1','normal_ticket2')),(a,b)
  routes[prefix]={'screens':len(files),'changed_current_native_gate_rows':changed,'whole_frames_equal':len(files)-changed,'RAM_changes_constrained':ramdiff}
  matched+=len(files);changed_total+=changed
  for k,n in observed.items():font_observed[k]+=n
 assert all(n>0 for n in font_observed.values())
 timing={}
 for prefix,ref in [('variable029_castle_irq','gate028_castle_irq'),('variable029_gold4_irq','branch028_gold4_irq'),('variable029_normal50_irq','branch028_normal50_irq')]:
  ea=env(ref,prior);eb=env(prefix,rom)
  if 'seed' in ea:assert ea['seed']==eb['seed'] and ea['seed_file_sha256']==eb['seed_file_sha256']
  assert all(ea[k]==eb[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));old=rows(f'qa/dialogue/{ref}/irq_phase.csv');new=rows(f'qa/dialogue/{prefix}/irq_phase.csv');assert len(old)==len(new);changes=0
  for a,b in zip(old,new):
   assert all(a[k]==b[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(a,b)
   if a['value']!=b['value']:
    assert (a['address']=='A000' and a['value']=='AB' and int(b['value'],16) in fonts) or (a['address']=='A008' and a['value']=='AC' and int(b['value'],16)-1 in fonts),(a,b);changes+=1
  timing[prefix]={'actual_timestamps_equal':len(old),'font_values_only_changes':changes}
 hooks=j('qa/reports/variable031_hooks1504.json');assert hooks['abi_cases']==1504 and hooks['initial_latch_seed_cases']==720
 result={'status':'PASS','work':31,'adopted_build':'dialogue_kr_poc_031','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read(d+'/translation_used.csv')),'scope':'Castle price1A/alias2C preserve native FA numeral; observed permission1C translated; all25 prior drafts retained','source_units':54,'draft':27,'untranslated':27,'CHR_KiB':192,'ROM_size':len(rom),'ExpectedWrites_and_prior_whole_image_only_admitted_changes':True,'previous25_drafts_title_macros_helper008_preserved':True,'rebuild_actual_IPS_apply_equal':True,'CPU_ABI_cases':1504,'CPU_initial_font_seed_cases':720,'native_reader':cycles,'matched_screens':matched,'routes':routes,'changed_current_native_gate_rows':changed_total,'outside_current_native_gate_rows_pixels':0,'protected_PPU_OAM_game_state_equal':True,'native_reader_replay_constrained_buffer_pairs':True,'actual_font_samples':font_observed,'actual_timing':timing,'actual_timestamps_equal':sum(x['actual_timestamps_equal'] for x in timing.values()),'reserved_remaining_KiB':6,'reserved_ranges':[[0x6a810,0x6ac10],[0x6ec10,0x70010]],'runtime_ROMS_equal029_030_031':True,'029_metadata_erratum':'029 had variable_state_cases192 instead of48 and duplicate price metadata for alias;030 fixed count;031 fixed duplicate. All ROM hashes identical; no widened QA tolerance','visual_review':'Integer4x actual price2436/permission2124 reviewed in variable031_actual_pages.png; actual unchanged castle card2610 and game state6000 reviewed; native numeral50 readable; no fullplay claim','limits':['27 drafts are registered54 source units, not whole-game percentage; final names/tone review pending','Successful paths use explicit recorded RAM seeds; insufficient route controller-only; no fullplay or natural collection proof','Success booth15, top cards, other game assets/credits and full corpus remain pending','No fresh029 intro runtime; unchanged intro/title bytes with prior027 runtime reference only; no audio/reset/savestate/physical console/final review; prior PRG/RNG caveat; development only']}
 (ROOT/'qa/reports/variable031_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
