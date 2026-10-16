"""Archive superseded distribution bundles and provide exact restore; no deletion."""
from pathlib import Path
import argparse,json,re,zipfile
from seal_nonplay171 import R,sha

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--restore');a=ap.parse_args()
    archive=R/'qa/archive/obsolete_distribution223.zip';book=R/'qa/reports/obsolete_distribution223_archive.json'
    if a.restore:
        q=json.loads(book.read_text('utf-8'));assert sha(archive)==q['archive_sha256']
        rel=a.restore.replace('\\','/');assert rel in q['files'] and '..' not in rel.split('/')
        p=R/rel;assert p.resolve().is_relative_to(R)
        for s in [p,*p.parents]:
            if s.is_relative_to(R) and s.exists():assert not s.is_symlink() and not s.stat().st_file_attributes&1024
        with zipfile.ZipFile(archive) as z:raw=z.read(rel)
        import hashlib
        assert hashlib.sha256(raw).hexdigest()==q['files'][rel]['sha256']
        if p.exists():assert sha(p)==q['files'][rel]['sha256']
        else:p.parent.mkdir(parents=True,exist_ok=True);p.open('xb').write(raw)
        print('RESTORED_OR_IDENTICAL: '+rel);return
    assert not archive.exists() and not book.exists()
    pattern=re.compile(r'^TinyToonAdventures2_KR_(Review_|Opening11_|HomeBooth11_|Ordinary11_)')
    roots=[p for p in (R/'dist').iterdir() if pattern.match(p.name)]
    files=sorted(p for root in roots for p in ([root] if root.is_file() else root.rglob('*')) if p.is_file())
    assert files
    records={}
    for p in files:
        assert p.resolve().is_relative_to(R/'dist')
        for s in [p,*p.parents]:
            if s.is_relative_to(R) and s.exists():assert not s.is_symlink() and not s.stat().st_file_attributes&1024
        records[p.relative_to(R).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,p.relative_to(R).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())==set(records)
        for p in files:assert z.read(p.relative_to(R).as_posix())==p.read_bytes()
    q={'work':223,'status':'VERIFIED_NOT_DELETED','archive_sha256':sha(archive),
       'archive':archive.relative_to(R).as_posix(),'archive_bytes':archive.stat().st_size,
       'file_count':len(files),'selected_bytes':sum(x['bytes'] for x in records.values()),'files':records,
       'roots':[{'path':p.relative_to(R).as_posix(),'directory':p.is_dir()} for p in roots],
       'preserved':'Final v1.0 and Cafe ZIP/folder, Candidate062 package needed by immutable release220 reproduction'}
    book.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:q[k] for k in ('status','file_count','selected_bytes','archive_bytes')}))

if __name__=='__main__':main()
