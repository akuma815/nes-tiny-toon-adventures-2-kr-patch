"""Work89 controller experiment evidence, explicitly unsuccessful wholeclear."""
from pathlib import Path
import hashlib,json,csv
from verify_cart_geometry066 import classify
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart089_validation.json';assert not out.exists();q=R/'qa/dialogue/cart089_aligned2F046';env=json.loads((q/'environment.json').read_text('utf-8'));assert env['exit_code']==0 and env['frames']==36000 and(q/'trace_complete.txt').read_text()=='36000'
 for n,h in env['files'].items():assert sha(q/n)==h,n
 rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();assert sha(rom)==env['rom_sha256'];assert(q/'capture_survey_used.lua').read_bytes()==(R/'scripts/trace_cart_rounds_v6.lua').read_bytes()
 rows=list(csv.DictReader((q/'cart_round_policy.csv').open()));baseline=R/'qa/dialogue/cart087_no2Fbrake046';before={int(r['frame']):r for r in csv.DictReader((baseline/'cart_round_policy.csv').open())};first=min(int(r['frame'])for r in rows if r['mask']!=before[int(r['frame'])]['mask']);assert first>=14276
 prefix=[r for r in rows if int(r['frame'])<first];assert all(r['mask']==before[int(r['frame'])]['mask']for r in prefix);same=0
 for p in q.glob('frame_*.png'):
  if int(p.stem.split('_')[1])>=first:continue
  for suffix in ('.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):
   x=q/(p.stem+suffix);assert x.read_bytes()==(baseline/x.name).read_bytes();same+=1
 release=list(csv.DictReader((q/'cart2F_release_policy.csv').open()));until=0;bursts=[];eligible=0
 for r in release:
  frame=int(r['frame']);charge=int(r['charge']);alignment=float(r['alignment']);e=r['eligible']=='true'
  if e:assert r['mode']=='push'and charge>=512 and alignment>0.8;eligible+=1
  if e and frame>=until:until=frame+16;bursts.append({'frame':frame,'charge':charge,'alignment':alignment,'base_vx':r['base_vx'],'base_vy':r['base_vy']})
  assert int(r['burst_until'])==until
  if frame<until:assert r['A']=='false'
  elif r['mode']=='push':assert r['A']=='true'
 assert bursts
 for r in rows:
  m=int(r['mask'],16);assert not(m&1 and m&2)and not(m&4 and m&8)
 cache={};queries=list(csv.DictReader((q/'cart_tile_queries.csv').open()))
 for r in queries:
  k=tuple(int(r[x])for x in('x_page','x_low','y_page','y_low','level'))
  if k not in cache:cache[k]=classify(blob,*k)
  assert cache[k]==int(r['class'])
 images=list(q.glob('frame_*.png'));chunks=0
 for p in images:
  ppu=(q/(p.stem+'_ppu.bin')).read_bytes()
  for m in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
   if m['kind']=='chr':aa=int(m['cpu_or_ppu_address'],16);bb=int(m['relative_offset'],16);assert ppu[aa:aa+1024]==blob[0x40010+bb:0x40410+bb];chunks+=1
 world=list(csv.DictReader((q/'world_phase.csv').open()));assert world[-1]['root']=='08'and world[-1]['history']==world[-1]['gold']=='00';assert any(r['phase']=='11'and r['root']=='04'for r in world);final=[r for r in rows if r['level']=='1'and r['phase']=='05'][-1];assert final['remaining15']=='2F'
 result={'work':89,'status':'PASS_OBSERVATION_NATURAL_CLEAR_NOT_ACHIEVED','ROM_sha256':sha(rom),'ROM_CSV_changes':0,'runtime_frozen_files':len(env['files']),'screens':len(images),'CHR_chunks_exact':chunks,'first_controller_divergence':first,'same_V5_prefix_rows':len(prefix),'same_V5_prefix_files':same,'native_direction_gated_bursts':bursts,'eligible_rows':eligible,'release_rows':len(release),'actual_queries_exact':len(queries),'unique_query_inputs':len(cache),'last_play_before_timeout':final,'last_world':world[-1],'natural_fullclear':False,'decision':'Input variants87/89 have equivalent fullclear failure. Further repeatedwinningbot attempts are lower value; preserve bounded proof and move back to source/context language review, keeping naturalfullplay explicitly unperformed.','scope':'Controller-only strict2F approach/native-vector-gatedA release; no game code edits or wholeplay success.'}
 out.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','first_controller_divergence','same_V5_prefix_files','eligible_rows','native_direction_gated_bursts','actual_queries_exact','runtime_frozen_files']}))
if __name__=='__main__':main()