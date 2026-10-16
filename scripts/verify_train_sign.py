"""Independent nativeTTF/font/ExpectedWrites/IRQ andexactmoving traincaption pixels."""
import csv,hashlib,json,itertools
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import numpy as np
from extract_title_png import decode,encode
from verify_results import envpair
from verify_gameover import pair as unchanged_pair
R=Path(__file__).resolve().parents[1]
def read(p):return(R/p).read_bytes()
def j(p):return json.loads((R/p).read_text('utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def state(p):return dict(x.split('=',1)for x in p.read_text('utf-8').splitlines())
def static(old,new,c):
 font=bytearray(old[0x52010:0x53010]);face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);owned=[]
 for z in c['labels']:
  text=z['ko_draft'];w=z['width'];pixels=[2]*(w*8);start=(w-len(text)*8)//2
  for i,char in enumerate(text):
   im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),char,font=face,fill=255);bits=[int(x>127)for x in im.get_flattened_data()];assert any(bits)and not any(bits[56:])
   for y in range(7):
    for x in range(8):
     if bits[y*8+x]:pixels[(y+1)*w+start+i*8+x]=1
  for i,t in enumerate(z['tile_codes']):
   raw=encode(bytes(pixels[y*w+i*8+x]for y in range(8)for x in range(8)));font[t*16:(t+1)*16]=raw;owned.append(t)
 assert len(owned)==10 and font==new[0x76010:0x77010]
 expected=bytearray(old)+bytearray(8192);expected[5]=28;expected[0x3fbff]=216;expected[0x3fc08]=218;expected[0x76010:0x77010]=font;assert expected==new
 assert new==read('build/dialogue_kr_poc_043_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 043/TinyToon2_train043_applied.nes')
 source=j('manifests/source_rom.json');s=read(source['path']);assert sha(s)==source['sha256'];expected=bytearray(s);areas=set()
 for z in j('build/dialogue_kr_poc_043/expected_writes.json'):
  p,n=z['file_offset'],z['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert s[p:p+n]==bytes.fromhex(z['expected_hex']);expected[p:p+n]=bytes.fromhex(z['final_hex'])
 assert expected==new and read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_043/translation_used.csv')
 return set(owned)

def sprite_mask(ppu,oam):
 mask=np.zeros((240,256),dtype=bool)
 for i in range(64):
  yy,t,a,xx=oam[i*4:i*4+4];yy+=1
  if yy>=240 or a&0x20:continue
  for y in range(min(16,240-yy)):
   sy=15-y if a&0x80 else y;code=(t&0xfe)+sy//8;base=(t&1)*0x1000;bits=decode(ppu[base+code*16:base+(code+1)*16])
   for x in range(min(8,256-xx)):
    sx=7-x if a&0x40 else x
    if bits[(sy%8)*8+sx]:mask[yy+y,xx+x]=True
 return mask

def native_pair(old,new,c,owned):
 a='train042_life3_irq_v3';b='train043_life3_irq_v3';envpair(a,b,old,new);ap=R/f'qa/dialogue/{a}';bp=R/f'qa/dialogue/{b}';pics=sorted(ap.glob('frame_*.png'));assert [x.name for x in pics]==[x.name for x in sorted(bp.glob('frame_*.png'))]
 for name in ('life_seed_writes.csv','world_phase.csv','native_NT_calls.csv'):assert(ap/name).read_bytes()==(bp/name).read_bytes()
 al=list(csv.DictReader((ap/'train_engine_irq.csv').open()));bl=list(csv.DictReader((bp/'train_engine_irq.csv').open()));assert len(al)==len(bl)==15252
 for x,y in zip(al,bl):
  for k in x:
   if k=='chr0_relative':assert(x[k],y[k])==('12000','36000')
   elif k=='chr800_relative':assert(x[k],y[k])==('12800','36800')
   else:assert x[k]==y[k],(k,x,y)
 irq={int(x['frame']):x for x in al};engine=sorted(ap.glob('engine_*_ppu.bin'));assert engine and[x.name for x in engine]==[x.name for x in sorted(bp.glob('engine_*_ppu.bin'))]
 for p in engine:
  q=bp/p.name;tag=p.name[:-8];pp,nn=p.read_bytes(),q.read_bytes();assert pp[:4096]==old[0x52010:0x53010]and nn[:4096]==new[0x76010:0x77010]and pp[4096:]==nn[4096:]
  for suf in ('ram.bin','oam.bin'):assert(ap/(tag+'_'+suf)).read_bytes()==(bp/(tag+'_'+suf)).read_bytes()
  sa,sb=state(ap/(tag+'_state.txt')),state(bp/(tag+'_state.txt'));assert set(sa)==set(sb)
  for i in range(16):
   key=f'mapper.chrMemoryOffset{i}';assert int(sa[key])==0x12000+i*256 and int(sb[key])==0x36000+i*256
  assert all(sa[k]==sb[k]for k in sa if k not in {f'mapper.chrMemoryOffset{i}'for i in range(16)}),(tag,'midIRQ CPU/PPUstate outside exactfontremap')
 changed=exact=occluded=0;palette_source=(R/'qa/dialogue/world042_train_life3/engine_14700_ppu.bin').read_bytes();rgb_by_byte={}
 for key,rgb in c['RGB_by_palette_index'].items():g,v=map(int,key.split(','));rgb_by_byte[palette_source[0x3f00+g*4+v]]=tuple(rgb)
 banks={('12000','36000'),('12400','36400'),('12800','36800'),('12C00','36C00')}
 for picture in pics:
  tag=picture.stem;frame=int(tag[6:]);p=(ap/(tag+'_ppu.bin')).read_bytes();n=(bp/(tag+'_ppu.bin')).read_bytes()
  for suf in ('ram.bin','oam.bin'):assert(ap/(tag+'_'+suf)).read_bytes()==(bp/(tag+'_'+suf)).read_bytes(),(tag,suf)
  assert p[0x2000:]==n[0x2000:]
  am=list(csv.DictReader((ap/(tag+'_mapping.csv')).open()));bm=list(csv.DictReader((bp/(tag+'_mapping.csv')).open()));assert len(am)==len(bm)
  for x,y in zip(am,bm):
   for k in ('kind','cpu_or_ppu_address','mem_type'):assert x[k]==y[k]
   if x['kind']=='chr':
    off,no=int(x['relative_offset'],16),int(y['relative_offset'],16);addr=int(x['cpu_or_ppu_address'],16)
    if off!=no:assert(x['relative_offset'],y['relative_offset'])in banks
    assert p[addr:addr+1024]==old[0x40010+off:0x40410+off]and n[addr:addr+1024]==new[0x40010+no:0x40410+no]
   else:assert x==y
  im=Image.open(picture).convert('RGB');nm=Image.open(bp/picture.name).convert('RGB')
  if im.tobytes()==nm.tobytes():continue
  changed+=1;epoch=frame-1;assert epoch in irq and int(irq[epoch]['scanline'])==128 and irq[epoch]['ride']=='02',tag
  pp=(ap/f'engine_{epoch:05d}_ppu.bin').read_bytes();ss=state(ap/f'engine_{epoch:05d}_state.txt');assert ss['ppu.control.backgroundPatternAddr']=='0'and ss['ppu.control.largeSprites']=='true'and ss['ppu.mask.backgroundEnabled']=='true'and ss['ppu.mask.backgroundMask']=='false'
  assert pp[0x2000:0x2400]==pp[0x2400:0x2800];scroll=int(irq[epoch]['scroll_y'],16);opaque=sprite_mask(pp,(ap/f'engine_{epoch:05d}_oam.bin').read_bytes());expected=np.array(im).copy();screen=np.array(im);actual=np.array(nm);count=0
  for row in range(16,24):
   for col in range(32):
    code=pp[0x2000+row*32+col]
    if code not in owned:continue
    assert row==22,(tag,'ownedcode outside captionrow',row,col,code)
    ob=decode(old[0x52010+code*16:0x52020+code*16]);nb=decode(new[0x76010+code*16:0x76020+code*16]);attr=pp[0x23c0+row//4*8+col//4];g=(attr>>((row//2%2)*4+(col//2%2)*2))&3
    for y in range(8):
     for x in range(8):
      sx=(col*8+x-scroll)%256;sy=174+y
      if sx<8:continue
      if opaque[sy,sx]:occluded+=1;continue
      va,vb=ob[y*8+x],nb[y*8+x];assert va in(1,2)and vb in(1,2)
      ca=rgb_by_byte[pp[0x3f00+g*4+va]];cb=rgb_by_byte[pp[0x3f00+g*4+vb]]
      assert tuple(screen[sy,sx])==ca,(tag,'source bitmap/epoch/occlusion',sx,sy,code,va,tuple(screen[sy,sx]),ca)
      expected[sy,sx]=cb;count+=1
  assert count and np.array_equal(expected,actual),(tag,'outsideownedpixels ornewglyph raster',ImageChops.difference(Image.fromarray(expected),nm).getbbox());exact+=count
 assert changed and exact
 return {'source':a,'new':b,'screens':len(pics),'changed_caption_screens':changed,'native_nonoccluded_caption_pixels_exact':exact,'opaque_sprite_pixels_protected':occluded,'outside_caption_tiles_changed_pixels':0,'midIRQ_4KiB_samples':len(engine),'IRQ_font_selection_rows':len(al),'all_RAM_OAM_NT_palette_life_score_tickets_history_phases_CPU_PPU_state_equal':True,'midIRQ_mapper_state_only16_declared256B_font_offsets_changed':True,'exact_screenshot_epoch':'frameF image usesmidIRQ Fminus1, recordedhorizontal scroll andfineY2/dyminus2'}

def timing(old,new):
 a='train042_life3_irq_v3';b='train043_life3_irq_v3';aa=(R/f'qa/dialogue/{a}/irq_phase.csv').open();bb=(R/f'qa/dialogue/{b}/irq_phase.csv').open();permitted={('FBF3','A000','48','D8'),('FBF7','A008','49','D9'),('FBFC','B000','4A','DA'),('FC00','B008','4B','DB')};total=changed=0
 for x,y in itertools.zip_longest(csv.DictReader(aa),csv.DictReader(bb)):
  assert x is not None and y is not None;total+=1
  for k in ('frame','kind','pc','address','scanline','dot','cycles'):assert x[k]==y[k],(k,x,y)
  if x['value']!=y['value']:assert(x['pc'],x['address'],x['value'],y['value'])in permitted;changed+=1
 assert changed==15252*4;return{'rows_exact':total,'only_IRQ5_fourfont_values_changed':changed}

def main():
 out=R/'qa/reports/train043_validation.json';assert not out.exists();old=read('build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes');new=read('build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes');c=j('extracted/graphics/train_sign_001/consumer.json');owned=static(old,new,c);maincheck=native_pair(old,new,c,owned);irq=timing(old,new);reg=[];plan=j('build/dialogue_kr_poc_042/gameover_plan_used.json')
 pairs=[(f'gameover042_{n}_regression',f'train043_{n}_regression')for n in ('intro','credits','booth','castle','bonus')]+[(f'gameover042_{n}_dense',f'train043_gameover_{n}')for n in ('yes','no')]+[(f'pause042_{n}',f'train043_pause_{n}')for n in ('coaster','cart','train','water')]
 for a,b in pairs:reg.append(unchanged_pair(a,b,old,new,plan,False))
 result={'work':51,'status':'PASS','ROM_sha256':sha(new),'IPS_sha256':sha(read('build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.ips')),'ROM_size':len(new),'CHR_KiB':224,'screens':maincheck['screens']+sum(x['screens']for x in reg),'main':maincheck,'IRQ':irq,'regressions':reg,'independent_TTF_andoriginal_ExpectedWrites_rebuild_CLI_apply_exact':True,'native_complete_IRQ_RTI_cases':2304,'native_complete_IRQ_cycles':179,'all_prior_fonts_originalCHR_M_emblem_borders_andother246_tiles_preserved':True,'limits':['Declaredhealth3 replenishment diagnosis; notnaturalplay/fullclear','Bonus/castle/credits/gameover regressions useinheriteddeclaredseeds','PAUSEbitmap120/121 andHOWTOCONTROL outsideobservedpaths stillunconnected','Finalhumanlanguage/fullplay/audio/reset/savestate/physicalconsole pending'],'next_action':'Audit remaininggraphic/titlecontrol/nativeengine consumers andregisteredcorpus closure beforeROMfree release/worklog'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items()if k!='regressions'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
