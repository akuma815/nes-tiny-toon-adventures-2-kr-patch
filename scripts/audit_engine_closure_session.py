from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/engine_closure052_session.json';assert not out.exists();a=json.loads((R/'manifests/engine_closure_assets.json').read_text('utf-8'))
 for p,h in a['files'].items():assert sha(R/p)==h,p
 initial=json.loads((R/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in initial['first_game_references'].items():assert sha(R.parent/p)==h,p
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 links=0
 for p in [R/'README.md',R/'AGENTS.md',*sorted((R/'docs').rglob('*.md'))]:
  for angle,plain in re.findall(r'\]\((?:<([^>\n]+)>|([^()\n]+))\)',p.read_text('utf-8')):
   t=(angle or plain).strip().split('#')[0]
   if not t or re.match('[a-z]+://',t):continue
   q=(p.parent/t).resolve();assert q.exists()or q==(R/'qa/reports/train_sign051_session.json').resolve(),(p,t);links+=1
 result={'work':52,'status':'PASS','frozen_files':len(a['files']),'asset_manifest_sha256':sha(R/'manifests/engine_closure_assets.json'),'source_and_first_game_refs_unchanged':True,'current43_SHA':sha(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes'),'local_links_checked':links,'audit51_report_pending':not(R/'qa/reports/train_sign051_session.json').exists(),'limits':'Scoped52 artifact/source/first-game/link checks; not another global historical rehash.'}
 out.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
