"""Work49 read-only investigation audit; newevidence only, prior042 audit retained."""
import json,hashlib,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/pause_world049_session.json';assert not out.exists();assets=json.loads((R/'manifests/pause_world_assets.json').read_text('utf-8'))
 for group in ('inputs','outputs'):
  for p,h in assets[group].items():assert sha(R/p)==h,p
 frozen=0
 for name in assets['outputs']:
  if not name.endswith('/environment.json'):continue
  p=R/name;e=json.loads(p.read_text('utf-8'));assert e['exit_code']==0 and (p.parent/'trace_complete.txt').read_text()==str(e['frames'])
  for f,h in e['files'].items():assert sha(p.parent/f)==h;frozen+=1
 initial=json.loads((R/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(R.parent/p)==h,p
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 v=json.loads((R/'qa/reports/pause049_survey.json').read_text('utf-8'));assert v['status']=='PASS'and v['CPU_D_clear_cases']==1024
 t=json.loads((R/'qa/reports/train049_font_consumer.json').read_text('utf-8'));assert t['status']=='PASS_FONT_CONSUMER'and t['IRQ_rows']==4566 and t['actual_4KiB_samples']==152
 links=[]
 for p in [R/'README.md',R/'AGENTS.md',*sorted((R/'docs').rglob('*.md'))]:
  for target in re.findall(r'\]\(([^\n]+?)\)',p.read_text('utf-8')):
   target=target.strip().strip('<>').split('#')[0]
   if not target or re.match(r'[a-z]+://',target):continue
   q=(p.parent/target).resolve();assert q.exists()or q==out.resolve(),(p,target);links.append({'document':p.relative_to(R).as_posix(),'target':target})
 assert not list((R/'dist').iterdir())
 result={'work':49,'status':'PASS','adopted_build':'dialogue_kr_poc_042','ROM_sha256':v['ROM_sha256'],'source_and_first_game_reference_hashes_unchanged':True,'no_ROM_or_IPS_or_translation_writes':True,'prior_full_preservation_audit':'qa/reports/gameover_session_20261005.json','prior_audit_SHA256':sha(R/'qa/reports/gameover_session_20261005.json'),'audit_scope':'Hash allwork49 inputs/newoutputs andtheir runtimeenvironments; earlierfullhistoryaudit retained, notrerun','runtime_frozen_files':frozen,'local_markdown_links_checked':len(links),'links':links,'asset_manifest_SHA256':sha(R/'manifests/pause_world_assets.json'),'limits':v['limits']+t['limits'],'next_action':t['next_action']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k]for k in ('status','runtime_frozen_files','local_markdown_links_checked')},indent=2))
if __name__=='__main__':main()
