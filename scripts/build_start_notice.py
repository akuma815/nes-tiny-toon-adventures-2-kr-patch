"""045 native START Korean bitmap, isolated222/223 with source ExpectedWrites."""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from extract_title_png import decode,encode
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists()
 sm=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/sm['path']).read_bytes();assert sha(source)==sm['sha256'];prior=(R/'build/dialogue_kr_poc_044/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='58db7fa14239ecd71c0454c097293a3037bb3ce841ef455213b02530b521dbdf';c=json.loads((R/'extracted/graphics/start_001/consumer.json').read_text('utf-8'));draft=json.loads((R/'workspace/translation/start_graphics_draft_001.json').read_text('utf-8'));assert c['status']=='PASS_NATIVE_START_RGB_ROUNDTRIP';text=draft['translation_ko'];assert text=='시작!'
 raw=bytearray(prior[0x5e810:0x5f010]);assert raw==source[0x3e810:0x3f010] and not any(prior[0x77810:0x78010]);atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');font=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);mask=Image.new('L',(96,32));pieces=[];glyphs={}
 for ch in text:
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),ch,font=font,fill=255);bits=[int(v>127)for v in im.get_flattened_data()];assert any(bits)
  if '가'<=ch<='힣':
   n=ord(ch)-0xac00;ref=atlas.crop((n%64*8,n//64*8,n%64*8+8,n//64*8+8));assert bits==[int(v[3]>0 and max(v[:3])>127)for v in ref.get_flattened_data()]and not any(bits[56:]);glyphs[ch]=bits
  box=im.getbbox();im=im.crop((box[0],0,box[2],7));pieces.append(im.resize((im.width*3,21),Image.Resampling.NEAREST))
 length=sum(i.width+3 for i in pieces)-3;x=(96-length)//2;assert x>=2
 for im in pieces:mask.paste(im,(x,5));x+=im.width+3
 outline=mask.filter(ImageFilter.MaxFilter(3));index=Image.new('L',mask.size)
 for y in range(32):
  for x in range(96):
   v=1 if mask.getpixel((x,y))>127 else 2 if x>0 and y>0 and mask.getpixel((x-1,y-1))>127 else 3 if outline.getpixel((x,y))>127 else 0;index.putpixel((x,y),v)
 for y in range(4):
  for x in range(12):
   code=c['font_tile_codes'][y*12+x];bits=bytes(index.crop((x*8,y*8,x*8+8,y*8+8)).get_flattened_data());tile=encode(bits);assert decode(tile)==bits;raw[code*16:code*16+16]=tile
 for code in range(128):
  if code not in c['font_tile_codes']:assert raw[code*16:code*16+16]==prior[0x5e810+code*16:0x5e820+code*16]
 target=bytearray(prior);target[0x77810:0x78010]=raw
 for pos in c['producer_operands']:assert prior[pos-1:pos+3]==bytes([0xa9,122,0x85,0x34 if pos==0x26607 else 0x35]);target[pos]=222
 allowed={*c['producer_operands'],*range(0x77810,0x78010)};diff={i for i,(v,w)in enumerate(zip(prior,target))if v!=w};assert diff<=allowed and len(target)==len(prior)
 cases=0
 for flags in range(256):
  for sub in (0,1,254,255):
   states=[]
   for blob in (prior,target):
    m=Memory(blob);m.banks=[18,19,30,31];cpu=MPU(memory=m);m.cpu=cpu;cpu.pc=0xa5f6;cpu.a=99;cpu.x=17;cpu.y=31;cpu.p=flags;cpu.sp=0xf7;m.ram[0x6de]=sub
    steps=0
    while cpu.pc!=0xa621:cpu.step();steps+=1;assert steps<16
    states.append((cpu,m))
   (aa,am),(bb,bm)=states;assert(aa.pc,aa.p,aa.x,aa.y,aa.sp,aa.processorCycles)==(bb.pc,bb.p,bb.x,bb.y,bb.sp,bb.processorCycles)and aa.processorCycles==19 and(aa.a,bb.a)==(122,222);assert[i for i,(v,w)in enumerate(zip(am.ram,bm.ram))if v!=w]==[0x34,0x35];cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_044/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for z in writes:
  p,n=z['file_offset'],z['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(z['expected_hex']);z['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(z['final_hex'])
 assert expected==target;colors={int(k):v for k,v in c['palette'].items()};png=Image.new('RGB',index.size)
 for y in range(32):
  for x in range(96):png.putpixel((x,y),tuple(colors[index.getpixel((x,y))]))
 plan={**c,'work':77,'translation_ko':text,'draft_sha256':sha((R/'workspace/translation/start_graphics_draft_001.json').read_bytes()),'new_font_banks':[222,223],'font_hex':raw.hex(),'font_sha256':sha(raw),'glyphs':glyphs,'indices_hex':bytes(index.get_flattened_data()).hex(),'font_method':'Galmuri7 2.403/OFL native bitmap, scale3 nearest, onepixel outline/shadow; not AI','font_ttf_sha256':sha((R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf').read_bytes()),'font_atlas_sha256':sha((R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').read_bytes()),'producer_ABI_cases':cases,'producer_cycles_exact':19,'status':'draft_runtime_pending'}
 report={'work':77,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'changed_bytes_from044':len(diff),'only_bank222_223_and_two_producer_immediates':True,'original122_123_prior_notice220_and_fonts_preserved':True,'producer_ABI_cases':cases,'producer_cycles_exact':19,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'START! Korean draft, source/CPU checks; runtime and human approval pending'}
 out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);(out/'start_font.bin').write_bytes(raw);index.save(out/'start_indices.png');png.save(out/'start_kr.png');png.resize((768,256),Image.Resampling.NEAREST).save(out/'start_kr_8x.png')
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('start_graphics_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n','utf-8')
 (out/'builder_used.py').write_bytes(Path(__file__).read_bytes());(out/'draft_used.json').write_bytes((R/'workspace/translation/start_graphics_draft_001.json').read_bytes());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
