"""Private cold boot, two declared condition-field writes at native A5C6."""
from pathlib import Path
import argparse, csv, hashlib, json, os, subprocess

R = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rom',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); rom=a.rom.resolve(); output=a.output.resolve()
    meta=json.loads((R/'manifests/source_rom.json').read_text('utf-8'))
    source=R/meta['path'];assert sha(source)==meta['sha256']
    if rom==source.resolve(): assert sha(rom)==meta['sha256']
    else:
        report=json.loads((rom.parent/'build_report.json').read_text('utf-8'))
        assert sha(rom)==report['output_sha256'] and rom.stat().st_size==report['output_size']
        assert report['source_sha256']==meta['sha256']
    assert output.is_relative_to((R/'qa/dialogue').resolve()) and not output.exists()
    exe=R/'tools/mesen-2.1.1/Mesen.exe';config=R/'config/mesen_survey.json'
    assert sha(exe)=='d2eb03c2590c648bf329f127ebcfefd70130e7690a9e2ccdba8616faea1fe96b'
    assert sha(config)=='cee81286ae23bd0b4fa417a9429b63dcf645ce2bdd122db5aa1d572990803621'
    inputs=R/'config/menu_water_001.json';events=json.loads(inputs.read_text('utf-8'))
    for e in events:
        assert set(e)=={'frame','duration','button'} and 0<=e['frame']<4000
        assert 1<=e['duration']<=4000-e['frame'] and e['button']in{'start','select','a','b','up','down','left','right'}
    output.mkdir(parents=True,exist_ok=False)
    script=output/'capture_survey_used.lua';script.write_bytes((R/'scripts/trace_river121_v1.lua').read_bytes())
    (output/'config_used.json').write_bytes(config.read_bytes())
    (output/'inputs_used.json').write_bytes(inputs.read_bytes())
    (exe.parent/'settings.json').write_bytes(config.read_bytes())
    env=os.environ.copy();env.update(TTA2_QA_OUT=str(output),TTA2_FRAMES='4000',
                                    TTA2_INPUTS=';'.join(f"{e['frame']},{e['duration']},{e['button']}"for e in events))
    command=[str(exe),'--testrunner',str(script),str(rom),'--timeout=120','--enableStdout']
    romsha=sha(rom)
    proc=subprocess.run(command,capture_output=True,env=env,timeout=135,creationflags=subprocess.CREATE_NO_WINDOW)
    (output/'stdout.txt').write_bytes(proc.stdout);(output/'stderr.txt').write_bytes(proc.stderr)
    report={'work':121,'source_sha256':meta['sha256'],'rom_sha256':romsha,
            'exe_path':str(exe),'exe_sha256':sha(exe),'lua_sha256':sha(script),'config_sha256':sha(config),
            'command':command,'exit_code':proc.returncode,'frames':4000,
            'input':{'sequence':events,'file_sha256':sha(inputs)},
            'intervention':'At first physical native A5C6 after frame3000 in root4/course3/phase5/actor2state0, write RAM69=0B and6D=F0 once; no life/time/currency/PC/ROM/state-load change.',
            'scope':'Explicit condition diagnostic, not natural river late-game traversal or fullplay.',
            'files':{p.name:sha(p)for p in sorted(output.iterdir())if p.is_file()}}
    (output/'environment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    assert proc.returncode==0
    assert (output/'trace_complete.txt').read_text()=='4000'
    rows=list(csv.DictReader((output/'river121_injection.csv').open(encoding='utf-8',newline='')))
    assert len(rows)==2 and [(x['address'],x['after'])for x in rows]==[('0069','0B'),('006D','F0')]
    assert sha(rom)==romsha and sha(source)==meta['sha256']
    print('Completed river121',output.name,'exit',proc.returncode,'files',len(report['files']))

if __name__=='__main__':main()
