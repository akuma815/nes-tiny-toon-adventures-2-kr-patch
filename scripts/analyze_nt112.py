"""Bound direct native NT decoder suppliers, distinguish shared RAM counters."""
from pathlib import Path
import json,hashlib,csv
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'qa/reports/nt112_supplier_bounds.json';assert not out.exists()
 source=next((R/'original/rom').glob('*.nes'));current=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'
 s=source.read_bytes();c=current.read_bytes()
 assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'and sha(current)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10'
 def occurrences(hexbytes):
  b=bytes.fromhex(hexbytes);return[i for i in range(0x10,0x20010-len(b)+1)if s[i:i+len(b)]==b]
 expected={0x4019:0x22,0x401e:0x24,0x1cc19:2,0x1cc28:None,0x1ce65:0x1e,0x1cecd:0x20,0x1d380:0x14,0x1d385:0x16,0x1f8fc:0x26,0x1f992:None}
 assert occurrences('202580')==list(expected)and occurrences('4c2580')==[]
 callsites=[]
 for a,index in expected.items():
  assert s[a-3:a+3]==c[a+0x20000-3:a+0x20000+3]
  if index is not None:assert s[a-2:a]==bytes([0xa2,index])
  else:assert s[a-3:a]==bytes.fromhex('aed006'if a==0x1cc28 else'aee506')
  callsites.append({'source_file_offset':a,'current047_file_offset':a+0x20000,'CPU':f'{(0x8000+a-0x4010)if a<0x1c010 else(0xc000+a-0x1c010):04X}','selector':index,'supplier':'LDX immediate'if index is not None else('CC18 shared entry via CC10/CC02'if a==0x1cc28 else'F97F LDX06E5 via F97A')})
 # Five direct CC10 calls: four adjacent guarded stores, one intro helper with four bounded entries.
 cc10=occurrences('2010cc');assert cc10==[0x4f61,0x5b3c,0x5cb2,0x5e74,0x6014]
 adjacent={0x5b3c:0x0c,0x5cb2:0x0e,0x5e74:0x10,0x6014:0x12}
 for a,v in adjacent.items():assert s[a-5:a]==bytes([0xa9,v,0x8d,0xd0,6])
 assert s[0x4f59:0x4f61]==bytes.fromhex('a9068dd0062088f9')
 intro_jumps=occurrences('4c4b8f');assert intro_jumps==[0x4fff,0x507b,0x5126]
 for a,v in zip(intro_jumps,[8,10,4]):assert s[a-2:a]==bytes([0xa9,v])
 assert occurrences('204b8f')==[]and occurrences('2018cc')==[]and occurrences('4c18cc')==[]
 # The same RAM06D0 is a frame counter in other intro handlers. That does not invoke CC10.
 assert s[0x50c3:0x50cc]==bytes.fromhex('eed006add00620e193')
 assert s[0x50e2:0x50f0]==bytes.fromhex('eed006add006c936d0d6a9608558')
 f97a=occurrences('207af9');assert f97a==[0x13c9c,0x13ca4]
 for a,v in zip(f97a,[0x18,0x1a]):assert s[a-5:a]==bytes([0xa9,v,0x8d,0xe5,6])
 assert occurrences('4c7af9')==[]and occurrences('207ff9')==[]and occurrences('4c7ff9')==[]
 clear=occurrences('202380');assert clear==[0x4014,0x1cc0a]
 assert s[0x4033:0x4037]==bytes.fromhex('a200e01e')
 files={};observed=set()
 old=R/'qa/reports/nt109_consumers.json';j=json.loads(old.read_text('utf-8'));files[old.relative_to(R).as_posix()]=sha(old)
 observed|={int(x['selector_hex'],16)for x in j['records']if x['observed8025_call_rows']}
 for n in ['source','current047']:
  p=R/'qa/dialogue'/f'castle111_{n}';e=p/'environment.json';env=json.loads(e.read_text('utf-8'));log=p/'castle111_native.csv'
  assert sha(log)==env['files'][log.name]and env['exit_code']==0
  for x in csv.DictReader(log.open(encoding='utf-8')):
   if x['kind']=='NT_entry':observed.add(int(x['cpu_x'],16))
  for a in [log,e]:files[a.relative_to(R).as_posix()]=sha(a)
 assert sorted(set(range(0,0x28,2))-observed)==[0x0e,0x1c,0x26]
 bounds=sorted({0,2,4,6,8,10,12,14,16,18,20,22,24,26,30,32,34,36,38})
 assert len(bounds)==19 and 0x1c not in bounds
 report={'work':112,'status':'PASS_BOUNDED_DIRECT_NT_SUPPLIER_ANALYSIS','source_sha256':sha(source),'ROM047_sha256':sha(current),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'direct_JSR8025_sites':callsites,'direct_JSR8025_site_bytes_current_exact':10,'direct_JMP8025_motifs':0,'clear8023_direct_sites':clear,'CC10_direct_calls':cc10,'CC10_adjacent_guarded_selectors_hex':['0C','0E','10','12'],'intro_8F4B_named_selectors_hex':['04','06','08','0A'],'CC18_alternate_literal_entry_selector_hex':'04','F97A_direct_calls':f97a,'F97A_adjacent_guarded_selectors_hex':['18','1A'],'bounded_named_supplier_selector_set_hex':[f'{i:02X}'for i in bounds],'observed8025_selectors_hex':[f'{i:02X}'for i in sorted(observed)],'source20_catalog_connection_summary':{'8025_observed_selectors':17,'alternate_previously_verified':['0E booth literal','26 result specialCHRcopy'],'unconnected':['1C']},'NT1C':{'source_file_offset':0x4c09,'encoded_length':99,'native_pointer_CPU':'8BF9','classification':'No supplied1C in bounded named direct paths. Still not a global unused or product-scope exclusion decision.','raw_pointer_word_source_positions':occurrences('f98b'),'indirect_or_alternative_entry_closure':False},'shared_RAM_counter_warning':'06D0 INC/LDA atnative90B3/90D2 belongs other intro handlers; a sampled counter value1C alone is not a decoder selector invocation. CC10 bounded named callers overwrite it or intro8F4B before loading X.','ROM_CSV_changes':False,'new_CPU_or_emulator_or_scene':False,'global_corpus_closed':False,'release_eligible':False,'frozen_selected_files':files,'limits':['Exact bytes and adjacent named caller paths, not exhaustive reachable CFG/interrupt/indexed state writers. Raw pattern scans alone do not classify arbitrary bytes as instructions.','No blanket exclusion from unobserved1C, no finalhuman preservation approval.','Two successful111diagnostic NT logs supplement frozen109catalog; not naturalcastle traversal or fullplay.'],'next_action':'Decode the native8113 separate uncompressed command table and declared call-site inputs, catalog STAGE SELECT and palette-only aliases apart from registered dialogue/NT20; determine any new actual text consumer.'}
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:report[k]for k in ['status','bounded_named_supplier_selector_set_hex','source20_catalog_connection_summary']},ensure_ascii=False))
if __name__=='__main__':main()
