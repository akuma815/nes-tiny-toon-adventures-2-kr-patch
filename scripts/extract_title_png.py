"""Extract the split-bank title artwork using the verified runtime nametables."""
import argparse,hashlib,json
from collections import Counter
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def decode(raw):
 return bytes(((raw[y]>>(7-x))&1)|(((raw[y+8]>>(7-x))&1)<<1) for y in range(8) for x in range(8))
def encode(pixels):
 return bytes(sum(((pixels[y*8+x]>>plane)&1)<<(7-x) for x in range(8)) for plane in range(2) for y in range(8))
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--output',type=Path,default=ROOT/'extracted/title/title_20261004_001')
 a=ap.parse_args()
 m=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'));rom=(ROOT/m['path']).read_bytes()
 assert hashlib.sha256(rom).hexdigest()==m['sha256']
 p=ROOT/'qa/screenshots/baseline_attract_002';ppu=(p/'frame_00720_ppu.bin').read_bytes();screen=Image.open(p/'frame_00720.png').convert('RGB')
 out=a.output.resolve();assert ROOT/'original' not in out.parents and out!=ROOT/'original'
 out.mkdir(parents=True,exist_ok=False)
 sections=[]
 for name,ntbase,chrbase,box in [('main',0x2000,0x37010,(40,24,216,112)),('ribbon',0x2800,0x39010,(32,112,224,144))]:
  nt=ppu[ntbase:ntbase+1024];indexed=Image.new('L',(256,240));palette_ids=Image.new('L',(256,240))
  for y in range(240):
   for x in range(256):
    t=nt[y//8*32+x//8];v=decode(rom[chrbase+t*16:chrbase+(t+1)*16])[y%8*8+x%8]
    attr=nt[960+(y//32)*8+x//32];shift=((y//16)%2)*4+((x//16)%2)*2;pal=(attr>>shift)&3
    indexed.putpixel((x,y),v);palette_ids.putpixel((x,y),pal)
  colors={}
  for group in range(4):
   for v in range(4):
    pixels=[screen.getpixel((x,y+(-2 if name=='ribbon' else 0))) for y in range(box[1],box[3]) for x in range(box[0],box[2]) if indexed.getpixel((x,y))==v and palette_ids.getpixel((x,y))==group]
    if pixels: colors[(group,v)]=Counter(pixels).most_common(1)[0][0]
  rgb=Image.new('RGB',(256,240),'black')
  for y in range(box[1],box[3]):
   for x in range(box[0],box[2]):rgb.putpixel((x,y),colors[(palette_ids.getpixel((x,y)),indexed.getpixel((x,y)))])
  crop=rgb.crop(box);crop.save(out/f'{name}_original.png');crop.resize((crop.width*8,crop.height*8),Image.Resampling.NEAREST).save(out/f'{name}_original_8x.png')
  indexed.save(out/f'{name}_indices_full.png');palette_ids.save(out/f'{name}_palettes_full.png');(out/f'{name}_nametable.bin').write_bytes(nt)
  used={nt[y*32+x] for y in range(box[1]//8,box[3]//8) for x in range(box[0]//8,box[2]//8)}
  protected={nt[y*32+x] for y in range(30) for x in range(32) if not(box[0]//8<=x<box[2]//8 and box[1]//8<=y<box[3]//8)}
  for t in used:
   assert encode(decode(rom[chrbase+t*16:chrbase+(t+1)*16]))==rom[chrbase+t*16:chrbase+(t+1)*16]
  sections.append({'name':name,'nametable_ppu_base':ntbase,'chr_file_base':chrbase,'box':box,
   'used_tiles':sorted(used),'exclusive_tiles':sorted(used-protected),'protected_shared_tiles':sorted(used&protected),
   'rgb_by_palette_index':{f'{g},{v}':list(c) for (g,v),c in colors.items()},
   'indices_png':f'{name}_indices_full.png','palette_groups_png':f'{name}_palettes_full.png',
   'png_roundtrip':True,'display_dy':-2 if name=='ribbon' else 0,
   'layout_consumer':'See manifests/title_layout.json and qa/title/chr_stream_trace_001; extraction itself is read-only'})
 screen.save(out/'title_original.png');screen.resize((1024,960),Image.Resampling.NEAREST).save(out/'title_original_4x.png')
 report={'source_sha256':m['sha256'],'runtime_frame':720,'sections':sections,
  'split':'CHR page17/main NT2000 above y112; CHR page19/ribbon NT2800 below y112; IRQ switch at scanline111/112',
  'number_2':'Separate OAM sprites in CHR 1k bank95; preserve',
  'status':'PNG extraction and tile roundtrip only; no ROM modification'}
 (out/'title_extraction.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
