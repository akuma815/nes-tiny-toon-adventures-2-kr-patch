from pathlib import Path
import csv,json
from PIL import Image,ImageChops
from seal_continuation159 import R,sha,seal
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water163_hold_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water163_held_jump049';h=R/'qa/dialogue/water162_fish_prediction049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and(d/'trace_complete.txt').read_text()=='18000'
 for f,v in e['files'].items():assert sha(d/f)==v
 a,b=rows(d/'adaptive_inputs.csv'),rows(h/'adaptive_inputs.csv');div=next(i for i in range(min(len(a),len(b)))if a[i]!=b[i]);assert a[div]['frame']=='4645'
 raw=0;rgb=0;differences=[]
 for f in e['files']:
  if not f.startswith('frame_')or int(f[6:11])>=4645:continue
  if f.endswith('.png'):
   diff=ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB'))
   if diff.getbbox()is None:rgb+=1
   else:differences.append({'file':f,'bbox':diff.getbbox(),'different_pixels':sum(v!=(0,0,0)for v in diff.get_flattened_data()),'current_sha256':sha(d/f),'prior_sha256':sha(h/f)})
  else:assert(d/f).read_bytes()==(h/f).read_bytes();raw+=1
 # Report all observed RGB differences; do not exempt individual frames from an equality assertion.
 tr=rows(d/'raft_transfer.csv');damage=rows(d/'damage_events.csv');assert len(damage)==2 and damage[0]['frame']=='7716'
 ram=(d/'damage_0001_before_ram.bin').read_bytes();i=int(damage[0]['x']);assert ram[0x420+i]==0x21 and damage[1]['before']=='3'and damage[1]['value']=='2'
 exits=rows(d/'water_exit.csv');assert all(x['frame']=='8603'and x['life']=='2'for x in exits)
 tower=(d/'frame_08430_ram.bin').read_bytes();assert tower[0x422:0x425]==bytes([2,2,2])and tower[0x402]==0xed
 result={'work':163,'status':'PASS_BOUNDED_HELD_A_FISH_AVOIDANCE_WITH_ROUTE_FAILURE_AND_RGB_MISMATCH','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'input_rows':len(a),'same162_input_rows_before_change':div,'prefix_nonPNG_artifacts_exact':raw,'prefix_RGB_exact_count':rgb,'prefix_RGB_differences':differences,'whole_prefix_RGB_equality_passed':not differences,'hold_CPU_pairs':10,'actual_damage_events':damage,'avoided_previous_fish_hits':[4658,4922,6941],'transfer':tr,'native_exit':exits,'actual_late_tower_RAM':{'snapshot':8430,'types':list(tower[0x422:0x425]),'art2':tower[0x402],'X2':tower[0x4b2]*256+tower[0x4a2]},'natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['All raw prefix RAM/PPU/OAM/state/mapping exact but one PNG4410 differs7326 pixels; capture/render timing cause not proven, wholevideo equivalence FAIL','Only10CPU held-A cases and actual retained fish/life values; type21 hit remains','Towertype2 differs from rafttype1; controller never attempts this transfer. Native bottom exit8603; no naturalclear','No new sourcepairedruntime/build/apply/reset/state/audio/hardware/human QA']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
 body=f'''[검증](../qa/reports/water163_hold_validation.json), [10CPU중력 모델](../qa/reports/water163_hold_model.json), [준비 v2](../scripts/prepare_water_hold163_v2.py), [준비실패 기록](../qa/reports/water163_v1_preflight_error.json), [재현 명령](../work/water163/run_plan.json), [검증/인계](../scripts/verify_seal_water163.py).

native A held의 중력48/release80을10원본/049 CPU쌍으로 검증했다. type34 점프만A20으로늘려 앞서피해받은3물고기충돌이없고체력3을유지했다. 실제갈아타기stage1/2는이어지고7716의새type21 피해1회로체력2다. 자연8430에type2/2/2 artED/EE/EF 구조물이있고8603 native좌표분기가phase09를쓴다.기존type1 raft2만목표로하는정책은구조물로갈아타기를시도하지않았다.자연급류clear는없다.

입력{div}행(4645이전)은162와같고비PNG raw{raw}개가모두같다. PNG{rgb}개RGB동일,4410 PNG하나는7326pixel/bbox8,0..256,189가다르다. 두PNG를직접검토했다.전체prefix RGB동일판정은FAIL이며특정프레임을예외허용해PASS시키지않았다. 캡처/렌더시점원인은미증명이다. raw동일과영상동일을구분한다. 기존118의이미지/event경계한계와같은종류일가능성은추정뿐이다. 준비v1 문법오류는실행/출력전발생했고보존, v2구문분석후새실행했다.

변경:163준비v1/v2/Lua/work/새QA/CPU·실행보고·검증/상세/인계/journal/canonical·manifest/audit.원본보존·ROM SHA `{e['rom_sha256']}`,CSV SHA `{result['CSV_sha256']}`불변.각산출물SHA는manifest.정적/한정CPU/입력·raw·피해값 검증PASS,전체영상동일과자연완주FAIL. 새build/apply/reset/state/청음/실기/사람최종없음.全corpus/HOWTO/PAUSE/POW/전체게임/정식배포미완료.재현은계획명령·검증사본의새출력경로.카페원고/게시없음.'''
 files=[out,Path(__file__),R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes',R/'workspace/translation/text_ja.csv',R/'scripts/trace_water_fish_controller162.lua',R/'scripts/run_menu_qa.py',R/'scripts/analyze_river120_v2.py',R/'config/water_first_hazard_steer156.json',h/'frame_04410.png']
 for pat in ['scripts/*163*','qa/reports/water163_*','work/water163/*','qa/dialogue/water163_held_jump049/*']:files.extend(R.glob(pat))
 seal(163,'WATER_HELD_A_AND_NATURAL_TOWER.md','A 유지 회피와 자연 후반구조물',body,'A20으로세물고기피해없음.2갈아타기/type21피해1/자연towertype2도달,8603좌표실패.4410 PNG차이로전체영상동일FAIL.','자연8430 구조물type2의 실제 목표/발판 소비코드를 원본/049 CPU와 관측fixture로 연결하고, 통나무와 구분한 구조물 도약 조건을 설계한다.',files);print('SEALED163 raw exact; wholeRGBFAIL retained; fish avoided, laterexit')
if __name__=='__main__':main()
