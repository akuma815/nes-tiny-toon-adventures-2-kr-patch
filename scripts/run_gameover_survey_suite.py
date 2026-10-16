import sys
from run_game_hud_suite import run
if __name__=='__main__':
 for choice in ('yes','no'):
  run('run_gameover_seed_qa.py','041',f'gameover041_{choice}_consumer',8000,f'world_gameover_{choice}_001.json','trace_gameover_seed_v1.lua','world_coaster_ticket4_seed_001.json')
