"""Seal editorial-only reader revisions, preserve game release and prior publication bytes."""
from pathlib import Path
import base64, json, re, zipfile
from seal_nonplay171 import R, sha

WORKLOG=R/'workspace/publication/TinyToon2_KR_Worklog_Reader_20261009'
GUIDE=R/'workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009'
PAGE='https://chatgpt.com/space/page_7e1e9fe45f1881918ff36b3962ea16c0'
NEXT='사용자가 수정된 작업기·기술 지침을 게시하고, 배포 후 제보의 ROM 해시·환경·직전 행동·장면을 수집한다.'

def verify_protected():
    expected={
      'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d',
      'workspace/translation/text_ja.csv':'43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f',
      'build/release_v1_0_220/TinyToon2_KR_v1.0.nes':'7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce',
      'dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip':'0e470e45968cb388f296a3103c0004641ede834f14872921d087250d9f0c0aaa',
      'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip':'32ac4f3938ea0659216e1fae61a6ad6463ed2091c8470a0af5db360a686e1e9c',
      'dist/TinyToon12_NES_Korean_TechnicalGuide_20261009.zip':'bf23e6ccfc8a6e2ea21794bf0c4031bef6868e5dbdef6a47ab814101d7756c50'}
    for relative,digest in expected.items():assert sha(R/relative)==digest,relative
    old_public_count=0
    for work in (225,227):
        m=json.loads((R/f'manifests/nonplay{work}_assets.json').read_text('utf-8'))
        for relative,digest in m['files'].items():
            if relative.startswith('workspace/publication/'):
                assert sha(R/relative)==digest,relative;old_public_count+=1
    return {'protected_hashes':expected,'previous_frozen_publication_assets_verified':old_public_count}

def seal_folder(folder):
    files=sorted(p for p in folder.rglob('*') if p.is_file())
    assert all(p.suffix.lower() in ('.txt','.md','.html','.png','.json','.py') for p in files)
    for p in files:
        assert not p.is_symlink() and not p.read_bytes().startswith(b'NES\x1a'),p
        if p.suffix in ('.txt','.md','.html','.json'):
            text=p.read_text('utf-8-sig');text=re.sub(r'data:image/png;base64,[^"\s]+','[embedded PNG]',text)
            text=re.sub(r'\b[0-9a-f]{64}\b','[SHA256]',text)
            assert not re.search(r'(?<!\d)(?:003|049|050|051|053|055|062)(?!\d)|_\d{3}\b|작업\s*\d{3}',text),p
            assert '\ufffd' not in text,p
    hashes={p.relative_to(folder).as_posix():sha(p) for p in files}
    (folder/'SHA256.txt').write_text(''.join(digest+'  '+relative+'\n' for relative,digest in hashes.items()),'utf-8')
    files=sorted(p for p in folder.rglob('*') if p.is_file())
    target=R/'dist'/(folder.name+'.zip');assert not target.exists()
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            item=zipfile.ZipInfo(p.relative_to(folder).as_posix(),date_time=(2026,10,9,0,0,0))
            item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16
            z.writestr(item,p.read_bytes(),compresslevel=9)
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert sorted(z.namelist())==sorted(p.relative_to(folder).as_posix() for p in files)
        for p in files:assert z.read(p.relative_to(folder).as_posix())==p.read_bytes()
    digest=sha(target);hashpath=Path(str(target)+'.sha256');hashpath.write_text(digest+'  '+target.name+'\n','utf-8')
    return {'path':target.relative_to(R).as_posix(),'sha256':digest,'files':len(files),'ROM_free':True},files+[target,hashpath]

def main():
    doc=R/'docs/PUBLIC_ARTICLE_READER_REVISION_228.md';manifest=R/'manifests/nonplay228_assets.json'
    assert not doc.exists() and not manifest.exists()
    protected=verify_protected()
    evidence=json.loads((R/'qa/reports/publication228_sources.json').read_text('utf-8'))
    for figure in evidence['figures']:
        assert sha(WORKLOG/figure['image'])==figure['image_sha256']
        for source in figure['sources']:assert sha(R/source['path'])==source['sha256']
    page=(WORKLOG/'작업기.html').read_text('utf-8')
    embedded=re.findall(r'<img src="data:image/png;base64,([^" ]+)',page);assert len(embedded)==8
    for n,encoded in enumerate(embedded,1):assert base64.b64decode(encoded)==(WORKLOG/f'images/{n:02d}.png').read_bytes()
    page_report=json.loads((R/'qa/reports/technical228_page.json').read_text('utf-8'));assert page_report['normalized_body_equal']
    render=[]
    for path in ('reader228_worklog','reader228_guide'):
        report=json.loads((R/'qa/publication'/path/'render_report.json').read_text('utf-8'));assert report['status']=='PASS'
        assert not (R/'qa/publication'/path/'browser_profile').exists();render.append(report)
    assert sha(GUIDE/'examples_nes.py')==sha(R/'workspace/publication/TinyToon12_TechnicalGuide_20261009/examples_nes.py')
    packs=[];assets=[]
    for folder in (WORKLOG,GUIDE):
        pack,files=seal_folder(folder);packs.append(pack);assets.extend(files)
    assert packs[0]['files']==14 and packs[1]['files']==8
    verified={'work':228,'status':'PASS','scope':'Public prose, captions, labels, reader and posting ZIPs only',
      'reader_build_numbers_removed':True,'numbers_retained':['font metrics','hardware addresses','scope counts','release versions','SHA256','image ordering'],
      'new_game_execution':False,'new_game_build':False,'new_patch_apply':False,'cafe_posted':False,
      'raw_game_capture_sources_unchanged':True,'public_source_paths_removed':True,
      'user_first_playthrough':'COMPLETED_USER_REPORTED','post_release_QA':'PLANNED',
      'render':render,'native_page':page_report,'packages':packs,**protected}
    report_path=R/'qa/reports/publication228_verified.json';report_path.write_text(json.dumps(verified,ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''## 변경 범위

공개 작업기에서 내부 빌드·작업 번호를 제거하고 타이틀 제작, 출력기 조사, 티켓 교환 오류, HUD·움직이는 정지, 11px 확대, 검증과 배포 순서로 본문을 다시 썼다. 비교 그림8개는 보호된 실제 캡처·제작 원천·정적 복원에서 다시 구성하고 제목·부제·라벨·캡션을 수정 전/후 또는 목적 이름으로 바꿨다. 원래 게임 캡처 픽셀은 수정하지 않았다.

1·2편 기술 지침의 후보번호·번호 포함 빌더 명령·내부 문서 파일명도 독자에게 필요한 설명과 최신 인계 조회 방법으로 바꿨다. 주소·폰트 크기·문단 수·공식 릴리즈 버전·SHA는 기술 근거로 보존했다. Page는 해시를 지킨6개 블록 패치를 적용하고 전체 저장 본문120블록을 로컬 원천과 공백 정규화 대조했다. 교육 코드와 설명도는 동일하다.

## 독자용 산출물

- [수정 작업기 HTML](../{WORKLOG.relative_to(R).as_posix()}/작업기.html), [카페 본문](../{WORKLOG.relative_to(R).as_posix()}/카페_복사용_본문.txt)
- [작업기 ZIP](../{packs[0]['path']}), SHA `{packs[0]['sha256']}` — ROM없음,14파일.
- [기술 지침 Page]({PAGE}), [기술 지침 HTML](../{GUIDE.relative_to(R).as_posix()}/기술_지침.html)
- [기술 지침 ZIP](../{packs[1]['path']}), SHA `{packs[1]['sha256']}` — ROM없음,8파일.

## 검증 구분

정적: 공개 TXT/MD/HTML(내장이미지 제외)/JSON에서 내부 빌드·작업 번호와 번호 있는 문서/스크립트 참조가 없는지 검사했다. 공개 출처 JSON에 원천 경로·내부 빌드ID는 넣지 않았으며 비공개 원천 보고서에는 경로·해시를 유지했다. HTML내장8PNG와 파일PNG가 같은 바이트이고 ZIP CRC·목록·모든 추출 바이트가 원천 파일과 같다.

문서 시각·UI: 두 HTML을 격리 headless Edge로1280×1000 및390×844에서 렌더했다. 이미지8개/설명도2개 로드, 본문 잘림·가로넘침 없음, 작업기 확대와Escape닫기, 기술 지침 목차 이동을 확인했다. 그림8개와 각PC·모바일 첫화면을 직접 확인했다. native Page의 실제 미리보기는 사용할 수 없어 저장 Markdown 대조만 확인했고 로컬HTML의 시각 확인과 구분했다.

게임: 새 빌드·에뮬레이터·CPU·패치 적용·자연 플레이를 실행하지 않았다. 기존 사용자 실제 화면·완주1차 완료 보고와 배포 후 추가 검증 예정 상태를 그대로 유지했다. 과거 실제 캡처와 크레딧 정적 복원을 구분했다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT의 원문 유지 결정은 같다.

보존: 원본2편·CSV·최종로컬ROM·최종게임배포ZIP 및 이전 두 게시자료ZIP 해시가 같다. 이전 봉인 공개 파일{protected['previous_frozen_publication_assets_verified']}개를 manifest SHA와 대조했다. 1편 파일은 읽기참조하며 수정·빌드·복원을 하지 않았다. 현재 작업의 격리 렌더 프로필2개만 명시적 절대경로 검증 후 삭제했다. 최초 인라인 삭제 호출은 정책차단되어 실행되지 않았고, 삭제범위를 고정한 검사 스크립트는 승인·완료됐다.

## 재현과 근거

`scripts/publication228_reader_revision.py`는 새 출력폴더를 요구한다. 기존 봉인 폴더에 재실행하지 않는다. `scripts/build_technical_guide228.py`는 새 기술지침 리더를 생성한다. 원천·변환은 `qa/reports/publication228_sources.json`, Page 대조는 `technical228_page.json`, 전체 검증은 `publication228_verified.json`, 캐시삭제는 `publication228_cache_cleanup.json`과 현재 manifest를 따른다.

리더 재검사(기존QA를 덮어쓰지 않는 새 경로 사용):

```powershell
python -B scripts/render_publication221.py --input workspace/publication/TinyToon2_KR_Worklog_Reader_20261009/작업기.html --output qa/publication/reader_revision_recheck
python -B scripts/render_technical227.py --input workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html --output qa/publication/guide_revision_recheck
```

모든 해시와 변경파일 목록은 `manifests/nonplay228_assets.json`에 보관한다. 실제 카페 게시는 수행하지 않았다.

다음 작업 하나: {NEXT}
'''
    doc.write_text('# 공개 작업기·기술 지침 독자용 개정 — 2026-10-09\n\n'+body,'utf-8')
    entry=f'\n\n## 공개 작업기·기술 지침 독자용 개정 — 작업228\n\n내부 빌드 번호를 본문·비교 이미지·캡션·공개 출처에서 제거했다. 목적과 수정 전/후로 다시 설명했으며 두 리더의PC/모바일·ZIP검사가 통과했다. 게임 배포·번역·사용자1차 검수 상태는 같다. [상세 변경·해시·검증]({doc.name}).\n\n다음 작업 하나: {NEXT}\n'
    for name in ('HANDOFF_2026-10-09.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md'):
        p=R/'docs'/name;text=p.read_text('utf-8')
        if name=='LOCALIZATION_WORK_PLAN.md':text=re.sub(r'^> \*\*.*?\*\*','> **2026-10-09 공개 작업기·기술 지침 개정 완료. 최종 릴리즈와 사용자1차 검수 상태 유지.**',text,count=1)
        p.write_text(text+entry,'utf-8')
    p=R/'docs/journal/2026-10-09.md';p.write_text(p.read_text('utf-8')+entry.replace('('+doc.name+')','(../'+doc.name+')'),'utf-8')
    replacements={
      'dist/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009.zip':packs[0]['path'],
      'workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009/':WORKLOG.relative_to(R).as_posix()+'/',
      'dist/TinyToon12_NES_Korean_TechnicalGuide_20261009.zip':packs[1]['path']}
    for p in (R/'README.md',R/'docs/HANDOFF.md'):
        text=p.read_text('utf-8')
        for a,b in replacements.items():text=text.replace(a,b,1)
        if p.name=='HANDOFF.md':
            text=re.sub(r'^# .*?\n','# 최종 배포 유지 및 공개 작업기 개정 완료 — 2026-10-09\n',text,count=1)
            text=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+NEXT+'**',text,count=1)
        prefix=f'> 공개용 최신본: [작업기]({"../" if p.name=="HANDOFF.md" else ""}{WORKLOG.relative_to(R).as_posix()}/작업기.html) · [1·2편 기술 지침]({PAGE}). 내부 빌드 번호를 제거하고 수정 원인과 결과 중심으로 다시 썼다.\n\n'
        local_entry=entry if p.name=='HANDOFF.md' else entry.replace('('+doc.name+')','(docs/'+doc.name+')')
        p.write_text(prefix+text+local_entry,'utf-8')
    for path in ('reader228_worklog','reader228_guide'):assets.extend(p for p in (R/'qa/publication'/path).rglob('*') if p.is_file())
    assets.extend(R/x for x in ('scripts/publication228_reader_revision.py','scripts/build_technical_guide228.py','scripts/cleanup_publication228.ps1','scripts/seal_publication228.py',
      'qa/reports/publication228_sources.json','qa/reports/technical228_replacements.json','qa/reports/technical228_generation.json','qa/reports/technical228_page.json','qa/reports/publication228_cache_cleanup.json'))
    assets.extend([report_path,doc]);manifest.write_text(json.dumps({'work':228,'files':{p.relative_to(R).as_posix():sha(p) for p in sorted(set(assets))}},ensure_ascii=False,indent=2)+'\n','utf-8')
    verify_protected()
    print(json.dumps({'status':'SEALED_PASS','packages':packs,'handoff':doc.relative_to(R).as_posix()},ensure_ascii=False))

if __name__=='__main__':main()
