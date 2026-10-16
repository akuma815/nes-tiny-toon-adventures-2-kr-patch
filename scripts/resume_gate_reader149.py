"""Resume only uncompleted work148 runs; preserve the stopped capture."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=R/'work/gatereader149/resume_plan_20261007.json'
 assert not plan.exists()
 jobs=[]
 for route,build,frames,out in [
  ('normal49','049',6000,'gatereader148_normal49_049_resume'),
  ('gold4','047',9000,'gatereader148_gold4_047'),
  ('gold4','049',9000,'gatereader148_gold4_049')]:
  d=R/f'qa/dialogue/gate094_{route}047';e=json.loads((d/'environment.json').read_text('utf-8'))
  assert sha(d/'inputs_used.json')==e['input']['file_sha256'] and sha(d/'seed_used.json')==e['seed_file_sha256']
  assert not (R/'qa/dialogue'/out).exists()
  args=[sys.executable,str(R/'scripts/run_branch_reader141.py'),'--rom',f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes','--output',f'qa/dialogue/{out}','--frames',str(frames),'--inputs',str(d/'inputs_used.json'),'--seed',str(d/'seed_used.json'),'--script','scripts/trace_booth_reader141.lua']
  jobs.append({'route':route,'build':build,'frames':frames,'output':out,'command':args,'input_environment_sha256':sha(d/'environment.json')})
 plan.parent.mkdir(parents=True,exist_ok=True)
 plan.write_text(json.dumps({'work':149,'resumes_work':148,'date':'2026-10-07','reused_completed_baseline':'qa/dialogue/gatereader148_normal49_047','preserved_interrupted':'qa/dialogue/gatereader148_normal49_049','jobs':jobs},indent=2)+'\n','utf-8')
 for j in jobs:
  print('START '+j['output'],flush=True)
  p=subprocess.run(j['command'],cwd=R,capture_output=True)
  (plan.parent/(j['output']+'_stdout.txt')).write_bytes(p.stdout)
  (plan.parent/(j['output']+'_stderr.txt')).write_bytes(p.stderr)
  assert p.returncode==0,p.stderr.decode('utf-8','replace')
  print('PASS '+j['output'],flush=True)
if __name__=='__main__':main()
