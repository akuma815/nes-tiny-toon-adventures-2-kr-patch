"""Prepare062 with mapper restoration exclusively in mirrored code."""
from pathlib import Path
base = Path(__file__).resolve().parent
s = (base / 'build_credits11_210.py').read_text('utf-8').replace('061', '062').replace("'work': 210", "'work': 211")
definition = '''
PRIVATE_GUARD = GUARD.replace('$PRINTER', '$B300').replace('$FALLBACK', '$9650')
PRIVATE_GUARD = PRIVATE_GUARD.replace('    LDA #$08\\n    JSR $FDD3\\n', '')
PRIVATE_GUARD = PRIVATE_GUARD.replace('    PHP\\n    PHA\\n    JSR $FDDB\\n    PLA\\n    PLP\\n    RTS', '    RTS')
PRIVATE_GUARD = PRIVATE_GUARD.replace('restore:\\n    JSR $FDDB', 'restore:')
FALLBACK = """
 PHP
 PHA
 JSR $FDDB
 PLA
 PLP
 JMP $96F0
"""
'''
s = s.replace('WRAPPER =', definition + '\nWRAPPER =', 1)
old = "GUARD.replace('$PRINTER', '$B300').replace('$FALLBACK', '$96F0').replace('    LDA #$08\\n    JSR $FDD3\\n', '')"
assert old in s
s = s.replace(old, 'PRIVATE_GUARD')
s = s.replace("('wrapper_mirror', 8, 0x9630, 0x9690, WRAPPER),", "('wrapper_mirror', 8, 0x9630, 0x9650, WRAPPER),\n        ('fallback', 18, 0x9650, 0x9690, FALLBACK),\n        ('fallback_mirror', 8, 0x9650, 0x9690, FALLBACK),")
s = s.replace('empty:\n SEC\n RTS', 'empty:\n LDA #$00\n STA $58\ncontinue:\n SEC\n RTS')
s = s.replace(' BCC @empty\n LDA #$00\n STA $06C3', ' BCC @continue\n LDA #$00\n STA $06C3')
for before, after in [('build_credits11_210.py', 'build_credits11_211.py')]:
    p = base / after
    assert not p.exists()
    p.write_text(s, 'utf-8')
for old, new in [('verify_text11_ordinary210.py', 'verify_text11_ordinary211.py'),
                 ('verify_credits11_210.py', 'verify_credits11_211.py')]:
    p = base / new
    assert not p.exists()
    p.write_text((base / old).read_text('utf-8').replace('061', '062').replace('210', '211'), 'utf-8')
