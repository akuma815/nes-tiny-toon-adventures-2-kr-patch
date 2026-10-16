"""Read-only verification of completed work106 captures; never launches an emulator."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/context106_closeout.json';assert not out.exists()
 expected={
 'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d',
 'build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes':'a58a28bcb1449ad44b02cccbf6503af0e2792cbf96c9b9409bcc05025552a0f8',
 'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes':'82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10',
 'workspace/translation/text_ja.csv':'ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556'}
 for p,h in expected.items():assert sha(R/p)==h,p
 dirs=[R/'qa/dialogue/context106_normal3046',R/'qa/dialogue/context106_normal3047']
 envs=[json.loads((d/'environment.json').read_text('utf-8')) for d in dirs]
 for d,e,rom in zip(dirs,envs,list(expected)[1:3]):
  assert e['exit_code']==0 and e['frames']==4200
  assert e['rom_sha256']==expected[rom] and e['source_sha256']==expected[list(expected)[0]]
  assert sha(Path(e['exe_path']))==e['exe_sha256']
  assert sha(d/'capture_survey_used.lua')==e['lua_sha256']
  assert sha(d/'config_used.json')==e['config_sha256']
  assert sha(d/'inputs_used.json')==e['input']['file_sha256']
  assert sha(d/'seed_used.json')==e['seed_file_sha256']
  assert e['seed']['frame']==1000
  assert [(v['address'],v['value']) for v in e['seed']['writes']]==[(0x7D0,3),(0x7D1,0),(0x7D2,0)]
  for p,h in e['files'].items():assert sha(d/p)==h,p
 assert set(envs[0]['files'])==set(envs[1]['files'])
 differences=[p for p,h in envs[0]['files'].items() if envs[1]['files'][p]!=h]
 assert differences==['stdout.txt'],differences
 logs=[(d/'stdout.txt').read_text('utf-8').splitlines() for d in dirs]
 logdiff=[{'baseline':a,'current':b} for a,b in zip(*logs) if a!=b]
 assert len(logs[0])==len(logs[1]) and len(logdiff)==3
 assert all('CRC32:' in v['baseline'] and 'CRC32:' in v['current'] for v in logdiff)
 pngs=[p for p in envs[0]['files'] if p.endswith('.png')];assert len(pngs)==302
 fontpath=R/'build/dialogue_kr_poc_036/ui_stage_lower_shared_font.json'
 font=json.loads(fontpath.read_text('utf-8'));assert font['font_bank']==196
 rom=(R/list(expected)[2]).read_bytes();native=rom[0x40010+196*0x400:0x40010+198*0x400]
 assert native==bytes.fromhex(font['font_hex'])
 glyphs={v['code']:v['char'] for v in font['glyphs']};glyphs[0]=' '
 glyphs.update({0x70+i:str(i) for i in range(10)})
 rows=[]
 stages={1800:('MAIN_05833','1D',('   요금은 티켓  4장  ','티켓을 내줘! ')),2100:('MAIN_0590C','29',('아쉽지만      ','티켓을 더 모아줘! ')),2700:('MAIN_05929','2B',('지금  3장의 ','티켓을 갖고 있어  '))}
 for frame,(entry,slot,strings) in stages.items():
  d=dirs[1];ppu=(d/f'frame_{frame:05}_ppu.bin').read_bytes();ram=(d/f'frame_{frame:05}_ram.bin').read_bytes()
  assert ppu[:0x800]==native and ram[0xC6]==196
  assert ram[0x7D0:0x7D3]==bytes([3,0,0])
  decoded=[]
  for addr,want in zip((0x22A8,0x22E8),strings):
   data=ppu[addr:addr+len(want)];actual=''.join(glyphs[v] for v in data)
   assert actual==want,(frame,addr,actual,want)
   decoded.append({'ppu_address_hex':f'{addr:04X}','bytes_hex':data.hex(),'text':actual})
  rows.append({'frame':frame,'source_entry':entry,'native_slot_hex':slot,'post_read_next_slot_hex':f'{ram[0x6CF]:02X}','ticket_bytes_hex':ram[0x7D0:0x7D3].hex(),'font_bank':196,'font_ppu_2KiB_matches_current_ROM':True,'rows':decoded,'image_sha256':sha(d/f'frame_{frame:05}.png')})
 end=(dirs[1]/'frame_04200_ram.bin').read_bytes();assert end[0x7D0:0x7D3]==bytes([3,0,0])
 report={'work':106,'status':'PASS_BOUNDED_SEEDED_RUNTIME_CLOSEOUT','stop_requested':True,'automatic_resume':False,'protected_hashes':expected,'environments':{str(d.relative_to(R)).replace(chr(92),'/'):sha(d/'environment.json') for d in dirs},'frames_each':4200,'declared_files_each':len(envs[0]['files']),'equal_declared_files':len(envs[0]['files'])-len(differences),'whole_PNG_exact':len(pngs),'differences':differences,'stdout_difference_explanation':'Exactly three CRC32 lines differ because ROM046 and ROM047 differ; every other log line is equal.','stdout_differences':logdiff,'seed':envs[1]['seed'],'seed_file_sha256':envs[1]['seed_file_sha256'],'input_file_sha256':envs[1]['input']['file_sha256'],'emulator_sha256':envs[1]['exe_sha256'],'lua_sha256':envs[1]['lua_sha256'],'config_sha256':envs[1]['config_sha256'],'font_mapping_sha256':sha(fontpath),'actual_NT_rows':rows,'direct_visual_review_frames':[1800,2100,2700],'direct_visual_review':'Assistant inspected the three actual current047 PNGs: readable fee4, denial, possession3; human approval remains pending.','end_frame':4200,'end_observation':'Possession message remains displayed; ticket count3 preserved; no successful entry or return home claimed.','slot_caution':'RAM06CF advances after consuming a page. Post-read2A at frame2100 does not prove slot2A departure text was displayed; actual body is denial29.','validation_classes':{'static':'Hashes verified for declared captures, protected source/ROM/CSV, tool/config/Lua/input/seed; NT bytes decoded with existing glyph map; PPU font1962KiB equals currentROM.','build_apply':'No new ROM build or patch application. Earlier verified047 artifacts retained.','runtime':'Two already-started seeded4200frame Mesen runs finished with exit0. Only initial ticket seed; controller input thereafter.','direct_scene_visual':'Three actual current047 screenshots inspected; not independent RGB raster reconstruction or human approval.'},'not_performed':['new emulator run after stop','new CPU replay after stop','independent RGB raster reconstruction','natural full playthrough','whole corpus closure','PCM listening','hardware QA','final human wording/name/graphics approval','final public release or Cafe worklog/publication'],'resume_only_on_user_request':'Only after user resume: compare current047 successful ride entry slot2A departure text with scene_context_105.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
 print(json.dumps({k:report[k] for k in ['status','frames_each','declared_files_each','equal_declared_files','whole_PNG_exact','differences']},ensure_ascii=False))
if __name__=='__main__':main()
