"""One private-font ordinary shortage sentence; immutable new development build."""
from pathlib import Path
import argparse,csv,io,json,hashlib
from build_ui_home_booth import page
from build_dialogue_poc import FONT_SHA,TTF_SHA
from verify_gate_font_tag_hooks import compare,irq,Memory,MPU
from dialogue_ips import make,apply
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def irq_with_font(rom,font):
    m=Memory(rom);c=MPU(memory=m);m.cpu=c;c.pc=0xfb97;c.sp=0xf6;m.ram[0xc6]=font
    steps=0
    while c.pc!=0xfd13:c.step();steps+=1;assert steps<10000
    assert c.sp==0xf6 and m.ram[0x47]==0
    return c.processorCycles,[(a,v,t) for a,v,t in m.writes if a in (0x2000,0x2005,0x2006,0xa000,0xa008,0xb000,0xb008)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    out=a.output.resolve();out.relative_to(R/'build');assert not out.exists()
    planpath=R/'workspace/translation/shortage_editorial_plan_126.json';plan=j(planpath.relative_to(R))
    meta=j('manifests/source_rom.json');source=(R/meta['path']).read_bytes();assert sha(source)==meta['sha256']==plan['source_sha256']
    prior_dir=R/'build'/plan['prior_build'];prior=(prior_dir/'TinyToon2_dialogue_kr_poc.nes').read_bytes();assert sha(prior)==plan['prior_ROM_sha256']
    csvbytes=(R/'workspace/translation/text_ja.csv').read_bytes();before=(R/plan['backup_CSV']).read_bytes()
    assert sha(csvbytes)==plan['CSV_sha256'] and sha(before)==plan['backup_CSV_sha256']
    old=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));new=list(csv.DictReader(io.StringIO(csvbytes.decode('utf-8-sig'))))
    assert len(old)==len(new)==54 and sum(x['status']=='draft' for x in new)==45
    edits=[(x['entry_id'],k) for x,y in zip(old,new) for k in x if x[k]!=y[k]]
    assert edits==[('MAIN_0590C','translation_ko'),('MAIN_0590C','notes')]
    p=plan['profile'];assert p['font_bank']==226 and p['slot']==0x29 and p['text']==next(x['translation_ko'] for x in new if x['entry_id']=='MAIN_0590C')
    png=R/'workspace/fonts/galmuri7_8x8/Galmuri7_8x8.png';ttf=R/'workspace/fonts/galmuri7_8x8/Galmuri7.ttf'
    assert sha(png.read_bytes())==FONT_SHA and sha(ttf.read_bytes())==TTF_SHA
    body,font,info=page(prior,source,p,plan,j('build/dialogue_kr_poc_019/ui_macro_mapping.json'),png,ttf)
    start,end=p['source_file_offset']+0x20000,p['end_exclusive']+0x20000
    off=0x40010+226*0x400;tag=0x5710+2*0x29
    assert [off,off+0x800]==plan['reserved_font_range'] and not any(prior[off:off+0x800]) and prior[tag]==196
    output=bytearray(prior);output[start:end]=body;output[off:off+0x800]=font;output[tag]=226
    diffs=[i for i,(x,y) in enumerate(zip(prior,output)) if x!=y]
    assert diffs and all(start<=i<end or off<=i<off+0x800 or i==tag for i in diffs)
    assert len(output)==499728 and output[:16]==prior[:16] and output[0x40010:off]==prior[0x40010:off] and output[off+0x800:]==prior[off+0x800:]
    assert output[0x261ce:0x261ff]==prior[0x261ce:0x261ff]
    cases=0
    for slot in range(48):
        for flags in (0x30,0x31,0x70,0xb5):
            for seed in (0,0x5a,0x80,0xaf,0xe2,0xff):
                delta,selected=compare(prior,output,0x9417,slot,0,flags,0,seed)
                assert delta==0 and selected==output[0x5710+2*slot];cases+=1
    assert irq(prior)==irq(output)
    oldirq,newirq=irq_with_font(prior,196),irq_with_font(output,226)
    assert oldirq[0]==newirq[0] and len(oldirq[1])==len(newirq[1])
    substitutions=[]
    for oldw,neww in zip(oldirq[1],newirq[1]):
        assert (oldw[0],oldw[2])==(neww[0],neww[2])
        if oldw!=neww:
            assert (oldw[0],oldw[1],neww[1]) in ((0xa000,196,226),(0xa008,197,227));substitutions.append({'prior':oldw,'new':neww})
    assert len(substitutions)==2
    writes=j(f'build/{plan["prior_build"]}/expected_writes.json');model=bytearray(source);owned=set()
    for w in writes:
        pos,n=w['file_offset'],w['length'];area=set(range(pos,pos+n));assert not area&owned;owned|=area
        assert source[pos:pos+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(output[pos:pos+n]).hex();model[pos:pos+n]=bytes.fromhex(w['final_hex'])
    assert model==output
    patch=make(source,bytes(output));assert apply(source,patch)==output
    out.mkdir();(out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output);(out/'TinyToon2_dialogue_kr_poc.ips').write_bytes(patch)
    patchmeta={'source_sha256':sha(source),'output_sha256':sha(output),'output_size':len(output),'patch_sha256':sha(patch),'scope':'Work126 single ordinary shortage sentence plus current047; draft, not final release'}
    report={'work':126,'source_sha256':sha(source),'prior_adopted_sha256':sha(prior),'output_sha256':sha(output),'output_size':len(output),'IPS_sha256':sha(patch),'csv_sha256':sha(csvbytes),'plan_sha256':sha(planpath.read_bytes()),'PRG_KiB':256,'CHR_KiB':232,'draft':45,'untranslated':9,'selected_entries':['MAIN_0590C'],'changed_bytes':len(diffs),'admitted_prior_ranges':[[start,end],[tag,tag+1],[off,off+0x800]],'font_banks':[226,227],'preserved_shared_fonts':[196,197],'CPU_page_setup_cases':cases,'page_setup_cycle_delta':0,'native_reader_calls':info['reader_calls'],'native_reader_per_call_cycles_cursor_equal':True,'IRQ_write_addresses_and_cycles_equal':True,'IRQ_intended_font_substitution':substitutions,'source_expected_writes':len(writes),'human_final_review':False,'runtime':'Pending; candidate only,047 remains adopted until actual scene validation.'}
    for name,value in [('TinyToon2_dialogue_kr_poc.json',patchmeta),('build_report.json',report),('expected_writes.json',writes),('shortage_editorial_mapping.json',info)]:
        (out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf-8')
    for name,path in [('translation_used.csv',R/'workspace/translation/text_ja.csv'),('plan_used.json',planpath),('builder_used.py',Path(__file__))]:(out/name).write_bytes(path.read_bytes())
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
