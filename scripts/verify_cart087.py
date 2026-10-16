"""Work87 one-controller-policy experiment; preserve failure as failure."""
from pathlib import Path
import hashlib,json,csv,collections
from verify_cart_geometry066 import classify
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart087_validation.json';assert not out.exists();q=R/'qa/dialogue/cart087_no2Fbrake046';env=json.loads((q/'environment.json').read_text('utf-8'));assert env['exit_code']==0 and env['frames']==36000 and(q/'trace_complete.txt').read_text()=='36000'
 for n,h in env['files'].items():assert sha(q/n)==h,n
 rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();assert sha(rom)==env['rom_sha256']
 old=(R/'scripts/trace_cart_rounds_v4.lua').read_text('utf-8');change="if mode~='push'and vx*vx+vy*vy>6.25 then input.b=true end";new=old.replace(change,"if mode~='push'and vx*vx+vy*vy>6.25 and not(level>=1 and targettype==0x2f and mode=='intercept')then input.b=true end").replace('Work72 fine8px','Work87: only2F intercept automaticB disabled; pitB retained. Work72 fine8px');assert new==(q/'capture_survey_used.lua').read_text('utf-8')
 rows=list(csv.DictReader((q/'cart_round_policy.csv').open()));before={int(r['frame']):r for r in csv.DictReader((R/'qa/dialogue/start077_cart045/cart_round_policy.csv').open())};diffs=[int(r['frame'])for r in rows if int(r['frame'])in before and r['mask']!=before[int(r['frame'])]['mask']];assert diffs;first=min(diffs)
 prefix=[r for r in rows if int(r['frame'])<first];assert all(r['mask']==before[int(r['frame'])]['mask']for r in prefix)
 firstrow=next(r for r in rows if int(r['frame'])==first);oldrow=before[first];assert firstrow['target_type']=='47' and firstrow['mode']=='intercept'and int(oldrow['mask'],16)^int(firstrow['mask'],16)==64
 selected=[r for r in rows if r['level']=='1'and r['phase']=='05'and r['target_type']=='47'and r['mode']=='intercept'];assert selected and all(not(int(r['mask'],16)&64)for r in selected)
 for r in rows:
  m=int(r['mask'],16);assert not(m&1 and m&2)and not(m&4 and m&8)
 exact=0
 for p in q.glob('frame_*.png'):
  if int(p.stem.split('_')[1])>=first:continue
  for suffix in ('.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):
   x=q/(p.stem+suffix);assert x.read_bytes()==(R/'qa/dialogue/start077_cart045'/x.name).read_bytes();exact+=1
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
 world=list(csv.DictReader((q/'world_phase.csv').open()));assert world[-1]['root']=='08'and world[-1]['gold']==world[-1]['history']=='00';assert any(r['phase']=='11'and r['root']=='04'for r in world);assert set(int(r['level'])for r in queries)=={0,1}
 finalplay=[r for r in rows if r['level']=='1'and r['phase']=='05'][-1];assert finalplay['remaining13']==finalplay['remaining14']=='00'and finalplay['remaining15']=='2F'
 result={'work':87,'status':'PASS_OBSERVATION_NATURAL_CLEAR_NOT_ACHIEVED','ROM_sha256':sha(rom),'ROM_SSOT_changes':0,'runtime_frozen_files':len(env['files']),'screens':len(images),'CHR_1K_chunks_exact':chunks,'first_policy_divergence_frame':first,'first_changed_mask':{'old':oldrow['mask'],'new':firstrow['mask']},'same_policy_prefix_rows':len(prefix),'same_baseline_prefix_files':exact,'2F_intercept_rows_B_disabled':len(selected),'policy_rows':len(rows),'native_tile_queries_exact':len(queries),'unique_native_query_inputs':len(cache),'last_play_before_timeout':finalplay,'last_world':world[-1],'natural_all3_clear':False,'result':'Firstcart segment reproduced, secondsegment final2F remained then timeout/home. Removing onlyinterceptB did not solve fullclear. No new equivalent bot retry without new nativecollision evidence.','scope':'Controller-only isolated policy experiment. No ROM/translation changes, no wholeplay or humanapproval claim.'}
 out.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','first_policy_divergence_frame','same_baseline_prefix_files','2F_intercept_rows_B_disabled','native_tile_queries_exact','unique_native_query_inputs']}))
if __name__=='__main__':main()