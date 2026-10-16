# 작업105 — 현재047 본문 원문/slot 문맥 검토

현재047 ROM/CSV/기존검토자료를변경하지않았다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. 원본/1편/이전 증거를보존했다. [검토기](../scripts/review_native_context105.py), [45개개별검토기록](../qa/reports/context105_review.json), [정확한문맥원장](../workspace/translation/scene_context_105.json).

45초안을일본어원문과실제등록문맥으로수동대조했다. 각entry별의미·목표·서비스말투·고유명칭·native폭/변수·보존결정의고유검토메모를남겼다. 최종사람번역/명칭승인이아니다. 문맥상필수인단일prose수정은이번검토에서찾지못했으며일괄규칙변환이나재번역을하지않았다. Acme/Buster/놀이기구명칭,일반티켓“도”의대안표현,요금/실패안내의명령말투,기차보스목표식표현은사람문체검토여지가남는다. 기술macro폭의기차내부3공백과F8숫자leadingblank를단순띄어쓰기오류처럼편집하지않는다.

기계검증은54원천의raw범위/SHA/원본SHA를원본과대조했다. 원본과현재047의native48 pointer는전부같고46main source에매핑된다. CSVreference_ids도일치한다.45draft에서FA/F8 placeholder3개는원문과번역의종류·순서가같다.9technical/shared unit은재번역하지않았으며미번역일본문장9개라고세지않는다. 이것은등록표의폐쇄이며게임전체corpus/모든직접출력엔진의폐쇄는아니다.

정확한장면정정2건: MAIN_057AC “언제든오세요”는slot15의매표소교환후재방문인사다. MAIN_05920 “출발!”은slot2A의놀이기구시작이고별개원천이다. 과거CSV의scene/notes가두QA장면을그룹으로함께표기한부분을원장context_overrides에서행별로바로잡았다. reference_ids/원문/번역과ROM pointer는원래부터정확하며게임오출력이나뜻오류가아니다. 동결047CSV/빌드/과거검토자료를조용히덮어쓰지않았다. 앞으로이두행의문맥은원장의exact_context를사용하고새SSOT개정이필요한시점에정정을반영한다.

원장SHA `f085ed822e44e2ff9c946297549879dda1e2bfa029beb7b213fea61e275149ae`. 재현 `python scripts/review_native_context105.py`는기존보고서/원장을거부한다. [동결자산](../manifests/context105_assets.json). 정적/기계 source문맥및assistant수동검토만추가했다. 새runtime/build/apply/직접scene검토는없다.

사용자의optional우선순위답변은아직없으므로독립적인본문QA를계속한다. 사람결정/공식배포/전역미사용을자동확정하지않는다. 전역corpus/자연전체3구간완주/PCM청음/실기/최종사람검토/카페완성작업기는미완료다.

다음 작업 하나: 현재047 일반놀이기구 normal티켓3 부족분기에서실제FA/F8 숫자출력과이어지는대사문맥을초기티켓seed명시로검증한다.
