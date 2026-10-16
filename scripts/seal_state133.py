"""Document and freeze completed/private226 state/reset evidence and failure."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=R/'manifests/state133_assets.json';assert not manifest.exists();report=R/'qa/reports/state133_validation.json';v=json.loads(report.read_text('utf-8'));assert v['status']=='PASS_BOUNDED049_PRIVATE226_STATE_AND_RESET_REENTRY'
 nextaction='同じ入力の047/049でpage初期化entry/returnの実サイクルとRAM1B・IRQ書込みを読み取り専用で記録し、追加38cyclesとidleRNG差の推論モデルを実測で対照する。'.replace('同じ入力の047/049でpage初期化entry/returnの実サイクルとRAM1B・IRQ書込みを読み取り専用で記録し、追加38cyclesとidleRNG差の推論モデルを実測で対照する。','同一入力047/049のpage初期化entry/return実cycleとRAM1B・IRQ書込みをread-onlyで記録して追加38cyclesとidleRNG推論モデルを実測対照する。')
 nextaction='동일 입력047/049의 page 초기화 entry/return 실제 cycle과 RAM1B·IRQ 쓰기를 읽기 전용으로 기록해 추가38cycles와 idleRNG 추론 모델을 실측 대조한다.'
 detail='''# 작업133 — 현재049 전용 글꼴 저장·복원과 리셋

[검증 보고서](../qa/reports/state133_validation.json), [v1 미실행 기록](../qa/reports/state133_v1_observation.json), [정상 실행 환경](../qa/dialogue/state133_shortage049_v2/environment.json), [리셋 환경](../qa/dialogue/reset133_shortage049/environment.json).

초기1000 일반티켓3 seed 이후 컨트롤러로 부족 안내를 출력했다. native fixed idle FE53의2100에서 같은049 상태를 생성하고2400의같은exec에서 한 번 복원했다. 전용226/227이 실제매핑돼있던시점이며 NMI/성입구top 전용관측점으로 부르지 않는다. 저장직후와복원직후 RAM2KiB/PPU16KiB/OAM256B byte exact, CHR상단2KiB=049226/227 exact. CPU cycle62536565와 PC/매핑/티켓3도 복원됐다.826키중9개 OPLL홀수slot 갱신0→255만다르며 나머지817키는같다.

저장전→저장직후의APU9키 차이는 binary serializer EndFrame 처리다. [고정2.1.1 소스/해시](../work/state085_serializer/source_records.json) 및 [OPLL serializer](../work/savestate_001/source_records.json)를재확인했다. 저장전상태와복원상태를잘못같다고요구하지않았고 모든오디오차이를배제하지않았다. PCM동일성/청음 통과는아니다.

복원후2430/2460/2490/2520/2550의PNG/RAM/PPU/OAM/mapping25파일은현재049기준129의2130/2160/2190/2220/2250과byte exact. Lua의입력frame은되감기지않으므로이300offset은해당입력없는구간에한정된다. 이후2600넘김에서는nativeclear전226/2607phase03에196복귀,2700보유3장NT가129과같다. 임의출력buffer/PC수정없이새입력을처리했다.

리셋은별도실행:2160활성226에서console reset 요청/2161actual이벤트1회,상태load0회.2190에06F3=0으로초기화. title부터반복controller일정으로native새게임티켓10이생겼고4140의10→4161의6으로4차감해출발했다. reset후통화를다시seed하지않았다.4260출발NT/두행RGB는129성공4출발과exact.5400/6300root4/phase5/course0/티켓6/하단font0으로플레이가이어졌다. reset후0티켓부족이라고가정한초기예상은실측10→6 성공으로정정했다.

직접읽은7실제PNG: statev2 2430부족완성/2604넘김/2700보유량,reset2880타이틀/3900비용안내/4260출발/5400롤러코스터. 전체화면전수육안은아니다.3실행의동결6552파일·8672개1KiB CHR조각을ROM과대조했지만v1은실패실험으로구분했다.

실패보존: v1의FD9E성입구top지점은일반대사에서호출되지않았고savestate_events는header만있었다. exit0/trace_complete가실험성공을뜻하지않았다. v2는실제FE53·stop전finalize·명시적experiment_complete·state파일guard로교정했다. 기존v1출력/Lua/실행기그대로보존했다. 이는ROM결함이아니다.

원본/1편/현재ROM/CSV 불변. ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`. 새빌드/패치적용없음.132검토ZIP은작성당시미수행한계를담은동결본으로보존하며이번결과는별도인계에서연결한다.

변경: scripts/prepare_state133.py/v2,run_state133.py/v2,trace_state049_shortage133.lua/v2,trace_reset049_shortage133.lua,verify_state133.py,seal_state133.py; config/reset133_coaster.json; qa/dialogue세폴더; qa/reports미실행/최종보고서; 상세/정본/README/journal. 파일별SHA는동결manifest에기록한다.

재현: `python scripts/run_state133_v2.py --rom build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes --output qa/dialogue/새폴더 --frames 4200 --inputs config/menu_coaster_001.json --seed config/ride_normal3_seed_001.json --script scripts/trace_state049_shortage133_v2.lua`. 리셋은 run_state133.py,frames6300,config/reset133_coaster.json,trace_reset049_shortage133.lua를사용한다. 기존출력을거부한다.

한계: 같은빌드의완성대사대기1시점/리셋1경로뿐이다. 모든저장시점·다른build상태호환·모든resetcontext·전게임자연완주·전역corpus·HOWTO/PAUSE/commonPOW·실기·PCM·사람검토·최종배포는미완료. helper38cycles의게임난수효과는이번왕복으로폐쇄되지않는다. 외부게시/카페완성작업기없음.

'''
 p=R/'docs/STATE049_SHORTAGE_REGRESSION.md';p.write_text(detail+'다음 작업 하나: '+nextaction+'\n','utf-8')
 entry='\n\n## 작업133 —049 전용226 저장·복원/리셋\n\nFE53실제2100저장/2400복원·RAM/PPU/OAMexact·826키중OPLL9refresh만차이,복원후25기준파일exact/다음196복귀. reset2160/actual2161·native10→6입장/플레이·직접7PNG. v1미실행보존/v2완료guard해결. 원본/1편/ROM/CSV보존/사람false.\n\n[상세 변경·SHA·검증 구분·재현·한계](STATE049_SHORTAGE_REGRESSION.md).\n\n다음 작업 하나: '+nextaction+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(STATE049_SHORTAGE_REGRESSION.md)','(../STATE049_SHORTAGE_REGRESSION.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[049状態133](docs/STATE049_SHORTAGE_REGRESSION.md): 전용부족글꼴의동일빌드저장·복원/리셋한정검증.\n','utf-8')
 p=R/'docs/HANDOFF.md';text=p.read_text('utf-8').replace('작업132 이후','작업133 이후');text=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nextaction+'**',text,count=1);p.write_text(text+entry,'utf-8')
 files=[report,R/'qa/reports/state133_v1_observation.json',R/'docs/STATE049_SHORTAGE_REGRESSION.md',R/'config/reset133_coaster.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv']
 for n in ['state133_shortage049','state133_shortage049_v2','reset133_shortage049']:files.extend((R/'qa/dialogue'/n).iterdir())
 for pat in ['*state133*.py','*shortage133*.lua']:files.extend((R/'scripts').glob(pat))
 manifest.write_text(json.dumps({'work':133,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work133 handoff')
if __name__=='__main__':main()
