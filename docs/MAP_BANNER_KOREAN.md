# 지도 간판 한글화 — 작업40 / 038 채택

MONTANA LAND를 생성형 이미지의 **몬타나 랜드**로 바꿨다. 원래 간판 틀·뼈 장식·지도·배우·팔레트·NT배치를 보존했다. 코드·포인터·대사·기존 글꼴과 크레딧은037과 같다. SSOT45draft/9기술·공유원천 유지.

[원래PNG/실제소비](MAP_BANNER_EXTRACTION.md)에서 built-in image_gen 편집으로 [생성PNG](../workspace/graphics/map_banner_ai_001.png)를만들었다. [실제사용프롬프트](../workspace/graphics/map_banner_prompt_001.txt)와 [변환계획](../workspace/graphics/map_banner_kr_001/plan.json)을보존했다. 생성PNG SHA `9280a6e8bc3b0752390bf1d281aae56238d1f81eb023bfed197d611f925cdc53`. 중앙글자만crop/nearest13px/원래3색양자화했다. 프로그래밍으로대체한한글그림이나fallback이아니다. 144×16의문자영역외원래픽셀불변. [native](../workspace/graphics/map_banner_kr_001/native.png), [8배변환예시](../workspace/graphics/map_banner_kr_001/preview_8x.png). CHR상간판32타일/391바이트만변경,ROM크기475152/CHR208KiB 그대로다.

[ROM](../build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes) SHA `33b11de02e390d9617812350198bf60b023b64d65db9f1ea9bb5534a34f265d1`.
[IPS](../build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.ips) SHA `57b9361a911f7cb4aedaa329538e9039b8449f6928c33fe4bbf156de3f2768b6`.
CSV `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27`.
원본 `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`.

정적/빌드/적용: 원본전체 ExpectedWrites8/비중첩/원본기대바이트 PASS. 독립037전체이미지대조·타일decode·indices·틀보존 PASS. 038_rebuild와한글·공백경로 실제IPS CLI적용출력같음. 변경코드0으로새독립CPU시험은불필요했다. 원본확인PowerShell은처음기본ExecutionPolicy로차단돼프로세스한정Bypass로재실행PASS,시스템정책변경없음.

실행:037/038새지도tour각3600frame/390화면중217간판변경/173전체일치,지도선택0/1/2/5/6 상태. 6000frame intro848전체일치,9000frame 지정4seed 크레딧327중3초기지도간판변경/324전체일치. 총1565화면,보호픽셀0. PNG의바뀐정확한native픽셀만검사했고RAM/NT/팔레트/OAM/mapping·consumer로그완전일치,CHR은현재실제매핑된수정바이트만허용했다. tour IRQ70747이아닌 **70947**행/값/scanline/dot/cycle완전일치. [독립검증](../qa/reports/map038_validation.json).

모델의최초1950 crop비교는원래퇴장fade의red/white/blue팔레트가어두워져고정RGB와달라실패했다. ROM오류가아니다. 허용범위를늘리지않고원래캡처indices마다정확히하나의RGB가있음을확인한뒤같은팔레트로새indices모든픽셀을재구성했다. 팔레트바이트역시old/new같으며변환그림밖변화0이다.

직접장면검토: [1080 보통지도](../qa/dialogue/map038_01080_actual.png), [1950 native fade](../qa/dialogue/map038_01950_actual.png), [위치/해시](../qa/dialogue/map038_actual_pages.json). 실제캡처정수4배이며설명용합성이아니다.

변경파일compile_map_banner.py/build_map_banner.py/verify_map_banner.py,생성PNG·프롬프트·native/indices/계획,038/재빌드/IPS/실제적용,6QA환경·actual/검증,본문·인계·계획·journal. [자산](../manifests/map_banner_assets.json), [보존/링크감사](../qa/reports/map_banner_session_20261005.json).

```powershell
python scripts/build_map_banner.py --output build/dialogue_kr_poc_038_repro_next
python scripts/verify_map_banner.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/map038_repro_next --frames 3600 --inputs config/menu_tour_001.json --script scripts/trace_ui_consumers_v4.lua
```

원본/1편/모든성공·실패/생성 원천보존,dist빈상태/외부게시없음. 다섯관측지도상태와intro/지정credits만검증했으며다른CHR소비의부재·전체corpus·완주·오디오/reset/savestate/실기/최종사람검토는남는다. 다음행동하나:매표소영문간판·소지티켓·점수표시의실제PRG문자배치와NMI124/CHR102소비를추적한다. 계속한다.
