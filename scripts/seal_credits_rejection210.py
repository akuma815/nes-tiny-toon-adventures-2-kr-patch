"""061 CPU rejects an unmirrored post-bank-restore return and missing event delay reset."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha
records.DATE = '2026-10-09'
p = R / 'qa/reports/credits11_210_rejection.json'
assert not p.exists()
p.write_text(json.dumps({'work': 210, 'status': 'REJECTED061_PRIVATE_POST_BANK_RESTORE_PC_AND_EVENT_DELAY',
    'ROM_sha256': sha(R / 'build/text11_candidate_061/TinyToon2_Text11_Candidate061.nes'),
    'ordinary_CPU': 'PrivateB800 guard restored canonical18 then continued at unmappedB8xx; execution left expected printer.',
    'credits_CPU': 'Event7 left58=7 while native9227 resets58=0 for each glyph; first6 calls/end matched.',
    'resolution': 'Only mirrored9630 wrapper restores bank on target return; mirrored9650 native fallback restores then jumps96F0. Reset event58 without clearing FE delay7.',
    'runtime061': 'NOT_RUN', 'adopted': False, 'package': False}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
body = '''061은 중복FDD3를 제거했지만 privateB800 GUARD 안에서FDDB 후 다른bank18의B8xx로 이어져 일반 대사 CPU가 원래 출력기를 벗어났다. 원래9630 GUARD가 두 뱅크에 같게 복제되어 있었던 조건을 새주소에서도 지켜야 한다. 또한 크레딧7번째 호출부터58에줄끝 대기7이 남았다. 원래9227은매글자마다58을0으로 초기화한다. [거부 보고](../qa/reports/credits11_210_rejection.json).

061/독립재빌드·CPU실패 검사·읽기전용 진단을 보존하고 미채택·미패키지로 둔다. 새062는 대상출력뒤 bank복원을공통 mirrored9630 한곳에서 수행한다. 원래8pxfallback은 별도mirrored9650에서복원뒤96F0로간다. 크레딧 이벤트마다58을0으로하고FE/FF에서는원래7/60을유지한다. 원본·CSV·059·이전검증/실패·사용자Mesen/세이브 보존. 새실행/컨트롤러/장면/카페작업기/게시없음. 변경·해시는 [210매니페스트](../manifests/nonplay210_assets.json).'''
files = [Path(__file__), p, *[R / f'scripts/{n}' for n in ('prepare_credits210.py', 'build_credits11_210.py', 'verify_text11_ordinary210.py', 'verify_credits11_210.py', 'debug_credits210.py')],
         *[f for folder in (R / 'build/text11_candidate_061', R / 'build/text11_210_rebuild061') for f in folder.iterdir() if f.is_file()]]
records.seal(210, 'CREDITS11_CANDIDATE061_RETURN_AND_DELAY_REJECTION_210.md', '061 private복귀주소·대기값 CPU 거부', body,
    '061 일반CPU의미복제post-FDDB주소/크레딧58초기화결함 발견. 실패·빌드보존,059 유지.062 mirrored복원 및delay수정 예정.',
    '새062에서 mirrored복원·event대기값을수정하고 기존42·크레딧3·원래4000frame스케줄CPU를검증한다.', files)
