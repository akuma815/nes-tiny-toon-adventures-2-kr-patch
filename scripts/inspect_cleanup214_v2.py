"""One directory-entry stat per file; preserve the exact inventory for cleanup planning."""
from collections import Counter
from pathlib import Path
import json
import os
from seal_nonplay171 import R

sizes = Counter()
counts = Counter()
extensions = Counter()
files = []
reparse = []
pending = [str(R)]
while pending:
    base = pending.pop()
    with os.scandir(base) as entries:
        for entry in entries:
            st = entry.stat(follow_symlinks=False)
            rel = os.path.relpath(entry.path, R).replace('\\', '/')
            if getattr(st, 'st_file_attributes', 0) & 0x400 or entry.is_symlink():
                reparse.append(rel)
                continue
            if entry.is_dir(follow_symlinks=False):
                pending.append(entry.path)
                continue
            size = st.st_size
            parts = rel.split('/')
            for depth in (1, 2):
                group = '/'.join(parts[:depth])
                sizes[group] += size
                counts[group] += 1
            extensions[os.path.splitext(entry.name)[1].lower()] += size
            files.append({'path': rel, 'bytes': size})
folder = R / 'work/cleanup214'
folder.mkdir(exist_ok=False)
(folder / 'inventory.json').write_text(json.dumps({'files': files, 'reparse_points_excluded': reparse}, ensure_ascii=False, indent=2) + '\n', 'utf-8')
print(json.dumps({'total_files': len(files), 'total_bytes': sum(p['bytes'] for p in files),
    'largest_directories': [{'path': p, 'files': counts[p], 'bytes': size} for p, size in sizes.most_common(38)],
    'largest_files': sorted(files, key=lambda z: z['bytes'], reverse=True)[:12],
    'extension_bytes': extensions.most_common(12), 'reparse_points_excluded': reparse}, ensure_ascii=False, indent=2))
