"""Independent shared-card reconstruction and exact paired native runtime gates."""
import csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageChops,ImageFont,ImageDraw
from extract_title_png import decode
from verify_ui_macro_passthrough import state_reader
from verify_dialogue_home import MPU
from verify_gate_font_tag_hooks import Memory
from verify_gate_font_tag import env
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def controls(b):
 out=[];i=0
 while i<len(b):
  v=b[i]
  if v==253:out.append((i,v,b[i+1]));i+=2
  else:
   if v==0 or v>=127:out.append((i,v))
   i+=1
 return out
def print_page(rom,p,ride):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0x925e;c.sp=0xfd;m.ram[0x1fe:0x200]=bytes.fromhex('ff c0');m.ram[0x6cd:0x6cf]=p['pointer'].to_bytes(2,'little');m.ram[0x25]=ride
 nt=p['NT'];nt=int(nt,16) if isinstance(nt,str) else nt
 for a in (0x6c0,0x6d1):m.ram[a:a+2]=bytes([nt>>8,nt&255])
 n=0
 while c.pc!=0xc100:c.step();n+=1;assert n<20000,(p['entry_id'],hex(c.pc))
 return c,m
def main():
 d='build/dialogue_kr_poc_036';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_033/TinyToon2_dialogue_kr_poc.nes');report=j(d+'/build_report.json');plan=j(d+'/plan_used.json');pages=j(d+'/ui_korean_page_mapping.json');info=j(d+'/ui_stage_lower_shared_font.json');manifest=j('manifests/source_rom.json');source=read(manifest['path']);assert sha(source)==manifest['sha256'] and sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']
 expected=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  a,n=w['file_offset'],w['length'];area=set(range(a,a+n));assert not area&owned;owned|=area;assert source[a:a+n]==bytes.fromhex(w['expected_hex']);expected[a:a+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 font=bytearray(prior[0x65010:0x65810]);atlas=Image.open(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);reverse={0:' ',**{0x70+i:str(i) for i in range(10)}}
 for g in info['glyphs']:
  c,code,raw=g['char'],g['code'],bytes.fromhex(g['chr_hex']);reverse[code]=c
  if c==' ':assert raw==bytes(16)
  elif c in plan['native_punctuation']:
   old=plan['native_punctuation'][c];assert raw==source[0x36810+old*16:0x36810+(old+1)*16]
  else:
   assert '\uac00'<=c<='\ud7a3';n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(bits) and bits==[int(v>127) for v in im.get_flattened_data()] and decode(raw)==bytes(2*v for v in bits)
  font[code*16:(code+1)*16]=raw
 assert bytes(font)==bytes.fromhex(info['font_hex']) and info['Hangul_unique']==22 and len(info['remaining_literal_slots'])>0 and info['macro_ids']==[136]
 for code in (0,*range(0x41,0x4b),*range(0x70,0x7a)):assert font[code*16:(code+1)*16]==source[0x36810+code*16:0x36810+(code+1)*16]
 expected=bytearray(prior);expected.extend(bytes(len(rom)-len(prior)));expected[5]=25;expected[0x71010:0x71810]=font;view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010];by_slot={};glyph_pairs=set();nt_pairs={};printer_cases=0;reader_cases=0;native_reader={}
 for page in pages:
  p=page['profile'];a,b=p['source_file_offset'],p['end_exclusive'];body=bytes.fromhex(page['body_hex']);assert len(body)==b-a and sha(source[a:b])==p['source_raw_sha256'] and controls(prior[a+0x20000:b+0x20000])==controls(body) and 0x83 not in body
  expected[a+0x20000:b+0x20000]=body
  for slot in p['slots']:expected[0x5710+slot*2]=196;by_slot[slot]=page
  for digits in ((0,0,0),(9,9,9),(1,2,3),(0,1,9)):
   for offset in (0,0x2f):
    for ride in range(6):
     old,new=state_reader(oldview,p['pointer'],digits,offset,ride),state_reader(view,p['pointer'],digits,offset,ride);assert len(old)==len(new)
     for x,y in zip(old,new):
      assert all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor'));glyph_pairs.add((x['value'],y['value']))
      if x['value']>=254:assert x['value']==y['value']
     reader_cases+=1
  events=state_reader(view,p['pointer'],(3,0,0),0x2f,5);actual=[];line=[]
  for e in events:
   if e['value'] in (254,255):actual.append(''.join(line));line=[]
   else:line.append(reverse[e['value']])
  assert actual==[x['desired'] for x in page['layout']];native_reader[p['entry_id']]={'calls':len(events),'cycles':sum(e['cycles'] for e in events)}
  base=p['NT'];base=int(base,16) if isinstance(base,str) else base
  for ride in range(6):
   ca,ma=print_page(prior,p,ride);cb,mb=print_page(rom,p,ride);assert (ca.a,ca.x,ca.y,ca.p,ca.sp,ca.processorCycles)==(cb.a,cb.x,cb.y,cb.p,cb.sp,cb.processorCycles);printer_cases+=1
   aa=state_reader(oldview,p['pointer'],(0,0,0),0,ride);bb=state_reader(view,p['pointer'],(0,0,0),0,ride);row=col=0
   for x,y in zip(aa,bb):
    if x['value']==254:row+=1;col=0;continue
    if x['value']==255:break
    for alias in range(0,0x1c01,0x400):nt_pairs.setdefault(alias+(base-0x2000)%0x400+0x40*row+col,set()).add((x['value'],y['value']))
    col+=1
   for i in range(0x100,0x200):
    if ma.ram[i]!=mb.ram[i]:assert (ma.ram[i],mb.ram[i]) in glyph_pairs,(p['entry_id'],hex(i),ma.ram[i],mb.ram[i])
 assert len(pages)==5 and len(by_slot)==6 and reader_cases==240 and printer_cases==30 and expected==rom and len(rom)==0x72010 and rom[4:6]==bytes.fromhex('10 19')
 reserved=[[0x6a810,0x6ac10],[0x6ec10,0x6f010],[0x70010,0x70410],[0x70c10,0x71010],[0x71810,0x72010]]
 assert all(not any(rom[a:b]) for a,b in reserved) and rom[0x40010:0x70010]==prior[0x40010:0x70010] and rom[0x261b1:0x261ff]==prior[0x261b1:0x261ff]
 before=list(csv.DictReader(io.StringIO(read('backups/translation/text_ja_before_ui_stage_lower_001.csv').decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));keys={p['profile']['entry_id'] for p in pages};assert len(before)==len(after)==54
 for a,b in zip(before,after):
  for k in a:
   if a['entry_id'] in keys and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert a[k]==b[k]
 assert sum(r['status']=='draft' for r in after)==42 and sum(r['status']=='untranslated' for r in after)==12 and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv') and read('build/dialogue_kr_poc_036_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 036/TinyToon2_stage_lower036_applied.nes')==rom
 routes={};timing={};matched=changed_total=font_observed=0
 refs={r:f'cards033_{r}' for r in ('coaster','cart','train','water','gold4')};refs['normal3']='remaining033_normal3'
 maxline=max(x['expanded_tiles'] for p in pages for x in p['layout']);admitted=(0,*range(0x740,0x740+maxline+1));assert maxline==15
 for route,ref in refs.items():
  prefix=f'stage_lower036_{route}';ae,re=env(prefix,rom),env(ref,prior)
  assert all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  if 'seed' in ae:assert ae['seed']==re['seed'] and ae['seed_file_sha256']==re['seed_file_sha256']
  seed=read(f'qa/dialogue/{ref}/frame_00990_ram.bin');mems=[bytearray(65536),bytearray(65536)]
  for mem,v in zip(mems,(oldview,view)):mem[:2048]=seed;mem[0x8000:0xc000]=v[0x4010:0x8010]
  pairs={i:{(seed[i],seed[i])} for i in admitted};events=[x for x in rows(f'qa/dialogue/{ref}/menu_events.csv') if x['kind']=='exec' and x['address']=='9417'];new_events=[x for x in rows(f'qa/dialogue/{prefix}/menu_events.csv') if x['kind']=='exec' and x['address']=='9417'];assert len(events)==len(new_events)
  for event,new_event in zip(events,new_events):
   assert all(event[k]==new_event[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc','phase','ride','caller','gold_tickets','points_low','normal_ticket0','normal_ticket1','normal_ticket2')),(event,new_event)
   slot=int(event['id'],16);ptr=int.from_bytes(prior[0x55a9+2*slot:0x55ab+2*slot],'little')
   for mem in mems:mem[0x6cd:0x6cf]=ptr.to_bytes(2,'little');mem[0x6c3]=mem[0x6c4]=0;mem[0x25]=int(event['ride'],16)
   cpus=[MPU(memory=m) for m in mems]
   for call in range(200):
    for c,mem in zip(cpus,mems):
     c.pc=0x937c;c.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');n=0
     while c.pc!=0xc100:c.step();n+=1;assert n<10000
    assert cpus[0].processorCycles==cpus[1].processorCycles;glyph_pairs.add((cpus[0].a,cpus[1].a));pairs[0].add((cpus[0].a,cpus[1].a))
    for i in admitted:pairs[i].add((mems[0][i],mems[1][i]))
    if cpus[0].a==254:mems[0][0x6c4]=mems[1][0x6c4]=0
    if cpus[0].a==255:break
   else:raise AssertionError('reader did not terminate')
  folder=ROOT/'qa/dialogue'/prefix;reference=ROOT/'qa/dialogue'/ref;files=sorted(folder.glob('frame_*.png'));assert [f.name for f in files]==[f.name for f in sorted(reference.glob('frame_*.png'))];changed=0;ramdiff={};ntdiff=0;queuediff=0;completed_frame_lower_transitions=[];last_cost_nt_diff=-100
  for f in files:
   tag=f.stem;rb=read(f'qa/dialogue/{prefix}/{tag}_ram.bin');rr=read(f'qa/dialogue/{ref}/{tag}_ram.bin');ppu=read(f'qa/dialogue/{prefix}/{tag}_ppu.bin');rp=read(f'qa/dialogue/{ref}/{tag}_ppu.bin');assert read(f'qa/dialogue/{prefix}/{tag}_oam.bin')==read(f'qa/dialogue/{ref}/{tag}_oam.bin')
   for i in range(2048):
    if rb[i]==rr[i]:continue
    ramdiff[hex(i)]=ramdiff.get(hex(i),0)+1
    if i in (0xc6,0x6f3):assert rr[i] in (148,190,193) and rb[i]==196,(route,tag,hex(i),rr[i],rb[i]);continue
    if 0x100<=i<0x200:assert (rr[i],rb[i]) in glyph_pairs,(route,tag,'native command queue/stack',hex(i),rr[i],rb[i]);queuediff+=1;continue
    assert i in pairs and (rr[i],rb[i]) in pairs[i],(route,tag,'reader buffer',hex(i),rr[i],rb[i])
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(reference/f.name).convert('RGB'));hasdiff=diff.getbbox() is not None
   # Owned lower cells across native cost/number/insuff/start/possession clears.
   # Top title/rule pixels and both top latch values must remain identical.
   lower_nt_diff=any(ppu[0x22a8+row*0x40:0x22a8+row*0x40+width]!=rp[0x22a8+row*0x40:0x22a8+row*0x40+width] for row,width in enumerate((15,11)))
   frame=int(tag[6:])
   if lower_nt_diff:last_cost_nt_diff=frame
   owned_lower_transition=rb[0x34]==rr[0x34]==193 and frame-last_cost_nt_diff<=3
   if rb[0x6f3]==196 or owned_lower_transition:
    if rb[0x6f3]!=196:completed_frame_lower_transitions.append(tag)
    for row,width in enumerate((15,11)):diff.paste(0,(64,163+16*row,64+8*width,171+16*row))
   assert diff.getbbox() is None,(route,tag,'outside owned card cells',diff.getbbox(),rb[0x34],rb[0x6f3])
   if hasdiff:changed+=1
   for i,(old,new) in enumerate(zip(rp[0x2000:0x3f00],ppu[0x2000:0x3f00])):
    if old!=new:assert i in nt_pairs and (old,new) in nt_pairs[i],(route,tag,'native NT glyph pair',hex(i+0x2000),old,new);ntdiff+=1
   assert ppu[0x800:0x2000]==rp[0x800:0x2000] and ppu[0x3f00:]==rp[0x3f00:]
   maps=rows(f'qa/dialogue/{prefix}/{tag}_mapping.csv');off=int(next(x for x in maps if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
   if off//0x400==196:assert ppu[:0x800]==font;font_observed+=1
   else:assert ppu[:0x800]==rp[:0x800]
  routes[prefix]={'screens':len(files),'changed_owned_card_rows':changed,'whole_frames_equal':len(files)-changed,'RAM_changes_constrained':ramdiff,'native_command_queue_glyph_pairs':queuediff,'native_NT_glyph_pairs':ntdiff,'native_card_cost_clear_transitions_with_exact_NT_glyph_pairs':completed_frame_lower_transitions};matched+=len(files);changed_total+=changed
  a,b=env(ref+'_irq',prior),env(prefix+'_irq',rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  if 'seed' in a:assert a['seed']==b['seed'] and a['seed_file_sha256']==b['seed_file_sha256']
  old,new=rows(f'qa/dialogue/{ref}_irq/irq_phase.csv'),rows(f'qa/dialogue/{prefix}_irq/irq_phase.csv');assert len(old)==len(new);changes=0
  for a,b in zip(old,new):
   assert all(a[k]==b[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(route,a,b)
   if a['value']!=b['value']:assert (a['address'],a['value'],b['value']) in (('A000','94','C4'),('A008','95','C5'),('A000','C1','C4'),('A008','C2','C5'),('A000','BE','C4'),('A008','BF','C5')),(a,b);changes+=1
  timing[prefix+'_irq']={'actual_timestamps_equal':len(old),'font_values_only_changes':changes}
 assert font_observed>0;hooks=j('qa/reports/stage_lower036_hooks1504.json');assert hooks['abi_cases']==1504 and hooks['initial_latch_seed_cases']==720
 result={'status':'PASS','work':35,'adopted_build':'dialogue_kr_poc_036','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read(d+'/translation_used.csv')),'scope':'Shared lower196/197 for cost/F9 aliases0+23/insuff29/start2A/possession2B;42drafts, original code/timing retained','source_units':54,'draft':42,'untranslated':12,'CHR_KiB':200,'ROM_size':len(rom),'ExpectedWrites_and_prior_whole_image_only_admitted_changes':True,'all_previous_fonts_macros_helper008_numbers_controls_preserved':True,'rebuild_actual_IPS_apply_equal':True,'CPU_ABI_cases':1504,'CPU_initial_font_seed_cases':720,'native_reader_state_cases':reader_cases,'native_immediate_printer_cases':printer_cases,'native_reader':native_reader,'matched_screens':matched,'routes':routes,'changed_owned_card_rows':changed_total,'outside_owned_card_rows_pixels':0,'protected_PPU_OAM_game_state_equal':True,'reader_buffer_pairs_constrained_to_15_tiles_plus_terminator':True,'command_queue_stack_changes_only_native_glyph_pairs':True,'native_NT_changes_only_exact_owned_cell_output_pairs':True,'actual_font_samples':font_observed,'actual_timing':timing,'actual_timestamps_equal':sum(x['actual_timestamps_equal'] for x in timing.values()),'Hangul_unique':22,'remaining_literal_slots':len(info['remaining_literal_slots']),'reserved_remaining_KiB':6,'reserved_ranges':reserved,'visual_review':'Recorded separately in stage_lower036_actual_pages.json after direct image review','limits':['42 drafts are registered54 source units, not whole-game percentage; final tone/names review pending','Castle success and insuff normal3 use explicit recorded initial RAM seed; four normal-cost controller routes; no full playthrough','Other native messages/variables, game graphics/credits, complete corpus remain pending','Fresh036 intro verification pending; unchanged bytes and historical runtime reference only; audio/reset/savestate/physical console/final review pending; prior PRG/RNG caveat; development only']}
 (ROOT/'qa/reports/stage_lower036_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
