> **2026-10-09 작업226: v1.0(데이터062) 최종 배포·작업기 준비 완료. 사용자1차 실화면·완주 완료, 배포 이후 검증 예정.** [최신 인계](HANDOFF.md)

아래 본문은 각 작업 당시의 역사 기록입니다. 현재 공개 파일과 검수 상태는 최신 인계를 따릅니다.

> **2026-10-08 현재개발049 / 작업175 완료.** [최신 인계](HANDOFF.md)

현재 기준은 [검수 연결/잔여조건175](CURRENT049_USER_REVIEW_READINESS_175.md), [보존6건/검토·적용173](CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md), [오프라인 캡처174](CURRENT049_OFFLINE_CAPTURE_PROVENANCE_174.md)다. 아래는각작업당시의구조/관측기록이다.

# 2편 조사 현황 — 2026-10-04

기준: [원본 manifest](../manifests/source_rom.json). 현재 [통합012](POC_DIALOGUE_THIRD.md)는 타이틀003·첫째/둘째/셋째 도입 문단·홈 초안과 문단별 글꼴 공급을 포함한다. 아래 조사 기록은 각 작업 당시 결과이며 한글화 전체 완료를 주장하지 않는다.

## 확인된 구조

| 항목 | 2편에서 확인한 사실 | 근거 |
|---|---|---|
| 입력 | 262,160바이트, iNES 1.0, trainer 없음, mapper 85 | 원본 헤더·CHR 조사 JSON |
| PRG | 파일 `[0x00010,0x20010)`, 128 KiB | 헤더/실제 길이 |
| CHR | 파일 `[0x20010,0x40010)`, 128 KiB, 8,192타일 | 32페이지 모두 decode→encode 일치 |
| 실행 | Mesen 2.1.1 원본 콜드 부팅, 타이틀·자연 도입부·홈 선택 안내 | baseline_attract_002 / baseline_game_001 |
| 글꼴 | 관측한 도입부/홈에서 PPU `$0000/$0400` → CHR 상대 `0x16800/0x16C00` → 파일 `0x36810/0x36C10` | 각 캡처 mapping.csv와 PPU 덤프 |
| 주 대사 저장 | bank 2, 파일 포인터 `[0x55A9,0x5609)`, 48슬롯, 46고유 스트림; 데이터 `[0x5609,0x5A28)` 1,055바이트 | 소비 코드 `$9430/$9438`, 추출 왕복 |
| 읽기 | bank 2의 `$9393: LDA ($06),Y`, 포인터 `$06CD/$06CE`, cursor `$06C3`, 전개 버퍼 `$0740,X` | text_trace_003 실제 read와 text_consumer_001 실행 직전 trace |
| 매크로 | bank 3을 `$A000` 창에서 사용; 포인터 `[0x61B1,0x61C3)` 9슬롯/8고유 스트림; 데이터 `[0x61C3,0x61FF)` 60바이트 | 코드 `$9351/$9356/$9360`, 실제 실행 매핑 |
| PPU 소비 | 전개된 문자가 RAM 전송 큐를 거쳐 `$D09C: STA $2007`에서 표시 | text_trace_001 PPU write 로그, 정적 코드 |

CPU 주소만으로 파일 오프셋을 정하지 않는다. bank 2가 `$8000`에 매핑된 관측 경로는 `file = CPU - 0x3FF0`, bank 3이 `$A000`에 매핑된 매크로 경로도 이번 구성에서는 같은 산식이다. 다른 뱅크·장면에 이 산식을 자동 적용하지 않는다. 프레임 끝의 PRG 매핑은 대사 처리 중 임시 매핑을 놓친다. baseline에서 `$8000`의 bank 6만 보였지만 실제 대사는 bank 2를 잠시 사용했다.

VRC7의 CPU 8 KiB 창과 PPU 1 KiB 창, Tiny Toon 2 보드의 A3 레지스터 배선은 [NESdev VRC7](https://www.nesdev.org/wiki/INES_Mapper_085)을 참고한다. 헤더가 iNES 1.0이므로 submapper 숫자를 원본에 새로 확정하거나 수정하지 않았다. 런타임 도구는 [Mesen 공식 Lua 문서 원천](https://github.com/SourMesen/Mesen2/blob/master/UI/Debugger/Documentation/LuaDocumentation.json)을 참고했다.

## 문자와 제어

- 글자 칸은 관측한 일본어 폰트에서 8×8px. 현재 폰트 128타일의 실제 배치와 [코드별 이미지](../extracted/chr/survey_20261004_001/japanese_glyph_codes.png)를 보존했다. 1편의 문자표는 그대로 사용하지 않았다.
- `00` 공백, `FE` 줄바꿈, `FF` 스트림 끝, `FD nn` 공백 전개를 코드에서 확인했다. 원본 `FD` 인수는 양수이며 최대 `20` hex까지 관측했다. 제어 토큰의 출력 수와 레이아웃은 원래 소비 루틴으로 검증해야 한다.
- `F8/F9`는 `$07D0` 계열 숫자, `FA`는 `$25`로 고르는 숫자 테이블을 전개한다. 화면상 의미·숫자 범위·0일 때 처리의 전체 QA는 미완료. 일반 문자로 번역하거나 삭제하지 않는다.
- `80..88`은 현재 발견한 공통 문자열 매크로. `80/81`은 같은 원천을 참조한다. 도입부의 `81`이 ‘バスター’로 전개되는 실행 경로를 확인했다.
- 관측한 kana font에서 히라가나·가타카나·부호·숫자를 [현재 문자표](../workspace/tables/kana_codes.json)로 대응했다. 등록 kana 프로파일의 사용 코드 미대응0이다. 크레딧3원천은 다른 글꼴 프로파일 가능성이 있어 해석을 확정하지 않는다.

## 초기 규모와 남은 위험

등록한 두 테이블에 대해서는 54개 고유 원천 단위, 데이터 1,115바이트 + 포인터 114바이트가 정적 왕복 일치한다. 공유 참조·공백 전개·숫자·크레딧을 포함하므로 54개 대사 문장이라고 부르지 않는다. 전체 게임 문자/그래픽 텍스트 총량은 **미확정**이다. 자연 도입부의 주 인덱스 `01..09`와 홈 안내를 관측했으며 나머지 인덱스 장면은 아직 대응하지 않았다.

| 미해결 | 다음 증거와 구현 판단 |
|---|---|
| 다른 글꼴 프로파일 | 관측 kana 사용 코드 대응 완료; 크레딧/다른 소비기의 픽셀·코드표 확인 필요 |
| 홈·놀이기구·교환·엔딩의 인덱스/분기 | 호출부와 디스패처에서 목록을 만들고 원본 화면을 연결한다 |
| 문장별 한글 글리프 수·전송 버퍼 용량 | 첫 문단14글자/2행/24칸 창/18·17전개칸 PoC 통과; 전체 문단·숫자·매크로 예산은 별도 측정 |
| 폰트 bank 공유와 IRQ/NMI 수명 | 글자·숫자·UI·그림이 공존하는 뱅크와 대기/지우기/복귀를 조사한다 |
| 타이틀 외 그래픽 글자 | 타이틀 CHR17/19·CHR 내 압축 배치 소비는 확인 및003 구현; 나머지 장면은 개별 추적 필요 |
| 재삽입 공간·뱅크 변경 | 글꼴/문장 PoC의 실제 필요량을 측정한 뒤 결정한다 |

원본의 모든 장면·글로벌 텍스트 부재 증명·배포·전체 완주·실기 검증은 미수행이다. 첫 문단 이후의 확장에는 문단별 글꼴 공급과 폰트 수명 검증이 필요하다.

## 첫 구현: 타이틀 한글화

사용자 지시로 대사보다 타이틀을 먼저 구현했다. 실제 화면의 CHR17/19 전환과 숫자2 OAM을 보존하고, PNG/내장 생성형 이미지/타일 변환/압축 스트림 재삽입을 완료했다. 배치 원본은 CHR 파일`0x24939..0x24A0B`이며 RAM0400 복사 뒤 PPU 전개된다. [POC_TITLE](POC_TITLE.md), [배치 명세](../manifests/title_layout.json), [검증 보고서](../qa/reports/title_kr_ai_003_validation.json)를 따른다. 타이틀 기술 PoC 통과는 전체 번역 완료를 뜻하지 않는다.

## 다음 구현: 첫 도입 문단

네이티브 파서와 원본 IRQ를 유지한 `dialogue_kr_poc_002`에서 MAIN_05609 초안을 표시했다. CHR banks90/91 원본을 보존하고128/129에 한글14글자와 비0 빈 glyph7A를 추가한다. 공백의 빠른 분기를 피하고 원래28바이트/FD6·7/18·17칸/37호출 사이클을 맞췄다. 실제165표본에서 문단 밖 차이0이다. [POC_DIALOGUE](POC_DIALOGUE.md)를 재현/한계 기준으로 삼는다. 임시 pool은 전체 한글화의 문자집합/동적 글꼴 설계를 대신하지 않는다.

## 홈 구현과 수명 조사 — 작업10

현재003은 홈 `MAIN_05741`까지 포함한다. 홈font는34/35가 아닌06EA profile0→ROM1FB44→C6→FB1F IRQ에서 선택한다. 해당 테이블5A→82로130/131font를 공급하고 C7/상단장면/도입font를 보존했다. 홈12바이트/11전개칸/reader12호출1246사이클 유지,437표본의 홈 영역 밖 차이0이다. [현재 구현](POC_DIALOGUE_HOME.md)과 [검증](../qa/reports/dialogue_home003_validation.json)을 따른다.

도입부06CF는 FF 처리시 먼저 증가한다. 첫문단pointer95F9/현재font를 유지한 대기 후 두문자행은 frame1103부터 비었고, 다음pointer9615의 native init은1107/1244에 관측됐다. 따라서 다음font는 초기화완료9448에서 완성pointer를 기준으로 고정하는 방식을 검토한다. 실제동적후크는 아직 없다. 둘째문단18한글/40바이트/43reader호출4245사이클의 [미채택 준비](../work/dialogue_font/page_supply_001/supply_plan.json)는 CPU 검사만 통과했으며 실제ROM/번역CSV에는 넣지 않았다. 화면지우기·다음font복귀·IRQ지연·scratchRAM 소유권은 다음구현의 검증대상이다.
# 최신 통합 기준 — 2026-10-05 작업12

현재 채택본은 [dialogue_kr_poc_008](POC_DIALOGUE_PAGES.md)이다. PRG256KiB/CHR136KiB로 원래 native PRG 선택값과 원본CHR·타이틀003·첫 문단/홈 글꼴을 보존하며 둘째 문단을 추가했다. 완성된 native pointer에 따라 C6를128/132/90으로 고정하고 다음 일본어 문단에서90/91로 복귀한다. FF의06CF 선행증가만으로 글꼴을 바꾸지 않는다.

850개의 동일조건 화면 비교에서 대사 두 줄 밖 차이0, 홈233표본 전체일치, palette/OAM/문단ID/pointer 일치다. 정상콜드부팅, 출력/대기/지우기/다음일본문단/자연반복재진입/도입중Start 건너뛰기를 확인했다. CPU ABI784조건과 실제IRQ2820시점도 일치한다. 현재CSV는54원천 중3draft/51untranslated다. 아래 작업10까지의 기록은 당시 상태이며, 최신 재현·한계는 [페이지 글꼴 문서](POC_DIALOGUE_PAGES.md)와 [인계](HANDOFF_2026-10-05.md)를 따른다.

## 최신 통합 — 2026-10-05 작업13

012는 셋째 MAIN_0564D의12한글을134/135font에 추가했다. 기존2KiB padding을 사용해 크기는401424바이트다.24바이트/00 세개/FF와reader24호출2502사이클을 보존했다. selector145바이트,48슬롯 초기화시간008과동일,CPU1072조건통과다.1998화면에서셋째한줄밖차이0,홈407전체일치,IRQ8973시점동일을확인했다.012는현재CSV4draft/50untranslated와동봉snapshot이일치하고011에서실행검증한ROM과전체바이트가같다. 자세한한계와재현은 [셋째문단](POC_DIALOGUE_THIRD.md), [최신인계](HANDOFF.md)를따른다. 다음은이름macro81이있는MAIN_05665와추가font공간이다.

## 2026-10-05 작업14 — 넷째013 현재 검증

[넷째 구현](POC_DIALOGUE_FOURTH.md), [검증](../qa/reports/dialogue_fourth013_validation.json), [원천 식별](../manifests/dialogue_fourth_assets.json), [현재 인계](HANDOFF.md)를 따른다. MAIN_05665(pointer9655)의 두 줄을 “버스터 바니의 집에 / 편지 한 통이 도착했어”로 삽입했다. 원본macro81과 모든macro 테이블/페이로드를 보존했고 전용font에서5전개타일을 빈칸으로 삼아 이름을 inline 배치했다. 원문/raw/참조/포인터와 다른53행은 불변이다. 현재5draft/49untranslated이며 전게임 대사량은 미확정이다.

기존CHR padding 소진에 따라144KiB로 확장했다.17한글,font136/137,file62010..62810와 새6KiB padding62810..64010(16진,끝제외),ROM409616바이트. helper107바이트+256바이트font table9700..97FF(전용bank2)를 사용하며 모든48슬롯의 시간이008/012와 같다. canonical18의 native 텍스트/매크로,IRQ,이전font와 타이틀을 보존했다.

정적6 Expected Write/중첩0/012 전체 허용범위 외 바이트불변,reader44/4263호출별동일,CPU1168조건,깨끗한재빌드/실제IPS적용동일을 통과했다. 실제 Mesen2048표본 넷째두행밖 차이0,홈417전체일치,font531표본,복귀19회,IRQ9339시점일치(font선택384건만 변경)다. FF→대기→첫행1815/둘째1817지우기→1822원본font복귀,반복4500,Start1740/1530을 확인했다. 직접한글1790/4500·일본어1920·홈1080도 시각검토했다.

과거작업과 원본/1편/기존build/QA를 보존했다. 전게임·놀이기구분기/엔딩·오디오·reset/savestate/실기·최종번역/명칭/디자인 검토와 기존PRG/RNG22 영향 한계는 남는다. 개발본이며 dist/외부게시/최종카페글은 아직 없다.

**다음 작업 하나: MAIN_0568B의 네 줄 편지 본문과 이름 매크로81의 전개·버퍼·글꼴 수명을 확인하고 한글로 삽입한다.**

## 2026-10-05 작업15 현재 — 도입014

[관측도입9문단 구현](POC_INTRO_COMPLETE.md),[검증](../qa/reports/intro014_validation.json)을현재기준으로삼는다. 새5행번역으로10draft/44untranslated,CHR152KiB/ROM417808,예약4KiB다. 기존모든glyph/IRQ/제어/시간을보존하고5본문과font table/font만추가했다.2334화면문단밖차이0/홈492전체일치,IRQ41034시점동일,CPU1408조건,재빌드/실제적용동일이다. 사용자지시로계속진행한다.

**다음 작업 하나: 홈 선택·매표소·입장조건·스테이지설명의 원천ID/IRQprofile/숫자 소비를 실제controller 경로와 연결하고 한글 글꼴 공급 방식을 정한다.**


작업17/18: 홈 글꼴 latch 기반017 채택.015/016 타이밍 실패 후보 보존,017 전체2521화면 차이0/실제115353시점 일치. 원래 PPU2002 읽기 유지·초기화76사이클·10draft44미번역 불변. [상세 기록](UI_FONT_LATCH.md). 다음은 UI macro/인코딩 제약 검사이며 별도 중단 지시 없이 이어간다. 전체 완료·배포·카페 게시가 아니다.


작업19/20: 일본어를 보존하는UI매크로/font019 기반 채택.018의상단 설명판 결함을 실제NMI추적으로찾아9E28→RAM34를수정했다.679전체화면/74319시점동일,reader48슬롯/변수192조건검증.10draft44미번역불변. [상세](UI_MACRO_PASSTHROUGH.md). 다음은관측된홈/매표소8문구초안삽입이며바로이어간다.


## 작업21~23 현재 — 홈·매표소022

홈 선택4개/매표소 출발·환영·교환·부족4문구의초안을삽입했다. [구현/해시/재현/한계](UI_HOME_BOOTH.md),[실제8페이지](../qa/dialogue/ui022_actual_pages.png),[검증](../qa/reports/ui022_validation.json).020전환깨짐/021도입1사이클경계차이는기각하고보존했다.022는매표소중복초기화만조정해공통005와도입부를유지한다.1527표본현재행밖차이0/도입848전체일치/115353실제시점동일,CPU1504+108조건,재빌드/실제적용동일.18draft36미번역,CHR168KiB/ROM434192,전게임완료율아님. 다음은기차·급류타기·성입구 소비기조사이며즉시이어간다.


작업24: [기차·급류·성조사](UI_RIDE_GATE_SURVEY.md).2/3장요금·진입절차·성4골드/50일반부족분기확인. 성대사font불일치를발견해즉시교정/검증한다. ROM022/18draft36미번역불변,전체플레이/성공분기검증아님.


작업25: [성상단font023교정](GATE_TOP_FONT.md) 채택.2바이트만변경,한글18draft36미번역불변.1105표본홈한글행밖0/기차·급류631전체일치/성정상221,69714실제시점동일. 성은NMI font34로두행을공급한다. 다음은기차/급류홈2문구삽입이다.


작업26: [홈기차·급류024](UI_HOME_RIDES.md) 채택.20draft34미번역,CHR176KiB/예약6KiB.1105표본선택행밖0/성474전체일치,195169실제시점동일,CPU1504·재빌드/실제적용같음. 다음은성문단별상단font공급과전환검증이다.


작업27: [성NMI시점실패](../qa/reports/commit026_rejection.json).025/026은픽셀474/CPU1728·1504/실제적용통과에도NMI1077건2cycle차이로기각.024/SSOT20draft34유지. 시간증가없이홀수뱅크상단font공급으로수정해즉시검증한다.


작업28: [같은시간상단font027](GATE_FONT_TAG.md)채택.20draft34미번역불변.2001전체화면/PPU/OAM같음/185067실제시점같음,CPU1728·1504/재빌드·실제적용같음. 홀수custom font가상단도공급하며성fallback171은같은일본어glyph다. 다음은관측성5문구한글삽입이다.


## 작업29 — 성 입구 문구5개, 028 채택

[구현·변경 파일·해시·재현·검증 한계](UI_CASTLE_MESSAGES.md)를 기록했다. 신규 prepare_ui_gate.py/build_ui_gate.py/verify_ui_gate.py/verify_ui_gate_hooks.py/make_gate_page_evidence.py, plan/SSOT backup,028/재빌드/한글경로 적용,성 v4·IRQ 캡처와 직접5문구 화면을 보존한다. 이전20초안·원본·1편 불변. 정적/CPU1504·seed720/실제 적용·재빌드 PASS;474화면의 현재 행 밖 변화0/69714실제 시점 동일/일본어1A 복귀9장 전체 동일; 직접5장면 가독성 확인. 등록25draft29미번역, 전체 플레이 등은 미수행. ROM SHA256 `c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e`; IPS `352d9cf7f33ecefdba41b897bc12b989acff3b18eaaf81a087f2fe3774cba136`; CSV `2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8`.

다음 행동 하나: 골드4장·일반50장의 입장 성공 분기를 지정 RAM seed QA로 관측한다. 바로 계속한다.


## 작업30 — 입장권 충족·포인트 교환 성공 분기 관측

[변경 파일·해시·명령·검증 한계](NATIVE_BRANCH_SURVEY.md):028 ROM/SSOT25draft29미번역 불변. 별도 runner/Lua/4종 seed와4개 QA를 추가했다. frame1000의 지정 RAM 주입 주소·전후값·PC/cycle을 보존하며 일반 플레이와 구분한다. 원본 CPU 숫자 판정24건 동일. 골드4 입장/일반50→0 입장/49부족/3점→0과티켓10→11 교환을 실제 native 이벤트·RAM으로 확인했다. 실제 화면과 성 내부 상태도 검토했으나 완주/자연 수집은 미수행. 이전 산출물·원본·1편 보존. 다음 행동 하나: FA를 유지하는 성 가격1A와 허가1C 한글 삽입·검증. 바로 계속한다.


## 작업31 — 성 가격·입장 허가,031 채택

[구현·변경 파일·해시·명령·한계](UI_CASTLE_PRICE_ADMISSION.md): FA 원래 숫자 출력과alias2C를 보존하여 일반 티켓 가격1A/허가1C를 삽입했다. 이전25개 초안·원본·1편·모든 산출물 보존. 029/030의 검사 건수/별칭 중복 메타데이터를031에서 고쳤고 ROM은 모두 동일하다. 정적/문구별48변수조합/ABI1504·초기seed720/재빌드·실제적용 PASS. 실제1522화면의 성 대사행 밖 변화0/299240시점 동일, 직접 가격2436·허가2124 및 성 카드/게임상태 확인. 성공 경로는 명시RAM seed이며 자연수집/완주가 아니다. 등록27draft27미번역. ROM SHA256 `8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19`; IPS `3c5a6b88e040064ab664b93bd6cefc030f580d974a05dd8012ef769100febf2a`;CSV `979325a40d12762c62d27ec4a70edc33646ae780dedf2e787bbca4c498e67462`. 다음 행동 하나: 교환 완료 인사15/출발2A 한글화·검증. 바로 이어간다.


## 작업32 — 교환 완료 인사·출발,032 채택

[변경 파일·해시·명령·검증 한계](UI_SUCCESS_START.md): 인사15/출발2A를 하단 전용188/190으로 삽입하고 상단 일본어 카드를 보존했다. 원본/1편/이전27개 초안·모든 산출물 불변. 정적/reader각호출/ABI1504·seed720/재빌드·실제적용 PASS.863화면의 현재 행 밖 변화0/215827실제 시점 동일, 직접 두 문구/성 게임상태 검토. 성공은 지정RAM seed이며 자연수집/완주 증거가 아니다. 등록29draft25미번역. ROM `c4b40639bafba6a25a1c186c82005963ec4fecdf8d3a22308eaf1ab6643a7d67`;IPS `0eb0c8328e9196bf8c1e008b4d8ce080d0cb9794112f3097d002b835331c4ada`;CSV `ba881bbffdaf4f5fa84d43f941d9166914e156358a7337c3b1bb66be8af33c86`. 다음 행동 하나: 놀이기구 상단 제목·규칙·요금 공통font 구성/다섯 경로 검증. 즉시 진행한다.


## 작업33 — 다섯 놀이기구 공통 카드033

40draft/14미번역. 공통193/194에 한글79자, 제목5·규칙5·요금1. 원래FA 요금4/1/2/3 유지. 1786화면/505383시점, reader528/즉시출력66/ABI1504/초기font720, 재빌드·실제IPS 적용 통과. 보호 픽셀/상태 차이0. 요금 지우기 전환의 셀별·인접3frame 허용을 별도 기록. 다섯 실제 정수4배 화면 직접 검토. 성gold4만 지정RAM seed, 전체 플레이 미수행.

[구현·변경파일·해시·재현·한계](UI_RIDE_CARDS.md). 다음 행동 하나: native29/2B 소비를 특정하고 두 안내 한글화. 계속 진행.


## 작업34 — 부족/소지 문구034 시험 실패

실제normal3 지정seed에서2000/2008 slot29,2600/2607 slot2B 및F8 일반티켓07D0..2 소비 확인. 두 초안 등록으로SSOT42draft/12미번역.034 CPU/재빌드/실제IPS는 통과했으나frame2004 요금 x160..167/y163..170 보호 픽셀 변화로 거절했다. 새196font가 native9F09 초기화에서 기존 요금 지우기 전에 적용됐다. 모든034/재빌드/적용/소스/실행 보존,채택033유지. [실패 근거](../qa/reports/remaining034_rejected.json). 다음 행동 하나: postclear9A81 소비와209cycle/19위상 정합을 검증하고9F09의 조기 초기화만 수정한다. 바로 이어간다.


## 작업35 — 공통하단036 채택,034실패 수정

42draft/12미번역. 공통196/197에 요금/F9(00+23)/부족/출발/소지5unit6slot. 원래코드변경0, macro88 티켓을 통일. 조기font손상 제거.034전환실패와035메타키erratum보존. ABI1504/초기720/상단30/reader240/즉시출력30,6경로2125화면/599931시점 및 새intro848전체화면/41034전체시점 동일, 실제부족·소지3·요금4·출발·동일frame전환 직접검토. 재빌드/한글경로 실제IPS 통과. source원본무변경. [변경파일·해시·재현·증거·한계](UI_STAGE_LOWER.md). 다음행동 하나:크레딧CF0A/07DF소비와CHR/스크롤을 별도scene seed로 특정. 계속한다.


## 작업36 — 크레딧실제소비 조사,036/42draft 유지

ROM/CSV변경0,재빌드/적용없음. root18=7/19=1/07DF1/06DE0 지정4seed의v3에서2D/2E1001,2F2361 소비및NMI124/125/IRQ없음/NT2805·2005/스크롤을확인했다. 초기v1bootstrap실패/v2menu비소비대조보존. 실제4페이지직접검토,개발자·KONAMI·권리표시보존계획. 이전CPU925E NT바이트기하erratum와올바른96쌍+3크레딧명령주소근거추가,실제runtime근거는영향없음. [변경·해시·재현·한계](CREDITS_CONSUMER_SURVEY.md). 다음행동 하나:공통201/202로3크레딧·A457생산자한글화및스크롤/이름/권리표시보존검증. 계속한다.


## 작업37 — 크레딧037 채택

게임명·제작 역할3원천 한글화, 이름·KONAMI·권리표시 보존.45draft/9기술·공유원천. 정적/CPU/ABI1504·초기720/재빌드/한글 경로 실제IPS 통과. 크레딧327화면·99724시점, 새intro/coaster1150전체화면·137255전체IRQ값 동일. 직접 네 actual 화면 검토. 지정4seed이며 자연 엔딩/전체완주 증명이 아니다. [변경·해시·재현·검증 한계](CREDITS_KOREAN.md). 다음 행동 하나: 기술·공유 원천과 남은 영문 그림의 실제 소비 정리. 중단 없이 계속한다.


## 작업38 — 등록 기술/공유원천 관계정리

ROM/SSOT변경없음,037유지.45표시초안+F9숫자1+문맥글꼴macro7+등록내미사용macro1. 전체corpus완료아님. [변경·해시·정적검증·한계](REGISTERED_SOURCE_READINESS.md). 다음행동:지도간판NT/CHR소비연결과PNG추출. 계속한다.


## 작업39 — 지도간판실제소비·PNG추출

상단NMI CHR80~83/36NT셀/팔레트와144×16 원래PNG가전체RGB일치,현재지도상단타일각1회. ROM/SSOT변경0,037유지. [파일·해시·재현·정적/실제근거·한계](MAP_BANNER_EXTRACTION.md). 다음행동:imagegen으로몬타나랜드생성및틀보존삽입/관측consumer검증. 계속한다.


## 작업40 — 생성형지도간판038채택

몬타나랜드PNG→13px/원래palette→32tile/391bytes삽입. 코드·대사·틀·NT·팔레트불변,45draft/9기술공유유지. 재빌드·실제IPS/1565화면/70947동일IRQ값/보호픽셀0,직접정상/fade지도검토. [파일·해시·재현·검증·한계](MAP_BANNER_KOREAN.md). 다음행동:매표소영문NT/PRG·NMI/CHR소비추적. 계속한다.


## 작업41 — 매표소CHR/PRG문자실제소비조사

038/SSOT불변. controller-only4500+IRQ4500,원래NMI124/125/102/103·literal각806Eread·NT·간판24tile실제RGB연결확인. [파일·해시·재현·검증·한계](BOOTH_GRAPHICS_SURVEY.md). 다음행동:전용font204/205 및生成형매표소간판삽입/숫자·대사·보호픽셀·시점검증. 계속한다.


## 작업42 — 매표소그림/소지·점수039채택

생성형매표소24tile, literal5군/currentfont204·한글12자로삽입. 등록45draft/9기술공유유지. 정적/CPU생산자768·decoder128D-clear/재빌드/실제IPS/2243화면·188916시점/보호픽셀0,추가NMI204font17실제표본/124대조19같음. 내부3은실화면3000점,교환후0점/11장인원래동작보존. 직접정상/교환전후검토. [파일·해시·재현·검증·정정·한계](BOOTH_GRAPHICS_KOREAN.md). 다음행동:놀이기구게임/HUD·결과화면남은영문/일본문자소비조사. 계속한다.


## 작업43 — 실제놀이기구 HUD/결과후보 조사

039/CSV불변.4경로42,000프레임과read-onlyHUD4500,상단5행/NT2F00·CHR124/125·IRQ FCCF실제연결.4784픽셀 exact/마지막시간한칸 epoch차이3픽셀은이전9전체64pixels로설명. 결과CHR24A0B소비미확정. 정적/에뮬레이터/직접그림확인이고새빌드/적용/전체완주없음. [변경·해시·재현·근거·한계](GAME_HUD_SURVEY.md). 다음행동:206/207+fineY0/7행HUD040시험및시각·숫자·타이밍검증. 계속한다.


## 작업44 — HUD040 채택

체력/점수/시간/점/티켓/금티켓6종,전용206/207과fineY0로7행확보.하트·본문·숫자·틀2픽셀아래의의도된배치변경.768CPU/재빌드/한글경로실제IPS/4558화면/1321047시점통과,상태동일·HUD밖0.기차원래y191의검증기하정정/첫Lua명bootstrap실패보존.5게임+pause/resume6실제화면직접검토.등록45draft/9기술공유불변,자연완주/전체corpus/오디오/실기/최종사람검토없음. [변경·해시·재현·근거·한계](GAME_HUD_KOREAN.md). 다음행동 하나:결과nativephase20/font124/CHR24A0B 소비연결후보너스7종한글화. 바로계속한다.


## 작업45 — 보너스 실제 소비 조사

040/CSV불변.게임초기화후54=20/3200의1주소seed,nativeF8BA/F8BF/F8CF·8216/049FB→원본24A0B/현재44A0B/154바이트복사전체일치.7문구8literal/1024NT셀,5632nativeRGB·NMI124/12518표본일치,실제집계화면직접검토.자연클리어/전체corpus아님. [변경·해시·재현·근거·한계](RESULTS_CONSUMER_SURVEY.md). 다음행동:전용208/209·literal한글화/11cycle ABI·집계·완료·숫자·재진입검증. 계속한다.


## 작업46 — 결과 화면041 검증·채택

축하/체력·클리어·시간 보너스/획득 점수/점/보유 점수7종8literal, 전용208/209·20한글로 삽입했다. 원래 글꼴·숫자·계산·압축제어·NT/속성/길이 보존. CPU768·decoder128D-clear·재빌드·한글 경로 실제IPS 적용·5907화면·354362시점 비교 통과, 실제6장면 직접 검토. 네 놀이기구와 재클리어는 선언한phase/history seed이며 자연클리어를 주장하지 않는다. 등록45draft/9기술공유/CSV 유지. 원본·1편·이전 성공/실패/QA 모두 보존. [파일·해시·명령·검증 분류·한계](RESULTS_KOREAN.md). 다음 행동 하나: PAUSE/GAME OVER의 실제 배치·CHR78..7B 소비를 추적하여 추출. 바로 계속한다.


## 작업47 — 실제 게임오버·선택지 소비/PNG 추출

초기 normal4 seed 뒤 native 플레이 실패로 GAME OVER·CONTINUE ?·“YES!”·“NO.”에 진입. source그림 CHR123/NT64셀4,096RGB·문자21셀1,344RGB와 실제 읽기/생산자·NMI4KiB77표본 전체 연결. native 예=홈/normal10, 아니요=시작·타이틀/attract 복귀 확인. 041/CSV 불변, 원본·실패/기존 PNG 보존. 새 한글 빌드/적용/자연 초기화/전체완주 아님. PAUSE는 후보로 남음. [파일·해시·재현·근거·실패·한계](GAMEOVER_CONSUMER_SURVEY.md). 다음 행동 하나: 생성형 게임오버 PNG·전용210/211·212/213·선택3문구 삽입 및 두 복귀/시점 회귀. 계속한다.


## 작업48 — 생성형 게임오버/선택3문구042 검증·채택

원래PNG→imagegen게임오버→4색128×32/64tile, 전용210/211·212/213과 선택3문구21셀·8한글로 삽입.768CPU/384D-clear queue/재빌드/한글경로실제IPS/4040화면·378645시점 통과, 소유4영역 밖0·상태·커서·두복귀동일, 실제6장면직접검토. 테스트하네스SP·nativecommand길이127·fade의root8 자원수명 정정도 보존. 원래/기존글꼴·소스·1편·실패/QA 보존, 등록45draft/9기술공유/CSV불변. 초기티켓·회귀seed이며 전체자연완주/전체corpus 아님. [파일·해시·명령·검증 분류·한계](GAMEOVER_KOREAN.md). 다음 행동 하나: PAUSE native코드·CHR120/121와 세계영문그림 소비 목록 추적. 바로 계속한다.


## 작업49 — 일시정지·기차 그래픽 조사

042/원본/CSV 유지. PAUSE CPU1,024사례와 네 컨트롤러 경로1,194화면을 검증했으며 bank120/121은 해당 경로에서 선택되지 않았다. 기차 IRQ의72..75 뱅크 선택4,566회와 152개 전체 패턴 표본이 원본과 같다. 글자 표시 RGB는 미확인. [파일·해시·명령·검증 종류·실패 정정·한계](PAUSE_WORLD_SURVEY.md). 다음 작업 하나: native 기차 체력3 보충 진단으로 간판 실제 NT/RGB 연결. 계속한다.


## 작업50 — 기차의 실제 MONTY S / M 문양 / LAND R.R.

042/원본/CSV 불변. 실제 원문 MONTY'S·장식M·LAND R.R.로 이전 정적 후보를 정정했다. 정상 최대 체력3만126회 보충한 진단을 별도 기록했으며 자연 플레이 증명으로 쓰지 않는다. IRQ15,252회/전체4KiB508표본·실제PNG2,048픽셀이 원본과 같다. [파일·해시·명령·검증 분리·한계](TRAIN_SIGN_CONSUMER.md). 다음 작업 하나: 전용216..219에 세 문구를 삽입하고 IRQ5의 시점·보호픽셀·회귀·적용 검증. 계속한다.


## 작업51 — 기차 한글 간판043

채택043 ROM087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a / IPS4337ba28119d88135a8f3cca7f3a0a6d32a3e183e92e40aa3bfff84b2a45f1bb,491,536바이트. 3영역/10타일·CPU2,304사례179cycles·재빌드/실제 적용·6,005화면/637,476시점/실제6장면을 확인했다. 제한 종료와 의도한 mapper offset의 검증 모델 정정은 실패 자료를 남겼다. [변경 파일·해시·명령·검증 분리·한계](TRAIN_SIGN_KOREAN.md). 다음 작업 하나: 무입력attract/native root9의 실제 문자 소비·등록 원천 폐쇄 조사. 계속한다.


## 작업52 조사

[변경 파일·해시·재현·검증 종류·한계·다음 작업](ENGINE_CLOSURE.md). ROM/SSOT 변경0. 자동시연18,000+진단엔진12,000프레임/1,027화면/8,216 CHR조각, 등록 고유본문46개 호출 증거. 마지막 엔진의3 RAM seed는 정상 클리어가 아니다. 다음 작업은043 성 일반50/49 분기 검증이다.


## 작업53 실제 성 HUD 범위 정정

[변경 파일·해시·재현·검증 종류·한계·다음 작업](CASTLE_CURRENCY_QA.md). 현재043/SSOT 변경0. native일반50→0허용/49보존거절, 추가A4100 뒤 root4/phase5/course4 실제 성 플레이. 1,834화면/11,054파일. 실제 HUD 획 잘림 발견, 다음 작업54는 소비 추적/수정. 최종배포 보류하며 중단 없이 수정한다.


## 작업54 실제 성 HUD 검증

[파일·해시·재현·검증 종류·한계·다음 작업](CASTLE_HUD_QA.md). 실제 성 플레이293화면/6항목349,256픽셀·숫자618,816픽셀/146,750 IRQ시점 PASS, ROM/SSOT 수정0. 작업53 획잘림은 육안 의심으로 정정하고 원문/증거 보존. 다음은ROM없는043 개발판 패키지/실제Windows apply 검증이다.


## 작업55 ROM없는 개발판 패키지

[파일·해시·명령·검증 종류·한계·다음 작업](REVIEW_PACKAGE.md).11파일ROM없는검토용개발판,한글/공백 경로actualWindows8검사+최종ZIP적용PASS.43/SSOT그대로, 최종distribution_eligible=false/외부게시없음.다음은54원천/그림UI명칭·보존결정의사람검토자료정리.


## 작업56 검토자료/표시 검증

[파일·해시·재현·검증 종류·한계·다음 작업](TRANSLATION_REVIEW_KIT.md).54원천/29그림UI/실제9PNG·5파일ROM없는검토ZIP,desktop/mobile폭/검색/펼침/3원문영문크레딧PASS.최종사람검토pending·ROM/SSOT그대로·카페작업기아님.다음57은새부팅/놀이기구후reset·무세이브장기경로이다.


## 작업57 reset·장기경로 범위

[파일·해시·명령·검증 종류·한계·다음 작업](RESET_LONG_WORLD_QA.md).435reset쌍/342전체동일·93HUD glyph/숫자정확,네18k controller루트완료지만클리어없음.합계3,873PNG/30,984CHR조각/23,294runtime파일.ROM/SSOT그대로·55/56동결.다음58같은043 세이브상태왕복을검증한다.


## 작업58 저장 상태 검증

[파일·해시·재현·분리된 검증·한계](SAVESTATE_ROUNDTRIP_QA.md).826키 중 정상 OPLL refresh9개만 정확한 소스로 설명했고 RAM/PPU/OAM 및 복원 후3장면은byteexact다. ROM/SSOT 변경0. 다음 하나: 원본/043 오디오 레지스터 쓰기를 같은 입력으로 비교하며 계속한다.


## 작업59 — 오디오 레지스터 비교/미해결 위상 차이

[변경 파일·해시·재현·검증·실패·한계](AUDIO_REGISTER_QA.md).4경로88,164쌍의 값·순서·프레임이 같다.3경로 APU 전부 같으나 급류157상태는 다르고 최대8cycle 차이가 있다. 실제 청음/PCM은 미수행. ROM/SSOT 변경0. 다음 하나: 급류 복귀 첫 APU 차이를CPU/APU 갱신 소스·이벤트와 연결한다.


## 작업60 — 첫급류APU차이 관찰모델 검증

[파일·해시·재현·소스/실행/한계/실패](APU_OBSERVATION_QA.md).11개동기화관찰의출력값은같고7개무음DMCtimer/bit만다르다. 자기기준audio/world/RAM/PPU/OAM은같다.5PNG차이는peek전이며별도보존했다. ROM수정근거로해석하지않고043/SSOT변경0. 다음하나: 나머지급류9,000프레임관찰을동기화한다.


## 작업61 — APU 동기화 확대/출력위상차이 기록

[파일·SHA·재현·검증·한계](APU_EXTENDED_QA.md).기존157차이를161관찰로동기화했고146관찰의출력위상도다르다. 음악/효과음엔진24KiB와오디오쓰기값/순서/프레임은보존됐다. 실제PCM/청음은미수행이며ROM/SSOT변경0. 다음하나:새식별명/초기PCM-CDL0인실행에서DMC읽기바이트를연결한다.


## 작업62 — DMC 읽기 소비바이트 보존

[파일·SHA·재현·정적/runtime/실패/한계](DMC_CONSUMER_QA.md).새PCM-CDL0인두4,200프레임실행에서59,247read쌍과1,729바이트가같다. 최초V1 관찰비용timeout을보존했다. ROM/SSOT변경0,출력위상/청음한계는유지한다. 다음하나: 카트의실제조작소비기를연결해controller-only자연클리어에접근한다.


## 작업63 — 실제카트 입력/좌표소비기

[파일·SHA·명령·검증·실패·정정·한계](CART_CONTROL_SURVEY.md).held52/edge50의실제bank38 소비기와좌표저장3,519건을연결했다. native체력3→2 사망/재시작이관측됐지만클리어는없다. ROM/SSOT변경0. 다음하나:실제객체좌표로controller-only 추적policy를실행한다.


## 작업64 — 카트18k 추적입력/클리어미도달

[파일·SHA·재현·검증·한계](CART_PURSUIT_ATTEMPT.md).762PNG/4,582runtime파일/17,999정책행/6,096CHR조각을검증했다. native클리어는없고체력1/Gold·history0이다. A충전/해제후velocity추가소스를확인했다. ROM/SSOT변경0. 다음하나: B없이A충전/해제policy를실행하고실제충전/속도를기록한다.


## 작업65 — A충전·해제 관찰 / 자연클리어 미도달

[파일·SHA·재현·검증·한계](CART_CHARGE_ATTEMPT.md). 충전1024→해제0과 실제가속을 관측했다.18k 끝에 체력0/history·Gold0이며 자연보너스는 없다. ROM/SSOT 변경0. 다음 하나: 카트 충돌·구멍·남은 적의 실제 소비기를 추적한다.


## 작업66 — 카트 구멍 소비기/좌표 연결

[파일·SHA·재현·실패/정정·검증·한계](CART_GEOMETRY_SURVEY.md).12,105 실제tile 질의가원본CPU소비기와일치했다. level0 구멍중심128/256과native4점낙하검사를연결했다. 최종적제거/클리어는미해결이며ROM/SSOT변경0. 다음하나:구멍반대편 접근/회피·관성제어controller-policy를시험한다.


## 작업67 — 지형·관성 정책 / 생존 유지·클리어 미도달

[파일·SHA·재현·실패/정정·검증·한계](CART_GEOMETRY_POLICY_ATTEMPT.md).18k native플레이의체력3을유지했으나두적이남고Gold/history0이다. 최초Lua compile실패보존/V2실행검증. ROM/SSOT변경0. 다음하나:앞선낙하경로의적state4→제거소비기를추적한다.


## 작업68 — 적 카트 낙하·제거 실제 코드 연결

[파일·SHA·재현·검증·한계](CART_ENEMY_CONSUMER_SURVEY.md).4033 state4→4065 996B/AE3F 타입/활성/좌표clear를연결했다.3,451쓰기·4,520실행주소·2,898 corememory보존 확인. 한적제거는확인했으나클리어는없다. ROM/SSOT변경0. 다음하나:9540 남은적분기/state5 후속stage소비기를검증한다.


## 작업69 — 남은적/구간 완료 원본CPU 검증

[파일·SHA·재현·실패/정정·검증·한계](CART_CLEAR_BRANCH_SURVEY.md).500분기·3전환·6대기사례와두inlinepointer표를검증했다. 세구간완료후phase14(hex)이며자연완주는아니다. ROM/SSOT변경0. 다음하나:구간별지형/완전충전·예측입력으로실제구간전환시험.


## 작업70 — 카트 첫 구간 자연클리어

[파일·SHA·재현·V1차이/V2검증·한계](CART_NATURAL_ROUND_QA.md).V2 첫4200 mask동일,4970 level0→1/phase0E 실제전환·체력3. 최종Gold/history/3구간완료는없다.34,470고유query원본CPU일치. ROM/SSOT변경0. 다음하나:경로선분검사와확장실행으로나머지구간시험.


## 작업71 — 좌표축 정정/첫 구간재현/두번째구간timeout

[파일·SHA·재현·정정·검증·한계](CART_AXIS_RUNTIME_QA.md).40속도사례·실제right30프레임Y+15로축대응을정정했다. first4969 mask동일/4970 level1·체력3, 마지막적남기고시간00→홈.1362PNG/70737query 검증. ROM/SSOT변경0. 다음하나:8픽셀경로와native15/10 body probe로재시도.


## 작업72 — 8픽셀 몸체 경로 / 최종클리어 미도달

[파일·SHA·재현·검증·한계](CART_BODY_PATH_QA.md).58,365 bodyprobe 정적검증과36k/71,068 actualquery확인. 첫구간재현,두번째구간time00→홈·체력3/Goldhistory0. ROM/SSOT변경0. 다음하나:원본2F 이동·속도와B 감속조건을비교한다.


## 작업73 — 새 영문 안내 소비기/추출

[파일·해시·재현·실패·단위정정·검증·다음 작업](NOTICE_CONSUMER_SURVEY.md). ROM/SSOT변경0. 실제 CHR62/두 생산자/28타일을 연결했다. 다음 하나: 한글 안내 삽입 빌드044.


## 작업74 — 두 안내 한글화 / 빌드044

[파일·SHA·재현·검증·한계](NOTICES_KOREAN.md). 새CHR220/생산자2상수,512 CPU사례·실제진단604스냅숏·75,776PPU행·재빌드/IPS적용 통과. 현재044, 다음 하나: 자연20k 경로에서 안내/홈 전환 확인.


## 작업75 — 두 안내 자연 경로 검증

[파일·SHA·재현·실패·검증·한계](NOTICES_NATURAL_QA.md). controller-only20k/19,999입력행·666world행 기존043 동일,829PNG/6,632CHR조각 검증. 직접 다음라운드/시간초과/홈 확인. 전체클리어는 아님. 다음 하나:128CHR의8×16 그림/UI 목록 재검토.


## 작업76 — 실제 START! 누락/소비기

[파일·해시·재현·단위/범위·검증·한계](START_CONSUMER_SURVEY.md). START122/123 actual2670/3,072RGB/48타일 연결. 기존116..121 미관측검사와 구분. 다음 하나:‘시작!’ 빌드045.


## 작업77 — ‘시작!’ 한글화 / 045

[파일·SHA·재현·정적/적용/runtime/직접검증·한계](START_KOREAN.md). CPU1024사례/19cycles·재빌드/적용·자연20k/829PNG검증. 현재045. 다음하나:다른3놀이기구 공통시작 회귀.


## 작업78 — 다른세놀이기구 시작 회귀

[파일·SHA·재현·검증·새누락·한계](START_SHARED_QA.md). 3쌍1,704PNG/045의6,816CHR조각검증,직접6장면확인. 기차 STOP 영문표지를발견했다. 다음하나:STOP 실제소비기·PNG추출.


## 작업79 — STOP 실제배경 소비/PNG

[파일·SHA·재현·후보기각·검증·한계](STOP_CONSUMER_SURVEY.md). CHR68/69/NT2800/768RGB·20,560PPU행/단일font표값연결. 다음하나:‘정지’ 세로글꼴046.


## 작업80 — 정지 표지 /046

[파일·SHA·재현·CPU모델범위·실패·검증·한계](STOP_KOREAN.md). 046표지글자만변환/재빌드·IPS적용·20,560livePPU행/2,395정확pixel통과. 현재046, 다음하나:다른3코스CHR확장회귀.


## 작업81 — 046 다른코스 보존

[파일·SHA·재현·검증·한계](STOP_SHARED_QA.md). 852PNG/4260PNG·RAM·OAM·PPU·mapping파일이045동일, 직접3플레이화면확인. 다음하나:현재046 사람검토키트새버전.


## 작업82 — 빌드046 검토 자료 갱신

[상세 인계](TRANSLATION_REVIEW_046.md). 본문54/그림33/실제PNG13, 5파일 ROM 없는 ZIP과 desktop/mobile 렌더 PASS. 과거 촬영043/045와 새046 화면의 근거를 구분했다. 기존 번역·ROM·원본 변경 없음, 사람 검토 pending. 다음 작업 하나:046 검토 패치 묶음의 실제 Windows 적용과 ZIP 재적용.


## 작업83 — 빌드046 검토 패치 적용 검증

[상세 인계](REVIEW_PACKAGE_046.md). ROM 없는11파일 ZIP, 실제 Windows 적용8개 검사와 ZIP 추출 재적용 PASS. 원본/기존 번역/046 변경 없음. 최초 상태 이름 가정 실패와 v2 해결 기록. 최종 사람 검토 및 공개 적격은 false. 다음 작업 하나: CHR61 POW 후보의 실제 소비 조사.


## 작업84 — POW 후보 소비 조사

[상세 인계](POW_CONSUMER_SURVEY.md). bank61 선택 코드 실행은 확인했으나 메뉴/롤러코스터 제한 구간의 글자 소비는 미관측. 새 runtime과 기존046 총2095파일 byte exact, ROM/CSV 변경 없음. 전역 미사용이나 번역 완료를 주장하지 않는다. 다음 작업 하나:046 정지 표지의 reset/save-state 회귀.


## 작업85 — 현재046 저장 상태/리셋 검증

[상세 인계](STATE046_REGRESSION.md). 같은046 기차 top 저장/복원 RAM/PPU/OAM과 전용224/225 byte exact,826키 중 소스에서 요구한OPLL9개 외 일치. Mesen binary 저장의 APU EndFrame 영향을 v1/v2로 확인·정정. 리셋 후 시작!/정지 및 기차 재진입 PASS.046/CSV 변경 없음. 다음 작업 하나:2F 적 속도와 기존 B 감속 가설의 소비 검증.


## 작업86 — 2F 적 속도 생산자와 B 가설

[상세 인계](CART_2F_SPEED_SURVEY.md). 로컬CPU2592/실제48가속·8방향 정확, 기존045와2475파일 byte exact. 고정2.8속도 가설은 기각,2.5초과 가능과 과거target B1592행 확인. ROM/CSV 변경 없음.10k/과거20k 범위 가정 실패와v2 해결 보존. 다음 작업 하나:2F intercept 자동B만 제거한 V5 controller 실험.


## 작업87 — 2F 자동 B 제거 실험 실패 보존

[상세 인계](CART_2F_BRAKE_ATTEMPT.md).2F intercept3987행 자동B 제거/첫차이14317, prefix3195파일 exact. 첫 구간 재현/두번째2F 시간 초과·홈, 전체 클리어 미달.새 ROM/CSV 변경 없음.다음 작업 하나:2F–플레이어 충돌의native속도 교환과 추가 밀기 분기 관측.


## 작업88 — 2F/플레이어 충돌 소비

[상세 인계](CART_COLLISION_CONSUMER.md).206쌍 전체RAM/CPU 속도교환 exact, 추가 작은속도분기8회,105개 역방향 전달 관측. V5와4140파일·19999입력행 exact.87의runtime8184/manifest8190 구분 정정,원본/ROM/CSV 변경 없음.다음 작업 하나:접근각과 native 방향벡터로A해제를 맞추는V6 실험.


## 작업89 — 방향 정렬 A 해제 실험 실패 보존

[상세 인계](CART_ALIGNED_RELEASE_ATTEMPT.md).20개 조건부burst/24개eligible 로그검증, prefix3395파일 exact. 두번째2F 시간초과·홈, 전체완주 미달.추가자동입력 반복을중단하고 번역문맥검토로복귀. ROM/CSV 변경 없음.다음 작업 하나:원문54/그림33 수동대조와 필요한 한 항목의 재현 가능한 수정.


## 작업90 — 수동 원문 대조/성 입구 후보047

[상세 인계](GATE_EDITORIAL_BUILD.md).54원천/33그림 수동검토, MAIN_057C1 한 문장만 자연스럽게 수정·CSV백업. 후보047129바이트/전용175176만 변경,960ABI/39reader/IRQ/ExpectedWrites/독립재빌드8파일/실제IPS 적용PASS. Runtime미수행으로채택본046유지.다음 작업 하나:046/047 성 입구 동시점 출력·넘김·폰트수명 실제검증.


## 작업91 — 성 입구047 실제 출력 검증과 채택

[상세 인계](GATE_EDITORIAL_QA.md).046/047 각5400frames controller-only,396표본 중36대사두행만차이/360전체일치.37폰트PPU/2889메뉴로그/게임RAM nativeglyph쌍과4stackA검증PASS. 실제부분·완성·넘김·다음대사 직접확인,047채택.90재빌드9개 정정/v1검증기경로실패와v2보존. 자연골드4획득/전체완주/047state·reset/사람최종미수행. 다음 작업 하나:047 사람검토HTML/ZIP 및모바일렌더링 갱신.


## 작업92 — 현재047 사람 검토자료

[상세 인계](TRANSLATION_REVIEW_047.md).본문54/그림33/실제14사진/5파일 ROM-free ZIP, 한문장 최신CSV 반영.1280/390 렌더·검색·원문크레딧·현재성입구 DOM PASS, 직접PNG 확인. v1/v2 파일쓰기 전스키마 가정 실패 및v3 해결 보존. 최종사람검토 미완료. 다음 작업 하나:047 xdelta 검토패키지/Windows8적용검사/ZIP재적용.


## 작업93 — 현재047 검토 패치 묶음

[상세 인계](REVIEW_PACKAGE_047.md).ROM-free11파일 xdelta ZIP/Windows apply.cmd8실제검사/최종ZIP재적용047 whole-ROM exact. 도구라이선스·원본·1편·CSV 보존, v1과거상수변경 guard 실패/v2 해결 기록. 정식배포자격false/최종사람검토미완료. 다음 작업 하나:047 골드4·일반50·49 seed분기 회귀와성HUD 확인.


## 작업94 — 현재047 통화seed 입장 회귀

[상세 인계](GATE047_BRANCH_REGRESSION.md).골드4/일반50·49 각046/047 6실행,2096표본쌍 중108대사두행만변경/1988전체같음. 통화seed명시/50차감·49보존·골드4허용, 성실제플레이768표본 전체RAM/PPU/PNG exact 및HUD직접확인. 새ROM없음.다음 작업 하나:047 성입구저장·불러오기/리셋후175176문구회귀.


## 작업95 — 현재047 성 입구 상태/리셋

[상세 인계](STATE047_GATE_REGRESSION.md).같은047 top1920저장/2190불러오기 RAM·PPU·OAM/175176 exact,826키 중sourceOPLL9개외exact. binarycreate전후APU11차이구분. postload현재047기준15파일exact/리셋3000→실제3001/문장재진입RGB4920·6000 PASS.570PNG/4560CHR chunk확인, 새ROM없음.다음 작업 하나:POW61 실제sprite데이터·호출조건 역추적.


## 작업96 — POW 스프라이트 공급 정적조사

[상세 인계](POW_METASPRITE_SUPPLY.md).bank61지정3motif/RAM38→D000 native274cycle, 잠재common191/1910CPU source047 OAM·cycle exact.7descriptor별도해석 exact/정적POW회전후보·깃발3E구분, 실제POW소비는미연결. 과거RAM조건0관측은전역미사용증명아님. 새ROM없음.다음 작업 하나:047 게임오버깃발positive control 실제소비와POW producer추적.


## 작업97 — source61 깃발 positive control

[상세 인계](BANK61_POSITIVE_CONTROL.md).047 baseline/probe8000frames/606PNG·3682native파일 exact. frame3E→0405→9643→OAM83→actualCHR0F420의805프레임,PPU51520행/27실제RGB exact.동반blank와깃발/POW타일구분,POW실제소비미연결. 초깃값티켓4seed명시,새ROM없음.다음 작업 하나:RAM38 direct/computed bank writer와POW 조건역추적.


## 작업98 — bank38 writer/불꽃 후보 구분

[상세 인계](POW_BANK_WRITER_BOUNDS.md).direct15고정값/61은3site,source04730CPU slice exact.마지막장면bank54 constructor/9D..A2counter144case exact로잘못된bank61 POW가설배제.정적설명그림재현byte exact,새ROM없음/전역미사용아님.다음 작업 하나:HOWTO116117/PAUSE120121 bankproducer·nativeNT역추적.


## 작업99 — HOWTO 뱅크와 안내 NT

[상세 인계](HOWTO_BANK_NT_BOUNDS.md).literal bank35 12곳/24 CPU slice와3표 범위, selector10 NT1024셀/128 source047 decoder쌍을 검사했다.116은 장식267셀에 쓰이며 HOWTO90..96은 그NT/역사033 표본에 없다.047 원본후보 보존, 전역미사용 아님. v1..v4 guard실패와 v5해결 보존. 다음 작업 하나:현재047 동일입력 baseline/probe에서bank35·top·label pattern읽기와장식positive control을 연결한다.


## 작업100 — 현재047 HOWTO 장식 positive control

[상세 인계](HOWTO_CURRENT047_QA.md).controller-only baseline/probe4200frames 각각/1658파일·275전체화면 exact. bank35=116→top1060표본·장식tile81 실제읽기16896행/1056프레임·35 sourceRGB exact, label90..96은관측0.뱅크전체미사용아님. fade2표본v1 guard실패/v2해결 보존. 다음 작업 하나:PAUSE120121 나머지CHR shadow 공급/코드·데이터motif 구분.


## 작업101 — PAUSE 공급의 정적 경계

[상세 인계](PAUSE_SUPPLY_BOUNDS.md).rawCHR shadow motif190/인접immediate166에119120121 없음, source고정IRQ7/current고정6그룹 CPU와포트검사. 현재LDXC6 hook은동적소비로구분/v1실패보존.간접animation bank36 공급두곳은미해결,전역미사용아님. 다음 작업 하나:native803C/9362 player/action table과bank36 descriptor값/경계 검증.


## 작업102 — animation bank36 간접표 경계

[상세 인계](ANIMATION_BANK36_BOUNDS.md).bank38의803C 2표×4쌍은font8/9/24,9362 변신2표×7record는12/13/14. native전환42포함source04780 CPU조건쌍/전체RAM·cycles exact.이표PAUSE공급없음/다른창9417구분/전역미사용아님. 다음 작업 하나:sourceC6/C7 IRQ폰트래치 producer와값범위 추적.


## 작업103 — IRQ 폰트 래치 공급

[상세 인계](IRQ_FONT_LATCH_BOUNDS.md).C6/C7 raw5 motif의native2/data2/JMP경계1구분,profile4 producer/source047검사.등록48page×인위prior4=192 init유효font,IRQ96조건쌍52cycles/포트시점동일.legacy003표값v1실패/v2수정보존.해당경로PAUSE공급없음/전역미사용아님. 다음 작업 하나:047 HOWTO/PAUSE/POW 소비근거·미해결범위 ROM없는별도검토보충자료.


## 작업104 — 047 그림 소비 검토 보충자료

[상세 인계](CONSUMER_REVIEW_047_SUPPLEMENT.md).HOWTO/PAUSE/POW3후보·6이미지(현재0472/과거0421/정적3)/ROM없는5파일 ZIP.1280/390렌더·8PNG·실제합성JSON다운로드PASS/JS0,3결정pending·사람승인false. 기존047키트/패치보존. 다음 작업 하나:현재45초안의원문/control/실제문맥대조와단일수정필요여부검토.


## 작업105 — 본문 원문/slot 문맥 검토

[상세 인계](NATIVE_CONTEXT_REVIEW_047.md).원본54raw/48pointer/46main/45개개별수동메모·변수3 placeholder순서검사.57AC는booth15/5920는ride2A로정확한문맥원장정정,ROM/CSV그대로/사람승인false.본검토prose필수수정없음/문체·명칭검토pending. 다음 작업 하나:047 normal3 부족분기 actualFA/F8 숫자·이어가기문맥검증.


## 작업106 — 일반 티켓3 부족 분기 완료 및 사용자 지시로 종료

- 요청/목표: 이미 시작한 실행 결과를 정리하고 “여기까지 마무리 하자”에 따라 작업을 종료한다. 자동 재개하지 않는다.
- 기준: 현재047 ROM/CSV 유지, 원본·1편 보존. 원본/046/047/CSV SHA와 변경 파일별 SHA는 아래 상세문서/동결 manifest에 기록했다.
- 완료:046/047 각4200프레임, 공통1820파일/302전체PNG exact. stdout3CRC32 줄만 ROM 차이를 반영한다. 초기1000프레임의 일반티켓3 seed 명시. actual047 요금4→거절→보유3 확인,4200에서도 티켓3/보유대사이며 입장완료는 아니다.
- 변경 파일: 종료 상세문서, close_context106 v1/v2, 실패관찰/통과보고서, 두 실행QA 폴더, manifest/감사보고서. README/조사/계획/journal/날짜인계와 canonical HANDOFF 갱신. 원본/ROM/CSV는 변경하지 않았다.
- 정적: 캡처/도구/설정/입력/seed와 보호파일 SHA, PPU2KiB glyph/NT 실제코드 일치. 최종 원본/1편/문서링크 감사 결과는 session 보고서로 보존한다.
- 빌드/적용: 새 빌드/적용 없음. 기존 검증047 패키지 보존.
- 실행: 이미 시작한 통제 seed 두 회 exit0. 종료 지시 후 새 실행/CPU replay 없음.
- 직접 장면: 현재047 1800/2100/2700 실제PNG3장 assistant 확인. 독립RGB 재구성과 최종 사람승인은 미수행.
- 실패: 정리기v1 예상 리터럴의 PowerShell 인코딩 손실 guard 실패를 보존하고 UTF8 v2로 해결. 게임/캡처 오류가 아니다.
- 미해결: 사람 문체/명칭/그림 검토, 남은 소비경로, 전역corpus/자연전체3구간 완주/청음/실기/정식배포. 우선순위 질문은 미응답 보류.
- 작업기: 근거journal 보존, 전체 완료 후 카페 작업기 작성 요청 유지. 완성 작업기/외부게시 없음.
- 다음 작업 하나: 사용자 재개 지시 후047 성공입장 뒤 slot2A 출발 대사와 문맥원장 대조. 현재 실행하지 않는다.

[상세 결과·해시·재현](NORMAL3_CURRENT047_CLOSEOUT.md), [동결 manifest](../manifests/context106_assets.json), `qa/reports/context106_session.json` 종료 감사.


## 작업107 — 현재047 출발 대사와 성공 입장

2026-10-06 재개 지시를 반영했다. 초기 티켓4 seed 명시 후 실제4→0차감, slot2A/9910/font196의 “출발!”과 root4/phase5 플레이 진입을 확인했다. 원본·1편·047 ROM/CSV 보존. 각4200프레임 기본/probe는 공통1820파일/302전체PNG exact, mapped CHR2416조각 exact, 완성NT/RGB53캡처 exact. 실제5PNG assistant 확인/최종 사람승인은 아니다. 페이드색·PNG 이전 필터프레임·2634 latch reset 경계의 검증기 실패4건은 보존/v5해결. 새 빌드/패치 적용 없음. 자연전게임/전역corpus/실기/청음/최종검토는 미완료다.

다음 작업 하나: 현재047 본문·그림·소비경로·자연플레이 미완료 범위를 기존 동결 증거로 정리하고 다음 기술 조사 한 건을 선택한다. 중단 지시가 없으면 이어간다.

[상세 결과·해시·재현](RIDE_SUCCESS_CURRENT047.md).


## 작업108 — 현재047 완료 범위 원장

등록54=45초안+9기술공유, 그림검토33, nativeNT20(selector00..26hex)로서 서로 다른분모임을기록했다. macro원본/현재정의·등록소비와NT원본20SHA/계획SHA/047검토문구일치확인, 기존보고13개와미완료조건8종을연결했다. 전체완료율null/사람승인·전역corpus·자연완주·release_eligiblefalse. 원본/1편/047ROM·CSV보존, 새runtime/CPU/build/apply/직접장면없음. v1문법실패/v2해결보존.

다음 작업 하나: nativeNT20개(selector00..26hex)의실제NT호출/font근거를대조해미연결selector부터누락문구/그림여부판별. 중단지시가없으면이어간다.

[상세범위·변경파일·SHA·재현·검증과한계](SCOPE047_RECONCILIATION.md).


## 작업109 — nativeNT20과8025 관측 범위

원본20stream의pointer/encodedSHA/decode종료·셀수를확인했다. 기존97환경중정상95의1829개정확한8025호출은15selector에연결되며비정상종료2는이분모에서제외/이유보존. 미관측0E/26은별도매표소literal/보너스CHRcopy실제소비가이미있고,14/16은source RAM79>=6 producer쌍,1C는간접공급미폐쇄다. source단순ASCII/호출부재를미사용판단으로삼지않는다. 원본/1편/047/CSV보존, 새runtime/CPU/build/apply/sceneQA없음, v1BCCbyte guard실패/v2해결보존.

다음 작업 하나: fixedD347 RAM79 생산자/호출자와NT14/16의조건부stage진행문맥을역추적한다. 계속진행한다.

[상세근거·해시·재현·검증분류·한계](NT_SOURCE_CONSUMER_047.md).


## 작업110 — 성 배경 조건과 STAGE SELECT 후보

원본/047의8구간이 같고 RAM79 분기512건·일반 stage clear/skip512건 CPU 대조를 통과했다. 성 phase7→bank30/969C의 A5=35 레코드가 방6→NT14/16 조건에 연결된다. 기존047 실제 성 플레이768개 RAM 표본은 모두 방0으로, 방6 실제 화면 증거가 아니다. root3 inline target은 CD49/CD73/CE37이며 STAGE SELECT 초기화 CD52는 일반 phase0에서 건너뛴다. 문자열은 별도 진단 후보로 남겨 전역 미사용/완료 범위 제외를 확정하지 않았다. 원본·1편·047·CSV 보존, 새 runtime/build/apply/직접 장면 없음.

다음 작업 하나: 성 입장 후 A5=35/phase54=7을 명시적으로 주입하는 native 방 전환 진단으로 NT14/16→CHR/실제 표시를 연결한다. 자연 진행과 구분하고 계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](CASTLE_BACKGROUND_STAGE_ANALYSIS.md).


## 작업111 — 성 방6 native NT14/16 실제 소비

원본/047 각4800프레임의 초기gold4+4000프레임 A5=35/54=7 진단으로 실제 F5F8→969C→방6→8025/NT14·16/font118을 확인했다. 원본NT2048셀 정확한copy, 각3920회 실제CHR118/119읽기 집계동일,107캡처 NT전체/기존HUD밖RGB동일,각mappedCHR856조각 ROM동일. 현재047 개입전2742파일은작업94와exact. 실제2PNG직접확인,원본·1편·047·CSV보존,자연방진행/성완주/사람승인은아니다. preflight입력한계실패보존/4800전용입력해결.

다음 작업 하나: native8025의 원본 call site와 계산 selector 공급 범위를 조사해 NT1C 소비를 추적한다. 단순 immediate motif 부재를 미사용 판정으로 삼지 않고 계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](CASTLE_ROOM6_NATIVE_QA.md).


## 작업112 — native NT selector 공급 경계

직접JSR8025의10지점·두RAM공급caller·도입literal진입·clear 경로를대조했다. 명명한19selector 공급에1C는없고06D0의다른프레임counter를selector호출과혼동하지않는다. sourceNT20의8025관측17/기존별도소비2/미연결1개. 전역미사용·전체완료증명이아니다. ROM/CSV보존,새CPU/runtime/build/apply/장면검토없음.

다음 작업 하나: native8113의 별도 비압축 command 표와 실제 literal 입력을 전개해 STAGE SELECT/팔레트-only 별칭을 구분하고 새 문구 소비 여부를 조사한다. 계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](NT_SELECTOR_SUPPLIER_BOUNDS.md).


## 작업113 — native8113 command catalog와 진단 후보

12pointer slot/5고유pointer의palette·빈tail·NT진단문구·codeprefix를분리했다. source/current코드·표·데이터같음,48CPU queue사례모델exact. 추가문구는일반root3에서건너뛰는STAGE SELECT 후보이며스테이지 선택초안/raw/address를별도원장에보존했다. 실제font/진입미연결·build/human eligibilityfalse,54본문·33그림분모불변. ROM/CSV보존,새runtime/build/apply/장면없음.

다음 작업 하나: 카트3구간완료조건과이전2Fbot 실패를source/collision기록에대조해새진행근거를얻는다. 같은bot의근거없는재실행없이계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](NATIVE_COMMAND_PRINTER_CATALOG.md).


## 작업114 — 카트 접촉 순간 가설과88 방향 계산 정정

source/046/047 카트bank38..3B32KiB같음/nativeclassifier9사례로level1hole중심224,464를확인했다.88의잘못된128,256 내적을정정해206충돌중양수91/음수106/0은9,77개별부호변화·순합계1변화를기록했다. V6 A해제20시작의실제속도구멍쪽8/반대10/0은2,16프레임창의두축24미만근접표본있는창5/없는창15. 실제collision증명이아니므로읽기전용native관측으로확인할새근거다. 보고v1메타문구오류/v2정정 보존,ROM/CSV보존,새runtime/build/apply/장면없음.

다음 작업 하나: 현재047에서V6그대로실행하고2F/player 실제충돌callback으로burst와전달속도를대조한다.89prefix검사,새winning정책없이계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](CART_CONTACT_MOMENT_ANALYSIS.md).


## 작업115 — 현재047 V6 실제충돌 읽기전용 관측

V6 전체byteprefix에관측만추가한047 20000프레임 실행: 기존89 입력19999/해제4763행·PNG/RAM/PPU/OAM/매핑4140파일같음.4543pair/4375거절/168실제swap의전체RAM·A CPU재생exact,2zero fallback. 실제속도구멍쪽77/반대88/0은3,20burst창안18충돌중11쪽/7반대. 접촉연속속도재교환·창중방향반전확인,첫구간만통과/전체3구간미달유지. ROM/CSV보존,game RAM/PC/state/시간·체력·금액쓰기없음,새build/apply/직접장면없음.

다음 작업 하나: burst 접촉18개의입력·기본방향·재충돌을시계열분리해단일방향유지수정여부를판정한다. 근거없는V6 재실행없이계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](CART_V6_CURRENT047_COLLISION.md).


## 작업116 — 카트 방향 유지 단일 실험 준비

실제20해제창중14창/84 input표본의방향변화를확인했다. 방향이같아도재충돌하는경우는별개다. V7후보는level>=1/2F기존16프레임창의시작방향만유지하고pit_avoid는동적유지한다.3정확한코드대체역변환이V6전체와동일,첫구간/충전/B/지형/ROM불변. 아직새실행/CPU/build/apply/장면없음,3구간미달유지.

다음 작업 하나: 현재047 V7controller-only36000프레임한번실행해방향override 전prefix와native진행/history/gold를검증한다. 같은실패재시도없이계속한다.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](CART_HEADING_HOLD_EXPERIMENT.md).


## 작업117 — V7 실제 실패와prefix PNG 예외 분리

현재047 V7 36000프레임: 첫16220방향차이/앞16219controller행같음/첫구간성공유지·두번째2F잔존시간초과홈,Gold/history0·3구간미달. 방향유지391표본/query71200·고유32139 CPUexact/CHR10896조각·8185runtimeSHA검증. prefix702raw/core상태exact,699PNG같고1281/2820/4320의3PNG예외보존(v1가정실패/v2범위분리). 직접18900/19500/24000확인:19500검정은홈증거아님,24000실제한글홈. ROM/CSV/gameRAM·시간·체력·금액불변,새build/apply없음. 유사winningbot 재시도stream은닫고다른독립조사를계속한다.

다음 작업 하나: pinnedMesen2.1.1 비동기decoder/screenshot 경로에3PNG예외를대조해캡처시간증거범위를정리한다. winningbot 반복없음.

[상세 결과·변경 파일·해시·재현·검증 구분·한계](CART_V7_CURRENT047_ATTEMPT.md).


## 작업118 — 캡처 프레임 증거 범위

공식 태그의 6소스 Git blob 일치, EndFrame 이후 현재 프레임 제출·비동기 디코딩·캡처 래퍼의 완료 대기 없음·필터 적용/복사 공통 잠금을 확인했다. 예외 3시점의 36파일 SHA와 raw/core 동일·RGB 차이 8/7028/10630을 재확인했다. 정확한 지연량/원인/찢어짐은 미확정이다. 기존107/111의 실제 비교 범위는 유지한다. ROM/CSV/설정 보존, 새 CPU/build/apply/runtime/직접 장면 검증 없음.

[상세 결과·변경 파일·해시·검증 구분·한계](CAPTURE_FRAME_BOUNDS.md).

다음 작업 하나: 기차 간판·HOW TO CONTROL·PAUSE 정적 후보의 CHR 페이지와 native 폰트 공급 코드를 대조해, 소비가 연결되지 않은 후보의 기술적 범위를 정리한다.


## 작업119 — 미연결 NT1C의 후보 타일 경계

미연결 NT1C 99바이트/1024셀을 native803F 디코더 D-clear128조건쌍으로 대조했다. 가정한HOWTO116/PAUSE120 background 배치의 후보 타일과교집합0이지만 실제font·consumer는미연결이다. 기존99..103과104 결정을확대하지않고pending유지. ROM/CSV보존,새runtime/build/apply/직접장면없음.

[상세 결과·변경 파일·해시·검증 구분·한계](NT1C_CANDIDATE_BOUNDS.md).

다음 작업 하나: native bank38의 A5C6→A5FD에서 CHR61과 actor ED를 설정하는 조건·호출 문맥을 연결해, POW 후보와 다른 실제 소비인지 구분한다.


## 작업120 — 강 후반 CHR61 공급

CHR61의세번째literal공급을강course3/bank38/A645→A5C6→A5FD로연결했다.5dispatch·4096constructor·3stageart조건쌍source/047동일.ED/EE/EF는별도course3표로9/2/1sprites이고원본정적그림을직접확인했다.실제후반소비·게임물체명/문구·POW와의동일성은미확정이다.ROM/CSV보존,새runtime/build/apply없음.v1 loadedROM동일가정실패를v2RAM범위로교정/보존.

[상세 결과·변경 파일·해시·검증 구분·한계](RIVER_BANK61_STAGE_SPRITES.md).

다음 작업 하나: 현재047과원본의강phase5에서nativeA5C6직전RAM69=0B/6D=F0만명시적으로주입하는진단으로ED/EE/EF의실제OAM·CHR61읽기·화면을연결한다. 자연후반진행·완주와구분한다.


## 작업121 — 강 후반 조건 실제 진단

원본/047각4000프레임에서nativeA5C6직전69=0B/6D=F0두조건만기록해주입했다.ED생성A5FD/A642각1회·native435행source/current동일이나ED/EE/EF조립·CHR61읽기0으로실제그림소비미연결.047개입전100시점은역사적046 raw400/core100/PNG100same.2실제PNG직접확인,ROM/CSV보존,build/apply없음;자연후반/완주아님.

[상세 결과·변경 파일·해시·검증 구분·한계](RIVER_NATIVE_DIAGNOSTIC_047.md).

다음 작업 하나: 현재047에서같은두조건진단에읽기전용actor2상태쓰기관측을추가해,ED생성후0422/0402를지우는정확한native명령·조건을찾는다. 위치·체력·시간·ROM추가조작없이기존121의동일시점RAM/PPU/OAM/매핑을대조한다.


## 작업122 — 강 actor2 소멸 원인

동일두조건진단+읽기전용write관측으로95BF의artclear및960F/9614→F204/F20C의stateclear를찾았다.121raw620/core155/PNG155·native434행같음.6쓰기CPU쌍/2projection쌍source-current같음.실제viewport차0126/0175가nativeculling을일으켰고합성viewport의64/144는아직표시예측이다.후검증파일명·EndFrame경계실패와문구정정은동결보존.ROM/CSV보존,build/apply/직접장면없음.

[상세 결과·변경 파일·해시·검증 구분·한계](RIVER_ACTOR2_CULL_047.md).

다음 작업 하나: source/current047에서같은native생성뒤9582/actor2투영직전viewport68=01/6B=40/69=0C/6D=80을한번명시적으로주입해,CPU모델의screen64/144예측과실제ED/EE/EF·CHR61소비를대조한다.진단카메라이며자연후반·완주로보고하지않는다.


## 작업123 — 강 ED 실제 소비

원본/047각3300프레임의두조건+viewport4필드한번진단으로ED9sprites/36BOAM→CHR61읽기128행/288회→실제PNG검정opaque518픽셀을연결했다.사람승인/자연후반아님.122좌표축라벨정정(X144/Y64).50캡처상단0..189같으나기존HUD제외비교는하단235/236차이로50모두실패/범위분리.ROM/CSV보존,새build/apply없음.

[상세 결과·변경 파일·해시·검증 구분·한계](RIVER_ED_ACTUAL_CONSUMER_047.md).

다음 작업 하나: 원본/현재047의같은진단에서화면하단235/236의실제PPUpattern읽기·매핑·NT/scroll을추적해,HUD밖차이를정확한소비에연결한다.ROM/CSV변경전에원인을확인한다.


## 작업124 — HUD 하단 두 줄의 배치 확인

원본/047각3300프레임의동일6필드진단+읽기전용render3032하단PPU1190행으로font124/206의공백20→다음NT빈00전이를확인했다.동일pattern340행의2scanline이동·독립RGB3584픽셀일치.기존040HUDy190..239/fineY2→0의의도된여백이동으로123의너무좁은190..217비교범위를설명했고ROM/CSV수정없음.자연전체/사람승인아님.

[상세 결과·변경 파일·해시·검증 구분·한계](HUD_FOOTER_SHIFT_047.md).

다음 작업 하나: 등록45본문초안을일본어원문·정확한장면105·현재삽입계획과수동대조해의미/용어/높임말을검토한다.실제수정이필요한문장만별도근거와함께선별하며사람최종승인을자동부여하지않는다.


## 작업125 — 본문 충실도와 단일 수정 선택

45초안 수동 재대조/9기술공유 분리, ordinary slot29만 원문 부족 안내에 맞춰 ‘아쉽지만 / 티켓이 부족해!’ 수정 후보로 선정. 공유196/197 변경 금지·예약226/227 전용폰트 계획. 원본/1편/047/CSV 보존, 사람 승인false, 새build/apply/runtime/장면없음.

[상세 파일·SHA·검토 근거·재현·한계](PROSE_FIDELITY_REVIEW_125.md).

다음 작업 하나: MAIN_0590C 한 문장만 별도226/227 폰트를 사용하는 새048 후보로 삽입하고 원본 쓰기 범위·native timing·재빌드/적용을 검증한다.


## 작업126 — 일반 티켓 부족 안내048 후보

MAIN0590C단일초안/전용226227/slot29tag만변경,047대비839B범위guard·1152page CPU·23reader·IRQ시간동일. 재빌드9파일/실제IPS 적용exact. v1누락guard실패보존/v2해결. 후보048/SSOT새문구이며채택047은아직유지. 원본/1편/이전산출물보존, 사람승인false, 새runtime/scene없음.

[상세 파일·SHA·재현·검증분류·한계](SHORTAGE_EDITORIAL_BUILD_048.md).

다음 작업 하나: 047/048을 동일한 일반티켓3 seed·입력으로 실행해 slot29의 부분출력·완성·넘김·다음2B 보유량 대사에서226→196 복귀와 보호화면을 검증한다.


## 작업127 —048 전환결함/거부

4200새실행·기존106047재사용/각1821SHA확인. 완성/복귀는정상이나2004·2604잔류문구fontmixing직접확인. 048거부/채택047,259PNG같음43다름/OAM302exact. source/CSV불변/새build없음, 사람승인false.

[상세 파일·SHA·재현·검증분류·한계](SHORTAGE048_LIFETIME_REJECTION.md).

다음 작업 하나: slot29/2B의 native clear 전에는 활성폰트를 유지하고06DF03 초기화 때 새폰트를 선택하는049 후보를 만들며 CPU경로별 사이클/ABI를 검증한다.


## 작업128 —049 clear후font선택후보

29/2B phase00active유지·phase03선택,3840page+16setupCPU/모든page추가38cycles·19주기배수. IRQ·CHR·본문그대로/재빌드11·실제IPS적용exact. idleRAM22효과/실제QA미검증, 후보049/채택047유지. 범위v1오류보존/v2해결.

[상세 파일·SHA·재현·검증분류·한계](LOWER_FONT_POST_CLEAR_049_BUILD.md).

다음 작업 하나: 049 실제부족3·성공4 입장과다른page경로를같은입력으로실행해 native clear 전후의글꼴수명·타이밍·의도밖픽셀/상태변화를검증한다.


## 작업129 —049 부족/성공 actual QA

새2회4200/106107047재사용. 부족preclear196/postclear226/다음preclear226/postclear196복귀·261PNG같음41둘째행수정만. 성공302전체PNG/PPU/OAMsame·4→0/출발/플레이. 직접7PNG. 604RAM22차이는38cycle 가중idle모델로대조(1B추론/직접telemetry아님),전체state동일주장금지. SPv1가정실패/v2해결,049다른pageQA전후보/047채택.

[상세 파일·SHA·재현·검증분류·한계](LOWER_FONT_POST_CLEAR_049_BRANCH_QA.md).

다음 작업 하나: 049의 타이틀/9도입문단·홈선택/매표소·성입구·크레딧을동결된각기준실행과대조해 global helper 회귀를검증한뒤개발채택여부를결정한다.


## 작업130 —global page회귀/개발049채택

새7실행·5짝1503전체PNG/PPU/OAM/매핑same·CHR12024조각. intro9font·gate·booth·credits3slot/native보호계약대조. 성16/tour1idleCPU PCmicrocycle/저장PC와RAM22등차이명시,전체CPU상태동일아님. 039tour19PPU차이는fresh047추가로이전빌드차이분리. 직접8실제PNG/사람승인false, 현재개발049채택·047/실패048보존. 자연전체/정식배포아님.

[상세 파일·SHA·재현·검증분류·한계](DEVELOPMENT049_PAGE_REGRESSION.md).

다음 작업 하나: 채택049의단일본문수정·새실제화면·검증한계를반영한ROM없는검토자료를새폴더에작성하고047자료는역사본으로보존한다.


## 작업131 — 현재049 검토자료 갱신

54원천/33문구/21실제PNG(역사14/현재0497), 단일수정과장면105/개입출처 반영. ROM없는5파일ZIP 바이트·SSOT54 일치,PC1280/모바일390표시·검색·직접3렌더 확인. 현재ROM/CSV/원본/1편 보존, 신규게임실행없음/사람승인false.

[상세 변경·SHA·검증 구분·재현·한계](TRANSLATION_REVIEW_049.md).

다음 작업 하나: 현재049 ROM 없는 개발 패치를 새 dist 폴더에 만들고 일본판 원본부터 Windows 적용8검사와 최종ZIP 재적용을 실행한다.


## 작업132 — 현재049 검토용 차분 패치

ROM없는11파일ZIP·한국어공백경로Windows apply8검사·최종ZIP추출재적용 모두049전체byte exact. v1상태상수가정 실패보존/v2해결. 원본/1편/047/049/CSV보존,신규게임실행없음/사람승인·정식배포false.

[상세 파일·SHA·검증 구분·재현·한계](REVIEW_PACKAGE_049.md).

다음 작업 하나: 현재049의 전용226/227 부족 대사 도중 같은 빌드 저장·복원과 console reset 후 재진입을 별도 실행해 글꼴 복귀와 native 출력 계약을 검증한다.


## 작업133 —049 전용226 저장·복원/리셋

FE53실제2100저장/2400복원·RAM/PPU/OAMexact·826키중OPLL9refresh만차이,복원후25기준파일exact/다음196복귀. reset2160/actual2161·native10→6입장/플레이·직접7PNG. v1미실행보존/v2완료guard해결. 원본/1편/ROM/CSV보존/사람false.

[상세 변경·SHA·검증 구분·재현·한계](STATE049_SHORTAGE_REGRESSION.md).

다음 작업 하나: 동일 입력047/049의 page 초기화 entry/return 실제 cycle과 RAM1B·IRQ 쓰기를 읽기 전용으로 기록해 추가38cycles와 idleRNG 추론 모델을 실측 대조한다.


## 작업134 —live page/counter/IRQ 범위

4회4200·22호출live1B가129추론과일치/각4200RAM22가중모델exact. 첫page실측42증가(순수38외4미분류),나머지20호출38. 성공143883쓰기전체동일/부족127206중폰트1198값변경과17쓰기1cycle앞당김. 신규scene/ROM없음/사람false. v1callback·검증가정실패보존/v2해결.

[상세 변경·SHA·검증구분·재현·한계](LIVE049_PAGE_TIMING_BOUNDS.md).

다음 작업 하나: 처음 홈 문단의 추가4실측cycles를 좁은924프레임 opcode·DMC cursor/read·새PCM-CDL과 순수CPU모델로 대조해 DMA인지 다른진행인지 구분한다. ROM수정전에 원인을 확인한다.


## 작업135 —첫홈DMC대기위치/134경계정정

자연960각2최종실행·62/80명령모델/RAMexact·362DMC읽기동일. 047RTS6→10/049STA4→8,같은C686/cycle27519253대기4. 실제9BBA반환까지211→249=38.134beforeRTS42는맞으나nominalRTS6추가해석정정. v1범위누락/UTF8읽기실패보존/v2해결. 원본/1편/ROM/CSV보존.

[상세 변경·SHA·검증구분·재현·한계](HOME049_DMC_WAIT_BOUNDARY.md).

다음 작업 하나: 부족3의2001프레임 IRQ17쓰기1cycle차이를 실제IRQ vector진입·저장PC·대기opcode/명령cycle과 연결해 handler내부변경인지 interrupt수락시점차이인지 구분한다. ROM변경없이 읽기전용관측으로 확인한다.


## 작업136 —부족IRQ진입전위상

각2400counter가134prefixexact/4IRQ씩532opcode순서·402순수/406실측동일.2001의19port는IRQbody전체와1cycle빠르며FE58대기opcode이미1cycle빠름·복귀FE5A/진입까지10same. 빠른handler/수락지연으로해석하지않고upstream3/4지연미분류.원본/1편/ROM/CSV불변/새scene없음.

[상세 파일·SHA·검증구분·재현·한계](SHORTAGE049_IRQ_ENTRY_BOUNDS.md).

다음 작업 하나: 1999..2002 대기opcode의3/4cycle 지연을 실제DMC cursor/read·새PCM-CDL로구분하고,2001의IRQ이전1cycle위상차이에기여한같은sample읽기를대조한다. ROM변경없이같은티켓3 입력을사용한다.


## 작업137 —idle/IRQ DMC 정렬

각2400의6trace가136byte exact/각257DMC바이트·cursor같음,4시각±2(각2)/PC34차이. idle204+IRQ4gap각DMC와연결·1114PCchain의1112개-1/2개-5는같은4wait가exec앞뒤로이동한일시차이. 패딩ROM수정없음/원본·1편·049·CSV보존. v1음수만가정실패보존/v2해결.

[상세 변경·SHA·검증구분·재현·한계](SHORTAGE049_IDLE_DMC_ALIGNMENT.md).

다음 작업 하나: 현재049의동결실행들을54원천별로연결한coverage원장을만들어 실제읽기/폰트·부분출력/완성·과거증거/현재증거/미실행을구분하고,남은등록본문검증의정확한한경로를선택한다.


## 작업138 — 등록54원천 현재/역사 검증 원장

현재init+font15/init12/font9,역사init3/선택실행미연결7/macro별도reader8. 초기화와실제읽기·완성을구분했으며global unused/완료율로해석하지않는다. 원본/1편/049/CSV불변·새runtime없음.

[상세 변경·SHA·검증구분·재현·한계](COVERAGE049_REGISTERED_SOURCES.md).

다음 작업 하나: 현재049를094의동결 gold4 입력·초기seed·관측기로9000프레임 실행하고, 과거047과대조해 slot1C/상단22·28/하단2A의출력·폰트수명을확인한다.


## 작업139 — 현재049 gold4 성 입장

9000프레임/786wholePNG·PPU·OAM·mapping exact/6288CHR chunks. slot1C완성NT/22·28·2A수명/성진입475스냅샷확인·직접4PNG검토. helper25writePCrelocation명령바이트확인/RNG·stack·bus차이유지. 검증가정v1/v2실패보존/v3해결·ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](CASTLE049_GOLD4_BRANCH.md).

다음 작업 하나: 094 normal50의동결 입력/초기seed/관측기로현재049 성 입장을9000프레임실행해,일반티켓50→0 교환·입장 분기와문단폰트수명을과거047과대조한다.


## 작업140 — 현재049 normal50 성 입장

9000프레임/786wholePNG·PPU·OAM·mapping/6288CHR exact.50→0/gold0·성입장293snapshot/slot1C완성NT확인·4actualPNG직접검토.1614events/helper34PCrelocation검증·idle/stack/bus차이유지.ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](CASTLE049_NORMAL50_BRANCH.md).

다음 작업 하나: 현재049의점수3 booth 성공교환을새047baseline과동일입력·seed로실행하며,실제PRG data읽기매핑을추가관측해 slot15 farewell과macro88 소비·완성·clear를연결한다.


## 작업141 — 현재049 매표소 성공 교환/실제 reader

새047/049 각4500·339 wholePNG/PPU/OAM/mapping exact. 실제PRG읽기131건의주소/값/순서/문맥 동일,125 cycle동일/6건+38. main8/macro3 원천 소비,slot15 전체12byte·macro88 전체5byte·완성NT·font188·지도복귀 확인. 티켓10→11/점수0,직접4PNG·1680 PNG/RAM 시점 차이 보존. 원본/1편/ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](BOOTH049_SUCCESS_READER.md).

다음 작업 하나: 메뉴 기차 경로를 현재049와 새047에서 동일 입력으로 실행하고, RAM seed 없이 실제 PRG 읽기·요금·상단20/26·출발2A·게임 진입의 폰트 수명을 검증한다.


## 작업142 — 현재049 기차 controller-only reader

새047/049 각4500·339wholePNG/PPU/OAM/mapping·2712CHR exact.실제PRG159건·20/26/macro86 전체byte소비와title/rules/departNT완성확인.티켓10→8/초기기차63snapshot/지도복귀·직접6PNG. cycle0/38/76과idle/stack/bus차이유지·ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](TRAIN049_NATIVE_READER.md).

다음 작업 하나: 급류타기 메뉴 경로를 현재049와 새047에서 동일 입력으로 실행해, RAM seed 없이 실제 reader/상단21·27/하단요금·출발/게임진입의 폰트 수명을 확인한다.


## 작업143 — 현재049 급류 controller-only reader

새047/049 각4500·312wholePNG/PPU/OAM/mapping·2496CHR exact.실제PRG150건/21·27·macro87전체byte와title/rules/departNT완성확인.티켓10→7/초기급류63snapshot/지도복귀·직접5PNG. cycle0/38/76/idle·stack·bus차이유지·ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](WATER049_NATIVE_READER.md).

다음 작업 하나: 무입력 인트로9문단을 현재049/새047에서6000프레임 실행하며 물리PRG 읽기를 추가해,현재 font128..146과각문단·macro의실제소비및완성NT를연결한다.


## 작업144 — 현재049 무입력 인트로9 실제reader

각6000·200wholePNG/PPU/OAM/mapping·1600CHR exact.실제PRG676건/9main·macro버스터전체byte 소비 및모든줄완성NT·font128..146연결·9actualPNG직접검토.651cycle동일/24+1/1+2·idle/stack/bus차이유지.검증v1/v2가정실패보존/v3해결·기본티켓10/ROM·CSV불변.

[상세 변경·SHA·검증구분·재현·한계](INTRO049_NATIVE_READER.md).

다음 작업 하나: 138 원장을 보존하고 139..144를 반영한 새54원장145를 작성해, 현재초기화/실제reader/완성NT/직접PNG를구분한뒤 남은등록원천의reader 미연결 한경로를선택한다.


## 작업145 — 등록54 현재증거 원장 갱신

현재main46 presence/실제reader31(main25+macro6) 전체byte/새전줄NT완성16을구분. reader미연결23목록·macro82미관측≠unused.138보존·v1수기합집합오류/v2실측31해결·새runtime/ROM/CSV변경없음.

[상세 변경·SHA·검증구분·재현·한계](COVERAGE049_SOURCE_EVIDENCE_REFRESH.md).

다음 작업 하나: 현재049/새047의짧은카트메뉴·요금·출발경로에서실제reader를기록해 MAIN05867(rule1F)/MAIN058F6(title25)/MACRO061DE(cart85)를연결한다. 완주bot실험은재개하지않는다.


## 작업146 — 현재049 짧은카트경로 reader

각4500·339wholePNG/PPU/OAM/mapping·2712CHR exact. PRG142건/1F·25·macro85전체byte/전줄NT/티켓10→9/초기게임·4actualPNG. idle/stack/bus·cycle0/38/76보존. winningbot·완주stream재개없음/ROM·CSV불변.

[상세 변경·SHA·검증구분·재현·한계](CART049_NATIVE_READER.md).

다음 작업 하나: 현재049/새047에서RAM seed 없는기본10장 롤러코스터메뉴·요금·출발경로를실행해,MAIN05849(rule1E)/MAIN058F2(title24)의실제reader/전줄NT완성과초기게임폰트수명을연결한다.


## 작업147 — 현재049 롤러코스터 reader reader

각4500·312wholePNG/PPU/OAM/mapping·2496CHR exact. PRG137건/1E·24·macro84전체byte/전줄NT/티켓10→6/초기게임·4actualPNG. idle/stack/bus·cycle0/38/76보존. winningbot·완주stream재개없음/ROM·CSV불변.

[상세 변경·SHA·검증구분·재현·한계](COASTER049_NATIVE_READER.md).

다음 작업 하나: 성의normal49 거절과gold4 입장을현재049/새047에서각동결입력·seed로실행하며실제reader를기록해,main0F/16..1C/22/28의원천전체byte·완성NT를연결한다.


## 작업148 — 오늘 세션 종료/성 reader 실행 중단

사용자 “오늘은 여기까지”에따라즉시자동진행중단. 작업148의소유wrapper336/runner3448/Mesen24800만확인해종료·관련process없음. 완료047 normal49/중단049(685파일)/미시작gold4를구분하여보존. 새paired검증없음·마지막닫힌작업147·현재049/CSV불변.

[상세 중단·SHA·검증구분·재개명령·한계](SESSION_STOP_148.md).

다음 작업 하나(사용자 재개 지시 후): 사용자가재개를지시한뒤에만,완료047 normal49의동결environment/관측기/input/seed를확인하고중단049만새경로qa/dialogue/gatereader148_normal49_049_resume에서6000프레임재실행한다. 기존미완료QA를덮어쓰지않는다.


## 작업149 — 성 입장 reader 재개

일반49/골드4 경로 각각6000/9000프레임. 합1310 whole화면·10480CHR 일치, actual PRG222/179 읽기·10원천unit·13경로별 전줄NT 연결. 일반49 거절복귀/골드4 성진입·7실제PNG 확인. 중단148 보존, ROM·CSV 불변.

[상세 변경·SHA·검증구분·재현·한계](CASTLE049_SOURCE_READER_RESUME.md).

다음 작업 하나: 현재049 티켓부족 경로를 실제 PRG 읽기 관측기로 실행하여 변경한 MAIN0590C의 원천 바이트·전용226/227 폰트·완성문·clear를 연결한다.


## 작업150 — 수정 부족문구 실제reader

각4200프레임/190읽기. MAIN0590C·05929·macro88 전체byte,226/227·10/11tile NT·clear후196복귀.302PNG 중261전체/41둘째줄만 변경.새관측 실행이 각역사1812snapshot산출물과 동일.직접5PNG·ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](SHORTAGE049_SOURCE_READER.md).

다음 작업 하나: 145 이후의 실제 reader 보고서146/147/149/150을 등록 원천별로 합쳐 누락과 서로 다른 검증 범위를 재평가하고, 남은 작업을 실제 결함 또는 새 소비경로 근거에 따라 선택한다.


## 작업151 — 실제reader 원장·다음불확실성 재평가

등록54중 실제읽기49(main42/macro7), 전체byte49.미연결5정확목록 유지·전역완료율 아님.동일페이지증거수 반복을 피하고 급류 자연진행의 새판별근거를 조사한다.

[상세 변경·SHA·검증구분·재현·한계](READER049_REASSESSMENT.md).

다음 작업 하나: 급류타기의 기존 자연입력 실패와 native 죽음·구간완료·입력 소비 루틴을 읽어, 전체플레이 미해결을 줄일 수 있는 새로운 관측 또는 입력 경로 하나를 설계한다. 카트 winningbot 재실행은 하지 않는다.


## 작업152 — 급류 물에빠짐/점프/완료 조건

기존첫left로물에빠진state8/phase09복귀·체력3 유지.원본/049 코드동일·16점프/45clear CPU쌍. pressed50/80과supportC1·69=16/state09 완료를구분.새runtime없음.

[상세 변경·SHA·검증구분·재현·한계](WATER_NATIVE_PROGRESS_MODEL.md).

다음 작업 하나: 현재049 급류 경로에서2800프레임에 A를 한 번 누르고 무조건 좌우이동을 제외한 읽기전용 관측으로 발판·물에빠짐·clear 상태와 세로진행을 기록한다.


## 작업153 — 급류 첫점프 실제관측

A8프레임 nativeA80E실행/첫발판복귀,게임2779..3889/세로HI3.피해3회뒤실패·clear없음. v1Lua헤더escape오류보존/v2exit0·CHR2896·직접4PNG. ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](WATER_FIRST_JUMP_NATIVE_QA.md).

다음 작업 하나: 동일한첫점프 급류경로에서0430=6과7C0체력쓰기의 native PC·물리PRG·직전RAM·register를읽기전용으로관측해 실제피해소비조건을확인한다. 입력/RAM/ROM추가조작은없다.


## 작업154 — 급류 실제피해와회피모델

실제3피해=type44/art6C의E6E4충돌/AC95체력차감.153snapshot1812동일·6명령/24geometry CPU쌍.8픽셀상승해당순간회피.핀py65 CE cycle3→instance6정정·v1보존.

[상세 변경·SHA·검증구분·재현·한계](WATER_ACTUAL_DAMAGE_CONSUMER.md).

다음 작업 하나: 첫 native 장애물 충돌2910보다20프레임 앞선2890에 A8프레임만 추가한3300프레임 경로로 실제회피·체력·통나무재착지를 확인한다. RAM/ROM/좌표/시간조작없음.


## 작업155 — 급류 첫장애물회피/재착지실패

2890 A8으로첫actor피해0·체력3.공중playerVx0/boat260으로뒤처져2926state8물에빠짐.회피PASS/재착지FAIL분리·직접2PNG·ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](WATER_HAZARD_JUMP_LANDING_FAILURE.md).

다음 작업 하나: 실측통나무속도260에대한 A749 공중좌우입력 native연산을원본/049 CPU로검증하고,2890 A8에right8만추가해같은장애물회피와재착지를시험한다.


## 작업156 — 급류 공중right/재착지

24CPU쌍 boat260→right452. 실제2890 A+right8으로피해0/2922재착지/2930jump복귀/3300체력3유지.첫장애물경로만PASS·자연clear미달·ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](WATER_AIR_STEERING_LANDING.md).

다음 작업 하나: native충돌사각형·공중속도·발판조건으로 급류 전용 컨트롤러 입력을 설계하고, 읽기전용관측 및 실제입력기록과 함께 자연후반진행을시험한다.


## 작업157 — 급류 후반 객체 회피/미완주

36CPU쌍/8999입력요청/추가3점프/피해0·체력3.4023 이후 경로 종료로 자연clear 실패. 입력시점8불일치와 카메라축 오류를 별도 미해결로 보존. ROM/CSV불변.

[상세 변경·SHA·검증구분·재현·한계](WATER_ADAPTIVE_ACTOR_AVOIDANCE.md).

다음 작업 하나: 157과 같은 입력으로 native 화면하단 이탈 코드·4016 읽기/쓰기·RAM52 소비를 직접 관측하고, 카메라 축 이름을 원본 소비 코드로 정정한다.


## 작업158 — 실제 급류실패/입력시점/카메라 축정정

4023 nativeA65A phase09 기록,32경계/8투영CPU쌍.157과2034스냅샷/4499입력exact.8라벨불일치는 native소비가 없는 직전프레임으로 설명.647실제입력commit 검증/18무commit 원인미폐쇄. RAM69/6D는cameraX로정정,역사값보존.

[상세 변경·SHA·검증구분·재현·한계](WATER_EXIT_INPUT_AXIS_CORRECTION.md).

다음 작업 하나: 急류 통나무의 B+좌우 native 기울기/이동 코드와 첫 낙차 직전 fixture를 원본/049 CPU로 검증하여, 화면하단 이탈을 피할 입력 후보를 근거로 설계한다.


## 작업159 — 통나무 B 조작과 다음 통나무 연결

84기울기/21속도CPU쌍. 실제다음raft가78px 앞에 존재.158 경계 표기32→16 정정.

[상세 변경·SHA·검증구분·재현·한계](WATER_RAFT_CONTROL_AND_TRANSFER_MODEL.md).

다음 작업 하나: 실제 raft2 존재와 낙차 조건에 따라 A+우측으로 착지 목표를 raft2로 바꾼 컨트롤러를 새049 실행으로 검증한다.


## 작업160 — 첫 자연 통나무 갈아타기

3985 A→4035 native교체/4050 착지.6500까지진행,새물고기피해2회·체력1·clear없음.

[상세 변경·SHA·검증구분·재현·한계](WATER_FIRST_NATURAL_RAFT_TRANSFER.md).

다음 작업 하나: 160의 같은 입력으로 첫 물고기 type34의 실제 속도/상태 쓰기와 native갈아타기0716 쓰기를 읽기전용으로 추적한다.


## 작업161 — 물고기 중력과 통나무교체 실제소비

같은입력/스냅샷,181최종쓰기+12중력CPU쌍.물고기Vy+32/step,통나무INC0716 실제PC 연결.

[상세 변경·SHA·검증구분·재현·한계](WATER_FISH_AND_SWAP_NATIVE_CONSUMERS.md).

다음 작업 하나: 확인한 type34의 중력을 포함해 다음 충돌을 예측하는 컨트롤러를 설계하고, 새049 실제입력/피해/갈아타기/후반진행을 검증한다.


## 작업162 — 첫 물고기 회피와 두 통나무 교체

첫물고기회피/두갈아타기관측.착지flag128에서다음물고기2회피해·새type21피해로체력0.

[상세 변경·SHA·검증구분·재현·한계](WATER_FISH_PREDICTION_FIRST_RESULT.md).

다음 작업 하나: native A held에 따른 중력30/50hex를 원본/049 CPU로 검증하고, type34 점프 A 지속시간만 늘려 착지 시점 피해가 사라지는지 새 실행으로 확인한다.


## 작업163 — A 유지 회피와 자연 후반구조물

A20으로세물고기피해없음.2갈아타기/type21피해1/자연towertype2도달,8603좌표실패.4410 PNG차이로전체영상동일FAIL.

[상세 변경·SHA·검증구분·재현·한계](WATER_HELD_A_AND_NATURAL_TOWER.md).

다음 작업 하나: 자연8430 구조물type2의 실제 목표/발판 소비코드를 원본/049 CPU와 관측fixture로 연결하고, 통나무와 구분한 구조물 도약 조건을 설계한다.


## 작업164 — 자연 손잡이 소비 조건

type2=로프/손잡이.48CPU쌍 nonnegativeVy·충돌→C9/0541을검증,실제붙잡기는다음.

[상세 변경·SHA·검증구분·재현·한계](WATER_ROPE_CAPTURE_NATIVE_MODEL.md).

다음 작업 하나: 실제type2 손잡이를 향한 A/우측 도약을 컨트롤러에 추가하고 C9/0541 native쓰기·입력전수·후반진행을 새049 실행에서 확인한다.


## 작업165 — 실제 플레이 사용자 이관·잔여 정리

사용자 실제플레이담당.자동플레이종료/165자료보존/ROM·CSV불변.비플레이 잔여6종 정리.

[상세 변경·SHA·검증구분·재현·한계](ACTUAL_PLAY_USER_HANDOFF_AND_REMAINDERS.md).

다음 작업 하나: HOWTO/PAUSE/POW 및 등록범위 밖 원천의 기술 잔여를 정적으로 정리해 번역 추가·제외 판단 근거를 작성한다.


## 작업166 — 현재049 원천 전수 목록·미연결 후보 통합

등록54본문·33그림, 원본CHR128뱅크와NT20/별도프린터12슬롯 정적 대조. 후보7건 보존·미연결 유지. ROM/CSV 불변.

[상세 변경·SHA·검증 구분·제한](CURRENT049_NONPLAY_SOURCE_INVENTORY.md).

다음 작업 하나: 현재049 문장·그림 검토자료와 후보7건을 통합한 비플레이 결정 자료를 만들고 PC/모바일 표시 및 ZIP 무결성을 확인한다.


## 작업167 — 현재049 비플레이 통합 검토 묶음

54원천·33그림·후보7건, 기존실제21/정적4그림 통합.049 state/reset 근거·사용자 플레이 담당·163 RGB실패 표시. PC/모바일/ZIP PASS; ROM/CSV 불변.

[상세 변경·SHA·검증 구분·제한](CURRENT049_NONPLAY_REVIEW_PACKAGE.md).

다음 작업 하나: 검수용049 적용 패키지에 최신 지원 범위·사용자 검수 안내·알려진 한계를 반영한 새 ROM 없는 묶음을 만들고 최종 ZIP의 실제 Windows 적용을 확인한다.


## 작업168 — 최신 검토용 패키지·사용자 검수 안내

동일049 패치/도구 보존, 최신 한계·검수 안내·비플레이 검토자료 포함한20파일 ROM없는ZIP. 최종ZIP 한글/공백경로 실제Windows적용 byte-exact PASS. 플레이 실행 없음.

[상세 변경·SHA·검증 구분·제한](CURRENT049_REVIEW_PACKAGE_AND_USER_QA_GUIDE.md).

다음 작업 하나: 등록 밖 후보의 소비 근거를 정적 코드와 기존 증거로 추가 연결하고, 범위 응답을 반영할 때만 원문 보존 또는 번역 추가로 결정한다.


## 작업169 — 보존 범위 확정·PUSH START 타이틀 소비 연결

사용자HOWTO/PAUSE/POW 원문유지확정.별도PUSH START는기존타이틀sprite8E/CHR63 소비에연결. 발견7중3보존승인+1기존보존연결+3미해결. ROM/CSV불변.

[상세 변경·SHA·검증 구분·제한](SCOPE_RETENTION_AND_TITLE_PROMPT_CONNECTION.md).

다음 작업 하나: 사용자 원문 유지 결정과 타이틀 소비 연결을 비플레이 검토자료·검수용 적용 패키지의 새 버전에 반영하고 현재 상태를 인계한다.


## 작업170 — 범위 결정 검토자료 갱신·오늘 작업 중단

사용자 오늘마감으로중단·자동재개없음.최신170검토는HOWTO/PAUSE/POW 원문유지확정과PUSH START소비연결반영.PC/모바일/ZIP PASS.ROM/CSV불변.168적용묶음 범위문서갱신은재개후.

[상세 변경·SHA·검증 구분·제한](SESSION_STOP_20261007_SCOPE_REVIEW.md).

다음 작업 하나: 사용자가 명시적으로 재개하면169 보존 결정과170 검토자료를 새 ROM 없는 적용 패키지에 반영하고 최종ZIP 실제Windows적용을 확인한다.


## 작업171 — 원문 보존 결정 반영·최신 적용 패키지171

사용자 재개.169보존3/타이틀연결1/미연결3와검토170을21파일ROM없는ZIP에동기화. 최종ZIP한글/공백실제Windows적용 byte-exact PASS. ROM/CSV불변·게임실행없음.

[상세 변경·SHA·검증 구분·제한](CURRENT049_SCOPE_APPLY_PACKAGE_171.md).

다음 작업 하나: 미연결 RYO51/NT1C/진단STAGE SELECT의 현재 정적 근거와 범위 선택지를 묶고, 실제 소비 연결 또는 원천 보존에 필요한 결정 근거를 정리한다.


## 작업172 — 미연결3원천 현재 근거·범위 선택지

RYO51/NT1C/진단STAGE SELECT 현재049 코드/원천보존과한계를분리.원문유지/소비조사후번역 선택지준비·결정pending.171의옛외부스킬캐시링크누락을별도보고/내부자산감사PASS. ROM/CSV불변.

[상세 변경·SHA·검증 구분·제한](CURRENT049_REMAINING_THREE_SCOPE_OPTIONS.md).

다음 작업 하나: 남은3원천에 대한 사용자의 범위 선택을 기록하고 그 결정 범위만 현재 검토자료와 적용 패키지 설명에 반영한다.


## 작업173 — 보존6건 확정·검토/실제적용 반영

사용자 결정으로 발견7건의 범위 미결정0(명시보존6+기존타이틀연결1). 검토173 PC/모바일·25PNG·54/33·최종23파일ZIP 실제Windows적용 PASS. ROM/CSV불변; 플레이 사용자 담당.

[상세 변경·SHA·검증 구분·제한](CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md).

다음 작업 하나: 보존된162/163 종료 자료만 사용해 frame04410 PNG 차이의 캡처 출처를 오프라인 대조하고, 확인 가능한 원인과 확인 불가한 한계를 구분한다.


## 작업174 — 기존PNG 차이 오프라인 출처 대조

종료162/163의343쌍PNG/4410raw5쌍/입력4644행·공식소스6개 재대조. 저장인접PNG동일복사본없음.7326픽셀/전체RGB FAIL·원인미확정 유지; 새게임실행없음.

[상세 변경·SHA·검증 구분·제한](CURRENT049_OFFLINE_CAPTURE_PROVENANCE_174.md).

다음 작업 하나: 사용자 검수 결과를 연결할 현재049 점검표와 배포 전 남은 조건을 한 문서로 정리하고, 추가 기술 작업과 사용자 판단 항목을 구분한다.


## 작업175 — 현재049 사용자 검수 연결·잔여조건 정리

검수표12항목/빈응답양식·최종판단/증거공백·수정→검증→카페작업기 순서정리. 확인한기록의새수정요구없음; 전체완료/전역corpus/사람승인아님.173ZIP/ROM/CSV불변.

[상세 변경·SHA·검증 구분·제한](CURRENT049_USER_REVIEW_READINESS_175.md).

다음 작업 하나: 사용자의 현재049 실제 플레이 및 문구/명칭/그림 검수 결과를 받아 원천ID·재현장면에 연결하고 필요한 수정만 새 버전으로 검증한다.


## 작업176 — 사용자 티켓교환 대사 깨짐 재현·진단

사용자자연신고를동일2.2.1격리host/복사상태로재현. 정상MAIN05782 NT가162대신196폰트에표시됨. 상단F9 slot23 초기화가하단폰트를덮는결함등록; 수정전.

[상세 변경·SHA·검증 구분·제한](BOOTH_EXCHANGE_FONT_COLLISION_176.md).

다음 작업 하나: 매표소 숫자slot23에서 기존 하단폰트를 같은 사이클로 보존하는050 후보를 만들고, 교환 caller와 인접경로의 원인/수정 회귀를 검증한다.


## 작업177 — 티켓교환 폰트충돌 수정050 채택

사용자신고의 교환숫자갱신 폰트충돌을050에서수정.53,760 CPU사례·독립재빌드·네분기 paired1116실제화면/상태 PASS.050채택, 전체플레이/최종사람검수는별도.

[상세 변경·SHA·검증 구분·제한](BOOTH_EXCHANGE_FONT_FIX_050_177.md).

다음 작업 하나: 050 ROM없는 적용묶음을 만들고 한글·공백 경로에서 실제 Windows 적용을 검증한다.


## 작업178 — 수정050 ROM없는 적용묶음·실Windows 검증

050수정ZIP 준비. 실Windows helper8+최종ZIP적용 byte-exact/ROM-free PASS.049검토는역사자료로보존, 현재사용자Mesen/세이브는수정하지않음.

[상세 변경·SHA·검증 구분·제한](BOOTH_FIX050_APPLY_PACKAGE_178.md).

다음 작업 하나: 사용자가 새050 ROM을 열고 초기화/매표소 재진입 후 티켓 교환 대사를 검수한다.


## 작업179 — 티켓교환 수정050 최종 인계·자산감사

050수정/178ZIP/current인계 대조 완료.177의13,514자산·178의35자산/원본·1편/로컬링크PASS. 실제전체플레이/최종사람검수는사용자담당.

[상세 변경·SHA·검증 구분·제한](BOOTH_FIX050_FINAL_RECONCILIATION_179.md).

다음 작업 하나: 사용자가 새050 ROM을 열고 초기화/매표소 재진입 후 티켓 교환 대사를 검수한다.


## 작업180 — 상태창 왼쪽·아래 원본비교 조사

원본에도왼쪽8픽셀배경색띠/창아래검은20픽셀여백존재. 실제source/0507HUD시점·PPUMASK1896행동일.44의한글높이용2픽셀shift는구분;ROM/패키지변경없음.

[상세 변경·SHA·검증 구분·제한](HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md).

다음 작업 하나: 사용자 실제 플레이 검수를 이어가며 새로 발견한 표시 문제를 해당 장면과 함께 기록한다.


## 작업181 — 움직이는 STOP 별도소비 진단

고정정지와다른CHR46 스프라이트원문 STOP 확인. 사용자HUD 전놀이기구관측은별도기록. 잘못된CHR22 추정/host가드실패/다른카트세이브 관측을보존했다.

[상세 변경·SHA·검증 구분·제한](MOVING_STOP_CONSUMER_DIAGNOSIS_181.md).

다음 작업 하나: CHR46 움직이는표지판의글자영역만정지로삽입하고동일입력재현을비교한다.


## 작업182 — 움직이는 STOP 한글화051·동일조건 검증

051채택:CHR46 58바이트 글자만정지로수정.734 paired화면/상태 exact;90화면 글자픽셀만변경,644전체화면동일.독립ROM/IPS재빌드PASS.

[상세 변경·SHA·검증 구분·제한](MOVING_STOP_GLYPH_FIX_051_182.md).

다음 작업 하나: 원본일본판에적용하는051 ROM없는검수ZIP을만들고실Windows 적용검증한다.


## 작업183 — 수정051 ROM없는 적용묶음·실Windows 검증

051 움직이는STOP 수정ZIP 준비.실Windows8사례와최종ZIP적용 byte-exact/ROM-free PASS.원문유지6건및050티켓교환수정보존.

[상세 변경·SHA·검증 구분·제한](MOVING_STOP051_APPLY_PACKAGE_183.md).

다음 작업 하나: 사용자가 새051 ROM을 열고 초기화/기차 재진입 후 위아래로 움직이는 정지 표지판을 검수한다.


## 작업184 — 051 최종인계·이전자산 보존 감사

177..183고정자산해시/원본·1편/로컬링크 PASS.사용자적용050 보존,현재051+ROM-free ZIP183 인계.새플레이검수는사용자담당.

[상세 변경·SHA·검증 구분·제한](MOVING_STOP051_FINAL_HANDOFF_AUDIT_184.md).

다음 작업 하나: 사용자가 새051 ROM을 열고 초기화/기차 재진입 후 위아래로 움직이는 정지 표지판을 검수한다.


## 작업185 — 전체텍스트11px 정적가능성·배치후보

요구를전체텍스트11px로정정.현재8×8 출력은그대로대체불가;12×16셀/192px16칸/4줄3KiB 정적후보와PNG 비교작성.실제ROM/CPU/PPU검증전이며051 보존.

[상세 변경·SHA·검증 구분·제한](GLOBAL_TEXT11_FEASIBILITY_185.md).

다음 작업 하나: 11px 일반대사의12×16 출력셀/줄바꿈·소거·CHR공급 경로를 설계하고 대표문단 삽입PoC를 만든다.


## 작업186 — 오프닝 9문단 11px 전용 출력·빌드

오프닝9문단053 삽입·독립ROM/IPS재빌드·최종6502 PASS. 기존051/번역CSV/다른화면 유지; 실제표시검증은187에서 분리.

[상세 변경·SHA·검증 구분·제한](OPENING11_PAIRED_ROW_POC053_BUILD_186.md).

다음 작업 하나: 053의9문단 표시·지우기·3회반복·Start분기를 실제Mesen자료로 검증한다.


## 작업187 — 오프닝11px 실제9문단·반복·분기 검증과 오늘중단

오프닝053의9문단3회/2167RGB/3024상하소비/30지우기 PASS. Start분기·734기차화면회귀 PASS. 오늘중단;053적용ZIP·전체11px전환 미실시.

[상세 변경·SHA·검증 구분·제한](OPENING11_POC053_RUNTIME_HANDOFF_187.md).

다음 작업 하나: 사용자가 작업을 재개하면 오프닝11px PoC053의 ROM 없는 적용 패키지를 만들고 실제Windows 적용을 검증한다.


## 작업188 — 오프닝11px PoC053 적용패키지·Windows 검증

ROM없는053패키지·Windows8사례·최종ZIP실적용 byte-exact PASS. 오프닝전용범위·9문단비교·폰트라이선스포함;기준051유지.

[상세 변경·SHA·검증 구분·제한](OPENING11_POC053_APPLY_PACKAGE_188.md).

다음 작업 하나: 188패키지와186/187인계의해시·프로젝트링크·원본/1편보존을확인하고 전체11px의다음적용범위를정리한다.


## 작업189 — 오프닝053 패키지·고정근거·재개표지 감사

185~188고정해시·원본/1편/프로젝트링크 PASS. 외부과거캐시1건분리. 기준051/오프닝053 구분해전체11px설계준비.

[상세 변경·SHA·검증 구분·제한](OPENING11_POC053_PACKAGE_EVIDENCE_AUDIT_189.md).

다음 작업 하나: 오프닝외일반대사·동적숫자·카드·HUD·결과·크레딧의11px 배치/CHR용량을 구분해 다음대표UI 적용계획을 만든다.


## 작업190 — 전체11px 다음출력기·변수·공유폰트 용량계획

45draft를출력경로별로분리.42정적배치/FA6course/F8CPU1000숫자수요/공유font합집합 계산.다음홈한줄PoC;새ROM/실제실행없음.

[상세 변경·SHA·검증 구분·제한](GLOBAL_TEXT11_NEXT_CONSUMER_PLAN_190.md).

다음 작업 하나: 홈한줄MAIN_05741의lower22A8/5행지우기·font130 수명을확인하고11px 상하동시출력 대표UI 후보를 만든다.


## 작업191 — 홈한줄11px 후보054·원본빌드·CPU 검증

홈root8/168px/5행소거경계로054한줄후보제작.ROM/IPS독립동일·42상하/110소거·778fallbackCPU PASS.054실제실행미수행·미채택.

[상세 변경·SHA·검증 구분·제한](HOME11_SINGLE_LINE_CANDIDATE054_191.md).

다음 작업 하나: 054홈한줄의실제표시·상하타일소비·대기/지우기·선택지전환과오프닝회귀근거를확보한후 홈·매표소12문단확대로진행한다.


## 작업192 — 홈실행뱅크 판정정정·오프닝6문단 조정요청

기존049읽기와053동등범위로physical18홈소비연결.054실제미검증유지.사용자문단6줄바꿈/서명오른쪽정렬을다음작업으로전환.

[상세 변경·SHA·검증 구분·제한](HOME11_CONSUMER_AND_PAGE6_LAYOUT_CHOICE_192.md).

다음 작업 하나: 053기반으로문단6만사용자지정줄바꿈·서명오른쪽정렬한새오프닝PoC를만든다.


## 작업193 — 오프닝6문단 줄바꿈·서명우측정렬 PoC055

사용자지정문단6배치반영055.053대비508바이트/코드·제어위치·다른8문단불변.원본/IPS/독립ROM·최종CPU PASS;실제194분리.

[상세 변경·SHA·검증 구분·제한](OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md).

다음 작업 하나: 055오프닝9문단반복/6문단RGB와서명우측정렬·소거를실제Mesen자료로검증한다.


## 작업194 — 요청6문단 배치055 실제표시·반복·소거 검증

055요청6문단실제정렬확인.9문단3회/2167RGB/3024상하/30소거 PASS.053비교2086전체동일·232문단6영역만변경.

[상세 변경·SHA·검증 구분·제한](OPENING11_PAGE6_LAYOUT_POC055_RUNTIME_194.md).

다음 작업 하나: 055문단6조정판의ROM없는패키지를만들고Windows적용·최종ZIP실적용을검증한다.


## 작업195 — 요청6문단 조정055 패키지·Windows 실적용

ROM없는055사용자배치조정판·Windows8/최종ZIP실적용 exact PASS.053/055동일프레임비교·라이선스포함;054미포함.

[상세 변경·SHA·검증 구분·제한](OPENING11_PAGE6_LAYOUT_POC055_PACKAGE_195.md).

다음 작업 하나: 055패키지·193/194의고정근거·인계링크/원본보존을감사하고재개표지를갱신한다.


## 작업196 — 요청6문단 수정055 패키지·근거·최신 인계 감사

6문단 줄묶음·오른쪽 서명055 검증/패키지 완료. 188~195 고정 해시와 원본/1편 보존 PASS. 기준051·최신 오프닝055·홈054 CPU후보를 구분했다.

[상세 변경·SHA·검증 구분·제한](OPENING11_POC055_CURRENT_HANDOFF_AUDIT_196.md).

다음 작업 하나: 055를 기준으로 홈 대표 한 줄의 11px 후보를 재구성하고, 실제 소비 경로와 연결해 검증한다.


## 작업197 — 그림 글자 제외·문자열11px 확대 범위와 제약

사용자 범위를 문자열 출력기로 고정. 오프닝9/일반33/크레딧3 구분. HUD·정지 등 그림 유지, 다음 홈·매표소12개.

[상세 변경·SHA·검증 구분·제한](TEXT11_SCRIPT_SCOPE_AND_FEASIBILITY_197.md).

다음 작업 하나: 055를 기준으로 홈·매표소12개에11px 점진/즉시 출력을 적용하고 최종6502와 독립 재빌드를 검증한다.


## 작업198 — 홈·매표소12개 후보056 비대상CPU 플래그 실패 기록

056 독립 빌드 동일, 점진/즉시 출력 검사 후 비대상V flag 차이로 거부. 후보·실패 증거 보존, 미채택·미패키지.

[상세 변경·SHA·검증 구분·제한](HOME_BOOTH11_056_REJECTED_CPU_FLAG_198.md).

다음 작업 하나: 055 기반 새057 후보에서 범위 판정 전후P를 보존하고 전체 CPU 검사를 다시 수행한다.


## 작업199 — 홈·매표소12개11px 후보057 점진/건너뛰기 CPU 검증

055기반12개11px057.352 skip/4320 init/1556 fallback/050 retention/원래5행clear PASS. 독립ROM·IPS exact, 새실제 실행 없음.

[상세 변경·SHA·검증 구분·제한](HOME_BOOTH11_CANDIDATE057_TYPED_SKIP_CPU_199.md).

다음 작업 하나: 057 개발 후보를 ROM 없는 적용 패키지로 만들고 Windows 적용·최종 ZIP을 검증한다.


## 작업200 — 홈·매표소11px057 개발 후보 패키지·Windows 실적용

ROM 없는 CPU후보057 패키지, Windows8/최종ZIP 실적용 exact PASS. 실제057 실행 미수행을 명시, 정적PNG/라이선스 포함.

[상세 변경·SHA·검증 구분·제한](HOME_BOOTH11_CANDIDATE057_APPLY_PACKAGE_200.md).

다음 작업 하나: 나머지21개 일반대사의 실제 창 기하·동적숫자·상단 공유글꼴 용량을 검사해 다음 확대 설계를 고정한다.


## 작업201 — 남은 일반21개·크레딧3개 확대 설계와 숫자 용량 해결안

F8 1000값 숫자3000자리 고정타일 분리,175→54/128. 상단10페어·보유254/255 저장안, 크레딧144/128·긴커서/전송 재설계 필요. 새ROM/실행 없음.

[상세 변경·SHA·검증 구분·제한](TEXT11_REMAINING_NUMERALS_CARDS_CREDITS_DESIGN_201.md).

다음 작업 하나: 057 홈·매표소의 실제 출력/건너뛰기·NMI/IRQ·소거·교환 폰트 수명 근거를 확보한 뒤 나머지21개 소비기에 확대한다.


## 작업202 — 크레딧11px 영문 간격 대안·106타일 왕복

같은 글자 모양·문구 보존. 영문16px 간격이면144→106/128,2KiB 직렬화3문단 픽셀exact. 미채택 정적안, 긴커서/전송/실제스크롤 남음.

[상세 변경·SHA·검증 구분·제한](CREDITS11_SHARED_FONT106_SPACING_OPTION_202.md).

다음 작업 하나: 197~202 고정근거·원본/링크를 감사하고057 CPU후보와 남은21개·크레딧 설계를 최신 인계에 반영한다.


## 작업203 — 일반33개 후보058 단독CPU 성공·공유창 결함 거부

단독33문단/F8/FA/skip/초기화CPU PASS이나 제목·규칙 동시거주와 실제160/184px 창기하 결함 발견.058 미채택·미패키지.

[상세 변경·SHA·검증 구분·제한](ORDINARY11_058_ISOLATED_CPU_CARD_REJECTION_203.md).

다음 작업 하나: 새059 후보에서 놀이기구별 이름+설명 글꼴 공유와160/184px 기하·이름칸 높이를 수정해 동시거주를 검사한다.


## 작업204 — 일반33개11px059·카드 글꼴공유/이름칸 수정·최종CPU

42등록문단 후보(오프닝9+일반33).F8천값/FA6×2/1071skip/4320init/1556fallback/5쌍 카드공유 PASS.160/184px·이름 테두리 수정.새059 실행 없음.

[상세 변경·SHA·검증 구분·제한](ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md).

다음 작업 하나: 059 개발 후보의 ROM 없는 적용 패키지를 만들고 Windows 적용/최종 ZIP을 검증한 뒤 현재 인계를 갱신한다.


## 작업205 — 059 첫 적용 패키지 크기 검증 실패 보존

ROM059는 그대로이며 적용 도구의 이전499728바이트 검사 때문에 첫 Windows 적용 실패. 부분 패키지/QA를 보존하고 새206으로 수정한다.

[상세 변경·SHA·검증 구분·제한](ORDINARY11_PACKAGE059_SIZE_GUARD_FAILURE_205.md).

다음 작업 하나: 별도206 패키지에서 결과 크기524304/SHA 검사를 수정하고 Windows8사례·최종ZIP 적용을 검증한다.


## 작업206 — 일반대사11px059 개발 후보 패키지·Windows 실적용

ROM 없는 CPU후보059 패키지, Windows8/최종ZIP 실적용 exact PASS. 실제059 실행 미수행을 명시, 정적PNG/라이선스 포함.

[상세 변경·SHA·검증 구분·제한](ORDINARY11_CANDIDATE059_APPLY_PACKAGE_206.md).

다음 작업 하나: 197~206 고정근거와 원본/링크를 감사하고 최신059 후보와 남은 크레딧을 정본 인계에 반영한다.


## 작업207 — 059 확대 후보 정본 인계·고정 근거 감사

197~206 고정근거·2편 원본/CSV·프로젝트 링크 PASS.1편 참조5개 해시 일치/역사 원본 경로1개 현재 없음.059 CPU/적용 후보42개11px,실제미수행,크레딧3개8px.

[상세 변경·SHA·검증 구분·제한](TEXT11_CANDIDATE059_CURRENT_AUDIT_207.md).

다음 작업 하나: 크레딧3개의 실제 출력 루틴에서 초기 전송량·16px 줄 간격·모드5/6 주소를 확인하고 별도11px CPU 후보의 구현 조건을 확정한다.


## 작업208 — 크레딧11px 원래16px 기하·전송 큐 설계

원래 줄 간격16px.첫2D244바이트 큐/스택 충돌 위험으로 직접 화면출력 중지 전송을 설계,2E/2F는 원래호출수·최대62바이트 이벤트로 분할. 아직 ROM/실행 없음.

[상세 변경·SHA·검증 구분·제한](CREDITS11_NATIVE_GEOMETRY_AND_QUEUE_DESIGN_208.md).

다음 작업 하나: 새060에서 크레딧3개를 줄별 포인터·초기 직접NT·native호출수 보존 진행형 출력기로 구현하고 최종CPU를 검증한다.


## 작업209 — 크레딧 확대060 빌드·중복 뱅크저장 CPU 거부

060 독립빌드 exact이나 일반대사CPU에서 복귀태그08 남음: 공통/기존GUARD 중복FDD3 원인.060 미채택·미패키지,059 유지.

[상세 변경·SHA·검증 구분·제한](CREDITS11_CANDIDATE060_MAPPER_REJECTION_209.md).

다음 작업 하나: 별도061에서 중복 mapper저장을 제거하고 크레딧3·기존42·전체원래스케줄CPU를 검증한다.


## 작업210 — 061 private복귀주소·대기값 CPU 거부

061 일반CPU의미복제post-FDDB주소/크레딧58초기화결함 발견. 실패·빌드보존,059 유지.062 mirrored복원 및delay수정 예정.

[상세 변경·SHA·검증 구분·제한](CREDITS11_CANDIDATE061_RETURN_AND_DELAY_REJECTION_210.md).

다음 작업 하나: 새062에서 mirrored복원·event대기값을수정하고 기존42·크레딧3·원래4000frame스케줄CPU를검증한다.


## 작업211 — 062 등록45개11px 빌드·CPU·정적 복원

오프닝9+일반33+크레딧3 전등록45개11px 후보062.독립빌드/기존42CPU/크레딧327호출·4000frame동기CPU PASS.작은그림보존,실제062 미수행·미채택.

[상세 변경·SHA·검증 구분·제한](TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md).

다음 작업 하나: 062 ROM없는 적용패키지를 만들고 Windows8사례·최종ZIP 적용을 검증한다.


## 작업212 — 062 등록45개11px 개발 적용패키지·Windows 실적용

062 ROM없는 개발ZIP/Windows8/최종ZIP실적용 exact PASS.45문자·5모형·CPU·라이선스포함.실제062미수행·미채택,작은그림보존.

[상세 변경·SHA·검증 구분·제한](TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md).

다음 작업 하나: 197~212 고정근거·원본/CSV·프로젝트 링크를감사하고062와사용자실제검수목록을정본인계에반영한다.


## 작업213 — 062 등록45개11px 정본 인계·고정 근거 감사

197~212 해시·2편원본/CSV·프로젝트링크 PASS.062 등록45개11px CPU/재빌드/적용후보·실제미수행·미채택.1편역사원본경로1개누락별도기록.

[상세 변경·SHA·검증 구분·제한](TEXT11_CANDIDATE062_CURRENT_HANDOFF_AUDIT_213.md).

다음 작업 하나: 사용자가 새062 ROM을 초기화해 실제 화면을 검수한 결과를 받아, 보고된 글꼴·줄바꿈·소거·전환 결함을 별도 새 빌드로 수정한다.


## 작업214 — 불필요한 펼친 산출물·캐시 정리와 검증 보관

펼친 과거자료·캐시 1,004,563개 정리, 순 파일 바이트 7.48GiB 절감. 과거 바이트는 전수검증 압축보관, 원본·원천·051·062·링크 유지. 복원검증PNG1개는 직접삭제 정책차단으로 남음. 실제 플레이 없음.

[상세 변경·SHA·검증 구분·제한](PROJECT_CLEANUP_ARCHIVED_HISTORY_214.md).

다음 작업 하나: 사용자의 새062 실제 화면 검수 결과를 받아 보고된 글꼴·줄바꿈·소거·전환 결함을 별도 새 빌드로 수정한다.


## 작업215 — 062 즉시출력 두 문단의 조건부 NMI 전송예산 초과

062 CPU prefix에서1E/20 즉시출력 NTSC 기준초과(최대2319). 실제 화면/IRQ/DMC 미검증.062 보존,별도063 native언롤 큐 개선 준비.

[상세 변경·SHA·검증 구분·제한](TEXT11_NMI_PREFIX_BUDGET_215.md).

다음 작업 하나: 별도063에서 기존 native opcode4의 언롤 VRAM 전송을 즉시출력 큐에 적용하고, 모든 기존 문단/skip/큐/CPU 및 NMI prefix를 비교한다.


## 작업216 — 실제062 출력 진입점 NMI 검증·215 판단 정정

215는fallback직접호출로오판·철회.실제062 full231/skip1071 prefix초과0,명목여유44cycles.063없음·ROM/CSV동일·실제미검수.

[상세 변경·SHA·검증 구분·제한](TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md).

다음 작업 하나: 062의 출력/mapper복귀 중 IRQ를 주입하는 한정 CPU 검증으로 큐·레지스터·뱅크 복귀의 조합을 검사한다.


## 작업217 — 일반 대사33개 IRQ 경계 주입·복귀 CPU 검증

66출력 상태·62,940 IRQ 주입 PASS, 중간 은행66회 출력 완료 동일.051과 콜백 동일.062 불변·실제 검수 남음.

[상세 변경·SHA·검증 구분·제한](TEXT11_IRQ_INJECTION_217.md).

다음 작업 하나: 오프닝9개와 크레딧3개의 출력 경로에서 IRQ 마스크와 복귀 상태를 한정 CPU 모델로 확인한다.


## 작업218 — 오프닝·크레딧 IRQ CPU 검증과 재개 인계

852출력 호출·149,824 한정IRQ 주입 PASS. 재개 총212,764주입.062/패키지 불변·실제 검수 대기.

[상세 변경·SHA·검증 구분·제한](TEXT11_OPENING_CREDITS_IRQ_218.md).

다음 작업 하나: 사용자의062 실제 화면 검수 결과를 받아 첫 재현 장면 하나의 출력·소거·글꼴 매핑을 조사한다.


## 작업219 — IRQ 인계 스택 여유 수치 정정

217/218 문서의 스택 여유를 CPU 보고와 같은48/49바이트로 정정. 검사/ROM/패키지 불변.

[상세 변경·SHA·검증 구분·제한](TEXT11_IRQ_STACK_GAP_CORRECTION_219.md).

다음 작업 하나: 사용자의062 실제 화면 검수 결과를 받아 첫 재현 장면 하나의 출력·소거·글꼴 매핑을 조사한다.


## 작업220 — 최종배포 v1.0 빌드·ROM없는 적용패키지

062 exact데이터 v1.0/ExpectedWrites/독립재빌드/Windows8/최종ZIP 적용 PASS.실제062 플레이검수 미기록.

[상세 변경·SHA·검증 구분·제한](RELEASE_V1_0_BUILD_PACKAGE_220.md).

다음 작업 하나: 네이버 카페 복사용 작업기·근거구분 PNG·오프라인 HTML을 만들고 데스크톱/모바일 렌더를 확인한다.


## 작업221 — 네이버 카페 업로드용 작업기·8PNG·HTML

카페복사용글/8PNG/내장HTML/ROM없는ZIP13파일·CRC/desktop/mobile/zoom PASS.게임검수·실제게시 미수행.

[상세 변경·SHA·검증 구분·제한](NAVER_CAFE_WORKLOG_V1_0_221.md).

다음 작업 하나: 최종배포·공개작업기·재현원천·QA핵심을보존하고대량펼친보관중복과실패초안·임시적용사본·렌더캐시를정리한다.


## 작업222 — 과거 QA·중간물 손실 없는 정리

정확 경로 정리 완료.214/222 보관 SHA와 실제 복원 통과.원본·현재 빌드·재현원천 보존.

[상세 변경·SHA·검증 구분·제한](LOSSLESS_RELEASE_CLEANUP_222.md).

다음 작업 하나: 이전 배포 묶음223 보관과 정리 근거를 봉인한다.


## 작업223 — 이전 배포 묶음 정리

이전 묶음199파일을 SHA·CRC 확인 보관 후 삭제.212 재현입력과 현재 배포 유지.

[상세 변경·SHA·검증 구분·제한](SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md).

다음 작업 하나: 사용자062 실제 화면·완주1차 완료 보고를 최종 릴리즈와 작업기에 반영한다.


## 작업224 — 사용자062 1차완주 검수 반영 최종배포

사용자062 실화면·완주1차완료보고 반영.데이터불변·14파일ROMfree·최종ZIP 실제적용 PASS.배포후검증예정.

[상세 변경·SHA·검증 구분·제한](FINAL_RELEASE_USER_FIRST_QA_224.md).

다음 작업 하나: 카페작업기와검증표에도사용자1차완주완료/배포후검증예정을반영하고다시렌더한다.


## 작업225 — 사용자1차 검수 완료 반영 카페 작업기

1차실화면·완주 완료/배포후검증예정 반영.8PNG·13파일ROMfree·desktop/mobile/zoom PASS.

[상세 변경·SHA·검증 구분·제한](NAVER_CAFE_FINAL_USER_REVIEW_225.md).

다음 작업 하나: 최종 배포 파일명을 명확히 정리하고 임시 적용 사본·렌더 캐시를 삭제한 뒤 최종 인계를 갱신한다.


## 작업226 — 최종 배포·작업기·정리와 인계 완료

062 사용자1차화면·완주 완료 보고 반영.최종2ZIP·실제적용·작업기렌더 PASS.순약2.32GiB 정리·배포후검증 예정.

[상세 변경·SHA·검증 구분·제한](FINAL_DELIVERY_CLEANUP_226.md).

다음 작업 하나: 배포 이후 접수되는 제보의 ROM 해시·에뮬레이터 버전·직전 행동·장면을 기록하고 해당 경로의 추가 검증을 진행한다.


## 작업227 — 1·2편 NES 한글화 기술 지침과 게시자료

1·2편 기술지침15항목+자료참조·설명도2·ROM없는예제/8파일ZIP.전체Page읽기동일·HTML PC/모바일·예제 PASS.

[상세 변경·SHA·검증 구분·제한](TINYTOON12_TECHNICAL_GUIDE_227.md).

다음 작업 하나: 사용자가 기술 지침 본문과 설명도2개를 게시 위치에 배치하고 배포 후 제보를 같은 검증 원칙으로 수집한다.


## 공개 작업기·기술 지침 독자용 개정 — 작업228

내부 빌드 번호를 본문·비교 이미지·캡션·공개 출처에서 제거했다. 목적과 수정 전/후로 다시 설명했으며 두 리더의PC/모바일·ZIP검사가 통과했다. 게임 배포·번역·사용자1차 검수 상태는 같다. [상세 변경·해시·검증](PUBLIC_ARTICLE_READER_REVISION_228.md).

다음 작업 하나: 사용자가 수정된 작업기·기술 지침을 게시하고, 배포 후 제보의 ROM 해시·환경·직전 행동·장면을 수집한다.


## 작업229 — 카페 작업기 작성자 말투 적용

사용자도입부·어린시절경험·엔딩소감을살리고전체본문과이미지설명을게시판1인칭말투로개정했다. 내부빌드번호없는상태와기술범위·검수구분유지. HTML PC/모바일·확대·ZIP전수검사PASS. [상세 인계·SHA·재현](CAFE_WORKLOG_AUTHOR_VOICE_229.md).

다음 작업 하나: 사용자가 본문·그림을 카페 편집기에 배치하고, 배포 이후 제보의 ROM 해시·환경·직전 행동·화면을 수집한다.


## 작업230 — 불필요한 이전 게시자료·검토본 정리

20대상90파일을private230보관으로전수검증후삭제했다. 최신게임배포·작성자작업기·기술지침과보존4713파일SHA확인PASS. [변경·해시·검증·복원](SUPERSEDED_PUBLICATION_CLEANUP_230.md).

다음 작업 하나: 사용자가 최신 작업기·기술 지침과 최종 릴리즈를 게시하고, 배포 이후 제보를 수집한다.
