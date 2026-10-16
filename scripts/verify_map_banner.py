"""Independent prior delta, native pixels, exact protected runtime and timing."""
import json,hashlib,csv
from pathlib import Path
from PIL import Image,ImageChops
from extract_title_png import decode
from verify_gate_font_tag import env
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_bytes()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 prior=read('build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes');rom=read('build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes');m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256'];plan=j('build/dialogue_kr_poc_038/banner_plan_used.json');expected=bytearray(prior)
 for c in plan['changes']:
  p=c['expanded_file_offset'];assert prior[p:p+16]==bytes.fromhex(c['source_raw_hex']);expected[p:p+16]=bytes.fromhex(c['final_hex'])
 assert expected==rom and prior[:0x40010]==rom[:0x40010] and read('build/dialogue_kr_poc_038_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 038/TinyToon2_map038_applied.nes')==rom
 expected=bytearray(source);owned=set()
 for w in j('build/dialogue_kr_poc_038/expected_writes.json'):
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not owned&area;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==rom and read('build/dialogue_kr_poc_038/translation_used.csv')==read('workspace/translation/text_ja.csv')
 consumer=j('extracted/graphics/map_banner_001/consumer.json');colors={int(k):tuple(v) for k,v in consumer['palette'].items()};native=read('workspace/graphics/map_banner_kr_001/indices.bin');orig=read('extracted/graphics/map_banner_001/source_indices.bin');rgb=Image.new('RGB',(144,16));rgb.putdata([colors[v] for v in native]);assert rgb.tobytes()==Image.open(R/'workspace/graphics/map_banner_kr_001/native.png').convert('RGB').tobytes();reference_rgb=Image.new('RGB',(144,16));reference_rgb.putdata([colors[v] for v in orig]);assert all(native[y*144+x]==orig[y*144+x] for y in range(16) for x in range(144) if not 6<=x<137)
 for c in consumer['cells']:
  addr=c['NT'];col=addr%32-7;row=addr//32%32-3;assert decode(rom[c['expanded_file_offset']:c['expanded_file_offset']+16])==bytes(native[(row*8+y)*144+col*8+x] for y in range(8) for x in range(8))
 checks=[]
 for ref,new in [('map037_tour','map038_tour'),('credits037_intro','map038_intro'),('credits037_selector_v3','map038_credits')]:
  a,b=env(ref,prior),env(new,rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  if 'seed' in a:assert a['seed']==b['seed'] and a['seed_file_sha256']==b['seed_file_sha256']
  files=sorted((R/'qa/dialogue'/new).glob('frame_*.png'));assert files and [p.name for p in files]==[p.name for p in sorted((R/'qa/dialogue'/ref).glob('frame_*.png'))];changed=0;rides=set()
  for f in files:
   tag=f.stem;rb=read(f'qa/dialogue/{new}/{tag}_ram.bin');ppu=read(f'qa/dialogue/{new}/{tag}_ppu.bin');rp=read(f'qa/dialogue/{ref}/{tag}_ppu.bin');assert rb==read(f'qa/dialogue/{ref}/{tag}_ram.bin')
   for suffix in ('_oam.bin','_mapping.csv'):assert read(f'qa/dialogue/{new}/{tag}{suffix}')==read(f'qa/dialogue/{ref}/{tag}{suffix}')
   assert ppu[0x2000:]==rp[0x2000:]
   maps=rows(f'qa/dialogue/{new}/{tag}_mapping.csv');allowed=set()
   for mapping in maps:
    if mapping['kind']!='chr':continue
    base=int(mapping['cpu_or_ppu_address'],16);off=int(mapping['relative_offset'],16);assert ppu[base:base+0x400]==rom[0x40010+off:0x40410+off]
    for i in range(0x400):
     if rom[0x40010+off+i]!=prior[0x40010+off+i]:allowed.add(base+i)
   assert {i for i in range(0x2000) if ppu[i]!=rp[i]}<=allowed
   image=Image.open(f).convert('RGB');old=Image.open(R/f'qa/dialogue/{ref}/{f.name}').convert('RGB');diff=ImageChops.difference(image,old)
   if diff.getbbox():
    assert rb[0x34]==rb[0x3a]==80,(ref,tag,'wrong active top font');assert all(ppu[c['NT']]==c['tile'] for c in consumer['cells'])
    # Native fade changes palette values during exit. Learn exactly one RGB
    # per original pixel index from the complete prior capture, then require
    # every target pixel to be its compiled native index in that same palette.
    # Palette bytes already matched; no variable-color pixel tolerance.
    crop=old.crop((56,24,200,40));live={v:{crop.getpixel((x,y)) for y in range(16) for x in range(144) if orig[y*144+x]==v} for v in range(4)};assert all(len(s)==1 for s in live.values()),(ref,tag,'inconsistent native palette or overlap');live={v:next(iter(s)) for v,s in live.items()};projected=Image.new('RGB',(144,16));projected.putdata([live[v] for v in native]);assert image.crop((56,24,200,40)).tobytes()==projected.tobytes(),(ref,tag,'actual complete native banner with exact native fade')
    for y in range(16):
     for x in range(144):
      if orig[y*144+x]!=native[y*144+x]:diff.putpixel((56+x,24+y),(0,0,0))
    assert diff.getbbox() is None,(ref,tag,'outside exact changed native pixels');changed+=1;rides.add(rb[0x25])
  for log in ('menu_events.csv','seed_writes.csv'):
   if (R/'qa/dialogue'/new/log).exists():assert read(f'qa/dialogue/{new}/{log}')==read(f'qa/dialogue/{ref}/{log}')
  checks.append({'reference':ref,'candidate':new,'screens':len(files),'changed_native_banner_only':changed,'whole_frames_equal':len(files)-changed,'map_ride_states':sorted(rides),'RAM_NT_palette_OAM_mapping_native_events_equal':True})
 a,b=env('map037_tour_irq',prior),env('map038_tour_irq',rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));a=rows('qa/dialogue/map037_tour_irq/irq_phase.csv');b=rows('qa/dialogue/map038_tour_irq/irq_phase.csv');assert a==b
 out={'status':'PASS','work':40,'adopted_build':'dialogue_kr_poc_038','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read('build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'changed_tiles':len(plan['changes']),'changed_ROM_bytes':sum(x!=y for x,y in zip(prior,rom)),'ExpectedWrites':8,'rebuild_actual_IPS_apply_equal':True,'independent_native_art_indices_exact':True,'outside_exact_native_changed_pixels':0,'checks':checks,'matched_screens':sum(x['screens'] for x in checks),'actual_timestamps_and_values_equal':len(a),'visual_review':'Separate actual map scene PNG review required','limits':['Five observed map states and title/intro/controlled credits regression; no other-bank-consumer absence/global corpus proof','No whole gameplay/audio/reset/savestate/physical console/final translation review; development draft','Graphics only, code/CPU cycles unchanged; no new standalone CPU test required']};(R/'qa/reports/map038_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
