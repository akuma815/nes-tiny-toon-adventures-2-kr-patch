# 작업89 — native 방향벡터에 맞춘 A 해제 실험

작업88의 실제 충돌 근거에 따라2F 밀기 접근각을 좁히고, native RAM9D/9E의 X·9B/9C의 Y방향벡터가구멍 쪽과0.80초과로정렬되며 충전512이상·거리48미만일 때16프레임 A를해제하는 V6 controller를 시험했다. 첫구간·pit회피B·게임 ROM은 유지했다. [정책 생성기](../scripts/make_cart_policy089.py)에 각 변경을 재현 가능하게 기록했다.

[검증 보고서](../qa/reports/cart089_validation.json). 현재046의36000프레임에서15536에 처음controller가달라졌고, 그전15535행/3395개PNG·RAM·PPU·OAM·매핑 파일이V5와byte exact다. 조건에 맞는20개 burst가 발생했고 로그24개 eligible 행의 charge/정렬/16프레임 해제가 정책과 일치한다. 첫구간 클리어는 유지됐으나 두번째 마지막2F가 남은 채 시간 초과·홈 복귀했다. Gold/history0, 전체3구간 자연완주 미달이다. PASS는실행·관측 검증이며 클리어 성공이 아니다.

새경로 native query71042행/고유29767입력을CPU 분류와 대조했고,1362PNG/10896개1KiB CHR매핑 및runtime8185파일을검증했다. [실패직전](../qa/dialogue/cart089_aligned2F046/frame_18990.png), [홈복귀](../qa/dialogue/cart089_aligned2F046/frame_24000.png)를직접확인했다. 나머지 전수 육안 검토를 주장하지 않는다. ROM/CSV/원본/1편/검토 패키지 변경 없음, 임의체력·시간·금액·RAM·PC·상태 개입 없음.

V5/V6는 새native 근거로 만든 서로 다른 실험이지만 전체완주 결과는 동일하게 실패다. 추가자동입력 변형을 반복하는가치는낮으므로 이결과를보존하고 번역원문·문맥/화면검토로돌아간다. 자연전체완주·청음·실기·최종사람번역·전역corpus는미검증으로남긴다.

[Lua](../scripts/trace_cart_rounds_v6.lua), [실행기](../scripts/run_cart_rounds_qa_v6.py), [환경](../qa/dialogue/cart089_aligned2F046/environment.json), [검증기](../scripts/verify_cart089.py), [동결 파일/SHA](../manifests/cart089_assets.json). 새폴더로 `python scripts/run_cart_rounds_qa_v6.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 36000 --inputs config/menu_cart_001.json`.

다음 작업 하나: 등록번역54원천과 실제그림33문구를 원문/문맥과 수동대조해 표현·매크로·변수·크레딧 유지 항목을 정리하고, 수정이 필요한 한 항목부터 재현 가능한 다음 빌드로 다듬는다.
