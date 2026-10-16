from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
from analyze_river120_v2 import machine
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def setup(rom,row,ram):
 m,c=machine(rom);m.banks=[int(row[k],16)//8192+32 for k in ['bank8000','bankA000','bankC000','bankE000']];m.ram[:2048]=ram
 c.a=int(row['a']);c.x=int(row['x']);c.y=int(row['y']);c.sp=int(row['sp']);c.p=int(row['ps'])&~8
 return m,c
def main():
 out=R/'qa/reports/water154_damage_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water154_damage049';h=R/'qa/dialogue/water153_jump049_v2'
 e,he=[json.loads((p/'environment.json').read_text('utf-8'))for p in [d,h]]
 assert e['exit_code']==0 and e['frames']==4200 and (d/'trace_complete.txt').read_text()=='4200'
 for k in ['rom_sha256','source_sha256','exe_sha256','config_sha256','input','intervention']:assert e[k]==he[k],k
 for f,digest in e['files'].items():assert sha(d/f)==digest
 identical=0
 for f in e['files']:
  if not f.startswith('frame_'):continue
  assert sha(h/f)==he['files'][f]
  if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
  else:assert (d/f).read_bytes()==(h/f).read_bytes()
  identical+=1
 events=rows(d/'damage_events.csv');assert len(events)==6
 paths=[R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'];roms=[p.read_bytes()for p in paths]
 assert sha(paths[1])==e['rom_sha256']and sha(paths[0])==e['source_sha256']
 assert roms[0][0x1e6c5:0x1e6fd]==roms[1][0x3e6c5:0x3e6fd]and roms[0][0x12ca5:0x12ca8]==roms[1][0x32ca5:0x32ca8]
 replay=[];hazards=[];geometry=[]
 for row in events:
  ram=(d/f"damage_{int(row['event']):04d}_before_ram.bin").read_bytes();addr=int(row['address'],16);pc=int(row['pc'],16);pair=[]
  assert ram[addr]==int(row['before'])
  for rom in roms:
   m,c=setup(rom,row,ram);c.pc=pc-3
   assert bytes(m[c.pc+i]for i in range(3)).hex().upper()==row['preceding3_hex']
   c.step();expected=bytearray(ram);expected[addr]=int(row['value']);assert m.ram[:2048]==expected and c.pc==pc
   pair.append((c.a,c.x,c.y,c.sp,c.p,c.processorCycles))
  assert pair[0]==pair[1];replay.append({'event':int(row['event']),'store_PC':f'{pc-3:04X}','address':row['address'],'cycles':pair[0][-1]})
  if addr!=0x430:continue
  assert pc==0xe6e7 and row['preceding3_hex']=='8D3004'and int(row['value'])==6
  actor=int(row['x']);assert ram[0x420+actor]==0x44 and ram[0x400+actor]==0x6c
  hazards.append({'frame_label':int(row['frame']),'actor_slot':actor,'actor_type_hex':'44','actor_art_hex':'6C','native_hit_PC':'E6E4','player_state_before':ram[0x430],'supportC1':ram[0xc1],'life':ram[0x7c0]})
  for rise in [0,8,16,24,32,40,48,56]:
   b=bytearray(ram);y=(b[0x480]*256+b[0x470]-rise)&65535;b[0x480]=y>>8;b[0x470]=y&255
   outcomes=[]
   for rom in roms:
    m,c=setup(rom,row,b);c.pc=0xe6b5;c.sp=0xfd;m.ram[0x1fe:0x200]=bytes.fromhex('ff5f');trace=[]
    while c.pc!=0x6000:c.step();trace.append(c.pc);assert len(trace)<2000
    outcomes.append((c.a,c.x,c.y,c.sp,c.p,c.processorCycles,bytes(m.ram)))
   assert outcomes[0]==outcomes[1]
   hit=outcomes[0][-1][0x430]==6
   if rise==0:assert hit
   geometry.append({'damage_frame':int(row['frame']),'synthetic_player_rise_pixels':rise,'hit':hit,'cycles':outcomes[0][-2],'scope':'Offline same actor instant with only player Y shifted; not runtime camera/coordinate edit or full jump trajectory'})
 assert [(int(r['before']),int(r['value']))for r in events if r['address']=='07C0']==[(3,2),(2,1),(1,0)]
 result={'work':154,'status':'PASS_ACTUAL_WATER_DAMAGE_CONSUMER_AND_BOUNDED_GEOMETRY','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'frames':4200,'same153_snapshot_artifacts_exact':identical,'actual_damage_events':events,'single_store_CPU_pairs':replay,'actual_hazard_binding':hazards,'geometry_CPU_case_pairs':geometry,'finding':'All three actual hits come from fixed E6B5 actor collision, type44/art6C slots15/15/12, not the water terrain A8E2 callback. Native E6E4 sets state6; river AC95 later decrements life3→2→1→0. Terrain hit entry observed0 in153. Offline vertical separation discriminates collision at those actual actor states.','human_approved':False,'release_eligible':False,'limits':['Read-only observer/same inputs; no new route or natural clear','Synthetic Y shifts are offline CPU cases only; neither natural jump timing nor future actor trajectories proven','No new build/apply/reset/state/hardware/audio/human review']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in ['actual_damage_events','geometry_CPU_case_pairs']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
