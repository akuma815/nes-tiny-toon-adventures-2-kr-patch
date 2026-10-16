"""Convert generated raster lettering into exact native palette and source NT tiles."""
import json,hashlib
from pathlib import Path
from PIL import Image
from extract_title_png import encode,decode
R=Path(__file__).resolve().parents[1]
def compile_banner():
 consumer=json.loads((R/'extracted/graphics/map_banner_001/consumer.json').read_text('utf-8'));orig=(R/'extracted/graphics/map_banner_001/source_indices.bin').read_bytes();im=Image.open(R/'workspace/graphics/map_banner_ai_001.png').convert('RGB');assert im.size==(2172,724);area=im.crop((200,100,1972,600));mask=Image.new('1',area.size);colors=[(0,0,0),(192,223,255),(255,254,255),(181,49,32)]
 for y in range(area.height):
  for x in range(area.width):
   c=area.getpixel((x,y));red=c[0]>80 and c[0]>c[1]*1.7 and c[0]>c[2]*1.4;black=max(c)<80;mask.putpixel((x,y),int(red or black))
 box=mask.getbbox();assert box is not None;crop=area.crop(box);height=13;width=round(crop.width*height/crop.height);assert 55<=width<=85;small=crop.resize((width,height),Image.Resampling.NEAREST);target=bytearray(orig)
 for y in range(16):
  for x in range(6,137):target[y*144+x]=2
 x0=(144-width)//2;y0=1
 for y in range(height):
  for x in range(width):
   c=small.getpixel((x,y));nearest=min((0,2,3),key=lambda v:sum((c[k]-colors[v][k])**2 for k in range(3)));target[(y0+y)*144+x0+x]=nearest
 assert all(target[y*144+x]==orig[y*144+x] for y in range(16) for x in range(144) if not 6<=x<137);changes=[]
 for cell in consumer['cells']:
  addr=cell['NT'];col=(addr%32)-7;row=(addr//32%32)-3;pixels=bytes(target[(row*8+y)*144+col*8+x] for y in range(8) for x in range(8));raw=encode(pixels);assert decode(raw)==pixels
  if raw.hex()!=cell['source_raw_hex']:changes.append({**cell,'final_hex':raw.hex()})
 preview=Image.new('RGB',(144,16));preview.putdata([colors[v] for v in target]);out=R/'workspace/graphics/map_banner_kr_001';out.mkdir(exist_ok=True);preview.save(out/'native.png');preview.resize((1152,128),Image.Resampling.NEAREST).save(out/'preview_8x.png');(out/'indices.bin').write_bytes(target)
 plan={'date':'2026-10-05','work':40,'exact_text':'몬타나 랜드','generation':'built-in image_gen edit; source banner reference','AI_source':'workspace/graphics/map_banner_ai_001.png','AI_sha256':hashlib.sha256((R/'workspace/graphics/map_banner_ai_001.png').read_bytes()).hexdigest(),'AI_crop_region':[200+box[0],100+box[1],200+box[2],100+box[3]],'native_letter_size':[width,height],'placement':[x0,y0],'admitted_local_letter_box':[6,0,137,16],'native_frame_pixels_unchanged':True,'NT_mapping_unchanged':True,'palette_unchanged':True,'changes':changes,'indices_sha256':hashlib.sha256(target).hexdigest(),'scope':'AI raster quantization only; no code-drawn Hangul/fallback; actual scene review pending'};(out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return plan
if __name__=='__main__':print(json.dumps({k:v for k,v in compile_banner().items() if k!='changes'},ensure_ascii=False,indent=2))
