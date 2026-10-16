# 티켓 부족·소지 장수와 공통 하단 글꼴 — 작업34/35 / 036

채택036은 “아쉽지만 / 티켓을 더 모아줘!”, “지금{variable_F8}장의 / 티켓을 갖고 있어”를 출력한다. 등록54원천42draft/12미번역이며 전체 게임 완료율이 아니다. 나머지12개는 숫자전용1·공유macro8·크레딧3으로, 일본어 대사12문단이 남았다는 뜻은 아니다. 이들의 문맥별 처리와 게임그림/누락corpus 조사는 계속한다.

작업34에서 source9F52/9F60 및 실제normal3 seed 경로 slot29/2B를 확인했다. F8은 일반 티켓07D0~2의3자리이며 골드티켓이 아니다. 034는 별도196/198 글꼴을 즉시 고르는 바람에 기존 요금 지우기 전에 그 글자를 잘못 읽었다. [034 실패](../qa/reports/remaining034_rejected.json)를 보존하고 채택하지 않았다. 보호 픽셀 게이트가frame2004 x160~167/y163~170에서 거절했다.

원래9F09 초기화207cycles를4cycles로 제거하면203차이,19cycle 유휴루프 위상과 맞지 않았다. 작업34 인계의209cycle은 이전 common9CF3 수정에서 가져온 가설이며 이 실제 소비에 적용할 수 없다고 정정한다. ROM의9F09/9417/9A81/008 및 모든 실행 코드를 그대로 유지했다. 대신 요금1D,숫자F9 alias00/23,부족29,출발2A,소지2B의5unit/6slot을 공통 하단font196/197로 구성했다. 상단 제목·규칙은193/194를 계속 사용한다. 요금1D는 odd193에서 even196으로 바뀌어 초기상단을 덮지 않는다. 실제상단193 문맥과 [독립 초기상단30case 계약](../qa/reports/stage_lower036_top_contract.json)을 검증했다. macro88은 모두 “티켓을 ”로 일관되게 읽고 FA/F8/F9 숫자 및 제어·literal00·출력cycle은 유지한다. F9는 기술적 숫자원천으로 번역 상태를 임의로 올리지 않았다.

035는036과ROM byte가 같지만 메타데이터의 prior032 키 이름이 잘못돼, 수정된 메타데이터로036을 새로 만들고035/재빌드도 보존했다. 036의 기준은033이며 해시로 고정했다. 새공통글꼴은한글22자, 남은literal슬롯40개. 숫자/기존글꼴/타이틀/매크로/상단카드 보존. CHR200KiB/ROM466960바이트, 예약6KiB.

[독립 검증](../qa/reports/stage_lower036_validation.json): ExpectedWrites7/중첩0/전체이미지 재구성/재빌드/한글 경로 실제IPS 동일. reader240상태, 즉시출력925E의30상태와 [ABI1504/초기font720](../qa/reports/stage_lower036_hooks1504.json) 통과. 여섯 경로2125화면에서 상단 제목·규칙과 소유하단 셀 밖 변화0,1987전체화면 동일/138하단셀 변경. NT차이는 원래 출력 위치 글자쌍만, RAM740~74F는 최장15자+종료 reader replay쌍만,0100~01FF 명령큐/스택은 native 글자쌍만 인정했다. 원래 NT를 지우는 동안 상단카드193일 때만 해당하단셀을 인정하며 마지막 NT차이 뒤 인접3frame snapshot한 장까지만 잔여 framebuffer를 인정한다. NMI상단34/3A와 게임 상태/숫자계산/보호PPU/OAM 동일. IRQ/NMI/PPU/mapper599931시점 정확히 동일,값 차이는 원래하단148/190/193→196뿐. 원래print/clear 시간이 유지됐다.

[실제 부족](../qa/dialogue/stage_lower036_29_actual.png), [소지3장](../qa/dialogue/stage_lower036_2B_actual.png), [요금4장](../qa/dialogue/stage_lower036_1D_actual.png), [출발](../qa/dialogue/stage_lower036_2A_actual.png)을 직접 검토했다. [거절034 전환](../qa/dialogue/stage_lower036_transition_rejected034.png)과 [수정036 같은frame2004](../qa/dialogue/stage_lower036_transition_fixed036.png) 비교에서 원래글자 의미를 유지하며 지워지는 것을 확인했다. [완성NT·원본이미지](../qa/dialogue/stage_lower036_actual_pages.json). 실제요금1680 전체pixels는 직접검토한033과 동일하다. nativeFF는 완성 후6CF를 다음값으로 올리므로 evidence는 해당slot/slot+1와 정확한완성NT를 함께 검사한다.

[새 타이틀·9도입부 회귀](../qa/reports/stage_lower036_intro_validation.json):033/036 각6000frames fresh cold boot,848화면/RAM/PPU/OAM/mapping 전체동일. 별도2850frame IRQ41034시점/값 전체동일. 총2973비교화면과640965실행시점을 확인했다. 성 성공/부족은 기록된초기RAM seed이고 나머지4일반놀이기구/도입부는 컨트롤러뿐이다. 자연수집/전체플레이 증명이 아니다.

- 원본 SHA256: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 036 / 재빌드 / 실제 적용 SHA256: `9dbca87461d59ede5cf287d8842c63f498ebdd6b3830254dc2e1ad8b0a4ff21f`
- IPS SHA256: `c49d3570c2f8bfe8c1525728c213b76101ae300bd7888e4999e1c7ed003f738b`
- CSV42draft SHA256: `ccd784aa0e878cd30e4ae30690b4852f7f641e99dad9e875498ba413f9691447`
- 034 거절ROM SHA256: `b7ce3eb27e65321c142980fe4c914581a70800a5c3b2e4af5b97a99589410c4b`
- 034 IPS SHA256: `85cbfda7ee7eea97367d123b7cc7907fa856067bb5a107dcbc8353cbc98a897b`

변경 파일은 scripts/compile_ui_possession.py·prepare_ui_remaining.py·build_ui_remaining.py·verify_ui_remaining.py·hooks 및034/재빌드/실제적용/normal3실행, 이후 compile_ui_stage_lower.py/build_ui_stage_lower.py/verify_ui_stage_lower.py/verify_ui_stage_lower_hooks.py/verify_ui_stage_lower_intro.py/make_ui_stage_lower_evidence.py, 두plan·CSV백업·035/036·재빌드·실제적용·6경로·새intro실행·실화면·본인계·조사·계획·journal이다. 각SHA는 [자산](../manifests/ui_stage_lower_assets.json)과 [감사](../qa/reports/ui_stage_lower_session_20261005.json)에 기록한다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_ui_stage_lower.py --output build/stage_lower036_repro_next
python scripts/verify_ui_stage_lower_hooks.py --build build/dialogue_kr_poc_036 --report qa/reports/stage_lower036_hooks_repro_next.json
python scripts/verify_ui_stage_lower.py
python scripts/verify_ui_stage_lower_intro.py
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_036/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/stage_lower036_normal3_repro_next --frames 4500 --inputs config/menu_coaster_insuff_001.json --seed config/ride_normal3_seed_001.json
```

034재현은 격리복사본에서034 translation_used.csv와원래ui_remaining_plan_001.json을 사용한다.036고정검증 역시 당시CSV에 적용하며 현재SSOT를 되돌리지 않는다. 공개용dist는비어있고 외부게시 없음. 원본/1편/모든실패·과거산출물 보존. 오디오/reset/savestate/실기/전체플레이/최종번역·명칭 검토와기존PRG/RNG영향 미완료.

다음 행동 하나: nativeCF0A가07DF=1일 때A41E/A430 크레딧을 실행하는 경로를 별도기록scene seed로 확인하고3크레딧 원천의실제CHR/스크롤소비를 특정한다. 계속 진행.
