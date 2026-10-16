"""Work96 source-based common metasprite selectors and bank61 candidate supply."""
from pathlib import Path
import csv,json,hashlib
from PIL import Image,ImageDraw
from verify_dialogue_home import MPU
from verify_gate_font_tag_hooks import Memory
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def run(rom,art,course):
 mem=bytearray(65536);base=0xc010 if len(rom)==262160 else 0x2c010;mem[0x8000:0xc000]=rom[base:base+0x4000];mem[0x25]=course;mem[1]=mem[2]=128;mem[0x5c]=1;mem[0x1fe:0x200]=bytes.fromhex('ff c0');c=MPU(memory=mem);c.pc=0x9643;c.sp=0xfd;c.a=art;c.x=0;c.p=0x30;steps=0
 while c.pc!=0xc100:c.step();steps+=1;assert steps<5000,(art,course)
 return mem,c,bytes(mem[0x200:0x200+c.x]),steps
def parse(mem,art):
 table=0x971c+2*art if art<128 else 0x981e+2*(art-128);pointer=int.from_bytes(mem[table:table+2],'little');assert 0x8000<=pointer<0xc000;layout=pointer;redirect=mem[pointer]>=128
 if redirect:layout=int.from_bytes(mem[pointer+1:pointer+3],'little')
 size=mem[layout];assert size>0 and size<=64 and size%4==0;result=[]
 for i in range(size//4,0,-1):
  y,t,attr,x=mem[layout+4*i-3:layout+4*i+1]
  if redirect:t=mem[pointer+3+i-1]
  signed=lambda v:v if v<128 else v-256
  result.extend((128+signed(y),t,attr,128+signed(x)))
 return bytes(result),{'lookup_table':table,'descriptor_pointer':pointer,'layout_pointer':layout,'redirected_tile_list':redirect,'sprites':size//4,'descriptor_hex':bytes(mem[pointer:pointer+(3+size//4 if redirect else size+1)]).hex(),'layout_hex':bytes(mem[layout:layout+size+1]).hex()}
def banks(rom):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xfd67;c.sp=0xfd;c.p=0x30;m.ram[0x1fe:0x200]=bytes.fromhex('ff c0');m.ram[0x34:0x3a]=bytes([10,11,12,13,61,15])
 while c.pc!=0xc100:c.step();assert c.processorCycles<5000
 return c.processorCycles,[(a,v)for a,v,t in m.writes if a in(0xa000,0xa008,0xb000,0xb008,0xc000,0xc008,0xd000,0xd008)]
def main():
 output=R/'qa/reports/pow096_static.json';image=R/'work/pow_consumer_096/metasprites_native096_static.png';assert not output.exists()and not image.exists();m=j('manifests/source_rom.json');source=(R/m['path']).read_bytes();rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(source)==m['sha256']and sha(rom)==j('qa/reports/gate091_validation.json')['output_sha256']
 assert source[0x2f410:0x2f810]==rom[0x4f410:0x4f810]
 positions=[i for i in range(16,0x20010-4)if source[i:i+4]==bytes.fromhex('a9 3d 85 38')];assert positions==[0x5e47,0x1260d,0x1f717]
 for p in positions:assert source[p:p+4]==rom[p+0x20000:p+0x20004]
 timing,ports=banks(source);assert banks(rom)==(timing,ports)and ports==[(0xa000,10),(0xa008,11),(0xb000,11),(0xb008,12),(0xc000,12),(0xc008,13),(0xd000,61),(0xd008,15)]
 # This finite selector search is a hypothesis population, not proof every ID
 # is authored, valid, reachable, or uses bank61. Stage-only C0..FF excluded.
 enum=[];cases=0
 for art in range(1,192):
  baseline=None
  for course in range(5):
   x,a,u,s=run(source,art,course);y,b,v,t=run(rom,art,course);assert u==v and(a.a,a.x,a.y,a.p,a.sp,a.processorCycles)==(b.a,b.x,b.y,b.p,b.sp,b.processorCycles);cases+=2
   if baseline is None:baseline=(u,a.processorCycles);enum.append({'art_id':art,'OAM_hex':u.hex(),'cycles':a.processorCycles,'steps':s})
   else:assert(u,a.processorCycles)==baseline
 ids=(0x18,0x19,0x3c,0x3e,0x7c,0x9d,0x9c);selected=[];sheet=Image.new('RGB',(480,360),(25,25,25));draw=ImageDraw.Draw(sheet);palette=[(25,25,25),(255,254,255),(116,80,168),(248,216,32)]
 for index,art in enumerate(ids):
  mem,c,data,steps=run(source,art,0);expected,info=parse(mem,art);assert expected==data;selected.append(dict(info,art_id=art,OAM_hex=data.hex(),cycles=c.processorCycles))
  pic=Image.new('RGB',(64,64),palette[0])
  for i in range(0,len(data),4):
   y,t,attr,x=data[i:i+4];local=(t&0xfe)-0x80;assert t%2==1 and 0<=local<64
   raw=source[0x2f410+local*16:0x2f410+(local+2)*16];tile=Image.new('RGB',(8,16));tile.putdata([palette[v]for v in list(decode(raw[:16]))+list(decode(raw[16:]))])
   if attr&64:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if attr&128:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   pic.paste(tile,(x-128+24,y-128+32))
  ox=index%4*120;oy=index//4*180;draw.text((ox+5,oy+5),f'frame {art:02X}; STATIC',(255,255,255));sheet.paste(pic.resize((120,120),Image.Resampling.NEAREST),(ox,oy+25))
 sheet.save(image)
 observed=[]
 for name in('effect084_menu046','effect084_coaster046'):
  q=R/'qa/dialogue'/name;e=j(str(q.relative_to(R)/'environment.json'));p=q/'effect_top_banks.csv';assert sha(p.read_bytes())==e['files'][p.name];rr=list(csv.DictReader(p.open()));found=[x for x in rr if x['CHR1800']=='0F400'];assert found;observed.append({'build':'046','directory':q.relative_to(R).as_posix(),'file_sha256':sha(p.read_bytes()),'top61_at_PPU1800_rows':len(found),'first_frame':int(found[0]['frame']),'existing_no_OAM_pow_read_scope':'See work84; this reuses its frozen observation only'})
 sample_pop={};refs=['stop081_coaster046','stop080_train046_v2','stop081_water046','stop081_cart046','cart089_aligned2F046','gate094_gold4047']
 for name in refs:
  q=R/'qa/dialogue'/name;e=j(str(q.relative_to(R)/'environment.json'));candidates=[];files=sorted(q.glob('frame_*_ram.bin'))
  for p in files:
   raw=p.read_bytes();assert sha(raw)==e['files'][p.name]
   if raw[0x38]!=61:continue
   for i in range(16):
    if raw[0x420+i]and raw[0x400+i]in ids:candidates.append({'file':p.name,'actor':i,'art_id':raw[0x400+i]})
  assert not candidates;sample_pop[name]={'RAM_snapshots':len(files),'active_selected_ID_and_RAM38_61_candidates':len(candidates),'ROM_sha256':e['rom_sha256'],'environment_sha256':sha((q/'environment.json').read_bytes())}
 result={'work':96,'status':'PASS_STATIC_METASPRITE_SUPPLY_ACTUAL_POW_CONSUMER_PENDING','source_sha256':sha(source),'ROM047_sha256':sha(rom),'source61_unchanged':True,'immediate_bank61_producer_source_offsets':positions,'native_FD67_CPU_cycles':timing,'RAM38_goes_to_D000_port':True,'native_port_writes':ports,'historical_actual_mapping':observed,'potential_common_selector_count':191,'CPU_source_current047_cases':cases,'all_selected_source_current_cycles_and_OAM_exact':True,'independent_descriptor_parsed_records':selected,'candidate_analysis_png':image.relative_to(R).as_posix(),'candidate_analysis_png_sha256':sha(image.read_bytes()),'historical_bounded_RAM_scan':sample_pop,'consumer_connected':False,'ROM_CSV_edited':False,'limits':['Static rendering assumes bank61 and arbitrary explanation palette; not actual game images','Frame18/19 and other selected IDs are supply candidates; runtime producers/display still unresolved','Frame3E supplies a flag, so bank61 selection is not POW-specific','191common IDs exclude stage-only C0..FF and zero; enumeration does not prove all records or complete sprite population valid/reachable','Historical RAM38/activeIDs scan is weaker than actual PPU consumption and cannot prove global unused art','No POW translation/preservation decision or final human approval inferred']}
 output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');p=R/'work/pow_consumer_096/common_selector_cpu_records.json';assert not p.exists();p.write_text(json.dumps(enum,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in('independent_descriptor_parsed_records','historical_bounded_RAM_scan','historical_actual_mapping')},indent=2))
if __name__=='__main__':main()