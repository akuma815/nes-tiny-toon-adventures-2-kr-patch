"""Requested v1.0 distribution from exact062; rebuild, ExpectedWrites, Windows apply."""
from pathlib import Path
import json,shutil,subprocess,zipfile
import release_apply_helpers132 as helpers
import seal_nonplay171 as records
from seal_nonplay171 import R,sha
from dialogue_ips import apply

NAME='TinyToonAdventures2_KR_v1.0_20261009'
PATCH=NAME+'.xdelta'
SOURCE=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes'
BASE=R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes'
SOURCE_SHA='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
TARGET_SHA='7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce'

def put(p,z):p.write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n','utf-8')

def main():
    records.DATE='2026-10-09'
    assert sha(SOURCE)==SOURCE_SHA and sha(BASE)==TARGET_SHA
    build=R/'build/release_v1_0_220';compile_dir=R/'build/release220_compile'
    out=R/'dist'/NAME;archive=R/'dist'/(NAME+'.zip')
    assert all(not p.exists() for p in (build,compile_dir,out,archive))
    run=subprocess.run(['python','-B',str(R/'scripts/build_credits11_211.py'),'--output',str(compile_dir)],capture_output=True,text=True,check=True)
    compiled=compile_dir/'TinyToon2_Text11_Candidate062.nes'
    assert compiled.read_bytes()==BASE.read_bytes()
    assert (compile_dir/'TinyToon2_Text11_Candidate062.ips').read_bytes()==(BASE.with_suffix('.ips')).read_bytes()
    src=SOURCE.read_bytes();target=compiled.read_bytes();model=bytearray(src);owned=set()
    writes=json.loads((compile_dir/'expected_writes.json').read_text('utf-8'))
    for z in writes:
        p,n=z['file_offset'],z['length'];area=set(range(p,p+n))
        assert not owned&area and src[p:p+n]==bytes.fromhex(z['expected_hex'])
        final=bytes.fromhex(z['final_hex']);assert len(final)==n
        owned|=area;model[p:p+n]=final
    assert model==target and apply(src,(compile_dir/'TinyToon2_Text11_Candidate062.ips').read_bytes())==target
    build.mkdir();result=build/'TinyToon2_KR_v1.0.nes';result.write_bytes(target)
    shutil.copyfile(compile_dir/'TinyToon2_Text11_Candidate062.ips',build/'TinyToon2_KR_v1.0.ips')
    shutil.copyfile(compile_dir/'expected_writes.json',build/'expected_writes.json')
    put(build/'release_build.json',{'version':'1.0','source_sha256':SOURCE_SHA,'ROM_sha256':sha(result),
        'bytes':len(target),'regenerated_exact062':True,'ExpectedWrite_records':len(writes),
        'overlapping_writers':0,'unexplained_final_bytes':0,'IPS_apply_exact':True,
        'request':'User requested final distribution build and Cafe worklog;062 selected as packaging baseline.',
        'CSV_statuses_preserved':'45 draft +9 macro/template untranslated; no fabricated human signoff',
        'gameplay062_QA':'NOT_RECORDED_USER_OWNED'})
    prior=R/'dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009'
    prior_proof=json.loads((R/'qa/reports/text11_212_package.json').read_text('utf-8'))
    out.mkdir()
    for n in ('apply.cmd','tools/xdelta3.exe','tools/README_xdelta3.md','tools/LICENSE_xdelta3.txt',
              'licenses/Galmuri_OFL.md','licenses/Galmuri11_v2.40.4_OFL.txt'):
        assert sha(prior/n)==prior_proof['contents_sha256'][n]
        (out/n).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(prior/n,out/n)
    patch=out/PATCH
    subprocess.run([str(out/'tools/xdelta3.exe'),'-e','-s',str(SOURCE),str(result),str(patch)],check=True,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
    script=(prior/'apply.ps1').read_text('utf-8-sig')
    oldpatch=prior.name+'.xdelta'
    for old,new in [(oldpatch,PATCH),(sha(prior/oldpatch),sha(patch)),('텍스트11px 후보062','한글패치 v1.0')]:
        assert old in script;script=script.replace(old,new)
    helpers.windows_text(out/'apply.ps1',script)
    helpers.windows_text(out/'README_적용방법.txt',f'''타이니툰 어드벤처 2 한글패치 v1.0 — 2026-10-09

Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan) 일본판 전용입니다.
ROM은 포함하지 않습니다. 직접 준비한 깨끗한 원본 파일을 사용하세요.

적용 방법
1. ZIP을 폴더에 모두 풉니다. tools와 licenses 폴더도 함께 유지하세요.
2. 원본 .nes 파일을 apply.cmd 위로 끌어 놓습니다.
3. 같은 폴더에 원본이름_KR.nes가 생성됩니다.
명령행: apply.cmd "원본 게임.nes" "TinyToon2_KR_v1.0.nes"
Windows PowerShell과 함께 제공한 xdelta3 도구를 사용합니다.
원본·기존 출력은 덮어쓰지 않습니다. 기존 한글판에 덧씌우지 않습니다.
원본 크기:262160바이트 / SHA-256:{SOURCE_SHA}
결과 크기:524304바이트 / SHA-256:{TARGET_SHA}

이번 배포
062와 같은 게임 데이터를 v1.0 배포 파일로 고정했습니다.
타이틀·지도·매표소·결과·상태창·정지 표지판 등 기존 한글 그림을 포함합니다.
오프닝9·일반 대사33·크레딧3의 등록45문단에11px 글꼴을 적용했습니다.
HUD와 정지 표지판 등 작은 그림은 기존 크기를 유지했습니다.
숫자는8px 타일 간격이며 모든 글자의 실제 획높이가11px인 것은 아닙니다.

검증 상태
독립 재빌드·ExpectedWrites·전체 결과 해시·Windows 패치 적용을 검증했습니다.
기존062 정적 글꼴/CPU 및 한정 NMI·IRQ 검사도 같은 ROM 데이터의 근거입니다.
062 실제 에뮬레이터 화면·전체 플레이 검수 결과는 아직 기록되지 않았습니다.
본 배포 요청을 최종 화면/문체 승인이나 완주 통과 기록으로 바꾸지 않았습니다.
텍스트 출력·건너뛰기·지우기·티켓 교환·놀이기구·크레딧은 실제 플레이 확인 대상입니다.
이전 버전 세이브스테이트 호환은 미확인입니다. 새 ROM을 열고 초기화해 시작하세요.

원문 유지: HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT.
타이틀 숫자2·PUSH START·저작권 등 기존 보호 대상도 유지했습니다.
45는 등록 문단 수이며 전게임 텍스트 발견률/완료율을 뜻하지 않습니다.
오류 보고에는 ROM SHA·에뮬레이터 버전·직전 행동·장면 이미지를 함께 기록하세요.
원작·캐릭터의 권리는 해당 권리자에게 있습니다. 팬 번역 패치입니다.
글꼴과 적용 도구의 출처·라이선스는 licenses 및 tools 폴더에 있습니다.
''')
    (out/'RELEASE_NOTES_KO.md').write_text('''# 타이니툰 어드벤처2 한글패치 v1.0

062의 게임 데이터를 그대로 사용한 배포 패키지다. 타이틀 PNG 추출·생성형 이미지·NES 타일 변환, 대사별 글꼴, 지도/매표소/결과/HUD/정지 그림, 티켓교환 글꼴 충돌 수정050과 움직이는 정지 표지판 수정051을 계승한다. 등록45문단(오프닝9·일반33·크레딧3)의11px 글꼴을 포함한다. HUD·정지 등 작은 그림은 기존 크기다. 오프닝6은 ‘깜짝 놀랄 거다!’를 한 줄로 묶고 ‘의문의 대부호로부터’를 오른쪽 정렬했다.

원문 유지6건은 HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT다. 사용 경로가 미확정인 원천의 사용자 범위 결정이며 모든 화면의 전역 미사용을 뜻하지 않는다. 크레딧 이름·KONAMI·권리 문구는 같고 글자 그림은 확대했다. 영문16px 간격/한글12px 셀의 현재 배치를 사용한다.

빌드·패치 적용을 검증했고 같은062의 기존 정적/CPU/한정 NMI·IRQ 근거를 연결한다. 실제062 화면·가독성·CHR 매핑·소거/전환·완주 검수는 기록되지 않았다. 이전 버전 캡처를062 실제 플레이 통과로 표기하지 않는다. 원본 ROM과 저장상태를 배포하지 않는다.
''','utf-8')
    for n in ('text11_211_ordinary_CPU.json','credits11_211_CPU.json','nmi216_actual_entry_budget.json',
              'irq217_injection.json','irq218_opening_credits.json'):
        q=json.loads((R/'qa/reports'/n).read_text('utf-8'))
        assert q.get('ROM_sha256',q.get('rom_sha256',TARGET_SHA))==TARGET_SHA
    helpers.PATCH=PATCH;helpers.SOURCE_SHA=SOURCE_SHA;helpers.TARGET_SHA=TARGET_SHA
    qa=R/'qa/release/release220_apply'
    verification=helpers.check_apply(out,qa,SOURCE,result)
    shutil.copyfile(qa/'apply_verification.json',out/'Windows_apply_verification.json')
    release={'version':'1.0','date':'2026-10-09','status':'RELEASE_ARTIFACT_APPLY_VERIFIED_PLAY_QA_NOT_RECORDED',
        'user_requested_final_package':True,'ROM_free':True,
        'source':{'name':SOURCE.name,'bytes':len(src),'sha256':SOURCE_SHA},
        'target':{'name':result.name,'bytes':len(target),'sha256':TARGET_SHA,'data_baseline':'062'},
        'patch':{'file':PATCH,'bytes':patch.stat().st_size,'sha256':sha(patch)},
        'regenerated_exact062':True,'ExpectedWrite_records':len(writes),'Windows_apply_checks':8,
        'registered_11px_paragraphs':{'opening':9,'ordinary':33,'credits':3},
        'compact_graphic_size':'Preserved','original_retention':['HOWTO','PAUSE','POW','RYO51','NT1C','diagnostic STAGE SELECT'],
        'CPU_NMI_IRQ_evidence':'Scoped exact062; runtime/hardware/whole-game proof not claimed',
        'actual062_visual_gameplay_review':'NOT_RECORDED_USER_OWNED','human_translation_signoff':'NOT_RECORDED',
        'save_state_compatibility':'NOT_VERIFIED','global_text_population_closed':False}
    put(out/'release_report.json',release)
    files=sorted(p for p in out.rglob('*') if p.is_file())
    (out/'SHA256.txt').write_text(''.join(f'{sha(p).upper()}  {p.relative_to(out).as_posix()}\n' for p in files),'utf-8')
    files=sorted(p for p in out.rglob('*') if p.is_file())
    assert all(p.suffix.lower() not in ('.nes','.mss','.bin','.sqlite') for p in files)
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,NAME+'/'+p.relative_to(out).as_posix())
    extracted=qa/'최종 배포 ZIP 검증';extracted.mkdir()
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==len(files)
        for p in files:assert z.read(NAME+'/'+p.relative_to(out).as_posix())==p.read_bytes()
        z.extractall(extracted)
    final_output=extracted/'최종 한글 게임.nes'
    final_apply=helpers.apply(extracted/NAME,SOURCE,extracted,final_output)
    assert final_apply['exit_code']==0 and final_output.read_bytes()==target,final_apply
    hashfile=archive.with_suffix('.zip.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
    evidence=R/'qa/reports/release220_verified.json'
    put(evidence,{'work':220,'status':'PASS_BUILD_ROMFREE_WINDOWS8_FINAL_ZIP_APPLY',
        'archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
        'source_sha256':sha(SOURCE),'ROM_sha256':sha(result),'files':len(files),
        'contents_sha256':{p.relative_to(out).as_posix():sha(p) for p in files},
        'Windows8':verification,'final_ZIP_apply':final_apply,'final_output_sha256':sha(final_output),
        'ROM_free':True,'regenerated_exact062':True,'runtime_visual_fullplay':'NOT_RUN'})
    body=f'''사용자의 최종배포 요청에 따라062와 동일한 데이터를 v1.0로 고정했다. [배포 ZIP](../dist/{archive.name}) SHA `{sha(archive)}`. [적용 안내](../dist/{NAME}/README_적용방법.txt). [로컬 ROM](../build/release_v1_0_220/TinyToon2_KR_v1.0.nes) SHA `{sha(result)}`. publicZIP은ROM없이{len(files)}파일이다.

build_credits11_211.py의 새 독립출력으로062 ROM/IPS를 재생성하고 기존062와 byte-exact 비교했다. 원본에서ExpectedWrites {len(writes)}개를 replay해 중첩0/기대원본일치/최종전체동일을 확인했다. 최종IPS를원본에적용한결과도동일하다. source·CSV·기존ROM/보고/ZIP을변경하지않았다. [빌드 보고](../build/release_v1_0_220/release_build.json), [패키지 보고](../qa/reports/release220_verified.json).

Windows 정상적용·기존출력거부·원본=출력거부·동일크기타판본거부·이미패치본거부·손상패치거부·손상도구거부·인자없음8사례를실행했다. 한글/공백경로 최종ZIP 추출본apply.cmd도전체결과byte-exact PASS. CRC/파일목록/페이로드/ROM-free확인. tool·font라이선스포함.

정적/CPU근거는동일062의211/216~218에한정해계승한다. 실제062エ뮬레이터/장면/완주/가독성검수는미기록·사용자담당이며배포요청을완주승인이나CSV사람검토로바꾸지않았다. 원천45draft/9macro-template 상태도보존했다. release_report와플레이어안내가같은한계를명시한다. 이전버전저장상태호환도미확인이다. 사용자요청에따라파일은최종배포용으로구성했으나전게임완료율/최종QA승인을주장하지않는다.

변경: release220.py,새빌드/패키지/ZIP/해시/보고와인계. 재현: python -B scripts/release220.py (고정출력덮어쓰기거부,새경로복제에서실행). 이번시행의에뮬레이터/컨트롤러실행/외부업로드없음. 카페작업기는다음작업에서만든뒤불필요한펼친자료를정리한다.'''
    records.seal(220,'RELEASE_V1_0_BUILD_PACKAGE_220.md','최종배포 v1.0 빌드·ROM없는 적용패키지',body,
        '062 exact데이터 v1.0/ExpectedWrites/독립재빌드/Windows8/최종ZIP 적용 PASS.실제062 플레이검수 미기록.',
        '네이버 카페 복사용 작업기·근거구분 PNG·오프라인 HTML을 만들고 데스크톱/모바일 렌더를 확인한다.',
        [Path(__file__),result,build/'release_build.json',build/'expected_writes.json',evidence,archive,hashfile,*files])
    print(json.dumps({'status':'PASS','ZIP':archive.name,'sha256':sha(archive),'files':len(files)},ensure_ascii=False))

if __name__=='__main__':main()
