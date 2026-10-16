"""Build title003 plus MAIN_05609 draft through native parser and cloned font banks."""
import argparse,csv,hashlib,json,sys
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw,__version__ as pillow_version
from extract_title_png import decode,encode
ROOT=Path(__file__).resolve().parents[1]
FONT_SHA='a2be473e22a62942164c95db60f3f5aa88a99f76b525994d194e9f5f9df387ea'
TTF_SHA='3882bd35066c26b0392cd4963ff9b3c151041dec34adc9d5633d137d1d9b9855'
TITLE_SHA='d7e8870c98909339486ae6448346d6ba2c65dbaacbe7861fab05bbe35ad8737a'
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    manifest=json.loads((ROOT/'manifests/source_rom.json').read_text(encoding='utf-8'))
    source=(ROOT/manifest['path']).read_bytes();assert sha(source)==manifest['sha256'] and len(source)==0x40010
    title_dir=ROOT/'build/title_kr_ai_003';title=(title_dir/'TinyToon2_title_kr_poc.nes').read_bytes();assert sha(title)==TITLE_SHA
    writes=json.loads((title_dir/'expected_writes.json').read_text(encoding='utf-8'))
    for w in writes:w['owner']='preserved_'+w['owner']
    check=bytearray(source)
    for w in writes:
        p=w['file_offset'];n=w['length'];assert source[p:p+n]==bytes.fromhex(w['expected_hex']);check[p:p+n]=bytes.fromhex(w['final_hex'])
    assert bytes(check)==title
    csv_path=ROOT/'workspace/translation/text_ja.csv';rows=list(csv.DictReader(csv_path.open(encoding='utf-8-sig',newline='')))
    row=next(v for v in rows if v['entry_id']=='MAIN_05609');text=row['translation_ko'];lines=text.split('\n')
    assert row['status']=='draft' and len(lines)==2,'Explicit single-draft development policy only'
    assert row['raw_hex']==source[0x5609:0x5625].hex(' ').upper()
    catalog=json.loads((ROOT/'extracted/text/table_20261004_001/text_tokens.json').read_text(encoding='utf-8'))
    used={int(t['raw_hex'],16) for u in catalog['units'] for t in u['tokens'] if t['name']=='tile'}
    pool=[v for v in range(1,0x70) if v not in used]
    assert pool==[0x17,0x1e,0x21,0x36,0x38,0x3e,0x41,0x42,0x45,0x4a,0x54,0x62,0x69,0x6f]
    chars=list(dict.fromkeys(c for c in text if c not in ' \n'))
    assert len(chars)<=len(pool),'PoC slot budget; choose page supply before scaling translation'
    assert 0x7a not in used
    # Literal blank remains nonzero/<7F, matching source glyph parser branches.
    mapping={' ':0x7a,**dict(zip(chars,pool))}
    fontdir=ROOT/'workspace/fonts/galmuri7_8x8';font_png=fontdir/'Galmuri7_8x8.png';ttf_path=fontdir/'Galmuri7.ttf'
    assert sha(font_png.read_bytes())==FONT_SHA and sha(ttf_path.read_bytes())==TTF_SHA
    sheet=Image.open(font_png).convert('RGBA');assert sheet.size==(512,1400)
    symbol=ImageFont.truetype(str(ttf_path),8)
    fonts=bytearray(source[0x36810:0x37010]);before=bytes(fonts);glyphs=[]
    fonts[0x7a*16:0x7b*16]=bytes(16)
    assert set(decode(before[16:32]))=={0,2}
    for c in chars:
        assert '\uac00'<=c<='\ud7a3',f'Unmapped Korean glyph {c!r}'
        i=ord(c)-0xac00;x=i%64*8;y=i//64*8;tile=sheet.crop((x,y,x+8,y+8))
        bits=[int(v[3]>0 and max(v[:3])>127) for v in tile.get_flattened_data()];assert any(bits)
        ttf_image=Image.new('L',(8,8));ImageDraw.Draw(ttf_image).text((0,-1),c,font=symbol,fill=255)
        assert bits==[int(v>127) for v in ttf_image.get_flattened_data()],f'Atlas Unicode mapping mismatch {c}'
        raw=encode(bytes(2*b for b in bits));assert decode(raw)==bytes(2*b for b in bits)
        code=mapping[c];fonts[code*16:(code+1)*16]=raw
        glyphs.append({'char':c,'code':code,'atlas_xy':[x,y],'chr_hex':raw.hex(),'ttf_matches_at_y_minus1':True})
    assert all(fonts[c*16:(c+1)*16]==before[c*16:(c+1)*16] for c in used)
    assert fonts[:16]==before[:16]
    # Preserve each native line's expanded tile count; trailing blank ticks maintain cutscene timing.
    old_unit=next(u for u in catalog['units'] if u['entry_id']=='MAIN_05609')
    original_counts=[];count=0
    for t in old_unit['tokens']:
        if t['name']=='tile':count+=1
        elif t['name']=='spaces':count+=int(t['raw_hex'].split()[1],16)
        elif t['name'] in ('newline','end'):original_counts.append(count);count=0
        else:raise ValueError('Unexpected first-paragraph control')
    assert original_counts==[18,17]
    body=bytearray();layout=[]
    for n,line in enumerate(lines):
        assert 0<len(line)<=24
        pad=(24-len(line))//2;original_prefix=(6,7)[n]
        extra_leading=pad-original_prefix;trailing=original_counts[n]-pad-len(line)
        assert trailing>=0,'Native first-paragraph timing/width budget'
        assert extra_leading>=0
        body.extend((0xfd,original_prefix));body.extend([0x7a]*extra_leading);body.extend(mapping[c] for c in line);body.extend([0x7a]*trailing);body.append(0xfe if n==0 else 0xff)
        layout.append({'text':line,'nametable_row':15+n*2,'origin_column':4,'leading_blanks':pad,'native_FD_prefix':original_prefix,'extra_literal_leading_blanks':extra_leading,'trailing_timing_blanks':trailing,'visible_start_column':4+pad,'expanded_tiles':pad+len(line)+trailing})
    assert len(body)==28
    payload=bytes(body)
    assert source[0x1fbde:0x1fbe7]==bytes.fromhex('A2 5A 8E 00 A0 E8 8E 08 A0')
    def write(owner,p,final):
        writes.append({'owner':owner,'file_offset':p,'length':len(final),'expected_hex':source[p:p+len(final)].hex(),'final_hex':final.hex()})
    write('chr_extent_128_to136_KiB',5,b'\x11')
    write('intro_irq_font_banks_128_129',0x1fbdf,b'\x80')
    write('MAIN_05609_fixed_slot',0x5609,payload)
    tail=bytes(fonts)+bytes(0x1800)
    writes.append({'owner':'cloned_font_banks_and_padding','file_offset':len(source),'length':len(tail),'expected_hex':'','final_hex':tail.hex(),'kind':'append','expected_source_size':len(source)})
    owned=set();output=bytearray(source)
    for w in writes:
        p=w['file_offset'];n=w['length'];region=set(range(p,p+n));assert not region&owned;owned|=region
        if w.get('kind')=='append':assert p==len(source) and w['expected_source_size']==len(source)
        else:assert source[p:p+n]==bytes.fromhex(w['expected_hex'])
        output[p:p+n]=bytes.fromhex(w['final_hex'])
    diffs={i for i,(v,z) in enumerate(zip(source,output)) if v!=z}|set(range(len(source),len(output)))
    assert diffs<=owned and len(output)==len(source)+8192
    # Native IRQ is the same LDX/STX/INX/STX sequence with a different immediate operand.
    assert output[0x1fbde:0x1fbe7]==bytes.fromhex('A2 80 8E 00 A0 E8 8E 08 A0')
    out=a.output.resolve();out.relative_to((ROOT/'build').resolve());out.mkdir(parents=True,exist_ok=False)
    (out/'TinyToon2_dialogue_kr_poc.nes').write_bytes(output)
    (out/'expected_writes.json').write_text(json.dumps(writes,indent=2)+'\n',encoding='utf-8')
    (out/'glyph_mapping.json').write_text(json.dumps({'mapping':mapping,'glyphs':glyphs,'scope':'Temporary PoC pool absent from registered source text only; graphic/other-scene sharing requires runtime QA'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    preview=Image.new('RGB',(256,240));draw=ImageDraw.Draw(preview)
    for spec in layout:
        for i,c in enumerate(spec['text']):
            raw=fonts[mapping[c]*16:(mapping[c]+1)*16];im=Image.new('L',(8,8));im.putdata([255 if v else 0 for v in decode(raw)])
            preview.paste(im.convert('RGB'),((spec['visible_start_column']+i)*8,spec['nametable_row']*8-4))
    preview.resize((1024,960),Image.Resampling.NEAREST).save(out/'dialogue_bitmap_preview_4x.png')
    report={'source_sha256':sha(source),'title_base_sha256':sha(title),'csv_sha256':sha(csv_path.read_bytes()),'output_sha256':sha(output),'output_rom':'TinyToon2_dialogue_kr_poc.nes','output_size':len(output),'entry_id':'MAIN_05609','text':text,'input_policy':'Development PoC permits this draft only; not release eligible','glyph_count':len(chars),'temporary_slot_pool':pool,'font_png_sha256':FONT_SHA,'ttf_sha256':TTF_SHA,'font_ink_pixel_value':2,'font_original_file_range':[0x36810,0x37010],'new_font_banks':[128,129],'new_font_file_range':[0x40010,0x40810],'appended_bytes':8192,'encoded_body_bytes':len(body),'native_slot_bytes':28,'line_layout':layout,'native_expanded_line_counts_preserved':True,'original_font_and_registered_source_glyphs_preserved':True,'expected_write_count':len(writes),'changed_bytes_including_append':len(diffs),'python':sys.version,'pillow':pillow_version,'runtime':'NOT YET RUN','scope':'Title003 plus one intro paragraph. Full-corpus capacity, active graphic sharing, and other font consumers remain unproven.'}
    (out/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('output_sha256','output_size','glyph_count','encoded_body_bytes','changed_bytes_including_append')},indent=2))
if __name__=='__main__':main()
