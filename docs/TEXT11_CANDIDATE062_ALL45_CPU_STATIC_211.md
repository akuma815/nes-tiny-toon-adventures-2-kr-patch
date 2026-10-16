# 작업211 — 062 등록45개11px 빌드·CPU·정적 복원

[062 ROM](../build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes) SHA `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`·524304바이트에 등록45개(오프닝9+일반33+크레딧3)를11px로 삽입했다. [정적45문단·상단창5모형](../workspace/review/text11_211/review.html), [원장](../qa/reports/text11_211_static_review.json). HUD·정지 등 작은 그림, 번역CSV,원문유지6건은 기존대로다. 크레딧 이름·KONAMI·법적 문자열은 보존하고11px 획으로 확대했으므로 옛 글자 bitmap 보존이라고 주장하지 않는다. 영문16px 간격은 개발안이다.

정적·빌드: 원본ExpectedWrite 전체·허용 diff·IPS 적용·독립 ROM/IPS 재빌드 exact. 기존42개의 문자 스트림/글꼴 픽셀은059와 동일하다. 새크레딧 font201/202 106슬롯을 사용한다. [기존42 CPU](../qa/reports/text11_211_ordinary_CPU.json):33문단1042수치상태/1071건너뛰기/4320초기화/1556비대상/교환050 보존10/놀이기구5개 동시거주·이름 테두리·오프닝9 PASS.

[크레딧 CPU](../qa/reports/credits11_211_CPU.json): A448 직접첫756NT셀·NMI/렌더 중지중2006/2007쓰기·2000 복원, 진행2E169/2F158호출에서 원래 carry/58대기/종료·전NT픽셀 exact. 최대이벤트 큐20/62바이트, 관측stack최저248·충돌없음. 원래A492의4000frame 수동동기CPU스케줄(6DF/FC/FF/6CF/58)이059와일치한다. 프레임루프는 CPU 입력값을 제공한 검증이며 에뮬레이터를 실행하지 않았다.

원래FF17은2000만복원하고2001은출력을중지한상태로다음nativeNMI를기다린다. 초기전체A430 하드웨어·다음NMI·실제PPU aliasing/스크롤/전송예산/폰트수명·상단창소거·CHR256 실제매핑·최종가독성은미수행이다.062는실제검수전·미채택개발후보다. 이전055오프닝실제근거를062전체성공으로옮기지않는다.060/061 CPU거부본과이전051/055/057/059·원본/CSV/1편·사용자Mesen/세이브를보존했다. 카페완성작업기·외부게시없음. 변경·해시는 [211매니페스트](../manifests/nonplay211_assets.json).

재현: `python scripts/build_credits11_211.py --output build/text11_211_repro_next`. 검사기는고정보고를덮어쓰지않으므로 새보고/빌드경로를쓴복제에서수행한다. 패키지작업에서실Windows 적용을추가한다.

다음 작업 하나: 062 ROM없는 적용패키지를 만들고 Windows8사례·최종ZIP 적용을 검증한다.
