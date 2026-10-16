# 작업88 — 2F–플레이어 충돌 소비 연결

[검증 보고서](../qa/reports/cart_collision088_validation.json). 현재046을 V5 입력 그대로20000프레임 실행하고14000..19000 구간에서 실제2F/플레이어 쌍의native CPU 충돌 분기를 관측했다. 새controller 정책, ROM/CSV 수정, 체력·시간·금액·상태·PC 개입 없음.

실제 pair 검사4468회 중4262회는 거리 조건에서 거절됐다.206회는9D53..9D93에 진입해 두 카트의 X/Y8.8속도를 서로 교환했다. 충돌 전후 전체RAM2KiB를 덤프했고 해당native 구간을D-clear CPU로 재생한 결과206쌍 모두 전체RAM과 결과A가 일치했다. 같은 시점의 좌표차도 두 축 모두24픽셀 미만이었다. 방향 없는 ‘밀기 버튼’으로 해석하지 않는다.

이어9DCD의작은속도 추가분기는8회 실행됐다. 실제 명령주소·PRG뱅크·분기 전후RAM을 보존했다. 플레이어에게서 적으로 전달된 실제속도의 pit128,256 방향 내적은92회 양수/105회 음수/9회0이다. 즉105회는 구멍 반대쪽으로 힘을 전달했다. A가눌린 채의충돌은162회, 충전값이 남은충돌은150회, incoming 두축속도가 모두0인 충돌은9회였다. 전부0속도라는 초기 가설은 기각한다. 실제 native 방향벡터와 접근각·A 해제 시점이 추가조사 대상이며, 단일 실패 원인으로 확정하지 않는다.

기존 작업87 V5와 같은controller19999행 및PNG/RAM/PPU/OAM/매핑4140파일은 byte exact다. 새runtime 동결파일5819개를 해시 검사했다. 이번에는 새로운 화면 직접 육안 검사 없이 실제 RAM/CPU 관측을 검증했으며, 작업87의 실패 장면 시각근거를 계승한다. 전체클리어·새 한글빌드·패치 적용·PCM/청음·실기·최종사람검토는 주장하지 않는다.

정정: 작업87 동결 본문의 ‘8190 runtime파일’은8184개가 맞다.8190은 manifest에 선언한runtime8184와별도6파일의 합이다. 원 보고서/manifest/본문은 동결 보존하고 이 문서와88보고서에 정정한다.

[Lua](../scripts/trace_cart_collision088.lua), [실행기](../scripts/run_cart_collision088_qa.py), [환경](../qa/dialogue/cart088_collision046/environment.json), [검증기](../scripts/verify_cart_collision088.py), [동결 파일/SHA](../manifests/cart088_assets.json). 새폴더로 `python scripts/run_cart_collision088_qa.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 20000 --inputs config/menu_cart_001.json`.

다음 작업 하나: 2F 밀기 접근각을 좁히고 native 방향벡터가 구멍 쪽을 향할 때 A충전을 해제하는V6 controller를 시험한다. 첫구간·pit회피·게임 로직은 유지하고 성공/실패를 실제phase/history로 판정한다.
