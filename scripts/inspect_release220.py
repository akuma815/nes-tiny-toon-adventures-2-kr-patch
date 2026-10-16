"""Read-only release inputs, evidence inventory, and cleanup size summary."""
from pathlib import Path
import json,csv,sqlite3
from seal_nonplay171 import R

out={'roots':{},'graphics':{},'missing_rebuild_inputs':[]}
for root in ('build','dist','work','qa','workspace','tools','backups','extracted'):
    groups={};total=count=0
    for p in (R/root).rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(R/root);group=rel.parts[0] if len(rel.parts)>1 else '(root files)'
        n=p.stat().st_size;total+=n;count+=1
        g=groups.setdefault(group,{'files':0,'bytes':0});g['files']+=1;g['bytes']+=n
    out['roots'][root]={'files':count,'bytes':total,'largest':sorted(groups.items(),key=lambda x:x[1]['bytes'],reverse=True)[:8]}
for root in ('workspace/graphics/title','workspace/graphics/moving_stop182','workspace/review/opening11_194'):
    out['graphics'][root]=[p.relative_to(R).as_posix() for p in (R/root).rglob('*') if p.is_file() and p.suffix.lower() in ('.png','.json','.txt')][:24]
needed=['build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes',
        'workspace/review/credits11_202/credits11_latin16_font.chr']
for p in needed:
    if not (R/p).exists():out['missing_rebuild_inputs'].append(p)
rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')))
out['translation']={'rows':len(rows),'columns':list(rows[0]),'statuses':{}}
for z in rows:
    for k in ('status','review_status','translation_status'):
        if k in z:
            key=f'{k}:{z[k]}';out['translation']['statuses'][key]=out['translation']['statuses'].get(key,0)+1
db=sqlite3.connect(f'file:{(R/"qa/archive/cleanup214_history.sqlite").as_posix()}?mode=ro',uri=True)
out['archived_title_paths']=[x[0] for x in db.execute("SELECT path FROM entries WHERE path LIKE 'workspace/graphics/title/%' AND path LIKE '%.png' LIMIT 16")]
out['archived_stop_paths']=[x[0] for x in db.execute("SELECT path FROM entries WHERE path LIKE 'workspace/graphics/moving_stop182/%' AND path LIKE '%.png' LIMIT 10")]
print(json.dumps(out,ensure_ascii=False,indent=2))
