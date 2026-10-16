"""Prepare corrected helper packaging at an unused destination."""
from pathlib import Path

base = Path(__file__).resolve().parent
s = (base / 'package_ordinary11_205.py').read_text('utf-8')
s = s.replace('205', '206').replace(
    'TinyToonAdventures2_KR_Ordinary11_Candidate059_20261009',
    'TinyToonAdventures2_KR_Ordinary11_Candidate059_Apply206_20261009')
s = s.replace("('오프닝11px PoC055', '일반대사11px 후보059')",
              "('오프닝11px PoC055', '일반대사11px 후보059'), ('-ne 499728', '-ne 524304')")
out = base / 'package_ordinary11_206.py'
assert not out.exists() and "'-ne 524304'" in s
out.write_text(s, 'utf-8')
