# 작업94 — 현재047 입장 분기와 성 플레이 회귀

현재047 ROM/CSV를 바꾸지 않았다. ROM SHA82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10, CSVac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556, 원본/1편/모든과거산출물 보존. [검증보고서](../qa/reports/gate094_validation.json), [순차실행기](../scripts/run_gate094_matrix.py), [독립검증기](../scripts/verify_gate094.py).

명시적개입:1000frame에 골드4 또는 일반50/49 숫자RAM만 한번설정하고 이후controller만사용했다. 상태로드/ROM/PC/체력수정 없다. 각seed쓰기로그의 시점·값/실행환경/모든파일SHA를 확인했다. 자연적으로 티켓을 얻은 증거가 아니다.046과047 각각gold4/normal50은9000frames,normal49는6000frames 실행했다.

런타임: 2096표본쌍 중108표본의변경은 성입구 두행에만 한정,1988전체화면동일. 각경로37표본의175176폰트PPU가 각ROM과exact, 완성1920의nativeNT와RGB도 독립재구성exact. 모든OAM/상태txt/주소mapping/메뉴로그/seed로그 exact. RAM변경은 경로별native reader192회로 재현한glyph쌍과관측scratchA와같은stack103쌍에만한정한다. 전체스택을제외하지 않는다. 보호PPU 패턴·NT/속성/팔레트 일치.

분기:골드4는native1C입장허용→성course4/root4/phase5, 종료시gold4/일반10유지. 일반50은1A 가격안내/1B질문/1C허용 후50→0차감→성course4/root4/phase5. 일반49는1A가격/1B질문 뒤19거절/0A홈복귀, 종료시49/골드0 유지. 실제성플레이골드4의475표본·일반50의293표본은 화면/RAM/전체PPU까지046과byte exact. 성을끝까지완주한증거는 아니다.

직접장면: [골드4 성HUD4410](../qa/dialogue/gate094_gold4047/frame_04410.png), [일반50 가격2580](../qa/dialogue/gate094_normal50047/frame_02580.png), [입장인사3300](../qa/dialogue/gate094_normal50047/frame_03300.png), [일반49거절3321](../qa/dialogue/gate094_normal49047/frame_03321.png), [49홈복귀4200](../qa/dialogue/gate094_normal49047/frame_04200.png)를 보았다. 숫자50·한글HUD·문장·입장/거절뒤 폰트수명이 보존된다.

정적/빌드·적용은90/91/93동결근거를유지하며 새ROM/재빌드/패치작업이아니다. 사람최종검토/전게임완주/전역corpus폐쇄/신규047저장·리셋/실기/PCM청음은미완료다.047검토ZIP의93시점미수행표시는그때범위로유지하고본작업을추가근거로연결한다. 외부게시/카페완성작업기 없음.

재현: `python scripts/run_gate094_matrix.py`는기존출력을거부한다. 새폴더로 실행하려면 `python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 9000 --inputs config/menu_castle_continue_001.json --script scripts/trace_branch_seed_v1.lua --seed config/gate_gold4_seed_001.json`;50도동일inputs/frames,49는6000/menu_castle_001/gate_normal49_seed_001. 모든Mesen실행은순차. [동결manifest](../manifests/gate094_assets.json).

다음 작업 하나: 현재047 성입구의175176글꼴을 실제NMI상단에서저장·불러오고 리셋후같은대사에재진입해 글꼴·문구가유지되는지검증한다.
