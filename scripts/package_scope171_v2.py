"""Package unchanged049 and approved scope169 plus exact review170 as a new artifact."""
from pathlib import Path
import copy, hashlib, json, zipfile
from seal_nonplay171 import R, sha

NAME = 'TinyToonAdventures2_KR_Review_049_Scope171_20261008'
OUT = R / 'dist' / NAME
ARCHIVE = OUT.with_name(NAME + '.zip')

def main():
    report = R / 'qa/reports/nonplay171_package.json'
    assert not any(p.exists() for p in [OUT, ARCHIVE, report])
    old = R / 'dist/TinyToonAdventures2_KR_Review_049_20261007'
    previous = json.loads((R / 'qa/reports/nonplay168_package.json').read_text('utf-8'))
    final = json.loads((R / 'qa/reports/nonplay168_final.json').read_text('utf-8'))
    assert final['status'] == 'PASS_ROMFREE_FINAL_ZIP_ACTUAL_WINDOWS_APPLY'
    assert sha(R / previous['archive']) == previous['archive_sha256'] == final['archive_sha256']
    for f, h in previous['contents_sha256'].items(): assert sha(old / f) == h
    review = R / 'workspace/review/nonplay049_20261007_170'
    mf = json.loads((review / 'artifact_manifest.json').read_text('utf-8'))
    for f, h in mf['files'].items(): assert sha(review / f) == h
    inventory = json.loads((R / 'workspace/translation/nonplay_inventory049_169.json').read_text('utf-8'))
    decision = R / inventory['scope_decisions_file']
    assert sha(decision) == inventory['scope_decisions_sha256']
    assert json.loads(decision.read_text('utf-8')) == json.loads((review / 'scope_decisions.json').read_text('utf-8'))
    records = json.loads((review / 'review_records.json').read_text('utf-8'))
    rom = R / 'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'
    ssot = R / 'workspace/translation/text_ja.csv'
    assert sha(rom) == previous['current049_ROM_sha256'] == records['ROM_sha256']
    assert sha(ssot) == previous['CSV_sha256'] == records['SSOT_sha256']
    assert sum(d['human_approved'] for d in records['outside_registered_candidates']) == 3
    assert records['outside_population_summary']['still_unresolved_count'] == 3
    data = {p.relative_to(old).as_posix():p.read_bytes() for p in old.rglob('*') if p.is_file() and not p.is_relative_to(old / 'review')}
    release = json.loads(data['release_report.json'])
    release.update(name=NAME, date='2026-10-08', version='0.1.0-review049-scope171', status='DEVELOPMENT_REVIEW',
        artifact_policy='Private review. Same049 ROM/patch/helpers/tools. Explicit retention169 and verified review170 synchronized.',
        actual_play_owner='user', distribution_eligible=False, global_corpus_closed=False)
    release['unperformed'] = ['user actual-play review', 'all branches', 'global corpus closure',
        'RYO51/NT1C/diagnostic STAGE SELECT consumers and meaning',
        'all reset/state contexts and crossbuild compatibility', 'hardware', 'PCM listening', 'final wording/names/art decisions']
    release['outside_candidates'] = [{k:d[k] for k in ['id', 'state', 'decision', 'human_approved']} for d in records['outside_registered_candidates']]
    release['outside_population_summary'] = records['outside_population_summary']
    release['scope_decision'] = {'file':'review/scope_decisions.json', 'sha256':sha(review / 'scope_decisions.json'),
        'authoritative_record':'workspace/translation/scope_decisions_20261007_169.json', 'authoritative_sha256':sha(decision), 'projection_JSON_exact':True,
        'approved_by':'user', 'answer':'이번 범위에서는 원문 유지', 'IDs':['HOWTO', 'PAUSE', 'POW'],
        'limit':'Three graphics only. No global unused/English policy or final language/art/play/release approval.'}
    release['private_review'] = {'directory':'review', 'source_work':170, 'registered_units':54, 'graphics':33,
        'discovery_records':7, 'user_retention':3, 'connected_title_retention':1, 'unresolved_candidates':3,
        'reused_actual_images':21, 'static_atlases':4, 'ROM_free':True, 'human_final_review':False,
        'source_manifest_sha256':sha(review / 'artifact_manifest.json')}
    release['previous_package_actual_apply168'] = {'report':'qa/reports/nonplay168_final.json',
        'sha256':sha(R / 'qa/reports/nonplay168_final.json'), 'scope':'Earlier package using identical patch/helpers/tools; not the final171 ZIP application.'}
    release['apply_verification']['scope'] = 'Historical132 eight checks. New171 ZIP application is verified after final packaging in qa/reports/nonplay171_final.json.'
    for f, scope in [('nonplay169_scope_title_consumer.json','Explicit three scope decisions and source/current049 title prompt connection.'),
                    ('nonplay170_final_stop.json','Review170 records/embedded evidence/browser/ZIP; prior session stop is historical, not current workflow state.')]:
        release['verification_reports'][Path(f).stem] = {'sha256':sha(R / 'qa/reports' / f), 'scope':scope}
    release['status_scope'] = 'Private package only. Final171 Windows apply report stored in qa/reports/nonplay171_final.json; no public distribution approval.'
    data['release_report.json'] = (json.dumps(release, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    data['RELEASE_NOTES_KO.md'] = '''# 타이니툰 어드벤처 2 — 검토용049 · 범위 결정 반영171

2026-10-08 사용자 검수용 ROM 없는 개발 패키지다. 현재049 ROM·차분 패치·적용 도구는 기존 검증본과 동일하다. 사용자 원문 유지 결정169과 PC/모바일 검증을 마친170 검토자료를 문서에 반영했다. 실제 플레이는 사용자 담당이며 전체 문구·그림·플레이·공개 배포 승인은 미완료다.

포함된 번역: 생성형 타이틀·지도·매표소·게임오버, 등록45본문 초안, HUD·보너스·매표소·기차 간판·시간초과·다음라운드·시작·정지 문구. 등록54원천은45초안과9기술/공유 단위다. 전체 게임 번역률이나 일본어9문장 미번역을 뜻하지 않는다. 그림33문구, 이름·말투·생성형 그림의 최종 선택은 별도다.

확정된 보존 범위: 사용자가 HOWTO·PAUSE·POW를 이번 한글화 범위에서 원문 유지로 선택했다. review/scope_decisions.json에 답변을 기록했다. 세 항목은 추가 번역 대상에서 제외하되 미사용으로 확정하지 않는다. 전역 영어 보존이나 전체 작업 승인으로 확대하지 않는다. CHR0F PUSH START는 기존 타이틀 시작 안내의 스프라이트8E/CHR63 소비에 연결되었으며 기존 타이틀 보존 범위를 따른다.

발견7건 = 이번 범위 원문 유지 확정3 + 기존 타이틀 보존 연결1 + 소비·의미 미확정3(RYO51, NT1C, 진단 STAGE SELECT). 미확정 원천은 그대로 보존했고 숨겨진 진단 UI를 활성화하지 않았다. 전역 원천 목록 완결성은 미확정이다.

049의 일반 티켓 부족 안내는 ‘아쉽지만 / 티켓이 부족해!’다. 전용226/227 폰트를 사용하고 공유196/197과macro 정의를 보존한다. native clear 이후에 새 폰트를 선택한다.048의 clear 전 폰트 교체 결함은 채택하지 않았으며 실패 자료를 보존했다.

기존 검증은 정적 계약·Expected Writes·독립 재빌드·실제IPS/Windows xdelta 적용과 조건을 명시한 대사/입장/타이틀 회귀다. 작업133은049 전용226 폰트의 상태복원과 한 번의 리셋 후 재입장을 검증했다. 모든 상태/리셋 조건·다른빌드 저장 호환성·전체 자연 플레이·실기·PCM청음을 검증한 것은 아니다. 이번171 작업은 게임을 실행하지 않는다.

알려진 한계: page당38cycles 추가로 idle 난수용 RAM22·CPU/일부IRQ 값이 달라진다. 전체CPU나 모든 게임 입력/난수 결과의 동일성을 주장하지 않는다.163의 frame04410.png는7326픽셀이 달랐고 원인은 미확정이다. 같은 구간 RAM/PPU/OAM/상태/매핑 일치를 전체RGB 동일성으로 확대하지 않는다.

review/review.html의21 실제게임 PNG는 기존자료 재사용이며14장은 역사빌드,7장은현재049다.4원본CHR 아틀라스는 정적자료로 구분했다.54원천·33그림·발견7건의 상태와 조건을 확인할 수 있다. review/decisions_template.json은 나머지 응답용이며 전체 승인이 아니다.

지원 원본·결과 SHA와 적용방법은 README_적용방법.txt와 release_report.json을 따른다. 사용자검수안내.txt·알려진한계.md를 함께 제공한다. ROM·폰트파일·에뮬레이터를 포함하지 않으며 도구/글꼴 라이선스를 보존했다. 네이버 카페 작업기는 전체 작업 완료 후 작성하며 외부 게시하지 않았다.
'''.encode('utf-8')
    readme = data['README_적용방법.txt'].decode('utf-8').replace('2026-10-07 문서 갱신', '2026-10-08 범위 결정 반영171')
    readme += '\nHOWTO·PAUSE·POW는 이번 범위에서 원문 유지로 확정됐습니다. review/scope_decisions.json은 그 답변 기록이며 전체 최종 승인은 아닙니다. 이 패키지는 최신170 검토자료를 포함합니다.\n'
    data['README_적용방법.txt'] = readme.encode('utf-8')
    guide = data['사용자검수안내.txt'].decode('utf-8')
    guide = guide.replace('후보 HOWTO/PAUSE/POW가 표시되면 장면과 입력을 기록합니다.',
        'HOWTO/PAUSE/POW는 승인된 원문 유지 대상입니다. 보이더라도 번역 누락으로 기록하지 않습니다. 그 외 새 문구는 장면과 입력을 기록합니다.')
    data['사용자검수안내.txt'] = guide.encode('utf-8')
    data['알려진한계.md'] = '''# 현재049 지원 범위와 알려진 한계 ·171

실제 플레이는 사용자 담당이다. 결과 ROM은 기존049와 동일하며 다른빌드 저장상태 호환성은 미확인이다. 새 게임으로 시작하고 적용안내의 원본/결과 SHA를 확인한다.

HOWTO·PAUSE·POW는 사용자 선택으로 이번 범위 원문 유지다. 소비 경로 미확정은 기술 상태로 남지만 추가 번역을 요구하는 미완료 항목으로 세지 않는다. 기존 타이틀 PUSH START의 소비는 연결되었으며 그대로 유지했다. RYO51/NT1C/진단STAGE SELECT는 표시·의미 미확정 원천이며 보존 중이다. 전역 원천 목록 완결성과 최종 말투·이름·그림 결정은 남는다.

049 helper의38cycles/page 추가에 따른 idle RNG/CPU/IRQ 차이와163의 한PNG7326픽셀 비교 실패/원인 미확정은 유지한다. 정적·빌드·실제적용·한정런타임·사용자플레이는 별도의 검증이다. 과거 실패나씨드/진단 결과를 자연완주로 표현하지 않는다.

133의 상태복원/리셋 재입장은 한정된049 환경에서 통과했다. 모든 상태·모든 에뮬레이터·이전빌드 세이브호환·실기·PCM 음질을 보장하지 않는다. 모든 플레이/분기 검수는 사용자 결과를 기다린다.

네이버 카페 글과 공개 배포 확정은 전체 작업 완료 후 진행한다. 이 묶음은 검토용이며 외부 게시/전체 최종 승인 기록이 아니다.
'''.encode('utf-8')
    for p in review.iterdir():
        if p.is_file(): data['review/' + p.name] = p.read_bytes()
    data.pop('SHA256.txt')
    data['SHA256.txt'] = ''.join(hashlib.sha256(b).hexdigest() + '  ' + f + '\n' for f, b in sorted(data.items())).encode('utf-8')
    assert len(data) == 21
    assert not any(Path(f).suffix.lower() in ['.nes','.rom','.bin','.ttf','.otf','.sav','.state'] for f in data)
    unchanged = ['apply.cmd','apply.ps1',release['patch']['file'],*release['tools']['files_sha256']]
    for f in unchanged: assert data[f] == (old / f).read_bytes()
    OUT.mkdir()
    for f, b in data.items():
        p = OUT / f; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
    with zipfile.ZipFile(ARCHIVE, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(data): z.write(OUT / f, NAME + '/' + f)
    with zipfile.ZipFile(ARCHIVE) as z:
        assert z.testzip() is None and len(z.namelist()) == 21
        for f, b in data.items(): assert z.read(NAME + '/' + f) == b
    ARCHIVE.with_name(ARCHIVE.name + '.sha256').write_text(sha(ARCHIVE) + '  ' + ARCHIVE.name + '\n', 'utf-8')
    result = {'work':171,'status':'PASS_ROMFREE_SCOPE_PACKAGE_FINAL_APPLY_PENDING','archive':ARCHIVE.relative_to(R).as_posix(),
        'archive_sha256':sha(ARCHIVE),'files':21,'ROM_free':True,'ROM_sha256':sha(rom),'SSOT_sha256':sha(ssot),
        'unchanged_binary_payload':unchanged,'exact_review170':True,'scope_169_approved_retention':3,
        'unresolved_candidates':3,'new_game_execution':False,'distribution_eligible':False,'human_final_review':False,
        'contents_sha256':{f:sha(OUT / f) for f in sorted(data)}}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2) + '\n','utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'contents_sha256'}, indent=2))

if __name__ == '__main__': main()
