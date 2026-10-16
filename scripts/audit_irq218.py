"""Opening and credits cursor coverage; scoped CPU IRQ ABI, no gameplay."""
import json
from asm6502 import MPU
from audit_irq217 import Bus, REGS, IRQ_RAM, CALLBACKS, create, snapshot, inject
from verify_text11_ordinary211 import initial
from verify_credits11_211 import initial as credits_initial, expected
from verify_homebooth11_199 import queue
from seal_nonplay171 import R,sha

def check_trace(rom,trace,callbacks):
    first={};last={}
    for i,s in enumerate(trace):
        first.setdefault(s[2][0],i);last[s[2][0]]=i
    count=masked=0;low=255;states=set()
    for i in sorted(set(first.values())|set(last.values())):
        s=trace[i]
        if s[2][-1]&4:masked+=1;continue
        states.add(tuple(s[1][:2]))
        for mode,phase,cb in callbacks:
            _,_,q=inject(rom,s,mode,phase,cb);count+=1;low=min(low,q['lowest_SP'])
    return {'injections':count,'masked_boundaries':masked,'minimum_SP':low,
            'PRG_states':[list(z) for z in sorted(states)]}

def main():
    folder=R/'build/text11_candidate_062';target=folder/'TinyToon2_Text11_Candidate062.nes';rom=target.read_bytes()
    opening=json.loads((folder/'opening11_plan.json').read_text('utf-8'))['pages']
    credits=json.loads((folder/'credits11_plan.json').read_text('utf-8'))['pages']
    pages=[];total=0;lowest=255;call_count=0
    for family,entries in [('opening',opening),('credits_typed',credits[1:])]:
        for z in entries:
            seed=initial(rom,z).ram if family=='opening' else credits_initial(rom,z).ram
            seed[0x18]=7;seed[0x6f3]=seed[0xc6]
            m=Bus(rom);m.ram[:]=seed;cursor=0;body=bytes.fromhex(z['body_hex']) if family=='opening' else None
            calls=0;writes={};page_count=0;page_low=255;all_states=set();details=[]
            while True:
                m.ram[0x1e]=0;m.ram[0x100:0x1c0]=bytes(192)
                q,c=create(rom,m.ram,0x95f9 if family=='opening' else 0x93e1)
                trace=[];steps=0
                while c.pc!=0xc100:
                    trace.append(snapshot(q,c));c.step();steps+=1;assert steps<10000
                assert not q.irq_scratch_reads
                assert c.sp==255 and q.banks[:2]==[50,51]
                # Native terminal-ack IRQ at all cursors; all five dispatch phases
                # at first, line breaks, and paragraph completion only.
                callbacks=CALLBACKS if calls==0 or q.ram[0x1e]==0 else CALLBACKS[:1]
                result=check_trace(rom,trace,callbacks)
                page_count+=result['injections'];page_low=min(page_low,result['minimum_SP'])
                all_states.update(tuple(x) for x in result['PRG_states'])
                details.append({'call':calls+1,'cursor_before':m.ram[0x6c3],
                                'queue_bytes':q.ram[0x1e],'five_phases':len(callbacks)==5,**result})
                writes.update(queue(q.ram));m=q;calls+=1;assert calls<1000
                if family=='opening':
                    token=body[cursor];cursor+=2 if token<128 else 1
                    if token==255:break
                elif not c.p&1:break
            if family=='opening':
                wanted={z['NT_top_origin']+y*32+x:v for y,row in enumerate(z['NT_rows']) for x,v in enumerate(row)}
            else:
                wanted=expected(z);assert calls==z['native_calls']
            assert writes==wanted and m.ram[0x6cf]==z['page']+1
            total+=page_count;lowest=min(lowest,page_low);call_count+=calls
            pages.append({'family':family,'entry_id':z['entry_id'],'calls':calls,
                          'IRQ_injections':page_count,'minimum_SP':page_low,
                          'PRG_states_covered':[list(x) for x in sorted(all_states)],
                          'baseline_final_NT_exact':True,'cursor_details':details})
    # Exact A448 -> A44B first-credit callsite with screen-off native bus.
    m=credits_initial(rom,credits[0]);m.ram[0x6f3]=m.ram[0xc6]
    c=MPU(memory=m);m.cpu=c;c.pc=0xa448;c.sp=0xfd;c.p=0x30;trace=[];steps=0
    while c.pc!=0xa44b:
        trace.append(snapshot(m,c));c.step();steps+=1;assert steps<30000
    assert m.nt==expected(credits[0]) and m.control==0x90 and m.mask==6
    # Only terminal callback: other phases write PPU/CHR and would require
    # independent actual clock/context evidence before injection in direct I/O.
    direct=check_trace(rom,trace,CALLBACKS[:1]);total+=direct['injections'];lowest=min(lowest,direct['minimum_SP'])
    direct.update(entry_id=credits[0]['entry_id'],instructions=steps,NT_cells=len(m.nt),
                  first_credit_direct_NT_exact=True,callback_scope='mode0 terminal acknowledgement only; IRQ scheduling not proven')
    out=R/'qa/reports/irq218_opening_credits.json';assert not out.exists()
    report={'work':218,'status':'PASS_SCOPED_OPENING_CREDITS_IRQ_ABI',
            'ROM_sha256':sha(target),'pages':pages,'initial_direct_credit':direct,
            'typed_calls':call_count,'IRQ_injections':total,'minimum_SP':lowest,
            'minimum_gap_after_192_byte_queue':lowest+1-192,
            'limitations':['Opening9 and progressive credits2: terminal IRQ at each cursor; five callbacks at first/empty-output boundary calls only.',
                           'First-credit direct I/O: terminal callback only. PPU-changing IRQ modes not injected.',
                           'Instruction-boundary CPU injection does not establish VRC7 clock, callback reachability, PPU behavior or hardware safety.',
                           'No asynchronous NMI, DMC, emulator, input or gameplay execution. Actual062 visual review remains user-owned.']}
    out.write_text(json.dumps(report,indent=2)+'\n','utf-8')
    print(json.dumps({k:report[k] for k in ('status','typed_calls','IRQ_injections','minimum_SP')}))

if __name__=='__main__':main()
