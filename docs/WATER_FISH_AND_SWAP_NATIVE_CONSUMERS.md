# 작업161 — 물고기 중력과 통나무교체 실제소비

[검증](../qa/reports/water161_fish_validation.json), [재현 명령](../work/water161/run_plan.json), [실제 쓰기](../qa/dialogue/water161_fish_consumer049/fish_physics_writes.csv), [물고기 궤적](../qa/dialogue/water161_fish_consumer049/fish_actors.csv), [준비](../scripts/prepare_water_fish161.py), [검증/인계](../scripts/verify_seal_water161.py).

160과5099입력/2154스냅샷 자료가 같다.183 실제쓰기 중2는 INC의 dummy쓰기,181은 최종쓰기다.181원본/049 한명령 CPU쌍이 beforeRAM 및 실제쓰기값과 같다. 별도12 CPU쌍은 native826F의 Vy+0020(0.125pixel/native step)을 검증한다. type34/state2는 Vx0140/VyFC7F로 시작하며 올라갔다 내려오는 곡선이다. 프레임마다 반드시 한물리step이라고 주장하지 않는다. 이전 type44 일정속도예측은 물고기 유형과 가속도를 다루지 않았다.

통나무교체 실제생산자는4034 A5BB INC0716(콜백pcA5BE/PRG325BE)이며0→1이다.160의4035 inputPolled 관측은 다른 event경계임을 구분한다. 두피해 입력/결과를 그대로 재현했으며 새회피성공은 없다.

변경:161준비/Lua/검증·work계획·새QA/보고·상세/인계/journal/canonical·manifest/audit. 원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`,ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변.각산출물SHA는manifest. 정적/193CPU쌍/실제consumer/입력·스냅샷exact PASS. 새입력성공/직접PNG/build/apply/reset/state/청음/실기/사람최종없음. 自然전체완주/전역corpus/HOWTO/PAUSE/POW/정식배포미완료. 재현은계획명령·검증사본에새출력경로.카페원고/게시없음.

다음 작업 하나: 확인한 type34의 중력을 포함해 다음 충돌을 예측하는 컨트롤러를 설계하고, 새049 실제입력/피해/갈아타기/후반진행을 검증한다.
