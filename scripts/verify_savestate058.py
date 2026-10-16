"""Same043 state restore: exact memory/state except source-proven OPLL refresh flags."""
from pathlib import Path
import json,csv,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def main():
 out=R/'qa/reports/savestate058_validation.json';assert not out.exists()
 q=R/'qa/dialogue/state043_coaster_roundtrip';e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['frames']==9000 and(q/'trace_complete.txt').read_text()=='9000'
 rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)==e['rom_sha256'];frozen=0
 for n,h in e['files'].items():assert sha(q/n)==h,n;frozen+=1
 records=json.loads((R/'work/savestate_001/source_records.json').read_text())
 for x in records:assert sha(R/x['path'])==x['sha256'] and '/2.1.1/'in x['url']
 ser=(R/'work/savestate_001/Emu2413Serializer.h').read_text();emu=(R/'work/savestate_001/emu2413.cpp').read_text()
 assert 'if(!s.IsSaving()) {\n\t\t\tOPLL_forceRefresh(opll);'in ser
 refresh=emu.split('void OPLL_forceRefresh(OPLL *opll) {',1)[1].split('void OPLL_setRate',1)[0]
 assert 'i < 18'in refresh and 'request_update(&opll->slot[i], UPDATE_ALL)'in refresh and 'UPDATE_ALL = 255'in emu
 a=state(q/'saved_machine_state.txt');b=state(q/'restored_machine_state.txt');assert a.keys()==b.keys()
 fields={f'mapper.audio.opll->slot[{i}].update_requests'for i in range(18)}
 for k in fields:assert b[k]=='255' and a[k]in ('0','255')
 diff={k:{'saved':a[k],'restored':b[k]}for k in a if a[k]!=b[k]}
 assert set(diff)=={f'mapper.audio.opll->slot[{i}].update_requests'for i in range(1,18,2)}
 assert all(a[k]==b[k]for k in a if k not in fields)
 exact={}
 for suffix,size in (('_ram.bin',2048),('_ppu.bin',16384),('_oam.bin',256)):
  x=q/('saved_machine'+suffix);y=q/('restored_machine'+suffix);assert x.stat().st_size==size and x.read_bytes()==y.read_bytes();exact[suffix]={'size':size,'sha256':sha(x)}
 events=list(csv.DictReader((q/'savestate_events.csv').open()));assert [r['kind']for r in events]==['created_in_exec','request_load_in_exec','returned_from_load_in_exec','complete']
 assert [r['frame']for r in events]==['3000','3600','3600','9000']
 assert events[0]['cycle']==events[2]['cycle']=='89363093' and events[1]['cycle']=='107231389'
 assert all(events[0][k]==events[2][k]for k in events[0]if k not in ('frame','kind'))
 blob=rom.read_bytes();chunks=0;images=sorted(q.glob('frame_*.png'))
 for p in images:
  ppu=(q/(p.stem+'_ppu.bin')).read_bytes()
  for m in csv.DictReader((q/(p.stem+'_mapping.csv')).open()):
   if m['kind']!='chr':continue
   a0=int(m['cpu_or_ppu_address'],16);b0=int(m['relative_offset'],16);assert ppu[a0:a0+1024]==blob[0x40010+b0:0x40410+b0];chunks+=1
 refs=[]
 for f in (3630,3660,3690):
  for suffix in ('.png','_ram.bin','_ppu.bin','_oam.bin'):
   x=q/f'frame_{f:05d}{suffix}';y=R/f'qa/dialogue/reset043_coaster/frame_{f-600:05d}{suffix}';assert x.read_bytes()==y.read_bytes();refs.append({'restored':str(x.relative_to(R)),'native_reference':str(y.relative_to(R)),'sha256':sha(x)})
 report={'work':58,'status':'PASS','scope':'Same043 native-exec savestate roundtrip, exact memory/all826 state fields except nine exact source-proven OPLL refresh flags; three postload native frames byteexact','ROM_sha256':sha(rom),'runtime_frozen_files':frozen,'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'all_state_keys':len(a),'state_difference_count':len(diff),'exact_refresh_differences':diff,'source_proof':records,'exact_memory':exact,'events':events,'postload_reference':refs,'API_stateLoaded_event_observed':False,'API_event_scope':'Official docs state manual loading; API load returned in exec, verified by cycle rewind and full machine state, no reliance on event','audio_PCM_or_audible_identity_verified':False,'ROM_SSOT_changes':0,'limits':['One same-build native coasternativeHUD saved/loaded; no crossbuild compatibility or allsave situations','No audio PCM/listening proof; derived cache flag reinitialization follows fixed2.1.1 serializer source','No natural fullclear, hardware or finalhumanreview claim'],'next_action':'Compare original Japan and043 audio register writes under identical controller schedule, preserving timing differences explicitly.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','all_state_keys','state_difference_count','runtime_frozen_files','screens','mapped_CHR_1K_chunks_exact')},indent=2))
if __name__=='__main__':main()
