"""049 lower-font selection only after native clear; fixed38-cycle dispatch."""
from pathlib import Path
import argparse,hashlib,json
from asm6502 import assemble,verify_profile
from verify_gate_font_tag_hooks import Memory,MPU,irq
from dialogue_ips import make,apply
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def run(rom,pc,slot,phase,active,flags,arg=1,counter=0):
    m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=pc;c.sp=0xfd;c.a=arg;c.x=0x73;c.y=0x92;c.p=flags
    m.ram[0x1fe:0x200]=bytes.fromhex('ff c0');m.ram[0x2b]=0x36;m.ram[0x6cf]=slot;m.ram[0x6df]=phase
    m.ram[0xc6]=m.ram[0x6f3]=active;m.ram[0x34]=193;m.ram[0x6de]=counter
    steps=0
    while c.pc!=0xc100:c.step();steps+=1;assert steps<10000
    return c,m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();out=a.output.resolve();out.relative_to(R/'build');assert not out.exists()
    m=j('manifests/source_rom.json');source=(R/m['path']).read_bytes();assert sha(source)==m['sha256']
    prior_dir=R/'build/dialogue_kr_poc_048';prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==j('build/dialogue_kr_poc_048/build_report.json')['output_sha256']
    csv=(R/'workspace/translation/text_ja.csv').read_bytes();assert csv==(prior_dir/'translation_used.csv').read_bytes()
    oldasm=(R/'workspace/asm/dialogue_page_font_008.asm').read_text('utf-8');oldcode,_,oldsym=assemble(oldasm,0x95f9)
    assert prior[0x5609:0x5609+len(oldcode)]==oldcode
    asm=R/'workspace/asm/dialogue_page_font_009.asm';code,listing,symbols=assemble(asm.read_text('utf-8'),0x95f9)
    assert 0x95f9+len(code)<0x9700
    init,il,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @page_init\nPLA\nSTA $2B\nLDA $06CE\nPLP\nLDY #$00\nRTS',0x9430,symbols)
    setup,sl,_=assemble('PHP\nLDA $2B\nPHA\nLDA #$02\nJSR $FDD3\nJSR @intro_setup\nPLA\nSTA $2B\nPLP\nLDA #$01\nLDY #$FF\nCLC\nCLV\nINC $06DE\nRTS',0x8e88,symbols)
    output=bytearray(prior);output[0x5609:0x5609+len(code)]=code
    for base in (0x10,0x20010):
        output[base+0x5430:base+0x5449]=init.ljust(25,b'\xea');output[base+0x4e88:base+0x4ea3]=setup.ljust(27,b'\xea')
    diffs=[i for i,(x,y) in enumerate(zip(prior,output)) if x!=y]
    ranges=[[0x5609,0x5609+len(code)],[0x9430-0x8000+0x10,0x9449-0x8000+0x10],[0x9430-0x8000+0x20010,0x9449-0x8000+0x20010],[0x8e88-0x8000+0x10,0x8ea3-0x8000+0x10],[0x8e88-0x8000+0x20010,0x8ea3-0x8000+0x20010]]
    assert all(any(start<=i<end for start,end in ranges) for i in diffs)
    assert output[0x40010:]==prior[0x40010:] and output[0x261b1:0x261ff]==prior[0x261b1:0x261ff]
    cases=0;deferrals=0
    for slot in range(48):
        for phase in (0,1,2,3,4):
            for active in (90,193,196,226):
                for flags in (0x30,0x31,0x70,0xb5):
                    x,xm=run(prior,0x9417,slot,phase,active,flags);y,ym=run(output,0x9417,slot,phase,active,flags)
                    assert (x.a,x.x,x.y,x.sp,x.p)==(y.a,y.x,y.y,y.sp,y.p) and xm.banks==ym.banks
                    expected=active if slot in (0x29,0x2b) and phase==0 else output[0x5710+2*slot]
                    assert ym.ram[0xc6]==ym.ram[0x6f3]==expected,(slot,phase,active,ym.ram[0xc6],expected)
                    for i in range(2048):
                        if i in (0xc6,0x6f3,0x34) or 0x100<=i<0x200:continue
                        assert xm.ram[i]==ym.ram[i],(slot,phase,hex(i))
                    assert ym.ram[0x34]==xm.ram[0x34]
                    assert y.processorCycles-x.processorCycles==38,(slot,phase,active,y.processorCycles-x.processorCycles)
                    cases+=1;deferrals+=int(slot in (0x29,0x2b) and phase==0)
    setupcases=0
    for flags in (0x30,0x31,0x70,0xb5):
        for counter in (0,0x7f,0xfe,0xff):
            x,xm=run(prior,0x8e88,1,0,90,flags,counter=counter);y,ym=run(output,0x8e88,1,0,90,flags,counter=counter)
            assert x.processorCycles==y.processorCycles and (x.a,x.x,x.y,x.sp,x.p)==(y.a,y.x,y.y,y.sp,y.p)
            assert all(xm.ram[i]==ym.ram[i] for i in range(2048) if not 0x100<=i<0x200);setupcases+=1
    assert irq(prior)==irq(output)
    writes=j('build/dialogue_kr_poc_048/expected_writes.json');model=bytearray(source);owned=set()
    for w in writes:
        pos,n=w['file_offset'],w['length'];area=set(range(pos,pos+n));assert not area&owned;owned|=area
        assert source[pos:pos+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(output[pos:pos+n]).hex();model[pos:pos+n]=bytes.fromhex(w['final_hex'])
    assert model==output
    patch=make(source,bytes(output));assert apply(source,patch)==output
    out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output);(out/'TinyToon2_dialogue_kr_poc.ips').write_bytes(patch)
    meta={'source_sha256':sha(source),'output_sha256':sha(output),'output_size':len(output),'patch_sha256':sha(patch),'scope':'049 ordinary lower-font clear deferral plus selected shortage draft; no release'}
    report={'work':128,'source_sha256':sha(source),'prior_rejected048_sha256':sha(prior),'prior_adopted047_sha256':sha((R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()),'output_sha256':sha(output),'output_size':len(output),'IPS_sha256':sha(patch),'CSV_sha256':sha(csv),'PRG_KiB':256,'CHR_KiB':232,'draft':45,'untranslated':9,'helper_code_bytes':len(code),'changed_bytes_vs048':len(diffs),'admitted_vs048_ranges':ranges,'page_CPU_cases':cases,'targeted_deferral_cases':deferrals,'intro_setup_cases':setupcases,'all_page_cycle_delta':38,'idle_period':19,'all_page_phase_mod19':0,'IRQ_code_and_write_cycles_unchanged':True,'deferral':'Only slots29/2B at06DF00 retain old06F3; post-clear06DF03 commits table font. Pointer/cursor/buffer init otherwise retained.','expected_writes':len(writes),'human_approved':False,'runtime':'Pending;049 candidate,047 remains adopted.','risk':'38extra cycles can change two idle-loop iterations and RAM22 RNG counter per page init. CPU model does not prove real IRQ/PPU or full gameplay; actual partial/clear/next and successful branch plus other page paths required.','ISA':verify_profile()}
    for name,value in [('TinyToon2_dialogue_kr_poc.json',meta),('build_report.json',report),('expected_writes.json',writes),('asm_listing.json',{'helper':listing,'init':il,'setup':sl,'symbols':symbols})]:(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf-8')
    for name,path in [('page_font_used.asm',asm),('builder_used.py',Path(__file__)),('translation_used.csv',prior_dir/'translation_used.csv'),('plan_used.json',prior_dir/'plan_used.json'),('shortage_editorial_mapping.json',prior_dir/'shortage_editorial_mapping.json')]:(out/name).write_bytes(path.read_bytes())
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
