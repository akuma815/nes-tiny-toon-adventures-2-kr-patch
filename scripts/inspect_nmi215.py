"""Fixed-bank disassembly for the final062 NMI investigation, no emulator."""
from asm6502 import MPU, Disassembler
from verify_ui_native_latch_hooks import Memory
from seal_nonplay171 import R

rom=(R/'build/text11_candidate_062/TinyToon2_Text11_Candidate062.nes').read_bytes()
m=Memory(rom); c=MPU(memory=m);d=Disassembler(c)
vectors={n:m[a]+256*m[a+1] for n,a in [('NMI',0xfffa),('RESET',0xfffc),('IRQ',0xfffe)]}
out=R/'work/nmi215';out.mkdir(exist_ok=False)
rows=[];pc=0xf800
while pc<0xfffa:
    size,ins=d.instruction_at(pc)
    rows.append(f'{pc:04X} '+ ' '.join(f'{m[x]:02X}' for x in range(pc,pc+size))+f'  {ins}')
    pc+=size
(out/'fixed_F800_FFFF.txt').write_text('\n'.join(rows)+'\n','utf-8')
print('vectors:',{n:hex(v) for n,v in vectors.items()})
pc=vectors['NMI']
for _ in range(100):
    size,ins=d.instruction_at(pc);print(f'{pc:04X} {ins}');pc+=size
