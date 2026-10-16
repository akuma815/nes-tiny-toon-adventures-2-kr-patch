"""Shared cloned native124 ASCII plus verified Hangul; exact scroll/control budget."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
from compile_ui_variable import split
from extract_title_png import encode,decode
from verify_ui_macro_passthrough import state_reader
ROOT=Path(__file__).resolve().parents[1]
def group(prior,source,plan,macrodata,png,ttf):
 native={0:' ',0x43:'2',0x67:'.',**{0x4b+i:chr(65+i) for i in range(26)}};mapping={c:k for k,c in native.items() if k};mapping[' ']=0x7a;pool=list(range(1,43));pending=[];chars=[]
 for p in plan['profiles']:
  a,b=p['source_file_offset'],p['end_exclusive'];raw=prior[a+0x20000:b+0x20000];assert raw==source[a:b] and hashlib.sha256(raw).hexdigest()==p['source_raw_sha256'];lines=split(raw,{},{});texts=p['text'].split('\n');assert len(lines)==len(texts);desired=[];oldtext=[]
  for (tokens,count,term),text in zip(lines,texts):
   assert len(text)<=count<=32;v=text+' '*(count-len(text));desired.append(v);original=[]
   for t in tokens:
    index=t['position']
    if t['kind']=='spaces':assert v[index:index+t['count']]==' '*t['count'];original.extend(' '*t['count'])
    else:
     assert t['kind']=='glyph' and t['bytes'][0] in native;original.append(native[t['bytes'][0]])
     if t['bytes']==[0]:assert v[index]==' ',(p['entry_id'],index,v)
   oldtext.append(''.join(original))
  assert oldtext==p['source_lines']
  for i in p['preserved_lines']:assert desired[i]==oldtext[i],(p['entry_id'],i)
  chars.extend(c for c in p['text'] if c!='\n');pending.append((p,raw,lines,desired))
 for c in dict.fromkeys(chars):
  if c not in mapping:assert '\uac00'<=c<='\ud7a3' and pool;mapping[c]=pool.pop(0)
 font=bytearray(prior[0x5f010:0x5f810]);assert bytes(font)==source[0x3f010:0x3f810];atlas=Image.open(png).convert('RGBA');face=ImageFont.truetype(str(ttf),8);glyphs=[]
 for c in dict.fromkeys(chars):
  code=mapping[c]
  if c==' ':data=bytes(16);provider='nonzero blank, native literal00 retained separately'
  elif c in native.values():data=source[0x3f010+code*16:0x3f010+(code+1)*16];provider='explicit original ASCII/number/punctuation124 bitmap'
  else:
   n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(bits) and bits==[int(v>127) for v in im.get_flattened_data()];data=encode(bytes(2*v for v in bits));provider='verified Galmuri7 atlas/TTF, no fallback'
  font[code*16:(code+1)*16]=data;glyphs.append({'code':code,'char':c,'provider':provider,'chr_hex':data.hex()})
 for code in native:assert font[code*16:(code+1)*16]==source[0x3f010+code*16:0x3f010+(code+1)*16]
 oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010];view=bytearray(oldview);reverse={**{v:k for k,v in mapping.items()},0:' '};pages=[]
 for p,raw,lines,desired in pending:
  body=bytearray();layouts=[]
  for (tokens,count,term),v in zip(lines,desired):
   expanded=[]
   for t in tokens:
    if t['kind']=='spaces':body.extend(t['bytes']);expanded.extend([0]*t['count'])
    else:
     code=0 if t['bytes']==[0] else mapping[v[t['position']]];body.append(code);expanded.append(code)
   body.append(term);layouts.append({'desired':v,'expanded_tiles':count,'expanded_hex':bytes(expanded).hex()})
  assert len(body)==len(raw);view[p['source_file_offset']:p['end_exclusive']]=body;old,new=state_reader(oldview,p['pointer'],(0,0,0),0,0),state_reader(view,p['pointer'],(0,0,0),0,0);assert len(old)==len(new);actual=[];line=[]
  for a,b in zip(old,new):
   assert all(a[k]==b[k] for k in ('cycles','cursor','buffer_cursor'))
   if a['value'] in (254,255):assert a['value']==b['value'];actual.append(''.join(line));line=[]
   else:line.append(reverse[b['value']])
  assert actual==desired
  # Preserved staff names/publisher/legal rows also retain literal body bytes.
  def raw_lines(b):
   out=[];start=i=0
   while i<len(b):
    if b[i]==253:i+=2;continue
    if b[i] in (254,255):out.append(b[start:i+1]);start=i+1
    i+=1
   return out
  rr,bb=raw_lines(raw),raw_lines(body)
  for i in p['preserved_lines']:assert rr[i]==bb[i]
  pages.append({'profile':p,'body_hex':body.hex(),'layout':layouts,'reader_calls':len(new),'reader_cycles':sum(x['cycles'] for x in new),'per_call_cycles_cursor_equal':True,'preserved_name_publisher_legal_rows_binary_equal':True})
 info={'font_bank':201,'font_hex':bytes(font).hex(),'glyphs':glyphs,'mapping':mapping,'native_font_source_bank':124,'native_font_source_range':[0x3f010,0x3f810],'ASCII_map':native,'Hangul_unique':len({c for c in chars if '\uac00'<=c<='\ud7a3'}),'remaining_literal_slots':pool,'state_cases':3,'scope':'Three observed credits streams, ASCII staff names/KONAMI/legal bytes and bitmaps retained; FD32/literal00/FEFF and reader timing exact'}
 assert len(pages)==3
 return bytes(font),pages,info
