from pathlib import Path
import hashlib,json,csv,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water155_landing_observation.json';m=R/'manifests/water155_assets.json';assert not out.exists()and not m.exists()
 d=R/'qa/dialogue/water155_firsthazard049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==3300 and(d/'trace_complete.txt').read_text()=='3300'
 for f,h in e['files'].items():assert sha(d/f)==h
 assert e['intervention']=='controller input only; no state loading or RAM/ROM writes'
 assert e['input']['sequence'][-1]=={'frame':2890,'duration':8,'button':'a'}
 assert not rows(d/'damage_events.csv')
 n=rows(d/'water_native.csv');assert [int(x['frame'])for x in n if x['pc']=='A80E']==[2800,2890]
 drowning=next(x for x in n if x['pc']=='A7CF');assert int(drowning['frame'])==2926
 trajectory=[]
 for f in [2880,2892,2910,2922,2928]:
  b=(d/f'frame_{f:05d}_ram.bin').read_bytes();w=lambda a:b[a]+256*b[a+16]
  trajectory.append({'snapshot':f,'player_x':w(0x4a0),'boat_x':w(0x4a1),'player_velocity':w(0x4e0),'boat_velocity':w(0x4e1),'player_y':w(0x470),'state':b[0x430],'jump':b[0x99],'supportC1':b[0xc1],'life':b[0x7c0]})
 assert all(x['life']==3 for x in trajectory)and trajectory[-1]['state']==8 and trajectory[2]['player_velocity']==0 and trajectory[2]['boat_velocity']==260
 result={'work':155,'status':'OBSERVED_FIRST_HAZARD_AVOIDED_BUT_RAFT_LANDING_FAILED','execution_hash_validation':'PASS','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'frames':3300,'new_jump_frame':2890,'actor_damage_events':0,'drowning_entry':drowning,'trajectory':trajectory,'human_approved':False,'release_eligible':False,'natural_clear_observed':False,'limits':['Controller only; avoids prior actor hit but landing failed, not route success','One early A8 test; no new old/source pair/build/apply/reset/state/audio/hardware/human approval']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 visual=R/'qa/reports/water155_visual.json';assert not visual.exists()
 imgs=['qa/dialogue/water155_firsthazard049/frame_02910.png','qa/dialogue/water155_firsthazard049/frame_02940.png']
 visual.write_text(json.dumps({'work':155,'images':{p:sha(R/p)for p in imgs},'status':'DIRECT_ACTUAL_PNG_REVIEW','observations':['2910 airborne avoids actor','2940 in water while boat ahead, three hearts retained'],'human_approved':False},ensure_ascii=False,indent=2)+'\n','utf-8')
 nxt='実測boat速度260に対するA749空中左右入力のnative演算を原本/049 CPUで検証し、2890のA8にright8だけを加えて同じ障害物回避と再着地を試す。'
 nxt='실측통나무속도260에대한 A749 공중좌우입력 native연산을원본/049 CPU로검증하고,2890 A8에right8만추가해같은장애물회피와재착지를시험한다.'
 detail=f'''# 작업155 — 장애물 회피 성공, 재착지 실패

[검증/실패관측](../qa/reports/water155_landing_observation.json), [직접화면](../qa/reports/water155_visual.json), [계획](../work/water155/run_plan.json), [검증·인계](../scripts/verify_seal_water155.py).

현재049/3300프레임에서154의첫native피해2910보다20프레임앞선2890에A8만추가했다. 실제A80E 두번2800/2890이실행됐다. actor피해/체력쓰기0으로첫충돌은피했으나2926 nativeA7CF→state8/ACDF 물에빠짐을관측했다.체력3은유지됐고자연급류clear가아니다.

동결RAM snapshot2880/2892/2910/2922/2928을환경SHA와대조했다.2892부터playerX190/가로velocity0이유지됐지만boatX213→231→243→249와velocity260(1+4/256 pixels/frame)을확인했다.2910 playerY69의공중회피뒤2922Y106에서supportC1=0이었고2928state8이다. 이는jump가물체충돌만피하고통나무재착지조건은만족하지못한서로다른결과다.2910/2940두실제PNG에서공중과통나무앞물에빠짐/체력3을직접봤다.

좌표/속도/시간/RAM/ROM을수정하지않았다.해시/controller runtime와의도한회피판별은PASS지만요구한재착지는FAIL이다. 같은A타이밍유사retry를늘리지않고공중A749의right입력과boat속도상대연산을다음새CPU근거로검증한다.

변경: config/water_first_hazard_jump155.json,work/water155계획,새QA,관측/시각보고서,verify_seal_water155.py,상세·인계/journal·canonical·manifest/audit. ROM SHA `{e['rom_sha256']}`,CSV SHA `{result['CSV_sha256']}`불변. 원본·1편·실패/성공역사자료보존. 재현은계획의새QA출력경로. static/환경SHA·controller runtime·직접2PNG 수행.새build/apply/reset/state/audio/실기/사람최종없음. globalcorpus·自然전체진행·미연결소비·정식배포미완료. 카페완성기사/게시없음.

다음 작업 하나: {nxt}
'''
 doc=R/'docs/WATER_HAZARD_JUMP_LANDING_FAILURE.md';assert not doc.exists();doc.write_text(detail,'utf-8')
 entry='\n\n## 작업155 — 급류 첫장애물회피/재착지실패\n\n2890 A8으로첫actor피해0·체력3.공중playerVx0/boat260으로뒤처져2926state8물에빠짐.회피PASS/재착지FAIL분리·직접2PNG·ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER_HAZARD_JUMP_LANDING_FAILURE.md).\n\n다음 작업 하나: '+nxt+'\n'
 for name in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/name;p.write_text(p.read_text('utf-8')+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text(p.read_text('utf-8')+entry.replace('(WATER_HAZARD_JUMP_LANDING_FAILURE.md)','(../WATER_HAZARD_JUMP_LANDING_FAILURE.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[급류 점프착지155](docs/WATER_HAZARD_JUMP_LANDING_FAILURE.md):첫충돌회피/재착지실패분리.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업154 완료','작업155 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,out,visual,R/'config/water_first_hazard_jump155.json',Path(__file__),R/'scripts/trace_water_damage154.lua',R/'scripts/run_menu_qa.py',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv']
 for folder in ['qa/dialogue/water155_firsthazard049','work/water155']:files.extend((R/folder).iterdir())
 m.write_text(json.dumps({'work':155,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
