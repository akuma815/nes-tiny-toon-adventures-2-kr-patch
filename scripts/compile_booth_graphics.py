"""Galmuri labels in cloned124 font and generated header in native palette."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import encode,decode
R=Path(__file__).resolve().parents[1]
def compile_booth(prior,source):
 survey=json.loads((R/'extracted/graphics/booth_001/consumer.json').read_text('utf-8'));mapping={' ':0};chars=list(dict.fromkeys(c for p in survey['labels'] for c in p['translation_ko'] if c!=' '));assert len(chars)<=42;mapping.update({c:i+1 for i,c in enumerate(chars)});font=bytearray(prior[0x5f010:0x5f810]);assert font==source[0x3f010:0x3f810];atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);glyphs=[]
 for c in chars:
  n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(bits) and bits==[int(v>127) for v in im.get_flattened_data()];raw=encode(bytes(2*v for v in bits));code=mapping[c];font[code*16:(code+1)*16]=raw;glyphs.append({'char':c,'code':code,'chr_hex':raw.hex(),'provider':'Galmuri7 atlas and TTF exact, no fallback'})
 assert font[0x41*16:]==source[0x3f010+0x41*16:0x3f810] and font[:16]==bytes(16);labels=[]
 for p in survey['labels']:
  off,n=p['source_file_offset'],p['length'];old=bytes.fromhex(p['source_hex']);assert prior[off:off+n]==prior[off+0x20000:off+0x20000+n]==source[off:off+n]==old;desired=p['translation_ko'].ljust(n);assert len(desired)==n;body=bytes(mapping[c] for c in desired);assert all(v<0x80 for v in body);labels.append({**p,'desired_padded':desired,'body_hex':body.hex(),'status':'draft'})
 im=Image.open(R/'workspace/graphics/booth_header_ai_001.png').convert('RGB');assert im.size==(2172,724);area=im.crop((300,220,1850,500));mask=Image.new('1',area.size)
 for y in range(area.height):
  for x in range(area.width):mask.putpixel((x,y),int(max(area.getpixel((x,y)))<45))
 box=mask.getbbox();assert box;crop=area.crop(box);height=10;width=round(crop.width*height/crop.height);assert 30<=width<=50;small=crop.resize((width,height),Image.Resampling.NEAREST);orig=(R/'extracted/graphics/booth_001/header_source_indices.bin').read_bytes();target=bytearray(orig)
 for y in range(3,13):
  for x in range(3,93):target[y*96+x]=1
 x0=(96-width)//2
 for y in range(height):
  for x in range(width):target[(3+y)*96+x0+x]=2 if max(small.getpixel((x,y)))<70 else 1
 assert all(target[y*96+x]==orig[y*96+x] for y in range(16) for x in range(96) if not (3<=x<93 and 3<=y<13));changes=[]
 for c in survey['header_cells']:
  addr=c['NT'];col=addr%32-10;row=addr//32%32-4;pixels=bytes(target[(row*8+y)*96+col*8+x] for y in range(8) for x in range(8));raw=encode(pixels);assert decode(raw)==pixels
  if raw.hex()!=c['source_raw_hex']:changes.append({**c,'final_hex':raw.hex()})
 colors={int(k):tuple(v) for k,v in survey['header_palette'].items()};preview=Image.new('RGB',(96,16));preview.putdata([colors[v] for v in target]);out=R/'workspace/graphics/booth_header_kr_001';out.mkdir(exist_ok=True);preview.save(out/'native.png');preview.resize((768,128),Image.Resampling.NEAREST).save(out/'preview_8x.png');(out/'indices.bin').write_bytes(target)
 plan={'date':'2026-10-05','work':42,'prior_build':'dialogue_kr_poc_038','labels':labels,'font_bank':204,'font_range':[0x73010,0x73810],'font_hex':bytes(font).hex(),'mapping':mapping,'glyphs':glyphs,'Hangul_unique':len(chars),'native_ascii_digits_punctuation_graphics_preserved':True,'header':{'exact_text':'매표소','AI_source':'workspace/graphics/booth_header_ai_001.png','AI_sha256':hashlib.sha256((R/'workspace/graphics/booth_header_ai_001.png').read_bytes()).hexdigest(),'AI_crop_region':[300+box[0],220+box[1],300+box[2],220+box[3]],'native_letter_size':[width,height],'placement':[x0,3],'admitted_local_letter_box':[3,3,93,13],'native_frame_pixels_unchanged':True,'changes':changes,'indices_sha256':hashlib.sha256(target).hexdigest()},'producer':{'source_file_offsets':[0x5ca6,0x25ca6],'expected_hex':'7c','final_hex':'cc'},'scope':'Five observed literal labels plus generated header; native length/compression controls/numbers/UI/other fonts preserved; runtime pending'};p=R/'workspace/translation/booth_graphics_plan_001.json';p.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return plan
if __name__=='__main__':
 m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));p=compile_booth((R/'build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes').read_bytes(),(R/m['path']).read_bytes());print(json.dumps({'Hangul_unique':p['Hangul_unique'],'labels':len(p['labels']),'header':{k:v for k,v in p['header'].items() if k!='changes'}},ensure_ascii=False,indent=2))
