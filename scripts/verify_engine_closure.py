"""Work52 bounded runtime consumer closure; no global absence/full-play claim."""
from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/engine_closure052.json';assert not out.exists()
 rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';data=rom.read_bytes();build=json.loads((rom.parent/'build_report.json').read_text('utf-8'));assert sha(rom)==build['output_sha256']
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256'];s=(R/source['path']).read_bytes()
 # Unconnected candidates deliberately stay byte-identical in source banks116..121.
 assert data[0x5d010:0x5e810]==s[0x3d010:0x3e810]
 runs=[];native_seen={};runtimefiles=0;screens=0;chrchunks=0
 for name,frames,seed in [('closure043_attract',18000,False),('closure043_root9',12000,True)]:
  q=R/'qa/dialogue'/name;e=json.loads((q/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['frames']==frames and e['rom_sha256']==sha(rom) and (q/'trace_complete.txt').read_text()==str(frames)
  for n,h in e['files'].items():assert sha(q/n)==h;runtimefiles+=1
  writes=list(csv.DictReader((q/'root9_seed.csv').open()));assert len(writes)==(3 if seed else 0)
  if seed:
   assert [(int(x['frame']),int(x['address'],16),int(x['before'],16),int(x['after'],16))for x in writes]==[(1000,0x6de,2,0),(1000,0x19,1,0),(1000,0x18,8,9)]
  else:assert e['input']['sequence']==[] and e['root9_intervention'] is None
  candidate=list(csv.DictReader((q/'candidate_font_writes.csv').open()));assert not [x for x in candidate if 116<=int(x['value'],16)<=121]
  states=list(csv.DictReader((q/'world_phase.csv').open()));assert len(states)==frames//30
  if seed:assert any(x['root']=='09'and x['headfont']=='38'for x in states)and any(x['root']=='09'and x['headfont']=='C9'for x in states)
  for png in sorted(q.glob('frame_*.png')):
   tag=png.stem;ppu=(q/(tag+'_ppu.bin')).read_bytes();maps=list(csv.DictReader((q/(tag+'_mapping.csv')).open()))
   for row in maps:
    if row['kind']!='chr':continue
    addr=int(row['cpu_or_ppu_address'],16);relative=int(row['relative_offset'],16);assert ppu[addr:addr+1024]==data[0x40010+relative:0x40410+relative],(name,tag,row);chrchunks+=1
   screens+=1
  for row in csv.DictReader((q/'menu_events.csv').open()):
   if row['kind']=='exec'and row['address']=='9417':native_seen.setdefault(int(row['id'],16),{'QA':name,'frame':int(row['frame']),'pointer':row['pointer']})
  runs.append({'QA':name,'frames':frames,'intervention':e['intervention'],'screens':len(list(q.glob('frame_*.png'))),'root_subphase_counts':dict(collections.Counter(x['root']+':'+x['subphase']for x in states)),'unconnected116_121_font_writes':0,'root9_font_write_rows':len(candidate)})
 current_logs=[]
 for env in sorted((R/'qa/dialogue').glob('train043_*/environment.json')):
  q=env.parent;e=json.loads(env.read_text('utf-8'));assert e['exit_code']==0 and e['rom_sha256']==sha(rom)
  log=q/'menu_events.csv'
  if not log.exists():continue
  assert sha(log)==e['files']['menu_events.csv'];current_logs.append({'path':log.relative_to(R).as_posix(),'sha256':sha(log)})
  for row in csv.DictReader(log.open()):
   if row['kind']=='exec'and row['address']=='9417':native_seen.setdefault(int(row['id'],16),{'QA':q.name,'frame':int(row['frame']),'pointer':row['pointer']})
 prior=json.loads((R/'qa/reports/registered_source_readiness_20261005.json').read_text('utf-8'));seen=set(prior['native_init_observed_slots'])|set(native_seen)
 rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')));mainrows=[x for x in rows if x['kind']=='main'];assert len(mainrows)==46
 coverage=[]
 for x in mainrows:
  slots=[int(z,16)for z in x['reference_ids'].split(',')];observed=sorted(set(slots)&seen);assert observed,x['entry_id']
  coverage.append({'entry_id':x['entry_id'],'slots':slots,'native_observed_slots':observed,'status':x['status']})
 result={'work':52,'status':'PASS','ROM_sha256':sha(rom),'ROM_SSOT_changes':0,'runs':runs,'screens':screens,'mapped_CHR_1K_chunks_exact':chrchunks,'runtime_frozen_files':runtimefiles,'new_observed_init_slots':sorted(native_seen),'combined_registered_unique_main_units_with_native_call_evidence':46,'unobserved_alias_slots':[i for i in range(48)if i not in seen],'registered_coverage':coverage,'current43_selected_logs':current_logs,'coverage_evidence_prior':{'path':'qa/reports/registered_source_readiness_20261005.json','sha256':sha(R/'qa/reports/registered_source_readiness_20261005.json')},'limits':['Bounded two runs plus historical registered call evidence; no global corpus or unused-asset proof','Root9 initialized using three declared guarded RAM writes; not natural game completion','46 unique main units coverage uses earlier verified logs where specified; not all43 scene pixels reviewed','PAUSE/HOW TO CONTROL banks116..121 not selected in these two paths; source preserved','Full natural play/audio/reset/save-state/hardware/final human linguistic review pending'],'next_action':'Validate native castle normal50 payment path/alias2C using declared initial currency seed; preserve all prior artifacts.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ('status','screens','mapped_CHR_1K_chunks_exact','runtime_frozen_files','combined_registered_unique_main_units_with_native_call_evidence','unobserved_alias_slots')},indent=2))
if __name__=='__main__':main()
