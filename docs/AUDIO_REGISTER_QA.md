# 작업59 — 원본 일본판/043 오디오 레지스터 비교

[최종 비교 보고](../qa/reports/audio059_validation_v2.json), [첫 검증기 timing 상한 오류](../qa/reports/audio059_timing_model_error.json), [APU 상태 차이 전체 기록](../qa/reports/audio059_APU_state_observation.json), [초기 시점 조사](../work/audio_001/water_initial_timing_observation.json). **레지스터 비교는 통과했으나 네 경로의 APU 상태 동일성·실제 청음은 미확정**이다. 새 ROM을 만들지 않았고043/SSOT/원본/1편을 보존했다.

원본과043을 같은 설정·controller 일정으로 코스터/카트/기차/급류 각9,000프레임씩 새로 실행했다. RAM/PC/ROM 수정·체력/금액 seed·savestate는 없다. APU4000..4013/4015/4017과 고정2.1.1 VRC7 decoder의 FM/제어 쓰기를 기록했다.4014 DMA와4016 controller는 오디오 쓰기에서 제외했다. PRG 확장에 따른 물리주소+20000을 별도 확인했다.

각 경로의 쓰기는22,792/25,281/19,946/20,145건으로 합계88,164쌍이다. 값·순서·프레임·CPU PC·root/phase/course/pause가 모두 같다. VRC7 제어 쓰기는 경로별5회이고 FM 쓰기는 기록 구간에서0이다. 전체 ROM에 FM이 없다는 주장은 하지 않는다. 세 경로에서66건의CPU시점만1..4cycle 다르다. 급류는5,371건이 달라지며 절대최대8cycle다. 처음 비교기에서 코스터/카트의4cycle 상한을 전체 경로에 잘못 적용해 실패했다. 그 검증기·SHA·실패 근거를 보존하고 V2는 값/순서/프레임 비교와 시점 차이를 분리한다.8cycle을 음질 동등성의 허용치로 선언하지 않는다.

코스터435/카트462/기차435의 APU 상태는 모든 키가 같다. 급류462장 중157개 시점에서 APU timer/sequence/noise/DMC 등의 내부 값이 다르다. 첫 차이는4320의 메뉴복귀 후이고 CPU cycle·masterClock·PPU masterClock은 그 시점에 같다.4301부터 오디오 쓰기 cycle이 달라진다. 상태 차이를 무시하거나 청음 통과라고 해석하지 않는다. APU 갱신/관찰 시점과 실제 출력의 관계를 다음 작업에서 조사한다.

[고정2.1.1 DMC 구현과 SHA](../work/audio_001/source.json)의4012/4013 공식을 사용해 기록된 샘플 지정 주소/길이를 복원했다. C000의 실제 매핑은 각 화면에서 원본1C000/0433C000이었다. 모든 지정 샘플의 ROM 바이트/SHA가 같다. 이것은 지정한 샘플과 화면 시점 매핑의 보존이며 각 DMC fetch 또는 PCM output을 직접 기록한 것은 아니다.

총3,588PNG(원본 측 포함)·21,608실행 파일 SHA·28,704개1KiB CHR 조각을 각 원본/043 ROM과 대조했다. 게임 단계/체력/통화/이력 등의30프레임별값은 같다. headfont/한글 lowerfont는 다르고 일부idle PC도 다르므로 전체CPU/RAM 동일성은 주장하지 않는다. 이 작업에서 새 화면의 직접 육안 검토나 실제 청음은 하지 않았다. 빌드/적용은 동결 작업55 결과를 참조하며 새 빌드/적용을 수행하지 않았다.

재현: [실행기](../scripts/run_audio_qa.py) `--rom <원본 또는043> --output qa/dialogue/<새ID> --frames 9000 --inputs config/menu_<ride>_001.json`. [관찰 Lua](../scripts/trace_audio_v1.lua), [순차 실행기](../scripts/run_audio_remaining_suite.py), [V2 검증기](../scripts/verify_audio059_v2.py), [기각한 V1](../scripts/verify_audio059.py). 기존 경로/보고서를 덮어쓰지 않는다. source ROM SHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043 SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a, SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

미수행/미해결: 급류 복귀 후 APU 위상 차이의 원인/실제 출력 영향, PCM/청음, 모든 음악·효과음, 전체 자연완주, 실기, 최종 사람 번역 검토. 패키지55/검토자료56은 동결했고 외부 게시하지 않았다. 최종 배포를 승인하지 않는다.

다음 작업 하나: **급류 실패/메뉴복귀에서 처음 APU 상태가 달라지는 지점을 CPU/APU 갱신 소스와 실제 이벤트로 연결해, ROM 수정이 필요한지 판단한다.** 계속 진행한다.
