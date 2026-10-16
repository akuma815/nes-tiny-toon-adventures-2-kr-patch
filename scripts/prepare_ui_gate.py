"""Register five observed castle drafts; freeze prior20-row-draft SSOT."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 path=ROOT/'workspace/translation/text_ja.csv';before=path.read_bytes();assert sha(before)=='d57b739152817572a0f1833572ca7991eb7684a77a1c00a2ef44931ee2c228fe';backup=ROOT/'backups/translation/text_ja_before_ui_gate_001.csv';assert not backup.exists();planpath=ROOT/'workspace/translation/ui_gate_plan_001.json';assert not planpath.exists()
 rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));assert len(rows)==54
 texts=[('MAIN_057B8','어서 오세요',[0]),('MAIN_057C1','입장 조건은 골드 티켓 4장\n있으면 입장할 수 있어요',[1,1]),('MAIN_057E5','아쉽지만 티켓이 부족해요',[2]),('MAIN_057F7','다시 오세요\n',[0,0]),('MAIN_0581B','갖고 계세요?',[0])];profiles=[]
 for i,(id,text,padding) in enumerate(texts):
  row=next(x for x in rows if x['entry_id']==id);assert row['status']=='untranslated' and not row['translation_ko'];row.update(translation_ko=text,status='draft',scene='Castle gate native insufficient-gold/normal-ticket route; menu_castle_001',speaker='Castle gate attendant; identity unresolved',notes='Observed native slots16/17/18/19/1B with controller-only route. Preserve controls/macros/literal00/read timing. Odd private font supplies top34 after native clear; Japanese1A fallback171 retained. Fixed numeral4 uses explicit native bitmap. Final human review pending.')
  profiles.append({'entry_id':id,'slot':int(row['reference_ids'],16),'pointer':int(row['file_offset'])+0x3ff0,'source_file_offset':int(row['file_offset']),'end_exclusive':int(row['end_exclusive']),'source_raw_sha256':row['raw_sha256'],'text':text,'font_bank':173+i*2,'padding':padding,'scene':row['scene'],'speaker':row['speaker']})
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);after=buf.getvalue().encode('utf-8-sig');assert sum(x['status']=='draft' for x in rows)==25;backup.write_bytes(before);path.write_bytes(after)
 plan={'date':'2026-10-05','source_sha256':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d','prior_build':'dialogue_kr_poc_027','prior_ROM_sha256':'d9db24539a021723c42dd40c9b65d45bb59878226cc10349a862b5c06ffcd513','backup_CSV_sha256':sha(before),'CSV_sha256':sha(after),'profiles':profiles,'native_punctuation':{'?':0x6b,'!':0x6c,'「':0x6d,'」':0x6e,'4':0x74},'scope':'Five observed castle drafts; variable normal-price1A and unobserved entry1C remain Japanese, macro SSOT unchanged','review':'Draft; attendant identity and final translation review pending; no release'};planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'draft':25,'untranslated':29,'CSV_sha256':sha(after),'backup_CSV_sha256':sha(before),'profiles':profiles},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
