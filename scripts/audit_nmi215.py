"""Final062 native NMI prefix with actual text packets; CPU only, no play/PPU emulation."""
import json
from asm6502 import MPU
from verify_ui_native_latch_hooks import Memory
from verify_text11_ordinary211 import initial as ordinary
from verify_credits11_211 import initial as credits, execute
from verify_home11_cpu191 import run
from verify_homebooth11_199 import queue
from seal_nonplay171 import R, sha

class NmiBus(Memory):
    def __init__(self,rom,dma):
        super().__init__(rom);self.dma=dma;self.address=0;self.high=True;self.nt={};self.trace=[]
    def __getitem__(self,at):
        if at==0x2002:self.high=True;return 0x80
        return super().__getitem__(at)
    def __setitem__(self,at,v):
        if at==0x2006:
            self.address=((v&63)<<8) if self.high else self.address|v;self.high=not self.high
        elif at==0x2007:
            self.nt[self.address]=v;self.address+=32 if self.ram[0x2000]&4 else 1
        if at in (0x2000,0x2001,0x2007,0x4014):
            self.trace.append({'at':at,'value':v,'instruction_start_cycle':self.cpu.processorCycles})
        if at==0x4014:self.cpu.processorCycles+=self.dma
        super().__setitem__(at,v)

def prefix(rom,packet,blank_hold=0,irq_seed=0,dma=514):
    m=NmiBus(rom,dma);r=m.ram
    r[0x100:0x100+len(packet)]=packet;r[0x1e]=len(packet)-1
    r[0xfe]=0x1e;r[0xff]=0x90;r[0x1d]=blank_hold;r[0x40]=irq_seed
    r[0x600:0x609]=bytes((1,2,3,4,5,6,7,8,9))
    c=MPU(memory=m);m.cpu=c;c.pc=0xc100;c.sp=0xfd;c.nmi()
    steps=0
    while c.pc!=0xfecd:
        c.step();steps+=1;assert steps<20000,hex(c.pc)
    assert r[0x1e]==0 and r[0x100]==0 and r[0x1c]==1
    expect=bytearray(65536);expect[0x100:0x100+len(packet)]=packet;expect[0x1e]=len(packet)-1
    assert m.nt==queue(expect)
    return {'through_render_mask_restore_cycles':c.processorCycles,'last_VRAM_write_instruction_start_cycle':max((t['instruction_start_cycle'] for t in m.trace if t['at']==0x2007),default=None),
            'tiles':len(m.nt),'mask_restored':r[0x2001],'DMA_stall_added':dma,
            'over_2273_lower_bound':c.processorCycles>2273,'queue_and_native_stack_restore':True}

def measure(rom,packet):
    combinations=[prefix(rom,packet,hold,irq,dma) for hold in (0,2) for irq in (0,1) for dma in (513,514)]
    visible=[x for x in combinations if x['mask_restored']&24]
    return {'queue_bytes':len(packet)-1,'max_tiles':max(x['tiles'] for x in combinations),
            'minimum_cycles':min(x['through_render_mask_restore_cycles'] for x in combinations),
            'maximum_cycles':max(x['through_render_mask_restore_cycles'] for x in combinations),
            'visible_restore_minimum_cycles':min(x['through_render_mask_restore_cycles'] for x in visible),
            'visible_restore_maximum_cycles':max(x['through_render_mask_restore_cycles'] for x in visible),
            'cases':combinations}

def main():
    root=R/'build/text11_candidate_062';p=root/'TinyToon2_Text11_Candidate062.nes';rom=p.read_bytes()
    source=(R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes').read_bytes()
    a=Memory(source);b=Memory(rom)
    identical=[]
    for lo,hi in [(0xd068,0xd16c),(0xf9e6,0xfa5b),(0xfe83,0xfed0)]:
        assert bytes(a[i] for i in range(lo,hi))==bytes(b[i] for i in range(lo,hi))
        identical.append([lo,hi])
    plan=json.loads((root/'ordinary11_plan.json').read_text('utf-8'))
    rows=[]
    for z in plan['pages']:
        for number,ride in [(0,0),(999,0),*[(0,i) for i in range(1,6)]]:
            m=ordinary(rom,z,number,ride);run(m,0x96fc)
            n=m.ram[0x1e];packet=bytes(m.ram[0x100:0x101+n])
            rows.append({'entry_id':z['entry_id'],'page':z['page'],'number':number,'ride':ride,'mode':'ordinary_instant',**measure(rom,packet)})
    typed=bytes((1,0x22,0xa8,1,255,1,0x22,0xc8,2,255,0))
    typical=measure(rom,typed)
    cp=json.loads((root/'credits11_plan.json').read_text('utf-8'))
    cr=[]
    for z in cp['pages'][1:]:
        m=credits(rom,z);maximum=None;calls=0
        while True:
            m.ram[0x1e]=0;m.ram[0x100:0x1c0]=bytes(0xc0)
            c=execute(m,0x93e1);n=m.ram[0x1e]
            packet=bytes(m.ram[0x100:0x101+n])
            result=measure(rom,packet);calls+=1
            if maximum is None or result['maximum_cycles']>maximum['maximum_cycles']:maximum=result
            if not c.p&1:break
        cr.append({'entry_id':z['entry_id'],'calls':calls,**maximum})
    out=R/'qa/reports/nmi215_transfer_budget.json';assert not out.exists()
    over=[z for z in rows if z['visible_restore_minimum_cycles']>2273]
    report={'work':215,'ROM_sha256':sha(p),'status':'CPU_PREFIX_MEASURED_HARDWARE_NOT_RUN',
            'hardware_reference':{'vblank_cycles_approx':2273,'source':'https://www.nesdev.org/wiki/The_frame_and_NMIs','OAM_DMA_cycles':[513,514],'DMA_source':'https://www.nesdev.org/wiki/PPU_registers'},
            'unchanged_native_consumer_ranges':identical,'ordinary_instant':rows,'paired_typed_packet':typical,'credits_progressive_maxima':cr,
            'ordinary_instant_cases':len(rows),'instant_over_lower_bound_cases':len(over),'over_lower_bound_entries':sorted(set(z['entry_id'] for z in over)),
            'NMI_prefix_case_count':8*(len(rows)+1+sum(z['calls'] for z in cr)),
            'limits':['Seeded RAM; no actual PPU/frame/IRQ/DMC timing or input route observation',
                      'NMI prefix only throughFECD; remaining native game/audio tail not measured',
                      '513/514DMA included, asynchronous IRQ/DMC/instruction-boundary latency excluded',
                      '1D blank_hold2 intentionally leaves rendering disabled; visible-mask restore uses blank_hold0',
                      'Full instant producer starts at cursor0; partial skip queues and concurrent producers require follow-up',
                      'No ROM change, emulator/controller run or release adoption']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
    worst=max(rows,key=lambda z:z['maximum_cycles'])
    print(json.dumps({'status':report['status'],'instant_cases':len(rows),'over_entries':report['over_lower_bound_entries'],
                      'worst':{k:v for k,v in worst.items() if k!='cases'},'typed':{k:v for k,v in typical.items() if k!='cases'},
                      'credits':[{k:v for k,v in z.items() if k!='cases'} for z in cr]},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
