"""Conservative classification: lossless historical capture storage plus proven disposable copies."""
from collections import Counter
import json
from pathlib import Path
from seal_nonplay171 import R

inventory = json.loads((R / 'work/cleanup214/inventory.json').read_text('utf-8'))['files']
stats = Counter()
counts = Counter()
for f in inventory:
    parts = f['path'].split('/')
    if len(parts) > 3 and parts[:2] == ['qa', 'dialogue']:
        folder = '/'.join(parts[:3])
        stats[folder] += f['bytes']
        counts[folder] += 1
print(json.dumps({'capture_folders': len(stats), 'largest': [
    {'path': p, 'bytes': size, 'files': counts[p]} for p, size in stats.most_common(24)],
    'cards033_dirs': [p for p in stats if 'cards033' in p],
    'opening055_dirs': [p for p in stats if '055' in p]}, ensure_ascii=False, indent=2))
