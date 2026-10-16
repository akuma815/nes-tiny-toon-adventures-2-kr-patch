# 크레딧 한글화 — 작업37 / 037 채택

실제 소비를 확인한 세 크레딧 원천을 한글 초안으로 삽입했다. 게임명과 제작 역할을 번역하고 개발자 이름, KONAMI, ALL RIGHTS RESERVED.는 원래 바이트와 글꼴을 유지했다. 등록54원천 중45draft/9기술·공유원천이다. 전체게임 완료율을 뜻하지 않는다.

원래124/125 글꼴을 복제한201/202에 한글25자를 추가했다. A457의 NMI 글꼴 생산자 두 뷰(6468/26468)를7C→C9로 바꿨다. CHR208KiB/ROM475152, PRG256KiB이며 다른 모든 기존 글꼴과 코드·매크로·제어·문단 크기는 보존했다. FD32/FD20/FD3, literal00 위치, 이름/법적 표시 행과 원래 ASCII 비트맵을 독립 검증했다. 남은 예약공간12KiB.

[ROM](../build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes) SHA256 `401626540d7995a0e5c672f5aec1dec1737a60bce631f8c89e68b742631bb752`.
[IPS](../build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.ips) SHA256 `2b34f0c608097265ddf69d87038f8f78565bc279b0d21391ed562b34c3eea15c`.
CSV `26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27`.
원본 `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`.

정적·CPU: ExpectedWrites8 원본 전체 재구성/직전036 허용 변경만 PASS. reader 호출97/169/158의 매호출 cycle·cursor 및 올바른little-endian925E 즉시출력3case 동일. ABI1504/초기 글꼴720 PASS. 최초 ExpectedWrites gate가 저주소6468의 소유 누락을 잡아 출력 전에 수정했다. 원본기대7C와 비중첩 범위를 추가했으며 실패 ROM은 생성되지 않았다.

빌드·적용: 별도037_rebuild가 같은 ROM이며 한글·공백 경로의 실제 IPS CLI 적용 출력도 같다. [검증](../qa/reports/credits037_validation.json), [ABI](../qa/reports/credits037_hooks1504.json).

에뮬레이터: 같은 네 주소 seed(root18=7/19=1/07DF1/06DE0)로036/037을 각9000frame 실행했다. 자연 엔딩 진입이나 완주 증명이 아니다.327쌍 중267은 번역된 스크롤 셀만 변화,60은 전체 화면 동일. 번역 셀 밖 변화0, 다른 PPU/OAM·scroll·배우·게임상태 동일. 이름·권리표시69530셀 샘플 픽셀 동일, 실제99724시점 동일하며 CHR 선택값15996쓰기만7C/7D→C9/CA. 마스크는 실제 NT셀과 직전1/2frame의 FF17/FF20 NMI scroll에 한정했다. 전체화면 마스크/타이밍 오차는 허용하지 않았다.

새 회귀 실행: 인트로6000frame848화면, 코스터4200frame302화면의 전체 PNG/RAM/PPU/OAM/mapping 동일. 두 IRQ137255행은 값까지 같다. [회귀 보고](../qa/reports/credits037_regression.json). 크레딧+회귀1477화면/236979시점.

직접 시각 검토: [1500 게임명·제작진](../qa/dialogue/credits037_01500_actual.png), [2100 프로그램·그래픽·사운드와 이름](../qa/dialogue/credits037_02100_actual.png), [3000 패키지 그림·팀](../qa/dialogue/credits037_03000_actual.png), [3900 제공·KONAMI·권리문구](../qa/dialogue/credits037_03900_actual.png). 실제 캡처 정수4배이며 설명용 합성이 아니다. [위치/해시](../qa/dialogue/credits037_actual_pages.json).

변경파일: prepare_credits.py/compile_credits.py/build_credits.py/verify_credits_hooks.py/verify_credits.py/verify_credits_regression.py, backup CSV·credits_plan_001.json·SSOT3행,037/재빌드/IPS/실제적용, 여섯 새 QA 환경·검증/actual, 본문·인계·계획·journal. [자산 해시](../manifests/credits_assets.json), [보존/링크 감사](../qa/reports/credits_session_20261005.json).

```powershell
python scripts/build_credits.py --output build/dialogue_kr_poc_037_repro_next
python scripts/verify_credits_hooks.py
python scripts/verify_credits.py
python scripts/verify_credits_regression.py
python scripts/run_credits_seed_qa_v3.py --rom build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/credits037_repro_next --frames 9000 --inputs config/menu_credits_001.json --seed config/credits_selector_seed_002.json
```

원본/1편/전체 실패·성공 이력 보존. dist빈상태/외부 게시 없음. 전체corpus/영문 그림/전체플레이/오디오/reset/savestate/실기/최종 사람 검토와 기존PRG/RNG 한계는 남는다. 다음 행동 하나: 공유 매크로·숫자 기술원천의 실제 사용 관계를 정리하고 남은 영문 그림의 실제 CHR/NT 소비를 조사한다. 바로 이어간다.
