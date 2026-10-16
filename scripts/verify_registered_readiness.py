"""Frozen registered table use inventory; deliberately no global corpus assertion."""
import json,csv,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def main():
 p=R/'qa/reports/registered_source_readiness_20261005.json';report=json.loads(p.read_text('utf-8'));rows=list(csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig')));by={x['entry_id']:x for x in rows};rom=(R/'build/dialogue_kr_poc_037/TinyToon2_dialogue_kr_poc.nes').read_bytes();m=json.loads((R/'manifests/source_rom.json').read_text('utf-8'));source=(R/m['path']).read_bytes();assert hashlib.sha256(source).hexdigest()==report['source_sha256']==m['sha256'];assert hashlib.sha256(rom).hexdigest()==report['ROM_sha256'];assert hashlib.sha256((R/'workspace/translation/text_ja.csv').read_bytes()).hexdigest()==report['CSV_sha256'];assert len(rows)==54
 for x in report['macro_units']:
  row=by[x['entry_id']];a,b=int(row['file_offset']),int(row['end_exclusive']);assert source[a:b].hex()==x['source_definition_hex'] and rom[a+0x20000:b+0x20000].hex()==x['current_definition_hex']
  for c in x['registered_consumers']:assert by[c['entry_id']]['status']=='draft' and by[c['entry_id']]['translation_ko']==c['translation'];assert source[int(by[c['entry_id']]['file_offset'])+c['source_position']] in x['macro_codes']
  if not x['registered_consumers']:assert x['entry_id']=='MACRO_061C9' and source[a:b]==rom[a+0x20000:b+0x20000]
 for x in report['runtime_evidence']:assert hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256']
 print(json.dumps({'status':'PASS','registered_units':54,'drafts':45,'remaining_units_policy':'one F9 variable, seven contextual macro definitions, one macro unused only in registered tables','ROM_SSOT_changes':0,'global_corpus_complete':False},indent=2))
if __name__=='__main__':main()
