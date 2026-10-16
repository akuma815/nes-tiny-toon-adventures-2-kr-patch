# 작업64 — 카트 controller-only 추적 시도

[실행/검증 보고](../qa/reports/cart_pursuit064_validation.json), [정적A충전함수](../work/cart_control_001/A294_acceleration_candidate.json), [해제 후속도적용](../work/cart_control_001/velocity_apply_A0D1.json), [작업63 보존 감사](../qa/reports/cart_control063_session.json). ROM/SSOT 변경0이다.

같은043을새로부팅해18,000프레임 실행했다. 입력은기존메뉴controller와관찰한플레이어/0420type2E/2F 다른카트좌표에따른Dpad·정렬됐을때B·근처A짧은펄스였다. native입력방향table과heading0510을사용했고17999행의실제inputPolled 결정을기록했다. RAM/ROM/PC·phase·금액·체력쓰기·reset·savestate는없다. policy에서한방향의상반키를동시에누르지않는것도검사했다.

18,000프레임에서는카트phase5·체력1·history/Gold0·score210이다. 체력3→2→1 사망/재시작을포함하나native보너스20..24/클리어는없다. 플레이어가시도한입력으로클리어하지못했음을명시하며게임/번역결함으로단정하지않는다.6000 실제카트화면을직접확인했다.762PNG·4582runtime파일SHA·6096개1KiB CHR조각을043과검증했다. 전체육안검토나전체자연완주가아니다.

첫policy는B를속도조절에쓴가정과근처A8/30펄스를사용했지만A의충전·해제기전을먼저특성화하지않았다. sourceA294는A9/AA를20h단위로쌓고4단위로제한한다. heldA분기에서호출하며해제분기974C..9773는heading벡터와축적값으로A088을계산하고A0D1으로플레이어velocity04C0/D0·04E0/F0에더한다. ±4범위로제한한다. 다음은이소스근거로충전/해제를시험한다. B의공식행동이름·전체물리는아직확정하지않는다. NPC추적은경로/구멍회피를증명한것이아니다.

재현: [실행기](../scripts/run_cart_pursuit_qa.py) `--rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 18000 --inputs config/menu_cart_001.json`, [Lua](../scripts/trace_cart_pursuit_v1.lua), [검증기](../scripts/verify_cart_pursuit064.py). 입력정책은Lua SHA와실제cart_policy CSV로고정한다. 독립실험환경/실패를기존QA에덮어쓰지않는다.

sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 정적소스·완료runtime·매핑/입력검증·1장직접확인을구분한다. 새빌드/패치적용·PCM/청음·실기·최종사람검토는하지않았다. 원본/1편/모든이전자료/검토패키지를보존하고외부게시하지않았다.

다음 작업 하나: **A의소스확인된충전/해제를사용하고B를끄는새controller-only 추적입력으로충전·속도변화를기록하며클리어를시도한다.** 계속한다.
