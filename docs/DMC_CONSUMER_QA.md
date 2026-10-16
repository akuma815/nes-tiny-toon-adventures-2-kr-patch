# 작업62 — 실제 DMC 읽기와 새 PCM-CDL

[검증 보고](../qa/reports/dmc062_validation.json), [완료 실행 목록](../qa/reports/dmc062_runs.json), [최초 관찰기 timeout](../qa/reports/dmc062_observer_timeout.json), [고정2.1.1 CDL 타입 소스·SHA](../work/dmc_001/source_v4.json). ROM/SSOT 변경0이다. [작업61 보존 감사](../qa/reports/audio_sync061_session.json)를 통과했다.

최초V1은C000..DFFF의일반 코드/데이터읽기에도전체상태를직렬화해240초안에4,200프레임을마치지못했다. Mesen exit4294967295·미완료환경·부분데이터를보존했고게임실패로판정하지않았다. 새V2는네경로에서기록한DMC 지정주소범위C000..C880로관찰을한정한다. 다른조건이나ROM을수정하지않았다.

각QA폴더에검증된ROM의byteexact사본을만들고유일한TTA2_DMC062 이름으로실행했다. 기존동명CDL 누적을피하며initial_PRG_cdl의PCM bit0x80이모두0인지검사했다. 원본/043 코스터는controller-only4,200프레임씩실행했고APU디버그peek·savestate·RAM/PC/ROM/체력/금액쓰기나seed는없다. QA 사본은비공개QA에만있고dist의ROM없는원칙은유지했다.

native DMC currentAddr와양수bytesRemaining에일치하는실제ROM read콜백을기록했다. 양쪽59,247건의바이트값·순서·프레임·current주소·남은바이트·지정sample주소/길이·silence 상태가모두같았다. 모든값은실제매핑된ROM바이트와같다.59,004건의cycle도같고나머지243건은±2cycle다. CPU PC는1,237건다르므로전체CPU실행동일성을주장하지않는다.

최종nativePCM-CDL은원본PRGrelative1C1C0..1C880과0433C1C0..3C880의연속1,729바이트를확인했다. 모든cursor일치read주소는이새PCM영역에속하고소비바이트전체/SHA가같다. Mesen NesDebugger는DmaRead·IsDmcDma·PRG ROM인경우에만PcmData0x80을표시한다. Lua read콜백자체에는DMA종류가노출되지않으므로각콜백이API차원에서typed라고하지않는다. cursor/남은바이트 조건과새nativeDMC-DMA영역증거를연결한검증이다.

완료된두실행의3,330파일SHA를검증했다. 각실행은자기작업59 기준의오디오쓰기값/순서/cycle/프레임및world필드가같다. 초기/최종CDL·실제read CSV·유일QA ROM SHA·CLI 실제명령을환경에보존했다. [실행기V2](../scripts/run_dmc_qa_v2.py) `--rom <원본 또는043> --output qa/dialogue/<새ID> --frames 4200 --inputs config/menu_coaster_001.json`, [관찰V2](../scripts/trace_dmc_v2.lua), [순차실행](../scripts/run_dmc062_suite.py), [검증기](../scripts/verify_dmc062.py). 기각한V1[실행기](../scripts/run_dmc_qa.py)/[Lua](../scripts/trace_dmc_v1.lua)와미완료QA도보존한다.

정적소스·완료runtime·실제ROM읽기/매핑·typed영역/바이트검증이다. 새빌드/패치적용·실제청음·새장면직접육안검토는수행하지않았다. 원본SHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a, SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 음향결론은레지스터/음악24KiB/소비샘플보존이며, 작업61의출력위상차이와PCM/청음미확정은그대로다.

미수행: 모든후속DMC/음향·PCM/청음·전체자연완주/실기/최종사람검토. 원본·1편·현재/과거빌드/성공·실패·QA·검토패키지는보존하고외부게시하지않았다.

다음 작업 하나: **실제카트의플레이어·조작소비기를연결하고controller-only로자연클리어분기에접근한다.** 이전금액/체력/bonus/ending 진단seed와분리해계속한다.
