"""Verify or recover exact historical paths from private cleanup230 archive."""
import argparse, hashlib, json, os, zipfile
from prepare_cleanup230 import R, ROOTS, PLAN, digest, safe

def main():
    ap=argparse.ArgumentParser();select=ap.add_mutually_exclusive_group(required=True)
    select.add_argument('--file');select.add_argument('--root',choices=ROOTS);select.add_argument('--verify-all',action='store_true');a=ap.parse_args()
    plan=json.loads(PLAN.read_text('utf-8'));assert plan['work']==230 and plan['root']==str(R)
    archive=R/plan['archive'];assert digest(archive)==plan['archive_sha256']
    if a.verify_all:chosen=list(plan['archived_files'])
    elif a.file:
        assert a.file in plan['archived_files'];chosen=[a.file]
    else:chosen=[rel for rel in plan['archived_files'] if rel==a.root or rel.startswith(a.root+'/')]
    assert chosen
    with zipfile.ZipFile(archive) as z:
        for rel in chosen:
            assert any(rel==root or rel.startswith(root+'/') for root in ROOTS)
            expected=plan['archived_files'][rel];data=z.read(rel)
            assert len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'],rel
            if a.verify_all:continue
            p=safe(R/rel)
            if p.exists():assert p.is_file() and digest(p)==expected['sha256'],'Different existing file refused: '+rel
            else:
                p.parent.mkdir(parents=True,exist_ok=True);safe(p)
                with p.open('xb') as dest:dest.write(data)
                os.utime(p,ns=(expected['mtime_ns'],expected['mtime_ns']))
                assert digest(p)==expected['sha256'],rel
    print(json.dumps({'status':'PASS','action':'VERIFY_ALL' if a.verify_all else 'EXACT_RECOVERY','files':len(chosen),'archive_public_upload':False}))

if __name__=='__main__':main()
