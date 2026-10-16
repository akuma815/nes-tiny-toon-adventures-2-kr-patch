"""Sequential isolated Mesen039/040 regression, never parallel shared settings."""
import subprocess,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def run(runner,build,out,frames,inputs,script,seed=None):
 args=[sys.executable,str(R/'scripts'/runner),'--rom',str(R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/{out}'),'--frames',str(frames),'--inputs',str(R/'config'/inputs),'--script',str(R/'scripts'/script)]
 if seed:args.extend(['--seed',str(R/'config'/seed)])
 assert (R/'scripts'/script).is_file();assert not (R/f'qa/dialogue/{out}').exists();print('START '+out,flush=True);p=subprocess.run(args,capture_output=True,env=os.environ.copy(),cwd=R);assert p.returncode==0,(out,p.stdout.decode('utf-8','replace'),p.stderr.decode('utf-8','replace'));print('PASS '+out,flush=True)
def main():
 for ride,frames in [('coaster',12000),('cart',10000),('train',10000),('water',10000)]:
  run('run_menu_qa.py','040',f'game040_{ride}_survey_v2' if ride=='coaster' else f'game040_{ride}_survey',frames,f'menu_{ride}_001.json','trace_ui_consumers_v4.lua')
  for build in ('039','040'):run('run_menu_qa.py',build,f'game{build}_{ride}_irq',frames,f'menu_{ride}_001.json','trace_ui_irq_v2.lua')
 for build in ('039','040'):
  for mode in ('native','irq'):run('run_branch_seed_qa.py',build,f'game{build}_castle_{mode}',6000,'menu_castle_001.json','trace_branch_seed_irq_v1.lua' if mode=='irq' else 'trace_branch_seed_v1.lua','gate_gold4_seed_001.json')
 run('run_menu_qa.py','040','game040_booth_regression',4500,'menu_ticket_001.json','trace_booth_layout_v1.lua')
 # Intro & credits have own established runners; kept separate from this suite.
if __name__=='__main__':main()
