from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def main():
 plan=R/'work/train142/run_plan.json';assert not plan.exists();jobs=[]
 for build in ['047','049']:
  args=[sys.executable,str(R/'scripts/run_menu_qa.py'),'--rom',f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes','--output',f'qa/dialogue/train142_native_{build}','--frames','4500','--inputs','config/menu_train_001.json','--script','scripts/trace_train_reader142.lua']
  assert not (R/f'qa/dialogue/train142_native_{build}').exists();jobs.append({'build':build,'command':args})
 plan.write_text(json.dumps({'work':142,'jobs':jobs,'scope':'Controller-only train selection/fee/start; no RAM seed, state load or ROM writes'},indent=2)+'\n','utf-8')
 for j in jobs:
  print('START train142 '+j['build'],flush=True);p=subprocess.run(j['command'],cwd=R,capture_output=True)
  (plan.parent/(j['build']+'_runner_stdout.txt')).write_bytes(p.stdout);(plan.parent/(j['build']+'_runner_stderr.txt')).write_bytes(p.stderr)
  assert p.returncode==0,p.stderr.decode('utf-8','replace');print('PASS train142 '+j['build'],flush=True)
if __name__=='__main__':main()
