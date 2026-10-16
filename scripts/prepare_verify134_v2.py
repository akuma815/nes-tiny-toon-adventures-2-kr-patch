from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
p=R/'scripts/verify_live134_v2.py';obs=R/'qa/reports/live134_verifier_v1_observation.json';assert not p.exists() and not obs.exists()
s=(R/'scripts/verify_live134.py').read_text('utf-8');s=s.replace("==int(b[1]['cycle'])-int(b[0]['cycle'])==87","==int(b[1]['cycle'])-int(b[0]['cycle'])")
s=s.replace("'entry_cycle_delta':int(b[0]['cycle'])-int(a[0]['cycle'])","'common_live_prefix_elapsed':int(a[1]['cycle'])-int(a[0]['cycle']),'entry_cycle_delta':int(b[0]['cycle'])-int(a[0]['cycle'])")
p.write_text(s,'utf-8');obs.write_text(json.dumps({'work':134,'status':'FAILED_FIXED_PREFIX87_GUARD','reason':'Actual pre-helper elapsed values87/90/91 were equal between both builds but were incorrectly required to always87. v2 verifies paired equality and records actual elapsed rather than assuming instruction-only time. Probe data/ROM unchanged.'},indent=2)+'\n','utf-8')
