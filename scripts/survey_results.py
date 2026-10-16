"""Native bonus CHR stream, literal boundaries, actual font/NT/RGB consumer."""
import json,csv,hashlib
from pathlib import Path
from PIL import Image
from title_codec import unpack
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
TRANSLATIONS={'CONGRATULATIONS!':'축하합니다!','LIFE BONUS':'체력 보너스','CLEAR BONUS':'클리어 보너스','TIME BONUS':'시간 보너스','NOW YOU GET':'획득 점수','POINTS':'점','YOUR POINTS':'보유 점수'}
ASCII={0:' ',**{0x4b+i:chr(65+i) for i in range(26)},**{0x41+i:str(i) for i in range(10)},0x66:'!',0x67:'.'}
def literals(b):
 p=2;a=int.from_bytes(b[:2],'little');out=[]
 while True:
  c=b[p];p+=1
  if c==255:return out
  if c==127:a=int.from_bytes(b[p:p+2],'little');p+=2;continue
  if c>=192:n=c&63 or 256;p+=1
  elif c>=128:
   n=c&127 or 256;raw=b[p:p+n];text=''.join(ASCII.get(v,'?') for v in raw);out.append({'offset':p,'NT':a,'length':n,'source_padded':text,'source':text.strip(),'source_hex':raw.hex()});p+=n
  else:n=c or 256;p+=1
  a+=n
def main():
 m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));s=(R/m['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes').read_bytes();sha=lambda b:hashlib.sha256(b).hexdigest();assert sha(s)==m['sha256'];q=R/'qa/dialogue/results040_native';e=json.loads((q/'environment.json').read_text('utf-8'));assert e['exit_code']==0 and e['rom_sha256']==sha(rom) and e['seed']['writes']==[{'address':84,'value':20}];copies=list(csv.DictReader((q/'result_asset_copies.csv').open(encoding='utf-8')));assert len(copies)==1;c=copies[0];assert (c['frame'],c['selector'],c['CHR_relative_start'])==('3231','08','049FB');b=(q/c['file']).read_bytes();assert len(b)==154 and b==s[0x24a0b:0x24aa5]==rom[0x44a0b:0x44aa5];nt,n=unpack(b);assert n==154 and len(nt)==1024
 p=(q/'frame_03600_ppu.bin').read_bytes();screen=Image.open(q/'frame_03600.png').convert('RGB');assert p[:0x800]==rom[0x5f010:0x5f810]==s[0x3f010:0x3f810];selected=[x for x in literals(b) if x['source'] in TRANSLATIONS and x['NT']<0x23c0];assert len(selected)==8 and {x['source'] for x in selected}==set(TRANSLATIONS);labels=[];pixels=0
 for x in selected:
  addr=x['NT'];raw=bytes.fromhex(x['source_hex']);assert bytes(nt[addr+i] for i in range(x['length']))==raw==p[addr:addr+x['length']];row,col=(addr-0x2000)//32,addr%32;colors={};pred=Image.new('RGB',(x['length']*8,8))
  for cy in range(8):
   for cx in range(x['length']*8):
    glyph=raw[cx//8];v=decode(p[glyph*16:(glyph+1)*16])[cy*8+cx%8];rgb=screen.getpixel((col*8+cx,row*8+cy));colors.setdefault(v,set()).add(rgb)
  assert all(len(v)==1 for v in colors.values());colors={k:next(iter(v)) for k,v in colors.items()}
  for cy in range(8):
   for cx in range(x['length']*8):glyph=raw[cx//8];v=decode(p[glyph*16:(glyph+1)*16])[cy*8+cx%8];pred.putpixel((cx,cy),colors[v])
  assert pred.tobytes()==screen.crop((col*8,row*8,(col+x['length'])*8,row*8+8)).tobytes();pixels+=x['length']*64;labels.append({**x,'translation_ko':TRANSLATIONS[x['source']],'source_file_offset':0x24a0b+x['offset'],'expanded_file_offset':0x44a0b+x['offset'],'screen_box':[col*8,row*8,(col+x['length'])*8,row*8+8],'native_colors':colors,'status':'draft_plan'})
 events=list(csv.DictReader((q/'menu_events.csv').open(encoding='utf-8')));assert any(x['frame']=='3230' and x['kind']=='write' and x['address']=='0034' and x['value']=='7C' and x['pc']=='F8D3' for x in events);fonts=list(csv.DictReader((q/'result_top_fonts.csv').open(encoding='utf-8')));actual=0
 for f in fonts:
  if f['font0']!='1F000':continue
  assert f['font1']=='1F400' and (q/(f['tag']+'_ppu.bin')).read_bytes()[:0x800]==s[0x3f010:0x3f810];actual+=1
 assert actual;out=R/'extracted/graphics/results_001';out.mkdir(exist_ok=False,parents=True);screen.save(out/'source_actual.png');screen.resize((1024,960),Image.Resampling.NEAREST).save(out/'source_actual_4x.png');(out/'source_stream.bin').write_bytes(b);result={'work':45,'status':'PASS','source_sha256':sha(s),'ROM_sha256':sha(rom),'scope':'One-address phase54=20 at3200 afteractualroot4/phase5/55=0; native bonus initialization/calc, notnaturalclear','asset':{'source_file_offset':0x24a0b,'expanded_file_offset':0x44a0b,'length':154,'decoded_cells':1024,'copied_frame':3231,'selector':8,'CHR_relative_offset':0x49fb,'native_copy_exact':True},'labels':labels,'distinct_labels':7,'literal_blocks':8,'native_RGB_pixels_exact':pixels,'post_NMI_font124_125_samples':actual,'font_producer':{'CPU':0xf8cf,'expanded_immediate':0x3f8e0,'source_bytes':'a97c8534a9388d8206','next_LDA38_overwrites_NZ':True},'limits':['Naturalclear/fullgame/alltextpopulation unproven','Source031 legal notice andKONAMI staticcatalog originalretention isseparate; selector1EinitialGAMEOVERguessdiscarded','No newROM/CSV edit inwork45; preserved native source labels and calculation states','ExistingKoreanHUD040 isbaseline, separate originalfont124 result consumer'],'next_action':'Font208/209 and8same-length literal blocks,11cycle producer ABI/decoder/runtime numbers and borders'};(out/'consumer.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('labels',)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
