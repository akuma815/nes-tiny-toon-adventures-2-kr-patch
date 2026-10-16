"""Independent reconstructed booth labels/font plus exact protected runtime."""
import json,hashlib,csv
from pathlib import Path
from PIL import Image,ImageChops,ImageFont,ImageDraw
from extract_title_png import encode,decode
from verify_gate_font_tag import env
from build_booth_graphics import producer
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_bytes()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 prior=read('build/dialogue_kr_poc_038/TinyToon2_dialogue_kr_poc.nes');rom=read('build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.nes');manifest=j('manifests/source_rom.json');source=read(manifest['path']);assert sha(source)==manifest['sha256'];plan=j('build/dialogue_kr_poc_039/booth_plan_used.json');expected=bytearray(prior);atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');face=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);font=bytearray(prior[0x5f010:0x5f810]);assert font==source[0x3f010:0x3f810];fontcodes=set()
 for g in plan['glyphs']:
  code,c=g['code'],g['char'];assert '\uac00'<=c<='\ud7a3' and code not in fontcodes; fontcodes.add(code);n=ord(c)-0xac00;x=n%64*8;y=n//64*8;bits=[int(v[3]>0 and max(v[:3])>127) for v in atlas.crop((x,y,x+8,y+8)).get_flattened_data()];im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),c,font=face,fill=255);assert any(bits) and bits==[int(v>127) for v in im.get_flattened_data()];raw=encode(bytes(2*v for v in bits));assert raw.hex()==g['chr_hex'];font[code*16:(code+1)*16]=raw
 assert len(fontcodes)==12 and bytes(font).hex()==plan['font_hex'];expected[0x73010:0x73810]=font;nt_pairs={};glyph_pairs=set()
 for p in plan['labels']:
  old,new=bytes.fromhex(p['source_hex']),bytes.fromhex(p['body_hex']);assert len(old)==len(new)==p['length'];assert ''.join({v:k for k,v in plan['mapping'].items()}[v] for v in new)==p['desired_padded'];assert p['desired_padded'].strip()==p['translation_ko']
  for off in (p['source_file_offset'],p['expanded_file_offset']):assert prior[off:off+p['length']]==old;expected[off:off+p['length']]=new
  for i,(a,b) in enumerate(zip(old,new)):
   glyph_pairs.add((a,b));addr=p['NT']+i
   for alias in (addr,addr^0x400,addr+0x1000,(addr^0x400)+0x1000):nt_pairs[alias]=(a,b)
 for off in (0x5ca6,0x25ca6):assert prior[off]==124;expected[off]=204
 for c in plan['header']['changes']:
  off=c['expanded_file_offset'];assert prior[off:off+16]==bytes.fromhex(c['source_raw_hex']);expected[off:off+16]=bytes.fromhex(c['final_hex'])
 assert expected==rom and rom[0x5f010:0x5f810]==prior[0x5f010:0x5f810] and rom[0x72410:0x72c10]==prior[0x72410:0x72c10];expected=bytearray(source);covered=set()
 for w in j('build/dialogue_kr_poc_039/expected_writes.json'):
  off,n=w['file_offset'],w['length'];area=set(range(off,off+n));assert not area&covered;covered|=area;assert source[off:off+n]==bytes.fromhex(w['expected_hex']);expected[off:off+n]=bytes.fromhex(w['final_hex'])
 assert expected==rom and rom==read('build/dialogue_kr_poc_039_rebuild/TinyToon2_dialogue_kr_poc.nes')==read('qa/dialogue/한글 패치 적용 039/TinyToon2_booth039_applied.nes');assert read('build/dialogue_kr_poc_039/translation_used.csv')==read('workspace/translation/text_ja.csv')
 cases=0
 for flags in range(256):
  for initial in (0,124,255):
   a,ma=producer(prior,flags,initial);b,mb=producer(rom,flags,initial);assert (a.a,a.x,a.y,a.sp,a.p,a.processorCycles)==(b.a,b.x,b.y,b.sp,b.p,b.processorCycles) and a.processorCycles==10 and {i for i in range(2048) if ma.ram[i]!=mb.ram[i]}=={0x34};assert (ma.ram[0x34],mb.ram[0x34])==(124,204);cases+=1
 decoder=j('qa/reports/booth039_native_decoder.json');assert decoder['status']=='PASS' and decoder['cycles']==19415 and decoder['original_decoder_128_D_clear_flag_cases']==128
 survey=j('extracted/graphics/booth_001/consumer.json');orig=read('extracted/graphics/booth_001/header_source_indices.bin');native=read('workspace/graphics/booth_header_kr_001/indices.bin');assert len(native)==96*16 and sha(native)==plan['header']['indices_sha256'];assert all(orig[y*96+x]==native[y*96+x] for y in range(16) for x in range(96) if not(3<=x<93 and 3<=y<13));checks=[];numbers=set();ram_changes={};font_samples=0;header_samples=0
 for ref,new in [('booth038_native','booth039_native'),('booth038_points3','booth039_points3'),('map038_tour','booth039_tour'),('map038_intro','booth039_intro'),('map038_credits','booth039_credits')]:
  ea,eb=env(ref,prior),env(new,rom);assert all(ea[k]==eb[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
  if 'seed' in ea:assert ea['seed']==eb['seed'] and ea['seed_file_sha256']==eb['seed_file_sha256']
  files=sorted((R/'qa/dialogue'/new).glob('frame_*.png'));assert files and [f.name for f in files]==[f.name for f in sorted((R/'qa/dialogue'/ref).glob('frame_*.png'))];changed=0
  for f in files:
   tag=f.stem;frame=int(tag[6:]);a=read(f'qa/dialogue/{ref}/{tag}_ram.bin');b=read(f'qa/dialogue/{new}/{tag}_ram.bin');rp=read(f'qa/dialogue/{ref}/{tag}_ppu.bin');ppu=read(f'qa/dialogue/{new}/{tag}_ppu.bin')
   for i in range(2048):
    if a[i]!=b[i]:assert i in (0x34,0x3a) and (a[i],b[i])==(124,204),(new,tag,hex(i),a[i],b[i]);ram_changes[hex(i)]=ram_changes.get(hex(i),0)+1
   assert read(f'qa/dialogue/{ref}/{tag}_oam.bin')==read(f'qa/dialogue/{new}/{tag}_oam.bin');assert ppu[0x3f00:]==rp[0x3f00:]
   for addr in range(0x2000,0x3f00):
    if ppu[addr]!=rp[addr]:assert nt_pairs.get(addr)==(rp[addr],ppu[addr]),(new,tag,'NT',hex(addr),rp[addr],ppu[addr])
   ma,mb=rows(f'qa/dialogue/{ref}/{tag}_mapping.csv'),rows(f'qa/dialogue/{new}/{tag}_mapping.csv');assert len(ma)==len(mb)
   for x,y in zip(ma,mb):
    assert all(x[k]==y[k] for k in ('kind','cpu_or_ppu_address','mem_type'))
    if x['relative_offset']!=y['relative_offset']:assert x['kind']=='chr' and (x['relative_offset'],y['relative_offset']) in (('1F000','33000'),('1F400','33400')),(new,tag,x,y)
    if y['kind']=='chr':
     base=int(y['cpu_or_ppu_address'],16);off=int(y['relative_offset'],16);assert ppu[base:base+0x400]==rom[0x40010+off:0x40410+off];oldoff=int(x['relative_offset'],16);assert rp[base:base+0x400]==prior[0x40010+oldoff:0x40410+oldoff]
     if base==0 and off==204*0x400:font_samples+=1
   image=Image.open(f).convert('RGB');old=Image.open(R/f'qa/dialogue/{ref}/{f.name}').convert('RGB');diff=ImageChops.difference(image,old)
   if diff.getbbox():
    assert (a[0x34],b[0x34])==(124,204),(new,tag,'font lifetime')
    crop=old.crop((80,32,176,48));live={v:{crop.getpixel((x,y)) for y in range(16) for x in range(96) if orig[y*96+x]==v} for v in range(4)};assert all(len(s)==1 for s in live.values()),(new,tag,'header palette consistency');live={v:next(iter(s)) for v,s in live.items()};predicted=Image.new('RGB',(96,16));predicted.putdata([live[v] for v in native]);assert image.crop((80,32,176,48)).tobytes()==predicted.tobytes(),(new,tag,'header native pixels')
    for y in range(16):
     for x in range(96):
      if orig[y*96+x]!=native[y*96+x]:diff.putpixel((80+x,32+y),(0,0,0))
    header_samples+=1
    # Literal labels must be completed and in the native booth NT. Only those
    # exact8x8 cells change; numbers and every other pixel remain protected.
    for p in plan['labels']:
     addr=p['NT'];aa=bytes.fromhex(p['source_hex']);bb=bytes.fromhex(p['body_hex']);assert rp[addr:addr+p['length']]==aa and ppu[addr:addr+p['length']]==bb,(new,tag,p['source'],'completed literal NT')
     y=(addr&0x3ff)//32*8;x=(addr&31)*8
     oldbits=[decode(prior[0x5f010+v*16:0x5f010+(v+1)*16]) for v in aa];newbits=[decode(font[v*16:(v+1)*16]) for v in bb];live={}
     for col,bits in enumerate(oldbits):
      for yy in range(8):
       for xx in range(8):live.setdefault(bits[yy*8+xx],set()).add(old.getpixel((x+col*8+xx,y+yy)))
     assert set(live)=={0,2} and all(len(s)==1 for s in live.values()),(new,tag,p['source'],'source exact glyph palette');live={v:next(iter(s)) for v,s in live.items()};expected_label=Image.new('RGB',(len(bb)*8,8))
     for col,bits in enumerate(newbits):
      for yy in range(8):
       for xx in range(8):expected_label.putpixel((col*8+xx,yy),live[bits[yy*8+xx]])
     assert image.crop((x,y,x+len(bb)*8,y+8)).tobytes()==expected_label.tobytes(),(new,tag,p['source'],'actual Korean label raster')
     for col,(v,w) in enumerate(zip(aa,bb)):
      if v!=w:diff.paste(0,(x+col*8,y,x+(col+1)*8,y+8))
    assert diff.getbbox() is None,(new,tag,'outside header/label glyph cells',diff.getbbox());changed+=1;numbers.add((tuple(b[0x7d0:0x7d3]),tuple(b[0x7f2:0x7f7])))
  checks.append({'reference':ref,'candidate':new,'screens':len(files),'changed_header_labels_only':changed,'whole_frames_equal':len(files)-changed})
 timing=0;font_writes=0
 for ref,new in [('booth038_native_irq','booth039_native_irq'),('booth038_points3_irq','booth039_points3_irq')]:
  a,b=env(ref,prior),env(new,rom);assert all(a[k]==b[k] for k in ('exe_sha256','lua_sha256','config_sha256','frames','input','intervention'));aa,bb=rows(f'qa/dialogue/{ref}/irq_phase.csv'),rows(f'qa/dialogue/{new}/irq_phase.csv');assert len(aa)==len(bb)
  for x,y in zip(aa,bb):
   assert all(x[k]==y[k] for k in ('frame','kind','pc','address','scanline','dot','cycles')),(ref,x,y)
   if x['value']!=y['value']:assert (x['address'],x['value'],y['value']) in (('A000','7C','CC'),('A008','7D','CD')),(ref,x,y);font_writes+=1
  timing+=len(aa)
 result={'status':'PASS','work':42,'adopted_build':'dialogue_kr_poc_039','source_sha256':sha(source),'output_sha256':sha(rom),'IPS_sha256':sha(read('build/dialogue_kr_poc_039/TinyToon2_dialogue_kr_poc.ips')),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'ExpectedWrites':8,'rebuild_actual_IPS_apply_equal':True,'native_producer_768_CPU_cases_10_cycles':cases,'native_decoder_128_D_clear_CPU_cases':128,'native_decoder_cycles':19415,'Hangul_unique':12,'registered_drafts':45,'technical_shared_source_units':9,'graphics_labels':5,'generated_header_tiles':24,'other_native_ascii_digits_fonts_title_map_credits_preserved':True,'matched_screens':sum(x['screens'] for x in checks),'outside_owned_header_label_cells_pixels':0,'protected_game_numeric_actor_PPU_OAM_palette_equal':True,'exact_actual_timestamps':timing,'only_font_write_values_changed':font_writes,'RAM_changes_only_NMI_producer_cache':ram_changes,'actual_font204_samples':font_samples,'actual_header_complete_samples':header_samples,'numeric_states':sorted(numbers),'checks':checks,'visual_review':'Actual normal/success-seeded booth review separate','limits':['Source decoder model is NMOS6502,D-clear only; real NES timing separate','Point3 initial seed is controlled branch, not natural earning/fullplay','Registered-table plus observed five graphic literals, not global corpus/other scene absence proof','Full gameplay/audio/reset/savestate/physical console/final human translation review and priorPRG/RNG caveat pending','039 frozen report12-cycle key label corrected here to actual10 without altering frozen builds']};(R/'qa/reports/booth039_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
