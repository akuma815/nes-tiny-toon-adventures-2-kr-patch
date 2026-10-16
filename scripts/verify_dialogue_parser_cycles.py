"""Execute original 6502 reader for both serialized paragraphs and compare per-call cycles."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/python/py65-1.2.0'))
from py65.devices.mpu6502 import MPU
def run(rom):
    memory=bytearray(65536);memory[0x8000:0xa000]=rom[0x4010:0x6010];memory[0xa000:0xc000]=rom[0x6010:0x8010]
    memory[0x6cd]=0xf9;memory[0x6ce]=0x95
    cpu=MPU(memory=memory);results=[]
    for index in range(37):
        cpu.pc=0x937c;cpu.sp=0xfd;memory[0x1fe]=0xff;memory[0x1ff]=0xc0
        before=cpu.processorCycles;steps=0
        while cpu.pc!=0xc100:
            cpu.step();steps+=1;assert steps<10000
        results.append({'index':index,'value':cpu.a,'cycles':cpu.processorCycles-before,'cursor':memory[0x6c3],'buffer_cursor':memory[0x6c4]})
        if cpu.a==0xfe:memory[0x6c4]=0
        if cpu.a==0xff:break
    assert len(results)==37 and results[-1]['value']==0xff
    return results
def main():
    m=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'));source=(ROOT/m['path']).read_bytes();assert hashlib.sha256(source).hexdigest()==m['sha256']
    path=ROOT/'build/dialogue_kr_poc_002/TinyToon2_dialogue_kr_poc.nes';new=path.read_bytes();a=run(source);b=run(new)
    for x,y in zip(a,b):
        assert x['cycles']==y['cycles'] and x['cursor']==y['cursor'] and x['buffer_cursor']==y['buffer_cursor'],(x,y)
    result={'status':'PASS','scope':'Native reader937C for first paragraph; instruction-level CPU harness, not live NMI/IRQ evidence','source_sha256':m['sha256'],'output_sha256':hashlib.sha256(new).hexdigest(),'calls':37,'cycles_equal_per_call':True,'cursor_equal_per_call':True,'total_reader_cycles':sum(x['cycles'] for x in a),'original_calls':a,'modified_calls':b,'py65_cpu_sha256':hashlib.sha256((ROOT/'tools/python/py65-1.2.0/py65/devices/mpu6502.py').read_bytes()).hexdigest()}
    (ROOT/'qa/reports/dialogue_parser_cycles002.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('original_calls','modified_calls')},indent=2))
if __name__=='__main__':main()
