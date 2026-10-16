# 작업54 — 실제 성 플레이 HUD 검증과 작업53 육안 의심 정정

[검증 보고](../qa/reports/castle_hud054_validation.json), [의심 정정](../qa/reports/castle054_visual_suspicion_erratum.json). ROM/SSOT 변경0, 현재043을 유지한다. 작업53의 원문/보고서/실제 장면은 덮어쓰지 않았다.

실제4410프레임의 ‘체력’ 필드 x24..47/y190..196은 font206의7개 Galmuri7 행과 모두 일치했다. 잘림은 육안 의심이었으며 실제 결함으로 확인되지 않았다. 여기에 다른5항목과 숫자·시점을 더해 검증했다.

동일한1000프레임 normal50 seed, controller 입력, Mesen/config/Lua로 [039 원래 HUD](../qa/dialogue/castle039_hud_reference/environment.json)와 [043 현재 HUD](../qa/dialogue/castle043_hud_consumer/environment.json)를 각각9,000프레임 실행했다. 자연 티켓 수집/전체 클리어의 증거는 아니다. root4/phase5/course4의 실제 성 플레이293화면을 비교했다. 입구/카드 화면을 성 플레이로 계산하지 않았다.

native FCB6→FCCF 경로가 선택되고, 실제 직전 프레임의 FCF1/A008 scanline189+1로 header190을 정했다. 7행 한글 체력/점수/시간과 점/티켓/금티켓의349,256픽셀은 현재 ROM glyph와 정확히 같다. 체력 하트·점수·시간·티켓/골드의 x표시와 숫자618,816픽셀은 원래039 화면과 의도한2px 이동 후 정확히 같다. RAM/OAM/NT/palette도 같다. 게임 영역 y0..189 변경0이다.

146,750 IRQ 기록의 프레임/PC/address/scanline/dot/cycles/context는 모두 같다. 기존040의 의도한 bank124/125→206/207과 fineY2→0 값만 허용했다. 별도 getState/raw PPU/OAM을 IRQ FCF1에서 기록했으며 통째로 현재 ROM과 무관한 임의색 도식으로 판정하지 않았다.

[관찰 Lua](../scripts/trace_castle_hud_v1.lua), [실행기](../scripts/run_castle_hud_qa.py), [독립 화면·시점 검증기](../scripts/verify_castle_hud.py)를 보존한다. 재현은 `python scripts/run_castle_hud_qa.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 9000 --inputs config/menu_castle_continue_001.json --seed config/gate_normal50_seed_001.json`. 비교 기준 ROM만039로 바꾸고 다른 새 경로에 실행한다. 기존 환경·증거를 덮어쓰지 않는다.

043 원본/rebuild/apply/6,005화면/637,476 IRQ의 작업51 증거를 유지하며 이번 조사에서 재빌드했다고 주장하지 않는다. [51 전체 보존 감사](../qa/reports/train_sign051_session.json)는513,359기존 산출물과49,071 runtime 파일을 확인했다. 괄호 파일명 링크 파서만별도V2로 정정했으며 [원래 오류 기록](../qa/reports/train051_link_parser_error.json)과 기존 검사기를 보존했다. [53 범위별 보존 감사](../qa/reports/castle_currency053_session.json)도 완료했다.

ROM SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`, IPS SHA `4337ba28119d88135a8f3cca7f3a0a6d32a3e183e92e40aa3bfff84b2a45f1bb` 그대로다. 현재 조사된 HUD 의심은 해소됐고 불필요한044 ROM을 만들지 않았다. 전체 자연플레이·다른 성 방/실기·오디오/reset/savestate/최종 사람 번역 검토는 미수행이다. PAUSE/HOW TO CONTROL의 관측 밖 소비/전체 corpus의 전역 부재 증명도 주장하지 않는다.

다음 작업 하나: **현재043으로 ROM 없는 개발판 xdelta/Windows 적용 도구 패키지를 만들고 한글·공백 경로에서 실제 적용을 검증한다.** 사람 최종 검토/완주가 끝난 최종판으로 표기하지 않으며, 중단 지시 없이 이어간다.
