"""Publish a new private review snapshot with explicit three-graphic scope decisions."""
from pathlib import Path
import copy, html, json, re, zipfile
from seal_nonplay166 import R, sha

def main():
    old = R / 'workspace/review/nonplay049_20261007_167'
    out = R / 'workspace/review/nonplay049_20261007_170'
    archive = R / 'workspace/review/TinyToon2_Nonplay_Review_049_Scope170_20261007.zip'
    report = R / 'qa/reports/nonplay170_package.json'
    assert not any(p.exists() for p in [out, archive, report])
    mf = json.loads((old / 'artifact_manifest.json').read_text('utf-8'))
    for f, h in mf['files'].items(): assert sha(old / f) == h
    invpath = R / 'workspace/translation/nonplay_inventory049_169.json'
    inventory = json.loads(invpath.read_text('utf-8'))
    scopepath = R / inventory['scope_decisions_file']
    scope = json.loads(scopepath.read_text('utf-8'))
    assert sha(scopepath) == inventory['scope_decisions_sha256']
    assert scope['user_answer'] == '이번 범위에서는 원문 유지'
    records = json.loads((old / 'review_records.json').read_text('utf-8'))
    assert records['ROM_sha256'] == inventory['ROM_sha256'] and records['SSOT_sha256'] == inventory['SSOT_sha256']
    records['outside_registered_candidates'] = copy.deepcopy(inventory['outside_registered_candidates'])
    records['outside_population_summary'] = inventory['outside_population_summary']
    records['scope_decisions_file'] = 'scope_decisions.json'
    records['scope_decisions_sha256'] = sha(scopepath)
    records['human_review_complete'] = False
    records['limits'] = [v for v in records['limits'] if not v.startswith('Seven outside')]
    records['limits'].append('Discovery7: user-approved HOWTO/PAUSE/POW retention3; connected existing title PUSH START retention1; unlinked RYO51/NT1C/diagnostic3. No global-unused/corpus/final-wording approval.')
    records['technical_reports']['nonplay169_scope_title_consumer.json'] = sha(R / 'qa/reports/nonplay169_scope_title_consumer.json')
    source = (old / 'review.html').read_text('utf-8')
    start = source.index('<h2 id="outside">')
    end = source.index('<h2>후보가 있는 원본 CHR 페이지', start)
    parts = ['<h2 id="outside">등록 목록 밖의 발견 7건 · 결정 반영170</h2><p>사용자는 HOWTO·PAUSE·POW를 이번 한글화 범위에서 원문 유지로 선택했습니다. 이 세 범위 작업은 닫았습니다. 미사용 확정이나 전역 영어 보존 결정은 아닙니다. 별도 PUSH START 후보는 기존 타이틀의 시작 안내에 연결되어 중복 번역 대상에서 제외했습니다. RYO51·NT1C·진단 STAGE SELECT는 소비·의미가 미확정인 원천으로 보존했습니다. 전체 원천 완결성이나 최종 문장·그림 승인은 미완료입니다.</p>']
    labels = {'retained_by_explicit_scope':'이번 범위 원문 유지 · 사용자 결정',
              'connected_title_prompt_retained':'기존 타이틀 보존 안내 · 소비 연결',
              'preserved_unresolved':'원천 보존 · 소비/의미 미확정'}
    korean = {
        'HOWTO':('글자가 아닌 장식에는 이 뱅크가 실제로 사용됩니다. 조사한 놀이기구 안내 NT에는 HOWTO 글자 타일이 없었습니다.', '다른 글자 소비까지 미사용으로 확정하지 않습니다.'),
        'PAUSE':('조사한 일시정지/재개 경로와 제한된 폰트 공급에서는 이 글자 뱅크를 선택하지 않았습니다.', '다른 간접 공급·표시 경로의 전역 미사용 증명은 아닙니다.'),
        'POW':('같은 뱅크에는 깃발과 수상 놀이기구 줄 그림의 소비가 연결되어 있습니다. POW 글자는 그 소비와 구분합니다.', '효과 글자의 실제 소비는 미연결입니다. 이번 범위에서는 사용자의 선택으로 원문을 유지합니다.'),
        'PUSH_START_PAGE0F':('타이틀 초기화→CHR63→스프라이트8E→현재049의 기존 화면/PPU/OAM을 연결했습니다. 화면의 PUSH START가 이 원천입니다.', '이번에 게임을 실행하지 않았습니다. 종료된 작업130 자료와 현재 정적/한정 CPU 결과입니다.'),
        'RYO51_PAGE17':('원본 타이틀 타일의 마지막 행에 RYO51 모양이 있습니다. 타이틀 숫자2의 스프라이트와 선택한 실제 타이틀 OAM은 이 행을 사용하지 않습니다.', '타이틀 한 조건의 결과입니다. 작성자·다른 장면·전역 미사용 여부를 확정하지 않습니다.'),
        'NT1C':('99바이트의 압축 원천은1024 NT셀로 복원되며 현재049에 그대로 있습니다.', '실제 호출자와 표시할 폰트가 미연결입니다. 타일값만으로 문자/장식/미사용을 확정하지 않습니다.'),
        'DIAGNOSTIC_STAGE_SELECT':('별도 큐 프린터에서 STAGE SELECT / 1 0으로 읽히는 후보입니다. 일반 스테이지 초기화는 해당 호출자를 건너뜁니다.', '실제 표시 폰트·다른 계산 진입은 미확정입니다. 숨겨진 진단 UI를 켜거나 번역을 삽입하지 않았습니다.')}
    for item in records['outside_registered_candidates']:
        fact, limit = korean[item['id']]
        item['review_fact_ko'] = fact; item['review_limit_ko'] = limit
        if item['id'] in ['HOWTO', 'PAUSE', 'POW']:
            item['proposal'] = '이번 한글화 범위에서는 원문 유지로 확정. 추가 번역 작업 없음.'
        parts.append(f'<details class="candidate" data-state="{item["state"]}" id="{item["id"]}"><summary>{html.escape(item["id"])} · {html.escape(item["text"])} · {labels[item["state"]]}</summary><p>{fact}</p><p><strong>확인 한계:</strong> {limit}</p><p><strong>작업 제안:</strong> {html.escape(item["proposal"])}</p><p class="note">근거 작업: {", ".join(map(str,item["evidence_works"]))} / 현재049 원천 보존 / {"이번 범위 원문 유지 사용자 결정 기록 있음" if item["human_approved"] else "전체 최종 사람 승인 없음"}</p></details>')
    source = source[:start] + ''.join(parts) + source[end:]
    source = source.replace('2026-10-07 갱신:', '2026-10-07 범위 결정 반영170:')
    source = source.replace('미연결7후보', '발견7건(사용자보존3·타이틀연결1·미연결3)')
    source = source.replace('decisions_template.json은 응답용 빈 양식이며 승인 기록이 아닙니다.', 'scope_decisions.json은 HOWTO·PAUSE·POW의 명시적 원문 유지 결정입니다. decisions_template.json은 나머지 문구·그림·범위 응답 양식이며 전체 승인 기록이 아닙니다.')
    decisions = json.loads((old / 'decisions_template.json').read_text('utf-8'))
    decisions['work'] = 170
    decisions['scope_decisions_file'] = 'scope_decisions.json'
    decisions['outside_candidates'] = [v for v in decisions['outside_candidates'] if v['id'] in inventory['outside_population_summary']['still_unresolved']]
    decisions['instructions'] = 'Only three unresolved discovery records and final wording/art remain editable. Approved three-graphic retention is in scope_decisions.json; title prompt follows established title preservation.'
    pending = '''# 현재049 결정 기록 · 작업170

사용자 명시적 답변 ‘이번 범위에서는 원문 유지’를 HOWTO·PAUSE·POW의 현재 한글화 범위 결정으로 기록했다. scope_decisions.json이 근거다. 세 항목을 미사용 확정·전역 영어 보존·전체 문구/그림 승인으로 확대하지 않는다.

CHR0F PUSH START는 타이틀의 기존 보존 안내에 연결되었다. 새 번역 누락 건으로 중복 집계하지 않는다.

여전히 선택/확인이 필요한 사항:
- 본문45초안과 그림33문구, 이름·말투·타이틀 철자/그림의 최종 판단.
- RYO51, NT1C, 진단STAGE SELECT 원천의 미연결 소비/의미. 현재 원천 보존, 임의 삽입/활성화 없음.
- 실제 플레이는 사용자 담당. 결과를 장면/조건/재현순서와 함께 기록.

수정 응답: ID / 수정 전·후 / 이유 / 장면. JSON은 나머지 응답용이며 전체 승인 기록이 아니다.
'''
    payload = {p.name:p.read_bytes() for p in old.iterdir() if p.is_file() and p.name != 'artifact_manifest.json'}
    for name, value in [('review_records.json',records),('decisions_template.json',decisions),('source_inventory.json',inventory),('scope_decisions.json',scope)]:
        payload[name]=(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    payload['review.html']=source.encode('utf-8');payload['DECISIONS_PENDING.md']=pending.encode('utf-8')
    payload['README.txt']='타이니툰2 검토용049 · 범위 결정 반영170\nreview.html:54원천/33그림, 발견7(원문유지 사용자결정3/기존타이틀 연결1/미연결3). 기존실제21/정적4그림. 실제플레이 사용자담당. scope_decisions.json은HOWTO/PAUSE/POW 원문유지 답변 기록. 전체 문구·그림·플레이 승인 아님. ROM/패치/폰트/에뮬레이터 없음.\n'.encode('utf-8')
    out.mkdir()
    for f,b in payload.items(): (out/f).write_bytes(b)
    newmf={'work':170,'ROM_sha256':records['ROM_sha256'],'SSOT_sha256':records['SSOT_sha256'],'ROM_free':True,
        'human_review_complete':False,'explicit_retention_decisions':3,'unresolved_candidates':3,'files':{f:sha(out/f)for f in sorted(payload)}}
    (out/'artifact_manifest.json').write_text(json.dumps(newmf,indent=2)+'\n','utf-8')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(out.iterdir()): z.write(p,out.name+'/'+p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and len(z.namelist()) == 8
        for p in out.iterdir(): assert z.read(out.name+'/'+p.name) == p.read_bytes()
    result={'work':170,'status':'PASS_RECORDS_ROMFREE_ZIP_BROWSER_PENDING','archive':archive.relative_to(R).as_posix(),
        'archive_sha256':sha(archive),'ROM_sha256':records['ROM_sha256'],'SSOT_sha256':records['SSOT_sha256'],
        'user_approved_retention':3,'title_prompt_connected_retention':1,'unresolved_candidates':3,
        'human_final_review':False,'new_game_execution':False}
    report.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
