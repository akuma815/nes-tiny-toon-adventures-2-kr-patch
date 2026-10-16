# 플레이 HUD 한글화 — 작업44 / 040

현재 채택 `dialogue_kr_poc_040`. 별도 그래픽 초안 6종: 체력, 점수, 시간, 점, 티켓, 금티켓. 금티켓은 대사의 골드 티켓을 줄인 HUD 표기다. 등록 문단 SSOT는45draft/9기술·공유 원천 그대로이며, 이 수치를 전체 게임 완료율로 쓰지 않는다.

| 파일 | SHA-256 |
|---|---|
| 원본 | f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d |
| [040 ROM](../build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes) | bdf5ca3a986d50b145571db13dfc75b58d3d2e4d140ae7805ef4a3f4f494ae0c |
| [040 IPS](../build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.ips) | 1d3a3a53cec8b2e7e492010ac5415975c3abaafb7e6c63872c56767223c7b2fd |
| 문단 CSV | 26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27 |

변경 원천은 [그래픽 계획](../workspace/translation/game_hud_plan_001.json), [compiler](../scripts/compile_game_hud.py), [builder](../scripts/build_game_hud.py), [독립 검증](../scripts/verify_game_hud.py), [순차 실행](../scripts/run_game_hud_suite.py), [회귀 실행](../scripts/run_game_hud_regressions.py)이다. [native font](../workspace/graphics/game_hud_kr_001/font206_207.bin), [Expected Writes](../build/dialogue_kr_poc_040/expected_writes.json), [빌드 보고서](../build/dialogue_kr_poc_040/build_report.json), [실제 적용본](<../qa/dialogue/한글 패치 적용 040/TinyToon2_hud040_applied.nes>)을 보존한다. 원본/1편/실패본 포함 모든 이전 산출물은 보존한다.

원래124/125 글꼴을 전용206/207로 복제했다. Galmuri7 atlas/TTF가 같은9한글 문자의 비트를 제공하며,20캡션 타일만 편집했다. 원래숫자70..79, 곱셈33, 하트, 기호, 틀과 나머지타일은 그대로다. 현재208KiB CHR의 마지막 예약2KiB73810..74010을 사용하여475152바이트 크기를 유지한다. 기존 타이틀·지도·매표소·크레딧 글꼴/대사/그래픽은 수정하지 않았다.

원래 영문 상단은5행만 보인다. [NESdev PPU scrolling](https://www.nesdev.org/wiki/PPU_scrolling)의 내부v와fineY 구성을 실제 IRQ/화면과 대조하여 $2006 첫 값2F→0F로fineY2→0을 적용했다. NT주소의low12는 유지한다. 상단 한글은7행을 확보하고, 하트/본문/숫자/틀 및 하단검은여백은2픽셀 아래로 이동한다. 이 배치 변경을 동일 좌표 보존이라고 주장하지 않는다. IRQ 자체의 실행 시점은 동일하다. native HUD는기차y191,나머지관측경로y190이며,기차의원래1픽셀차이도유지한다. 소유영역은y190..239, 게임 화면y0..189는 전체 픽셀 동일하다.

정적/CPU: 원본 Expected Writes8범위·기대 원본·중첩·전체최종diff 검증.039와의 차이는 예약 font206/207 및 fixedIRQ immediate2곳3FCE5/3FCF9만이다.768플래그/카운터조건에서 CPU ABI/RAM/PRG와 쓰기시점 동일, 바뀐쓰기값은 font124/125→206/207 및fineY첫값2F→0F뿐이다. 글꼴은 TTF로독립재구성하여 전체2KiB 일치했다.

빌드/적용: 별도040_rebuild와 한글/공백 경로에서 실제CLI IPS 적용 출력 모두 전체SHA 동일. 에뮬레이터 결과와 구분한다.

실행: [4558화면·1321047동일시점 검증](../qa/reports/game040_validation.json). coaster12000/cart10000/train10000/water10000, gold4초기seed castle6000, pause/resume6000 및 매표소4500/intro6000/credits9000를 이전039와 비교했다. 모든 비교 RAM2KiB/OAM/NT/팔레트 동일, 변경된장면의 한글캡션은 native RGB 전체일치, 하트/숫자/곱셈은2픽셀 이동후전체RGB 동일. HUD 밖 변경0. 시작/정지/진입/퇴장과실패후메뉴 복귀도 비교에 포함된다. source/target IRQ 로그의 각frame/PC/scanline/dot/cycle은 전부 동일하며 허용된3종 값만 차이난다. [Start pause 관측](../qa/reports/game040_pause_observation.json)은RAM55=1 표본40개3402..3798,3900에는0이다.

직접 시각: [실제 6장면](../qa/dialogue/game040_actual_pages.json)의 코스터/카트/기차/급류/성/일시정지를 확인했다. 실제 화면4배 확대만 했고7행 한글의 잘림을 확인했다. 관측 장면에서 잘린 획은 없으며 틀/원래숫자/하트가 보인다. 자연완주/전체플레이/오디오/reset/savestate/실기/최종사람검토 증명은 아니다. castle은 gold4 seed로입장,credits는이전과동일4주소 ending seed다.

실패·정정: 첫 suite는 잘못된Lua파일명으로 Mesen실행전에 중단됐다. [기록](../qa/reports/game040_suite_bootstrap_failure.json)과빈부분디렉터리를보존하고,실제 trace_ui_consumers_v4를사전확인한새_v2이름으로실행했다. 최초검증기는모든HUD를y190으로가정하여기차하트비교에실패했다. [정정근거](../qa/reports/game040_train_geometry_diagnostic.json)는원래FCF1/A008의scanline+1과직전화면시점을사용한다. 허용픽셀조건을느슨하게바꾸지않았고기차64변경장면의캡션76288/하트·숫자135168픽셀전체일치했다. 040ROM 자체의실패수정은아니다. 첫 인계감사에서journal하위폴더에붙인43/44링크의상대경로가틀려실패했고,../를추가해해결했다. 원본·빌드·runtime증거는영향없다. 변경이력/실행산출물은보존했다.

재현은 기존 검증폴더를덮어쓰지않는새출력명을쓴다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_game_hud.py --output build/dialogue_kr_poc_040_replay
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/replay_game040_coaster --frames 12000 --inputs config/menu_coaster_001.json --script scripts/trace_ui_consumers_v4.lua
python scripts/verify_game_hud.py
python scripts/audit_game_hud_session.py
```

순차suite가 사용한 원래 모든 명령/Lua/설정/inputs/seed는 각environment.json과*_used 파일에동결되어있다. suite는이미존재하는출력에거절하므로재실행은별도이름으로한다. builder/검증은GUI에뮬레이터를새로여는권한요청없이기존허가범위에서진행한다.

[자산목록](../manifests/game_hud_assets.json), [원본·1편·역사·runtime·인계링크 감사](../qa/reports/game_hud_session_20261005.json), [날짜별 인계](HANDOFF_2026-10-05.md). dist는빈상태며외부게시없음. 기존PRG/RNG 한계,전체corpus와최종언어검토는미해결이다.

다음행동 하나: 실제결과초기화와font124/CHR24A0B를연결하고보너스7종문구를한글화한다. nativephase20의준비시험은진행했으나별도작업45인계에서완료근거를정리한다. 바로계속한다.
