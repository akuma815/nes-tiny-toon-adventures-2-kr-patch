"""Same049 private226 serialized state and native reset reentry, bounded contract."""
from pathlib import Path
import csv,hashlib,json
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text('utf-8'))
def st(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 report=R/'qa/reports/state133_validation.json';assert not report.exists()
 rom=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();source=j(R/'manifests/source_rom.json');assert sha(R/source['path'])==source['sha256']
 for folder in ['work/state085_serializer','work/savestate_001']:
  for v in j(R/folder/'source_records.json'):assert '/2.1.1/' in v['url'] and sha(R/v['path'])==v['sha256']
 apu=(R/'work/state085_serializer/NesApu.cpp').read_text();body=apu.split('void NesApu::Serialize(Serializer& s)',1)[1].split('void NesApu::AddExpansionAudioDelta',1)[0];assert 's.GetFormat() != SerializeFormat::Map' in body and 'EndFrame();' in body
 assert 'OPLL_forceRefresh(opll)' in (R/'work/savestate_001/Emu2413Serializer.h').read_text() and 'UPDATE_ALL = 255' in (R/'work/savestate_001/emu2413.cpp').read_text()
 q=R/'qa/dialogue/state133_shortage049_v2';a=st(q/'saved_machine_state.txt');b=st(q/'restored_machine_state.txt');pre=st(q/'precreate_machine_state.txt');assert len(a)==826 and a.keys()==b.keys()==pre.keys()
 diff={k:[a[k],b[k]]for k in a if a[k]!=b[k]};expected={f'mapper.audio.opll->slot[{i}].update_requests' for i in range(1,18,2)}
 assert set(diff)==expected and all(v==['0','255'] for v in diff.values())
 prediff={k:[pre[k],a[k]] for k in a if pre[k]!=a[k]};assert len(prediff)==9 and all(k.startswith('apu.') for k in prediff)
 for suf,size in [('_ram.bin',2048),('_ppu.bin',16384),('_oam.bin',256)]:
  p=q/('saved_machine'+suf);assert p.stat().st_size==size and p.read_bytes()==(q/('restored_machine'+suf)).read_bytes()
 assert (q/'restored_machine_ppu.bin').read_bytes()[:0x800]==blob[0x78810:0x79010]
 events=rows(q/'savestate_events.csv');assert [e['kind'] for e in events]==['created_in_exec','request_load_in_exec','returned_from_load_in_exec','complete'] and [e['frame'] for e in events]==['2100','2400','2400','4200']
 assert events[0]['cycle']==events[2]['cycle']=='62536565' and events[0]['pc']=='FE53' and events[0]['lowerfont']=='E2' and events[0]['CHR0_relative']=='38800'
 assert all(events[0][k]==events[2][k] for k in events[0] if k not in ['frame','kind'])
 refs=[]
 for f in [2430,2460,2490,2520,2550]:
  for suf in ['.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv']:
   p=q/f'frame_{f:05d}{suf}';old=R/f'qa/dialogue/clear129_normal3049/frame_{f-300:05d}{suf}';assert p.read_bytes()==old.read_bytes();refs.append({'file':p.relative_to(R).as_posix(),'reference':old.relative_to(R).as_posix(),'sha256':sha(p)})
 e=rows(q/'menu_events.csv');inits=[z for z in e if z['kind']=='exec' and z['address']=='9445']
 for f,font,phase in [(2600,226,0),(2607,196,3)]:
  z=next(z for z in inits if int(z['frame'])==f);assert int(z['font'],16)==int(z['active_font'],16)==font and int(z['phase'],16)==phase
 mapping=j(R/'build/dialogue_kr_poc_049/shortage_editorial_mapping.json')
 ppu=(q/'frame_02430_ppu.bin').read_bytes()
 for addr,line in zip([0x22a8,0x22e8],mapping['layout']):assert ppu[addr:addr+line['expanded_tiles']]==bytes.fromhex(line['expanded_hex'])
 assert (q/'frame_02700_ram.bin').read_bytes()[0x6f3]==196 and (q/'frame_02700_ram.bin').read_bytes()[0x7d0:0x7d3]==bytes([3,0,0])
 # Native possession after next controller input, not a forced printed buffer.
 old=R/'qa/dialogue/clear129_normal3049/frame_02700_ppu.bin';assert (q/'frame_02700_ppu.bin').read_bytes()[0x22a8:0x22f8]==old.read_bytes()[0x22a8:0x22f8]
 reset=R/'qa/dialogue/reset133_shortage049';rr=rows(reset/'reset_events.csv');assert [e['kind']for e in rr]==['request_console_reset','actual_reset_event','complete'] and [e['frame']for e in rr]==['2160','2161','6300'] and rr[0]['lowerfont']=='E2'
 assert (reset/'frame_02190_ram.bin').read_bytes()[0x6f3]==0
 assert (reset/'frame_04140_ram.bin').read_bytes()[0x7d0:0x7d3]==bytes([0,1,0]) and (reset/'frame_04161_ram.bin').read_bytes()[0x7d0:0x7d3]==bytes([6,0,0])
 assert (reset/'frame_04260_ram.bin').read_bytes()[0x6f3]==196
 base=R/'qa/dialogue/clear129_normal4049/frame_02100_ppu.bin';assert (reset/'frame_04260_ppu.bin').read_bytes()[0x22a8:0x22f8]==base.read_bytes()[0x22a8:0x22f8]
 crop=(64,163,224,187);assert ImageChops.difference(Image.open(reset/'frame_04260.png').convert('RGB').crop(crop),Image.open(base.with_name('frame_02100.png')).convert('RGB').crop(crop)).getbbox() is None
 for f in [5400,6300]:
  ram=(reset/f'frame_{f:05d}_ram.bin').read_bytes();assert ram[0x18]==4 and ram[0x54]==5 and ram[0x25]==0 and ram[0x6f3]==0 and ram[0x7d0:0x7d3]==bytes([6,0,0])
 runtime={}
 for name in ['state133_shortage049','state133_shortage049_v2','reset133_shortage049']:
  folder=R/'qa/dialogue'/name;env=j(folder/'environment.json');assert env['rom_sha256']==sha(rom) and env['exit_code']==0
  for f,h in env['files'].items():assert sha(folder/f)==h
  assert (folder/'trace_complete.txt').read_text()==str(env['frames']);chunks=0
  for image in folder.glob('frame_*.png'):
   ppu=(folder/(image.stem+'_ppu.bin')).read_bytes()
   for v in rows(folder/(image.stem+'_mapping.csv')):
    if v['kind']=='chr':
     aa=int(v['cpu_or_ppu_address'],16);bb=int(v['relative_offset'],16);assert ppu[aa:aa+0x400]==blob[0x40010+bb:0x40410+bb];chunks+=1
  runtime[name]={'frames':env['frames'],'declared_files':len(env['files']),'mapped_CHR_chunks_exact':chunks,'environment_sha256':sha(folder/'environment.json'),'experiment':('FAILED_UNEXECUTED_STATE' if name=='state133_shortage049' else 'PASS_BOUNDED')}
 direct=['state133_shortage049_v2/frame_02430.png','state133_shortage049_v2/frame_02604.png','state133_shortage049_v2/frame_02700.png','reset133_shortage049/frame_02880.png','reset133_shortage049/frame_03900.png','reset133_shortage049/frame_04260.png','reset133_shortage049/frame_05400.png']
 result={'work':133,'status':'PASS_BOUNDED049_PRIVATE226_STATE_AND_RESET_REENTRY','ROM_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'state_keys':826,'restore_RAM_PPU_OAM_exact':True,'restored_font226227_CHR_exact':True,'source_proven_OPLL_refresh_fields':diff,'precreate_APU_serializer_EndFrame_changes':prediff,'postload_native_reference25_files_exact':refs,'next_paragraph_clear_font226_to196_native':True,'reset_events':rr,'native_after_reset_ticket_charge':'Initial seed3 existed before reset only; native new-game10→6 after4 charge, no postreset manual seed','reset_departure_NT_RGB_exact':True,'runtime':runtime,'direct_actual_visuals':{p:sha(R/'qa/dialogue'/p) for p in direct},'human_final_review':False,'scope':'Same049 completed-shortage wait at native idleFE53 saved2100/load2400; one console reset2160 and successful native admission/reentry. Initial seed recorded. No all states/reset contexts/crossbuild states/PCM/hardware/wholeplay/global gameplay identity.'}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','state_keys','restored_font226227_CHR_exact','runtime']},indent=2))
if __name__=='__main__':main()
