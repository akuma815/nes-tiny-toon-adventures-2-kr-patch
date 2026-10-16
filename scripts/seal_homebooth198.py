"""Record failed056 CPU guard attempt without adopting or discarding artifacts."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    report = R / 'qa/reports/homebooth11_198_attempt.json'
    assert not report.exists()
    d = {'work': 198, 'status': 'REJECTED056_NONTARGET_OVERFLOW_FLAG_GUARD',
         'ROM_sha256': sha(R / 'build/homebooth11_candidate_056/TinyToon2_HomeBooth11_Candidate056.nes'),
         'builder_v1': 'CSV field source_file_offset absent; rejected before output; v2 uses file_offset',
         'CPU_before_rejection': ['Twelve progressive paths and all skip boundaries inside5row clear',
                                  'Opening nine finalCPU', 'Native initializer and050 retention comparisons'],
         'failing_case': {'root': 8, 'id': 11, 'font': 130, 'pointer': 0x9731, 'PC': 0x925e,
                          'expected_flags': 0x77, 'actual_flags': 0x37, 'difference': 'V overflow flag'},
         'cause': 'Guard SBC changes overflow; fallback must preserve incoming processor flags',
         'adopted': False, 'new_runtime': False, 'distribution': False}
    report.write_text(json.dumps(d, indent=2) + '\n', 'utf-8')
    folders = [R / 'build/homebooth11_candidate_056', R / 'build/homebooth11_198_rebuild056']
    body = '''ホーム12文の056候補を作ったがCPU非対象分岐のVflag差で不採用とした。'''
    body = '''ホーム・매표소12개를11px로 만든056 후보를 최종CPU 검사에서 거부했다. 첫 빌더는 CSV 열 이름의 잘못된 가정으로 출력 전에 중단됐고, v2에서 실제 `file_offset`을 사용했다. 후보056과 독립 재빌드의 ROM/IPS는 동일하며 기존055 오프닝·HUD/정지 등 그림·원본·CSV를 보존했다.

점진 출력과 모든 건너뛰기 경계,5행 지우기, 오프닝9개 CPU, 기존 초기화/050 매표소 글꼴 보존 검사를 수행한 뒤 비대상 fallback 검사에서 실패했다. root8/slot0B/font130/pointer9731의 즉시 출력925E에서 A/X/Y/SP·큐는 같지만 P의V가77→37로 달랐다. 새 범위 판정의SBC가V를 바꿨다. 원래 명령어가V를 보존하는 비대상 경로도 있기 때문에 성공으로 처리하지 않았다. [실패 원장](../qa/reports/homebooth11_198_attempt.json), [변경·해시 목록](../manifests/nonplay198_assets.json).

056은 미채택·패키지 없음·에뮬레이터 미실행이며 두 빌드와 실패 스크립트를 그대로 보존한다. 다음 새 후보는 판정 전 processor flags를 저장하고 대상/비대상 분기에서 복원한다. 기존055 검토본과 기준051은 그대로다. 새 자동 플레이·컨트롤러/전체 장면·직접 시각 검증은 하지 않았다. 재현 실패 명령은 `python scripts/verify_homebooth11_198.py`이며 기존 출력이 없는 실패 검사만 대상으로 한다. 원본/1편/사용자Mesen/세이브를 변경하지 않았다.'''
    records.seal(198, 'HOME_BOOTH11_056_REJECTED_CPU_FLAG_198.md', '홈·매표소12개 후보056 비대상CPU 플래그 실패 기록', body,
                 '056 독립 빌드 동일, 점진/즉시 출력 검사 후 비대상V flag 차이로 거부. 후보·실패 증거 보존, 미채택·미패키지.',
                 '055 기반 새057 후보에서 범위 판정 전후P를 보존하고 전체 CPU 검사를 다시 수행한다.',
                 [Path(__file__), R / 'scripts/build_homebooth11_198.py', R / 'scripts/build_homebooth11_198_v2.py',
                  R / 'scripts/verify_homebooth11_198.py', report,
                  *[f for folder in folders for f in folder.iterdir() if f.is_file()]])


if __name__ == '__main__':
    main()
