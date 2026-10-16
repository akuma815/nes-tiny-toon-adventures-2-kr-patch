"""Final054 home guard/paired writer, unchanged opening9 and native5row clear CPU."""
from pathlib import Path
import json
from asm6502 import MPU
from verify_opening11_cpu186_v2 import Memory
from seal_nonplay171 import R,sha

def run(mem,pc,a=0,p=0x34):
    r=mem.ram;cpu=MPU(memory=mem);cpu.pc=pc;cpu.a=a;cpu.p=p;cpu.sp=0xfd;r[0x1fe:0x200]=bytes.fromhex('ff c0');steps=0
    while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<10000,(hex(cpu.pc),pc)
    assert cpu.sp==255
    return cpu

def paragraph(rom,z,pc,root,origin,columns):
    mem=Memory(rom);r=mem.ram;r[0x18]=root;r[0x6cf]=z['page'];r[0xc6]=z['font_bank'];r[0x6cd:0x6cf]=z['original_pointer'].to_bytes(2,'little');r[0x6d1:0x6d3]=origin.to_bytes(2,'little');r[0x6c0:0x6c2]=origin.to_bytes(2,'little');r[0x2b]=0x32
    body=bytes.fromhex(z['body_hex']);cursor=0;writes={};calls=0;cycles=[]
    while cursor<len(body):
        r[0x1e]=0;r[0x100:0x140]=bytes(64);cpu=run(mem,pc);calls+=1;cycles.append(cpu.processorCycles)
        assert mem.banks==[18,19] and r[0x2b]==0x32
        first=body[cursor];size=r[0x1e]
        if first<128:
            assert size==10 and cpu.p&1
            addresses=[]
            for at,k in ((0x100,0),(0x105,1)):
                assert r[at]==1 and r[at+4]==255
                a=r[at+1]*256+r[at+2];v=r[at+3];assert v==body[cursor+k];writes[a]=v;addresses.append(a)
            assert addresses[1]==addresses[0]+32
            assert int.from_bytes(r[0x6c0:0x6c2],'little')==addresses[0]+1
            cursor+=2
        else:
            assert first in (254,255) and size==0;assert bool(cpu.p&1)==(first==254)
            assert r[0x58]==(7 if first==254 else 96);cursor+=1
        assert r[0x6c3]==(0 if first==255 else cursor)
    for y,line in enumerate(z['NT_rows']):assert [writes[origin+y*32+x] for x in range(columns)]==line
    assert r[0x6cf]==z['page']+1
    return {'entry_id':z['entry_id'],'calls':calls,'tile_writes':len(writes),'max_wrapper_cycles':max(cycles),'all_NT_rows_exact':True,'all_PRG18_19_tag32_restored':True},writes

def main():
    folder=R/'build/home11_candidate_054';rom=(folder/'TinyToon2_Home11_Candidate054.nes').read_bytes();z=json.loads((folder/'home11_plan.json').read_text('utf-8'));old=(R/'build/opening11_poc_053/TinyToon2_Opening11_PoC053.nes').read_bytes();opening=json.loads((R/'build/opening11_poc_053/opening11_plan.json').read_text('utf-8'))
    out=R/'qa/reports/home11_cpu191.json';assert not out.exists()
    # Existing053 current observation, not a new emulator run.
    observed=(R/'qa/dialogue/opening11_187_train053/frame_00930_ram.bin').read_bytes()
    assert observed[0x18]==8 and observed[0xc6]==130 and int.from_bytes(observed[0x6cd:0x6cf],'little')==0x9731
    assert rom[0x2559b:0x2559d]==bytes.fromhex('a8 22') # mode1 origin958B/958C
    home,writes=paragraph(rom,z,z['wrapper_PC'],8,0x22a8,21)
    mem=Memory(rom);r=mem.ram;r[0x2b]=0x32;run(mem,0x920a);assert r[0x6e8]==22 and r[0x6e9]==5 and int.from_bytes(r[0x6e6:0x6e8],'little')==0x22a7
    cleared=set();steps=[]
    for y in range(5):
        r[0x1e]=0;r[0x100:0x140]=bytes(64);cpu=run(mem,0x919a)
        assert r[0x100]==1 and r[0x1e]==26 and r[0x119]==255
        address=r[0x101]*256+r[0x102];assert address==0x22a7+32*y and not any(r[0x103:0x119])
        cleared.update(range(address,address+22));assert bool(cpu.p&1)==(y<4);steps.append(cpu.processorCycles)
    assert set(writes)<=cleared and r[0x6e9]==0
    intro=[paragraph(rom,q,0x95f9,7,0x21e4,24)[0] for q in opening['pages']]
    # Nontarget guard: final native reader ABI/RAM/queue equals original05393E1.
    conditions=[]
    for root in range(16):
        for slot in range(48):
            if root==8 and slot==10:continue
            conditions.append((root,slot,130,0x9731))
    conditions.extend((8,10,font,0x9731) for font in (0,90,128,132,193,196,255))
    conditions.extend((8,10,130,ptr) for ptr in (0x973d,0x9740,0x9743,0x9746))
    for root,slot,font,ptr in conditions:
        memories=[];cpus=[]
        for image,pc in ((old,0x93e1),(rom,0x9630)):
            m=Memory(image);r=m.ram;r[0x18]=root;r[0x6cf]=slot;r[0xc6]=font;r[0x6cd:0x6cf]=ptr.to_bytes(2,'little');r[0x6c0:0x6c2]=(0x22a8).to_bytes(2,'little');r[0x6d1:0x6d3]=(0x22a8).to_bytes(2,'little');r[0x2b]=0x32
            cpu=run(m,pc,0x49,0x75);memories.append(m);cpus.append(cpu)
        a,b=cpus;assert (a.a,a.x,a.y,a.p,a.sp)==(b.a,b.x,b.y,b.p,b.sp),(root,slot,font,ptr)
        # Stack belowSP retains callsite return addresses; not persistent game state.
        assert memories[0].ram[:0x100]==memories[1].ram[:0x100]
        assert memories[0].ram[0x100:0x140]==memories[1].ram[0x100:0x140]
        assert memories[0].ram[0x200:0x800]==memories[1].ram[0x200:0x800]
        assert memories[0].banks==memories[1].banks==[18,19]
    report={'work':191,'status':'PASS_STATIC_CPU_HOME054_AND_OPENING9','ROM_sha256':sha(folder/'TinyToon2_Home11_Candidate054.nes'),'home':home,'original5row_clear':{'rows':5,'width':22,'origin':0x22a7,'cells':len(cleared),'all42home_tile_cells_covered':True,'step_cycles':steps},'opening9_finalCPU_paired_rows_preserved':intro,'nontarget_fallback_ABI_gameRAM_cases':len(conditions),'fallback_added_guard_latency_not_equal':True,'home_text_NT_width':21,'root8_from_existing053_actual_RAM':True,'runtime054':'NOT_RUN','limits':['FinalCPU excludesNMI/IRQ preemption/actual font consumption','Canonical9630 reuses openingrawdata nowshadowed by053 private streams; global other reachability unresolved','Font130 other unobserved consumers unresolved; homeentry only candidate','Original053runtime cannot be transferred wholesale to054','Not adopted/package/global11px/human final approval']}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in report.items() if k!='opening9_finalCPU_paired_rows_preserved'},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
