from pathlib import Path
import csv,json,hashlib,collections
from verify_cart_geometry066 import classify
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_runtime071_validation.json';assert not out.exists();q=R/'qa/dialogue/cart071_axis_v3';e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==36000 and(q/'trace_complete.txt').read_text()=='36000'
 for p,h in e['files'].items():assert sha(q/p)==h
 blob=(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert hashlib.sha256(blob).hexdigest()==e['rom_sha256']
 rows=list(csv.DictReader((q/'cart_round_policy.csv').open()));old={int(r['frame']):r for r in csv.DictReader((R/'qa/dialogue/cart070_rounds_v2/cart_round_policy.csv').open())};prefix=[r for r in rows if int(r['frame'])<4970];assert all(r['mask']==old[int(r['frame'])]['mask']for r in prefix)
 for r in rows:
  m=int(r['mask'],16);assert not(m&1 and m&2)and not(m&4 and m&8)
 cache={};queries=list(csv.DictReader((q/'cart_tile_queries.csv').open()))
 for r in queries:
  k=tuple(int(r[x])for x in('x_page','x_low','y_page','y_low','level'))
  if k not in cache:cache[k]=classify(blob,*k)
  assert cache[k]==int(r['class'])
 images=list(q.glob('frame_*.png'));chunks=0
 for p in images:
  pp=(q/(p.stem+'_ppu.bin')).read_bytes()
  for r in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
   if r['kind']!='chr':continue
   a=int(r['cpu_or_ppu_address'],16);k=int(r['relative_offset'],16);assert pp[a:a+1024]==blob[0x40010+k:0x40410+k];chunks+=1
 world=list(csv.DictReader((q/'world_phase.csv').open()));assert world[-1]['root']=='08'and world[-1]['history']==world[-1]['gold']=='00'
 assert any(r['root']=='04'and r['phase']=='11'for r in world)
 before=(q/'frame_18990_ram.bin').read_bytes();after=(q/'frame_24000_ram.bin').read_bytes();assert before[0x79]==1 and after[0x7c0]==3
 report={'work':71,'status':'NATIVE_AXIS_CORRECTED_FIRST_ROUND_REPRODUCED_FINALCLEAR_PENDING','ROM_SSOT_changes':0,'runtime_files':len(e['files']),'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'policy_rows':len(rows),'first_round_prefix_masks_exact':len(prefix),'actual_tile_queries_exact':len(queries),'unique_inputs_exact':len(cache),'levels_runtime_observed':sorted(set(int(r['level'])for r in queries)),'last_world':world[-1],'phase11_timeout_then_home':'Actual19110 phase11(hex) HUD00:00, phase09/0A then19680 root08 phase13; actual24000 is home/map selection, not a persistentGAMEOVER screen. Life3/history0/gold0.','direct_visual':'Actual19110 timer00 and24000 home viewed','axis_evidence':'qa/reports/cart_axis071_cpu.json and work/cart_geometry_001/axis071_native_velocity_proof.json','limits':['One of3 rounds cleared; level1 last enemy remained before failure exit; global exit clears actors, not proof last enemy fell','Level2 remains static only','Current coarsepath +/-8 lineclearance underestimates native15pixel body probes','No ROM/RAM/PC/state/reset/life/currency edits; no wholeplay/PCM/listening/finalhumanreview'],'next_action':'Construct an8pixel navigation graph using all native +/-15/cardinal and +/-10/diagonal body probes, preserving knownlevel0 input, and retry the remaining rounds.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in('status','runtime_files','screens','mapped_CHR_1K_chunks_exact','actual_tile_queries_exact','unique_inputs_exact')},indent=2))
if __name__=='__main__':main()
