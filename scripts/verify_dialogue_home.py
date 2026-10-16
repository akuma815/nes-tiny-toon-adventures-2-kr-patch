"""Independent whole-ROM/SSOT/native-CPU and matched runtime verification for home003."""
import csv,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/python/py65-1.2.0'))
from py65.devices.mpu6502 import MPU
def sha(b):return hashlib.sha256(b).hexdigest()
def reader(rom,ptr):
 memory=bytearray(65536);memory[0x8000:0xc000]=rom[0x4010:0x8010];memory[0x6cd]=ptr&255;memory[0x6ce]=ptr>>8
 cpu=MPU(memory=memory);result=[]
 for i in range(200):
  cpu.pc=0x937c;cpu.sp=0xfd;memory[0x1fe]=0xff;memory[0x1ff]=0xc0;before=cpu.processorCycles;steps=0
  while cpu.pc!=0xc100:
   cpu.step();steps+=1;assert steps<10000
  result.append({'value':cpu.a,'cycles':cpu.processorCycles-before,'cursor':memory[0x6c3],'buffer_cursor':memory[0x6c4]})
  if cpu.a==0xfe:memory[0x6c4]=0
  if cpu.a==0xff:return result
 raise AssertionError('Missing terminator')
def main():
 manifest=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));source=(ROOT/manifest['path']).read_bytes();assert sha(source)==manifest['sha256']
 directory=ROOT/'build/dialogue_kr_poc_003';rom=(directory/'TinyToon2_dialogue_kr_poc.nes').read_bytes();report=json.loads((directory/'build_report.json').read_text('utf-8'));assert sha(rom)==report['output_sha256']
 base=(ROOT/'build/dialogue_kr_poc_002/TinyToon2_dialogue_kr_poc.nes').read_bytes();writes=json.loads((directory/'expected_writes.json').read_text('utf-8'));expected=bytearray(source);owned=set()
 for w in writes:
  p=w['file_offset'];n=w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region
  assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(expected)==rom
 changed={i for i,(a,b) in enumerate(zip(source,rom)) if a!=b}|set(range(len(source),len(rom)));assert changed<=owned
 assert rom[0x20010:0x40010]==base[0x20010:0x40010] and rom[0x40010:0x40810]==base[0x40010:0x40810]
 assert rom[0x36810:0x37010]==source[0x36810:0x37010]
 before=list(csv.DictReader((ROOT/'backups/translation/text_ja_before_home_001.csv').open(encoding='utf-8-sig',newline='')))
 after=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(before)==len(after)==54
 for x,y in zip(before,after):
  if x['entry_id']=='MAIN_05741':
   for k in x:
    if k not in ('translation_ko','status','scene','speaker','notes'):assert x[k]==y[k]
  else:assert x==y
 assert sum(x['status']=='draft' for x in after)==2 and sum(x['status']=='untranslated' for x in after)==52
 cycles={}
 for entry,ptr in [('MAIN_05609',0x95f9),('MAIN_05741',0x9731)]:
  original=reader(source,ptr);modified=reader(rom,ptr);assert len(original)==len(modified)
  for a,b in zip(original,modified):
   assert all(a[k]==b[k] for k in ('cycles','cursor','buffer_cursor')),(entry,a,b)
  cycles[entry]={'calls':len(original),'total_cycles':sum(a['cycles'] for a in original),'original':original,'modified':modified}
 assert (ROOT/'build/dialogue_kr_poc_003_rebuild/TinyToon2_dialogue_kr_poc.nes').read_bytes()==rom
 assert (ROOT/'qa/dialogue/한글 패치 적용 003/TinyToon2_home003_applied.nes').read_bytes()==rom
 results={};screens=0
 for route in ('attract','start'):
  ref=ROOT/f'qa/dialogue/home003_reference_{route}';actual=ROOT/f'qa/dialogue/home003_{route}'
  aenv=json.loads((actual/'environment.json').read_text('utf-8'));renv=json.loads((ref/'environment.json').read_text('utf-8'))
  assert aenv['rom_sha256']==sha(rom) and renv['rom_sha256']==sha(base)
  assert all(aenv[k]==renv[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  paths=sorted(actual.glob('frame_*.png'));assert [p.name for p in paths]==[p.name for p in sorted(ref.glob('frame_*.png'))]
  different=0;identical=0
  for p in paths:
   if not p.stat().st_size:assert not (ref/p.name).stat().st_size;continue
   left=Image.open(ref/p.name).convert('RGB');right=Image.open(p).convert('RGB');diff=ImageChops.difference(left,right)
   if diff.getbbox():
    different+=1;assert route=='start'
    # Native NT22A8..22B2 (11 tiles), raster translation y=-5.
    diff.paste((0,0,0),(64,163,152,171));assert diff.getbbox() is None,p.name
   else:identical+=1
   tag=p.stem;rb=(ref/(tag+'_ram.bin')).read_bytes();nb=(actual/(tag+'_ram.bin')).read_bytes()
   assert rb[0x6cf]==nb[0x6cf] and rb[0x6cd:0x6cf]==nb[0x6cd:0x6cf]
   rp=(ref/(tag+'_ppu.bin')).read_bytes();np=(actual/(tag+'_ppu.bin')).read_bytes();assert rp[0x3f00:0x3f20]==np[0x3f00:0x3f20]
   assert (ref/(tag+'_oam.bin')).read_bytes()==(actual/(tag+'_oam.bin')).read_bytes()
  results[route]={'samples':different+identical,'changed_in_home_prompt_only':different,'entire_image_identical':identical};screens+=different+identical
  assert different>0 if route=='start' else different==0
 ppu=(ROOT/'qa/dialogue/home003_start/frame_01080_ppu.bin').read_bytes();assert ppu[:0x800]==rom[0x40810:0x41010]
 assert ppu[0x22a8:0x22b3]==rom[0x5741:0x574c]
 mapping=(ROOT/'qa/dialogue/home003_start/frame_01080_mapping.csv').read_text();assert 'chr,0000,20800,' in mapping and 'chr,0400,20C00,' in mapping
 image=Image.open(ROOT/'qa/dialogue/home003_start/frame_01080.png');image.resize((1024,960),Image.Resampling.NEAREST).save(ROOT/'qa/dialogue/home003_actual_4x.png')
 panel=Image.new('RGB',(2048,960))
 for row,frame in enumerate((930,940,1080)):
  for col,path in enumerate((ROOT/'qa/dialogue/home003_reference_start',ROOT/'qa/dialogue/home003_start')):
   im=Image.open(path/f'frame_{frame:05d}.png')
   # Uniform 4x scale, retaining the native glyph aspect ratio.
   panel.paste(im.crop((0,140,256,220)).resize((1024,320),Image.Resampling.NEAREST),(col*1024,row*320))
 panel.save(ROOT/'qa/dialogue/home003_comparison.png')
 result={'status':'PASS','source_sha256':sha(source),'output_sha256':sha(rom),'expected_writes':len(writes),'whole_diff_bytes':len(changed),'source_chr_title003_and_first_font_preserved':True,'rebuild_and_actual_ips_apply_equal':True,'csv_source_fields_preserved':True,'runtime_samples':screens,'routes':results,'outside_home_prompt_pixel_differences':0,'palette_oam_and_dialogue_ids_equal':True,'actual_home_font_and_nt_equal_build':True,'native_reader_cycles':cycles,'limits':['Dynamic per-paragraph font switch not implemented','Second intro paragraph and 52 source units untranslated','No full playthrough, ride-transition, physical-console, audio, reset or savestate QA','Human final title/translation review pending; no release']}
 (ROOT/'qa/reports/dialogue_home003_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='native_reader_cycles'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
