from pathlib import Path
import csv,json,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_policy067_validation.json';assert not out.exists();q=R/'qa/dialogue/cart067_geometry_policy_v2';e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and(q/'trace_complete.txt').read_text()=='18000'
 for p,h in e['files'].items():assert sha(q/p)==h
 rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)==e['rom_sha256'];blob=rom.read_bytes()
 rows=list(csv.DictReader((q/'cart_geometry_policy.csv').open()));modes=collections.Counter(r['mode']for r in rows)
 for r in rows:
  mask=int(r['mask'],16);assert not(mask&1 and mask&2)and not(mask&4 and mask&8)
  if r['mode']!='menu':assert r['root']=='04'and r['level']=='0'
 world=list(csv.DictReader((q/'world_phase.csv').open()));play=[r for r in world if r['root']=='04'and r['phase']=='05'];assert play and set(r['life']for r in play)=={'03'}
 assert not any(r['root']=='04'and 32<=int(r['phase'],16)<=36 for r in world)
 a=(q/'frame_18000_ram.bin').read_bytes();assert a[0x400+14]!=0 and a[0x400+15]!=0 and a[0x7e0]==a[0x7e1]==0
 images=list(q.glob('frame_*.png'));chunks=0
 for p in images:
  pp=(q/(p.stem+'_ppu.bin')).read_bytes()
  for m in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
   if m['kind']!='chr':continue
   x=int(m['cpu_or_ppu_address'],16);o=int(m['relative_offset'],16);assert pp[x:x+1024]==blob[0x40010+o:0x40410+o];chunks+=1
 report={'work':67,'status':'SURVIVAL_OBSERVED_NATURALCLEAR_NOT_REACHED','ROM_SSOT_changes':0,'runtime_files':len(e['files']),'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'policy_rows':len(rows),'mode_counts':dict(modes),'play_sample_count_life3':len(play),'last_world':world[-1],'two_enemy_actors_still_present':True,'natural_bonus':False,'direct_visual':'Actual18000 viewed','failed_first_attempt':'qa/reports/cart067_lua_compile_failure.json; frozen initial Lua/runner/output retained','limits':['Survival is not a clear or proof of routing completeness','Earlier65/66 removed one enemy; this67 removed neither by18000','Only original native level0 geometry, no RAM/ROM/PC/state intervention','No wholeplay/PCM/listening/finalhumanapproval'],'next_action':'Trace enemy state4/removal write consumers in a fresh version of the earlier one-enemy-fall controller route.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_files','screens','mapped_CHR_1K_chunks_exact','mode_counts')},indent=2))
if __name__=='__main__':main()
