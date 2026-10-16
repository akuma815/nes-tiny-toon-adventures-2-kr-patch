"""Seal updated user-reviewed Cafe article after desktop/mobile rendering."""
from pathlib import Path
import base64,json,re,zipfile
import seal_nonplay171 as records
from seal_nonplay171 import R,sha
from publication225_review_update import OUT,NAME,PATCH
records.DATE='2026-10-09'
render=R/'qa/publication/render225_final/render_report.json'
assert json.loads(render.read_text('utf-8'))['status']=='PASS'
report=R/'qa/reports/publication225_sources.json';q=json.loads(report.read_text('utf-8'))
source=(OUT/'작업기.html').read_text('utf-8');embedded=re.findall(r'<img src="data:image/png;base64,([^" ]+)"',source)
assert len(embedded)==8
for i,item in enumerate(q['figures']):
    assert item['index']==i+1 and base64.b64decode(embedded[i])==(OUT/item['image']).read_bytes()
    assert sha(OUT/item['image'])==item['image_sha256']
    for ref in item['sources']:assert sha(R/ref['path'])==ref['sha256']
plain=(OUT/'카페_복사용_본문.txt').read_text('utf-8-sig')
assert re.findall(r'\[이미지 (\d{2}) 삽입:',plain)==[f'{i:02d}' for i in range(1,9)]
assert PATCH in plain and '1차 검수를 마쳤습니다' in plain and '배포 이후 추가 검증' in plain
assert '미기록' not in plain
files=sorted(p for p in OUT.rglob('*') if p.is_file())
assert len(files)==13 and all(p.suffix in ('.txt','.md','.html','.png','.json') for p in files)
assert all('\ufffd' not in p.read_text('utf-8-sig') for p in files if p.suffix!='.png')
archive=R/'dist'/(NAME+'.zip');assert not archive.exists()
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,NAME+'/'+p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and len(z.namelist())==13
    for p in files:assert z.read(NAME+'/'+p.relative_to(OUT).as_posix())==p.read_bytes()
hashfile=Path(str(archive)+'.sha256');hashfile.write_text(f'{sha(archive).upper()}  {archive.name}\n','ascii')
evidence=R/'qa/reports/publication225_verified.json'
evidence.write_text(json.dumps({'work':225,'status':'PASS_UPDATED_USER_REVIEW_ARTICLE_RENDER_ZIP',
 'archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'files':13,'figures':8,
 'ROM_free':True,'CRC_payload_exact':True,'desktop_mobile_render':'PASS','image_zoom_escape':'PASS',
 'direct_updated_figure_and_render_review':True,'user_first_actual062_QA':'COMPLETED_USER_REPORTED',
 'post_distribution_QA':'REQUIRED_PLANNED','new_agent_game_execution':False,'cafe_uploaded':False,
 'contents_sha256':{p.relative_to(OUT).as_posix():sha(p) for p in files},
 'render_report':render.relative_to(R).as_posix()},ensure_ascii=False,indent=2)+'\n','utf-8')
body=f'''사용자062 실제 화면·완주1차 검수 완료 보고를 공개 본문·선두 안내·검증표·이미지08·업로드안내에 반영했다. 배포 이후 추가 검증 예정은 유지했다. [최종 작업기 ZIP](../dist/{archive.name}) SHA `{sha(archive)}`,13파일/8PNG/ROM없음. [오프라인 HTML](../{OUT.relative_to(R).as_posix()}/작업기.html), [카페 복사용 본문](../{OUT.relative_to(R).as_posix()}/카페_복사용_본문.txt).

이미지01/03/04/05/06은 과거 빌드의 실제 캡처,02는 제작 원천,07은062 정적 복원,08은 설명 표다. 새 완주 캡처를 만든 것으로 표기하지 않는다. 사용자 완료 보고는 [224 영수증](../qa/reports/user_review224.json)과 연결하고 이전221 당시 미기록 상태는 역사 근거로 유지한다. 공개 글은 사용자가 올릴 작업기 어조로1차 검수 완료를 썼다. 등록45문단을 전게임100%로 확대하지 않았고 원문 유지6원천도 명시했다.

UTF8·8마커 순서·내장PNG바이트·CRC·13파일 정확payload/ROM-free 통과. 격리 headless Edge 1280×1000 및390×844: 이미지8개 디코딩, 가로 넘침 없음, 확대/Escape 통과. 수정된08그림 및PC/모바일 선두 렌더를 직접 확인했다. [최종 검증](../qa/reports/publication225_verified.json), [렌더](../qa/publication/render225_final/render_report.json), [원천](../qa/reports/publication225_sources.json). 네이버카페 실제 게시나 배포 이후 게임 검증은 수행하지 않았다.

재현: python -B scripts/publication225_review_update.py, render_publication221.py --input <새HTML> --output <새QA경로>, seal_publication225.py. 고정 출력은 덮어쓰지 않으므로 새 경로를 지정한 복제에서 실행한다. 기존003 공개 원천은 이 갱신의 재현 입력으로 유지한다. 게임ROM과CSV는 수정하지 않았다.'''
records.seal(225,'NAVER_CAFE_FINAL_USER_REVIEW_225.md','사용자1차 검수 완료 반영 카페 작업기',body,
 '1차실화면·완주 완료/배포후검증예정 반영.8PNG·13파일ROMfree·desktop/mobile/zoom PASS.',
 '최종 배포 파일명을 명확히 정리하고 임시 적용 사본·렌더 캐시를 삭제한 뒤 최종 인계를 갱신한다.',
 [Path(__file__),R/'scripts/publication225_review_update.py',R/'scripts/render_publication221.py',
  evidence,report,render,archive,hashfile,*files,*[render.parent/n for n in ('desktop_top.png','desktop_bug_section.png','mobile_top.png','mobile_bug_section.png')]])
print(json.dumps({'status':'PASS','archive':archive.name,'sha256':sha(archive)},ensure_ascii=False))
