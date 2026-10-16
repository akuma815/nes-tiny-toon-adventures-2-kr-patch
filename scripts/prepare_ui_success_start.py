"""Register five observed castle drafts; freeze prior20-row-draft SSOT."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 path=ROOT/'workspace/translation/text_ja.csv';before=path.read_bytes();assert sha(before)=='979325a40d12762c62d27ec4a70edc33646ae780dedf2e787bbca4c498e67462';backup=ROOT/'backups/translation/text_ja_before_ui_success_start_001.csv';assert not backup.exists();planpath=ROOT/'workspace/translation/ui_success_start_plan_001.json';assert not planpath.exists()
 rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));assert len(rows)==54
 texts=[('MAIN_057AC','언제든 오세요\n',[0,0]),('MAIN_05920','출발!',[1])];profiles=[]
 for i,(id,text,padding) in enumerate(texts):
  row=next(x for x in rows if x['entry_id']==id);assert row['status']=='untranslated' and not row['translation_ko'];row.update(translation_ko=text,status='draft',scene='Observed booth successful exchange and shared ride lower start; recorded points3/gold4 seed branches',speaker='Ticket booth attendant' if i==0 else 'Buster',notes='Observed native booth15 after successful points exchange / shared ride2A start. Preserve FD20 blank line, literal00, control positions and all native reader cycles. Even private font188/190 for lower window; top34 remains native card font. Final human review pending.')
  profiles.append({'entry_id':id,'slot':int(row['reference_ids'],16),'slots':[int(row['reference_ids'],16)],'pointer':int(row['file_offset'])+0x3ff0,'source_file_offset':int(row['file_offset']),'end_exclusive':int(row['end_exclusive']),'source_raw_sha256':row['raw_sha256'],'text':text,'font_bank':188+i*2,'padding':padding,'scene':row['scene'],'speaker':row['speaker']})
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);after=buf.getvalue().encode('utf-8-sig');assert sum(x['status']=='draft' for x in rows)==29;backup.write_bytes(before);path.write_bytes(after)
 plan={'date':'2026-10-05','source_sha256':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d','prior_build':'dialogue_kr_poc_031','prior_ROM_sha256':'8c323f0445d2e35e70404b6dae269c11dbb8c1c3edfe486ecdbd1702c4093a19','backup_CSV_sha256':sha(before),'CSV_sha256':sha(after),'profiles':profiles,'native_punctuation':{'?':0x6b,'!':0x6c,'「':0x6d,'」':0x6e,'4':0x74},'scope':'Observed successful booth farewell15 and shared ride lower start2A; all27 prior drafts retained','review':'Draft; attendant identity and final translation review pending; no release'};planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'draft':29,'untranslated':25,'CSV_sha256':sha(after),'backup_CSV_sha256':sha(before),'profiles':profiles},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
