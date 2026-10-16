"""Verify embedded evidence and seal the167 browser-reviewed private package."""
from pathlib import Path
from html.parser import HTMLParser
import base64, csv, hashlib, json, zipfile
from seal_nonplay166 import R, sha, seal

class Images(HTMLParser):
    def __init__(self): super().__init__(); self.sources=[]
    def handle_starttag(self,tag,attrs):
        if tag=='img': self.sources.append(dict(attrs)['src'])

def main():
    out=R/'workspace/review/nonplay049_20261007_167'
    archive=R/'workspace/review/TinyToon2_Nonplay_Review_049_20261007.zip'
    render=R/'qa/review/nonplay049_167_render_v2'
    report=R/'qa/reports/nonplay167_final.json';assert not report.exists()
    records=json.loads((out/'review_records.json').read_text('utf-8'))
    mf=json.loads((out/'artifact_manifest.json').read_text('utf-8'))
    for f,h in mf['files'].items(): assert sha(out/f)==h
    imgs=Images();imgs.feed((out/'review.html').read_text('utf-8'));assert len(imgs.sources)==25
    evidence=records['actual_images']+records['static_source_images'];assert len(evidence)==25
    for src,entry in zip(imgs.sources,evidence):
        assert src.startswith('data:image/png;base64,')
        assert hashlib.sha256(base64.b64decode(src.split(',',1)[1],validate=True)).hexdigest()==entry['sha256']==sha(R/entry['path'])
    rows={r['entry_id']:r for r in csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline=''))}
    for u in records['units']:
        for k in ['translation_ko','status','source_tokens','raw_sha256']:assert u[k]==rows[u['entry_id']][k]
    assert len(records['units'])==54 and len(records['graphics'])==33
    assert len(records['outside_registered_candidates'])==7 and all(i['decision']=='pending'and not i['human_approved']for i in records['outside_registered_candidates'])
    decisions=json.loads((out/'decisions_template.json').read_text('utf-8'))
    assert not decisions['human_approved']and all(i['decision']=='pending'for i in decisions['outside_candidates'])
    ui=json.loads((render/'render_report.json').read_text('utf-8'));assert ui['status']=='PASS'
    with zipfile.ZipFile(archive)as z:
        assert z.testzip()is None and len(z.namelist())==7
        for p in out.iterdir():assert z.read(out.name+'/'+p.name)==p.read_bytes()
    result={'work':167,'status':'PASS_PRIVATE_RECORDS_EMBEDDED_EVIDENCE_BROWSER_ZIP',
        'archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'ROM_free':True,
        'SSOT54_units_exact':True,'graphics33_preserved':True,'outside_candidates7_pending':True,
        'embedded_PNGs_hash_exact':25,'reused_actual_images':21,'static_source_images':4,
        'browser_UI_report':(render/'render_report.json').relative_to(R).as_posix(),'browser_UI_report_sha256':sha(render/'render_report.json'),
        'direct_browser_document_visuals':['desktop_top.png','mobile_candidate_pause.png'],
        'render_v1_failed':True,'render_v1_failure_preserved':'qa/reports/nonplay167_render_v1_failure.json',
        'ROM_sha256':records['ROM_sha256'],'SSOT_sha256':records['SSOT_sha256'],
        'actual_play_owner':'user','new_game_execution':False,'human_approved':False,'release_eligible':False}
    report.write_text(json.dumps(result,indent=2)+'\n','utf-8')
    body=f'''現在049の [비플레이 검토 HTML](../{out.relative_to(R).as_posix()}/review.html)와 [ROM 없는 ZIP](../{archive.relative_to(R).as_posix()})를 작성했다. 기존131 자료와 이전104 소비 보충 자료는 그대로 보존했다. 새 묶음은 등록54원천/33그림, 미연결7후보, 21기존 실제 PNG 및4정적 원본CHR 페이지를 포함한다. 실제 PNG21장은 이전 기록을 재사용한 것으로 이번에 게임을 새로 실행한 자료가 아니다.4타일 아틀라스에는 정적 자료 표기를 붙여 게임 장면과 구분했다.

저장상태/리셋을 미완료로 적었던 옛 검토 본문을 작업133의 제한된049 상태복원/리셋 후 재입장 검증으로 갱신했다. 모든 저장상태나 이전빌드 호환성으로 확대하지 않는다. 사용자 플레이 소유권, 38cycle page/idle 난수·CPU 차이, 작업163 PNG4410의7326픽셀 차이/전체RGB FAIL을 명시했다. 문구·이름·생성형 그림·원문 보존 범위 승인과 전역 원천 완결성은 보류다. 빈 JSON 응답 양식은 승인이 아니다.

[최종 검증 보고](../{report.relative_to(R).as_posix()}):54원천의 번역·토큰·상태·원천SHA와33그림 보존, HTML에 내장된25PNG 각각의 원본SHA, ZIP7파일/CRC/내용 동일성 PASS. [브라우저 보고](../{render.relative_to(R).as_posix()}/render_report.json)는 PC1280/모바일390에서 넘침없음·검색·상세열기·이미지로드·크레딧 표시3건·후보7건을 확인했다. PC상단/모바일PAUSE 후보의 문서 렌더를 직접 보았다. 첫 render167은 새 한국어 검증 문자열의 PowerShell 파이프 인코딩 때문에 실패했다. 스크립트·실패출력·보고를 보존하고UTF8을 명시한v2가 통과했다. 검토HTML/ROM 내용의 결함은 아니었으며 실패를 삭제하지 않았다.

ZIP SHA `{sha(archive)}`. ROM `{records['ROM_sha256']}`, CSV `{records['SSOT_sha256']}` 불변. 재현 생성: `python scripts/make_nonplay_review167.py`; 브라우저 검사: `python scripts/render_nonplay167_v2.py --input workspace/review/nonplay049_20261007_167/review.html --output qa/review/nonplay049_167_render_v2`; 봉인: `python scripts/seal_nonplay167.py`. 모든 출력은 덮어쓰기 보호이며 기존 증거를 재실행으로 덮지 않는다. 신규 정적/패키지·문서 브라우저 검증만 수행했다. 신규ROM빌드/적용/게임런타임/플레이/청음/사람최종검수 없음. 변경과 사용 근거의SHA는manifest에 고정했다.'''.replace('現在049の','현재049의')
    files=[report,Path(__file__),R/'scripts/make_nonplay_review167.py',R/'scripts/render_nonplay167.py',R/'scripts/render_nonplay167_v2.py',
        R/'qa/reports/nonplay167_render_v1_failure.json',R/'qa/reports/nonplay167_package.json',archive,
        R/'workspace/translation/nonplay_inventory049_166.json',R/'workspace/translation/coverage049_151.json',R/'qa/reports/state133_validation.json',
        R/'qa/reports/water163_hold_validation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv']
    files.extend(p for p in out.iterdir()if p.is_file())
    files.extend(p for p in render.iterdir()if p.is_file())
    files.extend(R/i['path']for i in evidence)
    failed=R/'qa/review/nonplay049_167_render';files.extend(p for p in failed.iterdir()if p.is_file())
    seal(167,'CURRENT049_NONPLAY_REVIEW_PACKAGE.md','현재049 비플레이 통합 검토 묶음',body,
        '54원천·33그림·후보7건, 기존실제21/정적4그림 통합.049 state/reset 근거·사용자 플레이 담당·163 RGB실패 표시. PC/모바일/ZIP PASS; ROM/CSV 불변.',
        '검수용049 적용 패키지에 최신 지원 범위·사용자 검수 안내·알려진 한계를 반영한 새 ROM 없는 묶음을 만들고 최종 ZIP의 실제 Windows 적용을 확인한다.',files)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
