# 작업67 — 지형·관성 제어 카트 조작 시도

[검증보고](../qa/reports/cart_policy067_validation.json), [실행기V2](../scripts/run_cart_geometry_policy_qa_v2.py), [고정Lua V2](../scripts/trace_cart_geometry_policy_v2.lua), [검증기](../scripts/verify_cart_policy067.py), [정책근거](../work/cart_geometry_001/policy067_basis.json).043/SSOT 변경0.

작업66의level0 분류표에서 벽 안272개 연결타일을 구했고 구멍 주위의회피영역을제외한경로를사용했다. 상대카트의구멍반대편으로접근하고 속도에따라방향/A충전·해제/B입력을조절했다.18,000프레임의새부팅을controller-only로실행했다.실제17,999행은approach8,652/push1,287/pit_avoid487/no_target1/menu7,572이다. menu는본정책의조건밖에서기존입력표를사용하는행으로,모두메뉴화면이라는뜻은아니다.

18k까지 실제카트플레이샘플에서체력3을유지했지만두적카트가남아history/금티켓0·보너스없음이다. 생존과클리어는구분한다.762PNG/4,582runtime파일/6,096mapped CHR조각을검증했고18000 실제화면을직접확인했다. 모든화면육안검토·경로완전성·자연완주를주장하지 않는다.

최초Lua에and24/or12 토큰공백누락이있어게임실행callback이시작하지않았다. 전용exe+전체Lua commandline을확인하고작업소유 Mesen만종료했다. [실패기록](../qa/reports/cart067_lua_compile_failure.json), [초기Lua](../scripts/trace_cart_geometry_policy_v1.lua), [초기실행기](../scripts/run_cart_geometry_policy_qa.py)와실패output를보존하고V2/새output로수정했다. 게임/ROM결함이아니다. SSOT조회일회성translation키는실제translation_ko로고쳤다.

추가로작업66의actor로그에서slot14/type2E가4050에state4·좌표131/260으로낙하하고뒤에id0이되는것을확인했다. 앞선65/66 입력은한적을제거했지만현재67은18k에둘다남는다. 다른전략을같은성공이라고합치지않는다. 최종제거/남은적/clear 소비기는다음추적으로연결한다.

재현: `python scripts/run_cart_geometry_policy_qa_v2.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 18000 --inputs config/menu_cart_001.json`. 새출력만사용하고이전환경/SHA를보존한다. sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

정적지형·runtime생존/매핑·직접1장검증을구분한다. 실제RAM/ROM/PC/phase/금액/체력/state/reset쓰기·새빌드/패치적용·PCM/청음·실기·최종사람검토는없다. 원본·1편·이전성공/실패/검토패키지보존·외부게시없음.

다음 작업 하나: **적카트 하나가 낙하한 기존controller 경로를 새로 실행해 state4→제거의 실제 쓰기 소비기를 추적한다.**
