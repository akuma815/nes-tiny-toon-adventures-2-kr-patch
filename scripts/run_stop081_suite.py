"""046 other-course header/CHR expansion regression, preserved045 baselines."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
def main():
 log=R/'work/stop_regression_081';log.mkdir(exist_ok=False);runs=[]
 for course in ('coaster','cart','water'):
  runner='run_cart_rounds_qa_v4.py'if course=='cart'else'run_world_qa.py';name=f'stop081_{course}046';cmd=[sys.executable,str(R/'scripts'/runner),'--rom',str(R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/{name}'),'--frames','4200','--inputs',str(R/f'config/menu_{course}_001.json')]
  p=subprocess.run(cmd,cwd=R,capture_output=True,timeout=150);(log/(name+'_runner_stdout.txt')).write_bytes(p.stdout);(log/(name+'_runner_stderr.txt')).write_bytes(p.stderr);assert p.returncode==0,(name,p.stderr);runs.append({'name':name,'command':cmd,'exit_code':p.returncode});print(name+' complete',flush=True)
 (log/'suite_runs.json').write_text(json.dumps({'work':81,'runs':runs,'scope':'Three natural controller-only coldboots; source045 frozen runs reused. No seeds, no machine edits.'},indent=2)+'\n','utf-8')
if __name__=='__main__':main()
