# 홈 대사와 문단별 글꼴 공급 — 개발본003

이 문서는 작업10의 [003 ROM](../build/dialogue_kr_poc_003/TinyToon2_dialogue_kr_poc.nes)과 [IPS](../build/dialogue_kr_poc_003/TinyToon2_dialogue_kr_poc.ips)에 대한 기록이다. 당시 타이틀003·첫 도입 문단002에 홈 대사 `MAIN_05741`의 초안 **자, 어디로 갈까?**를 추가했다. IPS는 깨끗한 일본어 원본에 적용한다. 현재 통합본과 둘째 문단/동적 글꼴 구현은 [008 문서](POC_DIALOGUE_PAGES.md)를 따른다.

[실제 홈 화면4배](../qa/dialogue/home003_actual_4x.png), [출력 중/완성/대기 비교](../qa/dialogue/home003_comparison.png), [전체 검증](../qa/reports/dialogue_home003_validation.json), [입출력 해시](../manifests/dialogue_home_assets.json)를 연결한다. 비교의 왼쪽은002 기준, 오른쪽은003이며 위부터 프레임930/940/1080이다. 모든 확대는 정수배 최근접 방식이다.

## 실제 소비 경로

도입부는 고정PRG CPU `FBCE`의 `LDX #5A; STX A000; INX; STX A008`을 통해 scanline94에 원본font90/91을 선택한다.002부터 immediate만80으로 바꿔128/129를 선택한다. 홈의 경로는 다르다. `06EA` 프로파일을 두 배로 만든 뒤 `FB34/Y`와`FB35/Y`를 C6/C7에 읽고, `FB1F`의 `LDX C6`가 scanline157에 A000/A008을 설정한다. 홈에서 관측한 프로파일은0이고 원본 테이블은 `5A 3A 5A 66 5A 74`다. 따라서 **ROM1FB44의 테이블값만5A→82**로 변경해130/131을 공급한다. 실행 명령과 지연 루프는 그대로다. C7의3A→B000/B008→CHR58/59는 보존했다.

프레임 끝 PRG가6/7로 보여도 실제 대사는 잠시 bank2/3에서 소비된다. 홈 초기화는 frame924, `9417→9448`, stream pointer9731, NT destination22A8로 관측됐다. 종료 뒤 script ID는0B가 되지만 pointer는9731로 남는다. [읽기 전용 추적](../qa/dialogue/lifetime_home_001/lifetime.csv)과 [수명 요약](../qa/reports/dialogue_font_lifetime001.json)을 근거로 삼는다. 앞 단계의 ‘34/35 직접 공급일 수 있다’는 후보는 홈 대사font의 실제 경로로 채택하지 않았다.34/35는 이 경로의 상단 장면font50/52이다.

## 글꼴·스트림·원본 보호

003은 원본CHR128KiB와 타이틀003 변경을 그대로 유지한다.002에서 추가한8KiB 안의 padding2048바이트를 홈font로 사용해 ROM 크기는270352바이트로 같다. 첫 font128/129는 파일40010..40810, 홈font130/131은40810..41010이며 나머지 padding4096바이트는0이다. 원본font36810..37010도 보존한다. 글리프 슬롯은 등록된 일본어 원천에서 사용하지 않는14칸 중7칸을 사용한다. `자 어 디 로 갈 까`6글자는 Galmuri7 PNG/TTF 픽셀 일치를 검사하고, 쉼표는 같은 Galmuri7.ttf의8px/좌표(0,-1)에서 **명시적으로** 래스터화한다. 물음표6B는 원본glyph, 빈7A는 비0 코드의 빈비트맵이다. 누락 글리프 대체는 없다. 출처·SHA·OFL은 [글꼴 등록](../workspace/fonts/galmuri7_8x8/font_source.json)과 새manifest에 기록했다.

원래12바이트 슬롯과 마지막FF 위치, 전개11칸을 유지한다. 원문의 literal00 빠른 분기1회도 유지하도록 첫 공백은00, 다른 공백과 끝의 시간유지 빈칸은7A를 쓴다. 실제font2048바이트와NT22A8..22B2의11타일이 빌드 데이터와 일치했다. 홈 표시좌표는 이번 실제 화면에서 x64..151/y163..170이다. 도입부의 y=-4 보정을 홈에 자동 적용하지 않았다.

번역 단일 원천54행 중2draft/52untranslated다. 이번에 MAIN_05741의 번역·상태·장면·화자·메모만 변경했다. 화자Buster는 화면에 근거한 추론이고 최종 번역 검토는 대기다. 변경 전 [CSV 백업](../backups/translation/text_ja_before_home_001.csv)을 보존한다. 모든 원문raw/token/pointer/hash와 다른53행은 동일하다.

## 문단별 공급 조사와 둘째 문단 준비

첫 도입 문단의 FF는 frame1002에 처리돼06CF가02로 먼저 증가하지만, 현재font128/129와pointer95F9는 유지된다. frame1090..1100의두문자행에는22개의 비0 타일이 남고1101/1102에는10개,1103부터0개다. 다음pointer9615의 초기화는1107에 완료되고1244에 다시 초기화되며1245부터 새 스트림을 읽는다. `06CD` 하위 바이트 쓰기와`06CE` 상위 바이트 쓰기 사이의9515 같은 일시값으로 선택해서도 안 된다.

따라서 관측한 경로의 설계 후보는 **현재 화면을 지운 다음, native init의9448에서 완성된06CD/06CE를 읽고font bank를 고정해 해당 페이지를 유지**하는 것이다.06CF만으로 IRQ마다 즉석 선택하면 대기 중 기존글자가 다른font로 변한다. 동적 후크에는 scratchRAM 소유권·실제 코드 공간·IRQ 지연 보정·폰트fallback·다음 문단/재진입의 별도 증명이 필요하다. 연속00 영역을 발견했다는 이유만으로 free cave로 사용하지 않았다.

둘째 문단은 `어느 날 마을 변두리에 / 커다란 놀이공원이 생겼어`를 **미채택 준비용 문구**로 시험했다. [준비 패킷](../work/dialogue_font/page_supply_001/supply_plan.json)은한글18글자/별도font2048바이트와 원래40바이트스트림을 만든다. FD3/4, FE의20번 offset, 마지막FF39번 offset, 전개21/20칸, literal00의2/1회를 유지했고, 실제6502 reader43호출 각각의 사이클·커서가 같았다(총4245). 임시메모리 CPU 검사이며 실제ROM에는 넣지 않았다. 준비 문구는 번역CSV에 복사하지 않았고, 향후 채택 시 CSV를 갱신해 빌드입력으로 연결해야 한다. 준비font는01..12 슬롯의 기존일본어glyph를 바꾸므로 **이 페이지가 보일 때만** 선택하고 다른 소비기 전에는 복구해야 한다. plan001의 설명문 `01..13`은 범위 상한의 메모 오류이며 실제mapping은01..12다; 현재 재현 스크립트는 실제글자수로 상한을 기록한다.

## 분리한 검증

- 정적:250 Expected Write와 전체11436바이트diff, 쓰기영역 중첩0, 원본 기대바이트검사, title003 CHR/원본font/첫font 보존, CSV 원천보존, 사용한글 누락0 통과.
- CPU:첫문단37호출/3282사이클, 홈12호출/1246사이클의 각호출·커서가 원본과 같다. 둘째 준비패킷43호출/4245는 별도의 CPU 증거다.
- 빌드/적용:003 새폴더 재빌드와 한글·공백 경로에서 독립CLI로 실제IPS 적용한 ROM이같다.
- 실행:고정Mesen2.1.1/콜드부팅/컨트롤러만 사용. 무입력5400프레임249표본은002와 화면전체 동일. Start720..727/3000프레임188표본 중172개는 홈대사만 변경,16개는 화면전체 동일. 합계437표본에서 홈대사영역 밖0픽셀, OAM/팔레트/문단ID·pointer동일.
- 직접시각:실제frame1080 확대와930부분출력/940완성/1080대기 비교를 확인했다. 한글·쉼표·물음표가 읽히며 창과캐릭터/상단그림은 보존됐다. 사용자 최종문구·디자인승인은 별도다.

라이드 선택 후 이동·대사교체, 다른font프로파일1/2의 실제장면, 전체문단 동적전환, 모든선택/교환/엔딩, 전체완주·실기·오디오·reset/savestate, 최종승인·정식배포·카페게시를 완료했다고 주장하지 않는다. 기존002/title의검증보고서와manifest는 당시입력의 역사적 증거로 보존하며 현재CSV로 옛세션감사`audit_dialogue_session.py`를 다시 실행하지 않는다. 이번capture 환경json의scope 문자열은 당시wrapper의‘title/first-paragraph’기본설명이며 실제 대상은 기록된ROM SHA로 식별한다. 향후runner는 build_report의scope를 사용하도록 정정했다.

## 재현

프로젝트 루트에서 새출력경로를 사용한다. 기존검증build ID를 덮어쓰지 않는다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_source.ps1
python .\scripts\build_dialogue_home.py --output .\build\dialogue_home_repro_next
python .\scripts\dialogue_ips.py create --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --target .\build\dialogue_home_repro_next\TinyToon2_dialogue_kr_poc.nes --patch .\build\dialogue_home_repro_next\TinyToon2_dialogue_kr_poc.ips --scope 'Title003 + first/home draft development PoC'
python .\scripts\dialogue_ips.py apply --source '.\original\rom\Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes' --patch .\build\dialogue_home_repro_next\TinyToon2_dialogue_kr_poc.ips --output '.\qa\dialogue\한글 적용 재현 next\TinyToon2_home_applied.nes'
python .\scripts\run_dialogue_qa.py --rom .\build\dialogue_home_repro_next\TinyToon2_dialogue_kr_poc.nes --output .\qa\dialogue\home_repro_start_next --frames 3000 --start 720 --script .\scripts\capture_dialogue_lifetime.lua
python .\scripts\run_dialogue_qa.py --rom .\build\dialogue_home_repro_next\TinyToon2_dialogue_kr_poc.nes --output .\qa\dialogue\home_repro_attract_next --frames 5400 --script .\scripts\capture_dialogue_lifetime.lua
python .\scripts\plan_dialogue_page_supply.py --output .\work\dialogue_font\page_supply_next
python .\scripts\verify_dialogue_home.py
python .\scripts\audit_dialogue_home_session.py
```

읽기 전용 수명 추적은 `run_dialogue_qa.py --rom <002 ROM> --output <새폴더> --script .\scripts\trace_dialogue_lifetime.lua --frames 5400`과`--frames 3100 --start 720`로 나누어 수행한다. 네이티브reader 검사는py65-1.2.0의CPU 모델이며실제NMI/IRQ가없다.현재437표본 검사기는 고정된003/기준002 캡처를 대상으로 하고 새이름의캡처를자동탐색하지 않는다.

**다음 작업 하나: 검증된 지우기/초기화 경계에서 문단별font를 고정하는 동적 공급 후크를 구현해 MAIN_05625를 실제 삽입하고, 대기·다음 일본어 문단·도입 재진입을 비교 검증한다.**
# 현재 기준 안내 — 2026-10-05

이 문서는 작업10의003 구현과 당시2draft 입력에 대한 기록이다. 현재 통합본은 [008](POC_DIALOGUE_PAGES.md)이며 홈 구현은 그대로 보존했다. 현재CSV는3draft/51untranslated다. 아래 역사적 검사 스크립트는 현재CSV로 다시 실행하지 않는다. 최신 인계는 [HANDOFF](HANDOFF.md)를 따른다.

