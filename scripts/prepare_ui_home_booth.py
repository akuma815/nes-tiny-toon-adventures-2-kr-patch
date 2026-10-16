"""Freeze prior SSOT and register eight observed home/booth Korean drafts."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 path=ROOT/'workspace/translation/text_ja.csv';before=path.read_bytes();assert sha(before)=='76bcc0d985c41dff6ce19cf0dd1a8a02e58bbb6814ca0b2f26e9e8239b9e8c48'
 backup=ROOT/'backups/translation/text_ja_before_ui_home_booth_001.csv';assert not backup.exists();backup.write_bytes(before)
 rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));assert len(rows)==54
 texts=[('MAIN_0574D','롤러코스터','home selection, roller coaster','Buster'),('MAIN_05750','쇼킹카트','home selection, Shocking Cart','Buster'),('MAIN_05759','수수께끼의 성','home selection, mystery castle','Buster'),('MAIN_05762','매표소','home selection, ticket booth','Buster'),('MAIN_05769','나중에 또 보자!\n','leaving home for ticket booth/ride','Buster'),('MAIN_05777','매표소에 어서 오세요','ticket booth welcome','Babs'),('MAIN_05782','포인트를 티켓으로\n바꿔 드릴게요','ticket booth exchange intent','Babs'),('MAIN_05794','아쉽지만\n포인트가 부족해요','ticket booth insufficient points','Babs')]
 profiles=[]
 for i,(id,text,scene,speaker) in enumerate(texts):
  row=next(r for r in rows if r['entry_id']==id);assert row['status']=='untranslated' and not row['translation_ko']
  row.update(translation_ko=text,status='draft',scene=scene,speaker=speaker)
  note='Observed controller routes menu_tour/ticket_001; source controls and macro83 zero retained; page-specific glyphs; final human review pending.'
  if i<4:note+=' Selection displays place/ride name only; source explanatory suffix is omitted to retain macro83 leading00 and natural Korean name spacing. Proper names are drafts.'
  row['notes']=note
  slot=int(row['reference_ids'],16);profiles.append({'entry_id':id,'slot':slot,'pointer':int(row['file_offset'],0)+0x3ff0 if row['file_offset'].startswith('0x') else int(row['file_offset'])+0x3ff0,'source_file_offset':int(row['file_offset'],0) if row['file_offset'].startswith('0x') else int(row['file_offset']),'end_exclusive':int(row['end_exclusive']),'source_raw_sha256':row['raw_sha256'],'text':text,'font_bank':150+i*2,'padding':[0]*len(text.split('\n')),'scene':scene,'speaker':speaker})
 stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows);after=stream.getvalue().encode('utf-8-sig');path.write_bytes(after)
 plan={'date':'2026-10-05','source_sha256':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d','prior_build':'dialogue_kr_poc_019','prior_ROM_sha256':'1243fcf1450c1a46df55edd63d6528565cb49204b5f53d24dd731183dbcb7c5d','backup_CSV_sha256':sha(before),'CSV_sha256':sha(after),'profiles':profiles,'native_punctuation':{'?':0x6b,'!':0x6c,'「':0x6d,'」':0x6e},'scope':'Eight observed home/booth drafts only; source macros remain untranslated SSOT entries and other consumers keep Japanese passthrough','review':'Draft; final proper-name/service-tone review pending; no release'}
 p=ROOT/'workspace/translation/ui_home_booth_plan_001.json';assert not p.exists();p.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'draft':18,'untranslated':36,'CSV_sha256':sha(after),'backup_CSV_sha256':sha(before),'profiles':profiles},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
