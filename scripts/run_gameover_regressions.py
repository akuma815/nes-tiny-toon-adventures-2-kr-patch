import sys,subprocess,os
from pathlib import Path
from run_game_hud_suite import run
R=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 print('START gameover042_intro_regression',flush=True);p=subprocess.run([sys.executable,str(R/'scripts/run_dialogue_qa.py'),'--rom',str(R/'build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/'qa/dialogue/gameover042_intro_regression'),'--frames','6000','--script',str(R/'scripts/capture_intro_complete.lua')],capture_output=True,cwd=R,env=os.environ.copy());assert p.returncode==0,(p.stdout.decode('utf-8','replace'),p.stderr.decode('utf-8','replace'));print('PASS gameover042_intro_regression',flush=True)
 run('run_credits_seed_qa_v3.py','042','gameover042_credits_regression',9000,'menu_credits_001.json','trace_credits_seed_v3.lua','credits_selector_seed_002.json')
 run('run_menu_qa.py','042','gameover042_booth_regression',4500,'menu_ticket_001.json','trace_booth_layout_v1.lua')
 run('run_branch_seed_qa.py','042','gameover042_castle_regression',6000,'menu_castle_001.json','trace_branch_seed_v1.lua','gate_gold4_seed_001.json')
 run('run_results_seed_qa_v2.py','042','gameover042_bonus_regression',7500,'menu_results_001.json','trace_results_seed_v2.lua','results_native_phase_seed_001.json')
