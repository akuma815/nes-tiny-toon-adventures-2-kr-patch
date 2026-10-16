from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
from verify_dialogue_home import reader
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/booth141_validation.json';assert not out.exists()
 a,b=[R/'qa/dialogue'/n for n in ['booth141_points3_047','booth141_points3_049']]
 ea,eb=[json.loads((p/'environment.json').read_text('utf-8'))for p in [a,b]]
 assert ea['exit_code']==eb['exit_code']==0 and ea['frames']==eb['frames']==4500
 for k in ['source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256']:assert ea[k]==eb[k],k
 assert eb['seed']['frame']==1000 and eb['seed']['writes']==[{'address':x,'value':3 if x==0x7f2 else 0}for x in range(0x7f2,0x7f7)]
 rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';rom=rp.read_bytes();oldrom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
 assert sha(rp)==eb['rom_sha256'] and hashlib.sha256(oldrom).hexdigest()==ea['rom_sha256']
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
 events=[r for r in B if r['kind']=='exec'and r['address']=='9445'];assert any(r['id']=='15'and r['active_font']=='BC'for r in events)
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
 assert 'MAIN_057AC'in groups and 'MACRO_061FA'in groups
 farewell=next(u for u in cat['units']if u['entry_id']=='MAIN_057AC')
 assert set(g['source_relative_offset']for g in groups['MAIN_057AC'])==set(range(farewell['end_exclusive']-farewell['file_offset']))
 assert set(g['source_relative_offset']for g in groups['MACRO_061FA'])==set(range(5))
 view=bytearray(rom);view[0x4010:0x8010]=rom[0x24010:0x28010]
 ptr=int.from_bytes(rom[0x255d3:0x255d5],'little');assert ptr==0x979c
 values=reader(view,ptr);lines=[];line=[]
 for z in values:
  if z['value']in [254,255]:lines.append(bytes(line));line=[]
  else:line.append(z['value'])
 assert len(lines)==2
 imgs=sorted(f for f in eb['files']if f.endswith('.png'));assert imgs==sorted(f for f in ea['files']if f.endswith('.png'))
 ramdiff=collections.Counter();statediff=collections.Counter();chunks=0;complete=[];transitions=[];prev=None
 for f in imgs:
  stem=f[:-4];ra,rb=[(p/(stem+'_ram.bin')).read_bytes()for p in [a,b]]
  ramdiff.update(f'{i:04X}'for i,(x,y)in enumerate(zip(ra,rb))if x!=y)
  for suffix in ['_ppu.bin','_oam.bin','_mapping.csv']:assert (a/(stem+suffix)).read_bytes()==(b/(stem+suffix)).read_bytes(),(f,suffix)
  assert ImageChops.difference(Image.open(a/f).convert('RGB'),Image.open(b/f).convert('RGB')).getbbox()is None,f
  pp=(b/(stem+'_ppu.bin')).read_bytes()
  for z in rows(b/(stem+'_mapping.csv')):
   if z['kind']!='chr':continue
   addr=int(z['cpu_or_ppu_address'],16);off=int(z['relative_offset'],16);assert pp[addr:addr+1024]==rom[0x40010+off:0x40410+off];chunks+=1
  sa,sb=[dict(line.split('=',1)for line in (p/(stem+'_state.txt')).read_text('utf-8').splitlines()if '='in line)for p in [a,b]]
  statediff.update(k for k in set(sa)|set(sb)if sa.get(k)!=sb.get(k))
  if rb[0x6f3]==188 and all(pp[0x22a8+row*64:0x22a8+row*64+len(codes)]==codes for row,codes in enumerate(lines)):complete.append(int(stem[6:]))
  currency=(list(rb[0x7d0:0x7d3]),list(rb[0x7f2:0x7f7]))
  if currency!=prev:transitions.append({'first_snapshot_frame':int(stem[6:]),'normal_digits':currency[0],'point_digits':currency[1]});prev=currency
 assert complete
 last=(b/'frame_04500_ram.bin').read_bytes();assert list(last[0x7d0:0x7d3])==[1,1,0]and not any(last[0x7f2:0x7f7])
 result={'work':141,'status':'PASS_BOUNDED049_BOOTH_SUCCESS_ACTUAL_PRG_READER','ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'baseline':'Fresh047 same new read-only observer; historical039 only input/seed supplier','frames_each':4500,'whole_PNG_PPU_OAM_mapping_exact':len(imgs),'actual_CHR_chunks_match_ROM':chunks,'actual_PRG_data_reads_each':len(readrows[1]),'all_read_values_mapping_context_PC_order_frame_exact':True,'source_read_cycle_deltas':dict(cycles),'actual_read_units':dict(groups),'native_page_init_events':events,'helper_write_PC_relocations':dict(relocated),'farewell_completed_NT_frames':complete,'farewell_native_reader_expected_lines':[z.hex(' ')for z in lines],'currency_first_snapshot_transitions':transitions,'final_normal':11,'final_points':0,'RAM_difference_keys':dict(ramdiff),'state_difference_keys':dict(statediff),'direct_visual_review':'Pending separately','human_approved':False,'release_eligible':False,'limits':['Point digit3 (300-point unit) explicitly seeded, not naturally earned points','Native ID can already advance; physical PRG address connects actual source independently','Reader exactness only this booth path; not all54/globalcorpus','No whole CPU/globalIRQ/audio/hardware/wholeplay/human approval']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in ['actual_read_units','native_page_init_events','farewell_completed_NT_frames']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
