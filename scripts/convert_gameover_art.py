"""Technical AI-to-NES palette conversion, separate from image generation."""
import json,hashlib
from pathlib import Path
from PIL import Image
from extract_title_png import encode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def convert():
 d=R/'workspace/graphics/gameover_kr_ai_001';src=d/'generated_gameover_ko.png';im=Image.open(src).convert('RGBA');bounds=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();assert bounds==(53,115,2123,631);art=im.crop(bounds);w,h=art.size;nh=28;nw=round(w*nh/h);assert nw==112 and nw<=124;art=art.resize((nw,nh),Image.Resampling.LANCZOS);left=(128-nw)//2;top=(32-nh)//2;meta=json.loads((R/'extracted/graphics/gameover_001/consumer.json').read_text('utf-8'));colors={int(k):tuple(v) for k,v in meta['logo_native_colors'].items()};grid=bytearray(128*32)
 for y in range(nh):
  for x in range(nw):
   p=art.getpixel((x,y));v=0 if p[3]<128 else min((1,2,3),key=lambda i:sum((p[k]-colors[i][k])**2 for k in range(3)));grid[(y+top)*128+x+left]=v
 assert all(v==0 for v in grid[:128]) and all(v==0 for v in grid[-128:]);raw=bytearray()
 for row in range(4):
  for col in range(16):raw.extend(encode(bytes(grid[(row*8+y)*128+col*8+x] for y in range(8) for x in range(8))))
 assert len(raw)==1024;preview=Image.new('RGB',(128,32));preview.putdata([colors[v] for v in grid]);record={'work':48,'generated_SHA256':sha(src.read_bytes()),'reference':'extracted/graphics/gameover_001/source_logo.png','crop_alpha128_bbox':bounds,'resample':'Pillow LANCZOS, alpha128 foreground, closest native3ink colors inRGB','fitted_size':[nw,nh],'placement':[left,top],'native_canvas':[128,32],'palette':colors,'tile_layout':'4rows x16columns, sourceNTcodesC0..FF unchanged','native_raw_sha256':sha(raw),'scope':'Technical color/dimension conversion of exact게임 오버 generatedart; actualROM visualpending'}
 for p,content in [(d/'converted_bank213.bin',bytes(raw)),(d/'conversion.json',(json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))]:
  if p.exists():assert p.read_bytes()==content
  else:p.write_bytes(content)
 for name,image in [('converted_logo.png',preview),('converted_logo_4x.png',preview.resize((512,128),Image.Resampling.NEAREST))]:
  if (d/name).exists():assert Image.open(d/name).convert('RGB').tobytes()==image.tobytes()
  else:image.save(d/name)
 return bytes(raw),record
if __name__=='__main__':print(json.dumps(convert()[1],ensure_ascii=False,indent=2))
