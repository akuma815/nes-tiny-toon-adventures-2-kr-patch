"""Selected, individually reviewed work125 sentence; single SSOT edit and backup."""
from pathlib import Path
import csv, hashlib, io, json
R=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    csvpath=R/'workspace/translation/text_ja.csv'
    backup=R/'backups/translation/text_ja_before_shortage126.csv'
    planpath=R/'workspace/translation/shortage_editorial_plan_126.json'
    assert not backup.exists() and not planpath.exists()
    before=csvpath.read_bytes();review=json.loads((R/'workspace/translation/prose_review_125.json').read_text('utf-8'))
    assert sha(before)==review['CSV_sha256']
    selected=review['single_selected_revision'];assert selected['entry_id']=='MAIN_0590C'
    rows=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));fieldnames=list(rows[0])
    row=next(r for r in rows if r['entry_id']==selected['entry_id'])
    assert row['status']=='draft' and row['translation_ko']==selected['translation_before']
    row['translation_ko']=selected['translation_candidate']
    row['notes']+=' | 작업126: 원문의 티켓 부족 상태를 직접 안내하도록 단일 초안 수정. 전용font226/227, macro88/제어/두 행 유지. 최종 사람 승인 아님.'
    s=io.StringIO(newline='');writer=csv.DictWriter(s,fieldnames=fieldnames,lineterminator='\r\n');writer.writeheader();writer.writerows(rows)
    after=(('\ufeff' if before.startswith(b'\xef\xbb\xbf') else '')+s.getvalue()).encode('utf-8')
    old=list(csv.DictReader(io.StringIO(before.decode('utf-8-sig'))));new=list(csv.DictReader(io.StringIO(after.decode('utf-8-sig'))))
    edits=[(x['entry_id'],k) for x,y in zip(old,new) for k in fieldnames if x[k]!=y[k]]
    assert edits==[('MAIN_0590C','translation_ko'),('MAIN_0590C','notes')]
    nativeplan=json.loads((R/'workspace/translation/ui_stage_lower_plan_001.json').read_text('utf-8'))
    p=next(p for p in nativeplan['profiles'] if p['entry_id']==selected['entry_id']).copy()
    p.update(text=row['translation_ko'],font_bank=226)
    rom=(R/'build/dialogue_kr_poc_047/TinyToon2_dialogue_kr_poc.nes').read_bytes()
    assert sha(rom)==review['ROM047_sha256'] and not any(rom[0x78810:0x79010])
    plan={'work':126,'source_sha256':review['source_sha256'],'prior_build':'dialogue_kr_poc_047','prior_ROM_sha256':sha(rom),'backup_CSV':backup.relative_to(R).as_posix(),'backup_CSV_sha256':sha(before),'CSV_sha256':sha(after),'profile':p,'native_punctuation':nativeplan['native_punctuation'],'manual_review': 'workspace/translation/prose_review_125.json','manual_review_sha256':sha((R/'workspace/translation/prose_review_125.json').read_bytes()),'reserved_font_range':[0x78810,0x79010],'scope':'One ordinary ride shortage draft. Private226/227 even lower-only tag, no shared macro/font change. Human approval false.'}
    backup.write_bytes(before);csvpath.write_bytes(after);planpath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps({'CSV_before':sha(before),'CSV_after':sha(after),'edited_fields':edits,'font_banks':[226,227]},ensure_ascii=False))
if __name__=='__main__':main()
