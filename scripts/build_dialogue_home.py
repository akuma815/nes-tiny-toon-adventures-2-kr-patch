"""Immutable-source title003 + first paragraph002 + independently selected home font PoC."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import encode,decode
from build_dialogue_poc import FONT_SHA,TTF_SHA
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='7261596d059e50afafaba12252c6b41320f9f4c18190e53a82e528a421323598'
POOL=[0x17,0x1e,0x21,0x36,0x38,0x3e,0x41,0x42,0x45,0x4a,0x54,0x62,0x69,0x6f]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 m=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256']
 base_dir=ROOT/'build/dialogue_kr_poc_002';base=(base_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(base)==BASE_SHA
 writes=json.loads((base_dir/'expected_writes.json').read_text('utf-8'))
 check=bytearray(source)
 for w in writes:
  p=w['file_offset'];n=w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);check[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(check)==base
 csv_path=ROOT/'workspace/translation/text_ja.csv';rows=list(csv.DictReader(csv_path.open(encoding='utf-8-sig',newline='')))
 row=next(v for v in rows if v['entry_id']=='MAIN_05741');text=row['translation_ko'];assert row['status']=='draft' and text=='자, 어디로 갈까?'
 assert row['raw_hex']==source[0x5741:0x574d].hex(' ').upper()
 catalog=json.loads((ROOT/'extracted/text/table_20261004_001/text_tokens.json').read_text('utf-8'))
 used={int(t['raw_hex'],16) for u in catalog['units'] for t in u['tokens'] if t['name']=='tile'}
 assert not set(POOL+[0x7a])&used
 fontdir=ROOT/'workspace/fonts/galmuri7_8x8';png=fontdir/'Galmuri7_8x8.png';ttf=fontdir/'Galmuri7.ttf'
 assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 sheet=Image.open(png).convert('RGBA');font=ImageFont.truetype(str(ttf),8)
 fonts=bytearray(source[0x36810:0x37010]);fonts[0x7a*16:0x7b*16]=bytes(16)
 chars=list(dict.fromkeys(c for c in text if c not in ' ?'));assert len(chars)<=len(POOL)
 mapping={' ':0x7a,'?':0x6b,**dict(zip(chars,POOL))};glyphs=[]
 for c in chars:
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=font,fill=255);bits=[int(v>127) for v in im.get_flattened_data()]
  assert any(bits)
  if '\uac00'<=c<='\ud7a3':
   i=ord(c)-0xac00;x=i%64*8;y=i//64*8
   atlas=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()]
   assert bits==atlas;provider='verified Galmuri7_8x8 atlas'
  else:
   assert c==',';provider='explicit Galmuri7.ttf punctuation raster at (0,-1); no fallback'
  raw=encode(bytes(v*2 for v in bits));assert decode(raw)==bytes(v*2 for v in bits)
  code=mapping[c];fonts[code*16:(code+1)*16]=raw;glyphs.append({'char':c,'code':code,'chr_hex':raw.hex(),'provider':provider})
 assert all(fonts[c*16:(c+1)*16]==source[0x36810+c*16:0x36810+(c+1)*16] for c in used)
 # Keep one native literal-zero branch; use a nonzero blank for the other space/padding.
 body=bytearray(mapping[c] for c in text);body[text.index(' ')]=0
 body.extend([0x7a]*(11-len(body)));body.append(0xff)
 assert len(body)==12 and body.count(0)==1 and len(text)==10
 # Home IRQ uses profile 06EA=0: FB34 -> C6 -> LDX C6 at FB1F.
 # Change the table value, preserving every executed instruction and raster delay.
 assert source[0x1fb44:0x1fb4a]==bytes.fromhex('5A 3A 5A 66 5A 74')
 for owner,p,final in [('home_profile0_font_130_131',0x1fb44,b'\x82'),('MAIN_05741_fixed_slot',0x5741,bytes(body))]:
  writes.append({'owner':owner,'file_offset':p,'length':len(final),'expected_hex':source[p:p+len(final)].hex(),'final_hex':final.hex()})
 tail=next(w for w in writes if w.get('kind')=='append');payload=bytearray.fromhex(tail['final_hex'])
 assert payload[0x800:]==bytes(0x1800);payload[0x800:0x1000]=fonts;tail['final_hex']=payload.hex();tail['owner']='intro128_129_home130_131_fonts_and_padding'
 owned=set();output=bytearray(source)
 for w in writes:
  p=w['file_offset'];n=w['length'];region=set(range(p,p+n));assert not owned&region;owned|=region
  assert source[p:p+n]==bytes.fromhex(w['expected_hex'])
  if w.get('kind')=='append':assert p==len(source) and w['expected_source_size']==len(source)
  output[p:p+n]=bytes.fromhex(w['final_hex'])
 diffs={i for i,(x,y) in enumerate(zip(source,output)) if x!=y}|set(range(len(source),len(output)));assert diffs<=owned and len(output)==len(base)
 delta={i for i,(x,y) in enumerate(zip(base,output)) if x!=y};assert delta<=set(range(0x5741,0x574d))|{0x1fb44}|set(range(0x40810,0x41010))
 assert output[0x40010:0x40810]==base[0x40010:0x40810] and output[0x20010:0x40010]==base[0x20010:0x40010]
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False)
 (out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 (out/'expected_writes.json').write_text(json.dumps(writes,indent=2)+'\n',encoding='utf-8')
 (out/'home_glyph_mapping.json').write_text(json.dumps({'mapping':mapping,'glyphs':glyphs,'body_hex':body.hex(' '),'visible_text':text,'font_banks':[130,131]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report={'source_sha256':sha(source),'base_sha256':BASE_SHA,'csv_sha256':sha(csv_path.read_bytes()),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','entry_ids':['MAIN_05609','MAIN_05741'],'home_text':text,'home_glyph_count':len(chars),'home_font_banks':[130,131],'home_font_file_range':[0x40810,0x41010],'expected_write_count':len(writes),'changed_bytes_including_append':len(diffs),'changed_bytes_from002':len(delta),'home_body_bytes':len(body),'font_png_sha256':FONT_SHA,'ttf_sha256':TTF_SHA,'native_home_profile_table_file_offset':0x1fb44,'original_chr_and_first_poc_font_preserved':True,'policy':'Two explicit draft units admitted to development build; not release eligible','runtime':'NOT YET RUN','scope':'Title003 + first paragraph002 + home profile0 idle prompt. Per-paragraph dynamic switching not implemented.'}
 (out/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
