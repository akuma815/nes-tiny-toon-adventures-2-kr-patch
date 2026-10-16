"""Sequential cold-boot native failure/gameover YES/NO old041/new042."""
from run_game_hud_suite import run
if __name__=='__main__':
 for choice in ('yes','no'):
  for b in ('041','042'):
   for mode in ('dense','irq'):
    run('run_gameover_seed_qa_v2.py',b,f'gameover{b}_{choice}_{mode}',8000,f'world_gameover_{choice}_001.json','trace_gameover_seed_v2.lua' if mode=='dense' else 'trace_gameover_seed_irq_v2.lua','world_coaster_ticket4_seed_001.json')
