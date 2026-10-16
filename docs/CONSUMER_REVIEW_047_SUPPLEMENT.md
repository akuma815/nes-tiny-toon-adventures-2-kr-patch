# 작업104 — 현재047 남은 그림 소비 검토 보충자료

현재047 ROM/CSV/기존검토패치를변경하지않았다. 원본/1편/이전 증거 유지. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. [내부검토 HTML](../workspace/review/consumer047_104_20261005/review.html), [ROM없는5파일 ZIP](../workspace/review/TinyToon2_Consumer_Review_047_20261005_104.zip).

ZIP SHA `20082bf789c4e7adf4a855daad425025b0869f973757a3e66ad61768cfb11504`,36454bytes. HOWTO/PAUSE/POW3후보,6이미지(현재047실제2/과거042실제1/정적추출·가설3)를자체포함한다. 기존54본문/33그림 [047검토자료](TRANSLATION_REVIEW_047.md)와 [047검토패치](REVIEW_PACKAGE_047.md)를대체하거나덮어쓰지않는다. HTML/consumer_records.json/DECISIONS_PENDING.md/README.txt/artifact_manifest.json의5파일이다. ZIP기본오류/전체파일byte동일/ROM·bin·state없음을검증했다.

HOWTO는99/100의nativeNT와actual장식positive control, PAUSE는49의실제4경로와101..103의한정된공급검사, POW는96정적7조립/97깃발actual/98다른bank불꽃배제를정리했다. 잘못된초기17혼합그림은포함하지않았다. HOWTO56×8,PAUSE48×32는원본CHR PNG에서정확한native타일영역을추출했으며실제표시나생성형그림이라고부르지않는다. 실제화면캡션에build/frame/seed와역사적범위를명시했다. 전역미사용/최종사람보존을자동결정하지않는다.

각후보의의견select/메모/JSON저장기능을추가했다. 기본3항목 pending, human_approved/release_eligible=false다. 선택값저장만으로ROM/SSOT/배포자격을변경하지않는다. [생성기](../scripts/make_consumer_review104.py)/[생성검증](../qa/reports/consumer104_build.json)의render pending상태는생성시점동결기록이고, 이후 [렌더검증](../qa/review/consumer104_047/render_report.json)은PASS다.

[렌더실행기](../scripts/render_consumer_review104.py)는사용자브라우저와별개의headlessEdge profile을썼다.1280/390폭 모두6이미지decode/3후보/수평넘침0/17px본문/controlsFit/externalImages0/JS예외0을검사했다.8PNG를보존했다. [desktop HOWTO](../qa/review/consumer104_047/desktop_HOWTO.png), [mobile POW](../qa/review/consumer104_047/mobile_POW.png)를직접보아실제·정적캡션과표시를확인했다. 실제버튼으로JSON다운로드후choice/메모를검사하고UI를모두pending으로되돌렸다. [다운로드](../qa/review/consumer104_047/synthetic_download/TinyToon2_047_consumer_review_input.json)는“합성 UI 저장 검사 — 사람 검토 의견 아님”으로표기한자동테스트파일이며사용자답변/승인으로취급하지않는다.

재현 `python scripts/make_consumer_review104.py`, `python scripts/render_consumer_review104.py`는각기존산출물/QA출력폴더를거부한다. 검토HTML은ZIP을풀고브라우저로직접열수있으며외부이미지/ROM/서버가필요없다. [동결자산](../manifests/consumer104_assets.json).

새게임runtime/빌드/적용없음. 전역corpus·자연전체완주·최종사람문장/명칭/디자인검토·PCM청음/실기/공식배포/카페완성작업기는미완료다. 사용자에게optional 조사우선순위를물었으며답변을기다리는동안독립적인본문문맥검토를진행한다. 질문은현재산출물승인이나자동범위축소가아니다.

다음 작업 하나: 현재CSV45초안과일본어원문/control·실제장면근거를대조해문맥·명칭·조사·행길이의문제및단일수정필요여부를기록한다.
