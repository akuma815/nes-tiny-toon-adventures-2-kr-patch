"""Independent native glyph equivalence, variable cases and actual raster gates for019."""
import csv,hashlib,json
from pathlib import Path
from PIL import Image,ImageChops
from verify_dialogue_home import reader,MPU
ROOT=Path(__file__).resolve().parents[1]
def read(p):return (ROOT/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def state_reader(rom,ptr,digits,offset,ride):
 mem=bytearray(65536);mem[0x8000:0xc000]=rom[0x4010:0x8010];mem[0x6cd:0x6cf]=ptr.to_bytes(2,'little');mem[0x7d0:0x7d3]=bytes(digits);mem[0xb]=offset;mem[0x25]=ride;cpu=MPU(memory=mem);out=[]
 for _ in range(200):
  cpu.pc=0x937c;cpu.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');before=cpu.processorCycles;steps=0
  while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<10000
  out.append({'value':cpu.a,'cycles':cpu.processorCycles-before,'cursor':mem[0x6c3],'buffer_cursor':mem[0x6c4]})
  if cpu.a==0xfe:mem[0x6c4]=0
  if cpu.a==0xff:return out
 raise AssertionError('No terminator')
def main():
 d='build/dialogue_kr_poc_019';rom=read(d+'/TinyToon2_dialogue_kr_poc.nes');prior=read('build/dialogue_kr_poc_017/TinyToon2_dialogue_kr_poc.nes');report=j(d+'/build_report.json');m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256'] and sha(rom)==report['output_sha256'] and sha(prior)==report['prior_adopted_sha256']
 model=bytearray(source);owned=set()
 for w in j(d+'/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==rom
 data=j(d+'/ui_macro_mapping.json');font=bytes.fromhex(data['font_hex']);native=source[0x36810:0x37010];assert len(font)==2048 and rom[0x65010:0x65810]==font
 expected=bytearray(prior)
 for p in data['pages']:
  start,end=p['source_file_offset'],p['end_exclusive'];expected[start+0x20000:end+0x20000]=bytes.fromhex(p['body_hex']);assert sha(source[start:end])==p['source_raw_sha256']
  for slot in p['slots']:expected[0x5710+2*slot]=148
 for p in data['macros']:
  start,end=p['source_file_offset'],p['end_exclusive'];expected[start+0x20000:end+0x20000]=bytes.fromhex(p['output_hex']);assert source[start:end]==bytes.fromhex(p['source_hex'])
 expected[0x65010:0x65810]=font
 for base in (0,0x20000):assert prior[0x5e38+base:0x5e3c+base]==bytes.fromhex('a95a8534');expected[0x5e39+base]=148
 assert bytes(expected)==rom and rom[0x40010:0x65010]==prior[0x40010:0x65010] and rom[0x65810:]==prior[0x65810:]
 assert read(d+'/translation_used.csv')==read('workspace/translation/text_ja.csv')==read('build/dialogue_kr_poc_017/translation_used.csv') and read('build/dialogue_kr_poc_019_rebuild/TinyToon2_dialogue_kr_poc.nes')==rom and read('qa/dialogue/한글 패치 적용 019/TinyToon2_macro019_applied.nes')==rom
 cat=j('extracted/text/table_20261004_001/text_tokens.json');selected={p['entry_id'] for p in data['pages']};assert selected=={s['unit_id'] for s in cat['tables'][0]['slots'] if s['index']==0 or 11<=s['index']<=44}
 view=bytearray(source);view[0x4010:0x8010]=rom[0x24010:0x28010];pv=bytearray(source);pv[0x4010:0x8010]=prior[0x24010:0x28010]
 def equal(a,b):
  assert len(a)==len(b) and all(all(x[k]==y[k] for k in ('cycles','cursor','buffer_cursor')) for x,y in zip(a,b))
  for x,y in zip(a,b):
   if x['value'] in (0xfe,0xff):assert x['value']==y['value']
   else:assert native[x['value']*16:(x['value']+1)*16]==font[y['value']*16:(y['value']+1)*16],(x,y)
 for slot in cat['tables'][0]['slots']:
  if slot['unit_id'] in selected:equal(reader(source,slot['cpu_pointer']),reader(view,slot['cpu_pointer']))
  else:assert reader(pv,slot['cpu_pointer'])==reader(view,slot['cpu_pointer'])
 variable_cases=0
 for p in data['pages']:
  start,end=p['source_file_offset'],p['end_exclusive']
  if not any(c in source[start:end] for c in (0xf8,0xf9,0xfa)):continue
  for digits in ((0,0,0),(9,9,9),(1,2,3),(0,1,9)):
   for offset in (0,0x2f):
    for ride in range(6):equal(state_reader(source,p['pointer'],digits,offset,ride),state_reader(view,p['pointer'],digits,offset,ride));variable_cases+=1
 for c in [0,*range(0x41,0x4b),*range(0x70,0x7a),0x6b,0x6c,0x6d,0x6e]:assert font[c*16:(c+1)*16]==native[c*16:(c+1)*16]
 screens=0;routes={};new_bank_samples=0
 for route in ('tour','ticket'):
  actual=ROOT/f'qa/dialogue/macro019_{route}';ref=ROOT/f'qa/dialogue/latch017_{route}';ae=j(f'qa/dialogue/macro019_{route}/environment.json');re=j(f'qa/dialogue/latch017_{route}/environment.json');assert ae['rom_sha256']==sha(rom) and re['rom_sha256']==sha(prior) and ae['exit_code']==re['exit_code']==0 and all(ae[k]==re[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  files=sorted(actual.glob('frame_*.png'));assert [f.name for f in files]==[f.name for f in sorted(ref.glob('frame_*.png'))]
  for f in files:
   tag=f.stem;assert ImageChops.difference(Image.open(f).convert('RGB'),Image.open(ref/f.name).convert('RGB')).getbbox() is None,(route,tag)
   p=(actual/(tag+'_ppu.bin')).read_bytes();rp=(ref/(tag+'_ppu.bin')).read_bytes();ram=(actual/(tag+'_ram.bin')).read_bytes();rr=(ref/(tag+'_ram.bin')).read_bytes();assert (actual/(tag+'_oam.bin')).read_bytes()==(ref/(tag+'_oam.bin')).read_bytes() and p[0x3f00:0x3f20]==rp[0x3f00:0x3f20]
   assert ram[0x6cd:0x6d0]==rr[0x6cd:0x6d0] and ram[0x6ea]==rr[0x6ea] and ram[0xc7]==rr[0xc7]
   for nt in range(0x2000,0x3000,0x400):
    assert p[nt+0x3c0:nt+0x400]==rp[nt+0x3c0:nt+0x400]
    for old,new in zip(rp[nt:nt+0x3c0],p[nt:nt+0x3c0]):
     if old!=new:assert old<127 and new<127 and native[old*16:(old+1)*16]==font[new*16:(new+1)*16]
   maps=rows(f'qa/dialogue/macro019_{route}/{tag}_mapping.csv')
   for entry in maps:
    if entry['kind']=='chr':
     address=int(entry['cpu_or_ppu_address'],16);off=int(entry['relative_offset'],16)+0x40010;assert p[address:address+0x400]==rom[off:off+0x400]
   if ram[0xc6]==148:new_bank_samples+=1
  x=[e for e in rows(f'qa/dialogue/latch017_{route}/menu_events.csv') if e['kind']=='exec'];y=[e for e in rows(f'qa/dialogue/macro019_{route}/menu_events.csv') if e['kind']=='exec'];assert len(x)==len(y)
  for a,b in zip(x,y):assert all(a[k]==b[k] for k in ('frame','address','id','pointer','profile','return_bank','sp','pc'))
  routes[route]={'whole_frames_equal':len(files),'init_returns':len(x)//2};screens+=len(files)
 timings={}
 for route in ('tour','ticket'):
  x=rows(f'qa/dialogue/latch017_{route}_irq/irq_phase.csv');y=rows(f'qa/dialogue/macro019_{route}_irq/irq_phase.csv');assert len(x)==len(y)>30000;changes=0
  for a,b in zip(x,y):
   assert all(a[k]==b[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(a,b)
   if a['value']!=b['value']:assert (a['address'],a['value'],b['value']) in {('A000','5A','94'),('A008','5B','95')},(a,b);changes+=1
  timings[route]={'actual_IRQ_NMI_PPU_mapper_timestamps_equal':len(x),'native_to_passthrough_font_changes':changes}
 cpu=j('qa/reports/macro019_hooks1408.json');assert cpu['abi_cases']==1408
 result={'status':'PASS','adopted_build':'dialogue_kr_poc_019','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read(d+'/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':report['csv_sha256'],'source_units':54,'draft':10,'untranslated':44,'scope':'Work20 glyph-code normalization; native Japanese passthrough, no new Korean text; original intro/title/home retained','whole_prior_image_admitted_changes_only':True,'native_reader_all_slots':48,'passthrough_unique_units':33,'macro_units':6,'placeholders':42,'all_native_glyph_bitmaps_and_controls_equal':True,'variable_seed_cases':variable_cases,'protected_numeric_ranges':['41..4A for F9','70..79 for F8/FA and inherited0B=2F'],'CPU_ABI_cases':1408,'rebuild_actual_IPS_apply_equal':True,'matched_screens':screens,'whole_frame_pixel_differences':0,'routes':routes,'actual_new_font_samples':new_bank_samples,'actual_timing':timings,'visual_review':'Actual019 home1170, booth1620/1740 and stage2310 directly reviewed;018 corrupt stage-card candidate retained and rejected','limits':['Runtime only recorded home/booth/cart routes; other rides/gate/variables remain pending','No complete game corpus or full playthrough; original00 preserved at macro83 position0 constrains Korean phrasing','Font for stage-card top uses NMI RAM34 independently from lower C6; future Korean cards need a separate shared top font','No audio/reset/savestate/physical console/final human review; prior PRG/RNG caveat; no release']}
 (ROOT/'qa/reports/macro019_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
