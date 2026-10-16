from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=R/'manifests/live134_assets.json';assert not manifest.exists();v=json.loads((R/'qa/reports/live134_validation.json').read_text('utf-8'));assert v['unclassified_extra_first_call_cycles']==4
 nextaction='처음 홈 문단의 추가4실측cycles를 좁은924프레임 opcode·DMC cursor/read·새PCM-CDL과 순수CPU모델로 대조해 DMA인지 다른진행인지 구분한다. ROM수정전에 원인을 확인한다.'
 detail='''# 작업134 — 실제 page 시간·counter·IRQ 범위

[실측 검증](../qa/reports/live134_validation.json), [읽기전용 Lua v2](../scripts/trace_live_page134_v2.lua), [동일입력 실행계획](../work/live134_v2/run_plan.json), [v1callback 실패](../qa/reports/live134_v1_observation.json), [v1검증기 고정87 가정 실패](../qa/reports/live134_verifier_v1_observation.json).

047/049×초기티켓3/4의4회4200프레임을 별도 실행했다. 실제native9417(entryPRG25417),95F9(helper55F9),9445(RTS25445직전)의CPUcycle/RAM1B/RAM22/레지스터와 모든frame counter를 기록했다. 새PNG·장면육안·ROM수정·build/apply·청음은 없고129/130의 화면 증거를 계승한다.

티켓3의12호출/4의10호출에서liveRAM1B가129의추론값과모두같다. 실제1B로 ‘문단당2회 idle 생략×(1+1B)’ 모델을계산하면두경로각4200EndFrame RAM22차이를정확히예측한다. 처음1575의같은frame3호출은entrycycle차이0/38/76으로누적되므로모든entry의절대cycle이같다고하지않는다. 기본체크사이의같은before-helper시간은87/90/91이다.

**순수CPU모델의38cycles와실제경과시간을구분한다.**22호출중처음홈924의각047→049는207→249cycles(각RTS6포함),42증가다. 나머지20호출은각38증가. 첫호출구간에기록한매퍼/PPU port쓰기는0이며추가4의원인은미분류다. DMA라고추측확정하지않았다. 이차이를129의counter모델이맞다는이유로숨기지않는다.

실제port쓰기의주소/PC/순서/scanline은두짝같다. 성공4는143883행의값·절대cycle·dot까지전부같다. 부족3은127206행중1198행의A000196→226/A008197→227만의도된폰트값변경(2008..2606),별도로2001프레임의17쓰기만 **1CPUcycle/3PPUdot앞당겨졌다**. 값은같고해당17쓰기의서로간상대간격은같다. 따라서순수IRQ코드의명령/cycle동일과 실제모든IRQ쓰기절대시각동일을혼동하지않는다. 이전129/130의픽셀/보호snapshot 결과는별도유효하며전역CPU/게임난수동일성을뜻하지않는다.

시행착오: v1은paddingNOP9448을RTS로오인해닫히지않는호출을만들었다. 실행한첫probe만실패했고나머지3은시작하지않았다. executable/commandline이우리private실험과같은PID22116만종료해실패환경을보존했다. 사용자앱은건드리지않았다. v2실행전두ROM의9445=60/9448=EA를정적확인했다. 검증기v1의고정prefix87가정은실측90/91에서실패했고v2는047/049 prefix의짝별동일을확인하며값을기록했다. 모든실패/Lua/실행/검증본을보존했다.

원본/1편/049/CSV SHA유지: ROM `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 변경은scripts의134프로브/실행/검증v1v2와prepare/seal,qa/dialogue실패1+완료4폴더,work/live134및v2계획/log,qa/reports관측/최종검증,상세/정본인계·README·오늘journal. 개별SHA는동결manifest.

재현 `python scripts/run_pair134_v2.py`와 `python scripts/verify_live134_v2.py`는기존출력을거부한다. 단일새출력은run_live134_v2.py에ROM/4200/input menu_coaster_001/seed3또는4/trace_live_page134_v2를지정한다. 초기seed이외RAM/PC/ROM/state 개입은없다.

한계:38純CPU/42실측차이 원인미분류,실측부족IRQ17개시각차이,모든IRQ/CPU/게임난수동일성·자연전체·전역corpus·HOWTO/PAUSE/POW·실기/PCM/사람검토 미완료. 현재개발049 유지/최종배포승인false. 카페완성작업기·외부게시없음.

'''.replace('38純CPU','38 순수CPU')
 (R/'docs/LIVE049_PAGE_TIMING_BOUNDS.md').write_text(detail+'다음 작업 하나: '+nextaction+'\n','utf-8')
 entry='\n\n## 작업134 —live page/counter/IRQ 범위\n\n4회4200·22호출live1B가129추론과일치/각4200RAM22가중모델exact. 첫page실측42증가(순수38외4미분류),나머지20호출38. 성공143883쓰기전체동일/부족127206중폰트1198값변경과17쓰기1cycle앞당김. 신규scene/ROM없음/사람false. v1callback·검증가정실패보존/v2해결.\n\n[상세 변경·SHA·검증구분·재현·한계](LIVE049_PAGE_TIMING_BOUNDS.md).\n\n다음 작업 하나: '+nextaction+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(LIVE049_PAGE_TIMING_BOUNDS.md)','(../LIVE049_PAGE_TIMING_BOUNDS.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[実測134](docs/LIVE049_PAGE_TIMING_BOUNDS.md)'.replace('実測','실측')+': page38순수cycle/첫42경과와부족IRQ17시각차이를분리기록했다.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업133 이후','작업134 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nextaction+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[R/'docs/LIVE049_PAGE_TIMING_BOUNDS.md',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*134*'),*(R/'qa/reports').glob('live134*.json')]
 for d in ['live134_normal3_047',*[f'live134v2_normal{s}_{b}'for s in [3,4]for b in ['047','049']]]:files.extend((R/'qa/dialogue'/d).iterdir())
 for d in ['work/live134','work/live134_v2']:files.extend((R/d).iterdir())
 manifest.write_text(json.dumps({'work':134,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work134 handoff')
if __name__=='__main__':main()
