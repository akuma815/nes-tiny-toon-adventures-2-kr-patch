# 작업163 — A 유지 회피와 자연 후반구조물

[검증](../qa/reports/water163_hold_validation.json), [10CPU중력 모델](../qa/reports/water163_hold_model.json), [준비 v2](../scripts/prepare_water_hold163_v2.py), [준비실패 기록](../qa/reports/water163_v1_preflight_error.json), [재현 명령](../work/water163/run_plan.json), [검증/인계](../scripts/verify_seal_water163.py).

native A held의 중력48/release80을10원본/049 CPU쌍으로 검증했다. type34 점프만A20으로늘려 앞서피해받은3물고기충돌이없고체력3을유지했다. 실제갈아타기stage1/2는이어지고7716의새type21 피해1회로체력2다. 자연8430에type2/2/2 artED/EE/EF 구조물이있고8603 native좌표분기가phase09를쓴다.기존type1 raft2만목표로하는정책은구조물로갈아타기를시도하지않았다.자연급류clear는없다.

입력4644행(4645이전)은162와같고비PNG raw1715개가모두같다. PNG342개RGB동일,4410 PNG하나는7326pixel/bbox8,0..256,189가다르다. 두PNG를직접검토했다.전체prefix RGB동일판정은FAIL이며특정프레임을예외허용해PASS시키지않았다. 캡처/렌더시점원인은미증명이다. raw동일과영상동일을구분한다. 기존118의이미지/event경계한계와같은종류일가능성은추정뿐이다. 준비v1 문법오류는실행/출력전발생했고보존, v2구문분석후새실행했다.

변경:163준비v1/v2/Lua/work/새QA/CPU·실행보고·검증/상세/인계/journal/canonical·manifest/audit.원본보존·ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변.각산출물SHA는manifest.정적/한정CPU/입력·raw·피해값 검증PASS,전체영상동일과자연완주FAIL. 새build/apply/reset/state/청음/실기/사람최종없음.全corpus/HOWTO/PAUSE/POW/전체게임/정식배포미완료.재현은계획명령·검증사본의새출력경로.카페원고/게시없음.

다음 작업 하나: 자연8430 구조물type2의 실제 목표/발판 소비코드를 원본/049 CPU와 관측fixture로 연결하고, 통나무와 구분한 구조물 도약 조건을 설계한다.
