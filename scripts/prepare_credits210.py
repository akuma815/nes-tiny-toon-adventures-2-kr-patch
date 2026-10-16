"""Prepare061 at fresh paths after preserving rejected060."""
from pathlib import Path
base = Path(__file__).resolve().parent
s = (base / 'build_credits11_209_v2.py').read_text('utf-8')
s = s.replace('060', '061').replace("'work': 209", "'work': 210")
s = s.replace("GUARD.replace('$PRINTER', '$B300').replace('$FALLBACK', '$96F0')",
              "GUARD.replace('$PRINTER', '$B300').replace('$FALLBACK', '$96F0').replace('    LDA #$08\\n    JSR $FDD3\\n', '')")
p = base / 'build_credits11_210.py'
assert not p.exists()
p.write_text(s, 'utf-8')
s = (base / 'verify_text11_ordinary209.py').read_text('utf-8').replace('060', '061').replace('209', '210')
p = base / 'verify_text11_ordinary210.py'
assert not p.exists()
p.write_text(s, 'utf-8')
s = (base / 'verify_credits11_209.py').read_text('utf-8').replace('060', '061').replace('209', '210')
s = s.replace('init.mask == 0x1e', 'init.mask == 0x06')
s = s.replace("assert init.trace[-2:] == [(0x2000, 0x90), (0x2001, 0x1e)], init.trace", "assert init.trace[-1] == (0x2000, 0x90) and init.ram[0xfe] == 0x1e, init.trace")
s = s.replace('initial_screen_NMI_off_and_register_restore_CPU', 'initial_screen_NMI_off_2000_restore_2001_native_NMI_pending_CPU')
p = base / 'verify_credits11_210.py'
assert not p.exists()
p.write_text(s, 'utf-8')
