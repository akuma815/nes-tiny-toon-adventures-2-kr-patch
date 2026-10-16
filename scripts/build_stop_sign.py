"""046 STOP→vertical Hangul, isolated224/225 and native train font-table value."""
from pathlib import Path
import argparse,json,hashlib
from PIL import Image,ImageFont,ImageDraw
from extract_title_png import decode,encode
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def run(blob,course,level,flags):
 m=Memory(blob);m.banks=[22,23,30,31];cpu=MPU(memory=m);m.cpu=cpu;cpu.pc=0xd1bf;cpu.p=flags;cpu.a=97;cpu.x=17;cpu.y=31;cpu.sp=0xfd;m.ram[0x25]=course;m.ram[0x79]=level;m.ram[0x1fe:0x200]=bytes([0xff,0xc0]);steps=0
 while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<100
 return cpu,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists();sm=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/sm['path']).read_bytes();assert sha(source)==sm['sha256'];prior=(R/'build/dialogue_kr_poc_045/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='15e9f17dcbaaa02778e6a28d5dcf9c318232508ca5fb0346a6e6303a2ff15350';c=json.loads((R/'extracted/graphics/stop_001/consumer.json').read_text('utf-8'));assert c['status']=='PASS_STOP_CONSUMER_RGB_ROUNDTRIP';draft=json.loads((R/'workspace/translation/stop_graphics_draft_001.json').read_text('utf-8'));assert draft['translation_ko']=='정지'
 raw=bytearray(prior[0x51010:0x51810]);assert raw==source[0x31010:0x31810];original=Image.open(R/'extracted/graphics/stop_001/stop_indices.png').convert('L');index=original.copy();fields={z['y']:(z['left'],z['right'])for z in c['inner_label_fields']};mask=set()
 for y,(left,right)in fields.items():
  for x in range(left,right):mask.add((x,y));assert original.getpixel((x,y))in(1,2);index.putpixel((x,y),2)
 atlas=Image.open(R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').convert('RGBA');font=ImageFont.truetype(str(R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'),8);glyphs={}
 for ch,top in zip(draft['translation_ko'],(8,16)):
  im=Image.new('L',(8,8));ImageDraw.Draw(im).text((0,-1),ch,font=font,fill=255);bits=[int(v>127)for v in im.get_flattened_data()];n=ord(ch)-0xac00;ref=atlas.crop((n%64*8,n//64*8,n%64*8+8,n//64*8+8));assert bits==[int(v[3]>0 and max(v[:3])>127)for v in ref.get_flattened_data()]and im.getbbox()==(0,0,6,7);glyphs[ch]=bits
  for y in range(7):
   left,right=fields[top+y];assert right-left>=6
   for x in range(6):
    if bits[y*8+x]:assert(left+x,top+y)in mask;index.putpixel((left+x,top+y),1)
 for y in range(32):
  for x in range(24):assert(x,y)in mask or index.getpixel((x,y))==original.getpixel((x,y))
 for y in range(4):
  for x in range(3):
   code=c['NT_tile_codes'][y*3+x];tile=encode(bytes(index.crop((x*8,y*8,x*8+8,y*8+8)).get_flattened_data()));assert decode(tile)==bytes(index.crop((x*8,y*8,x*8+8,y*8+8)).get_flattened_data())
   if code not in c['owned_text_tiles']:assert tile==raw[code*16:code*16+16]
   raw[code*16:code*16+16]=tile
 for code in range(128):
  if code not in c['owned_text_tiles']:assert raw[code*16:code*16+16]==prior[0x51010+code*16:0x51020+code*16]
 target=bytearray(prior)+bytearray(8192);target[5]=29;p=c['native_font_table_D20B_course2_Y4_file_operand'];assert prior[p]==68;target[p]=224;target[0x78010:0x78810]=raw;assert len(target)==0x7a010 and not any(target[0x78810:]);assert{i for i,(v,w)in enumerate(zip(prior,target))if v!=w}=={5,p}
 cases=0;cycles=set()
 for course in range(5):
  for level in range(3):
   for flags in range(256):
    aa,am=run(prior,course,level,flags);bb,bm=run(target,course,level,flags);assert(aa.pc,aa.a,aa.x,aa.y,aa.sp,aa.p,aa.processorCycles)==(bb.pc,bb.a,bb.x,bb.y,bb.sp,bb.p,bb.processorCycles);dif=[i for i,(v,w)in enumerate(zip(am.ram,bm.ram))if v!=w];assert dif==([0x34]if course==2 else[]) and am.banks==bm.banks
    if course==2:assert(am.ram[0x34],bm.ram[0x34])==(68,224)
    cycles.add(aa.processorCycles);cases+=1
 writes=json.loads((R/'build/dialogue_kr_poc_045/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for z in writes:
  p=z['file_offset']
  if p==0x20010:z['length']=len(target)-p;z['composition']='Prior045 PRG/CHR retained, newSTOP bank224225,226..231 zero'
  if p==5:z['owner']='CHR128_to232_KiB'
  n=z['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(z['expected_hex']);z['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(z['final_hex'])
 assert expected==target;colors={int(k):tuple(v)for k,v in c['palette'].items()};png=Image.new('RGB',index.size)
 for y in range(32):
  for x in range(24):png.putpixel((x,y),colors[index.getpixel((x,y))])
 plan={**c,'work':80,'translation_ko':draft['translation_ko'],'new_font_banks':[224,225],'new_font_range':[0x78010,0x78810],'font_hex':raw.hex(),'font_sha256':sha(raw),'glyphs':glyphs,'indices_hex':bytes(index.get_flattened_data()).hex(),'only_inner_label_pixels_changed':True,'native_full_loader_ABI_cases':cases,'loader_cycles_exact':sorted(cycles),'font_method':'Galmuri7 2.403/OFL verified6x7 native ink, vertical/sheared, no AI','font_ttf_sha256':sha((R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf').read_bytes()),'font_atlas_sha256':sha((R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png').read_bytes()),'status':'draft_runtime_pending'}
 report={'work':80,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'native_full_loader_ABI_cases':cases,'loader_cycles_exact':sorted(cycles),'only_header_CHRsize_one_font_table_and_new_bank224225_changed':True,'prior_ROM_body_Korean_fonts_original68_69_train216_219_unchanged':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'STOP Korean draft; full loaderCPU, source rebuild; actualruntime/humanapproval pending'}
 out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target);(out/'stop_font.bin').write_bytes(raw);index.save(out/'stop_indices.png');png.save(out/'stop_kr.png');png.resize((192,256),Image.Resampling.NEAREST).save(out/'stop_kr_8x.png')
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('stop_graphics_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n','utf-8')
 (out/'builder_used.py').write_bytes(Path(__file__).read_bytes());(out/'draft_used.json').write_bytes((R/'workspace/translation/stop_graphics_draft_001.json').read_bytes());print(json.dumps(report,indent=2))
if __name__=='__main__':main()
