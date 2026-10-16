"""All157 old water APU differences synchronized; preserve exact event proof and phase limits."""
from pathlib import Path
import hashlib,json,csv,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def st(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def main():
 out=R/'qa/reports/audio_sync061_validation.json';assert not out.exists();runs=[];frozen=0
 for name,base in (('audio_sync061_japan_water','audio_japan_water'),('audio_sync061_043_water','audio043_water')):
  q=R/'qa/dialogue'/name;b=R/'qa/dialogue'/base;e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==9030 and(q/'trace_complete.txt').read_text()=='9030'
  for p,h in e['files'].items():assert sha(q/p)==h;frozen+=1
  ra=[x for x in csv.DictReader((q/'audio_writes.csv').open())if int(x['frame'])<9000];rb=list(csv.DictReader((b/'audio_writes.csv').open()));assert ra==rb
  wa=[x for x in csv.DictReader((q/'world_phase.csv').open())if int(x['frame'])<=9000];wb=list(csv.DictReader((b/'world_phase.csv').open()));assert wa==wb
  for suffix in ('_ram.bin','_ppu.bin','_oam.bin'):
   for p in q.glob('frame_*'+suffix):
    if int(p.name[6:11])<=9000:assert p.read_bytes()==(b/p.name).read_bytes()
  peeks=list(csv.DictReader((q/'APU_peeks.csv').open()));assert len(peeks)==161 and[int(x['frame'])for x in peeks]==list(range(4200,9001,30))and all(x['cycle_before']==x['cycle_after']for x in peeks)
  for f in range(4200,9001,30):
   x=st(q/f'phase_{f:05d}_before_state.txt');y=st(q/f'phase_{f:05d}_after_state.txt');assert x.keys()==y.keys()and all(x[k]==y[k]for k in x if not k.startswith('apu.'))
   for suffix in ('_ram.bin','_ppu.bin','_oam.bin'):assert(q/f'phase_{f:05d}_before{suffix}').read_bytes()==(q/f'phase_{f:05d}_after{suffix}').read_bytes()
  runs.append({'QA':name,'frames':e['frames'],'screens':len(list(q.glob('frame_*.png'))),'audio_world_RAM_PPU_OAM_exact_ownbaseline_through9000':True,'nonAPU_state_and_all_memory_unchanged_at161peeks':True,'peek_CPUcycle_unchanged':True})
 a=R/'qa/dialogue/audio_sync061_japan_water';b=R/'qa/dialogue/audio_sync061_043_water';observations=[];fields=collections.Counter();classes=collections.Counter();outputs=('apu.dmc.outputLevel','apu.dmc.timer.lastOutput','apu.noise.timer.lastOutput','apu.square1.timer.lastOutput','apu.square2.timer.lastOutput','apu.triangle.timer.lastOutput');outputdiff=0
 for f in range(4200,9001,30):
  x=st(a/f'phase_{f:05d}_after_state.txt');y=st(b/f'phase_{f:05d}_after_state.txt');d={k:{'source':x[k],'043':y[k]}for k in x if k.startswith('apu.')and x[k]!=y[k]};fields.update(d.keys())
  category='all_APU_exact'if not d else'silent_DMC_remaining'if x['apu.dmc.silenceFlag']==y['apu.dmc.silenceFlag']=='true'and x['apu.dmc.bytesRemaining']==y['apu.dmc.bytesRemaining']=='0'else'active_DMC_remaining';classes[category]+=1
  od={k:{'source':x[k],'043':y[k]}for k in outputs if x[k]!=y[k]};outputdiff+=bool(od);observations.append({'frame':f,'APU_differences':d,'output_value_differences':od,'DMC_category':category})
 old=json.loads((R/'qa/reports/audio059_APU_state_observation.json').read_text());wanted={int(x['frame'][6:11])for ride in old['results']if ride['ride']=='water'for x in ride['APU_differing_states']};assert len(wanted)==157 and wanted<={x['frame']for x in observations}
 source=json.loads((R/'manifests/source_rom.json').read_text());original=R/source['path'];rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(original)==source['sha256'];ob=original.read_bytes();nb=rom.read_bytes();ranges=[]
 for start,end,newstart,label in ((0x18010,0x1c010,0x38010,'native3C/3D music engine'),(0x1c010,0x1e010,0x3c010,'native3E DMC sample/data bank')):
  v=ob[start:end];assert v==nb[newstart:newstart+len(v)];ranges.append({'source_file_start':hex(start),'043_file_start':hex(newstart),'bytes':len(v),'description':label,'sha256':hashlib.sha256(v).hexdigest()})
 report={'work':61,'status':'REGISTER_DATA_PRESERVATION_PASS_OUTPUT_PHASE_DIFFERENCES_RECORDED','scope':'All157 oldwater APU differences covered in161 explicit-catchup observations; actual outputphases can differ, no audioidentity claim','runtime_frozen_files':frozen,'runs':runs,'synchronized_observations':observations,'APU_difference_field_counts':dict(fields),'DMC_observation_categories':dict(classes),'observations_with_some_channel_output_difference':outputdiff,'all157_previous_raw_difference_frames_covered':True,'native_music_DMC_banks_24K_byteexact':ranges,'ROM_SSOT_changes':0,'limits':['11-observation60 result was scoped; laterphase/output differences now expressly retained','DMC categories describe sample activity, not whether allchanneloutputs areequal; triangle/noise maydiffer in silentDMCcategory','Exact native music code/data and note register values/order/frame do not establish PCM/waveform/audioquality equivalence','No audible defect confirmed nor audible identity confirmed; actual listening/PCM output notdone','No naturalfullclear/hardware/finalhumanapproval'],'next_action':'Trace actual DMC sample reads with fresh uniqueROMnames and native typedPCM-CDL evidence to confirm consumed bytes preserved, then retain waveform phase limit.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_frozen_files','DMC_observation_categories','observations_with_some_channel_output_difference')},indent=2))
if __name__=='__main__':main()
