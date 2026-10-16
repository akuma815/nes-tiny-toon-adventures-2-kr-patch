"""Validate actual native enemy lifecycle writers and executed removal path; no winningbot claim."""
from pathlib import Path
import csv,json,hashlib,collections
from verify_gate_font_tag_hooks import Memory,MPU
from py65.disassembler import Disassembler
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/cart_enemy068_validation.json';assert not out.exists();rom=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';b=rom.read_bytes();total=0;writes=0;compared=0
 runs=[]
 for name,frames in [('cart068_enemy',6000),('cart068_enemy_v2',4200),('cart068_enemy_v3',4200)]:
  q=R/'qa/dialogue'/name;e=json.loads((q/'environment.json').read_text());assert e['exit_code']==0 and e['rom_sha256']==sha(rom)and(q/'trace_complete.txt').read_text()==str(frames)
  for p,h in e['files'].items():assert sha(q/p)==h;total+=1
  rows=list(csv.DictReader((q/'enemy_writes.csv').open()))
  for r in rows:
   k=int(r['next_PRG'],16);code=b[0x10+k-3:0x10+k];op=code[0];assert op in(0x9d,0x99,0xfe,0xde),code.hex()
   base=int.from_bytes(code[1:],'little');idx=int(r['cpu_y']if op==0x99 else r['cpu_x'],16);assert(base+idx)&65535==int(r['address'],16)
   if op in(0xfe,0xde):assert int(r['value'],16)in(int(r['old'],16),(int(r['old'],16)+(1 if op==0xfe else -1))&255)
   writes+=1
  falling=[r for r in rows if r['address']=='043E'and r['value']=='04'];assert len(falling)==1 and falling[0]['frame']=='4033'and falling[0]['next_PRG']=='35B46'
  removed=[r for r in rows if r['address']=='042E'and r['value']=='00'and int(r['frame'])>4000];assert len(removed)==1 and removed[0]['frame']=='4065'and removed[0]['next_PRG']=='36E4A'
  # Same controller route with read-only telemetry: authoritative raw memory matches work66.
  for p in q.glob('frame_*_ram.bin'):
   for suffix in ('ram.bin','ppu.bin','oam.bin'):
    f=q/(p.name.replace('ram.bin',suffix));baseline=R/'qa/dialogue/cart066_geometry'/f.name
    assert f.read_bytes()==baseline.read_bytes(),(name,f.name);compared+=1
  runs.append({'name':name,'frames':frames,'write_rows':len(rows),'fall':falling[0],'remove_type':removed[0]})
 ex=list(csv.DictReader((R/'qa/dialogue/cart068_enemy_v2/enemy_fall_exec.csv').open()));m=Memory(b);m.banks=[0x3a,0x3b,0x3e,31];d=Disassembler(MPU(memory=m));instructions={}
 for r in ex:
  pc=int(r['address'],16);k=int(r['PRG_relative'],16);assert k==(0x34000 if pc<0xa000 else 0x36000)+(pc&8191)
  n,s=d.instruction_at(pc);assert '???'not in s;instructions[r['address']]={'PRG_relative':r['PRG_relative'],'instruction':s,'bytes':b[0x10+k:0x10+k+n].hex()}
 clear=[i for i,r in enumerate(ex)if r['address']=='AE3F'and r['state']=='04'];assert len(clear)==1;i=clear[0];assert ex[i-1]['address']=='996B'and instructions['996B']['instruction']=='JMP $ae3f'
 proof=R/'work/cart_enemy_001/executed_native_instructions.json';assert not proof.exists();proof.parent.mkdir(exist_ok=True);proof.write_text(json.dumps({'ROM_sha256':sha(rom),'observed_exec_rows':len(ex),'instructions':instructions,'removal_path':ex[i-6:i+5],'scope':'Actual executed addresses in frame4030..4070 withX14, canonical3A/3B. Inline pointer bytes are not linearly decoded.'},indent=2)+'\n')
 readq=R/'qa/dialogue/cart068_enemy_v3';reads=list(csv.DictReader((readq/'enemy_type_consumers.csv').open()));assert reads
 report={'work':68,'status':'NATIVE_ENEMY_FALL_AND_REMOVAL_CONNECTED','ROM_SSOT_changes':0,'runtime_files':total,'validated_write_rows':writes,'core_memory_files_exact_against66':compared,'runs':runs,'exec_rows':len(ex),'unique_actual_instructions':len(instructions),'type_read_aggregated_rows':len(reads),'type_read_count':sum(int(r['count'])for r in reads),'sprite_zero_is_not_removal':'Many animation writers clear040E/F while0420type and0410active remain nonzero; only the4033 fall and4065 AE3F full object clear establishes removal.','natural_clear':False,'direct_visual':'No new direct visual check; actual raw-memory and native-code observation','limits':['Only one enemy removed; no naturalbonus/history/gold claim','Read/write/exec callbacks do not edit actual machine state','Runtime core memory equals66 in observed snapshots, not waveform/framebuffer identity','Globalcorpus/PCM/listening/hardware/finalhumanreview pending'],'next_action':'Connect the native cart remaining-enemy/clear consumer from actual0420 read observations, then retune the level0 controller strategy.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','runtime_files','validated_write_rows','core_memory_files_exact_against66','exec_rows','unique_actual_instructions','type_read_aggregated_rows')},indent=2))
if __name__=='__main__':main()
