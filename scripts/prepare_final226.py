"""Correct dotted-version archive basename; verify final ZIP and prepare scoped cleanup."""
from pathlib import Path
import json,shutil,zipfile,hashlib
from seal_nonplay171 import R,sha
import release_apply_helpers132 as helpers
from release220 import SOURCE,BASE
NAME='TinyToonAdventures2_KR_v1.0_Release_20261009'

def main():
    old=R/'dist/TinyToonAdventures2_KR_v1.zip';final=R/'dist'/(NAME+'.zip')
    assert not final.exists();shutil.copyfile(old,final);assert final.read_bytes()==old.read_bytes()
    Path(str(final)+'.sha256').write_text(f'{sha(final).upper()}  {final.name}\n','ascii')
    qa=R/'qa/release/release226_final_zip';qa.mkdir()
    with zipfile.ZipFile(final) as z:
        assert z.testzip() is None;z.extractall(qa)
    output=qa/'최종 배포 확인.nes';actual=helpers.apply(qa/NAME,SOURCE,qa,output)
    assert actual['exit_code']==0 and output.read_bytes()==BASE.read_bytes(),actual
    report={'work':226,'status':'PASS_CORRECT_FILENAME_FINAL_ZIP_APPLY',
      'archive':final.relative_to(R).as_posix(),'archive_sha256':sha(final),
      'package_data_changed':False,'file_name_correction':'Path.with_suffix treated .0_Release_20261009 as a suffix; appended .zip instead',
      'actual_final_named_ZIP_apply':actual,'output_ROM_sha256':sha(output)}
    (R/'qa/reports/release226_apply.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    obsolete=['dist/TinyToonAdventures2_KR_v1.0_20261009.zip',
      'dist/TinyToonAdventures2_KR_v1.0_20261009.zip.sha256',
      'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009.zip',
      'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009.zip.sha256',
      'dist/TinyToonAdventures2_KR_v1.zip','dist/TinyToonAdventures2_KR_v1.zip.sha256']
    backup=R/'qa/archive/release226_superseded.zip';assert not backup.exists()
    archivefiles={rel:{'sha256':sha(R/rel),'bytes':(R/rel).stat().st_size} for rel in obsolete}
    with zipfile.ZipFile(backup,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in obsolete:z.write(R/rel,rel)
    with zipfile.ZipFile(backup) as z:
        assert z.testzip() is None
        for rel,item in archivefiles.items():assert hashlib.sha256(z.read(rel)).hexdigest()==item['sha256']
    roots=[{'path':rel,'directory':False,'kind':'ARCHIVED_SUPERSEDED'} for rel in obsolete]
    for rel in ('qa/release/release224_final_zip','qa/release/release226_final_zip','qa/publication/render225_final/browser_profile'):
        roots.append({'path':rel,'directory':True,'kind':'DISPOSABLE_OWN_APPLY_OR_RENDER_TEMP'})
    files={}
    for item in roots:
        p=R/item['path'];assert p.exists() and p.resolve().is_relative_to(R)
        for file in p.rglob('*') if item['directory'] else [p]:
            if file.is_file():files[file.relative_to(R).as_posix()]={'sha256':sha(file),'bytes':file.stat().st_size}
    plan={'work':226,'status':'VERIFIED_READY_FOR_SCOPED_CLEANUP','archive':backup.relative_to(R).as_posix(),
      'archive_sha256':sha(backup),'archive_bytes':backup.stat().st_size,'archived_files':archivefiles,
      'roots':roots,'files':files,'file_count':len(files),'selected_bytes':sum(x['bytes'] for x in files.values())}
    (R/'qa/reports/cleanup226_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'status':report['status'],'ZIP':final.name,'cleanup_files':len(files)},ensure_ascii=False))

if __name__=='__main__':main()
