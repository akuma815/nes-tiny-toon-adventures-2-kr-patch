"""Execute final6502 wrapper/printer under real PRG8/9 switching; decode native queue."""
from pathlib import Path
import json
from asm6502 import MPU
from seal_nonplay171 import R,sha

class Memory:
    def __init__(self,rom):self.rom=rom;self.ram=bytearray(65536);self.banks=[18,19];self.switches=[]
    def __getitem__(self,a):
        if isinstance(a,slice):return bytes(self[x] for x in range(a.start or 0,a.stop,a.step or 1))
        if 0x8000<=a<0xc000:return self.rom[16+self.banks[(a-0x8000)//8192]*8192+(a&8191)]
        if a>=0xe000:return self.rom[0x3e010+(a&8191)]
        return self.ram[a]
    def __setitem__(self,a,v):
        if a in (0x8000,0x8008):self.banks[0 if a==0x8000 else 1]=v&31;self.switches.append((a,v))
        else:self.ram[a]=v

def main():
    folder=R/'build/opening11_poc_053';rom=(folder/'TinyToon2_Opening11_PoC053.nes').read_bytes();plan=json.loads((folder/'opening11_plan.json').read_text('utf-8'))
    out=R/'qa/reports/opening11_cpu186.json';assert not out.exists()
    cases=[]
    for page in plan['pages']:
        body=bytes.fromhex(page['body_hex']);mem=Memory(rom);r=mem.ram;r[0x18]=7;r[0x6cf]=page['page'];r[0x6cd:0x6cf]=page['original_pointer'].to_bytes(2,'little');r[0x6d1:0x6d3]=(0x21e4).to_bytes(2,'little');r[0x6c0:0x6c2]=(0x21e4).to_bytes(2,'little');r[0x2b]=0x32
        cpu=MPU(memory=mem);writes={};stepsizes=[];cursor=0;calls=0;worst=0
        while cursor<len(body):
            cpu.pc=0x95f9;cpu.sp=0xfd;r[0x1fe:0x200]=bytes.fromhex('ff c0');r[0x1e]=0;r[0x100:0x140]=bytes(64)
            before=cpu.processorCycles;steps=0
            while cpu.pc!=0xc100:cpu.step();steps+=1;assert steps<10000,(page['page'],hex(cpu.pc))
            count=r[0x1e];assert count in (0,10),count;stepsizes.append(count);calls+=1;worst=max(worst,cpu.processorCycles-before)
            assert cpu.sp==0xff and mem.banks==[18,19] and r[0x2b]==0x32,(page['page'],mem.banks,r[0x2b])
            first=body[cursor]
            if first<128:
                second=body[cursor+1]
                assert count==10 and cpu.p&1
                packets=[]
                for p in (0x100,0x105):
                    assert r[p]==1 and r[p+4]==255
                    address=r[p+1]*256+r[p+2];value=r[p+3];writes[address]=value;packets.append((address,value))
                assert packets[1][0]==packets[0][0]+32 and [v for _,v in packets]==[first,second]
                assert int.from_bytes(r[0x6c0:0x6c2],'little')==packets[0][0]+1
                cursor+=2
            else:
                assert count==0 and first in (254,255);cursor+=1
                assert bool(cpu.p&1)==(first==254)
                assert r[0x58]==(7 if first==254 else 96)
            assert r[0x6c3]==(0 if first==255 else cursor)
        for row,values in enumerate(page['NT_rows']):
            address=0x21e4+(row//2)*64+(row%2)*32
            assert [writes[address+i] for i in range(24)]==values
        assert r[0x6cf]==page['page']+1
        cases.append({'page':page['page'],'entry_id':page['entry_id'],'print_calls':calls,'tile_writes':len(writes),'max_added_packet_bytes_per_call':max(stepsizes),'max_wrapper_printer_cycles':worst,'PRG_restore_tag32_all_calls':True,'native_NT_coordinates_exact':True})
    result={'work':186,'status':'PASS_FINAL6502_PAIRED_ROW_PRINTER9PAGES','ROM_sha256':sha(folder/'TinyToon2_Opening11_PoC053.nes'),'cases':cases,'scope':'Final code including FDD3/FDDB/9227/93F0/93B5 and wrapper stack. No emulator/NMI transfer-budget proof yet.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
