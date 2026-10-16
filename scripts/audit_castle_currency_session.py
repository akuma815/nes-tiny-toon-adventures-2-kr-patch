from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/castle_currency053_session.json';assert not out.exists();v=json.loads((R/'qa/reports/castle_currency053.json').read_text('utf-8'));assert v['status']=='PASS'
 for p,h in v['frozen_files'].items():assert sha(R/p)==h,p
 first=json.loads((R/'qa/reports/initial_session_20261004.json').read_text('utf-8'))
 for p,h in first['first_game_references'].items():assert sha(R.parent/p)==h,p
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256'];assert sha(R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes')==v['ROM_sha256']
 pages=json.loads((R/'qa/dialogue/castle053_actual_pages.json').read_text('utf-8'));assert len(pages['pages'])==4
 for p in pages['pages']:assert p['direct_reviewed'] and sha(R/p['source'])==p['sha256']
 historical=json.loads((R/'qa/reports/train_sign051_session.json').read_text('utf-8'));assert historical['status']=='PASS'
 result={'work':53,'status':'PASS','scope':'Frozen53 files/source/first-game/4direct pages and reference to full51 preservation audit; HUD suspicion resolved only by separate54 report','frozen_files_checked':len(v['frozen_files']),'historical051_audit_sha256':sha(R/'qa/reports/train_sign051_session.json'),'source_and_first_game_unchanged':True,'ROM_sha256':v['ROM_sha256'],'final_release_status':'No release assembled yet'}
 out.write_text(json.dumps(result,indent=2)+'\n','utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
