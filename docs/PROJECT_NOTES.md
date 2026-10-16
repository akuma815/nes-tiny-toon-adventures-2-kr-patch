> 최신공개자료: [게임배포](dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip) · [작성자작업기](workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html) · [기술지침](workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html). 이전게시자료·QA·중복재빌드는 [230보관·복원안내](docs/SUPERSEDED_PUBLICATION_CLEANUP_230.md)를따른다.

# Tiny Toon Adventures 2 — 한글패치 v1.0 — 2026-10-09, 작업226


[1·2편 한글화 기술 지침 Page](https://chatgpt.com/space/page_7e1e9fe45f1881918ff36b3962ea16c0)와 [게시자료 ZIP](dist/TinyToon12_TechnicalGuide_Reader_20261009.zip)을 추가했다. 기존 게임 배포파일과062 검수 상태는 그대로다. [기술지침 인계](docs/TINYTOON12_TECHNICAL_GUIDE_227.md).

**v1.0은062와 같은 데이터입니다. 사용자가 실제 화면·완주1차 검수를 완료했다고 보고했으며, 배포 이후 추가 검증이 필요합니다.** 새 게임 실행이나 실제 카페 게시를 수행한 것은 아닙니다. 아래 역사 기록의 ‘미검수·미채택’은 추가 사용자 보고 전 당시 상태입니다.

- [최종 배포 ZIP](dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip) — ROM 없음,14파일,실제 Windows 적용 결과062와 완전히 같음.
- [네이버 카페 작업기 ZIP](dist/TinyToon2_KR_Worklog_Reader_20261009.zip) — 본문·안내·8PNG·HTML,ROM 없음.
- [오프라인 작업기](workspace/publication/TinyToon2_KR_Worklog_Reader_20261009/작업기.html), [카페 복사용 본문](workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_Release_20261009/카페_복사용_본문.txt).
- [로컬 최종 ROM](build/release_v1_0_220/TinyToon2_KR_v1.0.nes),SHA `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`.
- [사용자1차 검수 보고](qa/reports/user_review224.json), [최종 감사](qa/reports/final_delivery226_audit.json), [최종 인계](docs/FINAL_DELIVERY_CLEANUP_226.md).

독립 재빌드·ExpectedWrites·ROM/IPS 비교, Windows 적용 사례와 최종ZIP 실제 적용, 한정 CPU/NMI/IRQ 검사 및 작업기PC/모바일/확대 확인은 통과했습니다. 실제 화면·완주1차 완료는 사용자 보고로 구분합니다. 배포 후 검증 결과는 아직 없습니다. 등록45문단(오프닝9·일반33·크레딧3)은 전게임 발견률100%를 뜻하지 않습니다. HUD·정지 그림의 크기와 원문 유지6원천은 사용자 결정대로 유지했습니다. CSV 행별 상태를 사람 검토 완료로 일괄 변경하지 않았습니다.

불필요한 과거 QA·이전 공개ZIP·임시 적용 사본·렌더 캐시를 손실 없는 보관/정확 경로 삭제로 정리했습니다.222/223/226 합계110,831파일,순약2.32GiB 절감. 원본·번역원천·재현 스크립트·최종산출물·QA근거는 보존했습니다.214/222는 SQLite 보관,223/226은 ZIP 보관이며 private 보관본은 공개하지 않습니다. [222복원](docs/LOSSLESS_RELEASE_CLEANUP_222.md), [223복원](docs/SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md), [226복원](docs/FINAL_DELIVERY_CLEANUP_226.md).212/220 패키지 및003 작업기 폴더는 재현 입력입니다.

**다음 작업 하나: 배포 이후 접수되는 제보의 ROM 해시·에뮬레이터 버전·직전 행동·장면을 기록하고 해당 경로의 추가 검증을 진행한다.** [오늘 인계](docs/HANDOFF_2026-10-09.md), [오늘 journal](docs/journal/2026-10-09.md), [계획](docs/LOCALIZATION_WORK_PLAN.md).

---

## 이전 작업 당시의 역사 기록

> **작업218:** 062의 한정 NMI·IRQ CPU 검증 추가, ROM/IPS/ZIP 불변. 실제 화면 검수는 사용자 담당. [최신 인계](docs/TEXT11_OPENING_CREDITS_IRQ_218.md)

> **작업216 정정:** 실제062 출력CPU prefix full231/skip1071 시간초과0. 215의fallback측정판단은철회,063없음·실제062미검수. [최신검증](docs/TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md)

> **2026-10-09 작업214 정리 완료:** 펼친 과거자료·캐시 1,004,563개 정리, 순 파일 바이트 7.48GiB 절감. 과거 바이트는 전수검증 압축보관, 원본·원천·051·062·링크 유지. 복원검증PNG1개는 직접삭제 정책차단으로 남음. 실제 플레이 없음. [정리 인계](docs/PROJECT_CLEANUP_ARCHIVED_HISTORY_214.md)

> **2026-10-09 작업213 / 기준051 유지 / 062: 등록45개11px CPU·빌드·적용 검토 후보 / 실제062 미검수·미채택** [최신 인계](docs/HANDOFF.md)

## 최신 텍스트11px 검토 후보 — 062

HUD·정지 등 작은 그림을 보존하고 오프닝9+일반33+크레딧3을11px 글꼴로 확대한 개발후보다. [062 ROM](build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes), [정적 배치45개·창 모형5개](workspace/review/text11_211/review.html), [ROM 없는 적용ZIP212](dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip), [구현·CPU211](docs/TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md). 독립재빌드·기존42개와크레딧 CPU·Windows실적용 PASS. 실제062 실행·CHR256·NMI/IRQ·소거/전환·가독성은미검수이며 실제플레이는사용자담당이다. 등록45개는전게임완료율이아니다. 크레딧영문16px간격은개발안이다.

# 기준 개발본 — 051 (작업184 근거)

[움직이는 표지판 수정·검증182](docs/MOVING_STOP_GLYPH_FIX_051_182.md), [ROM](build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes), [IPS](build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.ips), [051 적용ZIP183](dist/TinyToonAdventures2_KR_Review_051_MovingStop_20261008.zip). 처음고정표지판뒤위아래로움직이는 STOP을정지로수정했다.050대비CHR46 58바이트만변경.티켓교환글꼴수정050 포함.734 paired화면 비교/독립ROM·IPS재빌드/실Windows8·최종ZIP적용 PASS. 전체플레이/최종문구·명칭·그림검수는사용자담당이다.

[HUD원본비교180](docs/HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md)의왼쪽띠/아래여백은원본구성이며051 HUD수정없음.원문유지6건및CSV그대로다.등록33그림과이번추가움직이는소비를별도로기록했다.이전049/050자료는각버전의역사기록이며새051 전장면검증으로해석하지않는다.

작업51 당시 채택043: [기차 간판 한글화·6005화면 검증](docs/TRAIN_SIGN_KOREAN.md). 다음은 attract/root9 및 실제 문자 원천 폐쇄 조사.

작업50: [기차 간판 실제 소비·PNG](docs/TRAIN_SIGN_CONSUMER.md). 다음은 전용216..219의 한글 간판043 빌드.

작업49: [일시정지·기차 IRQ 조사](docs/PAUSE_WORLD_SURVEY.md). ROM042 유지, 다음은 기차 간판 실제 RGB 소비 진단.

# Tiny Toon Adventures 2 — NES 한글화

2026-10-04 한글화 착수. 작업48 당시 **`dialogue_kr_poc_042`**: 생성형 타이틀·지도·매표소·게임오버 그림, 등록 대사45초안, 놀이기구 안내/크레딧/HUD·보너스·게임오버 선택지를 삽입했다. 게임오버 검증4040화면/378645시점 통과. 전체자연플레이·세계그림/PAUSE소비·최종사람검토·정식배포는 진행중이다.

작업 재개는 [최신 인계](docs/HANDOFF.md), 현재 확인 사항은 [조사 현황](docs/SURVEY.md), 구현 순서는 [작업 계획](docs/LOCALIZATION_WORK_PLAN.md)을 따른다. [작업 규칙](AGENTS.md)에 매 작업 인계와 최종 네이버 카페 작업기 자료 보존을 명시했다.

## 원본

- 경로: `original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes`
- 크기: 262,160바이트
- SHA-256: `f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d`
- iNES 1.0 / mapper 85 / PRG 128 KiB / CHR 128 KiB. 일본어 화면 확인. 외부 DB 리비전 식별은 미확정.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify_source.ps1
```

## 폴더

| 경로 | 책임 |
|---|---|
| original/rom/ | 수정하지 않는 원본 |
| extracted/prg/, chr/, text/ | 원본에서 추출한 데이터·정적 프리뷰 |
| workspace/translation/ | 원문 토큰·번역·검토 상태의 단일 원천 |
| workspace/fonts/, graphics/, tables/, asm/ | 폰트·그림·문자표·코드의 편집 원천 |
| workspace/publication/ | 완료 후 카페 작업기 본문과 공개용 이미지 |
| scripts/, config/, manifests/ | 재현 스크립트·설정·입출력 식별 |
| docs/, docs/journal/ | 조사·현재 계획·인계·작업기 근거 기록 |
| qa/reports/, logs/, screenshots/, saves/, states/ | 검증 결과와 격리 실행 증거 |
| work/, backups/ | 실험 중간물·필요한 변경 전 백업 |
| build/<ID>/, dist/ | 재현 빌드·ROM 없는 배포 패치 |
| tools/ | 프로젝트 전용 실행 도구 |

빈 폴더는 작업 위치 예약이다. 원본 ROM은 루트에서 보존 경로로 이동했고, 1편 파일은 수정하지 않았다.

## 현재 산출물

- 역사적014 [ROM](build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.nes)/[IPS](build/dialogue_kr_poc_014/TinyToon2_dialogue_kr_poc.ips),[새5문단 화면](qa/dialogue/intro014_actual_pages.png),[구현](docs/POC_INTRO_COMPLETE.md),[2334표본 검증](qa/reports/intro014_validation.json),[세션감사](qa/reports/intro_complete_session_20261005.json). 관측도입1~9·홈·타이틀을포함한다.10draft/44untranslated,개발본이다. 이후메뉴/매표소/놀이기구의별도IRQ소비기를계속조사한다.

- [넷째 문단 실제 화면](qa/dialogue/pages013_actual_4x.png), [넷째 구현과 재현](docs/POC_DIALOGUE_FOURTH.md), [2048표본 검증](qa/reports/dialogue_fourth013_validation.json), [자산 식별](manifests/dialogue_fourth_assets.json), [세션감사](qa/reports/dialogue_fourth_session_20261005.json). 두 행 밖 차이0,홈417표본 전체일치,IRQ9339시점 일치,재빌드/실제IPS적용 동일. 당시5draft/49untranslated,CHR144KiB다.

- 이전013 통합 [ROM](build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.nes) / [IPS](build/dialogue_kr_poc_013/TinyToon2_dialogue_kr_poc.ips): 타이틀003·도입부 첫째/둘째/셋째/넷째 문단·홈 초안. IPS는 깨끗한 일본어 원본에 적용한다. 개발 검증본이며 정식 배포본은 아니다.
- [셋째 문단 실제 화면](qa/dialogue/pages012_actual_4x.png), [셋째 구현과 재현](docs/POC_DIALOGUE_THIRD.md), [1998표본 검증](qa/reports/dialogue_third012_validation.json). 당시 실행검증011과012 ROM은 전체바이트가 같으며012는 인물근거 notes를 정정해 동봉했다. 홈407표본 전체일치,셋째 한줄밖 차이0,IRQ8973시점 일치다.
- [둘째 문단 실제 화면](qa/dialogue/pages008_attract/frame_01320.png), [문단별 글꼴 구현과 재현](docs/POC_DIALOGUE_PAGES.md), [850표본 검증](qa/reports/dialogue_pages008_validation.json), [현재 인계](docs/HANDOFF_2026-10-05.md). 홈233표본은003과 전체 화면이 같고, 도입/건너뛰기 경로의 대사 영역 밖 픽셀 차이는0이다.
- [실제 홈 대사](qa/dialogue/home003_actual_4x.png), [홈 비교](qa/dialogue/home003_comparison.png), [소비 경로/글꼴 수명/재현](docs/POC_DIALOGUE_HOME.md), [437표본 검증](qa/reports/dialogue_home003_validation.json).002는 아래의 첫 문단 검증 기준으로 보존했다.
- [실제 한글 문단](qa/dialogue/poc002_actual_4x.png), [원본 조건과 비교](qa/dialogue/poc002_comparison.png), [구현·재현·한계](docs/POC_DIALOGUE.md), [165표본 검증](qa/reports/dialogue_poc002_validation.json).
- [한글 타이틀 실제 화면](qa/title/title_kr_ai_003_actual_4x.png), [원본/수정 비교](qa/title/title_kr_ai_003_comparison.png), [타이틀 구현/재현 문서](docs/POC_TITLE.md).
- 타이틀 실험본 [ROM](build/title_kr_ai_003/TinyToon2_title_kr_poc.nes) / [IPS](build/title_kr_ai_003/TinyToon2_title_kr_poc.ips). 재빌드·실제 적용·Mesen 실행·72표본 비교 검증. [검증 보고서](qa/reports/title_kr_ai_003_validation.json).
- 원본/AI/변환 PNG와 프롬프트는 [타이틀 원천 manifest](manifests/title_assets.json)에 연결했다. 작은 보조 문구의 최종 디자인 검토는 남아 있다.
- [원본 화면 모음](qa/screenshots/baseline_intro_contact_sheet.png), [선택 안내 화면 모음](qa/screenshots/baseline_home_contact_sheet.png).
- [CHR 조사](extracted/chr/survey_20261004_001/rom_survey.json): 32페이지 / 8,192타일 왕복 일치.
- [추출 보고서](extracted/text/table_20261004_001/extraction_report.json): 주 테이블 48슬롯/46고유 스트림 + 매크로 9슬롯/8고유 스트림, 총 54개 원천 단위. 모든 단위가 번역 문장이라는 의미는 아니다.
- [번역 작업 원천](workspace/translation/text_ja.csv):작업26 당시54행 중20행`draft`,34행`untranslated`. 원문·토큰·포인터를 보존했다. 이전 준비패킷과002/003/008 QA는 각 당시 입력을 기준으로 한 역사적 자료다. 크레딧 원천은 글꼴 프로파일 미확정으로 보존했다.
- [초기 검증 보고서](qa/reports/initial_session_20261004.json).

새 출력 경로를 지정해 재현한다. 기존 번역 CSV를 덮어쓰지 않는다.

```powershell
python .\scripts\survey_rom.py --output .\extracted\chr\survey_repro_next
python .\scripts\run_survey_qa.py --output .\qa\screenshots\baseline_attract_next --frames 5400
python .\scripts\run_survey_qa.py --output .\qa\screenshots\baseline_game_next --frames 3000 --start 720
python .\scripts\run_survey_qa.py --script .\scripts\trace_text_consumer.lua --output .\qa\logs\text_consumer_next --frames 3100
python .\scripts\extract_text.py --output .\extracted\text\table_repro_next
```

Python 3.12 / Pillow 12.3.0 / 로컬 Mesen 2.1.1을 사용한다. 실제 시각 검토는 새 캡처를 직접 확인한 뒤 별도로 기록한다.


작업17/18: 홈 글꼴 latch 기반017 채택.015/016 타이밍 실패 후보 보존,017 전체2521화면 차이0/실제115353시점 일치. 원래 PPU2002 읽기 유지·초기화76사이클·10draft44미번역 불변. [상세 기록](docs/UI_FONT_LATCH.md). 다음은 UI macro/인코딩 제약 검사이며 별도 중단 지시 없이 이어간다. 전체 완료·배포·카페 게시가 아니다.


작업19/20: 일본어를 보존하는UI매크로/font019 기반 채택.018의상단 설명판 결함을 실제NMI추적으로찾아9E28→RAM34를수정했다.679전체화면/74319시점동일,reader48슬롯/변수192조건검증.10draft44미번역불변. [상세](docs/UI_MACRO_PASSTHROUGH.md). 다음은관측된홈/매표소8문구초안삽입이며바로이어간다.


## 작업21~23 현재 — 홈·매표소022

홈 선택4개/매표소 출발·환영·교환·부족4문구의초안을삽입했다. [구현/해시/재현/한계](docs/UI_HOME_BOOTH.md),[실제8페이지](qa/dialogue/ui022_actual_pages.png),[검증](qa/reports/ui022_validation.json).020전환깨짐/021도입1사이클경계차이는기각하고보존했다.022는매표소중복초기화만조정해공통005와도입부를유지한다.1527표본현재행밖차이0/도입848전체일치/115353실제시점동일,CPU1504+108조건,재빌드/실제적용동일.18draft36미번역,CHR168KiB/ROM434192,전게임완료율아님. 다음은기차·급류타기·성입구 소비기조사이며즉시이어간다.


작업24: [기차·급류·성조사](docs/UI_RIDE_GATE_SURVEY.md).2/3장요금·진입절차·성4골드/50일반부족분기확인. 성대사font불일치를발견해즉시교정/검증한다. ROM022/18draft36미번역불변,전체플레이/성공분기검증아님.


작업25: [성상단font023교정](docs/GATE_TOP_FONT.md) 채택.2바이트만변경,한글18draft36미번역불변.1105표본홈한글행밖0/기차·급류631전체일치/성정상221,69714실제시점동일. 성은NMI font34로두행을공급한다. 다음은기차/급류홈2문구삽입이다.


작업26: [홈기차·급류024](docs/UI_HOME_RIDES.md) 채택.20draft34미번역,CHR176KiB/예약6KiB.1105표본선택행밖0/성474전체일치,195169실제시점동일,CPU1504·재빌드/실제적용같음. 다음은성문단별상단font공급과전환검증이다.


작업27: [성NMI시점실패](qa/reports/commit026_rejection.json).025/026은픽셀474/CPU1728·1504/실제적용통과에도NMI1077건2cycle차이로기각.024/SSOT20draft34유지. 시간증가없이홀수뱅크상단font공급으로수정해즉시검증한다.


작업28: [같은시간상단font027](docs/GATE_FONT_TAG.md)채택.20draft34미번역불변.2001전체화면/PPU/OAM같음/185067실제시점같음,CPU1728·1504/재빌드·실제적용같음. 홀수custom font가상단도공급하며성fallback171은같은일본어glyph다. 다음은관측성5문구한글삽입이다.


## 작업29 — 성 입구 문구5개, 028 채택

[구현·변경 파일·해시·재현·검증 한계](docs/UI_CASTLE_MESSAGES.md)를 기록했다. 신규 prepare_ui_gate.py/build_ui_gate.py/verify_ui_gate.py/verify_ui_gate_hooks.py/make_gate_page_evidence.py, plan/SSOT backup,028/재빌드/한글경로 적용,성 v4·IRQ 캡처와 직접5문구 화면을 보존한다. 이전20초안·원본·1편 불변. 정적/CPU1504·seed720/실제 적용·재빌드 PASS;474화면의 현재 행 밖 변화0/69714실제 시점 동일/일본어1A 복귀9장 전체 동일; 직접5장면 가독성 확인. 등록25draft29미번역, 전체 플레이 등은 미수행. ROM SHA256 `c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e`; IPS `352d9cf7f33ecefdba41b897bc12b989acff3b18eaaf81a087f2fe3774cba136`; CSV `2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8`.

다음 행동 하나: 골드4장·일반50장의 입장 성공 분기를 지정 RAM seed QA로 관측한다. 바로 계속한다.


## 작업30 — 입장권 충족·포인트 교환 성공 분기 관측

[변경 파일·해시·명령·검증 한계](docs/NATIVE_BRANCH_SURVEY.md):028 ROM/SSOT25draft29미번역 불변. 별도 runner/Lua/4종 seed와4개 QA를 추가했다. frame1000의 지정 RAM 주입 주소·전후값·PC/cycle을 보존하며 일반 플레이와 구분한다. 원본 CPU 숫자 판정24건 동일. 골드4 입장/일반50→0 입장/49부족/3점→0과티켓10→11 교환을 실제 native 이벤트·RAM으로 확인했다. 실제 화면과 성 내부 상태도 검토했으나 완주/자연 수집은 미수행. 이전 산출물·원본·1편 보존. 다음 행동 하나: FA를 유지하는 성 가격1A와 허가1C 한글 삽입·검증. 바로 계속한다.


## 작업31 — 성 가격·입장 허가,031 채택

[구현·변경 파일·해시·명령·한계](docs/UI_CASTLE_PRICE_ADMISSION.md): FA 원래 숫자 출력과alias2C를 보존하여 일반 티켓 가격1A/허가1C를 삽입했다. 이전25개 초안·원본·1편·모든 산출물 보존. 029/030의 검사 건수/별칭 중복 메타데이터를031에서 고쳤고 ROM은 모두 동일하다. 정적/문구별48변수조합/ABI1504·초기seed720/재빌드·실제적용 PASS. 실제1522화면의 성 대사행 밖 변화0/299240시점 동일, 직접 가격2436·허가2124 및 성 카드/게임상태 확인. 성공 경로는 명시RAM seed이며 자연수집/완주가 아니다. 등록27draft27미번역. ROM SHA256 `8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19`; IPS `3c5a6b88e040064ab664b93bd6cefc030f580d974a05dd8012ef769100febf2a`;CSV `979325a40d12762c62d27ec4a70edc33646ae780dedf2e787bbca4c498e67462`. 다음 행동 하나: 교환 완료 인사15/출발2A 한글화·검증. 바로 이어간다.


## 작업32 — 교환 완료 인사·출발,032 채택

[변경 파일·해시·명령·검증 한계](docs/UI_SUCCESS_START.md): 인사15/출발2A를 하단 전용188/190으로 삽입하고 상단 일본어 카드를 보존했다. 원본/1편/이전27개 초안·모든 산출물 불변. 정적/reader각호출/ABI1504·seed720/재빌드·실제적용 PASS.863화면의 현재 행 밖 변화0/215827실제 시점 동일, 직접 두 문구/성 게임상태 검토. 성공은 지정RAM seed이며 자연수집/완주 증거가 아니다. 등록29draft25미번역. ROM `c4b40639bafba6a25a1c186c82005963ec4fecdf8d3a22308eaf1ab6643a7d67`;IPS `0eb0c8328e9196bf8c1e008b4d8ce080d0cb9794112f3097d002b835331c4ada`;CSV `ba881bbffdaf4f5fa84d43f941d9166914e156358a7337c3b1bb66be8af33c86`. 다음 행동 하나: 놀이기구 상단 제목·규칙·요금 공통font 구성/다섯 경로 검증. 즉시 진행한다.


작업33: 다섯 놀이기구 제목·규칙·요금11원천 추가,40draft/14미번역.1786화면/505383시점 검증 및 실제5장 직접 검토. [공통 카드 구현·재현·한계](docs/UI_RIDE_CARDS.md).


작업35:034거절문제수정 후036채택.42draft/12미번역(기술적숫자·공유macro·크레딧).2973화면/640965시점 검증,원래코드변경0. [구현/재현/한계](docs/UI_STAGE_LOWER.md).


[작업36 크레딧실제소비/CPU좌표교정](docs/CREDITS_CONSUMER_SURVEY.md). 현재036/42draft그대로이며게임완주와별도인scene seed조사다.


## 작업37 — 크레딧037 채택

게임명·제작 역할3원천 한글화, 이름·KONAMI·권리표시 보존.45draft/9기술·공유원천. 정적/CPU/ABI1504·초기720/재빌드/한글 경로 실제IPS 통과. 크레딧327화면·99724시점, 새intro/coaster1150전체화면·137255전체IRQ값 동일. 직접 네 actual 화면 검토. 지정4seed이며 자연 엔딩/전체완주 증명이 아니다. [변경·해시·재현·검증 한계](docs/CREDITS_KOREAN.md). 다음 행동 하나: 기술·공유 원천과 남은 영문 그림의 실제 소비 정리. 중단 없이 계속한다.


## 작업38 — 등록 기술/공유원천 관계정리

ROM/SSOT변경없음,037유지.45표시초안+F9숫자1+문맥글꼴macro7+등록내미사용macro1. 전체corpus완료아님. [변경·해시·정적검증·한계](docs/REGISTERED_SOURCE_READINESS.md). 다음행동:지도간판NT/CHR소비연결과PNG추출. 계속한다.


## 작업39 — 지도간판실제소비·PNG추출

상단NMI CHR80~83/36NT셀/팔레트와144×16 원래PNG가전체RGB일치,현재지도상단타일각1회. ROM/SSOT변경0,037유지. [파일·해시·재현·정적/실제근거·한계](docs/MAP_BANNER_EXTRACTION.md). 다음행동:imagegen으로몬타나랜드생성및틀보존삽입/관측consumer검증. 계속한다.


## 작업40 — 생성형지도간판038채택

몬타나랜드PNG→13px/원래palette→32tile/391bytes삽입. 코드·대사·틀·NT·팔레트불변,45draft/9기술공유유지. 재빌드·실제IPS/1565화면/70947동일IRQ값/보호픽셀0,직접정상/fade지도검토. [파일·해시·재현·검증·한계](docs/MAP_BANNER_KOREAN.md). 다음행동:매표소영문NT/PRG·NMI/CHR소비추적. 계속한다.


## 작업41 — 매표소CHR/PRG문자실제소비조사

038/SSOT불변. controller-only4500+IRQ4500,원래NMI124/125/102/103·literal각806Eread·NT·간판24tile실제RGB연결확인. [파일·해시·재현·검증·한계](docs/BOOTH_GRAPHICS_SURVEY.md). 다음행동:전용font204/205 및生成형매표소간판삽입/숫자·대사·보호픽셀·시점검증. 계속한다.


## 작업42 — 매표소그림/소지·점수039채택

생성형매표소24tile, literal5군/currentfont204·한글12자로삽입. 등록45draft/9기술공유유지. 정적/CPU생산자768·decoder128D-clear/재빌드/실제IPS/2243화면·188916시점/보호픽셀0,추가NMI204font17실제표본/124대조19같음. 내부3은실화면3000점,교환후0점/11장인원래동작보존. 직접정상/교환전후검토. [파일·해시·재현·검증·정정·한계](docs/BOOTH_GRAPHICS_KOREAN.md). 다음행동:놀이기구게임/HUD·결과화면남은영문/일본문자소비조사. 계속한다.

작업43: [실제게임 HUD 소비 조사](docs/GAME_HUD_SURVEY.md),039 유지,040 배치 시험 진행.

현재 채택040: [플레이HUD 한글화](docs/GAME_HUD_KOREAN.md).4558화면/1321047시점,다음결과보너스문구작업.

작업45: [보너스 실제소비 조사](docs/RESULTS_CONSUMER_SURVEY.md).040 유지,다음보너스7종한글화.


현재 작업46: [041 결과 한글화·검증·한계](docs/RESULTS_KOREAN.md). 다음 행동 하나: PAUSE/GAME OVER 실제 소비 추적·추출. 중단 없이 계속한다.


작업47: [실제 게임오버·PNG 소비 조사](docs/GAMEOVER_CONSUMER_SURVEY.md).041/CSV 유지. 다음 행동 하나: 생성형 게임오버와 세 선택문구 삽입·복귀/시점 검증.


작업48: [생성형 게임오버042·선택지·검증·한계](docs/GAMEOVER_KOREAN.md). 다음 행동 하나: PAUSE/세계 영문그림의 실제소비 목록 추적. 중단 없이 계속한다.


작업52 [자동시연/마지막 엔진/등록46본문 호출](docs/ENGINE_CLOSURE.md) 완료. 현재043/SSOT 그대로, 다음은 성 일반50/49 분기 검증.


작업53 [성 일반50/49·실제 플레이](docs/CASTLE_CURRENCY_QA.md) 검증: 성 HUD 획 잘림을 발견해 작업54로 계속 수정한다. 현재043은 최종 배포본이 아니다.


작업54 [실제 성 HUD 검증/의심 정정](docs/CASTLE_HUD_QA.md) PASS. 53의 획잘림은 발견 확정이 아닌 육안 의심이었으며 픽셀/IRQ 대조로 해소됐다. 현재043으로ROM없는 개발판 패키지를 준비한다. 최종사람검토/전체완주를 주장하지 않는다.


작업55 [ROM없는검토용개발판043](docs/REVIEW_PACKAGE.md)과Windows8검사/최종ZIP실제적용PASS. 최종판이아니며 사람검토자료를이어준비한다.


작업56 [원문/번역/그림UI/실제장면 검토자료](docs/TRANSLATION_REVIEW_KIT.md)와desktop/mobile 표시검증PASS. ROM/SSOT그대로,다음57 reset/무세이브장기경로를이어진행한다.


작업57 [reset/재진입/네controller장기경로](docs/RESET_LONG_WORLD_QA.md) PASS. 전체완주를주장하지않으며같은043세이브상태왕복을이어검증한다.


작업58 [같은043 저장 상태 왕복](docs/SAVESTATE_ROUNDTRIP_QA.md) PASS. 다음은 원본/043 오디오 레지스터 비교이며 계속 진행한다.


작업59 [오디오 레지스터 비교](docs/AUDIO_REGISTER_QA.md): 값/순서/프레임은 같으며 급류 APU 상태 차이는 조사 중이다. 청음 통과를 주장하지 않고 계속한다.


작업60 [APU 관찰모델](docs/APU_OBSERVATION_QA.md): 동기화11출력상태는같고무음DMC위상차이만잔여다. 후속관찰을계속한다.


작업61 [APU 동기화 확대](docs/APU_EXTENDED_QA.md): 출력위상차이를기록했다. 음악/효과음24KiB와레지스터보존은통과했고PCM/청음은미확정이다.


작업62 [실제DMC읽기](docs/DMC_CONSUMER_QA.md) 소비바이트보존PASS. 카트의자연플레이경로를이어조사한다.


작업63 [카트 입력/좌표소비기](docs/CART_CONTROL_SURVEY.md) PASS. 좌표를이용한controller-only 입력으로자연클리어를이어시도한다.


작업64 [카트18k 추적입력](docs/CART_PURSUIT_ATTEMPT.md)은클리어에미도달했다. A충전/해제소스에맞춘다음controller 실험을이어간다.

작업65 [A 충전·해제 관찰](docs/CART_CHARGE_ATTEMPT.md): 가속 연결 확인, 자연클리어 미도달.

작업66 [카트 구멍 소비기](docs/CART_GEOMETRY_SURVEY.md):12,105 실제질의 일치.

작업67 [지형·관성 조작 시도](docs/CART_GEOMETRY_POLICY_ATTEMPT.md):18k 체력3 유지, 자연클리어 미도달.

작업68 [적 카트 낙하·제거 소비기](docs/CART_ENEMY_CONSUMER_SURVEY.md):실제객체제거 연결, 자연클리어 미도달.

작업69 [카트 구간 완료 원본 분기](docs/CART_CLEAR_BRANCH_SURVEY.md):3구간 전환 구조를검증했다.

작업70 [카트 첫 구간 자연클리어](docs/CART_NATURAL_ROUND_QA.md):4970에두번째구간진입,최종3구간완료는미수행.

작업71 [좌표축정정/카트36k](docs/CART_AXIS_RUNTIME_QA.md):첫구간재현, 두번째구간시간만료/홈복귀.

작업72 [8픽셀 몸체경로](docs/CART_BODY_PATH_QA.md):첫구간재현,최종클리어 미도달.


## 작업73 — 새 영문 안내 소비기/추출

[파일·해시·재현·실패·단위정정·검증·다음 작업](docs/NOTICE_CONSUMER_SURVEY.md). ROM/SSOT변경0. 실제 CHR62/두 생산자/28타일을 연결했다. 다음 하나: 한글 안내 삽입 빌드044.


## 작업74 — 두 안내 한글화 / 빌드044

[파일·SHA·재현·검증·한계](docs/NOTICES_KOREAN.md). 새CHR220/생산자2상수,512 CPU사례·실제진단604스냅숏·75,776PPU행·재빌드/IPS적용 통과. 현재044, 다음 하나: 자연20k 경로에서 안내/홈 전환 확인.


## 작업75 — 두 안내 자연 경로 검증

[파일·SHA·재현·실패·검증·한계](docs/NOTICES_NATURAL_QA.md). controller-only20k/19,999입력행·666world행 기존043 동일,829PNG/6,632CHR조각 검증. 직접 다음라운드/시간초과/홈 확인. 전체클리어는 아님. 다음 하나:128CHR의8×16 그림/UI 목록 재검토.


## 작업76 — 실제 START! 누락/소비기

[파일·해시·재현·단위/범위·검증·한계](docs/START_CONSUMER_SURVEY.md). START122/123 actual2670/3,072RGB/48타일 연결. 기존116..121 미관측검사와 구분. 다음 하나:‘시작!’ 빌드045.


## 작업77 — ‘시작!’ 한글화 / 045

[파일·SHA·재현·정적/적용/runtime/직접검증·한계](docs/START_KOREAN.md). CPU1024사례/19cycles·재빌드/적용·자연20k/829PNG검증. 현재045. 다음하나:다른3놀이기구 공통시작 회귀.


## 작업78 — 다른세놀이기구 시작 회귀

[파일·SHA·재현·검증·새누락·한계](docs/START_SHARED_QA.md). 3쌍1,704PNG/045의6,816CHR조각검증,직접6장면확인. 기차 STOP 영문표지를발견했다. 다음하나:STOP 실제소비기·PNG추출.


## 작업79 — STOP 실제배경 소비/PNG

[파일·SHA·재현·후보기각·검증·한계](docs/STOP_CONSUMER_SURVEY.md). CHR68/69/NT2800/768RGB·20,560PPU행/단일font표값연결. 다음하나:‘정지’ 세로글꼴046.


## 작업80 — 정지 표지 /046

[파일·SHA·재현·CPU모델범위·실패·검증·한계](docs/STOP_KOREAN.md). 046표지글자만변환/재빌드·IPS적용·20,560livePPU행/2,395정확pixel통과. 현재046, 다음하나:다른3코스CHR확장회귀.


## 작업81 — 046 다른코스 보존

[파일·SHA·재현·검증·한계](docs/STOP_SHARED_QA.md). 852PNG/4260PNG·RAM·OAM·PPU·mapping파일이045동일, 직접3플레이화면확인. 다음하나:현재046 사람검토키트새버전.


작업82: [빌드046 검토 자료](docs/TRANSLATION_REVIEW_046.md)를 갱신했다. 54원천/33문구/실제13화면과 ROM 없는 ZIP, PC·모바일 표시 검증 완료. 사람 검토는 대기 중이다.


작업83: [현재046 검토 패치](docs/REVIEW_PACKAGE_046.md) — ROM 없는 ZIP 및 실제 Windows 적용8개 검사/ZIP 재적용 PASS.


작업84: [POW 후보 소비 조사](docs/POW_CONSUMER_SURVEY.md). 실제 뱅크 선택과 그림 소비를 구분해 기록했다. 원본 그래픽 보존, 전역 미사용 증명 아님.


작업85: [현재046 저장 상태/리셋](docs/STATE046_REGRESSION.md) 검증 완료. 기차 재진입 및 정지224/225 복원, APU 저장 시점 비교 정정 근거를 보존했다.


작업86: [2F 적 속도 조사](docs/CART_2F_SPEED_SURVEY.md). 실제 속도 계산과 자동 B 감속 조건을 연결했다. 자연 전체 완주 판정은 별도다.


작업87: [2F B 제거 실험](docs/CART_2F_BRAKE_ATTEMPT.md)을 실패 결과로 보존했다. 전체 클리어 성공이 아니며 실제 충돌 계산을 다음 조사한다.


작업88: [실제2F 충돌 소비](docs/CART_COLLISION_CONSUMER.md).206쌍 속도 교환과 구멍 반대 방향 힘 전달을 확인했다.


작업89: [방향 정렬 A 해제 실험](docs/CART_ALIGNED_RELEASE_ATTEMPT.md)도 전체완주 미달로 보존했다. 추가자동입력 반복보다 번역문맥 검토를 진행한다.


작업90: [원문 수동 검토/후보047](docs/GATE_EDITORIAL_BUILD.md). 성 입구 한 문장을 다듬고 독립 빌드·IPS 적용 검증했다. 실제 장면 검증 전으로 채택본046 유지.


## 작업91 — 성 입구047 실제 출력 검증과 채택

[상세 인계](docs/GATE_EDITORIAL_QA.md).046/047 각5400frames controller-only,396표본 중36대사두행만차이/360전체일치.37폰트PPU/2889메뉴로그/게임RAM nativeglyph쌍과4stackA검증PASS. 실제부분·완성·넘김·다음대사 직접확인,047채택.90재빌드9개 정정/v1검증기경로실패와v2보존. 자연골드4획득/전체완주/047state·reset/사람최종미수행. 다음 작업 하나:047 사람검토HTML/ZIP 및모바일렌더링 갱신.


## 작업92 — 현재047 사람 검토자료

[상세 인계](docs/TRANSLATION_REVIEW_047.md).본문54/그림33/실제14사진/5파일 ROM-free ZIP, 한문장 최신CSV 반영.1280/390 렌더·검색·원문크레딧·현재성입구 DOM PASS, 직접PNG 확인. v1/v2 파일쓰기 전스키마 가정 실패 및v3 해결 보존. 최종사람검토 미완료. 다음 작업 하나:047 xdelta 검토패키지/Windows8적용검사/ZIP재적용.


## 작업93 — 현재047 검토 패치 묶음

[상세 인계](docs/REVIEW_PACKAGE_047.md).ROM-free11파일 xdelta ZIP/Windows apply.cmd8실제검사/최종ZIP재적용047 whole-ROM exact. 도구라이선스·원본·1편·CSV 보존, v1과거상수변경 guard 실패/v2 해결 기록. 정식배포자격false/최종사람검토미완료. 다음 작업 하나:047 골드4·일반50·49 seed분기 회귀와성HUD 확인.


## 작업94 — 현재047 통화seed 입장 회귀

[상세 인계](docs/GATE047_BRANCH_REGRESSION.md).골드4/일반50·49 각046/047 6실행,2096표본쌍 중108대사두행만변경/1988전체같음. 통화seed명시/50차감·49보존·골드4허용, 성실제플레이768표본 전체RAM/PPU/PNG exact 및HUD직접확인. 새ROM없음.다음 작업 하나:047 성입구저장·불러오기/리셋후175176문구회귀.


## 작업95 — 현재047 성 입구 상태/리셋

[상세 인계](docs/STATE047_GATE_REGRESSION.md).같은047 top1920저장/2190불러오기 RAM·PPU·OAM/175176 exact,826키 중sourceOPLL9개외exact. binarycreate전후APU11차이구분. postload현재047기준15파일exact/리셋3000→실제3001/문장재진입RGB4920·6000 PASS.570PNG/4560CHR chunk확인, 새ROM없음.다음 작업 하나:POW61 실제sprite데이터·호출조건 역추적.


## 작업96 — POW 스프라이트 공급 정적조사

[상세 인계](docs/POW_METASPRITE_SUPPLY.md).bank61지정3motif/RAM38→D000 native274cycle, 잠재common191/1910CPU source047 OAM·cycle exact.7descriptor별도해석 exact/정적POW회전후보·깃발3E구분, 실제POW소비는미연결. 과거RAM조건0관측은전역미사용증명아님. 새ROM없음.다음 작업 하나:047 게임오버깃발positive control 실제소비와POW producer추적.


## 작업97 — source61 깃발 positive control

[상세 인계](docs/BANK61_POSITIVE_CONTROL.md).047 baseline/probe8000frames/606PNG·3682native파일 exact. frame3E→0405→9643→OAM83→actualCHR0F420의805프레임,PPU51520행/27실제RGB exact.동반blank와깃발/POW타일구분,POW실제소비미연결. 초깃값티켓4seed명시,새ROM없음.다음 작업 하나:RAM38 direct/computed bank writer와POW 조건역추적.


## 작업98 — bank38 writer/불꽃 후보 구분

[상세 인계](docs/POW_BANK_WRITER_BOUNDS.md).direct15고정값/61은3site,source04730CPU slice exact.마지막장면bank54 constructor/9D..A2counter144case exact로잘못된bank61 POW가설배제.정적설명그림재현byte exact,새ROM없음/전역미사용아님.다음 작업 하나:HOWTO116117/PAUSE120121 bankproducer·nativeNT역추적.


## 작업99 — HOWTO 뱅크와 안내 NT

[상세 인계](docs/HOWTO_BANK_NT_BOUNDS.md).literal bank35 12곳/24 CPU slice와3표 범위, selector10 NT1024셀/128 source047 decoder쌍을 검사했다.116은 장식267셀에 쓰이며 HOWTO90..96은 그NT/역사033 표본에 없다.047 원본후보 보존, 전역미사용 아님. v1..v4 guard실패와 v5해결 보존. 다음 작업 하나:현재047 동일입력 baseline/probe에서bank35·top·label pattern읽기와장식positive control을 연결한다.


## 작업100 — 현재047 HOWTO 장식 positive control

[상세 인계](docs/HOWTO_CURRENT047_QA.md).controller-only baseline/probe4200frames 각각/1658파일·275전체화면 exact. bank35=116→top1060표본·장식tile81 실제읽기16896행/1056프레임·35 sourceRGB exact, label90..96은관측0.뱅크전체미사용아님. fade2표본v1 guard실패/v2해결 보존. 다음 작업 하나:PAUSE120121 나머지CHR shadow 공급/코드·데이터motif 구분.


## 작업101 — PAUSE 공급의 정적 경계

[상세 인계](docs/PAUSE_SUPPLY_BOUNDS.md).rawCHR shadow motif190/인접immediate166에119120121 없음, source고정IRQ7/current고정6그룹 CPU와포트검사. 현재LDXC6 hook은동적소비로구분/v1실패보존.간접animation bank36 공급두곳은미해결,전역미사용아님. 다음 작업 하나:native803C/9362 player/action table과bank36 descriptor값/경계 검증.


## 작업102 — animation bank36 간접표 경계

[상세 인계](docs/ANIMATION_BANK36_BOUNDS.md).bank38의803C 2표×4쌍은font8/9/24,9362 변신2표×7record는12/13/14. native전환42포함source04780 CPU조건쌍/전체RAM·cycles exact.이표PAUSE공급없음/다른창9417구분/전역미사용아님. 다음 작업 하나:sourceC6/C7 IRQ폰트래치 producer와값범위 추적.


## 작업103 — IRQ 폰트 래치 공급

[상세 인계](docs/IRQ_FONT_LATCH_BOUNDS.md).C6/C7 raw5 motif의native2/data2/JMP경계1구분,profile4 producer/source047검사.등록48page×인위prior4=192 init유효font,IRQ96조건쌍52cycles/포트시점동일.legacy003표값v1실패/v2수정보존.해당경로PAUSE공급없음/전역미사용아님. 다음 작업 하나:047 HOWTO/PAUSE/POW 소비근거·미해결범위 ROM없는별도검토보충자료.


## 작업104 — 047 그림 소비 검토 보충자료

[상세 인계](docs/CONSUMER_REVIEW_047_SUPPLEMENT.md).HOWTO/PAUSE/POW3후보·6이미지(현재0472/과거0421/정적3)/ROM없는5파일 ZIP.1280/390렌더·8PNG·실제합성JSON다운로드PASS/JS0,3결정pending·사람승인false. 기존047키트/패치보존. 다음 작업 하나:현재45초안의원문/control/실제문맥대조와단일수정필요여부검토.


## 작업105 — 본문 원문/slot 문맥 검토

[상세 인계](docs/NATIVE_CONTEXT_REVIEW_047.md).원본54raw/48pointer/46main/45개개별수동메모·변수3 placeholder순서검사.57AC는booth15/5920는ride2A로정확한문맥원장정정,ROM/CSV그대로/사람승인false.본검토prose필수수정없음/문체·명칭검토pending. 다음 작업 하나:047 normal3 부족분기 actualFA/F8 숫자·이어가기문맥검증.


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

[상세 결과·해시·재현](docs/NORMAL3_CURRENT047_CLOSEOUT.md), [동결 manifest](manifests/context106_assets.json), `qa/reports/context106_session.json` 종료 감사.


## 작업107 — 현재047 출발 대사와 성공 입장

2026-10-06 재개 지시를 반영했다. 초기 티켓4 seed 명시 후 실제4→0차감, slot2A/9910/font196의 “출발!”과 root4/phase5 플레이 진입을 확인했다. 원본·1편·047 ROM/CSV 보존. 각4200프레임 기본/probe는 공통1820파일/302전체PNG exact, mapped CHR2416조각 exact, 완성NT/RGB53캡처 exact. 실제5PNG assistant 확인/최종 사람승인은 아니다. 페이드색·PNG 이전 필터프레임·2634 latch reset 경계의 검증기 실패4건은 보존/v5해결. 새 빌드/패치 적용 없음. 자연전게임/전역corpus/실기/청음/최종검토는 미완료다.

다음 작업 하나: 현재047 본문·그림·소비경로·자연플레이 미완료 범위를 기존 동결 증거로 정리하고 다음 기술 조사 한 건을 선택한다. 중단 지시가 없으면 이어간다.

[상세 결과·해시·재현](docs/RIDE_SUCCESS_CURRENT047.md).


## 작업108 — 현재047 완료 범위 원장

등록54=45초안+9기술공유, 그림검토33, nativeNT20(selector00..26hex)로서 서로 다른분모임을기록했다. macro원본/현재정의·등록소비와NT원본20SHA/계획SHA/047검토문구일치확인, 기존보고13개와미완료조건8종을연결했다. 전체완료율null/사람승인·전역corpus·자연완주·release_eligiblefalse. 원본/1편/047ROM·CSV보존, 새runtime/CPU/build/apply/직접장면없음. v1문법실패/v2해결보존.

다음 작업 하나: nativeNT20개(selector00..26hex)의실제NT호출/font근거를대조해미연결selector부터누락문구/그림여부판별. 중단지시가없으면이어간다.

[상세범위·변경파일·SHA·재현·검증과한계](docs/SCOPE047_RECONCILIATION.md).


## 작업109 — nativeNT20과8025 관측 범위

원본20stream의pointer/encodedSHA/decode종료·셀수를확인했다. 기존97환경중정상95의1829개정확한8025호출은15selector에연결되며비정상종료2는이분모에서제외/이유보존. 미관측0E/26은별도매표소literal/보너스CHRcopy실제소비가이미있고,14/16은source RAM79>=6 producer쌍,1C는간접공급미폐쇄다. source단순ASCII/호출부재를미사용판단으로삼지않는다. 원본/1편/047/CSV보존, 새runtime/CPU/build/apply/sceneQA없음, v1BCCbyte guard실패/v2해결보존.

다음 작업 하나: fixedD347 RAM79 생산자/호출자와NT14/16의조건부stage진행문맥을역추적한다. 계속진행한다.

[상세근거·해시·재현·검증분류·한계](docs/NT_SOURCE_CONSUMER_047.md).


작업110: 성 NT14/16 조건과 일반 경로에서 건너뛰는 STAGE SELECT 후보를 조사했다. 한정 CPU1024사례/과거047 성 RAM768표본 검증, ROM/CSV 보존. [상세 인계](docs/CASTLE_BACKGROUND_STAGE_ANALYSIS.md). 현재 전체 한글화 완료·배포 승인 상태는 아니다.


작업111: 성 방6의 실제nativeNT14/16·CHR을명시적방전환진단으로검증했다. 원본/047 각4800프레임,107장HUD밖RGB동일, 자연성완주아님. [상세 인계](docs/CASTLE_ROOM6_NATIVE_QA.md).


작업112: source NT20의소비연결은8025관측17/별도실제소비2/미연결1C 한개이며전역unused판정은보류한다. [상세 인계](docs/NT_SELECTOR_SUPPLIER_BOUNDS.md).


작업113: 별도printer의12slot을정리하고STAGE SELECT의한국어후보를원장에보존했다. 실제소비미연결로ROM삽입/등록완료분모추가없음. [상세 인계](docs/NATIVE_COMMAND_PRINTER_CATALOG.md).


작업114:카트88의구멍좌표계산정정과V6실제속도/접촉창을분리해새읽기전용조사근거를얻었다. [상세 인계](docs/CART_CONTACT_MOMENT_ANALYSIS.md). 전체완주미달유지.


작업115:현재047의V6읽기전용충돌관측168쌍CPU/RAM검증. 전체3구간클리어실패유지. [상세 인계](docs/CART_V6_CURRENT047_COLLISION.md).


작업116:실제접촉시계열근거로V7의16프레임방향유지후보를준비했다. 아직실행전/전체클리어미달. [상세 인계](docs/CART_HEADING_HOLD_EXPERIMENT.md).


작업117:V7첫구간통과/전체3구간미달을보존하고유사botstream을닫았다. prefix3PNG예외는raw/core상태동일과분리해다음캡처조사로연결. [상세 인계](docs/CART_V7_CURRENT047_ATTEMPT.md).


## 작업118 — 캡처 프레임 증거 범위

공식 태그의 6소스 Git blob 일치, EndFrame 이후 현재 프레임 제출·비동기 디코딩·캡처 래퍼의 완료 대기 없음·필터 적용/복사 공통 잠금을 확인했다. 예외 3시점의 36파일 SHA와 raw/core 동일·RGB 차이 8/7028/10630을 재확인했다. 정확한 지연량/원인/찢어짐은 미확정이다. 기존107/111의 실제 비교 범위는 유지한다. ROM/CSV/설정 보존, 새 CPU/build/apply/runtime/직접 장면 검증 없음.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/CAPTURE_FRAME_BOUNDS.md).

다음 작업 하나: 기차 간판·HOW TO CONTROL·PAUSE 정적 후보의 CHR 페이지와 native 폰트 공급 코드를 대조해, 소비가 연결되지 않은 후보의 기술적 범위를 정리한다.


## 작업119 — 미연결 NT1C의 후보 타일 경계

미연결 NT1C 99바이트/1024셀을 native803F 디코더 D-clear128조건쌍으로 대조했다. 가정한HOWTO116/PAUSE120 background 배치의 후보 타일과교집합0이지만 실제font·consumer는미연결이다. 기존99..103과104 결정을확대하지않고pending유지. ROM/CSV보존,새runtime/build/apply/직접장면없음.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/NT1C_CANDIDATE_BOUNDS.md).

다음 작업 하나: native bank38의 A5C6→A5FD에서 CHR61과 actor ED를 설정하는 조건·호출 문맥을 연결해, POW 후보와 다른 실제 소비인지 구분한다.


## 작업120 — 강 후반 CHR61 공급

CHR61의세번째literal공급을강course3/bank38/A645→A5C6→A5FD로연결했다.5dispatch·4096constructor·3stageart조건쌍source/047동일.ED/EE/EF는별도course3표로9/2/1sprites이고원본정적그림을직접확인했다.실제후반소비·게임물체명/문구·POW와의동일성은미확정이다.ROM/CSV보존,새runtime/build/apply없음.v1 loadedROM동일가정실패를v2RAM범위로교정/보존.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/RIVER_BANK61_STAGE_SPRITES.md).

다음 작업 하나: 현재047과원본의강phase5에서nativeA5C6직전RAM69=0B/6D=F0만명시적으로주입하는진단으로ED/EE/EF의실제OAM·CHR61읽기·화면을연결한다. 자연후반진행·완주와구분한다.


## 작업121 — 강 후반 조건 실제 진단

원본/047각4000프레임에서nativeA5C6직전69=0B/6D=F0두조건만기록해주입했다.ED생성A5FD/A642각1회·native435행source/current동일이나ED/EE/EF조립·CHR61읽기0으로실제그림소비미연결.047개입전100시점은역사적046 raw400/core100/PNG100same.2실제PNG직접확인,ROM/CSV보존,build/apply없음;자연후반/완주아님.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/RIVER_NATIVE_DIAGNOSTIC_047.md).

다음 작업 하나: 현재047에서같은두조건진단에읽기전용actor2상태쓰기관측을추가해,ED생성후0422/0402를지우는정확한native명령·조건을찾는다. 위치·체력·시간·ROM추가조작없이기존121의동일시점RAM/PPU/OAM/매핑을대조한다.


## 작업122 — 강 actor2 소멸 원인

동일두조건진단+읽기전용write관측으로95BF의artclear및960F/9614→F204/F20C의stateclear를찾았다.121raw620/core155/PNG155·native434행같음.6쓰기CPU쌍/2projection쌍source-current같음.실제viewport차0126/0175가nativeculling을일으켰고합성viewport의64/144는아직표시예측이다.후검증파일명·EndFrame경계실패와문구정정은동결보존.ROM/CSV보존,build/apply/직접장면없음.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/RIVER_ACTOR2_CULL_047.md).

다음 작업 하나: source/current047에서같은native생성뒤9582/actor2투영직전viewport68=01/6B=40/69=0C/6D=80을한번명시적으로주입해,CPU모델의screen64/144예측과실제ED/EE/EF·CHR61소비를대조한다.진단카메라이며자연후반·완주로보고하지않는다.


## 작업123 — 강 ED 실제 소비

원본/047각3300프레임의두조건+viewport4필드한번진단으로ED9sprites/36BOAM→CHR61읽기128행/288회→실제PNG검정opaque518픽셀을연결했다.사람승인/자연후반아님.122좌표축라벨정정(X144/Y64).50캡처상단0..189같으나기존HUD제외비교는하단235/236차이로50모두실패/범위분리.ROM/CSV보존,새build/apply없음.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/RIVER_ED_ACTUAL_CONSUMER_047.md).

다음 작업 하나: 원본/현재047의같은진단에서화면하단235/236의실제PPUpattern읽기·매핑·NT/scroll을추적해,HUD밖차이를정확한소비에연결한다.ROM/CSV변경전에원인을확인한다.


## 작업124 — HUD 하단 두 줄의 배치 확인

원본/047각3300프레임의동일6필드진단+읽기전용render3032하단PPU1190행으로font124/206의공백20→다음NT빈00전이를확인했다.동일pattern340행의2scanline이동·독립RGB3584픽셀일치.기존040HUDy190..239/fineY2→0의의도된여백이동으로123의너무좁은190..217비교범위를설명했고ROM/CSV수정없음.자연전체/사람승인아님.

[상세 결과·변경 파일·해시·검증 구분·한계](docs/HUD_FOOTER_SHIFT_047.md).

다음 작업 하나: 등록45본문초안을일본어원문·정확한장면105·현재삽입계획과수동대조해의미/용어/높임말을검토한다.실제수정이필요한문장만별도근거와함께선별하며사람최종승인을자동부여하지않는다.


작업125: [본문 충실도 검토](docs/PROSE_FIDELITY_REVIEW_125.md), 단일 shortage문장 개발수정 선택/047·CSV 보존/최종사람승인false. 다음: MAIN_0590C 한 문장만 별도226/227 폰트를 사용하는 새048 후보로 삽입하고 원본 쓰기 범위·native timing·재빌드/적용을 검증한다.


작업126: [048 부족 대사 후보](docs/SHORTAGE_EDITORIAL_BUILD_048.md), 단일초안·전용폰트/build/apply통과, 실제QA전에는047채택유지. 다음: 047/048을 동일한 일반티켓3 seed·입력으로 실행해 slot29의 부분출력·완성·넘김·다음2B 보유량 대사에서226→196 복귀와 보호화면을 검증한다.


작업127: [048 실제전환거부](docs/SHORTAGE048_LIFETIME_REJECTION.md), 완성정상만으로채택하지않음/clear전글꼴혼합/채택047. 다음: slot29/2B의 native clear 전에는 활성폰트를 유지하고06DF03 초기화 때 새폰트를 선택하는049 후보를 만들며 CPU경로별 사이클/ABI를 검증한다.


작업128: [049 clear후font선택](docs/LOWER_FONT_POST_CLEAR_049_BUILD.md), CPU/build/apply완료·실제QA전후보/채택047. 다음: 049 실제부족3·성공4 입장과다른page경로를같은입력으로실행해 native clear 전후의글꼴수명·타이밍·의도밖픽셀/상태변화를검증한다.


작업129: [049 actual branch QA](docs/LOWER_FONT_POST_CLEAR_049_BRANCH_QA.md), 글꼴혼합해결·성공302화면same/RAM22차이구분·다른pageQA전후보. 다음: 049의 타이틀/9도입문단·홈선택/매표소·성입구·크레딧을동결된각기준실행과대조해 global helper 회귀를검증한뒤개발채택여부를결정한다.


작업130: [개발049채택](docs/DEVELOPMENT049_PAGE_REGRESSION.md), 1503전체화면same/idleRNG·microPC차이구분·최종사람승인false. 다음: 채택049의단일본문수정·새실제화면·검증한계를반영한ROM없는검토자료를새폴더에작성하고047자료는역사본으로보존한다.


현재049 [검토자료131](docs/TRANSLATION_REVIEW_049.md): ROM없는ZIP·PC/모바일 검토 HTML 갱신. 사람최종승인false.


현재049 [ROM없는개발패치132](docs/REVIEW_PACKAGE_049.md): Windows 실제적용·ZIP재적용확인, 최종배포승인false.


[049状態133](docs/STATE049_SHORTAGE_REGRESSION.md): 전용부족글꼴의동일빌드저장·복원/리셋한정검증.


[실측134](docs/LIVE049_PAGE_TIMING_BOUNDS.md): page38순수cycle/첫42경과와부족IRQ17시각차이를분리기록했다.


[처음홈DMC/경계정정135](docs/HOME049_DMC_WAIT_BOUNDARY.md): 두빌드같은4cycle DMC대기위치만이동,완전한실제호출차이38.


[부족IRQ136](docs/SHORTAGE049_IRQ_ENTRY_BOUNDS.md): 1cycle차이는handler전대기부터존재,IRQ상대명령시간같음.


[idle DMC137](docs/SHORTAGE049_IDLE_DMC_ALIGNMENT.md): IRQ이전시점차이를실제DMC정렬에연결,소비바이트보존/4읽기±2cycle은한계로유지.


[登録원천 검증138](docs/COVERAGE049_REGISTERED_SOURCES.md): 현재/역사 증거를 구분하고 gold4 성의현재049 미실행분기를 선택.


[성 gold4 현재049 검증139](docs/CASTLE049_GOLD4_BRANCH.md): 신규slot1C현재완성및성진입,786화면일치.


[성 normal50 현재049 검증140](docs/CASTLE049_NORMAL50_BRANCH.md): 일반50→0 진입·786화면일치.


[매표소 성공049 검증141](docs/BOOTH049_SUCCESS_READER.md): 티켓10→11/실제PRG reader/slot15 문장 완성과 지도 복귀 확인.


[기차049 검증142](docs/TRAIN049_NATIVE_READER.md): 실제reader·요금2·title/rules/depart/초기플레이·지도복귀.


[급류049 검증143](docs/WATER049_NATIVE_READER.md): 실제reader·요금3·title/rules/depart/초기플레이·지도복귀.


[인트로049 실제reader144](docs/INTRO049_NATIVE_READER.md): 전체9문단의실제원천byte·완성NT·직접9PNG·2순환.


[등록54 현재증거145](docs/COVERAGE049_SOURCE_EVIDENCE_REFRESH.md): main46presence/reader31/새완성NT16의서로다른범위.


[쇼킹 카트049 실제reader146](docs/CART049_NATIVE_READER.md): 짧은메뉴·요금1·출발·첫구간;완주bot은닫힘.


[롤러코스터049 실제reader147](docs/COASTER049_NATIVE_READER.md): 짧은메뉴·요금4·출발·첫구간;완주bot은닫힘.


[오늘 세션 종료148](docs/SESSION_STOP_148.md): 사용자중단지시·현재049보존·미완료성reader자료보존·재개지시대기.


[현재049 성 입장 실제읽기149](docs/CASTLE049_SOURCE_READER_RESUME.md): 중단148 보존·재개 검증.


[不足대사 실제읽기150](docs/SHORTAGE049_SOURCE_READER.md): 전용226/227과지우기수명확인.


[등록원천 실제읽기 재평가151](docs/READER049_REASSESSMENT.md):49개읽기·미연결5, 전체게임완료율아님.


[급류 입력·진행 모델152](docs/WATER_NATIVE_PROGRESS_MODEL.md): 점프와물에빠짐·완료조건분리.


[급류첫점프 관측153](docs/WATER_FIRST_JUMP_NATIVE_QA.md): 점프연결·피해조건은다음관측.


[급류 실제피해154](docs/WATER_ACTUAL_DAMAGE_CONSUMER.md): 장애물충돌주소·회피CPU조건.


[급류 점프착지155](docs/WATER_HAZARD_JUMP_LANDING_FAILURE.md):첫충돌회피/재착지실패분리.


[급류회피/착지156](docs/WATER_AIR_STEERING_LANDING.md): native속도모델+실제초기경로.


[급류 후반 회피157](docs/WATER_ADAPTIVE_ACTOR_AVOIDANCE.md): 객체 피해0, 자연clear 실패 및 입력시점 미해결.


[급류실패/입력/축정정158](docs/WATER_EXIT_INPUT_AXIS_CORRECTION.md): RAM69/6D=cameraX, 실제phase09 분기.


[통나무 B 조작과 다음 통나무 연결159](docs/WATER_RAFT_CONTROL_AND_TRANSFER_MODEL.md): 84기울기/21속도CPU쌍. 실제다음raft가78px 앞에 존재.158 경계 표기32→16 정정.


[첫 자연 통나무 갈아타기160](docs/WATER_FIRST_NATURAL_RAFT_TRANSFER.md): 3985 A→4035 native교체/4050 착지.6500까지진행,새물고기피해2회·체력1·clear없음.


[물고기 중력과 통나무교체 실제소비161](docs/WATER_FISH_AND_SWAP_NATIVE_CONSUMERS.md): 같은입력/스냅샷,181최종쓰기+12중력CPU쌍.물고기Vy+32/step,통나무INC0716 실제PC 연결.


[첫 물고기 회피와 두 통나무 교체162](docs/WATER_FISH_PREDICTION_FIRST_RESULT.md): 첫물고기회피/두갈아타기관측.착지flag128에서다음물고기2회피해·새type21피해로체력0.


[A 유지 회피와 자연 후반구조물163](docs/WATER_HELD_A_AND_NATURAL_TOWER.md): A20으로세물고기피해없음.2갈아타기/type21피해1/자연towertype2도달,8603좌표실패.4410 PNG차이로전체영상동일FAIL.


[자연 손잡이 소비 조건164](docs/WATER_ROPE_CAPTURE_NATIVE_MODEL.md): type2=로프/손잡이.48CPU쌍 nonnegativeVy·충돌→C9/0541을검증,실제붙잡기는다음.


[실제 플레이 사용자 이관·잔여 정리165](docs/ACTUAL_PLAY_USER_HANDOFF_AND_REMAINDERS.md): 사용자 실제플레이담당.자동플레이종료/165자료보존/ROM·CSV불변.비플레이 잔여6종 정리.


[현재049 원천 전수 목록·미연결 후보 통합166](docs/CURRENT049_NONPLAY_SOURCE_INVENTORY.md): 등록54본문·33그림, 원본CHR128뱅크와NT20/별도프린터12슬롯 정적 대조. 후보7건 보존·미연결 유지. ROM/CSV 불변.


[현재049 비플레이 통합 검토 묶음167](docs/CURRENT049_NONPLAY_REVIEW_PACKAGE.md): 54원천·33그림·후보7건, 기존실제21/정적4그림 통합.049 state/reset 근거·사용자 플레이 담당·163 RGB실패 표시. PC/모바일/ZIP PASS; ROM/CSV 불변.


[최신 검토용 패키지·사용자 검수 안내168](docs/CURRENT049_REVIEW_PACKAGE_AND_USER_QA_GUIDE.md): 동일049 패치/도구 보존, 최신 한계·검수 안내·비플레이 검토자료 포함한20파일 ROM없는ZIP. 최종ZIP 한글/공백경로 실제Windows적용 byte-exact PASS. 플레이 실행 없음.


[보존 범위 확정·PUSH START 타이틀 소비 연결169](docs/SCOPE_RETENTION_AND_TITLE_PROMPT_CONNECTION.md): 사용자HOWTO/PAUSE/POW 원문유지확정.별도PUSH START는기존타이틀sprite8E/CHR63 소비에연결. 발견7중3보존승인+1기존보존연결+3미해결. ROM/CSV불변.


[범위 결정 검토자료 갱신·오늘 작업 중단170](docs/SESSION_STOP_20261007_SCOPE_REVIEW.md): 사용자 오늘마감으로중단·자동재개없음.최신170검토는HOWTO/PAUSE/POW 원문유지확정과PUSH START소비연결반영.PC/모바일/ZIP PASS.ROM/CSV불변.168적용묶음 범위문서갱신은재개후.


[원문 보존 결정 반영·최신 적용 패키지171171](docs/CURRENT049_SCOPE_APPLY_PACKAGE_171.md): 사용자 재개.169보존3/타이틀연결1/미연결3와검토170을21파일ROM없는ZIP에동기화. 최종ZIP한글/공백실제Windows적용 byte-exact PASS. ROM/CSV불변·게임실행없음.


[미연결3원천 현재 근거·범위 선택지172](docs/CURRENT049_REMAINING_THREE_SCOPE_OPTIONS.md): RYO51/NT1C/진단STAGE SELECT 현재049 코드/원천보존과한계를분리.원문유지/소비조사후번역 선택지준비·결정pending.171의옛외부스킬캐시링크누락을별도보고/내부자산감사PASS. ROM/CSV불변.


[보존6건 확정·검토/실제적용 반영173](docs/CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md): 사용자 결정으로 발견7건의 범위 미결정0(명시보존6+기존타이틀연결1). 검토173 PC/모바일·25PNG·54/33·최종23파일ZIP 실제Windows적용 PASS. ROM/CSV불변; 플레이 사용자 담당.


[기존PNG 차이 오프라인 출처 대조174](docs/CURRENT049_OFFLINE_CAPTURE_PROVENANCE_174.md): 종료162/163의343쌍PNG/4410raw5쌍/입력4644행·공식소스6개 재대조. 저장인접PNG동일복사본없음.7326픽셀/전체RGB FAIL·원인미확정 유지; 새게임실행없음.


[현재049 사용자 검수 연결·잔여조건 정리175](docs/CURRENT049_USER_REVIEW_READINESS_175.md): 검수표12항목/빈응답양식·최종판단/증거공백·수정→검증→카페작업기 순서정리. 확인한기록의새수정요구없음; 전체완료/전역corpus/사람승인아님.173ZIP/ROM/CSV불변.


[사용자 티켓교환 대사 깨짐 재현·진단176](docs/BOOTH_EXCHANGE_FONT_COLLISION_176.md): 사용자자연신고를동일2.2.1격리host/복사상태로재현. 정상MAIN05782 NT가162대신196폰트에표시됨. 상단F9 slot23 초기화가하단폰트를덮는결함등록; 수정전.


[티켓교환 폰트충돌 수정050 채택177](docs/BOOTH_EXCHANGE_FONT_FIX_050_177.md): 사용자신고의 교환숫자갱신 폰트충돌을050에서수정.53,760 CPU사례·독립재빌드·네분기 paired1116실제화면/상태 PASS.050채택, 전체플레이/최종사람검수는별도.


[수정050 ROM없는 적용묶음·실Windows 검증178](docs/BOOTH_FIX050_APPLY_PACKAGE_178.md): 050수정ZIP 준비. 실Windows helper8+최종ZIP적용 byte-exact/ROM-free PASS.049검토는역사자료로보존, 현재사용자Mesen/세이브는수정하지않음.


[티켓교환 수정050 최종 인계·자산감사179](docs/BOOTH_FIX050_FINAL_RECONCILIATION_179.md): 050수정/178ZIP/current인계 대조 완료.177의13,514자산·178의35자산/원본·1편/로컬링크PASS. 실제전체플레이/최종사람검수는사용자담당.


[상태창 왼쪽·아래 원본비교 조사180](docs/HUD050_LEFT_BOTTOM_SOURCE_COMPARISON_180.md): 원본에도왼쪽8픽셀배경색띠/창아래검은20픽셀여백존재. 실제source/0507HUD시점·PPUMASK1896행동일.44의한글높이용2픽셀shift는구분;ROM/패키지변경없음.


[움직이는 STOP 별도소비 진단181](docs/MOVING_STOP_CONSUMER_DIAGNOSIS_181.md): 고정정지와다른CHR46 스프라이트원문 STOP 확인. 사용자HUD 전놀이기구관측은별도기록. 잘못된CHR22 추정/host가드실패/다른카트세이브 관측을보존했다.


[움직이는 STOP 한글화051·동일조건 검증182](docs/MOVING_STOP_GLYPH_FIX_051_182.md): 051채택:CHR46 58바이트 글자만정지로수정.734 paired화면/상태 exact;90화면 글자픽셀만변경,644전체화면동일.독립ROM/IPS재빌드PASS.


[수정051 ROM없는 적용묶음·실Windows 검증183](docs/MOVING_STOP051_APPLY_PACKAGE_183.md): 051 움직이는STOP 수정ZIP 준비.실Windows8사례와최종ZIP적용 byte-exact/ROM-free PASS.원문유지6건및050티켓교환수정보존.


[051 최종인계·이전자산 보존 감사184](docs/MOVING_STOP051_FINAL_HANDOFF_AUDIT_184.md): 177..183고정자산해시/원본·1편/로컬링크 PASS.사용자적용050 보존,현재051+ROM-free ZIP183 인계.새플레이검수는사용자담당.


[전체텍스트11px 정적가능성·배치후보185](docs/GLOBAL_TEXT11_FEASIBILITY_185.md): 요구를전체텍스트11px로정정.현재8×8 출력은그대로대체불가;12×16셀/192px16칸/4줄3KiB 정적후보와PNG 비교작성.실제ROM/CPU/PPU검증전이며051 보존.


[오프닝 9문단 11px 전용 출력·빌드186](docs/OPENING11_PAIRED_ROW_POC053_BUILD_186.md): 오프닝9문단053 삽입·독립ROM/IPS재빌드·최종6502 PASS. 기존051/번역CSV/다른화면 유지; 실제표시검증은187에서 분리.


[오프닝11px 실제9문단·반복·분기 검증과 오늘중단187](docs/OPENING11_POC053_RUNTIME_HANDOFF_187.md): 오프닝053의9문단3회/2167RGB/3024상하소비/30지우기 PASS. Start분기·734기차화면회귀 PASS. 오늘중단;053적용ZIP·전체11px전환 미실시.


[오프닝11px PoC053 적용패키지·Windows 검증188](docs/OPENING11_POC053_APPLY_PACKAGE_188.md): ROM없는053패키지·Windows8사례·최종ZIP실적용 byte-exact PASS. 오프닝전용범위·9문단비교·폰트라이선스포함;기준051유지.


[오프닝053 패키지·고정근거·재개표지 감사189](docs/OPENING11_POC053_PACKAGE_EVIDENCE_AUDIT_189.md): 185~188고정해시·원본/1편/프로젝트링크 PASS. 외부과거캐시1건분리. 기준051/오프닝053 구분해전체11px설계준비.


[전체11px 다음출력기·변수·공유폰트 용량계획190](docs/GLOBAL_TEXT11_NEXT_CONSUMER_PLAN_190.md): 45draft를출력경로별로분리.42정적배치/FA6course/F8CPU1000숫자수요/공유font합집합 계산.다음홈한줄PoC;새ROM/실제실행없음.


[홈한줄11px 후보054·원본빌드·CPU 검증191](docs/HOME11_SINGLE_LINE_CANDIDATE054_191.md): 홈root8/168px/5행소거경계로054한줄후보제작.ROM/IPS독립동일·42상하/110소거·778fallbackCPU PASS.054실제실행미수행·미채택.


[홈실행뱅크 판정정정·오프닝6문단 조정요청192](docs/HOME11_CONSUMER_AND_PAGE6_LAYOUT_CHOICE_192.md): 기존049읽기와053동등범위로physical18홈소비연결.054실제미검증유지.사용자문단6줄바꿈/서명오른쪽정렬을다음작업으로전환.


[오프닝6문단 줄바꿈·서명우측정렬 PoC055193](docs/OPENING11_PAGE6_USER_LAYOUT_POC055_BUILD_193.md): 사용자지정문단6배치반영055.053대비508바이트/코드·제어위치·다른8문단불변.원본/IPS/독립ROM·최종CPU PASS;실제194분리.


[요청6문단 배치055 실제표시·반복·소거 검증194](docs/OPENING11_PAGE6_LAYOUT_POC055_RUNTIME_194.md): 055요청6문단실제정렬확인.9문단3회/2167RGB/3024상하/30소거 PASS.053비교2086전체동일·232문단6영역만변경.


[요청6문단 조정055 패키지·Windows 실적용195](docs/OPENING11_PAGE6_LAYOUT_POC055_PACKAGE_195.md): ROM없는055사용자배치조정판·Windows8/최종ZIP실적용 exact PASS.053/055동일프레임비교·라이선스포함;054미포함.


[요청6문단 수정055 패키지·근거·최신 인계 감사196](docs/OPENING11_POC055_CURRENT_HANDOFF_AUDIT_196.md): 6문단 줄묶음·오른쪽 서명055 검증/패키지 완료. 188~195 고정 해시와 원본/1편 보존 PASS. 기준051·최신 오프닝055·홈054 CPU후보를 구분했다.


[그림 글자 제외·문자열11px 확대 범위와 제약197](docs/TEXT11_SCRIPT_SCOPE_AND_FEASIBILITY_197.md): 사용자 범위를 문자열 출력기로 고정. 오프닝9/일반33/크레딧3 구분. HUD·정지 등 그림 유지, 다음 홈·매표소12개.


[홈·매표소12개 후보056 비대상CPU 플래그 실패 기록198](docs/HOME_BOOTH11_056_REJECTED_CPU_FLAG_198.md): 056 독립 빌드 동일, 점진/즉시 출력 검사 후 비대상V flag 차이로 거부. 후보·실패 증거 보존, 미채택·미패키지.


[홈·매표소12개11px 후보057 점진/건너뛰기 CPU 검증199](docs/HOME_BOOTH11_CANDIDATE057_TYPED_SKIP_CPU_199.md): 055기반12개11px057.352 skip/4320 init/1556 fallback/050 retention/원래5행clear PASS. 독립ROM·IPS exact, 새실제 실행 없음.


[홈·매표소11px057 개발 후보 패키지·Windows 실적용200](docs/HOME_BOOTH11_CANDIDATE057_APPLY_PACKAGE_200.md): ROM 없는 CPU후보057 패키지, Windows8/최종ZIP 실적용 exact PASS. 실제057 실행 미수행을 명시, 정적PNG/라이선스 포함.


[남은 일반21개·크레딧3개 확대 설계와 숫자 용량 해결안201](docs/TEXT11_REMAINING_NUMERALS_CARDS_CREDITS_DESIGN_201.md): F8 1000값 숫자3000자리 고정타일 분리,175→54/128. 상단10페어·보유254/255 저장안, 크레딧144/128·긴커서/전송 재설계 필요. 새ROM/실행 없음.


[크레딧11px 영문 간격 대안·106타일 왕복202](docs/CREDITS11_SHARED_FONT106_SPACING_OPTION_202.md): 같은 글자 모양·문구 보존. 영문16px 간격이면144→106/128,2KiB 직렬화3문단 픽셀exact. 미채택 정적안, 긴커서/전송/실제스크롤 남음.


[일반33개 후보058 단독CPU 성공·공유창 결함 거부203](docs/ORDINARY11_058_ISOLATED_CPU_CARD_REJECTION_203.md): 단독33문단/F8/FA/skip/초기화CPU PASS이나 제목·규칙 동시거주와 실제160/184px 창기하 결함 발견.058 미채택·미패키지.


[일반33개11px059·카드 글꼴공유/이름칸 수정·최종CPU204](docs/ORDINARY11_CANDIDATE059_CARD_COEXISTENCE_CPU_204.md): 42등록문단 후보(오프닝9+일반33).F8천값/FA6×2/1071skip/4320init/1556fallback/5쌍 카드공유 PASS.160/184px·이름 테두리 수정.새059 실행 없음.


[059 첫 적용 패키지 크기 검증 실패 보존205](docs/ORDINARY11_PACKAGE059_SIZE_GUARD_FAILURE_205.md): ROM059는 그대로이며 적용 도구의 이전499728바이트 검사 때문에 첫 Windows 적용 실패. 부분 패키지/QA를 보존하고 새206으로 수정한다.


[일반대사11px059 개발 후보 패키지·Windows 실적용206](docs/ORDINARY11_CANDIDATE059_APPLY_PACKAGE_206.md): ROM 없는 CPU후보059 패키지, Windows8/최종ZIP 실적용 exact PASS. 실제059 실행 미수행을 명시, 정적PNG/라이선스 포함.


[059 확대 후보 정본 인계·고정 근거 감사207](docs/TEXT11_CANDIDATE059_CURRENT_AUDIT_207.md): 197~206 고정근거·2편 원본/CSV·프로젝트 링크 PASS.1편 참조5개 해시 일치/역사 원본 경로1개 현재 없음.059 CPU/적용 후보42개11px,실제미수행,크레딧3개8px.


[크레딧11px 원래16px 기하·전송 큐 설계208](docs/CREDITS11_NATIVE_GEOMETRY_AND_QUEUE_DESIGN_208.md): 원래 줄 간격16px.첫2D244바이트 큐/스택 충돌 위험으로 직접 화면출력 중지 전송을 설계,2E/2F는 원래호출수·최대62바이트 이벤트로 분할. 아직 ROM/실행 없음.


[크레딧 확대060 빌드·중복 뱅크저장 CPU 거부209](docs/CREDITS11_CANDIDATE060_MAPPER_REJECTION_209.md): 060 독립빌드 exact이나 일반대사CPU에서 복귀태그08 남음: 공통/기존GUARD 중복FDD3 원인.060 미채택·미패키지,059 유지.


[061 private복귀주소·대기값 CPU 거부210](docs/CREDITS11_CANDIDATE061_RETURN_AND_DELAY_REJECTION_210.md): 061 일반CPU의미복제post-FDDB주소/크레딧58초기화결함 발견. 실패·빌드보존,059 유지.062 mirrored복원 및delay수정 예정.


[062 등록45개11px 빌드·CPU·정적 복원211](docs/TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md): 오프닝9+일반33+크레딧3 전등록45개11px 후보062.독립빌드/기존42CPU/크레딧327호출·4000frame동기CPU PASS.작은그림보존,실제062 미수행·미채택.


[062 등록45개11px 개발 적용패키지·Windows 실적용212](docs/TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md): 062 ROM없는 개발ZIP/Windows8/최종ZIP실적용 exact PASS.45문자·5모형·CPU·라이선스포함.실제062미수행·미채택,작은그림보존.


[062 등록45개11px 정본 인계·고정 근거 감사213](docs/TEXT11_CANDIDATE062_CURRENT_HANDOFF_AUDIT_213.md): 197~212 해시·2편원본/CSV·프로젝트링크 PASS.062 등록45개11px CPU/재빌드/적용후보·실제미수행·미채택.1편역사원본경로1개누락별도기록.


[불필요한 펼친 산출물·캐시 정리와 검증 보관214](docs/PROJECT_CLEANUP_ARCHIVED_HISTORY_214.md): 펼친 과거자료·캐시 1,004,563개 정리, 순 파일 바이트 7.48GiB 절감. 과거 바이트는 전수검증 압축보관, 원본·원천·051·062·링크 유지. 복원검증PNG1개는 직접삭제 정책차단으로 남음. 실제 플레이 없음.


[062 즉시출력 두 문단의 조건부 NMI 전송예산 초과215](docs/TEXT11_NMI_PREFIX_BUDGET_215.md): 062 CPU prefix에서1E/20 즉시출력 NTSC 기준초과(최대2319). 실제 화면/IRQ/DMC 미검증.062 보존,별도063 native언롤 큐 개선 준비.


[실제062 출력 진입점 NMI 검증·215 판단 정정216](docs/TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md): 215는fallback직접호출로오판·철회.실제062 full231/skip1071 prefix초과0,명목여유44cycles.063없음·ROM/CSV동일·실제미검수.


[일반 대사33개 IRQ 경계 주입·복귀 CPU 검증217](docs/TEXT11_IRQ_INJECTION_217.md): 66출력 상태·62,940 IRQ 주입 PASS, 중간 은행66회 출력 완료 동일.051과 콜백 동일.062 불변·실제 검수 남음.


[오프닝·크레딧 IRQ CPU 검증과 재개 인계218](docs/TEXT11_OPENING_CREDITS_IRQ_218.md): 852출력 호출·149,824 한정IRQ 주입 PASS. 재개 총212,764주입.062/패키지 불변·실제 검수 대기.


[IRQ 인계 스택 여유 수치 정정219](docs/TEXT11_IRQ_STACK_GAP_CORRECTION_219.md): 217/218 문서의 스택 여유를 CPU 보고와 같은48/49바이트로 정정. 검사/ROM/패키지 불변.


[최종배포 v1.0 빌드·ROM없는 적용패키지220](docs/RELEASE_V1_0_BUILD_PACKAGE_220.md): 062 exact데이터 v1.0/ExpectedWrites/독립재빌드/Windows8/최종ZIP 적용 PASS.실제062 플레이검수 미기록.


[네이버 카페 업로드용 작업기·8PNG·HTML221](docs/NAVER_CAFE_WORKLOG_V1_0_221.md): 카페복사용글/8PNG/내장HTML/ROM없는ZIP13파일·CRC/desktop/mobile/zoom PASS.게임검수·실제게시 미수행.


[과거 QA·중간물 손실 없는 정리222](docs/LOSSLESS_RELEASE_CLEANUP_222.md): 정확 경로 정리 완료.214/222 보관 SHA와 실제 복원 통과.원본·현재 빌드·재현원천 보존.


[이전 배포 묶음 정리223](docs/SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md): 이전 묶음199파일을 SHA·CRC 확인 보관 후 삭제.212 재현입력과 현재 배포 유지.


[사용자062 1차완주 검수 반영 최종배포224](docs/FINAL_RELEASE_USER_FIRST_QA_224.md): 사용자062 실화면·완주1차완료보고 반영.데이터불변·14파일ROMfree·최종ZIP 실제적용 PASS.배포후검증예정.


[사용자1차 검수 완료 반영 카페 작업기225](docs/NAVER_CAFE_FINAL_USER_REVIEW_225.md): 1차실화면·완주 완료/배포후검증예정 반영.8PNG·13파일ROMfree·desktop/mobile/zoom PASS.


[최종 배포·작업기·정리와 인계 완료226](docs/FINAL_DELIVERY_CLEANUP_226.md): 062 사용자1차화면·완주 완료 보고 반영.최종2ZIP·실제적용·작업기렌더 PASS.순약2.32GiB 정리·배포후검증 예정.


[1·2편 NES 한글화 기술 지침과 게시자료227](docs/TINYTOON12_TECHNICAL_GUIDE_227.md): 1·2편 기술지침15항목+자료참조·설명도2·ROM없는예제/8파일ZIP.전체Page읽기동일·HTML PC/모바일·예제 PASS.


## 공개 작업기·기술 지침 독자용 개정 — 작업228

내부 빌드 번호를 본문·비교 이미지·캡션·공개 출처에서 제거했다. 목적과 수정 전/후로 다시 설명했으며 두 리더의PC/모바일·ZIP검사가 통과했다. 게임 배포·번역·사용자1차 검수 상태는 같다. [상세 변경·해시·검증](docs/PUBLIC_ARTICLE_READER_REVISION_228.md).

다음 작업 하나: 사용자가 수정된 작업기·기술 지침을 게시하고, 배포 후 제보의 ROM 해시·환경·직전 행동·장면을 수집한다.


## 작업229 — 카페 작업기 작성자 말투 적용

사용자도입부·어린시절경험·엔딩소감을살리고전체본문과이미지설명을게시판1인칭말투로개정했다. 내부빌드번호없는상태와기술범위·검수구분유지. HTML PC/모바일·확대·ZIP전수검사PASS. [상세 인계·SHA·재현](docs/CAFE_WORKLOG_AUTHOR_VOICE_229.md).

다음 작업 하나: 사용자가 본문·그림을 카페 편집기에 배치하고, 배포 이후 제보의 ROM 해시·환경·직전 행동·화면을 수집한다.


## 작업230 — 불필요한 이전 게시자료·검토본 정리

20대상90파일을private230보관으로전수검증후삭제했다. 최신게임배포·작성자작업기·기술지침과보존4713파일SHA확인PASS. [변경·해시·검증·복원](docs/SUPERSEDED_PUBLICATION_CLEANUP_230.md).

다음 작업 하나: 사용자가 최신 작업기·기술 지침과 최종 릴리즈를 게시하고, 배포 이후 제보를 수집한다.
