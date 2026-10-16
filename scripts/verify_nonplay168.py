"""Apply the finalized168 ZIP in a fresh Korean/space path and seal support artifacts."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, zipfile
from seal_nonplay166 import R, sha, seal

def main():
    report=R/'qa/reports/nonplay168_final.json';assert not report.exists()
    pkg=json.loads((R/'qa/reports/nonplay168_package.json').read_text('utf-8'))
    archive=R/pkg['archive'];assert sha(archive)==pkg['archive_sha256']
    root=R/'qa/apply/2편 개발049 한글 공백 적용 검증 20261007_168';assert not root.exists();root.mkdir()
    with zipfile.ZipFile(archive)as z:
        assert z.testzip()is None
        for n in z.namelist(): assert (root/n).resolve().is_relative_to(root.resolve())
        z.extractall(root)
    extracted=root/'TinyToonAdventures2_KR_Review_049_20261007'
    for f,h in pkg['contents_sha256'].items():assert sha(extracted/f)==h
    sums=(extracted/'SHA256.txt').read_text('utf-8').splitlines()
    assert len(sums)==19
    for line in sums:
        h,f=line.split('  ',1);assert sha(extracted/f)==h
    source_meta=json.loads((R/'manifests/source_rom.json').read_text('utf-8'))
    original=R/source_meta['path'];source=root/'검증 원본 일본판.nes';target=root/'새 결과 검토049.nes'
    assert sha(original)==source_meta['sha256'];shutil.copy2(original,source)
    helper=extracted/'apply.cmd'
    # Use the same proven Windows cmd invocation as132; new paths include Korean/spaces.
    command=[os.environ.get('COMSPEC',r'C:\Windows\System32\cmd.exe'),'/d','/s','/c',f'""{helper}" "{source}" "{target}""']
    run=subprocess.run(command,capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    observation={'command':command,'exit_code':run.returncode,'stdout':run.stdout.decode('utf-8',errors='replace'),'stderr':run.stderr.decode('utf-8',errors='replace')}
    (root/'apply_observation.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2)+'\n','utf-8')
    assert run.returncode==0,observation
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    assert target.read_bytes()==rom.read_bytes()and sha(target)==pkg['current049_ROM_sha256']
    assert sha(source)==sha(original)==source_meta['sha256']
    for f,h in pkg['contents_sha256'].items():assert sha(extracted/f)==h
    assert sha(archive)==pkg['archive_sha256']
    result={'work':168,'status':'PASS_ROMFREE_FINAL_ZIP_ACTUAL_WINDOWS_APPLY','archive':pkg['archive'],
        'archive_sha256':sha(archive),'ZIP_files':20,'ROM_free':True,'SHA256_manifest_files':19,
        'actual_final_ZIP_Windows_apply':observation,'unicode_space_paths':True,'target_byte_exact':True,
        'source_and_payload_unchanged':True,'ROM_sha256':sha(target),'CSV_sha256':pkg['CSV_sha256'],
        'review167_records_UI_evidence':'qa/reports/nonplay167_final.json','review167_sha256':sha(R/'qa/reports/nonplay167_final.json'),
        'runtime_evidence_reused_without_rerun':True,'new_game_execution':False,'actual_play_owner':'user',
        'human_approved':False,'distribution_eligible':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''[최신 검토용049 ZIP](../{pkg['archive']})을 작성했다. 기존132 패치/적용helper/도구/라이선스를 SHA로 확인해 그대로 사용하고, 최신 원천 목록·비플레이 검토자료167·지원 한계·사용자 검수 안내를 반영했다. 기존132 묶음은 보존했다. 새20파일 묶음은 ROM/폰트/에뮬레이터 없는 개발 검토본이다. 동일049이며 새 번역ROM 빌드나 최종 공개배포 승인이 아니다.

최신 지원 설명은133의 제한된 저장상태/리셋 검증을 반영하고, 다른빌드 세이브호환·모든상태·실기·PCM·전체플레이와 분리한다. 사용자검수안내는 타이틀/본문/HUD/성 입구/각놀이기구/게임오버/엔딩/리셋을 확인할 조건과 재현 결과 양식을 제공한다.7소비 미연결 후보·38cycle idle/RNG차이·163 PNG4410 비교실패를 명시했다. 검토자료21기존 실제/4정적PNG를 함께 제공한다. 외부게시하지 않았으며 카페 작업기는 전체완료뒤 작성한다.

[최종 적용 보고](../{report.relative_to(R).as_posix()}): 최종ZIP CRC/20파일 내용과19파일 SHA목록, 압축해제 후한글·공백경로에서 실제Windows `apply.cmd`를 실행했다. exit0,499728바이트 결과가현재049와 바이트단위 일치했다. 원본·ZIP·도구/패치/helper 모두불변. 이번변경은 새문서/패키지이므로 새로운최종ZIP 적용검사를 수행했고기존8검사를반복하지않았다. 새게임실행/정적CPU테스트/재빌드/런타임/직접게임장면/청음/사람플레이검수는실행하지않았다.167의문서브라우저검사는재사용한다.

ZIP SHA `{sha(archive)}`,ROM `{sha(rom)}`,CSV `{pkg['CSV_sha256']}`. 재현 생성 `python scripts/package_nonplay168.py`; 최종ZIP실제적용/봉인 `python scripts/verify_nonplay168.py` (기존출력을보호하므로 별도새출력경로를사용해야한다). 새스크립트/패키지/해시사이드카/적용보고/개별QA/인계문서/manifest변경. 모든신규산출물과근거SHA는manifest에기록한다. 실제플레이사용자담당·최종문구/명칭/그림/소비범위·전역원천폐쇄보류.'''
    files=[Path(__file__),R/'scripts/package_nonplay168.py',R/'qa/reports/nonplay168_package.json',report,archive,
        archive.parent/(archive.name+'.sha256'),rom,R/'workspace/translation/text_ja.csv',R/'qa/reports/review049_package_final132.json',
        R/'qa/reports/nonplay167_final.json',R/'qa/reports/state133_validation.json',R/'workspace/translation/nonplay_inventory049_166.json']
    out=R/'dist/TinyToonAdventures2_KR_Review_049_20261007'
    files.extend(p for p in out.rglob('*')if p.is_file());files.extend(p for p in root.rglob('*')if p.is_file())
    seal(168,'CURRENT049_REVIEW_PACKAGE_AND_USER_QA_GUIDE.md','최신 검토용 패키지·사용자 검수 안내',body,
        '동일049 패치/도구 보존, 최신 한계·검수 안내·비플레이 검토자료 포함한20파일 ROM없는ZIP. 최종ZIP 한글/공백경로 실제Windows적용 byte-exact PASS. 플레이 실행 없음.',
        '등록 밖 후보의 소비 근거를 정적 코드와 기존 증거로 추가 연결하고, 범위 응답을 반영할 때만 원문 보존 또는 번역 추가로 결정한다.',files)
    print(json.dumps({k:v for k,v in result.items()if k!='actual_final_ZIP_Windows_apply'},indent=2))

if __name__=='__main__':main()
