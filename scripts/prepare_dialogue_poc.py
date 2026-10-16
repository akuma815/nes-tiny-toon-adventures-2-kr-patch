"""Resolve the observed kana font and prepare a single draft translation, preserving raw data."""
import csv,hashlib,json,unicodedata
from pathlib import Path
from extract_text import GLYPHS
ROOT=Path(__file__).resolve().parents[1]
KATAKANA='ェアイウエォカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンャュョッ'
TEXT='여기는 모두가 아는\n애크미 에이커스'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode_view(unit,mapping):
    parts=[]
    for t in unit['tokens']:
        b=int(t['raw_hex'].split()[0],16)
        if t['name']=='tile':parts.append(mapping.get(b,t['token']))
        elif t['name']=='spaces':parts.append(' '*int(t['raw_hex'].split()[1],16))
        elif t['name']=='newline':parts.append('\n')
        elif t['name']!='end':parts.append(t['token'])
    return unicodedata.normalize('NFC',''.join(parts))
def main():
    assert len(KATAKANA)==0x66-0x33
    mapping={**GLYPHS,**{0x33+i:c for i,c in enumerate(KATAKANA)}}
    source=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    payload=json.loads((ROOT/'extracted/text/table_20261004_001/text_tokens.json').read_text(encoding='utf-8'))
    used={int(t['raw_hex'],16) for u in payload['units'] for t in u['tokens'] if t['name']=='tile'}
    unknown=sorted(used-set(mapping))
    kana_unknown=sorted({int(t['raw_hex'],16) for u in payload['units'] if u['font_profile']=='kana_partial' for t in u['tokens'] if t['name']=='tile'}-set(mapping))
    assert not kana_unknown
    out=ROOT/'extracted/text/kana_mapping_001';out.mkdir(parents=True,exist_ok=False)
    units=[{**u,'resolved_view':decode_view(u,mapping) if u['font_profile']=='kana_partial' else u['original_view']} for u in payload['units']]
    (out/'resolved_units.json').write_text(json.dumps(units,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'workspace/tables/kana_codes.json').write_text(json.dumps({'source_sha256':source['sha256'],'font_file_start':0x36810,'font_bytes':2048,'glyphs':{f'{k:02X}':v for k,v in sorted(mapping.items())},'evidence':'extracted/chr/survey_20261004_001/japanese_glyph_codes.png; native tiles and first paragraph screenshot; work/dialogue_font/katakana_detail.png','kana_used_unmapped_codes':kana_unknown,'all_registered_used_unmapped_codes':unknown,'scope':'Observed kana font only; credit profile not established; unused symbol tiles not assigned a guessed meaning'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    csv_path=ROOT/'workspace/translation/text_ja.csv';before=csv_path.read_bytes()
    backup=ROOT/'backups/translation/text_ja_before_dialogue_001.csv';backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(before)
    rows=list(csv.DictReader(csv_path.open(encoding='utf-8-sig',newline='')));fields=list(rows[0]);original_raw={r['entry_id']:r['raw_hex'] for r in rows}
    by_id={u['entry_id']:u for u in units}
    for row in rows:
        u=by_id[row['entry_id']]
        assert row['raw_hex']==u['raw_hex'] and row['source_tokens']==u['source_tokens']
        if row['font_profile']=='kana_partial':
            row['original_view']=u['resolved_view'];row['font_profile']='kana_verified_observed'
        if row['entry_id']=='MAIN_05609':
            assert row['status']=='untranslated' and not row['translation_ko']
            assert row['original_view']=='      ここはみんながしってる\n       アクミ・エイカーズ'
            row.update(scene='intro_acme_acres',speaker='narrator',translation_ko=TEXT,status='draft',notes='Single-paragraph development PoC; faithful draft, human final review pending. Source layout uses origin column4, rows15/17. Credit profile and full-game glyph population unresolved.')
    assert {r['entry_id']:r['raw_hex'] for r in rows}==original_raw
    with csv_path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    report={'source_sha256':source['sha256'],'original_csv_sha256':hashlib.sha256(before).hexdigest(),'current_csv_sha256':sha(csv_path),'rows':len(rows),'draft_rows':1,'unchanged_raw_tokens_and_bytes':True,'kana_used_unmapped_codes':kana_unknown,'all_registered_used_unmapped_codes':unknown,'scope':'Kana mapping and one draft; credits kept unresolved; not approved distribution input'}
    (out/'preparation_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
