"""Work94 sequential isolated current/prior castle currency branch matrix."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
def main():
 for route,frames,inputs,seed in [('gold4',9000,'menu_castle_continue_001','gate_gold4_seed_001'),('normal50',9000,'menu_castle_continue_001','gate_normal50_seed_001'),('normal49',6000,'menu_castle_001','gate_normal49_seed_001')]:
  for build in ('046','047'):
   output=f'qa/dialogue/gate094_{route}{build}';assert not (R/output).exists()
   command=[sys.executable,str(R/'scripts/run_branch_seed_qa.py'),'--rom',f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes','--output',output,'--frames',str(frames),'--inputs',f'config/{inputs}.json','--script','scripts/trace_branch_seed_v1.lua','--seed',f'config/{seed}.json']
   run=subprocess.run(command,cwd=R,capture_output=True);p=R/'qa/logs'/f'gate094_{route}{build}_runner.txt';assert not p.exists();p.write_bytes(run.stdout+run.stderr);assert run.returncode==0,(route,build,run.returncode)
   print(json.dumps({'route':route,'build':build,'frames':frames,'exit_code':run.returncode}),flush=True)
if __name__=='__main__':main()