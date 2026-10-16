# 놀이기구 제목·규칙·요금 — 작업33 / 033

다섯 놀이기구의 제목5개, 규칙5개, 공통 요금1개를 한글 초안으로 삽입했다. 등록54개 원천 중40draft/14미번역이다. 전체 게임 완료율은 아니다. 이전29개 초안과 타이틀003은 유지했다.

상단 제목·규칙과 하단 요금은 동시에 보이므로 font193/194 하나를 공유한다. 한글79자, 원래 macro84~88의39슬롯을 함께 배치했다. 사용하지 않는 macro83의1~3 코드를 이11개 전용 문맥에서만 재사용했고 원래 매크로 바이트는 보존했다. 남은 글자 슬롯은0개다. 새 문구를 이 글꼴에 추가할 때는 재할당 검증이 필요하다. PNG/TTF 글리프를 대조했고 누락 글자는 대체하지 않았다. 기차 뒤3칸은 원래 macro86 폭을 유지하기 위한 공백이다.

원래 FA가 출력하는 요금4/1/2/3을 실제 화면에서 확인했다. 높은 자리0은 원래 blank00이다. 성은 지정 gold4 초기 RAM seed로 입장해 제목·규칙·출발을 확인했다. 다른 네 경로는 컨트롤러 입력만 사용했다. 자연 수집·전체 완주의 근거는 아니다.

[독립 검증](../qa/reports/cards033_validation.json): ExpectedWrites7/중첩0, 원본 전체 이미지 재구성, 이전032 전체 이미지의11본문·11font표·새2KiB font·CHR확장 외 보존, 재빌드·한글 경로 실제 IPS 적용 동일. [CPU ABI1504/초기font720](../qa/reports/cards033_hooks1504.json), reader528상태, 즉시출력925E의66문구/ride 조합에서 호출별cycle/cursor 및 전체 출력cycle이 같았다. literal00, FD/FE/FF/FA, 포인터와 숫자 원형을 유지했다.

실제1786화면 중291장만 제목·규칙·요금 셀에서 변경했고1495전체화면 동일했다. 다른 픽셀/보호 PPU/팔레트/OAM/게임 상태 변화0. 네임테이블 변화는 정확한 원래 출력 위치의 old/new 글자 쌍으로 제한했다. RAM740~755는 최장21자와 종료코드의 reader replay 쌍으로 제한했다. RAM0100~01FF는 네임테이블 명령 큐와 스택이 공유하는 공간이며, 전체를 무시하지 않고 변경된 바이트 모두를 native 글자 출력 쌍에 대조했다.

요금에서 출발로 넘어갈 때 원래 지우기 루틴이 옛 글자 셀을 잠시 남긴다. 각 일반 놀이기구 frame2001/2004/2007에서 요금 셀만 허용했다. 마지막 NT 차이가 기록된 직후에는 인접3frame 캡처 한 장까지만 인정한다. live RAM/NT와 screenshot은 원자적 캡처가 아니므로 이 구간을 별도 기록했다. 카드 문맥 밖 전체 화면에는 이 허용 영역을 적용하지 않는다. 잘못된 글꼴 전환을 숨기기 위한 전체 창 마스크/시간 오차 허용은 없다.

IRQ/NMI/mapper/PPU505383시점이 정확히 같고 바뀐 값은148/149→193/194뿐이다. 직접 검토한 실제 화면: [롤러코스터](../qa/dialogue/cards033_coaster_actual.png), [쇼킹카트](../qa/dialogue/cards033_cart_actual.png), [기차](../qa/dialogue/cards033_train_actual.png), [급류타기](../qa/dialogue/cards033_water_actual.png), [수수께끼의 성](../qa/dialogue/cards033_gold4_actual.png). [완성 NT/원본 캡처 위치](../qa/dialogue/cards033_actual_pages.json).

ROM466960바이트, PRG256KiB/CHR200KiB, 예약8KiB 분산 bank170/187/192/195~199. 아래는 SHA256이다.

- 원본: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 033 / 재빌드 / 실제 적용: `aedbd41c9cb013ffcd4b809fa5288c4c9044040caf17caeacdc80439383e0af1`
- IPS: `5bf6d36d4468013d6cd9b32915c020fa524e27052dd2e95b93ad646a2d6a5873`
- CSV40draft: `347876b63d580132e06dbdf9c28350bac4f83ed5cc74e631ddddf3dc9458d08d`

[자산](../manifests/ui_cards_assets.json), [감사](../qa/reports/ui_cards_session_20261005.json). 새 파일: prepare_ui_cards.py/compile_ui_card_group.py/build_ui_cards.py/verify_ui_cards.py/verify_ui_cards_hooks.py/make_ui_cards_evidence.py, ui_cards_plan_001.json/변경 전CSV,033/재빌드/실제 적용, 다섯 경로 비교 캡처·IRQ·정수4배 실화면.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_ui_cards.py --output build/cards033_repro_next
python scripts/verify_ui_cards_hooks.py --build build/dialogue_kr_poc_033 --report qa/reports/cards033_hooks_repro_next.json
python scripts/verify_ui_cards.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_033/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/cards033_coaster_repro_next --frames 4200 --inputs config/menu_coaster_001.json --script scripts/trace_ui_consumers_v4.lua
python scripts/run_branch_seed_qa.py --rom build/dialogue_kr_poc_033/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/cards033_gold4_repro_next --frames 6000 --inputs config/menu_castle_001.json --seed config/gate_gold4_seed_001.json
```

고정 검증은 이40draft CSV에 적용한다. 후속 SSOT를 되돌리지 않고 나중에 재현할 때는 격리 복사본에서033 translation_used.csv를 사용한다.

다른 안내·변수·영문 그림·크레딧, 전체corpus/플레이, 오디오/reset/savestate/실기/최종 번역·명칭 검토와 기존PRG/RNG 영향은 남는다.033 도입부는 새로 실행하지 않았고 바이트 보존과 이전 실행을 참조한다. 개발용이며dist는 비어 있고 외부 게시하지 않았다. 원본/1편/모든 이전 산출물 보존.

다음 행동 하나: native29의 티켓 부족 경로와2B 소지 장수 표시를 실제 소비로 특정하고 두 안내를 한글화한다. 중단 지시 없이 계속한다.
