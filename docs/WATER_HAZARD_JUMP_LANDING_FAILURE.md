# 작업155 — 장애물 회피 성공, 재착지 실패

[검증/실패관측](../qa/reports/water155_landing_observation.json), [직접화면](../qa/reports/water155_visual.json), [계획](../work/water155/run_plan.json), [검증·인계](../scripts/verify_seal_water155.py).

현재049/3300프레임에서154의첫native피해2910보다20프레임앞선2890에A8만추가했다. 실제A80E 두번2800/2890이실행됐다. actor피해/체력쓰기0으로첫충돌은피했으나2926 nativeA7CF→state8/ACDF 물에빠짐을관측했다.체력3은유지됐고자연급류clear가아니다.

동결RAM snapshot2880/2892/2910/2922/2928을환경SHA와대조했다.2892부터playerX190/가로velocity0이유지됐지만boatX213→231→243→249와velocity260(1+4/256 pixels/frame)을확인했다.2910 playerY69의공중회피뒤2922Y106에서supportC1=0이었고2928state8이다. 이는jump가물체충돌만피하고통나무재착지조건은만족하지못한서로다른결과다.2910/2940두실제PNG에서공중과통나무앞물에빠짐/체력3을직접봤다.

좌표/속도/시간/RAM/ROM을수정하지않았다.해시/controller runtime와의도한회피판별은PASS지만요구한재착지는FAIL이다. 같은A타이밍유사retry를늘리지않고공중A749의right입력과boat속도상대연산을다음새CPU근거로검증한다.

변경: config/water_first_hazard_jump155.json,work/water155계획,새QA,관측/시각보고서,verify_seal_water155.py,상세·인계/journal·canonical·manifest/audit. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변. 원본·1편·실패/성공역사자료보존. 재현은계획의새QA출력경로. static/환경SHA·controller runtime·직접2PNG 수행.새build/apply/reset/state/audio/실기/사람최종없음. globalcorpus·自然전체진행·미연결소비·정식배포미완료. 카페완성기사/게시없음.

다음 작업 하나: 실측통나무속도260에대한 A749 공중좌우입력 native연산을원본/049 CPU로검증하고,2890 A8에right8만추가해같은장애물회피와재착지를시험한다.
