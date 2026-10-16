# 작업72 — 카트 몸체 폭의 8픽셀 경로

[정적body graph](../qa/reports/cart_body072_static.json), [실행검증](../qa/reports/cart_runtime072_validation.json), [8픽셀graph](../work/cart_geometry_001/bodyclear072_graph.json), [실행기V4](../scripts/run_cart_rounds_qa_v4.py), [고정Lua V4](../scripts/trace_cart_rounds_v4.lua), [검증기](../scripts/verify_cart_runtime072.py).043/SSOT 변경0.

nativeA142..A212와같은cardinal±15/diagonal±10 및중심9개probe를 사용했다.각probe의원본16픽셀분류가class0/1일때만8픽셀vertex를경로로허용했다.3정적구간총6,485 vertex의58,365 probe를검증했다. 벽밖class0 성분은플레이어의coarse내부연결성으로제외하고,경로선분에도같은몸체검사를사용했다. 보수적인회피graph로원본의가능한bumper/반사shortcut까지모두허용한것은아니다. level0 성공입력은그대로다.

새36k에서first4969 mask와4970 첫구간클리어를재현했다. 두번째구간은마지막적을남기고time00/phase11→09/0A→홈으로돌아왔다.체력3/history·Gold0이다. 경로계획의모서리검사를강화해도전체카트클리어는달성하지못했다. 같은claim의기계반복으로성공이라고합치지않는다. 다음은원본2F 이동과policy의과속B 제한을확인한다. NPC 속도보다낮은속도로감속한다는가설을아직확정하지않는다.

8,184runtime파일/1,362PNG/10,896CHRmapped조각/71,068 actualquery·30,901고유원본CPU입력이일치했다. 0/1구간실제소비,2구간정적모델만이며전체corpus/wholeplay는아니다.19110 실제time00와24000 실제홈을직접확인했다. 검증JSON direct_visual 문구는71 template에서복사돼해당72 화면을보기전기록됐으며,본문의직접검토는검증후수행한72 실제두PNG이다. 현재근거를각실행별로보존한다.

재현: `python scripts/run_cart_rounds_qa_v4.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 36000 --inputs config/menu_cart_001.json`. 고정출력을덮어쓰지않는다. 조사중enemy타입의inlinepointer가800C라는가설은실제801A 조건분기/CFC2 조사로거절했다. 실제8058 subtract20→805B CFC2를CPU로실행해2D/2E/2F의883B/97DF/95E3 dispatch를얻었으나아직상세AI consumer로채택하지않았고다음작업에서연결한다. table9791/9799는명령이아닌방향데이터로취급한다.

sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 실제RAM/ROM/PC/phase/금액/체력/state/reset 개입·새빌드/패치적용·PCM/청음·실기·최종사람검토없음. 원본/1편/이전성공·실패·검토패키지보존/외부게시없음.

다음 작업 하나: **원본2F 적 이동/속도 소비기와policy B 감속조건을비교한다.**
