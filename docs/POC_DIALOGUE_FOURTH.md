# 넷째 도입 문단과 이름 매크로 — 013

2026-10-05 작업14의 개발 검증본은 [ROM](../build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes) / [IPS](../build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.ips)다. [실제 화면](../qa/dialogue/pages013_actual_4x.png), [반복·다음 일본어·홈 시각 근거](../qa/dialogue/pages013_visual_review.png), [검증](../qa/reports/dialogue_fourth013_validation.json), [자산 식별](../manifests/dialogue_fourth_assets.json), [현재 인계](HANDOFF.md)를 따른다. [셋째012](POC_DIALOGUE_THIRD.md)은 이전 검증 기준으로 보존했다.

MAIN_05665의 원문은 버스터 바니의 집에 편지 한 통이 도착해 있었다는 내레이션이다. 실제 일본어 화면의 バスター・バニー와 macro81의 バスター 전개를 확인했다. 초안은 **버스터 바니의 집에 / 편지 한 통이 도착했어**다. 이름은 원문의 한글 음역이며 최종 번역·명칭 검토는 남는다. 원문/raw/tokens/reference/포인터는 보존하고 이 행의 번역·상태·장면·화자·notes만 갱신했다. 현재54원천 중5draft/49untranslated이며 전체 게임 대사량은 아직 확정하지 않았다.

## 매크로와 글꼴 공간

원본 macro81은 MACRO_061C3의 `4D 67 40 43 66 FF`를 전개한다. 다른 대사에서도 사용하는 원본 매크로 테이블과 페이로드는 수정하지 않았다. 넷째 본문의 같은 위치에81을 유지하고, 넷째 전용 글꼴에서 전개되는 다섯 타일만 빈칸으로 만든 뒤 한글 이름을 inline으로 배치한다. 첫 줄은 원래00 두 칸과 매크로 다섯 칸을 합친7칸 여백,10칸 본문,5칸 뒤 여백이다. 둘째 줄은 FD04와 추가2칸을 합친6칸 여백,12칸 본문,2칸 뒤 여백이다. 첫22/둘째20전개칸과 native 나머지 빈칸을 보존했다. 이 방식은 이 문단만의 배치이며 전역 이름 매크로 한글화 완료를 뜻하지 않는다.

38바이트,81/FE/FD04/FF, literal00 네 개를 유지했다. 실제 native reader44호출/4263사이클과 호출별 사이클·커서·버퍼 커서는 원본과 같다. 조립된 PPU21E4..21FB와2224..223B의 타일이 전개 결과와 일치한다. 직접 시각 검토에서는 중앙 배치, 띄어쓰기,17한글의 획과 두 줄 출력을 확인했다.

Galmuri7 2.403의17글자를 기존512×1400 atlas와 TTF8px에서 픽셀 단위로 비교하고 NES2bpp 왕복을 검사했다. SIL OFL1.1 폰트의 기존 출처/라이선스는 보존했다. 기존136KiB CHR의 padding이 소진되어 iNES CHR 길이를144KiB로 늘렸다. 넷째 font136/137은 파일 `62010..62810`, 추가6KiB 예약 공간은 `62810..64010`이다. 모두16진/끝 제외이며 PRG256KiB는 유지한다. 전체 ROM은409616바이트다. 원본CHR와 첫째128/129·홈130/131·둘째132/133·셋째134/135, 타이틀003을 그대로 보존했다.

## 선택 코드와 글꼴 수명

helper bank2의 ASM003은 source pointer table을 먼저 읽고, 문단 슬롯의 동일한2배 인덱스로 helper 전용9700..97FF 글꼴 테이블을 읽는다.48슬롯의 완성pointer로 생성한 선택은95F9→80,9615→84,963D→86,9655→88,나머지→5A다. 글꼴 테이블은 canonical native bank18의 원문을 건드리지 않는다. 유효한48슬롯의 전체 초기화 시간이 채택008/012와 정확히 같도록 high96 경로와 나머지 경로를 패딩했다. helper는107바이트이고 table은256바이트다.1바이트 글꼴 값만 추가하면 이후 슬롯을 등록할 수 있으나 새로운 본문의 제어/버퍼/생명주기는 따로 검증해야 한다. 임의의 잘못된 문단번호 안전성은 입증하지 않았다.

기존 양쪽 bank의 동일한 bootstrap,2B/SP/mapper 복구,setup114 추가사이클,IRQ 본문342사이클과 PPU/CHR 쓰기 offset을 유지했다. CPU1168조건에는8종 C6 초기값00/01/5A/80/84/86/88/FF의384조건이 포함된다. register/flags/RAM/stack/mapper와 선택·시간을 검사했고, 알려진 고장004 control은 거부됐다. py65 1.2.0의 공식6502 151opcode/mode·604벡터 roundtrip도 통과했다. CPU model은 실제 PPU와 비동기 인터럽트를 대신하지 않는다.

자연 진행 snapshot1630에서 pointer9655/font88을 선택한다. FF 처리 뒤 ID는5지만 pointer/font를 유지해 마지막 글자와 대기 상태가 깨지지 않는다. 첫 행은1815,둘째 행은1817에 지워지고1821까지font88을 유지한다. 다음 native 초기화 callback1821 뒤 snapshot1822에서는 pointer967B/font5A로 복귀하며 PPU의 원본90/91 글꼴과 일치한다. snapshot4500에서 자연 반복의 넷째 문단도 같은 두 줄을 출력한다. Start1740과1530 경로는1800에ID0/C6=0으로 건너뛰고 이후 도입으로 재진입한다. callback의 frame과 endFrame snapshot은 한 프레임 차이가 날 수 있다.

## 검증과 재현

immutable source에서6개의 비중첩 Expected Write를 적용해 전체 ROM을 재구성했다. 독립 verifier는012 전체 이미지에서 helper/양쪽 bootstrap/넷째38바이트/CHR 길이와 새 font·padding만 바꿔013 전체와 비교한다. 기존 Expected Write의 owner 이름은 이전 소유 범위에서 계승했으며 CHR의 실제 최종 크기는 header12와 build_report의144KiB를 따른다. 전체 원본 diff273347바이트의 대부분은 기존PRG 확장과CHR 이동이다.

깨끗한 재빌드와 한글/공백 경로의 실제 IPS 적용이 같은 SHA를 재현했다. IPS는 **깨끗한 일본어 원본에** 적용한다. Mesen2.1.1의 격리 coldboot,동일 Lua/config/controller 입력으로012와013을 비교했다. 자연5400프레임797표본,Start720/1740/1530 각3000프레임417표본,총2048표본이다. 넷째 두 행 밖 차이0,홈417전체일치,palette/OAM/문단ID/포인터 동일,실제font531표본 일치다. 수명 trace의19회 초기화 복귀에서SP/mapper/2B가 같고,1620..1850 IRQ 진입·쓰기9339시점이 동일하다. 값이 바뀐384건은 넷째font5A/5B→88/89 선택뿐이다.

처음 작성한 지우기 검사에서 두 줄이1815에 함께 지워질 것으로 가정했으나 실제 native 엔진은1815/1817에 순차로 지운다. ROM을 바꾸지 않고 검사 조건을 관측된 소비기 동작에 맞췄으며 문단 밖 픽셀 허용 범위는 확대하지 않았다. 직접 시각 검토는1790과4500의 한글,1920의 다음 일본어,홈1080을 별도로 수행했다.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_source.ps1
python scripts/build_dialogue_fourth.py --output build/dialogue_kr_poc_013_NEW
python scripts/verify_dialogue_fourth_hooks.py --build build/dialogue_kr_poc_013
python scripts/verify_dialogue_fourth.py
python scripts/audit_dialogue_fourth_session.py
```

빌드와 QA 출력 폴더는 매번 새로운 이름을 사용한다. 정상 캡처 재현은 다음과 같고 Start 경로는 `--frames 3000 --start 720`,1740,1530을 각각 지정한다. baseline에는012 ROM을 사용하며 같은 설정과 스크립트로 실행한다. Mesen 실행은 설정 파일 공유 때문에 순차 수행한다.

```powershell
python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/pages013_NEW --frames 5400 --script scripts/capture_dialogue_fourth.lua
python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/pages013_IRQ_NEW --frames 1860 --script scripts/trace_dialogue_fourth_irq.lua
python scripts/run_dialogue_qa.py --rom build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/pages013_LIFETIME_NEW --frames 5400 --script scripts/trace_dialogue_pages.lua
python scripts/dialogue_ips.py create --source "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --target build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes --patch build/dialogue_kr_poc_013_NEW/TinyToon2_dialogue_kr_poc.ips --scope "Development fourth page; five drafts"
python scripts/dialogue_ips.py apply --source "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --patch build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.ips --output "qa/dialogue/한글 패치 적용 013_NEW/TinyToon2_fourth013_applied.nes"
```

과거003/008/012 검증 스크립트와 manifest는 당시 입력의 기록이다. 현재5draft SSOT로 과거 검사를 재실행하지 않는다. 원본·1편 자료·기존 build/QA를 보존했다. 현재도 개발본이며49원천,전체 인벤토리,놀이기구 분기/엔딩,전게임 RNG22 영향,오디오,reset/savestate/실기,최종 문구와 타이틀 디자인 검토는 남는다. dist는 비어 있고 외부 게시를 수행하지 않았다. 최종 카페 작업기는 전체 작업 완료 후 작성한다.

**다음 작업 하나: MAIN_0568B의 네 줄 편지 본문과 이름 매크로81의 전개·버퍼·글꼴 수명을 확인하고 한글로 삽입한다.**
