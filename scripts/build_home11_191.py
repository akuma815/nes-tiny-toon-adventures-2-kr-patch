"""054 opening053 plus one home0A11px; source-composed development candidate."""
from pathlib import Path
import argparse,csv,json
from PIL import Image,ImageFont,ImageDraw
from asm6502 import assemble
from extract_title_png import encode,decode
from dialogue_ips import make,apply
from seal_nonplay171 import R,sha

WRAPPER='''
    PHA
    LDA $18
    CMP #$08
    BNE @fallback
    LDA $06CF
    CMP #$0A
    BNE @fallback
    LDA $C6
    CMP #$82
    BNE @fallback
    LDA $06CD
    CMP #$31
    BNE @fallback
    LDA $06CE
    CMP #$97
    BNE @fallback
    PLA
    LDA #$08
    JSR $FDD3
    JSR $9800
    PHP
    PHA
    JSR $FDDB
    PLA
    PLP
    RTS
fallback:
    PLA
    JMP $93E1
'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();out=args.output.resolve();out.relative_to(R/'build');assert not out.exists()
    prior=R/'build/opening11_poc_053';source=R/'original/rom/Tiny Toon Adventures 2 - Montana Land e Youkoso (Japan).nes';src=source.read_bytes();old=(prior/'TinyToon2_Opening11_PoC053.nes').read_bytes();new=bytearray(old)
    assert sha(source)=='f41607b80904a2e1150a155121405dd1fed007ce98ff00a274a7891cafd7e32d'
    assert sha(prior/'TinyToon2_Opening11_PoC053.nes')=='d27a78ddfd0f8b3d6d46bf1b9db85dbd1d1051bde99ea7eb65a46c5656b53e3c'
    rows={r['entry_id']:r for r in csv.DictReader((R/'workspace/translation/text_ja.csv').open(encoding='utf-8-sig'))};row=rows['MAIN_05741'];assert row['translation_ko']=='자, 어디로 갈까?' and row['status']=='draft'
    fontpath=R/'workspace/fonts/galmuri11_candidate185/Galmuri11.ttf';assert sha(fontpath)=='e24256f42e43713d2ea086a1e1669d78b968f5b3cc547e5c157f0606ffa5def1'
    face=ImageFont.truetype(str(fontpath),12);text=row['translation_ko'];assert len(text)<=14
    im=Image.new('L',(168,16));d=ImageDraw.Draw(im);left=(168-len(text)*12)//2
    for x,c in enumerate(text):
        glyph=Image.new('L',(16,16));ImageDraw.Draw(glyph).text((0,-1),c,font=face,fill=2);assert c.isspace() or glyph.getbbox()
        d.text((left+x*12,-1),c,font=face,fill=2)
    assert set(im.get_flattened_data())<={0,2}
    slots={bytes(64):0};font=bytearray(2048);codes=[[],[]];body=bytearray()
    for x in range(21):
        for half in range(2):
            bits=bytes(im.crop((x*8,half*8,x*8+8,half*8+8)).get_flattened_data())
            if bits not in slots:
                code=len(slots);assert code<128;slots[bits]=code;raw=encode(bits);assert decode(raw)==bits;font[16*code:16*code+16]=raw
            code=slots[bits];codes[half].append(code);body.append(code)
    body.append(255);assert len(body)==43
    opening=json.loads((prior/'opening11_plan.json').read_text('utf-8'));stream=max(z['stream_pointer']+len(bytes.fromhex(z['body_hex'])) for z in opening['pages']);assert stream+len(body)<0xa000
    def cpuput(bank,pc,data):
        p=16+bank*8192+pc-0x8000;new[p:p+len(data)]=data;return [p,p+len(data)]
    wrapper,listing,symbols=assemble(WRAPPER,0x9630);assert 0x9630+len(wrapper)<=0x9700
    ranges=[cpuput(18,0x9630,wrapper),cpuput(8,0x9630,wrapper)]
    for bank in (18,8):
        p=16+bank*8192+0x9c81-0x8000;assert old[p:p+3]==bytes.fromhex('20 e1 93');ranges.append(cpuput(bank,0x9c81,bytes.fromhex('20 30 96')))
    ranges.append(cpuput(8,0x9914,stream.to_bytes(2,'little')));ranges.append(cpuput(8,stream,body))
    bank=old[0x5710+20];assert bank==130
    fontoff=0x40010+bank*1024;new[fontoff:fontoff+2048]=font;ranges.append([fontoff,fontoff+2048])
    diffs=[i for i,(a,b) in enumerate(zip(old,new)) if a!=b];assert all(any(lo<=i<hi for lo,hi in ranges) for i in diffs)
    assert new[:16]==old[:16] and new[0x3e010:0x40010]==old[0x3e010:0x40010]
    for z in opening['pages']:
        off=z['font_file_offset'];assert new[off:off+2048]==old[off:off+2048]
        p=0x10010+z['stream_pointer']-0x8000;assert new[p:p+len(bytes.fromhex(z['body_hex']))]==old[p:p+len(bytes.fromhex(z['body_hex']))]
    writes=json.loads((prior/'expected_writes.json').read_text('utf-8'));model=bytearray(src);owned=set()
    for w in writes:
        p,n=w['file_offset'],w['length'];area=set(range(p,p+n));assert not area&owned;owned|=area;assert src[p:p+n]==bytes.fromhex(w['expected_hex']);w['final_hex']=bytes(new[p:p+n]).hex();model[p:p+n]=bytes.fromhex(w['final_hex'])
    assert model==new and apply(src,make(src,bytes(new)))==new
    out.mkdir();name='TinyToon2_Home11_Candidate054';(out/(name+'.nes')).write_bytes(new);(out/(name+'.ips')).write_bytes(make(src,bytes(new)))
    page={'page':10,'root':8,'entry_id':row['entry_id'],'text':text,'original_pointer':0x9731,'font_bank':130,'font_file_offset':fontoff,'font_hex':font.hex(),'font_unique_tiles':len(slots),'stream_pointer':stream,'body_hex':body.hex(),'NT_top_origin':0x22a8,'NT_rows':codes,'width_pixels':168,'tile_columns':21,'cell':[12,16],'wrapper_PC':0x9630,'wrapper_listing':listing,'wrapper_symbols':symbols,'allowed_ranges_vs053':ranges,'native_clear':{'origin':0x22a7,'width_tiles':22,'rows':5,'init_PC':0x920a,'step_PC':0x919a},'home_root_evidence':'qa/dialogue/opening11_187_train053/frame_00930_ram.bin'}
    report={'work':191,'source_sha256':sha(source),'prior053_sha256':sha(prior/'TinyToon2_Opening11_PoC053.nes'),'output_sha256':sha(out/(name+'.nes')),'output_size':len(new),'output_rom':name+'.nes','IPS_sha256':sha(out/(name+'.ips')),'CSV_sha256':sha(R/'workspace/translation/text_ja.csv'),'modified_bytes_vs053':len(diffs),'selected_entry':row['entry_id'],'opening9_font_stream_and_callers_unchanged':True,'fixedIRQ_header_unchanged':True,'runtime':'NOT_RUN; candidate not adopted or packaged','scope':'053opening11px plus only nativehome0A11px. Actualhomefield/cursor/clear/font life pending user/tailored runtime review; stable051 andtested053 unchanged.'}
    for n,v in [('home11_plan.json',page),('expected_writes.json',writes),('build_report.json',report)]: (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')
    (out/'builder_used.py').write_bytes(Path(__file__).read_bytes());(out/'translation_used.csv').write_bytes((R/'workspace/translation/text_ja.csv').read_bytes());im.save(out/'home11_static_indices.png');print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
