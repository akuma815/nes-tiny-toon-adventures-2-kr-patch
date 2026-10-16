"""Sequential non-HUD and gameplay pause/resume regression for040."""
import sys,subprocess,os,json
from pathlib import Path
from run_game_hud_suite import run
R=Path(__file__).resolve().parents[1]
def main():
 args=[sys.executable,str(R/'scripts/run_dialogue_qa.py'),'--rom',str(R/'build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/'qa/dialogue/game040_intro_regression'),'--frames','6000','--script',str(R/'scripts/capture_intro_complete.lua')]
 print('START game040_intro_regression',flush=True);p=subprocess.run(args,capture_output=True,env=os.environ.copy(),cwd=R);assert p.returncode==0,(p.stdout.decode('utf-8','replace'),p.stderr.decode('utf-8','replace'));print('PASS game040_intro_regression',flush=True)
 run('run_credits_seed_qa_v3.py','040','game040_credits_regression',9000,'menu_credits_001.json','trace_credits_seed_v3.lua','credits_selector_seed_002.json')
 for b in ('039','040'):
  run('run_menu_qa.py',b,f'game{b}_coaster_pause',6000,'menu_coaster_pause_001.json','trace_ui_consumers_v4.lua')
  run('run_menu_qa.py',b,f'game{b}_coaster_pause_irq',6000,'menu_coaster_pause_001.json','trace_ui_irq_v2.lua')
if __name__=='__main__':main()
