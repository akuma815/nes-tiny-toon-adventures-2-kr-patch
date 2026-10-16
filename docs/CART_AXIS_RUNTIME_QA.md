# 작업71 — 카트 좌표축 정정·36k 자연 경로

[원본CPU/실제이동 검증](../qa/reports/cart_axis071_cpu.json), [36k 검증](../qa/reports/cart_runtime071_validation.json), [재현CPU 스크립트](../scripts/verify_cart_axis071.py), [실행기](../scripts/run_cart_rounds_qa_v3.py), [고정controller](../scripts/trace_cart_rounds_v3.lua), [runtime검증기](../scripts/verify_cart_runtime071.py), [40속도사례/정정근거](../work/cart_geometry_001/axis071_native_velocity_proof.json). ROM/SSOT변경0.

기존작업63 native_direction_table.json의rawvector첫쌍을X·둘째를Y로이름붙인것은반대였다.99B0/1은Y,99B2/3은X이며nativeF062/F111은각각Y/08/09, X/0A/0B를만들고EE2F/EE4D는각좌표에더한다. logger의4C속도X/4E속도Y 자체는맞았다. 기존controller는방향키이름을그대로world방향으로가정해회전이잘못됐다. 원본A088/A0D1의8heading×5충전40사례와99D0 button표를실행해확인했다. 작업63 실제right held52=1인3330→3360도X319 고정/Y271→286으로일치한다. 기존table·문서·policy·실패는수정하지않고이작업에서정정한다.

world오른쪽/왼쪽/아래/위는controller mask4/8/1/2, 아래오른쪽/아래왼쪽/위오른쪽/위왼쪽은5/9/6/A다. 이는카트원본의좌표대응이며ROM입력매핑을바꾼것이아니다. nativelevel0의성공입력은그대로두고level1/2 정책만회전을교정했다. 경로lookahead는선분상의중심과±8 probe를추가했다.

새36,000프레임실행에서first4969 mask는작업70 V2와모두같고4970 level0→1을재현했다. level1에서한적을제거했으나마지막적을남기고19110 phase11(hex) HUD00:00, phase09/0A를거쳐19680 홈root08/phase13으로돌아왔다. 체력3/history·Gold0이다.24000 실제화면은게임오버대기가아닌지도/선택홈임을직접확인했다. 이전root08/phase13이라는숫자만으로게임오버최종화면이라고말하면안된다. life0실패경로와이번timeout·홈복귀를구분한다. 마지막홈에서042F=FF등배열값은플레이어/선택화면의scratch 재사용이므로게임중남은적타입으로해석하지않는다. 종료과정의전체actor초기화도적이구멍에떨어진증거로쓰지않는다.

8,184고정runtime파일/1,362PNG/10,896CHRmapped조각/70,737actualquery·28,616고유원본CPU입력을검증했다. 0/1구간실제소비를확인했고level2는아직정적뿐이다.19110/24000 actual을직접확인했다. 모든화면육안검토는아니다. Native collision probe는A142..A212에cardinal±15/diagonal±10으로더넓다. 현재±8 선분검사는카트몸체모서리간섭을충분히피하지못할수있어다음에는8픽셀경로와전체body probe를쓴다. 정책원인전체를완전확정하거나ROM을수정하지않는다.

재현: `python scripts/run_cart_rounds_qa_v3.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 36000 --inputs config/menu_cart_001.json`. 최대36k/CLI600초/전용hidden실행,실제inputPolled결정과Lua SHA로고정한다. `verify_cart_axis071.py`와`verify_cart_runtime071.py`는최초고정출력을덮어쓰지않는다. 일회성rg에서PowerShell glob 미확장오류가있었고후속검색은-g패턴으로분리했다.

sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 정적원본CPU·runtime/world/매핑·직접2장검증을구분한다. 실제RAM/ROM/PC/phase/금액/체력/state/reset쓰기·새빌드/적용·PCM/청음·실기·3구간완료/최종사람검토없음. 원본/1편/모든이전성공·실패·검토패키지보존·외부게시없음.

다음 작업 하나: **8픽셀경로를원본cardinal±15·diagonal±10 body probe로검사해level0 성공입력을보존하고나머지구간을다시시도한다.**
