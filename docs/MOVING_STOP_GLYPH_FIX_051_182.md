# 작업182 — 움직이는 STOP 한글화051·동일조건 검증

[개발051 ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes) SHA `b8bad5f333d4dfd04bbcb3e67dfddc0b4972486199810a2d9e5c0f45af3acb24` / [IPS](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.ips) SHA `cd6ab0cbdd68da067752700084989b934c85f501af99d0800034dac4b6feec6b`. [정적/빌드계획](../build/dialogue_kr_poc_051/build_report.json), [최종검증](../qa/reports/moving_stop182_validation.json). builder의runtime Pending는作成당시기록으로보존하고이최종검증으로051을채택한다.

수정:24×32 표지판의기울어진내부글자영역에고정표지판과같은Galmuri7 ‘정지’를삽입했다. CHR46의6타일42/43/45/48/49/50 총58바이트만050에서변경. 1↔2의녹색/검정글자픽셀만바꾸고투명/빨강·외곽/기둥은보존했다. PRG/헤더/IRQ/타이밍/고정224225/다른CHR/CSV는050과동일. [추출원천](../extracted/graphics/moving_stop182/source_indices.png), [편집원천](../workspace/graphics/moving_stop182/kr_indices.png), [삽입계획](../workspace/graphics/moving_stop182/insertion_plan.json). 기존33그림원장을고쳐전역완료로만들지않고이번추가소비를별도기록한다. 원문유지6건의선택도바꾸지않았다.

빌드:원본Expected Write/기대원본/중첩금지/전체model검사,PNG인덱스↔CHR왕복,원본IPS적용 PASS. 별도폴더독립ROM/IPS재빌드 byte-exact PASS. CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`.

에뮬레이터:같은전용Mesen/설정/입력/observer로050·051 각5000frame.734 paired화면의RAM/OAM/매퍼/CPU·PPU상태및HUD-time PPU덤프 byte-exact.644전체PNG 동일;90화면의7451변경픽셀은각표지판의정확한원문/번역글자쌍(녹색/검정)에서만변경. 상단실제매퍼288 CHR청크를각ROM과일치검사했다. HUD전체RGB,고정정지표지판,움직임/게임상태 보존. 전체게임/기차완주나최종사람그림승인은아니다.

직접화면: [4200 수정전](../qa/dialogue/moving_stop181_050/frame_04200.png)/[수정후](../qa/dialogue/moving_stop182_051/frame_04200.png)에서원문 STOP→정지 확인.4272의두표지판장면도수정후확인. 첫검증V1은endFrame의다음OAM과완료이미지사이에단일공통offset을요구해4272에서실패했다. 각각움직이는두표지판의시차를별도로취급한V2에서모든변경픽셀의정확한글자쌍을검증했다(객체별offset±2). 실패V1도보존하며넓은사각형허용으로덮지않았다.

재빌드: `python scripts/build_moving_stop182.py --output build/NEW_051`. 실행은181 명령의ROM/출력을051/새폴더로바꾼다. `python scripts/verify_moving_stop182_v2.py`는고정증거를다시쓰기방지하므로기존보고를재생성하지않는다. 변경파일/전체SHA:manifests/nonplay182_assets.json. 사용자원본/1편/Mesen/세이브/이전build/검증자료보존. 카페완성작업기/게시없음.

다음 작업 하나: 원본일본판에적용하는051 ROM없는검수ZIP을만들고실Windows 적용검증한다.
