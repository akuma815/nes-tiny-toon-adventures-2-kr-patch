"""Eight observed lower-window Korean drafts; other UI keeps native passthrough."""
import argparse,csv,hashlib,io,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from build_dialogue_poc import FONT_SHA,TTF_SHA
from extract_title_png import encode,decode
from verify_dialogue_home import reader
from verify_ui_native_latch_hooks import compare,irq
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
def split(raw,macros,variables):
 lines=[];tokens=[];pos=0;i=0
 while i<len(raw):
  c=raw[i]
  if c in (0xfe,0xff):lines.append((tokens,pos,c));tokens=[];pos=0;i+=1
  elif c==0xfd:
   n=raw[i+1];tokens.append({'kind':'spaces','position':pos,'bytes':[c,n],'count':n});pos+=n;i+=2
  elif c in variables:
   codes=variables[c];tokens.append({'kind':'variable','position':pos,'bytes':[c],'codes':codes,'count':len(codes)});pos+=len(codes);i+=1
  elif c in macros:
   codes=macros[c];tokens.append({'kind':'macro','position':pos,'bytes':[c],'codes':codes,'count':len(codes)});pos+=len(codes);i+=1
  else:assert c<0x7f,hex(c);tokens.append({'kind':'glyph','position':pos,'bytes':[c],'count':1});pos+=1;i+=1
 assert not tokens and lines[-1][2]==255
 return lines
def page(prior,source,p,plan,macrodata,png,ttf):
 start,end=p['source_file_offset'],p['end_exclusive'];raw=prior[start+0x20000:end+0x20000];assert sha(source[start:end])==p['source_raw_sha256']
 from verify_ui_macro_passthrough import state_reader
 # Actual native F8 decimal reader; preserve leading blank00, never synthesize.
 mem=bytearray(65536);mem[0x8000:0xc000]=source[0x4010:0x8010];mem[0x600:0x602]=bytes.fromhex('f8 ff');mem[0x6cd:0x6cf]=(0x600).to_bytes(2,'little');mem[0x7d0:0x7d3]=bytes([3,0,0]);variables={0xf8:[]}
 from verify_dialogue_home import MPU
 c=MPU(memory=mem)
 for call in range(4):
  c.pc=0x937c;c.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');n=0
  while c.pc!=0xc100:c.step();n+=1;assert n<10000
  if c.a==255:break
  variables[0xf8].append(c.a)
 assert variables[0xf8]==[0,0,0x73]
 macros={m['code']:list(bytes.fromhex(m['output_hex']))[:-1] for m in macrodata['macros']};lines=split(raw,macros,variables);texts=p['text'].replace('{variable_F8}','¤¤¤').split('\n');assert len(lines)==len(texts)==len(p['padding']);desired=[];forced={}
 for (tokens,count,term),text,pad in zip(lines,texts,p['padding']):
  assert pad+len(text)<=count<=24,(p['entry_id'],text,count);v=' '*pad+text+' '*(count-pad-len(text));desired.append(v)
  for t in tokens:
   index=t['position']
   if t['kind']=='spaces':assert v[index:index+t['count']]==' '*t['count']
   elif t['kind']=='variable':assert v[index:index+t['count']]=='¤'*t['count']
   elif t['kind']=='macro':
    for code,ch in zip(t['codes'],v[index:index+t['count']]):
     if code==0:assert ch==' ';continue
     assert code not in forced or forced[code]==ch;forced[code]=ch
   elif t['bytes']==[0]:assert v[index]==' ',(p['entry_id'],index)
 mapping={' ':0x7a,**plan['native_punctuation']}
 for code,ch in sorted(forced.items()):
  if ch!=' ':mapping.setdefault(ch,code)
 fixed=set(range(1,43))|set(range(0x41,0x4b))|set(range(0x70,0x7a))|set(plan['native_punctuation'].values())|{0x7a}
 pool=[c for c in range(43,0x7f) if c not in fixed];chars=list(dict.fromkeys(c for c in p['text'].replace('{variable_F8}','') if c!='\n'))
 for ch in chars:
  if ch not in mapping:mapping[ch]=pool.pop(0)
 slots={mapping[ch]:ch for ch in chars};slots.update(forced);slots[0x7a]=' '
 font=bytearray(prior[0x65010:0x65810]);sheet=Image.open(png).convert('RGBA');ttfont=ImageFont.truetype(str(ttf),8);glyphs=[]
 for code,ch in sorted(slots.items()):
  if ch==' ':data=bytes(16);provider='blank'
  elif ch in plan['native_punctuation']:
   old=plan['native_punctuation'][ch];data=source[0x36810+old*16:0x36810+(old+1)*16];assert any(data);provider='explicit native punctuation bitmap'
  else:
   assert '\uac00'<=ch<='\ud7a3',ch;im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),ch,font=ttfont,fill=255);bits=[int(v>127) for v in im.get_flattened_data()];assert any(bits)
   n=ord(ch)-0xac00;x=n%64*8;y=n//64*8;atlas=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];assert bits==atlas;data=encode(bytes(v*2 for v in bits));assert decode(data)==bytes(v*2 for v in bits);provider='verified Galmuri7 atlas and TTF; no fallback'
  font[code*16:(code+1)*16]=data;glyphs.append({'code':code,'char':ch,'provider':provider,'chr_hex':data.hex()})
 for code in (0,*range(0x41,0x4b),*range(0x70,0x7a)):assert font[code*16:(code+1)*16]==source[0x36810+code*16:0x36810+(code+1)*16]
 body=bytearray();layouts=[]
 for (tokens,count,term),v,text in zip(lines,desired,texts):
  expanded=[]
  for t in tokens:
   pos=t['position']
   if t['kind']=='glyph':code=0 if t['bytes']==[0] else mapping[v[pos]];body.append(code);expanded.append(code)
   elif t['kind']=='spaces':body.extend(t['bytes']);expanded.extend([0]*t['count'])
   else:body.extend(t['bytes']);expanded.extend(t['codes'])
  body.append(term);layouts.append({'text':text,'desired':v,'expanded_tiles':count,'expanded_hex':bytes(expanded).hex()})
 assert len(body)==len(raw)
 oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010];newview=bytearray(oldview);newview[start:end]=body;old,new=state_reader(oldview,p['pointer'],(3,0,0),0,p['ride']),state_reader(newview,p['pointer'],(3,0,0),0,p['ride']);assert len(old)==len(new) and all(all(a[k]==b[k] for k in ('cycles','cursor','buffer_cursor')) for a,b in zip(old,new)),p['entry_id']
 reverse={v:k for k,v in mapping.items()};reverse.update(slots);reverse[0]=' ';reverse.update({0x70+i:str(i) for i in range(10)});actual=[];line=[]
 for event in new:
  if event['value'] in (0xfe,0xff):actual.append(''.join(line));line=[]
  else:line.append(reverse[event['value']])
 expected_desired=[v.replace('¤¤¤','  3') for v in desired]
 assert actual==expected_desired,(p['entry_id'],actual,expected_desired)
 for layout,value in zip(layouts,expected_desired):layout['desired_template']=layout['desired'];layout['desired']=value
 for digits in ((0,0,0),(9,9,9),(1,2,3),(0,1,9)):
  for offset in (0,0x2f):
   for ride in range(6):
    a,b=state_reader(oldview,p['pointer'],digits,offset,ride),state_reader(newview,p['pointer'],digits,offset,ride);assert len(a)==len(b) and all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(a,b))
    for x,y in zip(a,b):
     if x['value']>=0x70 and x['value']<=0x79:assert x['value']==y['value']
 return bytes(body),bytes(font),{'profile':p,'mapping':mapping,'forced_macro_glyphs':forced,'glyphs':glyphs,'body_hex':body.hex(),'layout':layouts,'reader_calls':len(new),'reader_cycles':sum(x['cycles'] for x in new),'per_call_cycles_cursor_equal':True,'variable_state_cases':48,'native_possession_digit_codes':variables[0xf8]}