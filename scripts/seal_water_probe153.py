from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/water153_assets.json';assert not m.exists()
 p=R/'qa/reports/water153_probe_validation.json';v=json.loads(p.read_text('utf-8'));assert not v['natural_clear_observed']
 visual=R/'qa/reports/water153_visual.json';assert not visual.exists()
 images=['qa/dialogue/water153_jump049_v2/frame_'+n+'.png'for n in ['02820','02940','03540','03900']]
 visual.write_text(json.dumps({'work':153,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{z:sha(R/z)for z in images},'observations':['2820 actual jump above log','2940/3540 river route and remaining hearts visible','3900 defeat animation on river with current Korean HUD'],'limits':['Four actual PNGs; visual proximity does not determine native damage cause or natural clear'],'human_approved':False},ensure_ascii=False,indent=2)+'\n','utf-8')
 nxt='동일한첫점프 급류경로에서0430=6과7C0체력쓰기의 native PC·물리PRG·직전RAM·register를읽기전용으로관측해 실제피해소비조건을확인한다. 입력/RAM/ROM추가조작은없다.'
 detail=f'''# 작업153 — 급류 첫 점프 실제 관측

[검증](../qa/reports/water153_probe_validation.json), [실제 화면](../qa/reports/water153_visual.json), [v1관측기 오류](../qa/reports/water153_v1_observer_error.json), [v2계획](../work/water153/run_plan_v2.json), [수정준비](../scripts/prepare_water_probe153_v2.py), [검증v2](../scripts/verify_water_probe153_v2.py).

현재049를6000프레임 coldboot했다.기존메뉴입력 뒤2800 A8프레임만추가하고b/좌우이동/추가입력을제외했다. RAM/ROM/state조작없음. 실제nativeA80E/physicalPRG3280E에서pressed128/held128/jump0/supportC1=1을한번확인했다.2801점프flag1/2832발판접촉과flag128/2840flag0 복귀를기록했다. 물에빠진기존152경로와다르게 첫플레이가2779..3889까지지속됐으며세로HI최대3에그쳤다.

2911·3512·3868에state6피해가관측되고체력3→2→1→0 후지도root8/phase13hex로복귀했다. nativeA68E/B873실행은0이며클리어/완주성공으로보고하지않는다. wall/다른충돌중무엇이피해의원인인지는쓰기명령관측이없어단정하지않는다. 다음에는같은입력에서새읽기전용피해쓰기근거를수집해회피조건을확인한다. 반복A/좌우조작을수기로시험하는방식으로입력을늘리지않는다.

全환경 선언파일SHA와2896 actualCHR조각을현재ROM과대조했다. observer에는emu.write/state load가없고컨트롤러만사용했다. 실제4PNG에서jump·강진행·체력·실패애니메이션/한글HUD를직접검토했다. 원본/이전047 pair는이번새실행없으며global게임동일성주장없다.

v1준비기Python삼중문자열의CSVheader 2줄에서실제newline이Lua짧은따옴표안에들어갔다. 실행exit4294967295/frames·native출력없음으로실패했고ROM결함이아니다. v1script/6파일QA/계획/환경은보존했다. v2는해당두줄만escape하고모든short literal의실제newline가드뒤새QA에실행해exit0/trace6000을확인했다. 자동메모리해당변경없음.

변경: prepare_water_probe153.py/v2, trace_water_progress153.lua/v2, verify_water_probe153.py/v2, seal_water_probe153.py, config/water_jump_probe153.json, work/water153계획2개, 실패QA·새QA, 오류/검증/visual보고, 상세·인계/journal·canonical·manifest/audit. ROM SHA `{v['ROM_sha256']}`,CSV SHA `{v['CSV_sha256']}`불변. 原本/1편·실패역사자료보존.

재현은v2계획명령에새QA경로를사용한다: `python scripts/run_menu_qa.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새153경로 --frames 6000 --inputs config/water_jump_probe153.json --script scripts/trace_water_progress153_v2.lua`. 고정검증기는기존보고서를거부하므로새경로/보고서로복제한다. 정적/환경SHA/컨트롤러runtime/실제점프/CHR/직접4PNG PASS. 자연급류clear미달. 신규build/apply/reset/state/실기/청음/사람최종없음. globalcorpus·HOWTO/PAUSE/POW·자연전경로·정식배포미완료. 카페기사/외부게시없음.

다음 작업 하나: {nxt}
'''
 doc=R/'docs/WATER_FIRST_JUMP_NATIVE_QA.md';assert not doc.exists();doc.write_text(detail,'utf-8')
 entry='\n\n## 작업153 — 급류 첫점프 실제관측\n\nA8프레임 nativeA80E실행/첫발판복귀,게임2779..3889/세로HI3.피해3회뒤실패·clear없음. v1Lua헤더escape오류보존/v2exit0·CHR2896·직접4PNG. ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER_FIRST_JUMP_NATIVE_QA.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  q=R/'docs'/n;q.write_text(q.read_text('utf-8')+entry,'utf-8')
 q=R/'docs/journal/2026-10-07.md';q.write_text(q.read_text('utf-8')+entry.replace('(WATER_FIRST_JUMP_NATIVE_QA.md)','(../WATER_FIRST_JUMP_NATIVE_QA.md)'),'utf-8')
 q=R/'README.md';q.write_text(q.read_text('utf-8')+'\n\n[급류첫점프 관측153](docs/WATER_FIRST_JUMP_NATIVE_QA.md): 점프연결·피해조건은다음관측.\n','utf-8')
 q=R/'docs/HANDOFF.md';s=q.read_text('utf-8').replace('작업152 완료','작업153 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);q.write_text(s+entry,'utf-8')
 files=[doc,p,visual,R/'qa/reports/water153_v1_observer_error.json',R/'config/water_jump_probe153.json',R/'scripts/run_menu_qa.py',R/'scripts/trace_train_reader142.lua',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*153*')]
 for d in ['work/water153','qa/dialogue/water153_jump049','qa/dialogue/water153_jump049_v2']:files.extend((R/d).iterdir())
 m.write_text(json.dumps({'work':153,'files':{q.relative_to(R).as_posix():sha(q)for q in sorted(set(files))if q.is_file()}},indent=2)+'\n','utf-8');print('PASS153 handoff')
if __name__=='__main__':main()
