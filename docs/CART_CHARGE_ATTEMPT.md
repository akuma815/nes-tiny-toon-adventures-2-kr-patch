# 작업65 — 카트 A 충전·해제 관찰

[실행·검증 보고](../qa/reports/cart_charge065_validation.json), [실행기](../scripts/run_cart_charge_qa.py), [고정 정책](../scripts/trace_cart_pursuit_v2.lua), [검증기](../scripts/verify_cart_charge065.py). ROM과 번역 SSOT는 변경하지 않았다.

같은043의 새 부팅에서18,000프레임을 실행했다. 실제좌표로 다른카트를 추적하되 B는 끄고 A를40프레임 누른 뒤24프레임 놓았다.120프레임마다 가까운 카트를 다시 선택했다. RAM·ROM·PC·체력·금액·phase·savestate·reset 개입은 없다.

17,999 입력행 중9,303행이 카트 플레이 정책이고7,882행에서 속도가0이 아니었다. 충전은 최대1,024(8.8값4)에 도달했다.3492프레임 A+아래+오른쪽 입력에서 충전1,024였고,3496에서 A를 놓은 뒤3497 충전0·Y속도717이 관측됐다. 정적A294/A088/A0D1 소비기와 충전·해제·가속의 연결을 강화한다. 전체 물리나 B의 공식 행동 이름을 확정한 결과는 아니다.

체력은4920에서2,5550에서1,12360에서0으로 감소했다. 마지막에는 root08/phase13이며 history·금티켓0이다. 자연클리어와 보너스는 없다. 구멍 위치와 관성 제어를 고려하지 않은 추적 정책의 실패로 기록하며 게임·한글화 결함으로 단정하지 않는다.12000 실제화면을 직접 확인했다.762PNG·4,582고정 runtime파일과6,096개1KiB CHR조각을043과 검증했다. 전체 화면 육안 검토가 아니다.

재현: `python scripts/run_cart_charge_qa.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/<새ID> --frames 18000 --inputs config/menu_cart_001.json`. 전용 디렉터리와 Lua/환경 SHA를 고정하며 기존 결과를 덮어쓰지 않는다.

분석 중 일회성 JSON 요약에서 tuple키 직렬화 오류가 있었고 문자열로 고쳤다. 일회성 disassembler 생성에서 Memory를 직접 넘긴 오류도 MPU(memory=...)로 고쳤다. QA 실행/ROM 변경과는 관계가 없다. A05E의RTS 뒤는 방향별 데이터표이므로 명령으로 판독하지 않는다.

sourceSHA f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,043SHA087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a,SSOT26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27. 정적·runtime/매핑·직접1장 검증을 구분한다. 새 빌드/패치적용·PCM/청음·실기·자연완주·최종사람검토는 하지 않았다. 원본·1편·기존자료·검토 패키지를 보존했고 외부 게시하지 않았다.

다음 작업 하나: **카트 충돌·구멍·남은 적 판정의 실제 소비기를 추적한다.**
