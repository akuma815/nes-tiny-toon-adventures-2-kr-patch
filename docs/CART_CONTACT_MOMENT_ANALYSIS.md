# 작업114 — 실제 속도와 A 해제 시점의 카트 실패 재검토

[분석기](../scripts/analyze_cart114.py), [초기 보고](../qa/reports/cart114_analysis.json), [메타데이터 정정기](../scripts/finalize_cart114.py), [현재 v2 보고](../qa/reports/cart114_analysis_v2.json). 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`,047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`,CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지. 원본/1편/046·047·CSV·기존 성공/실패 증거 보존.

source bank38..3B의32KiB가046/047에서도 같다. 카드 구간 완료 조건·collision·geometry는 앞서 [작업69](CART_CLEAR_BRANCH_SURVEY.md), [작업88](CART_COLLISION_CONSUMER.md)의 named native 소비를 사용했다. 기존046 관측을 현재047 새 게임 실행처럼 표현하지 않는다.

## 작업88 방향 계산 정정

작업88 스크립트/보고에서 level1 구멍 방향을 첫 구간의 중심128,256으로 계산했다. 기존 V6의 level1 geometry 중심은224,464이며 실제 native classifier에서 class0F다. level1의128,256은class0이다. 각level0/1/2에서 세 후보를 대조한9개 CPU 사례는각128,256/224,464/224,256만hole class0F임을확인했다.

해시로 확인한 기존 실제 before_swap206행을 올바른level1 중심으로 다시 계산했다. 구멍 방향 양수91/반대106/속도 또는내적0은9다. 동결된88 보고의92/105는 정정 대상이다. **77개의 개별 부호가 바뀌었고 합계의 변화는 양수−1/음수+1이다.** 실제206RAM/CPU 속도교환 검증·거절4262쌍·zero fallback·파일 동일성은 기존 근거로 유지하며 다시 수행했다고 주장하지 않는다. oldsource/controller/ROM을고치지않았다.

## V6 입력 기록의 새 구분

해시로 확인한89의20개 A 해제 burst 시작에서 native 기본 방향 벡터는 모두구멍과0.8보다높게정렬되어있었다. 그러나그때실제플레이어8.8속도는구멍쪽8/반대10/0이2다. 기본방향 벡터와누적속도는같은값이아니다.

각16프레임해제창의 inputPolled 위치에서 두축모두24미만인근접표본을가진창은5개,없던창은15개다. 이것은실제CPU collision 발생이아니며,이거리표본만으로교환이나A해제의성공을판정하지않는다. 첫구간은통과/둘째마지막2F가남는89의실패결과를그대로보존한다. 단일실패원인을확정하지않았다.

새 가설은 **방향 정렬·충전량만으로는 실제 접촉 순간의속도전달을보장하지않는다**는것이다. 같은 V6를읽기전용으로추적해 burst와native9D53 교환시점을대조해야정책변경의근거가된다. 이번에새winningbot을실행하지않았다.

## 검증과 인계

정적32KiB source/046/047비교·새offlineclassifier9사례·동결된88/89 선택CSV/환경/보고SHA 재검토다. 새에뮬레이터/build/apply/직접장면 없음. 초기114보고의limit문장은합계1변화를개별1건변화로잘못표현했으나이미보존된목록은77건으로맞았다. 별도v2가77부호/합계1변화와실제callback주소를명확히했고기존보고를덮어쓰지않았다. 부가 탐색에서 scripts 경로를넣지않은import 실패와존재하지않는파일명검색은제품/QA쓰기전에발생했고sys.path/실제파일명으로수정했다.

재현 `python scripts/analyze_cart114.py`, `python scripts/finalize_cart114.py`는기존출력덮어쓰기를거부한다. 변경파일은분석기·정정기·보고2개·본문서와오늘인계/journal/canonical문서다. [동결 manifest](../manifests/cart114_assets.json)에 SHA, source/1편/로컬링크감사는 `qa/reports/cart114_session.json`에기록한다. 자연전체3구간완주/전역corpus/사람최종검토/실기·PCM청음·정식배포는미완료/release_eligible=false. 카페완성작업기는전체완료후작성한다.

다음 작업 하나: **현재047에서 V6 controller를그대로두고 실제2F/player 충돌읽기전용callback을추가해16프레임burst중교환된속도를검증한다.** 기존89prefix와대조하고새winning정책은아직넣지않는다.
