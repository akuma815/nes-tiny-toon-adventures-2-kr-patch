"""Scoped IRQ-at-instruction-boundary CPU audit. No PPU or gameplay execution."""
from pathlib import Path
import json
from asm6502 import MPU
from verify_ui_native_latch_hooks import Memory
from verify_text11_ordinary211 import initial
from seal_nonplay171 import R, sha

CALLBACKS = [(0, 0, 0xfd0b), (1, 0, 0xfb3a), (1, 1, 0xfb97),
             (4, 0, 0xfad9), (4, 1, 0xfbe3)]
IRQ_RAM = {0x41, 0x45, 0x46, 0x47, 0xc7}
REGS = ('pc', 'a', 'x', 'y', 'sp', 'p')

class Bus(Memory):
    def __init__(self, rom):
        super().__init__(rom)
        self.irq_scratch_reads = set()
    def __getitem__(self, a):
        if a in IRQ_RAM:
            self.irq_scratch_reads.add(a)
        return super().__getitem__(a)

def create(rom, seed, pc):
    m = Bus(rom)
    m.ram[:] = seed
    c = MPU(memory=m);m.cpu=c;c.pc=pc;c.sp=0xfd;c.p=0x30
    m.ram[0x1fe:0x200] = bytes.fromhex('ff c0')
    return m,c

def snapshot(m,c):
    return bytes(m.ram),list(m.banks),[getattr(c,k) for k in REGS]

def load(rom,s):
    m=Bus(rom);m.ram[:]=s[0];m.banks[:]=s[1]
    c=MPU(memory=m);m.cpu=c
    for k,v in zip(REGS,s[2]):setattr(c,k,v)
    return m,c

def inject(rom,s,mode,phase,callback):
    m,c=load(rom,s);r=m.ram
    r[0x40]=mode;r[0x41]=phase
    # F9E6 selects the native callback table. Explicit phase injection tests
    # callback behavior, not mapper-specific scheduling or phase reachability.
    table=m[0xfa70+2*mode]+256*m[0xfa71+2*mode]
    r[0x43:0x45]=table.to_bytes(2,'little')
    r[0x609:0x612]=bytes([82,82,0,168,0,0,0,0,0])
    selected=m[table+2*phase]+256*m[table+2*phase+1]
    assert selected==callback,(mode,phase,hex(selected))
    before=bytes(r);banks=list(m.banks);registers=[getattr(c,k) for k in REGS]
    assert not c.p&4
    c.irq();assert c.pc==0xfa5b
    low=c.sp;steps=0;seen=False
    while True:
        pc=c.pc;seen|=pc==callback;c.step();low=min(low,c.sp);steps+=1
        assert steps<2000,(hex(c.pc),mode,phase)
        if pc==0xfd18:break
    assert seen and [getattr(c,k) for k in REGS]==registers,('IRQ ABI',mode,phase,registers,[getattr(c,k) for k in REGS])
    assert m.banks==banks,('PRG',mode,phase,banks,m.banks)
    # Only native IRQ scratch and the actually used lower stack slots may differ.
    stack=set(range(0x100+low+1,0x100+registers[4]+1))
    differences=[i for i in range(2048) if r[i]!=before[i] and i not in IRQ_RAM|stack]
    assert not differences,('RAM or font latch',mode,phase,hex(registers[0]),[hex(i) for i in differences])
    assert r[0x100:0x1c0]==before[0x100:0x1c0],('queue overlap',hex(registers[0]),low)
    return m,c,{'cycles':c.processorCycles,'lowest_SP':low,'stack_gap_after_192_byte_queue':low+1-192,
                'writes':[(a,v,t) for a,v,t in m.writes]}

def main():
    folder=R/'build/text11_candidate_062';target=folder/'TinyToon2_Text11_Candidate062.nes'
    rom=target.read_bytes();prior=(R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes').read_bytes()
    # Native interrupt implementation remains byte-identical, including latch hook.
    fixed=lambda b:b[0x10+(b[4]*2-1)*8192:]
    assert fixed(rom)[0x1a5b:0x1d19]==fixed(prior)[0x1a5b:0x1d19]
    plan=json.loads((folder/'ordinary11_plan.json').read_text('utf-8'))
    cases=[];total=masked=0;minimum=255;callback_cycles={};restored=0
    for z in plan['pages']:
        for entry in (0x925e,0x93e1):
            seed=initial(rom,z,999,5).ram
            seed[0x6f3]=seed[0xc6]
            m,c=create(rom,seed,entry);trace=[];first={};last={};step=0
            while c.pc!=0xc100:
                first.setdefault(c.pc,step);last[c.pc]=step
                trace.append(snapshot(m,c));c.step();step+=1
                assert step<10000
            assert not m.irq_scratch_reads,('producer reads IRQ scratch',z['entry_id'],m.irq_scratch_reads)
            assert c.sp==255 and m.banks==[0x32,0x33,0x3e,31]
            finish=(bytes(m.ram),[getattr(c,k) for k in REGS],list(m.banks))
            points=sorted(set(first.values())|set(last.values()))
            tested=0;covered=set();chosen=None
            for index in points:
                s=trace[index]
                if s[2][-1]&4:masked+=1;continue
                covered.add(tuple(s[1][:2]))
                for mode,phase,callback in CALLBACKS:
                    q,d,result=inject(rom,s,mode,phase,callback)
                    total+=1;tested+=1;minimum=min(minimum,result['lowest_SP'])
                    callback_cycles.setdefault(f'{mode}:{phase}',set()).add(result['cycles'])
                    # One mid-bank continuation per producer validates final output.
                    if chosen is None and s[1][:2]!=[0x32,0x33] and mode==4 and phase==0:
                        chosen=(q,d,index)
            assert chosen is not None
            q,d,index=chosen;extra_reads=set(q.irq_scratch_reads);q.irq_scratch_reads.clear()
            n=0
            while d.pc!=0xc100:
                d.step();n+=1;assert n<10000
            assert not q.irq_scratch_reads
            assert [getattr(d,k) for k in REGS]==finish[1] and q.banks==finish[2]
            excluded=IRQ_RAM|set(range(0x1c0,0x200))|{0x40,0x43,0x44}|set(range(0x609,0x612))
            assert all(q.ram[i]==finish[0][i] for i in range(2048) if i not in excluded)
            restored+=1
            # Representative old/native comparison uses identical interrupted state.
            s=trace[index]
            for mode,phase,callback in CALLBACKS:
                _,_,a=inject(rom,s,mode,phase,callback)
                _,_,b=inject(prior,s,mode,phase,callback)
                assert a==b
            cases.append({'entry_id':z['entry_id'],'producer':f'{entry:04X}',
                          'baseline_instructions':step,'selected_first_last_PC_boundaries':len(points),
                          'IRQ_tests':tested,'PRG_states_covered':[list(x) for x in sorted(covered)],
                          'mid_bank_continuation_index':index,'final_output_equal':True})
    out=R/'qa/reports/irq217_injection.json';assert not out.exists()
    report={'work':217,'status':'PASS_SCOPED_INSTRUCTION_BOUNDARY_IRQ_ABI',
            'ROM_sha256':sha(target),'baseline051_sha256':sha(R/'build/dialogue_kr_poc_051/TinyToon2_dialogue_kr_poc.nes'),
            'scope':'33 ordinary registered pages, instant925E and first typed93E1, ticket999/ride5; first+last occurrence of each PC; five native callback phases',
            'IRQ_vector':0xfa5b,'callbacks':CALLBACKS,'cases':cases,'producer_states':len(cases),
            'IRQ_injections':total,'masked_boundaries_not_injected':masked,'minimum_SP':minimum,
            'minimum_gap_after_192_byte_queue':minimum+1-192,'full_producer_continuations':restored,
            'native_IRQ_051_062_code_equal':True,'representative_old_callback_cycle_write_results_equal':True,
            'callback_cycles':{k:sorted(v) for k,v in callback_cycles.items()},
            'limitations':['No mapper IRQ clock or chip-specific phase reachability model.',
                           'No NMI interleaving, DMC cycle stealing, PPU, hardware or emulator execution.',
                           'First/last PC boundary selection is not every loop iteration or every text cursor.',
                           'Opening and credits interrupt paths are outside this audit.',
                           'CHR writes are native callback behavior; actual visible CHR256 mapping remains user review.']}
    out.write_text(json.dumps(report,indent=2)+'\n','utf-8')
    print(json.dumps({k:report[k] for k in ('status','producer_states','IRQ_injections','minimum_SP','full_producer_continuations')}))

if __name__=='__main__':main()
