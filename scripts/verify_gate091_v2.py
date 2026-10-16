"""Work91 exact paired castle scene comparison, source reader pairs and RGB proof."""
from pathlib import Path
import json,csv,hashlib
from collections import Counter
from PIL import Image,ImageChops
from verify_dialogue_home import MPU
from extract_title_png import decode
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads(read(p).decode('utf-8'))
def rows(p):return list(csv.DictReader(read(p).decode('utf-8').splitlines()))
def main():
 out=R/'qa/reports/gate091_validation.json';assert not out.exists()
 old=read('build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes');new=read('build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes');m=j('manifests/source_rom.json');source=read(m['path']);assert sha(source)==m['sha256']
 build=j('build/dialogue_kr_poc_047/build_report.json');assert sha(old)==build['prior_adopted_sha256'] and sha(new)==build['output_sha256']
 changedbytes=[i for i,(a,b)in enumerate(zip(old,new))if a!=b];assert len(old)==len(new)==499728 and len(changedbytes)==129 and all(0x257c1<=i<0x257e5 or 0x6bc10<=i<0x6c410 for i in changedbytes)
 model=bytearray(source);owned=set()
 for w in j('build/dialogue_kr_poc_047/expected_writes.json'):
  i,n=w['file_offset'],w['length'];area=set(range(i,i+n));assert not area&owned;owned|=area;assert source[i:i+n]==bytes.fromhex(w['expected_hex']);model[i:i+n]=bytes.fromhex(w['final_hex'])
 assert model==new
 info=j('build/dialogue_kr_poc_047/gate_editorial_mapping.json');assert info['profile']['font_bank']==175
 dirs=['qa/dialogue/gate091_castle046','qa/dialogue/gate091_castle047'];envs=[]
 for directory,rom in zip(dirs,(old,new)):
  e=j(directory+'/environment.json');assert e['exit_code']==0 and e['rom_sha256']==sha(rom) and e['frames']==5400
  for p,h in e['files'].items():assert sha(read(directory+'/'+p))==h
  envs.append(e)
 assert all(envs[0][k]==envs[1][k]for k in ('source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention'))
 assert envs[0]['intervention']=='controller input only; no state loading or RAM/ROM writes'
 # Derive allowed scratch/buffer pairs from the actual native reader, including
 # the later page selected while the earlier sentence still waits on screen.
 seed=read(dirs[0]+'/frame_01590_ram.bin');mems=[]
 for rom in (old,new):
  mem=bytearray(65536);mem[:2048]=seed;mem[0x8000:0xc000]=rom[0x24010:0x28010];mems.append(mem)
 admitted=(0,*range(0x740,0x754));pairs={i:{(seed[i],seed[i])}for i in admitted};calls=0
 for slot in (22,23,24,26,27,24,25):
  ptr=int.from_bytes(old[0x55a9+2*slot:0x55ab+2*slot],'little');assert ptr==int.from_bytes(new[0x55a9+2*slot:0x55ab+2*slot],'little')
  for mem in mems:mem[0x6cd:0x6cf]=ptr.to_bytes(2,'little');mem[0x6c3]=mem[0x6c4]=0
  cpus=[MPU(memory=mem)for mem in mems]
  for _ in range(200):
   for c,mem in zip(cpus,mems):
    c.pc=0x937c;c.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');steps=0
    while c.pc!=0xc100:c.step();steps+=1;assert steps<10000
   assert cpus[0].processorCycles==cpus[1].processorCycles;calls+=1;pairs[0].add((cpus[0].a,cpus[1].a))
   for i in admitted:pairs[i].add((mems[0][i],mems[1][i]))
   assert (cpus[0].a in (254,255))==(cpus[1].a in (254,255))
   if cpus[0].a==254:
    for mem in mems:mem[0x6c4]=0
   if cpus[0].a==255:break
  else:raise AssertionError('reader termination')
 # Both native interrupt entries save A with PHA; one observed old stack byte
 # is admitted only when it equals that same observed glyph scratch value.
 assert old[0x3fa6b:0x3fa6c]==new[0x3fa6b:0x3fa6c]==b'\x48' # CPU FA5B
 assert old[0x3fe93:0x3fe94]==new[0x3fe93:0x3fe94]==b'\x48' # CPU FE83
 A,B=[R/p for p in dirs];images=sorted(B.glob('frame_*.png'));assert[f.name for f in images]==[f.name for f in sorted(A.glob('frame_*.png'))]
 ramdiff=Counter();changed=[];mapped=0;stack=0;protected=0
 for f in images:
  tag=f.stem;a=read(dirs[0]+'/'+tag+'_ram.bin');b=read(dirs[1]+'/'+tag+'_ram.bin')
  for i,(x,y)in enumerate(zip(a,b)):
   if x==y:continue
   ramdiff[hex(i)]+=1
   if i==0x103:
    assert(x,y)==(a[0],b[0]) and (x,y)in pairs[0];stack+=1
   else:assert i in pairs and(x,y)in pairs[i],(tag,hex(i),x,y)
  for suffix in ('_oam.bin','_mapping.csv','_state.txt'):assert read(dirs[0]+'/'+tag+suffix)==read(dirs[1]+'/'+tag+suffix)
  p=read(dirs[0]+'/'+tag+'_ppu.bin');q=read(dirs[1]+'/'+tag+'_ppu.bin');maps=rows(dirs[1]+'/'+tag+'_mapping.csv');bank=int(next(x['relative_offset']for x in maps if x['kind']=='chr'and x['cpu_or_ppu_address']=='0000'),16)//0x400
  if bank==175:
   assert p[:0x800]==old[0x6bc10:0x6c410] and q[:0x800]==new[0x6bc10:0x6c410];mapped+=1
  else:assert p[:0x800]==q[:0x800]
  nt=bytearray(q[0x2000:0x3f00]);pn=p[0x2000:0x3f00]
  if bank==175:
   for row,line in enumerate(info['layout']):
    for alias in range(0,0x1c01,0x400):
     off=alias+0x2a8+row*0x40;nt[off:off+line['expanded_tiles']]=pn[off:off+line['expanded_tiles']]
  assert nt==pn and p[0x800:0x2000]==q[0x800:0x2000]and p[0x3f00:]==q[0x3f00:]
  diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(A/f.name).convert('RGB'));bbox=diff.getbbox()
  if bbox:
   assert bank==175 and b[0x34]==175 and b[0x6cf]in(23,24);changed.append({'frame':int(tag[6:]),'bbox':bbox,'selected_slot':b[0x6cf]})
   for row,line in enumerate(info['layout']):diff.paste(0,(64,168+16*row,64+8*line['expanded_tiles'],176+16*row))
  assert diff.getbbox()is None,(tag,'outside gate rows');protected+=1
 assert len(images)==396 and len(changed)==36 and mapped==37 and stack==4
 # Complete real nametable and screenshot are independently reconstructed from
 # the target native page/font: no synthetic game background is substituted.
 p=read(dirs[1]+'/frame_01920_ppu.bin');actual=Image.open(B/'frame_01920.png').convert('RGB');font=new[0x6bc10:0x6c410];nativeRGB=[]
 for row,line in enumerate(info['layout']):
  codes=bytes.fromhex(line['expanded_hex']);assert p[0x22a8+row*0x40:0x22a8+row*0x40+len(codes)]==codes
  expected=Image.new('RGB',(len(codes)*8,8),'black')
  for col,code in enumerate(codes):
   pixels=decode(font[code*16:(code+1)*16]);assert set(pixels)<={0,2}
   for k,v in enumerate(pixels):
    if v:expected.putpixel((col*8+k%8,k//8),(255,254,255))
  crop=actual.crop((64,168+16*row,64+8*len(codes),176+16*row));assert ImageChops.difference(crop,expected).getbbox()is None;nativeRGB.append(line['desired'])
 events=[rows(p+'/menu_events.csv')for p in dirs];assert events[0]==events[1]
 execs=[x for x in events[1]if x['kind']=='exec'];assert any(x['id']=='17'and x['address']=='9445'and x['pointer']=='97B1'and x['font']=='AF'for x in execs)
 assert all(x['gold_tickets']=='00'for x in execs)
 # Work90 count erratum comes from the actual immutable map and directories.
 files=sorted(p.name for p in (R/'build/dialogue_kr_poc_047').iterdir()if p.is_file());rebuild='build/dialogue_kr_poc_047_rebuild090'
 assert len(files)==9 and len(j('qa/reports/gate090_validation.json')['independent_rebuild_exact_files'])==9
 for name in files:assert read('build/dialogue_kr_poc_047/'+name)==read(rebuild+'/'+name)
 result={'work':91,'status':'PASS_GATE047_NATURAL_RUNTIME','adopted_build':'dialogue_kr_poc_047','source_sha256':sha(source),'prior046_sha256':sha(old),'output_sha256':sha(new),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'identical_controller_only_frames_each':5400,'matched_screens':len(images),'whole_screens_equal':len(images)-len(changed),'changed_gate_two_rows_only':changed,'protected_OAM_mapping_and_full_state_text_exact':True,'game_RAM_exact_except_native_reader_proven_pairs':dict(ramdiff),'stack103_saved_glyph_A_pairs':stack,'native_reader_replay_calls':calls,'actual_font175176_PPU_exact_samples':mapped,'complete_native_NT_and_exact_RGB_rows':nativeRGB,'menu_events_all_fields_exact':len(events[1]),'actual_exec_events':len(execs),'runtime_files_each':len(envs[0]['files']),'work90_rebuild_count_erratum':{'documented':8,'actual':9,'frozen_old_document_preserved':True},'human_final_review':False,'visual_review':'Actual047 partial1812, complete1920, row clear2106 and next page2130 reviewed; no simulated game images','limits':['Native zero-gold insufficient admission route only; no new natural gold4 successful admission proof','No new047 wholeplay/reset/savestate/PCM listening/physical console or final human translation approval','Historical review046 kit/package use their frozen old CSV and remain historical; refresh pending','Registered54units/33graphics are a bounded inventory, not a global corpus closure']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k!='changed_gate_two_rows_only'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()