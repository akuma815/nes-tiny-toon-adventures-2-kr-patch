"""Read-only inventory for project-local cleanup; do not follow reparse points."""
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
for base, folders, names in os.walk(R, followlinks=False):
    for n in list(folders):
        p = Path(base) / n
        if p.is_symlink() or getattr(p.lstat(), 'st_file_attributes', 0) & 0x400:
            reparse.append(p.relative_to(R).as_posix())
            folders.remove(n)
    for n in names:
        p = Path(base) / n
        if p.is_symlink() or getattr(p.lstat(), 'st_file_attributes', 0) & 0x400:
            reparse.append(p.relative_to(R).as_posix())
            continue
        rel = p.relative_to(R)
        size = p.stat().st_size
        for depth in (1, 2):
            folder = '/'.join(rel.parts[:depth])
            sizes[folder] += size
            counts[folder] += 1
        extensions[p.suffix.lower()] += size
        files.append((size, rel.as_posix()))
print(json.dumps({'total_files': len(files), 'total_bytes': sum(size for size, _ in files),
    'largest_directories': [{'path': p, 'files': counts[p], 'bytes': size} for p, size in sizes.most_common(46)],
    'largest_files': [{'path': p, 'bytes': size} for size, p in sorted(files, reverse=True)[:18]],
    'extension_bytes': extensions.most_common(14), 'reparse_points_excluded': reparse}, ensure_ascii=False, indent=2))
