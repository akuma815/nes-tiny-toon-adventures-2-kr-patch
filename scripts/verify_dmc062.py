"""Actual DMC-cursor matched ROM reads and fresh native typed PCM-CDL preservation."""
from pathlib import Path
import json,csv,hashlib,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/dmc062_validation.json';assert not out.exists();src=json.loads((R/'manifests/source_rom.json').read_text());old=R/src['path'];new=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(old)==src['sha256'];runs=[];rows=[];frozen=0;pcm=[]
 for name,baseline,rom in (('dmc062_japan_coaster_v2','audio_japan_coaster',old),('dmc062_043_coaster_v2','audio043_coaster',new)):
  q=R/'qa/dialogue'/name;e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==4200 and(q/'trace_complete.txt').read_text()=='4200';assert e['rom_sha256']==sha(rom)==e['actual_QA_ROM_sha256']==sha(Path(e['actual_QA_ROM']));assert Path(e['actual_QA_ROM']).parent==q and 'TTA2_DMC062_'in Path(e['actual_QA_ROM']).name and e['command'][3]==e['actual_QA_ROM']
  for p,h in e['files'].items():assert sha(q/p)==h;frozen+=1
  initial=(q/'initial_PRG_cdl.bin').read_bytes();final=(q/'final_PRG_cdl.bin').read_bytes();blob=rom.read_bytes();assert len(initial)==len(final)==blob[4]*16384 and not any(x&128 for x in initial)
  marks={i for i,x in enumerate(final)if x&128};assert len(marks)==1729;pcm.append(marks)
  rs=list(csv.DictReader((q/'DMC_reads.csv').open()));assert len(rs)==59247
  for x in rs:
   a=int(x['address'],16);off=int(x['PRG_relative'],16);assert a==int(x['current_address'],16)and int(x['bytes_remaining'])>0 and 0xc000<=a<=0xc880 and off in marks;assert int(x['value'],16)==blob[16+off]
   assert int(x['sample_address'],16)<=a<=int(x['sample_address'],16)+int(x['sample_length'])-1
  rows.append(rs);b=R/'qa/dialogue'/baseline;actual=list(csv.DictReader((q/'audio_writes.csv').open()));prior=[x for x in csv.DictReader((b/'audio_writes.csv').open())if int(x['frame'])<4200];assert actual==prior
  actual=list(csv.DictReader((q/'world_phase.csv').open()));prior=[x for x in csv.DictReader((b/'world_phase.csv').open())if int(x['frame'])<=4200];assert actual==prior
  runs.append({'QA':name,'frames':4200,'screens':len(list(q.glob('frame_*.png'))),'candidate_cursor_reads':len(rs),'initial_PCM_marks':0,'final_typed_PCM_bytes':len(marks),'actual_QA_ROM_sha256':e['actual_QA_ROM_sha256'],'exact_ownbaseline_audio_all_fields':True,'exact_ownbaseline_world_all_fields':True})
 a,b=rows;fields=('frame','address','value','current_address','bytes_remaining','sample_address','sample_length','silence');assert all(all(x[k]==y[k]for k in fields)for x,y in zip(a,b));assert {x+0x20000 for x in pcm[0]}==pcm[1];assert pcm[0]==set(range(0x1c1c0,0x1c881))
 delta=collections.Counter(int(y['cycle'])-int(x['cycle'])for x,y in zip(a,b));pc=sum(x['pc']!=y['pc']for x,y in zip(a,b));v=old.read_bytes()[0x1c1d0:0x1c891];assert v==new.read_bytes()[0x3c1d0:0x3c891]
 source=json.loads((R/'work/dmc_001/source_v4.json').read_text());
 for x in source:assert sha(R/x['path'])==x['sha256']
 h=(R/'work/dmc_001/NesDebugger.h').read_text();d=(R/'work/audio_001/NesDebugger.cpp').read_text();assert 'PcmData = 0x80'in h and 'isDmcDma && addressInfo.Type == MemoryType::NesPrgRom'in d and 'SetData<NesCdlFlags::PcmData>'in d
 report={'work':62,'status':'PASS_CONSUMED_ROM_BYTES','scope':'Two fresh4200 coaster traces; DMC-cursor/remaining-byte-matched actualreads tied to initiallyempty native typedPCM-CDL; no percallback operationtype is exposed','source_sha256':sha(old),'ROM_sha256':sha(new),'ROM_SSOT_changes':0,'runtime_frozen_files':frozen,'runs':runs,'read_value_order_frame_cursor_sample_remaining_exact_pairs':len(a),'fresh_PCM_marked_contiguous_bytes':1729,'PCM_bytes_sha256':hashlib.sha256(v).hexdigest(),'read_cycle_delta043_minus_source_counts':dict(sorted(delta.items())),'read_PC_differences_expected_localized_execution':pc,'native_typed_CDL_source':source,'operationtype_limit':'Lua read callback doesnot expose DMA type. Each matchedread uses currentDMCcursor+positive remaining bytes and sameaddress is marked by fresh nativeDMC-DMA logger; avoids claim each callback inherentlytyped','failed_v1_observer_run':'qa/dialogue/dmc062_japan_coaster/environment.json and qa/reports/dmc062_observer_timeout.json preserved; not completedruntimeevidence','limits':['One native coaster path; not allfutureDMCfetches','Source/new read timing243 records differ by2cycles; PC1237 records differ; no CPUexecutionidentity','Outputphase differences61 remain; no PCM/audioquality/listening/hardware/fullnaturalclear/finalhumanreview'],'next_action':'Map actualcart player/steering consumers and use only controller input to exercise a naturalclear branch, keeping earlier diagnosticseeds separate.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_frozen_files','read_value_order_frame_cursor_sample_remaining_exact_pairs','fresh_PCM_marked_contiguous_bytes','read_cycle_delta043_minus_source_counts')},indent=2))
if __name__=='__main__':main()
