"""Current047 successful ride slot2A: frozen captures, native rows and independent RGB."""
from pathlib import Path
import csv,hashlib,json,re,collections
from PIL import Image,ImageChops
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/context107_validation.json';assert not out.exists()
 D=R/'qa/dialogue/context107_normal4047';e=json.loads((D/'environment.json').read_text('utf-8'));rompath=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';rom=rompath.read_bytes()
 assert sha(rompath)==e['rom_sha256']=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 meta=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/meta['path'])==e['source_sha256']==meta['sha256']
 assert sha(R/'workspace/translation/text_ja.csv')=='ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556'
 assert e['exit_code']==0 and e['frames']==4200 and (D/'trace_complete.txt').read_text()=='4200'
 for p,h in e['files'].items():assert sha(D/p)==h,p
 for p,k in [('capture_survey_used.lua','lua_sha256'),('config_used.json','config_sha256'),('seed_used.json','seed_file_sha256')]:assert sha(D/p)==e[k]
 assert sha(Path(e['exe_path']))==e['exe_sha256'] and sha(D/'inputs_used.json')==e['input']['file_sha256']
 assert e['seed']['frame']==1000 and [(w['address'],w['value'])for w in e['seed']['writes']]==[(0x7d0,4),(0x7d1,0),(0x7d2,0)]
 fontpath=R/'build/dialogue_kr_poc_036/ui_stage_lower_shared_font.json';font=json.loads(fontpath.read_text('utf-8'));glyph={v['code']:v['char']for v in font['glyphs']};glyph[0]=' ';glyph.update({0x70+i:str(i)for i in range(10)})
 fontbytes=bytes.fromhex(font['font_hex']);assert font['font_bank']==196 and rom[0x71010:0x71810]==fontbytes
 pages=json.loads((R/'build/dialogue_kr_poc_036/ui_korean_page_mapping.json').read_text('utf-8'));page=next(x for x in pages if x['profile']['entry_id']=='MAIN_05920');profile=page['profile'];assert profile['slot']==0x2a and profile['pointer']==0x9910 and profile['text']=='출발!'
 assert rom[0x25920:0x25929]==bytes.fromhex(page['body_hex'])
 assert int.from_bytes(rom[0x255a9+2*0x2a:0x255ab+2*0x2a],'little')==0x9910
 ledger=json.loads((R/'workspace/translation/scene_context_105.json').read_text('utf-8'));context=next(x for x in ledger['context_overrides']if x['entry_id']=='MAIN_05920');assert context['native_slots_hex']==['2A']
 events=list(csv.DictReader((D/'menu_events.csv').open(encoding='utf-8')))
 active=[x for x in events if x['kind']=='write' and x['address']=='06F3' and x['id']=='2A' and x['pointer']=='9910'];assert [int(x['frame'])for x in active]==[2001,2008] and all(x['value']==x['font']=='C4'for x in active)
 expected=bytes.fromhex(page['layout'][0]['expanded_hex']);assert expected==bytes.fromhex('0037386c7a7a7a7a')
 frames=[];fontframes=[];phases=[];clear=[];romchr=rom[0x40010:]
 P=R/'qa/dialogue/context107_palette047';pe=json.loads((P/'environment.json').read_text('utf-8'))
 assert pe['rom_sha256']==e['rom_sha256'] and pe['seed']==e['seed'] and pe['input']==e['input'] and pe['exit_code']==0
 for p,h in pe['files'].items():assert sha(P/p)==h,p
 comparable_probe=[p for p in e['files']if p!='capture_survey_used.lua']
 assert all(e['files'][p]==pe['files'][p]for p in comparable_probe)
 ink=list(csv.DictReader((P/'context107_render_ink.csv').open(encoding='utf-8')));render=collections.defaultdict(list)
 for x in ink:
  assert int(x['snapshot_frame'])==int(x['frame_before_end'])+1 and x['grayscale']=='false'
  addr=int(x['ppu_address'],16);relative=int(x['CHR_relative'],16);assert relative==0x31000+addr and int(x['value'],16)==rom[0x40010+relative]
  assert 163<=int(x['scanline'])<=170
  render[int(x['snapshot_frame'])].append(x)
 source=(R/'work/context107/NesDefaultVideoFilter_2.1.1.cpp').read_text('utf-8');line=next(x for x in source.splitlines()if '/* 2C02 */'in x)
 values=[int(v,16)for v in re.findall('0x([0-9A-F]{8})',line)];assert len(values)==64
 colors={i:((v>>16)&255,(v>>8)&255,v&255)for i,v in enumerate(values)}
 assert colors[0]==(102,102,102) and colors[0x10]==(173,173,173) and colors[0x20]==(255,254,255)
 assert 'ProcessEvent(EventType::EndFrame)' in (R/'work/context107/NesPpu_2.1.1.cpp').read_text('utf-8')
 screenshot_palette=[]
 for p in sorted(D.glob('frame_*_ram.bin')):
  frame=int(p.name[6:11]);tag=f'frame_{frame:05}';ram=p.read_bytes();ppu=(D/(tag+'_ppu.bin')).read_bytes()
  maps=list(csv.DictReader((D/(tag+'_mapping.csv')).open(encoding='utf-8')))
  for m in maps:
   if m['kind']=='chr':a=int(m['cpu_or_ppu_address'],16);offset=int(m['relative_offset'],16);assert ppu[a:a+0x400]==romchr[offset:offset+0x400],(frame,a)
  if 1578<=frame<=2634:
   assert ram[0xc6]==ram[0x6f3]==196 and ppu[:0x800]==fontbytes; fontframes.append(frame)
  if 2001<=frame<2634:assert ram[0x7d0:0x7d3]==bytes(3)
  if frame>=3000:assert ram[0x18]==4 and ram[0x54]==5 and ram[0x25]==0
  if 2004<=frame<=2040:phases.append({'frame':frame,'postread_id_hex':f'{ram[0x6cf]:02X}','row1_hex':ppu[0x22a8:0x22b7].hex(),'row2_hex':ppu[0x22e8:0x22f3].hex()})
  if 2010<=frame<=2019 and not any(ppu[0x22a8:0x22b7]+ppu[0x22e8:0x22f3]):clear.append(frame)
  if 2001<=frame<=2634 and ppu[0x22a8:0x22b0]==expected:
   assert ppu[0x22e8:0x22f3]==bytes(11)
   assert ''.join(glyph[v]for v in expected)==' 출발!    '
   row,col=21,8;attr=ppu[0x23c0+(row//4)*8+col//4];group=(attr>>(((row%4)//2)*4+((col%4)//2)*2))&3;assert group==2
   samples=render[frame-1];assert len(samples)==32
   palettes={x['palette_group2']for x in samples};assert len(palettes)==1
   live_palette=bytes.fromhex(next(iter(palettes)))
   assert {int(x['scanline'])for x in samples}==set(range(163,171))
   screenshot_palette.append({'PNG_frame':frame,'render_frame':frame-1,'read_rows':32,'render_palette_group2':live_palette.hex(),'endframe_palette_group2':ppu[0x3f08:0x3f0c].hex()})
   target=Image.new('RGB',(64,8))
   for i,code in enumerate(expected):
    tile=Image.new('RGB',(8,8));tile.putdata([colors[live_palette[b]]for b in decode(fontbytes[16*code:16*code+16])]);target.paste(tile,(i*8,0))
   crop=Image.open(D/(tag+'.png')).convert('RGB').crop((64,163,128,171));assert ImageChops.difference(target,crop).getbbox()is None,frame
   frames.append(frame)
 assert frames and 2019<=min(frames)<=2040 and max(frames)==2634 and clear
 def snap(f):return (D/f'frame_{f:05}_ram.bin').read_bytes()
 assert snap(1998)[0x7d0:0x7d3]==bytes([4,0,0]) and snap(2001)[0x7d0:0x7d3]==bytes(3)
 # Same currentROM historical run is comparable only before its extra6100 input.
 H=R/'qa/dialogue/bank61_097_baseline047';h=json.loads((H/'environment.json').read_text('utf-8'));assert h['rom_sha256']==e['rom_sha256'] and h['seed']==e['seed'] and h['input']['sequence'][:6]==e['input']['sequence']
 comparable=[p for p in e['files']if p.startswith('frame_') and p in h['files']]
 for p in comparable:assert sha(H/p)==h['files'][p]==e['files'][p],p
 result={'work':107,'status':'PASS_CURRENT047_SUCCESSFUL_RIDE_CONTEXT','ROM047_sha256':e['rom_sha256'],'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_sha256':meta['sha256'],'environment_sha256':sha(D/'environment.json'),'verified_capture_files':len(e['files']),'whole_capture_PNGs':sum(p.endswith('.png')for p in e['files']),'seed':e['seed'],'native_source_entry':'MAIN_05920','native_slot_hex':'2A','native_pointer_hex':'9910','context_105':context,'font_init_events':active,'cost_before_after':{'frame1998':'4','frame2001':'0'},'lower_font196_exact_frames':fontframes,'native_complete_NT_and_independent_RGB_frames':frames,'clear_frames':clear,'transition_samples':phases,'historical_same047_before_extra6100_input_equal_files':len(comparable),'historical_whole_PNG_exact':sum(p.endswith('.png')for p in comparable),'mapped_CHR_chunks_ROM_exact':8*sum(p.endswith('.png')for p in e['files']),'direct_visual_review_frames':[2004,2010,2040,2100,3000],'screenshot_palette_alignment':screenshot_palette,'read_only_probe_equal_declared_files':len(comparable_probe),'probe_PPU_glyph_read_rows':len(ink),'screenshot_timing':'Mesen2.1.1 NES sends EndFrame event before VideoDecoder.UpdateFrame. Lua takeScreenshot uses existing filtered buffer; PNG at snapshotN aligns to rendered frameN-1. Actual read telemetry and53 RGB crops verify this bound; not a universal timestamp rule.','runtime_observation':'Fee4 -> native charge4to0 -> F9 alias23 -> start2A -> coarse root4 phase5 gameplay. Seededinitialcurrency; no fullplay claim.','ROM_CSV_changed':False,'human_approved':False,'limits':['Only controlled initial ticket4 coaster route','Same-ROM historical comparison before input6100; not originalROM/fullgame equivalence','Font/NT/RGB proof applies to captured frames only; exact Mesen2.1.1 framebuffer timing bound','No new build/apply/hardware/PCM listening/fullplay/corpus closure/final human wording approval'],'next_action':'Reconcile current047 localization scope and remaining consumer/corpus/playthrough gaps from existing frozen evidence; choose a discriminating technical investigation without repeating equivalent QA.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:result[k]for k in ['status','verified_capture_files','whole_capture_PNGs','mapped_CHR_chunks_ROM_exact','historical_whole_PNG_exact']}))
if __name__=='__main__':main()
