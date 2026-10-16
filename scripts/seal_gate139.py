from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=R/'manifests/gate139_assets.json';assert not m.exists()
 v=json.loads((R/'qa/reports/gate139_validation.json').read_text('utf-8'));assert v['whole_PNG_PPU_OAM_mapping_exact']==786
 nextaction='094 normal50의동결 입력/초기seed/관측기로현재049 성 입장을9000프레임실행해,일반티켓50→0 교환·입장 분기와문단폰트수명을과거047과대조한다.'
 paths=['qa/dialogue/gate139_gold4049/'+f for f in ['frame_02130.png','frame_02280.png','frame_02580.png','frame_03000.png']]
 vr=R/'qa/reports/gate139_visual.json';assert not vr.exists()
 vr.write_text(json.dumps({'work':139,'status':'DIRECT_ACTUAL_PNG_REVIEW','images':{p:sha(R/p)for p in paths},'observations':['2130 slot1C completed 어서 들어오세요 readable','2280 entrance remains clear with Buster entering','2580 castle title/instruction and lower 출발! readable without font mixing','3000 castle gameplay HUD readable'],'scope':'Direct selected emulator PNG review; no human final language approval or natural wholeplay'},ensure_ascii=False,indent=2)+'\n','utf-8')
 detail='''# 작업139 — 현재049 골드4 성 입장

[최종 검증](../qa/reports/gate139_validation.json), [직접 시각검토](../qa/reports/gate139_visual.json), [실행 계획](../work/gate139/run_plan.json), [검증v3](../scripts/verify_gate139_v3.py).

현재049를9000프레임 실행했다. 과거094 gold4/047의 Lua·입력·초기seed·config를SHA대조하고 그대로 사용했다. 초기1000프레임 RAM7E0=4만 명시적으로 쓰고 이후 컨트롤러 입력으로 진행했다. 자연적으로 획득한 티켓/자연완주 증거가 아니다. 원본verify_source PASS,기존047/049 ROM·CSV·1편보존.

786개 whole PNG/PPU/OAM/CHR mapping exact,현재ROM과6288CHR chunks exact. 1079 menu events는25개 helper write PC relocation을 제외한모든값·시점·호출상태exact다. PC9613→964A/C6 9개,9616→964D/6F3 12개,961C→9653/34 4개는실제동일STA 명령바이트(각2/3/2byte)를확인했다. CPU A/flags/idleRAM22/IRQ stack·bus차이는보고서에유지한다. 전체CPU/모든IRQ쓰기시각동일성은주장하지않는다.

native slot1C/font185,상단22/28,하단2A/font196이실행되었다. slot1C 현재ROM stream의단순14glyph와실제NT22A8완성줄이2124부터일치한다. 이는정적바이트+실제완성NT대조이며reader바이트콜백을별도기록한것은아니다. 직접2130/2280/2580/3000 actualPNG를검토했고어서들어오세요·입장·성설명/출발·게임HUD를확인했다. 성gameplay스냅샷475개,최종gold4/normal10이다. 성전체완주/모든방QA가아니다.

검증v1은helperPC까지완전같다고가정해report쓰기전에실패했다. 임시진단이IRQ값차이라고잘못짐작했으나실제차이는helperPC뿐이었다. dictionary Counter사용도tuple누적오류였으며관측v2에정정했다. 검증v2는모든STA를3byteabsolute로가정하고세번째주소도6F4로오인해실패했다. v3는실제주소34와zero-page/absolute길이를확인했다. 실패파일/관측문서보존,실행자료/ROM수정없이해결했다. [v1관측](../qa/reports/gate139_verifier_v1_observation.json), [v2관측/정정](../qa/reports/gate139_verifier_v2_observation.json).

변경: run_gate139.py,verify_gate139.py/v2/v3,prepare_gate139_v2.py/v3,seal_gate139.py;work/gate139계획·runnerlog;qa/dialogue/gate139_gold4049전실행자료;qa/reports검증·관측·직접시각;본상세/정본문서/journal/README와manifest/audit. ROM049 SHA `31dfae821a603d8923b9a32bc1c0bb1ef19b6b98bd2f1670b29e4ea5e4b0f0aa`,CSV SHA `43bc5fe4218d8d01d29425f4dacdc5e92b7eae3db40cb1bb1852ca3e4e7f990f`불변. 개별SHA는동결manifest/environment에기록한다.

정적/동결해시/현재실행/whole영상대조/선택직접PNG PASS. 신규build/apply/state/reset/PCM청음/하드웨어없음. 재현 `python scripts/run_gate139.py`, `python scripts/verify_gate139_v3.py`;기존출력덮어쓰기거부. 글로벌corpus/자연전체완주/HOWTO·PAUSE·POW/사람문체·명칭·그림최종검토/정식배포미완료. 사람승인false. 카페완성작업기/외부게시없음.

'''
 doc=R/'docs/CASTLE049_GOLD4_BRANCH.md';doc.write_text(detail+'다음 작업 하나: '+nextaction+'\n','utf-8')
 entry='\n\n## 작업139 — 현재049 gold4 성 입장\n\n9000프레임/786wholePNG·PPU·OAM·mapping exact/6288CHR chunks. slot1C완성NT/22·28·2A수명/성진입475스냅샷확인·직접4PNG검토. helper25writePCrelocation명령바이트확인/RNG·stack·bus차이유지. 검증가정v1/v2실패보존/v3해결·ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](CASTLE049_GOLD4_BRANCH.md).\n\n다음 작업 하나: '+nextaction+'\n'
 for n in ['HANDOFF_2026-10-06.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/n;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-06.md';p.write_text(p.read_text('utf-8')+entry.replace('(CASTLE049_GOLD4_BRANCH.md)','(../CASTLE049_GOLD4_BRANCH.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[성 gold4 현재049 검증139](docs/CASTLE049_GOLD4_BRANCH.md): 신규slot1C현재완성및성진입,786화면일치.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업138 이후','작업139 이후');s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nextaction+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,vr,R/'qa/reports/gate139_validation.json',R/'qa/reports/gate139_verifier_v1_observation.json',R/'qa/reports/gate139_verifier_v2_observation.json',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',*(R/'scripts').glob('*139*')]
 for d in ['qa/dialogue/gate139_gold4049','work/gate139']:files.extend((R/d).iterdir())
 ep=R/'qa/dialogue/gate094_gold4047/environment.json';e=json.loads(ep.read_text('utf-8'));files.append(ep)
 files.extend(ep.parent/f for f in e['files'])
 m.write_text(json.dumps({'work':139,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print('PASS work139 handoff')
if __name__=='__main__':main()
