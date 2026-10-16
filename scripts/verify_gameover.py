"""Gameover042 actual art/text/cursor/choices/state/IRQ plus inherited scenes."""
import json,csv
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
from extract_title_png import decode,encode
from verify_results import read,j,sha,rows,envpair
from verify_gameover_native_queue import run,parse
R=Path(__file__).resolve().parents[1]
def pair(a,b,old,new,plan,gameover=True):
 envpair(a,b,old,new);ap=R/f'qa/dialogue/{a}';bp=R/f'qa/dialogue/{b}';files=sorted(ap.glob('frame_*.png'));assert files and [p.name for p in files]==[p.name for p in sorted(bp.glob('frame_*.png'))];allowed={};ntpairs={}
 if gameover:
  _,ma,_=run(old,0x34,0);_,mb,_=run(new,0x34,0);xa,_=parse(ma.ram[0x100:0x200],0,ma);xb,_=parse(mb.ram[0x100:0x200],0,mb)
  for p,(nt,va) in xa.items():
   ntb,vb=xb[p];assert nt==ntb
   if va!=vb:allowed[p]=(va,vb)
  allowed.update({0x34:(124,210),0x35:(122,212),0x3a:(124,210),0x3b:(122,212)})
  for z in plan['labels']:
   for i,(va,vb) in enumerate(zip(bytes.fromhex(z['source_hex']),bytes.fromhex(z['body_hex']))):
    for nt in (z['NT']+i,(z['NT']+i)^0x400,z['NT']+i+0x1000,((z['NT']+i)^0x400)+0x1000):ntpairs[nt]=(va,vb)
 oldbits=[];newbits=[]
 for y in range(32):
  for x in range(128):
   tile=(y//8)*16+x//8;idx=(y%8)*8+x%8;oldbits.append(decode(old[0x5ec10+tile*16:0x5ec20+tile*16])[idx]);newbits.append(decode(new[0x75410+tile*16:0x75420+tile*16])[idx])
 oldglyph={c:decode(old[0x5f010+c*16:0x5f020+c*16]) for c in range(128)};nglyph={c:decode(new[0x74810+c*16:0x74820+c*16]) for c in range(128)};changed=logo_pixels=label_pixels=0;font_samples=0;changed_roots=set()
 for f in files:
  tag=f.stem;ram=(ap/(tag+'_ram.bin')).read_bytes();nr=(bp/(tag+'_ram.bin')).read_bytes()
  for i,(va,vb) in enumerate(zip(ram,nr)):
   if va!=vb:assert allowed.get(i)==(va,vb),(b,tag,'RAM',hex(i),va,vb)
  assert (ap/(tag+'_oam.bin')).read_bytes()==(bp/(tag+'_oam.bin')).read_bytes();p=(ap/(tag+'_ppu.bin')).read_bytes();np=(bp/(tag+'_ppu.bin')).read_bytes()
  for i in range(0x2000,0x4000):
   if p[i]!=np[i]:assert gameover and ntpairs.get(i)==(p[i],np[i]),(b,tag,'NT/pal',hex(i),p[i],np[i])
  amap,bmap=rows(f'qa/dialogue/{a}/{tag}_mapping.csv'),rows(f'qa/dialogue/{b}/{tag}_mapping.csv');assert len(amap)==len(bmap)
  for x,y in zip(amap,bmap):
   for k in ('kind','cpu_or_ppu_address','mem_type'):assert x[k]==y[k]
   if x['relative_offset']!=y['relative_offset']:assert gameover and x['kind']=='chr' and (x['relative_offset'],y['relative_offset']) in (('1F000','34800'),('1F400','34C00'),('1E800','35000'),('1EC00','35400'))
   if x['kind']=='chr':
    addr=int(x['cpu_or_ppu_address'],16);off=int(x['relative_offset'],16);noff=int(y['relative_offset'],16);assert p[addr:addr+1024]==old[0x40010+off:0x40410+off] and np[addr:addr+1024]==new[0x40010+noff:0x40410+noff]
  im=Image.open(f).convert('RGB');nm=Image.open(bp/f.name).convert('RGB');box=ImageChops.difference(im,nm).getbbox()
  if not box:continue
  assert gameover and ram[0x3a]==124 and ram[0x3b]==122 and p[:4096]==old[0x5f010:0x5f810]+old[0x5e810:0x5f010],(b,tag,'actualfont resource lifetime',box);changed+=1;changed_roots.add(ram[0x18]);mask=im.copy();crop=im.crop((64,56,192,88));colors={}
  for idx,rgb in zip(oldbits,crop.get_flattened_data()):colors.setdefault(idx,set()).add(rgb)
  assert set(colors)=={0,1,2,3} and all(len(v)==1 for v in colors.values()),(b,tag,'source logo palette/epoch');colors={k:next(iter(v)) for k,v in colors.items()};expected=Image.new('RGB',(128,32));expected.putdata([colors[v] for v in newbits]);assert nm.crop((64,56,192,88)).tobytes()==expected.tobytes(),(b,tag,'nativeAI artpixels');mask.paste(nm.crop((64,56,192,88)),(64,56));logo_pixels+=4096
  for z in plan['labels']:
   x0,y0,x1,y1=z['screen_box'];w=x1-x0;cs={};ob=bytes.fromhex(z['source_hex']);nb=bytes.fromhex(z['body_hex'])
   for y in range(8):
    for x in range(w):idx=oldglyph[ob[x//8]][y*8+x%8];cs.setdefault(idx,set()).add(im.getpixel((x0+x,y0+y)))
   assert set(cs)=={0,2} and all(len(v)==1 for v in cs.values()),(b,tag,'labelpalette/epoch',z['source']);cs={k:next(iter(v)) for k,v in cs.items()};expected=Image.new('RGB',(w,8))
   for y in range(8):
    for x in range(w):expected.putpixel((x,y),cs[nglyph[nb[x//8]][y*8+x%8]])
   assert nm.crop((x0,y0,x1,y1)).tobytes()==expected.tobytes(),(b,tag,'Korean captionpixels',z['source']);mask.paste(nm.crop((x0,y0,x1,y1)),(x0,y0));label_pixels+=w*8
  assert mask.tobytes()==nm.tobytes(),(b,tag,'Outside4owners',box)
 if gameover:
  aa,bb=rows(f'qa/dialogue/{a}/gameover_top_fonts.csv'),rows(f'qa/dialogue/{b}/gameover_top_fonts.csv');assert len(aa)==len(bb)
  for x,y in zip(aa,bb):
   for k in ('frame','pc','scanline','dot','cycles','tag'):assert x[k]==y[k]
   assert tuple(x[k] for k in ('font0','font1','font2','font3'))==('1F000','1F400','1E800','1EC00') and tuple(y[k] for k in ('font0','font1','font2','font3'))==('34800','34C00','35000','35400')
   assert (ap/(x['tag']+'_ppu.bin')).read_bytes()[:4096]==old[0x5f010:0x5f810]+old[0x5e810:0x5f010] and (bp/(y['tag']+'_ppu.bin')).read_bytes()[:4096]==new[0x74810:0x75810];font_samples+=1
  assert changed and font_samples;final=(bp/'frame_08000_ram.bin').read_bytes();assert final[0x18]==(8 if '_yes_' in b else 7);assert list(final[0x7d0:0x7d3])==[0,1,0]
 else:assert changed==0
 return {'reference':a,'new':b,'screens':len(files),'changed_gameover':changed,'whole_unchanged':len(files)-changed,'native_AI_logo_pixels_exact':logo_pixels,'Korean_caption_pixels_exact':label_pixels,'outside_four_owned_boxes_changed_pixels':0,'RAM_exact_exceptions':'34/35/3A/3B fontpairs plusnativebase0 queueownedliteralpairs' if gameover else 'none','OAM_palette_points_tickets_history_player_phase_cursor_equal':True,'postNMI_font4KiB_samples':font_samples,'changed_logical_roots':sorted(changed_roots),'visual_context':'Actual4KiB font124/125/122/123 andlatches3A/3B; nativefade retainsgameovergraphics afterroot changes to8'}

def irq(a,b,old,new):
 envpair(a,b,old,new);aa,bb=rows(f'qa/dialogue/{a}/irq_phase.csv'),rows(f'qa/dialogue/{b}/irq_phase.csv');assert len(aa)==len(bb);font=0;permitted={('FD77','A000','7C','D2'),('FD92','A008','7D','D3'),('FD77','B000','7A','D4'),('FD92','B008','7B','D5')}
 for x,y in zip(aa,bb):
  for k in ('frame','kind','pc','address','scanline','dot','cycles'):assert x[k]==y[k],(b,k,x,y)
  if x['value']!=y['value']:assert (x['pc'],x['address'],x['value'],y['value']) in permitted and int(x['frame'])>=5034,(b,x,y);font+=1
 assert font;return {'new':b,'timing_rows_exact':len(aa),'only_gameover_NMI_font_values_changed':font}

def static(old,new,plan):
 font=bytearray(old[0x5f010:0x5f810]);face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8)
 for char,code in plan['mapping'].items():
  if not (0xac00<=ord(char)<=0xd7a3):continue
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),char,font=face,fill=255);bits=[int(v>127) for v in im.get_flattened_data()];assert any(bits) and not any(bits[56:]);font[code*16:code*16+16]=encode(bytes(v*2 for v in bits))
 assert font==new[0x74810:0x75010];art=Image.open(R/'workspace/graphics/gameover_kr_ai_001/converted_logo.png').convert('RGB');colors={tuple(v):int(k) for k,v in j('extracted/graphics/gameover_001/consumer.json')['logo_native_colors'].items()};logo=bytearray()
 for row in range(4):
  for col in range(16):logo.extend(encode(bytes(colors[art.getpixel((col*8+x,row*8+y))] for y in range(8) for x in range(8))))
 assert logo==new[0x75410:0x75810];expected=bytearray(old);expected[0x74810:0x75010]=font;expected[0x75010:0x75410]=old[0x5e810:0x5ec10];expected[0x75410:0x75810]=logo
 for z in plan['labels']:
  for p in (z['source_file_offset'],z['expanded_file_offset']):assert old[p:p+z['length']].hex()==z['source_hex'];expected[p:p+z['length']]=bytes.fromhex(z['body_hex'])
 for p,oldv,newv in zip(plan['producer']['expanded_immediates'],plan['producer']['old'],plan['producer']['new']):assert old[p]==old[p-0x20000]==oldv;expected[p]=expected[p-0x20000]=newv
 assert expected==new and new==read('build/dialogue_kr_poc_042_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 042/TinyToon2_gameover042_applied.nes');m=j('manifests/source_rom.json');s=read(m['path']);assert sha(s)==m['sha256'];expected=bytearray(s);owned=set()
 for w in j('build/dialogue_kr_poc_042/expected_writes.json'):
  p,n=w['file_offset'],w['length'];assert not owned.intersection(range(p,p+n));owned.update(range(p,p+n));assert s[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==new and read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_042/translation_used.csv')

def main():
 old=read('build/dialogue_kr_poc_041/TinyToon2_dialogue_kr_poc.nes');new=read('build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes');plan=j('build/dialogue_kr_poc_042/gameover_plan_used.json');static(old,new,plan);checks=[pair(f'gameover041_{c}_dense',f'gameover042_{c}_dense',old,new,plan) for c in ('yes','no')];timing=[irq(f'gameover041_{c}_irq',f'gameover042_{c}_irq',old,new) for c in ('yes','no')];regressions=[]
 for a,b in [('results041_intro_regression','gameover042_intro_regression'),('results041_credits_regression','gameover042_credits_regression'),('results041_booth_regression','gameover042_booth_regression'),('results041_castle_regression','gameover042_castle_regression'),('results041_coaster_dense','gameover042_bonus_regression')]:regressions.append(pair(a,b,old,new,plan,False))
 result={'work':48,'status':'PASS','ROM_sha256':sha(new),'IPS_sha256':sha(read('build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.ips')),'ROM_size':len(new),'CHR_KiB':216,'screens':sum(x['screens'] for x in checks+regressions),'gameover_dense_screens':sum(x['screens'] for x in checks),'IRQ_rows_exact':sum(x['timing_rows_exact'] for x in timing),'checks':checks,'IRQ':timing,'regressions':regressions,'independent_native_PNG_TTF_expected_writes_rebuild_real_CLI_apply_exact':True,'native_producer_cases':768,'native_queue_D_clear_cases':384,'all_prior_fonts_and_source_CHR_preserved':True,'limits':['Initialtickets4seed, nativegameplayfailure thereafter; notnaturalinitialcurrency/fullgame','Inheritedbonus/castle/credits regressions use theirdeclaredphase/gold/selector seeds','PAUSE consumer stillpending, wholecorpus incomplete','Finalhumanlanguage/fullplay/audio/reset/savestate/physicalconsole pending'],'next_action':'Trace PAUSE andtitlePUSHSTART remaininggraphic consumers'}
 out=R/'qa/reports/gameover042_validation.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('checks','IRQ','regressions')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
