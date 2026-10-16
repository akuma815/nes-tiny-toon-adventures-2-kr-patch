"""Freeze prior SSOT and register two observed train/water home selection drafts."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 path=ROOT/'workspace/translation/text_ja.csv';before=path.read_bytes();assert sha(before)=='1528501efb8983ff77b9514fd859a7a7cca91eb23eb5ca752132cd645c3fbcd6'
 backup=ROOT/'backups/translation/text_ja_before_ui_rides_001.csv';assert not backup.exists();backup.write_bytes(before)
 rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));assert len(rows)==54
 texts=[('MAIN_05753','기차','home train selection, observed consumers022_train1350','Buster'),('MAIN_05756','급류타기','home water ride selection, observed consumers022_water1200','Buster')]
 profiles=[]
 for i,(id,text,scene,speaker) in enumerate(texts):
  row=next(r for r in rows if r['entry_id']==id);assert row['status']=='untranslated' and not row['translation_ko']
  row.update(translation_ko=text,status='draft',scene=scene,speaker=speaker)
  note='Observed controller routes menu_train/water_001; source controls and macro83 zero retained; page-specific glyphs; final human review pending.'
  if i<4:note+=' Selection displays place/ride name only; source explanatory suffix is omitted to retain macro83 leading00 and natural Korean name spacing. Proper names are drafts.'
  row['notes']=note
  slot=int(row['reference_ids'],16);profiles.append({'entry_id':id,'slot':slot,'pointer':int(row['file_offset'],0)+0x3ff0 if row['file_offset'].startswith('0x') else int(row['file_offset'])+0x3ff0,'source_file_offset':int(row['file_offset'],0) if row['file_offset'].startswith('0x') else int(row['file_offset']),'end_exclusive':int(row['end_exclusive']),'source_raw_sha256':row['raw_sha256'],'text':text,'font_bank':166+i*2,'padding':[0]*len(text.split('\n')),'scene':scene,'speaker':speaker})
 stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows);after=stream.getvalue().encode('utf-8-sig');path.write_bytes(after)
 plan={'date':'2026-10-05','source_sha256':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d','prior_build':'dialogue_kr_poc_023','prior_ROM_sha256':'1f4341ef464146e25982e8bf25d01ff504be85a184b905240a69179d3c79e410','backup_CSV_sha256':sha(before),'CSV_sha256':sha(after),'profiles':profiles,'native_punctuation':{'?':0x6b,'!':0x6c,'「':0x6d,'」':0x6e},'scope':'Two observed home train/water name drafts only; source macros remain untranslated SSOT entries and other consumers keep Japanese passthrough','review':'Draft; final proper-name/service-tone review pending; no release'}
 p=ROOT/'workspace/translation/ui_rides_plan_001.json';assert not p.exists();p.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'draft':20,'untranslated':34,'CSV_sha256':sha(after),'backup_CSV_sha256':sha(before),'profiles':profiles},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
