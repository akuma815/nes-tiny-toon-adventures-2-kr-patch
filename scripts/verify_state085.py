"""Work85 same046 state roundtrip/reset; exact serialized state baseline."""
from pathlib import Path
import hashlib,json,csv
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def main():
 report=R/'qa/reports/state085_validation.json';assert not report.exists();rom=R/'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes()
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 for folder in ('work/state085_serializer','work/savestate_001'):
  for x in json.loads((R/folder/'source_records.json').read_text('utf-8')):assert '/2.1.1/'in x['url'] and sha(R/x['path'])==x['sha256']
 apu=(R/'work/state085_serializer/NesApu.cpp').read_text();s=apu.split('void NesApu::Serialize(Serializer& s)',1)[1].split('void NesApu::AddExpansionAudioDelta',1)[0];assert 's.GetFormat() != SerializeFormat::Map'in s and 'EndFrame();'in s
 ser=(R/'work/savestate_001/Emu2413Serializer.h').read_text();opll=(R/'work/savestate_001/emu2413.cpp').read_text();assert 'OPLL_forceRefresh(opll)'in ser and 'request_update(&opll->slot[i], UPDATE_ALL)'in opll and 'UPDATE_ALL = 255'in opll
 q=R/'qa/dialogue/state085_train046_v2';a=state(q/'saved_machine_state.txt');b=state(q/'restored_machine_state.txt');pre=state(q/'precreate_machine_state.txt');assert a.keys()==b.keys()==pre.keys()
 fields={f'mapper.audio.opll->slot[{i}].update_requests'for i in range(18)};diff={k:[a[k],b[k]]for k in a if a[k]!=b[k]};assert set(diff)=={f'mapper.audio.opll->slot[{i}].update_requests'for i in range(1,18,2)}
 assert all(b[k]=='255' and a[k]in ('0','255')for k in fields);assert all(a[k]==b[k]for k in a if k not in fields)
 prechanges={k:[pre[k],a[k]]for k in a if pre[k]!=a[k]};v1=R/'qa/dialogue/state085_train046';v1a=state(v1/'saved_machine_state.txt');v1b=state(v1/'restored_machine_state.txt');assert prechanges=={k:[v1a[k],v1b[k]]for k in v1a if v1a[k]!=v1b[k] and k.startswith('apu.')}
 for suffix,size in [('_ram.bin',2048),('_ppu.bin',16384),('_oam.bin',256)]:assert (q/('saved_machine'+suffix)).stat().st_size==size and (q/('saved_machine'+suffix)).read_bytes()==(q/('restored_machine'+suffix)).read_bytes()
 assert (q/'restored_machine_ppu.bin').read_bytes()[:2048]==blob[0x78010:0x78810]
 events=list(csv.DictReader((q/'savestate_events.csv').open()));assert [x['kind']for x in events]==['created_in_exec','request_load_in_exec','returned_from_load_in_exec','complete'];assert [x['frame']for x in events]==['3330','3600','3600','4200'];assert events[0]['cycle']==events[2]['cycle']=='99167971'
 assert all(events[0][k]==events[2][k]for k in events[0]if k not in ('frame','kind'))
 refs=[]
 for f in (3630,3660,3690):
  for suffix in ('.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):
   p=q/f'frame_{f:05d}{suffix}';r=R/f'qa/dialogue/stop080_train046_v2/frame_{f-270:05d}{suffix}';assert p.read_bytes()==r.read_bytes();refs.append({'loaded':p.relative_to(R).as_posix(),'reference':r.relative_to(R).as_posix(),'sha256':sha(p)})
 reset=R/'qa/dialogue/reset085_train046';rr=list(csv.DictReader((reset/'reset_events.csv').open()));assert [x['kind']for x in rr]==['request_console_reset','actual_reset_event','complete'];assert [x['frame']for x in rr]==['3600','3601','7200']
 wr=list(csv.DictReader((reset/'world_phase.csv').open()));assert any(x['frame']=='6300'and x['headfont']=='DE'for x in wr);assert wr[-1]['root']=='04' and wr[-1]['phase']=='05'and wr[-1]['ride']=='02'and wr[-1]['headfont']=='E0'
 # 0xDE =222 START, 0xE0=224 STOP. No crossed-build state compatibility claim.
 runtime={}
 for name in ('state085_train046','state085_train046_v2','reset085_train046'):
  x=R/'qa/dialogue'/name;env=json.loads((x/'environment.json').read_text('utf-8'));assert env['rom_sha256']==sha(rom) and env['exit_code']==0
  for n,h in env['files'].items():assert sha(x/n)==h,n
  chunks=0;images=list(x.glob('frame_*.png'))
  for p in images:
   ppu=(x/(p.stem+'_ppu.bin')).read_bytes()
   for m in csv.DictReader((x/(p.stem+'_mapping.csv')).open()):
    if m['kind']=='chr':
     aa=int(m['cpu_or_ppu_address'],16);bb=int(m['relative_offset'],16);assert ppu[aa:aa+1024]==blob[0x40010+bb:0x40410+bb];chunks+=1
  runtime[name]={'frozen_files':len(env['files']),'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'environment_sha256':sha(x/'environment.json')}
 result={'work':85,'status':'PASS_SERIALIZED046_STATE_AND_RESET','ROM_sha256':sha(rom),'all_state_keys':len(a),'restored_RAM_PPU_OAM_exact':True,'restored_STOP224_225_exact':True,'nine_source_proven_OPLL_refresh_fields':diff,'precreate_APU_changes_explained_by_binary_serializer_EndFrame':prechanges,'postload_native_reference_files_exact':refs,'reset_events':rr,'reset_reentry_START222_STOP224':True,'runtime':runtime,'scope':'Same046 train top state saved3330 loaded3600; one console reset and native train reentry. No crossbuild state compatibility/all-save-situations/PCM identity/hardware/fullplay/humanapproval claim.'}
 report.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k in ('status','all_state_keys','restored_STOP224_225_exact','reset_reentry_START222_STOP224','runtime')}))
if __name__=='__main__':main()