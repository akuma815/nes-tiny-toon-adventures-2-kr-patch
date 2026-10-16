# 작업122 — 강 actor2 소멸 원인과 투영 모델

[추적](../scripts/trace_river122_v1.lua), [최초 실행기](../scripts/run_river122.py), [수정 실행기](../scripts/run_river122_v2.py), [최초 검증기](../scripts/verify_river122.py), [v2 검증](../scripts/verify_river122_v2.py), [결과](../qa/reports/river122_validation_v2.json), [실행 환경](../qa/dialogue/river122_actor2_current047/environment.json).

## 실제 상태 쓰기

현재047의121과같은두조건주입을3300프레임실행하면서actor2의0402/0422쓰기만읽기전용으로관측했다.진단변경을늘리지않았다. 121의동일시점RAM/PPU/OAM/매핑620파일·core155·전체PNG155정확히같으며nativecallback434행도종료시점전범위에서같다.

3000프레임A617에서0422=2,A63F에서0402=ED를썼다.그뒤nativebank36/95BF의STA0400,Y(Y=2)가ED를0으로바꿨고fixedF206/F20C가art/state를지웠다. 기록6쓰기의직전전체RAM·CPU레지스터·physicalcode로source/current각6CPU조건쌍을재생했으며store의주소·값·cycle·다른RAM보존이같다. callbackPC는storeoperand를읽은다음주소라직전3바이트의명령경계로확인했다.

95xx투영은object좌표에서viewport필드68/6B,69/6D를뺀다.실제관측의수직차0126은95BF에서art를숨긴다.수평차0175·0572=0은960F/9614→F204정리로actor상태도지운다. **이번두조건진단의nativeculling을확인한것이며ROM/글꼴손상이나자연게임장면결함이아니다.**

## 다음 진단을 위한 새 예측

관측RAM을9582에공급한source/currentCPU모델은같이95BF/F204를거쳐소멸했다.별도합성viewport68=01/6B=40/69=0C/6D=80조건은원본이정한actor좌표를바꾸지않고ED/state2를보존하며sprite좌표64/144를계산했다.이두projection조건쌍은RAM/레지스터/cycles가같다.후자는아직실제표시증거가아니며다음진단의정확한가설이다.가설근거없이조건을무작정바꾸지않는다.

## 실패·인계

Mesen자체는exit0/3300완료였으나최초Python실행기의후검증이상속Lua의river121_injection.csv를river122이름으로읽으려해실패했다. [후검증 실패](../qa/reports/river122_v1_postflight_error.json)를보존하고실제파일을별도검증했다.v2실행기는올바른이름과3300입력한계를사용한다.에뮬레이터를재실행하지않았다.

최초검증기의<=3300callback비교는짧은실행이EndFrame3300에종료되고121이그뒤CPUcallback을계속기록하는경계를놓쳐실패했다. [관찰](../qa/reports/river122_verifier_v1_observation.json)을보존하고v2의<3300범위를대조했다.그관찰문장의추가callback3개표현은실제1개(435−434)로 [정정](../qa/reports/river122_errata.json)했다.동결파일/게임상태를수정하지않았다.

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지.새runtime/추적기/실행기2개/검증기2개/실패·정정/v2보고/문서·인계/journal/canonical/manifest작성.이번은실에뮬레이터읽기전용원인관측·제한된CPU재생이며새build/apply·직접장면검토는없다.원본/1편/기존QA보존.전역corpus·자연전체완주·사람최종검토·실기/청음·정식배포는미완료이며카페완성작업기는전체완료후다.

재현은`python scripts/run_river122_v2.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새관측폴더`로새경로를쓴다.검증기는동결기존경로/보고서를거부하므로복제본에새경로를지정한다. [동결 자산](../manifests/river122_assets.json), 감사 경로 `qa/reports/river122_session.json`.

다음 작업 하나: source/current047에서같은native생성뒤9582/actor2투영직전viewport68=01/6B=40/69=0C/6D=80을한번명시적으로주입해,CPU모델의screen64/144예측과실제ED/EE/EF·CHR61소비를대조한다.진단카메라이며자연후반·완주로보고하지않는다.
