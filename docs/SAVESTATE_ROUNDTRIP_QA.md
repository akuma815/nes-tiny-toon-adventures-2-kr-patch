# 작업58 — 같은 043 빌드 저장 상태 왕복

[검증 보고](../qa/reports/savestate058_validation.json), [실행 환경](../qa/dialogue/state043_coaster_roundtrip/environment.json), [고정 버전 소스와 SHA](../work/savestate_001/source_records.json). 원본·043 ROM·SSOT 변경 0. 작업57의 [23,312개 파일 보존 감사](../qa/reports/runtime057_session.json)도 통과했다.

Mesen 2.1.1 공식 Lua API가 요구하는 exec 메모리 콜백 안에서 실제 코스터 HUD IRQ FCF1, frame3000에 createSavestate를 호출했다. frame3600의 같은 콜백에서 같은 043 상태를 한 번 loadSavestate했다. 임의 RAM/PC/ROM 쓰기는 없다. CPU cycle이107231389에서 저장 시점89363093으로 복원됐고9,000프레임까지 실행을 마쳤다. API 호출에서는 stateLoaded 이벤트가 관찰되지 않았다. 공식 API의 이벤트 설명은 수동 로딩이며, 검증은 이벤트 발생을 가정하지 않고 실제 복원 상태와 반환을 확인했다.

RAM2KiB·PPU16KiB·OAM256B가 정확히 같다. getState의826개 키 중9개만 다르다. 모두 OPLL 홀수 slot의update_requests가0에서255로 바뀐 것이다. [2.1.1 Serializer](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Shared/Utilities/Emu2413Serializer.h)가 로딩 시OPLL_forceRefresh를 호출하고, [동일 버전 구현](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/Shared/Utilities/emu2413.cpp)은18개 slot 모두에UPDATE_ALL=255를 요청한다. 저장 시 짝수 slot은 이미255였다. 검증기는 이18개 필드의 정확한 기대값만 허용하며 그 밖의 모든 키와 값은 같아야 한다. 일반적인 오디오 차이를 무시하는 검사는 아니다. 초기 관찰 [미확정 기록](../qa/reports/state058_cache_field_observation.json)은 당시 상태로 보존했다.

435PNG·2,633실행 파일 SHA와3,480개1KiB CHR 매핑을043과 대조했다. 복원 후3630/3660/3690의PNG·RAM·PPU·OAM은 기존043 실행의3030/3060/3090과 각각 byteexact다.3630의 코스터와 한글HUD를 직접 확인했다. 전체435장을 직접 육안 검토했다고 주장하지 않는다.

재현: [실행기](../scripts/run_savestate_qa.py) `--rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 9000 --inputs config/menu_coaster_001.json`. [Lua](../scripts/trace_savestate_v1.lua), [검증기](../scripts/verify_savestate058.py). 검증 보고와 QA는 덮어쓰지 않는다.

정적 소스 확인·에뮬레이터 상태/매핑 검증·3시점 byteexact·1장 직접 확인을 구분한다. 빌드/적용은 작업55에서 검증한 동결043을 사용했으며 이번 작업에서 새 ROM을 만들지 않았다. ROM SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`, SSOT SHA `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27`.

미수행: 다른 빌드의 저장 상태 호환성, 모든 저장 상황, 오디오 PCM 동일성/실제 청음, 자연 전체 완주, 실기, 최종 사람 번역 검토. 개발판 패키지와 사람 검토자료는 그대로 보존한다. 외부 게시하지 않았다.

다음 작업 하나: **원본 일본판과043을 같은 controller 일정으로 실행해 APU/VRC7 레지스터 쓰기 값·순서·시점의 보존 여부를 비교한다.** 중단 지시 없이 이어간다.
