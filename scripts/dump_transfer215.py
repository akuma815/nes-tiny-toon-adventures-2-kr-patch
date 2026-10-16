"""Decode named native NMI/VRAM consumer ranges, scoped to final062."""
from asm6502 import MPU, Disassembler
from verify_ui_native_latch_hooks import Memory
from seal_nonplay171 import R
m=Memory((R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes').read_bytes())
d=Disassembler(MPU(memory=m));rows=[]
for start,end in [(0xd060,0xd180),(0xf9e6,0xfa5b),(0xfd67,0xfdb0),(0xfe5f,0xfe83)]:
    rows.append('\nRANGE '+hex(start)+'..'+hex(end));pc=start
    while pc<end:
        size,text=d.instruction_at(pc);rows.append(f'{pc:04X} {text}');pc+=size
p=R/'work/nmi215/native_transfer_and_prerequisites.txt';assert not p.exists()
p.write_text('\n'.join(rows)+'\n','utf-8');print('\n'.join(rows))
