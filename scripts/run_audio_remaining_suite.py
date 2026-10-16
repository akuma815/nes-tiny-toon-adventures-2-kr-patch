from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
def main():
 src=json.loads((R/'manifests/source_rom.json').read_text('utf-8'))
 items=[('043','cart')]+[(version,ride)for ride in ('train','water')for version in ('japan','043')]
 runs=[]
 for version,ride in items:
  output=R/f'qa/dialogue/audio{version}_{ride}'if version=='043'else R/f'qa/dialogue/audio_japan_{ride}'
  assert not output.exists()
  rom=R/src['path']if version=='japan'else R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes'
  cmd=[sys.executable,str(R/'scripts/run_audio_qa.py'),'--rom',str(rom),'--output',str(output),'--frames','9000','--inputs',str(R/f'config/menu_{ride}_001.json')]
  print('START',version,ride,flush=True);p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8');assert p.returncode==0,p.stdout+p.stderr
  e=json.loads((output/'environment.json').read_text('utf-8'));runs.append({'version':version,'ride':ride,'environment':str((output/'environment.json').relative_to(R)),'exit':e['exit_code']});print('DONE',version,ride,flush=True)
 out=R/'qa/reports/audio059_remaining_runs.json';assert not out.exists();out.write_text(json.dumps({'status':'RUNS_COMPLETED','runs':runs},indent=2)+'\n')
if __name__=='__main__':main()
