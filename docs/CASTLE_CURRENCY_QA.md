# 작업53 — 성 일반 티켓50/49 경로와 실제 성 플레이

[검증 보고](../qa/reports/castle_currency053.json), [실제4장면](../qa/dialogue/castle053_actual_pages.json). 현재043 ROM/SSOT는 변경하지 않았다. [작업52 범위별 보존 감사](../qa/reports/engine_closure052_session.json)도 완료했다.

원래 일반 티켓 변수07D0..2에1000프레임에만50 또는49를 넣었다. 골드 티켓은0이며 이후에는 controller 입력만 했다. 이는 자연 플레이로 티켓을 수집한 증거가 아니다. 각 실행의 원본/ROM/입력/seed/도구/로그/파일 SHA와 종료를 검사했고1,834화면과11,054파일을 보존했다.

50 경로는 native slot1A의 ‘일반 티켓50장으로 입장 가능해요’와slot1C 허용 대사를 거쳐50→0으로 차감된다. 이전6,000프레임 입력은 놀이기구 설명 카드에 멈췄다. 이를 실제 성 플레이 검증과 구분했다. [추가 확인 입력](../config/menu_castle_continue_001.json)의A4100 이후 root4/phase5/course4의 실제 성 스테이지에 진입했다. [환경](../qa/dialogue/castle043_normal50_continue/environment.json).

49 경로는 native slot19의 거절/복귀 대사를 거쳐 홈으로 돌아가며49를 보존한다. [환경](../qa/dialogue/castle043_normal49_visual/environment.json). 두 경로에서 골드0과 native 차감 코드의 원본 바이트를 확인했다. 슬롯2C는1A와 같은 원천의 alias이며 이번 경로도1A를 썼다. alias 미관측을 원천 문구 누락으로 계산하지 않는다.

CPU/재빌드/apply는 이전043 증거를 유지하며 이번에 다시 수행했다고 주장하지 않는다. IRQ 전 경로 timing-only 실행과 PNG/RAM/메뉴 소비 실행을 별도 환경으로 보존했다. [native IRQ50](../qa/dialogue/castle043_normal50/environment.json), [native IRQ49](../qa/dialogue/castle043_normal49/environment.json), [화면50](../qa/dialogue/castle043_normal50_visual/environment.json).

**새 결함:** 실제 성 플레이4410프레임에서 한글 HUD 위쪽 획이 잘리는 화면을 확인했다. 이전 ‘성 회귀’는 입구/카드까지만 관찰했으므로 그 성공이 실제 성 HUD의 성공을 의미하지 않는다. [실제4배 화면](../work/castle043_HUD_actual4410_4x.png)을 별도로 보존했다. 이 결함을 수정하기 전 최종 배포를 만들지 않는다. 이는 [SKILL.md](<C:/Users/akuma/.codex/plugins/cache/kr-patch/create-kr-patch/3.3.0/skills/create-kr-patch/SKILL.md>)의25행 ‘Fix it ... or withhold the release.’에 해당하며, 작업을 중단하거나 승인을 요구하지 않고 수정한다.

현재ROM SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`, IPS SHA `4337ba28119d88135a8f3cca7f3a0a6d32a3e183e92e40aa3bfff84b2a45f1bb` 그대로다. 원본·1편·과거 성공/실패·QA·SSOT를 보존했다. 전체 자연플레이·오디오/reset/savestate/실기/최종 사람 검토는 미수행이며 dist는 아직 비어 있다.

재현: `python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새이름> --frames 9000 --inputs config/menu_castle_continue_001.json --script scripts/trace_branch_seed_v1.lua --seed config/gate_normal50_seed_001.json`. 49 검증은frames6000/menu_castle_001.json/gate_normal49_seed_001.json이다. 기존 경로를 덮어쓰지 않는다.

다음 작업 하나: **실제 성 플레이 HUD IRQ/PPU 소비를 추적해 획 잘림을 고치고 시점·숫자·플레이 영역을 검증한다.** 중단 지시 없이 이어간다.
