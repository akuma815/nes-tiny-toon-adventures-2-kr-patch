# 작업194 — 요청6문단 배치055 실제표시·반복·소거 검증

사용자지정6문단배치를 **055실제Mesen**에서확인했다. [요청수정전053/후055 실제비교HTML](../workspace/review/opening11_194/review.html), [6문단055 PNG](../workspace/review/opening11_194/page06_11px.png), [최종검증](../qa/reports/opening11_194_validation.json), [빌드/CPU193](OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md). ROM SHA `8346499ca4240ffad350e3977f792735563779b8c749744a8d9b413ea0b44086`.

수정전/후6문단은같은frame02199의실제PNG다. 그밖의8px/11px전체9문단비교는각문단의완성시점캡처이므로동일프레임비교가아니다. 새055의1행‘친구들도데려와!’,2행‘깜짝놀랄거다!’,3행빈줄,4행오른쪽서명‘의문의대부호로부터’를직접열어확인했다. 셀정렬우측끝192px/서명시작72px,문구보존·원하는줄묶음과분리 PASS. 사람의최종미감/전체폰트승인으로간주하지않는다.

에뮬레이터: 동일181고정호스트·같은v3읽기전용관측기/설정으로055콜드부트9000프레임을새실행했다. 컨트롤러입력은빈목록,세이브/RAM/PC/생명수/ROM주입없음. 9문단각3회·1575출력호출/3024상하PPUNT다음vblank(scanline248/249)·최대큐10바이트/30회9행초기화지우기 PASS. NT로그N−1/화면N−2및이전팔레트/CHR매핑의고정소비시점으로2167출력도중·대기·소거RGB,29,956,608픽셀exact PASS.

기존053과같은관측프레임2318쌍을비교했다. 2086전체PNG동일,232는정확한6문단font140소비시점의text field32..224/y116..188안에서만변경되며그밖의전체픽셀은동일하다. 다른8문단과창외화면동일을확인했다. 넓은예외영역이나프레임별임의허용량을추가하지않았다. 이는9000프레임의해당오프닝경로로한정한다.

정적/빌드/CPU는193의immutable원본/IPS/독립재빌드/최종6502 PASS에연결한다. Start/기차분기는055에서새실행하지않았고053의187기록은역사자료로보존하며055실행으로재명명하지않았다. 054홈후보도새실행없다. 사용자실제플레이검수담당을유지하며전체11px/오디오·하드웨어/강제저장호환/전역privatePRG8도달성/최종폰트미감미완료다.

변경파일/해시: [194매니페스트](../manifests/nonplay194_assets.json), runtime환경JSON의모든캡처/로그SHA. 원본/051/053/054/CSV/1편/사용자Mesen·세이브보존. 원문유지6건/타이틀/다른그림변경없음. 카페완성작업기/게시없음. HTML브라우저렌더검증은미실시.

재현: `python scripts/run_opening11_186.py --rom build/opening11_poc_055/TinyToon2_Opening11_PoC055.nes --output qa/dialogue/<new-directory> --frames 9000 --inputs config/intro_no_inputs144.json --script scripts/trace_opening11_187_v3.lua`. 검사기는기존194보고를덮어쓰지않는다. 새대상/출력경로를정한복제에서검사한다.

다음 작업 하나: 055문단6조정판의ROM없는패키지를만들고Windows적용·최종ZIP실적용을검증한다.
