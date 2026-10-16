"""Work95 same047 gate save/reset, serialized state and actual glyph lifetime."""
from pathlib import Path
import json,csv,hashlib
from PIL import Image,ImageChops
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text('utf-8'))
def state(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def main():
 output=R/'qa/reports/state095_validation.json';assert not output.exists();rom=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();source=j(R/'manifests/source_rom.json');assert sha(R/source['path'])==source['sha256']
 prior=j(R/'qa/reports/state085_validation.json')
 for folder in('work/state085_serializer','work/savestate_001'):
  for z in j(R/folder/'source_records.json'):assert '/2.1.1/'in z['url']and sha(R/z['path'])==z['sha256']
 apu=(R/'work/state085_serializer/NesApu.cpp').read_text();ser=apu.split('void NesApu::Serialize(Serializer& s)',1)[1].split('void NesApu::AddExpansionAudioDelta',1)[0];assert 's.GetFormat() != SerializeFormat::Map'in ser and 'EndFrame();'in ser
 assert 'OPLL_forceRefresh(opll)'in(R/'work/savestate_001/Emu2413Serializer.h').read_text()and'UPDATE_ALL = 255'in(R/'work/savestate_001/emu2413.cpp').read_text()
 q=R/'qa/dialogue/state095_gate047';a=state(q/'saved_machine_state.txt');b=state(q/'restored_machine_state.txt');pre=state(q/'precreate_machine_state.txt');assert a.keys()==b.keys()==pre.keys()and len(a)==826
 fields={f'mapper.audio.opll->slot[{i}].update_requests'for i in range(18)};diff={k:[a[k],b[k]]for k in a if a[k]!=b[k]};assert set(diff)=={f'mapper.audio.opll->slot[{i}].update_requests'for i in range(1,18,2)}and all(v==['0','255']for v in diff.values())
 assert all(a[k]==b[k]for k in a if k not in fields);prechanges={k:[pre[k],a[k]]for k in a if pre[k]!=a[k]};assert len(prechanges)==11 and all(k.startswith('apu.')for k in prechanges)
 for suffix,size in(('_ram.bin',2048),('_ppu.bin',16384),('_oam.bin',256)):
  p=q/('saved_machine'+suffix);assert p.stat().st_size==size and p.read_bytes()==(q/('restored_machine'+suffix)).read_bytes()
 assert(q/'restored_machine_ppu.bin').read_bytes()[:0x800]==blob[0x6bc10:0x6c410]
 events=list(csv.DictReader((q/'savestate_events.csv').open()));assert[x['kind']for x in events]==['created_in_exec','request_load_in_exec','returned_from_load_in_exec','complete']and[x['frame']for x in events]==['1920','2190','2190','3000']
 assert events[0]['cycle']==events[2]['cycle']=='57177337'and events[0]['CHR0_relative']=='2BC00'and events[0]['CHR400_relative']=='2C000';assert all(events[0][k]==events[2][k]for k in events[0]if k not in('frame','kind'))
 refs=[]
 for frame in(2220,2250,2280):
  for suffix in('.png','_ram.bin','_ppu.bin','_oam.bin','_mapping.csv'):
   p=q/f'frame_{frame:05}{suffix}';r=R/f'qa/dialogue/gate091_castle047/frame_{frame-270:05}{suffix}';assert p.read_bytes()==r.read_bytes();refs.append({'postload':p.relative_to(R).as_posix(),'reference047':r.relative_to(R).as_posix(),'sha256':sha(p)})
 reset=R/'qa/dialogue/reset095_gate047';rr=list(csv.DictReader((reset/'reset_events.csv').open()));assert[x['kind']for x in rr]==['request_console_reset','actual_reset_event','complete']and[x['frame']for x in rr]==['3000','3001','6000']
 assert rr[0]['headfont']==rr[-1]['headfont']=='AF'and rr[-1]['root']=='08'and rr[-1]['course']=='05'
 info=j(R/'build/dialogue_kr_poc_047/gate_editorial_mapping.json');rgb=[]
 for frame in(4920,6000):
  ram=(reset/f'frame_{frame:05}_ram.bin').read_bytes();ppu=(reset/f'frame_{frame:05}_ppu.bin').read_bytes();actual=Image.open(reset/f'frame_{frame:05}.png').convert('RGB');assert ram[0x34]==ram[0x6f3]==175
  for row,line in enumerate(info['layout']):
   codes=bytes.fromhex(line['expanded_hex']);assert ppu[0x22a8+row*0x40:0x22a8+row*0x40+len(codes)]==codes;expected=Image.new('RGB',(len(codes)*8,8),'black')
   for col,code in enumerate(codes):
    pixels=decode(blob[0x6bc10+code*16:0x6bc10+(code+1)*16]);assert set(pixels)<={0,2}
    for k,v in enumerate(pixels):
     if v:expected.putpixel((col*8+k%8,k//8),(255,254,255))
   assert ImageChops.difference(actual.crop((64,168+row*16,64+len(codes)*8,176+row*16)),expected).getbbox()is None
  rgb.append(frame)
 runtime={}
 for name in('state095_gate047','reset095_gate047'):
  folder=R/'qa/dialogue'/name;e=j(folder/'environment.json');assert e['rom_sha256']==sha(rom)and e['exit_code']==0 and e['exe_sha256']==j(R/'qa/dialogue/state085_train046_v2/environment.json')['exe_sha256']
  for path,h in e['files'].items():assert sha(folder/path)==h
  assert(folder/'trace_complete.txt').read_text()==str(e['frames']);images=sorted(folder.glob('frame_*.png'));chunks=0
  for p in images:
   ppu=(folder/(p.stem+'_ppu.bin')).read_bytes()
   for z in csv.DictReader((folder/(p.stem+'_mapping.csv')).open()):
    if z['kind']=='chr':
     aa=int(z['cpu_or_ppu_address'],16);bb=int(z['relative_offset'],16);assert ppu[aa:aa+0x400]==blob[0x40010+bb:0x40410+bb];chunks+=1
  runtime[name]={'frames':e['frames'],'frozen_files':len(e['files']),'screens':len(images),'mapped_CHR_1K_chunks_exact':chunks,'environment_sha256':sha(folder/'environment.json')}
 result={'work':95,'status':'PASS_SERIALIZED047_GATE_STATE_AND_RESET','ROM_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'all_state_keys':len(a),'restored_RAM_PPU_OAM_exact':True,'restored_gate175176_exact':True,'nine_source_proven_OPLL_refresh_fields':diff,'precreate_APU_changes_due_to_binary_serializer_EndFrame':prechanges,'postload_native_current047_reference_files_exact':refs,'reset_events':rr,'reset_reentry_native_NT_and_exact_RGB_frames':rgb,'runtime':runtime,'human_final_review':False,'visual_review':'Actual postload2220 and reset-reentry4920 viewed; legible modified sentence. No simulation or enlarged redraw replaces game image.','scope':'Same047 gate top font175 at1920 saved once, load2190, console reset3000 and native reentry. No crossbuild states/all save situations/PCM listening/hardware/wholeplay/final human approval.'}
 output.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k in('status','all_state_keys','restored_gate175176_exact','reset_reentry_native_NT_and_exact_RGB_frames','runtime')},indent=2))
if __name__=='__main__':main()