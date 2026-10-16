# 작업120 — CHR61의 강 후반 공급과 별도 스프라이트

[최초 분석기](../scripts/analyze_river120.py), [v1 실패](../qa/reports/river120_v1_observation.json), [v2](../scripts/analyze_river120_v2.py), [결과](../qa/reports/river120_bank61_v2.json), [추가 코드·시각 확인](../work/river120/visual_and_guard_check.json), [POW 후보 조사96](POW_METASPRITE_SUPPLY.md).

## 공급 문맥

sourcefile1260D의LDA3D/STA38은 nativebank38의A5FD다. fixedECFC는course25별로bank/inline주소를선택한다.5개source/047 CPU조건쌍으로course3→bank38/A645를확인했다. 따라서이공급은강놀이기구의handler이며기차나공통POW전용초기화로확정하면틀린다.

A645의A665가A5C6을호출한다.0422=0,69=0B,6D>=F0일때CHR38=61과actor2selectorED,좌표·상태를설정하고B6CC로간다.0422=2이면ED를갱신하고B6CC로가지만bank61을다시설정하지않는다. 나머지상태는돌아간다. 이필드의자연게임시점/의미를현재CPU조건만으로확정하지않는다.

state0/1/2/3×69전256값×6D의00/EF/F0/FF 총4096조건쌍에서원본과047의전체RAM/레지스터/stack/cycles가같고예상쓰기범위와일치했다. 새초기화2건,state2갱신1024건,반환3070건이다. CPU는B6CC진입에서멈추며그뒤기하계산이나실PPU까지실행한검증이아니다.

## 별도 stage 스프라이트

bank36의9643조립기는ED/EE/EF에서course3의B8C8표를사용한다. 3개source/current조건쌍의OAM·RAM·cycles가같으며독립descriptor해석과도같다.ED는9개,EE는2개,EF는1개8×16스프라이트다. 공통18/19같은POW후보와다른표·namespace다.조립기코드와BD5F..BD92 descriptor도source/current정확히같다.

[원본 정적 조립 그림](../work/river120/stage_ED_EE_EF_static.png)을직접확인했다.ED는세로축·가로막대·타원형부품의조합이며EE/EF는분리부품이다. physicalCHR61을PPU1800에가정한설명팔레트·인위좌표그림이다. 실제게임이미지나물체의게임명/문구번역결정이아니다. 원본같은뱅크지정이곧POW표시라는추론을하지않는다.

## 인계

원본SHA `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`, 현재047SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556` 유지.원본/1편/기존ROM·CSV·성공실패QA를보존했다.이번은정적·제한된CPU·정적그림직접확인이다.새빌드/적용·에뮬레이터·실게임장면은없다.전역corpus/자연전체완주/사람검토/실기·청음·정식배포는미완료며카페완성작업기는전체완료후다.

v1이합성메모리의ROM영역까지전체동일을요구해기존게임오버폰트·문구의변경20바이트에서실패했다.OAM과RAM은같았다.기존변경을되돌리지않고v2에서RAM범위를비교하고대상코드/표를별도guard했다.실패스크립트/관찰을보존했고PNG/보고서출력전중단이다.

변경파일은분석기2개/실패기록/v2결과/정적PNG/추가guard·시각기록/본문서/인계·journal·canonical/manifest다.재현`python scripts/analyze_river120_v2.py`는최초출력용이며이미동결된출력은거부한다.재검증은새출력경로를사용하는복제본으로한다. [동결자산](../manifests/river120_assets.json), 감사 경로 `qa/reports/river120_session.json`.

다음 작업 하나: 현재047과원본의강phase5에서nativeA5C6직전RAM69=0B/6D=F0만명시적으로주입하는진단으로ED/EE/EF의실제OAM·CHR61읽기·화면을연결한다. 자연후반진행·완주와구분한다.
