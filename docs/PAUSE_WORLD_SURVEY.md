# 일시정지와 세계 그래픽 조사 — 작업49

현재 채택 빌드는 **042**이며 이번 조사에서 ROM·IPS·번역 CSV를 수정하지 않았다. [042 보존 감사](../qa/reports/gameover_session_20261005.json)는 기존 산출물 474,037개, 동결 실행 파일 39,274개, 문서 링크 686개를 확인했다. 원본 SHA256은 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d, 042는 f4b4aa288e03bb30fd9532d95f823e34c4c620b20438feb2e1de0f67845cfc7b, IPS는 ebd250d9f9750a52f8720850c78cc13a86506e866e3fe834106bf42364221ef8이다. CSV는 26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27을 유지한다.

## 일시정지

native F935는 root4의 phase5에서 Start로 RAM55를 켠다. F413은 이후 bank32/33 A514로 우회한다. A51A의 여덟 포인터는 0..6에서 A536의 RTS, 7에서 A52A의 재개 처리다. 일시정지 중 새 글자·CHR·PPU 출력이 없다. 재개 시 F935가 06DE=7을 지정하고 A52A가 55·06DE·0425를 지운다. 이 코드와 포인터는 원본과 042가 같다.

[검증기](../scripts/verify_pause_survey.py)에서 공식 NMOS MPU를 사용한 D-clear 1,024개 CPU 사례는 일반 호출 65cycles, 종료 80cycles이며 글꼴 레지스터와 PPU/mapper 쓰기가 없다. 모델은 비동기 IRQ·실제 PPU를 포함하지 않으며 NES의 decimal-disabled 동작과 구분해 D-set을 제외했다.

별도 Mesen coldboot 네 경로는 컨트롤러만 사용했다. 3000 Start, 3300 Start로 멈춤·재개를 기록했다. 롤러코스터는 실제 진입이 3001, 다른 세 경로는 3000이었다. 각 진입부터 종료까지 A514 호출은 정확히 연속이며 마지막 호출만 subphase7이다. 3030/3150/3270의 전체 RGB 화면이 경로별로 같고, RAM55=1에서 3330의 0으로 돌아왔다. 관측 기간에 모든 CHR 포트에서 bank120/121 선택은 0회였다. 1,194화면·동결 파일 7,204개를 확인했고 각 놀이기구 3150 실제 화면을 직접 검토했다. [상세 결과](../qa/reports/pause049_survey.json), [실행 묶음](../scripts/run_pause_survey_suite.py).

원본 PAUSE 그림이 다른 엔진에서 미사용이라는 전체 증명은 아니다. 소비가 연결되지 않은 그림은 아직 삽입 대상에서 보류한다. 초기 검증기의 고정 300호출·마지막 subphase0 가정은 실제 write55 및 종료7 근거로 정정했다. [실패와 정정](../qa/reports/pause049_model_error.json)을 남겼으며 ROM 결함이 아니다.

## 기차 간판 후보

새 컨트롤러 입력 두 경로는 18,000/9,000프레임을 실행했지만 각각 첫 체력 소진으로 지도에 돌아갔다. 두 번째 경로는 이후 컨트롤러 입력으로 재입장했다. 자연 완주·간판 표시 성공으로 주장하지 않는다. [첫 경로](../qa/dialogue/world042_train_controller/environment.json), [조정 경로](../qa/dialogue/world042_train_controller_v2/environment.json), [입력](../config/world_train_controller_002.json)을 보존했다.

기차 전용 IRQ FBE3는 FBF0/FBF9에서 72/74를 선택하고 다음 1KiB 뱅크도 지정한다. FC1C에서 실제 PRG mapping·CHR 상대12000/12800을 4,566회 기록했다. 중간 IRQ에서 채집한 실제 4KiB 152개는 원본 32010..33010과 전체 바이트가 같다. [소비 결과](../qa/reports/train049_font_consumer.json), [추적 코드](../scripts/trace_world_v2.lua).

원본 페이지에 있는 MONTANA LAND/R.R.는 지도 제목과 다른 그래픽이다. 실제 글자 배치·팔레트·화면 RGB는 아직 연결하지 않았다. [NT 분석 이미지](../work/train_engine_001/NT2000_actual_indices_analysis.png)는 실제 NT/CHR를 임의 색으로 해석한 설명용이며 실제 화면 캡처가 아니다. HOW TO CONTROL도 정적 후보로 남는다. 기존 타이틀의 PUSH START·법적 표시 유지 결정은 [타이틀 기록](POC_TITLE.md)에 따른다.

## 재현과 다음 행동

`python scripts/run_pause_survey_suite.py`의 출력 경로는 최초 실행 전용이다. 재현은 `run_pause_qa.py --rom build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes --output <새경로> --frames 4500 --inputs config/world_train_pause_001.json --script scripts/trace_pause_v1.lua`처럼 새 경로를 사용한다. CPU/기존 QA 검증기도 PASS 보고서를 덮어쓰지 않으므로 재검증 시 새 보고 경로를 사용하는 복제 실행을 남긴다. 기차는 `run_world_qa_v2.py`와 world_train_controller_002 입력으로 9000프레임을 기록한다. 실제 환경 파일에 모든 실행 파일·입력·출력 해시가 있다.

[자산](../manifests/pause_world_assets.json), [이번 작업 보존·링크 감사](../qa/reports/pause_world049_session.json). 빌드/패치 적용은 이번 작업에서 수행하지 않았으며 042의 기존 PASS를 계승한다. 전체 corpus·자연 플레이·오디오·실기·최종 사람 검토는 남아 있다.

다음 작업 하나: **기차 native phase5에서 정상 최대 체력3만 보충하는 명시적 진단 경로로 간판 NT·팔레트·실제 RGB를 연결한다.** 컨트롤러 경로와 분리하고 매 보충 시점·값·조건을 기록한다. 위치·시간·phase·PC·ROM은 변경하지 않는다. 소비가 확인되면 전용 글꼴로 간판을 한글화한다. 계속 진행한다.
