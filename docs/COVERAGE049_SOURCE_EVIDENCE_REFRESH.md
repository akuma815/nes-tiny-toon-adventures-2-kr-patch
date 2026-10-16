# 작업145 — 등록54원천 검증 원장 갱신

[새 원장145](../workspace/translation/coverage049_145.json), [보존된 원장138](../workspace/translation/coverage049_138.json), [재현v2](../scripts/make_coverage145_v2.py).

139..144의 동결검증/manifest/직접시각 보고서를 기존138의54원천에 연결했다. 새 원장은 현재 초기화 또는 폰트/실제reader 중 하나로 연결된 main46개, 실제 읽힌 main25+macro6=31개를 구분한다. 31개 각각의 원천 전체byte offset이 실제data read로 확인되었다. 새보고서의 native model 전줄NT 완성 근거는16개 원천에만 연결했다. 직접PNG보고서는 별도 필드다. 현재보임46/읽기31/완성16은 서로다른증거이며같은완료율이아니다.

main46에는 변수전용 기술원천1개가 포함되며 문체 초안은45개다. sharedmacro8의 status/raw/reference는 SSOT그대로 유지했다. 각read는일치한ROM값/물리주소로귀속하고, 동적인nativeID/공유font만으로원천을정하지않았다. private226의macro88glyph 수명/부족문구완성 등129/133의scene보고서는기존근거로보존하며, 새reader 보고서가없는source에reader판정을추가하지않았다.

미연결reader23개(21main+2macro)는정확한목록으로보존한다. 포인터/폰트만으로미사용을선언하지않는다. macro82(MACRO061C9)의해당경로미관측을전역unused로바꾸지않았다. 다음한경로는카트의native짧은menu/fee/start다. 현재init/영상130과 별개로reader가미연결된rule1F/title25/cart85를소비주소로확인하려는새구분이다. 117에서닫은winningbot/완주stream과동일실험을되풀이하지않는다.

v1은read원천합집합을수기로30개라고추정해guard가실패했다. 실제는25main+6macro=31이다. 원천set54/범위/동결자료는그대로검증하고v2가실측31/미연결23으로검증했다. [v1관측](../qa/reports/coverage145_v1_observation.json)과실패스크립트보존. ROM/CSV/QA변경없음.

변경: make_coverage145.py/v2,prepare_coverage145_v2.py,seal_coverage145.py,coverage049_145.json,v1관측,본상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README·manifest/audit. 참조한보고서/manifest/CSV/ROM/추출목록의SHA를새원장에기록한다. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변. 원본/1편/138·이전증거보존.

정적/동결자료/원천set·서로다른검증분류 PASS. 신규runtime/build/apply/직접PNG/state/reset/audio/하드웨어없음. 기존각작업의runtime/direct PNG결론은해당보고서에만귀속한다. 재현 `python scripts/make_coverage145_v2.py`는기존출력거부. globalcorpus/자연전체게임완주/HOWTO·PAUSE·POW/사람문체·명칭·그림최종검토/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

다음 작업 하나: 현재049/새047의짧은카트메뉴·요금·출발경로에서실제reader를기록해 MAIN05867(rule1F)/MAIN058F6(title25)/MACRO061DE(cart85)를연결한다. 완주bot실험은재개하지않는다.
