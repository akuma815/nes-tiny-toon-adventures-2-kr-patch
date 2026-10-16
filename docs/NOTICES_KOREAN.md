# 작업74 — 시간 초과 / 다음 라운드 한글 안내

[빌드044](../build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes), [IPS](../build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.ips), [빌드 보고서](../build/dialogue_kr_poc_044/build_report.json). 원본 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d / ROM 58db7fa14239ecd71c0454c097293a3037bb3ce841ef455213b02530b521dbdf / IPS a69a0cb1c944da8c5bb5fb0700f0316f615941e676d800afdf2d2aa4b2eeba1c.

TIME UP! → **시간 초과!**, NEXT ROUND! → **다음 라운드!** 개발 초안. [그림 번역/타일 계획](../workspace/translation/notices_graphics_plan_001.json), [PNG 원천](../workspace/graphics/notices_001/timeup_kr.png), [다음 라운드 PNG](../workspace/graphics/notices_001/nextround_kr.png). 기존 Galmuri7 2.403/OFL native 비트맵의 9개 한글 글리프를 atlas/TTF 대조한 뒤 수직2배/1픽셀 외곽선으로 변환했다. 이번 작은 스프라이트 글자는 생성형 이미지가 아닌 결정적 폰트 변환이며 타이틀의 생성형 이미지 작업은 기존003이다.

정적: bank62 전체를 새220에 복제하고 첫28타일만 번역했다. 나머지36타일/원래62/모든 이전 한글 폰트/헤더/ROM 길이491536을 보존했다. 043 대비519바이트 변화가 새bank220 1KiB 및 3F7CF/3F81F 두 상수 범위 안이다. 9개 ExpectedWrites가 원본 기대 바이트와 비중첩 검사 후 전체 ROM을 재구성한다.

CPU 검증: 각 생산자의 LDA #bank/STA39/다음 LDA #19 또는#1A를 256 flags×2곳=512사례로 실행했다. RAM39의62→220 이외 레지스터·스택·플래그 동일,7cycles 정확. 최초 V1은 두 명령만 검사해 음수 flag 변화로 실패했다. 다음 LDA가 곧바로 flag를 복원하며 중간 조건 분기가 없는 것을 V2로 검사했다. V1 보존. 전체 초기화 루틴 전체 ABI를 시험했다는 주장은 하지 않는다.

[재빌드/적용](../qa/reports/notices074_build_apply.json): 새폴더에서 ROM/plan/ExpectedWrites/builder/CSV 재생성 byte exact, 한국어와 공백 경로의 실제 Windows Python IPS CLI 출력이 ROM과 byte exact. 공개 apply.cmd나 최종 배포 패키지 검증은 이번 작업 범위가 아니다.

[Runtime](../qa/reports/notices074_runtime.json): 각4,200프레임 진단 시드 실행, 604개 스냅숏에서 OAM/네임테이블/팔레트 동일. RAM은39/3F의bank번호만 변화. 75,776행 실제 PPU 읽기 geometry/scanline/dot 집계 동일, 새CHR220의 바이트 일치. 70,821 mapper/latch 쓰기의 위치/실행 좌표 동일하며 지정bank만 변경. 12개 변경 PNG는 안내 스프라이트 영역 안에만 차이가 있다. TIME UP endframe PPU 11개 차이는 새 패턴 매핑이며 네임테이블/팔레트는 동일하다.

직접 장면 시각 검증: [시간 초과 actual3360](../qa/dialogue/notices074_timeup044/frame_03360.png), [다음 라운드 actual3420](../qa/dialogue/notices074_nextround044_v3/frame_03420.png)를 직접 확인했다. 첫 TIME UP 실행은 구62만 읽기 필터에 잡혀 새bank telemetry가 누락됐고 캡처는 유효하다. V3가구62/새220을 관찰해 새TIME UP 실행도 검증했다. 기존 실행/보고서는 보존한다.

재현: `python scripts/build_notices_v2.py --output build/새폴더`; `python scripts/run_notices_qa_v3.py --rom build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_cart_001.json --notice-phase 16` (NEXT14); `python scripts/verify_notices074.py` (새 보고서 없는 복제 공간). 모든 변경 파일과 SHA는 [동결 manifest](../manifests/notices074_assets.json).

미수행: 본문 CSV는45draft/9기술공유 그대로. 사람 최종 문장/명칭 승인, 전체게임, 실기/청음, 새044 공개 패키지는 미수행. 043 검토용패키지와 검토키트는 당시043 자료로 보존하며 새044에 자동 확대하지 않는다.

다음 작업 하나: 기존 몸체경로 controller-only 입력으로 빌드044를20,000프레임 실행해 자연 구간완료/시간초과 안내와 홈 복귀를 비교한다.
