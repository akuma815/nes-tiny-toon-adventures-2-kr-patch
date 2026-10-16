"""Read-only disassembly of059 native credits and printer, no emulator."""
from asm6502 import MPU, Disassembler
from verify_ui_native_latch_hooks import Memory
from seal_nonplay171 import R

m = Memory((R / 'build/ordinary11_candidate_059/TinyToon2_Ordinary11_Candidate059.nes').read_bytes())
m.banks[:2] = [18, 19]
d = Disassembler(MPU(memory=m))
for lo, hi in ((0xa42a, 0xa486), (0xa4ad, 0xa4d7), (0x925e, 0x92b6), (0x93b5, 0x9417),
               (0xf988, 0xf99c), (0xfe0a, 0xfe16), (0xcbf0, 0xcc22),
               (0xcf9e, 0xcfc2), (0xff31, 0xff4f), (0x80b6, 0x80c1)):
    pc = lo
    while pc < hi:
        n, s = d.instruction_at(pc)
        print(f'{pc:04X} {s}')
        pc += n
