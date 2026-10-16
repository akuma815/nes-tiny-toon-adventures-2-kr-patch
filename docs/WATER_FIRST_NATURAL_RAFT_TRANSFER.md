# 작업160 — 첫 자연 통나무 갈아타기

[검증](../qa/reports/water160_transfer_validation.json), [계획/재현 명령](../work/water160/run_plan.json), [입력전수](../qa/dialogue/water160_raft_transfer049/adaptive_inputs.csv), [갈아타기 관측](../qa/dialogue/water160_raft_transfer049/raft_transfer.csv), [준비](../scripts/prepare_water_transfer160.py), [검증/인계](../scripts/verify_seal_water160.py).

3985까지 이전158과 입력3984행/스냅샷1926개가 같다.3985 실제 낙하 통나무·앞 raft2 조건에서 A+우측을 시작했다.4035 native stage0716=1/raft1교체를 관측했고4050 jump0/support1/체력3으로 재착지했다. native생산자 A584..A5C6 source/current바이트는 같지만 이번에 PC 실행 콜백은 추가하지 않았다. 실제4020 공중·4050 두번째통나무 착지 PNG를 직접검토했다.이전4023 실패분기는없고6500 root4/phase5/발판1로진행했다.

4658/4925 두 피해는 실제 actor type34/art5F(shape0,state2)이다. 이전 type44만예측한범위밖이다. 체력3→2→1이며자연clear없음. 물고기 움직임의 실제 소비코드를 다음에 읽기전용 관측한다. 임의 무적/좌표/시간/ROM/RAM 개입없고 controller만조작했다.

변경:160준비/Lua/검증·work계획·새QA·보고·상세/인계/journal/canonical·manifest/audit. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`,ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변.각산출물 SHA는manifest. 정적/실행/첫자연갈아타기/2직접PNG한정 PASS. 자연급류clear와전체게임·전역corpus/HOWTO/PAUSE/POW미완료. 새build/apply/reset/state/청음/실기/사람최종없음. 재현은계획명령및검증사본에새출력경로사용. 카페원고/게시없음.

다음 작업 하나: 160의 같은 입력으로 첫 물고기 type34의 실제 속도/상태 쓰기와 native갈아타기0716 쓰기를 읽기전용으로 추적한다.
