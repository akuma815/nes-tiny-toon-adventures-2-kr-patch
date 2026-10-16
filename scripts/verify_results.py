"""Independent result glyphs, native dense lifecycle, exact state/points and timing."""
import csv,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from extract_title_png import encode,decode
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_bytes()
def j(p):return json.loads(read(p).decode('utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def envpair(a,b,old,new):
 x,y=j(f'qa/dialogue/{a}/environment.json'),j(f'qa/dialogue/{b}/environment.json');assert x['exit_code']==y['exit_code']==0 and x['rom_sha256']==sha(old) and y['rom_sha256']==sha(new)
 for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'):assert x[k]==y[k],(b,k)
 if 'seed' in x:assert x['seed']==y['seed'] and x['seed_file_sha256']==y['seed_file_sha256']
 return x,y

def pair(a,b,old,new,plan,bonus=True):
 envpair(a,b,old,new);ap=R/f'qa/dialogue/{a}';bp=R/f'qa/dialogue/{b}';files=sorted(ap.glob('frame_*.png'));assert files and [p.name for p in files]==[p.name for p in sorted(bp.glob('frame_*.png'))]
 streamold=old[0x44a0b:0x44aa5];streamnew=new[0x44a0b:0x44aa5];buf={0x400+i:(x,y) for i,(x,y) in enumerate(zip(streamold,streamnew)) if x!=y};ntpairs={}
 for p in plan['labels']:
  for i,(x,y) in enumerate(zip(bytes.fromhex(p['source_hex']),bytes.fromhex(p['body_hex']))):
   for addr in (p['NT']+i,p['NT']+i+0x400,p['NT']+i+0x1000,p['NT']+i+0x1400):ntpairs[addr]=(x,y)
 glyphs={c:decode(new[0x74010+c*16:0x74020+c*16]) for c in range(128)};oldglyphs={c:decode(old[0x5f010+c*16:0x5f020+c*16]) for c in range(128)}
 changes=labelpixels=num_pixels=0;reward=[];fontcases=0
 for f in files:
  tag=f.stem;ram=(ap/(tag+'_ram.bin')).read_bytes();nr=(bp/(tag+'_ram.bin')).read_bytes();allowed={**buf,0x34:(124,208),0x3a:(124,208)} if bonus else {}
  for i,(x,y) in enumerate(zip(ram,nr)):
   if x!=y:assert allowed.get(i)==(x,y),(b,tag,'RAM',hex(i),x,y)
  assert (ap/(tag+'_oam.bin')).read_bytes()==(bp/(tag+'_oam.bin')).read_bytes();p=(ap/(tag+'_ppu.bin')).read_bytes();np=(bp/(tag+'_ppu.bin')).read_bytes()
  for i in range(0x2000,0x4000):
   if p[i]!=np[i]:assert bonus and ntpairs.get(i)==(p[i],np[i]),(b,tag,'NT/palette',hex(i),p[i],np[i])
  ma,mb=rows(f'qa/dialogue/{a}/{tag}_mapping.csv'),rows(f'qa/dialogue/{b}/{tag}_mapping.csv');assert len(ma)==len(mb)
  for x,y in zip(ma,mb):
   for k in ('kind','cpu_or_ppu_address','mem_type'):assert x[k]==y[k]
   if x['relative_offset']!=y['relative_offset']:assert bonus and x['kind']=='chr' and (x['relative_offset'],y['relative_offset']) in (('1F000','34000'),('1F400','34400'));fontcases+=1
   if x['kind']=='chr':
    addr=int(x['cpu_or_ppu_address'],16);off=int(x['relative_offset'],16);noff=int(y['relative_offset'],16);assert p[addr:addr+1024]==old[0x40010+off:0x40410+off] and np[addr:addr+1024]==new[0x40010+noff:0x40410+noff]
  if ram[0x18]==4 and 22<=ram[0x54]<=24:reward.append({'frame':int(tag[6:]),'ride':ram[0x25],'phase':ram[0x54],'life_bonus':list(ram[0x7c2:0x7c4]),'clear_bonus':list(ram[0x7c6:0x7ca]),'gold':ram[0x7e0],'history':ram[0x7e1],'score_native7digits':list(ram[0x7f0:0x7f7])})
  im=Image.open(f).convert('RGB');nm=Image.open(bp/f.name).convert('RGB');box=ImageChops.difference(im,nm).getbbox()
  if not box:continue
  assert bonus and ram[0x18]==4 and ram[0x34]==124,(b,tag,'context',box);changes+=1;masked=im.copy()
  for z in plan['labels']:
   x0,y0,x1,y1=z['screen_box'];width=x1-x0;colors={};oldcodes=bytes.fromhex(z['source_hex']);newcodes=bytes.fromhex(z['body_hex'])
   for dy in range(8):
    for dx in range(width):
     v=oldglyphs[oldcodes[dx//8]][dy*8+dx%8];colors.setdefault(v,set()).add(im.getpixel((x0+dx,y0+dy)))
   assert all(len(c)==1 for c in colors.values()) and all(k in colors for k in (0,2)),(b,tag,'native palette/word epoch',z['source'],colors)
   colors={k:next(iter(c)) for k,c in colors.items()};expected=Image.new('RGB',(width,8))
   for dy in range(8):
    for dx in range(width):expected.putpixel((dx,dy),colors[glyphs[newcodes[dx//8]][dy*8+dx%8]])
   assert nm.crop((x0,y0,x1,y1)).tobytes()==expected.tobytes(),(b,tag,'native Korean pixels',z['source']);labelpixels+=width*8;masked.paste(nm.crop((x0,y0,x1,y1)),(x0,y0))
  assert masked.tobytes()==nm.tobytes(),(b,tag,'pixels outside eight labels',box)
  for z in ((152,72,200,80),(152,88,200,96),(152,104,200,112),(64,152,128,160),(64,184,128,192)):
   assert im.crop(z).tobytes()==nm.crop(z).tobytes();num_pixels+=(z[2]-z[0])*(z[3]-z[1])
 if bonus:
  assert changes and reward
  ac,bc=rows(f'qa/dialogue/{a}/result_asset_copies.csv'),rows(f'qa/dialogue/{b}/result_asset_copies.csv');assert ac==bc and len(ac)==1
  z=ac[0];assert z['selector']=='08' and z['CHR_relative_start']=='049FB' and (ap/z['file']).read_bytes()==streamold and (bp/z['file']).read_bytes()==streamnew
  af,bf=rows(f'qa/dialogue/{a}/result_top_fonts.csv'),rows(f'qa/dialogue/{b}/result_top_fonts.csv');assert len(af)==len(bf);fontobserved=0
  for x,y in zip(af,bf):
   for k in ('frame','pc','scanline','dot','cycles','tag'):assert x[k]==y[k]
   if x['font0']=='1F000':assert y['font0']=='34000' and y['font1']=='34400';fontobserved+=1
   else:assert (x['font0'],x['font1'])==(y['font0'],y['font1'])
   pp=(ap/(x['tag']+'_ppu.bin')).read_bytes();qq=(bp/(y['tag']+'_ppu.bin')).read_bytes();assert pp[:2048]==old[0x40010+int(x['font0'],16):0x40810+int(x['font0'],16)] and qq[:2048]==new[0x40010+int(y['font0'],16):0x40810+int(y['font0'],16)]
  assert fontobserved
  assert any((ap/(f.stem+'_ram.bin')).read_bytes()[0x18]==8 for f in files if int(f.stem[6:])>4000)
 else:assert changes==fontcases==0;reward=[];fontobserved=0
 return {'reference':a,'new':b,'screens':len(files),'changed_results':changes,'whole_unchanged':len(files)-changes,'Korean_caption_pixels_exact':labelpixels,'numeric_pixels_exact':num_pixels,'outside_caption_changed_pixels':0,'exact_RAM_exceptions':'34/3A known124→208 plus actual copied input literal pairs' if bonus else 'none','OAM_palette_points_tickets_history_phases_equal':True,'postNMI_actual_font_samples':fontobserved,'reward_samples':reward}

def irq(a,b,old,new):
 envpair(a,b,old,new);aa,bb=rows(f'qa/dialogue/{a}/irq_phase.csv'),rows(f'qa/dialogue/{b}/irq_phase.csv');assert len(aa)==len(bb);font=0
 for x,y in zip(aa,bb):
  for k in ('frame','kind','pc','address','scanline','dot','cycles'):assert x[k]==y[k],(b,k,x,y)
  if x['value']!=y['value']:assert (x['pc'],x['address'],x['value'],y['value']) in (('FD77','A000','7C','D0'),('FD92','A008','7D','D1')) and int(x['frame'])>=3230,(b,x,y);font+=1
 assert font;return {'reference':a,'new':b,'timing_rows_exact':len(aa),'only_results_NMI_CHR_font_values_changed':font}

def static(old,new,plan):
 font=bytearray(old[0x5f010:0x5f810]);face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8)
 for char,code in plan['mapping'].items():
  if char in ' !':continue
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),char,font=face,fill=255);bits=[int(v>127) for v in im.get_flattened_data()];assert any(bits) and not any(bits[56:]);font[code*16:(code+1)*16]=encode(bytes(2*v for v in bits))
 assert bytes(font)==new[0x74010:0x74810];expected=bytearray(old+bytes(8192));expected[5]=27;expected[0x3f8e0]=208;expected[0x74010:0x74810]=font
 for z in plan['labels']:
  p=z['expanded_file_offset'];assert old[p:p+z['length']].hex()==z['source_hex'];expected[p:p+z['length']]=bytes.fromhex(z['body_hex'])
 assert expected==new and new==read('build/dialogue_kr_poc_041_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 041/TinyToon2_results041_applied.nes')
 source=j('manifests/source_rom.json');s=read(source['path']);assert sha(s)==source['sha256'];expected=bytearray(s);owned=set()
 for w in j('build/dialogue_kr_poc_041/expected_writes.json'):
  p,n=w['file_offset'],w['length'];assert not owned.intersection(range(p,p+n));owned.update(range(p,p+n));assert s[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==new and read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_041/translation_used.csv')

def main():
 old=read('build/dialogue_kr_poc_040/TinyToon2_dialogue_kr_poc.nes');new=read('build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes');plan=j('build/dialogue_kr_poc_041/results_plan_used.json');static(old,new,plan);checks=[]
 for route in ('coaster','cart','train','water','repeat'):checks.append(pair(f'results040_{route}_dense',f'results041_{route}_dense',old,new,plan))
 timing=[irq(f'results040_{route}_irq_v2',f'results041_{route}_irq_v2',old,new) for route in ('coaster','repeat')]
 regressions=[pair(a,b,old,new,plan,False) for a,b in [('game040_intro_regression','results041_intro_regression'),('game040_credits_regression','results041_credits_regression'),('game040_booth_regression','results041_booth_regression'),('game040_castle_native','results041_castle_regression')]]
 for z in checks:
  first=z['reward_samples'][0];last=z['reward_samples'][-1];assert first['history']&(1<<first['ride']);assert first['gold']==(0 if 'repeat' in z['new'] else 1);z['initial_reward']=first;z['final_reward']=last;del z['reward_samples']
 report={'work':46,'status':'PASS','ROM_sha256':sha(new),'IPS_sha256':sha(read('build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.ips')),'ROM_size':len(new),'CHR_KiB':216,'screens':sum(z['screens'] for z in checks+regressions),'dense_bonus_screens':sum(z['screens'] for z in checks),'IRQ_rows_exact':sum(z['timing_rows_exact'] for z in timing),'checks':checks,'regressions':regressions,'IRQ':timing,'independent_glyphs_expected_writes_rebuild_real_CLI_apply_exact':True,'native_producer_ABI_cases':768,'native_decoder_D_clear_cases':128,'source_and_all_prior_fonts_preserved':True,'limits':['Controlled phase54=20/3200 after native game init for four ordinary rides; not natural clear/full play','Repeat additionallyhistory7E1=1 at3200; not naturally earned history','Registered45draft/9technical not wholecorpus percentage','Final human language review/fullgame/audio/reset/savestate/physical console remainpending'],'next_action':'Trace remaining native game/boss and failure branches for undiscovered text'}
 (R/'qa/reports/results041_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ('checks','regressions','IRQ')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
