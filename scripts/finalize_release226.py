"""Audit final delivery and synchronize canonical handoff after cleanup."""
from pathlib import Path
import json,sqlite3,zipfile,hashlib,re
from seal_nonplay171 import R,sha
import seal_nonplay171 as records
records.DATE='2026-10-09'
PATCH='TinyToonAdventures2_KR_v1.0_Release_20261009.zip'
ARTICLE='TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip'
ARTICLE_DIR='workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009'
TARGET='7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce'
NEXT='배포 이후 접수되는 제보의 ROM 해시·에뮬레이터 버전·직전 행동·장면을 기록하고 해당 경로의 추가 검증을 진행한다.'

def main():
    plan=json.loads((R/'qa/reports/cleanup226_plan.json').read_text('utf-8'))
    deleted=json.loads((R/'qa/reports/cleanup226_deletion.json').read_text('utf-8-sig'))
    assert deleted['status']=='DELETED_ARCHIVED_SUPERSEDED_AND_OWN_TEMP'
    for item in plan['roots']:assert not (R/item['path']).exists()
    oldplan=json.loads((R/'work/cleanup222/final_plan.json').read_text('utf-8-sig'))
    dbs=[]
    for n in ('214','222'):
        p=R/oldplan['archive'+n];assert sha(p)==oldplan['archive'+n+'_sha256']
        dbs.append(sqlite3.connect(f'file:{p.as_posix()}?mode=ro',uri=True))
    olddist=json.loads((R/'qa/reports/obsolete_distribution223_archive.json').read_text('utf-8'))
    assert sha(R/olddist['archive'])==olddist['archive_sha256']
    assert sha(R/plan['archive'])==plan['archive_sha256']
    z223=zipfile.ZipFile(R/olddist['archive']);z226=zipfile.ZipFile(R/plan['archive'])
    assert z226.testzip() is None
    live=archived=0
    def check(rel,digest):
        nonlocal live,archived
        p=R/rel
        if p.is_file() and sha(p)==digest:live+=1;return
        for db in dbs:
            row=db.execute('SELECT sha256 FROM entries WHERE path=?',(rel,)).fetchone()
            if row and row[0]==digest:archived+=1;return
        for book,z,key in ((olddist,z223,'files'),(plan,z226,'archived_files')):
            if rel in book[key] and book[key][rel]['sha256']==digest:
                assert hashlib.sha256(z.read(rel)).hexdigest()==digest;archived+=1;return
        raise AssertionError(('Missing or changed frozen asset',rel,digest))
    manifests={}
    for n in range(197,226):
        p=R/f'manifests/nonplay{n}_assets.json'
        if not p.is_file():continue
        q=json.loads(p.read_text('utf-8'));manifests[str(n)]={'sha256':sha(p),'files':len(q['files'])}
        for rel,digest in q['files'].items():check(rel,digest)
    for rel,item in plan['archived_files'].items():assert hashlib.sha256(z226.read(rel)).hexdigest()==item['sha256']
    packages={}
    for name,proof in ((PATCH,'release224_verified.json'),(ARTICLE,'publication225_verified.json')):
        p=R/'dist'/name;q=json.loads((R/'qa/reports'/proof).read_text('utf-8'))
        assert sha(p)==q['archive_sha256']
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None and len(z.namelist())==q['files']
            assert all(not rel.lower().endswith(('.nes','.mss','.sav','.sqlite')) for rel in z.namelist())
            for rel in z.namelist():assert hashlib.sha256(z.read(rel)).hexdigest()==q['contents_sha256'][rel.split('/',1)[1]]
        packages[name]={'sha256':sha(p),'files':q['files'],'CRC_payload_ROMfree':'PASS'}
    protected={
      'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d',
      'workspace/translation/text_ja.csv':'43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f',
      'build/release_v1_0_220/TinyToon2_KR_v1.0.nes':TARGET,
      'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes':TARGET,
      'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes':'b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24'}
    for rel,digest in protected.items():assert sha(R/rel)==digest
    apply=json.loads((R/'qa/reports/release226_apply.json').read_text('utf-8'))
    assert apply['archive']==f'dist/{PATCH}' and apply['archive_sha256']==sha(R/'dist'/PATCH)
    assert apply['actual_final_named_ZIP_apply']['exit_code']==0 and apply['output_ROM_sha256']==TARGET
    render=json.loads((R/'qa/publication/render225_final/render_report.json').read_text('utf-8'))
    assert render['status']=='PASS'
    prior=json.loads((R/'qa/reports/final_release222_audit.json').read_text('utf-8'))
    saved=prior['net_payload_bytes_saved']+deleted['removed_bytes']-deleted['archive_bytes']
    proof={'work':226,'status':'PASS_FINAL_DELIVERY_CLEANUP_USER_FIRST_QA',
      'packages':packages,'live_asset_checks':live,'archived_asset_checks':archived,'frozen_manifests':manifests,
      'protected_hashes':protected,'source_translation_ROM_unchanged':True,'final_named_ZIP_actual_apply':'BYTE_EXACT_PASS',
      'article_desktop_mobile_zoom':'PASS','user_initial_actual062_QA':'COMPLETED_REPORTED',
      'post_distribution_QA':'REQUIRED_PLANNED','new_agent_game_execution':False,'cafe_uploaded':False,
      'cleanup_removed_files':prior['removed_files']+deleted['files'],'cleanup_net_payload_bytes_saved':saved,
      'old_public_ZIPs_losslessly_archived':True,'reproduction_inputs_kept':['dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009',
       'dist/TinyToonAdventures2_KR_v1.0_20261009',ARTICLE_DIR.replace('_Release_20261009','_20261009_003')],
      'blocked214_folder_untouched':True}
    out=R/'qa/reports/final_delivery226_audit.json';assert not out.exists()
    out.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''[최종 배포 ZIP](../dist/{PATCH}) SHA `{sha(R/'dist'/PATCH)}`·14파일, [카페 작업기 ZIP](../dist/{ARTICLE}) SHA `{sha(R/'dist'/ARTICLE)}`·13파일/8PNG. 모두 ROM 없다. v1.0 게임 데이터는 사용자1차 실제 화면·완주 검수를 마친062와 같고, 배포 이후 추가 검증은 예정 상태다. 새로운 플레이나 카페 업로드는 수행하지 않았다.

224의 ZIP 이름 생성에서 Path.with_suffix가 버전명 .0 뒤를 확장자로 해석하여 v1.zip이 됐다. 원래 기대한 전체 이름에 .zip을 덧붙여 같은 ZIP 바이트를 복사하고 다시 추출·실제 apply.cmd를 실행하여062와 byte-exact 일치를 확인했다.224 당시 증거를 수정하지 않고 [226 적용 기록](../qa/reports/release226_apply.json)에 교정을 남겼다. 이전220/221 ZIP 및224 짧은 이름 ZIP6파일은 SHA·CRC 검사 후 private 보관226에 넣고 live 중복을 삭제했다.

224/226의 적용 임시폴더와 종료된 격리225 렌더 프로필도 정확 경로로 삭제했다. QA 보고·렌더 PNG·원천은 유지한다.226은282파일/23,255,642바이트를 정리했고 보관본은1,069,617바이트다.222/223/226 정리 합계110,831파일, 순{saved:,}바이트(약{saved/2**30:.2f}GiB) 절감. 원본·번역CSV·051·062·최종ROM해시 불변이다. [최종 감사](../qa/reports/final_delivery226_audit.json)는197~225의 봉인 근거를 live 또는214/222/223/226 보관에서 확인한다.

재현 입력인212 패키지,220 패키지 원천,221의003 작업기 원천은 유지했다. 최종 업로드는 최신 두 ZIP만 사용한다. 복원: python -B scripts/restore_superseded226.py --file <보관된 상대경로>. 기존214/222/223 복원 도구와 인계도 유지한다. private QA 보관본은 업로드하지 않는다. 이전 삭제 거부 폴더는 손대지 않았다.

변경: prepare_final226.py, execute_final226.ps1, restore_superseded226.py, finalize_release226.py, 새 이름 최종ZIP/해시·private보관·적용/정리/감사보고, 정본README/HANDOFF/SURVEY/PLAN/AGENTS. Windows 적용과 오프라인 작업기 UI 확인은 실제 게임 추가 검증을 대신하지 않는다. 날짜별 인계와 journal에 사용자 보고 및 다음 조치를 연결한다.'''
    records.seal(226,'FINAL_DELIVERY_CLEANUP_226.md','최종 배포·작업기·정리와 인계 완료',body,
      '062 사용자1차화면·완주 완료 보고 반영.최종2ZIP·실제적용·작업기렌더 PASS.순약2.32GiB 정리·배포후검증 예정.',NEXT,
      [Path(__file__),*[R/p for p in ('scripts/prepare_final226.py','scripts/execute_final226.ps1','scripts/restore_superseded226.py',
       'qa/reports/release226_apply.json','qa/reports/cleanup226_plan.json','qa/reports/cleanup226_deletion.json',
       'qa/archive/release226_superseded.zip')],out,R/'dist'/PATCH,R/'dist'/(PATCH+'.sha256')])
    current=f'''# 최종 배포 준비 완료 — 2026-10-09, 작업226

**v1.0은062와 같은 데이터입니다. 사용자가 실제 화면·완주1차 검수를 완료했다고 보고했으며, 배포 이후 추가 검증이 필요합니다.** 새 게임 실행이나 실제 카페 게시를 수행한 것은 아닙니다. 아래 역사 기록의 ‘미검수·미채택’은 추가 사용자 보고 전 당시 상태입니다.

- [최종 배포 ZIP](../dist/{PATCH}) — ROM 없음,14파일,실제 Windows 적용 결과062와 완전히 같음.
- [네이버 카페 작업기 ZIP](../dist/{ARTICLE}) — 본문·안내·8PNG·HTML,ROM 없음.
- [오프라인 작업기](../{ARTICLE_DIR}/작업기.html), [카페 복사용 본문](../{ARTICLE_DIR}/카페_복사용_본문.txt).
- [로컬 최종 ROM](../build/release_v1_0_220/TinyToon2_KR_v1.0.nes),SHA `{TARGET}`.
- [사용자1차 검수 보고](../qa/reports/user_review224.json), [최종 감사](../qa/reports/final_delivery226_audit.json), [최종 인계](FINAL_DELIVERY_CLEANUP_226.md).

독립 재빌드·ExpectedWrites·ROM/IPS 비교, Windows 적용 사례와 최종ZIP 실제 적용, 한정 CPU/NMI/IRQ 검사 및 작업기PC/모바일/확대 확인은 통과했습니다. 실제 화면·완주1차 완료는 사용자 보고로 구분합니다. 배포 후 검증 결과는 아직 없습니다. 등록45문단(오프닝9·일반33·크레딧3)은 전게임 발견률100%를 뜻하지 않습니다. HUD·정지 그림의 크기와 원문 유지6원천은 사용자 결정대로 유지했습니다. CSV 행별 상태를 사람 검토 완료로 일괄 변경하지 않았습니다.

불필요한 과거 QA·이전 공개ZIP·임시 적용 사본·렌더 캐시를 손실 없는 보관/정확 경로 삭제로 정리했습니다.222/223/226 합계110,831파일,순약{saved/2**30:.2f}GiB 절감. 원본·번역원천·재현 스크립트·최종산출물·QA근거는 보존했습니다.214/222는 SQLite 보관,223/226은 ZIP 보관이며 private 보관본은 공개하지 않습니다. [222복원](LOSSLESS_RELEASE_CLEANUP_222.md), [223복원](SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md), [226복원](FINAL_DELIVERY_CLEANUP_226.md).212/220 패키지 및003 작업기 폴더는 재현 입력입니다.

**다음 작업 하나: {NEXT}** [오늘 인계](HANDOFF_2026-10-09.md), [오늘 journal](journal/2026-10-09.md), [계획](LOCALIZATION_WORK_PLAN.md).

---

## 이전 작업 당시의 역사 기록

'''
    p=R/'docs/HANDOFF.md';old=p.read_text('utf-8');p.write_text(current+old,'utf-8')
    brief=f'> **2026-10-09 작업226: v1.0(데이터062) 최종 배포·작업기 준비 완료. 사용자1차 실화면·완주 완료, 배포 이후 검증 예정.** [최신 인계](HANDOFF.md)\n\n아래 본문은 각 작업 당시의 역사 기록입니다. 현재 공개 파일과 검수 상태는 최신 인계를 따릅니다.\n\n'
    for name in ('SURVEY.md','LOCALIZATION_WORK_PLAN.md'):
        p=R/'docs'/name;p.write_text(brief+p.read_text('utf-8'),'utf-8')
    readme=current.replace('# 최종 배포 준비 완료','# Tiny Toon Adventures 2 — 한글패치 v1.0').replace('(../dist/','(dist/').replace('(../build/','(build/').replace('(../workspace/','(workspace/').replace('(../qa/','(qa/')
    for name in ('FINAL_DELIVERY_CLEANUP_226.md','LOSSLESS_RELEASE_CLEANUP_222.md','SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md','HANDOFF_2026-10-09.md','LOCALIZATION_WORK_PLAN.md'):
        readme=readme.replace('('+name+')','(docs/'+name+')')
    readme=readme.replace('(journal/2026-10-09.md)','(docs/journal/2026-10-09.md)')
    p=R/'README.md';p.write_text(readme+p.read_text('utf-8'),'utf-8')
    p=R/'AGENTS.md';p.write_text(p.read_text('utf-8')+'''\n\n## 작업226 최종 배포 및 보관 갱신 — 2026-10-09

현재 배포는 docs/HANDOFF.md의 v1.0_Release ZIP이다. 사용자062 실제 화면·완주1차 완료 보고를 반영했으며 배포 이후 추가 검증은 예정 상태다. 사용자 실제 플레이 담당 지침은 유지한다.

물리적 과거 경로가 없으면214 외에222/223/226 보관도 확인한다.222: scripts/restore_history222.py --file <상대경로>;223: scripts/obsolete_distribution223.py --restore <상대경로>;226: scripts/restore_superseded226.py --file <상대경로>. 각 도구는 보관 및 payload SHA를 확인하고 다른 live 파일을 덮어쓰지 않는다. private 보관본은 공개하지 않는다.212 패키지·220 패키지 원천·003 작업기 원천은 최종 재현 입력으로 보존했다.\n''','utf-8')
    # Verify current links, excluding deliberately retained historical sections.
    for filename,txt in (('docs/HANDOFF.md',current),('README.md',readme)):
        base=(R/filename).parent
        for link in re.findall(r'\]\(([^)]+)\)',txt):assert (base/link).is_file(),(filename,link)
    m=json.loads((R/'manifests/nonplay226_assets.json').read_text('utf-8'))
    for rel,digest in m['files'].items():assert sha(R/rel)==digest
    print(json.dumps({'status':proof['status'],'packages':packages,'removed_files':proof['cleanup_removed_files'],
      'net_payload_bytes_saved':saved,'canonical_links':'PASS','frozen_manifest226':'PASS'},ensure_ascii=False))

if __name__=='__main__':main()
