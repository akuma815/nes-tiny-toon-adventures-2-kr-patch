from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 manifest=R/'manifests/dma135_assets.json';assert not manifest.exists();v=json.loads((R/'qa/reports/dma135_validation.json').read_text('utf-8'));assert v['real_complete_call_delta']==38
 nextaction='부족3의2001프레임 IRQ17쓰기1cycle차이를 실제IRQ vector진입·저장PC·대기opcode/명령cycle과 연결해 handler내부변경인지 interrupt수락시점차이인지 구분한다. ROM변경없이 읽기전용관측으로 확인한다.'
 detail='''# 작업135 — 첫 홈 문단의 DMC 대기 위치와 경계 정정

[최종 검증](../qa/reports/dma135_validation.json), [opcode·DMC 관측v2](../scripts/trace_dma135_v2.lua), [순수CPU 대조v2](../scripts/verify_dma135_v2.py), [정상실행계획](../work/dma135_v2/run_plan.json).

047/049를 각각960프레임 새로 부팅하고 Start720만 입력했다. 금액seed·RAM/PC/ROM수정·상태저장·APU동기화peek가 없다. 최초홈924만opcode추적하고DMC actualread는920..926으로한정했다. QA에유일한이름의동일ROM사본을만들어초기PCM-CDL bit80=0을확인했다. 실제게임PNG/직접장면/청음·build/apply를추가하지않았다.

**134 측정 경계를 정정한다.** 반환직전9445까지의실제차이42는맞지만,134에서뒤에붙인6은순수RTS모델시간이었다. 이번에는실제반환9BBA까지관측했다.047순수207/실제211,049순수245/실제249이며완전한호출차이는둘다38이다. 추가4가현재호출에만생긴것이아니다.047은RTS9445에서모델6/실제10,049는매퍼복귀STA FE00에서모델4/실제8의단일대기가있었다. 당시동일CPUcycle27519253에C686의바이트20을읽었다.047 PC9446/049 PCFE01은대기위치차이다.

원천RAM을각entry에서덤프해같은bank-aware CPU모델에넣었다.047의62/049의80실제명령transition 각각PC/opcode/A/X/Y/SP/실행flags가모델과같고복귀RAM2KiB전부같다. PHP/PLP의표현상B/U두reserved flags만normalize하고나머지6flags는검사했다. 각실행의단하나4cycle명령gap에nativeDMCcursor=address C686,bytesRemaining187,sampleC580/449 읽기가정확히들어있고그주소의새nativePCM-CDL bit80과실제ROM바이트도일치했다.

고정 [Mesen2.1.1 CPU DMA 처리](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/NesCpu.cpp)와 [DMC-CDL 분류](https://github.com/SourMesen/Mesen2/blob/2.1.1/Core/NES/Debugger/NesDebugger.cpp) 로컬SHA를재확인했다. Lua read콜백자체는DMA타입을주지않는다. cursor/양수remaining·새nativePCM표시·실제바이트/동일시각·명령별유일4cyclegap·소스DMA처리를결합해DMC대기의위치이동으로판별한것이다. 실제하드웨어나PCM청음결과는아니다.

920..926의각362읽기는값/순서/frame/cycle/주소/currentcursor/remaining/sample/silence가모두같고PC만5행다르다. 해당7프레임범위이며전구간DMC/PCM동일성은아니다.136에조사할부족3 IRQ17쓰기1cycle차이는이첫홈측정과다른현상이다.

시행착오: v1도960프레임/DMC·CDL은완료했지만fixed exec범위가FDFC에서끝나매퍼helperFE00..FE12 명령을빠뜨렸다. 순수CPU재현step19가FE00으로갔는데다음캡처9439여서부족한커버리지를확인했다. [v1기록](../qa/reports/dma135_v1_observation.json)/원본trace/2QA를보존하고v2범위를FE15로확대해새이름으로2회실행했다. inline modelimport의scripts경로누락은교정했고파일변경없음. verifierv1은UTF8 C++를Windowscp949로읽다중단했으며 [기록](../qa/reports/dma135_verifier_v1_observation.json)과v1을보존하고v2의명시UTF8읽기로해결했다.

정적소스SHA·CPU명령모델·4실행환경/캡처SHA·실제버스관측이다. 초기조사2와최종2를같은종류성공으로합치지않는다. 원본/1편/049/CSV보존, ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`, CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f` 불변.134문서/보고서는동결보존하며현재문서가‘RTS까지6단순추가’해석을정정한다.

변경: scripts/trace_dma135.lua/v2,run_dma135.py/v2,run_dma_pair135.py/v2,prepare_dma135.py/v2,verify_dma135.py/v2,prepare_verify135_v2.py,seal_dma135.py; config/first_home135.json;qa/dialogue4폴더(ROM사본은비공개QA에만);work/dma135/v2;qa/reports관측2/최종;상세/정본/README/오늘journal. 각SHA는동결manifest.

재현 `python scripts/run_dma_pair135_v2.py`, `python scripts/verify_dma135_v2.py`는기존출력거부. 새출력으로단일실행하려면run_dma135_v2.py에ROM/frames960/config first_home135/trace_dma135_v2를지정한다. 전체게임난수동일성/모든호출의RTS대기·부족IRQ시각/전역corpus·HOWTO/PAUSE/POW·자연전체·실기/PCM/사람검토/정식배포는미완료다. 카페완성작업기·외부게시없음.

'''
 (R/'docs/HOME049_DMC_WAIT_BOUNDARY.md').write_text(detail+'다음 작업 하나: '+nextaction+'\n','utf-8')
 entry='\n\n## 작업135 —첫홈DMC대기위치/134경계정정\n\n自然960各2'.replace('自然960各2','자연960각2')+'최종실행·62/80명령모델/RAMexact·362DMC읽기동일. 047RTS6→10/049STA4→8,같은C686/cycle27519253대기4. 실제9BBA반환까지211→249=38.134beforeRTS42는맞으나nominalRTS6추가해석정정. v1범위누락/UTF8읽기실패보존/v2해결. 원본/1편/ROM/CSV보존.\n\n[상세 변경·SHA·검증구분·재현·한계](HOME049_DMC_WAIT_BOUNDARY.md).\n\n다음 작업 하나: '+nextaction+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(HOME049_DMC_WAIT_BOUNDARY.md)','(../HOME049_DMC_WAIT_BOUNDARY.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[처음홈DMC/경계정정135](docs/HOME049_DMC_WAIT_BOUNDARY.md): 두빌드같은4cycle DMC대기위치만이동,완전한실제호출차이38.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업134 이후','작업135 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nextaction+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[R/'docs/HOME049_DMC_WAIT_BOUNDARY.md',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'config/first_home135.json',*(R/'scripts').glob('*135*'),*(R/'qa/reports').glob('dma135*.json')]
 for d in [f'{p}_home{b}'for p in ['dma135','dma135v2']for b in ['047','049']]:files.extend((R/'qa/dialogue'/d).iterdir())
 for d in ['work/dma135','work/dma135_v2']:files.extend((R/d).iterdir())
 files.extend(R/z['path']for z in v['source_records'])
 manifest.write_text(json.dumps({'work':135,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work135 handoff')
if __name__=='__main__':main()
