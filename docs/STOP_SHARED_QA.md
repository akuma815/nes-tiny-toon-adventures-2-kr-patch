# 작업81 — 046 CHR 확장 / 다른 세코스 보존

원본/046/기존CSV 변경없이 다른롤러코스터·카트·급류를각4200프레임coldboot했다. source045보존자료와같은컨트롤러/관측script를사용했고체력·시간·화폐·RAM/ROM/PC/세이브개입없음. [suite](../scripts/run_stop081_suite.py), [정확명령](../work/stop_regression_081/suite_runs.json), [검증기](../scripts/verify_stop081.py), [보고서](../qa/reports/stop081_regression.json).

852개PNG와같은시점RAM/OAM/PPU/mapping까지5종총4260파일이045와byte exact다. world420행동일, 카트4199controller정책행도045/20k자료prefix와동일하다. 각경로nativephase5에진입했다. CHR232KiB확장이기존뱅크맵핑과그림을훼손하지않은것을확인했다. target동결파일5142개(환경JSON제외)를SHA검사했다. 직접 [롤러코스터](../qa/dialogue/stop081_coaster046/frame_03330.png), [카트](../qa/dialogue/stop081_cart046/frame_03330.png), [급류](../qa/dialogue/stop081_water046/frame_03330.png)의actual3330도확인했다.

기차STOP/정확glyphRGB/빌드·적용은 [80](STOP_KOREAN.md)의증거를계승한다. 이번에새ROM빌드/apply를실행한것은아니다. 전게임/모든코스완주/실기/PCM청음/최종사람번역은미수행이다. 현재ROM SHAa58a28bcb1449ad44b02cccbf6503af0e2792cbf96c9b9409bcc05025552a0f8.

[파일/SHA manifest](../manifests/stop081_assets.json). 재현은suite고정출력이없는복제작업공간또는`python scripts/run_world_qa.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_coaster_001.json`(카트는run_cart_rounds_qa_v4).

다음 작업 하나: 본문54원천/그림33문구와새안내4개의실제화면을포함하는현재046 사람검토키트를새폴더/ROM없는ZIP으로갱신하고desktop/mobile렌더를확인한다.
