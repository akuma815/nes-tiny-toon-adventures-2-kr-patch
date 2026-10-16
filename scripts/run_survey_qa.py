"""Cold boot the registered source in isolated Mesen; preserve identity and evidence."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--frames', type=int, default=5400)
    ap.add_argument('--start', type=int, default=-1)
    ap.add_argument('--script', type=Path, default=ROOT/'scripts/capture_survey.lua')
    a=ap.parse_args()
    manifest=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    rom=ROOT/manifest['path']
    assert sha(rom)==manifest['sha256'] and rom.stat().st_size==manifest['size_bytes']
    assert 0<a.frames<=18000
    output=a.output.resolve()
    assert output!=ROOT/'original' and ROOT/'original' not in output.parents
    output.mkdir(parents=True,exist_ok=False)
    exe=ROOT/'tools/mesen-2.1.1/Mesen.exe'
    config=ROOT/'config/mesen_survey.json'
    script=output/'capture_survey_used.lua'
    script.write_bytes(a.script.read_bytes())
    (output/'config_used.json').write_bytes(config.read_bytes())
    (exe.parent/'settings.json').write_bytes(config.read_bytes())
    env=os.environ.copy()
    env.update(TTA2_QA_OUT=str(output),TTA2_FRAMES=str(a.frames),TTA2_START=str(a.start))
    command=[str(exe),'--testrunner',str(script),str(rom),'--timeout=120','--enableStdout']
    result=subprocess.run(command,capture_output=True,env=env,creationflags=subprocess.CREATE_NO_WINDOW,timeout=135)
    (output/'stdout.txt').write_bytes(result.stdout)
    (output/'stderr.txt').write_bytes(result.stderr)
    report={'source_sha256':sha(rom),'emulator':'Mesen 2.1.1','exe_path':str(exe),'exe_sha256':sha(exe),
        'lua_sha256':sha(script),'config_sha256':sha(config),'command':command,'exit_code':result.returncode,
        'frames':a.frames,'input':{'start_frame':a.start,'start_duration':8,'all_other_buttons':False},
        'intervention':'controller input only; no state loading or RAM/ROM writes',
        'files':{p.name:sha(p) for p in sorted(output.iterdir()) if p.is_file()},
        'scope':'Original baseline capture only. Direct visual review separate. No Korean build or full playthrough.'}
    (output/'environment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert result.returncode==0, f'Mesen exited {result.returncode}; inspect logs'
    if a.script.name=='capture_survey.lua':
        assert (output/f'frame_{a.frames:05d}.png').exists(), 'Missing final frame'
    else:
        assert (output/'trace_complete.txt').read_text()==str(a.frames), 'Trace incomplete'
    assert sha(rom)==manifest['sha256']
    print(json.dumps({k:v for k,v in report.items() if k not in ('files','command')},indent=2))
if __name__=='__main__': main()
