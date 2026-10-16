from pathlib import Path
import collections,csv,hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/water157_controller_validation.json';assert not out.exists()
 d=R/'qa/dialogue/water157_controller049';e=json.loads((d/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==9000 and(d/'trace_complete.txt').read_text()=='9000'
 for f,h in e['files'].items():assert sha(d/f)==h
 assert e['intervention']=='controller input only; no state loading or RAM/ROM writes'
 assert 'emu.write('not in(d/'capture_survey_used.lua').read_text('utf-8')
 pad=rows(d/'adaptive_inputs.csv');assert len(pad)==8999 and [int(x['poll'])for x in pad]==list(range(1,9000))
 byframe={int(x['frame']):x for x in pad};assert len(byframe)==len(pad)
 player=[{k:int(v)for k,v in x.items()}for x in rows(d/'water_player.csv')];game=[x for x in player if x['phase']==5];assert game
 checked=0;mismatches=[]
 for x in game:
  p=byframe[x['frame']-1];held=sum(int(p[k])*v for k,v in [('a',128),('b',64),('select',32),('start',16),('up',8),('down',4),('left',2),('right',1)])
  checked+=int(x['held']==held)
  if x['held']!=held:mismatches.append({'snapshot_frame':x['frame'],'actual_held':x['held'],'previous_label_request':held,'request_frame':int(p['frame'])})
 h=R/'qa/dialogue/water156_firsthazard_steer049';he=json.loads((h/'environment.json').read_text('utf-8'));prefix=0
 for f in e['files']:
  if not f.startswith('frame_')or int(f[6:11])>3300:continue
  assert sha(h/f)==he['files'][f]
  if f.endswith('.png'):assert ImageChops.difference(Image.open(d/f).convert('RGB'),Image.open(h/f).convert('RGB')).getbbox()is None
  else:assert(d/f).read_bytes()==(h/f).read_bytes()
  prefix+=1
 native=rows(d/'water_native.csv');decisions=rows(d/'jump_decisions.csv');damage=rows(d/'damage_events.csv')
 assert len(decisions)==3 and not damage
 actualjump=[int(x['frame'])for x in native if x['pc']=='A80E'];assert actualjump==[2800,2890]+[int(x['frame'])for x in decisions]
 assert all(x['life']==3 for x in game)and not any(x['pc']in ['A68E','B873']for x in native)
 last=(d/'frame_09000_ram.bin').read_bytes();assert last[0x18]==8
 result={'work':157,'status':'OBSERVED_ACTOR_AVOIDANCE_PASSED_BUT_ROUTE_EXITED_WITHOUT_CLEAR','execution_hash_and_input_request_log_validation':'PASS; request-to-native timing not closed','ROM_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'frames':9000,'complete_input_polls':len(pad),'one_label_request_matches_RAM52':checked,'one_label_assumption_mismatches':mismatches,'request_to_native_RAM_timing_proven':False,'fixed156_prefix_snapshot_artifacts_exact':prefix,'geometry_CPU_pairs':36,'adaptive_jump_decisions':decisions,'actual_jump_frames':actualjump,'actor_damage_events':len(damage),'gameplay_first_last':[game[0]['frame'],game[-1]['frame']],'maximum_RAM69':max(x['vertical_hi']for x in game),'final_life_in_game':game[-1]['life'],'last_gameplay_record':game[-1],'final_root':last[0x18],'final_phase':last[0x54],'natural_clear_observed':False,'human_approved':False,'release_eligible':False,'limits':['Actor avoidance and input REQUEST logging verified; natural water clear failed; final native input phase not yet closed','Predicted future constant velocity is a controller hypothesis, not native future-simulation proof','Historical vertical_hi/lo labels actually name RAM69/6D; axis must be corrected from source consumer before interpreting direction','Environment input.sequence is fixed prefix only; adaptive_inputs.csv is final complete controller evidence','No ROM/CSV/build/apply/reset/state/hardware/audio/human changes']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
