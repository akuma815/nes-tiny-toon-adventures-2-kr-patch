"""Vendored first-game Windows apply/ZIP verifier; copied without modifying first-game files."""
"""Build the standard ROM-free xdelta release and verify its Windows entry point."""
import argparse,csv,hashlib,json,os,shutil,subprocess,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NAME='TinyToonAdventures_KR_Patch_v1.0_20261004'
PATCH='TinyToonAdventures_KR_v1.0_20261004.xdelta'
SOURCE_SHA='73300dc1505564827ef95ba3e2a06c26aa48920e4981195f32b2101c185ef3dd'
TARGET_SHA='6d834cdde925dd808ef6d911ebf2f13f5a88e440c9da4bfc50b424035309483d'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,value):p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def windows_text(p,text,bom=True):p.write_bytes((b'\xef\xbb\xbf' if bom else b'')+text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))

def apply(folder,source,qa,destination=None):
    args=[str(folder/'apply.cmd')]+([] if source is None else [str(source)])+([] if destination is None else [str(destination)])
    assert not any('"' in s for s in args)
    command='"'+' '.join('"'+s+'"' for s in args)+'"'
    line='"'+os.environ.get('COMSPEC','cmd.exe')+'" /d /s /c '+command
    env=os.environ.copy();env['TT_PATCH_NO_PAUSE']='1'
    p=subprocess.run(line,cwd=qa,env=env,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=60)
    return {'command':line,'exit_code':p.returncode,'stdout':p.stdout.decode('utf-8',errors='replace'),'stderr':p.stderr.decode('utf-8',errors='replace')}

def check_apply(pkg,qa,source,target):
    qa.mkdir(parents=True,exist_ok=False)
    copy=qa/'패치 묶음';shutil.copytree(pkg,copy)
    original=qa/'원본 게임.nes';shutil.copyfile(source,original)
    output=qa/'원본 게임_KR.nes';checks={}
    checks['valid_apply']=apply(copy,original,qa);assert checks['valid_apply']['exit_code']==0,checks['valid_apply']
    assert output.read_bytes()==target.read_bytes()
    checks['existing_output']=apply(copy,original,qa);assert checks['existing_output']['exit_code']==1 and sha(output)==TARGET_SHA
    checks['same_source_and_output']=apply(copy,original,qa,original);assert checks['same_source_and_output']['exit_code']==1 and sha(original)==SOURCE_SHA
    wrong=qa/'別 판본.nes';bad=bytearray(source.read_bytes());bad[200]^=1;wrong.write_bytes(bad)
    checks['wrong_source_same_size']=apply(copy,wrong,qa);assert checks['wrong_source_same_size']['exit_code']==1 and not (qa/'別 판본_KR.nes').exists()
    checks['already_patched_source']=apply(copy,output,qa);assert checks['already_patched_source']['exit_code']==1 and not (qa/'원본 게임_KR_KR.nes').exists()
    corrupt=qa/'손상 패치';shutil.copytree(pkg,corrupt)
    patch=corrupt/PATCH;bad=bytearray(patch.read_bytes());bad[20]^=1;patch.write_bytes(bad)
    blocked=qa/'손상 패치 결과.nes';checks['corrupt_patch']=apply(corrupt,original,qa,blocked)
    assert checks['corrupt_patch']['exit_code']==1 and not blocked.exists()
    corrupt_tool=qa/'손상 도구';shutil.copytree(pkg,corrupt_tool)
    exe=corrupt_tool/'tools/xdelta3.exe';bad=bytearray(exe.read_bytes());bad[200]^=1;exe.write_bytes(bad)
    blocked=qa/'손상 도구 결과.nes';checks['corrupt_tool']=apply(corrupt_tool,original,qa,blocked)
    assert checks['corrupt_tool']['exit_code']==1 and not blocked.exists()
    checks['no_argument']=apply(copy,None,qa);assert checks['no_argument']['exit_code']==1
    assert not list(qa.glob('tinytoon_patch_*.tmp'))
    assert sha(original)==sha(source)==SOURCE_SHA
    report={'status':'PASS','checks':checks,'source_unchanged':True,'source_sha256':SOURCE_SHA,'output_sha256':sha(output),'byte_for_byte_target_match':True,'output_bytes':output.stat().st_size,'output':str(output.relative_to(ROOT)),'entrypoint_payload_sha256':{n:sha(pkg/n) for n in ['apply.cmd','apply.ps1',PATCH,'tools/xdelta3.exe']}}
    write_json(qa/'apply_verification.json',report)
    return report

def seal_package(out,qa,proof,source,target):
    archive=out.with_name(out.name+'.zip');hashfile=archive.with_suffix('.zip.sha256')
    assert not any(p.exists() for p in (archive,hashfile,proof))
    release=json.loads((out/'release_report.json').read_text(encoding='utf-8'))
    apply_report=json.loads((qa/'apply_verification.json').read_text(encoding='utf-8'))
    assert release['status']==apply_report['status']=='PASS' and release['source']['sha256']==SOURCE_SHA and release['target']['sha256']==TARGET_SHA
    assert len(apply_report['checks'])==8 and all(entry['exit_code']==(0 if name=='valid_apply' else 1) for name,entry in apply_report['checks'].items())
    for p,h in apply_report['entrypoint_payload_sha256'].items():assert sha(out/p)==h
    assert sha(source)==SOURCE_SHA and sha(target)==TARGET_SHA and release['patch']['sha256']==sha(out/PATCH)
    files=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='SHA256.txt')
    checksum=''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\r\n' for p in files).encode('utf-8')
    if (out/'SHA256.txt').exists() and (out/'SHA256.txt').stat().st_size:
        assert (out/'SHA256.txt').read_bytes()==checksum
    else:(out/'SHA256.txt').write_bytes(checksum)
    files=sorted(p for p in out.rglob('*') if p.is_file())
    expected={PATCH,'apply.cmd','apply.ps1','README_적용방법.txt','RELEASE_NOTES_KO.md','SHA256.txt','release_report.json','tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt','licenses/Galmuri_OFL.md'}
    assert {p.relative_to(out).as_posix() for p in files}==expected
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            item=zipfile.ZipInfo((Path(out.name)/p.relative_to(out)).as_posix(),(2026,10,6,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;z.writestr(item,p.read_bytes())
    extracted=qa/'최종 ZIP 추출 final';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())=={(Path(out.name)/p.relative_to(out)).as_posix() for p in files}
        for p in files:assert z.read((Path(out.name)/p.relative_to(out)).as_posix())==p.read_bytes()
        z.extractall(extracted)
    final_source=extracted/'검증 원본.nes';shutil.copyfile(source,final_source)
    final_apply=apply(extracted/out.name,final_source,extracted)
    assert final_apply['exit_code']==0,final_apply
    final_output=extracted/'검증 원본_KR.nes';assert final_output.read_bytes()==target.read_bytes() and sha(final_source)==SOURCE_SHA
    for p in files:assert (extracted/out.name/p.relative_to(out)).read_bytes()==p.read_bytes()
    hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n',encoding='ascii')
    assert sha(source)==SOURCE_SHA
    result={'status':'PASS','package':out.relative_to(ROOT).as_posix(),'archive':archive.relative_to(ROOT).as_posix(),'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive),'source_sha256':SOURCE_SHA,'output_sha256':TARGET_SHA,'patch_sha256':sha(out/PATCH),'ROM_free':True,'ZIP_contents_exact':True,'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files},'actual_Windows_apply_checks':8,'apply_report':(qa/'apply_verification.json').relative_to(ROOT).as_posix(),'apply_report_sha256':sha(qa/'apply_verification.json'),'final_ZIP_apply':final_apply,'final_ZIP_apply_byte_for_byte_target_match':True,'final_ZIP_payload_unchanged':True,'source_unchanged':True,'evidence_reuse':'Target ROM SHA identical; existing runtime/static/build evidence retained. Release changes packaging and xdelta apply path only.'}
    write_json(proof,result)
    print(json.dumps({'status':'PASS','archive':result['archive'],'archive_sha256':result['archive_sha256'],'patch_sha256':result['patch_sha256'],'files':len(files),'Windows_apply_checks':8,'final_ZIP_apply':'PASS'},ensure_ascii=False))
