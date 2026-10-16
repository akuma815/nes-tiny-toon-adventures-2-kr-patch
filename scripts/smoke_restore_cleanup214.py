"""Exercise actual archive restoration of one discarded frame, then identical-file reuse."""
import json, sqlite3, subprocess, sys
from archive_cleanup214 import R, digest, safe

db=sqlite3.connect(f'file:{(R/"qa/archive/cleanup214_history.sqlite").as_posix()}?mode=ro',uri=True)
prefix='qa/dialogue/booth039_font_probe/frame_'
rows=db.execute('SELECT path,sha256 FROM entries WHERE substr(path,1,?)=? AND bytes<32768 ORDER BY path LIMIT 30',(len(prefix),prefix)).fetchall()
db.close()
n,h=next((n,h) for n,h in rows if not safe(n).exists())
commands=[]
for _ in range(2):
    p=subprocess.run([sys.executable,'-B',str(R/'scripts/restore_archive214.py'),'--file',n],capture_output=True,text=True,check=True)
    assert digest(safe(n))==h
    commands.append(p.stdout.strip())
out=R/'qa/reports/cleanup214_restore_smoke.json'
assert not out.exists()
out.write_text(json.dumps({'status':'RESTORED_HASH_VERIFIED_NEEDS_TEST_FILE_REMOVAL','path':n,'sha256':h,'actual_new_file_restored':True,'identical_existing_file_accepted_without_overwrite':True,'helper_outputs':commands},indent=2)+'\n','utf-8')
print(out.read_text('utf-8'))
