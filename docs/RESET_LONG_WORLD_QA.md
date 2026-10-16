# 작업57 — native reset/재부팅/재진입과 네 controller 장기경로

[검증 보고](../qa/reports/runtime057_validation.json), [reset HUD 픽셀](../qa/reports/reset057_HUD_pixels.json), [anchor 설명 정정](../qa/reports/reset057_anchor_metadata_erratum.json). ROM/SSOT 변경0이며 검토용55 패키지는 동결했다. [55 보존 감사](../qa/reports/review043_package055_session.json), [56 보존 감사](../qa/reports/translation_review056_session.json)도 통과했다.

[공식 Mesen2.1.1 Lua API](https://raw.githubusercontent.com/SourMesen/Mesen2/2.1.1/UI/Debugger/Documentation/LuaDocumentation.json)의reset을 사용했다. [고정버전 원천·SHA](../work/reset_001/API_source.json)를 보존한다. CPU PC/ROM/RAM을 임의로 쓰지 않았으며 console reset과 controller 입력만 수행했다. stateLoaded 이벤트가 생기면 거절하는 관찰기를 사용해 이 경로에서 세이브 로딩이 없음을 확인했다.

043과 이전039를 같은9,000프레임/설정/입력으로 새로 실행했다. 3600프레임 native root4/phase5/course0에서reset을 요청했고3601프레임 실제reset 이벤트가발생했다. KONAMI/타이틀/홈이 재부팅되고 추가controller로코스터에재진입했다. [043](../qa/dialogue/reset043_coaster/environment.json), [039기준](../qa/dialogue/reset039_coaster_reference/environment.json). 두 실행의reset이벤트PC/cycle/context와30프레임별world상태는byte단위로같다.

435쌍의모든RAM/OAM/NT/palette가같고342전체PNG도같다.93장HUD만다르며7행한국어110,856픽셀과원래하트/점수/시간/티켓/금티켓숫자196,416픽셀을의도한2px이동후정확히대조했다. y0..189플레이영역 변경0이다. 이HUD모델은기존coastergeometry190과실제source/newglyph RGB를사용했다. 재사용함수의anchor_source문자열이직전IRQ수집이라고표현된부분은별도정정했다. 작업57은전체IRQ를새로기록하지않았으며reset이벤트/상태와실제glyph대조범위만주장한다.

네놀이기구043각18,000프레임을새부팅/controller-only로실행했다. 수동금액/체력/phase/PC/ROM쓰기나세이브 로딩은없다. coaster/train/water는기록한입력으로실패후홈복귀했고cart는18,000에서도native플레이중이었다. native보너스20..24/금티켓취득/클리어증거는없다. 입력이충분한공략이아니었음을구분하고전체완주를주장하지않는다. [네실행환경목록](../qa/reports/long_world057_runs.json), [연속입력실행기](../scripts/run_long_world_suite.py).

두reset측+네장기경로의합계3,873PNG/23,294runtime파일SHA,30,984개1KiB CHR맵핑조각을해당실제ROM과비교해통과했다. 합계에는비교기준039의435장도들어있으므로전부043화면이라고하지않는다. cart12000·리셋후코스터설명5760·리셋후최종홈9000을직접확인했다. 다른모든화면을사람이검토했다고주장하지않는다.

재현: [실행기](../scripts/run_reset_qa.py) `--rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 9000 --inputs config/coaster_reset_001.json --reset-frame 3600`. [Lua](../scripts/trace_reset_v1.lua), [검증기](../scripts/verify_runtime057.py)를보존하고새경로만쓴다. 장기경로는기존world_{ride}_controller_001.json으로18,000프레임씩순차실행한다.

현재43ROM SHA `087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a`, SSOT SHA `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27` 그대로다. 미수행범위는모든reset상황/세이브상태호환성·전체자연플레이/모든방·오디오·실기·최종사람번역/명칭검토·전역corpus폐쇄다. 원본·1편·모든과거증거·55 ZIP/56검토자료를보존하고외부게시하지않았다. 이전패키지의미수행설명은그패키지를만든시점의기록으로보존한다.

다음 작업 하나: **공식API의exec조건으로같은043세이브상태를생성/재로딩해glyph/mapper/CPU/RAM/PPU/OAM왕복을검증한다.** 이전빌드와의세이브상태호환성으로확대해말하지않으며중단지시없이계속한다.
