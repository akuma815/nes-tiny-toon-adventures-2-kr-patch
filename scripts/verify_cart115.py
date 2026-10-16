"""Read-only V6 collision observation versus frozen89, with current047 evidence."""
from pathlib import Path
import csv,json,hashlib,collections
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def signed(r,lo,hi):
 n=r[lo]+256*r[hi];return n-65536 if n>=32768 else n
def main():
 out=R/'qa/reports/cart115_validation.json';assert not out.exists()
 q=R/'qa/dialogue/cart115_v6collision047';old=R/'qa/dialogue/cart089_aligned2F046';env=json.loads((q/'environment.json').read_text('utf-8'));oe=json.loads((old/'environment.json').read_text('utf-8'))
 rom=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes()
 assert env['exit_code']==0 and env['frames']==20000 and(q/'trace_complete.txt').read_text()=='20000'
 assert sha(rom)==env['rom_sha256']=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 files={}
 for n,h in env['files'].items():assert sha(q/n)==h;files[(q/n).relative_to(R).as_posix()]=h
 ep=q/'environment.json';files[ep.relative_to(R).as_posix()]=sha(ep)
 base=R/'scripts/trace_cart_rounds_v6.lua';used=q/'capture_survey_used.lua'
 assert used.read_bytes().startswith(base.read_bytes()+b'\n')and b'emu.write('not in used.read_bytes()
 policy=rows(q/'cart_round_policy.csv');prev=rows(old/'cart_round_policy.csv')
 assert sha(old/'cart_round_policy.csv')==oe['files']['cart_round_policy.csv']
 prior=[x for x in prev if int(x['frame'])<20000];assert policy==prior
 release=rows(q/'cart2F_release_policy.csv');old_release=old/'cart2F_release_policy.csv';assert sha(old_release)==oe['files'][old_release.name]
 assert release==[x for x in rows(old_release)if int(x['frame'])<20000]
 until=0;bursts=[]
 for x in release:
  f=int(x['frame'])
  if x['eligible']=='true'and f>=until:until=f+16;bursts.append((f,until))
 paired=collections.defaultdict(list);all_events=rows(q/'collision2F_events.csv')
 for x in all_events:
  assert int(x['PRG_relative'],16)==0x34000+(int(x['pc'],16)%8192)
  if x['event']not in ['pair_test','pair_rejected']:paired[x['serial']].append(x)
 assert paired
 counts=collections.Counter();actual=[]
 for serial,events in paired.items():
  a,z=events[:2];assert a['event']=='before_swap'and z['event']=='after_swap'and events[-1]['event']=='before_collision_exit'
  before=(q/a['RAMfile']).read_bytes();after=(q/z['RAMfile']).read_bytes()
  assert len(before)==len(after)==2048 and a['X']==z['X']=='0F'and a['Y']==z['Y']=='00'
  assert abs(int(a['px'])-int(a['ex']))<24 and abs(int(a['py'])-int(a['ey']))<24
  assert(z['evx'],z['evy'])==(a['pvx'],a['pvy'])and(z['pvx'],z['pvy'])==(a['evx'],a['evy'])
  m=Memory(blob);m.banks=[0x3a,0x3b,0x3e,31];m.ram[:2048]=before;c=MPU(memory=m);m.cpu=c;c.pc=0x9d53;c.x=15;c.y=0;c.a=int(a['A'],16);c.p=0x34
  for n in range(100):
   if c.pc==0x9d93:break
   c.step()
  assert c.pc==0x9d93 and bytes(m.ram[:2048])==after and c.a==int(z['A'],16)
  f=int(a['frame']);active=next((list(x)for x in bursts if x[0]<=f<x[1]),None)
  dot=int(a['pvx'])*(224-int(a['ex']))+int(a['pvy'])*(464-int(a['ey']))
  alignment=signed(before,0x9d,0x9e)*(224-int(a['ex']))+signed(before,0x9b,0x9c)*(464-int(a['ey']))
  direction='toward'if dot>0 else'away'if dot<0 else'zero'
  counts[direction]+=1
  if active:counts['burst_'+direction]+=1;counts['during_burst']+=1
  actual.append({'frame':f,'serial':serial,'CPU_RAM_swap_exact':True,'transferred_velocity':[int(a['pvx']),int(a['pvy'])],'level1_pit_center':[224,464],'actual_incoming_dot':dot,'direction':direction,'native_base_vector_dot':alignment,'within_declared_release_burst':active,'native_held52':before[0x52],'charge':int(a['charge']),'native_course':before[0x25],'native_root':before[0x18],'native_phase':before[0x54]})
 exact=0;screens=0
 for p in sorted(q.glob('frame_*.png')):
  if not(old/p.name).exists():continue
  screens+=1
  for suffix in ['.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv']:
   n=p.stem+suffix;x=q/n;y=old/n;assert sha(y)==oe['files'][n]and x.read_bytes()==y.read_bytes();exact+=1
 native_counts=collections.Counter(x['event']for x in all_events)
 final=[x for x in policy if x['level']=='1'and x['phase']=='05'][-1];assert final['remaining15']=='2F'
 world=rows(q/'world_phase.csv');assert world[-1]['root']=='08'and world[-1]['history']==world[-1]['gold']=='00'
 report={'work':115,'status':'PASS_READ_ONLY_V6_COLLISION_MOMENT_OBSERVATION_NO_NATURAL_CLEAR','ROM047_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_sha256':env['source_sha256'],'frozen_files':len(env['files']),'frames':20000,'V6_controller_prefix_rows_exact':len(policy),'V6_release_prefix_rows_exact':len(release),'V6_common_screens_exact':screens,'V6_common_PNG_RAM_PPU_OAM_mapping_files_exact':exact,'native_pair_event_counts':dict(native_counts),'actual_velocity_swaps_fullRAM_CPU_exact':len(paired),'actual_transfer_directions_correct_level1_pit':dict(counts),'declared_bursts':bursts,'actual_cases':actual,'nativefullclear':False,'last_world':world[-1],'last_play':final,'ROM_CSV_changes':False,'new_build_apply':False,'direct_scene_visual_review':False,'frozen_selected_files':files,'limits':['Controller identicalV6, observer appended only; no game RAM/state/ROM edits. Natural cartfullclear remains failed as frozen89.','Actual incoming speed and direction only for guarded2F/player pairs14000..19000 in level1. No level2 runtime proof.','D-clear CPU replay covers local9D53..9D93 only, excluding NMI/IRQ/PPU. Entire before/afterRAM exact under this local model.','Burst association by declared controller-frame windows. Native held52 field remains authoritative for button seen at contact.','Old89comparison046; current047probe bound independently byROM/envSHA. No new winningpolicy or finalhuman release decision.'],'next_action':'Use observed contact moments to decide whether a single bounded controller correction is justified; preserve the successfulfirstsegment and avoid equivalent V6 replays without new evidence.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:report[k]for k in ['status','V6_controller_prefix_rows_exact','V6_common_PNG_RAM_PPU_OAM_mapping_files_exact','native_pair_event_counts','actual_velocity_swaps_fullRAM_CPU_exact','actual_transfer_directions_correct_level1_pit']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
