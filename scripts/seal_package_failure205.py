"""Preserve the first059 packaging failure; target ROM and earlier evidence unchanged."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha


def main():
    records.DATE = '2026-10-09'
    folder = R / 'dist/TinyToonAdventures2_KR_Ordinary11_Candidate059_20261009'
    target = R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes'
    proof = R / 'qa/reports/ordinary11_205_package_failure.json'
    assert not proof.exists()
    assert '-ne 499728' in (folder / 'apply.ps1').read_text('utf-8-sig')
    assert target.stat().st_size == 524304
    assert sha(target) == '8b44d79b19c490dc6c5e2f3dcf73d08d1716ab981b62878067043a5600f59930'
    proof.write_text(json.dumps({
        'work': 205, 'status': 'REJECTED_PACKAGE_HELPER_TARGET_SIZE',
        'actual_Windows_first_apply_exit_code': 1,
        'stdout': '[실패] 패치 결과 검증에 실패했습니다.',
        'cause': 'Copied055 helper retained499728 byte guard;059 is524304 bytes.',
        'target_ROM_sha256': sha(target), 'target_ROM_bytes': target.stat().st_size,
        'helper_expected_bytes': 499728, 'ROM_changed': False, 'ZIP_created': False,
        'runtime059': 'NOT_RUN', 'adopted': False,
        'partial_package_preserved': folder.relative_to(R).as_posix()
    }, ensure_ascii=False, indent=2) + '\n', 'utf-8')
    body = '''059의 첫 패키지 Windows 실적용이 결과 크기 검사에서 실패했다. 055 적용 도구를 복제하면서 결과 SHA는059로 바꿨지만 결과 크기499728바이트를 유지한 것이 원인이다. CHR256KiB 후보059의 실제 크기는524304바이트다. [실패 원장](../qa/reports/ordinary11_205_package_failure.json).

ROM059와 작업204의 CPU·재빌드·정적 근거는 변경하지 않았다. 첫 패키지 폴더와 QA 복제본, 사용한 스크립트를 보존한다. 완성 ZIP은 만들어지지 않았고 이 부분 패키지는 사용 대상으로 안내하지 않는다. 새 작업206은 별도 패키지/QA 경로에서 정확한 결과 크기와 SHA 검사를 적용한 뒤 Windows8사례와 최종ZIP 추출본을 확인한다.

이번 작업은 패키지 실패 기록이다. ROM 변경·에뮬레이터·컨트롤러·새 실제장면 검증은 없다. 원본·1편·CSV·기존 빌드/근거·사용자 Mesen/세이브 보존. 크레딧3개는 아직8px이며059 실제 표시 검수는 미수행이다.'''
    files = [Path(__file__), R / 'scripts/package_ordinary11_205.py', proof,
             *[p for p in folder.rglob('*') if p.is_file()],
             *[p for p in (R / 'qa/release/ordinary11_205_apply059').rglob('*') if p.is_file()]]
    records.seal(205, 'ORDINARY11_PACKAGE059_SIZE_GUARD_FAILURE_205.md',
                 '059 첫 적용 패키지 크기 검증 실패 보존', body,
                 'ROM059는 그대로이며 적용 도구의 이전499728바이트 검사 때문에 첫 Windows 적용 실패. 부분 패키지/QA를 보존하고 새206으로 수정한다.',
                 '별도206 패키지에서 결과 크기524304/SHA 검사를 수정하고 Windows8사례·최종ZIP 적용을 검증한다.', files)


if __name__ == '__main__':
    main()
