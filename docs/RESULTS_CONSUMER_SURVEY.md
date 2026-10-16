# 결과 화면 실제 소비 조사 — 작업45

040 ROM/CSV 수정 없음. 실제보너스초기화 경로, 원래font124/125와 CHR 내154바이트배치스트림을연결했다. [consumer·원천·해시](../extracted/graphics/results_001/consumer.json), [실제화면](../extracted/graphics/results_001/source_actual_4x.png), [조사코드](../scripts/survey_results.py).

source f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d,040 bdf5ca3a986d50b145571db13dfc75b58d3d2e4d140ae7805ef4a3f4f494ae0c. 등록CSV26274fdced8c950ec64d3b3dae7afbc7b92a49f8fd8fe4a31b6f92327e584c27/45draft·9기술공유 유지.

Mesen controller로게임초기화후3200에RAM54=20 하나만지정했다. 즉시직전조건root18=4/phase54=5/55=0를검사했고PC/ROM/state-load를바꾸지않았다. 자연클리어는아니다. nativeF8BA/F8BF→F8CF의font124생산자3230/F8D3→X26/8025→81C7/8216의copy selector08가3231에154바이트를복사했다. 실제CHR상대049FB=원본파일24A0B/040파일44A0B이며RAM복사전체가동일하다. 7500프레임의native캡처·IRQ를보존했다.

NT2000/1024셀, 위배치의8literal블록에7서로다른영문: CONGRATULATIONS!/축하합니다!, LIFE BONUS/체력보너스, CLEAR BONUS/클리어보너스, TIME BONUS/시간보너스, NOW YOU GET/획득점수, POINTS/점(2군), YOUR POINTS/보유점수. NT23C0이상의palette속성literal은문구로보지않는다. 원래단어5632픽셀전체RGB와font124/125 NMI직후18표본의2KiB데이터전체가원본과일치했다. 직접실제보너스화면을확인했고,숫자는집계전/집계도중/완료후로변한다. 07F0..6 전체점수상태와숫자·계산·팔레트·애니메이션을보호한다.

정적nativeNT20stream 후보목록은 [private분석](../work/graphics_population_001/native_NT_catalog.json)에보존한다. 모든stream에font124를가정한ASCII스캔은완료율이아니며graphic tileID의우연한문자열이포함된다. selector1E는KONAMI로고정적후보이고초기GAMEOVER추측은거절했다. 분석PNG의gameover파일명은거절된추측의이력일뿐 실제게임오버근거가아니다. selector20은원래권리표시후보로별도보존대상이다. consumer.limits의Source031은이권리표시후보를잘못표기한메타데이터문자열이며실제bonus오프셋/해시와무관하다. 기존consumer를덮어쓰지않고여기에정정한다.

재현은 `run_results_seed_qa.py --rom build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes --output <새QA이름> --frames 7500 --inputs config/menu_results_001.json --script scripts/trace_results_seed_v1.lua --seed config/results_native_phase_seed_001.json`; IRQ는trace_results_seed_irq_v1.lua. 원천environment.json 및*_used파일에명령/설정/seed/해시가동결되었다. 추출폴더는이미존재하므로survey기본실행은덮어쓰기거절한다.

새번역ROM의빌드/적용/CPU/시각검증은이작업에서하지않았다. 전체게임corpus/자연클리어/전체플레이/오디오/실기/최종사람검토미수행. 다음행동하나: 원래124보존·208/209복제와8literal길이보존한글화,생산자11cycles/decoder/집계·완료·재진입/회귀검증. 계속한다.
