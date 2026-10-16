"""Source-only bank54/61 native pose comparison; explanatory palette, not game PNG."""
from pathlib import Path
import argparse,json
from PIL import Image,ImageDraw
from analyze_pow_metasprites096 import run
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to(R/'work');assert not out.exists();r=(R/json.loads((R/'manifests/source_rom.json').read_text('utf-8'))['path']).read_bytes();pic=Image.new('RGB',(480,300),(25,25,25));dr=ImageDraw.Draw(pic);palette=[(25,25,25),(255,254,255),(116,80,168),(248,216,32)]
 for row,bank in enumerate((54,61)):
  for col,art in enumerate((0x9c,0x9d,0x9e,0x9f,0xa0,0xa1,0xa2,0xa3)):
   mem,c,data,n=run(r,art,0);tilePic=Image.new('RGB',(32,40),palette[0])
   for i in range(0,len(data),4):
    y,t,attr,x=data[i:i+4];lo=(t&254)-128;assert t%2==1 and 0<=lo<64;off=0x20010+bank*0x400+lo*16;raw=r[off:off+32];s=Image.new('RGB',(8,16));s.putdata([palette[v]for v in list(decode(raw[:16]))+list(decode(raw[16:]))]);tilePic.paste(s,(x-128+12,y-128+24))
   ox=col*60;oy=row*150;dr.text((ox+3,oy+3),f'{art:02X}/B{bank}',(255,255,255));pic.paste(tilePic.resize((48,80),Image.Resampling.NEAREST),(ox+4,oy+24))
 pic.save(out)
if __name__=='__main__':main()