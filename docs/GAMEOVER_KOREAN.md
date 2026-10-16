# 게임오버 한글화 — 작업48 / 042

생성형 “게임 오버” 그림과 “계속할까요?”, “예!”, “아니요”를 native 실패 화면에 삽입했다. **4,040화면·378,645개 실행 시점 대조 통과**. 실제 실패/선택/복귀/이전 장면에서 그림과 세 문구 밖 픽셀·커서·OAM·상태는 원래와 동일하다. [검증](../qa/reports/gameover042_validation.json), [실제6장면](../qa/dialogue/gameover042_actual_pages.json), [자산·해시](../manifests/gameover_assets.json), [보존 감사](../qa/reports/gameover_session_20261005.json).

원본 source f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d. 기준041 535fa114952587dfc0a6394ddff21b1aede053ade3dc0d3d9dfda77ed5888eae. [042 ROM](../build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes) `f4b4aa288e03bb30fd9532d95f823e34c4c620b20438feb2e1de0f67845cfc7b` /483,344바이트·CHR216KiB. [IPS](../build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.ips) `ebd250d9f9750a52f8720850c78cc13a86506e866e3fe834106bf42364221ef8`. [재빌드](../build/dialogue_kr_poc_042_rebuild/build_report.json)와 [한글 경로 실제 적용](<../qa/dialogue/한글 패치 적용 042/TinyToon2_gameover042_applied.nes>) 전체 해시 일치.

[실제 원천·소비 조사47](GAMEOVER_CONSUMER_SURVEY.md) 이후 내장 imagegen으로 원래 PNG를 참조해 정확한 “게임 오버”를 생성했다. [요청/프롬프트](../workspace/graphics/gameover_kr_ai_001/generation_request.json), [생성 원천](../workspace/graphics/gameover_kr_ai_001/generated_gameover_ko.png), [변환 결과](../workspace/graphics/gameover_kr_ai_001/converted_logo_4x.png), [변환 기록](../workspace/graphics/gameover_kr_ai_001/conversion.json). 생성 PNG2172×724/SHA4595124bfe860671bcbe6069ee35bb02e2bb29d5c4a3414ceba3210bd6eb9167. alpha128 영역[53,115,2123,631]→112×28, native128×32 canvas의[8,2]에 배치했다. 원래 검정/하늘색/흰색/파랑4색만 사용했다. generated 원본과 프로젝트 사본을 보존한다. 기술 변환 PNG는 실제 ROM 검증과 구분한다.

기존 font124/125를210/211로 복제해 Galmuri7의8한글을1..8에 넣었다. 질문10셀·예6셀·아니요5셀과 원래68/69 인용부호·물음표·느낌표를 보존해 처리했다. “NO.” 뒤94ED A5는 코드이며 범위에서 제외했다. 122/123을212/213으로 복제하고213의64tile/128×32 게임오버 그림만 바꿨다. 원래124/125·122/123과 이전 한글 글꼴은 전부 보존했다. 214/215의2KiB는0인 여백으로 남아 있다.

[SSOT 계획](../workspace/translation/gameover_graphics_plan_001.json), [font210/211](../workspace/graphics/gameover_kr_ai_001/font210_211.bin), [font212/213](../workspace/graphics/gameover_kr_ai_001/font212_213.bin), [컴파일](../scripts/compile_gameover.py), [빌드](../scripts/build_gameover.py). 변경은 nativebank36/93AC의34·35 생산 immediate D3BD/D3C1 및 확장2D3BD/2D3C1, literal21바이트의원래/확장 대응본, 예약4KiB 글꼴이다. 저주소bank06 대응본은 정적 호환 사본이며 실제 관측은canonicalbank22이다. 그 밖의 모든 기존 바이트·opcode·NT 그림64코드/주소·literal길이·팔레트·숫자/커서 데이터는 동일하다.

정적/CPU: 원본으로부터9 Expected Writes의 원래 바이트·중첩·전체 결과를 검증했다. 독립 TTF→CHR 재구성과 native PNG→64tile 배열 전체 일치. 생산자256flags×3초기값=768사례,15cycles 동일. [native queue](../qa/reports/gameover042_native_queue.json)는93AC/9412의 D-clear128flags×3queuebases=384사례,127바이트·7명령·935instructions·2964cycles, 매 write주소/시점·ABI·PRG·RAM(알려진글꼴쌍/문구값 제외) 동일. D16C는 길이별 dispatcher pointer두바이트를 출력하며 단순길이바이트가 아니다. 첫 호출하네스의 SP/길이 가정을 [실패 기록](../qa/reports/gameover042_queue_model_error.json)에 보존·정정했다. ROM 오류가 아니며 새검증이 통과했다.

실제 Mesen: 초기 일반티켓4 seed 후 native게임 실패로 진입하며 phase/PC/ROM/state-load는 바꾸지 않는다. 질문·선택·출력완료·idle·fade·재초기화를 밀집 기록한 두경로1,239화면 중362화면만 네 소유 영역이 달랐다. AI 그림1,482,752픽셀·한글 문구486,528픽셀 전체 native RGB 일치, 소유영역 밖 변화0. RAM 차이는34/35/3A/3B의 정확한글꼴쌍과 nativebase0 command queue의 소유문자값만 허용했다. OAM·팔레트·점수/티켓/이력·player/phase·커서/선택 상태 동일. NMI 직후4KiB 글꼴36/41표본 전체가 정확하다. 378,645개의frame/PC/scanline/dot/cycle 동일, NMI fontwrite 값9,652개만 바뀌었다.

예 선택 후 native home/일반10장, 아니요 후 시작·타이틀/attract 복귀를 확인했다. 예 선택의6168은root8이지만그림과activefont124/122가fade중남는원래수명이다. 정적root4만요구했던 검증기는 이를 거절했고 [자원수명 정정](../qa/reports/gameover042_visual_lifetime_error.json) 후 정확한source4KiB/3A·3B와 모든소유픽셀·영역밖/상태/타이밍 조건으로 검증했다. 범위를넓혀그림차이를무시하지않았다. 직접6장면에는 두커서선택·진입/완료·fade·홈·타이틀복귀가 포함된다.

회귀2,801화면: 도입848·크레딧327·매표소339·성524·보너스763에서 RAM/OAM/NT/팔레트/CHR매핑/실제화면 전체 동일. 크레딧/성/보너스는 기존selector/gold4/nativephase seed를 그대로 사용한 분기 증거이며 자연클리어·엔딩이 아니다. 기존041 build_report/runtimepending은 빌드시점 표현이며 이후PASS를 참조한다. 042도 frozen runtimepending은 빌드시점이고 이 검증이 후속근거다.

재현(기존 build/QA를 덮어쓰지 않으며 새경로 사용):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_gameover.py --output build/새로운_042_재빌드
python scripts/run_gameover_seed_qa_v2.py --rom build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새로운_042_게임오버 --frames 8000 --inputs config/world_gameover_yes_001.json --script scripts/trace_gameover_seed_v2.lua --seed config/world_coaster_ticket4_seed_001.json
```

아니요는world_gameover_no_001.json, 전체타이밍은trace_gameover_seed_irq_v2.lua. [독립검증](../scripts/verify_gameover.py), [QA모음](../scripts/run_gameover_suite.py), [회귀](../scripts/run_gameover_regressions.py). environment.json/used 파일은 실제명령·모든설정·입력·seed·파일해시를 동결한다.

등록 CSV45draft/9기술공유는 불변이고 전체 완료율이 아니다. PAUSE는 정적후보로실제소비를아직 연결하지못했다. 타이틀 PUSH START·저작권은 [기존 타이틀 범위의 보존 결정](POC_TITLE.md)에 따라 유지한다. 그보존결정을 모든환경영문에확장하지않는다. train MONTANA LAND/R.R. 등별도환경그림후보와root9는추가조사대상이다. 전체corpus·전체자연플레이/오디오/reset/savestate/실기/최종사람검토 미수행. 외부게시 없음/ROM없는배포·카페작업기는 전체작업완료후 준비한다.

다음 작업 하나: PAUSE의native코드·CHR120/121 소비를 추적하면서 실제세계영문그림의 소비 목록을 정리한다. 중단 지시 없으면 바로 이어간다.
