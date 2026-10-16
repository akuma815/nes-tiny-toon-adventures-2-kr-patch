from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
old=R/'scripts/make_review_package049_132.py';new=R/'scripts/make_review_package049_132_v2.py';obs=R/'qa/reports/review049_package132_v1_observation.json'
assert not new.exists() and not obs.exists()
statuses={n:json.loads((R/'qa/reports'/(n+'.json')).read_text('utf-8'))['status'] for n in ['clear128_validation','clear129_validation','pages130_validation','review049_validation131','review049_131_session']}
s=old.read_text('utf-8');before="assert j['status']=='PASS';reports[name]";assert s.count(before)==1
s=s.replace(before,"assert j['status']=="+repr(statuses)+"[name];reports[name]");new.write_text(s,'utf-8')
obs.write_text(json.dumps({'work':132,'status':'EXPECTED_STATUS_GUARD_FAILED_BEFORE_PACKAGE_OUTPUT','failed_script_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'reason':'Specific bounded success statuses were mistakenly required to equal simple PASS. Explicit frozen expected statuses used in v2.','actual_statuses':statuses,'package_output_exists':(R/'dist/TinyToonAdventures2_KR_Review_049_20261006').exists(),'preparation_shell_error':'First inline Python preparation was rejected by PowerShell quoting before any file was written; this file avoids inline quoting.'},indent=2)+'\n','utf-8')
