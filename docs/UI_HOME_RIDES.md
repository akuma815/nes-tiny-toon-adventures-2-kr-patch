# 홈 기차·급류타기 — 024 / 작업26

홈 선택의 남은2문구를 ‘기차’,‘급류타기’ 초안으로삽입했다. MAIN_05753(slot0D)/MAIN_05756(slot0E), font166/167·168/169이다. 이름만표시하며 원문의설명어미だよ는생략하는기존선택명방침을따른다. font별매크로그리프만바꾸고raw본문86/83/FF·87/83/FF,공통매크로,포인터/제어/00/시간을보존한다. 놀이기구설명판과성일본어는023그대로다. 새로운6글리프는atlas/TTF확인한Galmuri7이다.

54원천중20draft/34미번역이며전게임완료율이나최종번역승인이아니다. CHR176KiB/ROM442384,예약6KiB다. 원본·1편·이전빌드/증거를보존했다. [CSV 변경전](../backups/translation/text_ja_before_ui_rides_001.csv)에서18draft입력을동결했다.

## 검증

[독립보고](../qa/reports/rides024_validation.json): 원본ExpectedWrites7와023전체에서font2/table2/CHR길이·padding만변경,원문필드/다른52행/이전CHR/성상단148/코드불변. reader는기차10호출757cycles/급류15호출997cycles이며호출별cursor/cycles/출력코드가원래와같다. 실제font에서만한국어로읽힌다.

[CPU1504](../qa/reports/rides024_hooks1504.json),initialfontseed720/48slots/ABI/SP/flags/mapper/음수004대조/공식6502 ISA604벡터를통과했다. 재빌드와깨끗한원본에서실제한글·공백경로IPS적용동일. runtime1105:기차329중63·급류302중38현재선택행만바뀌고성474전체같음. 그행밖픽셀0,게임RAM은C6/06F3외전체같음,보호PPU/팔레트/OAM/상단font/포인터/티켓·포인트같음. 실제font166:34/168:73표본. 실제IRQ/NMI/PPU/mapper195169시점정확히같으며font1600값만바뀐다.

[실제2문구4배](../qa/dialogue/rides024_actual_names.png)에서train1350/water1200을검토했다. 본작업에서새도입런타임은반복하지않았으며타이틀/도입본문·폰트/helper를정적으로보존했다. 이전022도입848화면은022에대한증거다. 전체플레이/성한글·설명판·성공교환/골드충족·전corpus·오디오/reset/savestate/실기/최종번역검토는남는다. v3숫자열오류는raw주소정정대로해석하고v4를후속에사용한다. dist비어있고외부게시없음.

## 식별·재현

- 원본: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 024 ROM/재빌드/적용: `5ef5a86ce785f61586ebb17cbe11ec4a5e1d5be6e6f3e6ca77c2f4367a425fc8`
- 024 IPS: `ae326e8250caaa6ec07c7a9531ef2d401cf78c1ac9f06c71c0537008d6662327`
- 현재CSV: `d57b739152817572a0f1833572ca7991eb7684a77a1c00a2ef44931ee2c228fe`
- 삽입계획: `59b19d4283de50bd7958f7e1dcc26d912c99f14ed9ca0abd8f26c9e6b9852f21`

[자산해시](../manifests/ui_rides_assets.json),[세션감사](../qa/reports/ui_rides_session_20261005.json).

```powershell
python scripts/build_ui_rides.py --output build/rides024_repro_next
python scripts/verify_ui_rides_hooks.py --build build/dialogue_kr_poc_024 --report qa/reports/rides024_hooks_repro_next.json
python scripts/verify_ui_rides.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_024/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/rides024_train_repro_next --frames 4200 --inputs config/menu_train_001.json --script scripts/trace_ui_consumers_v3.lua
```

prepare_ui_rides.py는1회실행했다. 재실행으로SSOT를초기화하지않는다. 고정검사는현재20draft입력에대한것이며후속변경후그대로재실행하지않는다.

다음 행동 하나: 성 문단별상단font를native초기화완료때공급하는helper를CPU/도입·메뉴·성 실제실행으로검증한다. 즉시이어간다.
