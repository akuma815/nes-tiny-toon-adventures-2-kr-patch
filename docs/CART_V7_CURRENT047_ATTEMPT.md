# 작업117 — 현재047 방향 유지 실험 결과

[현재 v2 검증](../qa/reports/cart117_validation_v2.json), [최초 검증기](../scripts/verify_cart117.py), [v2 검증기](../scripts/verify_cart117_v2.py), [최초 가정 실패 기록](../qa/reports/cart117_v1_observation.json), [직접 장면 확인](../qa/reports/cart117_scene_check.json), [실행 환경](../qa/dialogue/cart117_headinghold047/environment.json). source SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지.

## 실제 진행 결과

[작업116 후보](CART_HEADING_HOLD_EXPERIMENT.md)를36000프레임 한 번 실행했다. 첫 방향 입력 차이는16220이며 그 앞16219개의 전체 controller 표본이 같은047 V6와 같다. 첫구간 통과는 유지했으나 두 번째 마지막2F가 남아 시간 초과 후 홈으로 돌아왔다. native phase5 관측은 level0/1, level3/phase14 표본0, gold/history는0이다. **전체3구간 자연 완주 미달이다.** PASS는 실험 관측·무결성 검증이며 클리어 성공이 아니다.

기존 해제창의 방향 유지391표본을 확인했다. 이번 active창에는 pit_avoid 예외0표본이었고, 지형 위험 시에는 여전히 동적 방향을 허용하는 코드가 남아 있다. native tile query71200행/고유32139입력이 CPU 분류와 같았다. 다른level 도메인으로 제외한 query는0이다.1362PNG의 mapped1KiB CHR10896조각은 사용047 ROM과 같다. 새 환경의 선언 runtime8185파일 SHA를 모두 확인했다.

[실패 직전18900](../qa/dialogue/cart117_headinghold047/frame_18900.png)의 플레이어·남은 적,19500의페이드/검정, [24000 실제 홈](../qa/dialogue/cart117_headinghold047/frame_24000.png)의 “몬태나 랜드/자, 어디로 갈까?”를 직접 확인했다.19500 검정 화면을 홈이나게임오버 증거로 부르지 않는다.24000과종료world의root08은홈 복귀를 뒷받침한다. 시간숫자 한 장으로native phase를대신판정하지않았다.

## 같은 입력 구간의 PNG 예외

prefix702시점의 RAM/PPU/OAM/매핑과전체core-state702파일은 모두V6와같다. PNG699장은같고3장은다르다. PNG포함5종3507파일 exact이며3 PNG를전체일치로주장하지않는다.

| 프레임 | RGB 다른 픽셀 | 차이 bounding box |
|---|---:|---|
|1281|8|(0,156)..(8,157)|
|2820|7028|(8,0)..(256,189)|
|4320|10630|(8,0)..(256,205)|

처음 검증기는전체PNGprefix동일을가정해실패했고그스크립트와관찰을보존했다. v2는raw/core동일성·PNG예외·실제진행결과를분리해기록했다. PNG를덮어쓰거나실패를숨기지않았다. 필터버퍼/비동기캡처와부합할수있으나이번증거만으로원인을확정하지않는다. [작업107](RIDE_SUCCESS_CURRENT047.md)의 실제53NT/RGB 비교와 [작업111](CASTLE_ROOM6_NATIVE_QA.md)의 실제107장 비교는그각각의검증된범위로유지하며, 모든capture가항상한프레임지연이라는일반보증으로확대하지않는다.

## 인계와 다음 조사

이실험은controller만사용했다. 체력·시간·금액·RAM·PC·state·ROM쓰기나새한글빌드·패치적용없음. 원본·1편·기존성공/실패·현재047·CSV를보존했다. 방향유지만으로전체실패를해결하지못했으므로이입력전략의유사winningbot 재시도는닫는다. 이것은작업가치판단이며추가사용자허가절차를뜻하지않는다. 자연전체완주·전역corpus/후보소비·사람최종검토·실기/PCM청음·정식배포미완료/release_eligible=false다. 카페완성작업기는전체완료후작성한다.

재현은기존출력덮어쓰기없이:

```powershell
python scripts/run_cart_rounds_qa_v7.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/cart117_headinghold047 --frames 36000 --inputs config/menu_cart_001.json
python scripts/verify_cart117_v2.py
```

변경파일은실행QA/검증기2개/가정실패/v2보고/scenecheck/본문서와오늘인계·journal·canonical문서다. V7후보/실행기는116동결파일이다. [동결manifest](../manifests/cart117_assets.json)에 SHA, source/1편/로컬링크감사는 `qa/reports/cart117_session.json`에기록한다.

다음 작업 하나: **pinnedMesen2.1.1의비동기decoder와screenshot 경로에3PNG예외를대조해캡처시간증거의범위를정리한다.** 이winningbot을다시실행하지않는다.
