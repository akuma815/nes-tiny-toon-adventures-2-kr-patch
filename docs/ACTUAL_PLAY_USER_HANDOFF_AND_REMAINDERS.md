# 작업165 — 실제 플레이 사용자 이관·잔여 정리

[검수 소유권/남은 일](../qa/reports/play_owner165_handoff.json), [165 실행계획](../work/water165/run_plan.json), [165 준비](../scripts/prepare_water_rope165.py), [정리기](../scripts/seal_play_owner165.py).

사용자가 실제 플레이 검수를 직접 맡겠다고 지시했다. 자동플레이/완주 컨트롤러 실험은 이 시점에 종료한다. 확인한 owned Mesen PID14764(parent13464/정확한전용exe와165명령)만 종료 요청했고 runner는종료했다. 보존된11500 완료마커/exit0 및3644산출물SHA를확인했다. 이는자료보존검증이며새플레이성공/실패/완주판정은추가하지않는다. 첫C9/0541쓰기자료등도보존한다. 실제플레이판정은사용자담당이다. 새에뮬레이터실행없음.

플레이를제외한잔여: (1)등록54문자/33그림/20NT 밖 전역원천누락·제외근거폐쇄, (2)HOWTO116117·PAUSE120121·POW61의실제대상/미사용/원본유지결정, (3)45문장초안과33그림/명칭/타이틀의최종선택, (4)163 PNG4410비교실패의캡처근거정리와지원되지않는전체영상동일주장제외, (5)수정반영후정식ROM없는배포설명·해시·도구라이선스·패키지, (6)모든작업완료뒤네이버카페본문·이미지·읽기HTML·업로드안내. 외부게시권한은없다. CSV9untranslated는기술/공유macro·숫자단위이며9일본어문장미번역이라는뜻이아니다.

현재검수본: [ROM049](../build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes), [ROM없는적용ZIP](../dist/TinyToonAdventures2_KR_Review_049_20261006.zip), [문장/그림검토HTML](../workspace/review/translation049_20261006/review.html). ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변. 검수패치ZIP SHA `27404b77f6afc4a6ad8e1e51e357a89aba804b0c5631fbac5193862acb2de42e`; 정식배포판은아니다. 기존132실제적용/133reset-state보고PASS는해당범위의역사검증으로보존하며재실행하지않았다.

변경:165준비/Lua/계획·QA보존·소유권보고·상세/날짜별인계/journal/canonical·프로젝트AGENTS·manifest/audit. 원본·1편·현재빌드·기존실패보존.각산출물SHA는manifest.이번정적SHA/완료마커/소유프로세스정리만수행.새CPU/build/apply/직접장면검토/청음/실기/사람최종없음. 미완료조건은사용자플레이검수와별개로위목록에기록한다.

다음 작업 하나: HOWTO/PAUSE/POW 및 등록범위 밖 원천의 기술 잔여를 정적으로 정리해 번역 추가·제외 판단 근거를 작성한다.
