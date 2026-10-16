from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_pursuit064_validation.json';assert not out.exists();q=R/'qa/dialogue/cart064_pursuit_v1';e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==18000 and(q/'trace_complete.txt').read_text()=='18000';rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)==e['rom_sha256'];blob=rom.read_bytes()
 for p,h in e['files'].items():assert sha(q/p)==h,p
 rows=list(csv.DictReader((q/'cart_policy.csv').open()));assert rows
 for x in rows:
  mask=int(x['mask'],16);assert not(mask&1 and mask&2)and not(mask&4 and mask&8)
  if int(x['desired_heading'])>=0:assert x['root']=='04'and x['phase']=='05'and x['course']=='01'and 0<=int(x['heading'])<=7 and(int(x['target_type'])in (-1,46,47))
 world=list(csv.DictReader((q/'world_phase.csv').open()));assert len(world)==600;bonus=[x for x in world if x['root']=='04'and 32<=int(x['phase'],16)<=36];assert not bonus and world[-1]['history']==world[-1]['gold']=='00'
 images=list(q.glob('frame_*.png'));chunks=0
 for p in images:
  pp=(q/(p.stem+'_ppu.bin')).read_bytes()
  for m in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
   if m['kind']!='chr':continue
   a=int(m['cpu_or_ppu_address'],16);off=int(m['relative_offset'],16);assert pp[a:a+1024]==blob[0x40010+off:0x40410+off];chunks+=1
 a=(q/'frame_18000_ram.bin').read_bytes();score=sum(v*10**i for i,v in enumerate(a[0x7f0:0x7f7]))*10
 report={'work':64,'status':'BOUNDED_EXECUTION_PASS_NATURALCLEAR_NOT_REACHED','scope':'Controller-only adaptive pursuit decisions and18k nativecart execution; no winningbot claim','ROM_sha256':sha(rom),'ROM_SSOT_changes':0,'runtime_frozen_files':len(e['files']),'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'policy_rows':len(rows),'native_play_sample_count':sum(x['root']=='04'and x['phase']=='05'for x in world),'bonus_observed':False,'last_world':world[-1],'last_score':score,'life3_to2_to1':True,'A_B_semantics_scope':'Firstpolicy assumed B forspeed and shortnearA pulse without priorcharge characterization. NativeA294 incrementsA9/AA to4; release branch974C..9773 converts headingvector andcharge to velocity viaA088/A0D1. Nextpolicy tests realcharge/release, Bmeaning not definitivelynamed.','native_charge_source':'work/cart_control_001/A294_acceleration_candidate.json and velocity_apply_A0D1.json','direct_visual':'Actual6000 viewed; no all-screen humanQA','limits':['Failednaturalclear attempt; currentlycartplayat18k withlife1/history0/gold0','No seed/life/phase/PC/ROM/state interventions','Player/enemy integercoordinate pursuit isnot obstacle-routing proof','No PCM/listening/hardware/fullgameplay/finalhumanreview'],'next_action':'Use source-confirmed A charge/release pulses with Bdisabled in a newcontroller-only pursuit, logging charge/velocity to validate control behavior before judging naturalclear.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_frozen_files','screens','mapped_CHR_1K_chunks_exact','policy_rows','last_score')},indent=2))
if __name__=='__main__':main()
