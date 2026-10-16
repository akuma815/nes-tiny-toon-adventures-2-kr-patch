"""Source042/new043 identicaldiagnostic life/control/fullIRQ+actualengine samples."""
import subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for version in ('042','043'):
 cmd=[sys.executable,str(R/'scripts/run_world_life_seed_qa_v3.py'),'--rom',str(R/f'build/dialogue_kr_poc_{version}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/train{version}_life3_irq_v3'),'--frames','18000','--inputs',str(R/'config/world_train_controller_003.json'),'--script',str(R/'scripts/trace_world_life_seed_v2.lua'),'--seed',str(R/'config/train_life3_diagnostic_001.json')]
 x=subprocess.run(cmd,cwd=R,capture_output=True,text=True);print(json.dumps({'version':version,'exit_code':x.returncode}),flush=True)
 if x.returncode:print(x.stdout,x.stderr);raise SystemExit(x.returncode)
