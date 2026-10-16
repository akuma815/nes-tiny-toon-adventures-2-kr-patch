"""Current home003 provenance, historical frozen artifacts, source/reference and link audit."""
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=ROOT/'qa/reports/dialogue_home_session_20261004.json'
 source=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));assert sha(ROOT/source['path'])==source['sha256']
 initial=json.loads((ROOT/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(ROOT.parent/p)==h,p
 historical=json.loads((ROOT/'qa/reports/dialogue_session_20261004.json').read_text('utf-8'))
 for p,h in historical['file_sha256'].items():
  if p.startswith(('build/dialogue_kr_poc_','qa/dialogue/','tools/python/')):assert sha(ROOT/p)==h,p
 assets=json.loads((ROOT/'manifests/dialogue_home_assets.json').read_text('utf-8'))
 for group in ('inputs','outputs'):
  for p,h in assets[group].items():assert sha(ROOT/p)==h,p
 rows=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')))
 assert len(rows)==54 and sum(x['status']=='draft' for x in rows)==2 and sum(x['status']=='untranslated' for x in rows)==52
 assert not list((ROOT/'dist').iterdir())
 validation=json.loads((ROOT/'qa/reports/dialogue_home003_validation.json').read_text('utf-8'));assert validation['status']=='PASS' and validation['runtime_samples']==437 and validation['outside_home_prompt_pixel_differences']==0
 links=[]
 for p in [ROOT/'README.md',ROOT/'AGENTS.md',*sorted((ROOT/'docs').rglob('*.md'))]:
  for target in re.findall(r'\]\(([^\n]+?)\)',p.read_text('utf-8')):
   target=target.strip().strip('<>').split('#')[0]
   if not target or re.match(r'[a-z]+://',target):continue
   resolved=(p.parent/target).resolve()
   assert resolved.exists() or resolved==out.resolve(),(p,target);links.append({'document':p.relative_to(ROOT).as_posix(),'target':target})
 files={}
 for folder in ('scripts','docs','manifests','workspace/translation','workspace/fonts','backups/translation','build/dialogue_kr_poc_003','build/dialogue_kr_poc_003_rebuild','qa/dialogue','work/dialogue_font'):
  for p in sorted((ROOT/folder).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(ROOT).as_posix()]=sha(p)
 for p in [ROOT/'README.md',*sorted((ROOT/'qa/reports').glob('dialogue_*.json'))]:
  if p!=out:files[p.relative_to(ROOT).as_posix()]=sha(p)
 result={'date':'2026-10-04','status':'PASS','scope':'Handoff work10: home003 and intro font lifetime investigation; dynamic second-page switch not implemented','adopted_build':'dialogue_kr_poc_003','source_sha256':source['sha256'],'output_sha256':validation['output_sha256'],'translation_rows':{'draft':2,'untranslated':52},'source_and_first_game_reference_hashes_unchanged':True,'historical_dialogue_builds_runtime_evidence_and_py65_preserved':True,'dist_empty':True,'file_sha256':files,'links':links,'local_markdown_links_checked':len(links),'evidence_classes':{'static':'250 Expected Writes, source/first-font/title/SSOT guards','cpu':'First37/3282 and home12/1246 per-call equal; unadopted second43/4245 equal','build_apply':'Rebuild and actual clean-source IPS application equal','emulator':'437 matched samples;172 home text only/265 identical; outside0','direct_visual':'Actual1080 and930/940/1080 comparison reviewed; final human wording/design review pending'},'next_action':'Implement page font latch at verified clear/init boundary; insert MAIN_05625 and validate wait/next-Japanese/reentry.','self_sha256':'Excluded to avoid recursive hash.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert all((ROOT/v['document']).parent.joinpath(v['target']).exists() for v in links)
 print(json.dumps({'status':'PASS','file_hashes':len(files),'links':len(links),'source_first_game_and_historical_evidence_unchanged':True},indent=2))
if __name__=='__main__':main()
