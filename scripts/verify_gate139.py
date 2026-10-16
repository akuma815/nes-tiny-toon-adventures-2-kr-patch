from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/gate139_validation.json';assert not out.exists()
 a,b=[R/'qa/dialogue'/n for n in ['gate094_gold4047','gate139_gold4049']]
 ea,eb=[json.loads((p/'environment.json').read_text('utf-8'))for p in [a,b]]
 assert ea['exit_code']==eb['exit_code']==0 and ea['frames']==eb['frames']==9000
 for k in ['source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256']:assert ea[k]==eb[k],k
 assert eb['seed']=={'purpose':'Controlled branch QA, not normal gameplay','frame':1000,'writes':[{'address':2016,'value':4}]}
 rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';rom=rp.read_bytes();assert sha(rp)==eb['rom_sha256']
 for d,e in [(a,ea),(b,eb)]:
  assert (d/'trace_complete.txt').read_text()=='9000'
  for f,h in e['files'].items():assert sha(d/f)==h,(d.name,f)
 assert (a/'seed_writes.csv').read_bytes()==(b/'seed_writes.csv').read_bytes()
 A,B=[rows(p/'menu_events.csv')for p in [a,b]]
 fields=['frame','kind','address','value','id','pointer','profile','font','return_bank','sp','pc','phase','ride','head_font','active_font','gold_tickets','points_low','normal_ticket0','normal_ticket1','normal_ticket2','caller']
 assert [{k:r[k]for k in fields}for r in A]==[{k:r[k]for k in fields}for r in B]
 events=[r for r in B if r['kind']=='exec'and r['address']=='9445'];assert all(s in [r['id']for r in events]for s in ['1C','22','28','2A'])
 imgs=sorted(f for f in eb['files']if f.endswith('.png'));assert imgs==sorted(f for f in ea['files']if f.endswith('.png'))
 ramdiff=collections.Counter();statediff=collections.Counter();chunks=0;gameplay=0
 for f in imgs:
  stem=f[:-4];ra,rb=[(p/(stem+'_ram.bin')).read_bytes()for p in [a,b]]
  ramdiff.update(f'{i:04X}'for i,(x,y)in enumerate(zip(ra,rb))if x!=y)
  for suffix in ['_ppu.bin','_oam.bin','_mapping.csv']:assert (a/(stem+suffix)).read_bytes()==(b/(stem+suffix)).read_bytes(),(f,suffix)
  assert ImageChops.difference(Image.open(a/f).convert('RGB'),Image.open(b/f).convert('RGB')).getbbox()is None,f
  pp=(b/(stem+'_ppu.bin')).read_bytes()
  for z in rows(b/(stem+'_mapping.csv')):
   if z['kind']!='chr':continue
   addr=int(z['cpu_or_ppu_address'],16);off=int(z['relative_offset'],16)
   assert pp[addr:addr+1024]==rom[0x40010+off:0x40410+off];chunks+=1
  sa,sb=[dict(line.split('=',1)for line in (p/(stem+'_state.txt')).read_text('utf-8').splitlines()if '='in line)for p in [a,b]]
  statediff.update(k for k in set(sa)|set(sb)if sa.get(k)!=sb.get(k))
  if rb[0x18]==4 and rb[0x54]==5 and rb[0x25]==4:gameplay+=1
 # Source paragraph1C has a simple native one-line byte stream; no macro/dynamic token.
 ptr=int.from_bytes(rom[0x255e1:0x255e3],'little') # table slot1C
 assert ptr==0x9814
 stream=rom[0x24010+ptr-0x8000:0x24010+ptr-0x8000+15]
 end=stream.index(255);codes=stream[:end];assert all(z<128 for z in codes)
 completed=[]
 for f in imgs:
  stem=f[:-4];ram=(b/(stem+'_ram.bin')).read_bytes();ppu=(b/(stem+'_ppu.bin')).read_bytes()
  if ram[0x6f3]==185 and ppu[0x22a8:0x22a8+len(codes)]==codes:completed.append(int(stem[6:]))
 assert completed and gameplay>0
 last=(b/'frame_09000_ram.bin').read_bytes();assert last[0x7e0]==4 and list(last[0x7d0:0x7d3])==[0,1,0]
 result={'work':139,'status':'PASS_BOUNDED049_GOLD4_CASTLE_BRANCH','ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'baseline':'historical047 gate094_gold4047','frames':9000,'whole_PNG_PPU_OAM_mapping_exact':len(imgs),'CHR_chunks_current_ROM_exact':chunks,'protected_menu_events_exact':len(B),'native_init_events':events,'completed_MAIN05824_slot1C_frames':completed,'slot1C_expected_NT_hex':codes.hex(' '),'castle_gameplay_screens':gameplay,'RAM_difference_keys':dict(ramdiff),'CPU_state_difference_keys':dict(statediff),'final_gold':4,'final_normal':10,'actual_source_reader_bytes':'Not separately observed; static ROM byte stream plus actual completedNT verified','direct_visual_review':'Pending separately','human_approved':False,'release_eligible':False,'limits':['Initial gold4 seed, not naturally earned tickets or castle completion','Whole CPU/RNG/IRQ timing equality not claimed; difference fields retained','No new ROM/build/apply/state/audio/hardware or human final review']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in ['native_init_events','completed_MAIN05824_slot1C_frames']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
