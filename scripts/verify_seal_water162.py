from pathlib import Path
import csv,json
from PIL import Image,ImageChops
from seal_continuation159 import R,sha,seal
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water162_prediction_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water162_fish_prediction049';h=R/'qa/dialogue/water161_fish_consumer049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and(d/'trace_complete.txt').read_text()=='10500'
 for f,v in e['files'].items():assert sha(d/f)==v
 a,b=rows(d/'adaptive_inputs.csv'),rows(h/'adaptive_inputs.csv');div=next(i for i in range(min(len(a),len(b)))if a[i]!=b[i]);assert a[div]['frame']=='4637';exact=0
 for f in e['files']:
  if not f.startswith('frame_')or int(f[6:11])>=4637:continue
  if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
  else:assert(d/f).read_bytes()==(h/f).read_bytes()
  exact+=1
 tr=rows(d/'raft_transfer.csv');assert [x['stage']for x in tr if x['event']=='native_raft_swap']==['1','2']
 damage=rows(d/'damage_events.csv');hits=[]
 for x in damage:
  if x['address']!='0430':continue
  b=(d/f"damage_{int(x['event']):04d}_before_ram.bin").read_bytes();i=int(x['x']);hits.append({'frame':int(x['frame']),'type_hex':f'{b[0x420+i]:02X}','shape':b[0x530+i],'jump':b[0x99],'support':b[0xc1]})
 assert [x['frame']for x in hits]==[4922,6941,7700]and[h['type_hex']for h in hits]==['34','34','21']and [h['jump']for h in hits[:2]]==[128,128]
 native=rows(d/'water_native.csv');jumps=[int(x['frame'])for x in native if x['pc']=='A80E'];assert 4637 in jumps and 4896 in jumps and 6914 in jumps
 last=(d/'frame_10500_ram.bin').read_bytes();assert last[0x18]==8 and not any(x['pc']in ['A68E','B873']for x in native)
 result={'work':162,'status':'OBSERVED_FIRST_FISH_AVOIDANCE_AND_TWO_TRANSFERS_BUT_ROUTE_DIED','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'same161_input_rows_before_change':div,'same161_snapshot_artifacts_before_change':exact,'frames':10500,'input_rows':len(a),'transfer':tr,'actual_jump_frames':jumps,'actual_hits':hits,'final_root':last[0x18],'final_phase':last[0x54],'natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['Type34 native gravity included but future1step/frame and linear raft velocity remain controller hypotheses','First4658 hit avoided; later fish hits atlanding flag128 and newtype21 exhaust health','No new directvisual/sourcepairedruntime/build/apply/reset/state/audio/hardware/human review']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[검증](../qa/reports/water162_prediction_validation.json), [재현 명령](../work/water162/run_plan.json), [준비](../scripts/prepare_water_fish_controller162.py), [검증/인계](../scripts/verify_seal_water162.py).

前161과4637까지입력{div}행/스냅샷{exact}개가같다. type34/state2의native중력32/step을예측에추가했다. 미래프레임당1물리step/raft일정속도는여전히가설이다.4637 실제점프로기존4658 첫피해를피했다.두번째갈아타기6593→6641도관측(stage2). 그러나4896/6914점프뒤4922/6941jump128착지flag에서물고기피해,7700 type21(shape1) 새피해로체력0이다.10500root8/자연clear없음. 가속도를추가한것만으로완주나전역회피를주장하지않는다.

변경:162준비/Lua/work계획/새QA·보고/검증/상세/인계/journal/canonical·manifest/audit.원본보존·ROM SHA `{e['rom_sha256']}`,CSV SHA `{result['CSV_sha256']}` 불변.각산출물SHA는manifest. 실행/입력·前스냅샷검증PASS,한정첫물고기/두갈아타기관측. 자연clear FAIL/전체게임·corpus·HOWTO/PAUSE/POW미완료. 새직접PNG/build/apply/reset/state/청음/실기/사람최종없음.재현은계획명령·검증사본의새출력경로. 카페원고/게시없음.'''
 files=[out,Path(__file__),R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'qa/reports/water161_fish_validation.json',R/'scripts/trace_water_fish161.lua',R/'scripts/run_menu_qa.py',R/'config/water_first_hazard_steer156.json']
 for pat in ['scripts/*162*','work/water162/*','qa/dialogue/water162_fish_prediction049/*']:files.extend(R.glob(pat))
 seal(162,'WATER_FISH_PREDICTION_FIRST_RESULT.md','첫 물고기 회피와 두 통나무 교체',body,'첫물고기회피/두갈아타기관측.착지flag128에서다음물고기2회피해·새type21피해로체력0.','native A held에 따른 중력30/50hex를 원본/049 CPU로 검증하고, type34 점프 A 지속시간만 늘려 착지 시점 피해가 사라지는지 새 실행으로 확인한다.',files);print('SEALED162 bounded progress; route failed retained')
if __name__=='__main__':main()
