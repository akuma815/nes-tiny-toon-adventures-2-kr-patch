"""Correct215 entry scope; actual925E full/partial packets and historical IRQ RAM contexts."""
from pathlib import Path
import hashlib,json,math
from asm6502 import MPU,Disassembler
from audit_nmi215 import NmiBus,measure
from verify_text11_ordinary211 import initial
from verify_home11_cpu191 import run
from verify_homebooth11_199 import queue
from seal_nonplay171 import R,sha

def emit(m,pc=0x925e):
    c=MPU(memory=m);c.pc=pc;c.sp=0xfd;c.p=0x34;m.ram[0x1fe:0x200]=bytes.fromhex('ff c0');visited=set();steps=0
    while c.pc!=0xc100:
        visited.add(c.pc);c.step();steps+=1;assert steps<10000,hex(c.pc)
    assert c.sp==255
    n=m.ram[0x1e];packet=bytes(m.ram[0x100:0x101+n])
    return c,packet,visited

def compact(result):
    return {k:v for k,v in result.items() if k!='cases'}

def contexts():
    captures=json.loads((R/'qa/dialogue/cards033_actual_pages.json').read_text('utf-8'))
    records=[];examples=[];scanned=matched=0
    for cap in captures:
        p=R/cap['source_image'];folder=p.parent;states={}
        for f in sorted(folder.glob('frame_*_ram.bin')):
            data=f.read_bytes();scanned+=1
            assert len(data)==2048
            if data[0x18]!=8 or data[0x6cf] not in range(0x1e,0x2a):continue
            matched+=1
            key=bytes([data[0x1d],data[0x40],data[0x88],data[0xfe],data[0xff]])+data[0x600:0x609]
            if key not in states:
                states[key]={'route':cap['route'],'path':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(data).hexdigest(),
                             'first_frame':int(f.stem.split('_')[1]),'samples':0,'1D':data[0x1d],'40':data[0x40],
                             '88':data[0x88],'FE':data[0xfe],'FF':data[0xff],'IRQ_config_600_608':list(data[0x600:0x609])}
                examples.append((states[key],data))
            states[key]['samples']+=1
        records.extend(states.values())
    return {'RAM_files_scanned':scanned,'matched_upper_text_RAM_files':matched,'unique_contexts':records},examples

def historical_prefix(rom,packet,data):
    m=NmiBus(rom,514);r=m.ram;r[:2048]=data
    # Captures can occur inside NMI. This CPU experiment specifically starts a new outer NMI.
    r[0x1c]=0;r[0x1e]=len(packet)-1;r[0x100:0x100+len(packet)]=packet
    c=MPU(memory=m);m.cpu=c;c.pc=0xc100;c.sp=0xfd;c.nmi();steps=0
    while c.pc!=0xfecd:c.step();steps+=1;assert steps<20000
    expected=bytearray(65536);expected[0x1e]=len(packet)-1;expected[0x100:0x100+len(packet)]=packet
    assert m.nt==queue(expected)
    controls=[(v,t+4) for a,v,t in m.writes if a==0xf000]
    assert len(controls)==1
    control,enabled_at=controls[0]
    reload_value=data[0x600]
    # Standard scanline prescaler schedule, not chip-level verification (VRC7 caveats retained).
    irq_at=enabled_at+math.ceil((256-reload_value)*341/3) if control&2 else None
    return {'cycles_to_mask_restore':c.processorCycles,'restored_mask':r[0x2001],
            'last_VRAM_store_completion_cycle':max((t['instruction_start_cycle']+4 for t in m.trace if t['at']==0x2007),default=None),
            'IRQ_control':control,'first_IRQ_earliest_standard_model_cycle':irq_at,
            'IRQ_before_prefix_end_in_standard_model':irq_at is not None and irq_at<=c.processorCycles,
            'queue_consumed_exact':True}

def main():
    p=R/'build/text11_candidate_062';target=p/'TinyToon2_Text11_Candidate062.nes';rom=target.read_bytes()
    assert (rom[6]>>4)|(rom[7]&240)==85
    plan=json.loads((p/'ordinary11_plan.json').read_text('utf-8'));rows=[];partial=[];packets={};paths=set()
    for z in plan['pages']:
        for number,ride in [(0,0),(999,0),*[(0,i) for i in range(1,6)]]:
            m=initial(rom,z,number,ride);c,packet,visited=emit(m);paths|=visited
            assert {0x925e,0x9690,0xb400}<=visited and 0x96fc not in visited,(z['entry_id'],sorted(visited))
            result=compact(measure(rom,packet))
            rows.append({'entry_id':z['entry_id'],'number':number,'ride':ride,'producer_cycles':c.processorCycles,**result})
            if number==ride==0:packets[z['entry_id']]=packet
        m=initial(rom,z);body=bytes.fromhex(z['body_hex']);cursor=0
        while True:
            q=initial(rom,z);q.ram[:]=m.ram;q.ram[0x1e]=0;q.ram[0x100:0x1c0]=bytes(0xc0)
            _,packet,_=emit(q)
            partial.append({'entry_id':z['entry_id'],'body_cursor':cursor,**compact(measure(rom,packet))})
            if body[cursor]==255:break
            m.ram[0x1e]=0;m.ram[0x100:0x140]=bytes(64);run(m,0x93e1)
            cursor+=2 if body[cursor]<128 or body[cursor]==253 else 1
    assert len(rows)==231 and len(partial)==1071
    scan,examples=contexts();historical=[]
    for desc,data in examples:
        for z in plan['pages']:
            if z['family'].startswith('ride_upper'):
                historical.append({'entry_id':z['entry_id'],'historical_context':desc['path'],**historical_prefix(rom,packets[z['entry_id']],data)})
    m=initial(rom,plan['pages'][0]);d=Disassembler(MPU(memory=m));caller=[];pc=0x925e
    while pc<0x9274:
        n,t=d.instruction_at(pc);caller.append(f'{pc:04X} {t}');pc+=n
    worst=max(rows+partial,key=lambda z:z['visible_restore_maximum_cycles'])
    over=[z for z in rows+partial if z['visible_restore_minimum_cycles']>2273]
    out=R/'qa/reports/nmi216_actual_entry_budget.json';assert not out.exists()
    result={'work':216,'status':'PASS_SCOPED_ACTUAL_ENTRY_PREFIX_215_DEFECT_CLAIM_WITHDRAWN','ROM_sha256':sha(target),
            'mapper':85,'actual_entry':0x925e,'actual_path':[0x925e,0x9690,0xb400],
            '215_correction':'215 called96FC directly, the native fallback, bypassing patched925E/9690. Its oversized packet is not evidence of actual registered11px entry failure. No063 built.',
            'caller_disassembly':caller,'all_target_traces_exclude_96FC':0x96fc not in paths,
            'full_instant_cases':rows,'partial_skip_cases':partial,'full_count':len(rows),'partial_count':len(partial),
            'actual_entry_over_2273_cases':len(over),'worst_actual_entry':worst,
            'nominal_margin_before2273':2273-worst['visible_restore_maximum_cycles'],
            'historical_RAM_scan':scan,'seeded_historical_irq_prefix_cases':historical,
            'standard_model_IRQ_before_prefix_end_cases':sum(x['IRQ_before_prefix_end_in_standard_model'] for x in historical),
            'references':['https://www.nesdev.org/wiki/The_frame_and_NMIs','https://www.nesdev.org/wiki/PPU_registers',
                          'https://www.nesdev.org/wiki/INES_Mapper_085','https://www.nesdev.org/wiki/VRC_IRQ'],
            'limits':['Existing historical033 RAM contexts are not actual062 execution or reachability proof',
                      'Instruction-based CPU model, fixed514 DMA bound, no asynchronous IRQ/DMC/PPU emulation',
                      'Approx2273 is nominal NTSC vblank; instruction-boundary latency and DMC steals unmodeled; positive margin not hardware safety guarantee',
                      'IRQ deadline uses standard VRC scanline schedule; VRC7 silicon distinctions unverified',
                      'NMI tail and global text-source closure pending; no gameplay/controller or emulator run',
                      'No change to ROM/CSV/fonts/packages, no release adoption']}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({k:result[k] for k in ['status','full_count','partial_count','actual_entry_over_2273_cases','worst_actual_entry','nominal_margin_before2273','standard_model_IRQ_before_prefix_end_cases']},ensure_ascii=False,indent=2))
    print('Historical RAM scan:',scan['RAM_files_scanned'],'matched:',scan['matched_upper_text_RAM_files'],'contexts:',len(examples),'seeded CPU cases:',len(historical))

if __name__=='__main__':main()
