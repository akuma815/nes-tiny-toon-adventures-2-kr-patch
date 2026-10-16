from pathlib import Path
import collections,copy,csv,hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=R/'workspace/translation/coverage049_145.json';assert not out.exists()
 priorpath=R/'workspace/translation/coverage049_138.json';prior=json.loads(priorpath.read_text('utf-8'))
 catpath=R/'extracted/text/table_20261004_001/text_tokens.json';cat=json.loads(catpath.read_text('utf-8'))
 slots={z['index']:z['unit_id']for z in cat['tables'][0]['slots']};sourceunits={z['entry_id']:z for z in cat['units']}
 units={z['entry_id']:copy.deepcopy(z)for z in prior['units']};assert len(units)==54
 for u in units.values():
  u['prior138_class']=u.pop('coverage_class');u['actual_PRG_reader_evidence']=[];u['completed_NT_evidence']=[];u['direct_visual_reports']=[]
 inputs={priorpath.relative_to(R).as_posix():sha(priorpath),catpath.relative_to(R).as_posix():sha(catpath)}
 for work,name in [(139,'gate'),(140,'gate'),(141,'booth'),(142,'train'),(143,'water'),(144,'intro')]:
  p=R/f'qa/reports/{name}{work}_validation.json';v=json.loads(p.read_text('utf-8'));assert v['work']==work and v['ROM_sha256']==prior['ROM_sha256']and v['CSV_sha256']==prior['CSV_sha256']
  assert v['status'].startswith('PASS_');inputs[p.relative_to(R).as_posix()]=sha(p)
  # Link each report to its already-frozen exact work manifest.
  mp=R/f'manifests/{name}{work}_assets.json';m=json.loads(mp.read_text('utf-8'));assert m['files'][p.relative_to(R).as_posix()]==sha(p);inputs[mp.relative_to(R).as_posix()]=sha(mp)
  for e in v.get('native_init_events',v.get('native_page_init_events',[])):
   slot=int(e['id'],16);u=units[slots[slot]];u['current_initializations'].append({'work':work,'report':p.relative_to(R).as_posix(),'frame':int(e['frame']),'slot_hex':e['id'],'pointer_hex':e['pointer'],'active_font':int(e['active_font'],16),'phase_hex':e['phase'],'scope':'Native9445 initialization; not automatically text completion or byte consumption'})
  for unit,events in v.get('actual_read_units',{}).items():
   offsets={e['source_relative_offset']for e in events};s=sourceunits[unit];size=s['end_exclusive']-s['file_offset']
   units[unit]['actual_PRG_reader_evidence'].append({'work':work,'report':p.relative_to(R).as_posix(),'read_count':len(events),'unique_source_byte_offsets':sorted(offsets),'source_bytes':size,'whole_unit_bytes_observed':offsets==set(range(size)),'active_fonts':sorted({e['active_font']for e in events}),'PCs':sorted({e['reader_PC']for e in events}),'scope':'Actual mapped physical PRG data read; exact value checked against current049. Does not alone assert rendered semantic completion.'})
  for key,t in v.get('complete_NT_targets',{}).items():
   unit=slots[t['slot']];units[unit]['completed_NT_evidence'].append({'work':work,'report':p.relative_to(R).as_posix(),'target':key,'NT':t['NT'],'font':t['font'],'first_verified_snapshot':t['complete_frames'][0],'sample_count':len(t['complete_frames']),'scope':'Native reader model all lines matched actualNT with active font; snapshot timing bounds118 retained'})
  if work in [139,140]:units['MAIN_05824']['completed_NT_evidence'].append({'work':work,'report':p.relative_to(R).as_posix(),'first_verified_snapshot':v['completed_MAIN05824_slot1C_frames'][0],'scope':'Literal14glyph currentROM stream matched actualNT/font185'})
  if work==141:units['MAIN_057AC']['completed_NT_evidence'].append({'work':work,'report':p.relative_to(R).as_posix(),'first_verified_snapshot':v['farewell_completed_NT_frames'][0],'scope':'Native reader2lines matched actualNT/font188'})
  visuals={'gate139':['MAIN_05824','MAIN_05920'],'gate140':['MAIN_0581B','MAIN_05824','MAIN_05920'],'booth141':['MAIN_05782','MAIN_057AC','MAIN_05741'],'train142':['MAIN_05882','MAIN_058FA','MAIN_05833','MAIN_05920','MAIN_05741'],'water143':['MAIN_058A6','MAIN_058FE','MAIN_05833','MAIN_05920','MAIN_05741'],'intro144':[slots[s]for s in range(1,10)]}
  vp=R/f'qa/reports/{name}{work}_visual.json'
  if work==140:vp=R/'qa/reports/gate140_visual_counter.json'
  assert vp.exists();assert m['files'][vp.relative_to(R).as_posix()]==sha(vp);inputs[vp.relative_to(R).as_posix()]=sha(vp)
  for unit in visuals[name+str(work)]:units[unit]['direct_visual_reports'].append(vp.relative_to(R).as_posix())
 for u in units.values():
  u['actual_source_byte_reads']='Linked actual PRG records'if u['actual_PRG_reader_evidence']else 'Not linked in selected actual-reader runs'
  u['current_presence_verified']=bool(u['current_initializations']or u['current_font_snapshots']or u['actual_PRG_reader_evidence'])
  u['actual_reader_full_unit']=any(z['whole_unit_bytes_observed']for z in u['actual_PRG_reader_evidence'])
  u['complete_text']='Linked bounded all-line NT evidence'if u['completed_NT_evidence']else 'No new per-unit all-line NT claim; earlier129/130/133 scene reports remain separate'
 present=[u['entry_id']for u in units.values()if u['current_presence_verified']and u['kind']=='main']
 read=[u['entry_id']for u in units.values()if u['actual_PRG_reader_evidence']]
 missing=[u['entry_id']for u in units.values()if not u['actual_PRG_reader_evidence']]
 assert len(present)==46 and len(read)==30 and len(missing)==24
 assert 'MACRO_061DE'in missing # cart85 new reader target
 csvpath=R/'workspace/translation/text_ja.csv';assert sha(csvpath)==prior['CSV_sha256']
 rompath=R/'build/dialogue_kr_poc_049/TinyToon2_dialogue_kr_poc.nes';assert sha(rompath)==prior['ROM_sha256']
 inputs[csvpath.relative_to(R).as_posix()]=sha(csvpath);inputs[rompath.relative_to(R).as_posix()]=sha(rompath)
 result={'work':145,'status':'PASS_BOUNDED_CURRENT49_SOURCE_EVIDENCE_REFRESH','registered_units':54,'main_unique_units':46,'macro_unique_units':8,'ROM_sha256':prior['ROM_sha256'],'CSV_sha256':prior['CSV_sha256'],'current_main_presence':len(present),'actual_reader_units':len(read),'actual_reader_main':sum(units[z]['kind']=='main'for z in read),'actual_reader_macro':sum(units[z]['kind']=='macro'for z in read),'actual_reader_full_unit':sum(u['actual_reader_full_unit']for u in units.values()),'per_unit_all_line_NT_units':sum(bool(u['completed_NT_evidence'])for u in units.values()),'actual_reader_not_yet_linked':missing,'units':list(units.values()),'verified_inputs':inputs,'prior138_preserved':True,'scope':'Presence, actual source bytes, semantic output completion and direct PNG evidence stay separate.46 main includes one technical variable-only unit;45 drafts not all-game percentage. Macro82 not observed does not imply unused.','next_action':'Run short native cart menu/fee/start reader path on current049 and fresh047 to connect MAIN05867 rule1F/MAIN058F6 title25/MACRO061DE cart85. Winningbot and course-completion stream remains closed.','human_approved':False,'release_eligible':False}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in result.items()if k not in ['units','verified_inputs']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
