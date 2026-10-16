from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/gate140_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/gate140_validation.json').read_text('utf-8'));assert v['final_normal']==0 and v['whole_PNG_PPU_OAM_mapping_exact']==786
 nxt='현재049의점수3 booth 성공교환을새047baseline과동일입력·seed로실행하며,실제PRG data읽기매핑을추가관측해 slot15 farewell과macro88 소비·완성·clear를연결한다.'
 paths=['qa/dialogue/gate140_normal50049/'+f for f in ['frame_02760.png','frame_03060.png','frame_03480.png','frame_04500.png']]
 vr=R/'qa/reports/gate140_visual_counter.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':140,'direct_actual_PNG_review':{p:sha(R/p)for p in paths},'observations':['2760 교환할까요? readable','3060 어서 들어오세요 readable with entry','3480 castle instruction and lower 출발! readable','4500 castle gameplay HUD normal000 gold0'],'counter_snapshot_transitions':[[30,[0,0,0],0],[600,[0,1,0],0],[1020,[0,5,0],0],[2718,[0,0,0],0]],'scope':'Snapshot first-observed transitions, not exact write cycle; seed at1000; no naturally earned currency or wholeplay/human approval'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail='''# 작업140 — 현재049 일반티켓50 성 입장

[최종 검증](../qa/reports/gate140_validation.json), [직접PNG·숫자변화](../qa/reports/gate140_visual_counter.json), [실행계획](../work/gate140/run_plan.json), [검증](../scripts/verify_gate140.py).

094 normal50 동결Lua·입력·초기seed를사용해현재049를9000프레임실행했다.1000에normal digits[0,5,0]만설정한명시적진단이며티켓을자연획득하지않았다.기록된최초snapshot1020의50이2718에0이되었고gold는0으로유지된다.정확한write cycle판정은아니다.최종normal0/gold0과성gameplay293스냅샷을확인했다.

과거047과786wholePNG·PPU·OAM·mapping exact/6288CHR chunks currentROM exact.1614menu events는helper34writePC의동일STA명령바이트를확인한제외외모든필드동일. C6 12/6F3 15/34 7개다. slot1C의현재NT14glyph완성은3024부터확인했다.상단22/28·lower2A/clear·출발수명이정상이다.2760교환질문/3060환영/3480설명·출발/4500게임HUD4actualPNG를직접검토했다.원래일반50이0으로바뀌어입장하는경로가현재049에서도유지된다.

RAM22/IRQ stack1FC·1FD·1FE,CPU A/flags/PC·bus차이는보고서에따로기록한다.全CPU/매IRQ시각/RNG결과의전역동일성은아니다.실제source-reader callback은아직없고static stream+actualNT대조다.139에서해결한명령길이/PCrelocation guard를재사용했으며140신규실패없음.과거139실패문서는보존한다.

변경: prepare_gate140.py/run_gate140.py/verify_gate140.py/seal_gate140.py,work/gate140계획·log,qa/dialogue/gate140_normal50049,최종/직접시각보고서,상세/datedhandoff·journal·README·SURVEY·PLAN·HANDOFF,manifest/audit.원본/1편/049/CSV불변.ROM SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7ae3db40cb1bb1852ca3e4e7f990f`의정확값은검증/manifest의실제SHA를참조한다.

정적/해시/seeded runtime/whole영상대조/직접4PNG PASS.신규ROM/build/apply/state/reset/audio청음/하드웨어없음.재현 `python scripts/prepare_gate140.py`, `python scripts/run_gate140.py`, `python scripts/verify_gate140.py`;기존출력거부.글로벌corpus/자연성완주/全game/HOWTO·PAUSE·POW/사람문체·명칭·그림최종/정식배포미완료.사람승인false/카페완성기사·외부게시없음.

'''
 # Keep the literal CSV digest exact; report is the authoritative value.
 detail=detail.replace('43bc5fe4218d8d01d29425f4dacdc5e92b7ae3db40cb1bb1852ca3e4e7f990f',v['CSV_sha256'])
 doc=R/'docs/CASTLE049_NORMAL50_BRANCH.md';doc.write_text(detail+'다음 작업 하나: '+nxt+'\n','utf-8')
 entry='\n\n## 작업140 — 현재049 normal50 성 입장\n\n9000프레임/786wholePNG·PPU·OAM·mapping/6288CHR exact.50→0/gold0·성입장293snapshot/slot1C완성NT확인·4actualPNG직접검토.1614events/helper34PCrelocation검증·idle/stack/bus차이유지.ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](CASTLE049_NORMAL50_BRANCH.md).\n\n다음 작업 하나: '+nxt+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(CASTLE049_NORMAL50_BRANCH.md)','(../CASTLE049_NORMAL50_BRANCH.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[성 normal50 현재049 검증140](docs/CASTLE049_NORMAL50_BRANCH.md): 일반50→0 진입·786화면일치.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업139 이후','작업140 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/gate140_validation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*140*')]
 for d in ['qa/dialogue/gate140_normal50049','work/gate140']:files.extend((R/d).iterdir())
 ep=R/'qa/dialogue/gate094_normal50047/environment.json';e=json.loads(ep.read_text('utf-8'));files.append(ep);files.extend(ep.parent/f for f in e['files'])
 m.write_text(json.dumps({'work':140,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work140 handoff')
if __name__=='__main__':main()
