"""Canonical062 handoff, immutable197..212 evidence and honest current references."""
from pathlib import Path
import json
import re
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def check_links():
    count = 0
    expired = Path('C:/Users/akuma/.codex/plugins/cache/kr-patch/create-kr-patch/3.3.0/skills/create-kr-patch/SKILL.md').resolve()
    historical = []
    for p in [R / 'README.md', R / 'AGENTS.md', *sorted((R / 'docs').rglob('*.md'))]:
        for a, b in re.findall(r'\]\((?:<([^>\n]+)>|([^()\n]+))\)', p.read_text('utf-8')):
            n = (a or b).strip().split('#')[0]
            if not n or re.match('[a-z]+://', n):
                continue
            target = (p.parent / n).resolve()
            if target.exists():
                count += 1
            else:
                assert p.name == 'CASTLE_CURRENCY_QA.md' and target == expired, (p, n)
                historical.append(str(target))
    return count, historical


def main():
    records.DATE = '2026-10-09'
    frozen = {}
    for work in range(197, 213):
        p = R / f'manifests/nonplay{work}_assets.json'
        d = json.loads(p.read_text('utf-8'))
        for n, h in d['files'].items():
            assert sha(R / n) == h, (work, n)
        frozen[str(work)] = {'files': len(d['files']), 'sha256': sha(p)}
    target = R / 'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes'
    assert sha(target) == '7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce'
    source = json.loads((R / 'manifests/source_rom.json').read_text('utf-8'))
    assert sha(R / source['path']) == source['sha256']
    csv = R / 'workspace/translation/text_ja.csv'
    assert sha(csv) == '43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    baseline = json.loads((R / 'qa/reports/initial_session_20261004.json').read_text('utf-8'))
    first = {}
    for n, h in baseline['first_game_references'].items():
        p = R.parent / n
        if p.is_file():
            assert sha(p) == h, n
            first[n] = 'HASH_UNCHANGED'
        else:
            first[n] = 'HISTORICAL_PATH_UNAVAILABLE_NOT_RESTORED_OR_MODIFIED'
    next_action = '사용자가 새062 ROM을 초기화해 실제 화면을 검수한 결과를 받아, 보고된 글꼴·줄바꿈·소거·전환 결함을 별도 새 빌드로 수정한다.'
    section = '''현재 텍스트 확대 검토 후보는 **text11_candidate_062**다. HUD·정지 표지판 등 작은 그림을 기존 크기로 유지하고, 등록 초안45개(오프닝9+일반33+크레딧3)에11px 글꼴을 넣었다. [062 ROM](../build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes), [정적45문단과 상단창5모형](../workspace/review/text11_211/review.html), [구현·검증211](TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md).

062는524304바이트, SHA `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`다. [ROM 없는 적용ZIP212](../dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip)은68파일, ZIP SHA `377b16522c31f3516869c9eb14acb925799ceeefa1051d06508570770bc19575`다. [Windows 적용 근거212](TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md).

| 검증 구분 | 현재 결과 |
|---|---|
| 정적·빌드 | 원본ExpectedWrite/허용diff·독립 ROM/IPS 재빌드·적용 동일,45문단 글꼴 디코딩 PASS |
| CPU | 기존42개/1042수치상태/1071건너뛰기/4320초기화/1556비대상/교환050 보존10/놀이기구5창 동시거주 PASS |
| 크레딧 CPU | 첫756NT셀, 진행169/158호출의 원래대기·종료,4000프레임 동기CPU 스크롤 상태 동일 PASS |
| 패키지·실제 적용 | Windows8사례와 최종ZIP 추출본 적용 byte-exact PASS |
| 실제062 실행·장면·플레이 | **미수행·사용자 담당.062 미채택 개발 후보** |

정적 PNG와 창 모형은062 게임 캡처가 아니다. CPU 스케줄의 프레임도 실제 에뮬레이터 프레임이 아니다. CHR256 실제매핑·비동기NMI/IRQ 전송예산·글꼴수명·상단창소거/화면전환·가독성·최종미감/문체·전체플레이는 남아 있다.45는 등록 초안에 대한 수량이며 전게임 원천 발견/완료율을 뜻하지 않는다. 숫자는8px 타일 간격이고 글자 종류에 따라 실제 획높이가 다르다.

오프닝6문단은1행 ‘친구들도 데려와!’,2행 ‘깜짝 놀랄 거다!’,3행 빈줄,4행 ‘의문의 대부호로부터’ 한줄 오른쪽 정렬을 유지했다. 크레딧은 한글12px·공백8px·영문16px 간격의 개발안이며 이름/KONAMI/권리 문자열은 같다. 원래8px 이름 bitmap도11px로 확대했으므로 옛 글자그림 보존이라고 표현하지 않는다. 첫크레딧은 nativeFF31의NMI/렌더중지 경로에서 직접NT에 쓰고FF17로2000을 복원한다.2001은 출력을 중지한 채 다음nativeNMI를 기다리며 실제 하드웨어 검수는 남는다.

**기준 개발본 dialogue_kr_poc_051은 유지**한다. [051 ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes)은 티켓교환050과 움직이는 정지051 수정을 포함한다. [오프닝055 실제 비교](../workspace/review/opening11_194/review.html)의9000프레임 근거는055 오프닝에 한정하며062 전체 실행 성공으로 옮기지 않는다.054/057/059는 이전 후보,056/058/060/061은 거부 실험,205는 적용도구 크기 검사 실패로 보존했다. 이전 자료를 덮어쓰거나 삭제하지 않았다.

원본2편·CSV·기존빌드/QA·사용자Mesen/세이브는 그대로다.1편 참조5개 해시는 동일하며 역사 원본 경로1개는 현재 없어 불변 확인을 완료했다고 주장하지 않는다.1편 파일을 수정하거나 복원하지 않았다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 원문 유지다. 카페 완성 작업기는 모든 작업 후 작성하며 현재 외부 게시하지 않았다.

사용자 실제 검수는 이전 한글판에 재패치하지 않고 새062 ROM을 열어 초기화한 뒤 진행한다. 오프닝 완성/건너뛰기, 홈·선택·매표소 티켓교환, 놀이기구 이름/규칙/가격/보유/입장·성, 크레딧의 출력/대기/지우기/재진입을 확인한다. 이전 세이브스테이트 호환은 미확인이다.
'''
    p = R / 'docs/HANDOFF.md'
    text = p.read_text('utf-8')
    marker = '아래는이전작업의역사기록이며상단재개위치를우선한다.'
    assert marker in text
    p.write_text('# 진행 중 — 2026-10-09, 작업213 감사\n\n' + section + '\n**다음 작업 하나: ' + next_action + '** [오늘 인계](HANDOFF_2026-10-09.md), [오늘 journal](journal/2026-10-09.md), [계획](LOCALIZATION_WORK_PLAN.md).\n\n' + text[text.index(marker):], 'utf-8')
    p = R / 'README.md'
    text = p.read_text('utf-8')
    marker = '# 기준 개발본 — 051 (작업184 근거)'
    assert marker in text
    intro = '''> **2026-10-09 작업213 / 기준051 유지 / 062: 등록45개11px CPU·빌드·적용 검토 후보 / 실제062 미검수·미채택** [최신 인계](docs/HANDOFF.md)

## 최신 텍스트11px 검토 후보 — 062

HUD·정지 등 작은 그림을 보존하고 오프닝9+일반33+크레딧3을11px 글꼴로 확대한 개발후보다. [062 ROM](build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes), [정적 배치45개·창 모형5개](workspace/review/text11_211/review.html), [ROM 없는 적용ZIP212](dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip), [구현·CPU211](docs/TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md). 독립재빌드·기존42개와크레딧 CPU·Windows실적용 PASS. 실제062 실행·CHR256·NMI/IRQ·소거/전환·가독성은미검수이며 실제플레이는사용자담당이다. 등록45개는전게임완료율이아니다. 크레딧영문16px간격은개발안이다.

'''
    p.write_text(intro + text[text.index(marker):], 'utf-8')
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    text = p.read_text('utf-8')
    start = text.index('현재207:')
    end = text.index('\n\n현재177:', start)
    text = text[:start] + '현재213: 기준051 유지, 새062에서 오프닝9+일반33+크레딧3의 등록45개를11px 글꼴로 구현했다. 작은그림/HUD/정지는 기존크기다. CPU·독립재빌드·Windows적용 PASS, 실제062 미수행·미채택이다. 크레딧영문16px간격/최종폰트·문체승인,실제CHR256/NMI/IRQ/소거/전환·가독성은미검수다. [최신 인계](HANDOFF.md), [CPU211](TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md), [적용212](TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md). 아래 계획의 당시 버전·수량은 역사 기록이다.' + text[end:]
    p.write_text(text, 'utf-8')
    count, external = check_links()
    proof = R / 'qa/reports/text11_213_current_audit.json'
    assert not proof.exists()
    proof.write_text(json.dumps({'work': 213,
        'status': 'PASS_FROZEN197_212_SOURCE2_CSV_PROJECT_LINKS_GAME1_ONE_HISTORICAL_PATH_UNAVAILABLE',
        'frozen_manifests': frozen, 'source2_and_CSV_unchanged': True,
        'first_game_references': first, 'all_game1_references_currently_verified': False,
        'existing_links_checked_before_seal': count, 'project_local_missing_links': [],
        'expired_external_historical_skill_cache': external,
        'current_candidate': '062', 'ROM_sha256': sha(target), 'registered11px': 45,
        'CPU_build_apply': 'PASS', 'runtime062': 'NOT_RUN', 'adopted': False,
        'direct_review': 'Static062 MAIN_05939/MAIN_059E7 PNG opened; no actual062 screenshot'}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = '''정본README·HANDOFF·계획을 등록45개11px 후보062와 실제검수 경계로 갱신했다. [197~212 고정근거·원본/CSV·링크 감사](../qa/reports/text11_213_current_audit.json). 선언된 고정 파일의 해시는 모두 일치하고2편 원본·CSV는 그대로다.1편 참조5개는해시동일,역사원본 경로1개는현재없어전참조불변검증성공을주장하지않는다.1편파일을수정/복원하지않았다. 프로젝트밖 역사 플러그인3.3 캐시 만료도 별도로기록했다.

[현재062 CPU/정적 근거211](TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md), [실Windows 적용212](TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md)를 현재SHA에 연결한다.45문자·5모형·68파일 ROM없는ZIP을 구별했다. 이름/KONAMI/권리문구와 크레딧327호출·4000frame 동기CPU스케줄은보존했고 글자그림은11px로커졌다. 전역원천목록/실제실행/전체완주·최종사람승인은미수행이다.

062 크레딧제작진·제공 PNG를직접열었으며정적자료의확인이다.새에뮬레이터/컨트롤러/실제장면·카페완성작업기·게시없음.작은그림·원문유지6건·051기준·055이전실제근거·거부056/058/060/061·부분205패키지·사용자Mesen/세이브보존. [213매니페스트](../manifests/nonplay213_assets.json).

재현: 이스크립트는고정보고를덮어쓰지않는다.새보고경로를사용하는복제에서해시/링크를다시검사한다. `python scripts/build_credits11_211.py --output build/text11_213_repro_next`는원본으로부터재빌드하는새경로명령이다. 사용자검수에는062를초기화한뒤오프닝/매표소교환/상단창·성/크레딧의출력·대기·소거·전환을확인한다.'''
    records.seal(213, 'TEXT11_CANDIDATE062_CURRENT_HANDOFF_AUDIT_213.md', '062 등록45개11px 정본 인계·고정 근거 감사', body,
        '197~212 해시·2편원본/CSV·프로젝트링크 PASS.062 등록45개11px CPU/재빌드/적용후보·실제미수행·미채택.1편역사원본경로1개누락별도기록.', next_action,
        [Path(__file__), proof, R / 'workspace/review/text11_211/MAIN_05939.png',
         R / 'workspace/review/text11_211/MAIN_059E7.png'])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    text = p.read_text('utf-8')
    text = re.sub(r'^> \*\*.*?\*\*', '> **2026-10-09 작업213 / 기준051 / 062 등록45개11px CPU·적용 후보 / 실제062 미검수·미채택. 실제 플레이 사용자 담당.**', text, count=1)
    p.write_text(text, 'utf-8')
    final_count, final_external = check_links()
    assert final_count >= count and final_external == external
    print(json.dumps({'status': 'PASS', 'frozen_works': len(frozen), 'current': '062',
                      'final_project_existing_links': final_count, 'runtime062': 'NOT_RUN'}, indent=2))


if __name__ == '__main__':
    main()
