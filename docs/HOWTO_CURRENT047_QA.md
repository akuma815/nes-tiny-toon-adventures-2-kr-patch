# 작업100 — 현재047 HOWTO 뱅크의 실제 장식 소비

현재047 ROM/CSV/검토패치는 변경하지 않았다. 원본/1편/이전 증거를 보존했다. ROM SHA `82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10`, CSV SHA `ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556`. [99 정적 NT 근거](HOWTO_BANK_NT_BOUNDS.md), [검증기 v2](../scripts/verify_candidate100_v2.py), [결과](../qa/reports/candidate100_runtime.json).

private Mesen2.1.1에서047 같은 ROM/메뉴 입력을 baseline와probe 각각4200frames coldboot했다. 순차 실행/auto load 없음/컨트롤러만/메모리·ROM·상태 쓰기 없음. baseline은 기존trace_world_v1, probe는 [읽기전용 확장](../scripts/trace_candidate100_v1.lua)이다. 두 실행의1658개 공통 파일은 byte exact이며275개 전체PNG, RAM/PPU/OAM/전체state/mapping/native menu/world/NT 로그를 포함한다. 다른 파일은 관측 Lua 자체와 새 관측 로그/capture뿐이다. 각environment의 선언한 파일SHA, exe/config/input도 검사했다. 이는 관측 추가로 해당 경로의 실행이 바뀌지 않았다는 증거이며 모든 관측 방법의 일반적 무해성을 뜻하지 않는다.

실제RAM35 producer는1574 observedPC9E30/PRGrelative25E30에서 value74를 쓰며 nativeSTA35는9E2E다. 콜백 시 RAM에는 쓰기 전52가 보이는 것을 구분했다. nativeFD9E 이후1060표본은 RAM35=74, PPU0800→CHR1D000/0C00→1D400, backgroundPatternAddr0이다. upperNT2000..225F의 HOWTO tile90..96은0개였다. actual pattern read 관측1500..3099 중1578..2633의1056프레임에서 테두리tile81의16바이트를 각1회씩 읽었다. 총16896행의 주소/값/scanline32..39가 source CHR1D010..1D020과 같다. HOWTO label CHR1D100..1D170 읽기는0이었다. 장식 positive control이므로 뱅크 전체의 미사용 주장은 기각한다. 전체 game/모든분기 label부재나 최종 사람 보존승인은 아니다.

35 top PPU capture1590..2610의0800..1000이source116/117과 같고 highNT267셀은99 디코더와 같다. nativeNT2082 tile81/sourceROM3D020..3D030을 독립 planar decode해 실제 PNG의x16..24/y32..40과35번 RGB exact를 확인했다. 33표본은 native palette0F272017,1590은 fade-in0F0F0F0F,2610은 fade-out0F171007이다. 팔레트는 private Mesen preset 범위이며 물리 콘솔 색을 주장하지 않는다. 실제 [1800 화면](../qa/dialogue/candidate100_probe047/frame_01800.png)을 직접 보았다. top/읽기/화면표본의 event 경계가 달라1060과1056을 같은 수로 맞추지 않았다.

v1검증기는 모든표본이 steady palette라고 잘못 제한해 report 전중단했다. [실패 기록](../qa/reports/candidate100_v1_observation.json)/[v1](../scripts/verify_candidate100.py)을 보존하고 v2가 세 실제 palette와35 RGB를 검증했다. 게임 실행이나 자산을 바꿔 검사를 통과시키지 않았다.

재현(새 출력폴더 필요): `python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새이름 --frames 4200 --inputs config/menu_coaster_001.json --script scripts/trace_candidate100_v1.lua`. 기준은script를trace_world_v1.lua로 지정한다. 검증 명령 `python scripts/verify_candidate100_v2.py`는 기존 보고서를 거부한다. [동결 자산](../manifests/candidate100_assets.json).

정적/CPU는99의 범위다. 이번에는047 실제 실행/파일 비교/장식 source-RGB 검증을 추가했다. 새 빌드/적용은 없었다. PAUSE/POW 실제 소비·전역corpus·자연 전체완주·PCM청음/실기·최종 사람 번역/명칭/그림·공식배포·카페완성작업기는 미완료다.

다음 작업 하나: PAUSE120121의 나머지 softwareCHR shadow register 공급을 정적으로 추적하고 코드 상수와 데이터 motif를 구분한다. 같은 zero runtime을 반복하지 않는다.
