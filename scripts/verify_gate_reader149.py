"""Seeded castle branches: physical source reads, full pages and paired renders."""
from verify_reader_pair142 import R,sha,rows,native_lines
from PIL import Image,ImageChops
import collections,json

def verify(route,frames,oldname,newname,slots,targets,required):
 a,b=[R/'qa/dialogue'/n for n in [oldname,newname]]
 ea,eb=[json.loads((d/'environment.json').read_text('utf-8'))for d in [a,b]]
 assert ea['exit_code']==eb['exit_code']==0 and ea['frames']==eb['frames']==frames
 for k in ['source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256']:assert ea[k]==eb[k],k
 assert ea['seed']['frame']==1000
 for d,e in [(a,ea),(b,eb)]:
  assert (d/'trace_complete.txt').read_text()==str(frames)
  for f,h in e['files'].items():assert sha(d/f)==h,(d.name,f)
 assert (a/'seed_writes.csv').read_bytes()==(b/'seed_writes.csv').read_bytes()
 rom=(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 old=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 import hashlib
 assert hashlib.sha256(rom).hexdigest()==eb['rom_sha256'] and hashlib.sha256(old).hexdigest()==ea['rom_sha256']
 A,B=[rows(d/'menu_events.csv')for d in [a,b]];assert len(A)==len(B)
 reloc=collections.Counter()
 for x,y in zip(A,B):
  assert {k:v for k,v in x.items()if k!='pc'}=={k:v for k,v in y.items()if k!='pc'}
  if x['pc']==y['pc']:continue
  assert x['kind']=='write'and(x['pc'],y['pc'],x['address'])in [('9613','964A','00C6'),('9616','964D','06F3'),('961C','9653','0034')]
  po,pn=[0x4010+int(z['pc'],16)-0x8000 for z in [x,y]];n=3 if x['address']=='06F3'else 2
  assert old[po-n:po]==rom[pn-n:pn] and old[po-n]==(0x8d if n==3 else 0x85)
  reloc[x['pc']+'->'+y['pc']+'/'+x['address']]+=1
 events=[r for r in B if r['kind']=='exec'and r['address']=='9445'];assert set(slots)<={r['id']for r in events}
 cat=json.loads((R/'extracted/text/table_20261004_001/text_tokens.json').read_text('utf-8'))
 rr=[rows(d/'prg_text_reads.csv')for d in [a,b]];assert rr[0]and len(rr[0])==len(rr[1])
 groups=collections.defaultdict(list);cycles=collections.Counter()
 for x,y in zip(*rr):
  assert {k:v for k,v in x.items()if k!='cycles'}=={k:v for k,v in y.items()if k!='cycles'}
  f=int(y['PRG_relative_offset'],16)+16;assert rom[f]==old[f]==int(y['value'],16)
  us=[u for u in cat['units']if u['file_offset']+0x20000<=f<u['end_exclusive']+0x20000];assert len(us)==1;u=us[0]
  p=0x24010+int(y['pc'],16)-0x8000;assert y['pc']in ['9395','9362','92CF']and rom[p-2:p]==bytes.fromhex('b1 06')
  groups[u['entry_id']].append({'frame':int(y['frame']),'source_relative_offset':f-u['file_offset']-0x20000,'value_hex':y['value'],'native_id_hex':y['native_id'],'reader_PC':y['pc'],'active_font':int(y['active_font'],16)})
  cycles[int(y['cycles'])-int(x['cycles'])]+=1
 for unit in required:
  u=next(z for z in cat['units']if z['entry_id']==unit)
  assert set(z['source_relative_offset']for z in groups[unit])==set(range(u['end_exclusive']-u['file_offset'])),unit
 expectations={str(slot):{'slot':slot,'NT':nt,'font_RAM':fr,'font':rom[0x5710+2*slot],'lines':native_lines(rom,slot),'complete_frames':[]}for slot,nt,fr in targets}
 imgs=sorted(f for f in eb['files']if f.endswith('.png'));assert imgs==sorted(f for f in ea['files']if f.endswith('.png'))
 ramdiff=collections.Counter();statediff=collections.Counter();chunks=0;trans=[];prev=None;game=[]
 for f in imgs:
  stem=f[:-4];frame=int(stem[6:]);ra,rb=[(d/(stem+'_ram.bin')).read_bytes()for d in [a,b]]
  ramdiff.update(f'{i:04X}'for i,(x,y)in enumerate(zip(ra,rb))if x!=y)
  for suffix in ['_ppu.bin','_oam.bin','_mapping.csv']:assert (a/(stem+suffix)).read_bytes()==(b/(stem+suffix)).read_bytes(),(f,suffix)
  assert ImageChops.difference(Image.open(a/f).convert('RGB'),Image.open(b/f).convert('RGB')).getbbox()is None,f
  pp=(b/(stem+'_ppu.bin')).read_bytes()
  for z in rows(b/(stem+'_mapping.csv')):
   if z['kind']!='chr':continue
   addr=int(z['cpu_or_ppu_address'],16);off=int(z['relative_offset'],16)
   assert pp[addr:addr+1024]==rom[0x40010+off:0x40410+off];chunks+=1
  sa,sb=[dict(line.split('=',1)for line in (d/(stem+'_state.txt')).read_text('utf-8').splitlines()if '='in line)for d in [a,b]]
  statediff.update(k for k in set(sa)|set(sb)if sa.get(k)!=sb.get(k))
  for t in expectations.values():
   if rb[t['font_RAM']]==t['font']and all(pp[t['NT']+row*64:t['NT']+row*64+len(codes)]==codes for row,codes in enumerate(t['lines'])):t['complete_frames'].append(frame)
  currency=(list(rb[0x7d0:0x7d3]),rb[0x7e0])
  if currency!=prev:trans.append({'first_snapshot_frame':frame,'normal_digits':currency[0],'gold':currency[1]});prev=currency
  if rb[0x18]==4 and rb[0x54]==5 and rb[0x25]==4:game.append(frame)
 for t in expectations.values():assert t['complete_frames'],t;t['lines']=[z.hex(' ')for z in t['lines']]
 last=(b/f'frame_{frames:05d}_ram.bin').read_bytes();normal=sum(last[0x7d0+i]*10**i for i in range(3))
 if route=='normal49':assert normal==49 and last[0x7e0]==0 and last[0x18]==8 and not game
 else:assert normal==10 and last[0x7e0]==4 and game
 return {'route':route,'baseline_directory':a.relative_to(R).as_posix(),'current_directory':b.relative_to(R).as_posix(),'frames_each':frames,'ROM_sha256':eb['rom_sha256'],'whole_PNG_PPU_OAM_mapping_exact':len(imgs),'actual_CHR_chunks_match_ROM':chunks,'actual_PRG_data_reads_each':len(rr[1]),'source_read_cycle_deltas':dict(cycles),'actual_read_units':dict(groups),'full_unit_byte_coverage':required,'native_page_init_events':events,'helper_write_PC_relocations':dict(reloc),'complete_NT_targets':expectations,'currency_first_snapshot_transitions':trans,'gameplay_frames':game,'final_normal':normal,'final_gold':last[0x7e0],'final_root':last[0x18],'final_phase':last[0x54],'RAM_difference_keys':dict(ramdiff),'state_difference_keys':dict(statediff)}

def main():
 out=R/'qa/reports/gatereader149_validation.json';assert not out.exists()
 routes=[verify('normal49',6000,'gatereader148_normal49_047','gatereader148_normal49_049_resume',['0F','16','17','18','19','1A','1B'],[(s,0x22a8,0x6f3)for s in [0xf,0x16,0x17,0x18,0x19,0x1b]],['MAIN_05759','MAIN_057B8','MAIN_057C1','MAIN_057E5','MAIN_057F7','MAIN_05805','MAIN_0581B']),verify('gold4',9000,'gatereader148_gold4_047','gatereader148_gold4_049',['0F','16','17','1C','22','28','2A'],[(s,0x22a8,0x6f3)for s in [0xf,0x16,0x17,0x1c,0x2a]]+[(0x22,0x2125,0x34),(0x28,0x20a6,0x34)],['MAIN_05759','MAIN_057B8','MAIN_057C1','MAIN_05824','MAIN_058CD','MAIN_05902'])]
 result={'work':149,'status':'PASS_BOUNDED_SEEDED_CASTLE_READER','routes':routes,'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'human_approved':False,'release_eligible':False,'direct_visual_review':'Pending separately','limits':['Explicit initial currency seed; no natural earnings/full castle completion','Dynamic MAIN05805 full source reads proven; complete expanded NT excluded from zero-RAM reader model','No global CPU/IRQ/RNG/audio/hardware identity or human approval','Same-labeled PNG/RAM capture time not assumed identical','Interrupted148 capture preserved and excluded']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({'status':result['status'],'routes':[{k:v for k,v in x.items()if k not in ['actual_read_units','native_page_init_events','complete_NT_targets','gameplay_frames']}for x in routes]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
