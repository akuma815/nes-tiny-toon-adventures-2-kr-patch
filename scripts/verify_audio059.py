"""Original Japan vs043 audio register/value/frame and APU state preservation; bounded routes."""
from pathlib import Path
import json,csv,collections,hashlib
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def state(p):return dict(x.split('=',1)for x in p.read_text().splitlines())
def main():
 out=R/'qa/reports/audio059_validation.json';assert not out.exists();src=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));old=R/src['path'];new=R/'build/dialogue_kr_poc_043/TinyToon2_dialogue_kr_poc.nes';assert sha(old)==src['sha256'];ob=old.read_bytes();nb=new.read_bytes();results=[];frozen=screens=apu_fields=chunks=0
 source=json.loads((R/'work/audio_001/source.json').read_text());assert sha(R/'work/audio_001/DeltaModulationChannel.cpp')==source['sha256']
 dmc=(R/'work/audio_001/DeltaModulationChannel.cpp').read_text();assert '_sampleAddr = 0xC000 | ((uint32_t)value << 6)'in dmc and '_sampleLength = (value << 4) | 0x0001'in dmc
 for ride in ('coaster','cart','train','water'):
  a=R/f'qa/dialogue/audio_japan_{ride}';b=R/f'qa/dialogue/audio043_{ride}';ea=json.loads((a/'environment.json').read_text());eb=json.loads((b/'environment.json').read_text());assert ea['frames']==eb['frames']==9000 and ea['exit_code']==eb['exit_code']==0 and ea['input']==eb['input'];assert ea['rom_sha256']==sha(old)and eb['rom_sha256']==sha(new)
  for q,e,blob,base,bank in ((a,ea,ob,0x20010,'1C000'),(b,eb,nb,0x40010,'3C000')):
   assert(q/'trace_complete.txt').read_text()=='9000'
   for p,h in e['files'].items():assert sha(q/p)==h;frozen+=1
   for p in q.glob('frame_*.png'):
    ppu=(q/(p.stem+'_ppu.bin')).read_bytes();mp=list(csv.DictReader((q/(p.stem+'_mapping.csv')).open()))
    assert [x['relative_offset']for x in mp if x['kind']=='prg'and x['cpu_or_ppu_address']=='C000']==[bank]
    for m in mp:
     if m['kind']!='chr':continue
     start=int(m['cpu_or_ppu_address'],16);off=int(m['relative_offset'],16);assert ppu[start:start+1024]==blob[base+off:base+off+1024];chunks+=1
    screens+=1
  ra=list(csv.DictReader((a/'audio_writes.csv').open()));rb=list(csv.DictReader((b/'audio_writes.csv').open()));assert len(ra)==len(rb)and len(ra)>1000
  required=('frame','pc','address','value','kind','root','phase','course','pause')
  assert all(all(x[k]==y[k]for k in required)for x,y in zip(ra,rb))
  assert all(int(y['PRG_relative'],16)-int(x['PRG_relative'],16)==0x20000 for x,y in zip(ra,rb))
  delta=collections.Counter(int(y['cycle'])-int(x['cycle'])for x,y in zip(ra,rb));assert max(map(abs,delta))<=4
  wa=list(csv.DictReader((a/'world_phase.csv').open()));wb=list(csv.DictReader((b/'world_phase.csv').open()));assert len(wa)==len(wb)==300
  assert all(all(x[k]==y[k]for k in x if k not in ('headfont','lowerfont','pc'))for x,y in zip(wa,wb))
  pc_changes=[{'frame':x['frame'],'source':x['pc'],'043':y['pc']}for x,y in zip(wa,wb)if x['pc']!=y['pc']]
  pairs=[];nf=0
  for p in sorted(a.glob('frame_*_state.txt')):
   x=state(p);y=state(b/p.name);keys={k for k in x if k.startswith('apu.')};assert keys=={k for k in y if k.startswith('apu.')};assert all(x[k]==y[k]for k in keys),(ride,p.name);apu_fields+=len(keys);nf+=1
  sample_start=sample_length=None;uses=collections.Counter()
  for x in ra:
   if x['address']=='4012':sample_start=int(x['value'],16)
   elif x['address']=='4013':sample_length=int(x['value'],16)
   elif x['address']=='4015'and int(x['value'],16)&16:assert sample_start is not None and sample_length is not None;uses[(sample_start,sample_length)]+=1
  for(s,l),count in sorted(uses.items()):
   off=s*64;size=l*16+1;v=ob[0x1c010+off:0x1c010+off+size];assert v==nb[0x3c010+off:0x3c010+off+size];pairs.append({'4012':s,'4013':l,'CPU_address':hex(0xc000+off),'bytes':size,'recorded_enable_writes':count,'ROM_sample_sha256':hashlib.sha256(v).hexdigest()})
  results.append({'ride':ride,'each_frames':9000,'audio_writes_each':len(ra),'kind_counts':dict(collections.Counter(x['kind']for x in ra)),'all_value_order_frame_context_PC_exact':True,'cycle_delta043_minus_source_counts':dict(sorted(delta.items())),'APU_snapshot_pairs_all_fields_exact':nf,'world_gameplay_currency_history_fields_exact':True,'world_PC_observations_differing':pc_changes,'world_font_differences_expected_scope':'Localized headfont and owned lowerfont latch differ; not wholeRAMidentity','DMC_programmed_sample_bytes_exact':pairs})
 report={'work':59,'status':'PASS','scope':'Original Japan/043 four declared9k native controller routes; audio write value/order/frame/context/PC exact; 1..4cycle differences recorded, APU states exact, DMC programmed ROM bytes exact','source_sha256':sha(old),'ROM_sha256':sha(new),'ROM_SSOT_changes':0,'runs':results,'screens_including_original_sides':screens,'runtime_frozen_files':frozen,'mapped_CHR_1K_chunks_exact':chunks,'APU_snapshot_field_comparisons_exact':apu_fields,'DMC_formula_source':source,'limits':['No PCM output or listening test, therefore no audibleidentity claim','Recorded routes only, none naturalfullclear; no allmusic/allsounds/allframescoverage','VRC7 FM write count applies onlythese paths, not wholeROMglobalabsence','DMC programmed ROM bytes and sampled C000bank verified, not each actualDMC fetch callback','WorldPC observations/fonts differ; do not claim fullCPUcycle/worldRAMidentity','No hardware/finalhumanreview/corpusglobalclosure'],'next_action':'Trace actual DMC fetch consumer on one bounded source/043 path, distinct from programmed ROM samples.'}
 out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k]for k in ('status','screens_including_original_sides','runtime_frozen_files','mapped_CHR_1K_chunks_exact','APU_snapshot_field_comparisons_exact')},indent=2));print([(r['ride'],r['audio_writes_each'])for r in results])
if __name__=='__main__':main()
