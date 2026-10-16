"""Keep a compact immutable live-file hash index before discarding staging."""
import json, sqlite3
from archive_cleanup214 import R, digest

plan = json.loads((R/'work/cleanup214/deletion_plan.json').read_text('utf-8'))
assert digest(R/plan['archive_path']) == plan['archive_sha256']
db = sqlite3.connect(f'file:{(R/plan["archive_path"]).as_posix()}?mode=ro',uri=True)
staging = R/plan['staging_path']
files = {}
for p in staging.rglob('*'):
    if p.is_file():
        n = p.relative_to(staging).as_posix()
        h = db.execute('SELECT sha256 FROM entries WHERE path=?',(n,)).fetchone()[0]
        assert digest(p) == h
        files[n] = h
out = R/'manifests/cleanup214_retained_live.json'
assert not out.exists()
out.write_text(json.dumps({'work':214,'archive_sha256':plan['archive_sha256'],'files':files},indent=2)+'\n','utf-8')
db.close()
print('Retained live file hashes:',len(files))
