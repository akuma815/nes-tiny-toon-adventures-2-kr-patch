"""Register five observed castle drafts; freeze prior20-row-draft SSOT."""
import csv,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 path=ROOT/'workspace/translation/text_ja.csv';before=path.read_bytes();assert sha(before)=='2a5c062710daf43969146b699c3269409666230ee2d3bbf72609b698567ee8b8';backup=ROOT/'backups/translation/text_ja_before_ui_gate_variable_001.csv';assert not backup.exists();planpath=ROOT/'workspace/translation/ui_gate_variable_plan_001.json';assert not planpath.exists()
 rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));assert len(rows)==54
 texts=[('MAIN_05805','일반 티켓 {variable_FA}장으로\n입장 가능해요',[3,1]),('MAIN_05824','어서 들어오세요',[0])];profiles=[]
 for i,(id,text,padding) in enumerate(texts):
  row=next(x for x in rows if x['entry_id']==id);assert row['status']=='untranslated' and not row['translation_ko'];row.update(translation_ko=text,status='draft',scene='Castle gate price and admission; native controller route and explicit gold4/normal50/49 branch seeds',speaker='Castle gate attendant; identity unresolved',notes='Observed price1A/alias2C and admission1C. Preserve variable_FA token and native numeral generation, all macros/controls/literal00/per-call cycles. Odd font183/185 also supplies top34. Final human review pending.')
  profiles.append({'entry_id':id,'slot':int(row['reference_ids'].split(',')[0],16),'slots':[int(x,16) for x in row['reference_ids'].split(',')],'ride':5,'pointer':int(row['file_offset'])+0x3ff0,'source_file_offset':int(row['file_offset']),'end_exclusive':int(row['end_exclusive']),'source_raw_sha256':row['raw_sha256'],'text':text,'font_bank':183+i*2,'padding':padding,'scene':row['scene'],'speaker':row['speaker']})
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows);after=buf.getvalue().encode('utf-8-sig');assert sum(x['status']=='draft' for x in rows)==27;backup.write_bytes(before);path.write_bytes(after)
 plan={'date':'2026-10-05','source_sha256':'f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d','prior_build':'dialogue_kr_poc_028','prior_ROM_sha256':'c39750936c24f354d199c5c0cb17756979deb80b546ccfd2b5db541160d2ae1e','backup_CSV_sha256':sha(before),'CSV_sha256':sha(after),'profiles':profiles,'native_punctuation':{'?':0x6b,'!':0x6c,'「':0x6d,'」':0x6e,'4':0x74},'scope':'Two observed castle drafts, FA numeric variable and alias2C retained; other25 drafts unchanged; development only','review':'Draft; attendant identity and final translation review pending; no release'};planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'draft':27,'untranslated':27,'CSV_sha256':sha(after),'backup_CSV_sha256':sha(before),'profiles':profiles},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
