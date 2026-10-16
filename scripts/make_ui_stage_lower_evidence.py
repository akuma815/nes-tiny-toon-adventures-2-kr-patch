"""Actual complete lower messages and exact rejected034 transition control."""
import json
from pathlib import Path
from PIL import Image
from verify_ui_macro_passthrough import state_reader
ROOT=Path(__file__).resolve().parents[1]
def main():
 d=ROOT/'build/dialogue_kr_poc_036';rom=(d/'TinyToon2_dialogue_kr_poc.nes').read_bytes();manifest=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));view=bytearray((ROOT/manifest['path']).read_bytes());view[0x4010:0x8010]=rom[0x24010:0x28010];pages=json.loads((d/'ui_korean_page_mapping.json').read_text('utf-8'));found=[]
 for page in pages:
  p=page['profile']
  if p['technical']:continue
  candidates=[];route='normal3' if p['slot'] in (41,43) else 'coaster';folder=ROOT/'qa/dialogue'/f'stage_lower036_{route}'
  for f in sorted(folder.glob('frame_*.png')):
   rb=(folder/(f.stem+'_ram.bin')).read_bytes()
   # The native FF consumer advances6CF after the completed last glyph.
   if rb[0x6f3]!=196 or rb[0x6cf] not in (p['slot'],p['slot']+1):continue
   lines=[];line=[]
   for e in state_reader(view,p['pointer'],tuple(rb[0x7d0:0x7d3]),rb[0xb],rb[0x25]):
    if e['value'] in (254,255):lines.append(bytes(line));line=[]
    else:line.append(e['value'])
   ppu=(folder/(f.stem+'_ppu.bin')).read_bytes();base=p['NT']
   if all(ppu[base+row*0x40:base+row*0x40+len(line)]==line for row,line in enumerate(lines)):candidates.append(f)
  assert len(candidates)>1,p['entry_id'];f=candidates[1];out=ROOT/'qa/dialogue'/f"stage_lower036_{p['slot']:02X}_actual.png";assert not out.exists();Image.open(f).convert('RGB').resize((1024,960),Image.Resampling.NEAREST).save(out);found.append({'entry_id':p['entry_id'],'slot':p['slot'],'route':route,'frame':int(f.stem[6:]),'source_image':f.relative_to(ROOT).as_posix(),'review_image':out.relative_to(ROOT).as_posix(),'completed_native_NT_equal':True,'review':'pending direct review'})
 for prefix,label in [('remaining034_normal3','rejected034'),('stage_lower036_normal3','fixed036')]:
  f=ROOT/'qa/dialogue'/prefix/'frame_02004.png';out=ROOT/'qa/dialogue'/f'stage_lower036_transition_{label}.png';assert not out.exists();Image.open(f).convert('RGB').resize((1024,960),Image.Resampling.NEAREST).save(out);found.append({'scene':'same controller/seed transition2004','build_control':label,'frame':2004,'source_image':f.relative_to(ROOT).as_posix(),'review_image':out.relative_to(ROOT).as_posix(),'review':'pending direct review'})
 out=ROOT/'qa/dialogue/stage_lower036_actual_pages.json';assert not out.exists();out.write_text(json.dumps(found,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(found,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
