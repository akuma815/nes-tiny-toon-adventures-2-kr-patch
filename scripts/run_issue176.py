"""Focused private MesenCE state reproduction; does not attach to user's process."""
from pathlib import Path
import argparse,json,os,shutil,subprocess
from seal_nonplay171 import R,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rom',type=Path,required=True);ap.add_argument('--state',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    rom=a.rom.resolve();state=a.state.resolve();out=a.output.resolve();out.relative_to(R/'qa');assert not out.exists()
    exe=R/'tools/mesence_user176/Mesen.exe';prior=json.loads((R/'qa/issue176_user_booth/provenance.json').read_text('utf-8'))
    assert sha(exe)==prior['host_copies'][0]['sha256'];assert any(sha(state)==s['sha256'] for s in prior['states'])
    rh=sha(rom);sh=sha(state);out.mkdir();lua=out/'observer_used.lua';lua.write_bytes((R/'scripts/trace_issue176.lua').read_bytes())
    env=os.environ.copy();env.update(TT_ISSUE_OUT=str(out),TT_ISSUE_STATE=str(state))
    command=[str(exe),'--testrunner','--donotsavesettings',str(lua),str(rom),'--timeout=30','--enableStdout']
    p=subprocess.run(command,env=env,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=40)
    (out/'stdout.txt').write_bytes(p.stdout);(out/'stderr.txt').write_bytes(p.stderr)
    report={'ROM_path':str(rom),'ROM_sha256':rh,'state_path':str(state),'state_sha256':sh,'exe_sha256':sha(exe),
        'lua_sha256':sha(lua),'command':command,'exit_code':p.returncode,
        'scope':'Targeted12-frame copied-user-state replay in private same2.2.1 host. Not current live memory or natural caller reproduction; only load intervention.',
        'files':{q.name:sha(q) for q in sorted(out.iterdir()) if q.is_file()}}
    (out/'environment.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    assert p.returncode==0 and (out/'trace_complete.txt').read_text()=='12',p.stdout[-2000:]
    assert sha(rom)==rh and sha(state)==sh
    print(json.dumps({k:v for k,v in report.items() if k not in ['files','command']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
