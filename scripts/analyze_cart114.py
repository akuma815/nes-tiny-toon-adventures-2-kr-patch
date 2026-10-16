"""New bounded evidence from frozen cart failures; correct pit context without rerunning a bot."""
from pathlib import Path
import csv,json,hashlib,collections,math
from verify_cart_geometry066 import classify
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/cart114_analysis.json';assert not out.exists()
 original=next((R/'original/rom').glob('*.nes'));current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';previous=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes'
 s=original.read_bytes();c=current.read_bytes();p=previous.read_bytes()
 assert sha(original)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'and sha(current)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 assert s[0x10010:0x18010]==c[0x30010:0x38010]==p[0x30010:0x38010]
 files={};q88=R/'qa/dialogue/cart088_collision046';q89=R/'qa/dialogue/cart089_aligned2F046'
 for directory,names in [(q88,['collision2F_events.csv']),(q89,['cart_round_policy.csv','cart2F_release_policy.csv'])]:
  ep=directory/'environment.json';env=json.loads(ep.read_text('utf-8'));assert env['exit_code']==0 and env['rom_sha256']==sha(previous)
  files[ep.relative_to(R).as_posix()]=sha(ep)
  for name in names:
   f=directory/name;assert sha(f)==env['files'][name];files[f.relative_to(R).as_posix()]=sha(f)
 for name in ['qa/reports/cart_collision088_validation.json','qa/reports/cart089_validation.json','scripts/trace_cart_rounds_v6.lua','qa/reports/cart_clear069_validation.json']:
  files[name]=sha(R/name)
 classification=[]
 for level in range(3):
  for x,y in [(128,256),(224,464),(224,256)]:
   value=classify(c,x//240,x%240,y//256,y%256,level)
   assert value==(15 if(x,y)==[(128,256),(224,464),(224,256)][level]else 0)
   classification.append({'level':level,'xy':[x,y],'native_class':value})
 transfers=collections.Counter();old=collections.Counter();changed=[]
 for x in rows(q88/'collision2F_events.csv'):
  if x['event']!='before_swap':continue
  dot=int(x['pvx'])*(224-int(x['ex']))+int(x['pvy'])*(464-int(x['ey']))
  bad=int(x['pvx'])*(128-int(x['ex']))+int(x['pvy'])*(256-int(x['ey']))
  key=lambda v:'toward'if v>0 else'away'if v<0 else'zero'
  transfers[key(dot)]+=1;old[key(bad)]+=1
  if key(dot)!=key(bad):changed.append({'frame':x['frame'],'serial':x['serial'],'old_dot':bad,'correct_dot':dot})
 assert transfers=={'away':106,'toward':91,'zero':9}and old=={'away':105,'toward':92,'zero':9}
 policy={int(x['frame']):x for x in rows(q89/'cart_round_policy.csv')};release=rows(q89/'cart2F_release_policy.csv');until=0;bursts=[];stats=collections.Counter()
 for x in release:
  f=int(x['frame'])
  if x['eligible']!='true'or f<until:continue
  until=f+16;r=policy[f];assert r['level']=='1'and r['target']=='15'and r['phase']=='05'
  dot=float(r['vx'])*(224-int(r['tx']))+float(r['vy'])*(464-int(r['ty']))
  gate=[k for k in range(f,until)if abs(int(policy[k]['px'])-int(policy[k]['tx']))<24 and abs(int(policy[k]['py'])-int(policy[k]['ty']))<24]
  stats['velocity_toward'if dot>0 else'velocity_away'if dot<0 else'velocity_zero']+=1
  stats['nearby_axis_gate_window'if gate else'no_nearby_axis_gate_window']+=1
  bursts.append({'frame':f,'native_basevector_alignment':float(x['alignment']),'actual_player_vx':float(r['vx']),'actual_player_vy':float(r['vy']),'actual_velocity_dot_to_level1_pit':round(dot,6),'nearby_policy_samples_both_axes_lt24':gate,'meaning':'Input-polled sample only; not an observed CPU collision or proof of transmitted velocity at later contact.'})
 assert len(bursts)==20 and stats=={'velocity_zero':2,'no_nearby_axis_gate_window':15,'velocity_away':10,'velocity_toward':8,'nearby_axis_gate_window':5}
 report={'work':114,'status':'PASS_BOUNDED_NEW_CART_CONTACT_HYPOTHESIS','source_sha256':sha(original),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_046_047_native_cart_38_3B_32KiB_exact':True,'native_pit_classification_cases':classification,'erratum088':{'incorrect_level1_pit_center':[128,256],'correct_level1_pit_center':[224,464],'old_direction_counts':dict(old),'correct_direction_counts':dict(transfers),'classification_changed_events':changed,'unchanged_valid_evidence':'206actualRAM/CPU velocity-swaps,4262rejected pairs,zero fallback and file equality remain frozen88evidence. Direction denominator only corrected; original reports/scripts retained.'},'V6_burst_start_analysis':{'count':20,'counts':dict(stats),'cases':bursts,'hypothesis':'Base vector/heading alignment and stored charge do not ensure actual incoming velocity or collision inside the16frame release window. Confirm actual swap moment under unchangedV6 before proposing a new policy.'},'new_offline_native_CPU_cases':9,'new_emulator_or_direct_scene':False,'ROM_CSV_changes':False,'natural_fullclear':False,'global_corpus_closed':False,'release_eligible':False,'frozen_selected_files':files,'limits':['Old88and89are046 histories, not newly executed047gameplay. Native32KiB exact only binds unchanged game logic/geometry.','Burst-start direction is not actual collision direction. Policy distance window uses sampled inputs, not callback9400pair condition.','Correcting wrong pit coordinate changes one observed88sign, not an identified sole timeout cause.','No repeated winningbot run or state/currency/health/time/ROM intervention.'],'next_action':'Run unchangedV6 controller with read-only actual2F/player collision callbacks in current047, comparing its prefix to frozen89 and capturing the velocity swap during declared16frame bursts; no newwinning policy yet.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in ['status','erratum088','V6_burst_start_analysis']},ensure_ascii=False,indent=2)[:1900])
if __name__=='__main__':main()
