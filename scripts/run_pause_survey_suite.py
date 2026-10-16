"""Four ordinary rides, recorded pause/resume, sequential private Mesen."""
import subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for ride in ('coaster','cart','train','water'):
 cmd=[sys.executable,str(R/'scripts/run_pause_qa.py'),'--rom',str(R/'build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/pause042_{ride}'),'--frames','4500','--inputs',str(R/f'config/world_{ride}_pause_001.json'),'--script',str(R/'scripts/trace_pause_v1.lua')]
 done=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
 print(json.dumps({'ride':ride,'exit_code':done.returncode}),flush=True)
 if done.returncode:print(done.stdout,done.stderr);raise SystemExit(done.returncode)
