# 작업97 — source61 깃발 실제 소비 positive control

현재047 ROM/CSV/패치를바꾸지않았다. ROM82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10/CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556. 원본/1편/과거증거유지. [독립검증](../scripts/verify_pow097.py), [보고서](../qa/reports/pow097_positive_control.json).

실행: 일반티켓4를1000frame에한번설정하고그후controller만사용한 native게임실패→게임오버→예/홈경로를8000frames씩 baseline047/probe047로순차실행했다. 자연획득통화/전게임완주와구분한다.6개배경·상태파일/PNG를포함해3682 native파일 byte exact,606실제PNG전체동일이다. 추적Lua와추가관측로그만다르며게임화면/상태/메뉴·세계로그·seed·native기존소비로그가같다. [baseline환경](../qa/dialogue/bank61_097_baseline047/environment.json)/[probe환경](../qa/dialogue/bank61_097_probe047/environment.json), [새추적Lua](../scripts/trace_bank61_gameover097_v1.lua).

소비연결: native F72A LDA3E→F72C STA0405(관측후PC F72F)의806쓰기, common9643 actor5/3E의805실행, actual OAM83/CHR0F420/8×16 mode의805프레임(5296..6100)을연결했다. 이때RAM38=61/D000/PPU1800=0F400. PPU의source61 64바이트 읽기51520행은각프레임64주소·1회/모든값이ROM과exact다. flag영역0F420..0F44025760행과동반blank sprite81영역25760행을구분했다. **깃발3E/83은POW글자가아니다.** 예선택뒤native홈복귀도확인했다.

직접장면/픽셀: [실제깃발5400](../qa/dialogue/bank61_097_probe047/frame_05400.png), [예뒤홈6900](../qa/dialogue/bank61_097_probe047/frame_06900.png)을직접봤다.27개의actualPNG에서source32바이트flag bitmap·OAM좌표120/164·sprite2 palette코드0F/2A/20/00를사용해8×16 RGB전체를재구성했고exact다. screenshotY는OAMY+1이며PPUfetch scanline의물리실기결론으로확대하지않았다. RGB는현재Mesen capture/default범위에한정한다.

분류/한계: source61에서선택POW후보영역과frame18/19/3C/7C/9C/9D를별도로기록했다. 이경로의POW후보producer/PPU읽기는0이고flag는정상검출되어관측기의작동이확인됐다. 이것은POW의전역미사용증명이나번역/보존 최종사람결정이아니다. 실제POWproducer와다른스테이지/아이템조건은남는다. 이전84의zero범위도동결된해당경로로만유지한다. 신규빌드/apply는미수행;047정적/적용은90/91/93근거유지. 전게임완주/전역corpus/실기/PCM청음/최종사람검토/카페완성작업기/외부게시미완료.

재현: `python scripts/run_bank61_gameover097_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 8000 --inputs config/world_gameover_yes_001.json --seed config/world_coaster_ticket4_seed_001.json`. 비교baseline은같은인자에run_gameover_seed_qa_v2.py를쓴다.순차실행필수. [동결manifest](../manifests/pow097_assets.json).

다음 작업 하나: 원본RAM38의직접/계산형bank지정 writer를역추적하고frame18등과bank61이동시에성립할수있는콜러·값범위를좁힌다.
