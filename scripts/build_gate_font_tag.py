"""Commit native castle top font after native initialization; other paths keep exact cycles."""
import argparse,hashlib,json
from pathlib import Path
from asm6502 import assemble,verify_profile
from verify_ui_native_latch_hooks import Memory,MPU,irq
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
def run(rom,slot,phase,active,screen_mode):
 mem=Memory(rom);cpu=MPU(memory=mem);mem.cpu=cpu;cpu.pc=0x9417;cpu.sp=0xfd;cpu.a=0;cpu.x=0x73;cpu.y=0x92;cpu.p=0x34;mem.ram[0x1fe:0x200]=bytes.fromhex('ff c0');mem.ram[0x2b]=0x36;mem.ram[0x6cf]=slot;mem.ram[0x6df]=phase;mem.ram[0x6f3]=active;mem.ram[0xc6]=active;mem.ram[0x34]=90;mem.ram[0x6d0]=screen_mode;steps=0
 while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<10000
 return cpu,mem
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256'];pdir=ROOT/'build/dialogue_kr_poc_024';prior=(pdir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='5ef5a86ce785f61586ebb17cbe11ec4a5e1d5be6e6f3e6ca77c2f4367a425fc8'
 csv=(ROOT/'workspace/translation/text_ja.csv').read_bytes();assert csv==(pdir/'translation_used.csv').read_bytes();writes=j('build/dialogue_kr_poc_024/expected_writes.json');model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 asm=ROOT/'workspace/asm/dialogue_page_font_008.asm';code,listing,symbols=assemble(asm.read_text('utf-8'),0x95f9);assert 0x95f9+len(code)<0x9700
 init,il,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @page_init\nPLA\nSTA $2B\nLDA $06CE\nPLP\nLDY #$00\nRTS',0x9430,symbols)
 setup,sl,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @intro_setup\nPLA\nSTA $2B\nPLP\nLDA #$01\nLDY #$FF\nCLC\nCLV\nINC $06DE\nRTS',0x8e88,symbols)
 output=bytearray(prior);output[0x5609:0x5609+len(code)]=code
 for base in (0x10,0x20010):output[base+0x5430:base+0x5449]=init.ljust(25,b'\xea');output[base+0x4e88:base+0x4ea3]=setup.ljust(27,b'\xea')
 gate_slots=(0x16,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x2c);font=prior[0x65010:0x65810];font_off=0x40010+171*0x400;assert not any(prior[font_off:font_off+0x800]);output[font_off:font_off+0x800]=font
 for slot in gate_slots:assert prior[0x5710+slot*2]==148;output[0x5710+slot*2]=171
 cases=0
 for slot in range(48):
  for phase in (0,1,3,4):
   for active in (90,148,166):
    for mode in (0,0x10,0x12):
     x,xm=run(prior,slot,phase,active,mode);y,ym=run(output,slot,phase,active,mode)
     assert (x.a,x.x,x.y,x.sp,x.p)==(y.a,y.x,y.y,y.sp,y.p) and xm.banks==ym.banks
     assert all(xm.ram[i]==ym.ram[i] for i in range(2048) if i not in (0x34,0xc6,0x6f3) and not 0x100<=i<0x200)
     assert y.processorCycles==x.processorCycles,(slot,mode,y.processorCycles-x.processorCycles)
     assert ym.ram[0x34]==(171 if slot in gate_slots else 90) and ym.ram[0xc6]==ym.ram[0x6f3]==(171 if slot in gate_slots else xm.ram[0xc6]);cases+=1
 assert irq(prior)==irq(output) and output[0x40010:font_off]==prior[0x40010:font_off] and output[font_off+0x800:]==prior[font_off+0x800:]
 for w in writes:
  p,n=w['file_offset'],w['length'];w['final_hex']=output[p:p+n].hex()
 model=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 parent=j('build/dialogue_kr_poc_024/build_report.json');report={**parent,'output_sha256':sha(output),'prior_adopted_sha256':sha(prior),'prior_candidate_sha256':sha(prior),'helper_code_bytes':len(code),'top_font_commit':{'classification':'Odd custom font-bank pairs also supply top RAM34; all prior native/intro/home banks are even','gate_Japanese_clone_bank':171,'gate_slots':list(gate_slots),'Japanese_glyph_data_preserved':True,'dispatch_cycles_each_path':11,'short_and_long_delay_cycles_removed':10,'equivalent_saved_high_pointer_fetch':'LDA07 saves1 cycle versusLDA06CE;07 stored fromsame pointerhigh above','all_page_elapsed_cycles_exact024':True},'CPU_page_phase_active_mode_cases':cases,'all_page_setup_cycles_equal_prior023':True,'all_page_setup_cycles_equal_prior024':True,'reserved_remaining_KiB':4,'scope':'Work28 exact-time top-font dispatch and Japanese gate clone;20 drafts unchanged; no release','runtime':'Pending actual intro/menu/gate timing/pixels; CPU models do not replace real execution','ISA':verify_profile()}

 for name,value in [('build_report.json',report),('expected_writes.json',writes),('asm_listing.json',{'helper':listing,'init':il,'setup':sl,'symbols':symbols})]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('page_font_used.asm',asm),('builder_used.py',Path(__file__)),('translation_used.csv',pdir/'translation_used.csv'),('plan_used.json',pdir/'plan_used.json'),('ui_korean_page_mapping.json',pdir/'ui_korean_page_mapping.json')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
