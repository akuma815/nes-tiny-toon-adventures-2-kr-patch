# 결과 화면 한글화 — 작업46 / 041

결과 화면의 축하 문구와 보너스·점수 7종을 한글 초안으로 삽입했다. 네 놀이기구의 최초 클리어 처리와 롤러코스터 재클리어 처리, 결과 후 지도 복귀·카드 재진입을 비교했다. **5,907화면과 354,362개 실행 시점 대조 통과**. 결과 진입은 지정 RAM seed이며 자연 클리어를 주장하지 않는다.

[전체 검증](../qa/reports/results041_validation.json), [실제 6장면](../qa/dialogue/results041_actual_pages.json), [자산·해시](../manifests/results_assets.json), [원본·이전 작업 보존 감사](../qa/reports/results_session_20261005.json). 기존 결과 소비 조사는 [작업45](RESULTS_CONSUMER_SURVEY.md)에 보존했다.

| 원문 | 한글 | 원래 NT 셀 수 |
|---|---|---:|
| CONGRATULATIONS! | 축하합니다! | 16 |
| LIFE BONUS | 체력 보너스 | 12 |
| CLEAR BONUS | 클리어 보너스 | 12 |
| TIME BONUS | 시간 보너스 | 12 |
| NOW YOU GET | 획득 점수 | 11 |
| POINTS (2곳) | 점 | 각각 7 |
| YOUR POINTS | 보유 점수 | 11 |

원본 source `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`. 기준040 `bdf5ca3a986d50b145571db13dfc75b58d3d2e4d140ae7805ef4a3f4f494ae0c`. [041 ROM](../build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes) SHA-256 `535fa114952587dfc0a6394ddff21b1aede053ade3dc0d3d9dfda77ed5888eae` / 483,344바이트. [IPS](../build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.ips) `f17bde7bb86332d75fa32c052b9c3ddf288c93f89e06c897648102b25ddc131c`. [재빌드](../build/dialogue_kr_poc_041_rebuild/build_report.json) 및 [한글·공백 경로 실제 적용](<../qa/dialogue/한글 패치 적용 041/TinyToon2_results041_applied.nes>) 전체 해시 동일.

변경은 CHR 크기 헤더26→27(216KiB), 실제 native 생산자 F8CF의 immediate/file3F8E0=7C→D0, 원래154바이트 배치스트림44A0B..44AA5 안의 8개 literal 본문, 추가208/209 글꼴이다. 기존 ROM의 나머지 바이트·124/125 원래 글꼴·기존 한글 글꼴은 전부 동일하다. 6KiB 추가 여백은 0. 압축 제어·NT 주소·속성·숫자 칸·literal 길이를 그대로 보존했다.

편집 원천은 [계획](../workspace/translation/results_graphics_plan_001.json), [native font208/209](../workspace/graphics/results_kr_001/font208_209.bin), [기술 변환 PNG](../workspace/graphics/results_kr_001/font208_209_4x.png). Galmuri7 v2.403/OFL의 20글자를 atlas와 TTF에 각각 대조했다. 기존 ASCII 숫자·구두점은 보존하고 1..20 빈 표시 문맥에 한글을 할당했다. [컴파일](../scripts/compile_results.py), [빌드](../scripts/build_results.py), [독립 검증](../scripts/verify_results.py), [native decoder 검증](../scripts/verify_results_native_decoder.py).

정적/CPU: 원본으로부터 8 Expected Write의 기대 바이트·범위 중첩·전체 결과를 검증했다. 생산자는 모든256 flags×3 초기값=768 ABI 사례, 11cycles 동일. 압축 해제803F/RAM0400/154바이트는 D-clear128사례, 4,086명령·12,385cycles·1,024개 PPU write의 주소와 시점 동일. NMOS6502 모델의 BCD D-set은 제외했으며 실제 NES 타이밍은 아래에서 별도로 비교했다.

에뮬레이터: Mesen2.1.1 격리 cold boot, root18=4/phase54=5/55=0 및 ride25<4를 확인한 뒤3200에54=20만 지정했다. 재클리어는 추가7E1=1을 먼저 지정한 별도 이력 분기이며 자연 획득 이력이 아니다. [V2 runner](../scripts/run_results_seed_qa_v2.py)는 이 두 설정만 허용한다. [밀집 캡처](../scripts/trace_results_seed_v2.lua)는 초기화 전후700프레임을3프레임 간격으로 기록한다.

보너스 5쌍 3,869화면 중 820화면에서만 한글8본문이 달라졌다. 문구 전체 native RGB, 숫자 영역, 문구 밖 모든 픽셀, OAM·팔레트·점수07F0..6·티켓·골드·획득 이력·phase가 일치했다. RAM 차이는34/3A의124→208와 실제 복사 literal의 알려진 값 쌍만 허용했다. 원래 CHR상대049FB의 스트림 전체가 실제 RAM에 복사되고, NMI 직후 글꼴208/209를 5경로 각18표본으로 확인했다. 두 IRQ 쌍의354,362개 frame/PC/scanline/dot/cycle가 모두 동일하며 결과 NMI font 값2,208개만124/125→208/209로 바뀌었다.

최초 처리 이력은 놀이기구 순서대로1/2/4/8, 골드1이 원래대로 기록되었다. 롤러코스터 실제 표시 기준 최초 클리어 보너스10,000점·집계15560점, 재클리어 보너스5,000점·집계10560점이며 재클리어 골드는0이다. 정수 RAM 한 바이트를 화면 점수 전체로 오해하지 않는다. 성은25=4이므로 이 보너스 seed를 적용하지 않는다.

회귀 2,038화면: 도입848·크레딧327·매표소339·성524에서 RAM/OAM/NT/팔레트/실제 화면 전체 동일. 성은 기존 gold4 초기 seed, 크레딧은 기존 selector seed의 실행 증거이며 자연 클리어/엔딩과 구분한다. 직접 시각 검토6장에는 최초·재클리어 집계 전후, 급류타기, 결과 후 카드 재진입이 포함된다.

재현(기존 build/QA는 덮어쓰기 거절; 새 경로를 선택):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_results.py --output build/새로운_041_재빌드
python scripts/run_results_seed_qa_v2.py --rom build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새로운_041_결과 --frames 7500 --inputs config/menu_results_001.json --script scripts/trace_results_seed_v2.lua --seed config/results_native_phase_seed_001.json
```

다른 놀이기구는 menu_results_cart/train/water_001.json, 재클리어는 results_repeat_phase_seed_001.json, 타이밍은 trace_results_seed_irq_v2.lua. 모든 실제 명령·환경·입력·seed·파일 해시는 각 environment.json과 used 파일에 동결했다. build_report의 runtimepending 문자열은 빌드 시점 상태이며 이 문서와 이후 PASS 검증이 최종 근거다. 기존 보고서는 덮어쓰지 않았다.

등록 CSV45draft/9기술·공유는 유지되며 전체 corpus 완료율이 아니다. 전체 자연 플레이·모든 게임 분기·오디오/reset/savestate/실기·최종 사람 문장 검토는 미수행. 전체 CHR 접촉표에서 별도 PAUSE/GAME OVER 그림 후보를 발견했고 실제 소비는 아직 조사 중이다. 040의 pause 관측에서 글자가 없었다는 것은 관측 경로의 한계이며 게임 전체 부재 증명이 아니다. 공개 배포·외부 게시 없음, 카페 작업기는 전체 작업 완료 후 작성한다.

다음 작업 하나: PAUSE/GAME OVER의 실제 배치·CHR78..7B 소비를 추적하여 추출한다. 중단 지시 없으면 바로 계속한다.
