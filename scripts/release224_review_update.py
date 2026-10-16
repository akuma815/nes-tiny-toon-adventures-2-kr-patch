"""Update final distribution documentation from user's initial062 playthrough report."""
from pathlib import Path
import json,shutil,zipfile,subprocess
from seal_nonplay171 import R,sha
import seal_nonplay171 as records
import release_apply_helpers132 as helpers
from release220 import SOURCE,BASE,SOURCE_SHA,TARGET_SHA
records.DATE='2026-10-09'
OLD='TinyToonAdventures2_KR_v1.0_20261009'
NAME='TinyToonAdventures2_KR_v1.0_Release_20261009'

def main():
    out=R/'dist'/NAME;archive=out.with_suffix('.zip');assert not out.exists() and not archive.exists()
    prior=R/'dist'/OLD;shutil.copytree(prior,out)
    oldpatch=OLD+'.xdelta';newpatch=NAME+'.xdelta'
    (out/newpatch).write_bytes((out/oldpatch).read_bytes());(out/oldpatch).unlink()
    ps=(out/'apply.ps1').read_text('utf-8-sig').replace(oldpatch,newpatch)
    helpers.windows_text(out/'apply.ps1',ps)
    user={'date':'2026-10-09','artifact':'062','ROM_sha256':TARGET_SHA,'reported_by':'user',
      'message':'062 실제 화면 완주는 내가 1차 완료 했고, 배포 이후 검증 필요해',
      'initial_actual_screen_playthrough':'COMPLETED_USER_REPORTED','post_distribution_validation':'REQUIRED_PLANNED',
      'new_agent_emulator_execution':False,'new_capture_or_input_log_submitted':False}
    receipt=R/'qa/reports/user_review224.json';receipt.write_text(json.dumps(user,ensure_ascii=False,indent=2)+'\n','utf-8')
    readme=(out/'README_적용방법.txt').read_text('utf-8-sig')
    start=readme.index('062 실제 에뮬레이터 화면');end=readme.index('이전 버전 세이브스테이트',start)
    readme=readme[:start]+'''2026-10-09 사용자가062의 실제 화면·완주1차 검수를 완료했다고 보고했습니다.
v1.0은 그062와 같은 데이터입니다. 배포 후 추가 검증은 계속 진행할 예정입니다.
이 기록은 사용자1차 검수 보고이며 이번 패키지 작업에서 새 게임 실행 로그를 만든 것은 아닙니다.
버그를 발견하면 ROM 해시·에뮬레이터 버전·직전 행동·장면 이미지를 함께 기록해 주세요.
'''+readme[end:]
    helpers.windows_text(out/'README_적용방법.txt',readme)
    notes=(out/'RELEASE_NOTES_KO.md').read_text('utf-8')
    notes=notes.replace('실제062 화면·가독성·CHR 매핑·소거/전환·완주 검수는 기록되지 않았다.',
      '2026-10-09 사용자가062의 실제 화면·완주1차 검수를 완료했다고 보고했다. 배포 이후 추가 검증을 이어간다. 사용자의 보고와 이번 패키지 작업의 검증 로그를 구분한다.')
    (out/'RELEASE_NOTES_KO.md').write_text(notes,'utf-8')
    q=json.loads((out/'release_report.json').read_text('utf-8'))
    q['status']='FINAL_RELEASE_USER_INITIAL_PLAYTHROUGH_REPORTED_POST_RELEASE_QA_PLANNED'
    q['patch']['file']=newpatch;q['actual062_visual_gameplay_review']='COMPLETED_INITIAL_USER_REPORT_2026-10-09'
    q['post_distribution_validation']='REQUIRED_PLANNED';q['user_review']=user
    q['human_translation_signoff']='Artifact selected for release by user; row-level CSV statuses preserved'
    (out/'release_report.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf-8')
    (out/'USER_REVIEW_KO.md').write_text('''# 1차 검수 및 배포 이후 검증

2026-10-09 사용자는062의 실제 화면·완주1차 검수를 완료했다고 보고했습니다. v1.0의 ROM은 그062와 완전히 같습니다. 배포 이후 추가 검증이 필요하다는 사용자 판단을 유지합니다.

이번 갱신은 검수 상태와 배포 안내의 반영입니다. 게임 데이터를 바꾸거나 에뮬레이터를 새로 실행하지 않았습니다. 초기 보고에 새 스크린샷·입력 로그가 첨부된 것은 아니므로 자동 검증의 정량 결과를 늘려 표기하지 않습니다.
''','utf-8')
    assert sha(SOURCE)==SOURCE_SHA and sha(BASE)==TARGET_SHA
    files=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='SHA256.txt')
    (out/'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files),'utf-8')
    files=sorted(p for p in out.rglob('*') if p.is_file())
    assert len(files)==14 and all(p.suffix.lower() not in ('.nes','.sav','.mss','.sqlite') for p in files)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,NAME+'/'+p.relative_to(out).as_posix())
    qa=R/'qa/release/release224_final_zip';qa.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p in files:assert z.read(NAME+'/'+p.relative_to(out).as_posix())==p.read_bytes()
        z.extractall(qa)
    output=qa/'1차 검수 반영 최종.nes';actual=helpers.apply(qa/NAME,SOURCE,qa,output)
    assert actual['exit_code']==0 and output.read_bytes()==BASE.read_bytes(),actual
    evidence=R/'qa/reports/release224_verified.json'
    proof={'work':224,'status':'PASS_FINAL_RELEASE_USER_FIRST_REVIEW_RECORDED','archive':archive.relative_to(R).as_posix(),
       'archive_sha256':sha(archive),'files':14,'ROM_sha256':TARGET_SHA,'ROM_free':True,'game_data_changed':False,
       'user_initial_review':'COMPLETED_REPORTED','post_release_QA':'PLANNED','actual_final_ZIP_apply':actual,
       'Windows8_reused':'220 negative/positive cases; guards unchanged except patch basename',
       'final_output_sha256':sha(output),'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files}}
    evidence.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n','utf-8')
    hashfile=archive.with_suffix('.zip.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
    body=f'''추가사용자보고 ‘062 실제 화면 완주는 내가1차 완료 했고, 배포 이후 검증 필요해’를 [검수기록](../qa/reports/user_review224.json)에반영했다. [최종배포ZIP](../dist/{archive.name}) SHA `{sha(archive)}`·14파일/ROM없음.062 ROM데이터는변경없고1차화면/완주검수는사용자완료보고로연결한다. 배포후추가검증필요판단을보존했다.

220의당시미기록안내를덮어쓰지않고새224파일의README/노트/report/USER_REVIEW에현재상태를반영했다. 기존CSV의행별상태는사람검토완료로일괄변경하지않았다. 원본/062해시동일·ZIP CRC/정확payload/ROM-free·한글/공백경로의최종ZIP 실제apply.cmd byte-exact PASS.220의Windows8경계거부검사는보존하며224에서는이름이바뀐최종ZIP정상적용을실행했다. [224검증](../qa/reports/release224_verified.json).

새게임/컨트롤러/장면/완주로그생성·카페게시없음. 사용자보고와CPU/자동검사근거를구분한다. 기존220/221 ‘062미기록’ 표기는당시역사상태이고새보고이후정본배포/작업기에서교체한다. 변경: release224_review_update.py,새패키지/ZIP/해시/검수영수증/보고와인계. 재현은새출력경로의복제에서실행한다.'''
    records.seal(224,'FINAL_RELEASE_USER_FIRST_QA_224.md','사용자062 1차완주 검수 반영 최종배포',body,
       '사용자062 실화면·완주1차완료보고 반영.데이터불변·14파일ROMfree·최종ZIP 실제적용 PASS.배포후검증예정.',
       '카페작업기와검증표에도사용자1차완주완료/배포후검증예정을반영하고다시렌더한다.',
       [Path(__file__),receipt,evidence,archive,hashfile,*files])
    print(json.dumps({'status':'PASS','ZIP':archive.name,'sha256':sha(archive)},ensure_ascii=False))

if __name__=='__main__':main()
