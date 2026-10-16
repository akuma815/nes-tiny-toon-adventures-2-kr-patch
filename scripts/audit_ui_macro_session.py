"""Current fourth013 pins, direct013 evidence, preserved history and handoff link audit."""
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=ROOT/'qa/reports/ui_macro_session_20261005.json';assets=json.loads((ROOT/'manifests/ui_macro_assets.json').read_text('utf-8'))
 for group in ('inputs','outputs'):
  for p,h in assets[group].items():assert sha(ROOT/p)==h,p
 runtime_files=0
 for p in assets['outputs']:
  if not p.endswith('/environment.json'):continue
  env=json.loads((ROOT/p).read_text('utf-8'));assert env['exit_code']==0;d=(ROOT/p).parent;assert (d/'trace_complete.txt').read_text()==str(env['frames'])
  for name,h in env['files'].items():assert sha(d/name)==h,(p,name);runtime_files+=1
 initial=json.loads((ROOT/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(ROOT.parent/p)==h,p
 assert sha(ROOT.parent/'Tiny Toon Adventures/scripts/asm6502.py')==sha(ROOT/'scripts/asm6502.py')
 source=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));assert sha(ROOT/source['path'])==source['sha256']
 history=json.loads((ROOT/'qa/reports/ui_font_latch_session_20261005.json').read_text('utf-8'));preserved=0
 for p,h in history['file_sha256'].items():
  if p.startswith(('build/','qa/dialogue/','tools/python/','work/dialogue_font/')) or p.startswith('qa/reports/'):
   assert sha(ROOT/p)==h,p;preserved+=1
 rows=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(rows)==54 and sum(x['status']=='draft' for x in rows)==10 and sum(x['status']=='untranslated' for x in rows)==44
 validation=json.loads((ROOT/'qa/reports/macro019_validation.json').read_text('utf-8'));assert validation['status']=='PASS' and validation['matched_screens']==679 and validation['whole_frame_pixel_differences']==0
 assert not list((ROOT/'dist').iterdir())
 links=[]
 for p in [ROOT/'README.md',ROOT/'AGENTS.md',*sorted((ROOT/'docs').rglob('*.md'))]:
  for t in re.findall(r'\]\(([^\n]+?)\)',p.read_text('utf-8')):
   t=t.strip().strip('<>').split('#')[0]
   if not t or re.match(r'[a-z]+://',t):continue
   resolved=(p.parent/t).resolve();assert resolved.exists() or resolved==out.resolve(),(p,t);links.append({'document':p.relative_to(ROOT).as_posix(),'target':t})
 files={}
 for folder in ('scripts','docs','manifests','workspace/translation','workspace/asm','backups/translation','build','qa/dialogue'):
  for p in sorted((ROOT/folder).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(ROOT).as_posix()]=sha(p)
 for p in [ROOT/'README.md',*sorted((ROOT/'qa/reports').glob('*.json'))]:
  if p!=out:files[p.relative_to(ROOT).as_posix()]=sha(p)
 result={'date':'2026-10-05','status':'PASS','adopted_build':'dialogue_kr_poc_019','source_sha256':source['sha256'],'output_sha256':validation['output_sha256'],'scope':'Work19/20 macro019 Japanese passthrough; rejected018 retained','source_and_first_game_references_unchanged':True,'historical_artifacts_preserved':preserved,'translation_rows':{'draft':10,'untranslated':44},'matched_screens':679,'runtime_frozen_files':runtime_files,'local_markdown_links_checked':len(links),'links':links,'file_sha256':files,'dist_empty':True,'next_action':'Translate observed home and booth8 main units with private fonts150..165','limits':validation['limits'],'self_sha256':'Excluded to avoid recursion'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ['status','adopted_build','historical_artifacts_preserved','runtime_frozen_files','local_markdown_links_checked']},indent=2))
if __name__=='__main__':main()
