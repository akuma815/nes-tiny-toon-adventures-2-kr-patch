"""Cold boot a verified dialogue development build in isolated Mesen; explicit controlled-RAM-seed branch evidence; not normal gameplay."""
import argparse, hashlib, json, os, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--frames', type=int, default=5400)
    ap.add_argument('--start', type=int, default=-1)
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--script', type=Path, default=ROOT/'scripts/trace_credits_seed_v1.lua')
    ap.add_argument('--seed',type=Path,required=True)
    a=ap.parse_args()
    manifest=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    rom=a.rom.resolve()
    expected=json.loads((rom.parent/'build_report.json').read_text(encoding='utf-8'))
    assert sha(rom)==expected['output_sha256'] and rom.stat().st_size==expected['output_size']
    assert expected['source_sha256']==manifest['sha256']
    assert sha(ROOT/manifest['path'])==manifest['sha256']
    rom_sha=sha(rom)
    events=json.loads(a.inputs.read_text('utf-8'))
    allowed={'start','select','a','b','up','down','left','right'}
    for e in events:assert set(e)=={'frame','duration','button'} and e['button'] in allowed and 0<=e['frame']<a.frames and 1<=e['duration']<=60
    assert len(events)<=128
    seed=json.loads(a.seed.read_text('utf-8'));assert set(seed)=={'purpose','frame','writes'} and 0<seed['frame']<a.frames and 1<=len(seed['writes'])<=9
    assert len(seed['writes'])==2 and {(w['address'],w['value']) for w in seed['writes']}=={(0x7df,1),(0x6de,0)}
    for w in seed['writes']:assert set(w)=={'address','value'} and (w['address'],w['value']) in ((0x7df,1),(0x6de,0))
    assert a.script.name in ('trace_credits_seed_v1.lua','trace_credits_seed_irq_v1.lua')
    schedule=';'.join(f"{e['frame']},{e['duration']},{e['button']}" for e in events)
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
    env.update(TTA2_QA_OUT=str(output),TTA2_FRAMES=str(a.frames),TTA2_START=str(a.start),TTA2_INPUTS=schedule)
    (output/'inputs_used.json').write_bytes(a.inputs.read_bytes())
    (output/'seed_used.json').write_bytes(a.seed.read_bytes())
    env.update(TTA2_SEED_FRAME=str(seed['frame']),TTA2_SEEDS=';'.join(f"{w['address']},{w['value']}" for w in seed['writes']))
    command=[str(exe),'--testrunner',str(script),str(rom),'--timeout=120','--enableStdout']
    result=subprocess.run(command,capture_output=True,env=env,creationflags=subprocess.CREATE_NO_WINDOW,timeout=135)
    (output/'stdout.txt').write_bytes(result.stdout)
    (output/'stderr.txt').write_bytes(result.stderr)
    report={'source_sha256':manifest['sha256'],'rom_sha256':rom_sha,'emulator':'Mesen 2.1.1','exe_path':str(exe),'exe_sha256':sha(exe),
        'lua_sha256':sha(script),'config_sha256':sha(config),'command':command,'exit_code':result.returncode,
        'frames':a.frames,'input':{'sequence':events,'file_sha256':sha(a.inputs),'unspecified_buttons':False},
        'intervention':'Explicit initial RAM seed at recorded frame; controller inputs thereafter; no state load or ROM writes; not normal gameplay',
        'seed':seed,'seed_file_sha256':sha(a.seed),
        'files':{p.name:sha(p) for p in sorted(output.iterdir()) if p.is_file()},
        'scope':'Controlled ending scene QA. Native ending selector07DF=1 and phase06DE=0 intentionally seeded; direct visual review separate; no game-clear/fullplay proof.'}
    (output/'environment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert result.returncode==0, f'Mesen exited {result.returncode}; inspect logs'
    if a.script.name=='capture_survey.lua':
        assert (output/f'frame_{a.frames:05d}.png').exists(), 'Missing final frame'
    else:
        assert (output/'trace_complete.txt').read_text()==str(a.frames), 'Trace incomplete'
    import csv
    recorded=list(csv.DictReader((output/'seed_writes.csv').open(encoding='utf-8',newline='')))
    assert len(recorded)==len(seed['writes'])
    for row,w in zip(recorded,seed['writes']):assert int(row['frame'])==seed['frame'] and int(row['address'],16)==w['address'] and int(row['value'],16)==int(row['after'],16)==w['value']
    assert sha(rom)==rom_sha
    assert sha(ROOT/manifest['path'])==manifest['sha256']
    print(json.dumps({k:v for k,v in report.items() if k not in ('files','command')},indent=2))
if __name__=='__main__': main()
