# 홈 선택·매표소 8문구 — 022

현재 개발본은 타이틀003, 도입9문단, 홈 안내와 관측된 홈 선택/매표소8문구를 포함한다. 원천54행 중18draft/36untranslated이며 전게임 완료율이 아니다. 이름과 서비스 말투의 최종 검토는 남는다.

| 원천 | 초안 | font |
|---|---|---|
| MAIN_0574D | 롤러코스터 |150/151|
| MAIN_05750 | 쇼킹카트 |152/153|
| MAIN_05759 | 수수께끼의 성 |154/155|
| MAIN_05762 | 매표소 |156/157|
| MAIN_05769 | 나중에 또 보자! |158/159|
| MAIN_05777 | 매표소에 어서 오세요 |160/161|
| MAIN_05782 | 포인트를 티켓으로 / 바꿔 드릴게요 |162/163|
| MAIN_05794 | 아쉽지만 / 포인트가 부족해요 |164/165|

선택 문구는 설명어미 대신 이름만 표시한다. macro83의 선두00와 원래 전개칸/바이트수/제어/읽기시간을 유지하면서 자연스러운 띄어쓰기를 확보하기 위한 초안이다. 다른 소비기의 일본어와 공통 매크로 데이터는019 그대로 보존했다. 8쌍의 전용 글꼴은 Galmuri7 atlas와8px TTF 대조로 만들었으며 대체 글리프를 쓰지 않았다. CHR168KiB, ROM434192바이트, 남는 padding2KiB다.

020은 매표소 전환 직전의 중복 초기화가 이전 문구에 새font를 입혀 잔상문자가 깨졌다.021은 공통 초기화에서font를 지연했지만 도입부 그림 경계가1 CPU사이클 달라져 기각했다. [020 실패](../qa/reports/ui020_rejection.json),[021 실패](../qa/reports/ui021_rejection.json)와 모든 후보/증거를 보존했다. 검사영역을 넓히지 않았다.

022는 원래005 공통 helper/도입부를 그대로 쓰고, 매표소만 native9CF3의 중복 JSR9417을 LDY00/NOP로 바꾼다. 원래5행 지우기가 끝난 뒤9C79에서 호출하는 초기화가 새 pointer와font를 적용한다. 지우는 동안 이전 pointer/font를 유지한다. 절감209사이클은19사이클 대기루프11회이며 전체 분기108조건에서 레지스터/flags/SP/mapper/게임RAM 상태를 확인했다. 의도된 차이는 지우기 중 아직 이전 문단을 가리키는 pointer와font뿐이다.

## 검증과 증거

- 정적: 원본 ExpectedWrites7와019 전체 이미지에 허용한 본문8/table8/font8/CHR길이·padding/매표소3바이트2개소만 변경. 원문 필드·54개 단위·제어/매크로/00위치와 읽기 호출별 시간 보존. 이전 폰트·타이틀·상단 설명판RAM34·도입부 helper 불변.
- CPU: [ABI1504조건](../qa/reports/ui022_hooks1504.json), 그중 초기font seed720. 별도 매표소 선초기화108조건. 비동기IRQ/PPU는 CPU모델로 증명하지 않았다.
- 빌드/적용: 별도 폴더 재빌드와 깨끗한 원본에 실제IPS적용이 동일 SHA. 한글·공백 경로 적용도 확인했다.
- 실행: [1527화면](../qa/reports/ui022_validation.json)의 현재 native문구 행밖 픽셀차이0. 도입848화면은 전체 픽셀/PPU/OAM 일치. IRQ/NMI/PPU/mapper115353시점 정확히 일치. 팔레트/OAM/다른네임테이블/원래인덱스/상단font 보존, 매표소 지우기 중 pointer차이만 명시적으로 검증.
- 직접 화면: [완성된8페이지](../qa/dialogue/ui022_actual_pages.png),[완성조건/원캡처](../qa/dialogue/ui022_actual_pages.json). tour1125/1605/1482/1362/1920, ticket1560/1680/1914를 실제네임테이블 완성값과 대조하고 가독성을 검토했다. 전환 중1653/1656은 이전font160,1659는 새font162다.

## 식별과 재현

- 원본: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 022 ROM/재빌드/적용: `88dada01f379ca25abb9cee08793b372fbe9508ba6d1581b131c9d07ff90ba08`
- 022 IPS: `f19bdb16878bd86621eec71e1c3d7f1bbbd2be7ca5eb31834096237618ef56c4`
- 현재 CSV: `1528501efb8983ff77b9514fd859a7a7cca91eb23eb5ca752132cd645c3fbcd6`

- 계획: `78a9d9926639c9efb006797669e7289d26fa98d651c98d00cbf85c9991ee1e6e`
- 변경 전 CSV: `76bcc0d985c41dff6ce19cf0dd1a8a02e58bbb6814ca0b2f26e9e8239b9e8c48` ([보존본](../backups/translation/text_ja_before_ui_home_booth_001.csv)).
- [자산별 해시](../manifests/ui_home_booth_assets.json),[세션감사](../qa/reports/ui_home_booth_session_20261005.json).

```powershell
python scripts/build_ui_home_booth.py --output build/ui020_repro_next
python scripts/build_ui_post_clear.py --output build/ui022_repro_next
python scripts/verify_ui_post_clear_hooks.py --build build/dialogue_kr_poc_022 --report qa/reports/ui022_hooks_repro_next.json
python scripts/verify_ui_home_booth_post_clear.py
python scripts/make_ui_page_evidence.py --build build/dialogue_kr_poc_022 --prefix ui022 --output qa/dialogue/ui022_review_next.png
```

현재 verifier는 고정022와현재18draft 입력을 검증한다. 후속SSOT 변경 후 과거 verifier/audit를 그대로 재실행하지 않는다. builder의 기본020 입력은 보존된 후보이며 재현폴더의 이름을 새로 지정한다. 실행은 run_menu_qa.py와 동결된 각 environment.json의 명령/설정/입력/Lua로 재현한다.

## 남은 작업

기차·급류타기·성입구·교환성공·동적숫자 분기·상단 설명판·영문그림·크레딧 및 전체corpus를 계속 조사한다. 전체플레이/오디오/reset/savestate/실기/최종사람검토는 수행하지 않았다. 기존PRG 확장과난수 영향도 전게임 동일성을 보장하지 않는다. dist는 비어 있고 외부 게시가 없다. 최종 카페 작업기는 전체 작업이 끝난 뒤 근거를 모아 작성한다.

다음 행동 하나: controller-only 경로로 기차·급류타기·성입구를 방문해 원천ID/font/상단NMI/동적숫자 소비를 연결한다. 별도중단지시 없이 이어간다.
