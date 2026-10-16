"""Remove only redundant booth pre-clear init; native post-clear init selects font."""
import argparse,hashlib,json
from pathlib import Path
from verify_ui_native_latch_hooks import Memory,MPU
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((ROOT/p).read_text('utf-8'))
def run(rom,slot,carry,overflow,points,tickets):
 mem=Memory(rom);cpu=MPU(memory=mem);mem.cpu=cpu;cpu.pc=0x9cf1;cpu.sp=0xf5;cpu.a=1;cpu.x=0x73;cpu.y=0xff;cpu.p=0x30|(1 if carry else 0)|(0x40 if overflow else 0);mem.ram[0x2b]=0x36;mem.ram[0x6cf]=slot;mem.ram[0x6df]=4;mem.ram[0x6de]=8;mem.ram[0x6f3]=160;mem.ram[0xc6]=160;mem.ram[0x6cd:0x6cf]=bytes.fromhex('67 97');mem.ram[0x7d0:0x7d3]=bytes(points);mem.ram[0x7f2]=tickets;steps=0
 while cpu.pc!=0x9d06:cpu.step();steps+=1;assert steps<100000,(hex(cpu.pc),mem.banks)
 return cpu,mem
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();m=j('manifests/source_rom.json');source=(ROOT/m['path']).read_bytes();assert sha(source)==m['sha256'];pdir=ROOT/'build/dialogue_kr_poc_020';prior=(pdir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='9ef95c43c1c9b23e7709d9fb11cf5298f3aef873e3a3080fdd1b851b013e3510';assert (ROOT/'workspace/translation/text_ja.csv').read_bytes()==(pdir/'translation_used.csv').read_bytes();writes=j('build/dialogue_kr_poc_020/expected_writes.json');model=bytearray(source)
 for w in writes:
  p,n=w['file_offset'],w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==prior
 output=bytearray(prior)
 for base in (0,0x20000):assert prior[0x5d03+base:0x5d06+base]==bytes.fromhex('20 17 94');output[0x5d03+base:0x5d06+base]=bytes.fromhex('a0 00 ea')
 cases=0;deltas=set();allowed={0x6,0x7,0xc6,0x6f3,0x6c0,0x6c1,0x6d1,0x6d2,0x6cd,0x6ce,0x6c3,0x6c4}
 for slot in (13,14,15):
  for carry in (False,True):
   for overflow in (False,True):
    for points in ((0,0,0),(9,9,9),(1,2,3)):
     for tickets in (0,10,99):
      x,xm=run(prior,slot,carry,overflow,points,tickets);y,ym=run(output,slot,carry,overflow,points,tickets)
      assert (x.a,x.x,x.y,x.sp,x.p)==(y.a,y.x,y.y,y.sp,y.p),(slot,carry,overflow,points,tickets)
      assert xm.banks==ym.banks and all(xm.ram[i]==ym.ram[i] for i in range(2048) if i not in allowed and not 0x100<=i<0x200)
      assert ym.ram[0x6f3]==ym.ram[0xc6]==160 and ym.ram[0x6df]==0 and ym.ram[0x6de]==9;delta=y.processorCycles-x.processorCycles;assert delta==-209 and delta%19==0;deltas.add(delta);cases+=1
 assert output[0x5609:0x5700]==prior[0x5609:0x5700] and output[0x40010:]==prior[0x40010:]
 for w in writes:
  p,n=w['file_offset'],w['length'];w['final_hex']=output[p:p+n].hex()
 model=bytearray(source);owned=set()
 for w in writes:
  p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not owned&area;owned|=area;assert source[p:p+n]==bytes.fromhex(w['expected_hex']);model[p:p+n]=bytes.fromhex(w['final_hex'])
 assert bytes(model)==output
 out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False);(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
 report={**j('build/dialogue_kr_poc_020/build_report.json'),'output_sha256':sha(output),'prior_candidate_sha256':sha(prior),'booth_pre_clear_replacement':{'CPU':0x9cf3,'source':'JSR9417','replacement':'LDY00;NOP','original_call_cycles':213,'replacement_cycles':4,'delta':-209,'idle_phase_mod19':0},'CPU_booth_pre_clear_cases':cases,'original_page_helper_and_intro_setup_preserved_from020':True,'scope':'Work23 eight home/booth drafts; redundant booth pre-clear init removed, native post-clear init commits pointer/font; no release','runtime':'NOT YET RUN; clear transition/intentional deferred-pointer checks, all screens and actual IRQ timing required'}
 for name,value in [('build_report.json',report),('expected_writes.json',writes)]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('translation_used.csv',pdir/'translation_used.csv'),('plan_used.json',pdir/'plan_used.json'),('ui_korean_page_mapping.json',pdir/'ui_korean_page_mapping.json')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
