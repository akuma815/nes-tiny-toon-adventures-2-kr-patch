"""Immutable-source page font latch, second paragraph, and preserved title/home in expanded PRG."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from asm6502 import assemble,verify_profile
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode,decode
from verify_dialogue_home import reader
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA='761f2495295dc07b1648a5aa0d1dbf85139d67b4e6962639d34e0688989ede3a'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 m=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256'] and len(source)==0x40010
 base_dir=ROOT/'build/dialogue_kr_poc_003';base=(base_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(base)==BASE_SHA
 old_writes=json.loads((base_dir/'expected_writes.json').read_text('utf-8'));check=bytearray(source)
 for w in old_writes:
  p=w['file_offset'];n=w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);check[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(check)==base
 rows=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')))
 row=next(x for x in rows if x['entry_id']=='MAIN_05625');text=row['translation_ko'];assert row['status']=='draft' and text=='어느 날 마을 변두리에\n커다란 놀이공원이 생겼어'
 assert row['raw_hex']==source[0x5625:0x564d].hex(' ').upper()
 assert sum(x['status']=='draft' for x in rows)==3
 chars=list(dict.fromkeys(c for c in text if c not in ' \n'));mapping={' ':0x7a,**dict(zip(chars,range(1,len(chars)+1)))};assert len(chars)==18
 fontdir=ROOT/'workspace/fonts/galmuri7_8x8';png=fontdir/'Galmuri7_8x8.png';ttf=fontdir/'Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 sheet=Image.open(png).convert('RGBA');font=ImageFont.truetype(str(ttf),8);fonts=bytearray(source[0x36810:0x37010]);fonts[0x7a*16:0x7b*16]=bytes(16);glyphs=[]
 for c in chars:
  assert '\uac00'<=c<='\ud7a3';i=ord(c)-0xac00;x=i%64*8;y=i//64*8
  bits=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];assert any(bits)
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=font,fill=255);assert bits==[int(v>127) for v in im.get_flattened_data()]
  raw=encode(bytes(v*2 for v in bits));assert decode(raw)==bytes(v*2 for v in bits);code=mapping[c];fonts[code*16:(code+1)*16]=raw;glyphs.append({'char':c,'code':code,'chr_hex':raw.hex(),'atlas_xy':[x,y]})
 body=bytearray();layout=[]
 for i,line in enumerate(text.split('\n')):
  prefix=(3,4)[i];expanded=(21,20)[i];pad=(24-len(line))//2;lead=pad-prefix;trail=expanded-pad-len(line);assert lead>=0 and trail>=0
  values=[mapping[c] for c in line];spaces=[j for j,c in enumerate(line) if c==' '];zero_count=(2,1)[i];assert len(spaces)>=zero_count
  for j in spaces[:zero_count]:values[j]=0
  body.extend([0xfd,prefix]+[0x7a]*lead+values+[0x7a]*trail+[0xfe if i==0 else 0xff]);layout.append({'text':line,'leading_blanks':pad,'expanded_tiles':expanded,'literal_zero_count':zero_count})
 assert len(body)==40 and body[20]==0xfe and body[39]==0xff
 asm=ROOT/'workspace/asm/dialogue_page_font_001.asm';code,listing,symbols=assemble(asm.read_text('utf-8'),0x95f9)
 assert len(code)<=0xa000-0x95f9 # Helper-only data; native bank18 retains every original string.
 init_text='''PHP
 LDA $2B
 PHA
 LDA #$02
JSR $FDD3
JSR @page_init
 PLA
 STA $2B
 LDA $06CE
PLP
LDY #$00
RTS'''
 init,init_listing,_=assemble(init_text,0x9430,symbols);assert len(init)<=25;init+=b'\xea'*(25-len(init))
 setup_text='''PHP
 LDA $2B
 PHA
 LDA #$02
JSR $FDD3
JSR @intro_setup
PLA
 STA $2B
PLP
LDA #$01
 LDY #$FF
 CLC
 CLV
INC $06DE
RTS'''
 setup,setup_listing,_=assemble(setup_text,0x8e88,symbols);assert len(setup)<=27;setup+=b'\xea'*(27-len(setup))
 assert source[0x5440:0x5459]==bytes.fromhex('B9 99 95 8D CD 06 85 06 B9 9A 95 8D CE 06 85 07 A0 00 8C C3 06 8C C4 06 60')
 assert source[0x4e98:0x4eb3]==bytes.fromhex('20 16 8E 20 1D 8E 20 00 8E 8D 18 06 8D C3 06 8D 0F 04 A9 01 8D CF 06 EE DE 06 60')
 # Construct each extension component before one registered immutable-source application.
 helper=bytearray(base[0x4010:0x6010]);assert helper[0]==0x32;helper[0]=2;helper[0x15f9:0x15f9+len(code)]=code
 # Bank switching resumes inside the bootstrap in the newly mapped bank.
 # Both copies must have identical instructions throughout that continuation.
 helper[0x9430-0x8000:0x9449-0x8000]=init
 helper[0x8e88-0x8000:0x8ea3-0x8000]=setup
 extension_prg=bytearray(base[0x10:0x20010])
 extension_prg[0x5440-0x10:0x5459-0x10]=init
 extension_prg[0x4e98-0x10:0x4eb3-0x10]=setup
 extension_prg[0x5625-0x10:0x564d-0x10]=body
 assert helper[0x1430:0x1449]==extension_prg[0x5430:0x5449]
 assert helper[0xe88:0xea3]==extension_prg[0x4e88:0x4ea3]
 irq_asm=ROOT/'workspace/asm/dialogue_font_irq_001.asm'
 irq,irq_listing,_=assemble(irq_asm.read_text('utf-8'),0xfb97);assert len(irq)==0xfbe3-0xfb97
 fixed=bytearray(base[0x1e010:0x20010]);assert fixed[0x1bce:0x1bd7]==bytes.fromhex('A2 80 8E 00 A0 E8 8E 08 A0');fixed[0x1b97:0x1be3]=irq
 extension_prg[-0x2000:]=fixed
 chr_payload=bytearray(base[0x20010:]);assert len(chr_payload)==0x22000 and chr_payload[0x21000:0x21800]==bytes(0x800);chr_payload[0x21000:0x21800]=fonts
 writes=[]
 for w in old_writes:
  if w['file_offset']<0x20010 and w.get('kind')!='append' and not (0x4010<=w['file_offset']<0x6010):writes.append(w.copy())
 # Header PRG size is one composed header write, not overlapping with the previous header.
 writes.append({'owner':'PRG_128_to256_KiB','file_offset':4,'length':1,'expected_hex':source[4:5].hex(),'final_hex':'10'})
 def replace(owner,p,final):
  assert not any(set(range(p,p+len(final)))&set(range(w['file_offset'],w['file_offset']+w['length'])) for w in writes)
  writes.append({'owner':owner,'file_offset':p,'length':len(final),'expected_hex':source[p:p+len(final)].hex(),'final_hex':final.hex()})
 replace('helper_bank2_with_original_data_retained_in_native_bank18',0x4010,bytes(helper))
 relocated=bytes(extension_prg)+bytes(chr_payload)
 writes.append({'owner':'native_PRG16_to31_mirrors_bank18_bootstraps_31_fixed_and_relocated_CHR','file_offset':0x20010,'length':len(relocated),'expected_hex':source[0x20010:].hex(),'final_hex':relocated.hex(),'composition':'16 added PRG8K mirrors; encoded30..3F resolves16..31; native32/33 resolves18/19; fixed31. CHR shifted +20000, preserved first/home fonts, generated second132/133. Helper uses bank02/03 only during bounded init.','expected_source_size':len(source)})
 owned=set();output=bytearray(source)
 for w in writes:
  p=w['file_offset'];n=w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region
  assert source[p:min(p+n,len(source))]==bytes.fromhex(w['expected_hex']);output[p:p+n]=bytes.fromhex(w['final_hex'])
 assert len(output)==0x62010 and output[:4]==source[:4] and output[4:6]==bytes.fromhex('10 11')
 assert output[0x40010:0x60010]==base[0x20010:0x40010]
 assert output[0x60010:0x61010]==base[0x40010:0x41010]
 assert output[0x61010:0x61810]==fonts
 assert output[0x1e168:0x1e258]==source[0x1e168:0x1e258] and output[0x3e168:0x3e258]==source[0x1e168:0x1e258]
 changed={i for i,(x,y) in enumerate(zip(source,output)) if x!=y}|set(range(len(source),len(output)));assert changed<=owned
 # Native reader stays in original bank2/3. Test the new text independently of mapper helpers.
 cpu_view=bytearray(source);cpu_view[0x4010:0x8010]=output[0x24010:0x28010]
 old=reader(source,0x9615);new=reader(cpu_view,0x9615);assert len(old)==len(new)
 for x,y in zip(old,new):assert all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor'))
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False)
 (out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 for name,p in [('page_font_used.asm',asm),('font_irq_used.asm',irq_asm),('builder_used.py',Path(__file__)),('asm6502_used.py',ROOT/'scripts/asm6502.py')]:
  (out/name).write_bytes(p.read_bytes())
 for name,value in [('expected_writes.json',writes),('second_glyph_mapping.json',{'mapping':mapping,'glyphs':glyphs,'body_hex':body.hex(' '),'layout':layout}),('asm_listing.json',{'isa_profile':verify_profile(),'helper_origin':0x95f9,'helper_bank':2,'native_bank':18,'symbols':symbols,'helper':listing,'init_bootstrap':init_listing,'setup_bootstrap':setup_listing,'font_irq':irq_listing})]:
  (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report={'source_sha256':sha(source),'base_sha256':BASE_SHA,'csv_sha256':sha((ROOT/'workspace/translation/text_ja.csv').read_bytes()),'asm_sha256':sha(asm.read_bytes()),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','PRG_KiB':256,'CHR_KiB':136,'entry_ids':['MAIN_05609','MAIN_05625','MAIN_05741'],'second_text':text,'second_glyph_count':len(chars),'second_font_banks':[132,133],'second_font_file_range':[0x61010,0x61810],'helper_bank':2,'native_bank':18,'fixed_bank':31,'helper_code_bytes':len(code),'expected_writes':len(writes),'whole_diff_bytes':len(changed),'native_reader_calls':len(old),'native_reader_cycles':sum(x['cycles'] for x in old),'native_reader_per_call_cycles_equal':True,'policy':'Three explicit draft units admitted only to development build','runtime':'NOT YET RUN','scope':'Title003 + first/second intro paragraphs and home prompt; dynamic font latch only for these two intro pointers; fallback original90/91 for other native pages. No full playthrough.'}
 (out/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
