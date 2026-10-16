"""Four current43 cold controller-only long routes, sequential privateMesen; no gameclear inference."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
def main():
 outputs=[]
 for ride in ['coaster','cart','train','water']:
  dest=R/f'qa/dialogue/world043_{ride}_controller';assert not dest.exists()
  args=[sys.executable,str(R/'scripts/run_world_qa.py'),'--rom',str(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes'),'--output',str(dest),'--frames','18000','--inputs',str(R/f'config/world_{ride}_controller_001.json')]
  print('RUN',ride,flush=True);subprocess.run(args,check=True,cwd=R);outputs.append(dest.relative_to(R).as_posix())
 out=R/'qa/reports/long_world057_runs.json';assert not out.exists();out.write_text(json.dumps({'status':'RUNS_COMPLETED','outputs':outputs,'frames_each':18000,'manual_RAM_ROM_writes':False,'save_loads':False,'scope':'Long coldcontroller paths; route completion/failure needs phase/log review, not automaticclear claim'},indent=2)+'\n','utf-8');print('Four long world traces completed')
if __name__=='__main__':main()
