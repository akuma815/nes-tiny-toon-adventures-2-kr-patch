from pathlib import Path
import collections,csv,hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def main():
 out=R/'qa/reports/irqdma137_validation.json';assert not out.exists();prior=json.loads((R/'qa/reports/irq136_validation.json').read_text('utf-8'))
 table={'FE53':('FE55',5),'FE55':('FE56',2),'FE56':('FE58',3),'FE58':('FE5A',3),'FE5A':('FE5C',3),'FE5C':('FE53',3)}
 result={};streams={}
 for build in ['047','049']:
  q=R/f'qa/dialogue/irqdma137_normal3_{build}';ref=R/f'qa/dialogue/irq136_normal3_{build}';rom=R/f'build/dialogue_kr_poc_{build}/TinyToon2_dialogue_kr_poc.nes';blob=rom.read_bytes();env=json.loads((q/'environment.json').read_text('utf-8'))
  assert env['rom_sha256']==env['actual_QA_ROM_sha256']==sha(rom) and env['exit_code']==0 and env['frames']==2400
  for f,h in env['files'].items():assert sha(q/f)==h
  reused=['frame_counters.csv','IRQ_entries.csv','IRQ_instructions.csv','IRQ_reads.csv','IRQ_ports.csv','idle_opcodes.csv']
  for f in reused:assert (q/f).read_bytes()==(ref/f).read_bytes()
  initial=(q/'initial_PRG_cdl.bin').read_bytes();final=(q/'final_PRG_cdl.bin').read_bytes();assert len(initial)==len(final)==0x40000 and all(not(v&0x80)for v in initial)
  dmc=rows(q/'DMC_reads.csv');idle=rows(q/'idle_opcodes.csv');assert len(dmc)==257
  for x in dmc:
   rel=int(x['PRG_relative'],16);assert final[rel]&0x80 and x['address']==x['current_address'] and int(x['bytes_remaining'])>0 and blob[16+rel]==int(x['value'],16)
  gaps=[]
  for a,b in zip(idle,idle[1:]):
   if a['frame']!=b['frame'] or b['pc']!=table[a['pc']][0]:continue
   pure=table[a['pc']][1];extra=int(b['cycle'])-int(a['cycle'])-pure
   if 0<extra<10:
    assert extra in [3,4];matches=[r for r in dmc if int(a['cycle'])<int(r['cycle'])<int(b['cycle'])];assert len(matches)==1
    gaps.append({'before':a,'after':b,'pure':pure,'extra':extra,'native_DMC_read':matches[0]})
  assert len(gaps)==204 and collections.Counter(x['extra']for x in gaps)==({3:27,4:177} if build=='047' else {3:25,4:179})
  irqs=[]
  for case in prior['builds'][build]['IRQ_cases']:
   g=case['one_extra4_gap_not_typed'];matches=[r for r in dmc if g['cycle']<int(r['cycle'])<g['cycle']+g['real']];assert len(matches)==1 and int(matches[0]['irq'])==case['frame']-1998
   irqs.append({'frame':case['frame'],'gap':g,'native_DMC_read':matches[0]})
  streams[build]={'dmc':dmc,'idle':idle,'gaps':gaps};result[build]={'environment_sha256':sha(q/'environment.json'),'initial_native_PCM_empty':True,'native_PCM_cursor_ROM_matched_reads':257,'six136_telemetry_files_byte_exact':True,'typed_idle_adjacent_opcode_waits':gaps,'typed_IRQ_waits':irqs,'wait_histogram':dict(collections.Counter(x['extra']for x in gaps))}
 a,b=streams['047']['dmc'],streams['049']['dmc'];timediffs=[]
 for x,y in zip(a,b):
  for k in ['frame','address','value','PRG_relative','current_address','bytes_remaining','sample_address','sample_length','silence','irq']:assert x[k]==y[k]
  if x['cycle']!=y['cycle']:
   assert x['frame']=='2001' and int(y['cycle'])-int(x['cycle']) in [-2,2];timediffs.append({'047':x,'049':y})
 assert len(timediffs)==4 and collections.Counter(int(x['049']['cycle'])-int(x['047']['cycle'])for x in timediffs)=={-2:2,2:2}
 chain={}
 for build,lo,hi in [('047',59604778,59608335),('049',59604777,59608334)]:
  chain[build]=[x for x in streams[build]['idle']if x['frame']=='2001' and lo<=int(x['cycle'])<=hi]
 assert len(chain['047'])==len(chain['049'])==1114 and all(x['pc']==y['pc']for x,y in zip(chain['047'],chain['049']))
 histogram=collections.Counter(int(y['cycle'])-int(x['cycle'])for x,y in zip(chain['047'],chain['049']));assert histogram=={-1:1112,-5:2}
 exception=[]
 for x,y in zip(chain['047'],chain['049']):
  if int(y['cycle'])-int(x['cycle'])==-5:
   oldgap=next(g for g in streams['047']['gaps']if g['after']==x);newgap=next(g for g in streams['049']['gaps']if g['before']==y)
   assert oldgap['extra']==newgap['extra']==4 and oldgap['native_DMC_read']['address']==newgap['native_DMC_read']['address'] and oldgap['native_DMC_read']['cycle']==newgap['native_DMC_read']['cycle']
   exception.append({'047_wait_before_exec':oldgap,'049_wait_after_exec':newgap})
 source=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));assert sha(R/source['path'])==source['sha256']
 src=json.loads((R/'work/audio_001/DMC_consumer_source.json').read_text('utf-8'))+json.loads((R/'work/dmc_001/source_v4.json').read_text('utf-8'))
 for x in src:assert '/2.1.1/'in x['URL'] and sha(R/x['path'])==x['sha256']
 v={'work':137,'status':'PASS_BOUNDED_IDLE_AND_IRQ_DMC_WAIT_DISCRIMINATION','ROM049_sha256':sha(R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes'),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'builds':result,'read_values_order_cursor_sample_state_equal':257,'native_read_PC_diff_count':sum(x['pc']!=y['pc']for x,y in zip(a,b)),'four_two_cycle_shifted_DMC_reads':timediffs,'2001_same_PC_idle_chain_to_IRQ':{'instructions':1114,'cycle_delta_histogram':dict(histogram),'two_4cycle_wait_moves_across_exec_callback':exception},'classification':'All204 short idle gaps plus4 IRQ gaps each linked to cursor/remaining + fresh native PCM-CDL + exact ROM read. Different3/4 DMC alignment patterns shift idle timing; sampled1114-PC chain ends at the1-cycle earlierADC/IRQ entry. Two transient-5cycle exec observations are4cycle DMA waits before vs after exec, not a persistent5cycle faster game. Values preserved but2 sample reads are2cycles earlier and2 are2cycles later, not all audio timing identity.','source_records':src,'human_final_review':False,'scope':'Declared1000 ticket3 seed, same2400-frame driver, bus observation1999..2002 only. No ROM/state change, newscene/build/apply/PCM listening/hardware/global gameplay equality. No timing-padding ROM fix justified by this bounded observation.'}
 out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':v['status'],'DMC_reads_each':257,'idle_waits_typed_each':204,'IRQ_waits_typed_each':4,'DMC_values_equal':True,'two_cycle_shifted_reads':4},indent=2))
if __name__=='__main__':main()
