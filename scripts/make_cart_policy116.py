"""One bounded heading-hold experiment from observed V6 contact timelines."""
from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart116_policy_basis.json';target=R/'scripts/trace_cart_rounds_v7.lua';runner=R/'scripts/run_cart_rounds_qa_v7.py'
 assert not out.exists()and not target.exists()and not runner.exists()
 q=R/'qa/dialogue/cart115_v6collision047';env=json.loads((q/'environment.json').read_text('utf-8'));ep=q/'environment.json';rp=R/'qa/reports/cart115_validation.json';report=json.loads(rp.read_text('utf-8'));log=q/'cart_round_policy.csv'
 assert env['exit_code']==0 and sha(log)==env['files'][log.name]
 policy={int(x['frame']):x for x in csv.DictReader(log.open(encoding='utf-8'))};timelines=[]
 for f,t in report['declared_bursts']:
  direction=int(policy[f]['mask'],16)&15
  changed=[k for k in range(f,t)if int(policy[k]['mask'],16)&15!=direction]
  contacts=[x for x in report['actual_cases']if x['within_declared_release_burst']==[f,t]]
  timelines.append({'start':f,'end_exclusive':t,'first_direction_mask':f'{direction:02X}','samples':[{k:policy[frame][k]for k in ['frame','mode','mask','px','py','tx','ty','vx','vy']}for frame in range(f,t)],'direction_changed_frames':changed,'actual_contacts':[{'frame':x['frame'],'direction':x['direction'],'native_held52':x['native_held52'],'incoming_dot':x['actual_incoming_dot']}for x in contacts],'pit_avoid_samples':sum(policy[k]['mode']=='pit_avoid'for k in range(f,t))})
 windows=sum(bool(x['direction_changed_frames'])for x in timelines);changed=sum(len(x['direction_changed_frames'])for x in timelines)
 assert len(timelines)==20 and(windows,changed)==(14,84)
 base=R/'scripts/trace_cart_rounds_v6.lua';s=base.read_text('utf-8')
 substitutions=[('local burst_until=0','local burst_until=0\nlocal locked_direction=0'),('if eligible and frame>=burst_until then burst_until=frame+16 end','if eligible and frame>=burst_until then burst_until=frame+16;locked_direction=direction end'),("if frame<burst_until then input.a=false elseif push2F then input.a=true end", """if frame<burst_until then
     input.a=false
     -- One changed behavior: keep launch direction during this2F release window, except pit avoidance.
     if mode~='pit_avoid' then
      input.right=(locked_direction&1)~=0;input.left=(locked_direction&2)~=0
      input.down=(locked_direction&4)~=0;input.up=(locked_direction&8)~=0
     end
    elseif push2F then input.a=true end""")]
 for a,b in substitutions:assert s.count(a)==1;s=s.replace(a,b)
 # Deleting these exact additions restores the immutable V6; no geometry/timer/charge/firstlevel edits.
 reverse=s
 for a,b in reversed(substitutions):assert reverse.count(b)==1;reverse=reverse.replace(b,a)
 assert reverse==base.read_text('utf-8')and 'emu.write('not in s
 target.write_text(s,'utf-8')
 wrapper=(R/'scripts/run_cart_collision115.py').read_text('utf-8').replace('trace_cart_collision115_v1.lua','trace_cart_rounds_v7.lua')
 a=wrapper.index("        'intervention':");b=wrapper.index("        'files':",a)
 wrapper=wrapper[:a]+"        'intervention':'V7 controller-only experiment: frozenV6 plus hold the release-start2F direction for16frames; pit avoidance steering retained. Level0/charge/geometry/timer/ROM unchanged; no RAM/PC/state/health/time/currency edits.',\n"+wrapper[b:]
 runner.write_text(wrapper,'utf-8')
 files={p.relative_to(R).as_posix():sha(p)for p in [ep,rp,log,base,target,runner]}
 result={'work':116,'status':'BOUNDED_V7_HEADING_HOLD_EXPERIMENT_PREPARED_NOT_EXECUTED','ROM047_sha256':report['ROM047_sha256'],'CSV_sha256':report['CSV_sha256'],'actual_V6_release_windows':20,'direction_changes_within_windows':windows,'changed_direction_samples':changed,'timelines':timelines,'source_to_candidate_exact_reversible_substitutions':3,'one_behavior_changed':'During existing level>=1/target2F16frame release window, hold the launch direction. Retain pit_avoid override. Firstlevel/charge/release eligibility/B threshold/geometry unchanged.','basis':'Two burst contact events observed in intercept with changed heading and away transfer; several contact chains occur without headingchanges. Directionhold is boundedpartial hypothesis, not cure for all7away contacts or guaranteed naturalclear.','source_ROM_or_CSV_changes':False,'new_CPU_or_emulator_or_scene':False,'release_eligible':False,'human_final_approval':False,'frozen_selected_files':files,'limits':['Frozen trajectories do not predict new candidate trajectory. Future nativeplay/history/tickets must decide actual progress.','Directionhold may alter later positions/contacts; pit_avoid steering remains dynamic for safety.','Other recurrent swap contacts18404window not solved by directionhold alone. No equivalentwinningbot retries automatically justified if it fails.'],'next_action':'Run one current047 V7 controller-only36000frame experiment, verify prefix before firstdirectionoverride and native stage/history/gold outcome; preserve success/failure without further equivalent retry.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','actual_V6_release_windows','direction_changes_within_windows','changed_direction_samples','source_to_candidate_exact_reversible_substitutions']}))
if __name__=='__main__':main()
