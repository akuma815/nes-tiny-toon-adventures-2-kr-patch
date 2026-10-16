"""Independent credits font/text/NT and exact real scroll/actor/timing gates."""
import csv,io,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from extract_title_png import decode
from verify_ui_macro_passthrough import state_reader
from verify_dialogue_home import MPU
from verify_gate_font_tag import env
from verify_native_printer_geometry import run as print_page
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def j(p):return json.loads(read(p).decode('utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def raw_lines(b):
 out=[];start=i=0
 while i<len(b):
  if b[i]==253:i+=2;continue
  if b[i] in (254,255):out.append(b[start:i+1]);start=i+1
  i+=1
 return out
def controls(b):
 out=[];i=0
 while i<len(b):
  if b[i]==253:out.append((i,253,b[i+1]));i+=2
  else:
   if b[i]==0 or b[i]>=127:out.append((i,b[i]))
   i+=1
 return out
def main():
 d='build/dialogue_kr_poc_037';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_036/TinyToon2_dialogue_kr_poc.nes');meta=j('manifests/source_rom.json');source=read(meta['path']);report=j(d+'/build_report.json');plan=j(d+'/plan_used.json');pages=j(d+'/ui_korean_page_mapping.json');info=j(d+'/credits_shared_font.json');assert sha(source)==meta['sha256'] and sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']
 expected=bytearray(source);owned=set();writes=j(d+'/expected_writes.json');assert len(writes)==8
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not owned&area;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==rom
 expected=bytearray(prior);expected.extend(bytes(len(rom)-len(prior)));expected[5]=26
 for p in (0x6468,0x26468):assert prior[p]==0x7c;expected[p]=0xc9
 font=bytearray(prior[0x5f010:0x5f810]);atlas=Image.open(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);reverse={0:' '};native={int(k):v for k,v in info['ASCII_map'].items()}
 for g in info['glyphs']:
  code,c,raw=g['code'],g['char'],bytes.fromhex(g['chr_hex']);reverse[code]=c
  if c==' ':assert raw==bytes(16)
  elif c in native.values():assert raw==source[0x3f010+code*16:0x3f010+(code+1)*16]
  else:
   assert '\uac00'<=c<='\ud7a3';n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(bits) and bits==[int(v>127) for v in im.get_flattened_data()] and decode(raw)==bytes(2*v for v in bits)
  font[code*16:(code+1)*16]=raw
 assert bytes(font)==bytes.fromhex(info['font_hex']) and info['Hangul_unique']==25
 for code in native:assert font[code*16:(code+1)*16]==source[0x3f010+code*16:0x3f010+(code+1)*16]
 expected[0x72410:0x72c10]=font;oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010];view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];glyph_pairs=set();nt_pairs={};translated_cells=set();preserved=[];readers={};slots={}
 for page in pages:
  p=page['profile'];a,b=p['source_file_offset'],p['end_exclusive'];old=prior[a+0x20000:b+0x20000];body=bytes.fromhex(page['body_hex']);assert source[a:b]==old and sha(old)==p['source_raw_sha256'] and len(body)==len(old) and controls(old)==controls(body);expected[a+0x20000:b+0x20000]=body
  for slot in p['slots']:expected[0x5710+2*slot]=201;slots[slot]=page
  for row in p['preserved_lines']:assert raw_lines(old)[row]==raw_lines(body)[row]
  aa,bb=state_reader(oldview,p['pointer'],(0,0,0),0,0),state_reader(view,p['pointer'],(0,0,0),0,0);assert len(aa)==len(bb);actual=[];line=[];row=col=0
  for x,y in zip(aa,bb):
   assert all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor'));glyph_pairs.add((x['value'],y['value']))
   if x['value'] in (254,255):assert x['value']==y['value'];actual.append(''.join(line));line=[];row+=1;col=0;continue
   line.append(reverse[y['value']]);addr=p['NT']+0x40*row+col
   for alias in (addr,addr^0x400):
    nt_pairs.setdefault(alias,set()).add((x['value'],y['value']))
    if alias+0x1000<0x3f00:nt_pairs.setdefault(alias+0x1000,set()).add((x['value'],y['value']))
   if x['value']!=y['value']:translated_cells.add(addr)
   col+=1
  assert actual==[x['desired'] for x in page['layout']];readers[p['entry_id']]={'calls':len(bb),'cycles':sum(x['cycles'] for x in bb)}
  ca,ma,na=print_page(prior,p,0);cb,mb,nb=print_page(rom,p,0);assert na==nb and (ca.a,ca.x,ca.y,ca.p,ca.sp,ca.processorCycles)==(cb.a,cb.x,cb.y,cb.p,cb.sp,cb.processorCycles)
  for row in p['preserved_lines']:preserved.append((p['entry_id'],row,p['NT']+row*0x40,bytes.fromhex(page['layout'][row]['expanded_hex'])))
 assert expected==rom and len(rom)==0x74010 and rom[4:6]==bytes.fromhex('10 1a') and rom[0x40010:0x72010]==prior[0x40010:0x72010]
 reserved=[[0x6a810,0x6ac10],[0x6ec10,0x6f010],[0x70010,0x70410],[0x70c10,0x71010],[0x71810,0x72010],[0x72010,0x72410],[0x72c10,0x74010]];assert all(not any(rom[a:b]) for a,b in reserved)
 before=list(csv.DictReader(io.StringIO(read('backups/translation/text_ja_before_credits_001.csv').decode('utf-8-sig'))));after=list(csv.DictReader(io.StringIO(read('workspace/translation/text_ja.csv').decode('utf-8-sig'))));keys={p['profile']['entry_id'] for p in pages};assert len(before)==len(after)==54
 for a,b in zip(before,after):
  for k in a:
   if a['entry_id'] in keys and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert a[k]==b[k]
 assert sum(x['status']=='draft' for x in after)==45 and sum(x['status']=='untranslated' for x in after)==9 and read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv') and read('build/dialogue_kr_poc_037_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 037/TinyToon2_credits037_applied.nes')==rom
 ref,prefix='credits036_selector_v3','credits037_selector_v3';a,b=env(ref,prior),env(prefix,rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256'));old_events=[x for x in rows(f'qa/dialogue/{ref}/menu_events.csv') if x['kind']=='exec'];new_events=[x for x in rows(f'qa/dialogue/{prefix}/menu_events.csv') if x['kind']=='exec'];assert len(old_events)==len(new_events)
 for a,b in zip(old_events,new_events):assert all(a[k]==b[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc','phase','ride','cpu_a','caller','gold_tickets','points_low','normal_ticket0','normal_ticket1','normal_ticket2')),(a,b)
 # Native chronological line-buffer replay: maxFD32 plus terminator, no broad RAM mask.
 seed=read(f'qa/dialogue/{ref}/frame_00990_ram.bin');mems=[bytearray(65536),bytearray(65536)];admitted=(0,*range(0x740,0x761));pairs={i:{(seed[i],seed[i])} for i in admitted}
 for mem,v in zip(mems,(oldview,view)):mem[:2048]=seed;mem[0x8000:0xc000]=v[0x4010:0x8010]
 for e in old_events:
  if e['address']!='9417':continue
  slot=int(e['id'],16);assert slot<48;ptr=int.from_bytes(prior[0x55a9+2*slot:0x55ab+2*slot],'little')
  for mem in mems:mem[0x6cd:0x6cf]=ptr.to_bytes(2,'little');mem[0x6c3]=mem[0x6c4]=0
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
 old_irq=rows(f'qa/dialogue/{ref}_irq/irq_phase.csv');new_irq=rows(f'qa/dialogue/{prefix}_irq/irq_phase.csv');a,b=env(ref+'_irq',prior),env(prefix+'_irq',rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256'));assert len(old_irq)==len(new_irq);font_changes=0;nmi={}
 for a,b in zip(old_irq,new_irq):
  assert all(a[k]==b[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(a,b)
  if a['value']!=b['value']:assert (a['address'],a['value'],b['value']) in (('A000','7C','C9'),('A008','7D','CA')),(a,b);font_changes+=1
  if a['kind']=='write' and (a['pc'],a['address']) in (('FF17','2005'),('FF20','2000')):nmi.setdefault(int(a['frame']),{})['y' if a['pc']=='FF17' else 'ctrl']=int(a['value'],16)
 files=sorted((ROOT/f'qa/dialogue/{prefix}').glob('frame_*.png'));assert [x.name for x in files]==[x.name for x in sorted((ROOT/f'qa/dialogue/{ref}').glob('frame_*.png'))];changed=font_samples=nt_changes=stack_glyphs=protected_row_samples=0;ram_changes={};first_complete={}
 def rect(addr,s):
  pos=addr&0x3ff;x=(pos%32)*8;row=pos//32;page=240 if addr&0x800 else 0;scroll=s['y']+(240 if s['ctrl']&2 else 0);y=(page+row*8-scroll)%480
  if y>472:y-=480
  if y>=240:return None
  return (x,max(0,y),x+8,min(240,y+8))
 for f in files:
  tag=f.stem;frame=int(tag[6:]);rb=read(f'qa/dialogue/{prefix}/{tag}_ram.bin');rr=read(f'qa/dialogue/{ref}/{tag}_ram.bin');ppu=read(f'qa/dialogue/{prefix}/{tag}_ppu.bin');rp=read(f'qa/dialogue/{ref}/{tag}_ppu.bin');assert read(f'qa/dialogue/{prefix}/{tag}_oam.bin')==read(f'qa/dialogue/{ref}/{tag}_oam.bin')
  for i in range(2048):
   if rb[i]==rr[i]:continue
   ram_changes[hex(i)]=ram_changes.get(hex(i),0)+1
   if i in (0x34,0x3a):assert (rr[i],rb[i])==(124,201),(tag,hex(i),rr[i],rb[i]);continue
   if i in (0xc6,0x6f3):assert (rr[i],rb[i])==(90,201),(tag,hex(i));continue
   if 0x100<=i<0x200:assert (rr[i],rb[i]) in glyph_pairs,(tag,'native queue/stack pair',hex(i),rr[i],rb[i]);stack_glyphs+=1;continue
   assert i in pairs and (rr[i],rb[i]) in pairs[i],(tag,'native reader pair',hex(i),rr[i],rb[i])
  for addr in range(0x2000,0x3f00):
   if ppu[addr]!=rp[addr]:assert addr in nt_pairs and (rp[addr],ppu[addr]) in nt_pairs[addr],(tag,'NT pair',hex(addr),rp[addr],ppu[addr]);nt_changes+=1
  assert ppu[0x800:0x2000]==rp[0x800:0x2000] and ppu[0x3f00:]==rp[0x3f00:]
  maps=rows(f'qa/dialogue/{prefix}/{tag}_mapping.csv');off=int(next(x for x in maps if x['kind']=='chr' and x['cpu_or_ppu_address']=='0000')['relative_offset'],16)
  if off//0x400==201:assert ppu[:0x800]==font;font_samples+=1
  else:assert ppu[:0x800]==rp[:0x800]
  actual=Image.open(f).convert('RGB');reference=Image.open(ROOT/f'qa/dialogue/{ref}/{f.name}').convert('RGB');diff=ImageChops.difference(actual,reference);hasdiff=diff.getbbox() is not None;scrolls=[nmi[z] for z in (frame-1,frame-2) if z in nmi and set(nmi[z])=={'y','ctrl'}]
  if rb[0x34]==201:
   assert scrolls,(tag,'missing exact preceding NMI scroll')
   for addr in translated_cells:
    for s in scrolls:
     box=rect(addr,s)
     if box:diff.paste(0,box)
   # Preserved Latin/legal rows must also match pixels after NT remained
   # complete for a full adjacent30-frame capture interval, beyond buffer lag.
   for id,row,addr,data in preserved:
    key=(id,row);complete=rp[addr:addr+len(data)]==ppu[addr:addr+len(data)]==data
    if not complete:first_complete.pop(key,None);continue
    first_complete.setdefault(key,frame)
    if frame-first_complete[key]>=30:
     for col in range(len(data)):
      for s in scrolls:
       box=rect(addr+col,s)
       if box:assert ImageChops.difference(actual.crop(box),reference.crop(box)).getbbox() is None,(tag,'preserved row pixels',id,row,col);protected_row_samples+=1
  assert diff.getbbox() is None,(tag,'outside translated exact scrolling cells',diff.getbbox(),rb[0x34],rr[0x34],scrolls)
  if hasdiff:changed+=1
 assert font_samples>0 and protected_row_samples>0;hooks=j('qa/reports/credits037_hooks1504.json');assert hooks['abi_cases']==1504 and hooks['initial_latch_seed_cases']==720
 result={'status':'PASS','work':37,'adopted_build':'dialogue_kr_poc_037','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read(d+'/translation_used.csv')),'draft':45,'untranslated':9,'source_units':54,'ROM_size':len(rom),'CHR_KiB':208,'ExpectedWrites':8,'ExpectedWrites_whole_source_and_prior_only_admitted_changes':True,'rebuild_actual_IPS_apply_equal':True,'native_reader':readers,'native_correct_little_endian_printer_cases':3,'CPU_ABI_cases':1504,'CPU_initial_font_seed_cases':720,'whole_other_fonts_UI_title_macros_controls_preserved':True,'names_publisher_legal_rows_binary_and_bitmaps_preserved':True,'matched_screens':len(files),'changed_translated_scrolling_cells_only':changed,'whole_frames_equal':len(files)-changed,'outside_translated_scrolling_cells_pixels':0,'actual_font_samples':font_samples,'native_NT_pairs':nt_changes,'native_command_queue_stack_glyph_pairs':stack_glyphs,'preserved_name_legal_pixel_cell_samples':protected_row_samples,'RAM_changes_constrained':ram_changes,'protected_PPU_OAM_scroll_actor_game_state_equal':True,'actual_timestamps_equal':len(old_irq),'font_values_only_changes':font_changes,'pixel_projection':'Exact NT cells of changed labels, hardware FF17/FF20 scroll from preceding frame-1/-2 NMI, no whole-screen mask or timing tolerance','Hangul_unique':25,'reserved_remaining_KiB':12,'reserved_ranges':reserved,'visual_review':'Separate actual completed scrolling labels image evidence required','limits':['45 drafts plus9 technical/shared source units are registered54, not whole-game percentage; fullcorpus/game graphics/finalreview pending','Credits use exact four recorded initial RAM writes, no PC/ROM/state writes; not natural gameclear/fullplay proof','Intro/menu fresh037 regression reported separately when completed','Audio/reset/savestate/physical console/finaltranslation names and priorPRG/RNG caveat remain; development only']};(ROOT/'qa/reports/credits037_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
