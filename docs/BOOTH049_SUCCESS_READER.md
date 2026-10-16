# 작업141 — 현재049 매표소 성공 교환과 실제 대사 읽기

[최종 검증](../qa/reports/booth141_validation.json), [직접 화면 검토](../qa/reports/booth141_visual.json), [관측기](../scripts/trace_booth_reader141.lua), [실행 계획](../work/booth141/run_plan.json), [검증 스크립트](../scripts/verify_booth141.py).

현재049와 새047을 같은 관측기·입력·초기 seed로 각각4500프레임 실행했다. 과거039는 동결 입력과 점수 seed 공급자로만 명명한다. 1000프레임에 점수 digit3 및 나머지0을 기록한 진단이며, 점수를 자연스럽게 획득한 플레이는 아니다. 실제 점수판은3000점을 표시한다. 교환 후 티켓10→11장, 점수0으로 바뀌고, slot15의 매표소 인사 뒤 지도로 돌아왔다. slot15와 놀이기구 출발 slot2A의 원천을 섞지 않았다.

실제 PRG data 읽기131건씩의 물리주소·ROM값·순서·프레임·소비PC·문맥이 두 빌드에서 같다. Lua 관측은 읽기값을 반환하거나 ROM/CPU 상태를 변경하지 않는다. 실제 매핑의 PRG offset+header16으로 원천별 범위를 연결했다. native ID는 이미 다음 슬롯으로 증가할 수 있으므로 주소를 우선한다. 각 callback의 PC9395/9362/92CF 바로 앞의 실제 명령 B1 06도 확인했다. 주본문 MAIN05741/0574D/05762/05769/058F0/05777/05782/057AC가 읽혔고, macro84(놀이기구 이름),83(접미사),88(티켓)도 읽혔다. 보고서의11개 고유 읽기 원천은 main8/macro3이다. 실제 body의12바이트 전체와 macro88의5바이트 전체를 확인했다. 페이지 초기화만으로 소비를 주장한 결과가 아니다.

읽기 cycle은125건 동일,6건049가38cycles 늦다. 추가 관측으로 이전의 전역 타이밍 차이를 숨기지 않았으며, 이번 경로 밖의 모든 읽기·CPU·IRQ 동등성을 주장하지 않는다. 339 whole PNG/PPU/OAM/mapping은 같고 현재ROM과2712 CHR chunks가 일치한다. helper21개 write PC 이동은 실제 동일STA 명령으로 확인했다. RAM22/IRQ stack/A·flags/bus 차이는 별도 보고한다.

slot15의 실제 font188과 native reader 모델의 첫 줄8glyph/둘째 줄20blank가1899부터 actual NT와 일치한다. 1893 부분출력/1920완성/2010다음지도 화면을 직접 확인했다. 1680의RAM은 이미 티켓11/점수0이지만 같은 이름의PNG는10/3000을 보여준다. [118의 캡처 시점 한계](CAPTURE_FRAME_BOUNDS.md)를 유지하고 PNG 숫자변화가 정확히1680에 보였다고 주장하지 않는다. 1893 화면에는11/0이 보인다.

변경: prepare_booth141.py,trace_booth_reader141.lua,run_branch_reader141.py,run_booth141.py,verify_booth141.py,seal_booth141.py; work/booth141 계획·log; qa/dialogue의 새047/현재049 전 자료; 최종/직접시각 보고서; 본 상세/dated handoff·journal·SURVEY·PLAN·HANDOFF·README 및 manifest/audit. 신규 실패 없음. 원본·1편·역사QA·049·CSV 보존. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 개별SHA는 동결manifest/environment에 기록한다.

정적/동결해시/seeded runtime/실제 reader/whole 영상/선택4PNG 직접 검토 PASS. 새 build/apply/state/reset/오디오 청음/하드웨어 없음. 재현 `python scripts/prepare_booth141.py`, `python scripts/run_booth141.py`, `python scripts/verify_booth141.py`; 기존출력 거부. 글로벌corpus/자연 전체완주/HOWTO·PAUSE·POW/사람 문체·명칭·그림 최종검토/정식배포 미완료. 사람승인false. 카페 완성기사·외부 게시 없음.

다음 작업 하나: 메뉴 기차 경로를 현재049와 새047에서 동일 입력으로 실행하고, RAM seed 없이 실제 PRG 읽기·요금·상단20/26·출발2A·게임 진입의 폰트 수명을 검증한다.
