"""Connect native train IRQfont/NT/palette/actualRGB; explicit life3 diagnostic."""
import csv,hashlib,json
from pathlib import Path
from collections import defaultdict
from PIL import Image
from extract_title_png import decode,encode
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'extracted/graphics/train_sign_001';assert not out.exists();out.mkdir(parents=True)
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));rom=(R/source['path']).read_bytes();assert hashlib.sha256(rom).hexdigest()==source['sha256']
 q=R/'qa/dialogue/world042_train_life3';env=json.loads((q/'environment.json').read_text('utf-8'));assert env['exit_code']==0 and (q/'trace_complete.txt').read_text()=='18000'
 for p,h in env['files'].items():assert sha(q/p)==h,p
 seed=json.loads((q/'seed_used.json').read_text('utf-8'));rows=list(csv.DictReader((q/'life_seed_writes.csv').open()));assert len(rows)==126
 assert [int(x['frame'])for x in rows]==list(range(2800,17841,120))
 assert all(x['address']=='07C0'and x['value']=='03'and (x['written']=='0'and x['before']==x['after']or x['written']=='1'and x['after']=='03'and x['root']=='04'and x['phase']=='05'and x['ride']=='02'and x['pause']=='00')for x in rows)
 irq=list(csv.DictReader((q/'train_engine_irq.csv').open()));assert all(x['chr0_relative']=='12000'and x['chr800_relative']=='12800'and x['PC']=='FC1C'for x in irq)
 fonts=sorted(q.glob('engine_*_ppu.bin'));raw=rom[0x32010:0x33010];assert all(p.read_bytes()[:4096]==raw for p in fonts)
 ppu=(q/'engine_14700_ppu.bin').read_bytes();picture=Image.open(q/'frame_14700.png').convert('RGB')
 previous=[x for x in irq if x['frame']=='14699'];assert len(previous)==1 and previous[0]['scroll_y']=='C3'and previous[0]['scanline']=='128'
 dx=(-int(previous[0]['scroll_y'],16))%256;dy=-2;assert dx==61
 codes=[0x2b,0x2c,0x2d,0x2e,0x2f,0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x67,0x68,0x69,0x6a]
 assert list(ppu[0x22c0:0x22d0])==codes
 index=Image.new('L',(128,16));groups=Image.new('L',(128,16));colors=defaultdict(set)
 for y in range(16):
  for x in range(128):
   yy=176+y;code=ppu[0x2000+(yy//8)*32+x//8];bits=decode(raw[code*16:(code+1)*16]);v=bits[yy%8*8+x%8]
   a=ppu[0x23c0+(yy//32)*8+x//32];g=(a>>(((yy//16)%2)*4+((x//16)%2)*2))&3
   index.putpixel((x,y),v);groups.putpixel((x,y),g);colors[(g,v)].add(picture.getpixel((x+dx,yy+dy)))
 assert all(len(v)==1 for v in colors.values()),{str(k):list(v)for k,v in colors.items()}
 palette={k:next(iter(v))for k,v in colors.items()};render=Image.new('RGB',(128,16));render.putdata([palette[(g,v)]for g,v in zip(groups.getdata(),index.getdata())]);actual=picture.crop((61,174,189,190));assert actual.tobytes()==render.tobytes()
 labels=[]
 for sourceword,ko,start,n,t in [("MONTY'S",'몬타나의',2,5,list(range(0x2d,0x32))),('LAND','랜드',9,3,[0x34,0x35,0x36]),('R.R.','철도',12,2,[0x67,0x68])]:
  assert list(ppu[0x22c0+start:0x22c0+start+n])==t
  assert all(set(decode(raw[i*16:(i+1)*16]))<={1,2}for i in t)
  box=[start*8,0,(start+n)*8,8]
  labels.append({'original':sourceword,'ko_draft':ko,'NT_first':0x22c0+start,'tile_codes':t,'width':n*8,'height':8,'field_box':box,'actual_box':[start*8+61,174,(start+n)*8+61,182],'font_ink':1,'font_background':2})
 for name,im in [('source_label',render),('source_indices',index)]:im.save(out/f'{name}.png')
 render.resize((512,64),Image.Resampling.NEAREST).save(out/'source_label_4x.png');(out/'source_font72_75.bin').write_bytes(raw)
 report={'work':50,'status':'PASS_CONSUMER_AND_RGB','source_sha256':source['sha256'],'ROM042_sha256':env['rom_sha256'],'ROM_unchanged':True,'source_CHR_bank':[72,73,74,75],'source_file_range':[0x32010,0x33010],'IRQ5_producer':{'native_start':'FBE3','LDX_low_PC':'FBEE','LDX_high_PC':'FBF7','active_expanded_operand_offsets':[0x3fbff,0x3fc08],'old_values':[72,74]},'IRQ_rows':len(irq),'actual4KiB_samples':len(fonts),'label_runtime_frame':14700,'exact_preceding_IRQ_frame':14699,'horizontal_offset':61,'NT_to_screen_dy':-2,'exact_actual_RGB_pixels':2048,'RGB_by_palette_index':{f'{g},{v}':list(c)for(g,v),c in palette.items()},'labels':labels,'protected_emblem':'Large decorative M, codes32/33/3A..3D andallrow23/borders unchanged','font_roundtrip_all256':all(encode(decode(raw[i:i+16]))==raw[i:i+16]for i in range(0,4096,16)),'health_diagnostic':{'config':seed,'scheduled_checks':len(rows),'writes':sum(x['written']=='1'for x in rows),'changed_life_values':sum(x['written']=='1'and x['before']!='03'for x in rows),'only_address':'07C0','max_value':3,'all_other_RAM_equal_at_each_write':True,'naturalplay':False},'files':{p.name:sha(p)for p in out.iterdir()if p.is_file()},'limits':['Health replenishment diagnosis, notnaturalplay/fullclear','Original text isMONTY S withdecorativeM / LAND R.R.; earlierstaticMONTANA interpretation corrected','Korean proper-name normalization 몬타나의 andabbreviation철도 aredraft forfinalhumanreview','No KoreanROM/build/apply/CPU/runtime regression yet'],'next_action':'Clone216..219 font; editonlythreecaptiontilegroups withGalmuri7; redirectIRQ5 operands, validate source/new timing/pixels andallprior regressions'}
 (out/'consumer.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k]for k in ('status','IRQ_rows','actual4KiB_samples','exact_actual_RGB_pixels','labels','health_diagnostic')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
