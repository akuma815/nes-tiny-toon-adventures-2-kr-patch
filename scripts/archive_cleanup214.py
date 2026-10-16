"""Lossless private history storage; never deletes source files."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, os, sqlite3, time, zlib

R = Path(__file__).resolve().parents[1]
W = R / 'work/cleanup214'

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()

def safe(n):
    p = R / n
    assert p.resolve().is_relative_to(R) and p.resolve() != R, n
    assert not any(q.is_symlink() or (q.exists() and q.stat().st_file_attributes & 1024)
                   for q in [p, *p.parents] if q.is_relative_to(R)), n
    return p

def read(item):
    p = safe(item['path'])
    st = p.stat()
    raw = p.read_bytes()
    assert len(raw) == item['bytes'] == st.st_size, item['path']
    assert p.stat().st_mtime_ns == st.st_mtime_ns, item['path']
    return item['path'], hashlib.sha256(raw).hexdigest(), len(raw), st.st_mtime_ns // 100 + 116444736000000000, zlib.compress(raw, 3)

def main():
    plan = json.loads((W / 'plan.json').read_text('utf-8'))
    assert Path(plan['root']).resolve() == R
    # A current builder reads this older metadata directly rather than through a document link.
    plan['retain_live_files'] = sorted(set(plan['retain_live_files']) | {'build/dialogue_kr_poc_037/ui_korean_page_mapping.json'})
    archive = safe(plan['archive_path'])
    archive.parent.mkdir(exist_ok=True)
    assert not archive.exists(), 'Refuse replacing an existing archive'
    db = sqlite3.connect(archive)
    db.executescript('PRAGMA journal_mode=DELETE; PRAGMA synchronous=NORMAL; CREATE TABLE objects(sha256 TEXT PRIMARY KEY, raw_bytes INTEGER NOT NULL, data BLOB NOT NULL) WITHOUT ROWID; CREATE TABLE entries(path TEXT PRIMARY KEY, sha256 TEXT NOT NULL REFERENCES objects(sha256), bytes INTEGER NOT NULL, mtime_filetime INTEGER NOT NULL) WITHOUT ROWID; CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL) WITHOUT ROWID;')
    db.execute('INSERT INTO metadata VALUES(?,?)', ('state', 'BUILDING'))
    db.execute('INSERT INTO metadata VALUES(?,?)', ('root', str(R)))
    seen = set()
    groups = {n: {'path': n, 'files': 0, 'bytes': 0, 'max_filetime': 0} for n in plan['directory_targets']}
    # All targets are disjoint top-level run directories.
    def group(n):
        parts = n.split('/')
        return '/'.join(parts[:3] if parts[0] == 'qa' else parts[:2])
    started = time.monotonic()
    files = plan['files_to_archive']
    with ThreadPoolExecutor(max_workers=4) as pool:
        for start in range(0, len(files), 2000):
            for n, h, size, ticks, compressed in pool.map(read, files[start:start+2000]):
                if h not in seen:
                    db.execute('INSERT INTO objects VALUES(?,?,?)', (h, size, compressed))
                    seen.add(h)
                db.execute('INSERT INTO entries VALUES(?,?,?,?)', (n,h,size,ticks))
                g = groups[group(n)]
                g['files'] += 1; g['bytes'] += size; g['max_filetime'] = max(g['max_filetime'], ticks)
            db.commit()
            if start % 10000 == 0:
                print(json.dumps({'archived': min(start+2000,len(files)), 'total': len(files), 'unique_objects': len(seen), 'seconds': round(time.monotonic()-started)}), flush=True)
    assert db.execute('SELECT count(*),sum(bytes) FROM entries').fetchone() == (len(files),plan['selected_bytes'])
    assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    checked = 0
    for h, size, compressed in db.execute('SELECT sha256,raw_bytes,data FROM objects'):
        raw = zlib.decompress(compressed)
        assert len(raw) == size and hashlib.sha256(raw).hexdigest() == h, h
        checked += 1
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    staging = safe('work/cleanup214/retained_live')
    staging.mkdir()
    retained_bytes = 0
    for n in plan['retain_live_files']:
        row = db.execute('SELECT e.sha256,e.bytes,o.data FROM entries e JOIN objects o USING(sha256) WHERE e.path=?', (n,)).fetchone()
        assert row is not None, n
        h, size, compressed = row
        raw = zlib.decompress(compressed)
        assert hashlib.sha256(raw).hexdigest() == h
        p = staging / n; p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f: f.write(raw)
        assert digest(p) == h, n
        retained_bytes += size
        g = groups[group(n)]
        g['restore_files'] = g.get('restore_files',0)+1
        g['restore_bytes'] = g.get('restore_bytes',0)+size
    db.execute('UPDATE metadata SET value=? WHERE key=?', ('VERIFIED','state'))
    db.commit(); db.close()
    archive_hash = digest(archive)
    compact = {'work':214, 'root':str(R), 'status':'VERIFIED_NOT_DELETED', 'archive_path':plan['archive_path'], 'archive_sha256':archive_hash,
               'staging_path':'work/cleanup214/retained_live', 'directories':list(groups.values()), 'cache_directory_targets':plan['cache_directory_targets']}
    (W / 'deletion_plan.json').write_text(json.dumps(compact,indent=2)+'\n','utf-8')
    report = {'work':214,'status':'ALL_ARCHIVE_OBJECTS_AND_STAGING_HASH_VERIFIED','archive_path':plan['archive_path'],'archive_sha256':archive_hash,
              'archive_bytes':archive.stat().st_size,'entries':len(files),'unique_objects':checked,'selected_bytes':plan['selected_bytes'],
              'restored_live_files':len(plan['retain_live_files']),'restored_live_bytes':retained_bytes,'directories':len(groups),
              'all_objects_decompressed_and_SHA256_verified':True,'sqlite_integrity_check':'ok','runtime':'NOT_RUN','seconds':round(time.monotonic()-started)}
    (R / 'qa/reports/cleanup214_archive.json').write_text(json.dumps(report,indent=2)+'\n','utf-8')
    print(json.dumps(report,indent=2),flush=True)

if __name__ == '__main__': main()
