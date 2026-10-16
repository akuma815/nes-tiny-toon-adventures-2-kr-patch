# 크레딧 실제 소비 조사 — 작업36 / 채택036 유지

ROM/SSOT는 바꾸지 않았다.42draft/12미번역, 채택036 그대로다. 크레딧3원천을 실제 실행해 nativechr124/125와 스크롤/문단 경로를 특정했다. 이는 별도기록scene seed로 엔딩 화면을 실행한 것이며 게임을 완주한 증명이 아니다.

fixedCC22의root18=7→CEE5,19=1→CEFE(입력없음)→CF0A,07DF=1→A41E,06DE=0→A430 원래코드를 검증했다. [source/036 CPU 원래분기278cycles](../extracted/analysis/credits_root_dispatch_cpu_20261005.json). 네값을frame1000에기록하며nesDebug에쓰는 별도v3runner/Lua를 만들었다. PC/ROM/저장상태 변경은 없다. 두번째값19=2는cleanupCF1D라서 쓰지 않는다. runner와Lua모두정확한4주소·4값만허용한다.

v1은잘못복사된ticket-only Lua허용목록으로첫frame 전에실패했고 해당태스크PID4472만종료했다. [실패](../qa/reports/credits036_selector_bootstrap_rejected.json)와실행복사·0로그·실패environment를보존했다. v2는07DF/06DE 두값쓰기·9000frame 실행은했으나menu root18=8을벗어나지않아endingcallback0이었다. [비소비대조](../qa/reports/credits036_selector_v2_no_consumer.json)를그대로보존했다. v3에서원래root까지정확히선택한뒤3원천의실제소비를확인했다. 이실험과교정은게임ROM실패나번역삽입완료를뜻하지않는다.

[실제조사](../qa/reports/credits036_native_survey.json):nativeA445/A44F→9417에서2D·2E를frame1001에각mode5/6으로선택했고 A4B8→9417에서2F를2361에mode5로선택했다. helper C6=90과실제NMI RAM34=124는서로다르다. A457의LDA7C/STA34가생산자이며IRQ40=0. 실제286snapshot에서PPU0000~07FF가sourcefont124/125(원본3F010~3F810,확장5F010~5F810)와같았다. 이름글꼴ink2/ASCII41~67을보존해야한다.2D/2F mode5 NT2805,2E mode6 NT2005. 수평alias2000/2400,2800/2C00과FC/FFbit1의세로스크롤을관측했다.

[타이틀·STAFF](../qa/dialogue/credits036_source_01500_actual.png), [PROGRAM/GRAPHIC와이름](../qa/dialogue/credits036_source_02100_actual.png), [PACKAGE/TEAM](../qa/dialogue/credits036_source_03000_actual.png), [PRESENTED BY/KONAMI/권리문구](../qa/dialogue/credits036_source_03900_actual.png)를정수4배로직접검토했다. [원래캡처위치](../qa/dialogue/credits036_source_actual_pages.json). work/credits_group_001/draft_plan.json은정적번역후보일뿐이다. 타이니툰·어드벤처2/제작진/프로그램/그래픽/사운드/패키지그림/팀/제공을계획하고모든개발자이름·KONAMI·법적권리표시는원래대로유지한다. sourceFD32/FD20/FD3와literal00 위치및스크롤출력량을유지할것이다.

조사중독립925E CPU모델의6C0/1·6D1/2 주소바이트초기화가이전033/036에서뒤집혀있음을찾았다. 이전모델의old/new cycle동등은그합성상태에서참이었지만실제주소기하의증명은아니었다. 이전보고서/스크립트는그대로보존하고 [올바른little-endian NT 명령주소와96쌍+3원래크레딧](../qa/reports/native_printer_geometry_corrected_20261005.json)을추가했다. 별도실제pixel/NT/IRQ검증은영향없다. 앞으로CPU좌표초기화는native low/high로한다.

변경파일: run_credits_seed_qa.py/v2/v3 및trace_credits_seed_v1/v2/v3·각IRQ,정확한seed설정001/002·credits입력,분기CPU JSON,credits036_selector 실패/비소비/소비·IRQ실행6환경,actual4PNG/JSON,source조사/실패보고서,정적draft_plan,verify_native_printer_geometry.py/수정근거보고서,본조사·인계·계획·journal. [각해시](../manifests/credits_native_assets.json), [보존·링크감사](../qa/reports/credits_native_session_20261005.json).

```powershell
python scripts/run_credits_seed_qa_v3.py --rom build/dialogue_kr_poc_036/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/credits036_native_repro_next --frames 9000 --inputs config/menu_credits_001.json --seed config/credits_selector_seed_002.json
python scripts/run_credits_seed_qa_v3.py --rom build/dialogue_kr_poc_036/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/credits036_native_irq_repro_next --frames 9000 --inputs config/menu_credits_001.json --seed config/credits_selector_seed_002.json --script scripts/trace_credits_seed_irq_v3.lua
```

작업36에는새ROM·재빌드·패치적용을하지않았다.원본/1편/모든산출물보존,dist빈상태/외부게시없음. 전체게임corpus/그래픽·전체플레이·오디오/reset/savestate/실기/최종검토·기존PRG/RNG한계는남는다. 다음행동하나:원래124 ASCII를복제한공통201/202글꼴에크레딧3원천을삽입하고A457소비자·3문단·스크롤과이름/법적표시보존을검증한다. 바로계속한다.
