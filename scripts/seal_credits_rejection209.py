"""Keep060 rejected by actual bank-restoration regression, not a runtime-tested build."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha
records.DATE = '2026-10-09'
p = R / 'qa/reports/credits11_209_rejection.json'
assert not p.exists()
p.write_text(json.dumps({'work': 209, 'status': 'REJECTED060_NESTED_MAPPER_BANK_SAVE',
    'ROM_sha256': sha(R / 'build/text11_candidate_060/TinyToon2_Text11_Candidate060.nes'),
    'actual_ordinary_CPU_first_case': {'banks': [8, 9], 'RAM2B': 8, 'expected_banks': [18, 19], 'expected_RAM2B': 50},
    'cause': 'Outer mapper switch and copied inner GUARD both call FDD3; second LDY8000/STY2B overwrites canonical return tag with08.',
    'builder_v1_prebuild_rejected': 'Attempted credit data9A00 overlaps immutable opening private streams; v2 moved dataAA00 before generating060.',
    'credits_initial_CPU': '756 NT cells correct; verifier initially expected FF17 to restore2001, but native FF17 only restores2000.2001 remains render-off until native NMI.',
    'new_candidate_resolution': 'Remove nested FDD3 from private ordinary guard; preserve original bank tag once. Correct register restoration oracle to native behavior.',
    'runtime060': 'NOT_RUN', 'package': False, 'adopted': False}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
body = '''060은 크레딧3개를 확대하고 독립 ROM/IPS 빌드는 일치했으나 일반 대사 CPU 회귀의 첫 사례에서 PRG8/9·복귀태그08에 남았다. 새 공통 래퍼와 복제한 기존 GUARD가 각각FDD3를 호출해 두번째저장이 원래32 복귀태그를08로 바꾼 것이 원인이다. [거부 보고](../qa/reports/credits11_209_rejection.json).060은 미채택·미패키지이며 기존059를 유지한다.

빌더v1은 저장하기 전에 오프닝9A00 스트림과의 겹침을 검사로 거부했다. v2에서 크레딧 자료를AA00으로 옮겨060을 만들었고 기존42문자원천·글꼴 픽셀은 동일했다. 크레딧 초기756셀 직접NT 결과도 같았지만 nativeFF17은2000만 복원하고2001은 출력을 중지한 채 다음NMI가 처리한다.208의 ‘스크롤/레지스터 복원’ 표현을 이 정확한 경계로 정정한다. 이를 실제NMI/화면 검증으로 주장하지 않는다.

새061은 private 일반 GUARD의 중복FDD3를 제거하고 크레딧 CPU 검사의2001 기대값을 원래 동작에 맞춘다. 실패060/재빌드/사용한 빌더와 검사기·원본/CSV/051/055/057/059·사용자Mesen/세이브를 보존한다. 새 에뮬레이터/컨트롤러/장면/카페 작업기·게시 없음. 변경·해시는 [209매니페스트](../manifests/nonplay209_assets.json).'''
files = [Path(__file__), p, *[R / f'scripts/{n}' for n in ('build_credits11_209.py', 'build_credits11_209_v2.py', 'prepare_credits_verifier209.py', 'verify_text11_ordinary209.py', 'verify_credits11_209.py')],
         *[f for folder in (R / 'build/text11_candidate_060', R / 'build/text11_209_rebuild060') for f in folder.iterdir() if f.is_file()]]
records.seal(209, 'CREDITS11_CANDIDATE060_MAPPER_REJECTION_209.md', '크레딧 확대060 빌드·중복 뱅크저장 CPU 거부', body,
    '060 독립빌드 exact이나 일반대사CPU에서 복귀태그08 남음: 공통/기존GUARD 중복FDD3 원인.060 미채택·미패키지,059 유지.',
    '별도061에서 중복 mapper저장을 제거하고 크레딧3·기존42·전체원래스케줄CPU를 검증한다.', files)
