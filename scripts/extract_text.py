"""Reversibly extract the observed bank-2 table and bank-3 macros. No ROM writes.

The table population is not a claim that no other renderer exists.
Raw tokens are authoritative; glyph views deliberately retain unresolved tiles.
"""
import argparse, csv, hashlib, json, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KANA=' あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんゃゅょっ'
GLYPHS={i:c for i,c in enumerate(KANA)}
GLYPHS.update({0x66:'ー',0x67:'\u3099',0x68:'\u309a',0x6A:'・',0x6B:'？',0x6C:'！',0x6D:'「',0x6E:'」'})
GLYPHS.update({0x70+i:str(i) for i in range(10)})
def sha(data): return hashlib.sha256(data).hexdigest()
def tokens(raw,kind):
    result=[];p=0
    while p<len(raw):
        b=raw[p];n=2 if b==0xFD and kind=='main' else 1
        if n==2: assert p+1<len(raw) and raw[p+1]>0
        name=('spaces' if b==0xFD else 'newline' if b==0xFE else 'end' if b==0xFF
            else 'variable_F8' if b==0xF8 else 'variable_F9' if b==0xF9 else 'variable_FA' if b==0xFA
            else 'macro' if 0x80<=b<=0x88 else 'tile')
        assert name!='tile' or b<0x7F, f'Unclassified code {b:02X}'
        token=(f'{{spaces:{raw[p+1]:02X}}}' if n==2 else f'{{macro:{b:02X}}}' if name=='macro'
            else f'{{tile:{b:02X}}}' if name=='tile' else '{'+name+'}')
        result.append({'relative_offset':p,'raw_hex':raw[p:p+n].hex(' ').upper(),'name':name,'token':token})
        p+=n
    assert bytes.fromhex(' '.join(t['raw_hex'] for t in result))==raw
    return result
def view(ts,profile):
    parts=[]
    for t in ts:
        b=int(t['raw_hex'].split()[0],16)
        if t['name']=='tile': parts.append(GLYPHS.get(b,t['token']) if profile=='kana_partial' else t['token'])
        elif t['name']=='newline': parts.append('\n')
        elif t['name']=='spaces': parts.append(' '*int(t['raw_hex'].split()[1],16))
        elif t['name']!='end': parts.append(t['token'])
    return unicodedata.normalize('NFC',''.join(parts))
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--initialize-translation',action='store_true')
    a=ap.parse_args()
    m=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    data=(ROOT/m['path']).read_bytes()
    assert sha(data)==m['sha256'] and len(data)==m['size_bytes']
    # Known consumer instructions, bank-relative mapping verified by Mesen trace.
    assert data[0x5440:0x5443]==bytes.fromhex('B9 99 95')
    assert data[0x5448:0x544B]==bytes.fromhex('B9 9A 95')
    assert data[0x53A3:0x53A5]==bytes.fromhex('B1 06')
    assert data[0x5361:0x5364]==bytes.fromhex('BD A1 A1')
    assert data[0x5370:0x5372]==bytes.fromhex('B1 06')
    specs=[('main',0x55A9,48,0x5609,0x5A28),('macro',0x61B1,9,0x61C3,0x61FF)]
    units=[];tables=[]
    for kind,table,count,lo,hi in specs:
        slots=[];addresses={}
        for i in range(count):
            p=table+2*i;ptr=int.from_bytes(data[p:p+2],'little');start=ptr-0x3FF0
            assert lo<=start<hi
            end=data.index(255,start,hi)+1
            addresses.setdefault(start,[]).append(i if kind=='main' else 0x80+i)
            slots.append({'index':i,'code':None if kind=='main' else 0x80+i,'pointer_file_offset':p,
                'cpu_pointer':ptr,'target_file_offset':start,'unit_id':f'{kind.upper()}_{start:05X}'})
        covered=set()
        for start,ids in sorted(addresses.items()):
            end=data.index(255,start,hi)+1;raw=data[start:end];ts=tokens(raw,kind)
            owned=set(range(start,end));assert not covered.intersection(owned)
            covered.update(owned)
            profile='credits_unresolved' if kind=='main' and any(i>=45 for i in ids) else 'kana_partial'
            units.append({'entry_id':f'{kind.upper()}_{start:05X}','kind':kind,'reference_ids':','.join(f'{i:02X}' for i in ids),
                'file_offset':start,'end_exclusive':end,'font_profile':profile,'original_view':view(ts,profile),
                'source_tokens':''.join(t['token'] for t in ts),'raw_hex':raw.hex(' ').upper(),
                'raw_sha256':sha(raw),'tokens':ts,'source_sha256':m['sha256']})
        assert covered==set(range(lo,hi)),f'Unclaimed bytes in {kind} extent'
        rebuilt=b''.join(bytes.fromhex(u['raw_hex']) for u in units if u['kind']==kind)
        assert rebuilt==data[lo:hi]
        ptr_rebuild=b''.join(s['cpu_pointer'].to_bytes(2,'little') for s in slots)
        assert ptr_rebuild==data[table:table+count*2]
        tables.append({'kind':kind,'pointer_start':table,'pointer_end_exclusive':table+count*2,'slots':slots,
            'pointer_slots':count,'unique_targets':len(addresses),'data_start':lo,'data_end_exclusive':hi,
            'data_bytes':hi-lo,'data_and_pointer_roundtrip':'PASS'})
    out=a.output.resolve()
    assert out!=ROOT/'original' and ROOT/'original' not in out.parents
    out.mkdir(parents=True,exist_ok=False)
    report={'source_sha256':m['sha256'],'main_pointer_slots':48,'main_unique_targets':46,
        'macro_pointer_slots':9,'macro_unique_targets':8,'unique_units':len(units),
        'main_data_bytes':tables[0]['data_bytes'],'macro_data_bytes':tables[1]['data_bytes'],
        'pointer_bytes':sum(t['pointer_slots']*2 for t in tables),'roundtrip':'PASS',
        'population_status':'Exact for these registered contiguous tables; global text population unresolved',
        'glyph_view_status':'Partial kana map only; unknown tiles are retained. Credits font profile unresolved.',
        'scope':'Reversible original extraction only; no Korean insertion, no all-scene runtime proof'}
    payload={'report':report,'tables':tables,'units':units,'partial_kana_glyphs':{f'{k:02X}':v for k,v in GLYPHS.items()}}
    (out/'text_tokens.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'extraction_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['entry_id','kind','reference_ids','file_offset','end_exclusive','font_profile','original_view','source_tokens','raw_hex','raw_sha256','source_sha256']
    with (out/'original_text.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:u[k] for k in fields} for u in units)
    if a.initialize_translation:
        target=ROOT/'workspace/translation/text_ja.csv'
        assert not target.exists(),'Translation SSOT already exists; do not overwrite'
        with target.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields+['scene','speaker','translation_ko','status','notes']);w.writeheader()
            w.writerows({**{k:u[k] for k in fields},'status':'untranslated',
                'notes':'Partial glyph view; raw tokens authoritative. Verify scene/profile before translation.'} for u in units)
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
