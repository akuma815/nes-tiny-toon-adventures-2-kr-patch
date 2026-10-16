"""Current059 CPU/apply candidate with explicit historical/runtime boundaries."""
from pathlib import Path
import json
import subprocess
import sys
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    target = R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes'
    checks = {}
    for work in range(197, 207):
        f = R / f'manifests/nonplay{work}_assets.json'
        d = json.loads(f.read_text('utf-8'))
        for p, h in d['files'].items():
            assert sha(R / p) == h, (work, p)
        checks[str(work)] = {'files': len(d['files']), 'sha256': sha(f)}
    assert sha(target) == '8b44d79b19c490dc6c5e2f3dcf73d08d1716ab981b62878067043a5600f59930'
    assert sha(R / 'workspace/translation/text_ja.csv') == '43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    pkg = json.loads((R / 'qa/reports/ordinary11_206_package.json').read_text('utf-8'))
    assert pkg['status'] == 'PASS_ROMFREE_CPU_ONLY059_WINDOWS8_FINAL_ZIP_APPLY'
    assert pkg['ROM_sha256'] == sha(target)
    next_action = '크레딧3개의 실제 출력 루틴에서 초기 전송량·16px 줄 간격·모드5/6 주소를 확인하고 별도11px CPU 후보의 구현 조건을 확정한다.'
    section = '''현재 확대 검토 후보는 **ordinary11_candidate_059**다. 오프닝9개와 일반 대사·선택지·놀이기구 이름/설명·가격/보유/입장33개, 합계42개의 등록 문자열을11px로 배치했다. [059 ROM](../build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes), [정적 문자·상단창 모형](../workspace/review/ordinary11_204/review.html), [CPU·공유창 인계204](ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md). 그림/HUD·정지 표지판은 기존 크기로 보존했다. 상단 이름 칸은 글자를 담도록 아래 테두리를 조정했다.

059 SHA `8b44d79b19c490dc6c5e2f3dcf73d08d1716ab981b62878067043a5600f59930`,524304바이트. 독립 ROM/IPS 재빌드·33문단/1042수치상태·1071건너뛰기 경계·4320초기화·1556비대상·교환050 보존10·놀이기구5개 공유창 CPU PASS. [ROM 없는 적용ZIP206](../dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009.zip)은56파일, Windows8사례와 최종ZIP 실제 적용 byte-exact PASS다. [패키지 인계206](ORDINARY11_CANDIDATE059_APPLY_PACKAGE_206.md).

**059 새 실제 실행은 미수행이며 채택하지 않았다.** 정적 PNG/상단창 모형은059 게임 캡처가 아니다. CHR256 실제 매핑·NMI/IRQ 전송 예산·글꼴 수명·소거/전환·실제 가독성은 사용자 검수가 남는다. 크레딧3개는 아직8px다. [106슬롯 크레딧 정적 대안202](CREDITS11_SHARED_FONT106_SPACING_OPTION_202.md)은 영문 간격16px의 미채택안이며 출력기에 삽입하지 않았다.42/45는 등록 초안에 대한 수량이지 전게임 완료율이 아니다.

**기준 개발본 dialogue_kr_poc_051은 유지**한다. [051 ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes)은 티켓 교환050과 움직이는 정지051 수정을 포함한다. [오프닝055 비교](../workspace/review/opening11_194/review.html)는 사용자6문단 요청 반영·이전 실제9000프레임9문단3회 검증본이다.055의 실제 근거를059 전체 실행 성공으로 옮기지 않는다.057/054는 이전 CPU후보,056/058은 거부한 실험으로 보존한다. [패키지205 실패](ORDINARY11_PACKAGE059_SIZE_GUARD_FAILURE_205.md)는 이전 결과 크기를 유지한 적용 도구 오류이며206의 별도 패키지에서 수정했다.

원본·1편·CSV·기존 빌드와 QA·사용자Mesen/세이브를 보존했다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 원문 유지다. 새 자동플레이/컨트롤러·전체완주·오디오·하드웨어·저장 호환·최종 글꼴/문체 승인·카페 완성 작업기와 외부 게시는 진행하지 않았다.
'''
    handoff = R / 'docs/HANDOFF.md'
    text = handoff.read_text('utf-8')
    marker = '아래는이전작업의역사기록이며상단재개위치를우선한다.'
    assert marker in text
    text = '# 진행 중 — 2026-10-09, 작업207 감사\n\n' + section + '\n**다음 작업 하나: ' + next_action + '** [오늘 인계](HANDOFF_2026-10-09.md), [오늘 journal](journal/2026-10-09.md), [계획](LOCALIZATION_WORK_PLAN.md).\n\n' + text[text.index(marker):]
    handoff.write_text(text, 'utf-8')
    p = R / 'README.md'
    text = p.read_text('utf-8')
    marker = '# 현재 개발본 — 작업184 / 051'
    assert marker in text
    intro = '''> **2026-10-09 작업207 / 기준051 유지 / 059: 오프닝9+일반33개11px CPU·빌드·적용 후보 / 크레딧3개8px / 실제059 검수 미수행** [최신 인계](docs/HANDOFF.md)

## 최신11px 검토 후보 — 059

HUD·정지 등 작은 그림을 보존하고 등록 텍스트42개를 확대한 개발 후보다. [059 ROM](build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes), [정적 배치·상단창 모형](workspace/review/ordinary11_204/review.html), [ROM 없는 적용ZIP206](dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009.zip), [CPU 근거204](docs/ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md). 독립 재빌드·CPU·실제Windows 패치 적용 PASS.059의 실제 실행/가독성·최종 채택은 아직 검수하지 않았고 크레딧3개는8px다. 기존 [오프닝055 실제 비교](workspace/review/opening11_194/review.html)의 검증 범위는055 오프닝이다.

'''
    p.write_text(intro + text[text.index(marker):].replace(marker, '# 기준 개발본 — 051 (작업184 근거)', 1), 'utf-8')
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    text = p.read_text('utf-8')
    start = text.index('현재196:')
    end = text.index('\n\n현재177:', start)
    text = text[:start] + '현재207: 기준051을 유지하고 확대 개발 후보059에서 오프닝9+일반33개를11px로 구현했다. CPU·독립 재빌드·Windows 적용 PASS, 실제059 검수 미수행·미채택이다. 크레딧3개는8px이며 영문16px 간격106슬롯안은 미채택 정적안이다. HUD·정지 등 작은 그림은 기존 크기를 보존한다. [최신 인계](HANDOFF.md), [검증204](ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md), [적용206](ORDINARY11_CANDIDATE059_APPLY_PACKAGE_206.md). 아래 각 계획의 버전·수량은 역사 기록이다.' + text[end:]
    p.write_text(text, 'utf-8')
    links = R / 'qa/reports/text11_207_local_links.json'
    subprocess.run([sys.executable, str(R / 'scripts/audit_project_links184.py'), '--manifest', 'manifests/nonplay206_assets.json', '--output', links.relative_to(R).as_posix()], check=True, capture_output=True)
    proof = R / 'qa/reports/text11_207_current_audit.json'
    assert not proof.exists()
    proof.write_text(json.dumps({'work': 207, 'status': 'PASS_FROZEN197_206_AND_CURRENT059_SOURCE_LINKS',
        'frozen_manifests': checks, 'source_CSV_and_first_game_unchanged': True,
        'local_links_report': links.relative_to(R).as_posix(), 'ROM_sha256': sha(target),
        'CPU_and_build_apply_verified': True, 'runtime059': 'NOT_RUN', 'adopted': False,
        'registered_11px_entries': 42, 'credits_remaining8px': 3,
        'compact_graphics_preserved': True, 'direct_new_game_visual_QA': False,
        'static_model_ride01_viewed': True}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = '''最新059는 등록 오프닝9+일반33개11px의 CPU/재빌드/실Windows 적용 검증 후보이고 실제 실행 미수행·미채택이다. 크레딧3개와 작은그림은 각각8px/기존 크기다. 정본README·HANDOFF·계획의 재개 위치를059로 갱신하고051 기준/055의 이전 실제근거/실패056·058·205를 구별했다.

[197~206 고정근거 감사](../qa/reports/text11_207_current_audit.json)와 [프로젝트 링크·원본·1편](../qa/reports/text11_207_local_links.json)을 확인했다. 원본/번역CSV/첫게임 참조는 그대로이며 기존 근거 파일의 해시는 모두 일치한다. 역사 문서의 외부 플러그인3.3 캐시 경로 하나는 만료되어 별도로 기록했고 프로젝트 파일 누락으로 취급하지 않는다.

059의 놀이기구1 상단 모형 PNG를 직접 열어 이름/설명 배치를 확인했다. 이는 원래033 NT 기하에 최종059 CPU 출력으로 만든 정적 모형이며 실제059 실행 캡처가 아니다. 새 에뮬레이터·컨트롤러·전체플레이/크레딧 스크롤·사람 최종 승인·카페 작업기/게시 없음. 원본·1편·CSV·사용자Mesen/세이브·기존 검증/실패 근거를 보존한다. 변경·해시는 [207매니페스트](../manifests/nonplay207_assets.json).

재현: `python scripts/audit_project_links184.py --manifest manifests/nonplay206_assets.json --output qa/reports/text11_207_repro_next.json`. 고정 보고를 덮어쓰지 않는다. 패키지 빌더 재현은 기존 결과 대신 새로운 정확한 패키지/QA 경로를 사용하는 복제에서 진행한다.'''.replace('最新059', '최신059')
    records.seal(207, 'TEXT11_CANDIDATE059_CURRENT_AUDIT_207.md', '059 확대 후보 정본 인계·고정 근거 감사', body,
                 '197~206 해시·원본/CSV/1편·프로젝트 링크 PASS.059 CPU/빌드/적용 후보·미채택·실제검수 미수행. 등록42개11px,크레딧3개8px.', next_action,
                 [Path(__file__), R / 'scripts/prepare_package206.py', proof, links,
                  R / 'workspace/review/ordinary11_204/model_ride01.png'])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    p.write_text(p.read_text('utf-8').replace('현재 개발049 / 작업207', '기준051 / 일반33개059 CPU패키지 / 작업207', 1), 'utf-8')
    print(json.dumps({'status': 'PASS', 'frozen_works': len(checks), 'latest_candidate': '059'}, indent=2))


if __name__ == '__main__':
    main()
