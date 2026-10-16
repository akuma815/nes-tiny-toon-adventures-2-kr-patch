# 작업63 — 카트 입력/플레이어 좌표 소비기

[최종V4 검증](../qa/reports/cart_control063_validation_v4.json), [저장명령 모델 실패](../qa/reports/cart063_store_model_error.json), [잘못된RMW설명 원문](../qa/reports/cart063_RMW_model_error.json), [실제Y-index 정정](../qa/reports/cart063_store_Yindex_erratum.json). ROM/SSOT 변경0이며 [작업62 보존감사](../qa/reports/dmc062_session.json)도통과했다.

controller-only4,800프레임 두실행에서방향키/A/B를각120프레임씩분리했다. Native카트phase5→0D에서체력3→2가되고phase1/4를거쳐phase5로재시작했다. 금액/체력/phase/ROM/PC 쓰기·savestate·seed는없다. Gold/history0으로클리어증거는없다.3390/3840/4500 실제카트화면을직접확인했다. 이전18k right+A 반복으로클리어하지못한것과분리한다.

최초추정F7/F8·3A/3B의held입력패턴검색은소비기를찾지못했다. RAM52와실제read콜백으로연결했다. right01/down04/left02/up08/A80/B40이다. Bank38의95E9/9673/970F/9718/982F/9846는52를읽고9735는edge50을읽는다. 프레임·PC다음명령·실제PRGoffset·직전A552/A550 명령을확인했다. 고정FFB6/FFBA의포트복사와게임소비기는구분한다. [실제입력read로시작한listing](../work/cart_control_001/validated_joy_reads_disassembly.json), [네방향/대각선벡터table](../work/cart_control_001/native_direction_table.json)를보존했다. A/B의세부행동을공식조작법으로확정하지않는다.

초기047E/F/049E/F는다른객체/좌표fraction 관찰이었다. 플레이어는direct0400 sprite·0470 Xinteger·04A0 Yinteger 소비기로연결됐다. 좌표갱신3,519건은absolute STA8D, absX STA9D, absY STA99를opcode/실제operand+X/Y로검증했다. 대부분은고정EE3F/EE5D의direct저장이며공통3B helper와혼동하지않는다. V1의모든저장을X0 indexed로가정한검사와V2의STA99누락이실패했다. V3는출력을읽기전에RMW라고추정해또실패했고그설명도틀렸다. 실제99 STAabsY를확인한V4/별도erratum이정정한다. 게임/ROM실패나수정으로표현하지않는다.

[초기ADA0 선형listing](../work/cart_control_001/position_consumer_initial_disassembly.json)은prefix의정렬이검증되지않은후보이며최종근거로사용하지않는다. 실제콜백으로연결한read/write명령만채택했다. Native객체포맷은Xint0470/Xpage0480, Yfraction0490/Yint04A0/Ypage04B0이고공통좌표코드는Xpage240/Ypage256을사용한다. 다음policy에서화면상의개체추정이아닌실제좌표를사용한다. 특정캐릭터이름은단정하지않는다.

3,885runtime파일SHA·644PNG·5,152개의1KiB CHR조각을실제043과비교했다. V1/V2의world CSV와모든화면시점RAM도byteexact다. nativecontroller38/39와movement3A/3B의32KiB는원본10010..18010/04330010..38010 전체바이트/SHA가같다. 새빌드/패치적용·PCM/청음·전체자연완주·실기·최종사람번역검토는수행하지않았다. 이미보기는3장한정이며전부육안검토로표현하지않는다.

재현: [실행기V2](../scripts/run_cart_control_qa_v2.py) `--rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 4800 --inputs config/cart_control_probe_001.json`, [LuaV2](../scripts/trace_cart_control_v2.lua), [검증V4](../scripts/verify_cart_control063_v4.py). V1/V2/V3검증기와실패원문은보존하며새보고/폴더만쓴다. sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a, SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

미수행: 자연클리어/보너스/Gold획득, A/B세부역할완전특성화, 음향위상/청음·실기·최종사람검토. 원본/1편/현재/과거자료·패키지55/검토56을보존했고외부게시하지않았다.

다음 작업 하나: **실제플레이어/다른카트좌표와검증한방향table을사용하는controller-only 추적입력을실행하고모든결정을기록한다.** 상태/체력/금액을수정하지않고자연클리어도달여부를확인한다.
