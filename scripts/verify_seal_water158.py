from pathlib import Path
import collections,csv,hashlib,json,re
from PIL import Image,ImageChops
from analyze_river120_v2 import machine
from verify_river122_v2 import project
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water158_exit_input_validation.json';mfest=R/'manifests/water158_assets.json';doc=R/'docs/WATER_EXIT_INPUT_AXIS_CORRECTION.md';assert not out.exists()and not mfest.exists()and not doc.exists()
 d=R/'qa/dialogue/water158_exit_input049';h=R/'qa/dialogue/water157_controller049';e=json.loads((d/'environment.json').read_text('utf-8'))
 assert e['exit_code']==0 and(d/'trace_complete.txt').read_text()=='4500'
 for f,v in e['files'].items():assert sha(d/f)==v
 exact=0
 for f in e['files']:
  if not f.startswith('frame_'):continue
  if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
  else:assert(d/f).read_bytes()==(h/f).read_bytes(),f
  exact+=1
 pad=rows(d/'adaptive_inputs.csv');assert pad==rows(h/'adaptive_inputs.csv')[:len(pad)]and len(pad)==4499
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';src,rom=sp.read_bytes(),rp.read_bytes()
 spans=[(0xd592,0xd627),(0x12655,0x1266f),(0x1ffa1,0x1fffd)]
 for a,b in spans:assert src[a:b]==rom[a+0x20000:b+0x20000]
 base=(d/'frame_03990_ram.bin').read_bytes();axis=[]
 for cx in [0,1024]:
  for cy in [0,200,240,460]:
   b=bytearray(base);b[0x1a]=0;b[0x69]=cx>>8;b[0x6d]=cx&255;b[0x68]=cy//240;b[0x6b]=cy%240
   b[0x4b2]=(cx+80)>>8;b[0x4a2]=(cx+80)&255;b[0x482]=(cy+96)//240;b[0x472]=(cy+96)%240
   a,t=project(src,b);z,t2=project(rom,b);assert a==z and t==t2 and a[-1][2]==80 and a[-1][1]==96
   axis.append({'cameraX':cx,'cameraY_packed240':cy,'screenX_RAM02':80,'screenY_RAM01':96,'cycles':a[-2]})
 exits=rows(d/'water_exit.csv');assert [x['pc']for x in exits]==['A658','A65A','A65C']and all(x['frame']=='4023'for x in exits)
 assert [x['phase']for x in exits]==['5','5','9']and all(x['player_yhi']=='1'and x['player_ylo']=='228'and x['life']=='3'for x in exits)
 boundary=[]
 for state in [2,9]:
  for hi in [0,1]:
   for lo in [223,224,228,255]:
    b=bytearray(base);b[0x430]=state;b[0x480]=hi;b[0x470]=lo;b[0x54]=5;pair=[]
    for data in [src,rom]:
     mm,c=machine(data);mm.ram[:2048]=b;c.pc=0xa645;n=0
     while c.pc not in [0xa65f,0xa65c,0xa66e]:c.step();n+=1;assert n<20
     pair.append((c.a,c.x,c.y,c.p,c.sp,c.pc,c.processorCycles,bytes(mm.ram)))
    assert pair[0]==pair[1];failed=state!=9 and hi!=0 and lo>=224;assert(pair[0][5]==0xa65c)==failed
    boundary.append({'state':state,'yhi':hi,'ylo':lo,'failure':failed,'stop_PC':f'{pair[0][5]:04X}'})
 bus=rows(d/'controller_bus.csv');group=collections.defaultdict(list)
 for x in bus:group[int(x['frame'])].append(x)
 requests={int(x['poll']):x for x in pad};accepted=[];unclosed=[]
 for f,g in group.items():
  writes=[x for x in g if x['kind']=='held_write'];samples=[x for x in g if x['kind']=='serial_read'];strobes=[int(x['value'])for x in g if x['kind']=='strobe_write']
  assert strobes==[1,0,1,0]
  if not writes:
   unclosed.append({'frame':f,'serial_read_count':len(samples),'scope':'No RAM52 commit; port2/DMA cause not proven by this port1-only trace'});continue
  p=requests[int(writes[0]['poll_epoch'])];wanted=sum(int(p[k])*v for k,v in [('a',128),('b',64),('select',32),('start',16),('up',8),('down',4),('left',2),('right',1)])
  assert len(writes)==1 and len(samples)==16 and int(writes[0]['value'])==wanted
  bits=[int(x['value'])%2 for x in samples];codes=[sum(bits[j+i]<<(7-i)for i in range(8))for j in [0,8]];assert codes==[wanted,wanted]
  accepted.append(f)
 writes=[x for x in bus if x['kind']=='held_write'];players=rows(d/'water_player.csv');matched=0
 for x in players:
  f=int(x['frame'])
  if not 3301<=f<=4050:continue
  prior=[w for w in writes if int(w['frame'])<f]
  assert prior and int(x['held'])==int(prior[-1]['value']);matched+=1
 old=json.loads((R/'qa/reports/water157_controller_validation.json').read_text('utf-8'));resolved=[]
 for x in old['one_label_assumption_mismatches']:
  f=x['snapshot_frame'];assert f-1 not in group;prior=[w for w in writes if int(w['frame'])<f];assert int(prior[-1]['value'])==x['actual_held']
  resolved.append({'snapshot':f,'no_native_bus_at_request_label':f-1,'last_actual_RAM52_commit_frame':int(prior[-1]['frame']),'actual_held':x['actual_held']})
 result={'work':158,'status':'PASS_BOUNDED_NATIVE_EXIT_AXIS_AND_INPUT_PHASE','ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_sha256':sha(sp),'same157_snapshot_artifacts':exact,'same157_input_rows':len(pad),'native_exit':exits,'axis_CPU_pairs':axis,'bottom_boundary_CPU_pairs':boundary,'controller_bus_events':len(bus),'native_input_sessions':len(group),'accepted_requests_serial_and_RAM52_exact':len(accepted),'held_endframe_records_explained_by_last_actual_commit':matched,'work157_eight_label_mismatches_resolved':resolved,'unclosed_no_RAM52_commit_sessions':unclosed,'axis_correction':'RAM69/6D=cameraX; RAM68/6B=cameraY. RAM02=screenX/RAM01=screenY. Old152-157 vertical names are wrong; values/native predicates retained. Native clear RAM69==16hex means horizontal camera page22.','natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['Port1-only trace explains eight prior snapshot mismatches;18 no-commit sessions are not global input proof, DMA/port2 root cause not established','Native coordinate gate failure observed4023, not actor damage or clear','Original/current code and bounded CPU pairs; no paired full runtime/global timing/audio/hardware/build/apply/human validation']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 nxt='急류 통나무의 B+좌우 native 기울기/이동 코드와 첫 낙차 직전 fixture를 원본/049 CPU로 검증하여, 화면하단 이탈을 피할 입력 후보를 근거로 설계한다.'
 doc.write_text(f'''# 작업158 — 실제 실패 전환·입력 소비·축 이름 정정

[검증](../qa/reports/water158_exit_input_validation.json), [재현 명령](../work/water158/run_plan.json), [실제 컨트롤러 버스](../qa/dialogue/water158_exit_input049/controller_bus.csv), [실제 이탈 코드](../qa/dialogue/water158_exit_input049/water_exit.csv), [준비](../scripts/prepare_water_trace158.py), [검증/인계](../scripts/verify_seal_water158.py).

157과 같은 입력4499행 및2034개 스냅샷 자료가 정확히 같다. 실제4023/A658→A65A→A65C는 phase5→9를 기록했다. 조건은 state09가 아닌 상태에서 플레이어0480!=0/0470>=E0이고 관측값은01/E4, 체력3이다. 원본/049의 해당 코드 및32경계 CPU쌍이 같다. 물/객체 피해 대신 이 좌표 분기가 실패 전환을 일으켰다.

은행36/9582 투영 루틴은 X actor04A/B에서6D/69를 빼 RAM02에, Y actor047/048에서6B/68을 빼 RAM01에 기록한다. 8쌍 CPU는 X80/Y96으로 검증했다. **152–157의 vertical_hi/lo(RAM69/6D)는 cameraX로 정정한다. cameraY는 RAM68/6B다.** 기존 동결문서/CSV/보고는 보존한다. 값·실제 분기·충돌상자 계산은 바꾸지 않으며 진행 최대3/4 및 clear69==16hex는 수평카메라 페이지다. 122의 축 이름 오류와123의 RAM02/01 정정 이력도 보존한다.

3300..4050의13956 버스 사건에서665 native 입력 세션,647번은 두8bit 읽기와 최종요청/RAM52가 정확히 같다. 18세션은 RAM52 기록이 없고 일부 추가읽기/포트2원인은 이번 포트1 관측으로 미폐쇄다. 요청과 소비를 동의어로 사용하지 않는다. 이전157의8 불일치는 직전프레임에 native 입력 읽기가 없었으며 이전 실제 RAM52 쓰기가 모두 설명한다. 플레이 기록750개도 마지막 실제쓰기와 같다. 프레임 라벨을 임의 확대하여 맞추지 않았다.

변경: 새158 준비/Lua/검증 스크립트, work/water158, 새QA·보고·상세/인계/journal/canonical·manifest/audit. 원본 SHA `{sha(sp)}`, ROM SHA `{sha(rp)}`, CSV SHA `{result['CSV_sha256']}` 불변. 각 산출물 SHA는 manifest. 정적/한정CPU/같은입력/실제bus/실패코드 PASS. 새 직접PNG 시각검토·build/apply/reset/state/청음/실기/사람최종 없음. 전체입력무오류/자연완주/全corpus/HOWTO/PAUSE/POW/정식배포 미완료. 재현은계획명령에 새출력경로 및검증출력변경한사본. 카페 원고/게시없음.

다음 작업 하나: {nxt}
''','utf-8')
 entry='\n\n## 작업158 — 실제 급류실패/입력시점/카메라 축정정\n\n4023 nativeA65A phase09 기록,32경계/8투영CPU쌍.157과2034스냅샷/4499입력exact.8라벨불일치는 native소비가 없는 직전프레임으로 설명.647실제입력commit 검증/18무commit 원인미폐쇄. RAM69/6D는cameraX로정정,역사값보존.\n\n[상세 변경·SHA·검증구분·재현·한계](WATER_EXIT_INPUT_AXIS_CORRECTION.md).\n\n다음 작업 하나: '+nxt+'\n'
 for name in ['HANDOFF_2026-10-07.md','SURVEY.md','LOCALIZATION_WORK_PLAN.md']:
  p=R/'docs'/name;s=p.read_text('utf-8')
  if name=='LOCALIZATION_WORK_PLAN.md':s=re.sub(r'^> \*\*.*?\*\*','> **2026-10-07 현재개발049 / 작업158 완료.**',s,count=1)
  p.write_text(s+entry,'utf-8')
 p=R/'docs/journal/2026-10-07.md';p.write_text(p.read_text('utf-8')+entry.replace('(WATER_EXIT_INPUT_AXIS_CORRECTION.md)','(../WATER_EXIT_INPUT_AXIS_CORRECTION.md)'),'utf-8')
 p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n\n[급류실패/입력/축정정158](docs/WATER_EXIT_INPUT_AXIS_CORRECTION.md): RAM69/6D=cameraX, 실제phase09 분기.\n','utf-8')
 p=R/'docs/HANDOFF.md';s=p.read_text('utf-8').replace('작업157 완료','작업158 완료',1);s=re.sub(r'\*\*다음 작업 하나:.*?\*\*','**다음 작업 하나: '+nxt+'**',s,count=1);p.write_text(s+entry,'utf-8')
 files=[doc,out,Path(__file__),sp,rp,R/'workspace/translation/text_ja.csv',R/'scripts/verify_river122_v2.py',R/'scripts/analyze_river120_v2.py',R/'scripts/trace_water_controller157.lua',R/'qa/reports/water157_controller_validation.json',R/'scripts/run_menu_qa.py',R/'config/water_first_hazard_steer156.json']
 for pat in ['scripts/*158*','work/water158/*','qa/dialogue/water158_exit_input049/*']:files.extend(R.glob(pat))
 mfest.write_text(json.dumps({'work':158,'files':{p.relative_to(R).as_posix():sha(p)for p in sorted(set(files))if p.is_file()}},indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','same157_snapshot_artifacts','accepted_requests_serial_and_RAM52_exact','held_endframe_records_explained_by_last_actual_commit']},indent=2))
if __name__=='__main__':main()
