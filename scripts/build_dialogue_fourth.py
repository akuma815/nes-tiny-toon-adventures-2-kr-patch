"""Source-guarded fourth intro development page; preserve verified012 components."""
import argparse,csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from asm6502 import assemble,verify_profile
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode,decode
from verify_dialogue_home import reader
from verify_dialogue_fourth_hooks import compare,irq
ROOT=Path(__file__).resolve().parents[1]
PRIOR_SHA='c516074626df8890900f8c2db532ae9d844aaeb6c775c5f17d53d5d55bea992a'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);z=ap.parse_args()
 m=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256'] and len(source)==0x40010
 prior_dir=ROOT/'build/dialogue_kr_poc_012';prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==PRIOR_SHA
 writes=json.loads((prior_dir/'expected_writes.json').read_text('utf-8'));check=bytearray(source)
 for w in writes:
  p=w['file_offset'];n=w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);check[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(check)==prior
 backup=(ROOT/'backups/translation/text_ja_before_fourth_001.csv').read_bytes();assert sha(backup)=='ac801c8b980a2298cccc3108a14e03c64df2d959fe3eb8ffc48fe35777ebd2b9'
 before=list(csv.DictReader(backup.decode('utf-8-sig').splitlines()));rows=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')))
 # splitlines would destroy embedded CSV newlines: use a newline-preserving stream.
 import io
 before=list(csv.DictReader(io.StringIO(backup.decode('utf-8-sig'))));assert len(before)==len(rows)==54
 for x,y in zip(before,rows):
  for k in x:
   if x['entry_id']=='MAIN_05665' and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k],(x['entry_id'],k)
 row=next(x for x in rows if x['entry_id']=='MAIN_05665');text=row['translation_ko'];assert row['status']=='draft' and text=='버스터 바니의 집에\n편지 한 통이 도착했어'
 assert row['raw_hex']==source[0x5665:0x568b].hex(' ').upper() and sum(x['status']=='draft' for x in rows)==5
 chars=list(dict.fromkeys(c for c in text if c not in ' \n'));mapping={' ':0x7a,**dict(zip(chars,range(1,len(chars)+1)))}
 fontdir=ROOT/'workspace/fonts/galmuri7_8x8';png=fontdir/'Galmuri7_8x8.png';ttf=fontdir/'Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 sheet=Image.open(png).convert('RGBA');font=ImageFont.truetype(str(ttf),8);fonts=bytearray(source[0x36810:0x37010]);glyphs=[]
 macro_codes=list(source[0x61c3:0x61c8]);assert macro_codes==[0x4d,0x67,0x40,0x43,0x66]
 for c in [0x7a,*macro_codes]:fonts[c*16:(c+1)*16]=bytes(16)
 for c in chars:
  assert '\uac00'<=c<='\ud7a3';i=ord(c)-0xac00;x=i%64*8;y=i//64*8
  bits=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];assert any(bits)
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=font,fill=255);assert bits==[int(v>127) for v in im.get_flattened_data()]
  raw=encode(bytes(v*2 for v in bits));assert decode(raw)==bytes(v*2 for v in bits);code=mapping[c];assert code not in macro_codes
  fonts[code*16:(code+1)*16]=raw;glyphs.append({'char':c,'code':code,'chr_hex':raw.hex(),'atlas_xy':[x,y]})
 lines=text.split('\n');first=[mapping[c] for c in lines[0]]+[0x7a]*(15-len(lines[0]));first[lines[0].index(' ')]=0
 second=[0x7a]*2+[mapping[c] for c in lines[1]]+[0x7a]*2;second[2+lines[1].index(' ')]=0
 body=bytes([0,0,0x81]+first+[0xfe,0xfd,4]+second+[0xff]);assert len(body)==38 and body[18:21]==bytes.fromhex('fe fd 04') and body[-1]==255
 assert body.count(0)==source[0x5665:0x568b].count(0)==4
 asm=ROOT/'workspace/asm/dialogue_page_font_003.asm';helper_code,listing,symbols=assemble(asm.read_text('utf-8'),0x95f9);assert 0x95f9+len(helper_code)<=0x9700
 init,init_listing,_=assemble('PHP\n LDA $2B\n PHA\n LDA #$02\n JSR $FDD3\n JSR @page_init\n PLA\n STA $2B\n LDA $06CE\n PLP\n LDY #$00\n RTS',0x9430,symbols);init=init.ljust(25,b'\xea');assert len(init)==25
 setup,setup_listing,_=assemble('PHP\n LDA $2B\n PHA\n LDA #$02\n JSR $FDD3\n JSR @intro_setup\n PLA\n STA $2B\n PLP\n LDA #$01\n LDY #$FF\n CLC\n CLV\n INC $06DE\n RTS',0x8e88,symbols);setup=setup.ljust(27,b'\xea');assert len(setup)==27
 font_table=bytearray([0x5a]*256);selections={0x95f9:0x80,0x9615:0x84,0x963d:0x86,0x9655:0x88}
 for slot in range(48):
  ptr=int.from_bytes(source[0x55a9+2*slot:0x55ab+2*slot],'little');font_table[slot*2]=selections.get(ptr,0x5a)
 output=bytearray(prior);output[5]=0x12
 # Clear only private old helper code; every canonical native text/macro remains.
 helper=bytearray(prior[0x4010:0x6010]);old_len=json.loads((prior_dir/'build_report.json').read_text('utf-8'))['helper_code_bytes'];helper[0x15f9:0x15f9+old_len]=source[0x5609:0x5609+old_len]
 helper[0x15f9:0x15f9+len(helper_code)]=helper_code;helper[0x1700:0x1800]=font_table;helper[0x1430:0x1449]=init;helper[0xe88:0xea3]=setup
 output[0x4010:0x6010]=helper;output[0x25440:0x25459]=init;output[0x24e98:0x24eb3]=setup;output[0x25665:0x2568b]=body
 output.extend(fonts+bytes(0x1800));assert len(output)==0x64010 and output[:6]==bytes.fromhex('4e45531a1012')
 assert output[0x261b1:0x261ff]==source[0x61b1:0x61ff] # All native macro pointers and payloads.
 assert output[0x40010:0x62010]==prior[0x40010:0x62010] and output[0x3fb97:0x3fbe3]==prior[0x3fb97:0x3fbe3]
 # Compose one nonoverlapping immutable-source transaction per prior ownership range.
 for w in writes:
  p,n=w['file_offset'],w['length']
  if p==0x20010:n=len(output)-p;w['length']=n
  w['final_hex']=bytes(output[p:p+n]).hex()
 owned=set();reconstructed=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region
  assert source[p:p+n]==bytes.fromhex(w['expected_hex']);reconstructed[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(reconstructed)==output
 view=bytearray(source);view[0x4010:0x8010]=output[0x24010:0x28010];old=reader(source,0x9655);new=reader(view,0x9655);assert len(old)==len(new)
 assert all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(old,new)),(old,new)
 for initial in (0,1,0x5a,0x80,0x84,0x86,0x88,0xff):
  for slot in range(48):
   ptr=int.from_bytes(source[0x55a9+2*slot:0x55ab+2*slot],'little');delta,selected=compare(prior,output,0x9417,slot,0,0x34,0,initial);assert delta==0 and selected==selections.get(ptr,0x5a),(slot,delta,selected)
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 changed={i for i,(a,b) in enumerate(zip(source,output)) if a!=b}|set(range(len(source),len(output)));assert changed<=owned
 out=z.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False)
 (out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 mapping_info={'text':text,'mapping':mapping,'glyphs':glyphs,'body_hex':body.hex(' '),'blank_macro_codes':macro_codes,'macro_policy':'Original81 expansion five tiles blanked only in font136/137; centered inline Korean name; no global macro edit','layout':[{'native_tiles':22,'leading_blanks':7,'text_tiles':10},{'native_tiles':20,'leading_blanks':6,'text_tiles':12}]}
 report={'source_sha256':sha(source),'prior_adopted_sha256':PRIOR_SHA,'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','PRG_KiB':256,'CHR_KiB':144,'csv_sha256':sha((ROOT/'workspace/translation/text_ja.csv').read_bytes()),'asm_sha256':sha(asm.read_bytes()),'helper_code_bytes':len(helper_code),'font_table_CPU':0x9700,'fourth_font_banks':[136,137],'fourth_font_file_range':[0x62010,0x62810],'unused_CHR_padding_range':[0x62810,0x64010],'fourth_glyph_count':len(chars),'native_reader_calls':len(new),'native_reader_cycles':sum(x['cycles'] for x in new),'native_reader_per_call_cycles_equal':True,'all48_page_cycles_equal_prior012':True,'entry_ids':['MAIN_05609','MAIN_05625','MAIN_0564D','MAIN_05665','MAIN_05741'],'expected_writes':len(writes),'whole_diff_bytes':len(changed),'runtime':'NOT YET RUN; consult separate validation','scope':'Title003 + four intro paragraphs and home draft; five draft source units, original90/91 fallback for other native pages; development only, no full playthrough'}
 for name,data in [('expected_writes.json',writes),('fourth_glyph_mapping.json',mapping_info),('asm_listing.json',{'isa_profile':verify_profile(),'helper':listing,'symbols':symbols,'init_bootstrap':init_listing,'setup_bootstrap':setup_listing,'font_table_hex':font_table.hex()}),('build_report.json',report)]:
  (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('page_font_used.asm',asm),('font_irq_used.asm',ROOT/'workspace/asm/dialogue_font_irq_001.asm'),('builder_used.py',Path(__file__)),('asm6502_used.py',ROOT/'scripts/asm6502.py')]:
  (out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
