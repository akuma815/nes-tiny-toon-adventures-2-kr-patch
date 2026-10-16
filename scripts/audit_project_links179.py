"""Strict artifact/local-link audit; explicitly report one expired historical skill-cache link."""
from pathlib import Path
import argparse, json, re
from seal_nonplay171 import R, sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    out=R/a.output;assert not out.exists()
    manifest=R/a.manifest;data=json.loads(manifest.read_text('utf-8'))
    for f,h in data['files'].items():assert sha(R/f)==h,f
    initial=json.loads((R/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
    for f,h in initial['first_game_references'].items():assert sha(R.parent/f)==h,f
    assert 'dialogue_kr_poc_050' in (R/'docs/HANDOFF.md').read_text('utf-8')
    source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
    expired=Path('C:/Users/akuma/.codex/plugins/cache/kr-patch/create-kr-patch/3.3.0/skills/create-kr-patch/SKILL.md').resolve()
    current=Path('C:/Users/akuma/.codex/plugins/cache/kr-patch/create-kr-patch/3.4.0/skills/create-kr-patch/SKILL.md')
    assert current.is_file()
    links=0;missing=[]
    for p in [R/'README.md',R/'AGENTS.md',*sorted((R/'docs').rglob('*.md'))]:
        for angle,plain in re.findall(r'\]\((?:<([^>\n]+)>|([^()\n]+))\)',p.read_text('utf-8')):
            t=(angle or plain).strip().split('#')[0]
            if not t or re.match('[a-z]+://',t):continue
            target=(p.parent/t).resolve()
            if target.exists():links+=1;continue
            # Exact historical document and exact environment-owned obsolete cache only.
            assert p.relative_to(R).as_posix()=='docs/CASTLE_CURRENCY_QA.md' and target==expired,(p,t)
            assert not target.is_relative_to(R)
            missing.append({'document':p.relative_to(R).as_posix(),'original_reference':str(target),
                'classification':'Historical external plugin-cache file expired; not project asset or live build input',
                'current_skill':str(current),'current_skill_sha256':sha(current),
                'historical_instruction_not_reconstructed_or_rewritten':True})
    result={'work':data['work'],'status':'PASS_PROJECT_ASSETS_SOURCE_AND_LOCAL_LINKS',
        'frozen_files':len(data['files']),'asset_manifest_sha256':sha(manifest),'source_and_first_game_refs_unchanged':True,
        'adopted_ROM_build':'dialogue_kr_poc_050','adopted_ROM_sha256':sha(R/'build/dialogue_kr_poc_050/TinyToon2_dialogue_kr_poc.nes'),
        'existing_links_checked':links,'historical_external_cache_missing':missing,
        'global_all_links_exist':not missing,'scope':'Exact declared assets/source/game1 refs and all project-local links. Missing historical external cache remains reported; no global-all-links/runtime/fullplay claim.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
