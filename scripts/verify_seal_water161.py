from pathlib import Path
import csv,json,collections
from PIL import Image,ImageChops
from analyze_river120_v2 import machine
from seal_continuation159 import R,sha,seal
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def setup(data,row,ram):
 m,c=machine(data);m.banks=[int(row[k],16)//8192+32 for k in ['bank8000','bankA000','bankC000','bankE000']];m.ram[:2048]=ram
 c.a=int(row['a']);c.x=int(row['x']);c.y=int(row['y']);c.sp=int(row['sp']);c.p=int(row['ps'])&~8
 return m,c
def main():
 out=R/'qa/reports/water161_fish_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water161_fish_consumer049';h=R/'qa/dialogue/water160_raft_transfer049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and(d/'trace_complete.txt').read_text()=='5100'
 for f,v in e['files'].items():assert sha(d/f)==v
 pads=rows(d/'adaptive_inputs.csv');assert pads==rows(h/'adaptive_inputs.csv')[:len(pads)]and len(pads)==5099
 exact=0
 for f in e['files']:
  if not f.startswith('frame_'):continue
  if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
  else:assert(d/f).read_bytes()==(h/f).read_bytes()
  exact+=1
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';roms=[p.read_bytes()for p in [sp,rp]]
 events=rows(d/'fish_physics_writes.csv');dummy=[];pairs=[]
 for j,row in enumerate(events):
  ram=(d/f"physics_{int(row['event']):04d}_before_ram.bin").read_bytes();addr=int(row['address'],16);pc=int(row['pc'],16)
  assert ram[addr]==int(row['before'])
  if row['preceding3_hex'].startswith('FE')and row['value']==row['before']:
   z=events[j+1];assert z['pc']==row['pc']and z['address']==row['address']and int(z['cycles'])==int(row['cycles'])+1 and int(z['value'])==(int(row['before'])+1)%256
   dummy.append(int(row['event']));continue
  pair=[]
  for data in roms:
   m,c=setup(data,row,ram);c.pc=pc-3;assert bytes(m[c.pc+i]for i in range(3)).hex().upper()==row['preceding3_hex'];c.step()
   expected=bytearray(ram);expected[addr]=int(row['value']);assert m.ram[:2048]==expected and c.pc==pc
   pair.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram)))
  assert pair[0]==pair[1];pairs.append({'event':int(row['event']),'store_PC':f'{pc-3:04X}','address':row['address'],'cycles':pair[0][-2]})
 swap=[x for x in events if x['slot']=='-1'];assert len(swap)==1 and swap[0]['pc']=='A5BE'and swap[0]['preceding3_hex']=='EE1607'and swap[0]['frame']=='4034'
 first=next(x for x in events if x['pc']=='8278');ram=(d/f"physics_{int(first['event']):04d}_before_ram.bin").read_bytes();grav=[]
 for hi in [0xfc,0xff,0,4]:
  for lo in [0,127,255]:
   b=bytearray(ram);i=int(first['slot']);b[0x4d0+i]=hi;b[0x4c0+i]=lo;pair=[]
   for data in roms:
    m,c=setup(data,first,b);c.pc=0x826f;n=0
    while c.pc!=0x8280:c.step();n+=1;assert n<10
    velocity=m.ram[0x4c0+i]+256*m.ram[0x4d0+i];assert velocity==((hi*256+lo+32)&65535)
    pair.append((c.a,c.x,c.y,c.p,c.sp,c.processorCycles,bytes(m.ram)))
   assert pair[0]==pair[1];grav.append({'velocity_before_word':hi*256+lo,'after_word':velocity,'cycles':pair[0][-2]})
 result={'work':161,'status':'PASS_ACTUAL_FISH_GRAVITY_AND_RAFT_SWAP_CONSUMERS','source_sha256':sha(sp),'ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'same160_input_rows':len(pads),'same160_snapshot_artifacts':exact,'actual_physics_events':len(events),'RMW_dummy_write_events':dummy,'single_instruction_CPU_pairs':pairs,'gravity_CPU_pairs':grav,'native_raft_swap_store':swap[0],'finding':'Fish type34/state2 initializes Vx0140/VyFC7F; native826F adds0020 to signed16-bit Vy per actual physics step. Before first damage fish descends toward player; constant-velocity type44-only controller does not cover this actor. Actual A5BB INC0716 observed4034 (inputPolled observation4035).','natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['183 observed writes include2 INC dummy writes;181 final-store source/current pairs and12 gravity cases, not183 independent instructions','Gravity per native step, not guaranteed once each video frame; lag frames and future trajectory remain separate','No new input/controller success, fullroute/build/apply/visual/audio/hardware/human QA']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[검증](../qa/reports/water161_fish_validation.json), [재현 명령](../work/water161/run_plan.json), [실제 쓰기](../qa/dialogue/water161_fish_consumer049/fish_physics_writes.csv), [물고기 궤적](../qa/dialogue/water161_fish_consumer049/fish_actors.csv), [준비](../scripts/prepare_water_fish161.py), [검증/인계](../scripts/verify_seal_water161.py).

160과5099입력/2154스냅샷 자료가 같다.183 실제쓰기 중2는 INC의 dummy쓰기,181은 최종쓰기다.181원본/049 한명령 CPU쌍이 beforeRAM 및 실제쓰기값과 같다. 별도12 CPU쌍은 native826F의 Vy+0020(0.125pixel/native step)을 검증한다. type34/state2는 Vx0140/VyFC7F로 시작하며 올라갔다 내려오는 곡선이다. 프레임마다 반드시 한물리step이라고 주장하지 않는다. 이전 type44 일정속도예측은 물고기 유형과 가속도를 다루지 않았다.

통나무교체 실제생산자는4034 A5BB INC0716(콜백pcA5BE/PRG325BE)이며0→1이다.160의4035 inputPolled 관측은 다른 event경계임을 구분한다. 두피해 입력/결과를 그대로 재현했으며 새회피성공은 없다.

변경:161준비/Lua/검증·work계획·새QA/보고·상세/인계/journal/canonical·manifest/audit. 원본SHA `{sha(sp)}`,ROM SHA `{sha(rp)}`,CSV SHA `{result['CSV_sha256']}` 불변.각산출물SHA는manifest. 정적/193CPU쌍/실제consumer/입력·스냅샷exact PASS. 새입력성공/직접PNG/build/apply/reset/state/청음/실기/사람최종없음. 自然전체완주/전역corpus/HOWTO/PAUSE/POW/정식배포미완료. 재현은계획명령·검증사본에새출력경로.카페원고/게시없음.'''
 files=[out,Path(__file__),sp,rp,R/'workspace/translation/text_ja.csv',R/'scripts/analyze_river120_v2.py',R/'scripts/verify_gate_font_tag_hooks.py',R/'scripts/trace_water_transfer160.lua',R/'scripts/run_menu_qa.py',R/'config/water_first_hazard_steer156.json']
 for pat in ['scripts/*161*','work/water161/*','qa/dialogue/water161_fish_consumer049/*']:files.extend(R.glob(pat))
 seal(161,'WATER_FISH_AND_SWAP_NATIVE_CONSUMERS.md','물고기 중력과 통나무교체 실제소비',body,'같은입력/스냅샷,181최종쓰기+12중력CPU쌍.물고기Vy+32/step,통나무INC0716 실제PC 연결.','확인한 type34의 중력을 포함해 다음 충돌을 예측하는 컨트롤러를 설계하고, 새049 실제입력/피해/갈아타기/후반진행을 검증한다.',files);print('PASS161 181 final-store+12 gravity pairs;2 dummy writes preserved')
if __name__=='__main__':main()
