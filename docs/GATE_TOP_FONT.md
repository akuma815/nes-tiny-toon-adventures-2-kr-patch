# 성 입구 일본어 보존 교정 — 023 / 작업25

작업24에서 새로 방문한 성 화면의 일본어가 깨지는 문제를 교정했다. native9FF7의 상단font90을148로바꾸며 낮은PRG와canonical미러의2바이트만변경한다. 문구/폰트/공통초기화/IRQ/NMI코드는그대로다. 한글범위는18draft36미번역으로불변이다.

실제1920프레임은 FD77의NMI font쓰기만있고 FB0D IRQ나하단font전환이없다. 성초기화9FEF에서RAM40을0으로두므로대사두행y168..191이모두RAM34의상단font를쓴다. 작업24의첫줄/둘째줄 분할추정은이실측으로정정한다. 작업24자료와추정기록은그대로보존한다. 이후성한글문구는06F3만바꾸면표시되지않으며상단34도공급해야한다.

또한022의9CF3는매표소전용이아니라성의문구전환에서도사용하는공통선초기화다. 성에서도원래지우기종료후초기화는남아있고022는선호출만제거한다. 017의6개전환은1800/2100/2400/2700/3000/3300에서pointer를먼저설정하지만022/023은이전pointer를지우기동안유지해7프레임뒤 nativeA050호출로설정한다. 실제화면은정상이다. 작업23CPU함수의 points/tickets변수이름도주소와반대로붙어있었다. 검사자체는07D0..2/07F2에명시한합성값을쓰기때문에그사실을새보고서에기록한다.10/99단일자리값은스트레스조건이며정상BCD플레이증거가아니다.

## 검증

[독립검증](../qa/reports/gate023_validation.json): 원본ExpectedWrites전체/중첩0,022대비2바이트외전체불변,CHR/SSOT불변,CPU모든초기flags256조건/추가시간0. 공통선초기화324조건으로성·매표소의슬롯/분기/flags/SP/mapper/게임RAM과209사이클절감을다시확인했다. 이전1504 ABI대상 helper/도입/IRQ바이트는022와동일하며이번256+324는새로실행했다.

재빌드와깨끗한원본에서한글·공백경로IPS실제적용의SHA가같다. runtime1105표본: 성474중79는이미한글화된홈문구행만변경/395전체화면같음,성상단font148이활성인221표본은native017과전체픽셀같음. 기차329·급류302는022와전체픽셀/PPU/게임RAM같음. gate023대022는34와NMI캐시3A만font값90→148로변경,모든다른RAM/네임테이블/팔레트/OAM/티켓·포인트/인덱스같음. 시점69714건정확히같고NMIfont선택3594값만변경했다. 성clear중pointer차이는정상source준거와좁은phase/frame조건으로검증했다.

직접[023 골드4장 화면4배](../qa/dialogue/gate023_castle_1920_4x.png)를확인했다. [실패022비교](../qa/dialogue/consumers022_gate_failure.png)와[작업24맥락](UI_RIDE_GATE_SURVEY.md)을보존한다. 최종번역검토·전체플레이·골드/일반충족·포인트교환성공·오디오/reset/savestate/실기검증은없다. dist비어있고외부게시없음.

## 식별·재현

- 원본: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- 023 ROM/재빌드/실제적용: `1f4341ef464146e25982e8bf25d01ff504be85a184b905240a69179d3c79e410`
- 023 IPS: `6f5f208a1c5b7e98e4e84b290f50f31f0707155191b7f42421237887f7a7e006`
- 현재CSV: `1528501efb8983ff77b9514fd859a7a7cca91eb23eb5ca752132cd645c3fbcd6`

[자산/해시](../manifests/gate_top_font_assets.json),[세션감사](../qa/reports/gate_top_font_session_20261005.json).

```powershell
python scripts/build_gate_top_font.py --output build/gate023_repro_next
python scripts/verify_gate_top_font.py
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_023/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/gate023_castle_repro_next --frames 4500 --inputs config/menu_castle_001.json --script scripts/trace_ui_consumers_v3.lua
python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_023/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/gate023_castle_irq_repro_next --frames 4500 --inputs config/menu_castle_001.json --script scripts/trace_ui_irq_v2.lua
```

현재verifier는고정023/18draft를검증한다. 후속SSOT변경후과거검사를그대로재실행하지않는다. v3숫자열은작업24정정과rawRAM/native주소를참조한다. 수정v4를별도저장했다.

다음 행동 하나: 실제소비가확인된 홈 기차/급류 선택2문구를font166..169로한글삽입하고이경로와성복귀를검증한다. 즉시이어간다.
