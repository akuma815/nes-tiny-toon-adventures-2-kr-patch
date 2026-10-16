# 작업116 — 카트 방향 유지 실험 준비

[근거 보고](../qa/reports/cart116_policy_basis.json), [재현 생성기](../scripts/make_cart_policy116.py), [V7 Lua 후보](../scripts/trace_cart_rounds_v7.lua), [실행기](../scripts/run_cart_rounds_qa_v7.py). 현재047 ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지. 원본·1편·기존성공/실패·V6를 보존했다.

작업115의 실제 20개 해제창을 버튼 기록과 18개 접촉에 연결했다. 14개 창에서 시작 방향과 다른 조작이 있었고 총84 input 표본이 바뀌었다. 17421/18118의 반대 방향 전달은 창 중 `intercept`와 방향 변경 상태에 있었다. 18404창의 반복 속도교환은 방향이 유지된 상태에서도 발생하므로 방향 유지가 모든 실패를 해결한다고 주장하지 않는다.

V7은 이미 있는 level>=1/target2F 조건과16프레임 해제창에서 시작 방향을 보관하고 방향키를 유지한다. `pit_avoid` 조작은 계속 현재 지형에 따라 방향을 바꿀 수 있다. 첫구간·충전량/해제 조건·B 기준·지형/몸체 판정·timer·게임 ROM은 같다. 세 개의 정확한 코드 대체를 역으로 지우면 동결 V6와 전체 바이트 문자열이 같다. 하나의 조작 행동만 달라지는 별도 후보이며 아직 실행하지 않았다.

이번은 동결115 자료 해시·시계열 재검토와 후보 생성/정적 diff 범위 검사다. 새CPU/에뮬레이터/build/apply/직접 장면 검토 없음. 기존 V6의 첫구간만 통과/3구간 미달은 유지한다. 실제 새 궤적과 gold/history/구간 진행은 한 번의 다음 실행에서 판정한다. 실패하면 같은 근거로 변형 bot을 반복할 권한이나 성공 근거가 자동으로 생기지 않는다.

재현 `python scripts/make_cart_policy116.py`는 후보/실행기/보고서가 있으면 거부한다. 변경 파일은 생성기·V7 후보·실행기·보고서·본문서와 오늘 인계·journal·canonical문서다. [동결 manifest](../manifests/cart116_assets.json)에 SHA, source/1편/링크 감사는 `qa/reports/cart116_session.json`에 기록한다. 전역corpus·최종 사람 검토·자연 전체 완주·실기/PCM청음·배포는 미완료이고 release_eligible=false다. 완성 카페 작업기는 전체 완료 후 작성한다.

다음 작업 하나: **현재047에서 V7을 controller-only 36000프레임 한 번 실행해 최초 방향 override 전 prefix와 native 구간/history/gold 결과를 검증한다.** 성공/실패를 보존하고 같은 실패 전략을 반복하지 않는다.
