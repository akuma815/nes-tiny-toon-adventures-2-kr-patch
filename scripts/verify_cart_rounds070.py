from pathlib import Path
import csv,json,hashlib,collections
from verify_cart_geometry066 import classify
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_rounds070_validation.json';assert not out.exists();rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';b=rom.read_bytes();old={int(r['frame']):r for r in csv.DictReader((R/'qa/dialogue/cart065_charge_v2/cart_policy.csv').open())};reports=[];cache={};total=0
 for name in('cart070_rounds_v1','cart070_rounds_v2'):
  q=R/'qa/dialogue'/name;e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['rom_sha256']==sha(rom)and(q/'trace_complete.txt').read_text()=='18000'
  for p,h in e['files'].items():assert sha(q/p)==h;total+=1
  rows=list(csv.DictReader((q/'cart_round_policy.csv').open()));diff=sum(r['mask']!=old[int(r['frame'])]['mask']for r in rows if int(r['frame'])<4200)
  assert diff==(566 if name.endswith('v1')else 0)
  levels=sorted(set(int(r['level'])for r in rows));queries=list(csv.DictReader((q/'cart_tile_queries.csv').open()))
  for r in queries:
   k=tuple(int(r[x])for x in('x_page','x_low','y_page','y_low','level'))
   if k not in cache:cache[k]=classify(b,*k)
   assert int(r['class'])==cache[k]
  world=list(csv.DictReader((q/'world_phase.csv').open()));changes=[{'frame':r['frame'],'level':r['level'],'phase':r['phase'],'life':r['life']}for i,r in enumerate(rows)if not i or r['level']!=rows[i-1]['level']]
  if name.endswith('v2'):
   assert levels==[0,1]and changes[1]['frame']=='4970'and changes[1]['phase']=='0E'
   before=(q/'frame_04830_ram.bin').read_bytes();after=(q/'frame_04980_ram.bin').read_bytes()
   assert before[0x42d:0x430]==b'\0\0\0'and before[0x430]==5 and after[0x79]==1 and after[0x54]==14
   assert all(r['life']=='03'for r in world if r['root']=='04'and r['phase']=='05')
   assert rows[-1]['history']==rows[-1]['gold']=='00'
  reports.append({'QA':name,'prefix_mask_differences':diff,'levels_observed':levels,'native_level_changes':changes,'tile_queries_exact':len(queries),'last_world':world[-1],'mode_counts':dict(collections.Counter(r['mode']for r in rows))})
 report={'work':70,'status':'NATURAL_FIRST_CART_ROUND_CLEAR_NEXT_ROUND_PENDING','ROM_SSOT_changes':0,'runtime_files':total,'runs':reports,'unique_native_tile_inputs_exact':len(cache),'geometry_runtime_coverage':'Levels0/1 query consumer observed; level2 remains static only. Raw models may read outside valid arena; only player-connected interior is routed.','direct_visual':'No new direct screen inspection yet; native state/typed object/actualquery evidence','limits':['First of3 cart rounds cleared naturally; no finalcartbonus/history/gold or wholeplay','V1 deadzone mismatch preserved and documented; V2 prefix0differences','Level1 routing stalls atuppercorridor; four-celllookahead maycutcorner, needs segment/clearance checks','No ROM/RAM/PC/state/reset/life/currency edits'],'next_action':'Fix geometric lookahead to require a clear line within the native interior, then extend the same controller run budget to attempt all3 rounds.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in('status','runtime_files','unique_native_tile_inputs_exact')},indent=2))
if __name__=='__main__':main()
