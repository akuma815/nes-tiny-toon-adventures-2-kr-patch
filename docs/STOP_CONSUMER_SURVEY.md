# 작업79 — 실제 기차 STOP 표지 소비/추출

빌드045/원본/기존CSV를바꾸지않았다. 별도native coldboot4,200프레임에서컨트롤러만사용했다. [환경](../qa/dialogue/stop079_train045/environment.json), [관측Lua](../scripts/trace_stop_v1.lua), [실행기](../scripts/run_stop_qa.py), [추출/검증](../scripts/extract_stop_sign.py), [소비기](../extracted/graphics/stop_001/consumer.json).

STOP는스프라이트가아닌 **위쪽배경CHR68/69**다. 원본bank46스프라이트 후보/68..75 atlas만으로글자판단한가정은기각했다. NMI mapper완료FD9E에서HUD IRQ전PPU를관측했고3330 top0..7FF가원본bank68/69(31010..31810)/현재51010..51810과같다. 실제PPU read20,560행의bank68..71바이트를ROM과검사했다. 실행루틴D1BF..D20A가course25×2를Y로해D20B font표를읽으며 native2719 RAM34=44 쓰기의nextPC는D1C8이다. 코스2/Y4의표값파일3D21F가68이다. 나머지글꼴35=70과철도간판216..219는별개다.

NT2800의3×4셀(56,96)-(80,128)과actual3330(24,96)-(48,128)의768전체RGB가같다. 수평차32는그장면의경험적 PNG/NT 정렬이며현재카메라RAM을단순동일시하지않는다. [원본표지PNG](../extracted/graphics/stop_001/stop_original_8x.png), [실제4배](../work/stop_sign_001/actual3330_4x.png)를직접확인했다. 글자필드22줄은6~7픽셀너비이고비틀린나무판형태를따른다. ‘정’/‘지’는Galmuri7에서각6×7실제ink이므로기존필드안에세로배치할수있다. 바깥테두리/기둥/나무판은보존대상이다. 8개글자타일10/11/15/16/19/20/26/27로범위를등록했다.

[NT2800 임의팔레트도해](../work/stop_sign_001/NT2800_assumed_group2.png)는배경전체를표지팔레트로칠한설명용으로실제화면이아니다. 처음수평0..12 가정은맞지않았고32에서ROI RGB가정확히같았다. 후보와관측실패가정을증거와구분한다.

정적/추출/실제readonly실행을검증했으며새빌드/apply는아직없다. [파일/SHA manifest](../manifests/stop079_assets.json). 현재ROM15e9f17dcbaaa02778e6a28d5dcf9c318232508ca5fb0346a6e6303a2ff15350/본문CSV26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 전게임/전기차구간완주/최종사람언어검토는미수행이다.

재현: `python scripts/run_stop_qa.py --rom build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_train_001.json`; `python scripts/extract_stop_sign.py --output extracted/graphics/새폴더`.

다음 작업 하나:표지내부에‘정지’를세로배치하고bank68/69복제224/225와코스2의단일font표값으로새046을빌드·검증한다.
