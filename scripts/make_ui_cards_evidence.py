"""Actual five completed shared-font cards; no synthetic game screenshots."""
import json,csv
from pathlib import Path
from PIL import Image,ImageDraw
from verify_ui_macro_passthrough import state_reader
ROOT=Path(__file__).resolve().parents[1]
def main():
 d=ROOT/'build/dialogue_kr_poc_033';rom=(d/'TinyToon2_dialogue_kr_poc.nes').read_bytes();m=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));view=bytearray((ROOT/m['path']).read_bytes());view[0x4010:0x8010]=rom[0x24010:0x28010];pages=json.loads((d/'ui_korean_page_mapping.json').read_text('utf-8'));by={p['profile']['slot']:p for p in pages};found=[]
 for ride,route in enumerate(('coaster','cart','train','water','gold4'),1):
  folder=ROOT/'qa/dialogue'/f'cards033_{route}';slots=[29+ride,35+ride]+([] if ride==5 else [29]);candidates=[]
  for f in sorted(folder.glob('frame_*.png')):
   rb=(folder/(f.stem+'_ram.bin')).read_bytes()
   if rb[0x34]!=193 or rb[0x25]!=ride or ride!=5 and rb[0x6f3]!=193:continue
   ppu=(folder/(f.stem+'_ppu.bin')).read_bytes();ok=True
   for slot in slots:
    p=by[slot]['profile'];base=p['NT'];line=[];lines=[]
    for e in state_reader(view,p['pointer'],tuple(rb[0x7d0:0x7d3]),rb[0xb],ride):
     if e['value'] in (254,255):lines.append(bytes(line));line=[]
     else:line.append(e['value'])
    ok&=all(ppu[base+row*0x40:base+row*0x40+len(line)]==line for row,line in enumerate(lines))
   if ok:candidates.append(f)
  assert len(candidates)>1,(route,len(candidates));f=candidates[1];out=ROOT/'qa/dialogue'/f'cards033_{route}_actual.png';assert not out.exists();im=Image.open(f).convert('RGB').resize((1024,960),Image.Resampling.NEAREST);im.save(out)
  found.append({'ride':ride,'route':route,'frame':int(f.stem[6:]),'source_image':f.relative_to(ROOT).as_posix(),'review_image':out.relative_to(ROOT).as_posix(),'completed_native_NT_slots':slots,'font':193,'cost_native_FA':None if ride==5 else json.loads((d/'ui_card_shared_font.json').read_text('utf-8'))['native_FA_codes_by_ride'][str(ride)],'intervention':'explicit initial gold4 RAM seed' if ride==5 else 'controller only','review':'pending direct image review'})
 out=ROOT/'qa/dialogue/cards033_actual_pages.json';assert not out.exists();out.write_text(json.dumps(found,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(found,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
