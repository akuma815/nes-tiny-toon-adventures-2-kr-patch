"""Frozen work51 andhistorical48 plus49/50 inventories; explicitfailedQA retained."""
import json,hashlib,re,csv
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/train_sign051_session.json';assert not out.exists();assets=json.loads((R/'manifests/train_sign_assets.json').read_text('utf-8'));history=json.loads((R/'qa/reports/gameover_session_20261005.json').read_text('utf-8'))
 prior_assets=[json.loads((R/p).read_text('utf-8'))for p in ('manifests/pause_world_assets.json','manifests/train_sign_source_assets.json')]
 # Fixedinventory beforeanylonghistoricalhash loop; laterwork newQA pathsareexcluded.
 files=dict(history['file_sha256'])
 for a in [*prior_assets,assets]:
  for group in ('inputs','outputs','failed_outputs'):
   for p,h in a.get(group,{}).items():files[p]=h
 for folder in ('scripts','docs','manifests','workspace/translation','workspace/asm','backups/translation'):
  for p in sorted((R/folder).rglob('*')):
   if p.is_file()and '__pycache__'not in p.parts:files[p.relative_to(R).as_posix()]=sha(p)
 for p in [R/'README.md',*sorted((R/'qa/reports').glob('*.json'))]:
  if p!=out:files[p.relative_to(R).as_posix()]=sha(p)
 preserved=0
 for p,h in history['file_sha256'].items():
  if p.startswith(('build/','qa/dialogue/','tools/python/','work/dialogue_font/','qa/reports/')):assert sha(R/p)==h,p;preserved+=1
 for a in [*prior_assets,assets]:
  for group in ('inputs','outputs','failed_outputs'):
   for p,h in a.get(group,{}).items():assert sha(R/p)==h,p
 runtime=0
 for p in assets['outputs']:
  if not p.endswith('/environment.json'):continue
  q=R/p;e=json.loads(q.read_text('utf-8'));assert e['exit_code']==0 and(q.parent/'trace_complete.txt').read_text()==str(e['frames'])
  for name,h in e['files'].items():assert sha(q.parent/name)==h;runtime+=1
 failures=[]
 for p in assets['failed_outputs']:
  if not p.endswith('/environment.json'):continue
  q=R/p;e=json.loads(q.read_text('utf-8'));assert e['exit_code']==4294967295 and not(q.parent/'trace_complete.txt').exists()
  for name,h in e['files'].items():assert sha(q.parent/name)==h
  failures.append({'path':p,'exit_code':e['exit_code'],'frozen_files':len(e['files']),'classified':'Incomplete120second trace; correctedV3 successful, notPASS run'})
 initial=json.loads((R/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(R.parent/p)==h,p
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256'];assert sha(R/'scripts/asm6502.py')==sha(R.parent/'Tiny Toon Adventures/scripts/asm6502.py')
 v=json.loads((R/'qa/reports/train043_validation.json').read_text('utf-8'));assert v['status']=='PASS'and v['screens']==6005 and v['IRQ']['rows_exact']==637476
 rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(rows)==54 and sum(x['status']=='draft'for x in rows)==45 and sum(x['status']=='untranslated'for x in rows)==9
 pages=json.loads((R/'qa/dialogue/train043_actual_pages.json').read_text('utf-8'));assert len(pages['pages'])==6 and all(x['direct_reviewed']for x in pages['pages'])
 links=[]
 for p in [R/'README.md',R/'AGENTS.md',*sorted((R/'docs').rglob('*.md'))]:
  for t in re.findall(r'\]\(([^\n]+?)\)',p.read_text('utf-8')):
   t=t.strip().strip('<>').split('#')[0]
   if not t or re.match(r'[a-z]+://',t):continue
   q=(p.parent/t).resolve();assert q.exists()or q==out.resolve(),(p,t);links.append({'document':p.relative_to(R).as_posix(),'target':t})
 assert not list((R/'dist').iterdir())
 result={'work':51,'status':'PASS','adopted_build':'dialogue_kr_poc_043','source_sha256':source['sha256'],'output_sha256':v['ROM_sha256'],'IPS_sha256':v['IPS_sha256'],'scope':'6005screens/637476IRQrows, sixdirectscenes, 2304completeIRQ ABI, original/rebuild/CLIapply; healthdiagnostic declared','source_and_first_game_references_unchanged':True,'historical_artifacts_preserved':preserved,'prior_scoped49_50_inputs_andoutputs_unchanged':True,'runtime_frozen_files':runtime,'preserved_failed_runs':failures,'local_markdown_links_checked':len(links),'links':links,'file_sha256':files,'file_inventory_mode':'Fixed48history plusfrozen49/50/51 assets andcurrentmetadata; laterwork newfilesexcluded','dist_empty':True,'limits':v['limits'],'next_action':v['next_action'],'self_sha256':'Excluded to avoid recursion'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k]for k in ('status','adopted_build','historical_artifacts_preserved','runtime_frozen_files','preserved_failed_runs','local_markdown_links_checked')},indent=2))
if __name__=='__main__':main()
