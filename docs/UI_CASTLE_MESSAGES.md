# 성 입구 문구 5개 — 028 / 작업29

성 입구의 환영, 골드 티켓 조건, 부족 안내, 인사, 보유 여부 질문을 한글 초안으로 삽입했다. 54개 등록 원천 중 25개가 draft, 29개는 미번역이다. 전체 게임 완료율을 뜻하지 않는다. 숫자가 들어가는 일반 티켓 가격 안내 1A와 입장 허가 1C는 아직 일본어다.

| 원천 | 한글 초안 | 전용 글꼴 뱅크 |
|---|---|---|
| MAIN_057B8 | 어서 오세요 | 173/174 |
| MAIN_057C1 | 입장 조건은 골드 티켓 4장 / 있으면 입장할 수 있어요 | 175/176 |
| MAIN_057E5 | 아쉽지만 티켓이 부족해요 | 177/178 |
| MAIN_057F7 | 다시 오세요 | 179/180 |
| MAIN_0581B | 갖고 계세요? | 181/182 |

성은 IRQ 분할 없이 RAM34가 두 행의 글꼴을 공급한다. 027의 동일 시간 초기화 helper008을 그대로 사용했다. 원본 macro ID/FE/FF/FD/리터럴00 위치와 raw 길이, 문단별 reader 출력 수·호출별 cycle·cursor를 보존했다. 4와 물음표는 원래 글리프를 명시적으로 복사하고 한글은 고정 해시의 Galmuri7 PNG와 TTF 양쪽이 같은 비트맵인지 검증했다. 글꼴 대체는 없다. 배정 밖 원본 숫자 글리프와 일본어 fallback171/172, 이전 20개 초안·타이틀·도입부를 보존했다.

## 검증과 한계

[독립 검증](../qa/reports/gate028_validation.json)은 원본 ExpectedWrites/중첩0 및 이전027 전체 이미지의 지정 변경만 허용했다. [CPU ABI](../qa/reports/gate028_hooks1504.json) 1504건과 초기 글꼴 seed720건, 실제 352d9cf7f33ecefdba41b897bc12b989acff3b18eaaf81a087f2fe3774cba136 적용과 재빌드 해시가 통과했다.

Mesen의 동일 입력 성 경로에서 화면474장 중167장은 현재 대사 행만 바뀌고307장은 전체 픽셀이 같았다. 현재 행 바깥 픽셀 변화0, 보호 네임테이블·팔레트·OAM·게임 상태가 같았다. RAM00와740..753의 출력 버퍼 차이는 원래 reader를 두 c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e으로 재실행한 바이트 쌍만 허용했다. NT3000..3EFF는2000..2EFF의 하드웨어 mirror로 같은 행만 검사한다. 단순히 게임 RAM 전체나 대화상자 전체를 제외하지 않았다. IRQ/NMI/PPU/mapper69714개 실제 시점은 같고 글꼴 선택값2908개만 달랐다. 일본어 일반 가격1A로 돌아간9개 전체 화면도 같았다.

[완성 문구 5개의 실제 화면](../qa/dialogue/gate028_actual_pages.png)은 완성 NT 바이트를 확인한 frame1650/1848/2127/3321/2718이다. 정수4배 확대에서 한글·숫자·물음표를 직접 검토했다. 새028 도입부 실행은 반복하지 않았고 바이트 보존과027의 기존 실행 근거만 있다. 충분한 입장권 분기, 교환 성공, 상단 설명 카드, 기타 그림·크레딧, 전 corpus, 전체 플레이·오디오·reset·savestate·실기·최종 번역 검토는 남는다. c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e450576바이트, CHR184KiB, 분산 예약2KiB. 개발본이며 dist는 비어 있다.

## 해시와 재현

- 원본 SHA256: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 028 c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e / 재빌드 / 적용 SHA256: `c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e`
- 352d9cf7f33ecefdba41b897bc12b989acff3b18eaaf81a087f2fe3774cba136 SHA256: `352d9cf7f33ecefdba41b897bc12b989acff3b18eaaf81a087f2fe3774cba136`
- 2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8 SHA256: `2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8`

[자산 목록](../manifests/ui_gate_assets.json), [세션 감사](../qa/reports/ui_gate_session_20261005.json). 이전 산출물과 첫 번째 게임은 보존했다.

```powershell
python scripts/build_ui_gate.py --output build/gate028_repro_next
python scripts/verify_ui_gate_hooks.py --build build/dialogue_kr_poc_028 --report qa/reports/gate028_hooks_repro_next.json
python scripts/verify_ui_gate.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_028/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/gate028_castle_repro_next --frames 4500 --inputs config/menu_castle_001.json --script scripts/trace_ui_consumers_v4.lua
```

위 고정 빌더/검증은 당시25개 draft SSOT와028 입력에 적용한다. 이후 SSOT 변경 뒤 과거 검증을 그대로 실행하지 않는다.

다음 행동 하나: 골드4장과 일반50장의 성공 입장 분기를 명시적인 RAM seed QA로 관측하여 가격1A/입장1C의 실제 소비를 확인한다. 바로 이어간다.
