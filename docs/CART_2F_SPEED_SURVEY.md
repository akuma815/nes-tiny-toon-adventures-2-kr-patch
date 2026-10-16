# 작업86 — 카트2F 적의 실제 속도 생산자

[검증 보고서](../qa/reports/cart_speed086_validation.json). 현재046을 기존V4와 같은 controller policy로10000프레임 실행해 첫 구간 클리어와 두번째 구간의2F 적을 관측했다. 게임 로직·ROM·CSV·체력·시간·금액·PC·저장 상태 개입은 없다. 원본3A/3B 이동 코드16KiB 보존과 같은 시점 기존045의PNG/RAM/PPU/OAM/매핑2475파일 byte exact를 확인했다.

2F native dispatch95E3의state inline table95F9는9603/9648/97A1/97CF이며, subphase table9658은9개 포인터다. CFC2 뒤의 inline 포인터와9791/9799 방향 테이블은 데이터로 취급했다. 선형 listing에서 데이터까지 명령으로 표시된 초기 탐색은 채택하지 않았으며 실제 exec 주소·루틴 경계·테이블 바이트를 검증했다.

실제2F 가속 생산자9767은 두 축에64/256만큼 감속을 적용한 뒤9791(Y)/9799(X)에서 방향별 속도 highbyte를 덮어쓰고 fractional lowbyte는 보존한다. 이후state2/subphase0/timer80으로 들어간다. D-clear 로컬CPU2592사례로 이 계산을 검증했고, 실제48회 생산자의 helper 입력·두 방향 테이블 읽기·9781의 결과가 정확히 일치했다.8방향 모두 실제 관측했다. 적이 항상 고정2.8속도로 이동한다는 가설은 기각한다. 관측한2F161표본 중44개는2.5보다 빨랐다.

기존045/20k 정책 로그에서는2F를 실제 target으로 선택한14276 이후4724행 중1592행에서 intercept B를 눌렀다. 그 조건은 플레이어 속도 제곱6.25 초과다. 현재046/10k의2F 생산자 관측과 과거20k의target/B 분석은 서로 다른 범위다. 적이2.5보다 빠를 수 있고 기존 자동 감속이 추격을 방해할 수 있다는 실험 근거가 생겼으나, 시간 초과의 단일 원인이라고 확정하지 않는다.

시행착오: [최초 검증기](../scripts/verify_cart_speed086.py)는10k 안에2F target 선택까지 있다고 가정해 B행 조건에서 중단했다. 실제target 선택은14276이므로, [v2](../scripts/verify_cart_speed086_v2.py)는 해시 확인한 과거20k의B정책과 새10k 생산자를 명시적으로 구분한다. 보고서/ROM/입력을 임의 수정하지 않았다.

전체 카트3구간 자연 완주·전역 corpus·청음·실기·최종 사람 검토는 아직 미수행. [runtime 환경](../qa/dialogue/cart086_speed046/environment.json), [Lua](../scripts/trace_cart_speed086.lua), [실행기](../scripts/run_cart_speed086_qa.py), [동결 파일/SHA](../manifests/cart086_assets.json). 재현은 새 폴더로 `python scripts/run_cart_speed086_qa.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 10000 --inputs config/menu_cart_001.json`.

다음 작업 하나: 기존policy의2F intercept에만 자동 B 속도 제한을 제거한 V5를 새 실행에서 시험한다. 첫 구간 입력과 pit_avoid B는 그대로 두고 자연 클리어/실패를 실제 lifecycle·phase·history로 판정한다.
