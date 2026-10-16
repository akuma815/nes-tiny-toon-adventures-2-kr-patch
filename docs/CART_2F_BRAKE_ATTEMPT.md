# 작업87 — 2F 추격 중 자동 B 제거 실험

작업86의 실제 속도 근거에 따라 V4의2F intercept 구간에서만 자동 B 속도 제한을 제거한 V5 controller policy를 시험했다. pit_avoid B와 첫 구간 입력, 나머지 경로·충전·목표 선택·게임 ROM은 동일하다. [검증 보고서](../qa/reports/cart087_validation.json)의 PASS는 관측/무결성 검증이며 전체 클리어 성공을 뜻하지 않는다.

현재046의 새 부팅에서36000프레임을 실행했다. 첫 입력 차이는14317의C5→85로 B비트64만 달라졌고, 이전14316행/같은 시점3195개PNG·RAM·PPU·OAM·매핑 파일은 기존045와 byte exact다. 새2F intercept3987행에서 자동B가 꺼졌다. 첫 구간 클리어는 재현했지만 두번째 마지막2F가 남아 시간 초과로 홈에 돌아왔다. Gold/history0, 전체3구간 자연 클리어 미달이다. 감속 제거만으로 해결됐다고 보고하지 않는다.

정적/관측 검증: Lua diff를 정확한 한 조건과 주석 변경으로 한정했다. 새경로의 actual tilequery71180행/고유입력30786개를 native CPU 분류와 대조했고,1362PNG/10896개1KiB CHR 매핑과8190개 runtime 파일을 해시 검사했다. [실패 직전](../qa/dialogue/cart087_no2Fbrake046/frame_18990.png), [시간 초과 뒤](../qa/dialogue/cart087_no2Fbrake046/frame_19110.png), [홈](../qa/dialogue/cart087_no2Fbrake046/frame_24000.png)을 직접 확인했다.19110은 마지막 버퍼의native잔여 timer 표시일 수 있으므로 단독 화면 숫자로 phase 상태를 대신 판단하지 않는다.

새 ROM/번역/패치 적용 없음. 체력·시간·금액·RAM·PC·상태 로딩 개입 없이 controller만 사용했다. [V5 Lua](../scripts/trace_cart_rounds_v5.lua), [실행기](../scripts/run_cart_rounds_qa_v5.py), [환경](../qa/dialogue/cart087_no2Fbrake046/environment.json), [검증기](../scripts/verify_cart087.py), [동결 파일/SHA](../manifests/cart087_assets.json). 재현은 새 폴더로 `python scripts/run_cart_rounds_qa_v5.py --rom build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 36000 --inputs config/menu_cart_001.json`.

같은 실패 전략을 임의 반복하지 않는다. B 감속의 구체적인 공식 행동 이름, 밀기 충돌의 힘 전달, 전체 자연 완주·최종 사람 번역·전역 corpus·PCM 청음·실기는 남는다.

다음 작업 하나: 실제2F–플레이어 충돌에서native9D53..9D93 속도 교환과9DCD 이후 추가 밀기 분기가 어떻게 실행되는지 관측·CPU 재생으로 연결한다.
