from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=R/'work/booth141/run_plan.json';assert not plan.exists()
 d=R/'qa/dialogue/booth039_points3_irq';e=json.loads((d/'environment.json').read_text('utf-8'))
 assert sha(d/'inputs_used.json')==e['input']['file_sha256'] and sha(d/'seed_used.json')==e['seed_file_sha256']
 jobs=[]
 for build in ['047','049']:
  args=[sys.executable,str(R/'scripts/run_branch_reader141.py'),'--rom',f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes','--output',f'qa/dialogue/booth141_points3_{build}','--frames','4500','--inputs',str(d/'inputs_used.json'),'--seed',str(d/'seed_used.json'),'--script',str(R/'scripts/trace_booth_reader141.lua')]
  jobs.append({'build':build,'command':args});assert not (R/f'qa/dialogue/booth141_points3_{build}').exists()
 plan.write_text(json.dumps({'work':141,'jobs':jobs,'historical_route_environment_sha256':sha(d/'environment.json'),'scope':'Point digit3 seed at1000 then controller only; no state/ROM edits; fresh047 and current049 paired'},indent=2)+'\n','utf-8')
 for j in jobs:
  print('START booth141 '+j['build'],flush=True);p=subprocess.run(j['command'],cwd=R,capture_output=True)
  (plan.parent/(j['build']+'_runner_stdout.txt')).write_bytes(p.stdout);(plan.parent/(j['build']+'_runner_stderr.txt')).write_bytes(p.stderr)
  assert p.returncode==0,p.stderr.decode('utf-8','replace');print('PASS booth141 '+j['build'],flush=True)
if __name__=='__main__':main()
