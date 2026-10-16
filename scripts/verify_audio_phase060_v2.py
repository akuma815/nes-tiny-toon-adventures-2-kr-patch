"""Explicit APU catchup comparison and actual NMI latency evidence for first water divergence."""
from pathlib import Path
import csv,json,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def st(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def main():
 out=R/'qa/reports/audio_phase060_validation_v2.json';assert not out.exists();runs=[];frozen=0
 for name,baseline in (('audio_phase_japan_water','audio_japan_water'),('audio_phase043_water','audio043_water')):
  q=R/'qa/dialogue'/name;b=R/'qa/dialogue'/baseline;e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==4800
  for p,h in e['files'].items():assert sha(q/p)==h;frozen+=1
  a=list(csv.DictReader((q/'audio_writes.csv').open()));old=[x for x in csv.DictReader((b/'audio_writes.csv').open())if int(x['frame'])<4800];assert a==old
  world=list(csv.DictReader((q/'world_phase.csv').open()));old=list(csv.DictReader((b/'world_phase.csv').open()));assert world==old[:160]
  png_diff=[p.name for p in q.glob('frame_*.png')if p.read_bytes()!=(b/p.name).read_bytes()];assert all(int(n[6:11])<4200 for n in png_diff)
  for suffix in ('_ram.bin','_ppu.bin','_oam.bin'):
   for p in q.glob('frame_*'+suffix):assert p.read_bytes()==(b/p.name).read_bytes()
  rows=list(csv.DictReader((q/'APU_peeks.csv').open()));assert len(rows)==11 and all(x['cycle_before']==x['cycle_after']for x in rows)
  for f in range(4200,4501,30):
   a=st(q/f'phase_{f:05d}_before_state.txt');b=st(q/f'phase_{f:05d}_after_state.txt');assert a.keys()==b.keys()and all(a[k]==b[k]for k in a if not k.startswith('apu.'))
   for suffix in ('_ram.bin','_ppu.bin','_oam.bin'):assert(q/f'phase_{f:05d}_before{suffix}').read_bytes()==(q/f'phase_{f:05d}_after{suffix}').read_bytes()
  runs.append({'QA':name,'frames':e['frames'],'screens':len(list(q.glob('frame_*.png'))),'own_baseline_audio_all_fields_exact':True,'own_baseline_world_all_fields_exact':True,'own_baseline_PNGs_byteexact':not png_diff,'prepeek_PNG_differences':png_diff,'own_baseline_all_RAM_PPU_OAM_byteexact':True,'each_peek_CPU_nonAPU_state_RAM_PPU_OAM_unchanged':True,'intervention':e['intervention']})
 a=R/'qa/dialogue/audio_phase_japan_water';b=R/'qa/dialogue/audio_phase043_water';sync=[];raw=[]
 for f in range(4200,4501,30):
  for suffix,target in (('before',raw),('after',sync)):
   x=st(a/f'phase_{f:05d}_{suffix}_state.txt');y=st(b/f'phase_{f:05d}_{suffix}_state.txt');d={k:{'source':x[k],'043':y[k]}for k in x if k.startswith('apu.')and x[k]!=y[k]}
   if suffix=='after':
    assert set(d)<={'apu.dmc.timer.timer','apu.dmc.bitsRemaining'}
    if d:assert x['apu.dmc.silenceFlag']==y['apu.dmc.silenceFlag']=='true'and x['apu.dmc.bytesRemaining']==y['apu.dmc.bytesRemaining']=='0'
    for k in ('apu.dmc.outputLevel','apu.dmc.timer.lastOutput','apu.noise.timer.lastOutput','apu.square1.timer.lastOutput','apu.square2.timer.lastOutput','apu.triangle.timer.lastOutput'):assert x[k]==y[k]
   target.append({'frame':f,'APU_differences':d,'source_DMC_silence':x['apu.dmc.silenceFlag'],'source_DMC_bytesRemaining':x['apu.dmc.bytesRemaining']})
 na=list(csv.DictReader((a/'NMI_timing.csv').open()));nb=list(csv.DictReader((b/'NMI_timing.csv').open()));assert len(na)==len(nb)==601;delta=collections.Counter()
 for x,y in zip(na,nb):
  assert all(x[k]==y[k]for k in ('frame','pc','root','phase','course'));assert x['pc']=='FE83';delta[int(y['cycle'])-int(x['cycle'])]+=1
  assert 0xfe53<=int(x['interrupted_pc'],16)<=0xfe5c and 0xfe53<=int(y['interrupted_pc'],16)<=0xfe5c
 src=json.loads((R/'manifests/source_rom.json').read_text());original=R/src['path'];rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(original)==src['sha256'];assert original.read_bytes()[0x1fe62:0x1fe6f]==rom.read_bytes()[0x3fe62:0x3fe6f]
 source=json.loads((R/'work/audio_phase_001/source.json').read_text());
 for x in source:assert sha(R/x['path'])==x['sha256']
 report={'work':60,'status':'FIRST_DIVERGENCE_MODEL_RESOLVED_SCOPED','scope':'Explicit catchup eleven water-return observations: output states exact; only inactive silentDMC timer/bits differ. No blanket audioidentity or all157sample claim','ROM_SSOT_changes':0,'source_and_ROM_unchanged':True,'runtime_frozen_files':frozen,'runs':runs,'raw_APU_comparison':raw,'caught_up_APU_comparison':sync,'all_recorded_channel_output_values_exact':True,'residual_DMC_phase_scope':'Only DMC timer/bits at zero bytesRemaining and silenceFlagtrue. Not interpreted as audible defect, and no blanket futurePCMidentity','NMI_entries':len(na),'NMI_cycle_delta_counts':dict(sorted(delta.items())),'native_IDLE_RNG_loop_bytes_preserved':True,'first_differing_NMI':[{'source':x,'043':y}for x,y in zip(na,nb)if x['cycle']!=y['cycle']][:4],'source':source,'explanation':'Map-format serialization skips APU EndFrame/catchup; nonbus debugPeek4015 callsRun. Snapshot APUs can represent different elapsed internal update positions. Actual NMI reaches unchanged idleloop at different instruction boundaries. Detailed causality of alllaterCPU offsets not asserted.','limits':['No ROM timing repair justified from these rawcached observations alone','Eleven synchronized observations only; all157 oldraw differences not individuallysynchronized','No PCM/listening/nativefullclear/hardware/finalhumanreview','API debugpeeks explicitly recorded; unchanged ownbaselineaudio/world/RAM/PPU/OAM proven only this4.8k pair; fivePNG differences prepeek retained, render-frame relation not independentlyclassified'],'next_action':'Extend synchronized observations toall157 previous differing water snapshots, keeping original observer history and confirming unchanged audio events.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_frozen_files','NMI_entries','NMI_cycle_delta_counts')},indent=2))
if __name__=='__main__':main()
