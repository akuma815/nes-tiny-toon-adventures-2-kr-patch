# UI 공유 매크로의 글꼴 분리 — 작업19/20

채택 [빌드019](../build/dialogue_kr_poc_019/TinyToon2_dialogue_kr_poc.nes)/[IPS](../build/dialogue_kr_poc_019/TinyToon2_dialogue_kr_poc.ips). 새 한글 문구는 없으며10draft/44untranslated와 원래 SSOT는 그대로다. [검증](../qa/reports/macro019_validation.json), [실제 장면](../qa/dialogue/macro019_actual_scenes.png), [자산](../manifests/ui_macro_assets.json), [감사](../qa/reports/ui_macro_session_20261005.json).

macro83..88은 glyph 코드를 공유/반복하여 원문 그대로는 문단별 한글 배치에 제약이 있다.6매크로의42개 비영 glyph를 각기 다른01..2A로 분리했다.83의 첫00와 모든 FF·포인터·매크로 ID·확장 칸수는 유지한다.01/02를 포함한 버스터/몬타나 macro80..82는 건드리지 않는다. 등록 main00·0B..2C의33원천(35슬롯) literal glyph도 충돌하지 않도록 매핑하고, 공통 font148/149에서 해당 원래 일본어 bitmap을 그대로 복사한다. 아직 번역하지 않은 소비기의 일본어를 보존하는 기반이다. 원본 source raw와 추출54행은 변경하지 않았다.

폰트148/149는 기존 예약65010..65810의2KiB에만 쓴다. 헤더·PRG256/CHR152·ROM417808은017과 같고 예약2KiB가 남는다. font0 및 숫자 F9의41..4A, F8/FA의70..79, 구두점6B..6E는 그대로다. F9는0B를 직접 초기화하지 않아 변수 검증에0B=0/2F를 모두 포함했다. 등록된 숫자 입력0..9·ride25=0..5·source RAM07D0..2 조합192조건에서 glyph/각 호출 cycle/cursor 일치. 실제 관측한 숫자는0포인트/10일반티켓/카트1장 가격이며 그 외 수량은 정적 조건 검증이다.

원본 PRG의STA06CD/06CE는 정규9417 초기화에만 있었다. 등록 테이블48슬롯 전체 reader를 비교했고,33 일본어 원천의 원래 visible glyph bitmap/각 호출 시간·제어를 보존한다. 관측 밖 텍스트/다른 엔진의 전체 목록까지 확정한 것은 아니다.

018은 하단 C6 글꼴만 바꿔 카트 설명판108표본이 깨졌다. [실패 보고](../qa/reports/macro018_rejection.json)·후보·캡처는 보존하고 채택하지 않는다. 실제 FD77/FD92 trace에서 설명판 상단이 NMI RAM34=90을 사용함을 확인했다.019는 native9E28의LDA5A/STA34 생산값만148로 바꿔 상단에도 일본어 공통 글꼴을 적용한다. C7의 그림과 IRQ/NMI 코드·PPU상태 읽기는 그대로다.9FF7의별도 성 입구 글꼴은 수정하지 않았고 실제 방문 확인이 남는다. 앞으로 놀이기구 설명판을 한글화할 때에는 상단 title/규칙/가격의 글꼴을 하단 문단 글꼴과 별도로 설계해야 한다.

검증 분류:

- 정적: immutable 원본 및017 전체 이미지의 허용 데이터/폰트/lookup/9E28 즉시값 변경만 독립 일치. ExpectedWrites7영역 비중첩. 타이틀003·도입9문단·홈 초안·기존 글꼴은 유지.
- CPU/build/apply: 문단 ABI1408조건, 빌더 seed672조건, 전체 reader48슬롯/일본어33원천/변수192조건. 재빌드 및 실제 한글·공백 경로 IPS 적용 결과 동일.
- 런타임: 홈·카트390/매표소289, 합679전체화면 픽셀 차이0. 숫자 범위·OAM·팔레트·문단 ID/포인터·C7·속성테이블을 보존. 변경nametable 문자도 원래/새 glyph bitmap이 같음. 실제 C6=148은541표본 관측. IRQ/NMI/PPU/mapper의74319행 시점은017과 정확히 동일하고A000/A008의5A/5B→94/95 값만 바뀜.
- 직접 화면:019 홈1170, 매표소1620/1740, 카트2310 확인. 아래 일본어와 위 설명판을 동시에 보존했다. 미방문 장면은 CPU/정적 검증이며 전체 플레이가 아니다.

ROM `1243fcf1450c1a46df55edd63d6528565cb49204b5f53d24dd731183dbcb7c5d`  
IPS `773046edd8320f14e9148efdd070bd3c54f3df842b560d8661ce1c43431bfb89`  
CSV `76bcc0d985c41dff6ce19cf0dd1a8a02e58bbb6814ca0b2f26e9e8239b9e8c48`

재현: `python scripts/build_ui_macro_passthrough.py --output build/dialogue_kr_poc_019_NEW`, `python scripts/verify_ui_macro_hooks.py --build build/dialogue_kr_poc_019 --report qa/reports/macro019_hooks_NEW.json`, `python scripts/verify_ui_macro_passthrough.py`, `python scripts/audit_ui_macro_session.py`. UTF8 및새 폴더를 사용하고 과거 검증을 변경된 SSOT로 재실행하지 않는다. 실제환경/입력/스크립트는 environment.json에 동결했다.

다음 행동 하나: 실제 확인한 홈 선택명4개와 매표소 출발/환영/교환/부족 문구4개를SSOT draft로 추가하고 문단별 font150..165로 삽입한다. 무중단 지시에 따라 바로 이어간다. 놀이기구 설명판·미방문 분기·영문 그림/크레딧·전체수집·전체플레이·오디오/reset/savestate/실기·최종 사람 검토와 기존PRG/RNG 한계는 남는다. 배포나 외부 게시 없음.
