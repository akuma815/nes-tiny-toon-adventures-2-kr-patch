from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1];out=R/'work/dma135';assert not out.exists();out.mkdir()
commands=[]
for build in ['047','049']:
 commands.append([sys.executable,str(R/'scripts/run_dma135.py'),'--rom',str(R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes'),'--output',str(R/f'qa/dialogue/dma135_home{build}'),'--frames','960','--inputs',str(R/'config/first_home135.json'),'--script',str(R/'scripts/trace_dma135.lua')])
(out/'run_plan.json').write_text(json.dumps(commands,indent=2)+'\n','utf-8')
for i,c in enumerate(commands):
 print('START',i,flush=True);p=subprocess.run(c,cwd=R,capture_output=True);(out/f'run_{i}_stdout.txt').write_bytes(p.stdout);(out/f'run_{i}_stderr.txt').write_bytes(p.stderr);assert p.returncode==0,p.stderr.decode('utf-8','replace');print('DONE',i,flush=True)
