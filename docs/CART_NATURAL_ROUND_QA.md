# 작업70 — 카트 첫 구간 자연클리어

[검증보고](../qa/reports/cart_rounds070_validation.json), [수정실행기](../scripts/run_cart_rounds_qa_v2.py), [최종controller Lua](../scripts/trace_cart_rounds_v2.lua), [검증기](../scripts/verify_cart_rounds070.py), [구간별원본지형](../work/cart_geometry_001/all_level_classes070.json).043/SSOT변경0.

V2는첫4200프레임의controller mask를작업65와전부일치시켰다. 이후대상을유지하고움직임을예측해구멍반대편으로접근하며40/48 완전충전과B 과속/낙하회피를쓴다.13번째타입2D도남은적루틴의대상으로포함했다. RAM/ROM/PC/phase/금액/체력/state/reset 개입은없다.

V2에서4801경에남은세슬롯type0이되며4830 snapshot은0430=5 완료상태다.4970 실제level79가0→1·phase0E로변하고이후두번째구간phase5에진입했다. 체력3을유지했다. 이는첫구간자연클리어다.3구간전체/최종보너스·history·금티켓완료를주장하지않는다.18k에서는level1에서체력3·Gold/history0이며uppercorridor에머물렀다.4830/4980/18000 실제화면을직접확인했다.

0/1/2구간의DE91 오프라인지형표를만들었다. 두실행에서34,470고유실제tile query 입력이원본CPU와같아0/1구간소비를검증했다. level2는아직정적모델뿐이다. 유효맵밖질의는일부임의byte분류도나오므로원본모델전체를임의바닥으로간주하지않고플레이어가속한벽안연결성만사용한다. level1 경로의4칸lookahead가모서리를가로지를수있어 실제clearance/선분검사를다음에추가한다. 이동정체의전체원인을확정한것은아니다.

V1은이전초기입력을재현하려고했으나direction deadzone을6픽셀대신0.2로사용해first4200 mask566행이달랐다. [차이기록](../qa/reports/cart070_prefix_mismatch.json), [초기Lua](../scripts/trace_cart_rounds_v1.lua), [초기실행기](../scripts/run_cart_rounds_qa.py),18k 실행자료를보존했다. V1은level0·체력1·Gold/history0으로미클리어. V2의prefix차이0과첫구간성공을별도로판정했다.9,168 runtime파일SHA·완료마커/환경·query 비교를검증했다.

재현: `python scripts/run_cart_rounds_qa_v2.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 18000 --inputs config/menu_cart_001.json`. 고정현재결과를덮어쓰지않는다. sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27.

정적·runtime최초구간완료/actualquery·직접3장검증을구분한다. 보고서작성후위3장을직접확인했으므로JSON의미수행문구는당시기록이고본인계에후속직접검토를명시한다. 새빌드/패치적용·PCM/청음·실기·전체자연완주·최종사람검토없음. 원본·1편·기존성공/실패·검토패키지보존·외부게시없음.

다음 작업 하나: **경로lookahead에벽·구멍선분검사를추가하고확장프레임실행에서나머지두구간을시험한다.**
