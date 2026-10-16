"""Work65: validate bounded controller-only charge/release evidence, not natural completion."""
from pathlib import Path
import csv,json,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_charge065_validation.json';assert not out.exists()
 q=R/'qa/dialogue/cart065_charge_v2';e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==18000 and(q/'trace_complete.txt').read_text()=='18000'
 rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)==e['rom_sha256'];blob=rom.read_bytes()
 for p,h in e['files'].items():assert sha(q/p)==h,p
 rows=list(csv.DictReader((q/'cart_policy.csv').open()));play=[r for r in rows if int(r['desired_heading'])>=0]
 for r in rows:
  mask=int(r['mask'],16);assert not(mask&1 and mask&2)and not(mask&4 and mask&8)
  if int(r['desired_heading'])>=0:
   assert r['root']=='04' and r['phase']=='05' and r['course']=='01'
   assert not mask&64 and bool(mask&128)==(int(r['frame'])%64<40)
   assert 0<=int(r['charge'])<=1024 and int(r['target_type'])in(-1,46,47)
 byframe={int(r['frame']):r for r in rows};sample=[byframe[f]for f in (3492,3496,3497)]
 assert [int(r['charge'])for r in sample]==[1024,1024,0]
 assert [r['mask']for r in sample]==['85','05','05']
 assert [int(r['velocity_y'])for r in sample]==[0,0,717]
 world=list(csv.DictReader((q/'world_phase.csv').open()));assert len(world)==600
 assert not any(r['root']=='04'and 32<=int(r['phase'],16)<=36 for r in world)
 assert world[-1]['root']=='08' and world[-1]['life']==world[-1]['history']==world[-1]['gold']=='00'
 images=list(q.glob('frame_*.png'));chunks=0
 for p in images:
  pp=(q/(p.stem+'_ppu.bin')).read_bytes()
  for m in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
   if m['kind']!='chr':continue
   a=int(m['cpu_or_ppu_address'],16);off=int(m['relative_offset'],16);assert pp[a:a+1024]==blob[0x40010+off:0x40410+off];chunks+=1
 report={'work':65,'status':'CHARGE_RELEASE_OBSERVED_NATURALCLEAR_NOT_REACHED','ROM_sha256':sha(rom),'ROM_SSOT_changes':0,'runtime_frozen_files':len(e['files']),'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'policy_rows':len(rows),'native_play_policy_rows':len(play),'nonzero_velocity_play_rows':sum(int(r['velocity_x'])!=0 or int(r['velocity_y'])!=0 for r in play),'maximum_charge':max(int(r['charge'])for r in play),'observed_velocity_ranges':{k:[min(int(r[k])for r in play),max(int(r[k])for r in play)]for k in ('velocity_x','velocity_y')},'charge_release_sample':sample,'last_world':world[-1],'life_changes':[(r['frame'],r['life'])for i,r in enumerate(world)if not i or r['life']!=world[i-1]['life']],'direct_visual':'Actual12000 screenshot viewed; not all-screen human review','scope':'No RAM/ROM/PC/state/reset/currency/life edits; adaptive controller only. A charge and release evidence strengthens control mapping, not a winning policy or whole-game QA.','limits':['Natural cart clear and bonus absent; all three lives lost','No PCM/listening/hardware/finalhumanreview','Pursuit does not account for pit geometry or momentum'],'next_action':'Trace native cart collision/pit and remaining-enemy consumers before another pursuit policy.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_frozen_files','screens','mapped_CHR_1K_chunks_exact','maximum_charge','nonzero_velocity_play_rows')},indent=2))
if __name__=='__main__':main()
