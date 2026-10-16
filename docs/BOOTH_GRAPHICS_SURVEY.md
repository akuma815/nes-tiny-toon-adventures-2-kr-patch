# 매표소 그림·영문 표시 실제 소비 — 작업41 / 038 유지

새038 controller-only 매표소4500frame 및IRQ4500frame실행을보존했다. frame1473 9C95/9C99에서RAM34=124,직전1499NMI에서CHR124/125/102/103선택을확인했다. 실제 frame1500의간판24NT셀은원본CHR102/103과바이트/팔레트/RGB일치했다. 간판은96×16이며그타일은관측매표소상단에서각1회사용된다.

NUMBER OF/REMAINING TICKETS/TICKETS/YOUR POINTS/POINTS는등록대사9417원천이아닌PRG의압축NT배치literal이다. frame1474 806E에서각원래문자를읽는것을확인했다. callback address가물리PRG오프셋이라고가정하지않았다. 전달된CPU8681등과같은8000/8K창의실행PC806E→physical2406E매핑을이용해실제source24691등을계산하고값/원래바이트/actualNT를전부대조했다. [연결근거/번역계획](../extracted/graphics/booth_001/consumer.json) SHA `2d1a189085fcecc6bdbe5dd0bb3afb6379047984e58f29b44239802ccc51f264`.

[원래간판](../extracted/graphics/booth_001/header_source_native.png), [8배](../extracted/graphics/booth_001/header_source_8x.png), [실제매표소](../extracted/graphics/booth_001/booth_source_actual_4x.png). 원래간판·실제frame1500을직접검토했다. 예정표시는매표소/현재소지한·티켓수/장/보유점수/점이다. 숫자·디지트·골드/일반티켓·포인트교환원래동작은보존할것이다.

이번작업은정적/native실제소비조사이며ROM/CSV변경0,새번역빌드/적용/번역CPU/번역화면검증없음. NMIproducer9C95의LDA7C/STA34뒤LDA66이branch전에NZ를덮는원래바이트도확인했다. 다른bank124 HUD소비자에는이변경을전파하지않을계획이다. CHR204/205빈예약부분에124복제전용font를두고이producer만바꿀것이다.

변경파일trace_booth_layout_v1.lua/survey_booth_layout.py,booth038_native/IRQ환경·모든캡처·reads로그,consumer JSON/headerPNG2/indices/actualPNG/본조사·인계·journal. 038 ROM `33b11de02e390d9617812350198bf60b023b64d65db9f1ea9bb5534a34f265d1` 그대로,원본/1편/이력보존。전corpus/다른consumer부재/전체플레이등은미증명. 재현 `python scripts/survey_booth_layout.py`; 실행은 `python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/booth038_native_repro_next --frames 4500 --inputs config/menu_ticket_001.json --script scripts/trace_booth_layout_v1.lua`.

다음행동하나:새전용font204/205·원래literal길이/압축제어보존·생성형매표소간판을삽입하고실제숫자/대사/동일시점·보호픽셀을검증한다. 계속한다.
