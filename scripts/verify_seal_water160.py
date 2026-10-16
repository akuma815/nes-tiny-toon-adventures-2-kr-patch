from pathlib import Path
import csv,json
from PIL import Image,ImageChops
from seal_continuation159 import R,sha,seal
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water160_transfer_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water160_raft_transfer049';h=R/'qa/dialogue/water158_exit_input049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and(d/'trace_complete.txt').read_text()=='6500'
 for f,v in e['files'].items():assert sha(d/f)==v
 a,b=rows(d/'adaptive_inputs.csv'),rows(h/'adaptive_inputs.csv');div=next(i for i in range(min(len(a),len(b)))if a[i]!=b[i]);assert a[div]['frame']=='3985'
 exact=0
 for f in e['files']:
  if not f.startswith('frame_')or int(f[6:11])>=3985:continue
  if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
  else:assert(d/f).read_bytes()==(h/f).read_bytes()
  exact+=1
 tr=rows(d/'raft_transfer.csv');assert [(x['frame'],x['event'],x['stage'])for x in tr]==[('3985','begin','0'),('4035','native_raft_swap','1')]
 landing=(d/'frame_04050_ram.bin').read_bytes();last=(d/'frame_06500_ram.bin').read_bytes()
 assert landing[0x716]==1 and landing[0xc1]==1 and landing[0x99]==0 and landing[0x54]==5 and landing[0x7c0]==3
 assert last[0x18]==4 and last[0x54]==5 and last[0xc1]==1 and last[0x7c0]==1 and not rows(d/'water_exit.csv')
 damage=rows(d/'damage_events.csv');hazards=[]
 for x in damage:
  if x['address']!='0430':continue
  ram=(d/f"damage_{int(x['event']):04d}_before_ram.bin").read_bytes();i=int(x['x']);assert x['pc']=='E6E7'and ram[0x420+i]==0x34
  hazards.append({'frame':int(x['frame']),'actor':i,'type_hex':'34','art_hex':f'{ram[0x400+i]:02X}','state':ram[0x430+i],'shape':ram[0x530+i]})
 assert len(hazards)==2 and [(x['before'],x['value'])for x in damage if x['address']=='07C0']==[('3','2'),('2','1')]
 sp=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';rp=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';src,rom=sp.read_bytes(),rp.read_bytes();assert src[0x12594:0x125d6]==rom[0x32594:0x325d6]
 result={'work':160,'status':'PASS_FIRST_NATURAL_RAFT_TRANSFER_CONTINUATION_WITH_TWO_NEW_HITS','ROM_sha256':sha(rp),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'input_rows':len(a),'same158_input_rows_before_change':div,'same158_snapshot_artifacts_before_change':exact,'transfer':tr,'landing_snapshot':4050,'last_root':last[0x18],'last_phase':last[0x54],'last_life':last[0x7c0],'last_cameraX':[last[0x69],last[0x6d]],'actual_new_damage_hazards':hazards,'visual_review':{f:sha(d/f)for f in ['frame_04020.png','frame_04050.png']},'natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['Native0716 change and landing observed; exact producerPC not newly callback-traced','Two fish type34 hits outside previous type44 controller scope; health1 and still in play at6500, not river clear','No new source/047 paired fullruntime/build/apply/reset/state/audio/hardware/human review']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[검증](../qa/reports/water160_transfer_validation.json), [계획/재현 명령](../work/water160/run_plan.json), [입력전수](../qa/dialogue/water160_raft_transfer049/adaptive_inputs.csv), [갈아타기 관측](../qa/dialogue/water160_raft_transfer049/raft_transfer.csv), [준비](../scripts/prepare_water_transfer160.py), [검증/인계](../scripts/verify_seal_water160.py).

3985까지 이전158과 입력{div}행/스냅샷{exact}개가 같다.3985 실제 낙하 통나무·앞 raft2 조건에서 A+우측을 시작했다.4035 native stage0716=1/raft1교체를 관측했고4050 jump0/support1/체력3으로 재착지했다. native생산자 A584..A5C6 source/current바이트는 같지만 이번에 PC 실행 콜백은 추가하지 않았다. 실제4020 공중·4050 두번째통나무 착지 PNG를 직접검토했다.이전4023 실패분기는없고6500 root4/phase5/발판1로진행했다.

4658/4925 두 피해는 실제 actor type34/art5F(shape0,state2)이다. 이전 type44만예측한범위밖이다. 체력3→2→1이며자연clear없음. 물고기 움직임의 실제 소비코드를 다음에 읽기전용 관측한다. 임의 무적/좌표/시간/ROM/RAM 개입없고 controller만조작했다.

변경:160준비/Lua/검증·work계획·새QA·보고·상세/인계/journal/canonical·manifest/audit. 원본 SHA `{sha(sp)}`,ROM SHA `{sha(rp)}`,CSV SHA `{result['CSV_sha256']}` 불변.각산출물 SHA는manifest. 정적/실행/첫자연갈아타기/2직접PNG한정 PASS. 자연급류clear와전체게임·전역corpus/HOWTO/PAUSE/POW미완료. 새build/apply/reset/state/청음/실기/사람최종없음. 재현은계획명령및검증사본에새출력경로사용. 카페원고/게시없음.'''
 files=[out,Path(__file__),sp,rp,R/'workspace/translation/text_ja.csv',R/'scripts/trace_water_exit_input158.lua',R/'scripts/run_menu_qa.py',R/'config/water_first_hazard_steer156.json']
 for pat in ['scripts/*160*','work/water160/*','qa/dialogue/water160_raft_transfer049/*']:files.extend(R.glob(pat))
 seal(160,'WATER_FIRST_NATURAL_RAFT_TRANSFER.md','첫 자연 통나무 갈아타기',body,'3985 A→4035 native교체/4050 착지.6500까지진행,새물고기피해2회·체력1·clear없음.','160의 같은 입력으로 첫 물고기 type34의 실제 속도/상태 쓰기와 native갈아타기0716 쓰기를 읽기전용으로 추적한다.',files);print('PASS160 first transfer; two fish hits retained')
if __name__=='__main__':main()
