# 매표소 그림·소지/점수 표시 한글화 — 작업42 / 039 채택

영문 그림 간판TICKET BOOTH를생성형 **매표소**로,압축NTliteral5군을 **현재 소지한 / 티켓 수 / 장 / 보유 점수 / 점**으로삽입했다. 등록대사CSV45draft/9기술·공유원천은그대로이며별도그림번역원천[booth_graphics_plan_001](../workspace/translation/booth_graphics_plan_001.json)에초안5개를기록했다. 전체게임완료주장이아니다.

[원래소비조사](BOOTH_GRAPHICS_SURVEY.md)대로 원래font124/125를복제한204/205에Galmuri7한글12자를추가했다. 기존ASCII/숫자/글꼴/타이틀/지도/크레딧·기존대사보존,기존빈예약73010~73810에font2KiB를썼다. CHR208KiB/ROM475152 그대로다. 9C95의LDA7C/STA34 두뷰5CA6/25CA6만CC로바꿨고다른HUD/font124소비자는그대로다. 다음LDA66이NZ를덮으며분기는없다. 원래compressedliteral개수와361bytestream/1024NTcell·압축제어·다른NT셀·숫자실체를보존했다.

그림은 built-in image_gen의[생성PNG](../workspace/graphics/booth_header_ai_001.png)와[프롬프트](../workspace/graphics/booth_header_prompt_001.txt)를프로젝트에보존하고중앙매표소3글자만crop/nearest10px/nativeblack2·orange1로변환했다. AI SHA `560af447c3e93b2c9ce810cf9d63d68a8164372ced8bafd8f56ecf5a30134e8c`. [native](../workspace/graphics/booth_header_kr_001/native.png), [8배](../workspace/graphics/booth_header_kr_001/preview_8x.png). 24tile내문자범위외원래이중테두리·지붕·색/배치보존.

[ROM](../build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes) SHA `6b4b9150ff55140d959a12938dc549a58c8ebb6bdb0007c31f4a242e711f066b`.
[IPS](../build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.ips) SHA `193dc29f42ebc5dbca4c20dc6f5e6feb21e8cba80a4a30e6e3b2346f9d2d9002`.
CSV `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27`.
원본 `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`.

정적·CPU: 원본전체ExpectedWrites8/비중첩/전체037이후허용변경만PASS. 한글atlas/TTF동일·fallback0,ASCII/숫자/다른font원래바이트보존. 생산자768공식CPUcase에서10cycles/모든ABI·RAM34만차이. native803F 압축전송128 D-clear flagcase/19415cycles/6366instructions/1024개2007주소와각cycle정확히같다. [독립CPU·코덱](../qa/reports/booth039_native_decoder.json).

CPU조사정정: 원래readopcode는806C LDA($00),Y이며callback이advance된PC806E를보고한다. physicalmapping근거는같은8000창이라영향없다. 최초모델은256flag중D-set에서공식NMOS6502의BCD ADC로포인터가달라졌으므로128 D-clear로범위를제한했다. 전2A03모델이라고주장하지않고실제NES시점은별도검증했다. 초기039 frozen build보고서의producer12cycles라는key명은잘못붙었으며실제4명령은10cycles다. 당시768 old/new동등은맞았고현재빌더/독립검증은10을명시한다. frozen039/재빌드/빌더복사본은보존했다.

빌드·적용:039_rebuild와한글·공백경로 실제IPS CLI출력같음. [독립검증](../qa/reports/booth039_validation.json).

실제실행: 일반매표소4500frame339화면중182문구만변경,내부점수3 seed4500frame339중63문구만변경,지도tour390/intro848/지정credits327전체화면동일. 총2243쌍/보호픽셀0. 실제188916시점같고7000font쓰기값만7C/7D→CC/CD. RAM은34/3A의font값만변화. 숫자·교환상태·팔레트·OAM·배우같다. 실제crop의glyph별정확한팔레트를얻어새Galmuri/native간판 전체RGB를재구성하여그문자칸에서도번역그림자체가정확함을확인했다. 대사/유지숫자를문구마스크로덮지않았다.

상단글꼴은frame끝하단IRQ snapshot에서204표본0인것이정상이다. 그래서source/new각2000frame의추가read-onlyFD92 X0 callback으로A008선택직후를조사했다. 총36쌍중17개새204/205 PPU0000~07FF가ROMfont2KiB와완전일치,이전124font19대조도불변. physicalmapping·PC/X/frame/scanline/dot/cycle완전같음. [NMI실제글꼴근거](../qa/reports/booth039_top_font_validation.json).

숫자해석정정: seed의07F2=3은**내부값3**,실제source/new NT21EA~21F1는00003000이므로 **화면3,000점**이다. 교환후00000000/일반티켓11장이고원래게임과같다. 앞선points3폴더/파일명은seed명을뜻하며3점이라는화면의미로읽지않는다. 자연3,000점획득/전체완주증거는아니다.

직접검토: [보통10장/0점](../qa/dialogue/booth039_booth039_native_01500_actual.png), [내부3/화면3000점과교환안내](../qa/dialogue/booth039_booth039_points3_01680_actual.png), [11장/0점과완료인사](../qa/dialogue/booth039_booth039_points3_01899_actual.png), [위치/해시](../qa/dialogue/booth039_actual_pages.json). 실제캡처정수4배이며설명용합성이아니다. 모든명칭/문구는초안이다.

변경파일compile_booth_graphics.py/build_booth_graphics.py/verify_booth_native_decoder.py/verify_booth_graphics.py/trace_booth_top_font_v1.lua/verify_booth_top_font.py,그림PNG·prompt·native/indices·별도번역plan,039/재빌드/IPS/실제적용,9번역/대조QA환경+2fontprobe환경·검증/actual,본문·인계·계획·journal. [각자산해시](../manifests/booth_graphics_assets.json), [보존·링크감사](../qa/reports/booth_graphics_session_20261005.json).

```powershell
python scripts/build_booth_graphics.py --output build/dialogue_kr_poc_039_repro_next
python scripts/verify_booth_native_decoder.py
python scripts/verify_booth_graphics.py
python scripts/verify_booth_top_font.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/booth039_repro_next --frames 4500 --inputs config/menu_ticket_001.json --script scripts/trace_booth_layout_v1.lua
```

원본/1편/모든성공·실패/QA보존,dist빈상태/외부게시없음. 5관측literal이전corpus전체라는주장은하지않는다. 다른게임HUD/영문그래픽·전체corpus·전체플레이/오디오/reset/savestate/실기/최종사람검토·기존PRG/RNG한계남음. 다음행동하나:놀이기구실제게임/HUD와결과화면의남은영문·일본문자소비를조사한다. 계속한다.
