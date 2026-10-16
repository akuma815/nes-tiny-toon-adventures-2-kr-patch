"""Immutable042 to043 isolatedtrainfont clone, source ExpectedWrites, completeIRQ ABI."""
import argparse,hashlib,json
from pathlib import Path
from compile_train_sign import compile_train
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def irq(rom,flags,scroll,counter):
 m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xfbe3;c.p=flags;c.a=0;c.x=17;c.y=67;c.sp=0xf7;m.ram[0x60c]=0xa8;m.ram[0x60f]=scroll;m.ram[0x41]=counter
 m.ram[0x1f8:0x1fe]=bytes([0x27,0x17,0x31,flags,0,0xc1]);n=0
 while c.pc!=0xc100:c.step();n+=1;assert n<1000
 return c,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);z=ap.parse_args();out=z.output.resolve();out.relative_to((R/'build').resolve());assert not out.exists()
 manifest=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/manifest['path']).read_bytes();assert sha(source)==manifest['sha256'];prior=(R/'build/dialogue_kr_poc_042/TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)=='f4b4aa288e03bb30fd9532d95f823e34c4c620b20438feb2e1de0f67845cfc7b'
 plan=compile_train(prior,source);target=bytearray(prior)+bytearray(8192);target[5]=28
 for p,a,b in zip(plan['producer']['canonical_immediates'],plan['producer']['old'],plan['producer']['new']):assert target[p]==a;target[p]=b
 target[0x76010:0x77010]=bytes.fromhex(plan['font_hex']);assert len(target)==0x78010 and not any(target[0x77010:])
 allowed={5,*plan['producer']['canonical_immediates']};assert {i for i,(a,b)in enumerate(zip(prior,target))if a!=b}==allowed;assert target[0x1e010:0x20010]==prior[0x1e010:0x20010] and target[0x40010:0x76010]==prior[0x40010:0x76010]
 cases=0;timings=set();owned_ports={0xa000:(72,216),0xa008:(73,217),0xb000:(74,218),0xb008:(75,219)}
 for flags in range(256):
  for scroll in (0,195,255):
   for counter in (0,1,255):
    a,x=irq(prior,flags,scroll,counter);b,y=irq(target,flags,scroll,counter);assert (a.a,a.x,a.y,a.sp,a.p,a.pc,a.processorCycles)==(b.a,b.x,b.y,b.sp,b.p,b.pc,b.processorCycles) and a.sp==0xfd
    assert x.ram==y.ram and x.banks==y.banks and len(x.writes)==len(y.writes)
    for (p,v,t),(q,w,u)in zip(x.writes,y.writes):assert(p,t)==(q,u)and ((v,w)==owned_ports[p]if p in owned_ports else v==w)
    cases+=1;timings.add(a.processorCycles)
 writes=json.loads((R/'build/dialogue_kr_poc_042/expected_writes.json').read_text('utf-8'));expected=bytearray(source);areas=set()
 for w in writes:
  p=w['file_offset']
  if p==0x20010:w['length']=len(target)-p;w['composition']='Prior042 nativePRG mirrors andCHR retained; isolatedtrainfont216..219;220..223 zero'
  if p==5:w['owner']='CHR128_to224_KiB'
  n=w['length'];assert not areas.intersection(range(p,p+n));areas.update(range(p,p+n));assert source[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=target[p:p+n].hex();expected[p:p+n]=bytes.fromhex(w['final_hex'])
 assert expected==target;out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(target)
 report={'work':51,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(target),'output_size':len(target),'output_rom':'TinyToon2_dialogue_kr_poc.nes','expected_writes':len(writes),'font_banks':[216,217,218,219],'CHR_KiB':224,'distinct_labels':3,'Hangul_unique':8,'modified_tiles':10,'native_IRQ5_complete_RTI_ABI_cases':cases,'IRQ_cycles_exact':sorted(timings),'all_RAM_registers_stack_status_and_write_cycles_exact':True,'only_IRQ5_four_CHR_values_changed':True,'all_source_CHR_original_fixed_copy_prior_Korean_fonts_M_emblem_border_other246_tiles_unchanged':True,'CSV_sha256':sha((R/'workspace/translation/text_ja.csv').read_bytes()),'scope':'Trainthreebitmapcaptiondraft; guardedhealthdiagnostic actualconsumerknown; runtimepending'}
 for name,obj in [('build_report.json',report),('expected_writes.json',writes),('train_sign_plan_used.json',plan)]:(out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 for name,p in [('builder_used.py',Path(__file__)),('compiler_used.py',R/'scripts/compile_train_sign.py'),('translation_used.csv',R/'workspace/translation/text_ja.csv')]:(out/name).write_bytes(p.read_bytes())
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
