"""Verify the interrupted run against archive before the faster native PS continuation."""
import json, os, sqlite3
from archive_cleanup214 import R, digest, safe

plan = json.loads((R/'work/cleanup214/deletion_plan.json').read_text('utf-8'))
assert digest(R/plan['archive_path']) == plan['archive_sha256']
events = [json.loads(n) for n in (R/'work/cleanup214/deletion_progress.jsonl').read_text('utf-8-sig').splitlines() if n.strip()]
complete = {x['path'] for x in events if x['phase']=='completed'}
partial = {x['path'] for x in events if x['phase']=='validated'} - complete
assert len(partial) <= 1
db = sqlite3.connect(f'file:{(R/plan["archive_path"]).as_posix()}?mode=ro',uri=True)
states = []
for n in sorted(partial):
    p = safe(n); count = size = max_time = 0
    if p.exists():
        for base,dirs,files in os.walk(p,followlinks=False):
            for name in dirs: safe((__import__('pathlib').Path(base)/name).relative_to(R).as_posix())
            for name in files:
                f = __import__('pathlib').Path(base)/name
                rel = f.relative_to(R).as_posix(); safe(rel)
                expected = db.execute('SELECT sha256 FROM entries WHERE path=?',(rel,)).fetchone()
                assert expected and digest(f)==expected[0],rel
                st = f.stat();count+=1;size+=st.st_size;max_time=max(max_time,st.st_mtime_ns//100+116444736000000000)
    states.append({'path':n,'files':count,'bytes':size,'max_filetime':max_time,'exists':p.exists(),'remaining_files_SHA256_checked':True})
out=R/'work/cleanup214/resume_verified.json'
assert not out.exists()
out.write_text(json.dumps({'status':'PASS','archive_sha256':plan['archive_sha256'],'completed_directories':len(complete),'partial':states},indent=2)+'\n','utf-8')
db.close()
print(out.read_text('utf-8'))
