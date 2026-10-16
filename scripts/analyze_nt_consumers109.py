"""Native NT20 bounded source catalog -> frozen observations, never global-unused proof."""
from pathlib import Path
import csv,json,hashlib,collections
from title_codec import unpack
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf-8'))
def main():
 out=R/'qa/reports/nt109_consumers.json';work=R/'work/nt_consumers109';assert not out.exists() and not work.exists()
 meta=load(R/'manifests/source_rom.json');source=(R/meta['path']).read_bytes();assert sha(R/meta['path'])==meta['sha256']
 rom=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';assert sha(rom)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 catalog=load(R/'work/graphics_population_001/native_NT_catalog.json')['assets'];assert len(catalog)==20
 calls=collections.defaultdict(list);files={};envrefs=[];rejected=[]
 for directory in sorted((R/'qa/dialogue').iterdir()):
  log=directory/'native_NT_calls.csv';envpath=directory/'environment.json'
  if not directory.is_dir() or not log.exists() or not envpath.exists():continue
  env=load(envpath)
  if env['exit_code']!=0:rejected.append({'path':str(log.relative_to(R)),'reason':'Nonzero historical emulator exit; not observation evidence'});continue
  assert sha(log)==env['files']['native_NT_calls.csv']
  used=directory/'capture_survey_used.lua';assert sha(used)==env['lua_sha256']
  # This catalog reader only counts the established physical8025 entry point.
  lua=used.read_text('utf-8');assert '0x4025' in lua and '0x24025' in lua
  historical_rom=Path(env['command'][3]);assert sha(historical_rom)==env['rom_sha256']
  for p in [log,envpath,used]:files[p.relative_to(R).as_posix()]=sha(p)
  envrefs.append({'directory':directory.relative_to(R).as_posix(),'ROM_sha256':env['rom_sha256'],'environment_sha256':sha(envpath),'intervention':env['intervention'],'frames':env['frames']})
  for x in csv.DictReader(log.open(encoding='utf-8')):
   selector=int(x['selector'],16);assert selector in range(0,0x28,2) and x['pc']=='8025' and int(x['PRG_relative'],16)in[0x4025,0x24025]
   calls[selector].append({'path':log.relative_to(R).as_posix(),'ROM_sha256':env['rom_sha256'],**x})
 records=[];decoded=[]
 for asset in catalog:
  selector=asset['selector'];a=asset['source_file_offset'];n=asset['encoded_length'];raw=source[a:a+n];assert hashlib.sha256(raw).hexdigest()==asset['encoded_sha256'];nt,used=unpack(raw);assert used==n and len(nt)==asset['decoded_cells']
  if selector<0x1e:
   pointer=int.from_bytes(source[0x40d1+selector:0x40d3+selector],'little');derived=pointer-0x3ff0
  else:
   pointer=int.from_bytes(source[0x4243+selector-0x1e:0x4245+selector-0x1e],'little');derived=0x20010+18*0x400+pointer-0x1000
  assert derived==a,(selector,pointer,derived,a)
  z=calls[selector];current=[x for x in z if x['ROM_sha256']==sha(rom)]
  ctx=collections.Counter((x['root'],x['ride'],x['head_font'])for x in z)
  records.append({'selector_hex':f'{selector:02X}','source_file_offset':a,'source_encoded_sha256':asset['encoded_sha256'],'encoded_length':n,'decoded_cells':len(nt),'native_table_pointer_hex':f'{pointer:04X}','native_table_to_source_exact':True,'storage':asset['storage'],'observed8025_call_rows':len(z),'current047_8025_call_rows':len(current),'contexts_at_entry':[{'root':r,'ride':ride,'pre_draw_head_font_hex':font,'count':count}for(r,ride,font),count in ctx.most_common()],'example_call':current[0]if current else (z[0]if z else None),'ASCII_candidate_texts':[x['decoded_with_font124']for x in asset['ASCII_candidates']],'ASCII_interpretation':'Candidate only. Font124 is not universal and the entry head_font is pre-initialization; no text/nontext/exclusion decision from these values alone.'})
  decoded.append({'selector_hex':f'{selector:02X}','cells':{f'{a:04X}':v for a,v in sorted(nt.items())}})
 unmatched=[x['selector_hex']for x in records if x['observed8025_call_rows']==0];assert unmatched==['0E','14','16','1C','26']
 booth=load(R/'extracted/graphics/booth_001/consumer.json');result=load(R/'extracted/graphics/results_001/consumer.json')
 assert all(0x4649<=x['source_file_offset']<0x47b2 for x in booth['labels']) and result['asset']['source_file_offset']==0x24a0b
 for name in ['extracted/graphics/booth_001/consumer.json','extracted/graphics/results_001/consumer.json']:files[name]=sha(R/name)
 # Known direct source producers, not a census of all possible indexed suppliers.
 assert source[0x1d37e:0x1d388]==bytes.fromhex('a214202580a216202580')
 assert source[0x1d370:0x1d37e]==bytes.fromhex('a579c906901ba9408534a9768535')
 literal1c=[i for i in range(0x10,0x2000f)if source[i:i+2]==bytes.fromhex('a21c')];assert literal1c==[]
 alternatives=[{'selector_hex':'0E','evidence':'extracted/graphics/booth_001/consumer.json','classification':'Already translated booth compressed-literal/header consumer.8025 absence in selected logs is not absent display.','same_asset_bound':'Five literal source offsets are inside catalog0E PRG stream.'},{'selector_hex':'26','evidence':'extracted/graphics/results_001/consumer.json','classification':'Already translated result consumer; specialCHRcopy selector08 refers to globalNT26 source stream.','same_asset_bound':'Actual copied154bytes atsource24A0B and old/currentNT/font/RGB reports; separate entry/index namespace.'},{'selector_hex':'14,16','classification':'Source direct producer pair guarded by RAM79>=6, sets34=64/35=118. No actual8025 sample in selectedlogs.','source_file_offsets':[0x1d37e,0x1d383],'native_CPU_fixed_addresses_hex':['D36E','D373'],'meaning':'Deeper consumer/progression context unresolved; not automatically unused or text-free.'},{'selector_hex':'1C','classification':'Valid source NT pointer/99byte stream exists. No LDXimmediate1C raw motif in sourcePRG, but indexed/indirect suppliers remain unclosed.','meaning':'Raw motif absence is not complete code reachability proof.'}]
 work.mkdir();(work/'source_nt_cells.json').write_text(json.dumps(decoded,indent=2)+'\n','utf-8')
 report={'work':109,'status':'PASS_BOUNDED_NT_SOURCE_CONSUMER_INVENTORY','source_sha256':meta['sha256'],'ROM047_sha256':sha(rom),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'source_nt_streams':20,'source_table_pointers_and_decode_exact':20,'successful_frozen_environments':len(envrefs),'frozen8025_call_rows':sum(map(len,calls.values())),'8025_selectors_observed':20-len(unmatched),'8025_selectors_without_selected_call':unmatched,'alternate_or_unresolved_consumers':alternatives,'records':records,'environments':envrefs,'rejected_environments':rejected,'frozen_selected_files':files,'source1C_adjacent_LDX_immediate_motifs':len(literal1c),'ROM_CSV_changes':False,'new_runtime_or_CPU_execution':False,'global_corpus_closed':False,'human_preservation_approved':False,'limits':['Only20source NTcatalog assets and established physical8025 logged entry. Other direct/queue/copy entrypoints outside this observation denominator.','Entry head_font/CHR mapping is pre-initialization, not rendering-time font proof.','Source/revision-specific offsets; all observed historical artifact hashes verified; no new047 execution claim.','Source fixedD36E/D373 literalproducer static constraints only; RAM79 semantics/reachability and all indirect1C suppliers pending.','No semantic nontext/all-unused claim from ASCII/motifabsence or source decode.','No naturalfullplay/PCM/hardware/finallanguage approval/release claim'],'next_action':'Trace fixedD347 RAM79 producer/callers and guardedD36E/D373 pair to actual stage progression for NT14/16, without forcing targetphase or replaying old2Fbot.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in ['status','source_nt_streams','successful_frozen_environments','frozen8025_call_rows','8025_selectors_observed','8025_selectors_without_selected_call']},ensure_ascii=False))
if __name__=='__main__':main()
