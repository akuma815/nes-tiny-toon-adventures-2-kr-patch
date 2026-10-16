"""Reconcile bounded localization populations and open claims; no runtime or ROM writes."""
from pathlib import Path
import csv,hashlib,json,collections
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((R/n).read_text('utf-8'))
def main():
 out=R/'qa/reports/scope108_reconciliation.json';assert not out.exists()
 csvpath=R/'workspace/translation/text_ja.csv';rows=list(csv.DictReader(csvpath.open(encoding='utf-8-sig')));by={x['entry_id']:x for x in rows};assert len(rows)==54 and len(by)==54
 assert sha(csvpath)=='ac22c5842e4f8d1600925e0837508c82f198157553031bd7cc3371fb6e4cf556'
 meta=load('manifests/source_rom.json');source=(R/meta['path']).read_bytes();assert sha(R/meta['path'])==meta['sha256']
 rompath=R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes';assert sha(rompath)=='82ccec59ea23e899d0bcdb22123d67cc935a13305a843ca3f1f42fb24dc80c10';rom=rompath.read_bytes()
 review=load('workspace/review/translation047_20261005/review_records.json');assert review['ROM_sha256']==sha(rompath) and review['SSOT_sha256']==sha(csvpath) and review['human_review_complete']==False
 assert {x['entry_id']:x['translation_ko']for x in review['units']}=={x['entry_id']:x['translation_ko']for x in rows}
 drafts=[x for x in rows if x['status']=='draft'];assert len(drafts)==45 and all(x['translation_ko']for x in drafts)
 technical=[x for x in rows if x['status']!='draft'];assert len(technical)==9
 macro_old=load('qa/reports/registered_source_readiness_20261005.json');macro_records=[]
 for x in macro_old['macro_units']:
  row=by[x['entry_id']];a,b=int(row['file_offset']),int(row['end_exclusive']);assert source[a:b].hex()==x['source_definition_hex'] and rom[a+0x20000:b+0x20000].hex()==x['current_definition_hex']
  for c in x['registered_consumers']:assert by[c['entry_id']]['status']=='draft'
  macro_records.append({'entry_id':x['entry_id'],'macro_codes_hex':[f'{v:02X}'for v in x['macro_codes']],'source_raw_preserved':source[a:b]==rom[a+0x20000:b+0x20000],'registered_consumer_count':len(x['registered_consumers']),'registered_consumer_entry_ids':sorted({c['entry_id']for c in x['registered_consumers']}),'interpretation':'Context-specific glyph supply in translated main streams'if x['registered_consumers']else'No consumer in established registered main streams; not globally unused'})
 assert len(macro_records)==8 and sum(x['registered_consumer_count']==0 for x in macro_records)==1
 graphics=review['graphics'];assert len(graphics)==33 and len({x['id']for x in graphics})==33 and all(x['status']=='draft'for x in graphics)
 for x in graphics:
  if 'plan'in x:assert sha(R/x['plan'])==x['plan_sha256']
 credits=load('workspace/translation/credits_plan_001.json');assert len(credits['profiles'])==3 and all(by[x['entry_id']]['status']=='draft'for x in credits['profiles'])
 catalog=load('work/graphics_population_001/native_NT_catalog.json');assets=catalog['assets'];assert len(assets)==20 and [x['selector']for x in assets]==list(range(0,0x28,2))
 nt=[]
 for x in assets:
  a=x['source_file_offset'];n=x['encoded_length'];raw=source[a:a+n];assert hashlib.sha256(raw).hexdigest()==x['encoded_sha256']
  nt.append({'selector_hex':f"{x['selector']:02X}",'selector_decimal':x['selector'],'storage':x['storage'],'source_file_offset':a,'encoded_length':n,'source_hash_verified':True,'encoded_sha256':x['encoded_sha256'],'decoded_cells_recorded':x['decoded_cells'],'ASCII_candidate_only':True,'consumer_context_reconciliation':'pending','font124_must_not_be_assumed':True})
 reports=['qa/reports/context105_review.json','qa/reports/context106_closeout.json','qa/reports/context107_validation.json','qa/reports/gate094_validation.json','qa/reports/state095_validation.json','qa/reports/candidate099_bank_nt.json','qa/reports/candidate100_runtime.json','qa/reports/pause101_supply_bounds.json','qa/reports/animation102_bank36.json','qa/reports/latch103_supply.json','qa/reports/pow096_static.json','qa/reports/cart089_validation.json','qa/reports/engine_closure052.json']
 evidence=[]
 for n in reports:
  p=R/n
  if not p.exists():continue
  d=load(n);evidence.append({'path':n,'sha256':sha(p),'status':d['status'],'work':d.get('work'),'artifact_sha256':d.get('ROM047_sha256',d.get('ROM_sha256',d.get('ROM_sha256',d.get('ROM_sha256',d.get('ROM047_sha256',d.get('protected_hashes',{}).get('build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes'))))))),'record_policy':'Historical report retains its own exact artifact/intervention scope; statusPASS alone does not prove wholeplay or release.'})
 issues=[
 {'id':'SCOPE_GLOBAL','status':'open_technical','criterion':'All text/graphics consumers of declared game scope classified, with evidence for exclusions.','known':'54registered units and33graphics review records are bounded populations;20NTstream catalog is also bounded.','next_discriminating_work':'Connect20 native NT source entries to frozen actual consumer paths/fonts; do not labelASCII candidates as text without actual glyph context.'},
 {'id':'HOWTO116117','status':'open_consumer','criterion':'Connect actual label90..96 to visible consumer or obtain supported source exclusion/human scope decision.','known':'Current047 bank116 is active for decoration; candidate label observed0 on one menu route.99/100 prove positive control, not globalunused.','reports':['candidate099_bank_nt.json','candidate100_runtime.json']},
 {'id':'PAUSE120121','status':'open_consumer','criterion':'Connect another actual consumer or close all applicable producer population; sampled pause absence is insufficient.','known':'49 actual pause does not draw label;101..103 bound immediate motifs/animation/IRQ latch supply only.','reports':['pause101_supply_bounds.json','animation102_bank36.json','latch103_supply.json']},
 {'id':'POW61','status':'open_consumer','criterion':'Reach actualPOW pose producer/OAM/CHR/PPU and judge its semantic role.','known':'7valid static descriptors;61flag positivecontrol observed97; cannot use flag or bank selection asPOW visibility.','reports':['pow096_static.json']},
 {'id':'NATURAL_FULLPLAY','status':'open_technical','criterion':'Complete supported game progression without state/currency/health/PC/ROM intervention and retain actual text/interactions.','known':'Cart first segment cleared;87/89 second2F timeout. Seeded entry, rooted ending and seeded result screens are not fullplay.','next_discriminating_work':'A new playthrough method needs distinct native/player evidence; do not resume same automated2F attempts without new discriminating data.'},
 {'id':'HUMAN_LANGUAGE_GRAPHICS','status':'pending_human','criterion':'Final wording/voice/names/title/graphics judged by user against actual evidence and exact047baseline.','known':'45drafts/33graphics remainpending; no approval inferred from resume or syntheticJSON downloads.','options':[{'option':'Review current drafts','effort':'Human reading/image review using existing047kits','gain':'Can settle wording/name/artwork choices','risk':'May need a new build and affected-route QA after edits'},{'option':'Continue technical corpus/consumer work','effort':'Bounded static evidence reconciliation; runtime only for new questions','gain':'Can reduce missing-consumer uncertainty','risk':'Does not replace language/art direction or naturalfullplay'}]},
 {'id':'TARGET_SUPPORT_AUDIO','status':'not_run','criterion':'Perform exact target-environment and listening checks before corresponding support claims.','known':'Only privateMesen runtime; hardware and PCM listening remain unperformed.'},
 {'id':'RELEASE_CAFE','status':'withheld_incomplete','criterion':'Technical scope + human quality + applicableplay checks close on one artifact, then ROMfree release and accurateCafearticle.','known':'047review patch has realapply evidence; it is not finalrelease. Cafe finalarticle waits until all workcomplete; no publication permission.'}]
 result={'work':108,'status':'PASS_BOUNDED_SCOPE_RECONCILIATION','source_sha256':meta['sha256'],'ROM047_sha256':sha(rompath),'CSV_sha256':sha(csvpath),'populations':{'registered_unique_source_units':54,'registered_unique_main':46,'registered_pointer_slots':48,'draft_main_units':45,'technical_variable_F9':1,'unique_macros':8,'contextual_macros':7,'macro82_no_registered_consumer':1,'review_graphics_records':33,'native_NT_catalog_entries':20,'native_NT_selectors_hex':'00..26 even values','whole_game_completion_percent':None},'technical_units':[{'entry_id':x['entry_id'],'source_status_preserved':x['status']}for x in technical],'macro_use_records':macro_records,'graphics_review_inventory':graphics,'credits_policy':'3credits source paragraphs are already inside45drafts; native staff/publisher/legal names are preserved by recordedplan. Do not count them as extra33graphics or assume allEnglish retained.','native_NT_source_catalog':nt,'evidence_reports':evidence,'context_overrides':load('workspace/translation/scene_context_105.json')['context_overrides'],'open_conditions':issues,'product_closure':False,'global_corpus_closed':False,'natural_fullplay_passed':False,'human_review_complete':False,'release_eligible':False,'ROM_CSV_edits':False,'new_emulator_or_CPU_runs':False,'next_action':'Analyze20 native NT streams00..26hex against frozen actual NT-call/font evidence, beginning with unmatched selectors; retain candidate-vs-text distinction.'}
 out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'status':result['status'],'populations':result['populations'],'open_conditions':len(issues),'release_eligible':False},ensure_ascii=False))
if __name__=='__main__':main()
