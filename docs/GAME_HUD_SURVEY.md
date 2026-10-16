# 놀이기구 HUD 실제 소비 조사 — 작업43

현재039/등록45draft·9기술공유원천 유지. ROM/CSV 수정 및 신규 적용 검증은 없다.

[조사 원천·해시·표본](../extracted/graphics/hud_001/consumer.json), [실제 확대 화면](../extracted/graphics/hud_001/source_actual_6x.png), [재현 스크립트](../scripts/survey_game_hud.py). 원본 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,039 6b4b9150ff55140d959a12938dc549a58c8ebb6bdb0007c31f4a242e711f066b,CSV26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

정적: native font124/125와NT2F00/2B00, raw HUD template sourceD182 연결. LIFE/체력,SCORE/점수,TIME/시간,PTS./점,TICKET/티켓,G.TICKET/금티켓의 별도 그림초안 계획. 문단SSOT 등록54원천과 다른 그래픽 원천이다. 글꼴70..79 숫자·33 곱셈·하트와 틀은 별도 보호한다.

에뮬레이터: controller-only coaster12000/cart10000/train10000/water10000프레임, 자연 클리어/전체완주 아님. train활성IRQ5,다른세경로IRQ2,초기/종료 전환은IRQ0도 관측. 추가hud039_live_coaster4500에서FD08 뒤 font124/125 실데이터 전체 일치. screenshot4200과 IRQ/dump4200의 시각은 다르다. 마지막 시간 숫자 한 칸을 제외한4784픽셀 일치, 차이3픽셀은 이전숫자9 글꼴과 64픽셀 전체 일치하여 서로 다른 시각을 설명한다. 전체동시 HUD 일치 증명으로 과장하지 않는다. 실제 확대 LIFE/점수/시간/티켓 화면 직접검토.

원래 상단 영문은 5행만 보인다. 한글7행을 위해 IRQ의fineY2→0과 전용206/207을 시험할 계획이며, HUD 본문이2픽셀 아래로 이동하는 의도된 배치변경이다. NESdev [PPU scrolling](https://www.nesdev.org/wiki/PPU_scrolling)의 내부v/fineY 및타일주소 구성과 실제v=3F09/화면dy−5를 대조했다. 아직 새 배치의 성공/채택을 주장하지 않는다.

결과 CONGRATULATIONS/LIFE BONUS/CLEAR BONUS/TIME BONUS/NOW YOU GET/POINTS/YOUR POINTS 압축후보sourceCHR24A0B는 정적으로 확인했으나 실제 소비는 미확정이다. RAM25는 게임 중 다른 용도로 사용되므로 메뉴선택값으로 읽지 않는다. work/hud_survey_001의 이론 후보 PNG는 게임 근거가 아니다.

재현: `python scripts/survey_game_hud.py`는 새 추출 디렉터리를 만들며 기존43 결과를 덮어쓰지 않는다. 이미 생성된 결과의 재추출은 별도 이름으로 조사해야 한다. runtime 재현은run_menu_qa.py,039ROM,각menu_<ride>_001.json,trace_ui_consumers_v4.lua와 위프레임수;hudprobe는trace_hud_live_v1.lua/4500/coaster.

다음 행동 하나: 전용206/207 및fineY 배치를040개발초안으로 빌드하고 실제HUDowner픽셀·숫자/하트·게임상태·각IRQ시점을 검증한다. 바로 계속한다.
