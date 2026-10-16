"""Finish cleanup handoff and seal the archive/index/audit assets without rerunning games."""
import json, re
from audit_cleanup230 import audit
from prepare_cleanup230 import R, PLAN, digest, CANONICAL

def main():
    doc=R/'docs/SUPERSEDED_PUBLICATION_CLEANUP_230.md';manifest=R/'manifests/nonplay230_assets.json';report=R/'qa/reports/cleanup230_verified.json'
    assert not doc.exists() and not manifest.exists() and not report.exists()
    result=audit();plan=json.loads(PLAN.read_text('utf-8'))
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    next_action='사용자가 최신 작업기·기술 지침과 최종 릴리즈를 게시하고, 배포 이후 제보를 수집한다.'
    doc.write_text(f'''# 인계 2026-10-09

## 작업230 — 불필요한 이전 게시자료·검토본·중복 결과 정리

- 요청/목표: 불필요한 파일을 정리하되 원본·번역원천·재현스크립트·현재산출물·검증근거를 보존한다.
- 현재 기준 원본·빌드·완료 조건: 게임v1.0 릴리즈, 작성자말투작업기, 내부번호없는1·2편기술지침이최신이다. 사용자 실제화면·완주1차완료와배포후검증예정상태를유지한다. 재현·사용자환경은변경하지않는다.
- 완료 결과: 이전게시자료폴더3개·이전렌더QA8개·중복독립재빌드1개와이전ZIP/SHA8개경로, 합계20대상/90파일을전수검증보관후삭제했다. 원래파일8,492,956바이트가보관본6,010,648바이트가됐다. 차이2,482,308바이트는대상파일과보관본만의비교이며새문서·인덱스용량을제외한수치다.
- 변경 파일·산출물·SHA-256: private `qa/archive/cleanup230_superseded.zip`, SHA `{plan['archive_sha256']}`; index `qa/reports/cleanup230_plan.json`, 실행 `cleanup230_execution.json`, 사후 `cleanup230_verified.json`, 조사 `cleanup230_inventory.json`; preparation/execution/audit/restore/finish scripts와현재문서·날짜인계·journal·계획을갱신했다. 전체해시는 `manifests/nonplay230_assets.json`에있다. 보관본에는중복재빌드ROM이있으므로공개ZIP과분리한다.
- 재현 명령·환경: PowerShell로명시적절대경로만삭제했다. 삭제전모든대상의실제경로·프로젝트내포함·reparse부재·파일목록·크기·SHA와보관본SHA를검사했다. 사후검사 `python -B scripts/audit_cleanup230.py`; 보관전수확인 `python -B scripts/restore_cleanup230.py --verify-all`.
- 정적 검증: 삭제대상90파일의압축복원바이트를전수SHA확인했다. 보존파일{result['retained_files_SHA_verified']}개SHA와이전225/227/228/229manifest의{result['historical_manifest_entries_verified_current_or_archive']}항목을현재파일또는230보관에서대조했다. 현재공개ZIP3개CRC·ROM없음·SHA가같다. 현재리더·본문·그림·현재렌더QA는그대로다. 문서링크는최신사용경로와이보관안내를우선한다.
- 빌드/패치 적용 검증: 새빌드·새패치적용은미수행. 최종ROM과원본·CSV및이전빌드의해시불변을보존파일전수검사로확인했다. 독립재빌드ROM은현재채택후보ROM과같은SHA인것을확인하고230에보관했다.
- 에뮬레이터 실행 검증: 미수행. 사용자Mesen·세이브와프로젝트도구3개버전은삭제·조작하지않았다. 이전사용자복사본의hostSHA가서로달라서동일중복실행파일로취급하지않았다.
- 직접 장면 시각 검증: 새게임실행·새화면캡처·리더재렌더는미수행. 기존실제게임캡처원천은live로보존하고최신작업기/기술지침렌더QA를live로남겼다.
- 미수행·미해결·기각한 설명: 과거폴더가없으면파손으로추정하지않고230index를조회한다. 과거봉인스크립트의고정경로검사나이전재현입력에접근할때는필요한원천을먼저복원해야한다. 재현입력인초기작업기003·배포212/220패키지폴더·기준051/현재062·현재릴리즈220·번역/그래픽/폰트원천·도구·스크립트·문서·기존4보관본은live로유지했다. 예전에직접삭제가차단된 `qa/dialogue/booth039_font_probe`는대상에서제외했고재삭제하지않았다. 디렉터리빈껍데기전체나파일이름패턴만으로삭제하지않았다.
- 작업기용 근거: 최신작성자작업기및그림8개, 최신1·2편기술지침/설명도2개, 원본·수정실제캡처,사용자검수보고와현재증거분류를보존했다. 실제카페게시·Page수정은수행하지않았다.
- 다음 작업 하나: {next_action}

## 현재 배포와 게시자료

- [최종게임배포ZIP](../dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip)
- [작성자말투작업기ZIP](../dist/TinyToon2_KR_Worklog_AuthorVoice_20261009.zip), [리더](../workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html)
- [기술지침ZIP](../dist/TinyToon12_TechnicalGuide_Reader_20261009.zip), [리더](../workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html)

## 필요한 과거 파일만 복원하기

현재파일과다른바이트가있으면복원을거부하고덮어쓰지않는다. 모든복원경로는230index에있는프로젝트내경로로한정한다.

```powershell
# 작성자말투생성기의이전리더입력이필요할때
python -B scripts/restore_cleanup230.py --root workspace/publication/TinyToon2_KR_Worklog_Reader_20261009

# 내부번호제거생성기의이전HTML/기술MD입력이필요할때
python -B scripts/restore_cleanup230.py --root workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009
python -B scripts/restore_cleanup230.py --root workspace/publication/TinyToon12_TechnicalGuide_20261009

# 과거결과중하나만확인할때
python -B scripts/restore_cleanup230.py --file dist/TinyToon2_KR_Worklog_Reader_20261009.zip
```

여러과거봉인검사기의나머지QA/ZIP입력도같은방식으로해당루트를복원한다. `audit_cleanup230.py`는정리완료상태(이전루트부재)를검사하므로복원을수행한후에는루트가남아있다는결과를정리실패나archive파손으로오해하지않는다. 전수보관검사 `restore_cleanup230.py --verify-all`은live복원여부와관계없이쓸수있다.230보다이전의missing자료는214/222/223/226복원도구를함께확인한다.
''','utf-8')
    entry=f'\n\n## 작업230 — 불필요한 이전 게시자료·검토본 정리\n\n20대상90파일을private230보관으로전수검증후삭제했다. 최신게임배포·작성자작업기·기술지침과보존4713파일SHA확인PASS. [변경·해시·검증·복원]({doc.name}).\n\n다음 작업 하나: {next_action}\n'
    for name in ('HANDOFF_2026-10-09.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md'):
        p=R/'docs'/name;text=p.read_text('utf-8')
        if name=='LOCALIZATION_WORK_PLAN.md':text=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 이전 게시자료·검토본 정리 완료. 최신 배포·작업기·기술 지침 유지.**',text,count=1)
        p.write_text(text+entry,'utf-8')
    p=R/'docs/journal/2026-10-09.md';p.write_text(p.read_text('utf-8')+entry.replace('('+doc.name+')','(../'+doc.name+')'),'utf-8')
    for p in (R/'docs/HANDOFF.md',R/'README.md'):
        text=p.read_text('utf-8');text=re.sub(r'^(?:> [^\n]*\n\n)+','',text)
        link_prefix='../' if p.name=='HANDOFF.md' else ''
        doc_prefix='' if p.name=='HANDOFF.md' else 'docs/'
        prefix=f'> 최신공개자료: [게임배포]({link_prefix}dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip) · [작성자작업기]({link_prefix}workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html) · [기술지침]({link_prefix}workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html). 이전게시자료·QA·중복재빌드는 [230보관·복원안내]({doc_prefix}{doc.name})를따른다.\n\n'
        if p.name=='HANDOFF.md':
            text=re.sub(r'^# [^\n]*','# 최종 배포·게시자료 유지 및 불필요 파일 정리 완료 — 2026-10-09',text,count=1)
            text=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+next_action+'**',text,count=1)
        p.write_text(prefix+text+(entry if p.name=='HANDOFF.md' else entry.replace('('+doc.name+')','(docs/'+doc.name+')')),'utf-8')
    # All excluded canonical paths are exactly the authorized documentation updates.
    assert CANONICAL=={'README.md','docs/HANDOFF.md','docs/HANDOFF_2026-10-09.md','docs/SURVEY.md','docs/LOCALIZATION_WORK_PLAN.md','docs/journal/2026-10-09.md'}
    assets=[doc,report,PLAN,R/plan['archive'],R/'qa/reports/cleanup230_inventory.json',R/'qa/reports/cleanup230_execution.json']
    assets.extend(R/'scripts'/name for name in ('inventory_cleanup230.py','prepare_cleanup230.py','execute_cleanup230.ps1','restore_cleanup230.py','audit_cleanup230.py','finish_cleanup230.py'))
    manifest.write_text(json.dumps({'work':230,'files':{p.relative_to(R).as_posix():digest(p) for p in sorted(set(assets))}},ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
