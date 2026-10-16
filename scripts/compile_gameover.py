"""Native gameover labels,font210/211 and isolated122/123clone212/213."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import encode
from convert_gameover_art import convert
R=Path(__file__).resolve().parents[1]
def compile_gameover(prior,source):
 survey=json.loads((R/'extracted/graphics/gameover_001/consumer.json').read_text('utf-8'));labels=survey['labels'];chars=list(dict.fromkeys(c for p in labels for c in p['translation_ko'] if 0xac00<=ord(c)<=0xd7a3));assert len(chars)==8;mapping={' ':0,'?':0x65,'!':0x66,'“':0x68,'”':0x69,**{c:i+1 for i,c in enumerate(chars)}};font=bytearray(prior[0x5f010:0x5f810]);assert font==source[0x3f010:0x3f810];atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);glyphs=[]
 for char in chars:
  n=ord(char)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),char,font=face,fill=255);assert any(bits) and not any(bits[56:]) and bits==[int(v>127) for v in im.get_flattened_data()];code=mapping[char];raw=encode(bytes(2*v for v in bits));font[code*16:(code+1)*16]=raw;glyphs.append({'char':char,'code':code,'chr_hex':raw.hex()})
 result=[]
 for p in labels:
  text=p['translation_ko'];desired=text.center(p['length']) if p['source']=='CONTINUE ?' else text.ljust(p['length']);assert len(desired)==p['length'];result.append({**p,'desired_padded':desired,'body_hex':bytes(mapping[c] for c in desired).hex(),'status':'draft'})
 for code in range(128):
  if code not in range(1,len(chars)+1):assert font[code*16:(code+1)*16]==prior[0x5f010+code*16:0x5f020+code*16]
 art,conversion=convert();high=bytearray(prior[0x5e810:0x5f010]);assert high==source[0x3e810:0x3f010];high[1024:]=art;plan={'work':48,'prior_build':'041','labels':result,'literal_blocks':3,'literal_cells':21,'Hangul_unique':8,'mapping':mapping,'glyphs':glyphs,'font210_range':[0x74810,0x75010],'font210_hex':font.hex(),'font212_range':[0x75010,0x75810],'font212_hex':high.hex(),'conversion':conversion,'producer':{'expanded_immediates':[0x2d3bd,0x2d3c1],'low_compatibility_immediates':[0xd3bd,0xd3c1],'old':[124,122],'new':[210,212]},'native_logo_codes_NT_geometry_and_literal_lengths_preserved':True,'CHR_KiB':216,'scope':'Generated게임 오버 andnativecontinue3captiondraft; originalfonts124/122 retained; runtimepending'}
 (R/'workspace/translation/gameover_graphics_plan_001.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return plan
