"""Work97 real bank61 flag positive control, instrumentation parity and RGB."""
from pathlib import Path
import json,csv,hashlib
from collections import Counter
from PIL import Image,ImageChops
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads(p.read_text('utf-8'))
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 output=R/'qa/reports/pow097_positive_control.json';assert not output.exists();rom=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();m=j(R/'manifests/source_rom.json');assert sha(R/m['path'])==m['sha256'];assert blob[0x3f73a:0x3f73f]==bytes.fromhex('a9 3e 8d 05 04')
 A=R/'qa/dialogue/bank61_097_baseline047';B=R/'qa/dialogue/bank61_097_probe047';envs=[j(q/'environment.json')for q in(A,B)]
 for q,e in zip((A,B),envs):
  assert e['exit_code']==0 and e['frames']==8000 and e['rom_sha256']==sha(rom)
  for n,h in e['files'].items():assert sha(q/n)==h
  assert(q/'trace_complete.txt').read_text()=='8000'
 assert all(envs[0][k]==envs[1][k]for k in('source_sha256','rom_sha256','exe_sha256','config_sha256','frames','input','seed','seed_file_sha256','intervention'))
 native=[]
 for p in sorted(A.iterdir()):
  if p.name.startswith(('frame_','gameover_top_'))or p.name in('menu_events.csv','seed_writes.csv','world_phase.csv','native_NT_calls.csv','gameover_consumers.csv','gameover_top_fonts.csv','trace_complete.txt','config_used.json','inputs_used.json','seed_used.json'):
   assert p.read_bytes()==(B/p.name).read_bytes(),p.name;native.append(p.name)
 images=sorted(A.glob('frame_*.png'));assert len(images)==606 and[p.name for p in images]==[p.name for p in sorted(B.glob('frame_*.png'))]
 poses=rows(B/'bank61_pose_consumers.csv');patterns=rows(B/'bank61_pattern_reads.csv');top=rows(B/'bank61_top_OAM.csv');assert len(poses)==1611 and len(patterns)==51520 and len(top)==805
 assert all(x['art_id']=='3E'and x['RAM38']=='3D'and x['CHR1800']=='0F400'and x['actor']=='5'and x['root']=='04'and x['phase']=='0C'and x['largeSprites']=='true'for x in poses)
 execs=[x for x in poses if x['kind']=='native9643_exec'];writers=[x for x in poses if x['kind']=='art_RAM_write'];assert len(execs)==805 and len(writers)==806
 assert all(x['observed_pc']=='9643'and x['PRG_relative']=='2D643'for x in execs);assert all(x['observed_pc']=='F72F'and x['PRG_relative']=='3F72F'and x['address']=='0405'for x in writers)
 classes=Counter();count_by_frame=Counter();frame_values={}
 for x in patterns:
  frame=int(x['frame']);relative=int(x['CHR_relative'],16);value=int(x['value'],16);assert 5296<=frame<=6100 and value==blob[0x40010+relative]and int(x['count'])==1
  assert 0xf400<=relative<0xf440 and int(x['ppu_address'],16)==relative-0xf400+0x1800;classes[x['classification']]+=1;count_by_frame[frame]+=1;frame_values.setdefault(frame,set()).add(relative)
 assert dict(classes)=={'other61':25760,'flag_control':25760}and set(count_by_frame.values())=={64}and len(count_by_frame)==805
 assert all(s==set(range(0xf400,0xf440))for s in frame_values.values())
 captures=[];raw=blob[0x4f430:0x4f450];bits=list(decode(raw[:16]))+list(decode(raw[16:]));palette_RGB={0x0f:(0,0,0),0x2a:(92,228,48),0x20:(255,254,255),0x00:(102,102,102)}
 for x in top:
  frame=int(x['frame']);assert 5296<=frame<=6100 and x['tile']=='83'and x['CHR_relative']=='0F420'and x['CHR1800']=='0F400'and x['largeSprites']=='true'and x['y']=='164'and x['x']=='120'and x['attributes']=='02'
  tag=x['capture_tag']
  if not tag:continue
  ppu=(B/(tag+'_ppu.bin')).read_bytes();oam=(B/(tag+'_oam.bin')).read_bytes();i=int(x['OAM_index'])*4;assert oam[i:i+4]==bytes([164,0x83,2,120])and ppu[0x1820:0x1840]==raw
  assert ppu[0x3f18:0x3f1c]==bytes.fromhex('0f 2a 20 00');colors=[palette_RGB[c]for c in ppu[0x3f18:0x3f1c]];expected=Image.new('RGB',(8,16));expected.putdata([colors[v]for v in bits]);actual=Image.open(B/f'frame_{frame:05}.png').convert('RGB').crop((120,165,128,181));assert ImageChops.difference(actual,expected).getbbox()is None;captures.append({'frame':frame,'tag':tag,'OAM_index':int(x['OAM_index']),'sprite_Y_screen_offset':1})
 assert len(captures)==27
 world=rows(B/'world_phase.csv');assert any(x['root']=='04'and x['phase']=='0C'for x in world)and any(int(x['frame'])>6100 and x['root']=='08'for x in world)
 result={'work':97,'status':'PASS_NATIVE_BANK61_FLAG_POSITIVE_CONTROL','ROM047_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'controller_frames_each':8000,'initial_normal4_seed_at1000':True,'instrumentation_baseline_native_files_byte_exact':len(native),'actual_PNGs_byte_exact':len(images),'flag_art_RAM_writes':len(writers),'native9643_frame3E_calls':len(execs),'actual_flag_OAM_top_frames':len(top),'bank61_PPU_read_rows':len(patterns),'bank61_read_classification':dict(classes),'each805frame_reads_64_source_bytes_exact':True,'actual_flag_source_ROM_RGB_exact_captures':captures,'palette_RGB_scope':'Values matched to actual Mesen/default capture using native sprite2 palette codes; not physical-console palette claim','selected_POW_pose_producers_and_pattern_reads':0,'known_consumer_chain':'F72A LDA3E -> F72C STA0405 (observed PCF72F) -> common9643 actor5 -> OAM83 -> PPU1820 -> physicalCHR0F420 -> actual8x16 RGB','actual_gameover_YES_returns_home':True,'source_unchanged':True,'ROM_CSV_edited':False,'human_final_review':False,'limits':['Positive control proves this bank61 callback/OAM connection works for known flag; POW actual use still unresolved','Frame3E and physical0F420..0F440 are flag, not POW letters; no POW translation or preservation approval','POW zero observations in this initial-ticket4/gameover/YES route do not prove global unused art','Native labels/callback data are same047; no fullplay/hardware/PCM listening/finalhuman/Cafe claim']}
 output.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k!='actual_flag_source_ROM_RGB_exact_captures'},indent=2))
if __name__=='__main__':main()