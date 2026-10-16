"""Work88 exact real2F/player velocity swap and bounded collision consumer."""
from pathlib import Path
import hashlib,json,csv,collections,math
from verify_gate_font_tag_hooks import Memory,MPU
from py65.disassembler import Disassembler
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_collision088_validation.json';assert not out.exists();q=R/'qa/dialogue/cart088_collision046';env=json.loads((q/'environment.json').read_text('utf-8'));rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();assert env['rom_sha256']==sha(rom)and env['frames']==20000 and env['exit_code']==0
 for n,h in env['files'].items():assert sha(q/n)==h,n
 rows=list(csv.DictReader((q/'collision2F_events.csv').open()));groups=collections.defaultdict(list)
 for r in rows:
  if r['event']not in ('pair_test','pair_rejected'):groups[r['serial']].append(r)
 assert len(groups)==206
 counts=collections.Counter(r['event']for r in rows);directions=collections.Counter();actual_pc=collections.Counter();toward=away=zero=heldA=charged=0;examples=[]
 for serial,events in groups.items():
  assert events[0]['event']=='before_swap'and events[1]['event']=='after_swap'and events[-1]['event']=='before_collision_exit'
  a,z=events[:2];before=(q/a['RAMfile']).read_bytes();after=(q/z['RAMfile']).read_bytes();assert len(before)==len(after)==2048
  assert a['X']==z['X']=='0F' and a['Y']==z['Y']=='00'
  assert abs(int(a['px'])-int(a['ex']))<24 and abs(int(a['py'])-int(a['ey']))<24
  assert (z['evx'],z['evy'])==(a['pvx'],a['pvy'])and(z['pvx'],z['pvy'])==(a['evx'],a['evy'])
  m=Memory(blob);m.banks=[0x3a,0x3b,0x3e,31];m.ram[:2048]=before;c=MPU(memory=m);m.cpu=c;c.pc=0x9d53;c.x=15;c.y=0;c.a=int(a['A'],16);c.p=0x34;steps=0
  while c.pc!=0x9d93:c.step();steps+=1;assert steps<100
  assert bytes(m.ram[:2048])==after and c.a==int(z['A'],16)
  zero+=a['pvx']==a['pvy']=='0';heldA+=bool(before[0x52]&128);charged+=int(a['charge'])>0
  # Level1 pit center128,256 from source native geometry, not screenshot.
  dot=int(a['pvx'])*(128-int(a['ex']))+int(a['pvy'])*(256-int(a['ey']))
  if dot>0:toward+=1
  elif dot<0:away+=1
  directions[int(a['heading'])]+=1
  if len(examples)<4:examples.append({'frame':a['frame'],'enemy_position':[a['ex'],a['ey']],'player_incoming_velocity':[a['pvx'],a['pvy']],'velocity_dot_toward_pit':dot,'charge':a['charge'],'held52':f'{before[0x52]:02X}'})
  for e in events:actual_pc[e['pc']]+=1
 exact=0;baseline=R/'qa/dialogue/cart087_no2Fbrake046'
 for p in q.glob('frame_*.png'):
  if not(baseline/p.name).exists():continue
  for suffix in ('.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):
   x=q/(p.stem+suffix);assert x.read_bytes()==(baseline/x.name).read_bytes();exact+=1
 policy=list(csv.DictReader((q/'cart_round_policy.csv').open()));old=[r for r in csv.DictReader((baseline/'cart_round_policy.csv').open())if int(r['frame'])<20000];assert policy==old
 mem=Memory(blob);mem.banks=[0x3a,0x3b,0x3e,31];d=Disassembler(MPU(memory=mem));instructions={}
 for r in rows:
  pc=int(r['pc'],16);assert int(r['PRG_relative'],16)==0x34000+(pc%8192);n,t=d.instruction_at(pc);assert '???'not in t;instructions[r['pc']]={'instruction':t,'PRG_relative':r['PRG_relative']}
 result={'work':88,'status':'PASS_NATIVE2F_PLAYER_COLLISION_CONNECTED','ROM_sha256':sha(rom),'ROM_CSV_changes':0,'runtime_frozen_files':len(env['files']),'collision_pair_tests':counts['pair_test'],'pair_rejected':counts['pair_rejected'],'real_collisions_RAM_CPU_replay_exact':len(groups),'zero_speed_fallback_exec':counts['zero_speed_fallback'],'all_observed_exec_instructions':instructions,'all_headings':dict(directions),'incoming_zero_velocity':zero,'incoming_A_held':heldA,'incoming_charge_nonzero':charged,'impulses_toward_pit_dot_positive':toward,'impulses_away_from_pit_dot_negative':away,'examples':examples,'V5_controller_policy_prefix_rows_exact':len(policy),'V5_screenshot_RAM_PPU_OAM_mapping_files_exact':exact,'meaning':'Collision exchanges both8.8 velocity vectors; not a direction-independent push command. Native optional nearzero branch executes8times. Many transferred impulses point away from sourcelevel1 pit center. Incoming direction/contact timing deserves a native-vector-aligned controller experiment. Not solefailure cause or naturalfullclear proof.','erratum_work87':'Frozen work87 prose says8190 runtimefiles; actualruntime8184, declaredworkmanifest8190 including6 nonruntime files. Frozen reports and originals unchanged.','scope':'20k V5 controller unchanged plus read-only exec/RAM capture. LocalDclear CPU replay9D53..9D93 excludes asynchronous interrupts; exact206observedRAMpairs independently checked. No ROM edits/new winningclaim.'}
 out.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','real_collisions_RAM_CPU_replay_exact','zero_speed_fallback_exec','impulses_toward_pit_dot_positive','impulses_away_from_pit_dot_negative','V5_screenshot_RAM_PPU_OAM_mapping_files_exact']}))
if __name__=='__main__':main()