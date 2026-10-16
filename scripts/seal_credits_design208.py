"""Freeze credits consumer geometry and bounded queue strategy."""
from pathlib import Path
import json
import seal_nonplay171 as records
from seal_nonplay171 import R, sha

records.DATE = '2026-10-09'
p = R / 'qa/reports/credits11_208_engine_design.json'
assert not p.exists()
p.write_text(json.dumps({'work': 208, 'status': 'PASS_STATIC_CONSUMER_AND_BOUNDED_DESIGN_ONLY',
    'native': {'root': 7, 'slots': [45, 46, 47], 'font': 201,
               'initial_consumer_PC': 'A448', 'progressive_PC': 'A4AD',
               'line_stride': 64, 'origins': ['2805', '2005', '2805']},
    'initial_first_page_optimal_sparse_queue_bytes': 244,
    'unsafe_single_stack_page_queue_rejected': True,
    'native_screen_off': 'FF31 disables NMI bit7 and rendering bits3/4; FF17 restores scroll/registers.',
    'chosen_development_design': 'Initial2D uses FF31/direct27x28 NT writes/FF17;2E/2F preserve original expanded glyph/control call counts with per-event0..27 column paired packets.',
    'long_stream': 'Per-line pointer table plus event cursor and line cursor; no byte cursor wrap.',
    'max_event_queue_bytes': 62, 'font_slots': 106, 'Latin_spacing_final_adopted': False,
    'disassembler_attempt_failure': '208v1 omitted PC increment; stopped its own process, no ROM writes.208v2 bounded progression completed.',
    'ROM_changed': False, 'runtime': 'NOT_RUN', 'direct_game_visual': False,
    'limits': ['New CPU/PPU-register model and complete ending-state schedule still required',
               'Native register toggle alone is not asynchronous transfer/runtime proof',
               'Names/legal text retained; new11px glyph bitmaps and spacing are unadopted candidates']}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
body = '''크레딧은 root7의2D/2E/2F,201/202 글꼴, 모드5/6 NT2805/2005/2805다. native93B5가 줄마다64바이트(16px) 이동하므로11px 상하 타일을 기존 빈 아래 행에 넣을 수 있다. 원래이름·법적 문자열·빈행은 그대로 사용한다. [설계 원장](../qa/reports/credits11_208_engine_design.json).

첫2D 즉시출력은 가장 간단히 줄인 큐도244바이트라서 하위$0100 큐와 상위6502 스택이 겹칠 수 있다. 기존925E에 긴 paired 스트림을 넘기는 방식을 거부한다. native8023은FF31로 NMI/화면출력을 중지한 뒤2006/2007에 쓰고FF17로 복원한다. 별도 초기2D에서도 이 하드웨어 경로를 사용하고, 진행형2E/2F는 한 번에최대62바이트로 분할한다. 원래 줄마다 확장된 native 문자 호출 수를 그대로 유지해 전체 대사 종료/문단 전환 호출 수를 보존한다.

긴 자료는 전체8bit bytecursor 대신 줄별 포인터와 줄/이벤트 커서로 처리한다. 정적106슬롯 영문16px 간격안은 후보 구현에만 사용하며 최종 글꼴/명칭 승인이 아니다.208 분석v1은PC 증가 누락으로 같은명령 반복출력이 발생해 해당프로세스만 중지했고v2에서 수정했다. ROM/CSV/에뮬레이터·사용자Mesen/세이브/1편 수정은 없다. 이 설계는 실제스크롤·NMI예산 검증 성공이 아니다. 변경·해시는 [208매니페스트](../manifests/nonplay208_assets.json).

재현: `python scripts/inspect_credits11_208_v2.py`, `python scripts/analyze_credits11_208_v2.py`. 읽기전용 분석이며 새 ROM을 실행하지 않는다.'''
records.seal(208, 'CREDITS11_NATIVE_GEOMETRY_AND_QUEUE_DESIGN_208.md', '크레딧11px 원래16px 기하·전송 큐 설계', body,
    '원래 줄 간격16px.첫2D244바이트 큐/스택 충돌 위험으로 직접 화면출력 중지 전송을 설계,2E/2F는 원래호출수·최대62바이트 이벤트로 분할. 아직 ROM/실행 없음.',
    '새060에서 크레딧3개를 줄별 포인터·초기 직접NT·native호출수 보존 진행형 출력기로 구현하고 최종CPU를 검증한다.',
    [Path(__file__), p, R / 'scripts/inspect_credits11_208.py', R / 'scripts/inspect_credits11_208_v2.py',
     R / 'scripts/analyze_credits11_208.py', R / 'scripts/analyze_credits11_208_v2.py',
     R / 'qa/reports/credits11_202_capacity.json', R / 'build/dialogue_kr_poc_037/ui_korean_page_mapping.json'])
