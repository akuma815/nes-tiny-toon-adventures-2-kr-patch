"""Consolidate current049 user-owned review and remaining release claims."""
from pathlib import Path
import json,re
from seal_nonplay171 import R,sha,seal

def main():
    out=R/'workspace/review/user049_20261008_175';assert not out.exists()
    report=R/'qa/reports/nonplay175_review_readiness.json';assert not report.exists()
    pkg=json.loads((R/'qa/reports/nonplay173_package.json').read_text('utf-8'))
    final=json.loads((R/'qa/reports/nonplay173_final.json').read_text('utf-8'))
    capture=json.loads((R/'qa/reports/nonplay174_capture_provenance.json').read_text('utf-8'))
    assert final['target_byte_exact'] and final['unresolved_scope_decisions']==0
    assert not capture['whole_prefix_RGB_equality_passed'] and not capture['exception_cause_closed']
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';ssot=R/'workspace/translation/text_ja.csv'
    assert sha(rom)==pkg['ROM_sha256']==final['ROM_sha256']==capture['ROM_sha256']
    assert sha(ssot)==pkg['SSOT_sha256']==final['SSOT_sha256']==capture['SSOT_sha256']
    archive=R/pkg['archive'];assert sha(archive)==pkg['archive_sha256']==final['archive_sha256']
    package=R/'dist'/archive.stem
    for f,h in pkg['contents_sha256'].items():assert sha(package/f)==h
    scope=R/'workspace/translation/nonplay_inventory049_173.json';inv=json.loads(scope.read_text('utf-8'))
    assert inv['outside_population_summary']['still_unresolved_count']==0
    coveragepath=R/'workspace/translation/coverage049_151.json';coverage=json.loads(coveragepath.read_text('utf-8'))
    assert coverage['ROM_sha256']==sha(rom) and coverage['CSV_sha256']==sha(ssot)
    cases=[
        ('TITLE','타이틀','철자·숫자2·리본·시작 입력·법적 표시와 생성형 그림의 최종 선택'),
        ('INTRO','도입/건너뛰기','출력 중 진행·페이지 대기·Start 건너뛰기·새게임 재진입·이름/말투'),
        ('HOME_BOOTH','홈/매표소','선택 안내·포인트 부족 MAIN_05794·교환·동적 숫자·소지 티켓·간판'),
        ('RIDE_NORMAL','일반 놀이기구','자연 수집 티켓의 부족/충족·실제 요금 차감·출발·재입장'),
        ('CASTLE','성/금티켓','자연 수집 금티켓/일반티켓 조건·부족/입장·방 전환·보스/엔딩'),
        ('HUD_MAP','HUD/지도/보너스','작은 글자·숫자·공유 타일·행 하단·보너스 결과'),
        ('TRAIN','기차','간판·정지·시간초과·다음라운드·보스 도전 안내와 출력 전환'),
        ('ALL_RIDES','각 놀이기구/보스','잘린 글자·남은 일본어/영어·진행 중 그림/숫자·결과 화면'),
        ('GAMEOVER','게임오버/이어하기','선택·다시 시작·글꼴 복귀·반복 진입'),
        ('CREDITS','자연 엔딩/크레딧','스크롤·역할명·인명·KONAMI·권리 표시, MAIN_05939/05999/059E7'),
        ('LIFETIME','정지/재개/리셋/상태복원','수행한 조건을 기록하고 글꼴·숫자 복귀와 세이브 지원 판단'),
        ('LANGUAGE_ART','최종 문구/이름/그림','현재54원천/33그림 자료에서 수정할ID·문구·이유 기록')]
    info={'work':175,'status':'READY_FOR_USER_REVIEW_NOT_FINAL_RELEASE','ROM_build':'dialogue_kr_poc_049',
        'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),'archive':pkg['archive'],'archive_sha256':sha(archive),
        'approved_retention':final['approved_retention'],'scope_unresolved_in_named_discovery7':0,
        'registered_units':54,'draft_prose':45,'technical_shared_units':9,'graphics':33,
        'existing_actual_reader_units':coverage['actual_reader_units'],
        'existing_all_line_NT_units':coverage['per_unit_all_line_NT_units'],
        'current049_reader_evidence_not_linked':coverage['actual_reader_not_yet_linked'],
        'confirmed_fix_required_from_checked_current_records':[],
        'user_actual_play_owner':True,'user_play_result_received':False,'human_final_wording_art_approved':False,
        'full_release_ready':False,'global_corpus_closed':False,'new_game_execution':False,
        'capture163_exception':{'pixels':7326,'whole_RGB_equality':False,'cause_closed':False,'offline174_complete':True},
        'bounds':['No confirmed new fix in the checked records is not proof of full-game absence of defects.',
            'Six explicit original-retention decisions close their additional translation scope only.',
            'Unlinked5 reader records are evidence gaps, not five untranslated prose sentences; MACRO82 is a technical/shared record.',
            'All-game corpus completeness and all scene/lifetime/audio/hardware coverage remain unproved.'],
        'next_action':'Attach user current049 scene/wording/art results, triage actual issues, then correct only affected sources and verify a new version if needed.'}
    template={'work':175,'ROM_sha256':sha(rom),'user_submitted':False,'emulator':None,'version':None,
        'game_start_or_state_condition':None,'scenes':[{'ID':i,'scene':s,'check':c,'decision':'not_reviewed','observation':None,'reproduction':None,'evidence_path':None} for i,s,c in cases],
        'wording_art_changes':[],'new_original_text_observations':[],
        'final_approval':{'wording':False,'names':False,'title_and_graphics':False,'play_scope':None,'distribution':False},
        'original_retention_scope_already_decided':final['approved_retention'],
        'instructions':'Blank private response template, not user evidence or approval. Do not reconfirm six named retention choices. Report only actually reviewed scenes/conditions.'}
    table='\n'.join('| '+i+' | '+s+' | '+c+' | 미검수 |' for i,s,c in cases)
    doc=f'''# 현재049 사용자 검수 연결표 ·175

현재 적용 묶음은 프로젝트 `dist/{archive.name}`이며 결과ROM SHA는 `{sha(rom)}`이다.173 ZIP은 실제 Windows 한글·공백 경로 적용에서499728바이트가 현재049와 일치했다. 이전049와 같은ROM이므로 이 문서 때문에 다시 적용할 필요는 없다. 새 게임으로 시작하고 다른 빌드 저장상태 호환성은 미확인으로 기록한다.

원문 유지 결정은 완료됐다: HOWTO·PAUSE·POW·RYO51·NT1C·진단 STAGE SELECT. 실제 표시가 있어도 이6건은 이번 범위의 번역 누락으로 세지 않는다. 타이틀 PUSH START는 기존 보존 안내다. 다른 새 문구를 발견하면 장면/입력과 함께 기록한다. 이 결정은 전체 문구/이름/그림 승인이나 전역 미사용 증명이 아니다.

검토HTML: 프로젝트 `workspace/review/nonplay049_20261008_173/review.html` 또는 적용 묶음의 `review/review.html`. 등록54원천은45본문초안+9기술/공유 단위, 그림33항목이다.9개 일본어 본문을 남겼다는 뜻이 아니다. 최종 문구/명칭/타이틀 철자·그림 선택을 실제 플레이와 함께 확인한다.

| ID | 장면 | 확인 항목 | 사용자 결과 |
|---|---|---|---|
{table}

결과 양식은 `result_template.json`이다. 검수한 항목만 통과/수정 필요로 바꾸고, 에뮬레이터/버전·결과ROM SHA·새게임/저장복원 조건·장면/스테이지·입력/재현순서·관측/기대결과·증거 파일 위치를 기록한다. 빈 양식은 승인이나 플레이 근거가 아니다. 문구 수정은 ID/수정전후/이유/장면을 적는다. 전체 완주를 하지 않았으면 검수한 구간만 기록한다.

최종 문체 쟁점의 기존 후보: MAIN_05805의 ‘도’, MAIN_05833 요청 강도, MAIN_05882 보스 도전 목적식 표현, MAIN_05999의 PACKAGE D. 역할 표기, 고유명사/말투/생성형 그림. 자동 일괄 치환하지 않았으며 현 초안이 검토 기준이다. 부족 안내 MAIN_0590C ‘아쉽지만 / 티켓이 부족해!’는049에서 수정·검증했다.

현재049 실제reader 근거가 연결된 등록원천은49/54이고 단위별 모든 줄 NT근거는29/54다. reader 미연결5는 MAIN_05794·크레딧 MAIN_05939/05999/059E7·기술macro MACRO_061C9(82)다. 역사빌드의 크레딧검증과 정적삽입근거가 있으나 이를 현재049 자연엔딩 근거로 바꾸지 않는다. 전체원천 목록의 완결성도 미확정이며 이번 발견7건의 범위 결정0잔여와 구분한다.

기술검증에서 확인된 새로운 수정 요구는 없다. 이는 확인한 원장/보고의 범위로, 전게임 결함 부재나 완료 선언이 아니다.163 PNG1장의7326픽셀 차이/전체RGB FAIL은174 오프라인 대조까지 완료했지만 정확한 원인은 기존자료로 확정하지 못했다.38cycles/page idle RNG/CPU/IRQ 차이와133의 한정 상태복원/리셋 지원범위도 유지한다. 새 자동플레이로 사용자 검수를 대체하지 않는다.

검수 후 순서: 실제 수정사항을 원천ID/재현장면에 연결 → 필요한 항목만 수정해 새 빌드/해시/회귀자료/ROM없는 적용묶음 생성 → 최종 문구·그림 및 검수/지원범위를 정리 → 완료된 범위에 맞춰 네이버 카페용 작업기와 공개용 자료 작성. 아직 전체/정식배포 완료가 아니며 외부 게시하지 않았다. 실기·PCM·모든 상태/분기 지원은 미수행 범위로 남긴다.
'''
    out.mkdir()
    (out/'USER_QA_KO.md').write_text(doc,'utf-8')
    (out/'result_template.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n','utf-8')
    (out/'readiness.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n','utf-8')
    (out/'artifact_manifest.json').write_text(json.dumps({'work':175,'ROM_free':True,'user_evidence_or_approval':False,
        'files':{p.name:sha(p) for p in sorted(out.iterdir())}},indent=2)+'\n','utf-8')
    report.write_text(json.dumps({**info,'private_review_return_directory':out.relative_to(R).as_posix(),
        'source_reports_sha256':{f:sha(R/f) for f in ['qa/reports/nonplay173_final.json','qa/reports/nonplay173_session.json',
            'qa/reports/nonplay174_capture_provenance.json','qa/reports/nonplay174_session.json',
            'workspace/translation/coverage049_151.json','workspace/translation/prose_review_125.json']}},ensure_ascii=False,indent=2)+'\n','utf-8')
    body=f'''[사용자 검수 연결표](../{out.relative_to(R).as_posix()}/USER_QA_KO.md), [빈 응답양식](../{out.relative_to(R).as_posix()}/result_template.json), [현재조건 보고](../qa/reports/nonplay175_review_readiness.json)를 작성했다. 기존173 적용묶음/검토자료와54/45/9/33, 사용자원문유지6/타이틀연결1/번역범위미결정0, 현재049 reader49/54·모든줄NT29/54·미연결5단위를 대조했다. 크레딧/포인트부족과 기술macro의 증거 공백을 번역 누락과 구분했고 마지막 판단이 필요한 말투/이름/생성형그림을 명시했다. 현재 확인한 원장/보고에서 새 수정 요구는 없지만 전역corpus/전게임 무결함/완료를 뜻하지 않는다.

173최종ZIP/내장23파일SHA와 ROM/CSV,174의PNG미해결 조건을 다시 읽어 현재성을 확인했다. 같은적용/렌더/런타임 검사는 반복하지 않았다.174 오프라인조사는완료했지만 PNG원인확정과전체RGBPASS는아니다. 사용자 실제플레이 결과나전체문구/그림 승인자료는 아직 없으며 빈양식이이를대신하지않는다. 사용자보존6건은재승인대상이아니다. 지원범위판단/실제수정→새버전회귀→완료범위의카페작업기 순서를기록했다.

변경:175검수연결표/양식/readiness/manifest·보고·생성기·인계/조사/계획/journal·README/canonical 최신진입점. 이전README/조사 상단의130시점 표시는현재175진입점으로갱신하고 아래역사기록을유지했다. ROM `{sha(rom)}`,CSV `{sha(ssot)}`,173ZIP `{sha(archive)}` 불변. 정적문서/파일SHA검증뿐이며 새ROM빌드/적용/CPU/브라우저/에뮬레이터/장면/플레이/청음/사람최종검수 없음. 카페완성글/외부게시없음.

재현 `python scripts/prepare_user_review175.py`; 감사 `python scripts/audit_project_links171_v2.py --manifest manifests/nonplay175_assets.json --output qa/reports/nonplay175_session.json`. 기존출력은보호하므로새경로의복제로재현한다. 파일별SHA는manifest다. 지금 독립적으로 진행할 확인된 수정은 없고 다음 입력은 사용자 검수 결과다. 한정원천/지원범위의한계를실제완료로추정하지않는다.'''
    files=[Path(__file__),report,scope,coveragepath,rom,ssot,archive,
        R/'qa/reports/nonplay173_package.json',R/'qa/reports/nonplay173_final.json',R/'qa/reports/nonplay173_session.json',
        R/'qa/reports/nonplay174_capture_provenance.json',R/'qa/reports/nonplay174_session.json',
        R/'workspace/translation/prose_review_125.json',R/'scripts/audit_project_links171_v2.py']
    files.extend(p for p in out.iterdir() if p.is_file())
    seal(175,'CURRENT049_USER_REVIEW_READINESS_175.md','현재049 사용자 검수 연결·잔여조건 정리',body,
        '검수표12항목/빈응답양식·최종판단/증거공백·수정→검증→카페작업기 순서정리. 확인한기록의새수정요구없음; 전체완료/전역corpus/사람승인아님.173ZIP/ROM/CSV불변.',
        '사용자의 현재049 실제 플레이 및 문구/명칭/그림 검수 결과를 받아 원천ID·재현장면에 연결하고 필요한 수정만 새 버전으로 검증한다.',files)
    p=R/'README.md';text=p.read_text('utf-8')
    text=re.sub(r'^> \*\*.*?\*\*', '> **2026-10-08 현재개발049 / 작업175 완료 / 사용자 검수 결과 대기.**',text,count=1)
    text=text.replace('# 현재 개발본 — 작업130 / 049','# 현재 개발본 — 작업175 / 049',1)
    marker='\n\n작업51 당시 채택043:'
    insert='\n\n최신 [ROM없는 적용ZIP173](dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008.zip), [문구/그림 검토173](workspace/review/nonplay049_20261008_173/review.html), [사용자 검수 연결표175](workspace/review/user049_20261008_175/USER_QA_KO.md). 원문유지6건의 사용자 결정과 기존타이틀연결1건을 반영했다. 발견7건의 추가번역 범위 미결정0, 실제 적용 결과는 기존049와 byte-exact다. 아래 번호별 기록은 역사자료다.'
    assert marker in text;text=text.replace(marker,insert+marker,1);p.write_text(text,'utf-8')
    p=R/'docs/SURVEY.md';text=p.read_text('utf-8')
    text=re.sub(r'^> \*\*.*?\*\*','> **2026-10-08 현재개발049 / 작업175 완료.**',text,count=1)
    marker='\n\n# 2편 조사 현황';text=text.replace(marker,'\n\n현재 기준은 [검수 연결/잔여조건175](CURRENT049_USER_REVIEW_READINESS_175.md), [보존6건/검토·적용173](CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md), [오프라인 캡처174](CURRENT049_OFFLINE_CAPTURE_PROVENANCE_174.md)다. 아래는각작업당시의구조/관측기록이다.'+marker,1);p.write_text(text,'utf-8')
    p=R/'docs/LOCALIZATION_WORK_PLAN.md';text=p.read_text('utf-8')
    marker='\n\n# 2편 한글화 작업 계획'
    text=text.replace(marker,'\n\n현재175: [사용자 검수 연결/남은 조건](CURRENT049_USER_REVIEW_READINESS_175.md).45본문초안/9기술공유·33그림이현재049에삽입됐다. 사용자보존6건과기존타이틀연결1건은173에반영했다. 새자동플레이는하지않고사용자결과의실제수정사항에따라새버전검증을진행한다. 아래계획·규모는작업당시기록이다.'+marker,1);p.write_text(text,'utf-8')
    p=R/'docs/HANDOFF.md';text=p.read_text('utf-8')
    marker='\n\n[작업107';text=text.replace(marker,'\n\n[최신 사용자 검수 연결표175](../workspace/review/user049_20261008_175/USER_QA_KO.md)와 [잔여조건175](CURRENT049_USER_REVIEW_READINESS_175.md)를 따른다. 확인한 기록에서 새 수정 요구는 없으며 사용자 플레이/최종 문구·명칭·그림 결과를 기다린다.173적용묶음과ROM/CSV는같다. 발견7건의범위결정완료를전역원천/전체게임완료로확대하지않는다.'+marker,1);p.write_text(text,'utf-8')
    print(json.dumps(info,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
