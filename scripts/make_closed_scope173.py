"""Record the explicit remaining-three retention and refresh scope review; unchanged049."""
from pathlib import Path
import copy, html, json, zipfile
from seal_nonplay171 import R, sha

OUT = R/'workspace/review/nonplay049_20261008_173'

def main():
    primary=R/'workspace/translation/scope_decisions_20261008_173.json'
    invpath=R/'workspace/translation/nonplay_inventory049_173.json'
    archive=R/'workspace/review/TinyToon2_Nonplay_Review_049_Scope173_20261008.zip'
    report=R/'qa/reports/nonplay173_review_package.json'
    assert not any(p.exists() for p in [primary,invpath,OUT,archive,report])
    prior=R/'workspace/review/nonplay049_20261007_170'
    mf=json.loads((prior/'artifact_manifest.json').read_text('utf-8'))
    for f,h in mf['files'].items(): assert sha(prior/f)==h
    records=json.loads((prior/'review_records.json').read_text('utf-8'))
    inventory=json.loads((R/'workspace/translation/nonplay_inventory049_169.json').read_text('utf-8'))
    source169=R/'workspace/translation/scope_decisions_20261007_169.json'
    decision169=json.loads(source169.read_text('utf-8'))
    assert sha(source169)==inventory['scope_decisions_sha256']
    rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    ssot=R/'workspace/translation/text_ja.csv'
    assert sha(rom)==records['ROM_sha256']==inventory['ROM_sha256']
    assert sha(ssot)==records['SSOT_sha256']==inventory['SSOT_sha256']
    IDs=['RYO51_PAGE17','NT1C','DIAGNOSTIC_STAGE_SELECT']
    newdecision={'work':173,'date':'2026-10-08','approved_by':'user','source':'Explicit user reply to remaining-three scope question in this session',
        'question':'남은 RYO51(타이틀 타일의 서명 모양), NT1C(호출자 미연결 배경 데이터), STAGE SELECT(진단 UI 후보)도 이번 범위에서 원문 유지할까요?',
        'user_answer':'이번 범위에서는 원문 유지',
        'baseline_ROM_sha256':sha(rom),'baseline_SSOT_sha256':sha(ssot),'facts172_sha256':sha(R/'qa/reports/nonplay172_remaining_facts.json'),
        'decisions':[{'id':i,'decision':'preserve_original_for_this_scope','human_approved':True,'consumer_closed':False,'unused_proven':False} for i in IDs],
        'limits':['These three named source records only. They may remain original if a display exists.','Not global English policy, unused proof, whole-corpus closure, gameplay or final wording/art/distribution approval.'],
        'previous_retention_record':'workspace/translation/scope_decisions_20261007_169.json','previous_retention_sha256':sha(source169)}
    primary.write_text(json.dumps(newdecision,ensure_ascii=False,indent=2)+'\n','utf-8')
    for item in inventory['outside_registered_candidates']:
        if item['id'] in IDs:
            item.update(state='retained_by_explicit_scope',decision='preserve_original_for_this_scope',human_approved=True,
                scope_work_closed=True,decision_source=primary.relative_to(R).as_posix())
        if item['id']!='PUSH_START_PAGE0F':
            item['consumer_connected']=False
            item['proposal']='이번 한글화 범위에서 원문 유지 확정. 추가 번역하지 않음. 소비 미연결·미사용 미확정은 기술 사실로 유지.'
    summary={'discovery_records':7,'explicit_user_retention':6,'connected_existing_title_retention':1,
        'still_unresolved':[],'still_unresolved_count':0,'remaining_consumer_uncertainty':6,
        'limit':'Zero unresolved SCOPE decisions in these seven discovery records; six consumers remain unproven and whole-game corpus completeness is not established.'}
    inventory['work']=173;inventory['outside_population_summary']=summary
    inventory['scope_decision_sources']=[{'file':source169.relative_to(R).as_posix(),'sha256':sha(source169)},
        {'file':primary.relative_to(R).as_posix(),'sha256':sha(primary)}]
    inventory['scope_decisions_file']=primary.relative_to(R).as_posix();inventory['scope_decisions_sha256']=sha(primary)
    inventory['human_approved']=False;inventory['global_corpus_closed']=False
    invpath.write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n','utf-8')
    records['outside_registered_candidates']=copy.deepcopy(inventory['outside_registered_candidates'])
    records['outside_population_summary']=summary;records['scope_decisions_file']='scope_decisions.json'
    combined={'work':173,'baseline_ROM_sha256':sha(rom),'baseline_SSOT_sha256':sha(ssot),
        'artifact_policy':'Read-only projection of two explicit user decisions. No global/full review approval.',
        'sources':[{'file':'scope_decisions169.json','sha256':sha(source169),'IDs':['HOWTO','PAUSE','POW']},
            {'file':'scope_decisions173.json','sha256':sha(primary),'IDs':IDs}],
        'decisions':decision169['decisions']+newdecision['decisions'],'whole_language_art_play_approved':False}
    records['scope_decisions_sha256']=None # Set to the actual materialized file hash below.
    records['human_review_complete']=False
    records['limits']=[s for s in records['limits'] if not s.startswith('Discovery7:')]
    records['limits'].append('Discovery7 scope decisions closed: six explicitly original-retained by user and one connected existing title prompt. Six consumer uncertainties and global corpus/final review remain unclosed; no unused proof.')
    records['technical_reports']['nonplay172_remaining_facts.json']=sha(R/'qa/reports/nonplay172_remaining_facts.json')
    source=(prior/'review.html').read_text('utf-8')
    source=source.replace('2026-10-07 범위 결정 반영170:', '2026-10-08 보존 범위 결정 반영173:')
    start=source.index('<h2 id="outside">');end=source.index('<h2>후보가 있는 원본 CHR 페이지',start)
    cards='<h2 id="outside">발견7건의 범위 결정 완료 ·173</h2><p>HOWTO·PAUSE·POW와 RYO51·NT1C·STAGE SELECT는 사용자가 이번 한글화 범위에서 원문 유지로 선택했습니다. 타이틀 PUSH START는 기존 보존 안내에 연결했습니다. 발견7건의 추가 번역 범위는 모두 정리됐지만, 실제 소비가 미확정인6건을 미사용으로 확정한 것은 아닙니다. 전체 원천 목록과 최종 말투·명칭·그림·플레이 검수는 별도입니다.</p>'
    oldby={d['id']:d for d in json.loads((prior/'review_records.json').read_text('utf-8'))['outside_registered_candidates']}
    for item in records['outside_registered_candidates']:
        old=oldby[item['id']];label='이번 범위 원문 유지 · 사용자 결정' if item['human_approved'] else '기존 타이틀 보존 안내 · 소비 연결'
        fact=old['review_fact_ko'];limit=old['review_limit_ko']
        cards+=f'<details class="candidate" data-state="{item["state"]}" id="{item["id"]}"><summary>{html.escape(item["id"])} · {html.escape(item["text"])} · {label}</summary><p>{fact}</p><p><strong>기술 한계:</strong> {limit}</p><p><strong>범위 결정:</strong> {html.escape(item["proposal"])}</p><p class="note">원천 보존 / 전역 미사용 확정 아님 / 전체 문구·그림·플레이 승인 아님</p></details>'
        item['review_fact_ko']=fact;item['review_limit_ko']=limit
    source=source[:start]+cards+source[end:]
    source=source.replace('scope_decisions.json은 HOWTO·PAUSE·POW의 명시적 원문 유지 결정입니다.',
        'scope_decisions.json은6개 원천의 명시적 원문 유지 결정을 모은 읽기 자료입니다. 원본 결정 기록169/173을 함께 보존했습니다.')
    source=source.replace('decisions_template.json은 나머지 문구·그림·범위 응답 양식이며 전체 승인 기록이 아닙니다.',
        'decisions_template.json은 나머지 문구·그림·플레이 응답 양식이며 전체 승인 기록이 아닙니다.')
    decisions=json.loads((prior/'decisions_template.json').read_text('utf-8'))
    decisions.update(work=173,outside_candidates=[],scope_decisions_file='scope_decisions.json',
        instructions='Named discovery scope decisions are closed by explicit user retention6 and established title preservation1. Wording/art and user gameplay remain pending; no automatic approval.')
    payload={p.name:p.read_bytes() for p in prior.iterdir() if p.is_file() and p.name!='artifact_manifest.json'}
    payload['scope_decisions169.json']=source169.read_bytes();payload['scope_decisions173.json']=primary.read_bytes()
    payload['scope_decisions.json']=(json.dumps(combined,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    records['scope_decisions_sha256']=__import__('hashlib').sha256(payload['scope_decisions.json']).hexdigest()
    for name,value in [('review_records.json',records),('decisions_template.json',decisions),('source_inventory.json',inventory)]:
        payload[name]=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    payload['review.html']=source.encode('utf-8')
    payload['README.txt']='타이니툰2 현재049 검토자료·보존 범위 반영173\n54원천(45초안/9기술공유)/33그림·기존실제21/정적4PNG. 발견7건=사용자원문유지6+기존타이틀보존연결1, 범위미결정0. 소비미확정6/전역원천·최종문구/그림/사용자플레이는미완료. 결정원본169/173과읽기용합본을보존했다. ROM/패치/폰트/에뮬레이터없음.\n'.encode('utf-8')
    payload['DECISIONS_PENDING.md']='''# 현재049 결정 상태 ·173

확정: HOWTO·PAUSE·POW(169), RYO51·NT1C·진단STAGE SELECT(173)는 이번 범위에서 원문 유지다. 타이틀 PUSH START는 기존 보존 범위다. 원본169/173 결정 파일과읽기용합본을보존했다. 전역미사용이나전체승인으로확대하지않는다.

여전히 필요: 본문45초안/그림33, 말투·이름·타이틀철자/생성형그림의 최종 판단과 사용자 실제플레이 결과. 전체 원천 목록 완결성/모든분기/실기/PCM은 미확인이다. 기술 소비 미확정6건은보존 결정을 뒤집지않으며 추가번역 잔여로세지않는다.

수정 양식: ID / 수정 전·후 / 이유 / 장면. 플레이 결과: 에뮬레이터·버전 / ROM SHA / 새게임·저장조건 / 진행·입력 / 관측 / 판정. decisions_template.json은응답용이며전체승인아님.
'''.encode('utf-8')
    OUT.mkdir()
    for f,b in payload.items():(OUT/f).write_bytes(b)
    (OUT/'artifact_manifest.json').write_text(json.dumps({'work':173,'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),'ROM_free':True,
        'user_approved_retention':6,'connected_title_retention':1,'unresolved_scope_decisions':0,
        'human_final_review':False,'files':{f:sha(OUT/f) for f in sorted(payload)}},indent=2)+'\n','utf-8')
    assert len(list(OUT.iterdir()))==10
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(OUT.iterdir()):z.write(p,OUT.name+'/'+p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist())==10
        for p in OUT.iterdir():assert z.read(OUT.name+'/'+p.name)==p.read_bytes()
    result={'work':173,'status':'PASS_SCOPE_RECORDS_ROMFREE_REVIEW_RENDER_PENDING',
        'archive':archive.relative_to(R).as_posix(),'archive_sha256':sha(archive),'review_directory':OUT.relative_to(R).as_posix(),
        'source_decisions':[{'path':source169.relative_to(R).as_posix(),'sha256':sha(source169)},{'path':primary.relative_to(R).as_posix(),'sha256':sha(primary)}],
        'scope_retention_user_approved':6,'connected_title_preserved':1,'unresolved_scope_decisions':0,
        'consumer_uncertainty_retained':6,'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),
        'new_game_execution':False,'human_final_review':False,'global_corpus_closed':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
