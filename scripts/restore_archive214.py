"""Restore exact project history from private archive; refuse different live files."""
from pathlib import Path
import argparse, hashlib, json, sqlite3, zlib
R = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--file'); g.add_argument('--prefix'); g.add_argument('--verify',action='store_true')
    args = ap.parse_args()
    archive = R / 'qa/archive/cleanup214_history.sqlite'
    expected = json.loads((R/'qa/reports/cleanup214_archive.json').read_text('utf-8'))['archive_sha256']
    whole = hashlib.sha256()
    with archive.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''): whole.update(chunk)
    assert whole.hexdigest() == expected, 'Archive file SHA256 mismatch'
    db = sqlite3.connect(f'file:{archive.as_posix()}?mode=ro',uri=True)
    assert db.execute('SELECT value FROM metadata WHERE key="state"').fetchone()[0] == 'VERIFIED'
    if args.verify:
        count = 0
        for h,size,b in db.execute('SELECT sha256,raw_bytes,data FROM objects'):
            raw = zlib.decompress(b)
            assert len(raw)==size and hashlib.sha256(raw).hexdigest()==h
            count += 1
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        print('VERIFIED unique objects:',count); return
    n = (args.file or args.prefix).replace('\\','/').rstrip('/')
    assert n and not any(p in ('..','.') for p in n.split('/')) and not Path(n).is_absolute()
    query = 'e.path=?' if args.file else '(e.path=? OR substr(e.path,1,?)=?)'
    values = (n,) if args.file else (n,len(n)+1,n+'/')
    rows = db.execute('SELECT e.path,e.sha256,e.bytes,o.data FROM entries e JOIN objects o USING(sha256) WHERE '+query+' ORDER BY e.path',values)
    count = 0
    for name,h,size,b in rows:
        p = R / name
        assert p.resolve().is_relative_to(R) and p.resolve()!=R
        assert not any(q.is_symlink() or (q.exists() and q.stat().st_file_attributes & 1024) for q in [p,*p.parents] if q.is_relative_to(R))
        raw = zlib.decompress(b)
        assert len(raw)==size and hashlib.sha256(raw).hexdigest()==h
        if p.exists():
            assert hashlib.sha256(p.read_bytes()).hexdigest()==h, 'Different existing file: '+name
        else:
            p.parent.mkdir(parents=True,exist_ok=True)
            with p.open('xb') as f: f.write(raw)
        count += 1
    assert count, 'No archived entries matched'
    print('RESTORED/IDENTICAL files:',count)

if __name__=='__main__': main()
