"""Reproducible044 notice bank clone; source ExpectedWrites and producer ABI."""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from extract_title_png import encode,decode
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists()
 sm=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/sm['path']).read_bytes();assert sha(source)==sm['sha256'];prior=(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='087f327704908cc5f77cbe77cd5a872564f87660b0918e4efafe77667dbfb91a'
 c=json.loads((R/'extracted/graphics/notices_002/consumer.json').read_text('utf-8'));assert c['status']=='PASS_CONSUMER_RGB_ROUNDTRIP';raw=bytearray(prior[0x4f810:0x4fc10]);assert raw==source[0x2f810:0x2fc10] and not any(prior[0x77010:0x77410])
 atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');font=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);graphics={};glyphs={};labels=[]
 for z in c['labels']:
  text=z['translation_ko'];w,h=z['size'];mask=Image.new('L',(w,h));pieces=[]
  for ch in text:
   if ch==' ':pieces.append((None,4));continue
   im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),ch,font=font,fill=255);bits=[int(v>127) for v in im.get_flattened_data()];assert any(bits)
   if '\uac00'<=ch<='\ud7a3':
    n=ord(ch)-0xac00;ref=atlas.crop((n%64*8,n//64*8,n%64*8+8,n//64*8+8));assert bits==[int(v[3]>0 and max(v[:3])>127)for v in ref.get_flattened_data()] and not any(bits[56:]);glyphs[ch]=bits
   box=im.getbbox();im=im.crop((box[0],0,box[2],7));pieces.append((im,im.width+1))
  length=sum(p[1] for p in pieces)-1;x=(w-length)//2;assert x>=1
  for im,advance in pieces:
   if im:mask.paste(im.resize((im.width,14),Image.Resampling.NEAREST),(x,1))
   x+=advance
  outline=mask.filter(ImageFilter.MaxFilter(3));indices=Image.new('L',(w,h));fg=3 if z['name']=='timeup' else 2
  for yy in range(h):
   for xx in range(w):indices.putpixel((xx,yy),fg if mask.getpixel((xx,yy))>127 else 1 if outline.getpixel((xx,yy))>127 else 0)
  # NES 8x16 sprites use adjacent upper/lower 8x8 tiles.
  for i in range(z['tiles']):
   bits=bytes(indices.crop((i//2*8,i%2*8,i//2*8+8,i%2*8+8)).get_flattened_data());tile=encode(bits);assert decode(tile)==bits;offset=(z['tile_start']+i)*16;raw[offset:offset+16]=tile
  png=Image.new('RGBA',(w,h));colors={int(k):v for k,v in z['palette'].items()}
  for yy in range(h):
   for xx in range(w):v=indices.getpixel((xx,yy));png.putpixel((xx,yy),(*colors[v],255)if v else(0,0,0,0))
  graphics[z['name']+'_kr.png']=png;graphics[z['name']+'_kr_8x.png']=png.resize((w*8,h*8),Image.Resampling.NEAREST);graphics[z['name']+'_indices.png']=indices
  labels.append({**z,'indices_hex':bytes(indices.get_flattened_data()).hex(),'glyph_width':length,'new_CHR_bank':220,'font_method':'Galmuri7 nativebitmap, y2 nearest resize and onepixel outline; deterministic; not AI generated'})
 assert len(glyphs)==9 and raw[448:]==prior[0x4f810+448:0x4fc10]
 target=bytearray(prior);target[0x77010:0x77410]=raw
 for pos in (0x3f7cf,0x3f81f):assert prior[pos-1:pos+3]==bytes([0xa9,62,0x85,0x39]);target[pos]=220
 owned={0x3f7cf,0x3f81f,*range(0x77010,0x77410)};diff={i for i,(a,b)in enumerate(zip(prior,target))if a!=b};assert diff<=owned and {0x3f7cf,0x3f81f}<=diff and len(target)==len(prior)
 cases=0
 for pc in (0xf7be,0xf80e):
  for flags in range(256):
   states=[]
   for rom in (prior,target):
    m=Memory(rom);cpu=MPU(memory=m);m.cpu=cpu;cpu.pc=pc;cpu.p=flags;cpu.a=71;cpu.x=17;cpu.y=113;cpu.sp=0xc7;cpu.step();cpu.step();states.append((cpu,m))
   (aa,am),(bb,bm)=states;assert (aa.pc,aa.p,aa.x,aa.y,aa.sp,aa.processorCycles)==(bb.pc,bb.p,bb.x,bb.y,bb.sp,bb.processorCycles)and aa.processorCycles==5 and (aa.a,bb.a)==(62,220);assert [i for i,(v,w)in enumerate(zip(am.ram,bm.ram))if v!=w]==[0x39];cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_043/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for z in writes:
  p=z['file_offset'];n=z['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(z['expected_hex']);z['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(z['final_hex'])
 assert expected==target
 plan={'work':74,'labels':labels,'glyphs':glyphs,'font_banks':[220],'new_font_range':[0x77010,0x77410],'owned_tiles':list(range(28)),'preserved_tiles':list(range(28,64)),'producer_operands':[0x3f7cf,0x3f81f],'producer_ABI_cases':cases,'producer_cycles':5,'font_sha256':sha(raw),'font_ttf_sha256':sha((R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf').read_bytes()),'font_atlas_sha256':sha((R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').read_bytes()),'font_license':'OFL, existing project Galmuri7 2.403 provenance retained','status':'draft_runtime_pending'}
 report={'work':74,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'changed_bytes_from043':len(diff),'only_new_bank220_and_two_producer_operands':True,'original_CHR_bank62_and_prior_Korean_fonts_unchanged':True,'producer_ABI_cases':cases,'producer_cycles_exact':5,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'Two nativebitmap Korean notices; runtime pending; no finalhumanapproval'}
 out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);(out/'notice_font.bin').write_bytes(raw)
 for name,im in graphics.items():im.save(out/name)
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('notice_graphics_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n','utf-8')
 (out/'builder_used.py').write_bytes(Path(__file__).read_bytes());(out/'translation_used.csv').write_bytes((R/'workspace/translation/text_ja.csv').read_bytes());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
