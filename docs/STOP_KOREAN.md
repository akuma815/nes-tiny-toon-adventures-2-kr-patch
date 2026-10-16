# 작업80 — 기차 ‘정지’ 표지 / 빌드046

[ROM](../build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes), [IPS](../build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.ips), [빌드](../build/dialogue_kr_poc_046/build_report.json), [실제통합검증](../qa/reports/stop080_validation.json). ROM SHAa58a28bcb1449ad44b02cccbf6503af0e2792cbf96c9b9409bcc05025552a0f8 / IPS2321c83f9fca7188b25c4c4f651e390a029a01251669d8a35e77dd7e2ad3e4ff / 원본f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d.

STOP → **정지** 개발초안. [문구SSOT](../workspace/translation/stop_graphics_draft_001.json), [타일 계획](../workspace/translation/stop_graphics_plan_001.json), [PNG 원천](../workspace/graphics/stop_001/stop_kr_8x.png). Galmuri7 2.403/OFL의각6×7정/지 ink를atlas와대조하고기존비틀린6~7pixel필드안에서세로배치했다. 생성형이미지가아닌nativebitmap작업이다.

정적:22줄의기존글자필드만지우고정/지를그렸다.나무판/기둥/테두리/배경색은pixel일치. source68/69전체2KiB복제에서8글자타일만편집하고다른120타일보존. 새224/225(78010..78810),226..231은0예약.기존045몸체는header5(28→29)/3D21F font표값(68→224)외전부동일하며원래68/69/철도간판216..219/시작222223/다른한글폰트보존. CHR232KiB/ROM499728. 원본ExpectedWrites9개기대byte·비중첩·전체재구성통과.

CPU: D1BF..D20A 전체loader가5코스×3level×256flags=3,840 NMOS6502모델에서RAM34 외같고137cycles같다. 정확한범위는 **D-clear1,920사례가NES관련**이며D-set1,920은일반NMOS decimal SBC 비교이다. 모델은NES decimal-disabled처리·비동기IRQ/PPU를모사하지않는다. builder의native_ABI 표제만으로모든D-set을NES증명으로읽지않는다. [정정/한계](../qa/reports/stop080_observation_errata.json).

빌드/적용: 새폴더재빌드10파일byte exact,한국어·공백경로의실제Windows PythonIPS CLI결과가046과같다. 새공개apply.cmd/배포ZIP은이번에없다.

Runtime:4,200프레임coldboot 컨트롤러만사용.302PNG/2,416CHR조각이ROM과같고world140행은train font값만변한다. OAM/네임테이블/팔레트동일,RAM34/3A의68→224만차이.20,560 실제PPU read행의좌표/순서/횟수/scanline과현재ROM바이트검증.23변경PNG의 **2,395 모든변경pixel이원본/한글타일의glyph bit와각각의정확한RGB에일치**하며단순히넓은허용사각형에넣지않았다.

스크롤검증: 전체판이완전히NT에남는다는초기가정은화면끝부분에서실패했다. 타일별필드검사로수정했고3360은직전보존NT의같은소비스키마가필요하며3870은camera2차이가아닌0에서맞는다. 이는관측한화면버퍼/NT경계이며정확한하드웨어지연시간주장은아니다. 첫046 V1 실행은새font224의read필터가없어관측이제한됐고V2에서확대했다. 두실행을모두보존했다.

직접시각: [actual3330 세정지표지](../qa/dialogue/stop080_train046_v2/frame_03330.png), [actual3360 왼쪽부분표지](../qa/dialogue/stop080_train046_v2/frame_03360.png), 원본/변환PNG를확인했다. 작은글씨의최종사람미감승인은pending.

재현: `python scripts/build_stop_sign.py --output build/새폴더`; `python scripts/run_stop_qa_v2.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_train_001.json`; `python scripts/verify_stop080.py` (보고서없는복제공간). [파일/SHA manifest](../manifests/stop080_assets.json).

본문45draft/9기술공유/CSV SHA26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27 그대로다. 전기차/전게임완주/실기·PCM청음/사람최종번역은미수행.043 검토패키지는역사로보존하고현재046검토본은추후갱신한다.

다음 작업 하나: CHR확장046의다른3놀이기구4200프레임을045보존자료와비교해공통시작/기존화면이모두동일한지검증한다.
