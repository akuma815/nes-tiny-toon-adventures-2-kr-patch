# 작업143 — 현재049 급류타기 메뉴와 실제 reader

[최종 검증](../qa/reports/water143_validation.json), [직접 화면](../qa/reports/water143_visual.json), [실행 계획](../work/water143/run_plan.json), [검증](../scripts/verify_water143.py).

142의 동결 읽기전용 관측기/검증 기반을 사용해 현재049와 새047을 급류 메뉴 입력으로 각각4500프레임 실행했다. 냉부팅 기본티켓10장으로 진행하며 RAM seed/state load/ROM write가 없다. 요금3장 차감으로7장이 되고, 초기 급류 플레이를 거쳐 지도에 복귀했다. 실제course3/root4/phase5 게임 스냅샷은63개이며 급류 완주는 아니다.

312 whole PNG/PPU/OAM/mapping exact, 현재ROM과2496 CHR chunks가 일치한다. 실제 PRG data read150건씩의 주소·값·PC·프레임·순서·문맥이 같고96건cycle동일/39건+38/15건+76이다. helper18 writePC 이동은 같은STA 바이트로 확인했다. RAM22/IRQstack/A·flags/bus차이를유지하고전체CPU/IRQ/RNG/오디오동일성은주장하지않는다.

main21(MAIN058A6) 설명/main27(MAIN058FE) 제목/macro87(MACRO061EF)의 원천 전체byte가 실제로 소비되었다. native0E선택/21·27상단/1D요금/2A출발을따른다. font193 상단과196 하단을구분해 titleNT20A6/rules2125·2165는1578부터,출발22A8은2019부터native-reader모델의모든glyph와완성NT가일치한다. 요금·출발부분출력/지우기후폰트/다음지도는전체paired영상및선택직접화면으로확인했다.

직접1710 완성요금3/2010부분출발/2070완성/2790급류HUD007/4320지도5actualPNG를검토했다. 캡처118시점한계 유지. 신규실패없음. 원본/1편/역사QA/현재049/CSV보존.

변경: prepare_water143.py/run_water143.py/verify_water143.py/seal_water143.py;work/water143계획·log;qa/dialogue새047/현재049;최종/직접시각보고서;본상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README·manifest/audit. 실제재사용141/142 observer와검증스크립트도manifest SHA로동결한다. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변.

정적/해시/controller-only runtime/실제reader/whole영상/선택5PNG 직접 PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_water143.py`, `python scripts/run_water143.py`, `python scripts/verify_water143.py`;기존출력거부. 전체 급류/게임완주/globalcorpus/HOWTO·PAUSE·POW/사람문체·명칭·그림최종검토/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

다음 작업 하나: 무입력 인트로9문단을 현재049/새047에서6000프레임 실행하며 물리PRG 읽기를 추가해,현재 font128..146과각문단·macro의실제소비및완성NT를연결한다.
