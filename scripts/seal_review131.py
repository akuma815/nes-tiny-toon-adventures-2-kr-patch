"""Independent offline reader verification and immutable work131 handoff."""
from pathlib import Path
import base64,csv,hashlib,json,re,zipfile
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'workspace/review/translation049_20261006'; report=R/'qa/reports/review049_validation131.json';manifest=R/'manifests/review049_131_assets.json'
 assert not report.exists() and not manifest.exists()
 x=json.loads((out/'review_records.json').read_text('utf-8')); m=json.loads((out/'artifact_manifest.json').read_text('utf-8')); html=(out/'review.html').read_text('utf-8')
 for n,h in m['files'].items():assert sha(out/n)==h
 rows={r['entry_id']:r for r in csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline=''))}
 assert len(x['units'])==len(rows)==54 and len(x['graphics'])==33
 for u in x['units']:
  for k in ['translation_ko','status','source_tokens','raw_sha256','source_sha256','reference_ids','original_view','notes']:assert u[k]==rows[u['entry_id']][k],(u['entry_id'],k)
 assert sum(u['status']=='draft' for u in x['units'])==45 and x['human_review_complete'] is False
 encoded=re.findall(r'src="data:image/png;base64,([^"]+)"',html);assert len(encoded)==len(x['actual_images'])==21
 for a,img in zip(encoded,x['actual_images']):assert base64.b64decode(a)==(R/img['path']).read_bytes() and sha(R/img['path'])==img['sha256']
 archive=R/'workspace/review/TinyToon2_Translation_Review_049_20261006.zip'
 assert sha(archive)=='1e002d06df87e939acfa7eece21646bbb775f4c630bdfa04e4177305505ef2b4'
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None and len(z.namelist())==5
  for p in out.iterdir():assert z.read(out.name+'/'+p.name)==p.read_bytes()
 renderdir=R/'qa/review/translation049_131';render=json.loads((renderdir/'render_report.json').read_text('utf-8'))
 assert render['status']=='PASS' and render['desktop']['allLoaded'] and render['desktop']['externalImages']==0 and render['mobile']['allParagraphsFit'] and render['mobile']['imagesFit'] and not render['javascript_errors']
 assert render['current049_shortage_text_and_provenance']['text']=='아쉽지만\n티켓이 부족해!'
 rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';csvpath=R/'workspace/translation/text_ja.csv'
 assert sha(rom)==x['ROM_sha256'] and sha(csvpath)==x['SSOT_sha256']
 direct=['desktop_shortage049.png','mobile_shortage049.png','mobile_top.png']
 result={'work':131,'status':'PASS','ROM_sha256':sha(rom),'SSOT_sha256':sha(csvpath),'archive_sha256':sha(archive),'ROM_free':True,'units_exact_current_SSOT':54,'graphics':33,'inline_images_byte_exact':21,'historical_images':14,'current049_images':7,'browser_render_report_sha256':sha(renderdir/'render_report.json'),'direct_reader_visuals':{n:sha(renderdir/n) for n in direct},'human_review_complete':False,'scope':'Offline review UI/package only. Game scenes inherited from frozen129/130, not new runtime, build or apply. No publication.'}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 nextaction='現在049のROMなし開発パッチを新しいdistフォルダへ作成し、日本語原本からWindows適用8検査と最終ZIP再適用を実行する。'.replace('現在049のROMなし開発パッチを新しいdistフォルダへ作成し、日本語原本からWindows適用8検査と最終ZIP再適用を実行する。','현재049 ROM 없는 개발 패치를 새 dist 폴더에 만들고 일본판 원본부터 Windows 적용8검사와 최종ZIP 재적용을 실행한다.')
 detail='''# 작업131 — 현재049 번역·그림 검토자료

[검토 HTML](../workspace/review/translation049_20261006/review.html), [ROM 없는 ZIP](../workspace/review/TinyToon2_Translation_Review_049_20261006.zip), [기록](../workspace/review/translation049_20261006/review_records.json), [최종 검증](../qa/reports/review049_validation131.json), [PC·모바일 렌더 검증](../qa/review/translation049_131/render_report.json).

등록54원천(45초안/9기술공유)과33그림 문구를 현재 CSV와 대조했다. MAIN_0590C만 ‘아쉽지만 / 티켓이 부족해!’로 바뀌었고 다른53원천의 번역은 이전 검토자료와 같다. raw/source/reference/status는 보존했다. macro를 펼친 일본어 보기는 표시용이며 원천 토큰을 고치지 않았다. MAIN_057AC/05920의 정확한 장면은105 보조 원장으로 표시하고 CSV의 역사 메모는 현재009 helper 근거와 구분했다.

실제PNG21장 중14장은043/045/046/047 역사 증거,7장은049의 타이틀·성 입구·부족 대사 부분출력/완성/지우기/다음 보유량·출발이다. 각 이미지의 ROM SHA, controller/초기 티켓seed 개입, 경로, SHA를 명시했다. 새로운 게임 실행 없이129/130 증거를 재사용했다. 최종 사람 승인false이며 등록 목록이 전역corpus나 전체완주를 증명하지 않는다.

정적·포장 검증: SSOT54개 모든 번역/상태/원천/메모 일치, 그림계획33개 기존SHA 확인, inline PNG21개 바이트 일치, ZIP5파일 무결성과 추출 바이트 일치. ROM/패치/폰트/에뮬레이터가 없다. ZIP SHA `1e002d06df87e939acfa7eece21646bbb775f4c630bdfa04e4177305505ef2b4`. ROM049 SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 그대로다.

표시 검증: 격리된 headless Edge에서1280/390폭,21이미지 decode,54검색 복원,단일ID검색/원천details,영문credits3항목 표시를 확인했다. JS오류0/외부이미지0/모바일문단·이미지넘침0. desktop_shortage049/mobile_shortage049/mobile_top 렌더PNG를 직접 읽어 문구·배치·출처가 읽히는지 확인했다. 이는 검토 웹페이지 표시 검증이며 게임장면 검증과 다르다. 신규build/apply/runtime/실기/청음은 수행하지 않았다.

변경 파일: scripts/make_review049_131.py,render_review049_131.py,seal_review131.py; 새검토폴더5파일/ZIP; qa/reports/review049_records131.json(생성 당시render pending 기록 보존)과 최종검증; qa/review/translation049_131의렌더8PNG/report; 정본 인계/조사/계획/README/오늘journal. 원본·1편·이전047검토자료 보존. 세부 SHA는 동결manifest에 기록한다. browser_profile 캐시는 검증자산에 넣지 않는다.

재현: `python scripts/make_review049_131.py`, `python scripts/render_review049_131.py --input workspace/review/translation049_20261006/review.html --output qa/review/translation049_131`, `python scripts/seal_review131.py`. 기존 출력이 있으면 거부하며 동결자료를 덮어쓰지 않는다. 검토는 HTML을 새 브라우저에서 여는 것으로 재확인할 수 있다.

한계: helper의 추가38cycles와 idleRNG/CPU차이, 자연전게임완주/모든분기/전역원천폐쇄/HOWTO·PAUSE·POW 실제소비/현재049 reset·savestate/실기/PCM/사람검토가 남았다. 정식배포·카페작업기·외부게시를 수행하지 않았다.

'''
 (R/'docs/TRANSLATION_REVIEW_049.md').write_text(detail+'다음 작업 하나: '+nextaction+'\n','utf-8')
 entry='\n\n## 작업131 — 현재049 검토자료 갱신\n\n54원천/33문구/21실제PNG(역사14/현재0497), 단일수정과장면105/개입출처 반영. ROM없는5파일ZIP 바이트·SSOT54 일치,PC1280/모바일390표시·검색·직접3렌더 확인. 현재ROM/CSV/원본/1편 보존, 신규게임실행없음/사람승인false.\n\n[상세 변경·SHA·검증 구분·재현·한계](TRANSLATION_REVIEW_049.md).\n\n다음 작업 하나: '+nextaction+'\n'
 for name in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/name;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(TRANSLATION_REVIEW_049.md)','(../TRANSLATION_REVIEW_049.md)'),'utf-8')
 p=R/'README.md';text=p.read_text('utf-8');text+='\n\n현재049 [검토자료131](docs/TRANSLATION_REVIEW_049.md): ROM없는ZIP·PC/모바일 검토 HTML 갱신. 사람최종승인false.\n';p.write_text(text,'utf-8')
 p=R/'docs/HANDOFF.md';text=p.read_text('utf-8').replace('작업130 이후','작업131 이후');text=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nextaction+'**',text,count=1);text=text.replace('[본문/그림047](TRANSLATION_REVIEW_047.md)','[현재본문/그림049](TRANSLATION_REVIEW_049.md), [역사047](TRANSLATION_REVIEW_047.md)');p.write_text(text+entry,'utf-8')
 files=[R/'scripts/make_review049_131.py',R/'scripts/render_review049_131.py',Path(__file__),report,R/'qa/reports/review049_records131.json',R/'docs/TRANSLATION_REVIEW_049.md',archive,rom,csvpath,*out.iterdir(),*(p for p in renderdir.iterdir() if p.is_file()),*(R/i['path'] for i in x['actual_images'])]
 manifest.write_text(json.dumps({'work':131,'files':{p.relative_to(R).as_posix():sha(p) for p in sorted(set(files))}},indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
