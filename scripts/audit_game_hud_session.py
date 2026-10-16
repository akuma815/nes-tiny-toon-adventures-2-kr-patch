"""Frozen040 inputs/outputs, runtime records, protected039 history, handoff links."""
import csv,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/game_hud_session_20261005.json';assets=json.loads((R/'manifests/game_hud_assets.json').read_text('utf-8'))
 for group in ('inputs','outputs'):
  for p,h in assets[group].items():assert sha(R/p)==h,p
 runtime=0
 for p in assets['outputs']:
  if not p.endswith('/environment.json'):continue
  env=json.loads((R/p).read_text('utf-8'));d=(R/p).parent;assert env['exit_code']==0 and (d/'trace_complete.txt').read_text()==str(env['frames'])
  for name,h in env['files'].items():assert sha(d/name)==h,(p,name);runtime+=1
 initial=json.loads((R/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(R.parent/p)==h,p
 assert sha(R.parent/'Tiny Toon Adventures/scripts/asm6502.py')==sha(R/'scripts/asm6502.py');source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 history=json.loads((R/'qa/reports/booth_graphics_session_20261005.json').read_text('utf-8'));preserved=0
 for p,h in history['file_sha256'].items():
  if p.startswith(('build/','qa/dialogue/','tools/python/','work/dialogue_font/','qa/reports/')):assert sha(R/p)==h,p;preserved+=1
 rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(rows)==54 and sum(x['status']=='draft' for x in rows)==45 and sum(x['status']=='untranslated' for x in rows)==9
 v=json.loads((R/'qa/reports/game040_validation.json').read_text('utf-8'));assert v['status']=='PASS' and v['screens']==4558 and v['actual_IRQ_rows_exact']==1321047;assert not list((R/'dist').iterdir());links=[]
 for p in [R/'README.md',R/'AGENTS.md',*sorted((R/'docs').rglob('*.md'))]:
  for t in re.findall(r'\]\(([^\n]+?)\)',p.read_text('utf-8')):
   t=t.strip().strip('<>').split('#')[0]
   if not t or re.match(r'[a-z]+://',t):continue
   resolved=(p.parent/t).resolve();assert resolved.exists() or resolved==out.resolve(),(p,t);links.append({'document':p.relative_to(R).as_posix(),'target':t})
 files={}
 for folder in ('scripts','docs','manifests','workspace/translation','workspace/asm','backups/translation','build','qa/dialogue'):
  for p in sorted((R/folder).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(R).as_posix()]=sha(p)
 for p in [R/'README.md',*sorted((R/'qa/reports').glob('*.json'))]:
  if p!=out:files[p.relative_to(R).as_posix()]=sha(p)
 result={'date':'2026-10-05','status':'PASS','adopted_build':'dialogue_kr_poc_040','source_sha256':source['sha256'],'output_sha256':v['ROM_sha256'],'IPS_sha256':v['IPS_sha256'],'scope':'Works43actualHUD survey/44KoreanHUD;4558screens/1321047IRQ rows plus direct6scenes; bonus preparation remainsseparate','source_and_first_game_references_unchanged':True,'historical_artifacts_preserved':preserved,'runtime_frozen_files':runtime,'local_markdown_links_checked':len(links),'links':links,'file_sha256':files,'registered_translation_rows':{'draft':45,'technical_or_shared_untranslated':9},'dist_empty':True,'next_action':'Native bonus result font124/CHR24A0B consumer survey and sevenKoreanlabels','limits':v['limits'],'self_sha256':'Excluded to avoid recursion'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ('status','adopted_build','historical_artifacts_preserved','runtime_frozen_files','local_markdown_links_checked')},indent=2))
if __name__=='__main__':main()
