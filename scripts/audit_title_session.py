"""Freeze title session hashes and check handoff links without re-running the emulator."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    r=ROOT;out=r/'qa/reports/title_session_20261004.json'
    initial=json.loads((r/'qa/reports/initial_session_20261004.json').read_text(encoding='utf-8'))
    source=json.loads((r/'manifests/source_rom.json').read_text(encoding='utf-8'))
    assert sha(r/source['path'])==source['sha256']
    assert sha(r/'workspace/translation/text_ja.csv')=='934e13de97c024d4ee86420e0a2238447585b155ad1b21f2ffeef0d7b644d21f'
    for p,h in initial['first_game_references'].items():assert sha(r.parent/p)==h
    assets=json.loads((r/'manifests/title_assets.json').read_text(encoding='utf-8'))
    for f in assets['inputs']+assets['outputs']:assert sha(r/f['path'])==f['sha256']
    validation=json.loads((r/'qa/reports/title_kr_ai_003_validation.json').read_text(encoding='utf-8'))
    assert validation['status']=='PASS for title prototype checks only'
    assert not list((r/'dist').iterdir())
    files={}
    for folder in ('scripts','docs','manifests','extracted/title','workspace/graphics/title','build','qa/title'):
        for p in sorted((r/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(r).as_posix()]=sha(p)
    for name in ('README.md','qa/reports/title_kr_ai_003_validation.json'):files[name]=sha(r/name)
    changed={p:{'before':h,'after':sha(r/p)} for p,h in initial['changed_and_generated_files'].items() if (r/p).exists() and sha(r/p)!=h}
    final={'date':'2026-10-04','scope':'Title localization session; handoff work4/5/6','source_sha256':source['sha256'],'adopted_build':'title_kr_ai_003',
        'evidence_classes':{'static':'Source/translation/first-game reference hashes, Expected Writes, codec/pixels verified','build_apply':'Rebuild and actual IPS apply same SHA256','emulator':'Mesen5400/3000 frames exit0;72 sampled comparisons with zero outside-title differences','direct_visual':'Actual frame720 enlargement and original/modified comparison720/3360/1080/1920 manually reviewed; docs/POC_TITLE.md'},
        'changed_initial_registered_files':changed,'title_inputs_outputs_scripts_docs_sha256':files,'first_game_reference_hashes_unchanged':True,'dist_empty':True,
        'self_sha256':'Excluded to avoid recursive hash; audit script may regenerate this report.',
        'next_action':'Review actual title logo and small secondary caption design.'}
    # Write the named report before validating the document link to that report.
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
    print(json.dumps({'status':'PASS','file_hashes':len(files),'local_links':len(links),'original_and_first_game_reference_hashes_unchanged':True,'report':str(out)},ensure_ascii=True,indent=2))
if __name__=='__main__':main()
