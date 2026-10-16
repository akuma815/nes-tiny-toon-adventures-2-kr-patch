"""Separate shared UI macro glyph slots while preserving native Japanese glyphs."""
import argparse,csv,hashlib,json
from pathlib import Path
from verify_dialogue_home import reader
from verify_ui_native_latch_hooks import compare,irq
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
def literal_codes(raw):
 i=0
 while i<len(raw):
  c=raw[i]
  if c==0xfd:i+=2;continue
  if c<0x7f:yield i,c
  i+=1
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256']
 prior=(ROOT/'build/dialogue_kr_poc_017/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='57be85f5994ae0ebeb605dfc2ea82d920797e6496815f5b67be55e600eac9aa7'
 cat=j('extracted/text/table_20261004_001/text_tokens.json');units={u['entry_id']:u for u in cat['units']};slots=cat['tables'][0]['slots'];selected={s['unit_id'] for s in slots if s['index']==0 or 11<=s['index']<=44};assert len(selected)==33
 writes=j('build/dialogue_kr_poc_017/expected_writes.json');model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 csv_bytes=(ROOT/'workspace/translation/text_ja.csv').read_bytes();assert sha(csv_bytes)=='76bcc0d985c41dff6ce19cf0dd1a8a02e58bbb6814ca0b2f26e9e8239b9e8c48'
 output=bytearray(prior);font=bytearray(source[0x36810:0x37010]);native=bytes(font);markers={};byold={};macros=[];next_code=1
 for slot in cat['tables'][1]['slots'][3:]:
  u=units[slot['unit_id']];p,end=u['file_offset'],u['end_exclusive'];raw=source[p:end];body=bytearray()
  assert raw[-1]==0xff
  for old in raw[:-1]:
   if old==0:body.append(0);continue
   code=next_code;next_code+=1;body.append(code);markers[code]=old;byold.setdefault(old,code);font[code*16:(code+1)*16]=native[old*16:(old+1)*16]
  body.append(0xff);output[p+0x20000:end+0x20000]=body
  assert len(raw)==len(body) and [i for i,v in enumerate(raw) if v in (0,0xff)]==[i for i,v in enumerate(body) if v in (0,0xff)]
  macros.append({'entry_id':u['entry_id'],'code':slot['code'],'source_file_offset':p,'end_exclusive':end,'source_hex':raw.hex(),'output_hex':body.hex(),'policy':'Japanese passthrough; original zero and terminator positions retained'})
 # F9 uses41..4A plus inherited0B; F8/FA set0B=2F and use70..79.
 # Preserve both numeric tile ranges and punctuation in every font.
 fixed={0x6b,0x6c,0x6d,0x6e,*range(0x41,0x4b),*range(0x70,0x7a)};pool=[c for c in range(next_code,0x7f) if c not in fixed and c!=0x7a]
 direct=sorted({c for id in selected for _,c in literal_codes(source[units[id]['file_offset']:units[id]['end_exclusive']]) if c})
 mapping={0:0,**byold,**{c:c for c in fixed}}
 for old in direct:
  if old not in mapping:mapping[old]=pool.pop(0)
  code=mapping[old];assert code not in markers or markers[code]==old
  font[code*16:(code+1)*16]=native[old*16:(old+1)*16]
 font[0x7a*16:0x7b*16]=bytes(16)
 pages=[]
 for id in sorted(selected):
  u=units[id];p,end=u['file_offset'],u['end_exclusive'];raw=source[p:end];body=bytearray(raw)
  for index,old in literal_codes(raw):body[index]=mapping[old]
  output[p+0x20000:end+0x20000]=body
  indices=[s['index'] for s in slots if s['unit_id']==id];assert indices
  for index in indices:output[0x5710+index*2]=148
  pages.append({'entry_id':id,'slots':indices,'pointer':p+0x3ff0,'source_file_offset':p,'end_exclusive':end,'source_raw_sha256':sha(raw),'body_hex':body.hex(),'font_bank':148,'policy':'Japanese passthrough; translation SSOT unchanged'})
 output[0x65010:0x65810]=font
 # Stage-card text above the scanline157 split uses NMI RAM34, not lower C6.
 # Actual FD77/FD92 traces identify native9E28 LDA5A/STA34 as its producer.
 assert source[0x5e38:0x5e3c]==bytes.fromhex('a95a8534')
 for base in (0,0x20000):output[0x5e39+base]=148
 view=bytearray(source);view[0x4010:0x8010]=output[0x24010:0x28010];reader_cases=[]
 for slot in slots:
  ptr=slot['cpu_pointer'];old,new=reader(source,ptr),reader(view,ptr)
  if slot['unit_id'] in selected:
   assert len(old)==len(new) and all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(old,new)),slot
   for x,y in zip(old,new):
    if x['value'] in (0xfe,0xff):assert x['value']==y['value']
    else:assert native[x['value']*16:(x['value']+1)*16]==font[y['value']*16:(y['value']+1)*16],(slot,x,y)
   reader_cases.append({'slot':slot['index'],'entry_id':slot['unit_id'],'calls':len(new),'cycles':sum(x['cycles'] for x in new),'native_visible_glyphs_and_per_call_cycles_equal':True})
  else:assert prior[ptr-0x3ff0+0x20000:ptr-0x3ff0+0x20000+1]==output[ptr-0x3ff0+0x20000:ptr-0x3ff0+0x20000+1]
 for initial in (0,1,90,128,130,132,134,136,138,140,142,144,146,255):
  for slot in range(48):assert compare(prior,output,0x9417,slot,0,0x34,0,initial)[0]==0
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 # Independent prior-image mask: only UI payloads, macro payloads, lookup bytes and reserved2KiB.
 expected=bytearray(prior)
 for info in pages:
  p,end=info['source_file_offset']+0x20000,info['end_exclusive']+0x20000;expected[p:end]=bytes.fromhex(info['body_hex'])
  for index in info['slots']:expected[0x5710+2*index]=148
 for info in macros:expected[info['source_file_offset']+0x20000:info['end_exclusive']+0x20000]=bytes.fromhex(info['output_hex'])
 expected[0x65010:0x65810]=font
 for base in (0,0x20000):expected[0x5e39+base]=148
 assert expected==output and output[:0x10]==prior[:0x10] and output[0x40010:0x65010]==prior[0x40010:0x65010] and output[0x65810:]==prior[0x65810:]
 for w in writes:
  p,n=w['file_offset'],w['length'];w['final_hex']=output[p:p+n].hex()
 expected=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False)
 report={'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','csv_sha256':sha(csv_bytes),'PRG_KiB':256,'CHR_KiB':152,'scope':'Work20 shared UI macro glyph separation and stage-card NMI font;33 native Japanese units preserved; no new Korean translation','expected_writes':len(writes),'font_bank':148,'font_file_range':[0x65010,0x65810],'reserved_remaining_KiB':2,'stage_card_NMI_RAM34_native_9E28_font':148,'macro_units':6,'macro_placeholder_codes':42,'main_unique_units':33,'native_reader_slots':len(reader_cases),'reader_cases':reader_cases,'CPU_page_seed_cases':672,'all_page_setup_cycles_equal_prior017':True,'source_controls_and_original_zero_positions_preserved':True,'runtime':'NOT YET RUN; whole-frame/native variable/register timing comparison required; no release'}
 data={'markers':markers,'direct_mapping':mapping,'macros':macros,'pages':pages,'font_hex':font.hex(),'font_policy':'Every placeholder/direct glyph copies its exact immutable native Japanese bitmap; no fallback'}
 (out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 for name,value in [('build_report.json',report),('expected_writes.json',writes),('ui_macro_mapping.json',data)]: (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('builder_used.py',Path(__file__))]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps({k:v for k,v in report.items() if k!='reader_cases'},indent=2))
if __name__=='__main__':main()
