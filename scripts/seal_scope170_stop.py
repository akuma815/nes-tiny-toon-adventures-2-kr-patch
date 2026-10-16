"""Seal170 private scope review and the explicit session stop; no further project work."""
from pathlib import Path
import csv, json, zipfile
from seal_nonplay166 import R, sha, seal
from seal_nonplay167 import Images
import base64, hashlib, re

def main():
    out = R / 'workspace/review/nonplay049_20261007_170'
    archive = R / 'workspace/review/TinyToon2_Nonplay_Review_049_Scope170_20261007.zip'
    render = R / 'qa/review/nonplay049_170_render'
    report = R / 'qa/reports/nonplay170_final_stop.json'
    assert not report.exists()
    mf = json.loads((out / 'artifact_manifest.json').read_text('utf-8'))
    for f, h in mf['files'].items(): assert sha(out / f) == h
    records = json.loads((out / 'review_records.json').read_text('utf-8'))
    scope = json.loads((out / 'scope_decisions.json').read_text('utf-8'))
    assert scope['user_answer'] == '이번 범위에서는 원문 유지'
    assert [d['id'] for d in scope['decisions']] == ['HOWTO', 'PAUSE', 'POW']
    assert all(d['human_approved'] and not d['unused_proven'] for d in scope['decisions'])
    assert sum(d['human_approved'] for d in records['outside_registered_candidates']) == 3
    assert records['outside_population_summary']['still_unresolved_count'] == 3
    assert not records['human_review_complete']
    ssot = R / 'workspace/translation/text_ja.csv'
    rom = R / 'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    assert sha(rom) == records['ROM_sha256'] and sha(ssot) == records['SSOT_sha256']
    rows = {r['entry_id']:r for r in csv.DictReader(ssot.open(encoding='utf-8-sig', newline=''))}
    for u in records['units']:
        for k in ['translation_ko', 'status', 'source_tokens', 'raw_sha256']: assert u[k] == rows[u['entry_id']][k]
    parser = Images(); parser.feed((out / 'review.html').read_text('utf-8'))
    evidence = records['actual_images'] + records['static_source_images']; assert len(evidence) == len(parser.sources) == 25
    for src, img in zip(parser.sources, evidence):
        assert hashlib.sha256(base64.b64decode(src.split(',', 1)[1], validate=True)).hexdigest() == img['sha256'] == sha(R / img['path'])
    ui = json.loads((render / 'render_report.json').read_text('utf-8')); assert ui['status'] == 'PASS'
    assert ui['scope_states'].count('retained_by_explicit_scope') == 3
    assert ui['scope_states'].count('connected_title_prompt_retained') == 1
    assert ui['scope_states'].count('preserved_unresolved') == 3
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == 8
        for p in out.iterdir(): assert z.read(out.name + '/' + p.name) == p.read_bytes()
    result = {'work':170,'status':'PASS_PRIVATE_SCOPE_REVIEW_SESSION_STOPPED_BY_USER',
        'session_work_date':'2026-10-07','closing_handoff_date':'2026-10-08',
        'stop_instruction':'오늘은 마무리 하자','session_state':'stopped','auto_resume':False,
        'archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),
        'registered_units':54,'graphics':33,'user_approved_retention':3,'connected_title_retention':1,
        'still_unresolved_candidates':['RYO51_PAGE17','NT1C','DIAGNOSTIC_STAGE_SELECT'],
        'embedded25_images_hash_exact':True,'browser_PC_mobile_PASS':True,'ZIP8_files_exact':True,
        'direct_browser_visual':'qa/review/nonplay049_170_render/mobile_candidate_pause.png',
        'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),'new_game_execution':False,
        'human_final_review':False,'global_corpus_closed':False,'actual_play_owner':'user',
        'latest_apply_package':'dist/TinyToonAdventures2_KR_Review_049_20261007.zip',
        'latest_apply_package_scope_note':'168 package predates169 explicit retention. Patch/ROM is identical; latest170 review and169 decision record supersede pending wording in168 notes. Update a NEW package when user resumes.',
        'next_action_on_explicit_resume':'Create a new ROM-free review/apply package reflecting169 retention and170 review, preserving168 package, then verify its finalizedZIP Windows apply.'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    body = f'''사용자가 **‘오늘은 마무리 하자’**라고 지시했다. 새 소비 조사·번역·패키지 작업을 중단하고 진행 중인170 검토자료의 검증/인계만 마쳤다. **작업 중단 상태이며 사용자 재개 지시 전 자동으로 이어서 작업하지 않는다.** 실제 플레이 검수는 사용자 담당이다. 작업 묶음은2026-10-07 시작분이며 마감 중 시스템 날짜가2026-10-08로 바뀌어08인계/journal에도중단상태를기록했다. 날짜변경은재개지시가아니다.

오늘166..170 완료: (166)현재049 원천 두테이블54/그림33·원본CHR128/NT20/별도프린터12슬롯5원천 정적대조, (167)비플레이 검토자료/기존 실제21PNG와정적4아틀라스·PC/모바일/ZIP, (168)최신 지원한계/사용자 검수안내를 포함한20파일 ROM없는패키지와최종ZIP실제Windows적용 byte-exact, (169)사용자HOWTO·PAUSE·POW 이번범위원문유지확정 및 기존타이틀PUSH START sprite8E/CHR63 소비연결, (170)이결정을최신 검토자료에반영했다. 원본·1편·이전실패·현재ROM/CSV는보존했다.

[최신 비플레이 HTML](../{out.relative_to(R).as_posix()}/review.html), [최신 검토 ZIP](../{archive.relative_to(R).as_posix()}), [사용자 결정](../{out.relative_to(R).as_posix()}/scope_decisions.json), [최종 보고](../{report.relative_to(R).as_posix()}). 54원천·33그림 초안은SSOT와동일하다. 발견7건은명시적보존3+기존타이틀연결보존1+미연결3이다. 사용자답변을전역미사용/전체영문유지/전체문구·그림·배포승인으로확대하지않는다. RYO51·NT1C·진단STAGE SELECT는원천보존/소비·의미미확정. 전역corpus폐쇄·최종말투/명칭/그림·사용자플레이결과·실기/PCM은미완료이다.

170 검증:원본자료manifest/현재ROM·SSOT/54단위필드/사용자3결정·보류3/내장25PNG원본SHA/ZIP8파일CRC·내용 PASS. [브라우저 보고](../{render.relative_to(R).as_posix()}/render_report.json)는 PC1280/모바일390 표시·검색·상세열기·크레딧/25이미지·상태3+1+3을 확인했다. 모바일PAUSE ‘이번범위원문유지·사용자결정’ 렌더를 직접보았다. 신규게임런타임/플레이/빌드/적용/청음없음;170은문서브라우저검사다. 오늘168의실제적용은별도의보고에보존한다.167검증문자열인코딩·168호출인용실패와v2성공도보존했다.169의공백없는숫자/and에서SyntaxWarning이나왔지만CPU/정적검사는통과했으며사용된스크립트를덮어쓰지않았다.

검토ZIP SHA `{sha(archive)}`. ROM `{sha(rom)}`,CSV `{sha(ssot)}` 불변. 적용용 ZIP [168](../dist/TinyToonAdventures2_KR_Review_049_20261007.zip)의 SHA는 `0cc8deda78321640e0b95b9d4c00ef7d342c363e2e81fb4a9eedf6abc7b838af`이고 실제적용은PASS다. 단,168의문서/내장167자료는사용자보존답변 이전스냅샷이다. 최신170검토와169결정원장이우선하며범위결정반영적용묶음은아직만들지않았다. 패치/ROM내용은동일하여사용자플레이용049결과에는영향이없다.

변경:새170생성기/렌더기/봉인기·8파일검토묶음/ZIP·문서렌더QA/마감보고·날짜별인계/journal/canonical·manifest/audit. 사용SHA는manifest. 재현 생성`python scripts/refresh_scope_review170.py`;문서렌더`python scripts/render_scope170.py --input workspace/review/nonplay049_20261007_170/review.html --output qa/review/nonplay049_170_render`;마감`python scripts/seal_scope170_stop.py`(기존출력보호,이명령들은자동재개허가가아니다). 네이버카페완성작업기는전체완료뒤작성하며현재외부게시없음.'''
    files = [report, Path(__file__), R/'scripts/refresh_scope_review170.py', R/'scripts/render_scope170.py',
        R/'qa/reports/nonplay170_package.json', archive, rom, ssot,
        R/'workspace/translation/scope_decisions_20261007_169.json',R/'workspace/translation/nonplay_inventory049_169.json',
        R/'qa/reports/nonplay169_scope_title_consumer.json',R/'qa/reports/nonplay168_final.json',
        R/'dist/TinyToonAdventures2_KR_Review_049_20261007.zip',R/'scripts/seal_nonplay167.py']
    files.extend(p for p in out.iterdir() if p.is_file())
    files.extend(p for p in render.iterdir() if p.is_file())
    dated = R/'docs/HANDOFF_2026-10-08.md'
    journal = R/'docs/journal/2026-10-08.md'
    closing = '''\n\n## 작업170 — 전날 작업 마감·사용자 중단\n\n2026-10-07에 시작한166..170 비플레이 작업을 마감했다. 마감 중 환경 날짜가2026-10-08로 변경됐다. 사용자의 ‘오늘은 마무리 하자’ 지시를 유지하며 새 작업을 시작하지 않는다. 실제플레이 사용자담당/자동재개없음. 현재049 ROM·CSV불변. HOWTO/PAUSE/POW 이번범위원문유지 사용자결정 기록, PUSH START는기존타이틀소비에연결, RYO51/NT1C/진단STAGE SELECT는미확정원천보존.\n\n[170 상세 변경·SHA·검증 구분·잔여](SESSION_STOP_20261007_SCOPE_REVIEW.md), [현재 인계](HANDOFF.md).168적용패키지는실제Windows적용PASS이나169답변이전문서스냅샷이다. 최신170검토자료와169결정원장이우선이다.\n\n다음 작업 하나: 사용자가 명시적으로 재개하면169 보존결정과170검토자료를 새 ROM없는적용패키지에 반영하고 최종ZIP 실제Windows적용을 확인한다.\n'''
    dated.write_text((dated.read_text('utf-8') if dated.exists() else '# 인계 — 2026-10-08\n')+closing,'utf-8')
    journal.write_text((journal.read_text('utf-8') if journal.exists() else '# 작업 기록 — 2026-10-08\n')+closing.replace('(SESSION_STOP_', '(../SESSION_STOP_').replace('(HANDOFF.md)', '(../HANDOFF.md)'),'utf-8')
    seal(170,'SESSION_STOP_20261007_SCOPE_REVIEW.md','범위 결정 검토자료 갱신·오늘 작업 중단',body,
        '사용자 오늘마감으로중단·자동재개없음.최신170검토는HOWTO/PAUSE/POW 원문유지확정과PUSH START소비연결반영.PC/모바일/ZIP PASS.ROM/CSV불변.168적용묶음 범위문서갱신은재개후.',
        '사용자가 명시적으로 재개하면169 보존 결정과170 검토자료를 새 ROM 없는 적용 패키지에 반영하고 최종ZIP 실제Windows적용을 확인한다.',files)
    p=R/'docs/HANDOFF.md';text=p.read_text('utf-8')
    text=re.sub(r'^# .*?\n','# 작업 중단 — 2026-10-08 마감, 2026-10-07 시작분 작업170 완료\n',text,count=1)
    text=text.replace('2026-10-07 사용자의 “다시 진행”으로 재개했다.',
        '2026-10-07 사용자의 “오늘은 마무리 하자”로 작업을 중단했다. 사용자 재개 지시 전 자동 재개하지 않는다. 오늘166..170의 비플레이 작업을 마감했다.',1)
    text=text.replace('기존 사람 결정은pending/false이며 재개 지시는 최종번역/범위/배포 승인이 아니다.',
        'HOWTO·PAUSE·POW는 이번범위 원문유지로 사용자결정169에기록했다. 최신검토자료는170이다. 전체문구/그림/배포승인은미완료이며재개지시로자동승인하지않는다.',1)
    text=text.replace('자연 전체3구간완주/전역corpus/HOWTO·PAUSE·POW 남은소비경로/실기/PCM청음/사람문체·명칭·그림검토/정식배포가 남는다.',
        '실제플레이는사용자담당이다. 비플레이 잔여는168패키지문서의169/170반영, RYO51/NT1C/진단STAGE SELECT 소비·의미/전역corpus, 최종문체·명칭·그림검토와정식배포정리다. HOWTO·PAUSE·POW 번역추가는이번범위원문유지결정으로닫았다.',1)
    text=text.replace('검토자료는 [현재본문/그림049]',
        '최신170 [비플레이 검토HTML](../workspace/review/nonplay049_20261007_170/review.html)과 [오늘 마감](SESSION_STOP_20261007_SCOPE_REVIEW.md)을우선한다. 아래는각작업당시의역사자료다. 검토자료는 [현재본문/그림049]',1)
    p.write_text(text,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';text=p.read_text('utf-8')
    text=re.sub(r'^> \*\*.*?\*\*','> **2026-10-08 마감·전날 작업170 완료·사용자 요청으로 작업 중단. 명시적 재개 전 자동작업 없음. 실제 플레이 사용자 담당.**',text,count=1)
    p.write_text(text,'utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
