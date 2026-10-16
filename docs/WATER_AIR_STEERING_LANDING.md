# 작업156 — 급류 첫장애물 회피·통나무 재착지

[CPU모델](../qa/reports/water156_air_steer_model.json), [실제검증](../qa/reports/water156_steer_validation.json), [계획](../work/water156/run_plan.json), [준비](../scripts/prepare_water_steer156.py), [검증/인계](../scripts/verify_seal_water156.py).

155의실측boat가로속도260 fixture에서원본/049 nativeA749..A779를24쌍CPU로검증했다. heldright는boat+192/256,left는boat-192/256,no-direction은이전속도를유지한다. source/current명명한코드범위와전체RAM/register출력이같다. 관측boat260에서right는452(1.765625 pixels/frame)이되어움직이는통나무를따라갈수있다. 모델은실제재착지를대신하지않았다.

현재049/3300프레임에155의A8과같은2890 right8만추가했다. 실제두A점프/피해쓰기0·물에빠짐entry0.2892/2910/2922의player속도452/boat260과좌표192/213→223/231→244/243을확인했다.2922supportC1=1/jump128로재착지했고2930jump0으로복귀했다. 최종root4/phase5/체력3/발판1이다. 첫장애물회피와재착지PASS이며급류clear/全game완료가아니다. 이번직접PNG시각검토는없고nativeRAM/코드/실행검증이다.

변경:prepare_water_steer156.py,verify_seal_water156.py,config/water_first_hazard_steer156.json,work/water156계획,새QA,모델/실제보고,상세·인계/journal·canonical·manifest/audit. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변. 원본·1편·失敗155·이전관측보존. 재현은계획명령의새QA출력과검증코드복제. 정적/동결fixtureSHA·24CPU쌍·controller실행/실제값 PASS. 새build/apply/reset/state/직접PNG/청음/실기/사람최종없음. 자연후반·全corpus·HOWTO/PAUSE/POW·정식배포미완료. 카페기사/게시없음.

다음 작업 하나: native충돌사각형·공중속도·발판조건으로 급류 전용 컨트롤러 입력을 설계하고, 읽기전용관측 및 실제입력기록과 함께 자연후반진행을시험한다.
