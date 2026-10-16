import sys,subprocess,os
from pathlib import Path
from run_game_hud_suite import run
R=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 print('START train043_intro_regression',flush=True);p=subprocess.run([sys.executable,str(R/'scripts/run_dialogue_qa.py'),'--rom',str(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/'qa/dialogue/train043_intro_regression'),'--frames','6000','--script',str(R/'scripts/capture_intro_complete.lua')],capture_output=True,cwd=R,env=os.environ.copy());assert p.returncode==0,(p.stdout.decode('utf-8','replace'),p.stderr.decode('utf-8','replace'));print('PASS train043_intro_regression',flush=True)
 run('run_credits_seed_qa_v3.py','043','train043_credits_regression',9000,'menu_credits_001.json','trace_credits_seed_v3.lua','credits_selector_seed_002.json')
 run('run_menu_qa.py','043','train043_booth_regression',4500,'menu_ticket_001.json','trace_booth_layout_v1.lua')
 run('run_branch_seed_qa.py','043','train043_castle_regression',6000,'menu_castle_001.json','trace_branch_seed_v1.lua','gate_gold4_seed_001.json')
 run('run_results_seed_qa_v2.py','043','train043_bonus_regression',7500,'menu_results_001.json','trace_results_seed_v2.lua','results_native_phase_seed_001.json')

 for choice in ('yes','no'):
  run('run_gameover_seed_qa_v2.py','043',f'train043_gameover_{choice}',8000,f'world_gameover_{choice}_001.json','trace_gameover_seed_v2.lua','world_coaster_ticket4_seed_001.json')
 for ride in ('coaster','cart','train','water'):
  run('run_pause_qa.py','043',f'train043_pause_{ride}',4500,f'world_{ride}_pause_001.json','trace_pause_v1.lua')
