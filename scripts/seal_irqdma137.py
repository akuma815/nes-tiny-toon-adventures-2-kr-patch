from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=R/'manifests/irqdma137_assets.json';assert not manifest.exists();v=json.loads((R/'qa/reports/irqdma137_validation.json').read_text('utf-8'));assert v['read_values_order_cursor_sample_state_equal']==257
 nextaction='현재049의동결실행들을54원천별로연결한coverage원장을만들어 실제읽기/폰트·부분출력/완성·과거증거/현재증거/미실행을구분하고,남은등록본문검증의정확한한경로를선택한다.'
 detail='''# 작업137 — IRQ 전 대기의 DMC 지연 연결

[최종 검증](../qa/reports/irqdma137_validation.json), [관측기](../scripts/trace_irqdma137.lua), [검증v2](../scripts/verify_irqdma137_v2.py), [실행 계획](../work/irqdma137/run_plan.json).

047/049각2400프레임/1000 일반티켓3 seed와136의동일입력에,1999..2002의nativeDMCcursor/read와새PCM-CDL을추가했다.유일한이름의동일QA-ROM사본으로초기PCM bit80=0을확인했다.각실행의136 counter/IRQ entry·opcode·read·port/idle6파일은기존136과byte exact.추가관측이진행을바꾸지않았다.

각257실제cursor/read의frame/주소/바이트/원천PRG/remaining/sample/silence/IRQ문맥순서는같다.PC는34행다르고4읽기만시각이±2cycles(각2건)다.모든값이해당ROM바이트와같고소비주소에새nativePCM-CDL bit80이있다.Lua콜백은직접DMA타입을주지않으므로cursor/양수remaining·새typed영역·실제값을결합해판별했다.PCM청음/전역오디오시각동일성은아니다.

대기loop의인접opcode gap204개씩은각각DMC읽기1개와연결됐다.047은3cycle27개/4cycle177개,049는3cycle25개/4cycle179개다.136에서미분류였던4IRQ의각4cyclegap도모두nativeDMC읽기와연결했다.고정 [Mesen2.1.1 DMA정렬](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/NesCpu.cpp) 및 [PCM-CDL분류](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/Debugger/NesDebugger.cpp) 로컬SHA를재확인했다.이는에뮬레이터의bus관측결합결과며실기결과가아니다.

2001의C266읽기전후부터IRQ직전ADC까지1114개PC명령열은같다.1112개exec시각은현재049가1cycle빠르고2개는일시적으로5cycle빠르게관측됐다.두예외는같은바이트/같은시각의4cycleDMC 대기가047의exec콜백전/049의exec콜백후에걸리는위치이동과정확히연결돼다음opcode에서1cycle차이로돌아온다.따라서지속적으로5cycle빠른루프가아니다.여러3/4대기의정렬패턴속에서남은1cycle위상이IRQ까지이어졌고136의같은handler전체19port가함께빨라진것을설명한다.단일sample하나가처음부터모든위상차이를만들었다거나모든IRQ에서같다고주장하지않는다.

이차이를없애는ROM timing padding은만들지않았다.현재049의실제부분/완성/넘김/다음문단과보호화면회귀는129130별도증거다.이조사의1cycle시각차이와4읽기±2cycles를숨기지않고그렇다고픽셀결함으로오인하지않는다.전게임난수/입력결과동일성은미폐쇄다.

실행은첫시도완료.검증v1은두개의-2sample예를보고전체4건도-2만이라고잘못guard해보고서쓰기전실패했다.[관측](../qa/reports/irqdma137_verifier_v1_observation.json)/v1을보존하고v2가정확히+2두건/-2두건을검사했다.원천/캡처/ROM변경없음.

변경: scripts/prepare_irqdma137.py,trace_irqdma137.lua,run_irqdma137.py,run_irqdma_pair137.py,verify_irqdma137.py/v2,prepare_verify137_v2.py,seal_irqdma137.py;qa/dialogue두폴더의고유ROM사본/CDL/DMC/기존6종trace/IRQ RAM/환경;work/irqdma137계획/log;qa/reports최종/관측;상세/정본·README·오늘journal.개별SHA는동결manifest.

ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변.원본/1편/이전증거보존.새build/apply/PNG·직접장면/실기/청음없음.재현 `python scripts/run_irqdma_pair137.py`, `python scripts/verify_irqdma137_v2.py`는기존출력거부.

한계:4프레임DMC관측/같은seed경로만,전역CPU·IRQ·음성타이밍·난수동일성/자연전게임·모든분기·전역corpus·HOWTO/PAUSE/POW 소비·실기/PCM·사람최종검토·정식배포 미완료.현재개발049/최종사람승인false.카페완성작업기·외부게시없음.

'''
 (R/'docs/SHORTAGE049_IDLE_DMC_ALIGNMENT.md').write_text(detail+'다음 작업 하나: '+nextaction+'\n','utf-8')
 entry='\n\n## 작업137 —idle/IRQ DMC 정렬\n\n각2400의6trace가136byte exact/각257DMC바이트·cursor같음,4시각±2(각2)/PC34차이. idle204+IRQ4gap각DMC와연결·1114PCchain의1112개-1/2개-5는같은4wait가exec앞뒤로이동한일시차이. 패딩ROM수정없음/원본·1편·049·CSV보존. v1음수만가정실패보존/v2해결.\n\n[상세 변경·SHA·검증구분·재현·한계](SHORTAGE049_IDLE_DMC_ALIGNMENT.md).\n\n다음 작업 하나: '+nextaction+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(SHORTAGE049_IDLE_DMC_ALIGNMENT.md)','(../SHORTAGE049_IDLE_DMC_ALIGNMENT.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[idle DMC137](docs/SHORTAGE049_IDLE_DMC_ALIGNMENT.md): IRQ이전시점차이를실제DMC정렬에연결,소비바이트보존/4읽기±2cycle은한계로유지.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업136 이후','작업137 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nextaction+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[R/'docs/SHORTAGE049_IDLE_DMC_ALIGNMENT.md',R/'qa/reports/irqdma137_validation.json',R/'qa/reports/irqdma137_verifier_v1_observation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*137*')]
 for d in ['qa/dialogue/irqdma137_normal3_047','qa/dialogue/irqdma137_normal3_049','work/irqdma137']:files.extend((R/d).iterdir())
 files.extend(R/z['path']for z in v['source_records'])
 manifest.write_text(json.dumps({'work':137,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work137 handoff')
if __name__=='__main__':main()
