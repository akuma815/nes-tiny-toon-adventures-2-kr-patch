# 게임오버 실제 소비·PNG 추출 — 작업47

현재041/SSOT 유지, 새 번역 ROM 수정 없음. 티켓을 모두 쓴 뒤 실제 게임 실패가 native GAME OVER·CONTINUE ?·“YES!”·“NO.” 화면으로 이어지는 것을 확인했다. 이전의 게임오버 후보와 실제 사용 위치를 연결했다. [consumer·해시](../extracted/graphics/gameover_001/consumer.json), [원래 PNG](../extracted/graphics/gameover_001/source_logo_4x.png), [추출 검증 코드](../scripts/survey_gameover_source.py).

원본 f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,041 535fa114952587dfc0a6394ddff21b1aede053ade3dc0d3d9dfda77ed5888eae. 등록 CSV45draft/9기술공유·해시26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27 불변.

1,000프레임에 초기 일반 티켓07D0..2를4/0/0으로 지정하고 이후 실제 컨트롤러 입력과 native 플레이어 실패만으로 진입했다. phase나PC/ROM·save state를 바꾸지 않았다. 초기 티켓 수는 seed이며 자연 획득/전체 플레이 증명과 구분한다. [첫 관측](../qa/dialogue/world041_coaster_ticket4/environment.json), [계속 선택](../qa/dialogue/gameover041_yes_consumer/environment.json), [종료 선택](../qa/dialogue/gameover041_no_consumer/environment.json).

root4/phase0B F6ED→bank36/93AC가5034에RAM34=124·35=122를 만들고,9412가21문자를 실제 읽어 NT226B/22B0/22F0에 출력한다. 글자 읽기 PC9430/945B/9486와 대상주소·값·physical mapping을 검증했다. 예 선택6100/A는 native home로 돌아가 일반티켓10을 초기화한다. 아니요 선택6100/down·6250/A는 native 시작/타이틀 후 attract(root7)로 돌아간다. 8,000프레임 두 경로에서 각각21literal read·NMI 직후4KiB 글꼴36/41표본이 전체 원래 데이터와 일치했다.

게임오버 그림은 NT20E8부터16×4셀/코드C0..FF, 실제 background CHR123/PPU0C00..1000에 있다. 원래 파일3EC10..3F010, 확장041 파일5EC10..5F010. 실제 영역[64,56,192,88]/128×32의4,096픽셀을 원래 팔레트와 전체 RGB 대조해 PNG로 추출했다. 문자21셀1,344픽셀도 원래 font124와 실제RGB가 일치한다. 팔레트0검정,1(192,223,255),2(255,254,255),3(66,64,255)이며 임의 분석 색이 아니다.

CONTINUE ?는10셀, “YES!”는6셀, “NO.”는5셀이다. NO 뒤94ED의A5는 코드이므로 번역 범위에서 제외한다. 열림/닫힘 인용부호는68/69의 서로 다른 glyph다. 초기 추출의 원본/확장 주소와 인용부호 매핑 오류는 검증에서 거절했으며, ROM 수정0·원래 PNG 보존·실패 기록을 [별도 보고](../qa/reports/gameover047_geometry_offset_error.json)에 남겼다.

모든 원본 CHR 페이지의 [정적 목록](../work/graphics_population_002/source_CHR_all_pages_analysis_2x.png)에서 PAUSE와 GAME OVER 후보를 찾아 실제 실패 분기로 이어갔다. 목록은 임의 설명 색이며 실제 화면 근거가 아니다. PAUSE120/121은 여전히 실제 소비가 연결되지 않았다. 040의 관측 일시정지에서 글자가 없었던 것은 해당 경로의 한계이며 전체 게임에서 미사용이라는 증명은 아니다. root9는별도native engine 조사 대상으로 남아 있다.

재현: `run_gameover_seed_qa.py --rom build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes --output <새QA경로> --frames 8000 --inputs config/world_gameover_yes_001.json --script scripts/trace_gameover_seed_v1.lua --seed config/world_coaster_ticket4_seed_001.json`; 아니요는world_gameover_no_001.json. 실제 명령·해시는environment와 used 파일에 동결했다. PNG 추출은 `survey_gameover_source.py --output extracted/graphics/새추출폴더`로 재현하며 기존consumer를 덮어쓰지 않는다.

정적·실제 Mesen·직접 원래 화면/PNG 검토까지 완료. 새 한글 그림 생성/빌드/적용/CPU/시각 회귀는 아직 수행하지 않았다. 전체 corpus·전체 자연 플레이/오디오/reset/savestate/실기/최종 사람 검토 미수행. 다음 작업 하나: 생성형 “게임 오버” PNG와 전용210/211·212/213 및 선택문구3종을 삽입하고 native 예/아니요·복귀·시점 검증. 즉시 계속한다.
