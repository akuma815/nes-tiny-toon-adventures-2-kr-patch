# 작업108 — 현재047 완료 범위와 미완료 조건 정리

현재047 ROM/CSV/원본을 변경하지 않고 기존 증거를 재정리했다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. [기계 원장](../qa/reports/scope108_reconciliation.json), [정리기v2](../scripts/reconcile_scope108_v2.py). 원본/1편/기존 빌드/증거/사람 결정pending 상태를 보존했다.

## 세 가지 서로 다른 목록

| 목록 | 확인한 분모와 의미 | 이 목록으로 주장하지 않는 것 |
|---|---|---|
| 등록 문자열 |54고유 원천=46본문+8macro,48pointer slot.45본문 초안+F9숫자1+공유macro7+등록내사용없는macro82 1 | 게임 전체100%, 일본어 문장9개 미번역 |
| 그림 검토 | 기존047 검토자료의33개그림 레코드 모두draft. 계획SHA 확인 | 전체그림33개로 폐쇄, 사람승인, 남은 후보3개자동보존 |
| native NT 원천 | 원본catalog의20개스트림, selector00..26 **16진수**의짝수20개. 원본 저장구간SHA 모두확인 |20개텍스트장면, 모든항목font124 사용, ASCII 후보가실제영문 |

33그림은 HUD6/보너스8literal/게임오버선택3/매표소5/기차3/생성형제목·지도·매표소·게임오버4/공지2/시작1/정지1의 기존검토목록이다. 크레딧3본문은 이미45초안 안에 있고33그림에추가로세지않는다. 크레딧의인명/제공사/법적문구는기록된계획대로보존돼있으며모든영문을일괄유지한다는새정책은아니다. title의PUSH START/법적표시는 [기존타이틀범위](POC_TITLE.md)로구분한다.

macro8정의의원본/현재바이트와등록소비45초안관계를대조했다. macro82는이등록본문에서사용0일뿐전역미사용증명이아니다.9technical/shared unit의원래untranslated표시를보존하고성급하게approved/translated로바꾸지않았다. 현CSV/검토원장의54문구는같다. [105문맥원장](../workspace/translation/scene_context_105.json)에서2행의scene/notes만정정됐으며CSV문구/ROMpointer오류가아니다.

## 아직 닫히지 않은 조건8종

1. 전역본문/그림corpus: 등록54/검토33/nativeNT20은각각범위가한정돼있다. 다른소비기/제외근거를연결해야한다.
2. HOWTO116117: 현재047에서장식소비는확인, label90..96은한경로에서관측0. 뱅크전체미사용이나원본유지승인아님.
3. PAUSE120121: 실제pause49와정적101..103은지정경로의공급경계만검증했다. 전역소비경로폐쇄아님.
4. POW61:7개유효정적descriptor와깃발positivecontrol은있지만실제POW생산자/가시소비는미연결이다.
5. 자연전게임플레이:카트첫구간은클리어했으나87/89두번째2F시간초과. 통화seed/체력보충/phase·root진단은자연완주를대체하지않는다. 새로운구별근거없이같은카트bot실험을반복하지않는다.
6. 최종사람문장·명칭·그림검토:45draft/33그림과후보3개는pending. 재개지시/합성JSON다운로드를승인으로해석하지않는다.
7. 지원환경/청음:현재privateMesen기술검증과별개로실기·PCM청음은미수행이다. 수행하지않은지원주장을추가하지않는다.
8. 정식배포/카페완성작업기:기술범위·사람품질·해당플레이검증이한artifact에서닫힌후작성한다. 현재ROM없는047검토패치의실제applyPASS는정식배포적격이아니다. 외부게시권한없음.

각 조건의기준·이미알려진것·다음구별근거를원장open_conditions에기록했다. 기존보고13개에는개별SHA/당시ROM/관측개입범위를표기했다.037/043/046결과를현재047새runtime처럼표현하지않고과거자료는그당시기준을유지한다. whole_game_completion_percent는null, product_closure/global_corpus_closed/natural_fullplay_passed/human_review_complete/release_eligible은false다.

현재초안을사람이검토하면명칭/문체/그림방향을정할수있지만수정에따른새빌드·관련경로QA가필요할수있다. 기술조사를계속하면누락된소비기불확실성을줄일수있지만언어/그림최종판단이나자연완주를대체하지못한다. 이번에는이미있는검토키트를보존하고, 독립적인기술조사인20NT스트림의실제소비문맥대조를진행한다. 사용자의범위축소/후보보존결정을대신하지않는다.

정적검증은현재CSV/검토일치·macro구간·NT20원본SHA·계획SHA와기존보고해시대조뿐이다. 새에뮬레이터/CPU/빌드/적용/직접장면검토는없다. v1원장생성기는중첩fallback괄호문법오류로실행전거절됐고v2에서명시적변수로해결했다. [실패관찰](../qa/reports/scope108_v1_observation.json)과v1을보존했다. 파일별해시는 [동결manifest](../manifests/scope108_assets.json)에있으며종료감사결과는 `qa/reports/scope108_session.json`이다.

재현 `python scripts/reconcile_scope108_v2.py`는기존보고서를덮어쓰지않는다. 변경파일은정리기2버전/실패관찰/원장/본문서/오늘인계·journal/README·조사·계획/HANDOFF다. 카페완성작업기는미작성이고오늘journal에근거만추가했다.

다음 작업 하나: **native NT20개(selector00..26hex)를동결된실제NT호출·font근거와대조하고미연결selector부터누락된텍스트/그림여부를판별한다.** 계속진행한다.
