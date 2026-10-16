"""Work94 paired047/046 seeded currency branch and castle gameplay regression."""
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
def native_pairs(old,new,seed):
 mems=[]
 for rom in(old,new):
  mem=bytearray(65536);mem[:2048]=seed;mem[0x8000:0xc000]=rom[0x24010:0x28010];mems.append(mem)
 admitted=(0,*range(0x740,0x754));pairs={i:{(seed[i],seed[i])}for i in admitted};calls=0
 for slot in(22,23,24,26,27,24,25,28,44):
  ptr=int.from_bytes(old[0x55a9+2*slot:0x55ab+2*slot],'little')
  for mem in mems:mem[0x6cd:0x6cf]=ptr.to_bytes(2,'little');mem[0x6c3]=mem[0x6c4]=0
  cpus=[MPU(memory=mem)for mem in mems]
  for _ in range(200):
   for c,mem in zip(cpus,mems):
    c.pc=0x937c;c.sp=0xfd;mem[0x1fe:0x200]=bytes.fromhex('ff c0');steps=0
    while c.pc!=0xc100:c.step();steps+=1;assert steps<10000
   assert cpus[0].processorCycles==cpus[1].processorCycles;calls+=1;pairs[0].add((cpus[0].a,cpus[1].a))
   for i in admitted:pairs[i].add((mems[0][i],mems[1][i]))
   assert(cpus[0].a in(254,255))==(cpus[1].a in(254,255))
   if cpus[0].a==254:
    for mem in mems:mem[0x6c4]=0
   if cpus[0].a==255:break
  else:raise AssertionError('reader termination')
 return pairs,calls
def main():
 output=R/'qa/reports/gate094_validation.json';assert not output.exists()
 old=read('build/dialogue_kr_poc_046/TinyToon2_dialogue_kr_poc.nes');new=read('build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes');previous=j('qa/reports/gate091_validation.json');assert sha(old)==previous['prior046_sha256']and sha(new)==previous['output_sha256']
 m=j('manifests/source_rom.json');assert sha(read(m['path']))==m['sha256'];info=j('build/dialogue_kr_poc_047/gate_editorial_mapping.json');result={}
 for route,frames in(('gold4',9000),('normal50',9000),('normal49',6000)):
  prefixes=[f'qa/dialogue/gate094_{route}{build}'for build in('046','047')];A,B=[R/p for p in prefixes];envs=[j(p+'/environment.json')for p in prefixes]
  for prefix,e,rom in zip(prefixes,envs,(old,new)):
   assert e['exit_code']==0 and e['frames']==frames and e['rom_sha256']==sha(rom)
   for name,h in e['files'].items():assert sha(read(prefix+'/'+name))==h
   assert read(prefix+'/trace_complete.txt')==str(frames).encode()
  assert all(envs[0][k]==envs[1][k]for k in('source_sha256','exe_sha256','lua_sha256','config_sha256','frames','input','intervention','seed','seed_file_sha256'))
  assert envs[1]['seed']['frame']==1000 and 'not normal gameplay'in envs[1]['intervention']
  for suffix in('seed_writes.csv','menu_events.csv'):assert read(prefixes[0]+'/'+suffix)==read(prefixes[1]+'/'+suffix)
  pairs,calls=native_pairs(old,new,read(prefixes[0]+'/frame_01590_ram.bin'));images=sorted(B.glob('frame_*.png'));assert[f.name for f in images]==[f.name for f in sorted(A.glob('frame_*.png'))];changed=[];ramdiff=Counter();mapped=0;gameplay=0
  for f in images:
   tag=f.stem;a=read(prefixes[0]+'/'+tag+'_ram.bin');b=read(prefixes[1]+'/'+tag+'_ram.bin')
   for i,(x,y)in enumerate(zip(a,b)):
    if x==y:continue
    ramdiff[hex(i)]+=1
    if i==0x103:assert(x,y)==(a[0],b[0])and(x,y)in pairs[0]
    else:assert i in pairs and(x,y)in pairs[i],(route,tag,hex(i),x,y)
   for suffix in('_oam.bin','_mapping.csv','_state.txt'):assert read(prefixes[0]+'/'+tag+suffix)==read(prefixes[1]+'/'+tag+suffix)
   p=read(prefixes[0]+'/'+tag+'_ppu.bin');q=read(prefixes[1]+'/'+tag+'_ppu.bin');maps=rows(prefixes[1]+'/'+tag+'_mapping.csv');bank=int(next(x['relative_offset']for x in maps if x['kind']=='chr'and x['cpu_or_ppu_address']=='0000'),16)//0x400
   if bank==175:assert p[:0x800]==old[0x6bc10:0x6c410]and q[:0x800]==new[0x6bc10:0x6c410];mapped+=1
   else:assert p[:0x800]==q[:0x800]
   nt=bytearray(q[0x2000:0x3f00]);pn=p[0x2000:0x3f00]
   if bank==175:
    for row,line in enumerate(info['layout']):
     for alias in range(0,0x1c01,0x400):
      off=alias+0x2a8+row*0x40;nt[off:off+line['expanded_tiles']]=pn[off:off+line['expanded_tiles']]
   assert nt==pn and p[0x800:0x2000]==q[0x800:0x2000]and p[0x3f00:]==q[0x3f00:]
   diff=ImageChops.difference(Image.open(f).convert('RGB'),Image.open(A/f.name).convert('RGB'));bbox=diff.getbbox()
   if bbox:
    assert bank==175 and b[0x34]==175;changed.append({'frame':int(tag[6:]),'bbox':bbox,'selected_slot':b[0x6cf]})
    for row,line in enumerate(info['layout']):diff.paste(0,(64,168+16*row,64+8*line['expanded_tiles'],176+16*row))
   assert diff.getbbox()is None,(route,tag,'outside gate rows')
   if b[0x18]==4 and b[0x54]==5 and b[0x25]==4:
    assert bbox is None and a==b and p==q;gameplay+=1
  events=[x for x in rows(prefixes[1]+'/menu_events.csv')if x['kind']=='exec'and x['address']=='9445'];slots=[x['id']for x in events];last=read(prefixes[1]+f'/frame_{frames:05d}_ram.bin');normal=sum(last[0x7d0+i]*10**i for i in range(3));gold=last[0x7e0]
  assert len(changed)>0 and mapped>0 and '17'in slots
  if route=='gold4':assert '1C'in slots and gameplay>0 and gold==4 and normal==10
  elif route=='normal50':assert '1A'in slots and '1C'in slots and gameplay>0 and gold==0 and normal==0
  else:assert '19'in slots and '1C'not in slots and gameplay==0 and gold==0 and normal==49 and last[0x18]==8
  # All routes show the modified condition before their own acceptance/rejection.
  p=read(prefixes[1]+'/frame_01920_ppu.bin');actual=Image.open(B/'frame_01920.png').convert('RGB');font=new[0x6bc10:0x6c410]
  for row,line in enumerate(info['layout']):
   codes=bytes.fromhex(line['expanded_hex']);assert p[0x22a8+row*0x40:0x22a8+row*0x40+len(codes)]==codes;expected=Image.new('RGB',(len(codes)*8,8),'black')
   for col,code in enumerate(codes):
    pixels=decode(font[code*16:(code+1)*16]);assert set(pixels)<={0,2}
    for k,v in enumerate(pixels):
     if v:expected.putpixel((col*8+k%8,k//8),(255,254,255))
   assert ImageChops.difference(actual.crop((64,168+16*row,64+8*len(codes),176+16*row)),expected).getbbox()is None
  result[route]={'frames_each':frames,'screens_each':len(images),'frozen_runtime_files_each':len(envs[1]['files']),'changed_gate_rows_only':changed,'whole_frames_equal':len(images)-len(changed),'font175176_actual_PPU_exact_samples':mapped,'native_reader_calls':calls,'RAM_glyph_pair_differences':dict(ramdiff),'whole_OAM_mapping_state_and_menu_seed_logs_exact':True,'castle_gameplay_screens_whole_RAM_PPU_PNG_exact':gameplay,'native_slots':slots,'final_normal':normal,'final_gold':gold,'final_root':hex(last[0x18]),'final_phase':hex(last[0x54]),'final_course':last[0x25]}
 proof={'work':94,'status':'PASS_GATE047_SEEDED_BRANCH_REGRESSION','ROM_sha256':sha(new),'prior046_sha256':sha(old),'CSV_sha256':sha(read('workspace/translation/text_ja.csv')),'routes':result,'source_unchanged':True,'intervention':'Exactly recorded one-time currency RAM seed at1000, thereafter controller only; no ROM/state/health edits','human_final_review':False,'limits':['Currency was seeded, not naturally earned; gold4/normal50/normal49 branch proof only','No full castle or whole-game completion/047 save-reset/PCM listening/hardware/final human approval','Frozen review047 archive retains truthful pre-work94 scope; this work is supplemental runtime evidence']}
 output.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':proof['status'],'routes':{k:{a:b for a,b in v.items()if a not in('changed_gate_rows_only','RAM_glyph_pair_differences')}for k,v in result.items()}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()