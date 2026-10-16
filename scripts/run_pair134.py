"""Sequential private-Mesen runs to avoid shared private config collisions."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
out=R/'work/live134';assert not out.exists();out.mkdir()
commands=[]
for seed in [3,4]:
 for build in ['047','049']:
  commands.append([sys.executable,str(R/'scripts/run_live134.py'),'--rom',str(R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/live134_normal{seed}_{build}'),'--frames','4200','--inputs',str(R/'config/menu_coaster_001.json'),'--seed',str(R/('config/ride_normal3_seed_001.json' if seed==3 else 'config/world_coaster_ticket4_seed_001.json')),'--script',str(R/'scripts/trace_live_page134.lua')])
(out/'run_plan.json').write_text(json.dumps(commands,indent=2)+'\n','utf-8')
for i,c in enumerate(commands):
 print('START',i,flush=True);p=subprocess.run(c,cwd=R,capture_output=True);(out/f'run_{i}_stdout.txt').write_bytes(p.stdout);(out/f'run_{i}_stderr.txt').write_bytes(p.stderr);assert p.returncode==0,p.stderr.decode('utf-8','replace');print('DONE',i,flush=True)
