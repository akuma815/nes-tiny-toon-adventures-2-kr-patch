# 작업77 — 시작 안내 한글화 / 빌드045

[ROM](../build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes), [IPS](../build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.ips), [빌드](../build/dialogue_kr_poc_045/build_report.json), [통합 검증](../qa/reports/start077_validation.json). ROM SHA15e9f17dcbaaa02778e6a28d5dcf9c318232508ca5fb0346a6e6303a2ff15350 / IPS4b3efb0ce4227436cef2eacc25b7e90bc0651c99d629013844b947819d78d2dd / 원본f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d.

개발 초안 START! → **시작!**. [그림 번역 SSOT](../workspace/translation/start_graphics_draft_001.json), [컴파일 계획](../workspace/translation/start_graphics_plan_001.json), [PNG 원천](../workspace/graphics/start_001/start_kr_8x.png). Galmuri7 2.403/OFL 두한글 atlas/TTF검사 후3배nearest/1pixel외곽선·그림자, 기존3색 팔레트 유지. 타이틀 생성형 이미지003와 구분하는 nativebitmap 작업이다.

정적: 원본122/123복제를 새222/223 bank(77810..78010)에 넣고 NT와 연결된48타일만 바꿨다. 다른80타일/원래122/123/기존220 안내/모든 이전한글자료/헤더/ROM길이491536 동일.044대비1236byte차이가 새2KiB 및26607/2660B 두operand 안에 있다. 원본 ExpectedWrites9개 전체재구성/기대바이트/비중첩 통과.

CPU: A5F6의두LDA/두STA/BNE/INC6DE를256flags×4초기substate=1024사례로 실행. 두fontRAM34/35와bank값A만의도적으로변하고 레지스터·스택·최종status·분기목적지/19cycles 동일. LDA의N 차이는 BNE가Z만보고 다음INC가최종NZ를복원한다. 비동기PPU/IRQ모델은 실제런타임과구분.

빌드/적용: 새폴더 재빌드10파일 byte exact, 한국어·공백경로 실제Windows Python IPS CLI출력ROM byte exact. 공개 apply.cmd나 새최종배포ZIP은이번에없다.

자연runtime:20,000프레임/829PNG/6,632CHR매핑 검증.044와19,999정책행 같고666world행은START font7A→DE만차이. OAM/네임테이블/팔레트동일, RAM34/35/3A/3B의bank만다르다.15변경PNG가96×32 시작영역안이며 나머지814PNG는전체동일. native 첫구간완료/다음라운드/시간초과/홈복귀를유지한다.

직접 시각: [actual2670 시작](../qa/dialogue/start077_cart045/frame_02670.png), [actual5010 다음라운드](../qa/dialogue/start077_cart045/frame_05010.png), [actual19110 시간초과](../qa/dialogue/start077_cart045/frame_19110.png)를직접확인했다. 검증기V1의`and112` Python문법오류는 실행검증전실패였으며 [V2](../scripts/verify_start077_v2.py)로정정하고V1보존.

재현: `python scripts/build_start_notice.py --output build/새폴더`; `python scripts/run_cart_rounds_qa_v4.py --rom build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 20000 --inputs config/menu_cart_001.json`; `python scripts/verify_start077_v2.py` (고정출력이없는복제공간). [파일/SHA manifest](../manifests/start077_assets.json).

본문 CSV는45draft/9기술공유·SHA26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27 그대로다. 사람최종번역/명칭승인, 전체3구간/전게임,실기/PCM청음은미수행.043검토ZIP/키트는그때의동결자료로보존한다.

다음 작업 하나: 롤러코스터·기차·급류의044/045컨트롤러진입을짝으로실행해공통시작안내와그뒤게임화면을비교한다.
