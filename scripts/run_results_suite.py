"""Sequential cold boot bonus dense V2, four native ordinary rides and repeat branch."""
import sys,subprocess,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(build,name,script,inputs,seed,frames=7500):
 command=[sys.executable,str(R/'scripts/run_results_seed_qa_v2.py'),'--rom',str(R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/{name}'),'--frames',str(frames),'--inputs',str(R/f'config/{inputs}'),'--script',str(R/f'scripts/{script}'),'--seed',str(R/f'config/{seed}')]
 print('START '+name,flush=True);p=subprocess.run(command,cwd=R,capture_output=True,env=os.environ.copy());assert p.returncode==0,(name,p.stdout.decode('utf-8','replace'),p.stderr.decode('utf-8','replace'));print('PASS '+name,flush=True)
def main():
 for ride in ('coaster','cart','train','water'):
  inputs='menu_results_001.json' if ride=='coaster' else f'menu_results_{ride}_001.json'
  for build in ('040','041'):run(build,f'results{build}_{ride}_dense','trace_results_seed_v2.lua',inputs,'results_native_phase_seed_001.json')
 for build in ('040','041'):
  run(build,f'results{build}_coaster_irq_v2','trace_results_seed_irq_v2.lua','menu_results_001.json','results_native_phase_seed_001.json')
  run(build,f'results{build}_repeat_dense','trace_results_seed_v2.lua','menu_results_001.json','results_repeat_phase_seed_001.json')
  run(build,f'results{build}_repeat_irq_v2','trace_results_seed_irq_v2.lua','menu_results_001.json','results_repeat_phase_seed_001.json')
if __name__=='__main__':main()
