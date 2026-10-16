from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=R/'work/shortagereader150/run_plan.json';assert not plan.exists()
 d=R/'qa/dialogue/context106_normal3047';e=json.loads((d/'environment.json').read_text('utf-8'))
 assert sha(d/'inputs_used.json')==e['input']['file_sha256']and sha(d/'seed_used.json')==e['seed_file_sha256']
 jobs=[]
 for build in ['047','049']:
  args=[sys.executable,str(R/'scripts/run_branch_reader141.py'),'--rom',f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes','--output',f'qa/dialogue/shortagereader150_{build}','--frames','4200','--inputs',str(d/'inputs_used.json'),'--seed',str(d/'seed_used.json'),'--script','scripts/trace_booth_reader141.lua']
  assert not (R/f'qa/dialogue/shortagereader150_{build}').exists();jobs.append({'build':build,'command':args})
 plan.parent.mkdir(parents=True,exist_ok=True)
 plan.write_text(json.dumps({'work':150,'jobs':jobs,'input_supplier_environment_sha256':sha(d/'environment.json'),'scope':'Initial normal3 diagnostic seed; actual changed source read/private226 and clear lifetime; no source or CSV changes'},indent=2)+'\n','utf-8')
 for j in jobs:
  print('START shortage150 '+j['build'],flush=True);p=subprocess.run(j['command'],cwd=R,capture_output=True)
  (plan.parent/(j['build']+'_stdout.txt')).write_bytes(p.stdout);(plan.parent/(j['build']+'_stderr.txt')).write_bytes(p.stderr)
  assert p.returncode==0,p.stderr.decode('utf-8','replace');print('PASS shortage150 '+j['build'],flush=True)
if __name__=='__main__':main()
