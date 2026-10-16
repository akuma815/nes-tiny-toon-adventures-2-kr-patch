"""Same-cycle home font latch infrastructure; no new text selected."""
import argparse,hashlib,json
from pathlib import Path
from asm6502 import assemble,verify_profile
from verify_ui_latch_hooks import compare,irq,Memory,MPU
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
def home_irq(rom,profile,encoded=0):
 mem=Memory(rom);cpu=MPU(memory=mem);mem.cpu=cpu;cpu.pc=0xfb0d;cpu.sp=0xf6;mem.ram[0x6ea]=profile;mem.ram[0x6f3]=encoded
 while cpu.pc!=0xfd13:cpu.step()
 return cpu.processorCycles,mem.writes,mem.ram[0xc6],mem.ram[0xc7]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);z=ap.parse_args();m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256']
 pdir=ROOT/'build/dialogue_kr_poc_014';prior=(pdir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='d86875bf3e2411ff92ebcd511507473aefa3d4d622d2c6bb8a5bab1da8690c12';writes=j('build/dialogue_kr_poc_014/expected_writes.json');model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 csv=(ROOT/'workspace/translation/text_ja.csv').read_bytes();assert sha(csv)=='76bcc0d985c41dff6ce19cf0dd1a8a02e58bbb6814ca0b2f26e9e8239b9e8c48'
 asm=ROOT/'workspace/asm/dialogue_page_font_004.asm';code,listing,symbols=assemble(asm.read_text('utf-8'),0x95f9);assert 0x95f9+len(code)<0x9700
 init,il,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @page_init\nPLA\nSTA $2B\nLDA $06CE\nPLP\nLDY #$00\nRTS',0x9430,symbols);init=init.ljust(25,b'\xea')
 setup,sl,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @intro_setup\nPLA\nSTA $2B\nPLP\nLDA #$01\nLDY #$FF\nCLC\nCLV\nINC $06DE\nRTS',0x8e88,symbols);setup=setup.ljust(27,b'\xea')
 hcode,hl,_=assemble((ROOT/'workspace/asm/home_font_latch_001.asm').read_text('utf-8'),0xfb0d);assert len(hcode)==0xfb34-0xfb0d
 output=bytearray(prior);old_len=107;output[0x5609:0x5609+max(old_len,len(code))]=source[0x5609:0x5609+max(old_len,len(code))];output[0x5609:0x5609+len(code)]=code
 for base in (0x10,0x20010):output[base+0x5430:base+0x5449]=init;output[base+0x4e88:base+0x4ea3]=setup
 output[0x5710+0x0a*2]=130
 for base in (0x10,0x20010):output[base+0x1fb0d:base+0x1fb34]=hcode
 # No data/font/header/macro changes in this infrastructure build.
 assert output[0x40010:]==prior[0x40010:] and output[0x25609:0x25a28]==prior[0x25609:0x25a28] and output[0x261b1:0x261ff]==prior[0x261b1:0x261ff]
 for initial in (0,1,90,128,132,134,136,138,140,142,144,146,255):
  for slot in range(48):
   delta,font=compare(prior,output,0x9417,slot,0,0x34,0,initial);assert delta==0
 assert compare(prior,output,0x8e88,1,0,0x34,0)[0]==0 and irq(prior)==irq(output)
 irq_cases=0
 for profile in range(3):
  old=home_irq(prior,profile)
  for font in (90,128,130,132,134,136,138,140,142,144,146,148):
   new=home_irq(output,profile,font^90);assert old[0]==new[0] and old[3]==new[3] and new[2]==font
   assert [(a,t) for a,v,t in old[1]]==[(a,t) for a,v,t in new[1]]
   assert all(a[1]==b[1] for a,b in zip(old[1],new[1]) if a[0] not in (0xa000,0xa008));irq_cases+=1
 for w in writes:
  p,n=w['file_offset'],w['length'];w['final_hex']=output[p:p+n].hex()
 start=0x1fb1d;writes.append({'owner':'same_cycle_home_encoded_font_latch_FB0D_FB34','file_offset':start,'length':len(hcode),'expected_hex':source[start:start+len(hcode)].hex(),'final_hex':hcode.hex()})
 owned=set();model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];region=set(range(p,p+n));assert not owned&region;owned|=region;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==output
 out=z.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 report={'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','PRG_KiB':256,'CHR_KiB':152,'csv_sha256':sha(csv),'helper_code_bytes':len(code),'latch_RAM':0x6f3,'latch_encoding':'font bank XOR5A; default0 decodes original90','expected_writes':len(writes),'CPU_page_seed_cases':624,'home_IRQ_font_profile_cases':irq_cases,'all_page_setup_cycles_equal_prior014':True,'home_IRQ_write_cycles_equal_prior014':True,'original_text_fonts_and_macros_unchanged':True,'scope':'Infrastructure for home/booth/stage text fonts; all9 intro and existing home drafts retained;10 drafts, no release','runtime':'NOT YET RUN;06F3 ownership scoped to observed routes; PPU2002 redundant-read removal needs actual verification','ISA':verify_profile()}
 for name,data in [('expected_writes.json',writes),('asm_listing.json',{'helper':listing,'home_irq':hl,'init':il,'setup':sl,'symbols':symbols}),('build_report.json',report)]:
  (out/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for name,p in [('page_font_used.asm',asm),('home_font_used.asm',ROOT/'workspace/asm/home_font_latch_001.asm'),('translation_used.csv',ROOT/'workspace/translation/text_ja.csv'),('builder_used.py',Path(__file__)),('asm6502_used.py',ROOT/'scripts/asm6502.py')]:
  (out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
