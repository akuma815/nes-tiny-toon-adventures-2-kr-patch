from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=R/'work/gatereader148/run_plan.json';assert not plan.exists();plan.parent.mkdir(parents=True,exist_ok=True);jobs=[]
 for route,frames in [('normal49',6000),('gold4',9000)]:
  d=R/f'qa/dialogue/gate094_{route}047';e=json.loads((d/'environment.json').read_text('utf-8'))
  assert sha(d/'inputs_used.json')==e['input']['file_sha256']and sha(d/'seed_used.json')==e['seed_file_sha256']
  for build in ['047','049']:
   args=[sys.executable,str(R/'scripts/run_branch_reader141.py'),'--rom',f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes','--output',f'qa/dialogue/gatereader148_{route}_{build}','--frames',str(frames),'--inputs',str(d/'inputs_used.json'),'--seed',str(d/'seed_used.json'),'--script','scripts/trace_booth_reader141.lua']
   assert not (R/f'qa/dialogue/gatereader148_{route}_{build}').exists();jobs.append({'route':route,'build':build,'command':args,'input_supplier':d.relative_to(R).as_posix(),'input_environment_sha256':sha(d/'environment.json')})
 plan.write_text(json.dumps({'work':148,'jobs':jobs,'scope':'New actual-reader discrimination for castle refusal and admission. Frozen094 seed/input suppliers, fresh047 baselines, current049; no winningbot/ROM/state edits.'},indent=2)+'\n','utf-8')
 for j in jobs:
  print('START gatereader148 '+j['route']+' '+j['build'],flush=True);p=subprocess.run(j['command'],cwd=R,capture_output=True)
  (plan.parent/(j['route']+'_'+j['build']+'_runner_stdout.txt')).write_bytes(p.stdout);(plan.parent/(j['route']+'_'+j['build']+'_runner_stderr.txt')).write_bytes(p.stderr)
  assert p.returncode==0,p.stderr.decode('utf-8','replace');print('PASS gatereader148 '+j['route']+' '+j['build'],flush=True)
if __name__=='__main__':main()
