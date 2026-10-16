# 작업73 — 시간 초과/다음 라운드 스프라이트 소비기

기준은 빌드043이며 ROM/본문 CSV 변경은 없다. 자연 경로 작업72의 TIME UP! 영문 발견으로 한글화 우선순위를 바꿨다. 실제 소비기는 CHR62이고 F80E/F7BE의 LDA #3E가 RAM39 및 NMI D008로 이어진다. 최종 프레임 PPU는 HUD IRQ 뒤 bank126이므로 화면 위쪽 NMI와 실제 PPU 읽기를 연결했다.

[채택 추출/소비 보고서](../extracted/graphics/notices_002/consumer.json): TIME UP! 48×16/12타일, NEXT ROUND! 64×16/16타일. 나머지36타일은 보존 대상이다. 원본/043 bank62 일치, 1,309개 비투명 RGB 픽셀과 75,776개 PPU 읽기 행의 ROM 바이트 일치, PNG 타일 왕복을 검증했다. [재현 스크립트](../scripts/extract_notice_sprites_v3.py), [TIME UP 실제 화면](../qa/dialogue/notices073_timeup_v2/frame_03360.png), [NEXT ROUND 실제 화면](../qa/dialogue/notices073_nextround_v2/frame_03420.png).

에뮬레이터: 각각4,200프레임, 3300에서 root4/phase5/course1/pause0 검사 후 RAM54 한 바이트만 진단 시드했다. 전체2KiB RAM 전후 차이가 이 한 바이트임을 검사했다. 자연 클리어 증거로 사용하지 않는다. 실제 NEXT ROUND 화면을 직접 확인했으며 TIME UP 화면 픽셀은 대조했다. 전면 게임 완주는 미수행이다.

실패·정정: 초기 wait phase17(decimal) 시드는 초기화를 건너뛰어 안내를 만들지 못했다. [실패 메타데이터 정정](../qa/reports/notices073_seed_wait_phase_error.json)을 보존했다. V1 추출은 공통 Y를 가정해 실패했으며 V2 픽셀 검증은 통과했지만 PowerShell stdin 인코딩으로 한국어 초안이 ?로 기록됐다. V3 UTF8 인코딩과 새출력 notices_002에서 바로잡았다. 원본 notices_001/스크립트는 보존한다. 장면별 PNG/OAM Y 차이는 TIME UP 0, NEXT ROUND +1인 경험적 측정이며 하드웨어 타이밍 주장으로 확대하지 않는다.

phase 단위 정정: 작업69의 phase14(hex)는 decimal20으로 기존 보너스 초기화 시드와 **같은 상태**다. 기존 문서의 서로 다르다는 설명은 잘못됐다. TIME UP 초기화10hex=16dec, 대기11hex=17dec; NEXT ROUND 초기화0Ehex=14dec, 대기0Fhex=15dec; 보너스14..18hex=20..24dec. 과거 문서/실패 기록은 덮어쓰지 않는다.

재현: `python scripts/extract_notice_sprites_v3.py` (새 폴더가 없는 복제 작업공간에서 실행); `python scripts/run_notices_qa_v2.py --rom build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_cart_001.json --notice-phase 16` (NEXT ROUND는14).

변경 파일과 SHA는 [동결 manifest](../manifests/notices073_assets.json)에 기록한다. 정적/추출/runtime 검증이며 새빌드/패치 적용은 이번 작업에서 수행하지 않았다. 최종 사람 번역 검토는 pending.

다음 작업 하나: 기존 Galmuri7 native 비트맵으로 두 안내를 만들고 CHR220 복제와 두 생산자 상수 변경으로 빌드044를 검증한다.
