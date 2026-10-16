"""Carry meaningful ordinary/opening regression gates onto final060."""
from pathlib import Path

folder = Path(__file__).resolve().parent
s = (folder / 'verify_ordinary11_204.py').read_text('utf-8')
for before, after in [
    ('ordinary11_candidate_059', 'text11_candidate_060'),
    ('TinyToon2_Ordinary11_Candidate059', 'TinyToon2_Text11_Candidate060'),
    ('ordinary11_204_rebuild059', 'text11_209_rebuild060'),
    ('ordinary11_204_CPU.json', 'text11_209_ordinary_CPU.json'),
    ('PASS_FINAL059_33_ORDINARY_AND_NINE_OPENING_CPU', 'PASS_FINAL060_33_ORDINARY_AND_NINE_OPENING_CPU'),
    ("'work': 204", "'work': 209"),
    ('runtime059', 'runtime060'),
    ('Credits3 still8px, bitmap/HUD/signs unchanged; total registered inventory is not global closure',
     'Credits11px separately verified in credits11_209_CPU; bitmap/HUD/signs unchanged; registered inventory is not global closure')]:
    assert before in s
    s = s.replace(before, after)
p = folder / 'verify_text11_ordinary209.py'
assert not p.exists()
p.write_text(s, 'utf-8')
