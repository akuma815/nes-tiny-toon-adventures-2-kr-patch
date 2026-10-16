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
def split(raw,macros):
 lines=[];tokens=[];pos=0;i=0
 while i<len(raw):
  c=raw[i]
  if c in (0xfe,0xff):lines.append((tokens,pos,c));tokens=[];pos=0;i+=1
  elif c==0xfd:
   n=raw[i+1];tokens.append({'kind':'spaces','position':pos,'bytes':[c,n],'count':n});pos+=n;i+=2
  elif c in macros:
   codes=macros[c];tokens.append({'kind':'macro','position':pos,'bytes':[c],'codes':codes,'count':len(codes)});pos+=len(codes);i+=1
  else:assert c<0x7f,hex(c);tokens.append({'kind':'glyph','position':pos,'bytes':[c],'count':1});pos+=1;i+=1
 assert not tokens and lines[-1][2]==255
 return lines
def page(prior,source,p,plan,macrodata,png,ttf):
 start,end=p['source_file_offset'],p['end_exclusive'];raw=prior[start+0x20000:end+0x20000];assert sha(source[start:end])==p['source_raw_sha256']
 macros={m['code']:list(bytes.fromhex(m['output_hex']))[:-1] for m in macrodata['macros']};lines=split(raw,macros);texts=p['text'].split('\n');assert len(lines)==len(texts)==len(p['padding']);desired=[];forced={}
 for (tokens,count,term),text,pad in zip(lines,texts,p['padding']):
  assert pad+len(text)<=count<=24,(p['entry_id'],text,count);v=' '*pad+text+' '*(count-pad-len(text));desired.append(v)
  for t in tokens:
   index=t['position']
   if t['kind']=='spaces':assert v[index:index+t['count']]==' '*t['count']
   elif t['kind']=='macro':
    for code,ch in zip(t['codes'],v[index:index+t['count']]):
     if code==0:assert ch==' ';continue
     assert code not in forced or forced[code]==ch;forced[code]=ch
   elif t['bytes']==[0]:assert v[index]==' ',(p['entry_id'],index)
 mapping={' ':0x7a,**plan['native_punctuation']}
 for code,ch in sorted(forced.items()):
  if ch!=' ':mapping.setdefault(ch,code)
 fixed=set(range(1,43))|set(range(0x41,0x4b))|set(range(0x70,0x7a))|set(plan['native_punctuation'].values())|{0x7a}
 pool=[c for c in range(43,0x7f) if c not in fixed];chars=list(dict.fromkeys(c for c in p['text'] if c!='\n'))
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
 oldview=bytearray(source);oldview[0x4010:0x8010]=prior[0x24010:0x28010];newview=bytearray(oldview);newview[start:end]=body;old,new=reader(oldview,p['pointer']),reader(newview,p['pointer']);assert len(old)==len(new) and all(all(a[k]==b[k] for k in ('cycles','cursor','buffer_cursor')) for a,b in zip(old,new)),p['entry_id']
 reverse={v:k for k,v in mapping.items()};reverse.update(slots);reverse[0]=' ';actual=[];line=[]
 for event in new:
  if event['value'] in (0xfe,0xff):actual.append(''.join(line));line=[]
  else:line.append(reverse[event['value']])
 assert actual==desired,(p['entry_id'],actual,desired)
 return bytes(body),bytes(font),{'profile':p,'mapping':mapping,'forced_macro_glyphs':forced,'glyphs':glyphs,'body_hex':body.hex(),'layout':layouts,'reader_calls':len(new),'reader_cycles':sum(x['cycles'] for x in new),'per_call_cycles_cursor_equal':True}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();plan=j('workspace/translation/ui_home_booth_plan_001.json');m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==plan['source_sha256']==m['sha256']
 prior_dir=ROOT/'build'/plan['prior_build'];prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==plan['prior_ROM_sha256'];writes=json.loads((prior_dir/'expected_writes.json').read_text('utf-8'));model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 csv_bytes=(ROOT/'workspace/translation/text_ja.csv').read_bytes();before=(ROOT/'backups/translation/text_ja_before_ui_home_booth_001.csv').read_bytes();assert sha(csv_bytes)==plan['CSV_sha256'] and sha(before)==plan['backup_CSV_sha256']
 rows=list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8-sig'))));oldrows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));selected={p['entry_id']:p for p in plan['profiles']};assert len(rows)==len(oldrows)==54 and len(selected)==8
 for x,y in zip(oldrows,rows):
  for k in x:
   if x['entry_id'] in selected and k in ('translation_ko','status','scene','speaker','notes'):continue
   assert x[k]==y[k]
  if y['entry_id'] in selected:assert y['status']=='draft' and y['translation_ko']==selected[y['entry_id']]['text']
 assert sum(r['status']=='draft' for r in rows)==18
 png=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png';ttf=ROOT/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf';assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
 data=j('build/dialogue_kr_poc_019/ui_macro_mapping.json');output=bytearray(prior);output.extend(bytes(0x6a010-len(output)));output[5]=21;pages=[]
 for p in plan['profiles']:
  body,font,info=page(prior,source,p,plan,data,png,ttf);start,end=p['source_file_offset'],p['end_exclusive'];output[start+0x20000:end+0x20000]=body;off=0x40010+p['font_bank']*0x400;output[off:off+0x800]=font;output[0x5710+2*p['slot']]=p['font_bank'];pages.append(info)
 expected=bytearray(prior);expected.extend(bytes(len(output)-len(prior)));expected[5]=21
 for info in pages:
  p=info['profile'];expected[p['source_file_offset']+0x20000:p['end_exclusive']+0x20000]=bytes.fromhex(info['body_hex']);expected[0x5710+2*p['slot']]=p['font_bank'];off=0x40010+p['font_bank']*0x400
  for g in info['glyphs']:expected[off:off+0x800]=output[off:off+0x800]
 assert expected==output and output[0x40010:0x65810]==prior[0x40010:0x65810] and output[0x261ce:0x261ff]==prior[0x261ce:0x261ff] and not any(output[0x69810:])
 for initial in (0,1,90,128,130,132,134,136,138,140,142,144,146,148,255):
  for slot in range(48):assert compare(prior,output,0x9417,slot,0,0x34,0,initial)[0]==0
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 for w in writes:
  p,n=w['file_offset'],w['length']
  if p==5:w['owner']='CHR_128_to168_KiB'
  if p==0x20010:n=len(output)-p;w['length']=n
  w['final_hex']=output[p:p+n].hex()
 expected=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 report={'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','csv_sha256':sha(csv_bytes),'plan_sha256':sha((ROOT/'workspace/translation/ui_home_booth_plan_001.json').read_bytes()),'PRG_KiB':256,'CHR_KiB':168,'draft':18,'untranslated':36,'expected_writes':len(writes),'selected_entries':list(selected),'font_banks':[[p['font_bank'],p['font_bank']+1] for p in plan['profiles']],'reserved_remaining_KiB':2,'CPU_page_seed_cases':720,'all_page_setup_cycles_equal_prior019':True,'scope':'Work21 eight observed home/booth lower-window drafts; stage-card and other consumers keep Japanese passthrough; no release','runtime':'NOT YET RUN; scene review/timing/matched protected pixels required'}
 for name,value in [('build_report.json',report),('expected_writes.json',writes),('ui_korean_page_mapping.json',pages)]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('plan_used.json',ROOT/'workspace/translation/ui_home_booth_plan_001.json'),('builder_used.py',Path(__file__))]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
