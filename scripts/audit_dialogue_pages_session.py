"""Verify current pages008 pins, preserved historical artifacts, first-game references and doc links."""
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=ROOT/'qa/reports/dialogue_pages_session_20261005.json'
 manifest=json.loads((ROOT/'manifests/dialogue_pages_assets.json').read_text('utf-8'))
 for group in ('inputs','outputs'):
  for p,h in manifest[group].items():assert sha(ROOT/p)==h,p
 runtime_files=0
 for p in manifest['outputs']:
  if not p.endswith('/environment.json'):continue
  env=json.loads((ROOT/p).read_text('utf-8'));assert env['exit_code']==0
  directory=(ROOT/p).parent;assert (directory/'trace_complete.txt').read_text()==str(env['frames'])
  for name,h in env['files'].items():assert sha(directory/name)==h,(p,name);runtime_files+=1
 initial=json.loads((ROOT/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(ROOT.parent/p)==h,p
 history=json.loads((ROOT/'qa/reports/dialogue_home_session_20261004.json').read_text('utf-8'));preserved=0
 for p,h in history['file_sha256'].items():
  if p.startswith(('build/','qa/dialogue/','tools/python/','work/dialogue_font/')) or (p.startswith('qa/reports/') and p.endswith('.json')):
   assert sha(ROOT/p)==h,p;preserved+=1
 old=ROOT.parent/'Tiny Toon Adventures/scripts/asm6502.py';assert sha(old)==sha(ROOT/'scripts/asm6502.py')
 source=json.loads((ROOT/'manifests/source_rom.json').read_text('utf-8'));assert sha(ROOT/source['path'])==source['sha256']
 assert not list((ROOT/'dist').iterdir())
 rows=list(csv.DictReader((ROOT/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig',newline='')));assert len(rows)==54 and sum(x['status']=='draft' for x in rows)==3 and sum(x['status']=='untranslated' for x in rows)==51
 validation=json.loads((ROOT/'qa/reports/dialogue_pages008_validation.json').read_text('utf-8'));assert validation['status']=='PASS' and validation['matched_screens']==850 and validation['outside_text_pixels']==0
 cpu=json.loads((ROOT/'qa/reports/pages008_hooks_final.json').read_text('utf-8'));assert cpu['abi_cases']==784 and cpu['broken004_control_rejected'] and cpu['all_added_hook_cycles_multiple_of19']
 links=[]
 for p in [ROOT/'README.md',ROOT/'AGENTS.md',*sorted((ROOT/'docs').rglob('*.md'))]:
  for target in re.findall(r'\]\(([^\n]+?)\)',p.read_text('utf-8')):
   target=target.strip().strip('<>').split('#')[0]
   if not target or re.match(r'[a-z]+://',target):continue
   resolved=(p.parent/target).resolve();assert resolved.exists() or resolved==out.resolve(),(p,target);links.append({'document':p.relative_to(ROOT).as_posix(),'target':target})
 files={}
 for folder in ('scripts','docs','manifests','workspace/translation','workspace/asm','backups/translation','build','qa/dialogue','work/dialogue_font'):
  for p in sorted((ROOT/folder).rglob('*')):
   if p.is_file() and '__pycache__' not in p.parts:files[p.relative_to(ROOT).as_posix()]=sha(p)
 for p in [ROOT/'README.md',*sorted((ROOT/'qa/reports').glob('*.json'))]:
  if p!=out:files[p.relative_to(ROOT).as_posix()]=sha(p)
 result={'date':'2026-10-05','status':'PASS','adopted_build':'dialogue_kr_poc_008','source_sha256':source['sha256'],'output_sha256':validation['output_sha256'],'scope':'Work11 failures and work12 second-page latch/IRQ phase correction; development only','source_first_game_references_and_copied_assembler_unchanged':True,'historical_artifacts_verified':preserved,'translation_rows':{'draft':3,'untranslated':51},'dist_empty':True,'matched_screens':850,'file_sha256':files,'links':links,'local_markdown_links_checked':len(links),'next_action':'Translate MAIN_0564D and extend page-font registration; verify print/wait/clear/next/reentry','self_sha256':'Excluded to avoid recursion','limits':validation['limits']}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'status':'PASS','file_hashes':len(files),'links':len(links),'historical_artifacts_preserved':preserved,'runtime_frozen_files':runtime_files,'adopted':'dialogue_kr_poc_008'},indent=2))
if __name__=='__main__':main()
