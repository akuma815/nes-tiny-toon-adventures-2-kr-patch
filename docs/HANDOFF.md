> 최신 재현 보완: [HANDOFF_2026-10-16.md](HANDOFF_2026-10-16.md) 및 [REBUILD_RELEASE.md](REBUILD_RELEASE.md).

> 최신공개자료: [게임배포](../dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip) · [작성자작업기](../workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html) · [기술지침](../workspace/publication/TinyToon12_TechnicalGuide_Reader_20261009/기술_지침.html). 이전게시자료·QA·중복재빌드는 [230보관·복원안내](SUPERSEDED_PUBLICATION_CLEANUP_230.md)를따른다.

# 최종 배포·게시자료 유지 및 불필요 파일 정리 완료 — 2026-10-09

[1·2편 한글화 기술 지침 Page](https://chatgpt.com/space/page_7e1e9fe45f1881918ff36b3962ea16c0)와 [게시자료 ZIP](../dist/TinyToon12_TechnicalGuide_Reader_20261009.zip)을 추가했다. 기존 게임 배포파일과062 검수 상태는 그대로다. [기술지침 인계](TINYTOON12_TECHNICAL_GUIDE_227.md).

**v1.0은062와 같은 데이터입니다. 사용자가 실제 화면·완주1차 검수를 완료했다고 보고했으며, 배포 이후 추가 검증이 필요합니다.** 새 게임 실행이나 실제 카페 게시를 수행한 것은 아닙니다. 아래 역사 기록의 ‘미검수·미채택’은 추가 사용자 보고 전 당시 상태입니다.

- [최종 배포 ZIP](../dist/TinyToonAdventures2_KR_v1.0_Release_20261009.zip) — ROM 없음,14파일,실제 Windows 적용 결과062와 완전히 같음.
- [네이버 카페 작업기 ZIP](../dist/TinyToon2_KR_Worklog_AuthorVoice_20261009.zip) — 본문·안내·8PNG·HTML,ROM 없음.
- [오프라인 작업기](../workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/작업기.html), [카페 복사용 본문](../workspace/publication/TinyToon2_KR_Worklog_AuthorVoice_20261009/카페_복사용_본문.txt).
- [로컬 최종 ROM](../build/release_v1_0_220/TinyToon2_KR_v1.0.nes),SHA `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`.
- [사용자1차 검수 보고](../qa/reports/user_review224.json), [최종 감사](../qa/reports/final_delivery226_audit.json), [최종 인계](FINAL_DELIVERY_CLEANUP_226.md).

독립 재빌드·ExpectedWrites·ROM/IPS 비교, Windows 적용 사례와 최종ZIP 실제 적용, 한정 CPU/NMI/IRQ 검사 및 작업기PC/모바일/확대 확인은 통과했습니다. 실제 화면·완주1차 완료는 사용자 보고로 구분합니다. 배포 후 검증 결과는 아직 없습니다. 등록45문단(오프닝9·일반33·크레딧3)은 전게임 발견률100%를 뜻하지 않습니다. HUD·정지 그림의 크기와 원문 유지6원천은 사용자 결정대로 유지했습니다. CSV 행별 상태를 사람 검토 완료로 일괄 변경하지 않았습니다.

불필요한 과거 QA·이전 공개ZIP·임시 적용 사본·렌더 캐시를 손실 없는 보관/정확 경로 삭제로 정리했습니다.222/223/226 합계110,831파일,순약2.32GiB 절감. 원본·번역원천·재현 스크립트·최종산출물·QA근거는 보존했습니다.214/222는 SQLite 보관,223/226은 ZIP 보관이며 private 보관본은 공개하지 않습니다. [222복원](LOSSLESS_RELEASE_CLEANUP_222.md), [223복원](SUPERSEDED_DISTRIBUTIONS_CLEANUP_223.md), [226복원](FINAL_DELIVERY_CLEANUP_226.md).212/220 패키지 및003 작업기 폴더는 재현 입력입니다.

**다음 작업 하나: 사용자가 최신 작업기·기술 지침과 최종 릴리즈를 게시하고, 배포 이후 제보를 수집한다.** [오늘 인계](HANDOFF_2026-10-09.md), [오늘 journal](journal/2026-10-09.md), [계획](LOCALIZATION_WORK_PLAN.md).

---

## 이전 작업 당시의 역사 기록

# 진행 중 — 2026-10-09, 작업226 완료

**작업219 인계 수치 정정:** 217/218 보고의 큐 뒤 스택 범위 여유48/49바이트가 정확하다. 문서의47/48 표기는 [219정정](TEXT11_IRQ_STACK_GAP_CORRECTION_219.md)을 따른다. 검사와ROM은변경없다.

**작업218 재개 검증:** 실제 진입점 NMI prefix와 일반대사·오프닝·크레딧의 한정 IRQ CPU 검사를 마쳤다. 원본/CSV/051/062/IPS/ZIP은 불변이며062는 실제 검수 전 개발 후보다. [검증 범위·남은 실제 확인](TEXT11_OPENING_CREDITS_IRQ_218.md).
**작업216 정정:** 215의96FC 직접호출은현재등록11px 진입점이아니어서초과판단을철회했다. 실제925E→9690→B400의전체231/부분skip1071조건은NMI prefix시간초과0,명목여유44사이클이다. 실제하드웨어검수는남으며063은만들지않았다. [216측정·한계](TEXT11_ACTUAL_ENTRY_NMI_BUDGET_CORRECTION_216.md).

**작업214 정리 완료.** 펼친 과거자료·캐시 1,004,563개 정리, 순 파일 바이트 7.48GiB 절감. 과거 바이트는 전수검증 압축보관, 원본·원천·051·062·링크 유지. 복원검증PNG1개는 직접삭제 정책차단으로 남음. 실제 플레이 없음. [보관/복원·검증 인계](PROJECT_CLEANUP_ARCHIVED_HISTORY_214.md). 과거 물리적 파일 경로를 요구하는 검증기는 복원 후 사용한다. 현재 보관 상태는 `python -B scripts/audit_cleanup214.py`로 검사한다.

현재 텍스트 확대 검토 후보는 **text11_candidate_062**다. HUD·정지 표지판 등 작은 그림을 기존 크기로 유지하고, 등록 초안45개(오프닝9+일반33+크레딧3)에11px 글꼴을 넣었다. [062 ROM](../build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes), [정적45문단과 상단창5모형](../workspace/review/text11_211/review.html), [구현·검증211](TEXT11_CANDIDATE062_ALL45_CPU_STATIC_211.md).

062는524304바이트, SHA `7e32acb4ac08d47ec821421d0ebf704fd98225be194e736f9fff7b1b5b5722ce`다. [ROM 없는 적용ZIP212](../dist/TinyToonAdventures2_KR_Text11_Candidate062_20261009.zip)은68파일, ZIP SHA `377b16522c31f3516869c9eb14acb925799ceeefa1051d06508570770bc19575`다. [Windows 적용 근거212](TEXT11_CANDIDATE062_WINDOWS_APPLY_PACKAGE_212.md).

| 검증 구분 | 현재 결과 |
|---|---|
| 정적·빌드 | 원본ExpectedWrite/허용diff·독립 ROM/IPS 재빌드·적용 동일,45문단 글꼴 디코딩 PASS |
| CPU | 기존42개/1042수치상태/1071건너뛰기/4320초기화/1556비대상/교환050 보존10/놀이기구5창 동시거주 PASS |
| 크레딧 CPU | 첫756NT셀, 진행169/158호출의 원래대기·종료,4000프레임 동기CPU 스크롤 상태 동일 PASS |
| 패키지·실제 적용 | Windows8사례와 최종ZIP 추출본 적용 byte-exact PASS |
| 실제062 실행·장면·플레이 | **미수행·사용자 담당.062 미채택 개발 후보** |

정적 PNG와 창 모형은062 게임 캡처가 아니다. CPU 스케줄의 프레임도 실제 에뮬레이터 프레임이 아니다. CHR256 실제매핑·비동기NMI/IRQ 전송예산·글꼴수명·상단창소거/화면전환·가독성·최종미감/문체·전체플레이는 남아 있다.45는 등록 초안에 대한 수량이며 전게임 원천 발견/완료율을 뜻하지 않는다. 숫자는8px 타일 간격이고 글자 종류에 따라 실제 획높이가 다르다.

오프닝6문단은1행 ‘친구들도 데려와!’,2행 ‘깜짝 놀랄 거다!’,3행 빈줄,4행 ‘의문의 대부호로부터’ 한줄 오른쪽 정렬을 유지했다. 크레딧은 한글12px·공백8px·영문16px 간격의 개발안이며 이름/KONAMI/권리 문자열은 같다. 원래8px 이름 bitmap도11px로 확대했으므로 옛 글자그림 보존이라고 표현하지 않는다. 첫크레딧은 nativeFF31의NMI/렌더중지 경로에서 직접NT에 쓰고FF17로2000을 복원한다.2001은 출력을 중지한 채 다음nativeNMI를 기다리며 실제 하드웨어 검수는 남는다.

**기준 개발본 dialogue_kr_poc_051은 유지**한다. [051 ROM](../build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes)은 티켓교환050과 움직이는 정지051 수정을 포함한다. [오프닝055 실제 비교](../workspace/review/opening11_194/review.html)의9000프레임 근거는055 오프닝에 한정하며062 전체 실행 성공으로 옮기지 않는다.054/057/059는 이전 후보,056/058/060/061은 거부 실험,205는 적용도구 크기 검사 실패로 보존했다. 작업213까지 이전 자료를 덮어쓰거나 삭제하지 않았다. 작업214에서는 과거 바이트를 압축 보관하고 펼친 대량 파일을 정리했다.

원본2편·CSV·사용자Mesen/세이브는 그대로다. 작업214에서 과거빌드/QA의 대량 파일은 해시 검증된 비공개 압축 보관본으로 옮겼다. 현재062와 재현 체인·문서 링크는 원래 경로에 유지했다.1편 참조5개 해시는 동일하며 역사 원본 경로1개는 현재 없어 불변 확인을 완료했다고 주장하지 않는다.1편 파일을 수정하거나 복원하지 않았다. HOWTO·PAUSE·POW·RYO51·NT1C·진단STAGE SELECT는 원문 유지다. 카페 완성 작업기는 모든 작업 후 작성하며 현재 외부 게시하지 않았다.

사용자 실제 검수는 이전 한글판에 재패치하지 않고 새062 ROM을 열어 초기화한 뒤 진행한다. 오프닝 완성/건너뛰기, 홈·선택·매표소 티켓교환, 놀이기구 이름/규칙/가격/보유/입장·성, 크레딧의 출력/대기/지우기/재진입을 확인한다. 이전 세이브스테이트 호환은 미확인이다.

**다음 작업 하나: 배포 이후 접수되는 제보의 ROM 해시·에뮬레이터 버전·직전 행동·장면을 기록하고 해당 경로의 추가 검증을 진행한다.** [오늘 인계](HANDOFF_2026-10-09.md), [오늘 journal](journal/2026-10-09.md), [계획](LOCALIZATION_WORK_PLAN.md).

아래는이전작업의역사기록이며상단재개위치를우선한다.

[작업107 실제 성공입장/출발 대사 검증](RIDE_SUCCESS_CURRENT047.md): 초기 일반티켓4 seed,4→0차감, native2A/9910와 현재047 actual NT/RGB 및 플레이 진입을 확인했다. 두 실행 공통1820파일/302전체PNG exact. 최종사람검토나 자연완주는 아니다.

**다음 작업 하나: 사용자가 새051 ROM을 열고 초기화/기차 재진입 후 위아래로 움직이는 정지 표지판을 검수한다.** [오늘 인계](HANDOFF_2026-10-08.md), [오늘 journal](journal/2026-10-08.md), [조사](SURVEY.md), [계획](LOCALIZATION_WORK_PLAN.md).

최신 [적용ZIP173](../dist/TinyToonAdventures2_KR_Review_049_Scope173_20261008.zip), [검토HTML173](../workspace/review/nonplay049_20261008_173/review.html), [인계173](CURRENT049_SIX_RETENTIONS_REVIEW_APPLY_173.md)를 따른다.54원천/33그림/기존실제21·정적4PNG를 보존했다. HOWTO·PAUSE·POW(169)와 RYO51·NT1C·진단 STAGE SELECT(173)는 이번 범위 원문 유지로 사용자 결정됐다. 타이틀 PUSH START는 기존 보존 안내에 소비 연결됐다. 발견7건의 번역 범위 미결정은0이나 소비 미확정6건은 남으며 전역 미사용이나 전체게임 승인이 아니다. 아래 각 작업 기록은 당시 역사 자료다.

실제 플레이는 사용자 담당이다. 현재049 ROM/CSV는 동일하고173의 최종ZIP 실제 Windows 적용은 byte-exact PASS다. 비플레이의 명시적 번역 범위 잔여6건과 패키지 반영은 닫았다.163 캡처 PNG 차이는 원인 미확정이며 전역 원천 목록 완결성과 최종 문체·명칭·그림/플레이 검수는 미완료다. 전체 작업 완료 후 카페 완성 작업기를 작성하며 외부 게시하지 않는다.


[작업108 완료범위 원장](SCOPE047_RECONCILIATION.md):54/33/20목록은한정분모이며전역완료가아니다. 기존13보고·미완료8조건을연결했고ROM/CSV변경없음.


[작업109 NT원천과소비관측](NT_SOURCE_CONSUMER_047.md):20개중15selector의8025호출,0E/26별도소비,14/16조건부producer·1C간접공급미폐쇄. 새runtime/ROM/CSV수정없음.


[작업110 성 배경 조건과 STAGE SELECT 후보](CASTLE_BACKGROUND_STAGE_ANALYSIS.md): 한정 CPU1024사례, 기존047 성 RAM768개는 방0. 방6 실제 화면 미검증.


[작업111 성 방6 실제소비](CASTLE_ROOM6_NATIVE_QA.md): 명시적 A5/54진단으로NT14/16/CHR연결,107캡처HUD밖RGB동일. 자연방진행/성완주 아님.


[작업112 NT 공급 경계](NT_SELECTOR_SUPPLIER_BOUNDS.md): 명명한19selector 공급에1C없음. 다른06D0counter/간접경로는별도,전역unused아님.


[작업113 별도command printer](NATIVE_COMMAND_PRINTER_CATALOG.md):12slot/48CPU queue검증,STAGE SELECT 진단후보별도원장. 실제소비/사람범위결정미완료.


[작업114 카트 접촉 순간 가설](CART_CONTACT_MOMENT_ANALYSIS.md):88구멍방향정정, V6해제20시작중10속도반대/근접창5. 실제collision은다음읽기전용관측으로구분.


[작업115 현재047 실제V6충돌](CART_V6_CURRENT047_COLLISION.md):읽기전용168swap CPU/RAMexact,선언burst18충돌중7반대전달·방향변화/재교환관측.3구간미달유지.


[작업116 V7 방향유지후보](CART_HEADING_HOLD_EXPERIMENT.md):14해제창/84표본방향변화근거,첫구간·충전·B·pit회피보존한후보생성/실행전.


[작업117 V7 실패/PNG예외](CART_V7_CURRENT047_ATTEMPT.md):first16220입력차이,첫구간만/전체미달유지,702raw/core같음/3PNG예외별도. 유사botstream닫음.


[작업118 캡처 프레임 증거 범위](CAPTURE_FRAME_BOUNDS.md): 정확한 지연량은 미확정이며 프레임 이름만으로 PNG 시점을 동일시하지 않는다. 유사 winningbot 반복은 닫은 상태다.


[작업119 미연결 NT1C 경계](NT1C_CANDIDATE_BOUNDS.md): 가정한 후보 타일 부재와 실제 소비 미연결을 구분했다.


[작업120 강 후반 CHR61 공급](RIVER_BANK61_STAGE_SPRITES.md): 공통POW후보와별도stage소비를구분했다.


[작업121 강 조건 실제 진단](RIVER_NATIVE_DIAGNOSTIC_047.md): 생성은실행됐으나실제그림소비미연결.표시성공으로보고하지않는다.


[작업122 강 actor2 culling](RIVER_ACTOR2_CULL_047.md): native정리조건을확인했고다음camera진단을정확한CPU예측에연결했다.


[작업123 강 ED 실제 OAM/CHR/RGB](RIVER_ED_ACTUAL_CONSUMER_047.md): 하단두행차이는별도로미해결기록했다.


[작업124 HUD 하단2줄](HUD_FOOTER_SHIFT_047.md): 기존040의도된2px배치를livePPU/RGB로확인했다.ROM수정불필요.


[작업125 본문 충실도 검토](PROSE_FIDELITY_REVIEW_125.md): 한 문장 개발 후보 선택/공유 폰트 보존 계획, 아직 ROM/CSV 수정 없음.


[작업126 단일048 후보](SHORTAGE_EDITORIAL_BUILD_048.md): build/apply통과/새runtime전047채택유지.


[작업127 실제전환거부](SHORTAGE048_LIFETIME_REJECTION.md): 048은거부/새후보수정예정/채택047.


[작업128 post-clear049 후보](LOWER_FONT_POST_CLEAR_049_BUILD.md): 3840CPU/build/apply통과·실제QA전047채택유지.


[작업129 부족/성공 actual049](LOWER_FONT_POST_CLEAR_049_BRANCH_QA.md): 폰트혼합해결·RNG차이구분/다른pageQA전047채택.


[작업130 개발049채택](DEVELOPMENT049_PAGE_REGRESSION.md): 다른page회귀1503전체캡처same·idleRNG/PC차이구분/사람최종승인아님.


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


작업219 추가 검증: 이전218 검사기의 현재 인계 헤더 고정 조건은219 이후 맞지 않아 최신 `python -B scripts/verify_resume219.py`를 사용한다. 봉인45파일·핵심6파일·신규링크 PASS. [명령 정정과 최종 근거](TEXT11_RESUME219_FINAL_VERIFICATION.md).


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


### 작업227 마무리 — 렌더 캐시 정리

종료된 자체 기술지침 렌더의 browser_profile만 정확 경로로 삭제했다. 246파일/20,353,279바이트이며 렌더 보고·4PNG·게시원천·최종ZIP은 보존했다. 정리 후227 봉인 파일 25개 SHA 및 기존 게임 배포/작업기ZIP·번역CSV 불변 확인 PASS. 캐시 정리 실행은 powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cleanup_technical227.ps1, 마무리검사는 python -B scripts/finish_technical227.py다. [캐시정리보고](../qa/reports/technical227_cache_cleanup.json). 새게임/카페게시없음.

다음 작업 하나: 사용자가 완성한 기술 지침 본문과 설명도2개를 게시 위치에 배치하고 배포 후 제보를 수집한다.


## 공개 작업기·기술 지침 독자용 개정 — 작업228

내부 빌드 번호를 본문·비교 이미지·캡션·공개 출처에서 제거했다. 목적과 수정 전/후로 다시 설명했으며 두 리더의PC/모바일·ZIP검사가 통과했다. 게임 배포·번역·사용자1차 검수 상태는 같다. [상세 변경·해시·검증](PUBLIC_ARTICLE_READER_REVISION_228.md).

다음 작업 하나: 사용자가 수정된 작업기·기술 지침을 게시하고, 배포 후 제보의 ROM 해시·환경·직전 행동·장면을 수집한다.


## 작업229 — 카페 작업기 작성자 말투 적용

사용자도입부·어린시절경험·엔딩소감을살리고전체본문과이미지설명을게시판1인칭말투로개정했다. 내부빌드번호없는상태와기술범위·검수구분유지. HTML PC/모바일·확대·ZIP전수검사PASS. [상세 인계·SHA·재현](CAFE_WORKLOG_AUTHOR_VOICE_229.md).

다음 작업 하나: 사용자가 본문·그림을 카페 편집기에 배치하고, 배포 이후 제보의 ROM 해시·환경·직전 행동·화면을 수집한다.


## 작업230 — 불필요한 이전 게시자료·검토본 정리

20대상90파일을private230보관으로전수검증후삭제했다. 최신게임배포·작성자작업기·기술지침과보존4713파일SHA확인PASS. [변경·해시·검증·복원](SUPERSEDED_PUBLICATION_CLEANUP_230.md).

다음 작업 하나: 사용자가 최신 작업기·기술 지침과 최종 릴리즈를 게시하고, 배포 이후 제보를 수집한다.
