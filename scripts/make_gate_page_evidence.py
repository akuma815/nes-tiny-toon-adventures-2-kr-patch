"""Collect actual completed Korean page snapshots, never synthetic ROM previews."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--build',type=Path,required=True);ap.add_argument('--prefix',required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();pages=json.loads((a.build/'ui_korean_page_mapping.json').read_text('utf-8'));found=[]
 for page in pages:
  font=page['profile']['font_bank'];candidates=[]
  for route in ('castle',):
   folder=ROOT/'qa/dialogue'/f'{a.prefix}_{route}'
   for f in sorted(folder.glob('frame_*.png')):
    ram=(folder/(f.stem+'_ram.bin')).read_bytes()
    if ram[0x34]!=font:continue
    ppu=(folder/(f.stem+'_ppu.bin')).read_bytes()
    if all(ppu[0x22a8+0x40*i:0x22a8+0x40*i+line['expanded_tiles']]==bytes.fromhex(line['expanded_hex']) for i,line in enumerate(page['layout'])):candidates.append((route,f));break
  assert candidates,(font,page['profile']['entry_id']);route,f=candidates[0];found.append({'entry_id':page['profile']['entry_id'],'font':font,'route':route,'frame':int(f.stem[6:]),'image':f.relative_to(ROOT).as_posix(),'actual_completed_nametable_equal':True})
 out=a.output.resolve();out.relative_to((ROOT/'qa/dialogue').resolve());assert not out.exists();canvas=Image.new('RGB',(1024,len(found)*990),(25,25,25))
 for i,v in enumerate(found):
  canvas.paste(Image.open(ROOT/v['image']).convert('RGB').resize((1024,960),Image.Resampling.NEAREST),(0,i*990+30));ImageDraw.Draw(canvas).text((10,i*990+8),f"{v['entry_id']} font {v['font']} {v['route']} frame {v['frame']}",fill='white')
 canvas.save(out);out.with_suffix('.json').write_text(json.dumps(found,indent=2)+'\n',encoding='utf-8')
 for start in range(0,len(found),4):canvas.crop((0,start*990,1024,min(start+4,len(found))*990)).save(out.parent/f'{out.stem}_review_{start//4+1}.png')
 print(json.dumps(found,indent=2))
if __name__=='__main__':main()
