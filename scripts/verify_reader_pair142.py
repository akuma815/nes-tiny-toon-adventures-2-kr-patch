"""Frozen bounded controller-only read/CHR/NT pair verifier, also reusable by143."""
from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
from verify_dialogue_home import reader
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def native_lines(rom,slot):
 view=bytearray(rom);view[0x4010:0x8010]=rom[0x24010:0x28010]
 ptr=int.from_bytes(rom[0x255a9+2*slot:0x255ab+2*slot],'little')
 lines=[];line=[]
 for z in reader(view,ptr):
  if z['value']in [254,255]:lines.append(bytes(line));line=[]
  else:line.append(z['value'])
 return lines
def verify(work,name,slots,targets,required_full_units,course,final_normal):
 out=R/f'qa/reports/{name}{work}_validation.json';assert not out.exists()
 a,b=[R/'qa/dialogue'/f'{name}{work}_native_{build}'for build in ['047','049']]
 ea,eb=[json.loads((p/'environment.json').read_text('utf-8'))for p in [a,b]]
 assert ea['exit_code']==eb['exit_code']==0 and ea['frames']==eb['frames']==4500
 assert eb['intervention']=='controller input only; no state loading or RAM/ROM writes'
 for k in ['source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention']:assert ea[k]==eb[k],k
 assert 'seed'not in eb
 rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';rom=rp.read_bytes();oldrom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 assert sha(rp)==eb['rom_sha256']and hashlib.sha256(oldrom).hexdigest()==ea['rom_sha256']
 for d,e in [(a,ea),(b,eb)]:
  assert (d/'trace_complete.txt').read_text()=='4500'
  for f,h in e['files'].items():assert sha(d/f)==h,(d.name,f)
 A,B=[rows(p/'menu_events.csv')for p in [a,b]];assert len(A)==len(B);relocated=collections.Counter()
 for x,y in zip(A,B):
  assert {k:v for k,v in x.items()if k!='pc'}=={k:v for k,v in y.items()if k!='pc'}
  if x['pc']==y['pc']:continue
  assert x['kind']=='write'and(x['pc'],y['pc'],x['address'])in [('9613','964A','00C6'),('9616','964D','06F3'),('961C','9653','0034')]
  po,pn=[0x4010+int(z['pc'],16)-0x8000 for z in [x,y]];n=3 if x['address']=='06F3'else 2
  assert oldrom[po-n:po]==rom[pn-n:pn];relocated[x['pc']+'->'+y['pc']+'/'+x['address']]+=1
 events=[r for r in B if r['kind']=='exec'and r['address']=='9445'];assert set(slots)<={r['id']for r in events}
 cat=json.loads((R/'extracted/text/table_20261004_001/text_tokens.json').read_text('utf-8'))
 readrows=[rows(p/'prg_text_reads.csv')for p in [a,b]];assert readrows[0]and len(readrows[0])==len(readrows[1])
 groups=collections.defaultdict(list);cycles=collections.Counter()
 for x,y in zip(*readrows):
  assert {k:v for k,v in x.items()if k!='cycles'}=={k:v for k,v in y.items()if k!='cycles'}
  f=int(y['PRG_relative_offset'],16)+16;assert rom[f]==int(y['value'],16)==oldrom[f]
  candidates=[u for u in cat['units']if u['file_offset']+0x20000<=f<u['end_exclusive']+0x20000];assert len(candidates)==1
  u=candidates[0];groups[u['entry_id']].append({'frame':int(y['frame']),'source_relative_offset':f-u['file_offset']-0x20000,'value_hex':y['value'],'native_id_hex':y['native_id'],'reader_PC':y['pc'],'active_font':int(y['active_font'],16)})
  pc=int(y['pc'],16);p=0x24010+pc-0x8000;assert y['pc']in ['9395','9362','92CF']and rom[p-2:p]==bytes.fromhex('b1 06')
  cycles[int(y['cycles'])-int(x['cycles'])]+=1
 for unit in required_full_units:
  u=next(z for z in cat['units']if z['entry_id']==unit)
  assert set(z['source_relative_offset']for z in groups[unit])==set(range(u['end_exclusive']-u['file_offset'])),unit
 expectations={key:{**target,'lines':native_lines(rom,target['slot']),'complete_frames':[]}for key,target in targets.items()}
 imgs=sorted(f for f in eb['files']if f.endswith('.png'));assert imgs==sorted(f for f in ea['files']if f.endswith('.png'))
 ramdiff=collections.Counter();statediff=collections.Counter();chunks=0;transitions=[];prev=None;gameplay=[]
 for f in imgs:
  stem=f[:-4];frame=int(stem[6:]);ra,rb=[(p/(stem+'_ram.bin')).read_bytes()for p in [a,b]]
  ramdiff.update(f'{i:04X}'for i,(x,y)in enumerate(zip(ra,rb))if x!=y)
  for suffix in ['_ppu.bin','_oam.bin','_mapping.csv']:assert (a/(stem+suffix)).read_bytes()==(b/(stem+suffix)).read_bytes(),(f,suffix)
  assert ImageChops.difference(Image.open(a/f).convert('RGB'),Image.open(b/f).convert('RGB')).getbbox()is None,f
  pp=(b/(stem+'_ppu.bin')).read_bytes()
  for z in rows(b/(stem+'_mapping.csv')):
   if z['kind']!='chr':continue
   addr=int(z['cpu_or_ppu_address'],16);off=int(z['relative_offset'],16);assert pp[addr:addr+1024]==rom[0x40010+off:0x40410+off];chunks+=1
  sa,sb=[dict(line.split('=',1)for line in (p/(stem+'_state.txt')).read_text('utf-8').splitlines()if '='in line)for p in [a,b]]
  statediff.update(k for k in set(sa)|set(sb)if sa.get(k)!=sb.get(k))
  for t in expectations.values():
   if rb[t['font_RAM']]==t['font']and all(pp[t['NT']+row*64:t['NT']+row*64+len(codes)]==codes for row,codes in enumerate(t['lines'])):t['complete_frames'].append(frame)
  currency=list(rb[0x7d0:0x7d3])
  if currency!=prev:transitions.append({'first_snapshot_frame':frame,'normal_digits':currency});prev=currency
  if rb[0x18]==4 and rb[0x54]==5 and rb[0x25]==course:gameplay.append(frame)
 for t in expectations.values():assert t['complete_frames'];t['lines']=[z.hex(' ')for z in t['lines']]
 last=(b/'frame_04500_ram.bin').read_bytes();normal=sum(last[0x7d0+i]*10**i for i in range(3));assert normal==final_normal and gameplay
 result={'work':work,'status':f'PASS_BOUNDED049_{name.upper()}_CONTROLLER_READER','ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'baseline':'Fresh047 same reader observer; current049','frames_each':4500,'whole_PNG_PPU_OAM_mapping_exact':len(imgs),'actual_CHR_chunks_match_ROM':chunks,'actual_PRG_data_reads_each':len(readrows[1]),'source_read_cycle_deltas':dict(cycles),'actual_read_units':dict(groups),'full_unit_byte_coverage':required_full_units,'native_page_init_events':events,'helper_write_PC_relocations':dict(relocated),'complete_NT_targets':expectations,'currency_first_snapshot_transitions':transitions,'gameplay_frames':gameplay,'final_normal':normal,'final_root':last[0x18],'final_phase':last[0x54],'final_course_field':last[0x25],'RAM_difference_keys':dict(ramdiff),'state_difference_keys':dict(statediff),'direct_visual_review':'Pending separately','human_approved':False,'release_eligible':False,'limits':['Controller-only bounded route; not complete ride or wholeplay','Physical address connects actual source even when native ID changes','No whole CPU/globalIRQ/RNG/audio/hardware or human final review','Same-labeled PNG/RAM may differ in capture time; exact delay unproved118']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in ['actual_read_units','native_page_init_events','complete_NT_targets','gameplay_frames']},ensure_ascii=False,indent=2))
