"""Sequential private Mesen044/045 shared START regression, threeother courses."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
def main():
 log=R/'work/start_regression_078';log.mkdir(exist_ok=False);runs=[]
 for course in ('coaster','train','water'):
  for build in ('044','045'):
   name=f'start078_{course}{build}';cmd=[sys.executable,str(R/'scripts/run_world_qa.py'),'--rom',str(R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/{name}'),'--frames','4200','--inputs',str(R/f'config/menu_{course}_001.json')]
   p=subprocess.run(cmd,cwd=R,capture_output=True,timeout=150);(log/(name+'_runner_stdout.txt')).write_bytes(p.stdout);(log/(name+'_runner_stderr.txt')).write_bytes(p.stderr);assert p.returncode==0,(name,p.stderr);runs.append({'name':name,'command':cmd,'exit_code':p.returncode});print(name+' complete',flush=True)
 (log/'suite_runs.json').write_text(json.dumps({'work':78,'runs':runs,'scope':'Sequential controller-only coldboots; no seed/ROM/state/life/currency edits'},indent=2)+'\n','utf-8')
if __name__=='__main__':main()
