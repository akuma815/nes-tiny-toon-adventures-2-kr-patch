"""Independent full diff/write guards, real rebuild and Windows IPS CLI apply."""
from pathlib import Path
import csv,hashlib,io,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def main():
    out=R/'qa/reports/shortage126_validation.json';assert not out.exists()
    d=R/'build/dialogue_kr_poc_048';report=j('build/dialogue_kr_poc_048/build_report.json')
    original=j('manifests/source_rom.json');source=R/original['path']
    assert sha(source)==report['source_sha256']==original['sha256']
    old=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';new=d/'TinyToon2_dialogue_kr_poc.nes'
    assert sha(old)==report['prior_adopted_sha256'] and sha(new)==report['output_sha256']
    a,b=old.read_bytes(),new.read_bytes();diffs=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    assert len(diffs)==839==report['changed_bytes']
    expected_ranges=[[0x2590c,0x25920],[0x5762,0x5763],[0x78810,0x79010]]
    assert report['admitted_prior_ranges']==expected_ranges
    assert all(any(start<=i<end for start,end in expected_ranges) for i in diffs)
    assert len(a)==len(b)==499728 and a[:16]==b[:16] and a[0x71010:0x71810]==b[0x71010:0x71810] and not any(b[0x79010:])
    model=bytearray(source.read_bytes());owned=set()
    for w in j('build/dialogue_kr_poc_048/expected_writes.json'):
        offset,n=w['file_offset'],w['length'];area=set(range(offset,offset+n));assert not area&owned;owned|=area
        assert source.read_bytes()[offset:offset+n]==bytes.fromhex(w['expected_hex']);model[offset:offset+n]=bytes.fromhex(w['final_hex'])
    assert model==b
    oldrows=list(csv.DictReader(io.StringIO((R/'backups/translation/text_ja_before_shortage126.csv').read_text('utf-8-sig'))))
    newrows=list(csv.DictReader(io.StringIO((R/'workspace/translation/text_ja.csv').read_text('utf-8-sig'))))
    changes=[(x['entry_id'],k) for x,y in zip(oldrows,newrows) for k in x if x[k]!=y[k]]
    assert changes==[('MAIN_0590C','translation_ko'),('MAIN_0590C','notes')]
    m=j('build/dialogue_kr_poc_048/shortage_editorial_mapping.json')
    assert m['forced_macro_glyphs']=={'39':'티','40':'켓','41':'이','42':' '}
    assert [x['text'] for x in m['layout']]==['아쉽지만','티켓이 부족해!']
    assert b[0x261ce:0x261ff]==a[0x261ce:0x261ff]
    rebuild=R/'build/dialogue_kr_poc_048_rebuild126';assert not rebuild.exists()
    p=subprocess.run([sys.executable,str(R/'scripts/build_shortage126_v2.py'),'--output',str(rebuild)],cwd=R,capture_output=True)
    assert p.returncode==0,p.stderr.decode('utf-8','replace')
    files=sorted(x.name for x in d.iterdir() if x.is_file());assert files==sorted(x.name for x in rebuild.iterdir() if x.is_file())
    for name in files:assert (d/name).read_bytes()==(rebuild/name).read_bytes(),name
    applydir=R/'work/shortage126/패치 적용 검증';assert not applydir.exists();applydir.mkdir(parents=True)
    applied=applydir/'타이니툰 2 단일 문장 적용.nes'
    command=[sys.executable,str(R/'scripts/dialogue_ips.py'),'apply','--source',str(source),'--patch',str(d/'TinyToon2_dialogue_kr_poc.ips'),'--output',str(applied)]
    p=subprocess.run(command,cwd=applydir,capture_output=True)
    (applydir/'stdout.txt').write_bytes(p.stdout);(applydir/'stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0 and applied.read_bytes()==b
    result={'work':126,'status':'PASS_STATIC_BUILD_AND_REAL_IPS_APPLY','source_sha256':sha(source),'prior047_sha256':sha(old),'candidate048_sha256':sha(new),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'changed_bytes':len(diffs),'admitted_prior_ranges':expected_ranges,'source_expected_write_model_exact':True,'single_SSOT_edit_fields':changes,'preserved_shared_font196197_and_macro_definitions':True,'native_control_length_reader_cycles_and_cursor_equal':m['per_call_cycles_cursor_equal'],'CPU_page_setup_cases':report['CPU_page_setup_cases'],'rebuild_byte_exact_files':files,'apply_command':command,'real_Windows_IPS_CLI_apply_exit':0,'applied_sha256':sha(applied),'human_approved':False,'adopted_build':'dialogue_kr_poc_047','candidate_only':True,'runtime':'Not yet performed; actual shortage-to-possession font lifecycle and pixel bounds are next.','limits':['No real emulator or direct game-image claim in this build check','No formal release/apply.cmd package refreshed','Registered45 drafts are not a global corpus or final human approval']}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
