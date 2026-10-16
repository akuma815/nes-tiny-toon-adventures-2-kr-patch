# 작업153 — 급류 첫 점프 실제 관측

[검증](../qa/reports/water153_probe_validation.json), [실제 화면](../qa/reports/water153_visual.json), [v1관측기 오류](../qa/reports/water153_v1_observer_error.json), [v2계획](../work/water153/run_plan_v2.json), [수정준비](../scripts/prepare_water_probe153_v2.py), [검증v2](../scripts/verify_water_probe153_v2.py).

현재049를6000프레임 coldboot했다.기존메뉴입력 뒤2800 A8프레임만추가하고b/좌우이동/추가입력을제외했다. RAM/ROM/state조작없음. 실제nativeA80E/physicalPRG3280E에서pressed128/held128/jump0/supportC1=1을한번확인했다.2801점프flag1/2832발판접촉과flag128/2840flag0 복귀를기록했다. 물에빠진기존152경로와다르게 첫플레이가2779..3889까지지속됐으며세로HI최대3에그쳤다.

2911·3512·3868에state6피해가관측되고체력3→2→1→0 후지도root8/phase13hex로복귀했다. nativeA68E/B873실행은0이며클리어/완주성공으로보고하지않는다. wall/다른충돌중무엇이피해의원인인지는쓰기명령관측이없어단정하지않는다. 다음에는같은입력에서새읽기전용피해쓰기근거를수집해회피조건을확인한다. 반복A/좌우조작을수기로시험하는방식으로입력을늘리지않는다.

全환경 선언파일SHA와2896 actualCHR조각을현재ROM과대조했다. observer에는emu.write/state load가없고컨트롤러만사용했다. 실제4PNG에서jump·강진행·체력·실패애니메이션/한글HUD를직접검토했다. 원본/이전047 pair는이번새실행없으며global게임동일성주장없다.

v1준비기Python삼중문자열의CSVheader 2줄에서실제newline이Lua짧은따옴표안에들어갔다. 실행exit4294967295/frames·native출력없음으로실패했고ROM결함이아니다. v1script/6파일QA/계획/환경은보존했다. v2는해당두줄만escape하고모든short literal의실제newline가드뒤새QA에실행해exit0/trace6000을확인했다. 자동메모리해당변경없음.

변경: prepare_water_probe153.py/v2, trace_water_progress153.lua/v2, verify_water_probe153.py/v2, seal_water_probe153.py, config/water_jump_probe153.json, work/water153계획2개, 실패QA·새QA, 오류/검증/visual보고, 상세·인계/journal·canonical·manifest/audit. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변. 原本/1편·실패역사자료보존.

재현은v2계획명령에새QA경로를사용한다: `python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새153경로 --frames 6000 --inputs config/water_jump_probe153.json --script scripts/trace_water_progress153_v2.lua`. 고정검증기는기존보고서를거부하므로새경로/보고서로복제한다. 정적/환경SHA/컨트롤러runtime/실제점프/CHR/직접4PNG PASS. 자연급류clear미달. 신규build/apply/reset/state/실기/청음/사람최종없음. globalcorpus·HOWTO/PAUSE/POW·자연전경로·정식배포미완료. 카페기사/외부게시없음.

다음 작업 하나: 동일한첫점프 급류경로에서0430=6과7C0체력쓰기의 native PC·물리PRG·직전RAM·register를읽기전용으로관측해 실제피해소비조건을확인한다. 입력/RAM/ROM추가조작은없다.
