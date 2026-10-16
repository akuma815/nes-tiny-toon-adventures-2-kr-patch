"""Unadopted second-intro font/data packet and CPU budget; never emits or patches a ROM."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode
from verify_dialogue_home import reader
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 m=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256']
 proposed='어느 날 마을 변두리에\n커다란 놀이공원이 생겼어'
 chars=list(dict.fromkeys(c for c in proposed if c not in ' \n'));mapping={' ':0x7a,**dict(zip(chars,range(1,len(chars)+1)))}
 assert len(chars)<0x6b
 fdir=ROOT/'workspace/fonts/galmuri7_8x8';png=fdir/'Galmuri7_8x8.png';ttf=fdir/'Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 sheet=Image.open(png).convert('RGBA');font=ImageFont.truetype(str(ttf),8);fonts=bytearray(source[0x36810:0x37010]);fonts[0x7a*16:0x7b*16]=bytes(16);glyphs=[]
 for c in chars:
  assert '\uac00'<=c<='\ud7a3';i=ord(c)-0xac00;x=i%64*8;y=i//64*8
  bits=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];assert any(bits)
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=font,fill=255);assert bits==[int(v>127) for v in im.get_flattened_data()]
  raw=encode(bytes(b*2 for b in bits));code=mapping[c];fonts[code*16:(code+1)*16]=raw;glyphs.append({'char':c,'code':code,'chr_hex':raw.hex()})
 body=bytearray();layout=[]
 for i,line in enumerate(proposed.split('\n')):
  prefix=(3,4)[i];expanded=(21,20)[i];native_zero_count=(2,1)[i];pad=(24-len(line))//2;lead=pad-prefix;trail=expanded-pad-len(line)
  assert lead>=0 and trail>=0
  values=[mapping[c] for c in line];spaces=[j for j,c in enumerate(line) if c==' '];assert len(spaces)>=native_zero_count
  for j in spaces[:native_zero_count]:values[j]=0
  tokens=[0xfd,prefix]+[0x7a]*lead+values+[0x7a]*trail+[0xfe if i==0 else 0xff];body.extend(tokens)
  layout.append({'text':line,'native_prefix':prefix,'literal_zero_count':native_zero_count,'expanded_tiles':expanded,'leading_blanks':pad,'extra_literal_leading':lead,'trailing_blanks':trail})
 assert len(body)==40 and body[20]==0xfe and body[39]==0xff
 trial=bytearray(source);trial[0x5625:0x564d]=body
 old=reader(source,0x9615);new=reader(trial,0x9615);assert len(old)==len(new)
 for x,y in zip(old,new):assert all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')),(x,y)
 out=a.output.resolve();out.relative_to((ROOT/'work/dialogue_font').resolve());out.mkdir(parents=True,exist_ok=False)
 (out/'second_intro_stream.bin').write_bytes(body);(out/'second_intro_font.bin').write_bytes(fonts)
 result={'status':'UNADOPTED preparation; no ROM emitted or patched','entry_id':'MAIN_05625','source_sha256':sha(source),'proposed_translation':proposed,'translation_ssot_updated':False,'glyph_count':len(chars),'mapping':mapping,'glyphs':glyphs,'body_hex':body.hex(' '),'body_sha256':sha(body),'font_sha256':sha(fonts),'candidate_font_banks':[132,133],'layout':layout,'native_reader_calls':len(old),'total_reader_cycles':sum(x['cycles'] for x in old),'per_call_cycles_and_cursors_equal':True,'original_calls':old,'proposed_calls':new,'consumer_constraint':f'Codes 01..{len(chars):02X} replace active Japanese glyphs in this cloned pair. Select only after verified intro clear; restore another pair before any other page/consumer. No runtime font-switch validation yet.'}
 (out/'supply_plan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:result[k] for k in ('status','glyph_count','native_reader_calls','total_reader_cycles','per_call_cycles_and_cursors_equal')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
