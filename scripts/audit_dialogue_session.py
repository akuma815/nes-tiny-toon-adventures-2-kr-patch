"""Freeze current dialogue PoC evidence hashes and validate canonical handoff links."""
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    r=ROOT;out=r/'qa/reports/dialogue_session_20261004.json'
    source=json.loads((r/'manifests/source_rom.json').read_text(encoding='utf-8'));assert sha(r/source['path'])==source['sha256']
    initial=json.loads((r/'qa/reports/initial_session_20261004.json').read_text(encoding='utf-8'))
    for p,h in initial['first_game_references'].items():assert sha(r.parent/p)==h,p
    assets=json.loads((r/'manifests/dialogue_assets.json').read_text(encoding='utf-8'))
    for group in ('inputs','outputs'):
        for p,h in assets[group].items():assert sha(r/p)==h,p
    assert assets['translation']=='여기는 모두가 아는\n애크미 에이커스'
    title_assets=json.loads((r/'manifests/title_assets.json').read_text(encoding='utf-8'))
    assert title_assets['text']=={'main':'타이니 툰 / 어드벤처','subtitle':'몬타나랜드에 어서 오세요','secondary':'타이니 툰 어드벤처'}
    assert sha(r/'backups/translation/text_ja_before_dialogue_001.csv')=='934e13de97c024d4ee86420e0a2238447585b155ad1b21f2ffeef0d7b644d21f'
    rows=list(csv.DictReader((r/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')))
    assert len(rows)==54 and sum(v['status']=='draft' for v in rows)==1
    assert sum(v['status']=='untranslated' for v in rows)==53
    validation=json.loads((r/'qa/reports/dialogue_poc002_validation.json').read_text(encoding='utf-8'))
    assert validation['runtime']['samples']==165 and validation['runtime']['outside_paragraph_pixels']==0
    assert not list((r/'dist').iterdir())
    files={}
    for folder in ('scripts','docs','manifests','workspace/translation','workspace/tables','workspace/fonts','backups/translation','extracted/text/kana_mapping_001','build/dialogue_kr_poc_001','build/dialogue_kr_poc_001_rebuild','build/dialogue_kr_poc_002','build/dialogue_kr_poc_002_rebuild','qa/dialogue','work/dialogue_font','tools/python/py65-1.2.0'):
        for p in sorted((r/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(r).as_posix()]=sha(p)
    for p in [r/'README.md',*sorted((r/'qa/reports').glob('dialogue_*.json'))]:
        if p!=out:files[p.relative_to(r).as_posix()]=sha(p)
    final={'date':'2026-10-04','scope':'Handoff work7/8/9; one draft paragraph integrated with title003','adopted_build':'dialogue_kr_poc_002','source_sha256':source['sha256'],'output_sha256':validation['output_sha256'],'evidence_classes':{'static':'Expected Writes/whole diff/text/font/input guards passed; original sources preserved','cpu_harness':'37 original reader calls, identical per-call cycles/cursors; total3282','build_apply':'Rebuild and actual Korean/space path IPS application reproduce output SHA256','emulator':'Mesen5400/3000 exit0; matched title003165 samples,66 first-paragraph changes/99 whole-screen equal, outside0','direct_visual':'Actual1080 enlargement and partial976/wait1080/next1320/reentry3840 sheet reviewed; user final review separate'},'translation_rows':{'draft':1,'untranslated':53},'first_game_reference_hashes_unchanged':True,'dist_empty':True,'file_sha256':files,'self_sha256':'Excluded to avoid recursive hash.','next_action':'Design per-paragraph Hangul font supply/lifetime; trace second intro paragraph and home consumer.'}
    out.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    links=[]
    for p in (r/'README.md',r/'AGENTS.md',*sorted((r/'docs').rglob('*.md'))):
        for target in re.findall(r'\]\(([^\n]+?)\)',p.read_text(encoding='utf-8')):
            target=target.strip().strip('<>').split('#')[0]
            if not target or re.match(r'[a-z]+://',target):continue
            assert (p.parent/target).exists(),(p,target)
            links.append({'document':p.relative_to(r).as_posix(),'target':target})
    final['local_markdown_links_checked']=len(links);final['links']=links
    out.write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','file_hashes':len(files),'links':len(links),'source_and_first_game_reference_hashes_unchanged':True,'translation_raw_preserved_by_validation':True,'report':str(out)},indent=2))
if __name__=='__main__':main()
