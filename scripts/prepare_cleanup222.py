"""Lossless history supplement and exact-path cleanup plan; never deletes files."""
from pathlib import Path
from collections import defaultdict
import hashlib,json,sqlite3,zlib,shutil,time
from seal_nonplay171 import R,sha

def dump(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n','utf-8')
def safe(p):
    p=p.resolve();assert p.is_relative_to(R.resolve()) and p!=R.resolve()
    for z in [p,*p.parents]:
        if z.is_relative_to(R) and z.exists():assert not z.is_symlink() and not z.stat().st_file_attributes&1024,z
    return p
def snapshot(p):
    files=[z for z in p.rglob('*') if z.is_file()];sizes=[z.stat() for z in files]
    return {'files':len(files),'bytes':sum(s.st_size for s in sizes),'max_mtime_ns':max((s.st_mtime_ns for s in sizes),default=0)}

def main():
    work=R/'work/cleanup222';work.mkdir(exist_ok=False)
    archive=R/'qa/archive/release222_history.sqlite';assert not archive.exists()
    old=R/'qa/archive/cleanup214_history.sqlite'
    oldhash=json.loads((R/'qa/reports/cleanup214_archive.json').read_text('utf-8'))['archive_sha256']
    assert sha(old)==oldhash
    prior=sqlite3.connect(f'file:{old.as_posix()}?mode=ro',uri=True)
    keep=set()
    for n in range(197,222):
        p=R/f'manifests/nonplay{n}_assets.json'
        if p.exists():keep.update(json.loads(p.read_text('utf-8'))['files'])
    for item in json.loads((R/'qa/reports/publication221_sources.json').read_text('utf-8'))['figures']:
        keep.update(z['path'] for z in item['sources'])
    keep.add('qa/release/release220_apply/apply_verification.json')
    db=sqlite3.connect(archive);db.executescript('''
      CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);
      CREATE TABLE objects(sha256 TEXT PRIMARY KEY,raw_bytes INTEGER,data BLOB);
      CREATE TABLE entries(path TEXT PRIMARY KEY,sha256 TEXT,bytes INTEGER,mtime_ns INTEGER,source_archive TEXT);
      CREATE TABLE retained(path TEXT PRIMARY KEY,sha256 TEXT,bytes INTEGER);
      INSERT INTO metadata VALUES('state','BUILDING');
    ''')
    groups=[];file_targets=[];stats=defaultdict(int);staging=work/'preserve_live';staging.mkdir()
    blocked=R/'qa/dialogue/booth039_font_probe'
    # These are completed historical capture folders. User-owned emulator/save
    # directories, originals, translation sources and final artifacts are not selected.
    candidates=[p for p in (R/'qa/dialogue').iterdir() if p.is_dir() and p!=blocked]
    candidates += [R/'qa/release/release220_apply',R/'build/release220_compile',
      R/'workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009',
      R/'workspace/publication/TinyToon2_KR_v1.0_NaverCafe_Worklog_20261009_002']
    for i,p in enumerate(candidates):
        if not p.exists():continue
        safe(p);snap=snapshot(p)
        if not snap['files']:continue
        kept=[]
        for f in sorted(p.rglob('*')):
            if not f.is_file():continue
            safe(f);rel=f.relative_to(R).as_posix();raw=f.read_bytes();h=hashlib.sha256(raw).hexdigest();size=len(raw)
            if rel in keep:
                dst=staging/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dst);assert sha(dst)==h
                db.execute('INSERT OR IGNORE INTO retained VALUES(?,?,?)',(rel,h,size));kept.append({'path':rel,'sha256':h,'bytes':size})
                stats['retained_files']+=1;stats['retained_bytes']+=size;continue
            prev=prior.execute('SELECT sha256,bytes FROM entries WHERE path=?',(rel,)).fetchone()
            if prev==(h,size):source='214';stats['already_archived_files']+=1
            else:
                source='222'
                if not db.execute('SELECT 1 FROM objects WHERE sha256=?',(h,)).fetchone():
                    db.execute('INSERT INTO objects VALUES(?,?,?)',(h,size,zlib.compress(raw,9)))
                stats['supplement_files']+=1
            db.execute('INSERT INTO entries VALUES(?,?,?,?,?)',(rel,h,size,f.stat().st_mtime_ns,source))
            stats['removed_files']+=1;stats['removed_bytes']+=size
        assert snapshot(p)==snap,'Capture changed during archive: '+str(p)
        groups.append({'path':p.relative_to(R).as_posix(),'snapshot':snap,'retain':kept,'kind':'LOSSLESS_HISTORY'})
        db.commit()
        if i%50==0:print(json.dumps({'groups':i+1,'planned_files':stats['removed_files']}),flush=True)
    # Large frozen old report payloads remain losslessly recoverable. Keep all
    # current197-221 manifest-owned report assets directly accessible.
    for f in sorted((R/'qa/reports').glob('*')):
        if not f.is_file() or f.stat().st_size<2*1024*1024:continue
        rel=f.relative_to(R).as_posix()
        if rel in keep:continue
        safe(f);raw=f.read_bytes();h=hashlib.sha256(raw).hexdigest();size=len(raw)
        prev=prior.execute('SELECT sha256,bytes FROM entries WHERE path=?',(rel,)).fetchone()
        if prev==(h,size):source='214'
        else:
            source='222'
            if not db.execute('SELECT 1 FROM objects WHERE sha256=?',(h,)).fetchone():db.execute('INSERT INTO objects VALUES(?,?,?)',(h,size,zlib.compress(raw,9)))
        db.execute('INSERT INTO entries VALUES(?,?,?,?,?)',(rel,h,size,f.stat().st_mtime_ns,source))
        file_targets.append({'path':rel,'sha256':h,'bytes':size});stats['removed_files']+=1;stats['removed_bytes']+=size
    for p in [R/'qa/publication/render221/browser_profile',R/'qa/publication/render221_v2/browser_profile',
              R/'qa/publication/render221_final/browser_profile']:
        if p.exists():
            safe(p);snap=snapshot(p);groups.append({'path':p.relative_to(R).as_posix(),'snapshot':snap,'retain':[],'kind':'DISPOSABLE_ISOLATED_BROWSER_CACHE'})
            stats['cache_files']+=snap['files'];stats['cache_bytes']+=snap['bytes']
    checked=0
    for h,size,data in db.execute('SELECT sha256,raw_bytes,data FROM objects'):
        raw=zlib.decompress(data);assert len(raw)==size and hashlib.sha256(raw).hexdigest()==h;checked+=1
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert sha(old)==oldhash
    db.execute('INSERT INTO metadata VALUES(?,?)',('archive214_sha256',oldhash))
    db.execute("UPDATE metadata SET value='VERIFIED' WHERE key='state'");db.commit();db.close();prior.close()
    plan={'work':222,'root':str(R),'status':'VERIFIED_NOT_DELETED','archive214':old.relative_to(R).as_posix(),
      'archive214_sha256':oldhash,'archive222':archive.relative_to(R).as_posix(),'archive222_sha256':sha(archive),
      'new_unique_objects_verified':checked,'archive222_bytes':archive.stat().st_size,
      'staging':staging.relative_to(R).as_posix(),'groups':groups,'files':file_targets,'stats':dict(stats),
      'excluded_blocked_folder':blocked.relative_to(R).as_posix()}
    dump(work/'deletion_plan.json',plan)
    dump(R/'qa/reports/cleanup222_predelete.json',{k:v for k,v in plan.items() if k not in ('groups','files')})
    print(json.dumps({'status':plan['status'],'groups':len(groups),'large_reports':len(file_targets),'stats':dict(stats),'new_archive_bytes':archive.stat().st_size},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
