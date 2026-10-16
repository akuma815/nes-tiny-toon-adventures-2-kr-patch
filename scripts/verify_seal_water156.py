from pathlib import Path
import hashlib,json,csv,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water156_steer_validation.json';m=R/'manifests/water156_assets.json';assert not out.exists()and not m.exists()
 d=R/'qa/dialogue/water156_firsthazard_steer049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==3300 and(d/'trace_complete.txt').read_text()=='3300'
 for f,h in e['files'].items():assert sha(d/f)==h
 assert e['intervention']=='controller input only; no state loading or RAM/ROM writes'
 assert e['input']['sequence'][-1]=={'frame':2890,'duration':8,'button':'right'}and not rows(d/'damage_events.csv')
 n=rows(d/'water_native.csv');assert [int(x['frame'])for x in n if x['pc']=='A80E']==[2800,2890]and not any(x['pc']in ['A7CF','ACDF','A8E2','A68E','B873']for x in n)
 a=[{k:int(v)for k,v in x.items()}for x in rows(d/'water_player.csv')]
 landing=next(x for x in a if x['frame']>2891 and x['supportC1']==1 and x['jump']==128)
 assert landing['frame']==2922 and landing['life']==3
 recovered=next(x for x in a if x['frame']>=landing['frame']and x['jump']==0);assert recovered['frame']==2930 and recovered['supportC1']==1
 trajectory=[]
 for f in [2892,2910,2922]:
  b=(d/f'frame_{f:05d}_ram.bin').read_bytes();w=lambda x:b[x]+256*b[x+16]
  trajectory.append({'snapshot':f,'player_x':w(0x4a0),'boat_x':w(0x4a1),'player_velocity':w(0x4e0),'boat_velocity':w(0x4e1),'state':b[0x430],'jump':b[0x99],'supportC1':b[0xc1]})
 assert all(x['player_velocity']==452 and x['boat_velocity']==260 for x in trajectory)
 last=(d/'frame_03300_ram.bin').read_bytes();assert last[0x18]==4 and last[0x54]==5 and last[0x7c0]==3 and last[0xc1]==1
 result={'work':156,'status':'PASS_BOUNDED_FIRST_WATER_HAZARD_AVOIDANCE_AND_LANDING','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'frames':3300,'actor_damage_events':0,'landing':landing,'jump_flag_recovered':recovered,'trajectory':trajectory,'final_root':last[0x18],'final_phase':last[0x54],'final_life':last[0x7c0],'human_approved':False,'release_eligible':False,'natural_clear_observed':False,'limits':['First known actor hazard only; no full river or game completion','Controller A+right8 at2890; native velocities verified separately by24CPU pairs','Current049 only; no new source/047 runtime pair/build/apply/reset/state/audio/hardware/human approval']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 nxt='native衝突矩形・空中速度・足場条件を使った急流専用controller入力を設計し、読取専用telemetryと全入力記録付きで自然後半進行を試す。'
 nxt='native충돌사각형·공중속도·발판조건으로 급류 전용 컨트롤러 입력을 설계하고, 읽기전용관측 및 실제입력기록과 함께 자연후반진행을시험한다.'
 detail=f'''# 작업156 — 급류 첫장애물 회피·통나무 재착지

[CPU모델](../qa/reports/water156_air_steer_model.json), [실제검증](../qa/reports/water156_steer_validation.json), [계획](../work/water156/run_plan.json), [준비](../scripts/prepare_water_steer156.py), [검증/인계](../scripts/verify_seal_water156.py).

155의실측boat가로속도260 fixture에서원본/049 nativeA749..A779를24쌍CPU로검증했다. heldright는boat+192/256,left는boat-192/256,no-direction은이전속도를유지한다. source/current명명한코드범위와전체RAM/register출력이같다. 관측boat260에서right는452(1.765625 pixels/frame)이되어움직이는통나무를따라갈수있다. 모델은실제재착지를대신하지않았다.

현재049/3300프레임에155의A8과같은2890 right8만추가했다. 실제두A점프/피해쓰기0·물에빠짐entry0.2892/2910/2922의player속도452/boat260과좌표192/213→223/231→244/243을확인했다.2922supportC1=1/jump128로재착지했고2930jump0으로복귀했다. 최종root4/phase5/체력3/발판1이다. 첫장애물회피와재착지PASS이며급류clear/全game완료가아니다. 이번직접PNG시각검토는없고nativeRAM/코드/실행검증이다.

변경:prepare_water_steer156.py,verify_seal_water156.py,config/water_first_hazard_steer156.json,work/water156계획,새QA,모델/실제보고,상세·인계/journal·canonical·manifest/audit. ROM SHA `{e['rom_sha256']}`,CSV SHA `{result['CSV_sha256']}`불변. 원본·1편·失敗155·이전관측보존. 재현은계획명령의새QA출력과검증코드복제. 정적/동결fixtureSHA·24CPU쌍·controller실행/실제값 PASS. 새build/apply/reset/state/직접PNG/청음/실기/사람최종없음. 자연후반·全corpus·HOWTO/PAUSE/POW·정식배포미완료. 카페기사/게시없음.

다음 작업 하나: {nxt}
'''
 doc=R/'docs/WATER_AIR_STEERING_LANDING.md';assert not doc.exists();doc.write_text(detail,'utf-8')
 entry='\n\n## 작업156 — 급류 공중right/재착지\n\n24CPU쌍 boat260→right452. 실제2890 A+right8으로피해0/2922재착지/2930jump복귀/3300체력3유지.첫장애물경로만PASS·자연clear미달·ROM/CSV불변.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER_AIR_STEERING_LANDING.md).\n\n다음 작업 하나: '+nxt+'\n'
 for name in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/name;s=p.read_text('utf-8')
  if name=='LOCALIZATION_WORK_PLAN.md':s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-07 현재개발049 / 작업156 완료.**',s,count=1)
  p.write_text(s+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text(p.read_text('utf-8')+entry.replace('(WATER_AIR_STEERING_LANDING.md)','(../WATER_AIR_STEERING_LANDING.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[급류회피/착지156](docs/WATER_AIR_STEERING_LANDING.md): native속도모델+실제초기경로.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업155 완료','작업156 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,out,R/'qa/reports/water156_air_steer_model.json',R/'config/water_first_hazard_steer156.json',R/'qa/dialogue/water155_firsthazard049/frame_02892_ram.bin',R/'qa/dialogue/water155_firsthazard049/environment.json',R/'scripts/prepare_water_steer156.py',Path(__file__),R/'scripts/trace_water_damage154.lua',R/'scripts/run_menu_qa.py',R/'scripts/analyze_river120_v2.py',R/'scripts/verify_gate_font_tag_hooks.py',R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv']
 for folder in ['qa/dialogue/water156_firsthazard_steer049','work/water156']:files.extend((R/folder).iterdir())
 m.write_text(json.dumps({'work':156,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
