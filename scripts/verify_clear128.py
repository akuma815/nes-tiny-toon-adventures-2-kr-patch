"""049 independent write model, frozen048 diff, reproducible build and real apply."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def j(p):return json.loads((R/p).read_text('utf-8'))
def main():
    out=R/'qa/reports/clear128_validation.json';assert not out.exists()
    d=R/'build/dialogue_kr_poc_049';r=j('build/dialogue_kr_poc_049/build_report.json')
    m=j('manifests/source_rom.json');source=R/m['path'];assert sha(source)==m['sha256']==r['source_sha256']
    old=(R/'build/dialogue_kr_poc_048/TinyToon2_dialogue_kr_poc.nes').read_bytes();new=(d/'TinyToon2_dialogue_kr_poc.nes').read_bytes()
    assert sha(d/'TinyToon2_dialogue_kr_poc.nes')==r['output_sha256']
    diffs=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y];assert len(diffs)==165
    assert all(any(a<=i<b for a,b in r['admitted_vs048_ranges']) for i in diffs)
    assert old[:16]==new[:16] and old[0x40010:]==new[0x40010:] and old[0x24010:0x24440]==new[0x24010:0x24440]
    model=bytearray(source.read_bytes());owned=set()
    for w in j('build/dialogue_kr_poc_049/expected_writes.json'):
        pos,n=w['file_offset'],w['length'];area=set(range(pos,pos+n));assert not area&owned;owned|=area
        assert source.read_bytes()[pos:pos+n]==bytes.fromhex(w['expected_hex']);model[pos:pos+n]=bytes.fromhex(w['final_hex'])
    assert model==new
    rebuild=R/'build/dialogue_kr_poc_049_rebuild128';assert not rebuild.exists()
    p=subprocess.run([sys.executable,str(R/'scripts/build_clear128_v2.py'),'--output',str(rebuild)],cwd=R,capture_output=True);assert p.returncode==0,p.stderr.decode('utf-8','replace')
    files=sorted(p.name for p in d.iterdir() if p.is_file());assert files==sorted(p.name for p in rebuild.iterdir() if p.is_file())
    for f in files:assert (d/f).read_bytes()==(rebuild/f).read_bytes(),f
    applydir=R/'work/clear128/한글 패치 적용';assert not applydir.exists();applydir.mkdir(parents=True)
    applied=applydir/'타이니툰2 지우기 후 글꼴.nes'
    command=[sys.executable,str(R/'scripts/dialogue_ips.py'),'apply','--source',str(source),'--patch',str(d/'TinyToon2_dialogue_kr_poc.ips'),'--output',str(applied)]
    p=subprocess.run(command,cwd=applydir,capture_output=True);(applydir/'stdout.txt').write_bytes(p.stdout);(applydir/'stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0 and applied.read_bytes()==new
    result={'work':128,'status':'PASS_BOUNDED_CPU_BUILD_REAL_APPLY','source_sha256':sha(source),'candidate049_sha256':sha(d/'TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'changed_vs048':len(diffs),'source9writes_nonoverlapping_full_output_exact':True,'all_fonts_and_body_from048_preserved':True,'rebuild_files_byte_exact':files,'real_Windows_IPS_CLI_exit':0,'applied_sha256':sha(applied),'apply_command':command,'CPU_page_cases':r['page_CPU_cases'],'CPU_setup_cases':r['intro_setup_cases'],'all_page_extra_cycles':38,'actual_runtime':'Pending;048 failure retained,047 adopted,049 candidate only.','human_approved':False,'limitations':r['risk']}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
