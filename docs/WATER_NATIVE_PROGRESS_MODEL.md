# 작업152 — 급류 자연진행 실패와 점프·완료 조건

[CPU/역사관측 보고서](../qa/reports/water152_progress_model.json), [재현 코드](../scripts/analyze_water_progress152.py).

기존world043_water_controller(18000프레임)의 초기2790..3000 RAM 해시를 환경과 대조했다.2790 플레이어state2/supportC1=1에서2800부터점프없이left를눌렀고2820state3/2850state8/2970phase09/3000실패메시지phase0A로진행했다.체력RAM7C0는3이므로단순체력소진으로보고하지않는다. playerstate8=ACDF 물에빠짐과timer0530뒤phase09복귀를 코드로 연결했다. phase09는클리어판정이아니다.

원본/current049의명명한4코드범위를동일바이트로검증했다. snapshot 기반 A801의 입력flag 분기16쌍CPU는 RAM99가0일때 pressedRAM50 bit80에서만 jumpflag1/verticalvelocityFC/low0/artD3/다음A945를확인했다. heldRAM52 bit80만으로점프하지않는다. A67B의45쌍CPU는 state!=9/supportC1!=0/세로RAM69==16hex(22)일때만state09/0550=0을확인했다. native state09는B873실제clearhandler이며실패phase09와다르다. 비동기IRQ/PPU를포함하지않는D-clear NMOSCPU모델이다.

A69E..A6B2의10 state포인터와B879..B889의8 clear하위포인터를데이터로분리했다. 최초대화도구의선형disassembly에포인터byte가명령처럼보인부분은분석근거로사용하지않았다. 파일에저장된결과는정확한포인터표다. 기존143의2790RAM도seed없는모델fixture로해시확인했다. 새runtime·진행성공·clear실행·실제장면검토는없다.

변경: analyze_water_progress152.py, seal_water_progress152.py, water152_progress_model.json, 상세·datedhandoff·journal·README·SURVEY·PLAN·HANDOFF·manifest/audit. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변; 원본·1편·이전자료 보존. 재현 `python scripts/analyze_water_progress152.py` 기존출력거부. 정적/역사RAM해시/61CPU쌍 PASS. 새build/apply/emulator/직접PNG/청음/실기/사람최종 없음. 자연전체진행·globalcorpus·소비후보·최종검토미완료. 카페기사/외부게시없음.

다음 작업 하나: 현재049 급류 경로에서2800프레임에 A를 한 번 누르고 무조건 좌우이동을 제외한 읽기전용 관측으로 발판·물에빠짐·clear 상태와 세로진행을 기록한다.
