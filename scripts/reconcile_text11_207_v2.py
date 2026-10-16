"""Record missing historical game1 path without pretending its current hash was checked."""
from pathlib import Path
import json
import re
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    manifests = {}
    for work in range(197, 207):
        p = R / f'manifests/nonplay{work}_assets.json'
        d = json.loads(p.read_text('utf-8'))
        for n, h in d['files'].items():
            assert sha(R / n) == h, (work, n)
        manifests[str(work)] = {'files': len(d['files']), 'sha256': sha(p)}
    initial = json.loads((R / 'qa/reports/initial_session_20261004.json').read_text('utf-8'))
    first = {}
    for n, h in initial['first_game_references'].items():
        p = R.parent / n
        if p.is_file():
            assert sha(p) == h, n
            first[n] = {'status': 'PASS_HASH_UNCHANGED', 'sha256': h}
        else:
            first[n] = {'status': 'MISSING_HISTORICAL_REFERENCE_PATH_NOT_MODIFIED_OR_RESTORED', 'historical_sha256': h}
    missing = [n for n, v in first.items() if v['status'].startswith('MISSING')]
    assert missing == ['Tiny Toon Adventures/original/rom/Tiny Toon Adventures (Japan).nes']
    source = json.loads((R / 'manifests/source_rom.json').read_text('utf-8'))
    assert sha(R / source['path']) == source['sha256']
    assert sha(R / 'workspace/translation/text_ja.csv') == '43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f'
    count = 0
    external = []
    expired = Path('C:/Users/akuma/.codex/plugins/cache/kr-patch/create-kr-patch/3.3.0/skills/create-kr-patch/SKILL.md').resolve()
    for p in [R / 'README.md', R / 'AGENTS.md', *sorted((R / 'docs').rglob('*.md'))]:
        for a, b in re.findall(r'\]\((?:<([^>\n]+)>|([^()\n]+))\)', p.read_text('utf-8')):
            n = (a or b).strip().split('#')[0]
            if not n or re.match('[a-z]+://', n):
                continue
            t = (p.parent / n).resolve()
            if t.exists():
                count += 1
            else:
                assert p.name == 'CASTLE_CURRENCY_QA.md' and t == expired, (p, n)
                external.append(str(t))
    proof = R / 'qa/reports/text11_207_current_audit.json'
    assert not proof.exists()
    proof.write_text(json.dumps({'work': 207,
        'status': 'PASS_PROJECT197_206_SOURCE_CSV_LINKS_FIRSTGAME_ONE_PATH_UNAVAILABLE',
        'frozen_manifests': manifests, 'source2_and_CSV_unchanged': True,
        'first_game_references': first, 'all_first_game_references_verified': False,
        'local_existing_links_checked_before_seal': count, 'project_local_missing_links': [],
        'expired_external_historical_skill_cache': external,
        'initial_auditor_failure': 'First-game original/rom source path unavailable;207v1 stopped before seal. Five other references hashes unchanged.',
        'runtime059': 'NOT_RUN', 'adopted': False, 'registered11px': 42, 'credits_remaining8px': 3,
        'direct_new_game_visual_QA': False, 'static_model_ride01_viewed': True}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = '''059는 오프닝9+일반33개11px CPU/재빌드/실Windows 적용 검증 후보이고 실제 실행 미수행·미채택이다. 크레딧3개와 작은그림은 각각8px/기존 크기다. 정본README·HANDOFF·계획의 재개 위치를059로 갱신하고051 기준/055 이전 실제근거/실패056·058·205를 구별했다.

[197~206 고정근거·현재 원본·CSV·프로젝트 링크 감사](../qa/reports/text11_207_current_audit.json)는 PASS다. 207v1 감사기는1편의 역사 원본 경로 `Tiny Toon Adventures/original/rom/Tiny Toon Adventures (Japan).nes`가 현재 없어서 중단했다. 1편의 다른 참조5개는 해시 일치한다. 누락 경로를 복원하거나1편 파일을 수정하지 않았다.1편 전체 참조 불변을 현재 확인했다고 주장하지 않는다. 이전202 감사 성공은 당시 상태의 기록이다. 프로젝트 밖의 역사 플러그인3.3 캐시 경로 하나도 만료 상태를 별도로 기록했다.

059 놀이기구1 상단 모형 PNG를 직접 열어 이름/설명 배치를 확인했다. 이는 원래033 NT 기하에 최종059 CPU 출력으로 만든 정적 모형이며 실제059 캡처가 아니다. 새 에뮬레이터·컨트롤러·전체플레이·최종 글꼴 승인·카페 완성 작업기/외부 게시 없음. 현재2편 원본·CSV·기존 근거와 실패 파일·사용자Mesen/세이브를 보존한다. 변경·해시는 [207매니페스트](../manifests/nonplay207_assets.json).

재현: 이 감사 스크립트는 고정 보고를 덮어쓰지 않는다. 새 보고 경로를 사용하는 복제에서 해시·링크를 다시 검사한다. 패키지 적용은206 README를 따르고 새059에 초기화하여 검수한다. 055의 실제 검증을059의 검증으로 옮기지 않는다.'''
    next_action = '크레딧3개의 실제 출력 루틴에서 초기 전송량·16px 줄 간격·모드5/6 주소를 확인하고 별도11px CPU 후보의 구현 조건을 확정한다.'
    records.seal(207, 'TEXT11_CANDIDATE059_CURRENT_AUDIT_207.md', '059 확대 후보 정본 인계·고정 근거 감사', body,
                 '197~206 고정근거·2편 원본/CSV·프로젝트 링크 PASS.1편 참조5개 해시 일치/역사 원본 경로1개 현재 없음.059 CPU/적용 후보42개11px,실제미수행,크레딧3개8px.', next_action,
                 [Path(__file__), R / 'scripts/reconcile_text11_207.py', R / 'scripts/prepare_package206.py', proof,
                  R / 'workspace/review/ordinary11_204/model_ride01.png'])
    p = R / 'docs/LOCALIZATION_WORK_PLAN.md'
    p.write_text(p.read_text('utf-8').replace('현재 개발049 / 작업207', '기준051 / 일반33개059 CPU패키지 / 작업207', 1), 'utf-8')
    print(json.dumps({'status': 'PASS_PROJECT_WITH_ONE_HISTORICAL_GAME1_PATH_UNAVAILABLE', 'frozen_works': len(manifests), 'project_links': count}, indent=2))


if __name__ == '__main__':
    main()
