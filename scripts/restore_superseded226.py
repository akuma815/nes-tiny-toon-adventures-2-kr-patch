"""Recover a superseded public ZIP by exact archived relative path."""
import argparse,json,zipfile,hashlib
from seal_nonplay171 import R,sha
ap=argparse.ArgumentParser();ap.add_argument('--file',required=True);a=ap.parse_args()
q=json.loads((R/'qa/reports/cleanup226_plan.json').read_text('utf-8'))
assert a.file in q['archived_files'];p=R/a.file;assert p.resolve().is_relative_to(R)
archive=R/q['archive'];assert sha(archive)==q['archive_sha256']
with zipfile.ZipFile(archive) as z:data=z.read(a.file)
assert hashlib.sha256(data).hexdigest()==q['archived_files'][a.file]['sha256']
if p.exists():assert p.read_bytes()==data,'Existing different file refused'
else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
print('PASS exact recovery '+a.file)
