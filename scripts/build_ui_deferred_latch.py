"""Keep active text font until the native clear completes; preserve idle-loop phase."""
import argparse,hashlib,json
from pathlib import Path
from asm6502 import assemble,verify_profile
from verify_ui_native_latch_hooks import Memory,MPU,irq
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
def run(rom,slot,phase,active):
 mem=Memory(rom);cpu=MPU(memory=mem);mem.cpu=cpu;cpu.pc=0x9417;cpu.sp=0xfd;cpu.a=0;cpu.x=0x73;cpu.y=0x92;cpu.p=0x34;mem.ram[0x1fe:0x200]=bytes.fromhex('ff c0');mem.ram[0x2b]=0x36;mem.ram[0x6cf]=slot;mem.ram[0x6df]=phase;mem.ram[0x6f3]=active;mem.ram[0xc6]=active;steps=0
 while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<10000
 return cpu,mem
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256'];pdir=ROOT/'build/dialogue_kr_poc_020';prior=(pdir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='9ef95c43c1c9b23e7709d9fb11cf5298f3aef873e3a3080fdd1b851b013e3510'
 csv=(ROOT/'workspace/translation/text_ja.csv').read_bytes();assert csv==(pdir/'translation_used.csv').read_bytes();writes=j('build/dialogue_kr_poc_020/expected_writes.json');model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 asm=ROOT/'workspace/asm/dialogue_page_font_006.asm';code,listing,symbols=assemble(asm.read_text('utf-8'),0x95f9);assert 0x95f9+len(code)<0x9700
 init,il,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @page_init\nPLA\nSTA $2B\nLDA $06CE\nPLP\nLDY #$00\nRTS',0x9430,symbols)
 setup,sl,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @intro_setup\nPLA\nSTA $2B\nPLP\nLDA #$01\nLDY #$FF\nCLC\nCLV\nINC $06DE\nRTS',0x8e88,symbols)
 output=bytearray(prior);output[0x5609:0x5609+len(code)]=code
 for base in (0x10,0x20010):output[base+0x5430:base+0x5449]=init.ljust(25,b'\xea');output[base+0x4e88:base+0x4ea3]=setup.ljust(27,b'\xea')
 cases=0
 for slot in range(48):
  for phase in (0,1,3,4):
   for active in (90,160,162):
    x,xm=run(prior,slot,phase,active);y,ym=run(output,slot,phase,active)
    assert (x.a,x.x,x.y,x.sp,x.p)==(y.a,y.x,y.y,y.sp,y.p) and xm.banks==ym.banks
    assert all(xm.ram[i]==ym.ram[i] for i in range(2048) if i!=0x6f3 and not 0x100<=i<0x200)
    assert y.processorCycles-x.processorCycles==19 and ym.ram[0x6f3]==(active if phase==4 else ym.ram[0xc6]);cases+=1
 assert irq(prior)==irq(output) and output[0x40010:]==prior[0x40010:]
 for w in writes:
  p,n=w['file_offset'],w['length'];w['final_hex']=output[p:p+n].hex()
 model=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 parent=j('build/dialogue_kr_poc_020/build_report.json');report={**parent,'output_sha256':sha(output),'prior_candidate_sha256':sha(prior),'helper_code_bytes':len(code),'deferral_RAM_state':{'phase':0x6df,'active_font':0x6f3,'defer_value':4,'post_clear_commit_value':3},'CPU_page_phase_active_cases':cases,'page_added_cycles_to020':19,'all_page_setup_cycles_equal_prior019':False,'page_phase_mod19':0,'original_intro_IRQ_and_all_fonts_text_macros_preserved_from020':True,'scope':'Work22 eight home/booth drafts with pre-clear font deferral; no release','runtime':'NOT YET RUN; reject020 preserved; verify native clear transition, all rows and actual IRQ alignment','ISA':verify_profile()}
 for name,value in [('build_report.json',report),('expected_writes.json',writes),('asm_listing.json',{'helper':listing,'init':il,'setup':sl,'symbols':symbols})]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('page_font_used.asm',asm),('builder_used.py',Path(__file__)),('translation_used.csv',pdir/'translation_used.csv'),('plan_used.json',pdir/'plan_used.json'),('ui_korean_page_mapping.json',pdir/'ui_korean_page_mapping.json')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
