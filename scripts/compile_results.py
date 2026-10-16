"""Eight native literal blocks, seven Korean captions; unchanged controls/digits."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from title_codec import unpack
from extract_title_png import encode
R=Path(__file__).resolve().parents[1]
def compile_results(prior,source):
 survey=json.loads((R/'extracted/graphics/results_001/consumer.json').read_text('utf-8'));font=bytearray(prior[0x5f010:0x5f810]);assert font==source[0x3f010:0x3f810];chars=list(dict.fromkeys(c for p in survey['labels'] for c in p['translation_ko'] if c not in ' !'));assert len(chars)<=42;mapping={' ':0,'!':0x66,**{c:i+1 for i,c in enumerate(chars)}};atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);glyphs=[]
 for c in chars:
  n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(bits) and bits==[int(v>127) for v in im.get_flattened_data()];raw=encode(bytes(v*2 for v in bits));code=mapping[c];font[code*16:(code+1)*16]=raw;glyphs.append({'char':c,'code':code,'chr_hex':raw.hex()})
 stream=bytearray(prior[0x44a0b:0x44aa5]);assert stream==source[0x24a0b:0x24aa5];labels=[];owned=set()
 for p in survey['labels']:
  n=p['length'];text=p['translation_ko'];desired=(' '+text).ljust(n) if p['source']=='POINTS' else text.center(n);assert len(desired)==n;body=bytes(mapping[c] for c in desired);off=p['offset'];assert stream[off:off+n]==bytes.fromhex(p['source_hex']) and not owned.intersection(range(off,off+n));owned.update(range(off,off+n));stream[off:off+n]=body;labels.append({**p,'desired_padded':desired,'body_hex':body.hex(),'status':'draft'})
 oldnt,oldn=unpack(prior[0x44a0b:0x44aa5]);nt,n=unpack(stream);assert oldn==n==154 and len(nt)==len(oldnt)==1024;allowed={p['NT']+i for p in labels for i in range(p['length'])};assert all(nt[a]==oldnt[a] for a in nt if a not in allowed);assert all(font[c*16:(c+1)*16]==source[0x3f010+c*16:0x3f020+c*16] for c in range(128) if c not in range(1,len(chars)+1));assert font[:16]==bytes(16)
 plan={'work':46,'prior_build':'dialogue_kr_poc_040','labels':labels,'distinct_labels':7,'literal_blocks':8,'font_bank':208,'font_range':[0x74010,0x74810],'font_hex':font.hex(),'mapping':mapping,'glyphs':glyphs,'Hangul_unique':len(chars),'stream_file':0x44a0b,'stream_length':154,'stream_hex':stream.hex(),'compression_controls_NT_addresses_attrs_and_digit_cells_unchanged':True,'producer':{'file':0x3f8e0,'old':124,'new':208},'CHR_size_KiB':216,'scope':'Development draft, sourcefont124 preserved andcloned208; literal lengths andnumeric/sourcecontrols fixed; runtimepending'};(R/'workspace/translation/results_graphics_plan_001.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return plan
