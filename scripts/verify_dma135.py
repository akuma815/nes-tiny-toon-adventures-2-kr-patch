"""Actual opcode replay + DMC cursor/fresh PCM-CDL explains before-RTS boundary."""
from pathlib import Path
import csv,hashlib,json
from verify_gate_font_tag_hooks import Memory,MPU
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/dma135_validation.json';assert not out.exists();source_records=[]
 for name in ['work/audio_001/DMC_consumer_source.json','work/dmc_001/source_v4.json']:
  for v in json.loads((R/name).read_text('utf-8')):assert '/2.1.1/' in v['URL'] and sha(R/v['path'])==v['sha256'];source_records.append(v)
 cpu=(R/'work/audio_001/NesCpu.cpp').read_text();debug=(R/'work/audio_001/NesDebugger.cpp').read_text()
 assert 'void NesCpu::ProcessPendingDma(' in cpu and '_isDmcDmaRead = true' in cpu and 'MemoryOperationType::DmaRead' in debug and 'IsDmcDma' in debug
 result={};allreads={}
 for build in ['047','049']:
  q=R/f'qa/dialogue/dma135v2_home{build}';env=json.loads((q/'environment.json').read_text('utf-8'));rom=R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes()
  assert env['rom_sha256']==env['actual_QA_ROM_sha256']==sha(rom) and env['exit_code']==0 and env['frames']==960
  for f,h in env['files'].items():assert sha(q/f)==h
  initial=(q/'initial_PRG_cdl.bin').read_bytes();final=(q/'final_PRG_cdl.bin').read_bytes();assert len(initial)==len(final)==0x40000 and all(not(v&0x80) for v in initial)
  z=rows(q/'instructions.csv');assert len(z)==(63 if build=='047' else 81) and z[0]['kind']=='entry' and z[-1]['kind']=='returned' and z[-1]['pc']=='9BBA'
  m=Memory(blob);m.ram[:0x800]=(q/'entry_RAM.bin').read_bytes();c=MPU(memory=m);m.cpu=c;c.pc=int(z[0]['pc'],16)
  for k in ['a','x','y','sp']:setattr(c,k,int(z[0][k],16))
  c.p=int(z[0]['ps'],16);gaps=[]
  for i,row in enumerate(z[:-1]):
   assert c.pc==int(row['pc'],16) and m[c.pc]==int(row['opcode'],16)==blob[16+int(row['PRG_relative'],16)]
   for k in ['a','x','y','sp']:assert getattr(c,k)==int(row[k],16)
   assert c.p&0xcf==int(row['ps'],16)&0xcf # PHP/PLP normalized reserved B/U; all six operational flags equal.
   start=c.processorCycles;c.step();pure=c.processorCycles-start;elapsed=int(z[i+1]['cycle'])-int(row['cycle'])
   assert c.pc==int(z[i+1]['pc'],16)
   if elapsed!=pure:gaps.append({'instruction':row,'next':z[i+1],'pure_cycles':pure,'elapsed':elapsed,'extra':elapsed-pure})
  assert m.ram[:0x800]==(q/'returned_RAM.bin').read_bytes() and len(gaps)==1 and gaps[0]['extra']==4
  assert gaps[0]['instruction']['pc']==('9445' if build=='047' else 'FE00') and gaps[0]['pure_cycles']==(6 if build=='047' else 4)
  d=rows(q/'DMC_reads.csv');assert len(d)==362;allreads[build]=d
  for x in d:
   rel=int(x['PRG_relative'],16);assert final[rel]&0x80 and x['address']==x['current_address'] and int(x['bytes_remaining'])>0 and blob[16+rel]==int(x['value'],16)
  g=gaps[0];matching=[x for x in d if int(g['instruction']['cycle'])<int(x['cycle'])<int(g['next']['cycle'])];assert len(matching)==1
  read=matching[0];assert read['cycle']=='27519253' and read['address']=='C686' and read['value']=='20' and read['PRG_relative']=='3C686' and read['bytes_remaining']=='187'
  live=int(z[-1]['cycle'])-int(z[0]['cycle']);assert c.processorCycles==(207 if build=='047' else 245) and live==(211 if build=='047' else 249)
  result[build]={'instruction_transitions_PC_opcode_register_and_operational_flags_exact':len(z)-1,'whole_returned_RAM_model_exact':True,'pure_cycles_to_actual_return':c.processorCycles,'real_cycles_to_actual_return':live,'only_wait_gap':g,'native_cursor_CDLPcm_ROM_byte_matched_read':read,'window920_926_native_DMC_reads':len(d),'initial_PCM_CDL_empty':True,'before_RTS_elapsed':int(next(x for x in z if x['pc']=='9445')['cycle'])-int(z[0]['cycle']),'environment_sha256':sha(q/'environment.json')}
 for a,b in zip(allreads['047'],allreads['049']):
  for k in a:
   if k!='pc':assert a[k]==b[k],k
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 v={'work':135,'status':'PASS_NATURAL_FIRST_HOME_DMC_WAIT_RELOCATION','ROM049_sha256':sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'builds':result,'DMC_read_window_values_order_frames_cycles_cursor_and_sample_state_exact':362,'DMC_read_PC_difference_count':sum(a['pc']!=b['pc'] for a,b in zip(allreads['047'],allreads['049'])),'real_complete_call_delta':38,'pure_complete_call_delta':38,'134_boundary_erratum':'134 measured until beforeRTS and added nominal6. Old RTS actually waited4 DMCcycles, current earlierSTA FE00 waited4. BeforeRTS delta42 is correct but complete-call delta38; no total additional4 current-call overhead. Frozen134 retained and this correction linked.','source_records':source_records,'source_inference':'Lua read callback is untyped; native DMC cursor/remaining, fresh native PCM-CDL bit80, exact read value/cycle inside sole4-cycle instruction gap and pinned ProcessPendingDma distinguish DMC wait relocation. Not hardware or PCM listening.','human_final_review':False,'scope':'Two natural960-frame cold boots/onlyStart720, no currency/PC/RAM/ROM/state edits. First home924 call and7-frame DMC window only; shortage IRQ1cycle issue from134 is separate and still bounded/open.'}
 out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':v['status'],'pure_call_delta':38,'complete_live_call_delta':38,'DMC_bytes_equal':362,'first_home_DMA_read_cycle':27519253},indent=2))
if __name__=='__main__':main()
