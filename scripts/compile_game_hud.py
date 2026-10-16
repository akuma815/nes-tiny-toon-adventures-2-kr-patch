"""Dedicated HUD clone; seven-row headers, original numbers/hearts/borders."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def compile_hud(prior,source):
 survey=json.loads((R/'extracted/graphics/hud_001/consumer.json').read_text('utf-8'));font=bytearray(prior[0x5f010:0x5f810]);assert font==source[0x3f010:0x3f810];atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);labels=[];used=set()
 for label in survey['labels']:
  codes=label['codes'];text=label['draft_ko'];width=len(codes)*8;assert len(text)*8<=width and not used.intersection(codes);used.update(codes);bits=bytearray([1]*width*8);x0=(width-len(text)*8)//2;glyphs=[]
  for i,c in enumerate(text):
   n=ord(c)-0xac00;x=n%64*8;y=n//64*8;g=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(g) and g==[int(v>127) for v in im.get_flattened_data()] and not any(g[56:]);glyphs.append({'char':c,'bits':''.join(str(v) for v in g)})
   # Headers must fit source rows1..7; body labels retain rows0..6.
   dy=1 if label['source'] in ('LIFE','SCORE','TIME') else 0
   for yy in range(7):
    for xx in range(8):
     if g[yy*8+xx]:bits[(yy+dy)*width+x0+i*8+xx]=label['ink']
  for i,code in enumerate(codes):font[code*16:(code+1)*16]=encode(bytes(bits[y*width+i*8+x] for y in range(8) for x in range(8)))
  labels.append({**label,'glyphs':glyphs,'header_y':dy,'center_x':x0,'status':'draft'})
 for code in range(128):
  if code not in used:assert font[code*16:(code+1)*16]==source[0x3f010+code*16:0x3f020+code*16]
 assert not used.intersection(range(0x70,0x7a)) and 0x33 not in used
 plan={'work':44,'prior_build':'dialogue_kr_poc_039','font_banks':[206,207],'font_range':[0x73810,0x74010],'font_hex':font.hex(),'labels':labels,'changed_codes':sorted(used),'protected':'All other native tiles, dynamic digits70..79, multiply33, hearts, punctuation, borders unchanged','producers':[{'file':0x3fce5,'CPU_immediate':0xfcd5,'old':0x2f,'new':0x0f,'purpose':'fineY2→0; background NT low12 unchanged, gives7 visible header rows and shifts native body2px down'},{'file':0x3fcf9,'CPU_immediate':0xfce9,'old':0x7c,'new':0xce,'purpose':'HUD-only CHR206/207; nextLDX7E restoresX/NZ before return'}],'hardware_source':'https://www.nesdev.org/wiki/PPU_scrolling','scope':'Development draft pending runtime, per-ride split geometry, protected pixels, digit values and exact timing'}
 (R/'workspace/translation/game_hud_plan_001.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return plan
