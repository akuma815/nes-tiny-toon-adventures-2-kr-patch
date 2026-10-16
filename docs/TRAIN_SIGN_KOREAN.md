# 기차 간판 한글화 — 작업51 / 채택043

기차의 작은 간판 세 영역을 **몬타나의 / 큰 M 문양 유지 / 랜드 철도**로 삽입했다. [실제 확대 화면](../qa/dialogue/train043_actual/engine_full_14700_actual_4x.png), [변환 PNG](../workspace/graphics/train_sign_kr_001/converted_label_4x.png), [실제 원문 소비](TRAIN_SIGN_CONSUMER.md)를 확인할 수 있다. 이번에는 작은 글자를 기존 Galmuri7 비트맵으로 만들었다. 앞서 타이틀·지도·매표소·게임오버에 사용한 생성형 그림과 제작 방법을 구분한다.

## 파일과 해시

| 파일 | SHA256 |
|---|---|
| [원본](<../original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes>) | f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d |
| [043 ROM](../build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes) | 087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a |
| [043 IPS](../build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.ips) | 4337ba28119d88135a8f3cca7f3a0a6d32a3e183e92e40aa3bfff84b2a45f1bb |
| [번역 CSV](../workspace/translation/text_ja.csv) | 26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27 |

491,536바이트 / PRG256KiB·CHR224KiB다. CSV45draft/9기술 공유 항목은 그대로며 전체 게임 완료율을 뜻하지 않는다. [그래픽 초안 원천](../workspace/translation/train_sign_graphics_plan_001.json), [Expected Writes](../build/dialogue_kr_poc_043/expected_writes.json), [빌드 보고](../build/dialogue_kr_poc_043/build_report.json), [전체 검증](../qa/reports/train043_validation.json), [작업 자산](../manifests/train_sign_assets.json), [보존 감사](../qa/reports/train_sign051_session.json)를 남겼다. 빌드 보고의 runtimepending은 빌드 시점 문구이며 후속 PASS 보고서를 참조한다.

## 소유 범위

원본72..75를216..219에 복제하고 256타일 중 **10타일**만 편집했다. 앞부분40×8의2D..31, LAND24×8의34..36, R.R.16×8의67..68이다. 한글8종은 TTF와 PNG atlas가 같은 비트맵인지 확인했고 글자7행을 y1..7에 배치했다. index1의 노란 잉크와 index2의 검정 바탕을 유지했다. 큰 M, 아래 행, 테두리, 나머지246타일과 모든 원본 CHR·기존 한글 글꼴은 같다. 220..223의4KiB는0이며 기존214/215 여유 공간도 그대로다.

active canonical IRQ5의3FBFF/3FC08만72/74→216/218로 바꿨다. 원래 fixed-bank 사본은 유지했다. 042와 비교한 기존 영역의 차이는 CHR 크기 헤더1바이트와 두 즉시값뿐이고 새8KiB에 복제 글꼴과0패딩을 추가했다. original 기반9 Expected Writer로 원본 바이트·중첩·전체 결과를 재검증했다.

## 구분한 검증 결과

- **정적·CPU:** 독립 TTF 재구성,10타일 소유·나머지 보호·원본 Expected Writes가 맞는다. IRQ FBE3부터 FD13/RTI까지 flags256×scroll3×counter3=2,304사례에서179cycles와 레지스터·SP·상태·전체 RAM·포트 쓰기 시점이 같다. CHR 네 값만 변경됐다.
- **빌드·실제 적용:** [재빌드](../build/dialogue_kr_poc_043_rebuild/TinyToon2_dialogue_kr_poc.nes)와 [한국어·공백 경로의 CLI 적용 ROM](<../qa/dialogue/한글 패치 적용 043/TinyToon2_train043_applied.nes>)이 같은 해시다.
- **Mesen 실제 실행:** 원본042/수정043을 각각18,000프레임 coldboot했다. 체력3 보충 진단과 컨트롤러 입력은 같다. 771화면 중22화면에서 글자가 바뀌었으며 실제 글자10,552픽셀이 독립 원본/수정 글꼴에 맞고 그 밖의 변화는0이다. 실제 중간 IRQ4KiB1,017표본과 글꼴 선택15,252회를 검증했다. 전체637,476개의 IRQ/NMI/PPU/mapper 시점이 같고 변경 값은 IRQ5 네 글꼴61,008회뿐이다. RAM·OAM·NT·팔레트·체력·점수·티켓·history·phase·CPU/PPU 상태가 같다. mapper의 첫16개256B offset만 정확한 새 글꼴 주소로 바뀌었다.
- **별도 회귀:** 도입/크레딧/매표소/성/보너스/게임오버 예·아니요/네 놀이기구 일시정지의5,234화면은 전체 원본042와 같다. 기차와 합쳐6,005화면이다. seed를 사용한 분기는 각 environment에 명시한 그대로다.
- **직접 장면 검토:** 기차 진입·전체 간판·이동·빠져나감과 일시정지·게임오버를 [실제6장면](../qa/dialogue/train043_actual_pages.json)으로 보존하고 직접 확인했다.

이미지 F에는 실제 직전 IRQ F−1의 NT·OAM·scroll을 사용했다. y−2는 실제 fineY2, x는 기록된 scroll의256모듈로 계산했다. 왼쪽8픽셀의 실제 backgroundMask=false와 opaque sprite를 보호하며 임의 좌표 허용 오차를 넣지 않았다. 이번 변경 화면에서는 글자 위 sprite가 없어 보호 대상 occlusion은0이었다.

## 실패 자료와 정정

세밀한 120초 실행은9750 부근에서 종료돼 [미완료 자료](../qa/dialogue/train042_life3_irq/environment.json)를 보존했다. [별도 보고](../qa/reports/train043_trace_timeout.json)는 원인 추정과 같은 Lua/입력/ROM의300초 V3 재실행을 구분한다. V3 두 경로는 모두18,000까지 완료했다. 이는 실행 수집 제한의 복구이며 ROM 수정은 없었다.

첫 중간 getState 비교는 의도한 mapper.chrMemoryOffset0..15 변경까지 동일해야 한다고 가정해 거절했다. [모델 정정](../qa/reports/train043_state_mapping_model_error.json)에 따라16개 offset을 정확히12000+i×100→36000+i×100으로 검증하고 나머지 모든 키의 동일성을 요구했다. 현재 PASS는 이 엄격한 분리 후의 결과다. 실패 자료는 덮어쓰지 않았다.

## 재현과 다음 작업

`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1`로 원본을 확인한다. `build_train_sign.py --output build/<새ID>`는 immutable042를 입력으로 새 경로에만 만들고 기존 계획은 동일한 내용인지 검사한다. `dialogue_ips.py create/apply`는 원본·패치·결과 해시와 기존 파일 유무를 검사한다. [빌더](../scripts/build_train_sign.py), [독립 검증기](../scripts/verify_train_sign.py), [native 실행](../scripts/run_train_sign_suite_v3.py), [회귀 실행](../scripts/run_train_sign_regressions.py)을 보존했다. 기존 QA 경로와 PASS 보고서는 최초 실행 전용이므로 재실행은 새 경로를 기록한다.

체력 보충은 진단이며 자연 플레이·기차 클리어의 증명이 아니다. PAUSE120/121·HOW TO CONTROL의 관측 밖 소비, root9 엔진과 전체 corpus, 최종 사람 번역 검토·전체 자연 플레이·오디오/reset/savestate/실기는 남아 있다. 원본·1편 참조·기존 성공/실패/QA는 보존했고 dist는 비어 있다. 외부 게시도 하지 않았다.

다음 작업 하나: **무입력 attract와 native root9 초기화 경로를 조사해 남은 실제 문자 소비와 등록 원천의 폐쇄 범위를 확정한다.** 중단 지시가 없으면 계속 진행하고, 기술 작업이 끝난 뒤 ROM 없는 배포용 자료와 카페 작업기를 준비한다.
