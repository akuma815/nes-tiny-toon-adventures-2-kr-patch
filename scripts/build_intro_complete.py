"""Finish known intro pages05..09 with native shape and immutable-source transactions."""
import argparse,csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode,decode
from verify_dialogue_home import reader
from verify_dialogue_fourth_hooks import compare,irq
from asm6502 import verify_profile
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads((ROOT/p).read_text('utf-8'))
def split_source(raw):
 lines=[];tokens=[];pos=0;i=0
 while i<len(raw):
  c=raw[i]
  if c in (0xfe,0xff):lines.append((tokens,pos,c));tokens=[];pos=0;i+=1
  elif c==0xfd:
   n=raw[i+1];tokens.append({'kind':'spaces','position':pos,'bytes':[c,n],'count':n});pos+=n;i+=2
  elif c==0x81:
   tokens.append({'kind':'macro','position':pos,'bytes':[c],'codes':[0x4d,0x67,0x40,0x43,0x66],'count':5});pos+=5;i+=1
  else:
   assert c<0x7f,hex(c);tokens.append({'kind':'glyph','position':pos,'bytes':[c],'count':1});pos+=1;i+=1
 assert not tokens and lines[-1][2]==255
 return lines
def page(source,profile,plan,png,ttf):
 start,end=profile['file_offset'],profile['end_exclusive'];raw=source[start:end];assert sha(raw)==profile['source_raw_sha256']
 lines=split_source(raw);texts=profile['text'].split('\n');assert len(lines)==len(texts)==len(profile['padding'])
 desired=[];forced={};macro_codes=set()
 for (tokens,count,term),text,pad in zip(lines,texts,profile['padding']):
  assert pad+len(text)<=count<=24;v=' '*pad+text+' '*(count-pad-len(text));desired.append(v)
  for t in tokens:
   p=t['position']
   if t['kind']=='spaces':assert v[p:p+t['count']]==' '*t['count']
   elif t['kind']=='macro':
    for code,ch in zip(t['codes'],v[p:p+5]):
     assert code not in forced or forced[code]==ch,(code,ch,forced);forced[code]=ch;macro_codes.add(code)
 mapping={' ':0x7a,**plan['native_punctuation']}
 for code,ch in forced.items():
  if ch!=' ':assert ch not in mapping or mapping[ch]==code;mapping[ch]=code
 chars=list(dict.fromkeys(c for c in profile['text'] if c!='\n'));pool=[c for c in range(1,0x7a) if c not in macro_codes and c not in mapping.values()]
 for ch in chars:
  if ch not in mapping:mapping[ch]=pool.pop(0)
 glyph_slots={mapping[c]:c for c in chars};glyph_slots.update(forced);glyph_slots[0x7a]=' '
 fonts=bytearray(source[0x36810:0x37010]);sheet=Image.open(png).convert('RGBA');font=ImageFont.truetype(str(ttf),8);glyphs=[]
 for code,ch in sorted(glyph_slots.items()):
  if ch==' ':data=bytes(16);kind='blank'
  elif ch in plan['native_punctuation']:
   assert code==plan['native_punctuation'][ch];data=bytes(fonts[code*16:(code+1)*16]);kind='native punctuation';assert any(data)
  else:
   im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),ch,font=font,fill=255);bits=[int(x>127) for x in im.get_flattened_data()];assert any(bits),ch
   if '\uac00'<=ch<='\ud7a3':
    n=ord(ch)-0xac00;x=n%64*8;y=n//64*8;atlas=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];assert bits==atlas;kind='Hangul atlas and TTF'
   else:assert ch in plan['explicit_TTF_punctuation'];kind='explicit TTF punctuation'
   data=encode(bytes(x*2 for x in bits));assert decode(data)==bytes(x*2 for x in bits)
  fonts[code*16:(code+1)*16]=data;glyphs.append({'code':code,'char':ch,'kind':kind,'chr_hex':data.hex()})
 body=bytearray();layouts=[]
 for (tokens,count,term),v,text in zip(lines,desired,texts):
  literal_count=sum(t['kind']=='glyph' and t['bytes']==[0] for t in tokens);blank_positions=[t['position'] for t in tokens if t['kind']=='glyph' and v[t['position']]==' '];assert len(blank_positions)>=literal_count
  zero_positions=set(blank_positions[:literal_count]);expanded=[]
  for t in tokens:
   p=t['position']
   if t['kind']=='glyph':code=0 if p in zero_positions else mapping[v[p]];body.append(code);expanded.append(code)
   elif t['kind']=='spaces':body.extend(t['bytes']);expanded.extend([0]*t['count'])
   else:body.extend(t['bytes']);expanded.extend(t['codes'])
  body.append(term);layouts.append({'text':text,'expanded_tiles':count,'literal_zero_count':literal_count,'expanded_hex':bytes(expanded).hex(),'desired':v})
 assert len(body)==len(raw)
 original=reader(source,profile['pointer']);view=bytearray(source);view[start:end]=body;modified=reader(view,profile['pointer']);assert len(original)==len(modified)
 assert all(all(a[k]==b[k] for k in ('cycles','cursor','buffer_cursor')) for a,b in zip(original,modified)),profile['entry_id']
 reverse={v:k for k,v in mapping.items()};reverse.update(forced);reverse[0]=' '
 expanded_lines=[];current=[]
 for x in modified:
  if x['value'] in (0xfe,0xff):expanded_lines.append(''.join(reverse[v] for v in current));current=[]
  else:current.append(x['value'])
 assert expanded_lines==desired,(expanded_lines,desired)
 return bytes(body),bytes(fonts),{'profile':profile,'mapping':mapping,'forced_macro_glyphs':forced,'glyphs':glyphs,'body_hex':body.hex(' '),'layout':layouts,'reader_calls':len(modified),'reader_cycles':sum(x['cycles'] for x in modified),'per_call_cycles_cursor_equal':True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);z=ap.parse_args();plan=load('workspace/translation/intro_complete_plan_001.json');manifest=load('manifests/source_rom.json');source=(ROOT/manifest['path']).read_bytes();assert sha(source)==plan['source_sha256']==manifest['sha256']
 prior_dir=ROOT/'build'/plan['prior_build'];prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==plan['prior_ROM_sha256'];writes=json.loads((prior_dir/'expected_writes.json').read_text('utf-8'));model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 backup=(ROOT/'backups/translation/text_ja_before_intro_complete_001.csv').read_bytes();assert sha(backup)==plan['backup_CSV_sha256'];before=list(csv.DictReader(io.StringIO(backup.decode('utf-8-sig'))));csv_bytes=(ROOT/'workspace/translation/text_ja.csv').read_bytes();rows=list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8-sig'))));selected={p['entry_id']:p for p in plan['profiles']};assert len(before)==len(rows)==54
 for x,y in zip(before,rows):
  for k in x:
   if x['entry_id'] in selected and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k],(x['entry_id'],k)
  if x['entry_id'] in selected:assert y['status']=='draft' and y['translation_ko']==selected[x['entry_id']]['text']
 assert sum(x['status']=='draft' for x in rows)==10
 png=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png';ttf=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 output=bytearray(prior);output.extend(bytes(0x66010-len(output)));output[5]=19;pages=[]
 selections={0x95f9:128,0x9615:132,0x963d:134,0x9655:136}
 for p in plan['profiles']:
  body,font,info=page(source,p,plan,png,ttf);start,end=p['file_offset'],p['end_exclusive'];output[start+0x20000:end+0x20000]=body;f=0x40010+p['font_bank']*0x400;output[f:f+0x800]=font;output[0x5710+p['slot']*2]=p['font_bank'];selections[p['pointer']]=p['font_bank'];pages.append(info)
 assert len(output)==0x66010 and output[0x40010:0x62810]==prior[0x40010:0x62810] and output[0x261b1:0x261ff]==source[0x61b1:0x61ff]
 for initial in (0,1,90,128,132,134,136,138,140,142,144,146,255):
  for slot in range(48):
   ptr=int.from_bytes(source[0x55a9+2*slot:0x55ab+2*slot],'little');delta,font=compare(prior,output,0x9417,slot,0,0x34,0,initial);assert delta==0 and font==selections.get(ptr,90)
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 for w in writes:
  p,n=w['file_offset'],w['length']
  if p==5:w['owner']='CHR_128_to152_KiB'
  if p==0x20010:n=len(output)-p;w['length']=n;w['composition']='Original PRG mirrors and CHR relocation retained; intro01..09 and home fonts; unchanged original macros; CHR152KiB with4KiB unused padding.'
  w['final_hex']=output[p:p+n].hex()
 model=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==output
 changed={i for i,(a,b) in enumerate(zip(source,output)) if a!=b}|set(range(len(source),len(output)));assert changed<=owned
 out=z.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 for name,p in [('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('plan_used.json',ROOT/'workspace/translation/intro_complete_plan_001.json'),('page_font_used.asm',ROOT/'workspace/asm/dialogue_page_font_003.asm'),('builder_used.py',Path(__file__)),('asm6502_used.py',ROOT/'scripts/asm6502.py')]:
  (out/name).write_bytes(p.read_bytes())
 report={'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','PRG_KiB':256,'CHR_KiB':152,'csv_sha256':sha(csv_bytes),'plan_sha256':sha((ROOT/'workspace/translation/intro_complete_plan_001.json').read_bytes()),'expected_writes':len(writes),'whole_diff_bytes':len(changed),'CPU_seed_font_cases':624,'all48_page_elapsed_cycles_equal_prior013':True,'native_macro_bytes_preserved':True,'unused_CHR_padding_range':[0x65010,0x66010],'font_banks':[[p['font_bank'],p['font_bank']+1] for p in plan['profiles']],'draft_source_units':10,'untranslated_source_units':44,'scope':'Title003, all9 observed intro paragraphs, home prompt;10 explicit drafts, development only; rest of game unresolved','runtime':'NOT YET RUN; separate report required','ISA':verify_profile()}
 for name,data in [('expected_writes.json',writes),('intro_page_mapping.json',pages),('build_report.json',report)]:
  (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
