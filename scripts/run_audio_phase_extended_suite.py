from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1]
def main():
 src=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));runs=[]
 for version in ('japan','043'):
  rom=R/src['path']if version=='japan'else R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';out=R/('qa/dialogue/audio_sync061_japan_water'if version=='japan'else'qa/dialogue/audio_sync061_043_water');assert not out.exists()
  print('START',version,flush=True);cmd=[sys.executable,str(R/'scripts/run_audio_phase_extended_qa.py'),'--rom',str(rom),'--output',str(out),'--frames','9030','--inputs',str(R/'config/menu_water_001.json')];p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8');assert p.returncode==0,p.stdout+p.stderr;runs.append({'version':version,'environment':str((out/'environment.json').relative_to(R))});print('DONE',version,flush=True)
 out=R/'qa/reports/audio_sync061_runs.json';assert not out.exists();out.write_text(json.dumps({'status':'RUNS_COMPLETED','runs':runs},indent=2)+'\n')
if __name__=='__main__':main()
