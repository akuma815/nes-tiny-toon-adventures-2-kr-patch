from pathlib import Path
import csv,hashlib,json
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
class BusMemory(Memory):
 def __getitem__(self,a):
  if 0x2000<=a<=0x2007:
   v=self.reads.pop(0);assert int(v['address'],16)==a;return int(v['value'],16)
  return super().__getitem__(a)
def main():
 out=R/'qa/reports/irq136_validation.json';assert not out.exists();result={};streams={}
 for build in ['047','049']:
  q=R/f'qa/dialogue/irq136_normal3_{build}';rom=R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();env=json.loads((q/'environment.json').read_text('utf-8'))
  assert env['rom_sha256']==sha(rom) and env['exit_code']==0 and env['frames']==2400
  for f,h in env['files'].items():assert sha(q/f)==h
  reference=R/f'qa/dialogue/live134v2_normal3_{build}/frame_counters.csv';snap=rows(q/'frame_counters.csv');assert snap==rows(reference)[:2400]
  inst=rows(q/'IRQ_instructions.csv');reads=rows(q/'IRQ_reads.csv');entries=rows(q/'IRQ_entries.csv');ports=rows(q/'IRQ_ports.csv');idle=rows(q/'idle_opcodes.csv');assert len(entries)==4 and len(inst)==532 and len(ports)==144
  cases=[]
  for i in range(1,5):
   z=[v for v in inst if v['irq']==str(i)];assert len(z)==133 and z[0]['pc']=='FA5B' and z[-1]['pc']=='FD18'
   m=BusMemory(blob);m.ram[:0x800]=(q/f'IRQ_{i:02d}_entry_RAM.bin').read_bytes();m.reads=[r for r in reads if r['irq']==str(i)];c=MPU(memory=m);m.cpu=c;c.pc=int(z[0]['pc'],16)
   for k in ['a','x','y','sp']:setattr(c,k,int(z[0][k],16))
   c.p=int(z[0]['ps'],16);gaps=[]
   for n,v in enumerate(z[:-1]):
    assert c.pc==int(v['pc'],16) and m[c.pc]==int(v['opcode'],16)==blob[16+int(v['PRG_relative'],16)]
    for k in ['a','x','y','sp']:assert getattr(c,k)==int(v[k],16)
    assert c.p&0xcf==int(v['ps'],16)&0xcf
    before=c.processorCycles;c.step();pure=c.processorCycles-before;actual=int(z[n+1]['cycle'])-int(v['cycle'])
    assert c.pc==int(z[n+1]['pc'],16)
    if pure!=actual:gaps.append({'pc':v['pc'],'cycle':int(v['cycle']),'pure':pure,'real':actual,'extra':actual-pure})
   assert not m.reads and c.processorCycles==402 and int(z[-1]['cycle'])-int(z[0]['cycle'])==406 and len(gaps)==1 and gaps[0]['extra']==4
   cases.append({'frame':int(z[0]['frame']),'pure_body_until_RTI':402,'real_body_until_RTI':406,'operational_CPU_model_exact':True,'one_extra4_gap_not_typed':gaps[0]})
  streams[build]={'inst':inst,'ports':ports,'entries':entries,'idle':idle};result[build]={'environment_sha256':sha(q/'environment.json'),'2400_counter_rows_equal_frozen134':True,'IRQ_cases':cases}
 a,b=streams['047'],streams['049'];inst_diffs=[]
 for x,y in zip(a['inst'],b['inst']):
  for k in ['frame','irq','kind','pc','opcode','PRG_relative','x','y','sp']:assert x[k]==y[k]
  delta=int(y['cycle'])-int(x['cycle']);assert delta==(-1 if x['frame']=='2001' else 0)
  dot_delta=341*(int(y['scanline'])-int(x['scanline']))+int(y['dot'])-int(x['dot']);assert dot_delta==delta*3
  if x!=y:inst_diffs.append({k:[x[k],y[k]]for k in x if x[k]!=y[k]})
 port_diffs=[]
 for x,y in zip(a['ports'],b['ports']):
  for k in ['frame','irq','pc','address','value','scanline']:assert x[k]==y[k]
  delta=int(y['cycle'])-int(x['cycle']);assert delta==(-1 if x['frame']=='2001' and x['irq']=='3' else 0)
  assert int(y['dot'])-int(x['dot'])==delta*3
  if delta:port_diffs.append({'047':x,'049':y})
 assert len(port_diffs)==19 and {x['047']['address']for x in port_diffs}>={'F000','F008'}
 eold,enew=a['entries'][2],b['entries'][2];assert eold['frame']==enew['frame']=='2001' and eold['saved_pc']==enew['saved_pc']=='FE5A' and eold['last_idle_pc']==enew['last_idle_pc']=='FE58'
 assert int(eold['cycle'])-int(eold['last_idle_cycle'])==int(enew['cycle'])-int(enew['last_idle_cycle'])==10
 assert int(enew['last_idle_cycle'])-int(eold['last_idle_cycle'])==int(enew['cycle'])-int(eold['cycle'])==-1
 for e in [eold,enew]:
  stream=a if e is eold else b;v=next(v for v in stream['idle']if v['pc']=='FE58' and v['cycle']==e['last_idle_cycle']);assert v['frame']=='2001'
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 v={'work':136,'status':'PASS_BOUNDED_IDENTICAL_IRQ_BODY_WITH_PREEXISTING_IDLE_SHIFT','ROM049_sha256':sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'builds':result,'IRQ_pc_opcode_sequence_equal':532,'IRQ_relative_body_duration_equal':True,'port_writes_values_sequence_equal':144,'2001_one_cycle_advance_including_IRQ_ack_reload':port_diffs,'2001_before_IRQ_idle_ADC_started_one_cycle_earlier':{'047':eold,'049':enew},'idle_opcode_to_vector_delta_equal':10,'classification':'Difference already exists before IRQ entry, at same native idleADC FE58. Handler sequence/relative timing unchanged, not a new1-cycle faster handler or claimed changed IRQ acceptance latency. Upstream idle3/4-cycle short stalls remain untyped; next narrow DMC/CDL discrimination.','operational_flag_scope':'B/U normalized in pure model; real inherited overflow/A differences from idleRAM22 retained, not ignored as wholeCPU equality','human_final_review':False,'scope':'Two2400-frame initial ticket3 runs, native4IRQ1999..2002 each. New timing/bus CPU-model evidence only; no new scene/ROM/apply/PCM/hardware/global gameplay claim.'}
 out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':v['status'],'equal_irq_instructions':532,'ports_equal':144,'advanced_writes':19,'preexisting_idle_shift':-1},indent=2))
if __name__=='__main__':main()
