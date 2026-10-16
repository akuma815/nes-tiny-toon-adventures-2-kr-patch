# 작업95 — 현재047 성 입구 저장상태/리셋 검증

현재047 ROM/CSV/검토패치를변경하지않았다. ROM82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10/CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556, 원본/1편/모든과거증거유지. [독립검증](../scripts/verify_state095.py), [보고서](../qa/reports/state095_validation.json).

실행1: 같은047 빌드 성입구native NMI top FD9E의1920frame에서상태를만들고2190에서한번불러왔다. 실제CHR상단175/176 주소2BC00/2C000과CPUcycle57177337 복원을확인했다. serialized saved_machine와restored_machine의RAM2048/PPU16384/OAM256전체byte exact, 실제폰트175176도ROM2KiB와exact다.826상태키 중817은동일하고9개OPLL oddslot update_request의0→255만 Mesen2.1.1 소스의forceRefresh와일치한다. 저장create 이전과직후11개APU차이는 동일버전소스의binary Serialize EndFrame 요구로구분한다. 이전작업85의9개APU값차이를그대로가정하지않았다. 해당동결소스해시와같은실행파일을확인했다.

후속게임실행: postload2220/2250/2280의실제PNG/RAM/PPU/OAM/주소mapping15파일이 현재047 native기준1950/1980/2010과byte exact다. 이전046 화면을현재047실행으로사용하지않았다. [복원후실제2220](../qa/dialogue/state095_gate047/frame_02220.png)을직접봤다.

실행2: 대사대기3000frame에서console reset1회를요청했고실제reset3001을기록했다. 숫자seed/ROM·PC수정/상태로드없다. 반복controller입력으로타이틀부터성입구에재진입하여4920/6000 nativeNT코드와두행RGB를독립재구성해exact확인했다. head/lowerfont175가유지되며 [재진입4920](../qa/dialogue/reset095_gate047/frame_04920.png)을직접봤다. 한국어문장/숫자4/색/줄위치 유지.

570실제PNG 및4560개mapped CHR1KiB chunk가현재ROM과exact, 두환경의3457파일SHA/정상종료를검증했다. [저장환경](../qa/dialogue/state095_gate047/environment.json)/[리셋환경](../qa/dialogue/reset095_gate047/environment.json), [저장trace](../scripts/trace_savestate047_gate_v1.lua)/[리셋trace](../scripts/trace_reset047_gate_v1.lua). 이는 같은047 특정대기상태/1회리셋증거이며 빌드간상태호환·모든저장상황·전게임완주·실기·PCM동일성/청음·최종사람검토를뜻하지않는다.047패키지93의‘당시신규reset/state미수행’은동결기록으로남기고본작업을추가근거로연결한다. 최종카페완성작업기/외부게시 없음.

재현: `python scripts/run_savestate047_gate_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새state폴더 --frames 3000 --inputs config/state095_castle_001.json`; 종료후 `python scripts/run_reset047_gate_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새reset폴더 --frames 6000 --inputs config/reset095_castle_001.json --reset-frame 3000`. privateMesen실행은순차. [동결manifest](../manifests/state095_assets.json).

다음 작업 하나: 원본bank61 POW 후보타일을 sprite데이터/뱅크선택/호출루틴까지 정적으로역추적해 기존부분관측이놓친 실제소비조건을좁힌다.
