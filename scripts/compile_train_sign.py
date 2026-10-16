"""Galmuri7 nativebitmap captions; isolated clone oftrainfont72..75."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def compile_train(prior,source):
 c=json.loads((R/'extracted/graphics/train_sign_001/consumer.json').read_text('utf-8'));assert c['status']=='PASS_CONSUMER_AND_RGB';font=bytearray(source[0x32010:0x33010]);assert font==prior[0x52010:0x53010]
 atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);glyphs={};owned=[];labels=[]
 for z in c['labels']:
  text=z['ko_draft'];w=z['width'];im=Image.new('L',(w,8),2);x=(w-len(text)*8)//2;assert x>=0
  for i,char in enumerate(text):
   n=ord(char)-0xac00;assert 0<=n<11172;a=n%64*8;b=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127)for v in atlas.crop((a,b,a+8,b+8)).get_flattened_data()];ttf=Image.new('L',(8,8));ImageDraw.Draw(ttf).text((0,-1),char,font=face,fill=255);assert bits==[int(v>127)for v in ttf.get_flattened_data()]and any(bits)and not any(bits[56:]);glyphs[char]=bits
   for yy in range(7):
    for xx in range(8):
     if bits[yy*8+xx]:im.putpixel((x+i*8+xx,yy+1),1)
  for i,code in enumerate(z['tile_codes']):
   assert code not in owned;owned.append(code);font[code*16:(code+1)*16]=encode(bytes(im.crop((i*8,0,i*8+8,8)).get_flattened_data()))
  labels.append({**z,'status':'draft','Hangul_origin':[x,1],'indices_hex':bytes(im.get_flattened_data()).hex()})
 assert len(owned)==10 and len(glyphs)==8
 for code in range(256):
  if code not in owned:assert font[code*16:(code+1)*16]==source[0x32010+code*16:0x32020+code*16]
 plan={'work':51,'prior_build':'042','labels':labels,'Hangul_unique':8,'owned_tile_codes':owned,'original_font_range':[0x32010,0x33010],'new_font_range':[0x76010,0x77010],'new_font_banks':[216,217,218,219],'font_hex':font.hex(),'font_sha256':hashlib.sha256(font).hexdigest(),'producer':{'canonical_immediates':[0x3fbff,0x3fc08],'old':[72,74],'new':[216,218],'instruction_cycles_unchanged':True},'CHR_KiB':224,'padding220_223_zero_range':[0x77010,0x78010],'original_fixed_copy_and_original_CHR_prior_fonts_emblem_all_other_tiles_unchanged':True,'scope':'Three trainbitmap captions Korean draft, diagnosednativeIRQconsumer; runtimepending'}
 p=R/'workspace/translation/train_sign_graphics_plan_001.json';payload=json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
 if p.exists():assert p.read_text('utf-8')==payload
 else:p.write_text(payload,encoding='utf-8')
 return plan
