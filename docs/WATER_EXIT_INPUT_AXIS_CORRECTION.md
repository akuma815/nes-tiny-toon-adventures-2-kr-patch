# 작업158 — 실제 실패 전환·입력 소비·축 이름 정정

[검증](../qa/reports/water158_exit_input_validation.json), [재현 명령](../work/water158/run_plan.json), [실제 컨트롤러 버스](../qa/dialogue/water158_exit_input049/controller_bus.csv), [실제 이탈 코드](../qa/dialogue/water158_exit_input049/water_exit.csv), [준비](../scripts/prepare_water_trace158.py), [검증/인계](../scripts/verify_seal_water158.py).

157과 같은 입력4499행 및2034개 스냅샷 자료가 정확히 같다. 실제4023/A658→A65A→A65C는 phase5→9를 기록했다. 조건은 state09가 아닌 상태에서 플레이어0480!=0/0470>=E0이고 관측값은01/E4, 체력3이다. 원본/049의 해당 코드 및32경계 CPU쌍이 같다. 물/객체 피해 대신 이 좌표 분기가 실패 전환을 일으켰다.

은행36/9582 투영 루틴은 X actor04A/B에서6D/69를 빼 RAM02에, Y actor047/048에서6B/68을 빼 RAM01에 기록한다. 8쌍 CPU는 X80/Y96으로 검증했다. **152–157의 vertical_hi/lo(RAM69/6D)는 cameraX로 정정한다. cameraY는 RAM68/6B다.** 기존 동결문서/CSV/보고는 보존한다. 값·실제 분기·충돌상자 계산은 바꾸지 않으며 진행 최대3/4 및 clear69==16hex는 수평카메라 페이지다. 122의 축 이름 오류와123의 RAM02/01 정정 이력도 보존한다.

3300..4050의13956 버스 사건에서665 native 입력 세션,647번은 두8bit 읽기와 최종요청/RAM52가 정확히 같다. 18세션은 RAM52 기록이 없고 일부 추가읽기/포트2원인은 이번 포트1 관측으로 미폐쇄다. 요청과 소비를 동의어로 사용하지 않는다. 이전157의8 불일치는 직전프레임에 native 입력 읽기가 없었으며 이전 실제 RAM52 쓰기가 모두 설명한다. 플레이 기록750개도 마지막 실제쓰기와 같다. 프레임 라벨을 임의 확대하여 맞추지 않았다.

변경: 새158 준비/Lua/검증 스크립트, work/water158, 새QA·보고·상세/인계/journal/canonical·manifest/audit. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 각 산출물 SHA는 manifest. 정적/한정CPU/같은입력/실제bus/실패코드 PASS. 새 직접PNG 시각검토·build/apply/reset/state/청음/실기/사람최종 없음. 전체입력무오류/자연완주/全corpus/HOWTO/PAUSE/POW/정식배포 미완료. 재현은계획명령에 새출력경로 및검증출력변경한사본. 카페 원고/게시없음.

다음 작업 하나: 急류 통나무의 B+좌우 native 기울기/이동 코드와 첫 낙차 직전 fixture를 원본/049 CPU로 검증하여, 화면하단 이탈을 피할 입력 후보를 근거로 설계한다.
