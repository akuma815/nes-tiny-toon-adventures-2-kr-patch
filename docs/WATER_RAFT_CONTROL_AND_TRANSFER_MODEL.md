# 작업159 — 통나무 B 조작과 다음 통나무 연결

[검증 보고](../qa/reports/water159_raft_control_model.json), [분석 재현](../scripts/analyze_seal_water159.py), [실제3990 RAM](../qa/dialogue/water158_exit_input049/frame_03990_ram.bin).

원본/049 nativeAEDE..AF45를84쌍 CPU로 검증했다. B+우측이 기울기를+3 방향으로 바꾼다. B16D..B200 21쌍은 가로속도를5씩 target으로 이동시키며, angle0 target256/+3 target416이다. target 도달/유지는 실제 경로 검증이 아니다. 3990의 raft1 X1146/Y377, raft2 X1224/Y408(type1/artDF)은 기존 실제 관측이다. 다음 통나무가78px 앞에 존재한다. 이전 컨트롤러는 공중조작으로 raft1 중심을 계속 따라갔다. raft2 목표의 A/우측 갈아타기는 새 가설로 검증해야 한다.

작업158 prose/인계의32경계 CPU쌍은16쌍으로 정정한다. JSON16항목이 실제 결과다. 기존 동결 이력을 보존한다. 외부 설명서 PDF는 접근실패로 내용/조작 근거로 사용하지 않았다.

변경:159분석/공통인계스크립트·보고·상세/날짜별인계/journal/canonical·manifest/audit. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 각산출물SHA는manifest. 정적/105CPU쌍/fixtureSHA PASS. 새실행/직접PNG/build/apply/reset/state/청음/실기/사람최종없음. 자연갈아타기/전체게임/全corpus/HOWTO/PAUSE/POW/정식배포미완료. 재현은분석스크립트출력경로를 새이름으로복제. 카페원고/게시없음.

다음 작업 하나: 실제 raft2 존재와 낙차 조건에 따라 A+우측으로 착지 목표를 raft2로 바꾼 컨트롤러를 새049 실행으로 검증한다.
