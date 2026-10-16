"""Restore release cleanup history, checking both immutable private archives."""
from pathlib import Path
import argparse,sqlite3,zlib,hashlib,json
from seal_nonplay171 import R,sha

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--file');g.add_argument('--prefix');g.add_argument('--verify',action='store_true');a=ap.parse_args()
    proof=json.loads((R/'qa/reports/cleanup222_predelete.json').read_text('utf-8'))
    paths={k:R/proof['archive'+k] for k in ('214','222')}
    for k,p in paths.items():assert sha(p)==proof['archive'+k+'_sha256']
    dbs={k:sqlite3.connect(f'file:{p.as_posix()}?mode=ro',uri=True) for k,p in paths.items()}
    db=dbs['222'];assert db.execute("SELECT value FROM metadata WHERE key='state'").fetchone()[0]=='VERIFIED'
    if a.verify:
        n=0
        for h,size,data in db.execute('SELECT sha256,raw_bytes,data FROM objects'):
            raw=zlib.decompress(data);assert len(raw)==size and hashlib.sha256(raw).hexdigest()==h;n+=1
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        print(json.dumps({'status':'PASS_PRIVATE_ARCHIVES_SHA_AND_NEW_OBJECTS','new_objects':n}));return
    name=(a.file or a.prefix).replace('\\','/').rstrip('/')
    assert name and not Path(name).is_absolute() and not any(x in ('.','..') for x in name.split('/'))
    query='path=?' if a.file else '(path=? OR substr(path,1,?)=?)'
    args=(name,) if a.file else (name,len(name)+1,name+'/')
    rows=db.execute('SELECT path,sha256,bytes,source_archive FROM entries WHERE '+query+' ORDER BY path',args)
    n=0
    for rel,h,size,source in rows:
        p=R/rel;assert p.resolve().is_relative_to(R) and p.resolve()!=R
        for q in [p,*p.parents]:
            if q.is_relative_to(R) and q.exists():assert not q.is_symlink() and not q.stat().st_file_attributes&1024
        data=dbs[source].execute('SELECT raw_bytes,data FROM objects WHERE sha256=?',(h,)).fetchone()
        assert data and data[0]==size;raw=zlib.decompress(data[1]);assert len(raw)==size and hashlib.sha256(raw).hexdigest()==h
        if p.exists():assert sha(p)==h,'Different existing file: '+rel
        else:p.parent.mkdir(parents=True,exist_ok=True);p.open('xb').write(raw)
        n+=1
    assert n,'No release222 history entry matched; check archive214 for older-only paths'
    print(json.dumps({'status':'RESTORED_OR_IDENTICAL','files':n}))

if __name__=='__main__':main()
