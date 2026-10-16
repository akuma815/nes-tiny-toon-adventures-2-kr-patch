# 작업85 — 현재046 저장 상태 복원과 리셋 재진입

[검증 보고서](../qa/reports/state085_validation.json). Mesen2.1.1의 실제 기차 NMI top FD9E,3330프레임에서 같은046 상태를 생성하고3600프레임의 같은 exec 콜백에서 한 번 복원했다. RAM2KiB/PPU16KiB/OAM256B는 byte exact이며 PPU 상단2KiB가046의 전용 STOP224/225와 정확히 같다. 복원 직후 getState826개 키 중817개는 그대로이고9개 OPLL 홀수 slot 갱신 요청만 소스에서 요구한0→255로 변했다. 전체18개 해당 필드의 기대값과 그 밖의 모든 키를 검사했다. 임의 RAM/ROM/PC 조작은 없다.

복원 후3630/3660/3690의 실제PNG·RAM·PPU·OAM·매핑15파일은 기존046의3360/3390/3420과 byte exact다. [복원 후 정지 표지](../qa/dialogue/state085_train046_v2/frame_03630.png)를 직접 확인했다. CPU cycle99167971과 뱅크38000/38400도 저장 시점으로 복원됐다.

리셋은 별도 실행이다.3600프레임에 console reset을 요청하고3601에 실제 reset 이벤트를 한 번 관측했다. 저장 상태 로딩은 없었다. 동일 컨트롤러 일정을3600프레임 뒤 반복해 기차에 다시 진입했다. [재시작 안내](../qa/dialogue/reset085_train046/frame_06300.png)의 시작!과 [재진입 표지](../qa/dialogue/reset085_train046/frame_06930.png)의 정지를 직접 확인했다.7200까지 native root4/phase5/course2와 STOP224가 유지됐다.

시행착오/정적 소스 확인: v1은 createSavestate 호출 전 getState와 복원 후 상태를 비교해 APU9개 필드와 OPLL9개 필드의 차이를 관측했다. [당시 기록](../qa/reports/state085_precreate_observation.json)을 보존했다. 고정 [Mesen2.1.1 NesApu::Serialize](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/APU/NesApu.cpp)는 binary 저장/로딩 때 EndFrame을 호출하므로 호출 전 상태를 저장된 상태로 취급할 수 없었다. [로컬 소스/해시](../work/state085_serializer/source_records.json)를 기록하고 v2에서 생성 직전·생성 직후·복원 후를 각각 덤프했다. APU9개 차이가 생성 직전→직후에서 정확히 재현됐고, 생성 직후→복원 후에는 OPLL9개 외 모두 일치했다. 폭넓은 오디오 차이를 무시한 검사가 아니다. OPLL forceRefresh/UPDATE_ALL=255는 [고정 소스](../work/savestate_001/source_records.json)로 확인했다.

총3실행1006PNG/8048개1KiB CHR 매핑을046 ROM과 대조했다. runtime 동결 파일6096개를 해시 확인했다. v1관측/v2해결/reset 각각 환경을 보존했다. 사람 직접 육안은 위3장면과 리셋 후 KONAMI 화면을 확인했으며1006장 전수 육안 검토를 주장하지 않는다. 이전043 검증을 현재046으로 대신 주장하지 않았다.

원본/046/번역CSV 변경 없으며 새빌드나 패치 적용은 하지 않았다. 현재 검토 ZIP의 설명은 작업83 당시 한계로 동결 유지한다. 모든 저장 상황/다른 빌드 상태 호환성/PCM 동일성·청음/실기/전체 자연 완주/최종 사람 검토/전역 corpus 폐쇄는 미수행이다.

재현: [v2 실행기](../scripts/run_savestate046_qa_v2.py) `--rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_train_001.json`; [리셋 실행기](../scripts/run_reset046_qa.py) `--rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/다른새폴더 --frames 7200 --inputs config/reset085_train_001.json --reset-frame 3600`. [검증기](../scripts/verify_state085.py), [동결 파일/SHA](../manifests/state085_assets.json).

다음 작업 하나: 카트 두번째 구간의2F 적 이동/속도 루틴과 기존policy의 B 감속 조건을 실제 소비 기준으로 비교한다. 같은 실패 입력을 반복하기 전에 아직 미확정인 속도 가설부터 검증한다.
