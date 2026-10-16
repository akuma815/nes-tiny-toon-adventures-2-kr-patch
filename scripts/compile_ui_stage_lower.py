"""Shared stage lower font across cost, numbers, insufficient, start and possession. Native timing untouched."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from extract_title_png import encode,decode
from verify_dialogue_home import MPU
from verify_ui_macro_passthrough import state_reader
from compile_ui_variable import split
ROOT=Path(__file__).resolve().parents[1]

def variable_codes(source,ride):
 mem=bytearray(65536);mem[0x8000:0xc000]=source[0x4010:0x8010];mem[0x600:0x602]=bytes.fromhex('fa ff');mem[0x6cd:0x6cf]=(0x600).to_bytes(2,'little');mem[0x25]=ride;c=MPU(memory=mem);out=[]
 for call in range(10):
  c.pc=0x937c;c.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');steps=0
  while c.pc!=0xc100:c.step();steps+=1;assert steps<10000
  if c.a==255:return out
  out.append(c.a)
 raise AssertionError('FA reader did not end')

def group(prior,source,plan,macrodata,png,ttf):
 macros={m['code']:list(bytes.fromhex(m['output_hex']))[:-1] for m in macrodata['macros']};variables={0xfa:variable_codes(source,5),0xf8:[0,0,0x73],0xf9:[0,0,0x73]};assert variables[0xfa]==[0x75,0x70]
 forced={};pending=[];chars=[];used_macro_ids=set()
 for p in plan['profiles']:
  start,end=p['source_file_offset'],p['end_exclusive'];assert hashlib.sha256(source[start:end]).hexdigest()==p['source_raw_sha256'];raw=prior[start+0x20000:end+0x20000];lines=split(raw,macros,variables);texts=p['text'].replace('{variable_FA}','¤¤').replace('{variable_F8}','◇◇◇').replace('{variable_F9}','◇◇◇').split('\n');assert len(lines)==len(texts)==len(p['padding']);desired=[]
  for (tokens,count,term),text,pad in zip(lines,texts,p['padding']):
   assert pad+len(text)<=count<=24,(p['entry_id'],text,pad,count);v=' '*pad+text+' '*(count-pad-len(text));desired.append(v)
   for t in tokens:
    i=t['position']
    if t['kind']=='spaces':assert v[i:i+t['count']]==' '*t['count']
    elif t['kind']=='variable':assert v[i:i+t['count']]==('¤' if t['bytes']==[0xfa] else '◇')*t['count']
    elif t['kind']=='macro':
     used_macro_ids.add(t['bytes'][0])
     for code,ch in zip(t['codes'],v[i:i+t['count']]):
      if code==0:assert ch==' ';continue
      assert code not in forced or forced[code]==ch,(p['entry_id'],code,forced.get(code),ch);forced[code]=ch
    elif t['bytes']==[0]:assert v[i]==' ',(p['entry_id'],i,v)
  chars.extend(c for c in p['text'].replace('{variable_FA}','').replace('{variable_F8}','').replace('{variable_F9}','') if c!='\n');pending.append((p,raw,lines,desired,texts))
 assert used_macro_ids=={0x88} and set(forced)==set(range(39,43))
 mapping={' ':0x7a,**plan['native_punctuation']}
 for code,ch in sorted(forced.items()):
  if ch!=' ':mapping.setdefault(ch,code)
 fixed=set(range(1,43))|set(range(0x41,0x4b))|set(range(0x70,0x7a))|set(plan['native_punctuation'].values())|{0x7a}
 pool=[c for c in range(1,0x7f) if c not in fixed];pool_original=pool.copy()
 for ch in dict.fromkeys(chars):
  if ch not in mapping:assert pool,('shared card font exhausted',ch);mapping[ch]=pool.pop(0)
 slots={mapping[ch]:ch for ch in chars};slots.update(forced);slots[0x7a]=' ';font=bytearray(prior[0x65010:0x65810]);sheet=Image.open(png).convert('RGBA');face=ImageFont.truetype(str(ttf),8);glyphs=[]
 for code,ch in sorted(slots.items()):
  if ch==' ':data=bytes(16);provider='blank'
  elif ch in plan['native_punctuation']:
   old=plan['native_punctuation'][ch];data=source[0x36810+old*16:0x36810+(old+1)*16];assert any(data);provider='explicit native punctuation bitmap'
  else:
   assert '\uac00'<=ch<='\ud7a3';n=ord(ch)-0xac00;x=n%64*8;y=n//64*8;atlas=[int(v[3]>0 and max(v[:3])>127) for v in sheet.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),ch,font=face,fill=255);bits=[int(v>127) for v in im.get_flattened_data()];assert any(bits) and bits==atlas;data=encode(bytes(2*v for v in bits));assert decode(data)==bytes(2*v for v in bits);provider='verified Galmuri7 atlas and TTF; no fallback'
  font[code*16:(code+1)*16]=data;glyphs.append({'code':code,'char':ch,'provider':provider,'chr_hex':data.hex()})
 for code in (0,*range(0x41,0x4b),*range(0x70,0x7a)):assert font[code*16:(code+1)*16]==source[0x36810+code*16:0x36810+(code+1)*16]
 reverse={v:k for k,v in mapping.items()};reverse.update(slots);reverse[0]=' ';reverse.update({0x70+i:str(i) for i in range(10)})
 oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010];view=bytearray(oldview);pages=[]
 for p,raw,lines,desired,texts in pending:
  body=bytearray();layouts=[]
  for (tokens,count,term),v,text in zip(lines,desired,texts):
   expanded=[]
   for t in tokens:
    pos=t['position']
    if t['kind']=='glyph':c=0 if t['bytes']==[0] else mapping[v[pos]];body.append(c);expanded.append(c)
    elif t['kind']=='spaces':body.extend(t['bytes']);expanded.extend([0]*t['count'])
    else:body.extend(t['bytes']);expanded.extend(t['codes'])
   body.append(term);layouts.append({'text':text,'desired_template':v,'desired':v.replace('¤¤','50').replace('◇◇◇','  3'),'expanded_tiles':count,'expanded_hex':bytes(expanded).hex()})
  assert len(body)==len(raw);view[p['source_file_offset']:p['end_exclusive']]=body
  for digits in ((0,0,0),(9,9,9),(1,2,3),(0,1,9)):
   for offset in (0,0x2f):
    for ride in range(6):
     a,b=state_reader(oldview,p['pointer'],digits,offset,ride),state_reader(view,p['pointer'],digits,offset,ride);assert len(a)==len(b) and all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(a,b)),p['entry_id']
     for x,y in zip(a,b):
      if x['value'] in (254,255):assert x['value']==y['value']
  events=state_reader(view,p['pointer'],(3,0,0),0x2f,5);actual=[];line=[]
  for e in events:
   if e['value'] in (254,255):actual.append(''.join(line));line=[]
   else:line.append(reverse[e['value']])
  assert actual==[x['desired'] for x in layouts],(p['entry_id'],actual,layouts)
  pages.append({'profile':p,'body_hex':body.hex(),'layout':layouts,'reader_calls':len(events),'reader_cycles':sum(x['cycles'] for x in events),'per_call_cycles_cursor_equal':True,'state_cases':48})
 info={'mapping':mapping,'font_bank':196,'font_hex':bytes(font).hex(),'glyphs':glyphs,'forced_macro_glyphs':forced,'macro_ids':sorted(used_macro_ids),'released_macro_codes':[],'release_scope':'Five units/six tagged native lower slots, all other fonts untouched; codes1..38 remain reserved','Hangul_unique':len(set(ch for ch in chars if '\uac00'<=ch<='\ud7a3')),'allocation_pool':pool_original,'remaining_literal_slots':pool,'native_FA_codes_by_ride':{str(i):variable_codes(source,i) for i in range(6)},'state_cases':48*len(pages)}
 assert len(pages)==5 and info['state_cases']==240
 return bytes(font),pages,info
