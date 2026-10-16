# 작업111 — 성 방6의 native NT14/16 실제 소비

원본·현재047·CSV를 변경하지 않고 성 방 전환 진단을 완료했다. 원본 SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047 SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지. [선행 정적 조사](CASTLE_BACKGROUND_STAGE_ANALYSIS.md), [검증 보고](../qa/reports/castle111_validation.json).

## 실제 관측과 개입

원본과047을 각각4800프레임 실행했다. 각 실행은1000프레임에 gold4를 주입하고 기존 버튼 경로로 성에 입장한 뒤4000프레임의 root4/course4/phase5/방0에서 **A5=35, phase54=7** 두 RAM 값을 썼다. 기록은 각 `castle111_injection.csv`에 before/after로 남는다. 자연 획득·방 이동·성 완주가 아니다. ROM/state-load 변경은 없다.

두 실행 모두4000프레임에서 F5F8→물리 bank30의969C→96ED가 방6을 만들었다. 4002프레임에는 fixed D347→D36E→8025/selector14→D373→8025/selector16, bodyfont118로 이어졌다. source PRGrelative0169C/1D347/04025와 current2169C/3D347/24025를 별도로 guard해 같은 CPU 주소의 다른 bank를 잘못 기록하지 않았다. 4005프레임에는 두 원본 NT의2048셀 전체가 PPU 전개 결과와 일치했다. 이후 NT16 일부는 정상 native HUD가 덮어쓰므로 압축 원천과 계속 전체 일치할 것으로 가정하지 않았다.

직접 확인한 [현재047 4092](../qa/dialogue/castle111_current047/frame_04092.png), [현재047 4200](../qa/dialogue/castle111_current047/frame_04200.png)은 성 보스의 기체와 배경을 표시한다. 이 두 장면에서 NT14/16의 추가 번역 문구는 관찰하지 않았다. 글자처럼 보이는 임의 font124 코드 후보를 번역 대상으로 확정하지 않는다. 최종 사람 그림/문구 검토는 별개다.

## 원본과047의 비교

선택한 실제 패턴 읽기 두 프레임에는 CHR118/119가 각각838행,3920회 읽혔고 원본/047의 물리 타일별 읽기 집계가 같다. 해당2KiB ROM 원천도 같다. 각107캡처의 mapped CHR856개 조각이 사용 ROM과 일치했다. 현재047의 개입 전 파일2742개는 동결된 작업94 현재047 기록과 같다.

4005 이후107개의 같은 프레임 비교에서 전체 NT2000..2FFF는 원본/047이 같다. 실제 RGB 차이의 합집합은 `(20,190)..(236,217)`의 기존 HUD 영역이며 그 위0..189/아래218..239는107장 모두 같다. **전체 PNG가 같다고 주장하지 않는다.** HUD는 원본 nativefont124/125와 이미 한글화한206/207의 차이를 포함한다. 실제 NT/표시 검증이지 새 빌드나 새 패치 적용 검증은 아니다.

Mesen의 PNG는 이전 필터 프레임이라는 [작업107](RIDE_SUCCESS_CURRENT047.md)의 근거를 유지한다. 읽기 집계4091/4121과 screenshot4092/4122가 연결된다. 집계에 실제 읽기 값 자체는 보존하지 않았으므로 모든 fetch값의 byte exact 검증이라고 표현하지 않는다. 전역 IRQ/전환/효과까지 검사한 것이 아니다.

## 재현·검증·인계

[실행기](../scripts/run_castle111.py), [진단 Lua](../scripts/trace_castle111_v1.lua), [4800 입력](../config/castle111_inputs_4800.json), [초기 티켓 seed](../config/gate_gold4_seed_001.json), [검증기](../scripts/verify_castle111.py). 첫 실행은9000용 입력의5000..7500 이벤트를4800 한계와 함께 줘 guard에서 거절됐고, 에뮬레이터/출력 폴더를 만들기 전이었다. [preflight 실패 기록](../qa/reports/castle111_preflight_observation.json)을 보존하고4800 입력을 별도 생성했다.

```powershell
python scripts/run_castle111.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/castle111_current047 --frames 4800 --inputs config/castle111_inputs_4800.json --seed config/gate_gold4_seed_001.json
python scripts/run_castle111.py --rom "original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes" --output qa/dialogue/castle111_source --frames 4800 --inputs config/castle111_inputs_4800.json --seed config/gate_gold4_seed_001.json
python scripts/verify_castle111.py
```

기존 출력 폴더/보고서를 덮어쓰지 않는다. [원본 실행 환경](../qa/dialogue/castle111_source/environment.json), [현재047 실행 환경](../qa/dialogue/castle111_current047/environment.json)의 모든 선언 파일 SHA를 확인했다. 변경 파일은 두 실행 QA/실행기/Lua/검증기/입력/preflight/보고서/본문서와 오늘 인계·journal·canonical 문서다. [동결 manifest](../manifests/castle111_assets.json)에 SHA, source/1편/링크 감사는 `qa/reports/castle111_session.json`에 기록했다.

정적 원천 비교·에뮬레이터 진단·직접 두 장면 검토를 분리했다. 자연 방 진행/보스 클리어/전게임 완주, STAGE SELECT의 모든 진입과 source NT1C, HOWTO/PAUSE/POW 전역 소비, 사람 최종 검토, 실기·PCM청음·정식 배포는 남는다. release_eligible=false. 전체 완료 후 카페 작업기를 작성하며 현재는 근거 journal을 유지한다.

다음 작업 하나: **native8025의 원본 call site와 계산 selector 공급 범위를 조사해 남은 NT1C 소비를 추적한다.** LDX#1C motif 부재만으로 미사용이라고 정하지 않는다.
