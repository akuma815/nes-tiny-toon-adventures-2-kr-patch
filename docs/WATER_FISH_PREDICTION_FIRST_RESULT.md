# 작업162 — 첫 물고기 회피와 두 통나무 교체

[검증](../qa/reports/water162_prediction_validation.json), [재현 명령](../work/water162/run_plan.json), [준비](../scripts/prepare_water_fish_controller162.py), [검증/인계](../scripts/verify_seal_water162.py).

前161과4637까지입력4636행/스냅샷2058개가같다. type34/state2의native중력32/step을예측에추가했다. 미래프레임당1물리step/raft일정속도는여전히가설이다.4637 실제점프로기존4658 첫피해를피했다.두번째갈아타기6593→6641도관측(stage2). 그러나4896/6914점프뒤4922/6941jump128착지flag에서물고기피해,7700 type21(shape1) 새피해로체력0이다.10500root8/자연clear없음. 가속도를추가한것만으로완주나전역회피를주장하지않는다.

변경:162준비/Lua/work계획/새QA·보고/검증/상세/인계/journal/canonical·manifest/audit.원본보존·ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변.각산출물SHA는manifest. 실행/입력·前스냅샷검증PASS,한정첫물고기/두갈아타기관측. 자연clear FAIL/전체게임·corpus·HOWTO/PAUSE/POW미완료. 새직접PNG/build/apply/reset/state/청음/실기/사람최종없음.재현은계획명령·검증사본의새출력경로. 카페원고/게시없음.

다음 작업 하나: native A held에 따른 중력30/50hex를 원본/049 CPU로 검증하고, type34 점프 A 지속시간만 늘려 착지 시점 피해가 사라지는지 새 실행으로 확인한다.
