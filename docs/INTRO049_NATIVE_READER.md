# 작업144 — 현재049 인트로9문단 실제 읽기와 완성

[최종 검증](../qa/reports/intro144_validation.json), [직접9화면](../qa/reports/intro144_visual.json), [실행계획](../work/intro144/run_plan.json), [검증v3](../scripts/verify_intro144_v3.py).

현재049와새047을각6000프레임냉부팅했다. 입력목록은빈배열이고Start/RAM seed/state load/ROM write가없다. 제목과9인트로문단의두번순환을같은동결142 reader로기록했다.실제PRG read676건씩의주소·값·PC·프레임·순서·문맥이같다.주본문01..09의각전체원천byte와공유버스터macro80/81원천(MACRO061C3)의전체범위가소비되었다. nativeID가진행해도실제물리주소로귀속한다. macro82가이경로에서관측되지않았다는사실을전역unused로해석하지않는다.

200 whole PNG/PPU/OAM/mapping exact 및현재ROM과1600CHR chunks exact. reader651건cycle동일/24건+1/1건+2는보고서에그대로보존한다. 전체CPU/IRQ/RNG/오디오동일성아니다. helper42 writePC이동은같은STA 명령바이트로확인했다. intro전용06CF/C6/6F3초기화3종각2회도별도허용목록이다. RAM22/IRQstack/A·flags·bus차이는보고서에기록한다.

각font128/132/134/136/138/140/142/144/146은native-reader모델의모든줄과actualNT21E4+row64가완성시일치했다. 실제줄수는01/02/04/07/09가2줄,03/08이1줄,05가4줄,06이3줄이다. 완성시작은각1020/1320/1500/1740/1920/2100/2340/2640/2760의기록된snapshot이며exactprinterfinishcycle을뜻하지않는다.9개완성PNG1080/1320/1560/1800/1920/2160/2520/2640/2880을직접검토했고문장·버스터·원래장면·인용부호를확인했다.부분출력/지우기/다음문단수명은전체200paired자료로비교했다. 캡처118시점한계 유지.

검증v1은메뉴의writePCrelocation목록만재사용해인트로초기화3명령을놓쳤다. v2는이동STA byte를확인했지만무입력상태티켓0을잘못가정해최종숫자guard가실패했다. 실제native기본티켓10장은600부터설정되며두빌드동일하다. v3는관측대로10을검증했다. [v1관측](../qa/reports/intro144_verifier_v1_observation.json), [v2관측](../qa/reports/intro144_verifier_v2_observation.json) 및실패스크립트를보존했다. 보고서쓰기전검증가정실패이며실행자료/ROM변경없이해결했다.

변경: prepare_intro144.py/run_intro144.py/prepare_verify_intro144.py/v2/v3/verify_intro144.py/v2/v3/seal_intro144.py;config/intro_no_inputs144.json;work/intro144계획·log;qa/dialogue새047/현재049자료;최종/직접시각/관측보고서;본상세/datedhandoff·journal·SURVEY·PLAN·HANDOFF·README;manifest/audit. 기존138원장/130인트로/역사QA·원본·1편·049·CSV보존. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변.

정적/해시/무입력runtime/실제reader/whole영상/9선택직접PNG PASS. 새build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/prepare_intro144.py`, `python scripts/run_intro144.py`, `python scripts/verify_intro144_v3.py`;기존출력거부. globalcorpus/전체게임/기타소비경로/사람문체·명칭·그림최종/정식배포미완료. 사람승인false/카페완성기사·외부게시없음.

다음 작업 하나: 138 원장을 보존하고 139..144를 반영한 새54원장145를 작성해, 현재초기화/실제reader/완성NT/직접PNG를구분한뒤 남은등록원천의reader 미연결 한경로를선택한다.
